---
name: unified-research-finder
description: 统一的学术文献检索助手。覆盖两大体系：(1) PubMed 官方 E-utilities API（esearch+efetch，真实
  PMID/摘要/DOI）与 PubMed 网页检索；(2) Google Scholar 及其镜像站——灯塔学术搜索、烂番薯学术搜索、Google
  Scholar 香港镜像、Google Scholar 官方站，以及 KipHub学术、学术搜索Pro 等大陆镜像，按「kiphub → 烂番薯 → 学术搜索Pro → 灯塔 → 香港 → 官方」优先级自动回退。当用户要找文献、查论文、搜 PubMed、查 Google
  学术/谷歌学术、用学术镜像站、要影响因子或引用数据时启用。找不到就是找不到，绝不编造。
agent_created: true
version: v1.1.1
triggers:
  - 找文献
  - 检索论文
  - 搜索文献
  - 查论文
  - 查 PubMed
  - PubMed 检索
  - 医学文献
  - Google 学术
  - 谷歌学术
  - 学术搜索
  - 学术镜像
  - 烂番薯
  - 灯塔学术
  - KipHub
  - 学术搜索Pro
  - 查影响因子
  - 论文引用
  - 相关论文
  - 推荐文献
  - 双库检索
  - 合并去重
  - 跨库检索
  - 多库去重
disable: false
tools:
  - unified_search
  - pubmed_search
  - scholar_search
---

# 学术文献检索助手 (Unified Research Finder)

## ⚠️ 第一原则：真实、可验证，绝不编造

- ✅ 只返回脚本真实返回的文献（PubMed API / Scholar 镜像真实响应）。
- ✅ 明确标注「未找到」当检索无果或所有源被拦截。
- ✅ 提供可点击的链接（PubMed / DOI / 原文 / PDF）。
- ❌ 绝不生成虚假标题、作者、PMID、引用数或下载链接。
- ❌ 网络不通或源被拦截时，如实说明，不臆造结果。

## 🔁 默认行为：PubMed + Scholar 多库合并去重（默认开启）

- **默认同时检索两大库**：PubMed（官方 E-utilities API）+ Google Scholar 及镜像站（灯塔 JSON 优先），再合并。
- **默认开启跨库去重**：以 DOI 或归一化标题为键，剔除 PubMed 与 Scholar 之间的重复文献（同一篇论文不会重复出现）。
- **⚠️ 每次查找，必须明确告知用户**：「已开启多库去重，可手动关闭」（即 `unified_search.py` 输出里的 `dedup_note`）。
- **用户要求不去重时**：改用 `unified_search.py --no-dedup`（仍同时检索两库，但保留重复项）；或直接走流程 A / 流程 B 的单库检索。
- 入口脚本：`scripts/unified_search.py`（详见下方「流程 C」）。

## 何时使用本技能

- 用户要找某主题 / 篇名 / 作者 / 关键词的文献。
- 用户要查 PubMed（医学、生物、生物医学预印本）。
- 用户要查 Google Scholar、谷歌学术，或点名「烂番薯 / 灯塔 / 香港镜像 / 官方站」。
- 用户要影响因子、被引次数、PDF 全文链接、DOI。

## 两大子系统与脚本

| 子系统 | 脚本 | 说明 |
|--------|------|------|
| **PubMed（API + 网页）** | `scripts/pubmed_search.py` | 基于 NCBI E-utilities 官方 API，仅用标准库，无需装包。 |
| **Google Scholar + 镜像** | `scripts/scholar_search.py` | 自动按优先级检索 4 个源，纯标准库；可选 Playwright 兜底。 |
| **双库合并去重（默认）** | `scripts/unified_search.py` | 同时检索 PubMed + Scholar，合并并按 DOI/标题去重；`--no-dedup` 可关。 |

参考文档：`references/scholar-sources.md`（四源技术细节）、
`references/pubmed-query-syntax.md`（PubMed 检索语法）、
`references/register-api-key.md`（NCBI API key 注册引导）。

