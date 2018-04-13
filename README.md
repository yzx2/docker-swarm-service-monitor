# docker-swarm-service-monitor

## zabbix agent 配置文件中增加
UserParameter=dockerservice.discovery,/usr/bin/python /usr/local/zabbix/scripts/docker_low_discovery.py
UserParameter=dockerservice.status[*],/usr/bin/python /usr/local/zabbix/scripts/docker_service_monitor.py $1
UserParameter=ds[*],/usr/bin/python /usr/local/zabbix/scripts/get_service_stats.py $1 $2

## 创建docker service 在每个节点上都部署
docker service create -d --name get-container-stats \
    	--restart-max-attempts 5 \
    	--mode global \
    	--no-resolve-image=true \
    	--with-registry-auth \
    	-e Redis_host=x.x.x.x \
    	-e Redis_port=6379 \
    	-e Redis_pass=xxxx \
    	-e interval_time=300
    	--mount type=bind,source=/etc/localtime,target=/etc/localtime \
    	--mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock \
    	--mount type=bind,source=/sys/fs/cgroup,target=/sys/fs/cgroup \
    	get-container-stats:v1.0.2
