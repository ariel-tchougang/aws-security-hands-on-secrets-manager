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