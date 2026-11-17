---
name: udi-db-submission-check
title: "UDI Database Submission Compliance Checker"
slug: udi-db-submission-check
display_name: UDI 数据库提交合规判定器
display_name_en: UDI Database Submission Compliance Checker
version: 1.0.1
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
author: SynomosAI (LGD initiative)
copyright: SynomosAI
category: medtech-reg
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
description: UDI 数据库提交合规判定器——UDI 格式对了，但该传哪个库、什么时候传、必填哪些字段，漏传或漏维护上市即违规（零依赖规则判定，JSON IR，rc=0/1/2）。
description_zh: "UDI 数据库提交合规判定器：UDI 码格式对了，但该传哪个库、何时传、必填哪些字段需判定；漏传/漏维护上市即违规（零依赖规则判定，JSON IR，rc=0/1/2）。"
description_en: "UDI database submission compliance checker: given the UDI string, which database, when, and which fields are mandatory; missing or lapsed submission is non-compliant at market launch (zero-dependency rule determination, JSON IR, rc=0/1/2)."
classification:
  skillhub: ["medtech-reg", "medical-device", "udi"]
  clawhub: ["productivity", "data-analytics", "development"]
  iso_25010: ["Functional suitability"]
read_when:
  - 需判定 UDI 数据该提交到哪个库（NMPA/GUDID/EUDAMED）
  - 不清楚提交时机与必填字段清单
  - 需确认漏传/漏维护是否构成上市违规
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [udi-db-submission-check, 医疗器械合规, UDI, medtech-reg]
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
changelog: "1.0.1: Bilingual rewrite (EN-first) + read_when/classification; all branding/copyright refs neutralized; 1.0.0 initial"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# UDI Database Submission Compliance Checker

## When to use
The UDI string format is correct, but which database, when, and which fields are mandatory are unclear; a missing or lapsed submission is non-compliant at launch.

## What it is
A zero-dependency, deterministic rule determination: pass known conditions as parameters; it returns a structured determination + obligation list + risk warnings as JSON IR. Rules sourced from NMPA UDI rules, FDA 21 CFR 830 / GUDID, and EU MDR Art 27-29 / EUDAMED.

## Determination core
- Rules: NMPA UDI system rules / FDA 21 CFR 830 + GUDID / EU MDR Art 27-29 + EUDAMED.
- Output: JSON IR (`result` + `rc` + `error_code`).
- Error codes: E_INPUT_MISSING / E_ENUM_INVALID / E_RUNTIME.
- rc: 0 determination complete; 1 complete with warnings; 2 input insufficient/invalid.

## Boundary
Rule determination only, not legal advice or certification; conclusions need human review against the regulator. Under-input triggers strict warnings (rc=1), not silent "submittable". Does not cover special cases (innovative, drug-device combos, boundary products, nanomaterials). Clause numbers are given; verify against the latest official text.

## Disclaimer
AI-assisted decision support, not a registration/compliance/legal opinion. Human review; defer to the latest official documents. Text verification date 2026-09-26.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# UDI 数据库提交合规判定器

## 何时用
UDI 码格式对了，但该传哪个库、什么时候传、必填哪些字段没人一次说清；漏传或漏维护，上市即违规。

## 这是什么
零依赖、确定性规则判定：传入已知条件，按公开规则源给出结构化判定+义务清单+风险提示，输出 JSON IR。规则源：NMPA UDI 规则 / FDA 21 CFR 830+GUDID / EU MDR Art 27-29+EUDAMED。

## 判定核心
- 输出 JSON IR（result+rc+error_code）；错误码 E_INPUT_MISSING/E_ENUM_INVALID/E_RUNTIME。
- rc=0 判定完成；rc=1 完成带风险提示；rc=2 输入不足或非法。

## 能力边界
只做规则判定，不出法律意见或证明；输入不足从严提示(rc=1)；不覆盖创新器械/药械组合/边界产品/纳米材料；条款号已给出，以官方最新文本核对。

## 免责
AI 辅助决策支持，不构成注册/合规/法律意见；人工复核并以官方最新文件为准。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立安全扫描（TBD）。
