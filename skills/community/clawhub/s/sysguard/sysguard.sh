#!/usr/bin/env bash
#===============================================================================
# SysGuard v2.0 - Main Entry Point
#===============================================================================

# Resolve real path (follow symlinks)
REAL_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$REAL_PATH")" && pwd)"

# === Load and Execute ===
source "$SCRIPT_DIR/scripts/lib/logger.sh"
source "$SCRIPT_DIR/scripts/lib/config.sh"
source "$SCRIPT_DIR/scripts/lib/util.sh"

CMD="${1:-status}"

case "$CMD" in
    status|gs)
        source "$SCRIPT_DIR/scripts/health_check.sh"
        source "$SCRIPT_DIR/scripts/ui.sh"
        run_health_check | format_status
        ;;
    check)
        source "$SCRIPT_DIR/scripts/health_check.sh"
        run_health_check
        ;;
    diagnose|diag)
        source "$SCRIPT_DIR/scripts/diagnostics.sh"
        run_diagnostics
        ;;
    trend|graph)
        source "$SCRIPT_DIR/scripts/trend.sh"
        show_trend "${2:-24}"
        ;;
    clean|gc)
        source "$SCRIPT_DIR/scripts/clean.sh"
        run_clean
        ;;
    monitor)
        source "$SCRIPT_DIR/scripts/monitor.sh"
        run_monitor
        ;;
    notify)
        source "$SCRIPT_DIR/scripts/notifier.sh"
        send_notification "SysGuard 测试" "${2:-Test message}"
        ;;
    help|--help|-h)
        echo "SysGuard v2.0 - OpenClaw 系统守护"
        echo ""
        echo "Usage: sysguard <command>"
        echo ""
        echo "Commands:"
        echo "  gs, status    Show status (IM-friendly)"
        echo "  check         Run health check"
        echo "  diagnose      Run diagnostic report"
        echo "  trend [hours] Show trend chart"
        echo "  clean, gc     Clean cache"
        echo "  monitor       Start monitoring daemon"
        echo "  notify <msg>  Send test notification"
        echo "  help          Show this help"
        ;;
    *)
        echo "Unknown command: $CMD"
        echo "Run 'sysguard help' for usage"
        exit 1
        ;;
esac
