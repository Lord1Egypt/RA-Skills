# RAG优化快速入门

## 5分钟上手指南

### 第一步：诊断你的RAG问题

使用自查清单：

```python
# 运行诊断
from rag_optimization import diagnose

diagnose.run(
    test_queries=["查询1", "查询2", "查询3"],
    expected_results=[...]
)
```

**输出示例**：
```
诊断报告：
❌ 召回率偏低 (0.45) → 建议使用"由小到大检索"
⚠️ 精确率一般 (0.52) → 建议添加"重排序"
✅ 响应速度正常
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

**最简单的优化（由小到大检索）**：

```python
from rag_optimization import SmallToBigRetriever

# 初始化
retriever = SmallToBigRetriever(
    vector_store=your_vector_store,
    embedding_model=your_embedding_model
)

# 构建索引
retriever.index_documents(your_documents)

# 检索
results = retriever.retrieve("你的查询")
```

**效果**：准确率从 0.30 → 0.85

---

### 第四步：验证效果

```python
from rag_optimization import RAGEvaluator

evaluator = RAGEvaluator()
report = evaluator.evaluate(test_cases)

print(f"召回率提升: {report['recall_improvement']}")
print(f"准确率提升: {report['accuracy_improvement']}")
```

---

## 常见场景模板

### 场景1：企业知识库问答

```python
config = {
    'chunk_strategy': 'small_to_big',
    'retrieval_strategy': 'hybrid',
    'use_rerank': True,
    'use_compression': True,
}
```

### 场景2：法律条文检索

```python
config = {
    'chunk_strategy': 'semantic',  # 保持法条完整性
    'retrieval_strategy': 'hybrid',
    'hybrid_alpha': 0.5,  # 增加关键词权重
    'use_rerank': True,
}
```

### 场景3：学术论文问答

```python
config = {
    'chunk_strategy': 'small_to_big',
    'parent_chunk_size': 800,  # 更大的上下文
    'use_multi_hop': True,  # 支持复杂推理
}
```

---

## 下一步

1. 阅读完整 [skill.md](./skill.md) 了解所有策略细节
2. 参考 [config-template.json](./config-template.json) 配置你的系统
3. 使用 [evaluate.py](./evaluate.py) 建立评估流程

