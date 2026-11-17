---
name: 统计假设检验技能
slug: hypothesis-testing
displayName: 统计假设检验技能
description: 统计假设检验工具；支持正态性检验(Shapiro-Wilk/K-S)、t检验(单样本/独立/配对)、卡方检验(拟合优度/独立性)、ANOVA、Levene检验、Mann-Whitney U检验；自动计算统计量、p值、置信区间与效应量；提供结果解释指南
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 假设检验工具

## 任务目标
- 本Skill用于:对样本数据进行统计假设检验，判断样本与总体、样本与样本之间是否存在显著差异
- 能力包含:正态性检验(Shapiro-Wilk/K-S)、t检验(单样本/独立/配对)、卡方检验(拟合优度/独立性)、ANOVA、方差齐性检验、非参数检验
- 触发条件:用户需要"检验正态性"、"比较两组数据"、"验证比例是否符合预期"、"判断多组均值是否相等"

## 前置准备
- 依赖包:numpy, pandas, scipy
- 数据准备:CSV/TXT/Excel文件或逗号分隔的数值列表

## 操作步骤

### 1. 数据准备
确保数据格式符合要求:
- 数值型数据
- 缺失值已处理
- 异常值已检查(可选)

### 2. 选择检验方法
根据研究问题选择合适的检验:

| 目的 | 检验方法 |
|------|----------|
| 判断数据是否正态 | Shapiro-Wilk / K-S检验 |
| 比较样本均值与总体均值 | 单样本t检验 |
| 比较两组独立样本 | 独立样本t检验 / Mann-Whitney U |
| 比较配对样本 | 配对样本t检验 |
| 检验分类变量关联 | 卡方独立性检验 |
| 检验观测与期望频数 | 卡方拟合优度检验 |
| 比较三组及以上均值 | 单因素ANOVA |
| 检验方差齐性 | Levene检验 |

### 3. 执行检验
调用脚本进行分析:

```bash
python scripts/hypothesis_test.py --test <检验类型> --data1 <数据> [参数]
```

### 4. 解读结果
- 查看p值与显著性水平α的比较
- 结合效应量评估实际意义
- 参考置信区间
- 使用 [references/interpretation_guide.md](references/interpretation_guide.md) 获取详细解释

## 使用示例

### 示例1:正态性检验
- 场景:检验某班级数学成绩是否服从正态分布
- 输入:成绩数据 [85, 90, 78, 92, 88, 76, 95, 82, 89, 91]
- 命令:
  ```bash
  python scripts/hypothesis_test.py --test shapiro --data1 "85,90,78,92,88,76,95,82,89,91"
  ```
- 关键要点:p > 0.05时认为数据服从正态分布，可进一步使用参数检验

### 示例2:两独立样本t检验
- 场景:比较实验组与对照组的疗效差异
- 输入:实验组 [85, 88, 90, 92, 87], 对照组 [78, 82, 80, 76, 79]
- 命令:
  ```bash
  python scripts/hypothesis_test.py --test two_sample_t --data1 "85,88,90,92,87" --data2 "78,82,80,76,79"
  ```
- 关键要点:报告Cohen's d评估效应大小；先做Levene检验验证方差齐性

### 示例3:卡方拟合优度检验
- 场景:检验骰子是否公平(期望每个面出现概率相等)
- 输入:观测频数 [18, 22, 16, 20, 15, 19] (每个面出现次数)
- 命令:
  ```bash
  python scripts/hypothesis_test.py --test chi_square_goodness --data1 "18,22,16,20,15,19"
  ```
- 关键要点:期望频数默认相等；可指定--expected自定义期望分布

### 示例4:单因素ANOVA
- 场景:比较三种教学方法的效果
- 输入:方法A [85, 90, 88], 方法B [78, 82, 80], 方法C [92, 95, 90]
- 命令:
  ```bash
  python scripts/hypothesis_test.py --test anova --data1 "85,90,88" --data2 "78,82,80;92,95,90"
  ```
- 关键要点:ANOVA显著后需进行事后检验(如Tukey HSD)确定具体哪些组有差异

### 示例5:从文件读取数据
- 场景:数据存储在CSV文件中
- 命令:
  ```bash
  python scripts/hypothesis_test.py --test shapiro --data1 ./data/grades.csv
  ```
- 关键要点:支持.csv/.txt/.xlsx文件；脚本会读取第一列数据

## 检验参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --test | 检验类型 | 必需 |
| --data1 | 第一组数据 | 必需 |
| --data2 | 第二组数据(两样本检验) | 可选 |
| --alpha | 显著性水平 | 0.05 |
| --pop_mean | 总体均值(单样本t检验) | 样本均值 |
| --expected | 期望频数(卡方检验) | 均匀分布 |
| --output | 输出JSON文件路径 | 输出到stdout |

## 支持的检验类型

| test值 | 检验名称 | 适用场景 |
|--------|----------|----------|
| shapiro | Shapiro-Wilk正态性检验 | 小样本(n<5000)正态判断 |
| ks | K-S正态性检验 | 大样本正态判断 |
| one_sample_t | 单样本t检验 | 与已知总体比较 |
| two_sample_t | 独立样本t检验 | 两独立组比较 |
| paired_t | 配对样本t检验 | 配对/重复测量比较 |
| chi_square_goodness | 卡方拟合优度检验 | 观测vs期望频数 |
| chi_square_independence | 卡方独立性检验 | 两分类变量关联 |
| anova | 单因素ANOVA | 三组及以上均值比较 |
| levene | Levene方差齐性检验 | 方差齐性判断 |
| mann_whitney | Mann-Whitney U检验 | 两组非参数比较 |

## 结果输出说明

脚本输出JSON格式结果，包含:
- `test_name`: 检验名称
- `statistic`: 检验统计量(t值/F值/χ²值等)
- `p_value`: p值
- `df`: 自由度
- `alpha`: 显著性水平
- `confidence_interval`: 置信区间(适用时)
- `effect_size`: 效应量(适用时)
- `conclusion`: 结论描述
- `interpretation`: 解释字符串

## 资源索引

- 脚本:见 [scripts/hypothesis_test.py](scripts/hypothesis_test.py)(用途:执行各种假设检验计算，参数定义见上方检验参数说明)
- 参考:见 [references/interpretation_guide.md](references/interpretation_guide.md)(何时读取:需要解读检验结果或了解检验方法适用场景时)

## 注意事项

1. **正态性前提**:t检验和ANOVA要求数据近似正态分布；大样本(n>30)时中心极限定理可缓解此要求
2. **方差齐性**:独立样本t检验和ANOVA要求方差齐性；可先做Levene检验
3. **样本量影响**:p值受样本量影响，大样本时需关注效应量
4. **多重比较**:进行多次检验时需校正显著性水平(如Bonferroni校正)
5. **非参数替代**:数据严重偏态或方差不齐时，使用Mann-Whitney U或Wilcoxon符号秩检验
6. **因果关系**:假设检验仅判断差异显著性，不能推断因果关系

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
