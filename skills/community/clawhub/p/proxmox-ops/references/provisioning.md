# Proxmox Provisioning Reference

Create, clone, template, and delete VMs and LXC containers.

## Table of Contents

- [Finding a Free Static IP](#finding-a-free-static-ip)
- [Create LXC Container](#create-lxc-container)
- [Create VM](#create-vm)
- [Clone VM/Container](#clone-vmcontainer)
- [Convert to Template](#convert-to-template)
- [Delete VM/Container](#delete-vmcontainer)
- [Available Templates & ISOs](#available-templates--isos)
- [Quick Reference](#quick-reference)

---

## Finding a Free Static IP

Before assigning a static IP to a new VM/LXC, check **all three** of these — any one alone misses cases:

### 1. Proxmox-managed IPs (the authoritative source for PVE-controlled assignments)

Cluster-wide enumeration of every IP set in a VM/LXC config. Catches **stopped** containers (which UniFi/ping miss).

```bash
# Quick: helper command (filter by subnet prefix)
pve.sh ips 10.10.20

# Or via raw API:
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/cluster/resources?type=vm" | \
  jq -r '.data[] | "\(.type) \(.vmid) \(.node)"' | \
while read -r typ vmid node; do
  if [[ "$typ" == "lxc" ]]; then
    fields='.net0,.net1,.net2,.net3'
  else
    fields='.ipconfig0,.ipconfig1,.ipconfig2,.ipconfig3'
  fi
  curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/$node/$typ/$vmid/config" | \
    jq -r ".data | $fields | select(. != null)" | \
    grep -oE 'ip=[0-9.]+' | sed "s|^|$vmid $typ |"
done | sort
```

### 2. DHCP / live ARP table (catches DHCP leases + currently-online statics)

Use UniFi/Mikrotik/pfSense client list, OPNsense leases, or an `arp-scan`/`nmap -sn` of the subnet.

### 3. Ping the candidate

Final sanity check from a host on the same VLAN. Free IPs typically return ~1/N packets at ~3000 ms latency (gateway sending ICMP host-unreachable after ARP fails); real hosts return 100% replies at normal RTT.

```bash
ping -c 3 -W 500 <candidate-ip>
```

### What each source misses

| Source | Misses |
|--------|--------|
| **PVE config** | Guest-side static IPs (set inside the OS, not via cloud-init) — DCs, TrueNAS, hand-configured VMs |
| **DHCP/UniFi list** | **Stopped** LXCs/VMs that own a static reservation; offline hosts; static IPs configured guest-side that haven't checked in recently |
| **Ping** | Stopped hosts that own the IP; hosts that drop ICMP |

**Rule of thumb:** stopped LXC with a static `ip=` in its PVE config is the classic trap — invisible to ping and UniFi, visible only via PVE config enumeration.

---

## Create LXC Container

```bash
# Get next available VMID
NEWID=$(curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/cluster/nextid" | jq -r '.data')

# Create container
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/lxc" \
  -d "vmid=$NEWID" \
  -d "hostname=my-container" \
  -d "ostemplate=local:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst" \
  -d "storage=local-lvm" \
  -d "rootfs=local-lvm:8" \
  -d "memory=1024" \
  -d "swap=512" \
  -d "cores=2" \
  -d "net0=name=eth0,bridge=vmbr0,ip=dhcp" \
  -d "password=changeme123" \
  -d "start=1"
```

### LXC Parameters

| Param | Example | Description |
|-------|---------|-------------|
| vmid | 200 | Container ID |
| hostname | myct | Container hostname |
| ostemplate | local:vztmpl/debian-12-... | Template path |
| storage | local-lvm | Storage for rootfs |
| rootfs | local-lvm:8 | Root disk (8GB) |
| memory | 1024 | RAM in MB |
| swap | 512 | Swap in MB |
| cores | 2 | CPU cores |
| net0 | name=eth0,bridge=vmbr0,ip=dhcp | Network config |
| password | secret | Root password |
| ssh-public-keys | ssh-rsa ... | SSH keys (URL encoded) |
| unprivileged | 1 | Unprivileged container |
| start | 1 | Start after creation |

---

## Create VM

```bash
# Get next VMID
NEWID=$(curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/cluster/nextid" | jq -r '.data')

# Create VM
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu" \
  -d "vmid=$NEWID" \
  -d "name=my-vm" \
  -d "memory=2048" \
  -d "cores=2" \
  -d "sockets=1" \
  -d "cpu=host" \
  -d "net0=virtio,bridge=vmbr0" \
  -d "scsi0=local-lvm:32" \
  -d "scsihw=virtio-scsi-pci" \
  -d "ide2=local:iso/ubuntu-22.04.iso,media=cdrom" \
  -d "boot=order=scsi0;ide2;net0" \
  -d "ostype=l26"
```

### VM Parameters

| Param | Example | Description |
|-------|---------|-------------|
| vmid | 100 | VM ID |
| name | myvm | VM name |
| memory | 2048 | RAM in MB |
| cores | 2 | CPU cores per socket |
| sockets | 1 | CPU sockets |
| cpu | host | CPU type |
| net0 | virtio,bridge=vmbr0 | Network |
| scsi0 | local-lvm:32 | Disk (32GB) |
| ide2 | local:iso/file.iso,media=cdrom | ISO |
| ostype | l26 (Linux), win11 | OS type |
| boot | order=scsi0;ide2 | Boot order |

---

## Clone VM/Container

```bash
# Clone VM (full clone)
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/clone" \
  -d "newid=201" \
  -d "name=cloned-vm" \
  -d "full=1" \
  -d "storage=local-lvm"

# Clone LXC
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/lxc/{vmid}/clone" \
  -d "newid=202" \
  -d "hostname=cloned-ct" \
  -d "full=1" \
  -d "storage=local-lvm"
```

### Clone Parameters

| Param | Description |
|-------|-------------|
| newid | New VMID |
| name/hostname | New name |
| full | 1=full clone, 0=linked clone |
| storage | Target storage |
| target | Target node (for migration) |

---

## Convert to Template

```bash
# Convert VM to template (irreversible — VM must be stopped)
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/template"

# Convert LXC to template
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/lxc/{vmid}/template"
```

---

## Delete VM/Container

```bash
# Delete VM (must be stopped first)
curl -ks -X DELETE -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}"

# Delete LXC
curl -ks -X DELETE -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/lxc/{vmid}"

# Force delete with disk cleanup
curl -ks -X DELETE -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}?purge=1&destroy-unreferenced-disks=1"
```

---

## Available Templates & ISOs

```bash
# List available LXC templates
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/storage/local/content?content=vztmpl" | jq '.data[] | .volid'

# List ISOs
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/storage/local/content?content=iso" | jq '.data[] | .volid'

# Download template from Proxmox appliance repo
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/aplinfo" \
  -d "storage=local" \
  -d "template=debian-12-standard_12.2-1_amd64.tar.zst"

# Restore from backup
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu" \
  -d "vmid=300" \
  -d "archive=local:backup/vzdump-qemu-100-2024_01_01-12_00_00.vma.zst" \
  -d "storage=local-lvm"
```

---

## Quick Reference

| Action | Endpoint | Method |
|--------|----------|--------|
| Next ID | /cluster/nextid | GET |
| Create VM | /nodes/{node}/qemu | POST |
| Create LXC | /nodes/{node}/lxc | POST |
| Clone VM | /nodes/{node}/qemu/{vmid}/clone | POST |
| Clone LXC | /nodes/{node}/lxc/{vmid}/clone | POST |
| Template VM | /nodes/{node}/qemu/{vmid}/template | POST |
| Delete VM | /nodes/{node}/qemu/{vmid} | DELETE |
| Delete LXC | /nodes/{node}/lxc/{vmid} | DELETE |
| List templates | /nodes/{node}/storage/{s}/content?content=vztmpl | GET |
| List ISOs | /nodes/{node}/storage/{s}/content?content=iso | GET |
