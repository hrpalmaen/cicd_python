#!/usr/bin/env python3
import os

import aws_cdk as cdk

from app_cdk.app_cdk_stack import AppCdkStack
from app_cdk.pipeline_cdk_stack import PipelineCdkStack
from app_cdk.ecr_cdk_stack import EcrCdkStack

app = cdk.App()
# AppCdkStack(app, "AppCdkStack",
#     # If you don't specify 'env', this stack will be environment-agnostic.
#     # Account/Region-dependent features and context lookups will not work,
#     # but a single synthesized template can be deployed anywhere.

#     # Uncomment the next line to specialize this stack for the AWS Account
#     # and Region that are implied by the current CLI configuration.

#     #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

#     # Uncomment the next line if you know exactly what Account and Region you
#     # want to deploy the stack to. */

#     #env=cdk.Environment(account='123456789012', region='us-east-1'),

#     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#     )

ecr_stack = EcrCdkStack(
    app,
    'ecr-stack'
)

test_app_stack = AppCdkStack(
    app,
    'test-app-stack',
    ecr_repository = ecr_stack.ecr_data
)

prod_app_stack = AppCdkStack(
    app,
    'prod-app-stack',
    ecr_repository = ecr_stack.ecr_data
)

pipeline_stack = PipelineCdkStack(
    app,
    'pipeline-stack',
    ecr_repository = ecr_stack.ecr_data,
    test_app_fargate = test_app_stack.ecs_service_data,
    # prod_app_fargate = prod_app_stack.ecs_service_data,
    prod_app_fargate = prod_app_stack.ecs_service_data,
    green_target_group = prod_app_stack.green_target_group,
    green_load_balancer_listener = prod_app_stack.green_load_balancer_listener,
)

app.synth()
