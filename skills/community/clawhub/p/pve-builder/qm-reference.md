# ============================================================
# Proxmox QM Command Reference
# ============================================================
# For use with pve-builder skill
# ============================================================

# CRITICAL LIMITATIONS

## Node Parameter

DO NOT USE --node parameter with qm commands

# Wrong:
qm create 100 --node MB-PVE-03 --name test

# Correct:
# SSH to the node first, then run qm without --node
ssh root@MB-PVE-03
qm create 100 --name test

# Reason: qm is a node-local command, not a cluster command

## Access Requirements

- Run qm commands on the Proxmox node itself
- No remote execution supported
- pve-builder agent outputs commands for you to copy/paste
- Agent cannot access Proxmox directly

# Common QM Commands

## Create VM

qm create <VMID> \
  --name <VM-NAME> \
  --memory <MEMORY_MB> \
  --cores <CORES> \
  --sockets <SOCKETS> \
  --cpu <CPU_TYPE> \
  --machine <MACHINE_TYPE> \
  --bios <BIOS_TYPE> \
  --ostype l26 \
  --scsihw virtio-scsi-pci \
  --onboot 0

# Note: --cpu, --machine, --bios, --ostype values are read from pve-env.md

## Import Disk (Cloud Image)

qm importdisk <VMID> <PATH_TO_IMAGE> <STORAGE> --format raw
qm set <VMID> --scsi0 <STORAGE>:vm-<VMID>-disk-0,discard=on,ssd=1
qm resize <VMID> --scsi0 <SIZE>

## Network Configuration

### DHCP
qm set <VMID> --net0 <INTERFACE_TYPE>,bridge=<bridge>,tag=<VLAN>
qm set <VMID> --ipconfig0 ip=dhcp

### Static IP
qm set <VMID> --net0 <INTERFACE_TYPE>,bridge=<bridge>,tag=<VLAN>
qm set <VMID> --ipconfig0 ip=<IP/CIDR>,gw=<GATEWAY>
qm set <VMID> --nameserver <DNS1> <DNS2> ...

## Cloud-Init Setup

# Attach cloud-init drive
qm set <VMID> --ide0 <STORAGE>:cloudinit

# Configure network
qm set <VMID> --ipconfig0 ip=dhcp
# or static: qm set <VMID> --ipconfig0 ip=10.0.12.50/24,gw=10.0.12.1

# Set user and SSH key (either sshkeys OR cipassword, not both)
qm set <VMID> --ciuser <USER>
qm set <VMID> --sshkeys "ssh-ed25519 AAAAC...PUBLIC-KEY-CONTENT..."

# Optional: DNS (for static IP)
qm set <VMID> --nameserver 8.8.8.8

# Optional: Custom user-data (proxy, packages, disk formatting)
qm set <VMID> --cicustom user=/path/to/user-data.yaml

# Update cloud-init after changes
qm cloudinit update <VMID>

# Note: cloud-init runs on first boot automatically
# No need for --ciupgrade if proxy is required

## Boot Order and Settings

qm set <VMID> --boot order=scsi0
qm set <VMID> --agent enabled=1
qm set <VMID> --tablet 0
qm set <VMID> --onboot 0

## Add Data Disks

# SCSI disk (recommended for Linux, default interface)
qm set <VMID> --scsi1 <STORAGE>:20G,discard=on,ssd=1

# VirtIO disk (alternative)
qm set <VMID> --virtio1 <STORAGE>:10G,discard=on

# NVMe disk (high performance)
qm set <VMID> --nvme1 <STORAGE>:50G,discard=on

# Note: Data disk interface type is configurable via `Data Disk Interface` in pve-env.md.
# Default: scsi. Each disk is numbered sequentially (--scsi1, --scsi2, --scsi3, etc.)

## Data Disk Formatting (via cloud-init)

When data disks are added with auto-format enabled, the cloud-init user-data YAML
includes mkfs and mount commands. Example for 2 disks (sdb, sdc):

# In user-data.yaml runcmd section:
runcmd:
  - mkfs.ext4 /dev/sdb
  - mkfs.ext4 /dev/sdc
  - mkdir -p /data
  - mount /dev/sdb /data
  - echo "/dev/sdb /data ext4 defaults 0 2" >> /etc/fstab

# Device mapping depends on interface type:
# - scsi/ide → /dev/sdX
# - virtio   → /dev/vdX
# - nvme     → /dev/nvme0nX

## VM Management

# Start VM
qm start <VMID>

# Stop VM
qm stop <VMID>

# Restart VM
qm restart <VMID>

# Shutdown VM (graceful)
qm shutdown <VMID>

# Delete VM
qm destroy <VMID>

# View VM config
qm config <VMID>

# List all VMs
qm list

# Cloud-Init Configuration Reference

## User-Data YAML Template

#cloud-config

# Apt Proxy (if needed)
apt:
  proxy: http://proxy.yourdomain.local:3128
  https_proxy: http://proxy.yourdomain.local:3128

# Packages (install on first boot)
package_update: true
package_upgrade: false
packages:
  - qemu-guest-agent
  - nano
  - curl
  - wget
  - btop
  - bind9-dnsutils
  - iputils-ping

