# RAG优化快速入门

## 5分钟上手指南

> 技能内所有脚本均为**纯标准库实现**，无需安装第三方依赖即可运行；
> 需要 LLM / 向量模型时按 `references/global-operations.md` 自行接入。

### 零、配置 LLM 凭证（可选）

若使用 `.env` 文件管理 API Key（推荐），执行：

```bash
pip install python-dotenv>=1.0   # 一次性安装
# 然后在项目根目录的 .env 中写入 NVIDIA_API_KEY / NVIDIA_API_URL
# evaluate.py 启动时自动加载并桥接到豆包协议
```

无需安装 `python-dotenv` 时，使用 `export` 手动注入环境变量。详见 `references/global-operations.md` 第 1.4 节。

### 第一步：诊断你的RAG问题

建立基准指标是优化的前提。使用 `scripts/evaluate.py`（核心评估 CLI；性能基准测试另有 `scripts/benchmark_retrieval.py --docs N`）：

```bash
# 终端运行（scripts/ 目录下）
python evaluate.py --test-data ../assets/test-cases-example.json --output eval_report.json

# 进阶：接配置装配管道 / 指定你的 RAG 类 / 与旧报告对比（Ablation）
python evaluate.py --test-data ../assets/test-cases-example.json \
    --config ../assets/config-template.json \
    --rag-class my_rag.MyRAGSystem \
    --compare eval_report.json
```

测试用例格式见 `assets/test-cases-example.json`：`query` / `expected_answer` / `expected_doc_ids` / `category` / `difficulty`。

代码方式接入（替换 Mock 为你的 RAG 系统）：

```python
from evaluate import RAGEvaluator

class YourRAG:
    def query(self, q):
        # 返回答案与来源文档
        return {'answer': "...", 'sources': [{'id': 'doc_1', 'text': '...'}]}

evaluator = RAGEvaluator(rag_system=YourRAG())
report = evaluator.evaluate(test_cases)   # test_cases 从 test-cases-example.json 加载
print(report['summary'])
```

**输出示例**：
```
召回率 Recall@5: 0.45  → 建议使用"由小到大检索"
精确率 Precision@5: 0.52 → 建议添加"重排序"
```

---

### 第二步：选择优化策略

根据诊断结果，参考决策树：

```
你的问题 → 推荐策略
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
检索不到内容 → 由小到大检索
检索噪音多 → 混合检索 + 重排序
查询太模糊 → HyDE
答案不完整 → 语义分块
复杂问题 → 多跳检索
```

---

### 第三步：快速实现

**最简单的优化（由小到大检索的分块部分）**：

技能内置 `proposition_chunker.py` 生成"子块（命题）→ 父块（原段落）"映射，检索子块、返回父块：

```python
from proposition_chunker import PropositionChunker

chunker = PropositionChunker()
chunks = chunker.chunk(document_text)

for prop in chunks[:5]:
    print(prop.content)                    # 子块（命题，用于向量索引）
    print(prop.parent_paragraph)           # 父块（原段落，用于返回给LLM）
```

检索侧需接入你的向量库：用子块向量检索 top-K，再映射回父块。

**效果**：由小到大检索可将准确率从 0.30 提升到 0.85（社区基准）。

---

### 第四步：验证效果

```python
from evaluate import RAGEvaluator

evaluator = RAGEvaluator(rag_system=YourRAG())   # 必须传入实现了 query(q) 的 RAG 系统
report = evaluator.evaluate(test_cases)

# 报告包含：检索指标(recall/precision/MRR)、生成质量、性能、分类&难度分析
print(report['summary'])
```

**关键实践**：优化前后各跑一次评估，用同一份测试集对比指标，判断策略是否真正有效。


**进阶功能（新增）**：

以下功能已实现，可直接使用：

- **HyDE 查询生成**：`from query_transformer import HyDETransformer`，短查询自动生成假设文档用于检索
- **重排序**：`from reranker import Reranker`，两阶段检索精排，无模型时自动回退 BM25
- **统一 LLM 客户端**：`from llm_client import LLMClient, OpenAILikeClient, load_from_env, wrap_llm`，统一 score/generate/classify 接口；`load_from_env()` 读 .env 零配置创建，`wrap_llm()` 归一各类入参（防重试叠套）
- **组合检索**：`from retriever_base import HybridRetriever, VectorRetriever`，`HybridRetriever(left, right, weight=0.7)` 加权融合两路检索结果；注意 `retriever_base.BM25Retriever(k1, b)` 是简化教学版，生产环境请用 `from bm25_retriever import BM25Retriever`（功能完整版，支持 bm25/vector/hybrid 策略与缓存）
- **配置装配**：`from config_loader import load_config, build_pipeline`，校验 config-template.json 并一键实例化组件

**安装**：

```
pip install python-dotenv>=1.0
pip install sentence-transformers>=2.2.0
```

---

## 常见场景模板

以下键名与 `assets/config-template.json` 保持一致，选择对应场景的 `presets` 直接使用：

### 场景1：企业知识库问答

```json
{
  "chunking": { "strategy": "small_to_big" },
  "retrieval": { "strategy": "hybrid" },
  "reranking": { "enabled": true },
  "context_compression": { "enabled": true }
}
```

### 场景2：法律条文检索

```json
{
  "chunking": { "strategy": "semantic" },
  "retrieval": { "strategy": "hybrid", "hybrid_retrieval": { "vector_weight": 0.5 } },
  "reranking": { "enabled": true },
  "citation_tracking": { "enabled": true, "format": "footnote" }
}
```

### 场景3：学术论文问答

```json
{
  "chunking": { "strategy": "small_to_big", "small_to_big": { "parent_chunk_size": 800 } },
  "multi_hop": { "enabled": true },
  "segment_extraction": { "enabled": true }
}
```

---

## 下一步

1. 阅读 [SKILL.md](../SKILL.md) 了解全部 21+ 策略细节
2. 参考 [config-template.json](../assets/config-template.json) 配置你的系统（含 9 个场景预设）
3. 阅读 [advanced-techniques.md](advanced-techniques.md) 查看各策略的完整实现
4. 使用 [evaluate.py](../scripts/evaluate.py) 建立评估流程
