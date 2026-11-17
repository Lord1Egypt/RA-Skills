---
name: single-gpu-passthrough
description: >-
  Comprehensive skill for the author's single-GPU passthrough setup: Fedora 44 bootc
  atomic host with Intel i5-12400F, NVIDIA RTX 2060 12GB (TU106), QEMU 10.2.2,
  libvirt 12.0.0, Wayland (niri on greetd). Covers hook scripts, kernel config,
  libvirt domain XML, virsh operations, and troubleshooting for single-GPU VFIO
  passthrough to a Win10 VM.
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
---

# Single GPU Passthrough — the author's Setup

## System Overview

| Component | Detail |
|-----------|--------|
| **Host OS** | Fedora 44 (bootc atomic — ostree-based, immutable root) |
| **Kernel** | 7.0.12-201.fc44.x86_64 |
| **CPU** | Intel i5-12400F (12th Gen Alder Lake, 6C/12T) |
| **GPU** | NVIDIA RTX 2060 12GB (TU106) — PCI 01:00.0 + HDMI Audio 01:00.1 |
| **NVIDIA Driver** | 610.43.02 |
| **Display** | greetd → dms-greeter → niri (Wayland compositor) |
| **QEMU** | 10.2.2 |
| **libvirt** | 12.0.0 (modular daemons) |
| **VM Name** | `win10` |
| **Boot** | UEFI (OVMF) |
| **Storage** | NVMe 238GB (boot), HDD 1.8TB (data: niabc NTFS / niaext ext4) |

## Hardware Topology

### IOMMU Groups
The GPU and its HDMI audio controller share a **clean IOMMU group** (Group 12):

- **pci_0000_01_00_0** — GPU (vendor 0x10de, product 0x1f03, class 0x030000)
- **pci_0000_01_00_1** — HDMI Audio (vendor 0x10de, product 0x10f9, class 0x040300)

Both devices must be passed together as they share IOMMU Group 12. They connect via PCI bridge at `0000:00:01.0`.

### Other Devices
- `03:00.0` — Realtek RTL8111H Gigabit Ethernet
- `04:00.0` — MAXIO NVMe SSD Controller

## Kernel Configuration

### Kernel Cmdline (bootc/ostree)
Kernel parameters are set via `rpm-ostree kargs` (NOT `/etc/default/grub` — bootc is immutable):

```bash
sudo rpm-ostree kargs \
  --append='intel_iommu=on' \
  --append='iommu=pt' \
  --append='rd.driver.blacklist=nouveau' \
  --append='modprobe.blacklist=nouveau' \
  --append='nvidia-drm.modeset=1'
```

**Current cmdline (from /proc/cmdline):**
```
intel_iommu=on iommu=pt rd.driver.blacklist=nouveau modprobe.blacklist=nouveau nvidia-drm.modeset=1
```

**IMPORTANT — bootc atomic context:** On a bootc/ostree system:
- `/etc` is writable (persists across updates)
- `/usr` is immutable (resets on each deployment update)
- Kernel params are applied via `rpm-ostree kargs` — add/remove requires a reboot
- To add: `sudo rpm-ostree kargs --append='new_param=value'`
- To remove: `sudo rpm-ostree kargs --delete='old_param=value'`
- To replace: `sudo rpm-ostree kargs --replace='old=value' --replace-to='new=value'`
- To view: `rpm-ostree kargs`

### modprobe.d /etc Configs
`/etc/modprobe.d/` is writable on bootc. The following reside there:
- **nvidia.conf** (performance profile): `NVreg_RegistryDwords`, `NVreg_EnableGpuFirmware`, `NVreg_DynamicPowerManagement`, `nvidia-drm modeset=1`
- **vhost.conf**: `max_mem_regions=509`

VFIO modules are **not** loaded at boot — they are loaded dynamically by the hook scripts on VM prepare.

### IOMMU Verification Commands

