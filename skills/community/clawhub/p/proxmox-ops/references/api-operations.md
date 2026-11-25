# Proxmox API — common operations (curl + jq)

Uses `$AUTH` and `$PROXMOX_HOST` from the Auth Header section of SKILL.md.

### Cluster & Nodes

```bash
# Cluster status
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/cluster/status" | jq

# List nodes with CPU/memory
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes" | jq '.data[] | {node, status, cpu, mem: (.mem/.maxmem*100|round)}'
```

### List VMs & Containers

```bash
# Cluster-wide (all VMs + LXC)
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/cluster/resources?type=vm" | jq '.data[] | {node, vmid, name, type, status}'

# VMs on specific node
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu" | jq '.data[] | {vmid, name, status}'

# LXC on specific node
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/lxc" | jq '.data[] | {vmid, name, status}'
```

### VM/Container Control

```bash
# Start / Stop / Shutdown / Reboot
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/status/start"
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/status/stop"
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/status/shutdown"
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/status/reboot"

# For LXC: replace /qemu/ with /lxc/
```

### Snapshots

**⚠️ vmstate parameter:** Do NOT include `vmstate=1` unless you specifically need to preserve running process state.
- `vmstate=1` freezes the VM and causes heavy I/O — can starve other guests on the same node
- For pre-change backups, omit vmstate (defaults to disk-only, no I/O spike)

```bash
# List snapshots
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/snapshot" | jq

# Create snapshot (disk-only, safe)
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/snapshot" \
  -d "snapname=snap1" -d "description=Before update"

# Rollback
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/snapshot/{snapname}/rollback"

# Delete snapshot
curl -ks -X DELETE -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/snapshot/{snapname}"
```

### Disk Resize

```bash
# Get current disk config
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/config" | jq

# Resize disk (use absolute size, NOT relative — +10G fails regex validation)
curl -ks -X PUT -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/resize" \
  -d "disk=scsi0" -d "size=20G" | jq
```

**Post-resize inside VM:**
1. Fix GPT: `parted /dev/sda print` → Fix
2. Resize partition: `parted /dev/sda resizepart 3 100%`
3. If LVM: `pvresize /dev/sda3 && lvextend -l +100%FREE /dev/vg/root`
4. Resize filesystem: `resize2fs /dev/mapper/vg-root` (ext4) or `xfs_growfs /` (xfs)

### Guest Agent (IP Discovery)

```bash
# Get VM network interfaces (requires qemu-guest-agent)
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/qemu/{vmid}/agent/network-get-interfaces" | \
  jq -r '.data.result[] | select(.name != "lo") | .["ip-addresses"][] | select(.["ip-address-type"] == "ipv4") | .["ip-address"]' | head -1
```

Always query guest agent for current IP — don't hardcode IPs.

### Storage & Backups

```bash
# List storage
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/storage" | jq '.data[] | {storage, type, active, used_fraction: (.used/.total*100|round|tostring + "%")}'

# List backups
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/storage/{storage}/content?content=backup" | jq

# Start backup
curl -ks -X POST -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/vzdump" \
  -d "vmid={vmid}" -d "storage={storage}" -d "mode=snapshot"
```

### Tasks

```bash
# Recent tasks
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/tasks" | jq '.data[:10] | .[] | {upid, type, status, user}'

# Task log
curl -ks -H "$AUTH" "$PROXMOX_HOST/api2/json/nodes/{node}/tasks/{upid}/log" | jq -r '.data[].t'
```
