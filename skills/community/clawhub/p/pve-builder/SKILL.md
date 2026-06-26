---
name: pve-builder
description: Proxmox VE VM builder with cloud-init automation, config-driven hardware defaults, validation, and static IP support
version: 1.0.10
author: mbojer
permissions:
  - shell
  - file_read
  - file_write
  - http_request
tools:
  - ssh_keygen
  - bash
  - file_operations
  - web_search
---

# CRITICAL: Agent Access Limitations

## YOU DO NOT HAVE ACCESS TO PROXMox

Agent runs on your local machine - NOT on Proxmox

Forbidden:
- Try to run qm commands
- Try to run pvesh commands
- Check storage availability
- Verify VM creation
- Access Proxmox API

Must Do:
- Output commands as text for user to copy/paste
- Tell user which node to SSH to
- Store keys locally in a configurable directory (default: ~/.ssh/pve-builder/)
- Never claim to create VMs
- Use web search for specs validation

---

# PVE Builder Skill

## Overview

Generates Proxmox VM creation commands with cloud-init configuration, SSH key management, and optional data disks. All hardware defaults are config-driven via `pve-env.md`.

**IMPORTANT:** Commands are output as text for you to copy/paste into Proxmox shell. The agent does NOT execute any Proxmox commands.

---

## Environment Setup

- **Config file:** `pve-env.md` in the skill directory
- **Ignored from git:** `.gitignore` excludes `pve-env.md`

### Critical Configuration Keys (pve-env.md)

| Section | Keys | Purpose |
|---------|------|---------|
| **Proxy** | `Proxy Required`, `HTTP Proxy`, `HTTPS Proxy`, `Proxy CA Certificate` | Network proxy for apt inside VMs |
| **SSH** | `Default User`, `Key Path`, `Key Type` | Default SSH user, key storage location, key type |
| **Network** | `Default Bridge`, `Default VLAN`, `DNS Server`, `Use DHCP Default`, `Network Interface` | Default network settings and interface type |
| **Storage** | `Default Storage`, `Template Path`, `Default OS Disk Size`, `Auto-Format Data Disks`, `Data Disk Interface`, `Default Cloud Image` | Storage defaults and cloud image path |
| **Node** | `Default Node`, `BIOS Type`, `Machine Type`, `CPU Type`, `OS Type`, `SCSI Controller`, `Onboot` | Hardware defaults for VM creation |
| **Workload Presets** | Preset table (RAM/CPU/Disk) | Recommended specs per workload type |
| **Package Defaults** | `Package Update`, `Base Packages` | Always-installed package list |

## Agent Workflow

The workflow uses **section-based numbered prompts** with continuous numbering across sections:

```
=== VM Specs ===
1. CPU cores  2. CPU sockets  3. RAM in GB  4. OS disk size

=== Network ===
5. Bridge  6. VLAN  7. DHCP?
  [if static:] 8. IP  9. Gateway  10. DNS

=== User & Disks ===
11. SSH user  12. Add data disks?  13. Format?  14. Count  15.x: Disk sizes
15. Proxy?  16. Extra packages  17. SSH key directory
```

Steps:
1. Load `pve-env.md` (error if missing)
2. Ask cloud image path (default from config: `Template Path` + `Default Cloud Image`)
3. Ask Proxmox node (default from config)
4. **Validate storage/bridge/image** (see Validation section below)
5. Ask VM name
6. Software lookup (name or URL) → web search for RAM/CPU recommendations (or manual)
7. Prompt specs (numbered prompts: cores, sockets, RAM, OS disk)
8. Prompt network (bridge, VLAN, DHCP vs static)
9. Static IP details (only if no DHCP)
10. Prompt SSH username
11. Prompt data disks (count, sizes, formatting option)
12. Proxy configuration (yes/no/change)
13. Extra apt packages
14. SSH key directory (default from config)
15. **Password setup** — **always generate** a random password via `openssl rand -base64 12 | tr -d '/+=' | head -c16`. Use this in `chpasswd`. If the user explicitly provides a password, use theirs instead. Always show the password in the final output summary.
16. Generate SSH key (unique ed25519 per VM)
17. Show summary & confirm
18. **VMID auto-detection** — Ask the user to run `pvesh get /cluster/nextid` on the Proxmox node and paste back the result. Use that VMID in all generated commands. Never hardcode a VMID — always get the next ID from the cluster. Add a `# Replace VMID=... if already taken` comment in the output.
19. Build cloud-init user-data YAML (packages, proxy, data disk formatting)
20. **Pre-flight validation** (see Command Pre-flight Validation below) — generate commands internally, validate, fix errors, then present
21. Generate and display the final verified commands in two sections: **Setup commands** (create VM through `qm start`) and **Post-boot cleanup** (delete the snippets YAML — only run after the VM is verified up).
22. Optional: save commands to file
22. Show SSH key path and chmod reminder

