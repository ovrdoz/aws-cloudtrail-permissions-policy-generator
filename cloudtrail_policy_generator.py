import boto3, argparse, json
from datetime import datetime, timedelta

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate an IAM policy based on CloudTrail events.')
parser.add_argument('--service', dest='service_name', required=True,
                    help='The name of the AWS service to generate a policy for (e.g., "ec2", "s3", "lambda", etc.)')
parser.add_argument('--region', dest='region_name', required=True,
                    help='The AWS region to search for CloudTrail events in')
parser.add_argument('--hours', dest='hours_ago', type=int, default=2,
                    help='The number of hours to look back in the CloudTrail events (default is 2)')
args = parser.parse_args()

# Initialize CloudTrail client
client = boto3.client('cloudtrail', region_name=args.region_name)

# Calculate start time for CloudTrail lookup
start_time = datetime.utcnow() - timedelta(hours=args.hours_ago)

# Dictionary to store permissions by service
permissions_by_service = {}

# Paginate through CloudTrail events
for response in client.get_paginator('lookup_events').paginate(
        StartTime=start_time,
        EndTime=datetime.utcnow(),
        LookupAttributes=[
            {
                'AttributeKey': 'EventSource',
                'AttributeValue': f'{args.service_name}.amazonaws.com'
            }
        ]
):
    # Iterate through events and extract permissions
    for event in response['Events']:
        permission = event['EventName']
        if ":" in permission:
            service, action = permission.split(':')
        else:
            service = args.service_name
            action = permission
        permissions_by_service.setdefault(service, set()).add(action)

# Create policy statement
policy = {
    "Version": "2012-10-17",
    "Statement": []
}

# Iterate through permissions by service and add to policy statement
for service, actions in permissions_by_service.items():
    statement = {
        "Sid": "VisualEditor0",
        "Effect": "Allow",
        "Action": [f"{service}:{action}" for action in actions],
        "Resource": "*"
    }
    policy["Statement"].append(statement)

# Print policy in JSON format
print(f"last: {args.hours_ago}h")
print(f"service name filter: {args.service_name}")
print(json.dumps(policy, indent=4))
