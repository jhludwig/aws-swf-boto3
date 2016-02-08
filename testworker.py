#!/usr/bin/python

import boto3
from botocore.client import Config

botoConfig = Config(connect_timeout=50, read_timeout=70)
swf = boto3.client('swf', config=botoConfig)

DOMAIN = "yourtestdomain"
WORKFLOW = "yourtestworkflow"
TASKNAME = "yourtaskname"
VERSION = "0.1"
TASKLIST = "testlist"

print "Listening for Worker Tasks"

while True:

  task = swf.poll_for_activity_task(
    domain=DOMAIN,
    taskList={'name': TASKLIST},
    identity='worker-1')

  if 'taskToken' not in task:
    print "Poll timed out, no new task.  Repoll"

  else:
    print "New task arrived"

    swf.respond_activity_task_completed(
        taskToken=task['taskToken'],
        result='success'
    )

    print "Task Done"


