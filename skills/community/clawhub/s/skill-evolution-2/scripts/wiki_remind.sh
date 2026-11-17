#!/bin/bash
# 技能进化（知行环）— Claude Code Stop Hook 提醒脚本
# 在 Agent 完成响应时触发，若项目存在 .wiki/ 则输出记录提醒。
# 注意：本脚本只输出提醒文本，不代替 Agent 判断或写入内容。

set -u

# 确定项目根目录。
# 优先级：CLAUDE_PROJECT_DIR（Claude Code 运行时自动注入）→ PWD → pwd
#
# 注意：某些沙箱化 shell（如 WorkBuddy 的 bash 集成）在启动子进程时会 source
# 环境脚本并 cd 回工作区，导致子 shell 内的 $(pwd) 与调用者目录不一致。
# 因此本脚本在 Claude Code 下依赖 CLAUDE_PROJECT_DIR，不依赖 pwd。
# 手动测试时请显式传参：
#   CLAUDE_PROJECT_DIR=/path/to/project bash wiki_remind.sh
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-${PWD:-$(pwd)}}"

if [ ! -d "$PROJECT_DIR/.wiki" ]; then
  exit 0
fi

RAW_FILE="$PROJECT_DIR/.wiki/raw/$(date +%Y-%m-%d).md"

cat <<EOF
[技能进化] 会话结束前检查：本次任务是否有值得记录的经验？

若有（踩坑、失败、或有效的解决技巧），追加到：
  $RAW_FILE

格式（≤10 行，只记关键决策点和异常，不记流水账）：
  ### [HH:MM] 任务简述
  - **域**：coding | data | research | debug | deploy
  - **结果**：✅ 成功 / ❌ 失败 / ⚠️ 部分成功
  - **轨迹**：1. [关键步骤] → [结果]
  - **关键观察**：[意外发现 / 踩坑点 / 有效技巧]

若无值得记录的内容，忽略本提醒即可。
EOF

exit 0
