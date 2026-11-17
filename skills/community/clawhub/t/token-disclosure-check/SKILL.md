---
name: token-disclosure-check
description: 代币信息披露检查器 — 白皮书/披露文案核查必备要素（总量/分配/锁仓/团队/风险提示），含收益承诺即 FAIL（零依赖） 适用场景：当需要代币信息披露检查器能力时使用本技能；触发词：token-disclosure-check。
slug: token-disclosure-check
title: token-disclosure-check
version: 1.0.1
display_name: 代币信息披露检查器
display_name_en: Token Disclosure Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "代币信息披露检查器 — 白皮书/披露文案核查必备要素（总量/分配/锁仓/团队/风险提示），含收益承诺即 FAIL（零依赖）"
description_en: "Check token whitepapers and disclosure copy for required elements: total supply, allocation, lockup, team and risk warnings; return promises FAIL (zero-dependency)."
read_when:
  - 核查代币白皮书/披露文案必备要素是否齐全
  - 识别收益承诺/保本话术（即 FAIL）
  - 项目方披露缺斤少两时的合规初筛
  - 机器可读 JSON 输出（--json）
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [token-disclosure-check, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/token_disclosure_check.py
  runtime: python3
  call_pattern: args
input_schema:
  text:
    type: string
    description: "白皮书/披露文案全文或要点"
    required: true
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - token
  - disclosure
  - crypto
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

**token-disclosure-check** v1.0.1 · LGD competitive-advantage family · zero-dependency
Domain: blockchain · law mapping: TH-LGD-020

### The pain
Projects skimp on disclosure while quietly guaranteeing returns — failing regulators and harming holders.

### When to use
When the user needs token disclosure review.

### Usage
```bash
python scripts/token_disclosure_check.py --help
```
- Compliance PASS → rc=0; violation FAIL → rc=1; usage error → rc=2
- `--json` machine-readable output

### Workflow
1. Trigger: identify a token-disclosure task (see When to use).
2. Execute: run token_disclosure_check.py per Usage.
3. Verify: check output / exit code.
4. Deliver: present results.

### Disclaimer
Compliance pre-screening aid; not legal / investment / medical advice; consult licensed professionals for important decisions.

### LGD Three Laws
LGD-in-blockchain landing piece: every AI output is registered, evidenced and gated.

### Install & usage matrix
```bash
npx skills@1.7.0 add <this-skill-repo-url>
# or clone and copy into your agent skill dir; SKILL.md is the runbook
```
| Agent | Skill dir | Example |
|---|---|---|
| Claude Code | `~/.claude/skills/token-disclosure-check/` | agent calls `scripts/` per SKILL.md |
| Codex CLI / Cursor / other agents | respective skill dirs | same |
| Direct CLI | anywhere | `python scripts/token_disclosure_check.py --help` |

## 中文

**token-disclosure-check** v1.0.1 · LGD 竞争优势家族 · 零依赖
域：区块链 · 三律映射：TH-LGD-020

### 痛点
项目方披露缺斤少两还暗带保证收益话术，接不住监管也坑持有人

### 何时用
- 当用户需要代币信息披露检查器相关能力时。

### 用法
```bash
python scripts/token_disclosure_check.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2
- 支持 --json 机器可读输出

### 流程
1. 触发：识别代币信息披露检查器相关任务（见「何时用」）。
2. 执行：按「用法」运行token_disclosure_check.py。
3. 校验：核对脚本输出/退出码是否符合预期。
4. 交付：向用户呈现结果/产物。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

### 免责
本工具为合规初筛辅助，不构成法律/投资/医疗意见；重要决策请咨询持牌专业人士。

### LGD 三律（有籍·有证·有门禁）
本技能是「LGD 三律」在区块链场景的落地件：让 AI 的每一次输出有籍可查、有证可依、有门禁可控。