# Proxy CA Certificate (if needed)
ca_certs:
  remove_defaults: false
  trusted:
    - |
      -----BEGIN CERTIFICATE-----
      ...your-proxy-ca-certificate-content...
      -----END CERTIFICATE-----

# Run commands on first boot
runcmd:
  - systemctl enable qemu-guest-agent
  - systemctl start qemu-guest-agent
  - echo "Cloud-init complete at $(date)" >> /var/log/cloud-init-complete.log

# Format and mount data disks (if enabled)
runcmd:
  - mkfs.ext4 /dev/sdb    # First data disk (scsi)
  - mkdir -p /data
  - mount /dev/sdb /data
  - echo "/dev/sdb /data ext4 defaults 0 2" >> /etc/fstab

  - mkfs.ext4 /dev/sdc    # Second data disk (scsi)

# Data disk device mapping:
#   scsi → /dev/sdX (sdb, sdc, sdd...)
#   virtio → /dev/vdX (vdb, vdc, vdd...)
#   nvme → /dev/nvme0nX (nvme0n1, nvme0n2, nvme0n3...)

## Network-Config YAML Template

# Version 2 (Default - DHCP)
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1

# Static IP
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 10.0.12.50/24
      gateway4: 10.0.12.1
      nameservers:
        addresses:
          - 8.8.8.8

# Note: qm set --nameserver handles DNS. Custom network-config can override.

# Disk Interface Comparison

| Interface | Max Disks | Performance | Use Case |
|-----------|-----------|-------------|----------|
| scsi0 - scsi30 | 31 | Best | Linux VMs (OS + data) |
| virtio0 - virtio15 | 16 | Best | Linux VMs (alternative) |
| sata0 - sata5 | 6 | Good | CD-ROM, slower disks |
| ide0 - ide3 | 4 | Slow | Cloud-init only |
| nvme0 - nvme15 | 16 | Best | High-performance storage |

# Proxy Considerations

## Apt Proxy Configuration

# In cloud-init user-data:
apt:
  proxy: http://proxy.yourdomain.local:3128
  https_proxy: http://proxy.yourdomain.local:3128

## CA Certificate Installation

# In cloud-init user-data:
ca_certs:
  remove_defaults: false
  trusted:
    - |
      -----BEGIN CERTIFICATE-----
      ...your-proxy-ca-certificate-content...
      -----END CERTIFICATE-----
runcmd:
  - update-ca-certificates
  - apt update

# Validation Commands

## On Proxmox Node

# Check VM configuration
qm config <VMID>

# Check cloud-init configuration
qm cloudinit dump <VMID>

# Check task log
pvesh get /nodes/[NODE]/tasks

# List all VM
qm list

# Check storage
pvesm status

## On VM After Boot

# Check cloud-init logs
cat /var/log/cloud-init-output.log
cat /var/log/cloud-init.log

# Check packages installed
apt list --installed | grep -E "qemu|nano|curl|wget|btop"

# Check proxy configuration
env | grep proxy

# Check data disk mounted
df -h
ls -la /data

# Troubleshooting

## Common Issues

| Issue | Solution |
|-------|----------|
| qm: command not found | Run commands on Proxmox node, not locally |
| --node: invalid option | Remove --node, SSH to target node first |
| Cloud-init not running | Verify cloud-init device attached (ide0) and custom user-data (cicustom) |
| SSH access denied | Check private key permissions (chmod 600) |
| Data disk not mounted | Check cloud-init runcmd executed in logs |
| Proxy failing | Verify CA Certificate is valid and apt proxy is set |
| VM not starting | Check boot order (boot order=scsi0) |
| Static IP not applied | Verify --ipconfig0 and --nameserver are both set |
| Network unreachable | Verify bridge name and VLAN tag match Proxmox config |
| Validation failed | Run pvesm status / ip link to check storage and bridge exist |

## USEFUL TIPS

## Recommended Workflow

1. Configure pve-env.md with your defaults (bridge, storage, node, SSH key path)
2. Run pve-builder to generate VM creation commands
3. Review validation output (storage/bridge/image checks)
4. SSH to Proxmox node: ssh root@[NODE]
5. Paste commands into Proxmox shell
6. Wait for VM to start and cloud-init to complete
7. SSH to VM: ssh -i <SSH_KEY_DIR>/[VM-NAME] [USER]@[VM_IP]
8. Verify services and disk mounts

## Best Practices

- Always use SSH keys instead of passwords
- Generate unique SSH key per VM
- Store keys in a configurable directory (default: ~/.ssh/pve-builder/)
- Set private key permissions to chmod 600
- Never commit private keys or pve-env.md to git
- Use cloud-init for package installation
- Skip --ciupgrade if proxy is required
- Add data disks for application storage
- Keep --onboot = 0 (do not auto-start until verified)
- Remove cloud-init YAML files after deployment (cleanup in generated commands)

## Security Checklist

- [ ] SSH keys generated per VM (unique, ed25519)
- [ ] Private key permissions set to 600
- [ ] Private keys never in commands or git
- [ ] pve-env.md permissions set to 600
- [ ] .gitignore excludes pve-env.md
- [ ] Passwords not used in cloud-init

# ============================================================
# Last Updated: 2026-03-31
# ============================================================
