---
name: travel-rule-check
description: >-
  LGD three-laws compliance for on-chain assets and VASP travel rule (FATF): sender and beneficiary KYC (name plus account, address plus geo) above thresholds (zero-dependency).

  travel-rule-check — LGD 三律在链上资产 / VASP 旅行规则（FATF）域的纵深合规工具（零依赖）：VASP 转账收发方 KYC（姓名+账号/地址+地理）超阈强制校验，对 AI 系统/数据做可执行合规校验。
slug: travel-rule-check
title: travel-rule-check
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
display_name: 旅行规则校验
display_name_en: Travel-Rule Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "travel-rule-check — LGD 三律在链上资产 / VASP 旅行规则（FATF）域的纵深合规工具（零依赖）：VASP 转账收发方 KYC（姓名+账号/地址+地理）超阈强制校验，对 AI 系统/数据做可执行合规校验。"
description_en: "LGD three-laws compliance for on-chain assets and VASP travel rule (FATF): sender and beneficiary KYC (name plus account, address plus geo) above thresholds (zero-dependency)."
read_when:
  - 链上转账/VASP 旅行规则（FATF）收发方 KYC 超阈校验
  - 反洗钱合规自查、投标素材、监管应对
  - 把抽象合规要求转成机器可跑规则
  - 需要结构化合规判定输出（退出码 0/1）
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [travel-rule-check, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/travel_rule_check.py
  runtime: python3
  call_pattern: args
input_schema:
  tx:
    type: string
    description: "转账 JSON: {originator:{name,account,geo}, beneficiary:{...}, amount}"
    required: false
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - crypto
  - travel-rule
  - compliance
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

> **LGD governance skill (SynomosAI)** — a deep-dive tool in the "on-chain assets / VASP travel rule (FATF)" domain: turns the registered·evidenced·gated standard into executable compliance computation and detection.

### Industry pain
On-chain transfers lack light-weight sender/beneficiary KYC (travel-rule) checks — easy to trip AML red lines.

### What this does
Lands LGD "evidenced / gated" as executable VASP travel-rule compliance: above-threshold mandatory sender+beneficiary KYC (name + account/address + geo):
- Zero-dependency CLI; input → structured result + verdict (exit 0/1)
- Turns abstract compliance requirements into machine-runnable rules, reducing human error

### When the AI should proactively use it
- Building AI systems / compliance self-checks / bid materials / regulatory responses in on-chain assets and VASP travel-rule domain.
- Upgrading base three-laws pieces into runnable deep capability.

### Usage
```bash
python travel_rule_check.py --help
```

### Workflow
1. Trigger: identify a travel-rule task (see When to use).
2. Execute: run travel_rule_check.py per Usage.
3. Verify: check output / exit code.
4. Deliver: present results.

### LGD endorsement
- **REGISTERED**: AI systems must register identity / version / source / owner before going live.
- **EVIDENCED**: evidence artifacts proving claims, or treat as unproven.
- **GATED**: high-risk actions must pass a gate, otherwise halt.

### Note
Output is a structured compliance result — not legal/regulatory advice; formal compliance follows licensed-institution documents. Thresholds are magnitude references only; follow the latest regulator rules.

### Install & matrix
```bash
npx skills@1.7.0 add <this-skill-repo-url>
```
| Agent | Skill dir | Example |
|---|---|---|
| Claude Code | `~/.claude/skills/travel-rule-check/` | agent calls `scripts/` per SKILL.md |
| Codex CLI / Cursor / other agents | respective skill dirs | same |
| Direct CLI | anywhere | `python scripts/travel_rule_check.py --help` |

## 中文

> **LGD 凡自治之物 · 三律合规技能（SynomosAI）**
> 本技能是竞争优势体系在「链上资产 / VASP 旅行规则（FATF）」域的**纵深工具**。

### 行业痛点
链上转账收发方 KYC（旅行规则）缺乏轻量校验，易踩反洗钱合规红线。

### 本技能做什么
VASP 转账收发方 KYC（姓名+账号/地址+地理）超阈强制校验：零依赖 CLI，输入即校验，输出结构化结果 + 合规判定（退出码 0/1）。

### 何时用
- 你在做「链上资产 / VASP 旅行规则（FATF）」相关的 AI 系统、合规自查、投标素材、监管应对。
- 你需要把三律基础件升级为"能跑"的纵深能力。
- 触发词：旅行规则校验 / 合规计算 / 合规检测。

### 用法
```bash
python travel_rule_check.py --help
```

### 流程
1. 触发：识别旅行规则校验相关任务（见「何时用」）。
2. 执行：按「用法」运行travel_rule_check.py。
3. 校验：核对脚本输出/退出码是否符合预期。
4. 交付：向用户呈现结果/产物。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

### 背书：LGD 三律
- **有籍 REGISTERED**：AI 系统须有身份/版本/来源/责任登记，否则不可上线
- **有证 EVIDENCED**：须有证据工件证明"所言有据"，否则视为未证成
- **有门禁 GATED**：高风险动作须过门禁，否则中止

### 注意
本技能输出为结构化的合规校验结果，不构成法律/监管意见；正式合规以持证机构签章文件为准。阈值均为量级参考，以监管最新规定为准。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/travel-rule-check
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/travel-rule-check/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