---

## 流程 A：PubMed 检索（医学 / 生物 / 影响因子）

适用于：医学、生物医学、生命科学，或用户明确提到 PubMed / PMID / DOI / 影响因子。

1. **构造检索式**：将自然语言转为 PubMed 查询。需要复杂式（MeSH、字段、文献类型、日期）时，先读 `references/pubmed-query-syntax.md`。
   - 「最新研究」→ 加 `--sort pub_date`
   - 「最相关 / 权威」→ 默认 `--sort relevance`
   - 「RCT / 系统综述 / Meta」→ 查询串加 `randomized controlled trial[pt]` 等
   - 未指定篇数 → 默认 `--retmax 5`
   - 用户直接给 PMID → 用 `--pmids` 模式
2. **运行脚本**：
   ```bash
   # 关键词检索（esearch → efetch 自动串联）
   python scripts/pubmed_search.py --query "metformin AND type 2 diabetes" --retmax 5
   # 限定年份 + 按日期排序
   python scripts/pubmed_search.py --query "semaglutide[tiab] AND obesity[mh]" --sort pub_date --mindate 2023/01/01 --retmax 5
   # 直接按 PMID 获取
   python scripts/pubmed_search.py --pmids 36967777 37397787
   ```
   脚本向 stdout 输出 JSON：`{ok, query, count, pmids, articles[]}`。每篇含 `pmid, title, authors[], journal, pubdate, abstract, doi, doi_url, pubmed_url`。
3. **整理为中文报告**（遵循 `references/` 中的模板）：标题（附中文翻译）、作者、期刊、日期、PMID、DOI、摘要中文概述、原文摘要折叠块。
4. **API key 引导**：当脚本输出 `api_key_hint: true`（批量或限流），读取 `references/register-api-key.md` 并用大白话引导用户注册免费 NCBI API key。key 仅作命令参数 / 环境变量 `NCBI_API_KEY`，不写入文件。

> 网络不通 `eutils.ncbi.nlm.nih.gov` 时如实告知，不编造。纯网页版 PubMed 检索可用浏览器访问 `pubmed.ncbi.nlm.nih.gov` 作为补充。

---

## 流程 B：Google Scholar 及镜像站检索

适用于：全学科文献、引用数据、PDF 全文、用户点名 Scholar / 谷歌学术 / 镜像站。

1. **运行脚本**（默认 auto，按优先级自动回退）：
   ```bash
   # 自动：kiphub → 烂番薯 → 学术搜索Pro → 灯塔 → 香港 → 官方，取首个有结果的源
   python scripts/scholar_search.py --query "large language model survey" --num 10
   # 指定单一源（如用户只要灯塔）
   python scripts/scholar_search.py --query "..." --source dotaindex
   # 按日期排序 + 限 2020 年以来
   python scripts/scholar_search.py --query "..." --sort date --ylo 2020
   # 分页 / 偏移
   python scripts/scholar_search.py --query "..." --num 20 --start 0
   ```
   输出 JSON：`{ok, source, query, count, results[], note}`。每篇结果含
   `title, url, authors, year, venue, snippet, citations, pdf_url`。
2. **源优先级与回退**（默认 auto 行为）：
   - **kiphub**（KipHub学术）优先——大陆直连、自定义 HTML 结构（`paper-summary-wrapper`），当前最快最稳。
   - **烂番薯**（lanfanshu）次之——经典 Scholar HTML，添加了 `hl/as_sdt/btnG` 固定参数以绕过反爬墙。
   - **学术搜索Pro**（scholar_pro）再次——card 布局自定义 HTML，含摘要和被引次数。
   - **灯塔**（dotaindex）——JSON API，最快最省内存，但近期后端不稳定（500/超时）。
   - **香港镜像 / 官方站**——经典 HTML，大陆常被网络阻断。
   - 任一源被拦截（403/验证码/超时）自动尝试下一源；全部失败则在 `note` 说明，**不返回虚构文献**。
