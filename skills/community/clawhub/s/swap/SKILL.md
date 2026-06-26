---
name: swap
description: Configure Linux swap — create swap file, set swappiness, persist via fstab, resize swap.
version: 1.0.0
tags:
  - linux
  - swap
  - memory
  - configuration
metadata:
  os:
    - linux
  requires:
    bins:
      - bash
      - swapon      # util-linux
      - mkswap      # util-linux
      - chmod       # coreutils
      - sysctl      # procps
    optional_bins:
      - fallocate   # util-linux (fast swap file creation)
      - dd          # coreutils (fallback swap file creation)
      - swapoff     # util-linux (resize swap)
      - free        # procps (verify memory)
  emoji: "\U0001F4BE"
---

# Linux Swap Configuration Skill

You are a Linux swap configuration assistant. When a user needs to create, resize, or tune swap on a Linux system, use this skill.

Typical scenarios:
- Server has no swap, user wants to add one
- User wants to resize existing swap
- User wants to tune swappiness
- Swap is lost after reboot (not persisted in fstab)

## Workflow

1. First check the current swap status to understand the starting point
2. Then execute the appropriate operation section based on the user's request
3. Always verify the result after any change

---

## 1. Check Current Swap Status

Before any operation, check the current state:

```bash
# Show active swap devices
swapon --show

# Show memory including swap
free -h

# Check fstab for swap persistence
grep -v '^#' /etc/fstab | grep swap

# Current swappiness value
sysctl vm.swappiness
```

---

## 2. Create Swap File

First根据 RAM 大小确定 swap 容量：

| RAM | Swap 大小 |
|-----|----------|
| <= 2 GB | 2x RAM |
| > 2 GB -- 8 GB | 与 RAM 相等 |
| > 8 GB -- 64 GB | >= 4 GB |

例如：RAM 为 2 GB 时创建 4G swap，RAM 为 4 GB 时创建 4G swap，RAM 为 16 GB 时创建 4G swap。

两种创建方式，优先用 `fallocate`（快）；ext3 或不支持 `fallocate` 的文件系统用 `dd`：

```bash
# 根据上表确定 SIZE，例如 4G

# Method 1: fallocate (preferred)
sudo fallocate -l <SIZE> /swapfile

# Method 2: dd (fallback)
# 例如 4G = 4096M
sudo dd if=/dev/zero of=/swapfile bs=1M count=<SIZE_IN_MB>

# Set permissions — swap files must be 0600
sudo chmod 600 /swapfile

# Format as swap
sudo mkswap /swapfile

# Enable
sudo swapon /swapfile

# Verify
swapon --show
free -h
```

---

## 3. Persist Swap Across Reboots

Without this step, swap will be lost after reboot.

```bash
# Add to /etc/fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Verify the entry:

```bash
grep swap /etc/fstab
```

---

## 4. Set Swappiness

`vm.swappiness` controls how aggressively the kernel uses swap (0-100, default 60). Value of 20 is recommended for most servers.

```bash
# Set immediately
sudo sysctl -w vm.swappiness=20

# Persist across reboots
echo 'vm.swappiness=20' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

## 5. Resize Swap

按 Section 2 的规则表确定新容量，然后先禁用再重建：

```bash
# Disable current swap
sudo swapoff /swapfile

# Recreate with new size
sudo fallocate -l <SIZE> /swapfile
# or: sudo dd if=/dev/zero of=/swapfile bs=1M count=<SIZE_IN_MB>

# Re-format and enable
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Verify
swapon --show
free -h
```

The fstab entry does not need to change if the file path stays the same.


