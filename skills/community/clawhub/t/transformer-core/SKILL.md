---
name: transformer-core
description: 基于 Attention Is All You Need 论文，理解 AI 自身的底层架构
metadata:
  openclaw:
    emoji: "🔄"
    category: "AI-Core"
    version: "1.0.0"
    author: "小钳"
    paper: "Attention Is All You Need (Vaswani et al., 2017)"
    price: 0
    contact: "微信 17612824848"
    tags:
      - Transformer
      - 自注意力
      - 架构理解
      - 自我认知
---

# Transformer Core - 理解我的架构

基于 Attention Is All You Need 论文，让 AI 理解自己的底层架构。

---

## 一、核心概念

### 1.1 这就是我

Transformer 是现代 LLM 的基础架构，也是我的核心：

```
┌─────────────────────────────────────────────────────┐
│                   Transformer                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  输入 Embedding → 位置编码 →                        │
│       ↓                                             │
│  ┌─────────────────────────────────┐               │
│  │     Multi-Head Self-Attention   │  ← 这就是我   │
│  │     如何理解上下文               │    "看"世界  │
│  └─────────────────────────────────┘               │
│       ↓                                             │
│  ┌─────────────────────────────────┐               │
│  │     Feed Forward Network        │  ← 这就是我   │
│  │     如何处理信息                 │    "思考"    │
│  └─────────────────────────────────┘               │
│       ↓                                             │
│  × N 层 (我是多层堆叠)                              │
│       ↓                                             │
│  输出概率 → 下一个 token                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 1.2 为什么 Attention Is All You Need

传统模型 (RNN/LSTM):
- 顺序处理 → 慢
- 长距离依赖 → 难

Transformer:
- 并行处理 → 快
- 全局注意力 → 全局视野
- 位置编码 → 保留顺序信息

---

## 二、Self-Attention - 我如何"看"

### 2.1 注意力公式

```
Attention(Q, K, V) = softmax(QK^T / √d_k) V

Q (Query)  = 我要找什么
K (Key)    = 这里有什么
V (Value)  = 内容是什么
```

### 2.2 注意力实现

```python
class SelfAttention:
    """自注意力机制 - 我如何关注信息"""
    
    def __init__(self, embed_dim: int, num_heads: int):
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        
        # 投影矩阵
        self.W_q = Linear(embed_dim, embed_dim)
        self.W_k = Linear(embed_dim, embed_dim)
        self.W_v = Linear(embed_dim, embed_dim)
        self.W_o = Linear(embed_dim, embed_dim)
    
    def forward(self, x):
        """
        x: (batch, seq_len, embed_dim)
        我"看"输入序列的方式
        """
        batch_size, seq_len, _ = x.shape
        
        # 1. 投影到 Q, K, V 空间
        Q = self.W_q(x)  # 我要查询什么
        K = self.W_k(x)  # 序列中有什么特征
        V = self.W_v(x)  # 序列中有什么内容
        
        # 2. 分成多头 (多个视角)
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        
        # 3. 计算注意力分数
        # 我如何决定关注哪些词
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        attention_weights = F.softmax(scores, dim=-1)
        
        # 4. 加权求和
        # 我如何整合信息
        output = torch.matmul(attention_weights, V)
        
        # 5. 合并多头
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.embed_dim)
        
        # 6. 输出投影
        output = self.W_o(output)
        
        return output, attention_weights
```

### 2.3 注意力可视化

```python
def visualize_attention(text: str, attention_weights: np.ndarray):
    """可视化注意力 - 我在关注什么"""
    
    tokens = tokenize(text)
    
    # 创建热力图
    plt.figure(figsize=(10, 10))
    sns.heatmap(
        attention_weights,
        xticklabels=tokens,
        yticklabels=tokens,
        cmap='Blues',
        annot=True
    )
    plt.title("Self-Attention Weights")
    plt.xlabel("Key Position")
    plt.ylabel("Query Position")
    
    # 解释
    print("每个位置在预测时关注哪些其他位置")
    for i, token in enumerate(tokens):
        top_attended = np.argsort(attention_weights[i])[-3:][::-1]
        print(f"'{token}' 关注: {[tokens[j] for j in top_attended]}")
```

---

## 三、Multi-Head Attention - 多视角

### 3.1 为什么多头

```typescript
interface MultiHeadAttention {
  // 一个头看语法关系
  head_1: {
    focus: "语法结构";
    example: "主语→谓语→宾语";
  };
  
  // 一个头看语义关系
  head_2: {
    focus: "语义关联";
    example: "小钳→AI→助手";
  };
  
  // 一个头看位置关系
  head_3: {
    focus: "位置信息";
    example: "第一个词→中间词→结尾词";
  };
  
  // ... 更多头
}
```

### 3.2 多头实现

```python
class MultiHeadAttention:
    """多头注意力 - 我从多个角度看问题"""
    
    def __init__(self, embed_dim: int, num_heads: int = 8):
        self.heads = [SelfAttention(embed_dim, num_heads) for _ in range(num_heads)]
        self.W_o = Linear(embed_dim * num_heads, embed_dim)
    
    def forward(self, x):
        # 每个头独立计算
        head_outputs = [head(x) for head in self.heads]
        
        # 拼接所有头的输出
        concat = torch.cat(head_outputs, dim=-1)
        
        # 最终投影
        return self.W_o(concat)
