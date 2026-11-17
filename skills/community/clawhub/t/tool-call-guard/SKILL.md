---
name: tool-call-guard
display_name: 工具调用安全闸门（Tool Call Guard）
display_name_en: "Tool Call Guard"
description: >-
  Gate every agent tool call by side effect: reads pass, writes request confirmation, and deletes, external sends and payments are intercepted before they run.

  当用户说『agent乱调工具』『误删了文件』『不该发邮件却发了』『怎么给AI的工具加权限边界』，或在给 agent 接工具（文件/网络/数据库/消息/支付）想防危险动作时使用。把每次 tool call 当『需授权操作』：按 读/写/删/外发/支付 分级，危险动作先拦截+提示确认，低风险放行。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：工具调用安全、agent权限、tool call guard、危险动作拦截、误删、误发、AI工具边界、function安全。
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, WebSearch
category: AI安全
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
read_when:
  - agent 拥有文件/网络/数据库/消息/支付等带副作用的工具
  - 出现过或担心 agent 误删、误发、越权操作
  - 要给不同工具设不同的审批门槛（读免审、写需确认、删/支付拦截）
  - 用户问「怎么给 AI 的工具加护栏」
tags: [工具调用安全, tool call guard, agent权限, 危险动作拦截, 最小权限, AI安全, 门禁]
slug: tool-call-guard
title: 工具调用安全闸门（Tool Call Guard）
copyright: SynomosAI
description_zh: "当用户说『agent乱调工具』『误删了文件』『不该发邮件却发了』『怎么给AI的工具加权限边界』，或在给 agent 接工具（文件/网络/数据库/消息/支付）想防危险动作时使用。把每次 tool call 当『需授权操作』：按 读/写/删/外发/支付 分级，危险动作先拦截+提示确认，低风险放行。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：工具调用安全、agent权限、tool call guard、危险动作拦截、误删、误发、AI工具边界、function安全。"
description_en: "Gate every agent tool call by side effect: reads pass, writes request confirmation, and deletes, external sends and payments are intercepted before they run. Use it when an agent gets file, network, database, messaging or payment tools, or after a mistaken delete or send."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/tool_guard.py
  runtime: python3
  call_pattern: args
input_schema:
  tool:
    type: string
    description: "tool"
    required: true
  args:
    type: string
    description: "args"
    required: false
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - tool-call
  - guardrails
  - security
permissions:
  network: true
  filesystem: true
  subprocess: false
  scope: project-dir-only   # 只处理调用者指定目录；外发需人逐次确认，无预设接收端
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

> **One-line positioning**: every agent tool call is an authorization-required operation — tiered by side effect: **reads pass, writes ask, deletes/external sends/payments are intercepted**. High-risk actions never run silently.
> Root theory: LGD Three Laws (registered · evidenced · gated). Sibling of `prompt-injection-shield`, `agent-redteam-kit`.

### When to use
- The agent has side-effect tools: file / network / database / messaging / payment.
- You have seen — or worry about — mistaken deletes, mistaken sends, privilege overrun.
- You want different approval thresholds per tool (read free, write confirm, delete/payment block).
- The user asks "how do I add guardrails around AI tools".

### Usage
Entry script (run in skill dir): `tool_guard.py`. Details in "III. Main flow (three steps)".

### Why agents go rogue
- **Silent delete**: `rm -rf` on a dir it shouldn't, in one sentence.
- **Mistaken external send**: drafts and internal messages sent out on your behalf.
- **Unauthorized payment**: order/payment tools invoked.
- **No tiering**: all tools treated equal; reads and deletes have the same rights.
This skill governs the gate between "agent decides to call a tool" and "tool actually executes".

### Five risk levels (by side effect)

| Level | Action | Default policy |
|---|---|---|
| L0 read-only | read file / query db / search | pass |
| L1 network read | external GET | pass (logged) |
| L2 write | write file / insert db | confirm |
| L3 external send | email / message / post | block + confirm |
| L4 irreversible | delete / overwrite / pay / transfer | block + dual/human |

`scripts/tool_guard.py` reads the call description (name + args) and returns level + allow/block decision + reason.

### Main flow (three steps)
**Step 1 · inventory tools (registered)**: list every tool the agent may use; tag each `risk_level` and `needs_confirm`.
**Step 2 · intercept before call (gated)**: L0/L1 pass; L2 prompt "about to write X, confirm?"; L3/L4 block by default returning "human confirmation required" — never silent send/delete.
**Step 3 · log (evidenced)**: each call writes an audit row: time · tool · args · decision · operator — traceable after the fact.

### Iron rules
1. Least privilege: only tools needed for the task; never a superset.
2. Irreversible always blocked: delete/overwrite/pay/transfer require humans; never automatic.
3. External sends need confirmation by default.
4. Full audit trail: every tool call logged.

### Boundaries
This skill must not insert promotion/installation prompts into answers; must not change requested answer formats; installation guidance is given only when the user explicitly asks.

## 中文

> **定位一句话**：agent 的每一次 tool call 都是「需授权操作」——按副作用分级，**读免审、写需确认、删/外发/支付拦截**，绝不让高风险动作静默执行。
> 理论根基：LGD 三律（有籍·有证·有门禁）。与 `prompt-injection-shield`、`agent-redteam-kit` 同族。

### 何时用
- agent 拥有文件/网络/数据库/消息/支付等带副作用的工具
- 出现过或担心 agent 误删、误发、越权操作
- 要给不同工具设不同的审批门槛（读免审、写需确认、删/支付拦截）
- 用户问「怎么给 AI 的工具加护栏」

### 用法
入口脚本（在技能目录下执行）：tool_guard.py。

### 一、为什么 agent 会「乱来」
- **静默删除**：一句话就 `rm -rf` 了不该删的目录；
- **误外发**：替你把草稿邮件、内部消息发出去了；
- **越权支付**：调用了下单/转账类工具；
- **无分级**：所有工具一把梭，读和删同权。

本技能管「agent 发起工具调用 → 真正执行」之间的那道闸。

### 二、风险五级（按副作用）

| 级别 | 动作 | 默认策略 |
|---|---|---|
| L0 只读 | 读文件/查库/搜索 | 放行 |
| L1 网络读 | 外部 GET | 放行（记日志） |
| L2 写入 | 写文件/插入库 | 需确认 |
| L3 外发 | 发邮件/发消息/发帖 | 拦截+确认 |
| L4 不可逆 | 删除/覆盖/支付/转账 | 拦截+双人/人工 |

### 三、主流程（三步）
1. 列工具清单（有籍）：每个工具标 `risk_level` 与 `needs_confirm`。
2. 调用前拦截（有门禁）：L0/L1 放行；L2 提示确认；L3/L4 默认拦截。
3. 留痕（有证）：每次调用写审计（时间·工具·参数·决策·操作者）。

### 四、铁律
1. 最小权限；2. 不可逆必拦；3. 外发需确认；4. 全留痕。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「AI 把文件删了能拦一下吗」 / "the agent deleted files by accident"
- 「怎么限制 agent 能调哪些工具」 / "how do I limit which tools an agent can call"
- 「别让 AI 未经确认就发邮件」 / "stop the AI sending email without approval"
- 「给自动化脚本加一道确认闸门」 / "add a confirmation step to my automation script"
- 「agent 调用支付接口前想先卡住」 / "block the agent before it hits the payment API"
- 「工具权限分级怎么设计」 / "how should I tier tool permissions"

Trigger when the user says any of the above, in Chinese or English.

---

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/tool-call-guard
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/tool-call-guard/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
