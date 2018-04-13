#!/usr/bin/python
# encoding: utf-8
import docker
import sys

ServiceName=sys.argv[1]
client = docker.DockerClient(base_url='unix://var/run/docker.sock',version='auto')

#根据服务名称获取docker service id
def get_service_id(ServiceName):
    Service_List=client.services.list(filters={'name':ServiceName})
    Service_Id=Service_List[0].id
    return Service_Id
#获取服务副本数量
def get_service_Replicas_num(Service_Id):
    service_attrs=client.services.get(Service_Id).attrs
    service_Spec=service_attrs['Spec']
    service_Mode=service_Spec['Mode']
    Replicas_num=service_Mode['Replicated']['Replicas']
    return Replicas_num
#获取运行中的服务task数量
def get_service_running_tasks_num(ServiceName):
    Service_Tasks=client.services.get(get_service_id(ServiceName)).tasks(filters={'name':ServiceName,'desired-state':'running'})
    return len(Service_Tasks)

def get_manager_nodes_num():
    Manager_nodes_list=client.nodes.list(filters={'role':'manager'})
    Manager_nodes_num=len(Manager_nodes_list)
    return Manager_nodes_num

def get_service_Mode(Service_Id):
    service_attrs=client.services.get(Service_Id).attrs
    service_Spec=service_attrs['Spec']
    service_Mode=service_Spec['Mode']

    return service_Mode.items()[0][0]

def get_service_status(ServiceName):
    if get_service_Mode(get_service_id(ServiceName)) ==  "Global":
        print ("%d.%d"%(get_service_running_tasks_num(ServiceName),get_manager_nodes_num()))
    else:
        print ("%d.%d"%(get_service_running_tasks_num(ServiceName),get_service_Replicas_num(get_service_id(ServiceName))))
get_service_status(ServiceName)

