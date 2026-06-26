# Python 数据分析指南

基于 pandas + scipy + statsmodels + scikit-learn。

## 环境准备

```bash
pip install pandas scipy statsmodels scikit-learn matplotlib seaborn openpyxl
```

## 数据加载

```python
import pandas as pd
import numpy as np

# CSV
df = pd.read_csv('data.csv')

# Excel
df = pd.read_excel('data.xlsx')

# SPSS (.sav) - 需要 pyreadstat
import pyreadstat
df, meta = pyreadstat.read_sav('data.sav')

# 查看数据结构
print(df.head())
print(df.dtypes)
print(df.describe())
```

## 描述性统计

```python
# 基本统计
df.describe()

# 按组统计
df.groupby('group').mean()
df.groupby('group')['score'].agg(['mean', 'std', 'n'])

# 频数
df['group'].value_counts()
```

## 假设检验

### t 检验（独立样本）

```python
from scipy import stats

# 独立样本 t 检验
group1 = df[df['group'] == '实验组']['score']
group2 = df[df['group'] == '对照组']['score']

t, p = stats.ttest_ind(group1, group2)
print(f"t = {t:.3f}, p = {p:.3f}")

# 方差不齐时（Welch's t）
t, p = stats.ttest_ind(group1, group2, equal_var=False)
```

### t 检验（配对样本）

```python
pre = df[df['time'] == '前测']['score']
post = df[df['time'] == '后测']['score']

t, p = stats.ttest_rel(pre, post)
```

### ANOVA

```python
# 单因素 ANOVA
from scipy import stats

# 被试间（Wide format）
groups = [df[df['group'] == g]['score'] for g in df['group'].unique()]
f, p = stats.f_oneway(*groups)

# 重复测量 ANOVA - 使用 statsmodels
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols

model = ols('score ~ C(time)', data=df).fit()
anova = anova_lm(model, typ=2)

# 混合 ANOVA（被试间 + 被试内）
model = ols('score ~ C(group) * C(time)', data=df).fit()
anova = anova_lm(model, typ=2)
```

### 相关分析

```python
# Pearson 相关
r, p = stats.pearsonr(df['var1'], df['var2'])

# Spearman 相关
r, p = stats.spearmanr(df['var1'], df['var2'])

# 偏相关
from statsmodels.stats.correlation_tools import partial_corr
result = partial_corr(df, x='var1', y='var2', cov='control_var')
```

### 回归分析

```python
import statsmodels.api as sm

# 多元线性回归
X = df[['x1', 'x2', 'x3']]
X = sm.add_constant(X)  # 添加截距
y = df['y']

model = sm.OLS(y, X).fit()
print(model.summary())

# 虚拟变量（分类自变量）
X = pd.get_dummies(df['group'], drop_first=True)
X = sm.add_constant(X)
```

### 中介效应

```python
# 使用 statsmodels 的 medians
from statsmodels.stats.mediation import Mediation

# 参考： Hayes PROCESS style 或手动 Bootstrap
# 简化版手动实现：
import numpy as np

def bootstrap_mediation(X, M, Y, n_bootstrap=5000):
    indirect_effects = []
    for _ in range(n_bootstrap):
        idx = np.random.choice(len(X), len(X), replace=True)
        # a path
        a = sm.OLS(M[idx], sm.add_constant(X[idx])).fit().params[1]
        # b path
        b = sm.OLS(Y[idx], sm.add_constant(np.column_stack([X[idx], M[idx]]))).fit().params[1]
        indirect_effects.append(a * b)
    
    indirect = np.percentile(indirect_effects, [2.5, 97.5])
    return np.mean(indirect_effects), indirect
```

### 调节效应

```python
# 层次回归
X_centered = df[['x', 'w']]
X_centered = X_centered - X_centered.mean()

model1 = sm.OLS(Y, sm.add_constant(X_centered[['x']])).fit()
model2 = sm.OLS(Y, sm.add_constant(X_centered)).fit()

# 加入交互项
X_centered['xw'] = X_centered['x'] * X_centered['w']
model3 = sm.OLS(Y, sm.add_constant(X_centered)).fit()

# 比较模型
from scipy import stats
f = ((model2.ssr - model3.ssr) / model3.df_resid) / (model3.ssr / model3.df_resid)
p = 1 - stats.f.cdf(f, model2.df_resid - model3.df_resid, model3.df_resid)
```

