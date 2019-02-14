from dockerspawner import DockerSpawner
from traitlets import observe, Float, Integer

c = get_config()

c.JupyterHub.spawner_class = MySpawner

c.DockerSpawner.image = 'jupyter/tensorflow-notebook'

# Remove containers when shutdown
c.DockerSpawner.remove_containers = True

# Avoid errors from multiple session...
c.PAMAuthenticator.open_sessions = False

from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

c.JupyterHub.ssl_key = 'ssl/jupyterhub.key'
c.JupyterHub.ssl_cert = 'ssl/jupyterhub.crt'

c.DockerSpawner.extra_host_config = {
    'mem_limit': '30m',
    'memswap_limit': -1,
    #'mem_swappiness': 1,
    #'cpu_period': 100000,
    #'cpu_quota': 250000
}
