#/usr/bin/env python
# -*- coding:utf-8 -*-
#zabbix low discovery
#550779638@qq.com
import docker
import json


client = docker.DockerClient(base_url='unix://var/run/docker.sock',version='auto')

Service_List=client.services.list()

data_list=[]
for i in Service_List:
    data_list.append({'{#SERVICENAME}':i.name})

jdata_list=json.dumps({'data':data_list},indent=4,separators=(',',':'))
print jdata_list
