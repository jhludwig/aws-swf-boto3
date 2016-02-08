#!/usr/bin/python

import boto3
from botocore.client import Config
import uuid

botoConfig = Config(connect_timeout=50, read_timeout=70)
swf = boto3.client('swf', config=botoConfig)

DOMAIN = "yourtestdomain"
WORKFLOW = "yourtestworkflow"
TASKNAME = "yourtaskname"
VERSION = "0.1"
TASKLIST = "testlist"

print "Listening for Decision Tasks"

while True:

  newTask = swf.poll_for_decision_task(
    domain=DOMAIN,
    taskList={'name': TASKLIST},
    identity='decider-1',
    reverseOrder=False)

  if 'taskToken' not in newTask:
    print "Poll timed out, no new task.  Repoll"

  elif 'events' in newTask:

    eventHistory = [evt for evt in newTask['events'] if not evt['eventType'].startswith('Decision')]
    lastEvent = eventHistory[-1]

    if lastEvent['eventType'] == 'WorkflowExecutionStarted' and newTask['taskToken'] not in outstandingTasks:
      print "Dispatching task to worker", newTask['workflowExecution'], newTask['workflowType']
      swf.respond_decision_task_completed(
        taskToken=newTask['taskToken'],
        decisions=[
          {
            'decisionType': 'ScheduleActivityTask',
            'scheduleActivityTaskDecisionAttributes': {
                'activityType':{
                    'name': TASKNAME,
                    'version': VERSION
                    },
                'activityId': 'activityid-' + str(uuid.uuid4()),
                'input': '',
                'scheduleToCloseTimeout': 'NONE',
                'scheduleToStartTimeout': 'NONE',
                'startToCloseTimeout': 'NONE',
                'heartbeatTimeout': 'NONE',
                'taskList': {'name': TASKLIST},
            }
          }
        ]
      )
      print "Task Dispatched:", newTask['taskToken']

    elif lastEvent['eventType'] == 'ActivityTaskCompleted':
      swf.respond_decision_task_completed(
        taskToken=newTask['taskToken'],
        decisions=[
          {
            'decisionType': 'CompleteWorkflowExecution',
            'completeWorkflowExecutionDecisionAttributes': {
              'result': 'success'
            }
          }
        ]
      )
      print "Task Completed!"



