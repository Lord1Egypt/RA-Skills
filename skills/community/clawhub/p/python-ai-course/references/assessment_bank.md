# 摸底考试题库 & 章节练习题规范（2026 行业版）

---

## 第一部分：摸底考试规则

### 核心规范
1. 六大维度调研完成后、正式教学前进行
2. 根据学员等级抽取 **10 题**：选择题 4 + 简答题 4 + 代码题 2
3. 批改输出：评分（x/10）+ 弱项诊断 + 每题逐项解析

### 题库等级对应

| 学员等级 | 题库 | 覆盖领域 |
|----------|------|----------|
| L1 零基础 | 题库 A | Python 基础 + AI 常识 + 逻辑思维 |
| L2 进阶 | 题库 B | Python + ML 基础 + Prompt 基础 + FastAPI |
| L3 实战 | 题库 C | ML/DL + RAG + Agent 基础 + Transformer |
| L4 深耕 | 题库 D | 深度学习进阶 + 微调 + Agent 架构 + 前沿 |

---

## 第二部分：题库 A（L1 零基础）

### 选择题

**A-S01** ⭐ Python 基础
```python
x = [1, 2, 3]
y = x
y.append(4)
print(len(x))
```
A. 3
B. 4
C. 报错
D. 不确定

> **答案：B。** 列表是可变对象，y=x 是引用赋值。y.append(4) 修改了同一个对象，所以 x 长度变为 4。区分「可变对象引用」和「不可变对象」是 Python 的核心考点。

**A-S02** ⭐ AI 基础
AI、ML、DL 的正确包含关系是？
A. AI ⊂ ML ⊂ DL
B. DL ⊂ ML ⊂ AI
C. ML ⊂ AI ⊂ DL
D. 三者并列

> **答案：B。** 深度学习是机器学习的一种方法，机器学习是实现人工智能的一种途径。

**A-S03** ⭐ Python 数据类型
以下哪个操作会原地修改列表 `nums = [3,1,4,2]`？
A. sorted(nums)
B. nums.sort()
C. nums[::-1]
D. max(nums)

> **答案：B。** sort() 原地排序返回 None，sorted() 返回新列表，[::-1] 创建副本。

**A-S04** ⭐ LLM 常识
大语言模型预训练的核心任务是什么？
A. 图像分类
B. 下一个 Token 预测
C. 翻译任务
D. 情感分析

> **答案：B。** GPT 系列的核心预训练任务就是「给定上文，预测下一个词」。

### 简答题

**A-A01** ⭐ 用自己的话解释列表（list）和元组（tuple）的区别和适合场景。

> **答案：** 列表可变（增删改），元组不可变（创建后锁定）。列表适合动态数据集合（购物车），元组适合固定数据（坐标、数据库记录）。元组更轻量，可作为 dict 的 key。

**A-A02** ⭐ 什么是 API？用餐厅类比解释。

> **答案：** API 是软件组件的通信约定。类比：顾客=客户端，厨房=后台，服务员=API。你不需要知道厨房怎么做菜，告诉服务员你要什么即可。菜单=API 文档。

**A-A03** ⭐ 什么是大模型的「幻觉」？举例说明。

> **答案：** LLM 生成看似合理但实际错误的内容。如问「列出某作者 2010 年前全部短篇」，模型可能编造不存在的作品名。原因是 LLM 基于概率生成，不加验证时会「创造」看似合理的信息。

**A-A04** ⭐ 什么是监督学习和无监督学习？各举一个例子。

> **答案：** 监督学习有标注数据（输入→正确答案），如垃圾邮件分类（标注了垃圾/正常）；无监督学习无标注数据，靠发现数据内在结构，如用户分群（根据行为自动聚类）。

### 代码题

**A-C01** ⭐ 修复 bug：
```python
def avg(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)
print(avg([]))  # 会报什么错？怎么修？
```

> **答案：** ZeroDivisionError。修复：`if not numbers: return 0.0`。最佳实践：永远检查分母是否为零。

**A-C02** ⭐ 补全：用列表推导式生成 1-20 中所有偶数的平方。
```python
result = [___ for i in range(1, 21) if ___]
```

