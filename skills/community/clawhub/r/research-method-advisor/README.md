# 研究方法决策助手

像决策树一样，根据研究特征自动推荐合适的统计检验方法。

## 功能特性

### 🌳 智能决策推荐
根据研究目的、因变量类型、组数、实验设计、假设是否满足，推荐最合适的统计检验。

### 📋 完整方法覆盖
- t 检验家族（单样本/独立/配对）
- 方差分析（单因素/多因素/重复测量）
- 非参数检验（Mann-Whitney/Kruskal-Wallis/Friedman 等）
- 相关分析（Pearson/Spearman）
- 回归分析（线性/逻辑/有序）
- 卡方检验

### 💡 贴心提示
每条推荐包含前提假设、参数/非参数备选、后续分析建议和对应 Python 函数。

## 快速开始

```python
from method_advisor import StatTestAdvisor

advisor = StatTestAdvisor()

result = advisor.recommend_test(
    goal="compare",
    dv_type="continuous",
    n_groups=2,
    design="independent"
)
print(result["推荐检验"])   # 独立样本 t 检验

# 或使用交互式引导
advisor.interactive_guide()
```

## 系统要求

- Python 3.8+
- 无需额外依赖（仅用标准库）

## 作者

@zhan599 - 华南师范大学应用心理学

## 许可证

MIT
