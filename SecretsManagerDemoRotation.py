import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

secretsmanager_client = boto3.client('secretsmanager')

def lambda_handler(event, context):
    """
    Lambda function to rotate a secret (demo version without external service update).
    """
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        secret_arn = event["SecretId"]
        token = event["ClientRequestToken"]
        step = event["Step"]

        # Validate the secret ARN and token
        secret_metadata = secretsmanager_client.describe_secret(SecretId=secret_arn)
        if not secret_metadata.get('RotationEnabled'):
            raise ValueError("Secret rotation is not enabled for this secret.")

        versions = secret_metadata.get("VersionIdsToStages", {})
        if token not in versions or "AWSCURRENT" in versions[token]:
            raise ValueError("Client request token is not valid or already marked as AWSCURRENT.")

        # Process the rotation step
        if step == "createSecret":
            create_secret(secret_arn, token)
        elif step == "setSecret":
            set_secret(secret_arn, token)
        elif step == "testSecret":
            test_secret(secret_arn, token)
        elif step == "finishSecret":
            finish_secret(secret_arn, token)
        else:
            raise ValueError(f"Invalid step: {step}")
    except Exception as e:
        logger.error(f"Error in rotation process: {str(e)}")
        raise

def create_secret(secret_arn, token):
    """
    Create a new version of the secret.
    """
    try:
        current_secret = secretsmanager_client.get_secret_value(SecretId=secret_arn, VersionStage="AWSCURRENT")
        current_credentials = json.loads(current_secret["SecretString"])

        # Generate new credentials (example: new password)
        new_password = f"{current_credentials['password']}_ROTATED"

        # Store the new credentials
        new_secret_string = json.dumps({
            "username": current_credentials["username"],
            "password": new_password
        })
        secretsmanager_client.put_secret_value(
            SecretId=secret_arn,
            ClientRequestToken=token,
            SecretString=new_secret_string,
            VersionStages=["AWSPENDING"]
        )
        logger.info(f"Created new secret version for {secret_arn}.")
    except Exception as e:
        logger.error(f"Error creating secret: {str(e)}")
        raise

def set_secret(secret_arn, token):
    """
    Set the new credentials (placeholder for demo purposes).
    """
    try:
        logger.info(f"Setting new credentials for {secret_arn} (demo: no action taken).")
        # No action needed for the demo
    except Exception as e:
        logger.error(f"Error setting secret: {str(e)}")
        raise

def test_secret(secret_arn, token):
    """
    Test the new credentials (placeholder for demo purposes).
    """
    try:
        logger.info(f"Testing new credentials for {secret_arn} (demo: no action taken).")
        # No action needed for the demo
    except Exception as e:
        logger.error(f"Error testing secret: {str(e)}")
        raise

def finish_secret(secret_arn, token):
    """
    Finalize the rotation by marking the new secret as 'AWSCURRENT'.
    """
    try:
        # Get current secret versions
        secret_metadata = secretsmanager_client.describe_secret(SecretId=secret_arn)
        current_version = None

        # Identify the version ID currently marked as 'AWSCURRENT'
        for version_id, stages in secret_metadata["VersionIdsToStages"].items():
            if "AWSCURRENT" in stages:
                current_version = version_id
                break

        # Update stages to mark the new version as 'AWSCURRENT'
        secretsmanager_client.update_secret_version_stage(
            SecretId=secret_arn,
            VersionStage="AWSCURRENT",
            MoveToVersionId=token,
            RemoveFromVersionId=current_version
        )
        logger.info(f"Successfully marked version {token} as AWSCURRENT for {secret_arn}.")
    except Exception as e:
        logger.error(f"Error finishing secret: {str(e)}")
        raise