```bash
# Check IOMMU is enabled
dmesg | grep -i iommu
cat /proc/cmdline | grep -o 'intel_iommu\|iommu'

# Check IOMMU groups
for g in $(find /sys/kernel/iommu_groups/* -maxdepth 0 -type d | sort -V); do
  echo "IOMMU Group $(basename $g):"
  for d in $g/devices/*; do
    echo -n "  $(basename $d): "
    lspci -nns "$(basename $d)" 2>/dev/null || echo "unknown"
  done
done

# Via virsh
virsh nodedev-list --cap pci
virsh nodedev-dumpxml pci_0000_01_00_0  # GPU
virsh nodedev-dumpxml pci_0000_01_00_1  # HDMI Audio
```

## Hook Architecture

### Overview
The passthrough uses **libvirt qemu hooks** — scripts that fire on VM lifecycle events. Three scripts form the system:

1. **`/etc/libvirt/hooks/qemu`** — dispatcher: called by libvirt on VM prepare/release
2. **`~/.local/sbin/vfio-startup`** — detaches GPU from host, called on VM prepare
3. **`~/.local/sbin/vfio-teardown`** — reattaches GPU to host, called on VM release
4. **`libvirt-nosleep@.service`** — systemd inhibit sleep while VM runs

### File Locations (Deployed)

| Script | Deployed To | Purpose |
|--------|-------------|---------|
| qemu hook | `/etc/libvirt/hooks/qemu` | Dispatches startup/teardown per VM name |
| vfio-startup | `~/.local/sbin/vfio-startup` | Prepare phase: detach GPU |
| vfio-teardown | `~/.local/sbin/vfio-teardown` | Release phase: reattach GPU |
| inhibit service | `/etc/systemd/system/libvirt-nosleep@.service` | Prevents sleep while VM active |

**NOTE:** The repo's `install_hooks.sh` installs to `/usr/local/bin/` but The author modified the qemu hook to call `~/.local/sbin/` instead. Always check which paths are active before modifying.

### Script Sources
The source repo is at `~/projects/single-gpu-passthrough/` but the **deployed scripts have been customized** — they differ from the repo versions significantly.

### Libvirt Hook Lifecycle

The qemu hook receives **4 positional arguments**:

```
/etc/libvirt/hooks/qemu <vm_name> <operation> <sub-operation> <extra>
```

| Phase | When Called | Operation | Sub-Op |
|-------|-------------|-----------|--------|
| **Prepare** | Before libvirt resource labeling, before guest start | `prepare` | `begin` |
| **Start** | After labeling, before QEMU starts | `start` | `begin` |
| **Started** | After QEMU process started | `started` | `begin` |
| **Stopped** | Before libvirt restores labels | `stopped` | `end` |
| **Release** | After libvirt releases resources | `release` | `end` |

The domain XML is passed on **stdin** during all guest hook calls.

the author's hook uses **`prepare`** and **`release`** — the outermost lifecycle phases.

### qemu Hook (Dispatcher)
Path: `/etc/libvirt/hooks/qemu`

```bash
#!/bin/bash
OBJECT="$1"
OPERATION="$2"

if [[ $OBJECT == "win10" ]]; then
    case "$OPERATION" in
        "prepare")
            systemctl start libvirt-nosleep@"$OBJECT" 2>&1 | tee -a /var/log/libvirt/custom_hooks.log
            ~/.local/sbin/vfio-startup 2>&1 | tee -a /var/log/libvirt/custom_hooks.log
            ;;
        "release")
            systemctl stop libvirt-nosleep@"$OBJECT" 2>&1 | tee -a /var/log/libvirt/custom_hooks.log
            ~/.local/sbin/vfio-teardown 2>&1 | tee -a /var/log/libvirt/custom_hooks.log
            ;;
    esac
fi
```

**Key details:**
- Only activates for VM named `win10` (change this for different VM names)
- Calls the startup/teardown scripts
- Starts/stops the no-sleep inhibitor service
- All output is tee'd to `/var/log/libvirt/custom_hooks.log`

### vfio-startup (GPU Detach)

Path: `~/.local/sbin/vfio-startup`

