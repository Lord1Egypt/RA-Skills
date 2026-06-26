#!/bin/bash
# Mini TimeBot skill 入口脚本（供外部 agent 非交互式调用）
#
# 用法:
#   bash selfskill/scripts/run.sh start                          # 后台启动服务
#   bash selfskill/scripts/run.sh stop                           # 停止服务
#   bash selfskill/scripts/run.sh status                         # 检查服务状态
#   bash selfskill/scripts/run.sh setup                          # 首次：安装环境依赖
#   bash selfskill/scripts/run.sh add-user <name> <password>     # 创建/更新用户
#   bash selfskill/scripts/run.sh configure <KEY> <VALUE>        # 设置 .env 配置项
#   bash selfskill/scripts/run.sh configure --batch K1=V1 K2=V2  # 批量设置配置
#   bash selfskill/scripts/run.sh configure --show               # 查看当前配置
#   bash selfskill/scripts/run.sh configure --init               # 从模板初始化 .env
#
# 所有命令均为非交互式，适合自动化调用。

set -e

# 定位项目根目录（skill/scripts/run.sh → 上两级）
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
export PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

# 激活虚拟环境
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

PIDFILE="$PROJECT_ROOT/.mini_timebot.pid"

case "${1:-help}" in

    start)
        if [ ! -f config/.env ]; then
            echo "❌ 未找到 config/.env，请先运行: $0 configure --init 并配置必要参数" >&2
            exit 1
        fi

        if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
            echo "⚠️  Mini TimeBot 已在运行 (PID: $(cat "$PIDFILE"))"
            exit 0
        fi

        echo "🚀 启动 Mini TimeBot (headless)..."
        export MINI_TIMEBOT_HEADLESS=1
        mkdir -p "$PROJECT_ROOT/logs"
        nohup python scripts/launcher.py > "$PROJECT_ROOT/logs/launcher.log" 2>&1 &
        LAUNCHER_PID=$!
        echo "$LAUNCHER_PID" > "$PIDFILE"
        echo "✅ Mini TimeBot 已在后台启动 (PID: $LAUNCHER_PID)"
        echo "   日志: $PROJECT_ROOT/logs/launcher.log"

        # 等待服务就绪
        source config/.env 2>/dev/null || true
        AGENT_PORT=${PORT_AGENT:-51200}
        echo -n "   等待服务就绪"
        for i in $(seq 1 30); do
            if curl -sf "http://127.0.0.1:$AGENT_PORT/v1/models" > /dev/null 2>&1; then
                echo " ✅"
                exit 0
            fi
            echo -n "."
            sleep 2
        done
        echo ""
        echo "⚠️  服务可能仍在启动中，请查看日志确认"
        exit 0
        ;;

    stop)
        if [ -f "$PIDFILE" ]; then
            PID=$(cat "$PIDFILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "正在停止 Mini TimeBot (PID: $PID)..."
                kill "$PID"
                for i in $(seq 1 30); do
                    if ! kill -0 "$PID" 2>/dev/null; then
                        break
                    fi
                    sleep 0.5
                done
                if kill -0 "$PID" 2>/dev/null; then
                    echo "⚠️  强制终止..."
                    kill -9 "$PID" 2>/dev/null
                fi
                echo "✅ 已停止"
            else
                echo "进程已不存在"
            fi
            rm -f "$PIDFILE"
        else
            echo "未找到 PID 文件，服务可能未运行"
        fi
        exit 0
        ;;

    status)
        if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
            PID=$(cat "$PIDFILE")
            echo "✅ Mini TimeBot 正在运行 (PID: $PID)"
            source config/.env 2>/dev/null || true
            for port in ${PORT_AGENT:-51200} ${PORT_SCHEDULER:-51201} ${PORT_OASIS:-51202} ${PORT_FRONTEND:-51209}; do
                if ss -tlnp 2>/dev/null | grep -q ":${port} " || netstat -tlnp 2>/dev/null | grep -q ":${port} "; then
                    echo "  ✅ 端口 $port 已监听"
                else
                    echo "  ⚠️  端口 $port 未监听"
                fi
            done
            exit 0
        else
            echo "❌ Mini TimeBot 未运行"
            exit 1
        fi
        ;;

    setup)
        echo "=== 环境配置 ==="
        bash scripts/setup_env.sh
        echo "=== 环境配置完成 ==="
        ;;

    add-user)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "用法: $0 add-user <username> <password>" >&2
            exit 1
        fi
        python selfskill/scripts/adduser.py "$2" "$3"
        exit 0
        ;;

    configure)
        shift
        python selfskill/scripts/configure.py "$@"
        exit 0
        ;;

    help|--help|-h)
        echo "Mini TimeBot Skill 入口"
        echo ""
        echo "用法: bash selfskill/scripts/run.sh <command> [args]"
        echo ""
        echo "命令:"
        echo "  start                          后台启动服务"
        echo "  stop                           停止服务"
        echo "  status                         检查服务状态"
        echo "  setup                          安装环境依赖（首次）"
        echo "  add-user <name> <password>     创建/更新用户"
        echo "  configure <KEY> <VALUE>        设置 .env 配置项"
        echo "  configure --batch K1=V1 K2=V2  批量设置配置"
        echo "  configure --show               查看当前配置"
        echo "  configure --init               从模板初始化 .env"
        echo "  help                           显示此帮助"
        exit 0
        ;;

    *)
        echo "未知命令: $1" >&2
        echo "运行 '$0 help' 查看可用命令" >&2
        exit 1
        ;;
esac
