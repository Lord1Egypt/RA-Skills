#!/usr/bin/env bash
# checks.sh — All 26 health checks as bash functions.
#
# Each function writes results to stdout, diagnostics to stderr.
# Exit codes: 0=pass, 1=fail, 2=config error, 3=skippable

# --- Requires: source lib/helpers.sh first ---

# 1.1  SSH Connectivity to peer nodes (REQUIRES PREFLIGHT_PEER_IPS)
check_1_1() {
  local peers="${PREFLIGHT_PEER_IPS:-}"
  if [ -z "$peers" ]; then
    echo "skipped: PREFLIGHT_PEER_IPS not set (cross-node check)" >&2
    return 3
  fi
  local fail=0
  IFS=',' read -ra ips <<< "$peers"
  for ip in "${ips[@]}"; do
    ip=$(echo "$ip" | xargs)
    if ssh -o BatchMode=yes -o ConnectTimeout=5 "$ip" echo ok 2>/dev/null; then
      echo "SSH to $ip: ok"
    else
      echo "SSH to $ip: FAILED" >&2
      fail=1
    fi
  done
  return $fail
}

# 1.2  Docker Service
check_1_2() {
  if command -v systemctl >/dev/null 2>&1; then
    systemctl is-active docker
  elif command -v docker >/dev/null 2>&1; then
    docker info >/dev/null 2>&1 && echo active
  else
    echo 'docker not found' >&2
    return 1
  fi
}

# 1.3  GPU Detection
check_1_3() {
  local vendor
  vendor=$(_gpu_vendor)
  if [ "$vendor" = nvidia ]; then
    nvidia-smi --query-gpu=gpu_name --format=csv,noheader
  elif [ "$vendor" = amd ]; then
    amd-smi static --gpu 2>/dev/null || rocm-smi --showproductname
  else
    echo "No supported GPU detected" >&2
    return 1
  fi
}

# 1.4  GPU Count and Model
check_1_4() {
  local vendor count model
  vendor=$(_gpu_vendor)
  if [ "$vendor" = nvidia ]; then
    count=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader | wc -l)
    model=$(nvidia-smi --query-gpu=gpu_name --format=csv,noheader | head -1)
    echo "${count}x ${model}"
  elif [ "$vendor" = amd ]; then
    count=$(amd-smi list 2>/dev/null | grep -c GPU || rocm-smi -i 2>/dev/null | grep -c "^GPU")
    model=$(amd-smi static --gpu 2>/dev/null | grep -m1 "Market" | awk -F: '{print $2}' | xargs || rocm-smi --showproductname 2>/dev/null | grep -m1 "Card" | awk -F: '{print $2}' | xargs)
    echo "${count}x ${model}"
  else
    echo "No GPU" >&2
    return 1
  fi
}

# 1.5  GPU Driver Version
check_1_5() {
  local vendor
  vendor=$(_gpu_vendor)
  if [ "$vendor" = nvidia ]; then
    nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1
  elif [ "$vendor" = amd ]; then
    amd-smi version 2>/dev/null || cat /sys/module/amdgpu/version 2>/dev/null || echo unknown
  else
    echo "No GPU" >&2
    return 1
  fi
}

# 1.6  OS and Kernel Version
check_1_6() {
  echo "kernel=$(uname -r)"
  # shellcheck disable=SC1091
  . /etc/os-release 2>/dev/null && echo "os=${PRETTY_NAME:-$NAME $VERSION}"
}

# 1.7  Network Type Detection
check_1_7() {
  if [ -d /sys/class/infiniband ] && ls /sys/class/infiniband/ 2>/dev/null | grep -q .; then
    if ibdev2netdev 2>/dev/null | grep -q ib; then
      echo 'InfiniBand'
    else
      echo 'RoCE'
    fi
  elif command -v rdma >/dev/null 2>&1 && rdma link show 2>/dev/null | grep -q .; then
    echo 'RoCE'
  else
    echo 'Ethernet (no RDMA)'
  fi
}

# 1.8  IB/NIC Ports Up
check_1_8() {
  if [ -d /sys/class/infiniband ]; then
    ibstat 2>/dev/null | grep -E "State|Physical state|Rate" || ibstatus 2>/dev/null
  else
    local iface
    iface=$(_hs_iface)
    ip -br link show "$iface" 2>/dev/null || ip link show "$iface"
  fi
}

