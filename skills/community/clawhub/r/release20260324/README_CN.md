<p align="center">
  <img alt="OpenPaperGraph" src="figures/logo-part-light-full.png" width="420">
</p>

<h3 align="center">OpenClaw 时代的学术研究助手</h3>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/dependencies-3-green.svg" alt="3 Dependencies">
  <img src="https://img.shields.io/badge/LLM_providers-20+-orange.svg" alt="20+ LLM Providers">
  <img src="https://img.shields.io/badge/data_sources-8-purple.svg" alt="8 Data Sources">
  <img src="https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-lightgrey.svg" alt="License">
</p>

<p align="center">
  中文 | <a href="README.md">English</a>
</p>

<p align="center">
  <b>跨 8 大数据源搜索论文，构建引用网络，生成 AI 摘要。</b><br>
  可作为 Claude Code / OpenClaw 的 <code>/opg</code> 技能使用，也可独立运行。<br>
  无需 API Key，仅需 3 个 pip 包，一键安装。
</p>

---

## 为什么选择 OpenPaperGraph？

在 **Claude Code** 和 **OpenClaw** 等 AI Agent 时代，研究者需要与工作流无缝配合的工具。OpenPaperGraph 正是为此而生：

- **Agent 原生** — JSON 标准输出，零交互输入，可与任何 AI 工具组合
- **多源容灾** — 8 大数据源 + 自动降级，单个 API 宕机不影响使用
- **本地优先** — 数据以 JSON 文件存储在本地，无云端依赖
- **极简依赖** — 仅 3 个依赖包，无数据库，无 Docker（GROBID 可选）

---

## 快速开始

### Claude Code / OpenClaw 用户

```bash
# 一键安装
bash install.sh --global

# 然后在 Claude Code 中直接输入：
#   /opg 搜索关于 LLM agent 安全的论文
#   /opg 基于 ARXIV:1706.03762 构建引用网络
```

### 独立 CLI 使用

```bash
pip install httpx pymupdf scholarly

# 搜索 → 构建 → 探索 → 导出
python openpapergraph_cli.py search "prompt injection" --limit 5 --pretty
python openpapergraph_cli.py graph ARXIV:1706.03762 -o graph.json
python openpapergraph_cli.py serve graph.json        # -> http://localhost:8787
python openpapergraph_cli.py export graph.json --format bibtex -o refs.bib
```

> 无需 API Key。所有核心功能均可通过免费公开 API 使用。

---

## 功能一览

| | 命令 | 说明 |
|---|------|------|
| **发现** | `search` | 跨 arXiv + DBLP + Semantic Scholar 多源搜索 |
| | `recommend` | 通过 S2 API 获取相关论文推荐 |
| | `monitor` | 追踪某个主题的最新论文 |
| **构建** | `graph` | 从标题、ID、PDF 或 BibTeX 构建引用网络 |
| | `graph-from-pdf` | 从 PDF 参考文献列表直接构建引用图 |
| | `pdf` | 从 PDF 中提取并解析参考文献 |
| | `zotero` | 从 Zotero 文献库导入 |
| **管理** | `serve` | 基于浏览器的交互式图编辑器（持久化存储） |
| | `remove-seed` | 删除种子论文及其独占连接 |
| | `remove-paper` | 从图中删除非种子论文 |
| **分析** | `analyze` | 主题分析：关键词、年份趋势、高产作者 |
| | `summary` | AI 驱动或抽取式研究摘要 |
| **导出** | `export` | BibTeX / CSV / Markdown / JSON |
| | `export-html` | 自包含的交互式 HTML 可视化 |
| **工具** | `conferences` | 列出支持的会议过滤项 |
| | `llm-providers` | 显示 20+ LLM 提供商及配置状态 |

**通用参数**：`--output` / `-o`（保存到文件）、`--pretty`（格式化 JSON）、`--quiet`（静默模式）

---

## 典型工作流

```
  搜索          构建           探索            分析           导出
  ──────>      ──────>       ──────>        ──────>       ──────>
  search   graph/graph-from-pdf  serve     analyze+summary   export/export-html
  recommend                  (浏览器 UI)                    (bibtex, csv, md, html)
  monitor                    添加/转化/删除
```

```bash
# 1. 查找种子论文
python openpapergraph_cli.py search "attention is all you need" --limit 5 --pretty

# 2. 构建引用网络
python openpapergraph_cli.py graph ARXIV:1706.03762 -o graph.json

# 3. 交互式探索（添加论文、扩展种子 — 所有修改自动保存）
python openpapergraph_cli.py serve graph.json

# 4. 分析
python openpapergraph_cli.py analyze graph.json --pretty
python openpapergraph_cli.py summary graph.json --style overview --pretty

# 5. 导出
python openpapergraph_cli.py export graph.json --format bibtex -o refs.bib
python openpapergraph_cli.py export-html graph.json -o graph.html --summary
```

---

## 交互式图谱服务器（`serve`）

**前提**：需要先有一个 graph JSON 文件。使用 `graph` 或 `graph-from-pdf` 构建：