## 效应量

```python
# Cohen's d
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (group1.mean() - group2.mean()) / pooled_std

# Pearson r
def r_from_t(t, df):
    return np.sqrt(t**2 / (t**2 + df))
```

## 正态性检验

```python
from scipy import stats

# Shapiro-Wilk（样本量 < 5000）
stat, p = stats.shapiro(df['score'])

# 查看偏度和峰度
print(f"Skewness: {df['score'].skew():.3f}")
print(f"Kurtosis: {df['score'].kurtosis():.3f}")
```

## 方差齐性检验

```python
# Levene 检验
stat, p = stats.levene(*groups)
```

## 可视化

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 箱线图
sns.boxplot(x='group', y='score', data=df)
plt.show()

# 散点图
sns.scatterplot(x='var1', y='var2', data=df)
plt.show()
```

## 输出 APA 格式

```python
def apa_ttest(t, df, p, d=None):
    result = f"t({df}) = {t:.3f}, p = {p:.3f}"
    if d:
        result += f", Cohen's d = {d:.3f}"
    return result

def apa_anova(f, df_between, df_error, p, eta2=None):
    result = f"F({df_between}, {df_error}) = {f:.3f}, p = {p:.3f}"
    if eta2:
        result += f", η² = {eta2:.3f}"
    return result
```

## 完整分析脚本模板

```python
"""
心理学数据分析脚本模板
使用方法: python python_analysis.py --data data.csv --analysis anova --group_var group --dep_var score
"""

import argparse
import pandas as pd
import numpy as np
from scipy import stats
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='数据文件路径')
    parser.add_argument('--analysis', required=True, 
                        choices=['ttest_ind', 'ttest_rel', 'anova', 'correlation', 'regression', 'describe'],
                        help='分析类型')
    parser.add_argument('--group_var', help='分组变量名')
    parser.add_argument('--dep_var', required=True, help='因变量名')
    parser.add_argument('--group1', help='组1名称')
    parser.add_argument('--group2', help='组2名称')
    args = parser.parse_args()
    
    # 加载数据
    if args.data.endswith('.csv'):
        df = pd.read_csv(args.data)
    elif args.data.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(args.data)
    else:
        print("不支持的文件格式，请使用 CSV 或 Excel 文件")
        sys.exit(1)
    
    y = df[args.dep_var]
    
    if args.analysis == 'describe':
        print("描述性统计:")
        print(df[args.dep_var].describe())
        if args.group_var:
            print("\n按组描述性统计:")
            print(df.groupby(args.group_var)[args.dep_var].describe())
    
    elif args.analysis == 'ttest_ind':
        g1 = df[df[args.group_var] == args.group1][args.dep_var]
        g2 = df[df[args.group_var] == args.group2][args.dep_var]
        t, p = stats.ttest_ind(g1, g2)
        # 效应量 Cohen's d
        pooled_std = np.sqrt(((len(g1)-1)*g1.std()**2 + (len(g2)-1)*g2.std()**2) / (len(g1)+len(g2)-2))
        d = (g1.mean() - g2.mean()) / pooled_std
        print(f"独立样本 t 检验: t = {t:.3f}, df = {len(g1)+len(g2)-2}, p = {p:.3f}, Cohen's d = {d:.3f}")
        print(f"组1 (M={g1.mean():.2f}, SD={g1.std():.2f}), 组2 (M={g2.mean():.2f}, SD={g2.std():.2f})")
    
    elif args.analysis == 'correlation':
        var1 = input("请输入第一个变量名: ")
        var2 = input("请输入第二个变量名: ")
        r, p = stats.pearsonr(df[var1], df[var2])
        print(f"Pearson 相关: r = {r:.3f}, p = {p:.3f}")

if __name__ == '__main__':
    main()
```

## SPSS 语法导出（Python 生成）

```python
def generate_spss_syntax(analysis_type, variables):
    """生成 SPSS 语法"""
    syntax_map = {
        'ttest_ind': f"T-TEST GROUPS={variables['group']}(1,2)\n  /VARIABLES={variables['dep']}.",
        'anova': f"ONEWAY {variables['dep']} BY {variables['group']}(1,3)\n  /STATISTICS=DESCRIPTIVES EFFSIZE.",
        'correlation': f"CORRELATIONS\n  /VARIABLES={variables['var1']} {variables['var2']}."
    }
    return syntax_map.get(analysis_type, "")
```
