#!/usr/bin/python

import boto3

swf = boto3.client('swf')

DOMAIN = "yourtestdomain"
WORKFLOW = "yourtestworkflow"
TASKNAME = "yourtaskname"
VERSION = "0.1"
TASKLIST = "testlist"

response = swf.start_workflow_execution(
  domain=DOMAIN,
  workflowId='test-1001',
  workflowType={
    "name": WORKFLOW,
    "version": VERSION
  },
  taskList={
      'name': TASKLIST
  },
  input=''
)

print "Workflow requested: ", response


