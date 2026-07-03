---
name: seo-backlink-article
description: >-
  生成单篇工业 B2B **外链 SEO 结构化 JSON**（schemas/output.json）：article_content、TDK、
  backlink_notes 等——不是第三方平台运营文案或普通 guest post 成稿。
  仅当用户要 guest post **JSON schema / output.json 交付** 时使用；无 schema 的外链写稿 → siluzan-cso。
  须先 siluzan-cso RAG，再 Read 本子 SKILL 与 schemas/output.json。
---

# SEO 外链 JSON Schema（非普通写稿）

产出 **schemas/output.json** 定义的外链 SEO 包（含 backlink_notes 等）——不是 CSO 平台发布文案。

## 何时使用

- 用户明确要 **guest post JSON / 外链 schema / output.json** 交付
- 必填：`title`、`keyword`
- **不要**用于：只说「写外链稿 / 投稿文」且未要 JSON schema（→ siluzan-cso）
- 单篇输出；口吻接近第三方行业内容，非厂家宣传稿

## 运行时配置

| 文件 | 用途 |
|------|------|
| [skill.yaml](skill.yaml) | WorkBuddy：模型、inputs、4 路 RAG |
| [prompts/system.md](prompts/system.md) | 结构、密度、外链语境规则 |
| [prompts/user.md](prompts/user.md) | 用户侧模板 |
| [schemas/output.json](schemas/output.json) | 输出 JSON Schema |

## RAG（siluzan-cso）

见 `skill.yaml`：`keyword_product_context`、`company_profile`、`product_detail`、`trust_assets`。

## 输出结构

```json
{
  "article_content": "英文正文，仅三级小标题，篇幅尽量长，纯文本",
  "meta_title": "45-55 英文字符",
  "seo_keywords": ["3-5 个"],
  "seo_description": "145-155 英文字符",
  "image_alt_suggestions": ["3-5 个"],
  "keyword_density_check": {},
  "chinese_summary": "150-300 字",
  "backlink_notes": "平台类型、锚文本、硬广风险控制（中文）"
}
```

## 内容要点

- 开头点明对采购决策的价值；中段技术/标准/合规/供应链判断
- 企业名仅作可信度补充；禁止 best/number one 等无依据绝对化表述
- 结尾以采购建议或供应商评估收束，非产品目录页

## 执行清单

- [ ] 确认 title、keyword
- [ ] Read `prompts/system.md` 全文
- [ ] RAG 检索或 KB 摘要
- [ ] 生成 `backlink_notes`（平台、锚文本、硬广风险）
- [ ] 校验 `schemas/output.json` 与根 [SKILL.md](../SKILL.md) 共用规则

## 导出

要 Word/PDF → `siluzan-seo export -f <output.json> -t docx|pdf`（见 [../references/export.md](../references/export.md)），勿自写 docx 脚本。