**Execution flow:**
1. **Stop display server** — `systemctl stop greetd`, then `killall -9 niri qs zen kitty Xwayland pipewire wireplumber`
2. **Isolate to multi-user.target** — prevents systemd from restarting GUI services
3. **Unbind VT consoles** — `echo 0 > /sys/class/vtconsole/vtcon0/bind` and `vtcon1/bind`
4. **Unbind EFI framebuffer** — `echo efi-framebuffer.0 > /sys/bus/platform/drivers/efi-framebuffer/unbind`
5. **Unload NVIDIA kernel modules** — in order: `nvidia_uvm`, `nvidia_drm`, `nvidia_modeset`, `nvidia`, `i2c_nvidia_gpu`, `drm_kms_helper`
6. **Detach PCI devices via virsh**:
   - `virsh nodedev-detach pci_0000_01_00_0` (GPU)
   - `virsh nodedev-detach pci_0000_01_00_1` (HDMI Audio)
7. **Logs** to `/var/log/libvirt/vfio-startup.log` with `set -x` trace

**IMPORTANT:** The NVIDIA module unload is a **single `modprobe -r`** call with all modules listed. If any module is busy (e.g., nvidia_uvm from a container), the entire unload fails. In that case, try unloading individually or find what's holding references:
```bash
lsmod | grep nvidia
lsof | grep nvidia  # what processes hold nvidia files
```

### vfio-teardown (GPU Reattach)

Path: `~/.local/sbin/vfio-teardown`

**Execution flow:**
1. **Reattach PCI devices via virsh**:
   - `virsh nodedev-reattach pci_0000_01_00_0` (GPU)
   - `virsh nodedev-reattach pci_0000_01_00_1` (HDMI Audio)
2. **Reload NVIDIA kernel modules**: `nvidia_drm`, `nvidia_modeset`, `nvidia_uvm`, `nvidia`
3. **Rebind VT consoles** — `echo 1 > vtcon0/bind` and `vtcon1/bind`
4. **Start greetd** — `systemctl start greetd`
5. **Logs** to `/var/log/libvirt/vfio-teardown.log` with `set -x` trace

### libvirt-nosleep@.service
Path: `/etc/systemd/system/libvirt-nosleep@.service`

```ini
[Unit]
Description=Preventing sleep while libvirt domain "%i" is running

[Service]
Type=simple
ExecStart=/usr/bin/systemd-inhibit --what=sleep --why="Libvirt domain \"%i\" is running" --who=%U --mode=block sleep infinity
```

This uses `systemd-inhibit` to block system sleep (suspend/hibernate) while the VM runs.

### Installation Steps

To deploy hooks from scratch:

```bash
# Become root
sudo -i

# Copy scripts
cp ~/projects/single-gpu-passthrough/hooks/vfio-startup ~/.local/sbin/vfio-startup
cp ~/projects/single-gpu-passthrough/hooks/vfio-teardown ~/.local/sbin/vfio-teardown
cp ~/projects/single-gpu-passthrough/hooks/qemu /etc/libvirt/hooks/qemu
cp ~/projects/single-gpu-passthrough/systemd-no-sleep/libvirt-nosleep@.service /etc/systemd/system/libvirt-nosleep@.service

# Make executable
chmod +x ~/.local/sbin/vfio-startup ~/.local/sbin/vfio-teardown /etc/libvirt/hooks/qemu

# Create log file
mkdir -p /var/log/libvirt
touch /var/log/libvirt/custom_hooks.log /var/log/libvirt/vfio-startup.log /var/log/libvirt/vfio-teardown.log

# Reload systemd
systemctl daemon-reload

# Verify hooks directory exists
ls -la /etc/libvirt/hooks/qemu
```

**NOTE:** The repo scripts are the base versions. The **deployed scripts** at `~/.local/sbin/` have been significantly customized for the author's Wayland+niri setup. Always check the deployed versions before modifying.

## Libvirt / QEMU Configuration

### Modular Daemons
Fedora 44 libvirt uses **modular daemons** (not the monolithic `libvirtd`):

```bash
systemctl status virtqemud      # QEMU-specific daemon
systemctl status virtnodedevd    # Node device management (needed for nodedev-detach)
systemctl status virtnetworkd    # Network management
systemctl status virtstoraged    # Storage management
```

Ensure `virtnodedevd` is running — the hooks depend on it for `virsh nodedev-detach` and `nodedev-reattach`.

### VM Domain XML Skeleton
The VM should be defined in virsh. Key passthrough-specific XML elements:

