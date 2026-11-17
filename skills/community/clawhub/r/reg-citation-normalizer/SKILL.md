---
name: reg-citation-normalizer
title: "Reg Citation Normalizer"
description: 医疗器械法规引用编号的识别、解析与规范化。将 21 CFR、ISO/IEC、中国国标行标（GB/YY/T）、NMPA 部令公告等各种写法解析为规范结构并给出标准书写建议。零依赖，可离线运行。
description_zh: "医疗器械法规引用编号的识别、解析与规范化：把 21 CFR、ISO/IEC、GB/YY/T、NMPA 部令公告等写法解析为规范结构并给标准书写建议。零依赖离线运行。"
description_en: "Recognize, parse and normalize medical-device regulatory citations (21 CFR, ISO/IEC, Chinese GB/YY-T, NMPA decrees) into a canonical structure with recommended standard formatting. Zero-dependency, offline."
license: MIT
metadata:
  author: SynomosAI
  category: other
  tags: [medical-device, regulatory, citation, FDA, NMPA, ISO]
permalink: internal/vault (neutralized)
version: 1.0.1
category: knowledge-management
classification:
  skillhub: ["medical-device", "regulatory", "productivity"]
  iso_25010: ["Maintainability", "Usability"]
read_when:
  - 注册文档审校 / IFU / 技术文件编写中需要规范化法规引用写法
  - 法规翻译中英对照，需保证条款号对齐
  - 批量检查文档中 21 CFR / ISO / GB·YY/T / NMPA 引用书写错误
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/cite_normalize.py
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
- citation
- regulatory
- normalizer
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: '3.8'
changelog: '1.0.1: Bilingual rewrite (EN-first) + read_when/classification added; 1.0.0 initial upload (USK v3 injected round2)'
---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# Reg Citation Normalizer

Recognize and normalize medical-device regulatory citation numbers — turn inconsistent citation styles in your documents into a canonical structure with recommended standard formatting.

## When to use
- Reviewing registration dossiers, writing IFU/technical files, or checking regulatory-translation consistency (normalizing 21 CFR / ISO·IEC / GB·YY-T / NMPA decree citations).
- Triggers: citation normalize, 21 CFR, ISO 13485, YY/T, NMPA.

## How to use
```bash
python scripts/cite_normalize.py normalize "21 CFR 820.30(a)(6)"
python scripts/cite_normalize.py parse "ISO 13485:2016 clause 7.5.1" --json
python scripts/cite_normalize.py check report.md [--json]
```

## Workflow
1. Run `check` on a document to find formatting issues;
2. Use `normalize`/`parse` to get canonical forms;
3. Batch-fix and re-review.

## Supported citation types

| Type | Example input | Canonical output |
|------|---------|-----------|
| US 21 CFR | `21 CFR 820.30 (a)(6)` | `21 CFR 820.30(a)(6)` |
| ISO/IEC | `ISO 13485:2016 clause 7.5.1` | `ISO 13485:2016, 7.5.1` |
| Chinese line standard | `YY/T 0287-2017 7.5.1` | `YY/T 0287-2017, clause 7.5.1` |
| Decree | `国家市场监督管理总局令第47号` | agency normalized (incl. SFDA→CFDA→NMPA history) |
| Announcement | `国家药监局公告 2021年第76号` | normalized announcement |

## Errata (check mode)
- Missing space between code and number (`ISO13485` → `ISO 13485`); lowercase code; misplaced `§`; year separator (`:` vs dash); undated ISO references → prompt to add year.

## Boundary
- Format recognition and normalization only; does NOT validate clause content currency (use openstd.samr.gov.cn / ecfr.gov / iso.org).
- Rules per ISO/IEC Directives Part 2 §10.4–10.5, GB/T 1.1-2020, GPO/eCFR, NMPA official style.

## Requirements
Python 3.8+, zero third-party deps.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# reg-citation-normalizer

医疗器械法规引用编号识别与规范化工具。把文档里五花八门的法规引用写法，解析成规范结构并给出标准书写建议。

## 何时用
- 注册文档审校、IFU/技术文件编写、法规翻译一致性检查时。
- 触发词：法规引用、21 CFR、ISO 13485、YY/T、NMPA。

## 用法
```bash
python scripts/cite_normalize.py normalize "21 CFR 820.30(a)(6)"
python scripts/cite_normalize.py parse "ISO 13485:2016 clause 7.5.1" --json
python scripts/cite_normalize.py check report.md [--json]
```

## 流程
1. 对文档跑 check 发现书写问题；
2. 用 normalize/parse 得到规范写法；
3. 批量回改并复核。

## 覆盖的引用类型

| 类型 | 示例输入 | 规范化输出 |
|------|---------|-----------|
| 美国 21 CFR | `21 CFR 820.30 (a)(6)` | `21 CFR 820.30(a)(6)` |
| ISO/IEC | `ISO 13485:2016 clause 7.5.1` | `ISO 13485:2016, 7.5.1` |
| 中国行标 | `YY/T 0287-2017 7.5.1` | `YY/T 0287-2017，第7.5.1条` |
| 部令 | `国家市场监督管理总局令第47号` | 机构归一化（含 SFDA→CFDA→NMPA 沿革） |
| 公告 | `国家药监局公告 2021年第76号` | 规范公告写法 |

## 勘误能力（check 模式）
缺空格、大小写、§ 误用、年份连接符、ISO 未注日期等 9 类常见书写问题。

## 边界声明
只做格式识别与规范化，不校验条款内容正确性与现行有效性（查现行状态用 openstd.samr.gov.cn / ecfr.gov / iso.org）。

## 环境要求
Python 3.8+，零第三方依赖。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立扫描（TBD）。
