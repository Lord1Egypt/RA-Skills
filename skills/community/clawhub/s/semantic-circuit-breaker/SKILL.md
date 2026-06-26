# Semantic Circuit Breaker

> 语义熔断器：基于内容语义而非错误率的服务保护机制。

## 何时使用
- API返回"正确格式但错误语义"的响应（如AI幻觉）
- 需要保护下游服务免受语义漂移影响
- LLM API的质量保障层

## 核心认知

### 1. 传统熔断看状态码，语义熔断看内容
传统Circuit Breaker基于HTTP状态码和超时率。但当LLM API返回200但内容是幻觉、偏见、或语义偏移时，传统熔断完全无效。

**语义熔断触发条件**：
- **语义漂移**：连续N个响应的语义embedding偏离历史基线超过阈值
- **一致性断裂**：对同一问题的多次回答语义差异过大
- **事实性崩塌**：响应中可验证事实的错误率超过阈值
- **毒性飙升**：响应中的有害内容评分突增

### 2. 三态模型（扩展传统熔断）
- **Closed（正常）**：语义质量在基线范围内，请求正常通过
- **Open（熔断）**：语义质量严重偏离，请求被拦截并返回降级响应
- **Half-Open（探测）**：定期发送探测请求，评估语义质量是否恢复

区别：转换条件不是"错误率"而是"语义距离"。

### 3. 语义距离计算
```python
def semantic_distance(responses, baseline):
    """计算响应集合与基线的语义距离"""
    embeddings = embed(responses)  # 句向量
    baseline_emb = embed(baseline)
    
    # 余弦距离
    cosine_dist = 1 - cosine_similarity(embeddings.mean(axis=0), baseline_emb.mean(axis=0))
    
    # 方差（一致性）
    variance = embeddings.std(axis=0).mean()
    
    # 事实性（与知识库比对）
    factuality = verify_against_kb(responses)
    
    return 0.4 * cosine_dist + 0.3 * variance + 0.3 * (1 - factuality)
```

## 碰撞来源
- `circuit-breaker-pattern` × `semantic-diff-engine` × `llm-output-validator`
- `semantic-cache-layer`（语义计算）× `adaptive-circuit-breaker`（自适应熔断）
