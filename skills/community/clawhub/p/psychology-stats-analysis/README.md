# 心理学统计分析助手

为心理学研究设计的全面统计分析工具，特别关注社会认知和实验心理学。

## 功能特性

### 📊 描述统计
- 计算均值、标准差、中位数和百分位数
- 生成频数分布
- 计算置信区间

### 🔬 假设检验
- **t检验**（独立样本、配对、单样本）
- **方差分析（ANOVA）**（单因素、双因素、被试内、混合设计）
- **卡方检验**用于分类数据
- **相关与回归分析**
- **事后检验**（Tukey、Bonferroni等）

### 📈 效应量与功效
- Cohen's d、f等效应量指标
- 统计功效分析
- 基于效应量的样本量推荐

### 🎯 实验设计指导
- 凝视线索和启动效应范式的设计验证
- 对平衡和拉丁方设计
- 随机化与刺激顺序

### 📉 数据可视化
- 生成出版级别的图表
- 效应量可视化
- 阶乘设计交互作用图

## 使用示例

```python
from psychology_stats import PsychologyAnalyzer

analyzer = PsychologyAnalyzer()

# 描述统计
stats = analyzer.descriptive_stats(数据, by_group='情绪')

# 独立t检验
t_result = analyzer.independent_t_test(控制组, 实验组, paired=False)

# 双因素方差分析及效应量
anova_result = analyzer.two_way_anova(数据, dv='反应时', factors=['情绪', '同余性'])

# 功效分析
样本量 = analyzer.power_analysis(effect_size=0.4, alpha=0.05, power=0.8)
```

## 应用领域

- **社会认知研究**：分析凝视线索效应、心理理论任务
- **隐性学习**：处理启动和隐性记忆范式数据
- **实验心理学**：阶乘设计、混合被试分析
- **快速数据检查**：验证假设前提（正态性、方差齐性）

## 系统要求

- Python 3.8+
- numpy、scipy、pandas、matplotlib

## 作者

@zhan599 - 华南师范大学应用心理学

## 许可证

MIT