> **答案：** `[i**2 for i in range(1, 21) if i % 2 == 0]` → [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]

---

## 第三部分：题库 B（L2 入门进阶）

### 选择题

**B-S01** ⭐⭐ 机器学习
关于过拟合，描述**不正确**的是？
A. 训练误差低、测试误差高是信号
B. 增加模型复杂度可以解决
C. Dropout 和 L2 可缓解
D. 增加数据可缓解

> **答案：B。** 增加复杂度反而加剧过拟合。正确方向：减少参数、增加正则化、加数据。

**B-S02** ⭐⭐ 提示词工程
「Let's think step by step」属于什么技术？
A. Few-Shot
B. Chain of Thought
C. RAG
D. Fine-tuning

> **答案：B。** CoT 提示让 LLM 逐步推理而非直接跳答案，显著提升数学/逻辑任务的准确率。

**B-S03** ⭐⭐ 特征工程
数据标准化的主要目的是？
A. 增加特征数
B. 将所有特征统一到相同尺度（均值 0/标准差 1），消除量纲影响
C. 将数据转为整数
D. 降低模型复杂度

> **答案：B。** 量纲差异大时（年龄 0-100 vs 收入 0-100000），梯度下降会被大量纲特征主导。

**B-S04** ⭐⭐ FastAPI
Pydantic BaseModel 的核心作用是？
A. 渲染 HTML 模板
B. 定义请求/响应数据结构，自动验证和序列化
C. 管理数据库 ORM
D. 处理用户认证

> **答案：B。** Pydantic 提供类型检查、数据校验、JSON 序列化，并自动生成 API 文档。

### 简答题

**B-A01** ⭐⭐ 解释偏差-方差权衡。

> **答案：** 偏差=模型预测的系统性误差（欠拟合，训练测试误差都高），方差=对训练数据的敏感度（过拟合，训练低测试高）。总误差 = 偏差² + 方差 + 噪声。最优模型在交叉验证中找平衡点。

**B-A02** ⭐⭐ 什么是交叉验证？K 折步骤？

> **答案：** 将数据分 K 份，每次用 1 份验证、K-1 份训练，重复 K 次取均值。优势：减少单次划分的随机性，适合小数据集，评估更稳定。

**B-A03** ⭐⭐ 简述 RAG 工作流程，解决了 LLM 什么问题。

> **答案：** 流程：用户提问→检索相关文档→检索结果+问题送入 LLM→基于文档生成答案。解决：1) 知识时效性（引用最新文档）2) 幻觉（有事实依据）3) 私域知识（无需重训模型）。

### 代码题

**B-C01** ⭐⭐ 补全 sklearn Pipeline：
```python
pipeline = Pipeline([
    ('scaler', ___),
    ('classifier', ___)
])
pipeline.fit(X_train, y_train)
pred = pipeline.predict(___)
```

> **答案：** `StandardScaler()` / `LogisticRegression(max_iter=200)` / `X_test`

**B-C02** ⭐⭐ PyTorch 训练循环找 2 个 bug：
```python
for epoch in range(10):
    for x, y in loader:
        out = model(x)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
```

> **答案：** 1) 缺 `optimizer.zero_grad()`（梯度累积）；2) 缺 `model.train()` 声明（显式更好）。修复版：在 backward 前加 `optimizer.zero_grad()`。

---

## 第四部分：题库 C（L3 中级实战）

### 选择题

**C-S01** ⭐⭐⭐ Transformer 中 Self-Attention 复杂度是？
A. O(n)
B. O(n log n)
C. O(n²)
D. O(1)

> **答案：C。** 每个 token 需与序列所有 token 算分数，得 n×n 矩阵。这是长文本瓶颈，催生 FlashAttention。

**C-S02** ⭐⭐⭐ RAG 中 chunk_size 过小的后果？
A. embedding 变快
B. 检索丢失关键上下文，语义不完整
C. 存储减少
D. 精度提升

> **答案：B。** chunk 太小会把完整语义拆分到多个块，检索时可能只命中片段。推荐 512-1024 + 10-15% overlap。

