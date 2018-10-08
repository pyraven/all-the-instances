import boto3
from tabulate import tabulate

# full region list
region_list = ["ap-south-1", "eu-west-3", "eu-west-2", "eu-west-1", "ap-northeast-2", "ap-northeast-1",
               "sa-east-1", "ca-central-1", "ap-southeast-1", "ap-southeast-2", "eu-central-1", "us-east-1",
               "us-east-2", "us-west-1", "us-west-2"]
instance_list = []

for region in region_list:
    try:
        ec2 = boto3.resource('ec2', region_name=region)
        filters = [
                {
                    'Name': 'instance-state-name',
                    'Values': ['running', 'stopped', 'pending', 'shutting-down', 'terminated', 'stopping']
                }
        ]
        instances = ec2.instances.filter(Filters=filters)
        for instance in instances:
            instance_tuple = (instance.private_ip_address, instance.public_ip_address, instance.state['Name'],
                              instance.instance_type, instance.key_name,
                              instance.image_id, instance.id, region)
            instance_list.append(instance_tuple)
    except Exception as e:
        print("Error %s during querying the %s region.".format(e, region))


headers = ["private_ip_address", "public_ip_address", "state", "instance_type",
           "key_pair_name", "image_id", "instance_id", "region"]

print(tabulate(instance_list, headers=headers))