# 1.9  GPU Container Toolkit
check_1_9() {
  local vendor
  vendor=$(_gpu_vendor)
  if [ "$vendor" = nvidia ]; then
    docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi --query-gpu=gpu_name --format=csv,noheader
  elif [ "$vendor" = amd ]; then
    docker run --rm --device /dev/kfd --device /dev/dri rocm/rocm-terminal rocm-smi --showproductname
  else
    echo "No GPU vendor detected" >&2
    return 1
  fi
}

# 1.10  Shared File System
check_1_10() {
  local mp="${MOUNT_POINT:-}"
  if [ -z "$mp" ]; then
    for p in /mnt/shared /mnt/nfs /mnt/lustre /shared; do
      [ -d "$p" ] && mp="$p" && break
    done
  fi
  [ -z "$mp" ] && mp=/tmp
  df -h "$mp" && touch "$mp/.clusterready_test" && rm -f "$mp/.clusterready_test" && echo "read/write OK on $mp"
}

# 1.11  GPUDirect Kernel Module
check_1_11() {
  local vendor
  vendor=$(_gpu_vendor)
  if [ "$vendor" = nvidia ]; then
    lsmod | grep -E "nvidia_peermem|nv_peer_mem|ib_peer_mem" || { echo "GPUDirect RDMA module NOT loaded" >&2; return 1; }
  elif [ "$vendor" = amd ]; then
    local amdgpu_loaded rdma_loaded ib_dev_present rdma_link_present
    amdgpu_loaded=$(lsmod | grep -c amdgpu || true)
    rdma_loaded=$(lsmod | grep -cE "ib_core|ib_uverbs|rdma_cm|mlx5_ib|mlx5_core|bnxt_re|irdma|amdp2p" || true)
    ib_dev_present=0
    [ -d /sys/class/infiniband ] && ls /sys/class/infiniband 2>/dev/null | grep -q . && ib_dev_present=1
    rdma_link_present=0
    command -v rdma >/dev/null 2>&1 && rdma link show 2>/dev/null | grep -q . && rdma_link_present=1
    if [ "$amdgpu_loaded" -gt 0 ] && { [ "$rdma_loaded" -gt 0 ] || [ "$ib_dev_present" -eq 1 ] || [ "$rdma_link_present" -eq 1 ]; }; then
      echo "amdgpu + RDMA stack loaded (GPUDirect RDMA capable)"
      lsmod | grep -E "amdgpu|ib_core|ib_uverbs|rdma_cm|mlx5_ib|mlx5_core|bnxt_re|irdma|amdp2p"
    else
      echo "GPUDirect RDMA module NOT loaded (amdgpu=$amdgpu_loaded rdma_mods=$rdma_loaded ib_dev=$ib_dev_present rdma_link=$rdma_link_present)" >&2
      return 1
    fi
  else
    echo "GPUDirect RDMA module NOT loaded" >&2
    return 1
  fi
}

# 1.12  IOMMU Passthrough
check_1_12() {
  local iommu_val intel_iommu amd_iommu
  iommu_val=$(cat /proc/cmdline | grep -oP 'iommu=\S+' || true)
  intel_iommu=$(cat /proc/cmdline | grep -oP 'intel_iommu=\S+' || true)
  amd_iommu=$(cat /proc/cmdline | grep -oP 'amd_iommu=\S+' || true)
  echo "${iommu_val:-iommu=not_set} ${intel_iommu:-} ${amd_iommu:-}" | xargs
  if echo "$iommu_val $intel_iommu $amd_iommu" | grep -qiE 'pt|passthrough|off'; then
    return 0
  else
    echo 'IOMMU may not be in passthrough mode' >&2
    return 1
  fi
}

# 1.13  NUMA Balancing
check_1_13() {
  sysctl kernel.numa_balancing
}

# 1.14  Firewall Disabled
check_1_14() {
  local rules fw_active ufw_active
  rules=$(iptables -L -n 2>/dev/null | wc -l || echo 0)
  fw_active=$(systemctl is-active firewalld 2>/dev/null || echo inactive)
  ufw_active=$(ufw status 2>/dev/null | head -1 || echo inactive)
  echo "iptables_lines=$rules firewalld=$fw_active ufw=$ufw_active"
  if [ "$fw_active" = active ] || echo "$ufw_active" | grep -qi 'active'; then
    echo 'Firewall is active' >&2
    return 1
  fi
  return 0
}

