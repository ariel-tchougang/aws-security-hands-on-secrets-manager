#!/bin/bash
# Install required packages
yum update -y
yum install -y jq

# Create a welcome message
cat > /etc/motd << EOF
=======================================================
Welcome to the AWS Secrets Manager Workshop!
=======================================================
This instance has been configured with:
- AWS CLI
- jq (for JSON processing)

All necessary permissions are attached via the instance profile.
EOF

echo "Installation complete!"