## Validation

Before generating commands, the agent validates that the target storage, bridge, and cloud image exist on the Proxmox node.

### Cache System
- **Cache file:** `~/.pve-builder/validation.json`
- **Valid for:** 24 hours
- **Cache invalidated if:** node, storage, or bridge values change
- **On cache hit:** validation is skipped if all checks passed

### Validation Process
If no valid cache exists, the agent shows these commands for the user to run on the Proxmox node:

```bash
echo "=== Storage ==="; pvesm status
echo "=== Bridge ==="; ip -br link show
echo "=== Image ==="; ls -la <image-path>
echo "=== END ==="
```

Results are parsed:
- **Storage:** Checks if configured storage name exists in `pvesm status`
- **Bridge:** Verifies bridge interface is present and UP
- **Image:** Confirms cloud image file exists at path

**On failure:** Agent aborts and reports which check(s) failed.
**On success:** Results are cached with node/storage/bridge/timestamp.

## Notes

- Custom cloud-init user-data is written to `/var/lib/vz/snippets/<VMNAME>-user-data.yaml` and attached via `--cicustom "user=local:snippets/<VMNAME>-user-data.yaml"`. The `local:snippets/` storage path maps to `/var/lib/vz/snippets/` on the Proxmox node. **Never** use `/var/lib/vz/template/cloud-init/` — that directory is not a recognized Proxmox snippets storage target.
- **`--cicustom` reads the snippets file at every boot.** The snippets YAML must exist on the node when the VM starts — cloud-init won't apply without it. **Do NOT delete the snippets file before the first boot.**
- **Always include `mkdir -p /var/lib/vz/snippets`** at the top of the generated commands.
- **After setting `--ide2` and `--citype`, add `--cicustom`** to wire the user-data: `qm set $VMID --cicustom "user=local:snippets/${VMNAME}-user-data.yaml"`.
- **After `--cicustom`, regenerate the cloud-init drive** before starting: `qm cloudinit update $VMID`.
- **ssh_pwauth: set `true` when a password is configured** (so the password actually works over SSH). Set `false` only for SSH-key-only VMs.
- The command to get the next VMID is provided as a hint; the agent does not run Proxmox commands
- SSH keys are stored locally in the configured directory (default: `~/.ssh/pve-builder/`)
- Generated commands include cleanup steps at the end: lists cloud-init YAML files for review, then removes the current VM's file. **IMPORTANT:** The cleanup step (rm snippets YAML) must NOT use `set -e` or be in the main command block. It should be in a separate "Post-boot" section that runs only after the VM is verified running and cloud-init applied. If the user deletes the YAML before the first boot, cloud-init fails silently.
- **Always include `echo "VMID: <id>"` in the verify/final section** so the user has the VMID referenced

## Command Pre-flight Validation

**Never present commands to the user without running this validation first.** Generate → validate → fix → present.

### Phase 1: Internal Draft

Build the complete command set internally (do not show yet).

### Phase 2: Parameter Verification Script

Generate a small bash validation script, set the variables to match the VM specs, and run it locally with `exec`. If it fails, fix the draft and re-run until it passes. Only then show the commands.

```bash
#!/bin/bash
# Pre-flight: verify parameters match intended spec
# SET THESE to match the VM being built:
VMID="1024"; VMNAME="MB-TBD"; RAM_MB="12288"; CORES="2"; SOCKETS="1"
OS_DISK_SIZE="25G"; BRIDGE="vmbr0"; VLAN_TAG="160"; STORAGE="Data"
IMAGE="/mnt/pve/ISO/template/iso/ubuntu-24.04-server-cloudimg-amd64.img"
CITYPE="nocloud"; VM_GB="12"
PASS=true
# RAM must be multiple of 256
(( RAM_MB % 256 != 0 )) && { echo "FAIL: RAM $RAM_MB not mult. of 256"; PASS=false; }
# Cores/sockets positive
(( CORES < 1 )) && { echo "FAIL: CORES < 1"; PASS=false; }
(( SOCKETS < 1 )) && { echo "FAIL: SOCKETS < 1"; PASS=false; }
# VLAN in valid range
(( VLAN_TAG < 1 || VLAN_TAG > 4094 )) && { echo "FAIL: VLAN out of range"; PASS=false; }
# Disk size format
[[ ! "$OS_DISK_SIZE" =~ ^[0-9]+[G]$ ]] && { echo "FAIL: OS_DISK_SIZE format"; PASS=false; }
# Valid CITYPE
case "$CITYPE" in nocloud|configdrive2|opennebula) ;; *) echo "FAIL: CITYPE=$CITYPE invalid"; PASS=false ;; esac
# Image path not empty
[ -z "$IMAGE" ] && { echo "FAIL: IMAGE path empty"; PASS=false; }
# RAM_MB must match VM_GB * 1024
EXPECTED_MB=$((VM_GB * 1024))
[ "$RAM_MB" -ne "$EXPECTED_MB" ] && { echo "FAIL: RAM_MB=$RAM_MB != VM_GB=$VM_GB (expected $EXPECTED_MB)"; PASS=false; }
$PASS && echo "PREFLIGHT OK" || { echo "PREFLIGHT FAILED"; exit 1; }
```

