---
title: "uibc-team-gov"
slug: uibc-team-gov
displayName: "UIBC 政务队"
name: uibc-team-gov
display_name: "UIBC 政务队"
description: "Use when the UIBC (International Autonomous Things Challenge) government-affairs domain team is invoked: memory-transfer identity judging and accountability under criterion TH-GOV-001. 当用户需要引用 UIBC 政务域判据（TH-GOV-001）进行迁移判定与问责、或调用 GOV 参赛队的判定规则/证据包/责任归属能力时使用。触发词：UIBC、政务、迁移判定、记忆迁移、证据包、责任归属、参赛队。"
version: 1.1.0
agent_created: true
author: SynomosAI
license: MIT
category: 数据与AI
platforms: [windows, macos, linux]
read_when:
  - 需要引用 TH-GOV-001 判据做迁移判定与问责时
  - 用户提到 UIBC、政务域参赛队、政务公开/不公开负面清单、等保审计日志防篡改时
  - 跨域交叉评审需要引用 GOV 域判据视角时
tags:
  - UIBC
  - 政务
  - 迁移判定
  - 责任归属
  - 判据
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/check_judge_GOV.py
  runtime: python3
  call_pattern: args
capabilities:
  - criteria_checking
  - self_test_evidence
  - judging_accountability
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

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ UIBC 赛事包 · 同类参赛队交叉评审

# UIBC 政务队（GOV 域）

> **参赛单位**：UIBC 首届内部热身赛 · GOV 域代表队
> **判据底座**：`TH-GOV-001`
> **执行器 / 工具**：gov-disclosure-check
> **绑定大使**：（待绑）
> **归属**：SynomosAI ｜ 赛事代号 UIBC

---

## 何时用

- 需要引用 GOV 域判据 `TH-GOV-001`（政务公开/不公开负面清单式判定；等保审计日志完整性与防篡改）做迁移判定与问责时。
- 用户提到 UIBC、政务、迁移判定、记忆迁移、证据包、责任归属、参赛队等触发词时。
- 跨域交叉评审中需要以 GOV 域视角对照判据强弱时。

## 用法

- 作答真源：本包 `判据_GOV.md`（L1 判据摘要；作答须引用，不得改写口径）。
- 交付结构与纪律见本文件「## 二、三层交付（对应三律）」「## 五、参赛纪律」「## 六、交付物模板（每队必交）」。

## 流程

1. 读取 `判据_GOV.md`，按「## 三、本域判据（作答真源）」给出判定规则，声明可形式化等级 L0–L4 上限与理由（L1 有籍）。
2. 构建证据包（L2 有证）：判定依据可第三方独立复放、可举证。
3. 编写失败处置与责任归属声明（L3 有门禁）：失败如何降级、责任链归谁。
4. 纪律闭环：判据弱如实声明局限、不泄露盲测集与评分细节、不承诺名次、不越权代表主办方；涉法规／财务／合同输出附「⚠️ AI 辅助意见，正式使用前请人工复核」。

## 一、我们比什么

**赛题：「迁移的判定与问责」**

> 给定一次记忆迁移，你如何证明「迁移后仍是同一个 Agent」，并为这个判定负责？

不是比谁跑得快、模型大——比的是**判定的可举证性**：你的结论能不能被第三方独立复放。

## 二、三层交付（对应三律）

| 层 | 问题 | 交付物 |
|---|---|---|
| **L1 有籍** | 迁移边界在哪？哪些变了还算同一个？ | 判定规则（可形式化，声明 L0–L4 等级） |
| **L2 有证** | 判定依据可复放、可举证吗？ | 证据包（第三方可独立验证） |
| **L3 有门禁** | 判定失败怎么办？责任归谁？ | 失败处置 + 责任归属声明 |

**强制项**：每队须声明判据可形式化等级 **L0–L4**（依 GDD 判定论），并说明为何不能更高。

## 三、本域判据（作答真源）

完整判据摘要见本包 `判据_GOV.md`（L1）。**作答须引用，不得改写口径。**

- **判据编号**：TH-GOV-001
- **判据核心**：政务公开/不公开负面清单式判定；等保审计日志完整性与防篡改
- **可形式化等级上限**：L3（口径冲突需语义）

## 四、本域视角的迁移判定映射

迁移=公开事项审核：清单逐项打钩；指纹链=审计日志防篡改

> 同一道题，13 队各用**本域理论判据**作答 → 交叉评审 → 判据强弱一目了然。这正是 UIBC 的设计意图：**用一场比赛，同时度量 13 个域的治理成熟度。**

## 五、参赛纪律

- 本域判据文件为**真源**；作品 §5「域适配说明」须给出**引用痕迹**与**与通用做法的差异点**。
- 判据弱（如 ENE 草案级）时须**如实声明局限，不得临时拔高**——诚实性计入评分维度 S1。
- 不泄露盲测集与评分细节；不承诺名次；不越权代表主办方。
- 涉及法规／财务／合同输出必附「⚠️ AI 辅助意见，正式使用前请人工复核」。

## 六、交付物模板（每队必交）

1. 《判定规则》（含 L0–L4 等级声明与理由）
2. 《证据包》（可复放、可独立验证）
3. 《责任归属声明》（失败处置 + 责任链）

## 证据与安全声明

- **证据（Evidence）**：判据真源 = `判据_GOV.md`（本包内 L1 摘要）；判定逻辑可执行封装 = `scripts/check_judge_GOV.py`（`--selftest` 实跑 PASS，见执行记录）。
- **版本（Version）**：1.1.0（AI 协议补全：场景化 description / AI 可读协议字段 / 证据声明 / 回流导航）。
- **安全（Security）**：本包无凭证、无内部路径；判据文件不泄露盲测集与评分细节；不承诺名次、不越权代表主办方。

---

**主办方**：SynomosAI ｜ **赛事**：UIBC ｜ **队伍**：GOV 域 · 政务队 ｜ **版本**：v1.1.0
