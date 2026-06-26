#!/usr/bin/env bash
# UserPromptSubmit hook for redline
#
# 配置进 ~/.claude/settings.json 后，每次用户发送 prompt 前会先跑这个脚本。
# 检查 cwd 下是否有 .redline-inbox.json：
#   有 → 把内容作为 additionalContext 注入到 prompt（连带 apply 指令）
#   无 → 静默退出，不影响正常对话
#
# 安装到 settings.json:
#   {
#     "hooks": {
#       "UserPromptSubmit": [
#         {"hooks": [{"type": "command", "command": "/abs/path/to/redline/hook.sh"}]}
#       ]
#     }
#   }

set -euo pipefail

# Claude Code 提供 $CLAUDE_PROJECT_DIR；fallback 到 PWD
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
INBOX="$PROJECT_DIR/.redline-inbox.json"

# 没有 inbox 就静默退出，不影响正常对话
[[ -f "$INBOX" ]] || exit 0

# 用 python 拼 JSON 输出，规避 bash JSON 转义
INBOX="$INBOX" python3 <<'PYEOF'
import json, os, sys

inbox_path = os.environ["INBOX"]
with open(inbox_path, "r", encoding="utf-8") as f:
    inbox_content = f.read()

context = f"""[redline hook] 检测到挂起的标注反馈：

```json
{inbox_content}
```

请按 redline skill 的"阶段 2：应用"流程处理这些标注：
1. 读 feedback-template.md 的渲染规则
2. 用 Edit 工具修改 inbox 里 `file` 字段对应的源文件（不要碰 .annotated.html）
3. apply 完成后，**必须**用 Bash 跑 `rm {inbox_path}`，否则下一次 prompt 会重复触发
4. 简明汇报每条标注的处理结果（✓ 已改 / ✗ 未匹配 / ⚠ 冲突已合并）

如果用户当前消息和反馈完全无关，先问"检测到 N 条挂起反馈，先处理还是继续当前话题？"，由用户决定。
"""

output = {
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": context,
    }
}
print(json.dumps(output, ensure_ascii=False))
PYEOF
