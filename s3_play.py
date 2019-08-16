import boto3
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

# 5. Get key enter from user
try:
	input = raw_input
except NameError:
	pass

input("\n[ Press enter to continue... ]")

# 6. Show bucket information
print('\n[ Now using Resource API ]\n')
s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(bucket_name)
obj = bucket.Object(object_key)
print('< Bucket name: {} >'.format(bucket.name))
print('< Object Key: {} >'.format(obj.key))
print('< Object content length: {} >'.format(obj.content_length))
print('< Object body: {} >'.format(obj.get()['Body'].read()))
print('< Object last modified: {} >'.format(obj.last_modified))

