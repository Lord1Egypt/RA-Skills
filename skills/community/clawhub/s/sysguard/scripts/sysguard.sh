#!/usr/bin/env bash
#===============================================================================
# SysGuard - System Guardian for OpenClaw
# Main Entry Point
#===============================================================================

set -euo pipefail

# === Paths ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$SKILL_DIR/config"
DATA_DIR="$SKILL_DIR/data"
LIB_DIR="$SCRIPT_DIR/lib"

# === Load Libraries ===
for lib in "$LIB_DIR"/*.sh; do
    [[ -f "$lib" ]] && source "$lib"
done

# === Command Hints ===
show_hints() {
    echo ""
    echo "💡 sgc清理 | sgch检查 | sgd诊断 | sgt趋势 | sgm监控"
}

# === Command Router ===
CMD="${1:-}"

# === Default: Show Status ===
if [[ -z "$CMD" ]] || [[ "$CMD" == "sg" ]]; then
    source "$SCRIPT_DIR/health_check.sh"
    source "$SCRIPT_DIR/ui.sh"
    run_health_check | format_status
    show_hints
    exit 0
fi

case "$CMD" in
    # sgc = clean
    sgc)
        source "$SCRIPT_DIR/clean.sh"
        run_clean
        ;;
    # sgch = check (c taken by clean, so +h)
    sgch|check)
        source "$SCRIPT_DIR/health_check.sh"
        run_health_check
        ;;
    # sgd = diagnose
    sgd|diagnose)
        source "$SCRIPT_DIR/diagnostics.sh"
        run_diagnostics
        ;;
    # sgt = trend (12h default)
    sgt|trend)
        HOURS="${2:-12}"
        source "$SCRIPT_DIR/trend.sh"
        show_trend "$HOURS"
        ;;
    # sgm = monitor (daemon)
    sgm|monitor)
        source "$SCRIPT_DIR/monitor.sh"
        run_monitor
        ;;
    # Legacy commands (for compatibility)
    status|gs)
        source "$SCRIPT_DIR/health_check.sh"
        source "$SCRIPT_DIR/ui.sh"
        run_health_check | format_status
        show_hints
        ;;
    clean)
        source "$SCRIPT_DIR/clean.sh"
        run_clean
        ;;
    diagnose)
        source "$SCRIPT_DIR/diagnostics.sh"
        run_diagnostics
        ;;
    health-check|hc)
        source "$SCRIPT_DIR/health_check.sh"
        run_health_check
        ;;
    trend)
        HOURS="${2:-12}"
        source "$SCRIPT_DIR/trend.sh"
        show_trend "$HOURS"
        ;;
    help|--help|-h)
        echo "SysGuard v2.1 - 系统守护"
        echo ""
        echo "用法: sg <命令>"
        echo ""
        echo "命令:"
        echo "  sg           系统状态 + 命令提示"
        echo "  sgc          清理缓存"
        echo "  sgch         健康检查"
        echo "  sgd          诊断报告"
        echo "  sgt [小时]   趋势图 (默认12小时)"
        echo "  sgm          守护监控"
        echo ""
        echo "示例:"
        echo "  sg           # 查看状态"
        echo "  sgc          # 清理缓存"
        echo "  sgt 24       # 查看24小时趋势"
        ;;
    *)
        echo "未知命令: $CMD"
        echo "输入 sg 查看可用命令"
        exit 1
        ;;
esac
