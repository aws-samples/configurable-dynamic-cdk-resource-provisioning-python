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

from constructs import Construct
import os
import hashlib
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_s3 as s3,
    aws_sns_subscriptions as subs,
    RemovalPolicy as rp,
)

def create_hash(input):
        return hashlib.sha256(input.encode('utf-8')).hexdigest()[:12]

deploy_region = os.getenv('DEPLOY_REGION', os.getenv('CDK_DEFAULT_REGION', 'us-east-1'))
deploy_account = os.getenv('DEPLOY_ACCOUNT', os.getenv('CDK_DEFAULT_ACCOUNT', 'NO-ACCOUNT'))
app_name = os.getenv('applicationName', create_hash(deploy_account+deploy_region))
bucket_names=os.getenv('BUCKET_NAMES', 'bucket1,bucket2,bucket3')
number_of_queues = os.getenv('NUMBER_OF_QUEUES', 1)
queue_name = os.getenv('QUEUE_NAME', 'testqueue1')
comp_queue_names = app_name+"-"+queue_name


class ConfigurableDynamicCdkResourceProvisioningPythonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        for i in range(int(number_of_queues)):
            queue = sqs.Queue(self, comp_queue_names+str(i), queue_name=comp_queue_names+str(i))
            topic = sns.Topic(self, "Topic-"+ comp_queue_names+str(i), topic_name="Topic-"+ comp_queue_names+str(i))
            topic.add_subscription(subs.SqsSubscription(queue))
        
        
        for bucket_name in bucket_names.split(","):
            bucket_name = ((app_name)+"-"+bucket_name+"-"+deploy_region+"-"+create_hash(deploy_account)).lower()

            print('bucket name {0}'.format(bucket_name))
            bucket = s3.Bucket(
                self, 
                bucket_name, 
                bucket_name=bucket_name,
                removal_policy=rp.DESTROY
            )







