#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-status}"
shift || true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─── 定位运行环境 ────────────────────────────────────────────
# 只使用已安装的正式 .app（自带内嵌 Python 和稳定 CLI 入口），
# 与 Windows 普通用户安装路径保持一致。

APP_CLI=""
ROOT=""
PYTHON=""

find_installed_app() {
    local candidate
    for candidate in \
        "${SCREEN_AUTOMATION_MAC_APP:-}" \
        "/Applications/Screen Automation Helper.app" \
        "$HOME/Applications/Screen Automation Helper.app"; do
        [[ -n "$candidate" ]] || continue
        if [[ -x "$candidate/Contents/MacOS/screen-automation-helper" ]]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done
    return 1
}

if APP_BUNDLE="$(find_installed_app)"; then
    APP_CLI="$APP_BUNDLE/Contents/MacOS/screen-automation-helper"
    ROOT="$APP_BUNDLE/Contents/Resources/screen-automation-helper"
    PYTHON="$APP_BUNDLE/Contents/Resources/python/bin/python3"
else
    cat <<'EOF'
{"ok": false, "platform": "macos", "error": "未找到屏幕自动化小助手。请从官网下载 macOS 安装包，将“屏幕自动化小助手”拖入“应用程序”后重试。", "instruction": "如安装在特殊位置，可设置 SCREEN_AUTOMATION_MAC_APP 指向 .app。"}
EOF
    exit 2
fi

BRIDGE="$ROOT/packaging/macos/workflow_bridge.py"

run_bridge() {
    if [[ ! -f "$BRIDGE" ]]; then
        echo '{"ok": false, "platform": "macos", "error": "当前安装包内未包含流程桥接脚本，请更新到支持流程管理的版本。"}'
        exit 2
    fi
    PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}" "$PYTHON" "$BRIDGE" "$@"
}

run_cli() {
    "$APP_CLI" "$@"
}

case "$ACTION" in
    cli-path)
        printf '%s\n' "$APP_CLI"
        ;;
    status)
        run_bridge status
        ;;
    capabilities)
        # 以本机实际 CLI 返回为准，不再硬编码能力清单。
        run_cli cli capabilities "$@"
        ;;
    health)
        run_cli cli health "$@"
        ;;
    list)
        run_bridge list
        ;;
    show|detail)
        [[ -n "${1:-}" ]] || { echo '{"ok": false, "error": "show 需要流程标识"}' ; exit 2; }
        run_bridge detail --workflow "$1"
        ;;
    inspect)
        [[ -n "${1:-}" ]] || { echo '{"ok": false, "error": "inspect 需要目录或流程标识"}' ; exit 2; }
        if [[ -e "$1" ]]; then
            run_cli cli workflow inspect "$1"
        else
            run_bridge detail --workflow "$1"
        fi
        ;;
    validate)
        [[ -n "${1:-}" ]] || { echo '{"ok": false, "error": "validate 需要目录或流程标识"}' ; exit 2; }
        if [[ -e "$1" ]]; then
            run_cli cli workflow validate "$1"
        else
            run_bridge detail --workflow "$1"
        fi
        ;;
    install)
        [[ -n "${1:-}" ]] || { echo '{"ok": false, "error": "install 需要源码目录或压缩包"}' ; exit 2; }
        run_bridge install --source "$1"
        ;;
    remove)
        [[ -n "${1:-}" ]] || { echo '{"ok": false, "error": "remove 需要流程标识"}' ; exit 2; }
        run_bridge remove --workflow "$1"
        ;;
    restore)
        [[ -n "${1:-}" ]] || { echo '{"ok": false, "error": "restore 需要流程标识"}' ; exit 2; }
        run_bridge restore --workflow "$1"
        ;;
    start|debug)
        [[ -n "${1:-}" ]] || { echo "{\"ok\": false, \"error\": \"$ACTION 需要流程标识\"}" ; exit 2; }
        run_bridge "$ACTION" --workflow "$1"
        ;;
    stop)
        if [[ -n "${1:-}" ]]; then
            run_bridge stop --run-id "$1"
        else
            run_bridge stop
        fi
        ;;
    pause-run)
        [[ -n "${1:-}" ]] || { echo '{"ok": false, "error": "pause-run 需要 run-id"}' ; exit 2; }
        run_bridge pause --run-id "$1"
        ;;
    resume-run)
        [[ -n "${1:-}" ]] || { echo '{"ok": false, "error": "resume-run 需要 run-id"}' ; exit 2; }
        run_bridge resume --run-id "$1"
        ;;
    continue-debug)
        if [[ -n "${1:-}" ]]; then
            run_bridge continue-debug --run-id "$1"
        else
            run_bridge continue-debug
        fi
        ;;
    runs)
        run_bridge status
        ;;
    target)
        run_cli cli window wait-selection "$@"
        ;;
    task-begin)
        run_cli cli task begin "$@"
        ;;
    task-status)
        run_cli cli task status "$@"
        ;;
    task-refresh)
        run_cli cli window refresh "$@"
        ;;
    task-restore)
        run_cli cli window restore "$@"
        ;;
    task-activate)
        run_cli cli window activate "$@"
        ;;
    task-ensure-visible)
        run_cli cli window ensure-visible "$@"
        ;;
    task-move)
        run_cli cli window move "$@"
        ;;
    task-resize)
        run_cli cli window resize "$@"
        ;;
    task-observe)
        run_cli cli task observe "$@"
        ;;
    task-find)
        run_cli cli task find "$@"
        ;;
    task-wait)
        run_cli cli task wait "$@"
        ;;
    task-click)
        run_cli cli task click "$@"
        ;;
    task-long-press)
        run_cli cli task long-press "$@"
        ;;
    task-drag)
        run_cli cli task drag "$@"
        ;;
    task-scroll)
        run_cli cli task scroll "$@"
        ;;
    task-write)
        run_cli cli task write "$@"
        ;;
    task-hotkey)
        run_cli cli task hotkey "$@"
        ;;
    task-end)
        run_cli cli task end "$@"
        ;;
    *)
        cat <<'EOF'
{"ok": false, "platform": "macos", "error": "不支持该动作。可先运行 capabilities 查看当前 Mac 核心能力。"}
EOF
        exit 2
        ;;
esac
