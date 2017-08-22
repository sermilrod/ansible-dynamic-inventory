# ansible-dynamic-inventory
Do you have Bare Metal or virtualized platform without a good API? If so, would you like to use a dynamic inventory like it was AWS, Azure or OpenStack?

This project provides a dynamic inventory interface that allows you to simplify your static management of the hosts file and also manage your legacy platform inventory like it was a cloud provider.

## Setup

1. Copy src/inventory.py file into your inventory folder in Ansible
2. Copy the src/hosts.yml sample into your inventory folder, at the same level of the inventory.py, and customize it to your needs.
3. [Configure Ansible to use the inventory.py](http://docs.ansible.com/ansible/latest/intro_inventory.html#splitting-out-host-and-group-specific-data) (an example through ansible.cfg):
    ```
    [defaults]
    hostfile = ./inventory/inventory.py
    ```
## Usage

To verify that it works:

```bash
$ chmod u+x inventory.py
$ python inventory.py --list
```

To take advance of this inventory script you will need to generate your hosts.yml according to some patterns.
First of all, you don't want to generate all the possible groups of your machines manually. For that we use tags:
```
node-1:
  ansible_ssh_host: node-1.example.com
  tags:
    - development
    - node
node-2:
  ansible_ssh_host: node-2.example.com
  tags:
    - production
    - node
```
Given that list of hosts the inventory script will generate all the possible groups based on the tags:
```
{
  'development': ['node-1.example.com'],
  'production': ['node-2.example.com'],
  'node': ['node-1.example.com', 'node-2.example.com']
}
```
That will allow you to run your playbook by using intersections without taking the effort of thinking of all possible combinations of tags:
```bash
$ ansible-playbook --limit 'node:&development' myplaybook.yml
$ ansible-playbook --limit 'node:&production' myplaybook.yml
$ ansible-playbook --limit 'node' myplaybook.yml
```
Or alternatively within your play (as an example):
```
---
- name: foo
  hosts: "node:&{{ env }}"

  roles:
    - role: foo-role
```
```bash
$ ansible-playbook -e 'env=production' myplaybook.yml
```

If you want to include host variables you have to add a key to the host properties:
```
node-1:
  ansible_ssh_host: node-1.example.com
  tags:
    - development
    - node
  hostvars:
    attr_1: value1
    attr_2:
      - value2
      - value3
    attr_3:
      something: value4
```

Ultimately, as you still don't have an API that can provide you with an organized result like this, you will have to maintain a simple list of tagged nodes, which is better than an unorganized and full of duplication plain hosts file. All the possible combinations are handled by the inventory script and returned to Ansible.

### Developer considerations:
The dynamic inventory script comes with a tests that can be run:
```bash
$ cd src/
$ python -m unittest inventory_test
```
