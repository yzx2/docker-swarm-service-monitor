#!/usr/bin/python
# encoding: utf-8
import docker
import sys,os,time
import redis

ServiceName=sys.argv[1]
Item=sys.argv[2]

client = docker.DockerClient(base_url='unix://var/run/docker.sock',version='auto')
R=redis.Redis(host='10.10.6.192',port=6379,password='sqbj@123')

def set_redis(k,v):
    R.set(k,v)
def get_redis(k):
    return R.get(k)
#根据服务名称获取docker service id
def get_service_id(ServiceName):
    Service_List=client.services.list(filters={'name':ServiceName})
    Service_Id=Service_List[0].id
    return Service_Id

#获取service tasks 在每个节点上的container id list
def get_service_task_container_id(ServiceName):
    Service_Tasks=client.services.get(get_service_id(ServiceName)).tasks(filters={'name':ServiceName,'desired-state':'running'})
    task_container_id_list=[]
    for task in Service_Tasks:
        task_container_id=task['Status']['ContainerStatus']['ContainerID']
	task_container_id_list.append(task_container_id)
    return  task_container_id_list

def get_cpu(ServiceName):
    container_id_list = get_service_task_container_id(ServiceName)
    precent_cpu_list=[]
    for container_id in  container_id_list:
	precent_cpu_list.append(float(get_redis(container_id+'_precent_cpu')))
    return precent_cpu_list

def get_precent_mem(ServiceName):
    container_id_list = get_service_task_container_id(ServiceName)
    precent_mem_list=[]
    for container_id in  container_id_list:
        precent_mem_list.append(float(get_redis(container_id+'_precent_mem')))
    return precent_mem_list

def get_usage_mem(ServiceName):
    container_id_list = get_service_task_container_id(ServiceName)
    usage_mem_list=[]
    for container_id in  container_id_list:
        usage_mem_list.append(int(get_redis(container_id+'_mem_usage')))
    return usage_mem_list    

def get_limit_mem(ServiceName):
    container_id_list = get_service_task_container_id(ServiceName)
    limit_mem_list=[]
    for container_id in  container_id_list:
        limit_mem_list.append(int(get_redis(container_id+'_limit_mem')))
    return limit_mem_list    
    

if Item == "max_cpu":
    print max(get_cpu(ServiceName))
elif Item == "min_cpu":
    print min(get_cpu(ServiceName))
elif Item == "avg_cpu":
    print format((sum((get_cpu(ServiceName)))/len(get_cpu(ServiceName))),'.2f')
elif Item == "max_precent_mem":
    print max(get_precent_mem(ServiceName))
elif Item == "min_precent_mem":
    print min(get_precent_mem(ServiceName))
elif Item == "avg_precent_mem":
    print format((sum((get_precent_mem(ServiceName)))/len(get_precent_mem(ServiceName))),'.2f')
elif Item == "max_usage_mem":
    print max(get_usage_mem(ServiceName))
elif Item == "min_usage_mem":
    print min(get_usage_mem(ServiceName))
elif Item == "avg_usage_mem":
    print (sum((get_usage_mem(ServiceName)))/len(get_usage_mem(ServiceName)))
elif Item == "limit_mem":
    print min(get_limit_mem(ServiceName))
else:
    print "xxxxx"