```xml
<domain type="kvm">
  <name>win10</name>
  <memory unit="GiB">16</memory>
  <vcpu>12</vcpu>
  <os>
    <type>hvm</type>
    <loader readonly="yes" type="pflash">/usr/share/edk2/ovmf/OVMF_CODE_4M.qcow2</loader>
    <nvram>/var/lib/libvirt/qemu/nvram/win10_VARS.fd</nvram>
    <boot dev="hd"/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <hyperv>
      <relaxed state="on"/>
      <vapic state="on"/>
      <spinlocks state="on" retries="8191"/>
    </hyperv>
    <kvm>
      <hidden state="on"/>
    </kvm>
  </features>
  <cpu mode="host-passthrough" check="none">
    <topology sockets="1" dies="1" cores="6" threads="2"/>
  </cpu>
  <devices>
    <!-- VFIO GPU Passthrough -->
    <hostdev mode="subsystem" type="pci" managed="yes">
      <source>
        <address domain="0x0000" bus="0x01" slot="0x00" function="0x0"/>
      </source>
      <rom bar="off"/>
    </hostdev>
    <!-- VFIO HDMI Audio -->
    <hostdev mode="subsystem" type="pci" managed="yes">
      <source>
        <address domain="0x0000" bus="0x01" slot="0x00" function="0x1"/>
      </source>
    </hostdev>
  </devices>
</domain>
```

**Key points:**
- `managed="yes"` — libvirt manages driver binding (detach/attach), which is what the hooks use via `nodedev-detach`
- `rom bar="off"` on GPU — prevents QEMU from trying to map the GPU ROM BAR (often causes issues with NVIDIA cards)
- `kvm hidden state=on` — hides KVM hypervisor signature from NVIDIA drivers (avoids Code 43)
- OVMF (UEFI) is required for GPU passthrough
- `cpu mode="host-passthrough"` — pass all host CPU features to guest (gaming performance)

Alternatively, for finer control, the QEMU command-line equivalent (used when not via libvirt):
```bash
-device vfio-pci,host=01:00.0,multifunction=on,x-vga=on,rombar=0
-device vfio-pci,host=01:00.1
```

Where:
- `multifunction=on` — tells QEMU the GPU is a multi-function device (required when passing both functions 0 and 1)
- `x-vga=on` — marks this device as the primary VGA (needed for boot-time video)
- `rombar=0` — don't expose the option ROM BAR (avoids conflicts)

### Storage Configuration
The VM disk should be on the ext4 partition for better performance:
- Path candidate: `/mnt/media/win10.qcow2`
- HDD storage: 1.4TB available on niaext (ext4)
- NTFS partition (niabc, 452GB) for Windows data sharing

```bash
# Create qcow2 disk (example: 120GB sparse)
qemu-img create -f qcow2 /mnt/media/win10.qcow2 120G
```

### Network Configuration
Default libvirt NAT network is sufficient:
```bash
virsh net-start default
virsh net-autostart default
```

Use `virtio` NIC for best performance:
```xml
<interface type="network">
  <mac address="52:54:00:xx:xx:xx"/>
  <source network="default"/>
  <model type="virtio"/>
</interface>
```

## Workflow

### Starting the VM
```bash
virsh start win10
```

Libvirt will:
1. Call `/etc/libvirt/hooks/qemu win10 prepare begin -`
2. Hook runs vfio-startup (stops GUI, unloads NVIDIA, detaches GPU via virsh)
3. libvirt starts QEMU with VFIO devices
4. GPU output switches to VM

### Shutting Down and Returning to Host
```bash
virsh shutdown win10     # Graceful shutdown
# or
virsh destroy win10      # Force power off
```

Libvirt will:
1. QEMU exits
2. Call `/etc/libvirt/hooks/qemu win10 release end <reason>`
3. Hook runs vfio-teardown (reattaches GPU, reloads NVIDIA, restarts greetd)
4. Display output returns to host (niri on tty1)

### Monitoring

```bash
# Hook logs
tail -f /var/log/libvirt/custom_hooks.log
tail -f /var/log/libvirt/vfio-startup.log
tail -f /var/log/libvirt/vfio-teardown.log

# virsh status
virsh list
watch -n 1 virsh list

# GPU status
lspci -nnk -s 01:00
nvidia-smi      # shows when host driver is bound
```

## Troubleshooting

### GPU Not Detaching (VFIO busy)