# 1.15  PCIe Link Speed and Width
check_1_15() {
  local vendor
  vendor=$(_gpu_vendor)
  if [ "$vendor" = nvidia ]; then
    for addr in $(nvidia-smi --query-gpu=pci.bus_id --format=csv,noheader | sed 's/^0000://'); do
      echo "=== GPU $addr ==="
      lspci -vvv -s "$addr" 2>/dev/null | grep -E "LnkSta:|LnkCap:" || echo "no pcie info"
    done
  elif [ "$vendor" = amd ]; then
    for addr in $(lspci | grep -i "AMD.*Display\|AMD.*Instinct" | awk '{print $1}'); do
      echo "=== GPU $addr ==="
      lspci -vvv -s "$addr" 2>/dev/null | grep -E "LnkSta:|LnkCap:" || echo "no pcie info"
    done
  else
    echo "no gpu pci device detected for pcie link check" >&2
    return 1
  fi
}

# 1.16  PCIe ACS Disabled
check_1_16() {
  local found=false
  for bridge in $(lspci -D 2>/dev/null | grep -i "PCI bridge" | awk '{print $1}'); do
    local acs
    acs=$(setpci -s "$bridge" ECAP_ACS+6.w 2>/dev/null) || continue
    found=true
    if [ -n "$acs" ] && [ "$acs" != "0000" ]; then
      echo "ACS enabled on $bridge: $acs"
    else
      echo "ACS disabled on $bridge"
    fi
  done
  $found || echo "No PCI bridges with ACS capability found"
}

# 1.17  GPU-NIC PCIe Affinity
check_1_17() {
  local vendor
  vendor=$(_gpu_vendor)
  if [ "$vendor" = nvidia ]; then
    nvidia-smi topo -m
  elif [ "$vendor" = amd ]; then
    rocm-smi --showtopo 2>/dev/null || echo "rocm-smi topo not available"
  else
    echo "No GPU vendor" >&2
    return 1
  fi
}

# 1.18  NIC Firmware Version
check_1_18() {
  local iface dev
  iface=$(_hs_iface)
  dev=$(_rdma_dev)
  if command -v mlxfwmanager >/dev/null 2>&1; then
    mlxfwmanager --query 2>/dev/null | head -20
  elif command -v ethtool >/dev/null 2>&1; then
    ethtool -i "$iface" 2>/dev/null
  elif [ -f "/sys/class/infiniband/$dev/fw_ver" ]; then
    echo "fw_ver=$(cat "/sys/class/infiniband/$dev/fw_ver")"
  else
    echo "No NIC firmware tool available" >&2
    return 1
  fi
}

# 1.19  BIOS Settings Validation
check_1_19() {
  dmidecode -t bios 2>/dev/null | head -30 || echo 'dmidecode not available'
  echo '---'
  if command -v ipmitool >/dev/null 2>&1; then
    ipmitool raw 0x06 0x01 2>/dev/null || echo 'ipmitool not accessible'
  else
    echo 'ipmitool not installed'
  fi
}

# 1.20  Link Quality / Error Counters
check_1_20() {
  local dev iface is_ib
  dev=$(_rdma_dev)
  iface=$(_hs_iface)
  is_ib=false
  if [ -d /sys/class/net/"$iface" ] && [ "$(cat /sys/class/net/"$iface"/type 2>/dev/null)" = "32" ]; then
    is_ib=true
  fi
  if [ -d /sys/class/infiniband ] && command -v ibdev2netdev >/dev/null 2>&1 && ibdev2netdev 2>/dev/null | grep -qE "=>\s*ib[0-9]+"; then
    is_ib=true
  fi
  if $is_ib && command -v perfquery >/dev/null 2>&1; then
    local perf_out perf_rc
    perf_out=$(perfquery -x -d "$dev" 1 2>&1)
    perf_rc=$?
    if [ "$perf_rc" -eq 0 ]; then
      printf "%s\n" "$perf_out"
      return 0
    fi
    echo "$perf_out" >&2
    echo "perfquery failed for dev=$dev iface=$iface; falling back to ethtool" >&2
  fi
  if command -v ethtool >/dev/null 2>&1; then
    local stats
    stats=$(ethtool -S "$iface" 2>/dev/null)
    if [ -z "$stats" ]; then
      echo "ethtool stats unavailable for $iface" >&2
      return 1
    fi
    printf "%s\n" "$stats" | grep -iE "error|drop|crc|fcs" | head -20 || echo "no error counters reported"
    echo "interface=$iface (ethtool path)"
  else
    echo "No link quality tool" >&2
    return 1
  fi
}