**C-S03** ⭐⭐⭐ 关于 Function Calling，不正确的是？
A. 让 LLM 调用外部工具
B. LLM 决定何时调用和参数
C. LLM 实际执行 Function 中的代码
D. 开发者需预定义 Function Schema

> **答案：C。** LLM 只负责决策（是否调用+参数），不负责执行。代码由应用层执行。

**C-S04** ⭐⭐⭐ LoRA 相比全参数微调的核心优势？
A. 效果更好
B. 只训练 0.1-1% 参数，显存极低
C. 增加层数
D. 不需训练数据

> **答案：B。** LoRA 冻结原权重，只训练低秩矩阵 B×A，使得单张消费级 GPU 可微调 7B-70B 模型。

### 简答题

**C-A01** ⭐⭐⭐ 详解 Scaled Dot-Product Attention 计算步骤，说明除 √d_k 的原因。

> **答案：** `Attention(Q,K,V) = softmax(Q·Kᵀ/√d_k)·V`。当 d_k 大时，点积值方差≈d_k，softmax 进入梯度饱和区。除 √d_k 将方差归一化到 1，保持梯度健康。

**C-A02** ⭐⭐⭐ RAG 检索优化策略列出 4 种并简述。

> **答案：** 1) Reranker：Cross-Encoder 二次排序 2) Hybrid Search：向量+BM25 互补 3) Query Rewriting：改写/扩展/分解查询 4) 递归检索：先粗后精。

**C-A03** ⭐⭐⭐ 什么是 ReAct 范式？描述工作循环。

> **答案：** ReAct = Reasoning + Acting。循环：Thought（分析）→ Action（调用工具）→ Observation（获取结果）→ 回到 Thought 直到可给出答案。优势：可追踪、可解释、任务完成率高。

**C-A04** ⭐⭐⭐⭐ 比较 SFT 和 DPO 的区别，DPO 有什么优势？

> **答案：** SFT 直接学标注（输入→正确输出）；DPO 从偏好对中学（A 比 B 好）。DPO 优势：不需独立训 Reward Model、不需 RL（训练更稳定）、参数更少、效果相当或更好。

### 代码题

**C-C01** ⭐⭐⭐ 补全 PyTorch Self-Attention：
```python
class SimpleSelfAttention(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
    def forward(self, x):
        Q, K, V = self.W_q(x), self.W_k(x), self.W_v(x)
        d_k = Q.size(-1)
        scores = ___                     # Q·Kᵀ/√d_k
        attn = ___                      # softmax
        out = ___                       # ×V
        return out
```

> **答案：** `torch.matmul(Q, K.transpose(-2,-1)) / d_k**0.5` / `F.softmax(scores, dim=-1)` / `torch.matmul(attn, V)`

**C-C02** ⭐⭐⭐ 修复 LoRA 配置错误：
```python
config = LoraConfig(
    r=8, lora_alpha=16,
    target_modules=["q_proj", "v_proj"],  # 只对 Q 和 V 做 LoRA
    lora_dropout=0.1
)
```
这段配置有什么潜在问题？如何优化？

> **答案：** 只对 Q/V 做 LoRA 不够全面。推荐同时覆盖 `["q_proj","k_proj","v_proj","o_proj"]`（QKV+输出投影），或加 `"gate_proj","up_proj","down_proj"`（FFN 层）。典型 r=8-16，alpha=2r。

---

## 第五部分：题库 D（L4 高级深耕）

### 选择题

**D-S01** ⭐⭐⭐ 以下哪个属于 RLHF 流程中的步骤？
A. 自监督预训练
B. 训练 Reward Model 预测人类偏好
C. Beam Search 推理
D. Tokenization

> **答案：B。** RLHF 三步：SFT → 训练 Reward Model（对回答排名）→ PPO 强化学习。

**D-S02** ⭐⭐⭐ MCP 协议的核心作用？
A. Prompt 模板管理
B. 标准化 AI 模型与外部工具的交互方式
C. 加速推理
D. 数据增强