```bash
# 1. 先构建引用图
python openpapergraph_cli.py graph ARXIV:1706.03762 -o graph.json

# 2. 再启动服务器
python openpapergraph_cli.py serve graph.json --port 8787
# 在浏览器中打开 http://localhost:8787
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--port` | 8787 | HTTP 服务器端口 |
| `--title` | `"Paper Graph"` | 浏览器页面标题 |

### 浏览器前端功能

**图谱可视化**（基于 vis.js）
- 交互式力导向网络布局，支持拖拽、缩放、平移
- 节点颜色编码：种子论文（紫色星形）、参考文献（蓝色，左侧）、引用文献（绿色，右侧）
- 基于年份的渐变着色 + 可视化图例
- 悬浮提示显示标题、作者、年份、引用数和摘要
- 点击节点高亮其直接连接

**工具栏 & 搜索**
- 实时搜索标题、作者和年份
- 按节点类型（全部 / 种子 / 参考文献 / 引用文献）和数据源过滤
- 论文数量统计芯片（种子、参考文献、引用文献）

**添加论文**（服务器模式独有）
- 点击 `+ Add Paper` 按钮打开模态框，支持三种输入方式：
  - **标题** — 输入论文标题，系统通过 arXiv + Semantic Scholar 自动解析
  - **BibTeX** — 粘贴 BibTeX 条目直接导入
  - **PDF** — 拖放或点击上传 PDF，自动提取元数据和参考文献
- 勾选 **"Treat as Seed Paper"** 触发完整扩展（参考文献 + 引用文献）
- 与 `graph` 命令相同的检索限制（每篇论文最多 50 条引用、100 条 S2 参考文献）
- SSE 驱动的实时进度条

**转化为种子论文**
- 悬浮在非种子节点上，点击提示框中的 **"Convert to Seed Paper"**
- 触发完整扩展：下载 PDF、解析参考文献、抓取引用文献
- 带实时进度追踪的确认对话框

**删除种子论文**
- 来源面板列出所有种子论文及其参考/引用数量
- 点击 **Remove** 删除种子及其独占连接
- 确认对话框防止误删

**元数据补全**
- **Enrich** 按钮为所有论文补全缺失的摘要、引用数、DOI 等元数据

**持久化存储**
- 所有操作（添加、转化、删除、补全）立即写入 JSON 文件
- 随时刷新页面，所有更改均已保存

**侧边栏**
- 按引用数排序的可滚动论文列表，按类型分组
- 点击任意论文定位并高亮图中节点
- 外部链接跳转至 Semantic Scholar、arXiv 和 DOI 页面

### 默认检索限制

构建图谱（`graph` 命令）和服务器模式（`serve` 添加论文）使用相同的检索限制：

| 数据 | 来源 | 默认限制 |
|------|------|---------|
| **参考文献** | PDF 解析（本地） | 无限制（提取 PDF 中所有参考文献） |
| **参考文献** | S2 API（降级） | 每篇论文 100 条 |
| **引用文献** | Google Scholar | 每篇论文 50 条 |
| **引用文献** | S2 API（降级） | 每篇论文 50 条 |
| **depth > 1 扩展** | S2 API | 20 条参考文献 × 前 10 篇高引论文 |

这些限制为硬编码值，在完整性和 API 速率限制之间取得平衡，当前不可通过命令行参数修改。对于有数百条引用的论文，仅检索前 50 条；其余可通过在 `serve` 中将这些论文转化为种子来发现。

---

## 架构：多源设计

OpenPaperGraph 通过组合 8 大学术数据库 + 智能降级策略，降低对单一数据源的依赖：

| 任务 | 主要数据源 | 降级方案 |
|------|-----------|---------|
| **搜索** | arXiv + DBLP + Semantic Scholar | 自动去重，按引用量排序 |
| **参考文献** | 下载 PDF -> 解析参考文献列表 | S2 API |
| **引用** | Google Scholar | S2 API |
| **推荐** | S2 推荐 API | — |
| **PDF 下载** | arXiv -> Unpaywall（开放获取） | 直接 URL |
| **参考文献解析** | arXiv -> CrossRef -> OpenAlex | 多级级联 |

即使某个 API 宕机或被限流，工具仍可正常工作。

---

## 安装

### 环境要求

- **Python 3.8+**
- **pip** 包管理器
- **网络连接**（用于查询学术 API）

### 核心依赖（3 个包）

```bash
pip install httpx pymupdf scholarly
```

| 包 | 用途 |
|----|------|
| `httpx` | 所有 API 调用的 HTTP 客户端 |
| `pymupdf` | PDF 文本提取 |
| `scholarly` | Google Scholar 访问（未安装时自动降级到 S2） |

### 可选

```bash
pip install openai  # 用于 LLM 驱动的摘要（支持 20+ 提供商）
```

### API Key（均为可选）

```bash
export S2_API_KEY="..."          # 推荐：避免 S2 限流（免费申请）
export OPENAI_API_KEY="sk-..."   # 或任意 20+ LLM 提供商的 Key，用于 AI 摘要
```

> **所有命令无需 API Key 即可使用。** arXiv、DBLP、CrossRef、OpenAlex、Unpaywall 完全免费。

