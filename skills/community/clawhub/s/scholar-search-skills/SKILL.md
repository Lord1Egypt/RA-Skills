---
name: scholar-search-skills
description: 学术论文搜索与下载工具。当用户要求搜索某一主题的科研论文时触发此技能，支持从 arXiv、ICLR、ICML、NeurIPS 等来源搜索、筛选和下载论文，并生成结构化摘要和 BibTeX 引用。
---

# Scholar Search Skills

## 概述

本技能用于系统性地搜索、筛选和下载学术论文，适用于研究课题调研、文献综述等场景。集成了 arxiv-search、docling 等工具，支持自动化摘要提取和引用追踪。

## 触发条件

当用户提出以下需求时触发：
- "帮我搜索关于 XXX 的论文"
- "查找 XXX 相关的学术文献"
- "搜索 XXX 主题的研究论文"
- "找一些 XXX 领域的核心文献"
- "帮我下载 XXX 主题的论文"

## 工作流

### 步骤 1: 确认基本信息

与用户确认以下信息：

1. **研究主题/论文标题**：用户想要搜索的具体主题
2. **关键词**：用逗号分隔，建议使用英文关键词
   - 如果用户提供中文关键词，自动翻译为英文
   - 示例：`Agent, Indirect Prompt Injection Attack, Black-box Defense`
3. **核心论文（可选）**：用户已有关键文献列表
4. **筛选条件（可选）**：
   - 时间范围：默认近3年（2023-2026）
   - 来源：arXiv、ICLR、ICML、NeurIPS
   - 引用量阈值（如有要求）

### 步骤 2: 创建工作目录

```bash
mkdir -p ~/papers/<研究主题>/{core-papers,cited-papers,output}
```

创建文献清单文件：
- `PAPER_LIST.md` - 论文列表
- `PAPER_SUMMARIES.md` - 论文摘要
- `references.bib` - BibTeX 引用格式

### 步骤 3: 论文搜索

#### 3.1 使用 arxiv-search (优先)

```bash
# 安装的 arxiv-search 技能位置
ls ~/.agents/skills/arxiv-search/
```

如果 arxiv-search 可用，使用它进行搜索：
- 调用其搜索 API 或脚本
- 获取更精准的论文匹配

#### 3.2 使用 web_fetch 备选

```
https://arxiv.org/search/?searchtype=all&query=<关键词>&start=0
```

### 步骤 4: 下载论文

```bash
# 下载 PDF
wget -q "https://arxiv.org/pdf/<arXiv_ID>" -O "<标题缩写>_<arXiv_ID>.pdf"

# 示例
wget -q "https://arxiv.org/pdf/2309.15817" -O "lm_agents_risks_2309.15817.pdf"
```

### 步骤 5: PDF 解析 (使用 docling)

#### 5.1 安装 docling

```bash
npx skills add existential-birds/beagle@docling -g -y
```

#### 5.2 解析论文

使用 docling 提取论文关键信息：
- 标题、作者、机构
- 摘要
- 方法
- 实验结果
- 结论
- 参考文献

```python
# docling 使用示例
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("paper.pdf")
# 提取结构化信息
```

### 步骤 6: 生成结构化摘要

为每篇论文创建摘要模板：

```markdown
### <论文标题>
- **作者**: Authors
- **arXiv**: [ID](https://arxiv.org/abs/ID)
- **日期**: YYYY-MM
- **核心贡献**: 
  1. 贡献点1
  2. 贡献点2
- **方法**: 
- **实验结果**: 
- **链接**: [PDF](./path/to/file.pdf)
- **BibTeX**:
```bibtex
@article{...}
```
```

### 步骤 7: 引用追踪 (Google Scholar)

1. 访问 Google Scholar 搜索核心论文
2. 获取 "Cited by" 列表
3. 筛选与研究主题相关的引用论文
4. 下载高相关度论文

```bash
# 搜索引用论文
# 使用 web_fetch 访问 Google Scholar
```

### 步骤 8: 自动化筛选评分

#### 8.1 关键词匹配评分

```python
def relevance_score(title, abstract, keywords):
    score = 0
    for kw in keywords:
        if kw.lower() in title.lower():
            score += 3
        if kw.lower() in abstract.lower():
            score += 1
    return score
```

#### 8.2 排序和过滤

- 按相关性分数降序排列
- 过滤低于阈值的论文
- 优先选择高引用量论文

### 步骤 9: 输出格式生成

#### 9.1 文献列表 (PAPER_LIST.md)

```markdown
| # | 论文标题 | arXiv ID | 相关度 | 日期 | 类型 |
|---|----------|----------|--------|------|------|
| 1 | Title | xxxx.xxxxx | ★★★★★ | 2024 | 核心 |
```

#### 9.2 BibTeX (references.bib)

