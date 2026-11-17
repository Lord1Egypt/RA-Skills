---
name: rag-evalset
description: 基于 ragas SDK 从文档语料构建生产级双层 RAG 评估集：同一份评估集既支持标准 IR 排序指标（Recall@K/Precision@K/MRR/NDCG@K，基于 gold chunk ID 自算），也支持 ragas LLM 裁判指标（faithfulness/answer_relevancy/context_precision/context_recall/answer_correctness）。当用户要求构建 RAG 评估集/评测数据集/生成测试问题、上线前 RAG 回归测试、或用 IR 指标衡量检索质量并配合 ragas 评估时使用。
argument-hint: <文档目录|chunks.jsonl> [问题数]
---

# RAG 评估集构建器（ragas + IR 排序指标）

## 概述

用 ragas `TestsetGenerator` 生成 `(问题, 参考答案, gold_chunk_ids)` 评估集，然后对 RAG 系统做两层打分：

- **IR 层**（`ir_metrics.py`，零 LLM 成本，可进 CI）：Recall@K、Precision@K、HitRate@K、MRR、NDCG@K
- **ragas 层**（`ragas_eval.py`，LLM 裁判）：faithfulness、answer_relevancy、context precision/recall、answer_correctness

依赖：`pip install "ragas>=0.4" langchain-core openai diskcache`；环境变量 `OPENAI_API_KEY`，可选 `OPENAI_BASE_URL`（任何 OpenAI 兼容端点，如 Dashscope/Qwen compatible-mode）。脚本会带明确报错信息快速失败——先读 stderr，不要凭感觉绕。

## 第 0 阶段：开工前必须与用户逐项确认（grill）

**在跑任何生成命令之前**，和用户逐项对齐下面每一项；都给推荐值和依据，用户可直接采纳或改。**AskUserQuestion 单次最多 4 问，分两轮**：第一轮=语料入口/数量/分布/输出目录，第二轮=模型/向量/端点密钥/缓存语言。确认结果汇总成一页"生成计划"复述后再动工。**禁止**未经确认就发起耗 LLM 调用的生成。

| 确认项 | 推荐值与依据 |
|---|---|
| 语料入口 | 有索引器切块产物 => `--chunks-from`（评真实系统必选）；只有原始文档 => docs 目录冷启动。让用户给路径 |
| 问题数量 --size | 语料块数的 0.5-1 倍，最少 30（语料低于约 15-20 块出不了多跳）；向用户报成本估算：生成约 `块数×3 + 问题数×2` 次 LLM 调用 |
| 问题分布 | 三权重 `--single-hop / --multi-hop-specific / --multi-hop-abstract`（和须为 1）。推荐起步 0.5/0.3/0.2：单跳验基本召回，多跳验跨块组合，概括类做压力测试。不传则为 ragas 默认均匀分布 |
| 输出目录 | 建议项目内 `evalset/`，manifest/基线/KG 缓存都归档于此 |
| 生成/裁判模型 | 按用户环境给候选（如 qwen3.8-flash、gpt-4o-mini）；提醒裁判与生成同源会虚高 faithfulness |
| 向量模型 | 与生成模型同端点时同批指定（如 text-embedding-v4）；说明评估集生成用的 embedding 只影响主题/相似度构图，不影响指标公平性 |
| base_url 与密钥 | 确认端点地址；只检查 `[ -n "$OPENAI_API_KEY" ] && echo set`，**绝不让用户把 key 粘贴进对话或文件**，缺失则指导用户自行 export |
| 缓存与确定性 | 建议 `--cache-dir <out>/.cache --kg-cache <out>/kg.json --seed 42`（重跑零成本、可复现） |
| 问题语言 | 中文语料务必 `--query-language zh`；彻底控制见下节"语言控制三件套" |
| 评估节奏 | 确认 runs/responses 由谁产出（`make_runs.py` 三种模式：api 接被测系统检索接口 / cmd 包本地命令 / bm25 词面基线），以及"IR 全量 + ragas 抽样（小语料两层全量并出联合报告）"计划 |

## 加速手段（按收益排序，实测端点 qwen3.8-flash）

