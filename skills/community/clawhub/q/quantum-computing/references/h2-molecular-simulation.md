# H2 分子模拟参考

这个主题最容易受版本和依赖影响。用户提到 “H2 模拟” 时，先不要默认当前环境已经具备完整、固定的量子化学求解栈，更稳妥的做法是先确认他到底想解决哪一层问题。

## 推荐的定位

当用户说“H2 模拟”时，先分清楚他要的是哪一层：

1. 想看一个最小 VQE 例子
2. 想看 `hea` / `uccsd_ansatz` 如何接进变分循环
3. 想接入真实量子化学积分与 Hamiltonian 生成

当前 UnifiedQuantum 更适合稳定覆盖前两层。

## 推荐的理解方式

优先把 H2 任务理解成：

- 选一个小规模哈密顿量
- 选一个 ansatz（HEA 或 UCCSD）
- 用本地模拟器估计目标值
- 用经典优化器最小化能量

不要默认当前环境已经“内置了完整分子积分、Jordan-Wigner、basis set 流水线”。

## 最常用两个入口

### HEA

```python
from uniqc.algorithmics.ansatz import hea
```

适合：

- 教学演示
- 先跑通 VQE 外框架

### UCCSD

```python
from uniqc.algorithmics.ansatz import uccsd_ansatz
```

适合：

- 更接近量子化学 ansatz 的表达
- 已知 qubit 数和电子数时的最小示例

## 结果估计

当前更推荐两种估计路线：

1. 从 `simulate_pmeasure()` 得到概率分布，再用 `calculate_expectation()` 算 Z 型项
2. 从 `simulate_statevector()` 得到态矢，在示例里手工实现所需的观测量计算

如果只做教学示例，第一种通常更简单。

## 应该明确说出的限制

- H2 示例通常依赖本地模拟能力，因此往往需要 `unified-quantum[simulation]`
- 这里的 H2 示例更偏“工作流模板”，不是完整量化化学软件替代品
- 如果用户真的需要从分子几何一路生成哈密顿量，通常还要引入额外化学工具链
