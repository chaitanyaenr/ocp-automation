#!/usr/bin/env python

import yaml
import sys
import argparse
import shutil

tmp_file_path = "/tmp/install-config.yml"
tmp_machineset = "/tmp/machine"
tmp_master_manifests_file = "/tmp/99_openshift-cluster-api_master-machines.yaml"
tmp_worker_manifests_file = "/tmp/99_openshift-cluster-api_worker-machineset.yaml"

def install_config(cfg_path, master_count, worker_count):
    with open(cfg_path, 'r') as install_config:
        try:
            config = yaml.load(install_config)
        except yaml.YAMLError as e:
            print ("Error loading the yaml file:%s" %(e))
            sys.exit(1)
        with open(tmp_file_path, 'w') as f:
           config['machines'][0]['replicas'] = int(master_count)
           config['machines'][1]['replicas'] = int(worker_count)
           yaml.dump(config, f,  default_flow_style=False)
    shutil.move(tmp_file_path, cfg_path)

def manifests(cfg_type, cfg_path, instance_type):
    with open(cfg_path, 'r') as manifests_file:
        try:
            config = yaml.load(manifests_file)
        except yaml.YAMLError as e:
            print ("Error loading the yaml file:%s" %(e))
            sys.exit(1)
        if cfg_type == "master_instances":
           for index, value in enumerate(config):
               config['items'][index-1]['spec']['providerConfig']['value']['instanceType'] = instance_type
           with open(tmp_master_manifests_file, 'w') as f:
               yaml.dump(config, f,  default_flow_style=False)
           shutil.move(tmp_master_manifests_file, cfg_path)
        elif cfg_type == "worker_instances":
           for index, value in enumerate(config):
               config['items'][index-1]['spec']['template']['spec']['providerConfig']['value']['instanceType'] = instance_type
           with open(tmp_worker_manifests_file, 'w') as f:
               yaml.dump(config, f,  default_flow_style=False)
           shutil.move(tmp_worker_manifests_file, cfg_path)
        else:
           print ("%s is not a valid config type, please check" %(cfg_type))

def main(cfg_type, cfg_path, master_count, worker_count, master_instance_type, worker_instance_type):
    if cfg_type == "install-config":
        install_config(cfg_path, master_count, worker_count)
    elif cfg_type == "master_instances":
        manifests(cfg_type, cfg_path, master_instance_type)
    elif cfg_type == "worker_instances":
        manifests(cfg_type, cfg_path, worker_instance_type)
    else:
        print ("%s is not a valid config type, please check" %(cfg_type))
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_type", help="config_type can be one of the following: install-config, machineset")
    parser.add_argument("config_path", help="config_path should point to the installer-config or machineset path")
    parser.add_argument("-master_count", help="number of master nodes")
    parser.add_argument("-worker_count", help="number of worker nodes")
    parser.add_argument("-master_instance_type", help="AWS instance type to use for master node")
    parser.add_argument("-worker_instance_type", help="AWS instance type to use for worker node")
    args = parser.parse_args()
    main(args.config_type, args.config_path, args.master_count, args.worker_count, args.master_instance_type, args.worker_instance_type)
