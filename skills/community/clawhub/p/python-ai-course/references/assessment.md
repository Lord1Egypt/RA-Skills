# AI 全栈教学导师 — 摸底考试题库 & 练习题规范

## 考试规则

- 考试在六大维度调研对话完成后进行，在正式教学前
- 根据学员自报水平和目标方向，从对应难度层抽取 **10 题**
- 题型组合：**4 道选择题 + 4 道简答题 + 2 道代码阅读/填空题**
- 批改后提供：客观评分（x/10）+ 每题完整解析（重点讲"为什么"）
- 根据考试结果二次校准等级，考试结果与自报水平不符时以考试为准

---

## 题库：Python 基础（L1 摸底使用）

### 选择题

**PY-S01** ⭐
以下代码的输出是？
```python
x = [1, 2, 3]
y = x
y.append(4)
print(x)
```
A. `[1, 2, 3]`
B. `[1, 2, 3, 4]`
C. `[4]`
D. 报错

> **答案：B**
> 解析：`y = x` 是引用赋值（浅拷贝），两个变量指向同一个列表对象。`y.append(4)` 修改的是同一个对象，所以 `x` 也变了。若要独立副本，需用 `y = x.copy()` 或 `y = x[:]`。

---

**PY-S02** ⭐
以下哪个 **不是** Python 内置数据类型？
A. list
B. tuple
C. array
D. dict

> **答案：C**
> 解析：`array` 需要从标准库 `array` 模块导入，或使用 NumPy 的 `ndarray`。`list`、`tuple`、`dict`、`set`、`str`、`int`、`float`、`bool` 均为内置类型。

---

**PY-S03** ⭐
`@staticmethod` 装饰器的作用是？
A. 只能通过类实例调用，会自动传入 self
B. 不需要传入 self 或 cls 参数，类或实例均可调用
C. 自动缓存函数的返回结果
D. 限制函数只能被调用一次

> **答案：B**
> 解析：静态方法不访问实例状态（self）也不访问类状态（cls），本质上是被放在类命名空间里的普通函数，通常用于工具函数。

---

**PY-S04** ⭐⭐
`yield` 关键字的作用是？
A. 返回函数结果并立即结束函数执行
B. 抛出一个异常
C. 将函数变为生成器，每次调用 next() 时暂停并返回值
D. 等待异步操作完成（相当于 await）

> **答案：C**
> 解析：含有 `yield` 的函数变成生成器函数，调用时不执行函数体，而是返回生成器对象。每次调用 `next()` 或在 for 循环中迭代时，从上次 `yield` 处继续执行直到下一个 `yield`。

---

### 简答题

**PY-A01** ⭐
解释 Python 中 `*args` 和 `**kwargs` 的区别，并各给出一个实际使用场景示例。

> **标准答案：**
> - `*args`：接收任意数量的**位置参数**，在函数内部以元组（tuple）形式存在
> - `**kwargs`：接收任意数量的**关键字参数**，在函数内部以字典（dict）形式存在
>
> 示例：
> ```python
> def demo(*args, **kwargs):
>     print("位置参数:", args)      # (1, 2, 3)
>     print("关键字参数:", kwargs)   # {'name': 'Alice', 'age': 20}
>
> demo(1, 2, 3, name='Alice', age=20)
>
> # 实际场景：包装函数（wrapper），需要透传所有参数
> def log_wrapper(func, *args, **kwargs):
>     print(f"调用 {func.__name__}")
>     return func(*args, **kwargs)
> ```

---

**PY-A02** ⭐
将下面的 for 循环改写为列表推导式，并解释列表推导式的语法结构：
```python
result = []
for i in range(10):
    if i % 2 == 0:
        result.append(i ** 2)
```

> **标准答案：**
> ```python
> result = [i**2 for i in range(10) if i % 2 == 0]
> # 结果：[0, 4, 16, 36, 64]
> ```
> 语法结构：`[表达式 for 变量 in 可迭代对象 if 条件（可选）]`
> 可读性提示：当逻辑过于复杂时（多层嵌套），应改回 for 循环，不要强用推导式。

---

