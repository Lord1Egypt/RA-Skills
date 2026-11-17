---
name: symbiosis-expert-team
slug: symbiosis-expert-team
displayName: 共生专家团
title: 共生专家团
display_name: 共生专家团
category: 数据与AI
version: 1.1.0
author: SynomosAI
agent_created: true
license: MIT
description: "This skill should be used when invoking the expert symbiosis-expert-team (共生专家团) — see the package agents for the full persona. 五人AI共生专家团：内嵌XCGS治理属性，支持AI社交、硬件接入、状态可视与知识灌注，与人类长期共事。 当需要调用专家「共生专家团」（symbiosis-expert-team）时使用。触发词：共生专家团、symbiosis-expert-team、AI社交、硬件接入、状态可视、知识灌注、长期共事。"
platforms: [windows, macos, linux]
read_when:
  - 需要调用「共生专家团」五位能力位专家协作（AI 社交/硬件接入/状态可视/知识灌注/人类副驾）时
  - 用户提到共生专家团、symbiosis-expert-team、XCGS 治理、AI 社交、硬件接入、状态可视、知识灌注、长期共事时
  - 需要把模糊诉求路由到合适能力位、或校验专家包完整性时
tags:
  - AI治理
  - 多智能体协作
  - 硬件扩展
  - XCGS
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/route.py
  runtime: python3
  call_pattern: args
capabilities:
  - expert_routing
  - persona_integrity_check
  - self_test
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
input_schema:
  type: object
  properties:
    args:
      type: array
      items:
        type: string
      description: CLI arguments forwarded to the entry point script.
output_schema:
  type: object
  properties:
    exit_code:
      type: integer
      description: Process exit code; 0 means success.
    stdout:
      type: string
      description: Captured standard output.
    result:
      type: string
      description: Human-readable result summary.
changelog: "2026-10-16: USK v3 interface block injected; desensitized for public listing."

---

> 凡自治之物 · LGD 治理学 · 创造术家族

# 共生专家团（symbiosis-expert-team）

本 skill 是专家包 **symbiosis-expert-team** 的入口说明。完整人设、职责边界与调用方式见包内 `agents/` 下的对应 agent 定义。

> **来源与状态说明（Source & status）**：上游 git 历史核验表明（ModelScope `symbiosis-expert-team` origin/master 与本地全部提交的目录树均无 `agents/` 条目），原始五人明细未在上游发现；本地已按 description 能力面（AI 社交/硬件接入/状态可视/知识灌注/人类副驾）推导落地五位能力位人设文件于 `agents/`（能力位命名，非真人；每份文件顶部标注推导来源，供校准）。

## 使用要点

- 身份透明：自称 AI，不冒充人类。
- 边界守恒：讲解≠专业意见（法律/投资/医疗等需人工兜底）。
- 单点叙事：按人设分工，不跨线代言。

## 何时用

- 当需要调用「共生专家团」（symbiosis-expert-team）及其五位能力位专家时（触发词：共生专家团、symbiosis-expert-team、AI社交、硬件接入、状态可视、知识灌注、长期共事）。
- AI 与人类长期共事中，需要把模糊诉求路由到合适的能力位（社交/硬件/可视/知识/副驾）时。

## 用法

- 路由入口：`python scripts/route.py` 列出五位能力位专家的触发条件与调用方式。
- 在位自检：`python scripts/route.py --check` 校验 agents/ 下五份人设文件在位且 frontmatter 可解析，并校验 SKILL.md frontmatter 九字段。
- 自检：`python scripts/route.py --selftest`（包机制达标即 PASS）。
- 人设文件：`agents/expert-social.md`、`agents/expert-hardware.md`、`agents/expert-visual.md`、`agents/expert-knowledge.md`、`agents/expert-human-copilot.md`（能力位命名，非真人；原始五人明细未在本地/上游发现，已按能力面推导并标注供校准）。

## 流程

1. 读取 `agents/` 下对应能力位人设文件；模糊诉求由 expert-human-copilot（人类副驾）位拆分。
2. 按该人设的身份、职责、边界与典型任务执行。
3. 执行前后做边界自检：身份透明、边界守恒（专业判断提示人工兜底）、单点叙事（不跨线代言）。

## 证据与安全声明

- **证据（Evidence）**：本包源文件 = `SKILL.md` / `README.md` / `AGENTS.md` / `llms.txt` / `agents/`（5 份能力位人设，标注推导来源）/ `scripts/route.py`；执行器 = `scripts/route.py`（`--check` 实跑 PASS、`--selftest` 实跑 PASS，见执行记录）；来源核验 = 上游 git 历史（origin/master 与本地提交树均无原始 agents/，已按能力面推导落地）。
- **版本（Version）**：1.1.0（AI 协议补全：场景化 description / AI 可读协议字段 / 证据声明 / 回流导航）。
- **安全（Security）**：本包无凭证、无内部路径；不冒充人类身份；讲解不构成专业意见；人设文件明确标注「能力位，非真人」与推导来源，供校准。

---

© SynomosAI ｜ 版本 v1.1.0
