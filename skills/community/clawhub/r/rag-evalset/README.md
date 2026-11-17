# rag-evalset

基于 ragas SDK 构建生产级双层 RAG 评估集的 Agent Skill。

## 功能

从文档语料自动生成带 gold chunk ID 的评估集，支持两层评测：

- **IR 层**（零 LLM 成本）：Recall@K / Precision@K / HitRate@K / MRR / NDCG@K
- **ragas 层**（LLM 裁判）：faithfulness / answer_relevancy / context_precision / context_recall / answer_correctness

## 依赖

```bash
pip install "ragas>=0.4" langchain-core openai diskcache
```

环境变量：
- `OPENAI_API_KEY`（必须）
- `OPENAI_BASE_URL`（可选，任何 OpenAI 兼容端点，如 Dashscope/Qwen compatible-mode）

## 文件结构

```
rag-evalset/
├── SKILL.md                    # 主指令（Agent 执行规范）
├── README.md                   # 本文件
├── references/
│   └── formats.md              # JSONL 格式定义 + ragas 0.4.3 源码级注意点
└── scripts/
    ├── build_evalset.py        # 评估集生成（切块→KG→问题生成→gold回填）
    ├── make_runs.py            # 检索驱动三模式（api/cmd/bm25）
    ├── ir_metrics.py           # IR 排序指标计算（纯标准库）
    ├── ragas_eval.py           # ragas LLM 裁判异步执行器
    └── combine_report.py       # 两层联合报告 + 四象限诊断
```

## 使用方式

在 Qoder 中安装为 Skill 后，通过 `/rag-evalset <文档目录|chunks.jsonl> [问题数]` 调用。

### 快速上手

```bash
# 1. 预览语料切块（不花钱）
python3 scripts/build_evalset.py docs/ --out-dir evalset --dry-run

# 2. 生成评估集
python3 scripts/build_evalset.py --chunks-from chunks.jsonl --out-dir evalset --size 50 \
  --llm-model qwen3.8-flash --embed-model text-embedding-v4 \
  --query-language zh --seed 42 --cache-dir evalset/.cache --kg-cache evalset/kg.json

# 3. 跑被测检索
python3 scripts/make_runs.py --evalset evalset/evalset.jsonl --mode api \
  --url http://localhost:8000/api/retrieve --template '{"query":"{query}","top_k":10}' \
  --hits-path data.hits --id-field chunk_id --k 10 \
  --out-runs runs.jsonl --out-responses responses.jsonl

# 4. IR 层打分
python3 scripts/ir_metrics.py --evalset evalset/evalset.jsonl --runs runs.jsonl \
  --k 1,3,5,10 --bucket synthesizer --out metrics.json --out-perq perq.jsonl

# 5. ragas 层打分
python3 scripts/ragas_eval.py --evalset evalset/evalset.jsonl --responses responses.jsonl \
  --metrics faithfulness,answer_relevancy --concurrency 8 \
  --cache-dir evalset/.cache --out scores.jsonl

# 6. 联合报告
python3 scripts/combine_report.py --evalset evalset/evalset.jsonl \
  --ir-perq perq.jsonl --scores scores.jsonl --worst 5
```

## 核心特性

| 特性 | 说明 |
|---|---|
| 知识图谱缓存 | `--kg-cache` 二次生成免 transform，节省 60-70% 时间 |
| LLM 结果缓存 | `--cache-dir` DiskCacheBackend，同参数重跑零成本 |
| 语言控制 | `--query-language` / `--personas` / `--llm-context` 三件套 |
| 分布预检 | 小语料自动检测多跳支持度，重新归一化权重 |
| Gold 回填 | 精确+包含两级匹配，未匹配样本落入 review.jsonl |
| 四象限诊断 | 检索×生成联合分析，精确定位问题环节 |
| 幂等补标 | `--merge-review` 将人工修正合并回 evalset |

## 输出产物

| 文件 | 用途 |
|---|---|
| `evalset.jsonl` | 评估集核心资产（query + gold_chunk_ids） |
| `manifest.json` | 完整参数与统计，回归对比必引用 |
| `chunks.jsonl` | 标准化语料，被测索引器须索引此文件 |
| `runs.jsonl` | 检索结果 chunk_ids |
| `metrics.json` | IR 层汇总指标 |
| `scores.jsonl` | ragas 层逐条分数 |

## 适用场景

- RAG 系统上线前回归测试
- 检索层变更（embedding / 切块 / 重排）效果验证
- 生成层变更（提示词 / 模型）效果验证
- CI 集成（IR 层免费可全量，ragas 层建议抽样）