**PY-A03** ⭐⭐
解释 Python 装饰器的原理，并手写一个计时装饰器，记录函数执行时间。

> **标准答案：**
> 装饰器本质是一个**接收函数作为参数，返回新函数的高阶函数**。`@decorator` 语法糖等价于 `func = decorator(func)`。
>
> ```python
> import time
> import functools
>
> def timer(func):
>     @functools.wraps(func)  # 保留原函数的 __name__、__doc__
>     def wrapper(*args, **kwargs):
>         start = time.time()
>         result = func(*args, **kwargs)
>         end = time.time()
>         print(f"{func.__name__} 执行耗时: {end - start:.4f}s")
>         return result
>     return wrapper
>
> @timer
> def slow_function():
>     time.sleep(1)
>
> slow_function()  # 输出: slow_function 执行耗时: 1.0012s
> ```

---

### 代码题

**PY-C01** ⭐
以下代码有一个 bug，找出并修复：
```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

print(calculate_average([]))
```

> **标准答案：**
> **问题**：空列表会导致 `ZeroDivisionError: division by zero`
>
> **修复方案：**
> ```python
> def calculate_average(numbers):
>     if not numbers:  # 空列表、None 等均为 falsy
>         return 0.0   # 或 return None，根据业务语义决定
>     return sum(numbers) / len(numbers)
>
> # 更 Pythonic 的写法：
> def calculate_average(numbers):
>     return sum(numbers) / len(numbers) if numbers else 0.0
> ```

---

## 题库：机器学习基础（L2 摸底使用）

### 选择题

**ML-S01** ⭐⭐
过拟合的解决方案 **不包括** 以下哪项？
A. 增加训练数据
B. 使用 Dropout
C. 增加模型复杂度（更多层/更多参数）
D. L2 正则化

> **答案：C**
> 解析：增加模型复杂度会**加剧**过拟合（模型有更大容量去记忆噪声）。解决过拟合的方向是：减小模型容量、增加数据量、加入正则化、使用 Dropout/Early Stopping。

---

**ML-S02** ⭐⭐
正负样本极度不平衡时（例如 1:99），最不适合单独使用哪个评估指标？
A. F1 Score
B. AUC-ROC
C. Precision（精确率）
D. Accuracy（准确率）

> **答案：D**
> 解析：若数据集中 99% 是负样本，模型全部预测为负类也能达到 99% 的准确率，但对正类完全没有识别能力。AUC-ROC 和 F1 对类别不平衡更鲁棒。

---

**ML-S03** ⭐⭐
K-Means 算法的 K 值如何合理选择？
A. 总是选最大的 K 以获得最高精度
B. 使用肘部法则（Elbow Method）观察惯性随 K 增大的下降趋势
C. K 值必须等于特征数量
D. 随机选择

> **答案：B**
> 解析：肘部法则绘制不同 K 值对应的 Inertia（簇内平方和），找"肘部"拐点处的 K 值。也可以结合轮廓系数（Silhouette Score）综合判断。

---

### 简答题

**ML-A01** ⭐⭐
解释偏差-方差权衡（Bias-Variance Tradeoff），并说明高偏差和高方差分别对应什么问题及解决方向。

> **标准答案：**
> - **偏差（Bias）**：模型预测值与真实值的系统性误差，来源于模型假设过于简单（欠拟合）
>   - 表现：训练误差和测试误差都很高
>   - 解决：增加模型复杂度、添加更多特征、选用更强的模型
>
> - **方差（Variance）**：模型对训练集微小变化的敏感程度，来源于模型过于复杂（过拟合）
>   - 表现：训练误差很低，但测试误差明显高
>   - 解决：增加训练数据、降低模型复杂度、正则化、Dropout
>
> - **权衡**：泛化误差 = 偏差² + 方差 + 不可避免噪声。目标是找到两者的最优平衡点（通过验证集调参）。

---

**ML-A02** ⭐⭐
什么是交叉验证（Cross-Validation）？K 折交叉验证的步骤是什么？为什么优于简单的训练/测试集划分？

