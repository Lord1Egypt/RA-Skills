# 归一化文档节选示例

> 本文件展示了 tech-doc-writer skill 的写作风格，以归一化文档中的"统一视角"章节和 BN 章节为例。

---

## 示例 1：统一视角（这种"元框架"是文档质量的关键）

### 归一化的统一视角：在哪个维度做统计

几乎所有归一化方法的本质区别，就在于**在哪些维度上计算均值和方差**。

对于 4D 特征张量 $\mathbf{X} \in \mathbb{R}^{N \times C \times H \times W}$：

| 方法 | 统计维度 | 对应轴 |
|------|---------|--------|
| **BN** | N, H, W（跨样本，每通道独立） | `axis=[0, 2, 3]` |
| **LN** | C, H, W（跨通道，每样本独立） | `axis=[1, 2, 3]` |
| **IN** | H, W（空间维度，每样本每通道独立） | `axis=[2, 3]` |
| **GN** | C/G, H, W（按组分通道） | 按组划分 |

> 这个"统一视角"框架是原文没有的——它帮助读者从根本上理解各方法，而不是机械地记忆各个公式。

---

## 示例 2：BN（展示"重要修正"的写法）

### Batch Normalization

**提出动机**：Ioffe & Szegedy（2015）认为 BN 解决了 **Internal Covariate Shift（ICS）**——每层输入分布随参数更新而变化，导致训练不稳定。

> **⚠️ 重要修正**：Santurkar et al.（2018）在论文《How Does Batch Normalization Help Optimization?》中通过实验证明，BN 的有效性**并非**主要来自解决 ICS，而是通过**平滑损失曲面（loss landscape）**使梯度更稳定。这是对原始论文叙事的重要修正，不必迷信 ICS 叙事。

**训练 vs 推理的差异**（原文常忽略的细节）：

- **训练阶段**：用当前 mini-batch 的均值和方差
- **推理阶段**：用训练期间积累的**移动平均**（Running Statistics）

$$\mu_{\text{running}} \leftarrow (1 - \alpha) \mu_{\text{running}} + \alpha \mu_\mathcal{B}$$

**常见陷阱**：

```python
# ⚠️ PyTorch BN 的 momentum 定义与数学通常写法相反！
# PyTorch: new = (1 - momentum) * old + momentum * batch_stat
# 数学写法通常: new = momentum * old + (1-momentum) * new_val
# PyTorch 默认 momentum=0.1，表示"当前 batch 权重 0.1，历史权重 0.9"

bn = nn.BatchNorm2d(64, momentum=0.1)  # 这是 PyTorch 默认值

# 另一个常见错误：忘记切换 eval 模式
model.eval()  # 必须切换！否则推理用 batch 统计，batch=1 时不稳定
with torch.no_grad():
    output = model(x)
```
