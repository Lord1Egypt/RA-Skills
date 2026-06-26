---
name: pve-automation
description: Automate Proxmox VE (PVE) virtual machine and container management tasks including VM lifecycle operations (create, start, stop, delete), template management, cloud-init configuration, plugin installation, and cluster operations. Use this skill whenever the user mentions Proxmox, PVE, VM management, container (LXC) operations, qemu, or virtualization automation.
---

# Proxmox VE Automation Skill

This skill provides comprehensive automation for Proxmox VE (Virtual Environment) management through its REST API.

## Overview

Proxmox VE is an open-source server virtualization management platform that supports:
- **QEMU/KVM Virtual Machines** (VMs)
- **LXC Containers** (Linux Containers)
- **Storage management**
- **Cluster management**
- **Backup and snapshots**

## API Basics

- **Base URL**: `https://<pve-host>:<port>/api2/json/`
  - Default port: `8006`
  - Custom port can be configured in PVE settings
- **Authentication**: Ticket-based (cookie) or API Token-based
- **Data format**: JSON
- **API Explorer**: `https://<pve-host>:<port>/pve-docs/api-viewer/`

### Custom API Port

PVE API port can be customized from the default 8006:

```bash
# Check current API port configuration
grep "port" /etc/default/pveproxy

# Or via API: GET /nodes/{node}/services
```

**Using custom port in code:**
```python
# Option 1: Include port in host
client = PVEClient(host='pve.example.com:8443', ...)

# Option 2: Explicit port parameter
class PVEClient:
    def __init__(self, host, port=8006, ...):
        self.base_url = f"https://{host}:{port}/api2/json"

# Option 3: Environment variable
port = os.environ.get('PVE_PORT', 8006)
```

## Authentication Methods

### Method 1: API Token (Recommended for automation)

API tokens provide stateless access without CSRF tokens:

```bash
# Header format
Authorization: PVEAPIToken=USER@REALM!TOKENID=UUID

# Example
curl -H 'Authorization: PVEAPIToken=root@pam!automation=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee' \
  https://pve.example.com:8006/api2/json/nodes
```

**Creating an API Token:**
1. Web UI: Datacenter → Permissions → API Tokens → Add
2. Or via API: `POST /access/users/{userid}/token/{tokenid}`

### Method 2: Ticket-based Authentication

For interactive sessions or when API tokens aren't available:

```bash
# 1. Get ticket and CSRF token
curl -k -d 'username=root@pam' --data-urlencode 'password=secret' \
  https://pve.example.com:8006/api2/json/access/ticket

# Response: { "data": { "ticket": "...", "CSRFPreventionToken": "..." } }

# 2. Use ticket in subsequent requests
curl -k -b "PVEAuthCookie=<ticket>" \
  -H "CSRFPreventionToken: <csrf_token>" \
  https://pve.example.com:8006/api2/json/nodes
```

Tickets expire after 2 hours. Renew by passing the old ticket as password.

## Common Operations

### Node Operations

```bash
# List all nodes
GET /nodes

# Get node status
GET /nodes/{node}/status

# Get node resources (CPU, memory, disk usage)
GET /nodes/{node}/resources
```

### VM (QEMU) Operations

```bash
# List VMs on a node
GET /nodes/{node}/qemu

# Get VM status
GET /nodes/{node}/qemu/{vmid}/status/current

# Start VM
POST /nodes/{node}/qemu/{vmid}/status/start

# Stop VM (graceful shutdown)
POST /nodes/{node}/qemu/{vmid}/status/shutdown

# Stop VM (force/poweroff)
POST /nodes/{node}/qemu/{vmid}/status/stop

# Reset VM
POST /nodes/{node}/qemu/{vmid}/status/reset

# Delete VM
DELETE /nodes/{node}/qemu/{vmid}
```

### LXC Container Operations

```bash
# List containers
GET /nodes/{node}/lxc

# Get container status
GET /nodes/{node}/lxc/{vmid}/status/current

# Start container
POST /nodes/{node}/lxc/{vmid}/status/start

# Stop container
POST /nodes/{node}/lxc/{vmid}/status/stop

# Delete container
DELETE /nodes/{node}/lxc/{vmid}
```

### VM/Container Creation

**Create a VM from template:**
```bash
POST /nodes/{node}/qemu

Parameters:
- vmid: Unique VM ID (100-999999999)
- name: VM name
- memory: RAM in MB
- cores: Number of CPU cores
- sockets: Number of CPU sockets
- cpu: CPU type (host, kvm64, etc.)
- net0: Network config (e.g., "virtio,bridge=vmbr0")
- ide2: CD/DVD drive or cloud-init (e.g., "local:iso/ubuntu-22.04.iso,media=cdrom")
- scsi0: Disk (e.g., "local-lvm:32,format=raw")
- ostype: OS type (l26 for Linux 2.6+, win11 for Windows 11)
```

