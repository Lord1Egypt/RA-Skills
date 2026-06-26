#!/usr/bin/env bash
# helpers.sh — Shared detection helpers for cluster pre-flight checks.

# Detect the first high-speed NIC interface name.
# Prefers ibdev2netdev (IB), falls back to first RDMA netdev, then first
# non-lo non-docker non-veth interface with speed >= 10000.
_hs_iface() {
  # 1) InfiniBand: ibdev2netdev gives "mlx5_0 port 1 ==> ib0 (Up)"
  if command -v ibdev2netdev >/dev/null 2>&1; then
    local iface
    iface=$(ibdev2netdev 2>/dev/null | awk '/Up/{print $5; exit}')
    [ -n "$iface" ] && echo "$iface" && return
  fi
  # 2) RDMA netdev (RoCE)
  if command -v rdma >/dev/null 2>&1; then
    local iface
    iface=$(rdma link show 2>/dev/null | grep -oP 'netdev \K\S+' | head -1)
    [ -n "$iface" ] && echo "$iface" && return
  fi
  # 3) Fallback: highest-speed physical interface
  for d in /sys/class/net/*/speed; do
    local spd name
    spd=$(cat "$d" 2>/dev/null) || continue
    name=$(basename "$(dirname "$d")")
    [[ "$name" == lo || "$name" == docker* || "$name" == veth* || "$name" == br-* ]] && continue
    [ "$spd" -ge 10000 ] 2>/dev/null && echo "$name" && return
  done
  # 4) Last resort
  echo "eth0"
}

# Detect the first RDMA device name (e.g. mlx5_0)
_rdma_dev() {
  if [ -d /sys/class/infiniband ]; then
    ls /sys/class/infiniband/ 2>/dev/null | head -1 && return
  fi
  if command -v rdma >/dev/null 2>&1; then
    rdma link show 2>/dev/null | grep -oP '^\d+/\d+: \K\S+' | sed 's|/.*||' | head -1 && return
  fi
  echo "mlx5_0"
}

# Detect GPU vendor — prints "nvidia", "amd", or "unknown"
_gpu_vendor() {
  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi -L >/dev/null 2>&1 && echo nvidia && return
  fi
  if command -v amd-smi >/dev/null 2>&1; then
    amd-smi list >/dev/null 2>&1 && echo amd && return
  fi
  if command -v rocm-smi >/dev/null 2>&1; then
    rocm-smi -i >/dev/null 2>&1 && echo amd && return
  fi
  # Fallback: check lspci
  lspci 2>/dev/null | grep -qi nvidia && echo nvidia && return
  lspci 2>/dev/null | grep -qi 'AMD.*Instinct\|AMD.*MI[0-9]' && echo amd && return
  echo unknown
}
