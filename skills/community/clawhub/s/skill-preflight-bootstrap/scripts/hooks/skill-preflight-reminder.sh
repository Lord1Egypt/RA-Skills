#!/bin/bash
set -e

cat <<'EOF'
<skill-preflight-reminder>
在处理当前任务前，先执行技能预检：
1. 运行 `./scripts/skill-preflight.py "<任务描述>"`
2. 如果本地结果不贴合，再运行 `./scripts/skill-preflight.py "<任务描述>" --remote`
3. 在首条执行说明里明确：本次准备使用哪些技能；如果没有合适技能，也要说明原因
4. 若过程中产生可复用经验、错误模式或流程改进，记录到 `.learnings/`
</skill-preflight-reminder>
EOF