# 1.21  Transceiver Health
check_1_21() {
  local iface dev
  iface=$(_hs_iface)
  dev=$(_rdma_dev)
  if command -v mlxlink >/dev/null 2>&1; then
    mlxlink -d "$dev" -m 2>/dev/null | head -30
  elif command -v ethtool >/dev/null 2>&1; then
    ethtool --module-info "$iface" 2>/dev/null || echo "module-info not available for $iface"
  else
    echo "No transceiver tool" >&2
    return 1
  fi
}

# 1.22  MTU Configuration
check_1_22() {
  local iface mtu
  iface=$(_hs_iface)
  mtu=$(cat /sys/class/net/"$iface"/mtu 2>/dev/null || ip link show "$iface" | grep -oP 'mtu \K\d+')
  echo "interface=$iface mtu=$mtu"
  if [ "$mtu" -ge 9000 ] 2>/dev/null; then
    echo "Jumbo frames OK"
  else
    echo "MTU $mtu < 9000, jumbo frames not configured" >&2
    return 1
  fi
}

# 1.23  Fabric Topology (InfiniBand only)
check_1_23() {
  if command -v ibnetdiscover >/dev/null 2>&1; then
    ibnetdiscover 2>/dev/null | head -50
  elif command -v ibdiagnet >/dev/null 2>&1; then
    ibdiagnet 2>/dev/null | head -50
  else
    echo 'ibnetdiscover/ibdiagnet not available' >&2
    return 1
  fi
}

# 1.24  RoCE QoS and NIC Configuration
check_1_24() {
  local iface dev
  iface=$(_hs_iface)
  dev=$(_rdma_dev)
  echo "=== QoS ==="
  if command -v mlnx_qos >/dev/null 2>&1; then
    mlnx_qos -i "$iface" 2>/dev/null
  else
    echo "mlnx_qos not available"
  fi
  echo "=== GIDs ==="
  if command -v show_gids >/dev/null 2>&1; then
    show_gids "$dev" 2>/dev/null
  elif [ -d "/sys/class/infiniband/$dev/ports/1/gids" ]; then
    for g in /sys/class/infiniband/"$dev"/ports/1/gids/*; do
      local val
      val=$(cat "$g" 2>/dev/null)
      [ "$val" != "0000:0000:0000:0000:0000:0000:0000:0000" ] && echo "$(basename "$g"): $val"
    done
  else
    echo "No GID info available"
  fi
}

# 1.25  Ethernet Switch QoS (requires switch access env vars)
check_1_25() {
  if [ -n "${SWITCH_CLI_CMD:-}" ]; then
    eval "$SWITCH_CLI_CMD"
  elif [ -n "${SWITCH_HOST:-}" ]; then
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "${SWITCH_USER:-admin}@${SWITCH_HOST}" "${SWITCH_SHOW_CMD:-show interface status}"
  else
    echo "switch validation requires SWITCH_CLI_CMD or SWITCH_HOST env var" >&2
    return 2
  fi
}

# 1.26  Network Routing Validation (REQUIRES PREFLIGHT_PEER_IPS)
check_1_26() {
  local peers="${PREFLIGHT_PEER_IPS:-}"
  if [ -z "$peers" ]; then
    echo "skipped: PREFLIGHT_PEER_IPS not set (cross-node check)" >&2
    return 3
  fi
  local fail=0
  IFS=',' read -ra ips <<< "$peers"
  for ip in "${ips[@]}"; do
    ip=$(echo "$ip" | xargs)
    if ping -c 1 -W 3 "$ip" >/dev/null 2>&1; then
      echo "ping $ip: ok"
    else
      echo "ping $ip: FAILED" >&2
      fail=1
    fi
  done
  return $fail
}

# Bonus: L3 mesh ping to all peers (REQUIRES PREFLIGHT_PEER_IPS)
check_mesh_ping() {
  local peers="${PREFLIGHT_PEER_IPS:-}"
  if [ -z "$peers" ]; then
    echo "skipped: PREFLIGHT_PEER_IPS not set (cross-node check)" >&2
    return 3
  fi
  local fail=0
  IFS=',' read -ra ips <<< "$peers"
  for ip in "${ips[@]}"; do
    ip=$(echo "$ip" | xargs)
    echo "--- ping $ip ---"
    if ping -c 3 -W 3 "$ip"; then
      echo "mesh ping $ip: ok"
    else
      echo "mesh ping $ip: FAILED" >&2
      fail=1
    fi
  done
  return $fail
}
