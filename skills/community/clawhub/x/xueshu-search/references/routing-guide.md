# Routing Guide — 数据源选择决策

## 快速决策表

| 用户意图 | 推荐源 | 原因 |
|---|---|---|
| "找中文论文/中文文献" | baidu_scholar + crossref | 百度学术中文最强，CrossRef 补 DOI |
| "找几篇关于 X 的论文"（英文） | all | 通用搜索，全源覆盖最广 |
| "最近 X 领域有什么新论文" | arxiv + semantic_scholar | arXiv 最快收录预印本，S2 有引用数据 |
| "X 方向的核心文献有哪些" | semantic_scholar | 有被引次数，可按影响力排序 |
| "医学/生物相关的论文" | pubmed + semantic_scholar | PubMed 是生物医学权威，S2 补充引用 |
| "这篇论文被谁引用了" | semantic_scholar | 唯一支持引用链的源 |
| "这个 DOI 是哪篇论文" | crossref | DOI 权威解析源 |
| "Yann LeCun 发了什么" | semantic_scholar | 唯一支持作者检索的源 |
| "导出 BibTeX" | crossref | 唯一支持 BibTeX 格式的源 |
| "NLP/CV/ML 论文" | arxiv + semantic_scholar | CS 领域 arXiv 覆盖最全 |

## 源选择决策树

```
用户查询
├── 包含 DOI？ → crossref --doi + 可选 --bibtex
├── 包含中文？ → baidu_scholar + crossref（自动检测）
├── 包含作者名 + "论文/发了什么"？ → semantic_scholar --author
├── 包含"引用/被引/citation"？ → semantic_scholar --citations / --references
├── 包含医学/生物/临床关键词？ → pubmed + semantic_scholar
├── 包含 CS/Math/Physics 关键词？ → arxiv + semantic_scholar
└── 其他英文关键词/不确定领域？ → 全部五源并发
```

## 中文自动检测

`search.py` 内置 `_is_chinese_query()` 函数，通过 Unicode 范围 `\u4e00-\u9fff` 检测中文。

- 含中文 → 自动路由 `baidu_scholar + crossref`
- 纯英文 → 按关键词规则选择
- 可通过 `--source` 手动覆盖自动路由

百度学术需设置环境变量：`export BAIDU_QIANFAN_API_KEY="bce-v3/ALTAK-xxx"`。
获取方式：https://console.bce.baidu.com/qianfan/ais/console/apiKey（免费，50次/天）

## 关键词 → 源映射

**中文** → baidu_scholar + crossref（自动）

**生物医学关键词** → pubmed + semantic_scholar
- cancer, tumor, disease, clinical, patient, therapy, drug, gene, protein, cell, immunology, surgery, diagnosis, treatment, vaccine, virus, bacteria, pathology, radiology, anatomy, physiology

**计算机科学关键词** → arxiv + semantic_scholar
- neural network, deep learning, machine learning, NLP, computer vision, reinforcement learning, algorithm, GPU, transformer, LLM, diffusion model, GAN, CNN, RNN, attention mechanism

**物理/数学关键词** → arxiv + semantic_scholar
- quantum, particle, relativity, cosmology, string theory, topology, differential equation, statistical mechanics, condensed matter, astrophysics

**不确定** → 全部五源

## 并发策略

- 中文搜索：baidu_scholar + crossref 两源并发
- 英文搜索：五源并发，每个源最多取 `max(5, max_results/5 + 2)` 条
- 聚合后去重（按 DOI → 标题），保留信息最丰富的版本
- 最终排序：被引次数 desc → 年份 desc
- 超过 `max_results` 的截断