**Create an LXC container:**
```bash
POST /nodes/{node}/lxc

Parameters:
- vmid: Unique container ID
- hostname: Container hostname
- memory: RAM in MB
- swap: Swap in MB
- cores: CPU cores
- ostemplate: Template path (e.g., "local:vztmpl/debian-12-standard_12.0-1_amd64.tar.zst")
- storage: Storage for rootfs
- rootfs: Root filesystem size (e.g., "local-lvm:8")
- net0: Network config (e.g., "name=eth0,bridge=vmbr0,ip=dhcp")
- password: Root password (or use ssh-public-keys)
```

### Template Management

```bash
# List available templates on storage
GET /nodes/{node}/storage/{storage}/content?content=vztmpl

# Download template from Proxmox VE repository
POST /nodes/{node}/storage/{storage}/download-url

Parameters:
- url: Template URL
- filename: Target filename
- content: "vztmpl" for container templates, "iso" for ISO images

# List container templates available for download
GET /nodes/{node}/aplinfo

# Download from aplinfo (official templates)
POST /nodes/{node}/storage/{storage}/aplinfo
```

### Cloud-Init Configuration

Cloud-init allows automatic VM initialization on first boot:

```bash
# Set cloud-init parameters
POST /nodes/{node}/qemu/{vmid}/config

Parameters:
- cicustom: Custom cloud-init config (optional)
- ciuser: Default user name
- cipassword: Default user password
- citype: Config drive type (configdrive2, nocloud)
- ciupgrade: Run package upgrade on boot (0/1)
- sshkeys: Public SSH keys (URL-encoded)
- ipconfig0: IP config (e.g., "ip=192.168.1.100/24,gw=192.168.1.1")
- ipconfig1: Additional network config
- nameserver: DNS server
- searchdomain: DNS search domain
```

**Important**: Cloud-init requires a cloud-init capable image (Ubuntu Cloud Images, Debian Cloud, etc.) and a configured CD/DVD drive (usually ide2) for the config drive.

### Snapshots and Backups

```bash
# List snapshots
GET /nodes/{node}/qemu/{vmid}/snapshot

# Create snapshot
POST /nodes/{node}/qemu/{vmid}/snapshot
Parameters:
- snapname: Snapshot name
- description: Optional description
- vmstate: Include RAM state (1/0)

# Rollback to snapshot
POST /nodes/{node}/qemu/{vmid}/snapshot/{snapname}/rollback

# Delete snapshot
DELETE /nodes/{node}/qemu/{vmid}/snapshot/{snapname}

# Create backup
POST /nodes/{node}/vzdump
Parameters:
- vmid: VM ID to backup
- storage: Target storage
- mode: snapshot/suspend/stop
- compress: Compression level (0-9)
```

### Storage Operations

```bash
# List storage
GET /storage

# Get storage status
GET /nodes/{node}/storage/{storage}/status

# List storage content
GET /nodes/{node}/storage/{storage}/content

# Upload file to storage (ISO, template)
POST /nodes/{node}/storage/{storage}/upload
Content-Type: multipart/form-data
```

### Network Configuration

```bash
# List network interfaces on node
GET /nodes/{node}/network

# Create network bridge
POST /nodes/{node}/network
Parameters:
- iface: Interface name (e.g., "vmbr1")
- type: "bridge"
- bridge_ports: Physical ports to bridge
- autostart: Start on boot (1/0)
```

### Cluster Operations

```bash
# Get cluster status
GET /cluster/status

# Get cluster resources
GET /cluster/resources

# Get cluster tasks
GET /cluster/tasks

# Get task status
GET /nodes/{node}/tasks/{upid}/status

# Wait for task completion by polling task status
```

## Working with Tasks

Most write operations return a task UPID (Unique Process ID). Poll the task status to track completion:

```bash
# Get task status
GET /nodes/{node}/tasks/{upid}/status

Response includes:
- status: "running", "stopped"
- exitstatus: "OK" on success, error message on failure
- pid: Process ID
```

## Best Practices

### 1. VM ID Management
- VM IDs must be unique across the cluster
- Common convention: 100-999 for VMs, 100000+ for containers (though not required)
- Check available VM IDs: `GET /cluster/resources` and filter by type

