#!/usr/bin/env python3
"""
Proxmox VE API Client

A reusable Python client for PVE automation.
Usage: python pve_client.py <command> [options]

Commands:
  list-nodes              List all nodes in the cluster
  list-vms <node>         List all VMs on a node
  list-containers <node>  List all LXC containers on a node
  start-vm <node> <vmid>  Start a VM
  stop-vm <node> <vmid>   Stop a VM
  create-vm <node>        Create a VM (interactive)
  wait-task <node> <upid> Wait for a task to complete

Environment variables:
  PVE_HOST      PVE server hostname/IP
  PVE_USER      PVE username (default: root@pam)
  PVE_TOKEN_ID  API token ID
  PVE_SECRET    API token secret
"""

import os
import sys
import time
import json
import argparse
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PVEClient:
    """Proxmox VE API Client"""

    def __init__(self, host=None, user=None, token_id=None, token_secret=None):
        self.host = host or os.environ.get('PVE_HOST')
        self.user = user or os.environ.get('PVE_USER', 'root@pam')
        self.token_id = token_id or os.environ.get('PVE_TOKEN_ID')
        self.token_secret = token_secret or os.environ.get('PVE_SECRET')

        if not self.host:
            raise ValueError("PVE_HOST not set")
        if not self.token_id or not self.token_secret:
            raise ValueError("PVE_TOKEN_ID and PVE_SECRET must be set")

        self.base_url = f"https://{self.host}:8006/api2/json"
        self.headers = {
            'Authorization': f'PVEAPIToken={self.user}!{self.token_id}={self.token_secret}'
        }

    def request(self, method, endpoint, **kwargs):
        """Make an API request"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(
            method, url,
            headers=self.headers,
            verify=False,
            **kwargs
        )

        if response.status_code >= 400:
            try:
                error_data = response.json()
                error_msg = error_data.get('message', response.text)
            except:
                error_msg = response.text
            raise Exception(f"API Error {response.status_code}: {error_msg}")

        return response.json().get('data')

    def get(self, endpoint, params=None):
        return self.request('GET', endpoint, params=params)

    def post(self, endpoint, data=None):
        return self.request('POST', endpoint, data=data)

    def delete(self, endpoint):
        return self.request('DELETE', endpoint)

    # Node operations
    def list_nodes(self):
        return self.get('nodes')

    def get_node_status(self, node):
        return self.get(f'nodes/{node}/status')

    # VM operations
    def list_vms(self, node):
        return self.get(f'nodes/{node}/qemu')

    def get_vm_status(self, node, vmid):
        return self.get(f'nodes/{node}/qemu/{vmid}/status/current')

    def start_vm(self, node, vmid):
        return self.post(f'nodes/{node}/qemu/{vmid}/status/start')

    def stop_vm(self, node, vmid):
        return self.post(f'nodes/{node}/qemu/{vmid}/status/stop')

    def shutdown_vm(self, node, vmid, timeout=60):
        return self.post(f'nodes/{node}/qemu/{vmid}/status/shutdown',
                        data={'timeout': timeout})

    def reset_vm(self, node, vmid):
        return self.post(f'nodes/{node}/qemu/{vmid}/status/reset')

    def create_vm(self, node, **params):
        return self.post(f'nodes/{node}/qemu', data=params)

    def delete_vm(self, node, vmid):
        return self.delete(f'nodes/{node}/qemu/{vmid}')

    def clone_vm(self, node, vmid, newid, **params):
        return self.post(f'nodes/{node}/qemu/{vmid}/clone', data={'newid': newid, **params})

    # LXC operations
    def list_containers(self, node):
        return self.get(f'nodes/{node}/lxc')

    def get_container_status(self, node, vmid):
        return self.get(f'nodes/{node}/lxc/{vmid}/status/current')

    def start_container(self, node, vmid):
        return self.post(f'nodes/{node}/lxc/{vmid}/status/start')

    def stop_container(self, node, vmid):
        return self.post(f'nodes/{node}/lxc/{vmid}/status/stop')

    def create_container(self, node, **params):
        return self.post(f'nodes/{node}/lxc', data=params)

    def delete_container(self, node, vmid):
        return self.delete(f'nodes/{node}/lxc/{vmid}')

    # Task operations
    def get_task_status(self, node, upid):
        return self.get(f'nodes/{node}/tasks/{upid}/status')

    def wait_for_task(self, node, upid, timeout=300, interval=1):
        """Wait for a task to complete"""
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(node, upid)
            if status['status'] == 'stopped':
                return status
            time.sleep(interval)
        raise TimeoutError(f"Task {upid} did not complete within {timeout}s")

    # Storage operations
    def list_storage(self):
        return self.get('storage')

    def get_storage_content(self, node, storage, content_type=None):
        params = {}
        if content_type:
            params['content'] = content_type
        return self.get(f'nodes/{node}/storage/{storage}/content', params=params)

    # Cluster operations
    def get_cluster_resources(self):
        return self.get('cluster/resources')

    def get_cluster_status(self):
        return self.get('cluster/status')

    # Snapshot operations
    def list_snapshots(self, node, vmid):
        return self.get(f'nodes/{node}/qemu/{vmid}/snapshot')

    def create_snapshot(self, node, vmid, snapname, **params):
        return self.post(f'nodes/{node}/qemu/{vmid}/snapshot',
                        data={'snapname': snapname, **params})

    def rollback_snapshot(self, node, vmid, snapname):
        return self.post(f'nodes/{node}/qemu/{vmid}/snapshot/{snapname}/rollback')


# CLI commands
def cmd_list_nodes(client, args):
    nodes = client.list_nodes()
    print(json.dumps(nodes, indent=2))


def cmd_list_vms(client, args):
    vms = client.list_vms(args.node)
    print(json.dumps(vms, indent=2))


def cmd_list_containers(client, args):
    containers = client.list_containers(args.node)
    print(json.dumps(containers, indent=2))


def cmd_start_vm(client, args):
    result = client.start_vm(args.node, args.vmid)
    print(json.dumps(result, indent=2))


def cmd_stop_vm(client, args):
    result = client.stop_vm(args.node, args.vmid)
    print(json.dumps(result, indent=2))


def cmd_create_vm(client, args):
    params = {
        'vmid': args.vmid,
        'name': args.name,
        'memory': args.memory,
        'cores': args.cores,
    }
    if args.storage and args.disk:
        params['scsi0'] = f"{args.storage}:{args.disk}"
    if args.net:
        params['net0'] = args.net
    if args.iso:
        params['ide2'] = f"{args.iso},media=cdrom"

    result = client.create_vm(args.node, **params)
    print(json.dumps(result, indent=2))


def cmd_wait_task(client, args):
    status = client.wait_for_task(args.node, args.upid, timeout=args.timeout)
    print(json.dumps(status, indent=2))


def main():
    parser = argparse.ArgumentParser(description='Proxmox VE API Client')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Global options
    parser.add_argument('--host', help='PVE host')
    parser.add_argument('--user', default='root@pam', help='PVE user')
    parser.add_argument('--token-id', help='API token ID')
    parser.add_argument('--token-secret', help='API token secret')

    # list-nodes
    subparsers.add_parser('list-nodes', help='List all nodes')

    # list-vms
    p = subparsers.add_parser('list-vms', help='List VMs on a node')
    p.add_argument('node', help='Node name')

    # list-containers
    p = subparsers.add_parser('list-containers', help='List LXC containers')
    p.add_argument('node', help='Node name')

    # start-vm
    p = subparsers.add_parser('start-vm', help='Start a VM')
    p.add_argument('node', help='Node name')
    p.add_argument('vmid', type=int, help='VM ID')

    # stop-vm
    p = subparsers.add_parser('stop-vm', help='Stop a VM')
    p.add_argument('node', help='Node name')
    p.add_argument('vmid', type=int, help='VM ID')

    # create-vm
    p = subparsers.add_parser('create-vm', help='Create a VM')
    p.add_argument('node', help='Node name')
    p.add_argument('--vmid', type=int, required=True, help='VM ID')
    p.add_argument('--name', required=True, help='VM name')
    p.add_argument('--memory', type=int, default=2048, help='Memory in MB')
    p.add_argument('--cores', type=int, default=2, help='CPU cores')
    p.add_argument('--storage', help='Storage name')
    p.add_argument('--disk', help='Disk size in GB')
    p.add_argument('--net', default='virtio,bridge=vmbr0', help='Network config')
    p.add_argument('--iso', help='ISO image path')

    # wait-task
    p = subparsers.add_parser('wait-task', help='Wait for task completion')
    p.add_argument('node', help='Node name')
    p.add_argument('upid', help='Task UPID')
    p.add_argument('--timeout', type=int, default=300, help='Timeout in seconds')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        client = PVEClient(
            host=args.host,
            user=args.user,
            token_id=args.token_id,
            token_secret=args.token_secret
        )

        commands = {
            'list-nodes': cmd_list_nodes,
            'list-vms': cmd_list_vms,
            'list-containers': cmd_list_containers,
            'start-vm': cmd_start_vm,
            'stop-vm': cmd_stop_vm,
            'create-vm': cmd_create_vm,
            'wait-task': cmd_wait_task,
        }

        if args.command in commands:
            commands[args.command](client, args)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