> **答案：B。** MCP 定义 AI↔工具的标准接口，类似「AI 的 USB 协议」。

**D-S03** ⭐⭐⭐ 多 Agent 通信模式不包括？
A. 顺序链式
B. 广播式
C. 集中路由式
D. 梯度共享式

> **答案：D。** 梯度共享是分布式训练概念，不是 Agent 通信模式。

**D-S04** ⭐⭐⭐ FlashAttention 核心优化思路？
A. 减少参数
B. 分块计算+核融合，减少 HBM 读写，显存 O(n²)→O(n)
C. 降低精度
D. 使用更小模型

> **答案：B。** 标准 Attention 瓶颈在 IO（写 n×n 矩阵到 HBM），FlashAttention 在 SRAM 中完成分块计算再写回。

### 简答题

**D-A01** ⭐⭐⭐⭐ 设计企业级 RAG 系统的 6 大组件。

> **答案：** 1) 文档处理层（解析+分块+元数据）2) 向量化层（Embedding 模型）3) 存储层（向量DB+原始存储）4) 检索层（多路召回+Reranker+查询改写）5) 生成层（Prompt 组装+LLM+后处理）6) 评估监控层（RAGAS+反馈收集+质量监控）。

**D-A02** ⭐⭐⭐⭐ 如何设计模型路由（Model Router）降低 LLM 成本？

> **答案：** 意图分类器判断复杂度 → 简单任务用便宜模型（Haiku/GPT-3.5），复杂任务用强模型（Claude 3.5/GPT-4o）。加缓存层（相同请求直接返回）、级联降级（便宜→强）、超时重试。预期降本 50-70%。

**D-A03** ⭐⭐⭐⭐⭐ 生产环境部署 LLM 应用的核心挑战和解决方案。

> **答案：** 1) 延迟：Continuous Batching + 量化 + Streaming 2) 成本：模型路由 + 缓存 + Token 优化 3) 可靠性：熔断+重试+降级+多模型 fallback 4) 安全：Guardrails+审计+脱敏 5) 可观测性：LangSmith/Prometheus/Grafana 全链路监控。

### 代码题

**D-C01** ⭐⭐⭐⭐ 实现简版 Model Router：
```python
class ModelRouter:
    def __init__(self):
        self.cheap = CheapModel()  # 低成本
        self.strong = StrongModel()  # 高质量
    
    def route(self, query):
        # TODO: 复杂度判断 + 路由 + 兜底
        pass
```

> **答案：** 先判断复杂度（长度<50 且无「分析/设计/代码」关键词→简单→便宜模型），否则用强模型。进阶：加质量检查→不满足则升级模型。

---

## 第六部分：章节练习题生成规范

### 标准模板（每章 5 题）

```
## 📝 第 X 章练习题

> 💡 先独立完成，再看答案

### 题 1 — 概念理解 ⭐/⭐⭐
[选择题/判断题]

### 题 2 — 概念理解 ⭐/⭐⭐
[选择题/简答题]

### 题 3 — 代码实践 ⭐⭐/⭐⭐⭐
[补全代码]

### 题 4 — 代码实践 ⭐⭐/⭐⭐⭐
[找 Bug 修复]

### 题 5 — 综合应用 ⭐⭐⭐/⭐⭐⭐⭐
[场景题 100-200 字]

---

## ✅ 标准答案

### 答案 1（逐选项分析为什么对/错）
### 答案 2（原理+常见误解）
### 答案 3（完整代码+关键步骤+变体写法）
### 答案 4（Bug 定位+修复+原因+预防建议）
### 答案 5（思路分解≥3步+参考实现+≥2条优化方向）
```

### 难度分布矩阵

| 章节等级 | 难度组合 |
|----------|----------|
| L1 | ⭐×3 + ⭐⭐×2 |
| L2 | ⭐×1 + ⭐⭐×3 + ⭐⭐⭐×1 |
| L3 | ⭐⭐×2 + ⭐⭐⭐×2 + ⭐⭐⭐⭐×1 |
| L4 | ⭐⭐⭐×3 + ⭐⭐⭐⭐×2 |
