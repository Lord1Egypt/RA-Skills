# semanticscholar-skill — 命令行下的 Semantic Scholar 📚

[English](README.md) | [Semantic Scholar API 文档](https://api.semanticscholar.org/api-docs/) | [申请 API Key](https://www.semanticscholar.org/product/api#api-key)

## 功能特性

- **搜索** Semantic Scholar 语料库 —— 支持关键词、布尔表达式、全文片段、标题、作者
- **查论文** —— 支持 DOI / arXiv / PMID / PMCID / CorpusId / MAG / ACL / SHA / URL 等任意 ID
- **引用遍历** —— 前向 / 后向引用,支持分页
- **相似论文推荐** —— 单种子 `find_similar`,或多种子正负样本 `recommend`
- **作者检索** —— 按姓名找研究者,列出发表论文、拉取 h-index / 单位
- **批量查询** —— 一次最多 500 篇论文 / 1000 位作者
- **过滤** —— 年份、日期范围、venue、学科、最小引用数、论文类型、开放获取
- **导出** —— BibTeX / Markdown / JSON
- **内置限流与重试** —— 请求间隔 1.1s,429/504 指数退避
- **单脚本执行模式** —— 避免顺序 API ping-pong,所有调用合并到一个 Python 脚本
- 当用户提到论文、引用、学术搜索、文献发现时自动触发

## 多平台支持

适配所有支持 [Agent Skills](https://agentskills.io) 格式的 AI 编程助手:

| 平台 | 状态 | 说明 |
|------|------|------|
| **Claude Code** | ✅ 完全支持 | 原生 SKILL.md 格式 |
| **Codex** | ✅ 完全支持 | 原生 SKILL.md + `agents/openai.yaml` 界面元数据 |
| **Hermes** | ✅ 完全支持 | `metadata.hermes` tags / category / related_skills |
| **OpenClaw** | ✅ 完全支持 | `metadata.openclaw` 命名空间 |
| **ClawHub** | ✅ 已发布 | `clawhub install semanticscholar-skill` |
| **SkillsMP** | ✅ 已收录 | GitHub topics 已配置 |

## 为什么选择 Semantic Scholar?

Semantic Scholar **不是又一个预印本服务器** —— 它是一个覆盖包括 arXiv 和 bioRxiv 在内整个学术语料库的**学术图谱 + 语义索引**。问题从来不是"S2 *还是* arXiv",而是"S2 *叠加在* arXiv *之上*"。

| 维度 | arXiv | bioRxiv | **Semantic Scholar** |
|---|---|---|---|
| 定位 | 预印本仓库(物理 / CS / 数学 / 统计) | 预印本仓库(生物 / 医学) | 覆盖 2 亿+ 论文的聚合学术图谱 |
| 语料范围 | 仅 arXiv(~250 万篇) | 仅 bioRxiv/medRxiv(~35 万篇) | arXiv + bioRxiv + PubMed + 会议论文 + 期刊 + 更多 |
| 搜索方式 | 关键词 / 分类号 | 关键词 / 学科 | 关键词 + **语义相关度排序** + 布尔 + 全文片段 |
| 引用图谱 | ❌ 无 | ❌ 无 | ✅ 前向 / 后向引用、influential citations |
| "相似论文" | ❌ | ❌ | ✅ `find_similar` + 多种子 `recommend` |
| 作者消歧 | 部分(无统一 ID) | 部分 | ✅ 统一 `authorId`、单位、h-index |
| venue / 年份 / 引用数过滤 | 有限 | 有限 | ✅ 丰富过滤:venue、学科、最小引用数、OA、论文类型 |
| TLDR 摘要 | ❌ | ❌ | ✅ 大多数论文有 `tldr` 字段 |
| BibTeX 导出 | 需去 arxiv.org | 需去 bioRxiv | ✅ API `citationStyles` 字段 |

**实操原则:**
- 已知具体 arXiv / bioRxiv 论文 ID → 直接访问源站
- 想**发现**相关 / 有影响力 / 被引 / 相似的论文 → 用 Semantic Scholar
- 想在**一次排序结果里同时看到预印本和已发表文献** → 用 Semantic Scholar
- 做文献综述、相关工作小节、引用分析 → 用 Semantic Scholar

这个技能不是取代 arXiv 或 bioRxiv,而是位于它们之上,补齐它们缺失的图谱 / 排序 / 推荐层。

## 对比

### vs. `asta-skill`(基于 MCP 的姊妹技能)

| 能力 | `semanticscholar-skill` | `asta-skill` |
|---|---|---|
| 传输方式 | Python + 直连 REST(`s2.py`) | MCP(streamable HTTP) |
| 运行依赖 | Python + `S2_API_KEY` | Host 支持 MCP |
| 最佳场景 | 脚本化批处理、复杂过滤 | 零代码 agent 集成 |
| 布尔查询构造器 | ✅ `build_bool_query()` | ❌ |
| 多种子推荐 | ✅ `recommend(pos, neg)` | ❌ |
| BibTeX / Markdown / JSON 导出 | ✅ 内置 | ❌ |
| Cursor / Windsurf 开箱即用 | ❌ | ✅ |

### vs. 原生 Agent(无技能)

| 能力 | 原生 Agent | 本技能 |
|---|---|---|
| 知道 S2 API 基础 URL 与认证头 | 或许 | ✅ |
| 布尔查询构造器 | ❌ | ✅ `build_bool_query()` |
| 单脚本执行模式(无 ping-pong) | ❌ | ✅ 强制 |
| 自动限流与指数退避 | ❌ | ✅ |
| BibTeX / Markdown / JSON 导出 | ❌ | ✅ |
| 去重辅助 | ❌ | ✅ `deduplicate()` |
| 阶段式工作流(Plan → Execute → Summarize → Loop) | ❌ | ✅ |

## 前置条件

- `python3`
- `pip install requests`
- (可选)[Semantic Scholar API Key](https://www.semanticscholar.org/product/api#api-key),用于提高速率上限:

  ```bash
  export S2_API_KEY=xxxxxxxxxxxxxxxx
  ```

未认证也可使用,但速率限制很严格。

## 技能安装

### Claude Code

```bash
# 全局安装(所有项目可用)
git clone https://github.com/Agents365-ai/semanticscholar-skill.git ~/.claude/skills/semanticscholar-skill

# 项目级
git clone https://github.com/Agents365-ai/semanticscholar-skill.git .claude/skills/semanticscholar-skill
```

### Codex

```bash
git clone https://github.com/Agents365-ai/semanticscholar-skill.git ~/.codex/skills/semanticscholar-skill
```

### OpenClaw

```bash
git clone https://github.com/Agents365-ai/semanticscholar-skill.git ~/.openclaw/skills/semanticscholar-skill

# 项目级
git clone https://github.com/Agents365-ai/semanticscholar-skill.git skills/semanticscholar-skill
```

### ClawHub

```bash
clawhub install semanticscholar-skill
```

### SkillsMP

```bash
skills install semanticscholar-skill
```

### 安装路径汇总

| 平台 | 全局路径 | 项目路径 |
|------|---------|---------|
| Claude Code | `~/.claude/skills/semanticscholar-skill/` | `.claude/skills/semanticscholar-skill/` |
| Codex | `~/.codex/skills/semanticscholar-skill/` | 暂无 |
| OpenClaw | `~/.openclaw/skills/semanticscholar-skill/` | `skills/semanticscholar-skill/` |
| ClawHub | 通过 `clawhub install` | — |
| SkillsMP | 通过 `skills install` | — |

## 使用方式

直接用自然语言描述需求:

```
> 用 semanticscholar-skill 搜索 2023 年以来 NeurIPS 的 mixture-of-experts 论文

> 找引用 "Attention Is All You Need" 的论文,按引用数排序

> 用 build_bool_query 查 IBD 中的 "stem-like T cells",排除 mesenchymal

> 推荐与 DOI:10.1038/nature14539 和 ARXIV:2010.11929 相似的论文,排除 NLP

> 将前 10 条结果导出为 BibTeX
```

技能会自动选对搜索函数、配置过滤器,并把全部调用放进一个 Python 脚本运行,限流由 `s2.py` 处理。

## 辅助模块

`s2.py` —— 单文件模块,通过 `from s2 import *` 导入:

| 类别 | 函数 |
|---|---|
| 论文搜索 | `search_relevance`, `search_bulk`, `search_snippets`, `match_title`, `get_paper`, `get_citations`, `get_references`, `find_similar`, `recommend`, `batch_papers` |
| 作者搜索 | `search_authors`, `get_author`, `get_author_papers`, `get_paper_authors`, `batch_authors` |
| 查询构造 | `build_bool_query(phrases, required, excluded, or_terms)` |
| 输出 | `format_table`, `format_details`, `format_results`, `format_authors`, `export_bibtex`, `export_markdown`, `export_json`, `deduplicate` |

完整 API 参考见 `SKILL.md`。

## 文件说明

- `SKILL.md` —— **唯一必需文件**。所有平台都以此作为技能指令加载
- `s2.py` —— Python 辅助模块(限流、重试、查询构造、格式化输出)
- `agents/openai.yaml` —— Codex 界面元数据
- `README.md` —— 英文文档(GitHub 主页显示)
- `README_CN.md` —— 本文件(中文文档)

## 已知限制

- **Semantic Scholar 免费层速率受限** —— 未认证约 1 req/sec,全体用户共享;API key 能提高个人上限但不是无限
- **bulk search 不返回 TLDR** —— 改用 `abstract` 字段
- **并非所有论文都有摘要** —— 有些只暴露标题 + TLDR
- **作者消歧** —— 常见姓名会重名,调用 `get_author_papers` 前先核对单位
- **大字段要小心** —— `get_paper` 的 `fields` 不要加 `citations` / `references`(高被引论文会炸上下文),改用分页的 `get_citations`

## License

MIT

## 支持

如果这个技能对你有帮助,欢迎打赏支持作者:

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="微信支付">
      <br>
      <b>微信支付</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="支付宝">
      <br>
      <b>支付宝</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
  </tr>
</table>

## 作者

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai
