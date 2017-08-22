#!/usr/bin/env python

import unittest
import inventory
from inventory import Inventory

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.ei={"_meta": {"hostvars": {}}}
        self.en={'etcd-1': {'ansible_ssh_host': 'etcd-1.example.com', 'tags': ['development', 'k8']}, 'etcd-2': {'ansible_ssh_host': 'etcd-2.example.com', 'tags': ['development', 'k8']}, 'etcd-3': {'ansible_ssh_host': 'etcd-3.example.com', 'tags': ['development', 'k8'], 'hostvars': {'etcd': 3}}}
        inv_args = {'entries': self.en, 'empty_inventory': self.ei}
        self.inventory = Inventory(**inv_args)

    def test_callable_module_methods(self):
        self.assertTrue(callable(inventory.parse_hosts_file))
        self.assertTrue(callable(inventory.check_command_line_args))

    def test_is_instance_of(self):
        self.assertTrue(isinstance(self.inventory, Inventory))

    def test_valid_instance_of(self):
        self.assertEqual(self.inventory.entries, self.en)
        self.assertEqual(self.inventory.processed_entries, self.ei)

    def test_generate_all_hosts(self):
        all_hosts = ['etcd-3.example.com', 'etcd-2.example.com', 'etcd-1.example.com']
        self.inventory.generate_all_hosts()
        self.assertEqual(self.inventory.processed_entries['all'], all_hosts)

    def test_group_by_tag(self):
        processed_entries = {'development': ['etcd-3.example.com', 'etcd-2.example.com', 'etcd-1.example.com'], 'k8': ['etcd-3.example.com', 'etcd-2.example.com', 'etcd-1.example.com'], '_meta': {'hostvars': {}}}
        self.inventory.group_by_tag()
        self.assertEqual(processed_entries, self.inventory.processed_entries)

    def test_generate_hosts_metadata(self):
        processed_entries = {'_meta': {'hostvars': {'etcd-3.example.com': {'etcd': 3}}}}
        self.inventory.generate_hosts_metadata()
        self.assertEqual(processed_entries, self.inventory.processed_entries)

if __name__ == '__main__':
    unittest.main()