#!/usr/bin/env python3

# this script will take a parameter and based on the parameter it will use different code build command
# for Creating or updating the paramter should be create or update
# for deleting the parameter should be delete/destroy
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import aws_cdk as cdk
import os
import hashlib


from configurable_dynamic_cdk_resource_provisioning_python.configurable_dynamic_cdk_resource_provisioning_python_stack import ConfigurableDynamicCdkResourceProvisioningPythonStack

#  Create a HASH of a string. DO NOT USE THIS IN PRODUCTION. This is just for demo purposes.
#  This is used to create a unique name for the application stack so the stack can deployed multiple times. It is most important for S3 buckets as they must have a unique name.

def create_hash(input):
    return hashlib.sha256(input.encode('utf-8')).hexdigest()[:12]

deploy_region = os.getenv('DEPLOY_REGION', os.getenv('CDK_DEFAULT_REGION', 'us-east-1'))
deploy_account = os.getenv('DEPLOY_ACCOUNT', os.getenv('CDK_DEFAULT_ACCOUNT', 'NO-ACCOUNT'))
app_name = os.getenv('applicationName', create_hash(deploy_account+deploy_region))




app = cdk.App()
ConfigurableDynamicCdkResourceProvisioningPythonStack(app, app_name)

app.synth()
