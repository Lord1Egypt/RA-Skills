---
name: seo-blog-article
description: >-
  生成单篇工业 B2B **Blog SEO 结构化 JSON**（schemas/output.json）：article_en、TDK、comparison_tables、
  seo_audit、publishing_recommendation 等上线字段——不是普通 Blog 成稿。
  仅当用户要官网 Blog **schema 包 / output.json 交付** 时使用；无 schema 的写 Blog → siluzan-cso。
  须先 siluzan-cso RAG，再 Read 本子 SKILL 与 schemas/output.json。
---

# SEO Blog 结构化 JSON（非普通写稿）

产出 **schemas/output.json** 定义的 Blog SEO 包（含 seo_audit、内链、对比表字段等），供 CMS/上线——不是 CSO 三库口播/公众号流程。

## 何时使用

- 用户明确要 **Blog SEO JSON / output.json / 上线 schema 包**（含 seo_audit、publishing_recommendation 等）
- 必填：`title`、`keyword`
- **不要**用于：只说「写一篇 Blog」且未要 JSON schema（→ siluzan-cso）
- 可选：`target_market`、`brand_name`、`product_page_urls`、`existing_page_context`、`buyer_problem`、`target_long_tail_keywords`、`case_study_context`（见 `skill.yaml`）

## 运行时配置

| 文件 | 用途 |
|------|------|
| [skill.yaml](skill.yaml) | WorkBuddy：模型、inputs、4 路 RAG |
| [prompts/system.md](prompts/system.md) | E-E-A-T、HCU、结构、密度规则 |
| [prompts/user.md](prompts/user.md) | 用户侧模板 |
| [schemas/output.json](schemas/output.json) | 完整输出字段定义 |

## RAG（siluzan-cso）

见 `skill.yaml`：`keyword_product_context`、`company_profile`、`product_detail`、`trust_assets`。

## 输出结构（摘要）

| 字段 | 说明 |
|------|------|
| `article_en` | 英文正文，仅二级小标题，5-7 段，1000-1500 词，末尾 3 个 Q&A，纯文本 |
| `h1` / `meta_title` / `seo_description` / `seo_keywords` | 上线 TDK |
| `comparison_tables` | 材料/牌号/标准等结构化对比（勿写入正文 Markdown） |
| `internal_links` / `image_alt_suggestions` / `featured_snippet_opportunities` | 运营增强 |
| `seo_audit` / `publishing_recommendation` / `publishing_checklist` | 中文审计与发布建议 |
| `keyword_density_check` | 密度与布局自检 |
| `chinese_summary` / `article_zh` | 中文总结与全文翻译 |

## 内容要点

- 行业指南口吻，非宣传册；禁止复用 About/Why Choose Us 叙事
- 至少一个 Case Study / Application 小节；无真实数据则匿名场景
- CTA 温和（spec review、material guidance 等），禁止强销售口吻
- `duplicate_content_risk` 须在 `seo_audit` 中评估

## 执行清单

- [ ] 收集 title、keyword 及可选上下文
- [ ] Read `prompts/system.md` 全文
- [ ] RAG 检索或 KB 摘要
- [ ] 生成并分离表格/内链到 schema 字段
- [ ] 校验 `schemas/output.json` 与根 Skill 共用 TDK/密度规则

## 导出

要 Word/PDF → `siluzan-seo export -f <output.json> -t docx|pdf`（见 [../references/export.md](../references/export.md)），勿自写 docx 脚本。