### 2. Resource Allocation
- Always specify memory and cores when creating VMs
- Leave overhead for the host (don't allocate 100% of resources)
- Use ballooning for dynamic memory: `balloon: 1024` with `memory: 4096`

### 3. Network Configuration
- Use virtio network drivers for best performance
- Configure bridges properly before creating VMs
- For VLANs: `net0: "virtio,bridge=vmbr0,tag=100"`

### 4. Storage
- Use appropriate storage types:
  - `local`: Directory storage
  - `local-lvm`: LVM thin provisioning
  - `zfs`: ZFS storage
  - `nfs`, `iscsi`, `ceph`: Network storage

### 5. Security
- Use API tokens with limited permissions instead of root
- Enable 2FA for user accounts
- Use firewall rules: `/nodes/{node}/qemu/{vmid}/firewall/rules`

## Common Workflows

### Create a VM from Cloud Image

1. Download cloud image ISO to storage
2. Create VM with cloud-init drive
3. Configure cloud-init parameters
4. Start VM

### Clone a Template VM

```bash
POST /nodes/{node}/qemu/{source-vmid}/clone
Parameters:
- newid: New VM ID
- name: New VM name
- target: Target node (for cluster)
- full: Full clone (1) or linked clone (0)
- storage: Target storage for full clone
```

### Bulk Operations

For multiple VMs, loop through and call API for each:
- Always add delays between operations to avoid overwhelming the API
- Check task completion before proceeding
- Handle errors gracefully

## API Parameters Reference

### VM Creation Parameters (POST /nodes/{node}/qemu)

**Required Parameters:**
- `vmid` (integer): Unique VM ID (100-999999999), must be unique across cluster
- `name` (string): VM name (must be valid DNS name)

**Resource Parameters:**
- `memory` (integer): RAM in MB. Examples: 512, 1024, 2048, 4096, 8192
- `balloon` (integer): Minimum memory for ballooning in MB (optional, enables memory overcommit)
- `cores` (integer): Number of CPU cores per socket (1-128)
- `sockets` (integer): Number of CPU sockets (1-4)
- `cpu` (string): CPU type. Common values: `host`, `kvm64`, `qemu64`, `x86-64-v2`
- `vcpus` (integer): Number of hotplugged vCPUs (defaults to cores*sockets)

**Storage Parameters:**
- `scsi0`, `scsi1`, `virtio0`, `virtio1`, `ide0`, `ide1`, `sata0`, etc.
  - Format: `<storage>:<size>` or `<storage>:<volume-name>`
  - Examples: `local-lvm:32`, `zfs:vm-disk-001`, `local-lvm:64,format=raw`
- `efidisk0` (string): EFI system partition. Example: `local-lvm:1,format=raw,efitype=4m`

**Network Parameters:**
- `net0`, `net1`, etc. (string): Network interface config
  - Format: `<model>,<options>`
  - Models: `virtio` (recommended), `e1000`, `rtl8139`, `vmxnet3`
  - Examples:
    - `virtio,bridge=vmbr0` (basic bridge)
    - `virtio,bridge=vmbr0,tag=100` (VLAN 100)
    - `virtio,bridge=vmbr0,ip=192.168.1.10/24,gw=192.168.1.1` (static IP via cloud-init)

**Boot/Media Parameters:**
- `ostype` (string): OS type for optimizations
  - Linux: `l24` (2.4), `l26` (2.6+), `other`
  - Windows: `wxp`, `w2k`, `w2k3`, `w2k8`, `wvista`, `win7`, `win8`, `win10`, `win11`
- `ide2` (string): CD/DVD drive or cloud-init drive
  - ISO: `local:iso/ubuntu-22.04.iso,media=cdrom`
  - Cloud-init: `local-lvm:cloudinit,media=cdrom`
- `boot` (string): Boot order. Example: `order=ide2;scsi0;net0`
- `bios` (string): `seabios` (default) or `ovmf` (UEFI)

**Cloud-Init Parameters:**
- `ciuser` (string): Default username
- `cipassword` (string): Default password (will be hashed)
- `cicustom` (string): Path to custom cloud-init config
- `citype` (string): `configdrive2` or `nocloud`
- `sshkeys` (string): URL-encoded SSH public keys
- `ipconfig0`, `ipconfig1` (string): Network config
  - DHCP: `ip=dhcp`
  - Static: `ip=192.168.1.10/24,gw=192.168.1.1`
- `nameserver` (string): DNS servers (comma-separated)
- `searchdomain` (string): DNS search domain

### LXC Container Parameters (POST /nodes/{node}/lxc)

**Required Parameters:**
- `vmid` (integer): Unique container ID
- `ostemplate` (string): Template path. Example: `local:vztmpl/debian-12-standard_12.0-1_amd64.tar.zst`

**Resource Parameters:**
- `memory` (integer): RAM in MB
- `swap` (integer): Swap in MB
- `cores` (integer): CPU cores
- `cpulimit` (number): CPU limit (0-128, 0=unlimited)
- `cpuunits` (integer): CPU weight (0-500000, default: 1024)

**Storage Parameters:**
- `rootfs` (string): Root filesystem. Format: `<storage>:<size>`
  - Example: `local-lvm:8`, `local-lvm:16,mountoptions=noatime`
- `mp0`, `mp1`, etc. (string): Mount points
  - Example: `local-lvm:32,mp=/data`, `/host/path:mp=/container/path`

**Network Parameters:**
- `net0`, `net1`, etc. (string): Network config
  - Format: `name=<ifname>,bridge=<br>[,options]`
  - Examples:
    - `name=eth0,bridge=vmbr0,ip=dhcp`
    - `name=eth0,bridge=vmbr0,ip=192.168.1.10/24,gw=192.168.1.1`
    - `name=eth0,bridge=vmbr0,tag=100,ip=dhcp` (VLAN)

**System Parameters:**
- `hostname` (string): Container hostname
- `password` (string): Root password
- `ssh-public-keys` (string): SSH public keys (newline-separated)
- `unprivileged` (boolean): Create unprivileged container (0/1)
- `features` (string): Enabled features. Example: `nesting=1,keyctl=1`
- `onboot` (boolean): Start on boot (0/1)
- `startup` (string): Startup order and delay. Example: `order=1,up=5,down=5`

## Safety and Resource Protection

### 1. Check Available Resources Before Creation

Always verify node resources before creating VMs/containers:

```python
def check_node_resources(client, node, required_memory, required_disk):
    """
    Check if node has enough resources for new VM/container.
    Returns (ok, message) tuple.
    """
    # Get node status
    status = client.get(f'nodes/{node}/status')

    memory = status['memory']
    disk = status['rootfs']  # or check specific storage

    # Memory check (leave 10% overhead for host)
    available_memory = memory['free']
    total_memory = memory['total']
    max_usable = total_memory * 0.9
    current_used = total_memory - available_memory

    if current_used + required_memory > max_usable:
        return False, f"Insufficient memory. Available: {available_memory/1024/1024:.1f}GB, Required: {required_memory/1024:.1f}GB"

    # Disk check
    available_disk = disk['avail']
    if required_disk and required_disk > available_disk:
        return False, f"Insufficient disk space. Available: {available_disk/1024/1024/1024:.1f}GB, Required: {required_disk/1024/1024/1024:.1f}GB"

    return True, "Resources OK"

# Usage before creating VM
ok, msg = check_node_resources(client, 'pve1', memory=4096, disk=32*1024*1024*1024)
if not ok:
    raise Exception(f"Cannot create VM: {msg}")
```

### 2. Get Cluster-Wide Resource Usage

```python
def get_cluster_resources_summary(client):
    """Get aggregated resource usage across all nodes"""
    resources = client.get('cluster/resources')

    summary = {
        'nodes': [],
        'vms': [],
        'containers': [],
        'storage': []
    }

    for r in resources:
        if r['type'] == 'node':
            summary['nodes'].append({
                'name': r['node'],
                'cpu': r.get('cpu', 0),
                'maxcpu': r.get('maxcpu', 0),
                'mem': r.get('mem', 0),
                'maxmem': r.get('maxmem', 0),
                'disk': r.get('disk', 0),
                'maxdisk': r.get('maxdisk', 0),
                'status': r['status']
            })
        elif r['type'] == 'qemu':
            summary['vms'].append(r)
        elif r['type'] == 'lxc':
            summary['containers'].append(r)
        elif r['type'] == 'storage':
            summary['storage'].append(r)

    return summary
```

### 3. Safe VM/Container Creation Helper

```python
class SafePVEClient(PVEClient):
    """PVE client with safety checks"""

    MAX_MEMORY_OVERCOMMIT = 1.2  # Allow 20% overcommit with ballooning
    MAX_SINGLE_VM_MEMORY = 128 * 1024  # 128GB max per VM
    MAX_SINGLE_VM_DISK = 10 * 1024 * 1024 * 1024  # 10TB max per VM

    def safe_create_vm(self, node, **params):
        """Create VM with safety checks"""

        # Validate VMID
        vmid = params.get('vmid')
        if not (100 <= vmid <= 999999999):
            raise ValueError(f"VMID {vmid} out of range (100-999999999)")

        # Check if VMID already exists
        try:
            existing = self.get(f'nodes/{node}/qemu/{vmid}/status/current')
            raise ValueError(f"VM {vmid} already exists on {node}")
        except requests.HTTPError as e:
            if e.response.status_code != 404:
                raise

        # Validate memory
        memory = params.get('memory', 0)
        if memory > self.MAX_SINGLE_VM_MEMORY:
            raise ValueError(f"Memory {memory}MB exceeds maximum {self.MAX_SINGLE_VM_MEMORY}MB")

        # Check node resources
        node_status = self.get(f'nodes/{node}/status')
        total_mem = node_status['memory']['total']
        used_mem = node_status['memory']['used']
        available_mem = total_mem - used_mem

        # Check if all VMs on node can fit (with overcommit)
        all_vms = self.get(f'nodes/{node}/qemu')
        total_allocated = sum(vm.get('maxmem', 0) for vm in all_vms) + memory
        max_allowed = total_mem * self.MAX_MEMORY_OVERCOMMIT

        if total_allocated > max_allowed:
            raise ValueError(
                f"Memory overcommit exceeded. Total allocated would be {total_allocated/1024/1024:.1f}GB, "
                f"max allowed is {max_allowed/1024/1024:.1f}GB"
            )

        # Validate disk size if specified
        for key, value in params.items():
            if key in ['scsi0', 'scsi1', 'virtio0', 'virtio1', 'ide0', 'ide1']:
                # Parse size from disk spec
                if ':' in str(value):
                    try:
                        size_str = str(value).split(':')[1].split(',')[0]
                        if size_str.isdigit():
                            size_gb = int(size_str)
                            if size_gb * 1024 * 1024 * 1024 > self.MAX_SINGLE_VM_DISK:
                                raise ValueError(f"Disk size exceeds maximum")
                    except (IndexError, ValueError):
                        pass

        return self.create_vm(node, **params)

    def safe_create_container(self, node, **params):
        """Create LXC container with safety checks"""

        vmid = params.get('vmid')
        if not (100 <= vmid <= 999999999):
            raise ValueError(f"VMID {vmid} out of range")

        # Check for existing VMID
        try:
            existing = self.get(f'nodes/{node}/lxc/{vmid}/status/current')
            raise ValueError(f"Container {vmid} already exists")
        except requests.HTTPError as e:
            if e.response.status_code != 404:
                raise

        # LXC-specific checks
        memory = params.get('memory', 512)
        if memory > self.MAX_SINGLE_VM_MEMORY:
            raise ValueError(f"Memory {memory}MB exceeds maximum")

        return self.create_container(node, **params)
```

### 4. Dry-Run Mode for Bulk Operations

```python
def bulk_vm_operation(client, node, vmids, operation, dry_run=True):
    """
    Perform bulk operations with dry-run support.
    Operations: 'start', 'stop', 'shutdown', 'delete'
    """
    results = []

    for vmid in vmids:
        try:
            # Verify VM exists and get current status
            vm_status = client.get(f'nodes/{node}/qemu/{vmid}/status/current')
            current_state = vm_status['status']

            if dry_run:
                results.append({
                    'vmid': vmid,
                    'operation': operation,
                    'dry_run': True,
                    'current_state': current_state,
                    'would_execute': True,
                    'message': f"Would {operation} VM {vmid} (currently {current_state})"
                })
            else:
                # Execute operation
                if operation == 'start' and current_state == 'stopped':
                    result = client.post(f'nodes/{node}/qemu/{vmid}/status/start')
                elif operation == 'stop' and current_state == 'running':
                    result = client.post(f'nodes/{node}/qemu/{vmid}/status/stop')
                elif operation == 'shutdown' and current_state == 'running':
                    result = client.post(f'nodes/{node}/qemu/{vmid}/status/shutdown')
                elif operation == 'delete':
                    # Extra safety: only delete if stopped
                    if current_state != 'stopped':
                        raise ValueError(f"VM {vmid} must be stopped before deletion")
                    result = client.delete(f'nodes/{node}/qemu/{vmid}')
                else:
                    result = {'message': f'No action needed (currently {current_state})'}

                results.append({
                    'vmid': vmid,
                    'operation': operation,
                    'success': True,
                    'result': result
                })

        except Exception as e:
            results.append({
                'vmid': vmid,
                'operation': operation,
                'success': False,
                'error': str(e)
            })

    return results
```

### 5. Safe Defaults Checklist

When generating PVE automation code, ensure these safeguards are included:

1. **Pre-flight Checks:**
   - Verify VMID is unique (not already in use)
   - Check node has sufficient resources
   - Validate storage exists and has space

2. **Resource Limits:**
   - Set reasonable defaults (2GB RAM, 2 cores, 32GB disk)
   - Warn if allocating >50% of node resources to single VM
   - Use ballooning for memory overcommit

3. **Operation Safety:**
   - Always use dry-run for bulk operations
   - Confirm destructive operations (delete, rollback)
   - Check VM is stopped before deletion or disk modification

4. **Error Handling:**
   - Handle 409 Conflict (VMID exists)
   - Handle 507 Insufficient Storage
   - Handle 595 PVE errors with meaningful messages

5. **Network Safety:**
   - Validate bridge exists before creating VM
   - Warn about IP conflicts (manual check required)
   - Use VLAN tags appropriately

## Error Handling

Common HTTP status codes:
- `400`: Bad request (missing/invalid parameters)
- `401`: Unauthorized (invalid credentials)
- `403`: Forbidden (insufficient permissions)
- `404`: Resource not found
- `409`: Conflict (VMID already exists)
- `500`: Internal server error
- `507`: Insufficient Storage
- `595`: PVE specific errors (check response body)

Error response format:
```json
{
  "errors": {
    "parameter_name": "error message"
  },
  "message": "Human readable error message"
}
```

### Common Error Patterns and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `vmid already exists` | VMID in use | Query `/cluster/resources` to find next available |
| `unable to create VM: out of memory` | Node overloaded | Check `memory.free` before creation |
| `unable to create disk: out of space` | Storage full | Check storage usage before creation |
| `bridge 'vmbrX' does not exist` | Invalid network config | List `/nodes/{node}/network` to get valid bridges |
| `OSTYPE not set` | Missing OS type | Add `ostype` parameter (l26 for Linux, win10 for Windows) |
| `timeout` | Task taking too long | Increase timeout for slow operations (template download) |

## Python Example

```python
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PVEClient:
    def __init__(self, host, token_id, token_secret, user='root@pam'):
        self.base_url = f"https://{host}:8006/api2/json"
        self.headers = {
            'Authorization': f'PVEAPIToken={user}!{token_id}={token_secret}'
        }

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(
            method, url,
            headers=self.headers,
            verify=False,
            **kwargs
        )
        response.raise_for_status()
        return response.json().get('data')

    def get_nodes(self):
        return self.request('GET', 'nodes')

    def get_vms(self, node):
        return self.request('GET', f'nodes/{node}/qemu')

    def start_vm(self, node, vmid):
        return self.request('POST', f'nodes/{node}/qemu/{vmid}/status/start')

    def stop_vm(self, node, vmid):
        return self.request('POST', f'nodes/{node}/qemu/{vmid}/status/stop')

    def create_vm(self, node, **params):
        return self.request('POST', f'nodes/{node}/qemu', data=params)

    def get_task_status(self, node, upid):
        return self.request('GET', f'nodes/{node}/tasks/{upid}/status')

    def wait_for_task(self, node, upid, timeout=300):
        import time
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_task_status(node, upid)
            if status['status'] == 'stopped':
                return status
            time.sleep(1)
        raise TimeoutError(f"Task {upid} did not complete within {timeout}s")
```

## Advanced Operations

### 1. High Availability (HA)

HA ensures VMs/containers restart on another node if the current node fails.

**HA Resources:**
```bash
# List HA groups
GET /cluster/ha/groups

# Create HA group (nodes that can host the VM)
POST /cluster/ha/groups
Parameters:
- group: Group name (e.g., "production")
- nodes: Node list with priority (e.g., "pve1:1,pve2:2,pve3:1")
- restricted: 1 = only run on these nodes, 0 = can run elsewhere
- nofailback: 1 = stay on current node after recovery

# Delete HA group
DELETE /cluster/ha/groups/{group}
```

**HA Resources (VMs to protect):**
```bash
# List HA managed resources
GET /cluster/ha/resources

# Add VM/container to HA
POST /cluster/ha/resources
Parameters:
- sid: Service ID (e.g., "vm:100" or "ct:200")
- group: HA group name (optional)
- state: "started" or "stopped"
- max_restart: Max restart attempts (default: 1)
- max_relocate: Max relocate attempts (default: 1)

# Remove from HA
DELETE /cluster/ha/resources/{sid}
```

**HA Status and Control:**
```bash
# Get HA status
GET /cluster/ha/status/current

# Request manual migration
POST /cluster/ha/resources/{sid}/migrate
Parameters:
- target: Target node name

# Request relocation (stop on current, start on new)
POST /cluster/ha/resources/{sid}/relocate
Parameters:
- target: Target node name
```

### 2. Live Migration

Migrate running VMs between nodes (requires shared storage or storage migration).

```bash
# Online migrate VM to another node
POST /nodes/{source-node}/qemu/{vmid}/migrate
Parameters:
- target: Target node name (required)
- online: 1 for live migration (VM stays running)
- with-local-disks: 1 to migrate local disks too (requires offline or very recent PVE)

# Check migration status (returns task UPID)
# Poll task status to track progress
```

**Migration Requirements:**
- Shared storage (VM disks accessible from both nodes) OR `with-local-disks=1`
- Same network bridges on both nodes (vmbr0, etc.)
- CPUs compatible (or use `cpu: kvm64` for portability)
- For live migration: Intel-Intel or AMD-AMD (same vendor)

### 3. PCI/GPU Passthrough

Pass physical PCI devices (GPUs, NICs) to VMs.

**Prerequisites:**
- Enable IOMMU in BIOS and kernel
- Load VFIO modules
- Blacklist GPU drivers on host

**Configuration:**
```bash
# Get available PCI devices
GET /nodes/{node}/hardware/pci

# Get PCI device details (includes IOMMU groups)
GET /nodes/{node}/hardware/pci/{pci-id}

# Update VM config with PCI device
POST /nodes/{node}/qemu/{vmid}/config
Parameters:
- hostpci0: PCI device mapping
  Format: "0000:01:00.0" (simple)
  Advanced: "0000:01:00.0,pcie=1,x-vga=1,rombar=0"
  Options:
  - pcie=1: Use PCIe (recommended for modern GPUs)
  - x-vga=1: Primary GPU
  - rombar=0: Hide ROM bar (some GPUs need this)
  - multifunction=1: Pass multifunction device

# Example for NVIDIA GPU
hostpci0: "0000:01:00.0,pcie=1,x-vga=1"

# Example for additional GPU functions (audio)
hostpci1: "0000:01:00.1,pcie=1"

# CPU type must be host for passthrough
cpu: host
```

**USB Passthrough:**
```bash
# List USB devices
GET /nodes/{node}/hardware/usb

# Add to VM config
usb0: "host=1234:5678"  # Vendor:Product ID
usb1: "host=1-2.3"       # Bus-Port path
```

### 4. Backup and Restore

**Backup (vzdump):**
```bash
# Create backup
POST /nodes/{node}/vzdump
Parameters:
- vmid: VM ID(s) to backup (comma-separated or multiple params)
- storage: Target storage ID
- mode: Backup mode
  - snapshot: No downtime, uses QEMU snapshot
  - suspend: Brief pause for consistency
  - stop: Shutdown, backup, start
- compress: Compression level (0-9, default: 1)
- remove: Remove old backups (keep N most recent)
- notes-template: Custom backup notes
- notification-mode: "auto", "always", or "failure"

# Backup all VMs on node
vmid: "all"

# Returns task UPID - poll for completion
```

**Restore:**
```bash
# Restore VM from backup
POST /nodes/{node}/storage/{storage}/content/{backup-file}/restore
Parameters:
- vmid: New VM ID (must be unique)
- force: Overwrite existing VM (dangerous!)
- unique: Generate new MAC addresses (recommended)
- storage: Target storage for disks (can differ from backup)

# Extract config from backup (inspect without restoring)
GET /nodes/{node}/storage/{storage}/content/{backup-file}/config
```

**Backup Management:**
```bash
# List backups in storage
GET /nodes/{node}/storage/{storage}/content?content=backup

# Get backup information
GET /nodes/{node}/storage/{storage}/content/{backup-file}

# Delete backup
DELETE /nodes/{node}/storage/{storage}/content/{backup-file}
```

### 5. Scheduled Jobs

Automate backups and other tasks.

```bash
# List scheduled jobs
GET /cluster/jobs/schedule-analyze

# Create scheduled backup job
POST /cluster/jobs
Parameters:
- id: Job ID (optional, auto-generated)
- type: "vzdump"
- schedule: Cron expression (e.g., "0 2 * * *" for 2 AM daily)
- enabled: 1 or 0
- vmid: VM ID(s) to backup
- storage: Target storage
- mode: "snapshot", "suspend", or "stop"
- compress: 0-9
- remove: Number of backups to keep
- notification-target: Where to send notifications

# Update job
PUT /cluster/jobs/{id}

# Delete job
DELETE /cluster/jobs/{id}

# Get job execution log
GET /cluster/jobs/{id}/log
```

**Cron Expression Examples:**
- `"0 2 * * *"`: Daily at 2 AM
- `"0 0 * * 0"`: Weekly on Sunday midnight
- `"0 */6 * * *"`: Every 6 hours
- `"0 3 1 * *"`: Monthly on 1st at 3 AM

### 6. Permission Management

**Users:**
```bash
# List users
GET /access/users

# Create user
POST /access/users
Parameters:
- userid: User ID (e.g., "john@pam" or "jane@pve")
- password: User password
- groups: Comma-separated group list
- comment: Description
- enable: 1 or 0
- expire: Account expiration (timestamp)

# Update user
PUT /access/users/{userid}

# Delete user
DELETE /access/users/{userid}
```

**Groups:**
```bash
# List groups
GET /access/groups

# Create group
POST /access/groups
Parameters:
- groupid: Group name
- comment: Description

# Delete group
DELETE /access/groups/{groupid}
```

**Roles:**
```bash
# List roles
GET /access/roles

# Create custom role
POST /access/roles
Parameters:
- roleid: Role name
- privileges: Comma-separated list of permissions
  - Common: VM.Allocate, VM.Audit, VM.Config.*, VM.Console, VM.Clone
  - Admin: Administrator (all permissions)
  - NoAccess: No permissions

# Built-in roles: Administrator, PVEAdmin, PVEUser, PVEVMUser, PVETemplateUser, NoAccess
```

**ACLs (Access Control):**
```bash
# List ACLs
GET /access/acl

# Create ACL rule
PUT /access/acl
Parameters:
- path: Resource path (e.g., "/vms/100", "/pool/production", "/")
- roles: Role name(s)
- users: User ID(s) (optional)
- groups: Group name(s) (optional)
- propagate: 1 to apply to children

# Examples:
# Grant user admin on VM 100
path: "/vms/100", users: "john@pam", roles: "Administrator"

# Grant group access to pool
path: "/pool/production", groups: "developers", roles: "PVEVMUser"

# Remove ACL
DELETE /access/acl?path={path}&users={userid}&roles={role}
```

**Pools:**
```bash
# List pools
GET /pools

# Create pool
POST /pools
Parameters:
- poolid: Pool name
- comment: Description

# Update pool (add/remove VMs)
PUT /pools/{poolid}
Parameters:
- vms: "100,101,102" (replaces current list)
- members: Array of objects with type and id

# Delete pool
DELETE /pools/{poolid}
```

### 7. Notifications (Webhooks)

Configure notifications for automation workflows.

```bash
# Get notification endpoints
GET /cluster/notifications/endpoints

# Create webhook endpoint
POST /cluster/notifications/endpoints
Parameters:
- name: Endpoint name
- type: "gotify" or "webhook"
- server: Server URL
- token: Authentication token
- comment: Description
- disable: 0 or 1

# Test notification
POST /cluster/notifications/endpoints/{name}/test

# Get notification targets (who receives what)
GET /cluster/notifications/targets

# Create notification target
POST /cluster/notifications/targets
Parameters:
- name: Target name
- endpoint: Endpoint name
- severity: "info", "notice", "warning", "error", "unknown"

# Get notification matchers (filter rules)
GET /cluster/notifications/matchers
```

**Notification Events:**
- Backup jobs: `vzdump`, `vzrestore`
- Replication: `vzrep`
- HA events: Resource migration, failover
- System: Updates, errors

### 8. Replication

Replicate VM disks to another node for disaster recovery.

```bash
# List replication jobs
GET /nodes/{node}/replication

# Create replication job
POST /nodes/{node}/replication
Parameters:
- id: Job ID (optional)
- target: Target node name
- vmid: VM ID to replicate
- schedule: Cron expression (default: every 15 min)
- rate: Speed limit (MB/s, 0 = unlimited)
- remove_job: Remove job if VM removed

# Get replication status
GET /nodes/{node}/replication/{id}/status

# Run replication now
POST /nodes/{node}/replication/{id}/run_now

# Delete replication job
DELETE /nodes/{node}/replication/{id}
```

### 9. Firewall

Host and VM-level firewall configuration.

**Host Firewall:**
```bash
# Get host firewall rules
GET /nodes/{node}/firewall/rules

# Create host rule
POST /nodes/{node}/firewall/rules
Parameters:
- type: "in" or "out"
- action: "ACCEPT", "DROP", "REJECT"
- macro: Predefined service (e.g., "SSH", "HTTP", "HTTPS")
- source/dest: IP/CIDR
- dport: Destination port(s)
- proto: Protocol (tcp, udp, icmp)
- enable: 0 or 1
- comment: Description

# Get firewall options
GET /nodes/{node}/firewall/options

# Update options
PUT /nodes/{node}/firewall/options
Parameters:
- enable: 0 or 1
- policy_in: Default input policy
- policy_out: Default output policy
```

**VM Firewall:**
```bash
# Get VM firewall rules
GET /nodes/{node}/qemu/{vmid}/firewall/rules

# Create VM rule
POST /nodes/{node}/qemu/{vmid}/firewall/rules
Parameters:
- type, action, macro, source, dest, dport, proto, enable, comment

# Get VM firewall aliases (IP groups)
GET /nodes/{node}/qemu/{vmid}/firewall/aliases

# Create alias
POST /nodes/{node}/qemu/{vmid}/firewall/aliases
Parameters:
- name: Alias name
- cidr: IP/CIDR or IP range

# Get firewall logs
GET /nodes/{node}/qemu/{vmid}/firewall/log
```

**Security Groups:**
```bash
# List security groups
GET /cluster/firewall/groups

# Create security group
POST /cluster/firewall/groups
Parameters:
- group: Group name
- comment: Description

# Add rules to security group
POST /cluster/firewall/groups/{group}
```

### 10. Storage Configuration

**Storage Types:**

| Type | Description | Common Options |
|------|-------------|----------------|
| `dir` | Directory on local filesystem | path, prune-backups |
| `lvm` | LVM logical volumes | vgname, base, safe-remove |
| `lvmthin` | LVM thin provisioning | vgname, thinpool |
| `zfspool` | ZFS pool | pool, sparse, blocksize |
| `nfs` | NFS share | server, export, options |
| `cifs` | SMB/CIFS share | server, share, username, password |
| `iscsi` | iSCSI target | portal, target |
| `cephfs` | CephFS | monhost, fs-name, userid |
| `rbd` | Ceph RBD | monhost, pool, userid |
| `glusterfs` | GlusterFS | server, volume, transport |

**Storage Operations:**
```bash
# List storage
GET /storage

# Get storage configuration
GET /storage/{storage}

# Create storage
POST /storage
Parameters:
- storage: Storage ID
- type: Storage type (dir, lvm, zfspool, nfs, etc.)
- content: Allowed content types (rootdir,images,iso,vztmpl,backup)
- nodes: Nodes that can use this storage
- [type-specific options]

# Update storage
PUT /storage/{storage}

# Delete storage
DELETE /storage/{storage}

# Get storage status
GET /nodes/{node}/storage/{storage}/status
```

### 11. Certificate Management

```bash
# Get current certificate info
GET /nodes/{node}/certificates/acme/certificate

# Get ACME account info
GET /nodes/{node}/certificates/acme/account

# List ACME plugins
GET /cluster/acme/plugins

# Create ACME plugin (for DNS challenge)
POST /cluster/acme/plugins
Parameters:
- id: Plugin name
- type: Plugin type (e.g., "dns_cf" for Cloudflare)
- data: Plugin-specific data (API keys, etc.)

# Order certificate
POST /nodes/{node}/certificates/acme/certificate
Parameters:
- force: 1 to renew even if valid
- restart: 1 to restart proxy after
```

### 12. Node Maintenance

```bash
# Get node subscription info
GET /nodes/{node}/subscription

# Upload subscription key
POST /nodes/{node}/subscription

# Get apt updates available
GET /nodes/{node}/apt/versions

# Run apt update
POST /nodes/{node}/apt/update

# Run apt upgrade
POST /nodes/{node}/apt/upgrade

# Get system log
GET /nodes/{node}/syslog

# Get support dump (diagnostics)
GET /nodes/{node}/report

# Start backup upload to Proxmox (support only)
POST /nodes/{node}/report
```

## References

- [Proxmox VE API Documentation](https://pve.proxmox.com/wiki/Proxmox_VE_API)
- [API Explorer](https://pve.proxmox.com/pve-docs/api-viewer/)
- [pvesh man page](https://pve.proxmox.com/pve-docs/pvesh.1.html)
- [HA Manager](https://pve.proxmox.com/wiki/High_Availability)
- [PCI Passthrough](https://pve.proxmox.com/wiki/PCI_Passthrough)
- [Backup and Restore](https://pve.proxmox.com/wiki/Backup_and_Restore)
- [Firewall](https://pve.proxmox.com/wiki/Firewall)