> **标准答案：**
> 交叉验证是一种评估模型泛化能力的技术，通过多次划分数据集获得更稳定的评估结果。
>
> **K 折交叉验证步骤：**
> 1. 将数据集随机划分为 K 个等大小的子集（fold）
> 2. 重复 K 次：用 K-1 个子集训练，第 i 个子集验证
> 3. 取 K 次验证结果的平均值作为最终指标
>
> **优势：**
> - 所有数据都参与了训练和验证（充分利用小数据集）
> - 结果更稳定（减小随机划分带来的方差）
> - 适合数据量不多的场景（医疗数据等）

---

### 代码题

**ML-C01** ⭐⭐
补全以下 sklearn 代码，实现一个完整的分类流水线（Pipeline）：
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: 创建包含标准化 + 逻辑回归的 Pipeline
pipeline = ___

# TODO: 训练模型
___

# TODO: 打印测试集准确率
print(f"准确率: {___:.4f}")
```

> **标准答案：**
> ```python
> pipeline = Pipeline([
>     ('scaler', StandardScaler()),
>     ('classifier', LogisticRegression(max_iter=200))
> ])
>
> pipeline.fit(X_train, y_train)
>
> print(f"准确率: {pipeline.score(X_test, y_test):.4f}")
> # 输出约: 准确率: 0.9667
> ```
> 要点：Pipeline 保证在预测时，测试数据经过的标准化参数来自训练集（防止数据泄露）。

---

## 题库：深度学习（L3 摸底使用）

### 选择题

**DL-S01** ⭐⭐⭐
Transformer 中 Self-Attention 的计算复杂度（相对于序列长度 n）是？
A. O(n)
B. O(n log n)
C. O(n²)
D. O(n² × d)（d 为隐藏维度）

> **答案：C（或 D，视是否考虑维度）**
> 解析：每个 token 需要与序列中所有 n 个 token 计算注意力分数（Q × Kᵀ），得到 n×n 的注意力矩阵，因此时间和空间复杂度均为 O(n²d)，序列维度简化后说 O(n²)。这是 Transformer 处理长文本的瓶颈，催生了 FlashAttention、线性注意力等改进。

---

**DL-S02** ⭐⭐
Batch Normalization 的主要作用是？
A. 减少模型参数数量
B. 加速训练收敛、稳定训练过程、缓解梯度消失/爆炸
C. 防止过拟合（类似 Dropout）
D. 增加模型非线性表达能力

> **答案：B**
> 解析：BN 将每个 mini-batch 内的特征归一化到均值为 0、方差为 1，然后通过可学习参数 γ 和 β 恢复表达能力。主要效果是稳定训练（可以用更大学习率）、缓解内部协变量偏移。

---

**DL-S03** ⭐⭐⭐
LoRA 的核心思想是？
A. 增加模型层数提升表达能力
B. 用低秩矩阵 B×A 来近似权重更新量 ΔW，大幅减少可训练参数
C. 在推理时随机丢弃神经元降低过拟合
D. 将大模型的知识蒸馏到小模型中

> **答案：B**
> 解析：LoRA 冻结预训练权重 W₀，引入可训练的低秩分解 ΔW = B×A（r 远小于 d）。前向传播变为 W₀x + BAx，只需训练 B 和 A，参数量从 d×d 降低到 d×r + r×d = 2dr（r 通常取 4-64）。推理时可将 BA 合并回 W₀ 无额外延迟。

---

### 简答题

**DL-A01** ⭐⭐⭐
请解释 Transformer 中的 Scaled Dot-Product Attention 计算过程，并说明为什么要除以 √d_k。

> **标准答案：**
> 计算步骤：
> 1. 输入 X 分别乘以三个权重矩阵，得到 Q（Query）、K（Key）、V（Value）
> 2. 计算注意力分数：`scores = Q × Kᵀ / √d_k`
> 3. 应用 Softmax：`attention_weights = softmax(scores)`
> 4. 加权求和：`output = attention_weights × V`
>
> **为什么除以 √d_k？**
> 当 d_k（key 的维度）较大时，Q 与 K 的点积会非常大（方差为 d_k），导致 Softmax 的输入落入梯度极小的区域（饱和区），梯度消失。除以 √d_k 将方差归一到 1，Softmax 的梯度保持健康。

---

**DL-A02** ⭐⭐⭐
解释梯度消失问题，并说明 ResNet 的残差连接如何解决这个问题。

> **标准答案：**
> **梯度消失**：在深层网络中，反向传播时梯度需要经过多层链式相乘。若激活函数（如 Sigmoid）的导数小于 1，经过数十层后梯度趋近于 0，浅层网络无法有效学习。
>
> **ResNet 残差连接**：引入 `output = F(x) + x`（即跳跃连接），反向传播时梯度可以通过两条路径流动：
> 1. 通过残差块 F(x)
> 2. 直接通过恒等映射（`+x` 这条路）
>
> 这条直接路径保证了梯度不会完全消失，使训练 100+ 层的深层网络成为可能。

---

### 代码题

**DL-C01** ⭐⭐⭐
以下 PyTorch 训练代码有 **2 个** 问题，找出并修复：
```python
model = SimpleNet()
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    for batch_x, batch_y in dataloader:
        output = model(batch_x)
        loss = criterion(output, batch_y)
        loss.backward()
        optimizer.step()
    
    print(f"Epoch {epoch}, Loss: {loss.item()}")
