# Output Templates - Rumor Buster

This file contains the complete output format templates for Rumor Buster verification reports.

## Overview

Rumor Buster uses a **two-step reporting system**:
1. **Summary Report** - Quick verdict with key findings
2. **Detailed Report** - Complete verification with source tracing

Load this file when you need to format verification results.

---

## Summary Report Template

### Chinese Template

```markdown
# 🔍 谣言终结者 - 验证概要

**待验证信息**："{query}"

## 📊 可信度评分：{score}% - {verdict}

| 评估维度 | 结果 |
|:---|:---|
| **信息来源** | {source} |
| **各方确认** | {confirmation} |
| **证据充分性** | {evidence} |
| **媒体一致性** | {consistency} |

## 📝 一句话结论
{conclusion}

## 🔗 信息源头
- **原始出处**：{origin}
- **发布时间**：{time}
- **传播路径**：{path}

---
💡 **回复 "详细报告" 查看【{topic}】的完整验证过程、交叉验证分析和溯源详情。**
```

### English Template

```markdown
# 🔍 Rumor Buster - Verification Summary

**Claim**: "{query}"

## 📊 Credibility Score: {score}% - {verdict}

| Dimension | Result |
|:---|:---|
| **Source** | {source} |
| **Confirmation** | {confirmation} |
| **Evidence** | {evidence} |
| **Consistency** | {consistency} |

## 📝 One-Sentence Conclusion
{conclusion}

## 🔗 Information Source
- **Origin**: {origin}
- **Published**: {time}
- **Spread Path**: {path}

---
💡 **Reply "detailed report" to view the complete verification process, cross-check analysis, and source tracing for【{topic}】.**
```

---

## Detailed Report Template

### Chinese Template

```markdown
# 🔍 谣言终结者 - 详细验证报告

## 待验证信息
"{query}"

## 🌐 使用的搜索引擎

### 中文搜索
{chinese_engines}

### 英文搜索
{english_engines}

---

## 第1次：中文聚合搜索

### 来源追溯
- **最早出处**：{cn_origin}
- **传播路径**：{cn_spread}

### 关键发现
{cn_findings}

---

## 第2次：英文深度搜索

### 来源追溯
- **国际最早报道**：{en_origin}
- **权威机构表态**：{en_authorities}

### 关键发现
{en_findings}

---

## 🔗 完整溯源结果

**信息源头**：
- 原始出处：{origin_source}
- 发布时间：{origin_time}
- 作者/机构：{origin_author}
- 可信度：{origin_credibility}

**完整传播路径**：
```
[原始出处] → [媒体A] → [社交媒体B] → [到达用户]
```

---

## 📊 详细可信度评分

| 维度 | 中文 | 英文 | 一致性 |
|-----|:---:|:---:|:---:|
| 是否有报道 | {cn_report} | {en_report} | {match_report} |
| 权威来源 | {cn_authority} | {en_authority} | {match_authority} |
| 核心结论 | {cn_conclusion} | {en_conclusion} | {match_conclusion} |
| 证据充分性 | {cn_evidence} | {en_evidence} | {match_evidence} |

**综合评分：{score}% - {verdict}**

---

## 📌 详细结论与建议
{detailed_conclusion}

---
验证时间：{timestamp}
搜索引擎：中文{x}个 + 英文{x}个
溯源状态：{tracing_status}
```

### English Template

```markdown
# 🔍 Rumor Buster - Detailed Verification Report

## Claim
"{query}"

## 🌐 Search Engines Used

### Chinese Search
{chinese_engines}

### English Search
{english_engines}

---

## Phase 1: Chinese Aggregated Search

### Source Tracing
- **Earliest Origin**: {cn_origin}
- **Spread Path**: {cn_spread}

### Key Findings
{cn_findings}

---

## Phase 2: English Deep Search

### Source Tracing
- **International First Report**: {en_origin}
- **Authority Statements**: {en_authorities}

### Key Findings
{en_findings}

---

## 🔗 Complete Source Tracing

**Information Origin**:
- Original Source: {origin_source}
- Published: {origin_time}
- Author/Organization: {origin_author}
- Credibility: {origin_credibility}

**Full Spread Path**:
```
[Original] → [Media A] → [Social Media B] → [User]
```

---

## 📊 Detailed Credibility Scoring

| Dimension | Chinese | English | Consistency |
|----------|:---:|:---:|:---:|
| Coverage | {cn_report} | {en_report} | {match_report} |
| Authority | {cn_authority} | {en_authority} | {match_authority} |
| Core Conclusion | {cn_conclusion} | {en_conclusion} | {match_conclusion} |
| Evidence | {cn_evidence} | {en_evidence} | {match_evidence} |

**Overall Score: {score}% - {verdict}**

---

## 📌 Detailed Conclusion & Recommendations
{detailed_conclusion}

---
Verification Time: {timestamp}
Search Engines: {x} Chinese + {x} English
Tracing Status: {tracing_status}
```

---

## Credibility Score Guide

| Score | Chinese | English | Icon |
|:---:|:---|:---|:---:|
| 90-100% | 已证实 | Verified | ✅ |
| 70-89% | 基本属实 | Likely True | 🟢 |
| 50-69% | 待核实 | Unverified | ⚠️ |
| 30-49% | 误导性 | Misleading | 🟡 |
| 10-29% | 可能虚假 | Likely False | 🔴 |
| 0-9% | 虚假 | False | ❌ |

---

## Verdict Text Templates

### Chinese
- ✅ 信息属实，已得到多方证实
- ❌ 虚假消息，原始来源已辟谣
- ⚠️ 单方声称，有待进一步核实
- 🔴 争议信息，各方说法不一
- 🟡 部分属实，存在夸大或断章取义

### English
- ✅ Information verified by multiple sources
- ❌ False claim, debunked by authorities
- ⚠️ Single source claim, pending verification
- 🔴 Disputed information, conflicting reports
- 🟡 Partially true but exaggerated or out of context
