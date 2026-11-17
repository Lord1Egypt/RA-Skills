#!/bin/bash
exec >>/var/log/libvirt/vfio-startup.log 2>&1
set -x

DATE=$(date +"%m/%d/%Y %R:%S")
echo "========================================================"
echo "[$DATE] BEGIN VFIO STARTUP"
echo "========================================================"

# 1. Stop display manager and Wayland consumers
echo ">>> [ACTION] Stopping greetd and killing Wayland/X11 processes..."
systemctl stop greetd
killall -9 niri qs zen kitty Xwayland pipewire wireplumber 2>/dev/null
sleep 2

# Isolate to text mode so systemd stops trying to restart the GUI
systemctl isolate multi-user.target
sleep 2

# 2. Unbind VTconsoles and EFI Framebuffer
echo ">>> [ACTION] Unbinding VTconsoles and EFI Framebuffer..."
echo 0 >/sys/class/vtconsole/vtcon0/bind 2>/dev/null || echo "vtcon0 unbind failed/missing"
echo 0 >/sys/class/vtconsole/vtcon1/bind 2>/dev/null || echo "vtcon1 unbind failed/missing"
echo efi-framebuffer.0 >/sys/bus/platform/drivers/efi-framebuffer/unbind 2>/dev/null || echo "efi-fb unbind failed"
sleep 1

# 3. Unload NVIDIA modules
echo ">>> [ACTION] Unloading NVIDIA modules..."
modprobe -r nvidia_uvm nvidia_drm nvidia_modeset nvidia i2c_nvidia_gpu drm_kms_helper || echo ">>> [WARNING] Module unload returned error!"
sleep 2

# 4. Detach GPU via virsh
echo ">>> [ACTION] Detaching GPU and Audio from host via virsh..."
virsh nodedev-detach pci_0000_01_00_0 || echo ">>> [ERROR] Failed to detach GPU (01:00.0)"
virsh nodedev-detach pci_0000_01_00_1 || echo ">>> [ERROR] Failed to detach Audio (01:00.1)"

# 5. Final verification
echo ">>> [DEBUG] Final PCI Status:"
lspci -nnk -s 01:00

echo "[$DATE] END VFIO STARTUP"
