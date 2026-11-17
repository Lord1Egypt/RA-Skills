---
name: udi-format-validator
title: "UDI Format Validator"
slug: udi-format-validator
display_name: UDI 格式校验器
display_name_en: UDI Format Validator
version: 1.0.1
agent_created: true
author: SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Bash
category: medtech-reg
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description: UDI 格式校验器 — 校验 DI 是否正确、生产标识是否齐全、Basic UDI-DI 如何区分（零依赖，确定性输出，rc=0/1/2，--json 机器可读）。
description_zh: "UDI 格式校验器：校验 DI 正确性、生产标识完整性、Basic UDI-DI 区分（零依赖，确定性 JSON IR，rc=0/1/2，--json）。"
description_en: "Validate UDI strings: DI correctness, production-identifier completeness and Basic UDI-DI distinction (zero-dependency, deterministic output, rc=0/1/2, --json)."
classification:
  skillhub: ["medtech-reg", "medical-device", "udi"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Functional suitability"]
read_when:
  - 拿到一串 UDI 需校验 DI 是否正确、生产标识是否齐全
  - 需区分 UDI-DI 与 Basic UDI-DI 结构
  - 注册资料提交前做格式/结构自检避免被打回
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [udi-format-validator, 医疗器械合规, UDI, medtech-reg]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/udi_format_validator.py
  runtime: python3
  call_pattern: args
output_schema:
  stdout: structured validation result (rc / error_code)
  exit_code: rc=0 pass / rc=1 issue / rc=2 usage error
changelog: "1.0.1: Bilingual rewrite (EN-first) + read_when/classification; attribution block neutralized; 1.0.0 initial"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# UDI Format Validator

## When to use
Given a UDI string, validate whether the DI is correct, whether production identifiers are complete, and how to distinguish Basic UDI-DI. Use before registration submission to avoid format rejections.

## How to use
```bash
python scripts/udi_format_validator.py "(01)06901234567892(17)260930(10)LOT2026A(21)SN0001"
python scripts/udi_format_validator.py --di 06901234567892
python scripts/udi_format_validator.py "(01)06901234567892" --json
```

## Workflow
Trigger → run the script per usage → check output/exit code → report results.

## Output (real run)
```
UDI 校验：通过
  DI 06901234567892  check digit ok (GS1 Mod10)
  expiry 2026-09-30  format ok
  batch LOT2026A     production id ok
```

## Exit / error codes
rc=0 pass / rc=1 issue found / rc=2 usage error. Error codes: UDI_E_LEN (DI not 14 digits), UDI_E_CHECKDIGIT (GS1 Mod10 mismatch), UDI_E_DATE (invalid date), UDI_E_UNKNOWN_AI (unsupported AI; only 01/10/11/17/21/240/30), UDI_E_AMBIGUOUS (unbracketed variable-length segment).

## FAQ
UDI-DI identifies a specific model/package; Basic UDI-DI is the registration-unit level identifier for a product family (EU MDR; NMPA has a corresponding approach). Passing the check digit is not the same as coding compliance — issuer prefix and agency qualification must be verified against the issuing agency and official database.

## Disclaimer
Deterministic format/structure judgment and rule-based advice; not legal advice or safety commitment. Human review against the latest official requirements.

## 中文

# UDI 格式校验器

## 何时用
拿到一串 UDI，校验 DI 是否正确、生产标识是否齐全、Basic UDI-DI 如何区分；注册资料提交前做格式自检避免被打回。

## 用法
```bash
python scripts/udi_format_validator.py "(01)06901234567892(17)260930(10)LOT2026A(21)SN0001"
python scripts/udi_format_validator.py --di 06901234567892
python scripts/udi_format_validator.py "(01)06901234567892" --json
```

## 流程
触发 → 按用法运行脚本 → 核对输出/退出码 → 呈现结果。

## 退出码与错误码
rc=0 通过 / rc=1 发现问题 / rc=2 用法错误。错误码：UDI_E_LEN（DI 非 14 位）、UDI_E_CHECKDIGIT（GS1 Mod10 不符）、UDI_E_DATE（日期非法）、UDI_E_UNKNOWN_AI（仅支持 01/10/11/17/21/240/30）、UDI_E_AMBIGUOUS（无括号变长段无法定界）。

## FAQ
UDI-DI 标识具体型号包装，Basic UDI-DI 是同族产品注册单元级标识（EU MDR，NMPA 亦有对应口径）。校验位通过不等于编码合规，发码机构资质与企业前缀仍需向发码机构与官方数据库核验。

## 免责
确定性格式/结构判定与规则化建议，不构成法规意见；关键决策人工复核并以官方最新要求为准。
