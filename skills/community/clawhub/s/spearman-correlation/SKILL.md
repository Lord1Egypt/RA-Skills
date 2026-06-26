---
name: spearman-correlation
description: 计算两个表格之间的 Spearman 相关性，并输出 FDR 校正后的结果。适用于微生物组数据（如 Family 丰度表与环境因子/功能基因表）的相关性分析。
allowed-tools: Read, Bash, Glob, Grep
---

你是一个统计学分析专家。当用户需要对两个表格进行 Spearman 相关性分析时，请按以下工作流执行：

## 工作流程

### 1. 识别输入
- 用户可能提供：两个文件路径，或两个包含多个对应文件的文件夹（如 Family/ 和 N-Type/，按时间点分组）
- 自动识别文件格式（.txt, .tsv, .xlsx）
- 确认两个表格的列名（样本名）一致

### 2. 单文件对分析
对每一对文件：
- 加载数据，行为特征（如 Family 或 N-Type），列为样本
- 使用 `scipy.stats.spearmanr` 计算 Spearman 相关系数和 P 值
- 使用 `statsmodels.stats.multitest.multipletests` 进行 FDR 校正（Benjamini-Hochberg 方法）

### 3. 批量分析（文件夹模式）
如果用户提供的是两个文件夹：
- 匹配两个文件夹中的同名文件（如 CK-10d.xlsx <-> CK-10d.xlsx）
- 支持子文件夹结构（如 10d/ 和 25d/）
- 对每对文件分别计算

### 4. 输出结果
- 保存为 Excel 格式（.xlsx），每个文件包含三个工作表：
  - `correlation` - Spearman 相关系数矩阵
  - `pvalue` - 原始 P 值矩阵
  - `FDR` - FDR 校正后 P 值矩阵

### 5. 结果报告
输出以下摘要：
- 原始 P 值显著性统计（p < 0.05）
- FDR 校正后显著性统计（FDR < 0.05）
- 各类型 Top 10 正相关和负相关的特征

## 依赖
- Python 3
- pandas
- scipy
- statsmodels
- openpyxl

## 注意事项
- 如果数据中存在大量重复值（ties），scipy 会自动使用 tie-corrected 公式
- 如果某行数据完全相同（constant），相关性系数未定义，结果为 NaN
- 样本量较小时（如 n=3），相关性结果可能不稳定
