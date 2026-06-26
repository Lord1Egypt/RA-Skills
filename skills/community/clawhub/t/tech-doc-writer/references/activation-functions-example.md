# 激活函数文档节选示例

> 本文件展示了 tech-doc-writer skill 的写作风格，以激活函数文档中的 ReLU 和 GELU 两节为例。

---

## 示例 1：ReLU（展示基础方法的写法）

### ReLU（修正线性单元）

**论文**：Rectified Linear Units Improve Restricted Boltzmann Machines（Nair & Hinton，2010）

**数学定义：**

$$\text{ReLU}(x) = \max(0, x) = \begin{cases} x & x > 0 \\ 0 & x \leq 0 \end{cases}$$

**导数：**

$$\text{ReLU}'(x) = \begin{cases} 1 & x > 0 \\ 0 & x < 0 \end{cases}$$

**直觉解释**：只保留正信号，负信号清零。计算只需一次比较，极其高效。正半轴梯度恒为 1，梯度可以无衰减地反向传播——这是解决梯度消失的核心。

**优点：**

| 优势 | 说明 |
|------|------|
| 缓解梯度消失 | 正半轴梯度恒为 1 |
| 稀疏激活 | 约 50% 输出为 0，正则化效果 |
| 计算高效 | 仅一次比较，无指数运算 |

**缺点：**

| 问题 | 说明 |
|------|------|
| Dead ReLU | 负输入区梯度为 0，神经元可能永久死亡 |
| 非零中心 | 输出均值大于 0，收敛略慢 |

```python
import torch.nn.functional as F

out = F.relu(x)
```

---

## 示例 2：GELU（展示现代方法的写法，含直觉解释）

### GELU（高斯误差线性单元）

**论文**：Gaussian Error Linear Units（Hendrycks & Gimpel，2016）

**数学定义：**

$$\text{GELU}(x) = x \cdot \Phi(x) = x \cdot P(X \leq x), \quad X \sim \mathcal{N}(0,1)$$

**近似公式**（实际实现常用）：

$$\text{GELU}(x) \approx 0.5x\left(1 + \tanh\left(\sqrt{\frac{2}{\pi}}\left(x + 0.044715 x^3\right)\right)\right)$$

**直觉解释**：GELU 是"概率门控"的 ReLU——以概率 $\Phi(x)$ 通过输入，概率随 $x$ 大小平滑变化。大正值几乎全部通过，小负值几乎全部被抑制，但不是硬截断而是平滑过渡。

**与 ReLU 对比：**

| 特性 | ReLU | GELU |
|------|------|------|
| 负半轴处理 | 硬截断为 0 | 平滑衰减 |
| 可微性 | x=0 不可微 | 处处可微 |
| 在 Transformer 中 | 较少使用 | 主流选择 |

```python
# 精确版本
out = F.gelu(x)

# 近似版本（速度稍快）
out = F.gelu(x, approximate='tanh')
```
