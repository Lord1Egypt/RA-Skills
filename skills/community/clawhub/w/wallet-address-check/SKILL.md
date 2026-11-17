---
name: wallet-address-check
description: 链上地址格式校验器 — 转账前校验 EVM/BTC系/TRON 地址格式与链系归属，格式可疑即 FAIL（零依赖） 适用场景：当需要链上地址格式校验器能力时使用本技能；触发词：wallet-address-check。
slug: wallet-address-check
title: wallet-address-check
version: 1.0.1
display_name: 链上地址格式校验器
display_name_en: Wallet Address Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "链上地址格式校验器 — 转账前校验 EVM/BTC系/TRON 地址格式与链系归属，格式可疑即 FAIL（零依赖）"
description_en: "Validate EVM, BTC-family and TRON wallet address format and chain attribution before transfers; suspicious formats FAIL (zero-dependency)."
read_when:
  - 转账前校验 EVM/BTC/TRON 地址格式与链系归属
  - 防止地址粘错链/抄错位导致资产归零
  - 可疑格式即 FAIL 的转账前格式门
  - 机器可读 JSON 输出（--json）
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [wallet-address-check, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/wallet_address_check.py
  runtime: python3
  call_pattern: args
input_schema:
  address:
    type: string
    description: "address"
    required: true
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - crypto
  - wallet
  - address
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

**wallet-address-check** v1.0.1 · LGD competitive-advantage family · zero-dependency
Domain: blockchain · law mapping: TH-LGD-019

### The pain
A slipped paste — wrong chain, or a mis-copied digit — wipes the assets. Put a format gate before every transfer.

### When to use
When the user needs on-chain address format validation.

### Usage
```bash
python scripts/wallet_address_check.py --help
```
- PASS → rc=0; FAIL → rc=1; usage error → rc=2; `--json` available.

### Workflow
1. Trigger: identify a wallet-address task (see When to use).
2. Execute: run wallet_address_check.py per Usage.
3. Verify: check output / exit code.
4. Deliver: present results.

### Disclaimer
Compliance pre-screening aid; not legal/investment/medical advice.

### LGD Three Laws
LGD-in-blockchain landing piece: every AI output registered, evidenced, gated.

### Install & matrix
```bash
npx skills@1.7.0 add <this-skill-repo-url>
```
| Agent | Skill dir | Example |
|---|---|---|
| Claude Code | `~/.claude/skills/wallet-address-check/` | agent calls `scripts/` per SKILL.md |
| Codex CLI / Cursor / other agents | respective skill dirs | same |
| Direct CLI | anywhere | `python scripts/wallet_address_check.py --help` |

## 中文

**wallet-address-check** v1.0.1 · LGD 竞争优势家族 · 零依赖
域：区块链 · 三律映射：TH-LGD-019

### 痛点
转账手滑地址粘错链/抄错位，资产直接归零——先过一道格式门

### 何时用
- 当用户需要链上地址格式校验器相关能力时。

### 用法
```bash
python scripts/wallet_address_check.py --help
```
- 合规 PASS → rc=0；违规 FAIL → rc=1；用法错误 → rc=2；支持 --json。

### 流程
1. 触发：识别链上地址格式校验器相关任务（见「何时用」）。
2. 执行：按「用法」运行wallet_address_check.py。
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
