#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management.libraries.script import Script

# server configurations
config = Script.get_config()

elastic_home = config['configurations']['elastic-sysconfig']['elastic_home']
conf_dir = config['configurations']['elastic-sysconfig']['conf_dir']
max_open_files = config['configurations']['elastic-sysconfig']['max_open_files']
max_map_count = config['configurations']['elastic-sysconfig']['max_map_count']

elastic_user = config['configurations']['elastic-sysconfig']['elastic_user']
user_group = config['configurations']['elastic-sysconfig']['user_group']
log_dir = config['configurations']['elastic-site']['path_logs']
pid_dir = '/var/run/elasticsearch'
pid_file = '/var/run/elasticsearch/elasticsearch.pid'
hostname = config['agentLevelParams']['hostname']
java64_home = config['ambariLevelParams']['java_home']
sysconfig_template = config['configurations']['elastic-sysconfig']['content']

cluster_name = config['configurations']['elastic-site']['cluster_name']
discovery_seed_hosts = config['configurations']['elastic-site']['discovery_seed_hosts']
cluster_initial_master_nodes = config['configurations']['elastic-site']['cluster_initial_master_nodes']

path_data = config['configurations']['elastic-site']['path_data']
http_cors_enabled = config['configurations']['elastic-site']['http_cors_enabled']
http_port = config['configurations']['elastic-site']['http_port']
transport_tcp_port = config['configurations']['elastic-site']['transport_tcp_port']

network_host = config['configurations']['elastic-site']['network_host']
