#!/bin/bash
# cross-agent - 主入口脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_help() {
    cat << 'EOF'
🔌 Cross-Agent 跨机器Agent协作

用法: openclaw cross-agent <命令> [参数]

命令:
  scan      扫描局域网内在线设备
  test      测试SSH连接
  sessions  查看目标机器的OpenClaw会话
  send      发送任务给目标Agent
  get       从目标机器获取文件
  put       向目标机器发送文件
  exec      在目标机器执行命令
  config    配置默认参数
  wizard    交互式配置向导

示例:
  # 扫描网络
  openclaw cross-agent scan 192.168.3.0/24

  # 测试连接
  openclaw cross-agent test 192.168.3.54 admin 123456

  # 发送任务
  openclaw cross-agent send 192.168.3.54 "请搜索教程" admin 123456

  # 获取文件
  openclaw cross-agent get 192.168.3.54 ~/Desktop/doc.md ~/Desktop/ admin 123456

  # 交互式向导
  openclaw cross-agent wizard

更多信息: openclaw cross-agent <命令> --help
EOF
}

# 检查参数
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

COMMAND="$1"
shift

case "$COMMAND" in
    scan)
        exec "${SCRIPT_DIR}/scripts/scan.sh" "$@"
        ;;
    test)
        exec "${SCRIPT_DIR}/scripts/test.sh" "$@"
        ;;
    sessions)
        exec "${SCRIPT_DIR}/scripts/sessions.sh" "$@"
        ;;
    send)
        exec "${SCRIPT_DIR}/scripts/send.sh" "$@"
        ;;
    get)
        exec "${SCRIPT_DIR}/scripts/get.sh" "$@"
        ;;
    put)
        exec "${SCRIPT_DIR}/scripts/put.sh" "$@"
        ;;
    exec)
        exec "${SCRIPT_DIR}/scripts/exec.sh" "$@"
        ;;
    config)
        exec "${SCRIPT_DIR}/scripts/config.sh" "$@"
        ;;
    wizard)
        exec "${SCRIPT_DIR}/scripts/wizard.sh"
        ;;
    help|--help|-h)
        show_help
        exit 0
        ;;
    *)
        echo "❌ 未知命令: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac