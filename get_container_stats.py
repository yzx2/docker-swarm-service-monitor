#!/usr/bin/python
# encoding: utf-8
import docker,redis
import sys,time
import thread
import os

client = docker.DockerClient(base_url='unix://var/run/docker.sock',version='auto')
redis_host = os.environ["Redis_host"]
redis_port = os.environ["Redis_port"]
redis_pass = os.environ["Redis_pass"]
#获取数据间隔时间，单位秒
interval_time = os.environ['Interval_time']

R=redis.Redis(host=redis_host,port=redis_port,password=redis_pass)

id_list= client.containers.list(filters={'status':'running'})

def set_redis(k,v,ex=300):
    R.set(k,v)
def get_redis(k):
    return R.get(k)

def get_cpu_usage(container_id):
    #获取docker container 分配的内核个数
    fpre = open('/sys/fs/cgroup/cpuacct/docker/%s/cpuacct.usage_percpu' % container_id ,'r')
    pre_cpu = len(fpre.readlines()[0].split())
    fpre.close()
    
    f1 = open('/sys/fs/cgroup/cpuacct/docker/%s/cpuacct.usage' % container_id ,'r')
    cpu_usage1 = f1.readlines()[0]
    f1.close()

    fs1 = open('/proc/stat','r')
    list_fs=fs1.readlines()[0].split()
    fs1.close()
    sum_list1=0
    for i in list_fs:
	if i.isdigit():
	    sum_list1+=int(i)
	else:
	    pass
     
    time.sleep(1)

    f2 = open('/sys/fs/cgroup/cpuacct/docker/%s/cpuacct.usage' % container_id ,'r')
    cpu_usage2 = f2.readlines()[0]
    f2.close()    
    fs2 = open('/proc/stat','r')
    list_fs=fs2.readlines()[0].split()
    fs2.close()
    sum_list2=0
    for i in list_fs:
        if i.isdigit():
            sum_list2+=int(i)
        else:
            pass

    cpu_delta = int(cpu_usage2) - int(cpu_usage1)
    sys_cpu_delta = int(sum_list2) - int(sum_list1)
    	
    precent_cpu = format((((float(cpu_delta) / float(sys_cpu_delta)) / 10000000 * pre_cpu) * 100.0),'.2f')

    set_redis(container_id+'_precent_cpu',precent_cpu)
    print container_id+'_precent_cpu'+'----->'+get_redis(container_id+'_precent_cpu')
def get_mem_info(container_id):
    #获取系统内存总量，单位KB
    fsys_mem = open('/proc/meminfo', 'r')
    sys_mem = fsys_mem.readlines()[0].split()[1]

    fmem = open('/sys/fs/cgroup/memory/docker/%s/memory.usage_in_bytes' % container_id , 'r')
    mem_usage = fmem.readlines()[0].split()[0]
    f_limit_mem = open('/sys/fs/cgroup/memory/docker/%s/memory.limit_in_bytes' % container_id , 'r')
    limit_mem = f_limit_mem.readline().split()[0]
    if int(limit_mem) <> 9223372036854771712 :
	precent_mem = format(float(mem_usage) / float(limit_mem) *100 , '.2f')
    else:
	limit_mem = int(sys_mem)*1024   
	precent_mem = format((float(mem_usage) / 1024) / float(sys_mem) * 100 ,'.2f')
	
    set_redis(container_id+'_mem_usage',mem_usage)
    set_redis(container_id+'_limit_mem',limit_mem)
    set_redis(container_id+'_precent_mem',precent_mem)
    print container_id+'_mem_usage'+'----->'+get_redis(container_id+'_mem_usage')
    print container_id+'_limit_mem'+'----->'+get_redis(container_id+'_limit_mem')
    print container_id+'_precent_mem'+'----->'+get_redis(container_id+'_precent_mem')




num = 1
while num == 1:
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for i in id_list:
    	container_id = i.id
	get_mem_info(container_id)	
    	try:
    	    thread.start_new_thread(get_cpu_usage,(container_id,))
    	except:
    	    print "Error: unable to start thread"
    time.sleep(int(interval_time))
    



