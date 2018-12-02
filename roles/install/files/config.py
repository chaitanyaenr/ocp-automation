#!/usr/bin/env python

import yaml
import sys
import argparse
import shutil

tmp_file_path = "/tmp/install-config.yml"

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

def main(cfg_type, cfg_path, master_count, worker_count):
    if cfg_type == "install-config":
        install_config(cfg_path, master_count, worker_count)
    else:
        print ("%s is not a valid config type, please check" %(cfg_type))
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_type", help="config_type can be one of the following: install-config")
    parser.add_argument("config_path", help="config_path should point to the installer-config path")
    parser.add_argument("master_count", help="number of master nodes")
    parser.add_argument("worker_count", help="number of worker nodes")
    args = parser.parse_args()
    main(args.config_type, args.config_path, args.master_count, args.worker_count)
