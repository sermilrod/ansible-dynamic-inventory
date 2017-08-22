#!/usr/bin/env python

import yaml
import sys
import os

def parse_hosts_file():
    hosts_file = os.path.dirname(os.path.realpath(__file__)) + '/' + 'hosts.yml'
    with open(hosts_file, "r") as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

def check_command_line_args():
    if (len(sys.argv) == 2 and sys.argv[1] != "--list") or \
       (len(sys.argv) == 2 and sys.argv[1] == "--help") or \
       (len(sys.argv) > 2):
        print "Usage ./inventory.py (--list)"
        sys.exit(1)

class Inventory:
    def __init__(self, **kwargs):
        self.entries = kwargs['entries']
        self.processed_entries = kwargs['empty_inventory']

    def generate_all_hosts(self):
        self.processed_entries['all'] = []
        for host,attributes in self.entries.iteritems():
            self.processed_entries['all'].append(attributes['ansible_ssh_host'])

    def get_all_tags(self):
        return list(set(reduce(lambda x,y: x+y, \
                    map(lambda (k,v): v['tags'], self.entries.iteritems()))))

    def group_by_tag(self):
        for tag in self.get_all_tags():
            self.generate_group(tag)

    def generate_group(self, tag):
        self.processed_entries[tag] = []
        hosts = filter(bool, map(lambda (k,v): v['ansible_ssh_host'] \
                                               if tag in v['tags'] else False, \
                                               self.entries.iteritems()))

        self.processed_entries[tag] = hosts

    def generate_hosts_metadata(self):
        hostvars = filter(bool, map(lambda (k,v): {v['ansible_ssh_host']: v['hostvars']} \
                                                  if v.has_key('hostvars') \
                                                  else False, \
                                                  self.entries.iteritems()) )
        self.processed_entries['_meta']['hostvars'] = \
                    dict(kv for item in hostvars for kv in item.iteritems())


if __name__ == '__main__':
    check_command_line_args()

    hosts_entries = parse_hosts_file()
    inventory_args = {'entries': hosts_entries, 'empty_inventory': {"_meta": {"hostvars": {}}}}

    inventory = Inventory(**inventory_args)
    inventory.generate_all_hosts()
    inventory.group_by_tag()
    inventory.generate_hosts_metadata()

    print inventory.processed_entries