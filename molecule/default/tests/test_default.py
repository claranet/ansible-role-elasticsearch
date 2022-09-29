#!/usr/bin/env python

import os
import stat
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")

def test_elasticsearch_version_(host):
    version = host.package("elasticsearch").version
    assert version == "7.17.6"

def test_elasticsearch_yml_exist(host):
    f = host.file("/etc/elasticsearch/elasticsearch.yml")
    assert f.exists


def test_log4j_properties_exist(host):
    f = host.file("/etc/elasticsearch/log4j2.properties")
    assert f.exists


def test_elasticsearch_is_installed(host):
    elasticsearch = host.package("elasticsearch")
    assert elasticsearch.is_installed


def test_elasticsearch_running_and_enabled(host):
    es = host.service("elasticsearch")
    assert es.is_running
    assert es.is_enabled

def test_elasticsearch_cluster_health_green(host):
    command = """curl http://localhost:9200/_cluster/health?pretty"""
    cmd = host.run(command)
    assert '"status" : "green"' in cmd.stdout

def test_elasticsearch_cluster_health(host):
    command = """curl --head --request GET -k --user elastic:changeme \
                 http://localhost:9200/_cluster/health?pretty"""
    cmd = host.run(command)
    assert '200 OK' in cmd.stdout

#def test_elasticsearch_plugin_is_installed(host):
#    host.ansible(
##        "elasticsearch_plugin",
 #       "name=discovery-ec2 state=present"
 #   )["changed"]