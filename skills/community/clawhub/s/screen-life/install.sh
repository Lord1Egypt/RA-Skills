#!/usr/bin/env bash
# screen-life install.sh — 一键安装 macOS 行为监控守护进程

set -e
MONITOR_HOME="$HOME/.orbitos-monitor"
SCRIPTS_DIR="$MONITOR_HOME/scripts"
LOGS_DIR="$MONITOR_HOME/logs"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─── 检查依赖的 orbitos-monitor 脚本 ───────────────────────────────────────────
ORBITOS_SCRIPTS="$HOME/.orbitos-monitor/scripts"
if [ ! -d "$ORBITOS_SCRIPTS" ]; then
  echo "⚠️  未找到 ~/.orbitos-monitor/scripts"
  echo "   将使用 screen-life 内置精简版守护进程"
  USE_BUILTIN=1
fi

usage() {
  echo "Usage: $0 [install|status|stop|restart|report|uninstall]"
  echo ""
  echo "  install    安装并启动守护进程（默认）"
  echo "  status     检查守护进程状态"
  echo "  stop       停止守护进程"
  echo "  restart    重启守护进程"
  echo "  report     立即生成今日报告"
  echo "  uninstall  卸载守护进程"
}

cmd_install() {
  echo "🔧 安装 screen-life 守护进程..."
  mkdir -p "$MONITOR_HOME/scripts" "$LOGS_DIR"

  # 复制守护脚本
  if [ "${USE_BUILTIN:-0}" = "1" ]; then
    cp "$SKILL_DIR/daemon.py" "$SCRIPTS_DIR/activity_daemon.py"
    cp "$SKILL_DIR/handler.py" "$SCRIPTS_DIR/report_generator.py"
    echo "  ✅ 已复制内置守护脚本"
  fi

  # 创建 launchd plist
  PLIST_PATH="$HOME/Library/LaunchAgents/com.screen-life.daemon.plist"
  PYTHON=$(which python3)
  cat > "$PLIST_PATH" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.screen-life.daemon</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$SCRIPTS_DIR/activity_daemon.py</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$MONITOR_HOME/daemon.log</string>
  <key>StandardErrorPath</key>
  <string>$MONITOR_HOME/daemon.err</string>
</dict>
</plist>
PLIST

  launchctl load "$PLIST_PATH" 2>/dev/null || launchctl bootstrap gui/$UID "$PLIST_PATH" 2>/dev/null || true
  echo "  ✅ 守护进程已启动"
  echo ""
  echo "✅ screen-life 安装完成！"
  echo "   日志目录: $LOGS_DIR"
  echo "   查看报告: python3 $SKILL_DIR/handler.py"
}

cmd_status() {
  python3 "$SKILL_DIR/handler.py" --status
}

cmd_stop() {
  PLIST_PATH="$HOME/Library/LaunchAgents/com.screen-life.daemon.plist"
  launchctl unload "$PLIST_PATH" 2>/dev/null || launchctl bootout gui/$UID "$PLIST_PATH" 2>/dev/null || true
  echo "✅ 守护进程已停止"
}

cmd_restart() {
  cmd_stop
  sleep 1
  cmd_install
}

cmd_report() {
  python3 "$SKILL_DIR/handler.py"
}

cmd_uninstall() {
  cmd_stop
  PLIST_PATH="$HOME/Library/LaunchAgents/com.screen-life.daemon.plist"
  rm -f "$PLIST_PATH"
  echo "✅ 已卸载。数据目录保留在 $MONITOR_HOME"
  echo "   如需完全删除: rm -rf $MONITOR_HOME"
}

# ─── 入口 ─────────────────────────────────────────────────────────────────────
case "${1:-install}" in
  install)   cmd_install ;;
  status)    cmd_status ;;
  stop)      cmd_stop ;;
  restart)   cmd_restart ;;
  report)    cmd_report ;;
  uninstall) cmd_uninstall ;;
  *)         usage; exit 1 ;;
esac
