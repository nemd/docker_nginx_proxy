import os
from fabric.api import local, env, settings
from fabric.colors import cyan, green, red

env.repo = 'nemd'

def proxy():
	env.service = 'proxy'

def build():
	local("docker build -t %(repo)s/%(service)s --rm=true ." % (
		{
			"service": env.service,
			"repo": env.repo
		}
	))

def pull():
	local("docker pull %s/%s" % (env.repo, env.service))

def push():
	local("docker push %s/%s" % (env.repo, env.service))

def run():
	local("docker run -d -p 80:80 -p 443:443 --restart=always --name %(service)s %(repo)s/%(service)s" % (
		{
			"repo": env.repo,
			"service": env.service
		}
	))

def launch():
	build()
	run()

def rm():
    with settings(warn_only=True):
        print(cyan("Stoping/Removing container: " + env.service))
        if local("docker rm -f $(docker ps -a | grep " + env.service + " | awk '{print $1}')").failed:
            print(red(env.service + " container doesn't exist...\n"))
        print(green("Container successfully removed.\n"))

def rmi():
    print(cyan("Deleting image: " + env.service))
    local("docker rmi $(docker images | grep " + env.service + " | awk '{print $1}')")
    print(green("Image successfully removed.\n"))
