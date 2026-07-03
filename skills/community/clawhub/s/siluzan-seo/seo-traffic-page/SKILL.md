---
name: seo-traffic-page
description: >-
  批量生成工业 B2B SEO **引流页 JSON**（schemas/output.json）：N 个关键词 → N 个 pages[]（Content 模块 + TDK）。
  仅当用户要 landing page **结构化 schema / 批量引流页 JSON** 时使用；普通写稿或单篇无 schema 文章 → siluzan-cso。
  须配合 siluzan-cso RAG，再 Read 本子 SKILL 与 schemas/output.json。
---

# SEO 引流页 JSON Schema 生成

产出 **schemas/output.json** 定义的 `pages[]` JSON，供建站灌入——不是 CSO 通用写稿。

## 何时使用

- 用户要 **批量引流页 / landing page JSON / traffic page schema** 交付
- 必填：`keywords`（字符串数组），几个词生成几个页面
- **不要**用于：口播、公众号、无 output.json 的普通 Blog（→ siluzan-cso）
- 一次性 JSON 输出，页面间 **禁止** 复用句子、案例、FAQ、亮点表述

## 运行时配置

| 文件 | 用途 |
|------|------|
| [skill.yaml](skill.yaml) | WorkBuddy：模型、inputs、5 路 RAG |
| [prompts/system.md](prompts/system.md) | 生成规则与 7 模块结构 |
| [prompts/user.md](prompts/user.md) | 用户侧模板 |
| [schemas/output.json](schemas/output.json) | 输出 JSON Schema |

## RAG（siluzan-cso）

见 `skill.yaml`：`keywords_context`、`company_profile`、`trust_assets`、`faq_pool`、`reviews`（merge union，dedup）。

## 输出结构

```json
{
  "pages": [
    {
      "Title": "页面关键词",
      "Content": "7 模块纯文本：优势 / 案例×3 / 产品 / 文本 / FAQ×5 / 评价×2 / 亮点×3",
      "TDK": { "seo_title", "seo_description", "seo_keywords" },
      "SEO_Check": "密度与 TDK 长度自检"
    }
  ]
}
```

## 内容要点

- 每页对应明确 **search intent**（供应商、规格比较、应用、质检、批量采购等）
- 品牌信息融入质量/供应链/案例语境，避免硬广结尾
- 评价：优先 KB 真实评价；无数据可匿名场景化，**不得** 声称为 verified 或虚构客户/订单

## 执行清单

- [ ] 确认 `keywords` 数组
- [ ] Read `prompts/system.md` 全文
- [ ] RAG 检索或收集 KB 素材
- [ ] 逐页差异化生成
- [ ] 校验 `schemas/output.json` 与共用 TDK/密度规则（见根 [SKILL.md](../SKILL.md)）

## 导出

要 Word/PDF → `siluzan-seo export -f <json> -t docx|pdf`（见 [../references/export.md](../references/export.md)），勿自写 docx 脚本。
