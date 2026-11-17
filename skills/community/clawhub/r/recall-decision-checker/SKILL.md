---
name: recall-decision-checker
title: "Medical Device Recall-level Decision Checker"
slug: recall-decision-checker
display_name: 医疗器械召回级别判定器
display_name_en: Medical Device Recall-level Decision Checker
version: 1.0.1
category: medtech-reg
author: SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
description: 医疗器械召回级别判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖 TH-MED-003 域（医疗器械全链路）。
description_zh: "医疗器械召回级别判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖 TH-MED-003 域（医疗器械全链路）。"
description_en: "Medical device recall-level determination tool: zero-dependency decision support with JSON IR output (domain TH-MED-003, full device chain)."
tags: [医疗器械, 合规, 判定器, TH-MED-003, recall-decision-checker, medtech-reg, 召回]
classification:
  skillhub: ["medtech-reg", "medical-device", "recall"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Functional suitability"]
read_when:
  - 需依据 NMPA 规则对召回风险分级且判定须基于官方规则源
  - 全链路质量管理需结构化 JSON IR 结果对接 ERP/QMS
  - 复杂产品缺陷报告需不依赖本地脚本的合规自动判定
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
ai_protocol: true
spec: usk/1.0
interface:
  type: prompt
  entry_point: SKILL.md
  runtime: none
  call_pattern: prompt
output_schema:
  stdout: structured JSON IR
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
changelog: "1.0.1: Bilingual rewrite (EN-first) + read_when; risk_rationale ref neutralized; 1.0.0 initial"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# Medical Device Recall-level Decision Checker

## When to use
1. When recall risk must be graded under NMPA rules with logic based on official sources, not an external model.
2. In full-chain quality management, when structured JSON IR results must feed directly into ERP/QMS interfaces.
3. For complex defect reports requiring automated compliance determination without local scripts.

## How to use
Input parameters as JSON: product model, defect description, affected-population scope. No scripts; reference TH-MED-003 rules as the reasoning basis and request JSON IR output with recall level, regulatory clauses, and confidence score.

## Workflow
1. Receive submitted data and validate completeness against TH-MED-003.
2. Extract key product attributes and retrieve the recall-level grading matrix.
3. Logically compare against risk indicators and affected scope with weighting.
4. Generate standard JSON IR with the recommended recall level.
5. Attach regulatory references for manual review and traceability.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# 医疗器械召回级别判定器

## 何时用
1. 需依据 NMPA 规则对召回风险分级，且判定逻辑须基于官方规则源而非外部模型。
2. 全链路质量管理场景，需结构化 JSON IR 结果直接对接 ERP/QMS 接口。
3. 复杂产品缺陷报告，需不依赖本地脚本的合规自动判定查询。

## 用法
以 JSON 传入产品型号、缺陷描述、受影响群体范围；无脚本，对话中引用 TH-MED-003 规则作为推理依据，要求返回含召回等级、法规条款、置信度评分的 JSON IR。

## 流程
接收数据并校验完整性 → 提取产品属性并检索召回级别判定矩阵 → 按风险指标与受影响范围做权重比对 → 生成含推荐召回级别的 JSON IR → 附加法规依据索引供人工复核与追溯。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立安全扫描（TBD）。
