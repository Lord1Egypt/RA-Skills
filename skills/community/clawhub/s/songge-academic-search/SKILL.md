---
name: songge-academic-search
description: 学术论文检索小助手（松哥版）。支持多源检索（OpenAlex/Semantic Scholar/Crossref/arXiv/PubMed），自动补全论文元数据，输出 BibTeX/RIS/JSON/Markdown 引用格式。当用户搜索学术论文、查找文献、生成参考文献列表时触发。
license: MIT
---

# 学术论文检索小助手

专业学术论文多源检索工具，支持 OpenAlex、Semantic Scholar、Crossref、arXiv、PubMed 五大数据源，自动 enrichment 补全元数据。

**作者：松哥（Zhang JinSong）**

---

## 核心功能

- 🌐 **五库并行检索**（OpenAlex / Semantic Scholar / Crossref / arXiv / PubMed）
- 🔗 **Multi 模式自动串联**：OpenAlex 搜 → S2 补摘要/引用 → Crossref 补卷期页
- 📤 **全格式导出**：Text / JSON / BibTeX / RIS / Markdown
- 📥 **PDF 下载**（arXiv、OpenAlex 有 PDF 时）
- 🔑 **S2_API_KEY 完全可选**（无 key 正常运行，仅受速率限制）

---

## 数据源说明

| 数据源 | 是否需要 Key | 特点 |
|--------|------------|------|
| OpenAlex | ❌ 免费 | 覆盖全学科，2 亿+ 记录，完整元数据 |
| Semantic Scholar | ⚠️ 可选 | CS 领域最全，有 key 速率更快（无 key 限 1/s） |
| Crossref | ❌ 免费 | 补充期刊卷/期/页/abstract |
| arXiv | ❌ 免费 | 预印本，PDF 可下载 |
| PubMed | ❌ 免费 | 生物医学方向 |

---

## Semantic Scholar API Key 配置说明

**完全可选。** 不配置也能正常使用，仅受速率限制（约 1 次/秒）。

**有 key 的效果：** 解除速率限制，每秒可发更多请求。

**申请步骤：**
1. 访问 https://www.semanticscholar.org/product/api
2. 注册账号，申请 Free tier（免费）
3. 使用时通过 CLI 参数传入：`--semantic-api-key 'your-key'`

**示例：**
```bash
# 无 key（正常运行）
python scripts/research.py multi "transformer attention" -n 10

# 有 key（速率更快）
python scripts/research.py multi "transformer attention" -n 10 --semantic-api-key 's2k-xxxxx'
```

**注意：** 本 skill 不读取也不存储 `S2_API_KEY` 环境变量，Key 仅通过 CLI 参数传入。

---

## 创作流程

### Step 1：确认检索需求
- 检索主题/关键词
- 目标数据库（multi 推荐）
- 结果数量

### Step 2：执行检索
- 推荐使用 `multi` 模式（自动三步串联）
- 或指定单一数据源（openalex / semantic / arxiv / pubmed）

### Step 3：选择输出格式
- 日常阅读 → `text`
- 论文写作 → `bibtex`（LaTeX / Word 插件导入）
- 文献管理器 → `ris`（Zotero / Mendeley 导入）
- 结构化数据 → `json`

---

## 命令行使用

```bash
python scripts/research.py <source> "<关键词>" [选项]
```

### 数据源（source）

| source | 说明 | 是否需要 Key |
|--------|------|-------------|
| `openalex` | 推荐，全学科覆盖 | ❌ |
| `semantic` | Semantic Scholar | ⚠️ 可选 |
| `multi` | 自动串联三库（推荐） | ⚠️ S2 可选 |
| `crossref` | 用 DOI 查元数据 | ❌ |
| `arxiv` | 预印本 + PDF 下载 | ❌ |
| `pubmed` | 生物医学文献 | ❌ |

### 常用选项

```bash
# 推荐：multi 模式（自动补全）
python scripts/research.py multi "large language model alignment" -n 10 -f bibtex

# OpenAlex 搜索（无需 key）
python scripts/research.py openalex "graph neural networks" -n 20 --year 2023

# 带引用数过滤的 S2 搜索（有 key 更快）
python scripts/research.py semantic "reinforcement learning" -n 10 --min-citations 100

# arXiv 下载 PDF
python scripts/research.py arxiv "transformers" -n 5 --download --output-dir ./papers/

# PubMed 生物医学检索
python scripts/research.py pubmed "CRISPR gene editing" -n 10

# 生成 BibTeX
python scripts/research.py multi "attention mechanism" -n 20 -f bibtex -o refs.bib
```

### 完整参数说明

| 参数 | 说明 | 适用数据源 |
|------|------|-----------|
| `-n, --max-results` | 最大结果数（默认 10） | 全部 |
| `-f, --format` | 输出格式（text/json/bibtex/ris/markdown） | 全部 |
| `-o, --output` | 保存到文件 | 全部 |
| `--year` | 年份过滤 | openalex/semantic/arxiv |
| `--start-date` | 开始日期（YYYY-MM-DD） | openalex/pubmed |
| `--end-date` | 结束日期 | openalex/pubmed |
| `--author` | 作者名 | openalex/semantic/arxiv/pubmed |
| `--min-citations` | 最低引用数 | semantic |
| `--enrich-s2` | S2 补全详情（摘要/引用数） | semantic |
| `--crossref-enrich` | Crossref 补充元数据（默认开启） | openalex/multi |
| `--journal-issn` | 按 ISSN 筛选期刊 | openalex |
| `--concept-id` | 按学科概念 ID 筛选 | openalex |
| `--category` | arXiv 学科分类（如 cs.LG） | arxiv |
| `--publication-type` | PubMed 文献类型 | pubmed |
| `--doi-file` | 从文件读取 DOI 列表 | crossref |
| `--download` | 下载 arXiv PDF | arxiv |
| `--output-dir` | PDF 下载目录 | arxiv |
| `--sort-by` | 排序（relevance/date/citations） | openalex |

---

## 参考文档

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/readme.md` | 详细使用说明、Workflow 示例 | 检索前必读 |
| `references/readme.md` | 安装依赖、故障排查 | 配置环境时 |

---

## 输出格式示例

### BibTeX（用于 LaTeX / Zotero）

```bibtex
@article{vaswani2017attention,
  title={Attention Is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki},
  year={2017},
  journal={arXiv preprint},
  doi={10.48550/arXiv.1706.03762},
  url={https://arxiv.org/abs/1706.03762}
}
```

### RIS（用于 Zotero / Mendeley）

```
TY  - JOUR
TI  - Attention Is All You Need
AU  - Vaswani, Ashish
AU  - Shazeer, Noam
PY  - 2017
JO  - arXiv preprint
DO  - 10.48550/arXiv.1706.03762
ER  -
```

---

## 安装依赖

```bash
pip install -r scripts/requirements.txt
```

**注意：** `S2_API_KEY` 环境变量由用户在 `~/.bashrc` 中自行配置，不写入 skill 文件。

---

*MIT License · 松哥专版*
