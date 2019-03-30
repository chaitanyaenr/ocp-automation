# ocp-automation
Playbooks to install and configure OpenShift on rhcos.

### Prepare the Jump host
- The jump host is the node which orchestrates the ocp install and configures the nodes to support the automation pipeline.
- Jump host needs to be a RHEL box and preferred if it is based out of the AMI or QCOW image built by the image provisioner.

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
.
├── ocp.inv
├── ocp.yml
├── README.md
└── roles
    ├── ansible-config
    │   └── tasks
    │       └── main.yml
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
    ├── disable-selinux
    │   └── tasks
    │       └── main.yml
    ├── install
    │   ├── files
    │   │   └── config.py
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       ├── config.j2
    │       ├── credentials.j2
    │       └── install-config.yaml.j2
    ├── node-config
    │   └── tasks
    │       └── main.yml
    ├── post-install
    │   ├── files
    │   │   └── cluster-monitoring-config.yml
    │   ├── tasks
    │   │   ├── bak
    │   │   └── main.yml
    │   └── templates
    │       └── ssh-config.j2
    ├── quickstart
    │   └── tasks
    │       └── main.yml
    ├── rhcos-post-install
    │   ├── tasks
    │   │   └── main.yml
    │   └── templates
    │       ├── cluster-monitoring-config.yml.j2
    │       ├── infra-node-machineset.yml.j2
    │       └── pbench-node-machineset.yml.j2
    └── selinux
        ├── files
        │   ├── selinux_patch1.pp
        │   ├── selinux_patch2.pp
        │   └── selinux_patch3.pp
        └── tasks
            └── main.yml
```
