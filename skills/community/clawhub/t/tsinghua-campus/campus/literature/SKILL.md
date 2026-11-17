---
name: campus-literature
description: 文献检索（多源：Scopus / arXiv / OpenAlex / Crossref）。基于共享文献引擎搜索学术论文、获取摘要、生成文献包。当用户需要"查文献、搜论文、找相关研究、看摘要"时使用。
metadata:
  openclaw:
    os:
      - windows
      - macos
      - linux
---

# 文献检索（多源）

四源学术检索：Scopus（Elsevier 付费权威）/ arXiv（物理/CS 预印本）/ OpenAlex（开放学术元数据）/ Crossref（DOI 元数据）。Scopus 走 agent 共享底座，其它三个源走校园技能包内置客户端。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：凭据分流**。
  - Scopus 凭据走 **campus 凭据保险箱**（`creds.py add scopus_api_key --value-stdin`），与 agent 项目 `.env` 解耦
  - OpenAlex 凭据走 **统一 .env** 的 `OPENALEX_API_KEY`（可选，强烈建议）
  - arXiv / Crossref 免费，无需凭据
- **铁律 4：多源默认行为**。`search` 不指定 `--source` 默认 `scopus`（保持向后兼容）。**用户未配 scopus_key 时**自动 fallback：OpenAlex/Crossref 免费源即可用。
- **铁律 5：source 顺序敏感**。`--source scopus,arxiv` → 先跑 scopus 失败不影响 arxiv，**结果按源顺序合并**。
- **铁律 6：abuse 检测 / 限流**。OpenAlex 免费版每天仅 $0.01 额度（约 100 次），强烈建议配 Key 升到 $1/天；arXiv 无 Key 限流但 QPS 不可过高；Crossref 建议带 `mailto` UA（已内置）。

### 数据源对比

| 源 | 凭据 | 覆盖 | 优势 | 局限 |
|----|------|------|------|------|
| **Scopus** | `scopus_api_key`（保险箱）| 全学科（生物医学偏弱）| 权威、引用准确、机构 token 提配额 | 付费；清华 IP 受限 |
| **arXiv** | 无 | 物理/数学/CS/生物/统计 | 预印本时效强、含摘要 | 无中文论文；无引用数据 |
| **OpenAlex** | `OPENALEX_API_KEY`（.env，可选）| 全学科，2 亿+ 篇元数据 | 免费、引用/主题/开放访问都有 | 部分元数据 abstract 仅 inverted index（已自动重排）|
| **Crossref** | 无 | DOI 注册的学术论文 | 元数据准确（出版商一手）| 部分论文无摘要（依赖出版商） |

**推荐组合**：
- 有 scopus → `search --source scopus`（默认）
- 无 scopus → `search --source openalex,crossref`（最广免费）
- 物理/CS → 加 `arxiv`（预印本时效强）
- 中文文献 → 当前**四源均不覆盖**，建议走 CNKI/万方（未在本技能包；规划中）

### 所需凭据

| 凭据 | 用途 | 必需 | 获取 |
|------|------|------|------|
| `scopus_api_key` | Scopus API Key | 可选（无则跳过 Scopus）| dev.elsevier.com 注册（清华 CARSI 登录） |
| `scopus_inst_token` | 提升 Scopus 配额 | 可选 | 清华图书馆 Institutional Token |
| `OPENALEX_API_KEY` | OpenAlex 高级额度 | 强烈建议 | openalex.org/settings/api 免费注册（$0.01→$1/天） |
| （无） | arXiv / Crossref 免 Key | — | — |

### 使用

```bash
# 检查凭据 + 列出所有源状态
literature.py status

# 单源检索
literature.py search -q "transformer attention" --source arxiv --count 5
literature.py search -q "graph neural network" --source openalex --count 10
literature.py search -q "TITLE(transformer) AND PUBYEAR > 2020" --source scopus --count 5

# 多源联合检索
literature.py search -q "knowledge graph" --source arxiv,openalex,crossref --count 5

# 按 DOI 取摘要（自动 fallback：openalex → crossref → scopus）
literature.py abstract --doi "10.1109/iccv48922.2021.00986"

# 搜索+摘要完整链路
literature.py full -q "diffusion model" --source openalex --count 3
```

### 检索式说明

- **Scopus 语法**：`TITLE(x)` / `TITLE-ABS-KEY(x)` / `AUTH(x)` / `PUBYEAR > 2023` / `DOCTYPE(ar)` / `AND/OR/NOT` 等
- **arXiv 语法**：`all:<自由词>` 或 `ti:<标题>` / `au:<作者>` / `abs:<摘要>`；`AND/OR/ANDNOT`
- **OpenAlex**：自由文本 + `filter=publication_year:2024` 等
- **Crossref**：自由文本 + `filter=from-pub-date:2024-01-01,until-pub-date:2024-12-31`

### 工作流（多源版）

```
用户: 帮我查一下知识图谱近三年的综述
AI:
  1. literature.py status → 看到 scopus 未配 → 用 openalex,crossref 跑
  2. literature.py search -q "knowledge graph survey" --source openalex,crossref --count 10
  3. per_source 看到两源都返回 → 合并 results 按 cited 排序
  4. 用户选中的 → literature.py abstract --doi <doi>（免费回源）
```

```
用户: 我要看 Swin Transformer 的摘要
AI:
  1. literature.py abstract --doi "10.1109/iccv48922.2021.00986"
     → openalex 自动重排 inverted_index → 返回完整摘要 + 引用数 32501
```

### 边界

- **中文文献不覆盖**（CNKI / 万方未接入；规划中）
- Scopus 免费层：count ≤ 25、start ≤ 5000、429 自动重试；STANDARD 视图无摘要（需 META_ABS）
- arXiv 无引用数据
- OpenAlex abstract_inverted_index 重排偶发空格异常（源数据限制）
- Crossref 部分元数据无摘要（依赖出版商提交）

---

## 如果你是用户，请阅读以下内容

对 AI 说："帮我查 XX 相关的文献"或"这篇论文摘要"。

AI 会从四源（Scopus / arXiv / OpenAlex / Crossref）选合适的源搜索，返回标题、年份、被引次数、DOI、作者。Scopus 需要 API Key（dev.elsevier.com 申请）；其他三源免费，无需配置。

如果想让 OpenAlex 更快（$0.01/天 → $1/天），到 openalex.org/settings/api 注册免费 Key 写到 `campus/.env` 的 `OPENALEX_API_KEY=...`。