#!/bin/bash
#===============================================
# OpenClaw Server Guardian - Auto Recovery
# 自动恢复脚本：根据诊断结果执行对应修复
#============================================

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

report() { echo -e "[$(date '+%H:%M:%S')] $1"; }
info()  { echo -e "${CYAN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }
ok()    { echo -e "${GREEN}[OK]${NC} $1"; }

# ---------- 工具函数 ----------
need_root() {
  if [ "$(id -u)" -ne 0 ]; then
    error "需要 root 权限执行此操作"
    exit 1
  fi
}

confirm() {
  local msg="$1"
  read -p "$msg (y/N): " yn
  [[ "$yn" =~ ^[Yy]$ ]]
}

# ---------- 恢复动作清单 ----------

recover_gateway() {
  report "=== 尝试恢复 Gateway ==="
  
  # 检查 gateway 是否真的挂了
  if pgrep -f "openclaw gateway" > /dev/null; then
    ok "Gateway 进程仍在，尝试重启..."
  fi
  
  info "正在重启 Gateway..."
  openclaw gateway restart
  sleep 5
  
  if pgrep -f "openclaw gateway" > /dev/null; then
    ok "Gateway 重启成功"
    return 0
  else
    error "Gateway 重启失败，尝试强制启动..."
    openclaw gateway start
    sleep 5
    if pgrep -f "openclaw gateway" > /dev/null; then
      ok "Gateway 强制启动成功"
      return 0
    else
      error "Gateway 启动失败，请检查日志"
      return 1
    fi
  fi
}

clear_mem_cache() {
  report "=== 清理内存缓存 ==="
  need_root
  sync
  echo 3 > /proc/sys/vm/drop_caches 2>/dev/null && ok "内存缓存已清理" || warn "无法清理缓存（非root或不支持）"
}

kill_high_mem_procs() {
  report "=== 查找并处理高内存进程 ==="
  # 找出内存占用 > 500MB 的非关键进程
  for pid in $(ps aux --sort=-%mem | awk '$4 > 5.0 && $11 !~ /^\[.*\]$/ {print $2}' | head -10); do
    pname=$(ps -o comm= -p "$pid" 2>/dev/null || true)
    mem_mb=$(ps -o rss= -p "$pid" 2>/dev/null | awk '{print int($1/1024)}')
    if [ -n "$pname" ] && [ "$mem_mb" -gt 500 ]; then
      warn "进程 $pname (PID:$pid) 占用 ${mem_mb}MB"
      if confirm "是否杀掉此进程?"; then
        kill -15 "$pid" && ok "已发送 SIGTERM" || true
        sleep 2
        kill -9 "$pid" 2>/dev/null && ok "已强制结束" || true
      fi
    fi
  done
}

rotate_logs() {
  report "=== 日志整理 ==="
  LOG_DIR="/root/.openclaw/logs"
  [ -d "$LOG_DIR" ] || LOG_DIR="/var/log/openclaw"
  
  if [ -d "$LOG_DIR" ]; then
    # 压缩超过 50MB 的日志
    find "$LOG_DIR" -name "*.log" -size +50M | while read -r f; do
      warn "压缩大日志: $f ($(du -h "$f" | cut -f1))"
      gzip "$f" 2>/dev/null && ok "已压缩: $f.gz" || warn "压缩失败: $f"
    done
    
    # 删除30天以上的旧日志
    OLD_COUNT=$(find "$LOG_DIR" -name "*.gz" -mtime +30 | wc -l)
    if [ "$OLD_COUNT" -gt 0 ]; then
      find "$LOG_DIR" -name "*.gz" -mtime +30 -delete
      ok "已清理 $OLD_COUNT 个旧日志"
    fi
  fi
}

free_disk_space() {
  report "=== 清理磁盘空间 ==="
  need_root
  
  # 常见大文件位置
  DIRS_TO_CHECK=("/tmp" "/var/cache" "/root/.npm" "/root/.pnpm-store")
  
  for d in "${DIRS_TO_CHECK[@]}"; do
    if [ -d "$d" ]; then
      size=$(du -sh "$d" 2>/dev/null | cut -f1)
      info "$d: $size"
    fi
  done
  
  if confirm "是否清理 npm/pnpm 缓存?"; then
    npm cache clean --force 2>/dev/null && ok "npm缓存已清理" || true
    pnpm store prune 2>/dev/null && ok "pnpm缓存已清理" || true
  fi
}

restart_bot() {
  report "=== 重启 Bot 服务 ==="
  openclaw gateway restart
  sleep 8
  if pgrep -f "openclaw" > /dev/null; then
    ok "Bot 重启成功"
    return 0
  else
    error "Bot 重启失败"
    return 1
  fi
}

check_oom_killer() {
  report "=== 检查 OOM Killer 记录 ==="
  OOM_RECORDS=$(dmesg 2>/dev/null | grep -i "killed process" | tail -5 || true)
  if [ -n "$OOM_RECORDS" ]; then
    warn "发现 OOM Killer 记录："
    echo "$OOM_RECORDS" | sed 's/^/  /'
    info "建议：增加 SWAP 或降低 Gateway 内存限制"
  else
    ok "无 OOM Killer 记录"
  fi
}

optimize_gateway_config() {
  report "=== 优化 Gateway 配置 ==="
  
  CONFIG_FILE="/root/.openclaw/config/gateway.yml"
  if [ ! -f "$CONFIG_FILE" ]; then
    CONFIG_FILE="/root/.openclaw/config/gateway.yaml"
  fi
  
  if [ -f "$CONFIG_FILE" ]; then
    # 检查是否已有资源限制配置
    if grep -q "maxMemory\|maxWorkers\|concurrency" "$CONFIG_FILE" 2>/dev/null; then
      info "Gateway 已配置资源限制，跳过"
    else
      warn "Gateway 建议添加以下配置限制内存："
      echo "  gateway:"
      echo "    maxWorkers: 2"
      echo "    timeout: 30000"
      echo "  plugins:"
      echo "    entries:"
      echo "      http:"
      echo "        maxConnections: 10"
    fi
  else
    info "未找到配置文件，跳过配置优化"
  fi
}

# ---------- 主菜单 ----------
show_menu() {
  echo ""
  echo "====== Server Guardian 恢复菜单 ======"
  echo "  1) 执行完整健康检查"
  echo "  2) 重启 Gateway"
  echo "  3) 清理内存缓存"
  echo "  4) 查找高内存进程"
  echo "  5) 整理/压缩日志"
  echo "  6) 清理磁盘空间"
  echo "  7) 检查 OOM Killer"
  echo "  8) 优化 Gateway 配置建议"
  echo "  9) 执行完整恢复流程（推荐）"
  echo "  0) 退出"
  echo "======================================="
}

# ---------- 完整恢复流程 ----------
full_recovery() {
  report "=== 开始完整恢复流程 ==="
  
  local failed=0
  
  # Step 1: 日志整理
  rotate_logs
  
  # Step 2: 检查 OOM
  check_oom_killer
  
  # Step 3: 若内存告警，清理缓存
  MEM_PCT=$(free -m | awk '/^Mem:/ {print $3*100/$2}')
  if [ "${MEM_PCT%.*}" -gt 75 ]; then
    warn "内存使用率 ${MEM_PCT%.*}%，执行清理..."
    clear_mem_cache
    kill_high_mem_procs || true
  fi
  
  # Step 4: 重启 Gateway
  if ! recover_gateway; then
    ((failed++))
  fi
  
  # Step 5: 再次检查
  sleep 5
  if pgrep -f "openclaw gateway" > /dev/null; then
    ok "恢复完成，Gateway 运行正常"
  else
    error "恢复后 Gateway 仍未运行"
    ((failed++))
  fi
  
  if [ "$failed" -eq 0 ]; then
    ok "✅ 全部恢复成功"
  else
    warn "⚠ $failed 项操作失败，请人工介入"
  fi
}

# ---------- 主入口 ----------
ACTION="${1:-menu}"

case "$ACTION" in
  check)
    exec "$(dirname "$0")/health_check.sh"
    ;;
  full)
    full_recovery
    ;;
  restart)
    recover_gateway
    ;;
  mem)
    clear_mem_cache
    ;;
  procs)
    kill_high_mem_procs
    ;;
  logs)
    rotate_logs
    ;;
  disk)
    free_disk_space
    ;;
  oom)
    check_oom_killer
    ;;
  optimize)
    optimize_gateway_config
    ;;
  menu|*)
    if [ "$ACTION" = "menu" ]; then
      show_menu
      read -p "选择操作 [0-9]: " opt
      case "$opt" in
        1) exec "$(dirname "$0")/health_check.sh" ;;
        2) recover_gateway ;;
        3) clear_mem_cache ;;
        4) kill_high_mem_procs ;;
        5) rotate_logs ;;
        6) free_disk_space ;;
        7) check_oom_killer ;;
        8) optimize_gateway_config ;;
        9) full_recovery ;;
        0) exit 0 ;;
        *) error "无效选择" ;;
      esac
    fi
    ;;
esac