3. **浏览器兜底（可选）**：当所有 HTTP 尝试被拦截且用户需要，安装 Playwright 后以 `--browser` 模式启动无头浏览器渲染：
   ```bash
   pip install playwright && playwright install chromium
   python scripts/scholar_search.py --query "..." --browser
   ```
   仅 HTML 源启用浏览器；灯塔 JSON 无需浏览器。此模式较重，按需使用以节省资源。
4. **整理为中文报告**：逐篇列出 标题、作者、年份、来源(vision)、摘要片段、被引次数、链接（原文 + PDF 全文若有）。

> 设计取舍：默认纯标准库 HTTP，启动快、内存低；Playwright 仅作被拦截时的兜底，避免常驻重进程。详见 `references/scholar-sources.md`。

---

## 流程 C：双库合并去重检索（默认推荐）

适用于绝大多数场景：用户只说「帮我找 XX 的文献」「搜一下 XX」，未限定只用某一库。

1. **运行入口脚本**（默认即开启跨库去重）：
   ```bash
   # 同时检索 PubMed + Scholar，合并并按 DOI / 归一化标题去重（默认）
   python scripts/unified_search.py --query "CRISPR gene editing" --num 10
   # 按日期排序 + 限 2022 以来
   python scripts/unified_search.py --query "..." --sort date --ylo 2022
   # 用户要求不去重时（仍同时检索两库，保留重复项）
   python scripts/unified_search.py --query "..." --no-dedup
   ```
   输出 JSON：`{ok, query, dedup_enabled, dedup_note, pubmed_count, scholar_count,
   merged_count, deduped_count, removed_count, pubmed{}, scholar{}, results[]}`。
   每条统一记录含 `db(pubmed|scholar), title, authors, year, venue, snippet, citations,
   url, pdf_url, doi, doi_url, pmid, pubmed_url`。
2. **⚠️ 必须告知用户**：无论结果多少，先说一句
   **「已开启多库去重，可手动关闭」**（即输出里的 `dedup_note`）。
   用户若说「不用去重 / 关掉去重」，则用 `--no-dedup` 重跑。
3. **整理为中文报告**：逐篇列出（用 `db` 字段标注来自 PubMed 还是 Scholar）：
   标题、作者、年份、来源、摘要/片段、被引次数、链接（原文 + PDF/DOI + PubMed）。
   去重计数可附注：「共合并 N 条，去重后 K 条（移除 R 条重复）」。
4. **单库回退**：当用户明确只要 PubMed 或只要 Scholar 时，分别走流程 A / 流程 B。

---

## 输出格式

### 找到文献时

```
📄 检索结果 [1/N]

标题：{title}（{中文译名，如有}）
作者：{authors}
年份 / 来源：{year} · {venue}
被引次数：{citations}（{source}）
🔗 链接：
- 原文：{url}
- PDF：{pdf_url}（若有）
📋 摘要：{snippet 或 PubMed 摘要中文概述}
---
```

### 未找到 / 全部源被拦截时

```
❌ 未找到符合条件的文献 / 全部数据源暂不可达

检索条件：{query}，年份≥{ylo}，排序={sort}
已开启多库去重：是（--no-dedup 可关）
尝试数据源：PubMed（官方 API）、KipHub、烂番薯、学术搜索Pro、灯塔、香港镜像、Google 官方
结果：{note 中的具体原因，如「PubMed 可达但无命中；烂番薯与灯塔均触发限流，香港/官方站网络不可达」}
建议：稍后重试；或换更宽泛关键词；或 installed Playwright 后用 --browser 模式。
```

## 相关技能 / 后续

- 读文献、做摘要：可配合阅读类 skill。
- 引用管理、影响因子核实：Crossref / JCR / 中科院分区。
