# CloudTrail Permissions Policy Generator

This Python script generates an AWS IAM policy based on the permissions recorded in the AWS CloudTrail service for a specified service in the past few hours. The generated policy can be used to grant the necessary permissions for that service to an IAM role or user.

## Requirements

To use this script, you must have AWS credentials configured on your machine or specify them using environment variables. You can use the **`aws configure`** command to set up your credentials or export them as environment variables:

```
export AWS_ACCESS_KEY_ID=<your_access_key>
export AWS_SECRET_ACCESS_KEY=<your_secret_key>
export AWS_DEFAULT_REGION=<your_aws_region>

```

You must also have the **`boto3`** Python package installed. You can install it using pip:

```
pip3 install boto3

```

## Usage

To use this script, simply run the **`cloudtrail_policy_generator.py`** file and specify the following arguments:

- **`-service`**: The name of the AWS service to generate a policy for (e.g., "ec2", "s3", "lambda", etc.).
- **`-region`**: The AWS region to search for CloudTrail events in.
- **`-hours`**: The number of hours to look back in the CloudTrail events (default is 2).

Example usage:

```
python3 cloudtrail_policy_generator.py --service eks --region us-east-1 --hours 3

```

This will generate an IAM policy for the "eks" service in the "us-east-1" region based on the CloudTrail events from the past 3 hours.

The generated policy will be printed to the console in JSON format, so you can copy and paste it into your AWS IAM console or include it in your infrastructure as code.

## Note

This script generates a policy based on the CloudTrail events recorded for the specified service in the past few hours. However, it is important to review and test the generated policy before applying it to your IAM roles or users to ensure that it grants the necessary permissions without being overly permissive. Always follow the principle of least privilege when granting permissions to IAM entities.