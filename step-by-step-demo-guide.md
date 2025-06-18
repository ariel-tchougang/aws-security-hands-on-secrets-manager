# AWS Secrets Manager Workshop - Step by Step Guide

This guide will walk you through a hands-on workshop with AWS Secrets Manager, demonstrating how to create, manage, and automatically rotate secrets.

## Part 1: Deploy CloudFormation Stack

1. Sign in to your AWS account and navigate to the CloudFormation console.

2. Click **Create stack** > **With new resources (standard)**.

3. Upload the `template.yaml` file from this repository and click **Next**.

4. Enter a stack name (e.g., `secrets-manager-workshop`).

5. For parameters:
   - Select your VPC ID
   - Select a public subnet ID
   - Optionally, specify a key pair name (or use the default)

6. Click **Next**, then **Next** again on the Configure stack options page.

7. Review the settings and click **Create stack**.

8. Wait for the stack creation to complete (typically 2-3 minutes).

## Part 2: Set Up an EC2 Instance (Optional)

You can run this workshop from AWS CloudShell, your local machine, or an EC2 instance. If you prefer using an EC2 instance, follow these steps:

1. Navigate to the EC2 console and click **Launch instance**.

2. Configure your instance:
   - Name: `secrets-manager-workshop-instance`
   - AMI: Amazon Linux 2023
   - Instance type: t2.micro
   - Key pair: Select the key pair created by CloudFormation or use an existing one
   - Network settings:
     - VPC: Select the same VPC you used in the CloudFormation template
     - Subnet: Select the public subnet you specified in the CloudFormation template
     - Auto-assign public IP: Enable
     - Security group: Select the security group created by CloudFormation (named `SecretsManagerWorkshopSG`)
   - Advanced details:
     - IAM instance profile: Select `SecretsManagerWorkshopInstanceProfile`
     - User data: Copy and paste the contents of the `user-data.sh` file from this repository

3. Click **Launch instance**.

4. Connect to your instance using SSH or EC2 Instance Connect:
   
   Using SSH:
   ```
   ssh -i /path/to/your-key.pem ec2-user@your-instance-public-ip
   ```
   
   Or use EC2 Instance Connect from the AWS Console.

5. Verify AWS CLI is installed and configured:
   ```
   aws --version
   ```

6. If you didn't use the user-data script or need to manually install jq:
   ```
   sudo yum install -y jq
   ```

## Part 3: Create and Manage Secrets

1. Create a secret with username and password:
   ```
   aws secretsmanager create-secret \
       --name WorkshopSecret \
       --description "Secret used for AWS Secrets Manager workshop" \
       --secret-string '{"username":"admin","password":"MySecurePassword123"}'
   ```

2. Retrieve the secret value:
   ```
   aws secretsmanager get-secret-value --secret-id WorkshopSecret
   ```

3. Update the secret value:
   ```
   aws secretsmanager put-secret-value \
       --secret-id WorkshopSecret \
       --secret-string '{"username":"admin","password":"UpdatedPassword456"}'
   ```

4. Verify the updated secret value:
   ```
   aws secretsmanager get-secret-value --secret-id WorkshopSecret
   ```

5. Describe the secret to see its metadata:
   ```
   aws secretsmanager describe-secret --secret-id WorkshopSecret
   ```

## Part 4: Create Lambda Rotation Function

1. Navigate to the Lambda console and click **Create function**.

2. Configure the function:
   - Function name: `SecretsManagerWorkshopRotation`
   - Runtime: Python 3.11
   - Architecture: x86_64
   - Execution role: Use an existing role
   - Existing role: Select the `SecretsManagerWorkshopLambdaRole` created by CloudFormation

3. Click **Create function**.

4. In the Code source section, replace the default code with the contents of `SecretsManagerDemoRotation.py`.

5. Click **Deploy** to save the function.

6. Add a resource-based policy to allow Secrets Manager to invoke the function:
   - Go to the **Configuration** tab
   - Click on **Permissions**
   - Scroll down to **Resource-based policy statements** and click **Add permissions**
   - Select **AWS Service** and choose **Secrets Manager**
   - For **Statement ID**, enter `SecretsManagerRotationPermission`
   - For **Principal**, enter `secretsmanager.amazonaws.com`
   - For **Action**, enter `lambda:InvokeFunction`
   - Click **Save**

## Part 5: Set Up Secret Rotation

1. Configure automatic rotation for your secret:
   ```
   aws secretsmanager rotate-secret \
       --secret-id WorkshopSecret \
       --rotation-lambda-arn "arn:aws:lambda:REGION:ACCOUNT_ID:function:SecretsManagerWorkshopRotation" \
       --rotation-rules '{"AutomaticallyAfterDays": 30}'
   ```
   Replace `REGION` and `ACCOUNT_ID` with your AWS region and account ID.

2. Trigger an immediate rotation:
   ```
   aws secretsmanager rotate-secret --secret-id WorkshopSecret
   ```

3. Verify the rotated secret value:
   ```
   aws secretsmanager get-secret-value --secret-id WorkshopSecret
   ```
   Notice that the password now has "_ROTATED" appended to it.

4. Describe the secret to see rotation information:
   ```
   aws secretsmanager describe-secret --secret-id WorkshopSecret
   ```

## Part 6: Clean Up Resources

1. Delete the secret:
   ```
   aws secretsmanager delete-secret \
       --secret-id WorkshopSecret \
       --force-delete-without-recovery
   ```

2. Delete the Lambda function (optional):
   ```
   aws lambda delete-function --function-name SecretsManagerWorkshopRotation
   ```

3. Terminate the EC2 instance if you created one.

4. Delete the CloudFormation stack:
   - Navigate to the CloudFormation console
   - Select your stack
   - Click **Delete** and confirm the deletion

## Bonus: Creating a Helper Script for Secret Retrieval

Create a helper script to extract and use secret values:

```bash
cat<<'EOF'>> get-secret.sh
#!/bin/bash

# Check if jq is installed
if ! command -v jq &> /dev/null; then
  echo "jq is not installed. Installing now..."
  sudo yum install -y jq || sudo apt-get install -y jq
  
  if [ $? -ne 0 ]; then
    echo "Failed to install jq. Please install it manually."
    exit 1
  fi
fi

getsecretvalue() {
  aws secretsmanager get-secret-value --secret-id $1 | \
    jq .SecretString | \
    jq fromjson
}

if [ -z "$1" ]; then
  echo "Usage: $0 <secret-name>"
  exit 1
fi

secret=$(getsecretvalue $1)

user=$(echo $secret | jq -r .username)
password=$(echo $secret | jq -r .password)

echo "Username: $user"
echo "Password: $password"

# If your secret contains database connection info, uncomment these lines
# endpoint=$(echo $secret | jq -r .host)
# port=$(echo $secret | jq -r .port)
# echo "Host: $endpoint"
# echo "Port: $port"
EOF

chmod +x get-secret.sh
```

Use the script:
```
./get-secret.sh WorkshopSecret
```

## Conclusion

Congratulations! You've completed the AWS Secrets Manager workshop. You've learned how to:
- Create and manage secrets
- Update secret values
- Set up automatic rotation with Lambda
- Retrieve and use secret values programmatically

For more information, visit the [AWS Secrets Manager documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html).