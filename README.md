# Ansible role - elasticsearch
[![Maintainer](https://img.shields.io/badge/maintained%20by-claranet-e00000?style=flat-square)](https://www.claranet.fr/)
[![License](https://img.shields.io/github/license/claranet/ansible-role-elasticsearch?style=flat-square)](LICENSE)
[![Release](https://img.shields.io/github/v/release/claranet/ansible-role-elasticsearch?style=flat-square)](https://github.com/claranet/ansible-role-elasticsearch/releases)
[![Status](https://img.shields.io/github/workflow/status/claranet/ansible-role-elasticsearch/Ansible%20Molecule?style=flat-square&label=tests)](https://github.com/claranet/ansible-role-elasticsearch/actions?query=workflow%3A%22Ansible+Molecule%22)
[![Ansible version](https://img.shields.io/badge/ansible-%3E%3D2.10-black.svg?style=flat-square&logo=ansible)](https://github.com/ansible/ansible)
[![Ansible Galaxy](https://img.shields.io/badge/ansible-galaxy-black.svg?style=flat-square&logo=ansible)](https://galaxy.ansible.com/claranet/elasticsearch)


> :star: Star us on GitHub — it motivates us a lot!

Install and configure Elasticsearch

## :warning: Requirements

Ansible >= 2.10

## :zap: Installation

```bash
ansible-galaxy install claranet.elasticsearch
```

## :gear: Role variables

Variable                                         | Default value                | Description
-------------------------------------------------|------------------------------|------------------------------------------------------
elasticsearch_version                            | **7.17.6**                   | version number
elasticsearch_version_depot                      | **7.x**                      | depot version number
elasticsearch_cluster_setup                      | **false**                    | Set True if you want a cluster
elasticsearch_cluster_nodes                      | **{}**                       | Setup each node of cluster
elasticsearch_settings                           | **{}**                       | Use for others parameters, use to configure only node 
elasticsearch_node_name                          | **{{ inventory_hostname }}** | Setup nodes name
elasticsearch_path_data                          | **/var/lib/elasticsearch**   | Setup data path
elasticsearch_path_logs                          | **/var/log/elasticsearch**   | Setup logs path
elasticsearch_cluster_name                       | **elasticsearch**            | Setup cluster name
elasticsearch_bootstrap_memory_lock              | **true**                     | 
elasticsearch_discovery_zen_minimum_master_nodes | **2**                        | Setup number minimum of master node
elasticsearch_templates_enabled                  | **false**                    | Active template 


## :arrows_counterclockwise: Dependencies

## :pencil2: Example Playbook only one node
[Coordinating only node](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#coordinating-only-node)

Some parameters have a dedicated variable.
The others have to be declared in *elasticsearch_settings* variable.

```yaml
---
- hosts: all
  roles:
    - name: elasticsearch
      role: claranet.elasticsearch
      elasticsearch_version: 7.17.6
      elasticsearch_settings:
        node.master: false
        node.data: false
        node.ingest: false
        cluster.remote.connect: false
```

## :pencil2: Example Playbook cluster (add ech node in inventory)

```yaml
---
- hosts: all
  roles:
    - name: elasticsearch
      role: claranet.elasticsearch
      elasticsearch_version: 7.17.6
      elasticsearch_cluster_setup: true
      elasticsearch_node_name: "{{ inventory_hostname }}"
      elasticsearch_path_data: /yourpath/elasticsearch
      elasticsearch_path_logs: /yourpath/logs/elasticsearch
      elasticsearch_bootstrap_memory_lock: true
      elasticsearch_cluster_name: 'elasticsearch'
      elasticsearch_discovery_zen_minimum_master_nodes: 2
      elasticsearch_cluster_nodes:
        - node: elastic01
          ip_address: "{{ hostvars['elastic01'].ansible_eth1.ipv4.address }}"
        - node: elastic02
          ip_address: "{{ hostvars['elastic02'].ansible_eth1.ipv4.address }}"
        - node: elastic03
          ip_address: "{{ hostvars['elastic03'].ansible_eth1.ipv4.address }}"
          port: 9300
      elasticsearch_discovery_zen_minimum_master_nodes: "{{ ( ( (elasticsearch_cluster_nodes | length) / 2 ) ) | round | int }}"
```

## :pencil2: Example Playbook use template

By default index templates are disabled.
The role does not push a default template, you have to put one. It is recommanded to define as a default template applying to all indices a minimum of 1 replica.

```yaml
---
- hosts: all
  roles:
    - name: elasticsearch
      role: claranet.elasticsearch
      elasticsearch_version: 7.17.6
      elasticsearch_elasticsearch_yml_template: elasticsearch/elasticsearch.yml.j2
      elasticsearch_jvm_options_template: elasticsearch/jvm.options.j2
      elasticsearch_log4j2_properties_template: elasticsearch/log4j2.properties.j2
      elasticsearch_templates_enabled: true
      elasticsearch_templates:
        all_default_settings:
          index_patterns: "*"
          settings:
            index:
              number_of_shards: 3
              number_of_replicas: 1
              refresh_interval: 5s
          mappings:
            properties:
              geoip:
                dynamic: true
                properties:
                  ip:
                    type: "ip"
                  location:
                    type: "geo_point"
                  latitude:
                    type: "half_float"
                  longitude:
                    type: "half_float"
```

## :pencil2: Example Playbook use plugins

```yaml
elasticsearch_plugins:
  # classic online installation using elasticsearch-plugins binary
  - name: analysis-icu
    state: present
  # online installation with proxy, will download file from url and install it
  - name: analysis-icu
    url: https://artifacts.elastic.co/downloads/elasticsearch-plugins/analysis-icu/analysis-icu-5.6.10.zip
    state: present
  # offline with custom previously downloaded file
  - name: x-pack
    path: /my/path/to/x-pack-5.6.10.zip
    state: present
```

## :closed_lock_with_key: [Hardening](HARDENING.md)

## :heart_eyes_cat: [Contributing](CONTRIBUTING.md)

## :copyright: [License](LICENSE)

[Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/)
