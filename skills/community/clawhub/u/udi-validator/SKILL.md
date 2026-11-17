---
name: udi-validator
description: 'Validate and parse medical device UDI (Unique Device Identification) strings: GS1 element strings (AI parser + GTIN mod-10 check digit + date fields), HIBCC format detection, and ICCBBA (ISBT 128) detection. Helps regulatory affairs and quality teams quickly spot malformed UDI-DI / UDI-PI data before database submission.'
slug: udi-validator
title: UDI Validator
version: 1.0.1
license: MIT
author: SynomosAI
tags:
- medical-device
- udi
- gs1
- regulatory
- quality
category: knowledge-management
description_zh: "校验并解析医疗器械 UDI：GS1 元素字符串（AI 解析器 + GTIN mod-10 校验位 + 日期字段）、HIBCC 格式识别、ICCBBA（ISBT 128）识别；提交 NMPA/FDA GUDID/EUDAMED 前快速定位畸形 UDI-DI/UDI-PI。"
description_en: "Validate and parse medical device UDI strings: GS1 element strings (AI parser + GTIN mod-10 check digit + date fields), HIBCC format detection, ICCBBA (ISBT 128) detection; triage malformed UDI-DI/UDI-PI before NMPA/FDA GUDID/EUDAMED submission."
read_when:
  - 提交 NMPA UDI / FDA GUDID / EU EUDAMED 前校验 UDI-DI/UDI-PI 结构
  - 解析 GS1 元素字符串字段（GTIN/lot/expiry/serial/生产日）
  - 供应商标签条码发码机构分诊（GS1/HIBCC/ICCBBA）
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/udi_validate.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: CLI arguments per skill usage
    required: false
output_schema:
  stdout: structured result (JSON IR)
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
capabilities:
- medical-devices
- udi
- validator
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: '3.8'
changelog: '1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)'
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
- Reviewing UDI-DI / UDI-PI strings on labels, IFUs, or UDI database submissions (NMPA UDI, FDA GUDID, EU EUDAMED, Japan PS-HOT).
- Checking whether a GS1 element string is structurally valid before submission.
- Extracting structured fields (GTIN, lot, expiry, serial, manufacture date) from a raw UDI string.
- Triaging supplier label samples: which issuing agency (GS1 / HIBCC / ICCBBA) the barcode belongs to.

### Issuing-agency triage
| Agency | Typical prefix | Validation |
|---|---|---|
| GS1 | starts with `01` | full |
| HIBCC | starts with `+` | format detection only |
| ICCBBA (ISBT 128) | starts with `=` | detection only |

### Usage
```bash
python scripts/udi_validate.py "0104006381333931"
python scripts/udi_validate.py --file barcode_dump.txt
python scripts/udi_validate.py --checkdigit 0400638133393
```
Exit `0` = all valid; `1` = any problem. Per input it reports: detected agency, parsed AI fields, check-digit verdict, date-field verdicts.

### Flow
1. Detect the issuing agency (GS1 / HIBCC / ICCBBA).
2. Parse AI fields; verify check digit and dates.
3. Emit per-item verdicts; point at the first failing position.

### Known limits
- HIBCC check-char arithmetic and ICCBBA identity verification are not implemented; final validation must use official agency tools.
- Validates structure, not whether the UDI-DI actually exists in a regulatory database (online query required).
- Date day `00` (GS1 "day unknown") is accepted and flagged.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
- 提交 NMPA UDI / FDA GUDID / EU EUDAMED 前校验 UDI-DI/UDI-PI 字符串结构。
- 校验 GS1 元素字符串提交前是否结构合法。
- 从原始 UDI 字符串提取结构化字段（GTIN、批号、效期、序列号、生产日期）。
- 供应商标签条码分诊：判断条码属于哪个发码机构（GS1 / HIBCC / ICCBBA）。

### 发码机构分诊
| 发码机构 | 典型前缀 | 校验程度 |
|---|---|---|
| GS1 | 以 `01` 开头 | 完整校验 |
| HIBCC | 以 `+` 开头 | 仅格式识别 |
| ICCBBA (ISBT 128) | 以 `=` 开头 | 仅识别 |

### 用法
```bash
python scripts/udi_validate.py "0104006381333931"
python scripts/udi_validate.py --file barcode_dump.txt
python scripts/udi_validate.py --checkdigit 0400638133393
```
退出码 `0` = 全部合法；`1` = 有任意问题。每个输入报告：识别的发码机构、解析的 AI 字段、校验位结论、日期字段结论。

### 流程
1. 检测发码机构（GS1 / HIBCC / ICCBBA）。
2. 解析 AI 字段并校验校验位/日期。
3. 输出逐项结论，定位首个失败位置。

### 已知局限
- HIBCC 校验字符算法与 ICCBBA 身份核验**未**实现；最终校验须用官方机构工具/数据库。
- 本脚本校验**结构**，不校验 UDI-DI 是否真实存在于监管数据库（NMPA UDI / GUDID / EUDAMED）——需在线查询。
- 日期日值 `00`（GS1 "日期未知"）会被接受并标记。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
