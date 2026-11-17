#!/bin/bash
exec >>/var/log/libvirt/vfio-teardown.log 2>&1
set -x

DATE=$(date +"%m/%d/%Y %R:%S")
echo "========================================================"
echo "[$DATE] BEGIN VFIO TEARDOWN"
echo "========================================================"

# 1. Reattach devices
echo ">>> [ACTION] Reattaching devices to host..."
virsh nodedev-reattach pci_0000_01_00_0 || echo ">>> [ERROR] Failed to reattach GPU (01:00.0)"
virsh nodedev-reattach pci_0000_01_00_1 || echo ">>>[ERROR] Failed to reattach Audio (01:00.1)"
sleep 1

# 2. Reload NVIDIA modules
echo ">>> [ACTION] Reloading NVIDIA modules..."
modprobe nvidia_drm nvidia_modeset nvidia_uvm nvidia || echo ">>> [ERROR] Failed to load NVIDIA modules"
sleep 2

# 3. Rebind VTconsoles
echo ">>> [ACTION] Rebinding VTconsoles..."
echo 1 >/sys/class/vtconsole/vtcon0/bind 2>/dev/null || echo "vtcon0 bind failed/missing"
echo 1 >/sys/class/vtconsole/vtcon1/bind 2>/dev/null || echo "vtcon1 bind failed/missing"

# 4. Start Display Manager
echo ">>> [ACTION] Starting Greetd..."
systemctl start greetd

# 5. Verify Host Reclamation
echo ">>> [DEBUG] Final PCI Status:"
lspci -nnk -s 01:00

echo "[$DATE] END VFIO TEARDOWN"
echo "========================================================"