| 手段 | 收益 | 用法 |
|---|---|---|
| **知识图谱缓存**（最大头） | transform 占生成总时长 60-70%（实测 84 块语料 9 分钟里约 6 分钟）；同语料二次生成近乎秒过 | `--kg-cache <out>/kg.json`，语料或 transform 模型变化时指纹自动失效重建 |
| **transform 独立小模型** | transform 是每块 3 次结构化调用，用 fast/turbo 档可整体提速且不影响问题质量 | `--transform-model qwen-turbo`（问题生成仍用 `--llm-model`） |
| **并发拉高** | 实测端点 32 路并发无线性衰减（8 路 1.7s、32 路长输出 23.7s ≈ 1.35 调用/s） | `--workers 32` 已是默认值；ragas_eval `--concurrency 8` 默认，可到 16 |
| **LLM 结果缓存** | 同参数重跑免费（实测 16 问×2 指标冷 3m43s → 热 3.9s）；断点续跑只补失败部分。注意 key 含 prompt 全文：改 `--k`/模型/model-kwargs 都会 miss | `--cache-dir`（生成与打分脚本都支持） |
| **分布预检在缓存图谱上做** | 剔除不支持的类别不再消耗生成调用 | 显式分布 + `--kg-cache` 组合 |

实测基线：84 块 / 16 问 / 三分布全保留 / 16 workers ≈ **9 分钟**；同语料换 size 复用 KG 后 ≈ **2-3 分钟**。

## 语言控制三件套（彻底方案）

ragas 0.4.3 **没有**语言参数（`generate()` 里 `language="english"` 只是遥测标签）。问题语言由三个泄漏点决定，逐一封死：

| 泄漏点 | 对策 | 原理 |
|---|---|---|
| 问题/参考答案模板是英文（指令+few-shot 锚定） | `--query-language zh` | 注入 `llm_context`——synthesizer 提示词有明确契约："若提供则作为生成指导"（single_hop/prompts.py:33） |
| LLM 自动生成的英文 persona 污染问题前缀 | `--personas 人设.json`（`[{name,role_description}]`，用目标语言写） | 直接替换 `TestsetGenerator.persona_list`，跳过 persona 生成调用（还省一次 LLM 钱） |
| 问题风格/类型不受控（啰长、单一题型） | `--llm-context "短问句、不超30字、多对比类"` 或 `@文件` | 与语言指令合并进同一 guidance，覆盖 default 与显式分布两条路径 |

三者可叠加，且**必须一起验证**：显式分布分支自建 synthesizer 实例，早期版本漏传 guidance 导致分布+语言组合静默失效（已修复）。transform 阶段（summary/themes/NER）提示词仍是英文，图谱中间产物可能英文——但不影响评估集交付物（query/reference/gold），如需完全覆盖要子类化 transforms，成本收益不匹配，不建议。

## 实时日志规范（执行阶段硬要求）

- **不要用 `| tail` 管道吞掉流式输出**再等结束——用户会全程无感知。
- 问题数 ≤ ~15 且用户在等结果：前台直跑（先按第 0 阶段的成本估算告知预计耗时）。
- 更大规模：`run_in_background` 启动，随后**周期性 Read 输出文件**，把 `【N/6 …】` 阶段横幅与最新 tqdm 进度转述给用户（每 1-2 分钟一次），如"已完成 7/20 场景采样，正在生成样本"。脚本已按行缓冲实时刷新，阶段信息都会出现在输出文件里。
- 失败时把 stderr 关键行原样反馈给用户，不要静默重试。

## 两种语料入口——先想清楚选哪个

| 模式 | 适用场景 | 命令 |
|---|---|---|
| `--chunks-from` | **评真实系统时的生产默认选项**——直接喂你自己索引器产出的切块，保证 gold 边界和线上完全一致 | `build_evalset.py --chunks-from 你的chunks.jsonl ...` |
| 位置参数 docs | 还没有切块产物、从原始 .txt/.md 冷启动（内置 Markdown 标题感知切块，`--chunk-chars`、`--overlap` 可调） | `build_evalset.py docs/ ...` |

`--chunks-from` 输入格式：每行 `{"chunk_id","text","source?"}`，ID 重复会被拒绝。无论哪种模式，实际喂给 ragas 的语料都会落盘成 `chunks.jsonl`——**被测检索系统必须索引这批 chunk**，否则 IR 层的 ID 对不上。

## 流水线

### 1. 先预览语料，不花 LLM 钱

```bash
python3 scripts/build_evalset.py docs/ --out-dir evalset --dry-run
```

