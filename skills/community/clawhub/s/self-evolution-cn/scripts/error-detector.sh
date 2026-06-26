#!/bin/bash
# Self-Evolution-CN Error Detector Hook
# 检测命令失败并提醒记录错误
# 读取 CLAUDE_TOOL_OUTPUT 环境变量

set -e

# 检查工具输出是否指示错误
# CLAUDE_TOOL_OUTPUT 包含工具执行的结果
OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

# 指示错误的模式（不区分大小写匹配）
ERROR_PATTERNS=(
    "error:"
    "Error:"
    "ERROR:"
    "failed"
    "FAILED"
    "command not found"
    "No such file"
    "Permission denied"
    "fatal:"
    "Exception"
    "Traceback"
    "npm ERR!"
    "ModuleNotFoundError"
    "SyntaxError"
    "TypeError"
    "exit code"
    "non-zero"
)

# 检查输出是否包含任何错误模式
contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

# 仅在检测到错误时输出提醒
if [ "$contains_error" = true ]; then
    cat << 'EOF'
<error-detected>
检测到命令错误。如果满足以下条件，考虑记录到 .learnings/ERRORS.md：
- 错误是意外或非显而易见的
- 需要调查才能解决
- 可能在类似上下文中重复出现
- 解决方案可能对未来会话有帮助

使用 self-evolution-cn 技能格式：[ERR-YYYYMMDD-XXX]
</error-detected>
EOF
fi
