import json
import os

app_file = os.environ.get('MARATHON_APP_FILE')

environment = os.environ.get('ENVIRONMENT')
image_name = os.environ.get('IMAGE_NAME')
image_tag = os.environ.get('IMAGE_TAG')
image = image_name + ':' + image_tag
memory = os.environ.get('MEMORY')
cpu_shares = os.environ.get('CPU_SHARES')
replicas = os.environ.get('REPLICAS')


with open(app_file) as data_file:
    data = json.load(data_file)

# image_info = data['container']['docker']['image']
# image = image_info.split(':')[0]
# image_info = image + ':' + version

data['container']['docker']['image'] = image
data['container']['env']['ENVIRONMENT'] = environment
data['cpus'] = cpu_shares
data['labels']['environment'] = environment
data['mem'] = memory
data['instances'] = replicas

with open(app_file, 'w') as outfile:
    json.dump(data, outfile, sort_keys = True, indent = 4)