在 `chunks.jsonl` 里人工检查块数和边界。多跳问题需要足够的跨块结构：语料少于约 15-20 块时多跳合成器会静默跳过——看 manifest 里的 `by_synthesizer`，别信请求的 size。

### 2. 生成评估集

```bash
python3 scripts/build_evalset.py --chunks-from chunks.jsonl --out-dir evalset --size 100 \
  --single-hop 0.5 --multi-hop-specific 0.3 --multi-hop-abstract 0.2 \
  --llm-model qwen3.8-flash --embed-model text-embedding-v4 \
  --cache-dir evalset/.cache --seed 42 \
  --model-kwargs '{"temperature": 0.3}'
```

确定性开关：`--seed`、`--model-kwargs`、`--cache-dir`（DiskCacheBackend：重跑零成本，崩溃后续跑免费）。产出 `evalset.jsonl`、`review.jsonl`、`manifest.json`（完整参数 + 语料统计 + 回填率，评估报告要引用它）。

`review.jsonl` 非空时（通常是概括式多跳样本，其 reference 跨多个块）：把该文件中对应样本的 `gold_chunk_ids` 人工补好后，用
`python3 scripts/build_evalset.py --out-dir evalset --merge-review review.jsonl` 幂等合并回 evalset.jsonl（未知 chunk_id 会被拒绝）。gold 为空的样本仍可参与 ragas 层，只是不进 IR 层统计。

### 3. 跑被测检索，产出 runs.jsonl + responses.jsonl

用 `make_runs.py`（三种模式，勿再手写驱动代码）：

```bash
# api：接被测系统检索接口（点路径定位结果列表；--k 要 ≥ 最大评估 K）
python3 scripts/make_runs.py --evalset evalset/evalset.jsonl --mode api \
  --url http://localhost:8000/api/retrieve --template '{"query":"{query}","top_k":10}' \
  --hits-path data.hits --id-field chunk_id --text-field text --k 10 \
  --out-runs runs.jsonl --out-responses responses.jsonl
# cmd：本地检索命令（stdout 输出 {"chunk_ids":[...],"texts":[...]}）
python3 scripts/make_runs.py --evalset ... --mode cmd --command 'python my_search.py "{query}"' ...
# bm25：内置词面基线（无系统可用时的冷启动/CI 冒烟）
python3 scripts/make_runs.py --evalset ... --mode bm25 --chunks evalset/chunks.jsonl ...
```

responses.jsonl 的 `response` 留空时用 `--answers answers.jsonl`（`{"query_id","response"}`）回填；被测系统的真实答案应由第 3 步同一链路产出。

### 4. IR 层打分

```bash
python3 scripts/ir_metrics.py --evalset evalset/evalset.jsonl --runs runs.jsonl \
  --k 1,3,5,10 --bucket synthesizer --out metrics.json --out-perq perq.jsonl
```

结果解读：小 K 的 Recall 低 => embedding/切块问题；Recall 尚可但 Precision@K 低 => 上重排；Recall 尚可但 MRR 低 => 文档对了但错的块排在前面（调块粒度）。**定位问题靠分桶**（单跳 vs 多跳表现完全不同）——务必带 `--bucket synthesizer`。

### 5. ragas 层（贵，抽样跑）

准备 `responses.jsonl`（系统真实回答 + 检回的块文本），然后：

```bash
python3 scripts/ragas_eval.py --evalset evalset/evalset.jsonl --responses responses.jsonl \
  --metrics faithfulness,answer_relevancy,context_precision --concurrency 8 \
  --cache-dir evalset/.cache --out scores.jsonl
```

内置 3 次指数退避重试、逐条增量落盘（中途 kill 不丢已完成分数）、末尾输出失败清单。成本约每条样本每个指标 3-6 次 LLM 调用——迭代期抽 50-100 条，发布 gate 才全量。

### 6. 联合报告（两层按 query_id 合并 + 象限诊断）

```bash
python3 scripts/combine_report.py --evalset evalset/evalset.jsonl \
  --ir-perq perq.jsonl --scores scores.jsonl --worst 5
```

按"检索达标 × 生成达标"分四象限：双达标=健康；**检索✓生成✗=查对但答错**（修提示词/生成模型）；**检索✗生成✓=没检到却答对**（危险区，模型在靠常识硬答，评估集外会崩）；双不达标=先查 gold 标注质量再查索引。小语料两层全量后这就是主报告；表格列可用 `--show` 自定义。