```bash
# Check current driver
lspci -nnk -s 01:00

# Check if NVIDIA modules still loaded
lsmod | grep nvidia

# Check if display server still running
systemctl is-active greetd

# Check what holds the GPU
fuser -v /dev/dri/* 2>/dev/null
lsof | grep -i nvidia

# Force detach (if not managed)
virsh nodedev-detach pci_0000_01_00_0
virsh nodedev-detach pci_0000_01_00_1
```

### vm starts but no display output (black screen)

- Ensure monitor is connected to the **same GPU port** used by host
- Check `rom bar="off"` is set in VM XML
- Try adding a GPU VBIOS ROM file (dump from Windows with GPU-Z, or from motherboard)
- Try `x-vga=on` in the QEMU args
- Ensure NVIDIA driver is installed in Windows VM

### Error Code 43 in Windows VM

NVIDIA drivers detect the KVM hypervisor and disable themselves. Fixes:
- `kvm hidden state=on` in domain XML
- Set `hyperv` features: `relaxed`, `vapic`, `spinlocks`
- CPU mode `host-passthrough`
- Some newer NVIDIA drivers also check for: `<vendor_id state="on" value="1234567890ab"/>`

### Module Unload Fails During Startup

```bash
# Check usage
lsmod | grep nvidia

# Find what's using nvidia_uvm
cat /sys/devices/virtual/misc/uvm/uevent

# Kill remaining processes
ps aux | grep -i nvidia
killall nvidia-persistenced 2>/dev/null
```

### Greetd / Niri Won't Restart After Teardown

```bash
# Check greetd status
systemctl status greetd

# Manually start
sudo systemctl start greetd

# Check niri log
journalctl -u greetd -n 50 --no-pager
```

### Bootc-specific Issues

On Fedora bootc (ostree atomic host):
- If you layer packages with `rpm-ostree install`, they persist through updates
- If you use `rpm-ostree usroverlay` for /usr modifications, those are **temporary** (lost on reboot)
- libvirt is part of the base image (container layer), not layered
- Hook scripts persist in /etc (writable state directory)
- For kernel args changes: `rpm-ostree kargs --append/--delete/--replace` **requires a reboot**

## Advanced: Manual VFIO Binding

If libvirt's managed mode isn't working, bind VFIO-PCI manually at startup:

```bash
# Bind GPU to vfio-pci (instead of virsh nodedev-detach)
echo "0000:01:00.0" > /sys/bus/pci/devices/0000:01:00.0/driver/unbind
echo "0000:01:00.1" > /sys/bus/pci/devices/0000:01:00.1/driver/unbind
echo "10de 1f03" > /sys/bus/pci/drivers/vfio-pci/new_id
echo "10de 10f9" > /sys/bus/pci/drivers/vfio-pci/new_id
```

But this is redundant with `virsh nodedev-detach` — prefer the virsh method which handles the bind/unbind lifecycle correctly.

## Key Paths Reference

| Path | Purpose |
|------|---------|
| `~/projects/single-gpu-passthrough/` | Git repo with hook sources |
| `~/.local/sbin/vfio-startup` | Deployed startup script **(customized!)** |
| `~/.local/sbin/vfio-teardown` | Deployed teardown script **(customized!)** |
| `/etc/libvirt/hooks/qemu` | Libvirt hook dispatcher |
| `/etc/systemd/system/libvirt-nosleep@.service` | Sleep inhibitor service |
| `/var/log/libvirt/custom_hooks.log` | Hook dispatcher log |
| `/var/log/libvirt/vfio-startup.log` | Startup trace log |
| `/var/log/libvirt/vfio-teardown.log` | Teardown trace log |
| `/var/lib/libvirt/qemu/nvram/` | VM NVRAM store (UEFI variables) |
| `/mnt/media/` | Ext4 data partition (recommended VM disk location) |

## References

- Risingprism Single GPU Passthrough guide (repo): https://gitlab.com/risingprismtv/single-gpu-passthrough
- QEMU system emulation docs: https://www.qemu.org/docs/master/system/
- libvirt hooks docs: https://libvirt.org/hooks.html
- libvirt domain XML format: https://libvirt.org/formatdomain.html
- OVMF firmware location: `/usr/share/edk2/ovmf/`
