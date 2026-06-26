# 研究方法决策助手

像一棵"决策树"，根据你的研究目的、数据类型和实验设计，自动推荐合适的统计检验方法，并提示前提假设、参数/非参数备选方案和对应的 Python 函数。

## 功能介绍

做研究时常常纠结"该用什么统计方法"。本工具把统计检验的选择逻辑结构化，你只需回答几个问题（研究目的、因变量类型、组数、设计等），即可得到推荐方法和注意事项，避免选错检验。

## 决策维度

工具基于以下维度做出推荐：

| 维度 | 选项 |
|------|------|
| **研究目的** | 比较差异 / 检验关系 / 预测 |
| **因变量类型** | 连续 / 分类 / 有序 |
| **组数/水平** | 1组 / 2组 / 3组及以上 |
| **实验设计** | 被试间(独立) / 被试内(配对) |
| **因素数量** | 单因素 / 多因素 |
| **假设满足** | 满足(参数) / 不满足(非参数) |

## 覆盖的统计方法

### 比较差异
- 单样本 t 检验 / Wilcoxon 符号秩检验
- 独立样本 t 检验 / Mann-Whitney U 检验
- 配对样本 t 检验 / Wilcoxon 符号秩检验
- 单因素方差分析 / Kruskal-Wallis 检验
- 重复测量方差分析 / Friedman 检验
- 多因素方差分析 (含交互作用)
- 卡方检验 / Fisher 精确检验

### 检验关系
- Pearson 相关 / Spearman 等级相关
- 卡方独立性检验

### 预测
- 线性回归 / 多元回归
- 逻辑回归 / 多项逻辑回归
- 有序逻辑回归

### 样本量与功效
- 各检验类型的样本量估算
- Cohen 效应量基准（小/中/大）
- 功效分析规划

### 信度与效度（量表研究）
- 信度：Cronbach's α、组合信度 CR、重测信度、评分者信度
- 效度：内容效度、EFA/CFA 结构效度、聚合效度 AVE、区分效度 HTMT
- 量表开发完整流程指引

### 中介与调节效应
- 中介效应（Bootstrap / PROCESS Model 4）
- 调节效应（层级回归 / PROCESS Model 1）
- 有调节的中介 / 有中介的调节

## 使用方法

### 直接获取推荐
```python
from method_advisor import StatTestAdvisor

advisor = StatTestAdvisor()

# 例：两组独立样本，连续因变量
result = advisor.recommend_test(
    goal="compare",          # 研究目的
    dv_type="continuous",    # 因变量类型
    n_groups=2,              # 组数
    design="independent"     # 设计
)
print(result["推荐检验"])    # → 独立样本 t 检验
print(result["前提假设"])    # → ['各组近似正态', '方差齐性...', '观测独立']
print(result["非参数备选"])  # → Mann-Whitney U 检验
```

### 2×2 被试内设计示例
```python
# 例：情绪(2) × 同余性(2) 双因素被试内设计
result = advisor.recommend_test(
    goal="compare",
    dv_type="continuous",
    n_groups=4,
    design="paired",
    n_factors=2
)
# → 2因素方差分析，含交互作用分析建议
```

### 不满足假设时
```python
# 数据不满足正态假设，自动推荐非参数方法
result = advisor.recommend_test(
    goal="compare",
    dv_type="continuous",
    n_groups=2,
    design="independent",
    assumptions_met=False    # 关键参数
)
# → Mann-Whitney U 检验
```

### 交互式问答引导
```python
# 逐步提问，引导式给出推荐
advisor.interactive_guide()
```

### 样本量/功效估算
```python
# 估算独立样本 t 检验所需样本量
result = advisor.recommend_sample_size(
    test_type="t_test_independent",
    effect_level="中",        # 小/中/大效应
    alpha=0.05,
    power=0.8
)
# → 每组样本量、总样本量、效应量基准、推荐用 G*Power 精算

# 也可指定具体效应量
advisor.recommend_sample_size("correlation", effect_size=0.3)
```

### 信度效度方法选择
```python
# 量表开发全流程指引
result = advisor.recommend_psychometric(need="development")
# → 信度方法 + 效度方法 + 7步开发流程 + 样本量建议

# 只看信度 / 只看效度
advisor.recommend_psychometric(need="reliability")
advisor.recommend_psychometric(need="validity")
```

### 中介/调节模型选择
```python
# 中介效应
advisor.recommend_mediation_moderation("mediation")
# → Bootstrap 法 + PROCESS Model 4 + 判断标准

# 调节效应
advisor.recommend_mediation_moderation("moderation")
# → 层级回归 + 交互项 + 简单斜率分析

# 有调节的中介
advisor.recommend_mediation_moderation("moderated_mediation")
# → 被调节的中介指数 + PROCESS Model 7/14/58/59
```

## 参数说明

| 参数 | 取值 | 说明 |
|------|------|------|
| `goal` | `compare` / `relationship` / `predict` | 研究目的 |
| `dv_type` | `continuous` / `categorical` / `ordinal` | 因变量类型 |
| `n_groups` | 整数 | 分组/水平数量(比较时) |
| `design` | `independent` / `paired` | 被试间/被试内 |
| `n_factors` | 整数 | 自变量(因素)数量 |
| `iv_type` | `continuous` / `categorical` / `ordinal` | 自变量类型(检验关系时) |
| `assumptions_met` | `True` / `False` | 是否满足参数假设 |

## 输出内容

每条推荐包含：
- **推荐检验/方法**：最适合的统计方法
- **适用**：什么情况下用
- **前提假设**：使用前需检查的假设
- **参数/非参数备选**：备选方案
- **后续分析**：事后比较、效应量等建议
- **Python函数**：对应的 scipy/statsmodels/pingouin 函数

## 应用场景

- **设计实验前**：规划该用什么分析方法
- **分析数据时**：确认检验选择是否正确
- **假设检查后**：数据不符合正态时找非参数备选
- **学习统计**：理解不同检验的适用条件

## 重要提示

- 本工具提供方法**推荐**，最终选择需结合具体研究情境
- 使用参数检验前务必检查前提假设（正态性、方差齐性等）
- 多重比较时记得做校正（Bonferroni、Tukey 等）
- 报告结果时应同时呈现效应量，而非仅看 p 值

## 系统要求

- Python 3.8 或更高版本
- 无需额外依赖（仅使用 Python 标准库）

## 关于本工具

为心理学及社会科学研究人员设计，帮助在统计方法选择上做出更稳妥的决策。

**作者**: @zhan599
**所属机构**: 华南师范大学 应用心理学系
**用途**: 研究方法决策、统计方法选择、教学辅助