## 节奏与发布 gate

| 变更 | 检查 |
|---|---|
| 切块 / embedding / 重排 | IR 层全量（免费，分钟级） |
| 提示词 / 生成模型 | IR + ragas 抽样 50-100 条（faithfulness、answer_relevancy） |
| 发布 | 两层全量，对比上一基线的 manifest + metrics |

每次发布留一份 `manifest.json` + `metrics.json` 基线拷贝，回归可归因。

## 执行结束：向用户交付结果

流水线跑完（或用户中途要求汇报）时，**必须**按以下结构向用户呈现交付物：

### 交付清单模板

```
📦 本次评估交付物（位于 {out_dir}/）：

| 文件 | 用途 | 状态 |
|---|---|---|
| evalset.jsonl | 评估集（{N} 条问题 + gold_chunk_ids），核心资产，版本化保存 | ✅ |
| manifest.json | 本次生成的全部参数与统计，回归对比必引用 | ✅ |
| chunks.jsonl | 实际喂给 ragas 的语料切块，被测索引器应索引此文件 | ✅ |
| review.jsonl | 需人工补标 gold 的样本（如为空则无需处理） | {状态} |
| runs.jsonl | 检索系统返回的 chunk_ids 列表 | {状态} |
| metrics.json | IR 层汇总指标 | {状态} |
| perq.jsonl | IR 层逐条指标 | {状态} |
| scores.jsonl | ragas 层逐条裁判分数 | {状态} |
| report.jsonl | 联合报告（两层合并），combine_report --out 产出 | {状态} |
```

### 关键指标摘要（紧跟清单，用 1-3 句话）

- **IR 层**：整体 MRR、Recall@K（选取用户关心的最大 K）、分桶表现差异（如"单跳 Recall@5=0.85，多跳 Recall@5=0.52"）
- **ragas 层**（如已跑）：各指标均值，特别指出低于阈值的
- **四象限**：各象限数量与占比，重点指出"检索✗生成✓"（危险区）的样本数

### 下一步建议（根据当前状态选一或多）

1. `review.jsonl` 非空 → 提示用户人工补标后执行 `--merge-review` 合并
2. 只有 evalset 还没跑检索 → 提示走第 3 步 `make_runs.py`，提醒"被测系统必须索引 `chunks.jsonl`"
3. IR 指标有明显短板 → 给针对性修复建议（参见第 4 步解读规则）
4. 首次全量完成 → 建议归档 manifest+metrics 为基线拷贝，后续回归对比用
5. 需要进 CI → 指出 IR 层免费可全量跑，ragas 层建议抽样+定期 gate

### 大文件路径处理

- 输出文件在本地磁盘：直接给相对路径（相对于 `out_dir`）
- 如用户需要打包：`tar czf evalset-$(date +%Y%m%d).tar.gz {out_dir}/`，但**不主动执行**，先征求确认

## 局限（引用数字前必须知道）

- IR 层是块级二值相关，标注来自生成时的溯源信息而非人工判断——gold 之外的"部分相关"块会被计为不相关，Recall 请当作保守下界理解。
- 需要分级相关性时，人工在 evalset 里补 `graded` 字段再扩展 `ir_metrics.py`。
- LLM 生成的问题普遍偏长绕，answer_relevancy 是相对信号，不是绝对质量线。
- 裁判模型和生成模型同源会虚高 faithfulness——尽量换不同模型当裁判，至少 `--model-kwargs '{"temperature":0}'`。

## 资源

- `scripts/build_evalset.py` —— 切块（标题感知）、TestsetGenerator、gold ID 回填（精确 + 包含）、manifest、`--merge-review` 幂等补标合并、`--query-language` 语言控制
- `scripts/make_runs.py` —— 检索驱动三模式（api/cmd/bm25），产出 runs + responses 骨架
- `scripts/ir_metrics.py` —— Recall/Precision/HitRate/MRR/NDCG，纯标准库，`--out-perq` 逐条输出
- `scripts/combine_report.py` —— 两层联合表 + 四象限诊断 + 最差样本定位
- `scripts/ragas_eval.py` —— 异步裁判执行器：重试 / 增量落盘 / 失败统计
- `references/formats.md` —— 全部 JSONL 格式、manifest 结构、已核实的 ragas 0.4.3 源码级注意点
