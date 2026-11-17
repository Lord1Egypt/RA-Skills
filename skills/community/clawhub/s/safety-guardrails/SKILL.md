---
name: safety-guardrails
description: |-
  给自主智能体/自动化流水线装上一道「预执行安全护栏」：对任何待执行动作做风险分级
  （low/medium/high/critical）并给出 ALLOW / CONFIRM / DENY 决策。内置破坏性强、不可逆、
  越权、外发隐私的 deny 规则与高影响 confirm 规则，强制拦截 rm -rf、强推、下载即执行、
  删表、关机等高危动作，并要求用户显式确认中高危操作。适配自动化每小时触发的无人值守场景，
  防止自主 agent 在没有护栏时造成不可逆损害。触发词：安全护栏、危险动作拦截、操作确认、
  safety guardrails、agent 安全、预执行校验、destructive 拦截。
agent_created: true
version: 1.0.0
display_name: "安全护栏"
display_name_en: "Safety Guardrails"
description_zh: "自主智能体的预执行安全护栏：风险分级+决策门+审计"
description_en: "Pre-execution safety guardrails for autonomous agents"
visibility: "public"
---

# 安全护栏（safety-guardrails）

## 什么时候用
- 自动化/自主 agent 要执行命令、改库、发消息、上线、转账等「有副作用」动作前。
- 无人值守场景（每小时触发的元进化、定时任务、CI）尤其需要——没有人在环兜底。
- 任何「先确认再执行」比「执行了再后悔」便宜得多的地方。

## 核心机制
1. **风险分级**：`classify(action)` 返回 (level, reasons)
   - `critical`：破坏性/不可逆/越权/下载即执行 → 默认 **DENY**
   - `high`：外发隐私/敏感越权 → **CONFIRM**（需 user_approved + high_risk_allowed）
   - `medium`：删除/写库/安装/提权/发布/支付 → **CONFIRM**（需 user_approved）
   - `low`：只读/低风险 → **ALLOW**
2. **决策门** `gate(action, context)`：返回 (decision, note, record)，并写入审计日志。
   context 字段：`user_approved`(是否用户确认)、`high_risk_allowed`(是否允许高危)。
3. **审计**：每次决策落盘（ts/action/level/decision/reason），`--audit` 可查。

## 内置规则（可扩展）
- DENY：`rm -rf`、`format`、`dd if=...of=/dev`、`shutdown/reboot`、`mkfs`、无条件 `drop/truncate`、
  `git push --force`、`git reset --hard`、fork 炸弹、`curl|bash`/`wget|sh` 下载即执行。
- CONFIRM：`rm -`、删除/更新/插入/改表、对外发送/upload/post、提权、安装依赖、终止进程、部署发布、资金转移。

## 用法
```bash
# 自检
python scripts/guardrails.py --selftest

# 单个动作决策
python scripts/guardrails.py --action "delete /tmp/cache" --context '{"user_approved":false}'
# => {"decision": "CONFIRM", "note": "需要用户确认：删除操作"}

# 查看审计日志
python scripts/guardrails.py --audit
```

## 与自动化/自主 agent 的集成
- 在调用 Bash/执行命令前先 `gate()`，决策为 DENY 直接中止；为 CONFIRM 时挂起等待人类确认。
- 配合 `human-in-loop-review`：CONFIRM 类动作转人工审核队列。
- 配合 `behavior-observability`：把 gate 决策与 action 落盘到行为日志，事后可审计归因。
---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
