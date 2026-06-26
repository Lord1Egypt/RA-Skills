---
name: med-doctor-literature-retrieval
description: 医生端临床科研 — 医学文献问答与检索延展，在用户提供的题录/摘要片段上做 PICO 对齐与证据叙事。
metadata:
  {
    "openclaw":
      {
        "emoji": "📑"
      }
  }
---

# 医学文献检索（问答 / 延展）

## 概述

将「临床问题」与可选的**本地已抓取题录或摘要片段**一并交给内部医疗大模型，生成 **PICO 对齐的问题重构、证据脉络梳理、检索式延展建议与知识空白提示**。适用于开题、综述大纲、或向上级汇报前的文献叙事草稿。

> 本 skill **不直连 PubMed / CNKI 等外部索引**；`passages` 由上游爬虫、图书馆 API 或手工粘贴提供。与药企侧 `literature-analysis` 相比，本包更强调**临床问题导向**与「下一步可查什么」的延展，而非研发管线证据表。

## 业界脉络（写法参考，非功能承诺）

系统综述与快速证据合成中广泛采用 **PICO（Population, Intervention, Comparator, Outcome）** 框架约束检索问题；实践型产品常在「关键词布尔检索」之上叠加 **语义段落排序** 与 **引用级摘要**。本 skill 在 prompt 层显式引导 PICO 与「可检索引言」，便于后续接入真实检索 API 时把同一 JSON 映射为查询 DSL。

## 快速开始

```bash
python3 scripts/run.py --input input.json --output output.json --appkey YOUR_KEY
```

## 输入字段（JSON）

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `clinical_question` | 是 | 临床或科研问题（一句话或多句） |
| `passages` | 否 | 文献片段数组：`title`、`year`、`excerpt`（可无 PMID/DOI） |
| `constraints` | 否 | 如人群、语种、研究设计偏好等 |

## 输出约定

```json
{
  "skill": "医学文献检索",
  "status": "ok",
  "data": { },
  "text": "Markdown：PICO、要点、延展检索建议等"
}
```

## 参数

- `--input PATH`：**必填**。
- `--output PATH`：可选。
- `--appkey STRING`：**必填**。内部医疗大模型鉴权 key。

## 模型配置

- `https://maas-api.hivoice.cn/v1/chat/completions` · `u1-insuremed`

## 边界

非实时文献库；**不替代**系统评价与人工全文阅读。若 `passages` 为空，模型仅基于通用医学知识给出检索策略级建议，须在呈现中区分「未锚定具体文献」。