The agent:
1. Writes this script to a temp file with actual VM values
2. Runs it with `exec bash /tmp/preflight.sh`
3. If it fails, fixes values, re-runs
4. Only presents commands when `PREFLIGHT OK`

### Checklist (run after pre-flight script passes)

- [ ] Shebang/header with VM name, VMID, node
- [ ] `mkdir -p /var/lib/vz/snippets`
- [ ] User-data written to `/var/lib/vz/snippets/$VMNAME-user-data.yaml`
- [ ] `ssh_pwauth: true` if password configured, `false` if SSH-only
- [ ] `--citype nocloud` (NOT `cloud-config`)
- [ ] `qm create` with no `--node`
- [ ] `qm importdisk` references correct image
- [ ] `--scsi0` attaches imported disk
- [ ] `--ide2 <storage>:cloudinit` attached
- [ ] `--cicustom "user=local:snippets/${VMNAME}-user-data.yaml"` added
- [ ] `qm cloudinit update $VMID` after cicustom set
- [ ] **`--ipconfig0 ip=dhcp`** (DHCP) **or** `--ipconfig0 ip=<CIDR>,gw=<GW>` (static) — this actually configures the network inside the guest
- [ ] `--net0 virtio,bridge=<bridge>,tag=<vlan>`
- [ ] `--boot order=scsi0`
- [ ] `qm resize $VMID scsi0 <size>` after import
- [ ] `echo "VMID: $VMID"` in output
- [ ] `qm config $VMID` for review
- [ ] Cleanup note at end (remove snippets YAML)
- [ ] No typos: `qm` not `vm`, `$VMID` not `$VM`
- [ ] Variable names consistent throughout

## Networking

### DHCP (default)
Simple network config: `qm set --ipconfig0 ip=dhcp`

**Do NOT use `--nameserver` with DHCP** — let the DHCP lease provide DNS. Only set `--nameserver` when using static IP.

### Static IP
When DHCP is declined, the agent prompts for:
- IP address with CIDR (e.g., `10.0.12.50/24`)
- Gateway (e.g., `10.0.12.1`)
- DNS servers (comma-separated, default from config)

Generated commands:
- `qm set --ipconfig0 ip=10.0.12.50/24,gw=10.0.12.1`
- `qm set --nameserver 8.8.8.8`

## Package Installation

All VMs get base packages from `pve-env.md` (deduplicated with any extra packages).

If proxy is configured, apt proxy is automatically enabled in cloud-init.

## Security

- **Passwords: ALL VMs get a random password by default.** Generate with: `openssl rand -base64 12 | tr -d '/+=' | head -c16`. Use in both `chpasswd` in cloud-init YAML and embed in command output. If the user provides an explicit password, use theirs instead — but always show it back in output so they have it. Set `ssh_pwauth: true` unless the user explicitly says SSH-only.
- SSH keys: Unique per VM, ed25519, no passphrase
- pve-env.md: chmod 600, excluded from git
- Private keys: chmod 600, never in commands
- Public keys: Safe to embed in commands
- SSH key directory: configurable via `Key Path` in pve-env.md (default `~/.ssh/pve-builder`); permissions 700 on base dir

## Version History

- **1.0.10:** Add `--cicustom` warning: snippets file must survive first boot. Split output into Setup and Post-boot sections. VMID auto-detection via `cluster/nextid`. Fix workflow numbering.
- **1.0.9:** Always generate random password per-VM (`openssl rand -base64 12`), user override option, always display password in output
- **1.0.7:** Fix custom user-data routing: `/var/lib/vz/snippets/` + `--cicustom`, `qm cloudinit update`, `ssh_pwauth` conditional
- **1.0.5:** `mkdir -p` for required dirs in generated commands, command self-review checklist, `--citype nocloud` enforced, automatic disk resize after importdisk
- **1.0.3:** Full config decoupling (all hardware defaults from pve-env.md), storage/bridge validation with 24h cache, static IP support, continuous numbered prompts with section headers, SSH key path not echoed in summary, duplicate package removal, direct VMID input, cloud-init cleanup commands
- **1.0.2:** Added URL analysis, web search validation, simplified proxy flow
- **1.0.1:** Added explicit access limitation warnings
- **1.0.0:** Initial release

---

_This file is yours to evolve. As you learn who you are, update it._