```

> **标准答案：**
> **问题 1**：缺少 `optimizer.zero_grad()`
> 梯度会在每次 `backward()` 后累积到已有梯度上，导致错误的参数更新。
>
> **问题 2**：验证阶段应使用 `model.eval()` 和 `torch.no_grad()`（此代码没有评估阶段，但建议添加）
> 另外，`print` 中的 `loss.item()` 只是最后一个 batch 的 loss，更好的做法是记录 epoch 平均 loss。
>
> **修复版本：**
> ```python
> for epoch in range(10):
>     model.train()
>     total_loss = 0.0
>     for batch_x, batch_y in dataloader:
>         optimizer.zero_grad()          # ✅ 清零梯度
>         output = model(batch_x)
>         loss = criterion(output, batch_y)
>         loss.backward()
>         optimizer.step()
>         total_loss += loss.item()
>
>     avg_loss = total_loss / len(dataloader)
>     print(f"Epoch {epoch}, Avg Loss: {avg_loss:.4f}")  # ✅ 记录平均 loss
> ```

---

## 题库：RAG 与提示词工程（L3-L4 摸底使用）

### 选择题

**RAG-S01** ⭐⭐⭐
向量数据库中，余弦相似度与欧氏距离的主要区别是？
A. 余弦相似度只关注向量的**方向**（角度），不考虑模长；欧氏距离关注**绝对距离**
B. 两者对于归一化向量完全等价，无区别
C. 余弦相似度只适用于图像向量，欧氏距离适用于文本向量
D. 欧氏距离在高维空间中比余弦相似度更稳定

> **答案：A（对于归一化向量，A 和 B 都正确，但通常说法以 A 为准）**
> 解析：语义搜索中，余弦相似度更常用，因为文本嵌入向量的语义由方向决定，不同模型生成的向量模长不一定可比。对于归一化（单位向量）的 embedding，余弦相似度和欧氏距离单调等价。

---

**RAG-S02** ⭐⭐⭐
以下哪种情况**最适合**使用 RAG 而非微调？
A. 需要改变模型的回答语气和风格（更正式/更口语化）
B. 需要让模型掌握新的语言能力（例如学会写特定格式的代码）
C. 需要让模型能够访问并引用**经常更新**的私有文档
D. 需要让模型更好地遵守特定的指令格式

> **答案：C**
> 解析：RAG 擅长处理"需要访问外部知识且知识频繁更新"的场景，无需重新训练。微调更适合改变模型行为模式（风格、格式、能力）而非注入特定知识。

---

### 简答题

**RAG-A01** ⭐⭐
什么是 LLM 的幻觉（Hallucination）问题？RAG 是如何帮助减少幻觉的？RAG 能完全消除幻觉吗？

> **标准答案：**
> **幻觉**：LLM 生成看似合理、逻辑流畅但实际上**错误或虚构**的内容（例如引用不存在的论文、编造人物经历）。根源是 LLM 基于概率生成下一个 token，倾向于生成"看起来合理"的内容，而非"保证真实"的内容。
>
> **RAG 如何减少幻觉：**
> 1. 提供真实的检索文档作为上下文，约束模型"基于文档回答"
> 2. 可以要求模型引用来源，使幻觉可被验证和检测
> 3. 减少模型对参数化记忆（可能已过时或不准确）的依赖
>
> **能否完全消除？** 不能。模型仍可能在检索到的上下文基础上产生幻觉（"忠实度"问题），或检索结果本身不相关导致模型凭空生成答案。需要配合 RAGAS 等评估框架持续监控。

---

**RAG-A02** ⭐⭐⭐
解释 RAG 中分块策略的重要性，以及固定窗口分块和语义分块各自的优劣势。

> **标准答案：**
> 分块是将长文档切割为可被检索的小单元。分块策略直接影响检索质量：
> - 分块太小：语义不完整，上下文丢失
> - 分块太大：噪声过多，与查询相关性稀释
>
> **固定窗口分块：**
> - 优点：实现简单、速度快、确定性强
> - 缺点：可能在句子中间截断，破坏语义完整性
> - 适用：内容结构均匀的文档（日志、表格数据）
>
> **语义分块：**
> - 优点：保持语义完整性，根据内容自然边界切割
> - 缺点：计算成本高（需要计算嵌入），分块大小不均匀
> - 适用：叙事性文档、技术文档、学术论文
>
> 实践建议：优先用递归字符分块（LangChain 的 `RecursiveCharacterTextSplitter`），添加 10-15% 的重叠（overlap）避免边界信息丢失。

---

## 章节练习题规范（正式教学阶段使用）

每章结束后，按以下模板生成 **5 道练习题**（题目和答案明确分隔）：

### 标准输出格式

```markdown
## 📝 第 X 章练习题

