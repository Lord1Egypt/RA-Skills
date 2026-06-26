#!/bin/bash
# TagMemory CLI Wrapper
# 用法: tag-memory <command> [args...]

# 使用绝对路径
CLI_PATH="/home/twrp/.openclaw/workspace/skills/tag-memory/src/cli.py"
PYTHON_CMD="python3"

# 命令处理
case "$1" in
    store)
        shift
        $PYTHON_CMD "$CLI_PATH" store "$@"
        ;;
    query)
        shift
        $PYTHON_CMD "$CLI_PATH" query "$@"
        ;;
    list)
        shift  # remove 'list' from args
        $PYTHON_CMD "$CLI_PATH" list --page=1 --page-size=5 "$@"
        ;;
    stats)
        $PYTHON_CMD "$CLI_PATH" stats
        ;;
    verify|verify-pending)
        shift  # remove 'verify-pending' from args
        $PYTHON_CMD "$CLI_PATH" verify-pending --max=3 "$@"
        ;;
    summarize)
        shift
        $PYTHON_CMD "$CLI_PATH" summarize "$@"
        ;;
    summarize-confirm)
        shift
        $PYTHON_CMD "$CLI_PATH" summarize-confirm "${@:-confirm}"
        ;;
    help|--help|-h)
        echo "TagMemory CLI - 标签化长期记忆系统"
        echo ""
        echo "用法: tag-memory <command> [args...]"
        echo ""
        echo "命令:"
        echo "  store <内容> [tags...]     存储记忆"
        echo "  query <内容>              查询记忆"
        echo "  list [--page=N]          列出记忆"
        echo "  stats                    查看统计"
        echo "  verify-pending [--max=N] 待核对列表"
        echo "  summarize [--days=N]     生成总结"
        echo "  summarize-confirm [反馈] 确认总结"
        echo ""
        ;;
    *)
        $PYTHON_CMD "$CLI_PATH" "$@"
        ;;
esac