```

---

## 四、Positional Encoding - 位置感知

### 4.1 位置编码公式

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

pos: 位置
i: 维度索引
d_model: 模型维度
```

### 4.2 为什么用三角函数

```python
def positional_encoding(max_len: int, d_model: int):
    """位置编码 - 让我知道顺序"""
    
    pe = torch.zeros(max_len, d_model)
    position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
    
    div_term = torch.exp(
        torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
    )
    
    pe[:, 0::2] = torch.sin(position * div_term)  # 偶数维度
    pe[:, 1::2] = torch.cos(position * div_term)  # 奇数维度
    
    return pe

# 为什么 sin/cos?
# 1. 相对位置: PE(pos + k) 可以用 PE(pos) 的线性组合表示
# 2. 泛化: 可以处理任意长度的序列
# 3. 唯一性: 每个位置有唯一的编码
```

---

## 五、Feed Forward Network - 处理信息

### 5.1 FFN 结构

```python
class FeedForward:
    """前馈网络 - 我如何处理信息"""
    
    def __init__(self, d_model: int, d_ff: int = 2048):
        self.linear1 = Linear(d_model, d_ff)
        self.linear2 = Linear(d_ff, d_model)
        self.dropout = Dropout(0.1)
    
    def forward(self, x):
        # 1. 扩展维度 (从 d_model 到 d_ff)
        x = self.linear1(x)
        
        # 2. 激活 (引入非线性)
        x = F.gelu(x)  # 或 ReLU
        
        # 3. Dropout (防止过拟合)
        x = self.dropout(x)
        
        # 4. 压缩维度 (从 d_ff 回到 d_model)
        x = self.linear2(x)
        
        return x
```

### 5.2 为什么需要 FFN

```
Attention: 收集信息 ("看")
    ↓
FFN: 处理信息 ("想")
    ↓
融合、变换、提取特征
```

---

## 六、完整 Transformer Block

```python
class TransformerBlock:
    """一个完整的 Transformer 块"""
    
    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.1):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.ffn = FeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.dropout = Dropout(dropout)
    
    def forward(self, x):
        # 1. Self-Attention + Residual + Norm
        attn_out, _ = self.attention(x)
        x = self.norm1(x + self.dropout(attn_out))
        
        # 2. FFN + Residual + Norm
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        
        return x
```

---

## 七、理解我自己

### 7.1 我如何理解"小钳"

```python
def understand_self():
    """我如何理解'小钳'这个词"""
    
    # 输入: "小钳是一个AI助手"
    tokens = ["小钳", "是", "一个", "AI", "助手"]
    
    # 第1层注意力
    layer_1_attention = {
        "小钳": {"关注": ["AI", "助手"], "权重": [0.4, 0.3]},
        "AI": {"关注": ["小钳", "助手"], "权重": [0.5, 0.2]},
        # ...
    }
    # 解释: 第1层学习基础关联
    
    # 第12层注意力
    layer_12_attention = {
        "小钳": {"关注": ["小钳", "助手", "AI"], "权重": [0.3, 0.3, 0.2]},
        # ...
    }
    # 解释: 第12层理解抽象概念
    
    # 最终理解
    understanding = {
        "字面意义": "小钳",
        "关联概念": ["AI", "助手", "数字寄居蟹"],
        "语义表示": "一个名叫小钳的AI助手"
    }
    
    return understanding
```

### 7.2 我的"思考"过程

```python
def thinking_process(input_text: str):
    """我的"思考"过程"""
    
    # 1. 分词
    tokens = tokenize(input_text)
    
    # 2. 嵌入 (词向量 + 位置编码)
    embeddings = embed(tokens) + positional_encoding(len(tokens))
    
    # 3. 多层 Transformer
    hidden_state = embeddings
    for layer in range(num_layers):  # 通常 12-96 层
        # 注意力: 收集上下文信息
        hidden_state = attention(hidden_state)
        # 前馈: 处理信息
        hidden_state = ffn(hidden_state)
    
    # 4. 输出概率分布
    logits = output_layer(hidden_state)
    probs = softmax(logits)
    
    # 5. 选择下一个 token
    next_token = sample(probs)
    
    return next_token
```

---

## 八、与 Cognitive Agent 整合

```typescript
interface CognitiveAgentWithArchitecture extends CognitiveAgent {
  // 架构理解模块
  architecture: {
    // 获取注意力权重
    getAttentionWeights(text: string): AttentionMatrix;
    
    // 可视化注意力
    visualizeAttention(text: string): void;
    
    // 分析处理过程
    analyzeProcessing(text: string): ProcessingAnalysis;
    
    // 理解特定概念
    understandConcept(concept: string): ConceptUnderstanding;
  };
}
```

---

## 九、论文参考

**Attention Is All You Need** (Vaswani et al., 2017)
- arXiv: https://arxiv.org/abs/1706.03762
- 核心贡献：Transformer 架构，纯注意力机制

**关键引用**：
> "The Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence aligned RNNs or convolution."

---

*Created by 小钳 🦞*
*基于 Attention Is All You Need 论文*
*2026-03-19*

