# Ensure CPU / memory limitations on notebook spawned by DockerSpawner

We use a machine learning algorithm with keras / tensorflow to stress the container's system and limit ressources, both CPU and memory, through jupyterhub configuration. 

First, pull tensorflow notebook image from [jupyter/docker-stacks](https://github.com/jupyter/docker-stacks) :

    docker pull jupyter/tensorflow-notebook

And, run 'jupyterhub' from your python install :

    jupyterhub

Loggin with a user '{username}' (from your host PAM), so a container 'jupyter-{username}' is spawned. Then copy the notebook file 'mnist.ipynb' in the home on the running container :

    docker cp notebook/mnist.ipynb jupyter-{username}:/home/jovyan/work

Note the file must be copy every shutdown of server.

Last, run the notebook and fit the model. It will consume ressources on container, use docker stats to check :

    CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT     MEM %
    ddf90face1f2        jupyter-desrozis    509.04%             529.5MiB / 3.702GiB   13.97%

To ensure limitation on memory, for instance 1Go memory maximum dedicated to the container :

    c.DockerSpawner.extra_host_config = {
        'mem_limit': '1g'
    }

and :

    CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT   MEM %
    0fb8386ca5bf        jupyter-desrozis    0.00%               49.11MiB / 1GiB     4.80%

To ensure limitation on CPU, for instance 250% CPU used maximum dedicated to the container :

   c.DockerSpawner.extra_host_config = {
        'cpu_period': 100000,
	'cpu_quota': 250000,
   }

and :

    CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT     MEM %
    447680e99707        jupyter-desrozis    297.31%             532.6MiB / 3.702GiB   14.05%

CPU pourcent exceeds limit on docker stats reporting but we can see with top command :

      PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND 
    17806 desrozis  20   0 2513900 566740  52356 S 249,0 14,6   0:42.92 python 
    
Another possible option is 'cpu_shares' to share relatively CPU ressources among containers. 

From SDK docker's [documentation](http://docker-py.readthedocs.io/en/stable/containers.html), keywords are :
+ cpu_period (int) – The length of a CPU period in microseconds.
+ cpu_quota (int) – Microseconds of CPU time that the container can get in a CPU period.
+ cpu_shares (int) – CPU shares (relative weight).
+ cpuset_cpus (str) – CPUs in which to allow execution (0-3, 0,1).
+ mem_limit (int or str) – Memory limit. Accepts float values (which represent the memory limit of the created container in bytes) or a string with a units identification char (100000b, 1000k, 128m, 1g). If a string is specified without a units character, bytes are assumed as an intended unit.
+ mem_swappiness (int) – Tune a container’s memory swappiness behavior. Accepts number between 0 and 100.
+ memswap_limit (str or int) – Maximum amount of memory + swap a container is allowed to consume.