---

## `/opg` 技能用法（Claude Code / OpenClaw）

安装为技能后（`bash install.sh --global`），所有命令均可在 Claude Code 或 OpenClaw 中通过自然语言调用：

| 你想做什么 | 在 Claude Code 中输入 |
|-----------|---------------------|
| 搜索论文 | `/opg 搜索关于 transformer attention 的论文` |
| 构建引用图 | `/opg 基于 ARXIV:1706.03762 构建引用网络` |
| 获取推荐 | `/opg 推荐与 ARXIV:1706.03762 相似的论文` |
| 交互查看 | `/opg 启动 graph.json 的图服务器` |
| 分析网络 | `/opg 分析 graph.json 的引文网络` |
| 导出 | `/opg 将引用网络导出为 BibTeX` |
| 监控新论文 | `/opg 监控 2025 年以来 LLM agent 安全的新论文` |
| PDF 提取 | `/opg 从 paper.pdf 提取参考文献` |

| | `/opg` 技能 | Python CLI |
|---|-------------|------------|
| **调用方式** | 自然语言 | 命令行参数 |
| **输出** | AI 自动格式化 | 原始 JSON（`--pretty` 格式化） |
| **多步骤** | AI 自动串联步骤 | 手动逐步执行 |
| **安装** | `bash install.sh --global` | `pip install httpx pymupdf scholarly` |

---

## 环境变量

### S2_API_KEY（推荐）

免费申请：[semanticscholar.org/product/api](https://www.semanticscholar.org/product/api)，避免限流。

```bash
export S2_API_KEY="your_key_here"
```

### LLM API Key（可选 — 任选其一）

<details>
<summary><b>20+ 支持的提供商</b></summary>

#### 国际提供商

| 提供商 | 环境变量 | 默认模型 |
|--------|---------|---------|
| OpenAI | `OPENAI_API_KEY` | `gpt-4o-mini` |
| Anthropic | `ANTHROPIC_API_KEY` | `claude-sonnet-4-20250514` |
| Google Gemini | `GEMINI_API_KEY` | `gemini-2.0-flash` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| Groq | `GROQ_API_KEY` | `llama-3.1-8b-instant` |
| Together AI | `TOGETHER_API_KEY` | `Llama-3.1-8B-Instruct-Turbo` |
| Mistral | `MISTRAL_API_KEY` | `mistral-small-latest` |
| xAI (Grok) | `XAI_API_KEY` | `grok-3-mini-fast` |
| Perplexity | `PERPLEXITY_API_KEY` | `sonar` |
| OpenRouter | `OPENROUTER_API_KEY` | `llama-3.1-8b-instruct:free` |

#### 国内提供商

| 提供商 | 环境变量 | 默认模型 |
|--------|---------|---------|
| 智谱 AI | `ZHIPUAI_API_KEY` | `glm-4-flash` |
| 月之暗面 | `MOONSHOT_API_KEY` | `moonshot-v1-8k` |
| 百川 | `BAICHUAN_API_KEY` | `Baichuan2-Turbo` |
| 零一万物 | `YI_API_KEY` | `yi-lightning` |
| 通义千问 | `DASHSCOPE_API_KEY` | `qwen-turbo` |
| 豆包 | `ARK_API_KEY` | `doubao-lite-32k` |
| MiniMax | `MINIMAX_API_KEY` | `MiniMax-Text-01` |
| 阶跃星辰 | `STEPFUN_API_KEY` | `step-1-flash` |
| 商汤日日新 | `SENSENOVA_API_KEY` | `SenseChat-Turbo` |

#### 自托管 / 自定义

```bash
export LLM_API_KEY="your_key"
export LLM_BASE_URL="http://localhost:11434/v1"  # 例如 Ollama
export LLM_MODEL="llama3"
```

</details>

---

## GROBID 设置（可选）

[GROBID](https://github.com/kermitt2/grobid) 提供结构化 PDF 提取，参考文献解析率 **70-90%**（正则方式为 40-60%）。

```bash
docker run -d --name grobid -p 8070:8070 lfoppiano/grobid:0.8.1
python openpapergraph_cli.py pdf paper.pdf --use-grobid
```

---

## 数据源

| 数据源 | 覆盖范围 | 用途 |
|--------|---------|------|
| **arXiv** | 预印本（CS、物理、数学、生物） | 搜索、PDF 下载、解析 |
| **DBLP** | CS 会议与期刊 | 搜索、会议过滤 |
| **Google Scholar** | 全学科 | 引用数据、引用计数 |
| **Semantic Scholar** | 2 亿+ 论文 | 搜索降级、推荐 |
| **CrossRef** | DOI 注册出版物 | 参考文献解析 |
| **OpenAlex** | 2.5 亿+ 作品 | 参考文献解析 |
| **Unpaywall** | 开放获取 PDF | PDF 下载 |
| **Zotero** | 用户个人文献库 | 导入文献集 |

---

## 联系方式

问题、建议或合作请联系：**notyour_mason@outlook.com**

---

## 许可证

OpenPaperGraph 采用 [PolyForm Noncommercial License 1.0.0](LICENSE) 许可。
