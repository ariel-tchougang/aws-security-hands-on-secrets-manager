# AWS Secrets Manager Workshop

This repository contains resources for a hands-on workshop on AWS Secrets Manager. The workshop is designed to be completed in under 20 minutes and demonstrates key features of AWS Secrets Manager using the AWS CLI.

## Workshop Overview

In this workshop, you will:

1. Deploy a CloudFormation stack with necessary IAM roles and security groups
2. Create and manage secrets in AWS Secrets Manager
3. Update secret values
4. Set up and test automatic secret rotation using a Lambda function

## Prerequisites

- AWS account with permissions to create IAM roles, EC2 instances, and Lambda functions
- AWS CLI installed and configured (or access to AWS CloudShell)
- Basic knowledge of AWS services and command line operations

## Getting Started

1. Clone this repository
2. Deploy the CloudFormation template
3. Follow the instructions in [step-by-step-demo-guide.md](step-by-step-demo-guide.md)

## Repository Contents

- `template.yaml`: CloudFormation template for deploying workshop resources
- `SecretsManagerDemoRotation.py`: Lambda function code for secret rotation
- `step-by-step-demo-guide.md`: Detailed instructions for the workshop

## Security Note

This workshop is for educational purposes only. In a production environment, you should follow AWS security best practices, including:

- Limiting IAM permissions to the minimum required
- Restricting network access to resources
- Using more complex secret rotation strategies
- Implementing proper secret access controls

## License

This project is licensed under the MIT License - see the LICENSE file for details.