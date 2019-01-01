# ocp-automation
Playbooks to install and configure OpenShift on rhcos.

### Prepare the Jump host
- The jump host is the node which orchestrates the ocp install and configures the nodes to support the automation pipeline.
- Jump host needs to be a RHEL box and preferred if it is based out of the AMI or QCOW image built by the image provisioner.
- Obtain the pull secret from coreos.com

### Run
Clone the github repo:
```
$ git clone https://github.com/chaitanyaenr/ocp-automation.git
$ cd ocp-automation
```
Set the variables including AWS credentials, number of master/worker instances, instance type to use in AWS e.t.c
You need to ssh as core user in case the install user is not set to root. It's recommended to use root user for
pipeline to work seamlessly. At this point of time, all we need to do is to kickoff the installer like:
```
$ ansible-playbook -vv -i ocp.inv ocp.yml
```

In the post-install phase, the playbook labels a worker node with role controller. This node is dedicated to run the
scale tests, the playbook ensures that the pbench data is collected from worker nodes which is not a controller node
for the performance data to be valid.

### Cleanup
Set OPENSHIFT_INSTALL to False and OPENSHIFT_AWS_INSTALL_CLEANUP to True in the ocp.inv and run the playbook:
```
$ ansible-playbook -vv -i ocp.inv ocp.yml
```

### Layout
```
├── ocp.inv
├── ocp.yml
├── README.md
└── roles
    ├── cleanup
    │   ├── files
    │   │   └── cleanup.sh
    │   └── tasks
    │       └── main.yml
    ├── controller-kickstart
    │   ├── files
    │   │   └── config
    │   └── tasks
    │       └── main.yml
    ├── install
    │   ├── files
    │   │   └── config.py
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       └── ocp-aws-env.sh.j2
    ├── node-config
    │   └── tasks
    │       └── main.yml
    ├── post-install
    │   └── tasks
    │       └── main.yml
    └── ssh-config
        ├── tasks
        │   └── main.yml
        └── templates
            └── ssh-config.j2
```
