#!/bin/bash
# 太极框架启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 默认值
MODE="auto"
WORKERS="3"
REQUEST=""
CONFIG_FILE="config.yaml"
LOG_LEVEL="INFO"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --workers)
            WORKERS="$2"
            shift 2
            ;;
        --request|-r)
            REQUEST="$2"
            shift 2
            ;;
        --config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        --log-level)
            LOG_LEVEL="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --mode MODE        centralized|distributed|hybrid|auto (default: auto)"
            echo "  --workers N        Number of workers (default: 3)"
            echo "  --request, -r TEXT User request text"
            echo "  --config FILE      Config file path (default: config.yaml)"
            echo "  --log-level LEVEL  DEBUG|INFO|WARNING|ERROR (default: INFO)"
            echo "  --help, -h        Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

export TAICHI_WORKSPACE="${TAICHI_WORKSPACE:-./workspace}"
export PYTHONPATH="$SCRIPT_DIR"
export TAICHI_LOG_LEVEL="$LOG_LEVEL"

echo "Starting Taichi Framework:"
echo "  Mode:    $MODE"
echo "  Workers: $WORKERS"
echo "  Request:  ${REQUEST:-<none>}"
echo "  Log:      $LOG_LEVEL"
echo ""

# 构造参数数组，避免 shell 引用问题
PYTHON_ARGS=(--config "$CONFIG_FILE" --mode "$MODE" --workers "$WORKERS")
if [[ -n "$REQUEST" ]]; then
    PYTHON_ARGS+=(--request "$REQUEST")
fi

exec python orchestrator.py "${PYTHON_ARGS[@]}"