> 💡 建议先独立完成所有题目，再查看答案

### 题 1 — 概念理解 ⭐
[选择题，4 个选项，有明确正确答案]

### 题 2 — 概念理解 ⭐⭐
[判断题或简答题，要求解释原因]

### 题 3 — 代码实践 ⭐⭐
[给出不完整代码，要求补全关键部分]
```python
# 你的代码
```

### 题 4 — 代码实践 ⭐⭐⭐
[给出有 1-2 个 bug 的代码，要求找出并修复]
```python
# 有问题的代码
```

### 题 5 — 综合应用 ⭐⭐⭐
[100-200 字的场景描述，要求设计方案或完整实现]

---

## ✅ 标准答案（向下滚动查看）

### 答案 1
**答案：X**
选项分析：
- A：...（错误原因）
- B：...（错误原因）
- C：...（正确原因）
- D：...（错误原因）

### 答案 2
[完整答案 + 原理解释 + 常见错误认知纠正]

### 答案 3
```python
# 完整代码 + 逐行关键注释
```
关键点说明：...

### 答案 4
**问题所在**：第 X 行，...
**修复版本**：
```python
# 修复后的完整代码
```
**原因解释**：...

### 答案 5
**思路分析**：...
**参考实现**：
```python
# 完整可运行实现
```
**优化方向**：...
```

---

## 难度分级标准

| 难度 | 标记 | 适用等级 | 典型题型 |
|------|------|----------|----------|
| ⭐ | 基础 | L1 | 概念判断、基础语法填空 |
| ⭐⭐ | 中级 | L2-L3 | 原理解释、简单调试 |
| ⭐⭐⭐ | 高级 | L3-L4 | 架构设计、复杂调试、性能分析 |
| ⭐⭐⭐⭐ | 挑战 | L4 | 从零实现、系统优化、创新应用 |

**每章练习题难度分布建议：**

| 章节等级 | 难度组合 |
|----------|----------|
| L1 章节 | ⭐×3 + ⭐⭐×2 |
| L2 章节 | ⭐×1 + ⭐⭐×3 + ⭐⭐⭐×1 |
| L3 章节 | ⭐⭐×2 + ⭐⭐⭐×2 + ⭐⭐⭐⭐×1 |
| L4 章节 | ⭐⭐⭐×2 + ⭐⭐⭐⭐×3 |
