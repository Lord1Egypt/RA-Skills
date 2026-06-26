#!/bin/bash
# inject_review.sh — Self-review prompt generator (单源)
# v4.0.0 — 触发规则参考 Hermes Agent，agent 自触发，不靠 hook 计数
# handler.js 通过 runScript() 调用，环境变量传入 LEARNINGS_DIR
# 也可直接调用: LEARNINGS_DIR=xxx bash inject_review.sh

LEARNINGS_DIR="${LEARNINGS_DIR:-$(pwd)/.learnings}"

python3 << 'PYEOF'
import os
ld = os.environ.get('LEARNINGS_DIR', '')
prompt = """
## 🔮 Self-Review — 任务回顾

如果在这次交互中出现以下任一情况，请主动触发回顾：
- 工具调用 ≥ 5
- 发现了非显而易见的解决方案或绕弯
- 预判这个工作流会重复

请按以下格式填写，完成后：
- 如果"技能候选"填了"有"→ 评价是否值得创建技能，值得则用 /create-skill 创建
- 如果"技能候选"填了"无"→ 将本次回顾写入 `{ld}/LEARNINGS.md`（参考模板格式）

```
## [YYYYMMDD-NNN] correction|best_practice|insight
**Logged**: YYYY-MM-DD
**Status**: pending
**Pattern-Key**: <source>.<type>.<identifier>

### What Happened
[描述这次用了什么方法、按什么顺序操作]

### Root Cause
[有没有坑/绕弯/失败的原因，没有就写"无"]

### How To Avoid Next Time
[下次怎么做更好，一句话可操作原则]

### 技能候选
- 有 / 无
- 标题：[给技能起个名字]
- 触发：[什么情况下用]
- 规则：[2-3句核心规则]
```
""".format(ld=ld)
print(prompt)
PYEOF