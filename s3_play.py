import boto3
import json
import uuid

s3_client = boto3.client('s3')

# 1. Make bucket name
# bucket name is generated by uuid.uuid4()
# uuid.uuid4() : generate uuid randomly
bucket_name = 'bob8th-sample-{}'.format(uuid.uuid4())
print('[ Creating new bucket with name: {} ]\n'.format(bucket_name))
s3_client.create_bucket(Bucket=bucket_name)

# 2. Make bucket list
list_buckets_resp = s3_client.list_buckets()
for bucket in list_buckets_resp['Buckets']:
	if bucket['Name'] == bucket_name:
		print('[ Just created ] -> {} - there since {} ]\n'.format(
			bucket['Name'], bucket['CreationDate']))

# 3. Reference a key file
object_key = 'some_information.txt'
print('[ Uploading some data to {} with key: {} ]\n'.format(bucket_name, object_key))
s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=b'KITRI BoB 8th!')

# 4. Make URL
url = s3_client.generate_presigned_url('get_object', {'Bucket':
bucket_name, 'Key': object_key})
print('[ Try this URL in your browser to download the object:')
print(url)
print(' ]')

# 5. Show bucket ACL
result = s3_client.get_bucket_acl(Bucket=bucket_name)
print(result)

# 6. Set a bucket policy
bucket_policy = {
	'Version': '2012-10-17',
	'Statement': [{
		'Sid': 'AddPerm',
		'Effect': 'Allow',
		'Principal': '*',
		'Action': ['s3:GetObject'],
		'Resource': "arn:aws:s3:::%s/*" % bucket_name }] }
bucket_policy = json.dumps(bucket_policy)
s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

# 7. Show bucket information
print('\n[ Now using Resource API ]\n')
s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(bucket_name)
obj = bucket.Object(object_key)
print('< Bucket name: {} >'.format(bucket.name))
print('< Object Key: {} >'.format(obj.key))
print('< Object content length: {} >'.format(obj.content_length))
print('< Object body: {} >'.format(obj.get()['Body'].read()))
print('< Object last modified: {} >'.format(obj.last_modified))

# 8. End Of Program
print('\n[ Done ]\n')
