# Platform Setup Reference

Detailed provider installation and configuration for each platform.

## Mac (Apple Silicon — M1/M2/M3/M4) — Parallels

VirtualBox on Apple Silicon is experimental and unreliable. **Use Parallels.**

```bash
# 1. Install Parallels Desktop (requires license)
#    Download from https://www.parallels.com/products/desktop/

# 2. Install Vagrant
brew install --cask vagrant

# 3. Install the Parallels provider plugin
vagrant plugin install vagrant-parallels

# 4. Start
vagrant up --provider=parallels
```

**Verified working:** macOS 26.3, Apple Silicon (arm64), Parallels Desktop, Vagrant 2.4.9, bento/ubuntu-24.04 arm64 box. Setup provisions Go 1.24.3 (arm64), Docker, mage. 11/11 checks pass.

**KVM note:** Nested KVM is not available on Mac (no `/dev/kvm`). The VM still provides Docker, Go, mage, and full sudo. If you need nested KVM (e.g., for Firecracker microVM testing), use a Linux host.

## Mac (Intel) — VirtualBox

```bash
# 1. Install VirtualBox
brew install --cask virtualbox

# 2. Install Vagrant
brew install --cask vagrant

# 3. Start
vagrant up --provider=virtualbox
```

## Linux — libvirt/KVM (Recommended)

This is the most capable setup — includes nested KVM for microVM testing.

```bash
# 1. Install KVM + libvirt
sudo apt-get install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils

# 2. Install Vagrant + libvirt plugin
sudo apt-get install -y vagrant
vagrant plugin install vagrant-libvirt

# 3. Start
vagrant up --provider=libvirt
```

**Nested KVM** is automatically enabled (`cpu_mode: host-passthrough`). Verify:
```bash
# Host must have KVM
test -e /dev/kvm && echo "KVM OK"

# After vagrant up, verify nested KVM inside VM
vagrant ssh -c "test -e /dev/kvm && echo 'Nested KVM OK'"
```

## Windows (WSL2) — VirtualBox

```bash
# 1. Install VirtualBox on Windows (not inside WSL2)
#    Download from https://www.virtualbox.org/wiki/Downloads

# 2. Inside WSL2, install Vagrant
sudo apt-get install -y vagrant

# 3. Tell Vagrant to use the Windows VirtualBox
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"
export PATH="$PATH:/mnt/c/Program Files/Oracle/VirtualBox"

# 4. Start
vagrant up --provider=virtualbox
```

## Provider Capabilities

| Feature | Parallels (Mac) | libvirt (Linux) | VirtualBox |
|---------|:-:|:-:|:-:|
| Nested KVM | No | Yes | Limited |
| Performance | Excellent | Excellent | Good |
| Apple Silicon | Native | N/A | Experimental |
| Docker-in-VM | Yes | Yes | Yes |
| Auto-detect | Yes | Yes | Yes |
