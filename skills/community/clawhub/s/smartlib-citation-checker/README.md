# SmartLib Citation Checker v2.0

> **中文** · [English below](#english)

基于 SmartLib 文献检索 API 的智能引用核查与纠错技能。**核心价值：验证 AI 生成的参考文献是否真实存在，防止 AI 幻觉。**

---

## 简介

对用户提交的论文稿件或 AI 生成的参考文献进行**真实性核查**与**格式纠错**。支持 **GB/T 7714、APA、MLA、Chicago、BibTeX** 五种格式，修正后输出格式始终与原始输入保持一致。

---

## 变现模式

本技能与 [smartlib-literature-search](../smartlib-literature-search) **共享凭证与配额**。首次使用自动注册，免费 100 次/月。

| 状态 | 展示规则 |
|------|---------|
| 配额充足 | 完整核查报告（含差异标记、验证链接、统计分析） |
| 配额耗尽 | 仅展示前 **2 条文献**的完整核查结果，其余遮罩引导付费 |

---

## 适用场景

| 场景 | 说明 |
|------|------|
| **AI 幻觉验真** | 核查豆包/ChatGPT/Kimi 等 AI 生成的参考文献是否真实存在 |
| **论文初稿审查** | 投稿前自查参考文献的作者、年份、期刊名等是否准确 |
| **粘贴式批量核查** | 直接粘贴参考文献列表，快速验证并导出修正版 |

---

## 功能特性

- **多格式解析**：自动识别 GB/T 7714、APA 7、MLA 9、Chicago、BibTeX
- **真实性核查**：联网核查每条文献，标记 ✅ / ❌ / ⚠️
- **信息比对**：原始引用 vs 数据库记录逐字段比对
- **差异标记**：`[删除]` / `[新增]` 直观标记错误与修正
- **统计分析**：引用 ≥3 时自动输出年份分布、期刊集中度、作者分析图表
- **验证链接**：每条匹配文献附带可点击的 SmartLib 验证链接

---

## 使用方式

```
核查这篇论文的参考文献
帮我验证一下 ChatGPT 给的这些参考文献是否真实：
[1] Li, J., & Wang, X. (2023). Deep learning for medical imaging...
```

**触发关键词**：核查参考文献、检查引用、引用验真、citation check、verify references

---

## 输出

生成完整的 HTML 核查报告，包含核查结果表格、修正后参考文献纯文本、统计分析。

> 📄 [样例一：论文稿件核查](./examples/citation_check_paper_draft_sample.html)
> 📄 [样例二：AI 幻觉检测](./examples/citation_check_ai_hallucination_sample.html)

---

## 依赖

- **smartlib-literature-search**（提供 SmartLib API 接入 + 配额管理）
- SmartLib API 凭证（首次使用自动注册，无需手动申请）

---

## 许可

MIT License — 代码开源，商用 API 需授权。

---

## 作者

**张亚东** — 重庆维普智图 · GitHub: [J-levee](https://github.com/J-levee)

---

<a name="english"></a>

# SmartLib Citation Checker v2.0 — English

> Smart citation verification skill. Detects AI hallucinations in references.

---

## Overview

Verifies whether academic references in paper drafts or AI-generated citation lists actually exist. Supports **GB/T 7714, APA, MLA, Chicago, BibTeX**.

---

## Monetization

Shares credentials and quota with [smartlib-literature-search](../smartlib-literature-search). Auto-registration with 100 free checks/month.

| Status | Display Rule |
|--------|-------------|
| Quota available | Full report (diff markers, verification links, analytics) |
| Quota exhausted | Only first **2 references** shown in full; rest masked behind paywall |

---

## Features

- Multi-format parsing & correction
- Live verification via SmartLib API (✅ / ❌ / ⚠️)
- Field-by-field diff with inline markers
- Citation analytics (year, journal, author distribution)
- Clickable SmartLib verification links

---

## Usage

```
Verify the references in this paper
Check if these AI-generated citations are real: ...
```

---

## Dependencies

- **smartlib-literature-search** (provides SmartLib API + quota management)

---

## License

MIT — Code open source; commercial API use requires authorization.

---

## Author

**Yadong Zhang** — VIP Smart · GitHub: [J-levee](https://github.com/J-levee)