```bibtex
@article{ruan2023toolemu,
  title={Identifying the Risks of LM Agents with an LM-Emulated Sandbox},
  author={Ruan, Yangjun and Dong, Honghua and Wang, Andrew and others},
  journal={arXiv preprint arXiv:2309.15817},
  year={2023}
}
```

#### 9.3 文献综述大纲

```markdown
# <研究主题> 文献综述

## 1. 引言
## 2. 背景与相关工作
## 3. 核心文献分析
## 4. 最新研究进展
## 5. 未来研究方向
```

## 已集成 Skills

| Skill | 用途 |
|-------|------|
| arxiv-search | 专业 arXiv 论文搜索 |
| docling | PDF 解析和信息提取 |
| academic-researcher | 学术研究工作流 |
| latex-paper-en | 论文格式模板 |

## 常用搜索查询

### arXiv 搜索
- 基础：`https://arxiv.org/search/?searchtype=all&query=<关键词>&start=0`
- 日期过滤：`https://arxiv.org/search/?searchtype=all&query=<关键词>&date-filter_by=all_dates&size=50`

### 会议论文
- ICLR: https://openreview.net/group?id=ICLR.cc/2025/Conference
- NeurIPS: https://proceedings.neurips.cc/
- ICML: https://proceedings.mlr.press/

### Google Scholar
- 引用追踪：访问论文主页查看 "Cited by"

## 注意事项

1. **时间筛选**：默认要求 2023-2026 年的论文
2. **去重**：下载前检查是否已存在相同 arXiv ID 的论文
3. **增量更新**：已有文献库时，仅搜索新增论文
4. **来源说明**：大多数顶会论文会先在 arXiv 预发布
5. **版权**：仅下载用于研究，仅提供摘要和下载链接

## 输出文件清单

| 文件 | 说明 |
|------|------|
| `core-papers/` | 核心文献 PDF |
| `cited-papers/` | 引用文献 PDF |
| `PAPER_LIST.md` | 论文清单 |
| `PAPER_SUMMARIES.md` | 结构化摘要 |
| `references.bib` | BibTeX 引用 |
| `literature_review.md` | 文献综述大纲 (可选) |

## 关键词相关性打分

### 使用脚本

本技能包含 `scripts/score_papers.py` 用于关键词相关性打分。

#### 安装依赖

```bash
pip install scikit-learn rapidfuzz
```

#### 基本用法

```bash
# 单一论文打分
python3 scripts/score_papers.py \
    --keywords "agent,LLM,security,prompt injection" \
    --title "Identifying the Risks of LM Agents with an LM-Emulated Sandbox" \
    --abstract "Recent advances in Language Model (LM) agents..."

# 批量打分 (CSV 格式)
python3 scripts/score_papers.py \
    --keywords "agent,LLM,security" \
    --papers paper_list.csv \
    --output results.json

# 自定义权重
python3 scripts/score_papers.py \
    --keywords "agent,defense" \
    --title "xxx" \
    --abstract "xxx" \
    --title-weight 0.7 \
    --abstract-weight 0.3
```

#### CSV 格式要求

```csv
title,abstract,arxiv_id,year
论文标题,论文摘要,2309.15817,2023
...
```

### 打分算法

#### 1. 模糊匹配 (Fuzzy Matching)
- **部分匹配 (partial_ratio)**: 关键词在文本中的部分匹配程度
- **词序无关匹配 (token_sort_ratio)**: 忽略词序的匹配程度
- **集合匹配 (token_set_ratio)**: 关键词集合与文本的交集比例

#### 2. TF-IDF 余弦相似度
- 将论文文本和关键词转换为 TF-IDF 向量
- 计算余弦相似度

#### 3. 加权组合
```
最终分数 = 0.6 × 模糊匹配分 + 0.4 × TF-IDF分数
标题权重 = 0.6 (可调整)
摘要权重 = 0.4 (可调整)
```

#### 输出示例

```
================================================================================
arXiv ID        年份   最终分    标题                                        
================================================================================
2309.15817      2023   0.8523   Identifying the Risks of LM Agents...       
2403.14771      2024   0.7832   InjecAgent: Benchmarking Indirect...        
...
================================================================================
匹配关键词统计:
  agent: 15
  LLM: 12
  security: 8
```

### 集成到工作流

在步骤 8 (自动化筛选评分) 中使用：

```bash
# 1. 生成 CSV
echo "title,abstract,arxiv_id,year" > paper_list.csv
# ... 添加论文信息 ...

# 2. 打分排序
python3 scripts/score_papers.py \
    --keywords "agent,prompt injection,defense" \
    --papers paper_list.csv \
    --output scored_papers.json

# 3. 筛选高分论文 (分数 > 0.6)
jq '.[] | select(.final_score > 0.6)' scored_papers.json
```
