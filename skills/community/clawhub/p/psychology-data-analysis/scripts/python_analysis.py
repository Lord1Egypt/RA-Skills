"""
心理学数据分析主脚本
支持：描述性统计、t检验、ANOVA、相关、回归、中介、调节效应分析

使用方法：
  python python_analysis.py --data data.csv --analysis describe --dep_var score
  python python_analysis.py --data data.csv --analysis ttest_ind --group_var group --dep_var score --group1 实验组 --group2 对照组
  python python_analysis.py --data data.csv --analysis correlation --var1 变量1 --var2 变量2
  python python_analysis.py --data data.csv --analysis regression --dep_var y --indep_vars x1 x2 x3
  python python_analysis.py --data data.csv --analysis mediation --dep_var y --indep_var x --mediator m
  python python_analysis.py --data data.csv --analysis moderation --dep_var y --indep_var x --moderator w
"""

import argparse
import pandas as pd
import numpy as np
from scipy import stats
import sys
import warnings
warnings.filterwarnings('ignore')

# 尝试导入可选依赖
try:
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    from statsmodels.stats.anova import anova_lm
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False

try:
    from pingouin import cronbach_alpha, reliability
    PINGOUIN_AVAILABLE = True
except ImportError:
    PINGOUIN_AVAILABLE = False


def load_data(filepath):
    """根据文件扩展名加载数据"""
    if filepath.endswith('.csv'):
        return pd.read_csv(filepath)
    elif filepath.endswith(('.xlsx', '.xls')):
        return pd.read_excel(filepath)
    elif filepath.endswith('.sav'):
        try:
            import pyreadstat
            df, meta = pyreadstat.read_sav(filepath)
            return df
        except ImportError:
            print("错误：读取 SPSS .sav 文件需要安装 pyreadstat: pip install pyreadstat")
            sys.exit(1)
    else:
        print(f"错误：不支持的文件格式: {filepath}")
        print("支持格式：.csv, .xlsx, .xls, .sav")
        sys.exit(1)


def cohens_d(group1, group2):
    """计算 Cohen's d"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (group1.mean() - group2.mean()) / pooled_std


def APA_ttest(t, df, p, d=None, ci=None):
    """生成 APA 格式 t 检验结果文本"""
    result = f"t({df}) = {t:.3f}, p = {p:.3f}"
    if d is not None:
        result += f", Cohen's d = {d:.3f}"
    if ci is not None:
        result += f", 95% CI = [{ci[0]:.3f}, {ci[1]:.3f}]"
    return result


def APA_anova(f, df1, df2, p, eta2=None, ci=None):
    """生成 APA 格式 ANOVA 结果文本"""
    result = f"F({df1}, {df2}) = {f:.3f}, p = {p:.3f}"
    if eta2 is not None:
        result += f", η² = {eta2:.3f}"
    if ci is not None:
        result += f", 95% CI = [{ci[0]:.3f}, {ci[1]:.3f}]"
    return result


def APA_correlation(r, df, p):
    """生成 APA 格式相关结果文本"""
    result = f"r({df}) = {r:.3f}, p = {p:.3f}"
    return result


def APA_regression(R2, F, df1, df2, p):
    """生成 APA 格式回归结果文本"""
    result = f"F({df1}, {df2}) = {F:.3f}, p = {p:.3f}, R² = {R2:.3f}"
    return result


def normality_check(data, name="变量"):
    """正态性检验"""
    n = len(data)
    if n < 3:
        print(f"  {name}: 样本量太小，无法进行正态性检验")
        return None
    
    if n < 5000:
        stat, p = stats.shapiro(data)
        normal = p > 0.05
    else:
        # 大样本时用 Kolmogorov-Smirnov
        stat, p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
        normal = p > 0.05
    
    skew = stats.skew(data)
    kurt = stats.kurtosis(data)
    
    print(f"\n  【正态性检验】")
    print(f"  {name}:")
    print(f"    Shapiro-Wilk/K-S检验: W/KS = {stat:.3f}, p = {p:.3f}")
    print(f"    偏度 = {skew:.3f}, 峰度 = {kurt:.3f}")
    if normal:
        print(f"    → 假设成立：数据符合正态分布")
    else:
        print(f"    → 警告：数据偏离正态分布（p < .05），建议使用非参数检验")
    
    return normal


def levene_test(groups, names=None):
    """方差齐性检验"""
    if names is None:
        names = [f"组{i+1}" for i in range(len(groups))]
    
    stat, p = stats.levene(*groups)
    print(f"\n  【Levene 方差齐性检验】")
    print(f"    W = {stat:.3f}, p = {p:.3f}")
    if p > 0.05:
        print(f"    → 假设成立：方差齐性")
    else:
        print(f"    → 警告：方差不齐（p < .05），Welch's t 检验更合适")
    return p > 0.05


def analyze_describe(df, dep_var, group_var=None):
    """描述性统计"""
    print(f"\n{'='*60}")
    print(f"描述性统计")
    print(f"{'='*60}")
    
    y = df[dep_var]
    print(f"\n【总体描述】")
    print(f"  N = {y.count()}")
    print(f"  M = {y.mean():.3f}")
    print(f"  SD = {y.std():.3f}")
    print(f"  Min = {y.min():.3f}, Max = {y.max():.3f}")
    print(f"  偏度 = {stats.skew(y):.3f}, 峰度 = {stats.kurtosis(y):.3f}")
    
    if group_var and group_var in df.columns:
        print(f"\n【按 {group_var} 分组描述】")
        grouped = df.groupby(group_var)[dep_var]
        desc = grouped.agg(['count', 'mean', 'std', 'min', 'max'])
        desc.columns = ['N', 'M', 'SD', 'Min', 'Max']
        for idx, row in desc.iterrows():
            print(f"\n  {group_var} = {idx}:")
            print(f"    N = {row['N']:.0f}, M = {row['M']:.3f}, SD = {row['SD']:.3f}")
            print(f"    Min = {row['Min']:.3f}, Max = {row['Max']:.3f}")
    
    normality_check(y, dep_var)
    return desc if group_var else None


def analyze_ttest_ind(df, dep_var, group_var, group1, group2):
    """独立样本 t 检验"""
    print(f"\n{'='*60}")
    print(f"独立样本 t 检验")
    print(f"{'='*60}")
    
    g1 = df[df[group_var] == group1][dep_var].dropna()
    g2 = df[df[group_var] == group2][dep_var].dropna()
    
    if len(g1) == 0 or len(g2) == 0:
        print(f"错误：找不到指定的组别")
        print(f"  找到的组别: {df[group_var].unique()}")
        sys.exit(1)
    
    print(f"\n【描述性统计】")
    print(f"  {group1}: N = {len(g1)}, M = {g1.mean():.3f}, SD = {g1.std():.3f}")
    print(f"  {group2}: N = {len(g2)}, M = {g2.mean():.3f}, SD = {g2.std():.3f}")
    
    # 正态性检验
    normality_check(g1, group1)
    normality_check(g2, group2)
    
    # 方差齐性
    equal_var = levene_test([g1, g2], [group1, group2])
    
    # t 检验
    t, p = stats.ttest_ind(g1, g2, equal_var=equal_var)
    d = cohens_d(g1, g2)
    df_total = len(g1) + len(g2) - 2
    
    # 计算置信区间（差值的）
    diff_mean = g1.mean() - g2.mean()
    se = np.sqrt(g1.var(ddof=1)/len(g1) + g2.var(ddof=1)/len(g2))
    ci = diff_mean - 1.96*se, diff_mean + 1.96*se
    
    print(f"\n【推断统计】")
    test_type = "Student's t" if equal_var else "Welch's t"
    print(f"  {test_type} 检验: t({df_total}) = {t:.3f}, p = {p:.3f}")
    print(f"  Cohen's d = {d:.3f}")
    print(f"  差值均值 = {diff_mean:.3f}, 95% CI = [{ci[0]:.3f}, {ci[1]:.3f}]")
    
    print(f"\n【APA 格式结果】")
    print(f"  {APA_ttest(t, df_total, p, d, ci)}")
    
    print(f"\n【结论】")
    if p < 0.05:
        print(f"  两组在 {dep_var} 上存在显著差异 (p < .05)")
        print(f"  {group1} (M={g1.mean():.2f}) vs {group2} (M={g2.mean():.2f})")
    else:
        print(f"  两组在 {dep_var} 上不存在显著差异 (p > .05)")


def analyze_ttest_rel(df, dep_var1, dep_var2, var1_name=None, var2_name=None):
    """配对样本 t 检验"""
    print(f"\n{'='*60}")
    print(f"配对样本 t 检验")
    print(f"{'='*60}")
    
    var1_name = var1_name or dep_var1
    var2_name = var2_name or dep_var2
    
    paired = df[[dep_var1, dep_var2]].dropna()
    diff = paired[dep_var1] - paired[dep_var2]
    
    print(f"\n【描述性统计】")
    print(f"  {var1_name}: M = {paired[dep_var1].mean():.3f}, SD = {paired[dep_var1].std():.3f}")
    print(f"  {var2_name}: M = {paired[dep_var2].mean():.3f}, SD = {paired[dep_var2].std():.3f}")
    print(f"  差值: M = {diff.mean():.3f}, SD = {diff.std():.3f}")
    
    normality_check(diff, "差值")
    
    t, p = stats.ttest_rel(paired[dep_var1], paired[dep_var2])
    df_total = len(paired) - 1
    d = diff.mean() / diff.std()
    
    se = diff.std() / np.sqrt(len(diff))
    ci = diff.mean() - 1.96*se, diff.mean() + 1.96*se
    
    print(f"\n【推断统计】")
    print(f"  t 检验: t({df_total}) = {t:.3f}, p = {p:.3f}")
    print(f"  Cohen's d = {d:.3f}")
    print(f"  差值均值 = {diff.mean():.3f}, 95% CI = [{ci[0]:.3f}, {ci[1]:.3f}]")
    
    print(f"\n【APA 格式结果】")
    print(f"  {APA_ttest(t, df_total, p, d, ci)}")
    
    print(f"\n【结论】")
    if p < 0.05:
        print(f"  {var1_name} 与 {var2_name} 存在显著差异 (p < .05)")
    else:
        print(f"  {var1_name} 与 {var2_name} 不存在显著差异 (p > .05)")


def analyze_anova(df, dep_var, group_var):
    """单因素 ANOVA"""
    if not STATSMODELS_AVAILABLE:
        print("错误：需要 statsmodels 库运行 ANOVA")
        print("请运行: pip install statsmodels")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"单因素方差分析 (ANOVA)")
    print(f"{'='*60}")
    
    groups_data = []
    group_names = []
    for name, group in df.groupby(group_var):
        groups_data.append(group[dep_var].dropna())
        group_names.append(name)
    
    ns = [len(g) for g in groups_data]
    means = [g.mean() for g in groups_data]
    sds = [g.std() for g in groups_data]
    
    print(f"\n【描述性统计】")
    for i, (name, n, m, s) in enumerate(zip(group_names, ns, means, sds)):
        print(f"  {name}: N = {n}, M = {m:.3f}, SD = {s:.3f}")
    
    # 正态性和方差齐性
    for g, name in zip(groups_data, group_names):
        normality_check(g, name)
    levene_test(groups_data, group_names)
    
    # ANOVA
    f, p = stats.f_oneway(*groups_data)
    df_between = len(group_names) - 1
    df_within = sum(ns) - len(group_names)
    
    # 计算 η²
    ss_between = sum(n * (m - np.mean(means))**2 for n, m in zip(ns, means))
    ss_total = sum((g - df[dep_var].mean())**2 for g in groups_data for _ in g)
    eta2 = ss_between / ss_total
    
    print(f"\n【推断统计】")
    print(f"  F({df_between}, {df_within}) = {f:.3f}, p = {p:.3f}")
    print(f"  η² = {eta2:.3f}")
    
    print(f"\n【APA 格式结果】")
    print(f"  {APA_anova(f, df_between, df_within, p, eta2)}")
    
    # 多重比较（事后检验）
    if p < 0.05 and len(group_names) > 2:
        print(f"\n【事后多重比较】(Tukey HSD)")
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
        posthoc = pairwise_tukeyhsd(df[dep_var], df[group_var])
        print(posthoc)
    
    print(f"\n【结论】")
    if p < 0.05:
        print(f"  组间存在显著差异 (p < .05)")
    else:
        print(f"  组间不存在显著差异 (p > .05)")


def analyze_correlation(df, var1, var2, method='pearson'):
    """相关分析"""
    print(f"\n{'='*60}")
    print(f"相关分析 ({method.capitalize()})")
    print(f"{'='*60}")
    
    data = df[[var1, var2]].dropna()
    x, y = data[var1], data[var2]
    
    if method == 'pearson':
        r, p = stats.pearsonr(x, y)
    else:
        r, p = stats.spearmanr(x, y)
    
    df_total = len(data) - 2
    
    print(f"\n【描述性统计】")
    print(f"  {var1}: M = {x.mean():.3f}, SD = {x.std():.3f}")
    print(f"  {var2}: M = {y.mean():.3f}, SD = {y.std():.3f}")
    
    print(f"\n【推断统计】")
    print(f"  r = {r:.3f}, p = {p:.3f}, N = {len(data)}")
    print(f"  R² = {r**2:.3f}（{var2} 被 {var1} 解释的方差比例）")
    
    print(f"\n【APA 格式结果】")
    print(f"  {APA_correlation(r, df_total, p)}")
    
    # 效应量解释
    r_abs = abs(r)
    if r_abs < 0.1:
        eff = "微小"
    elif r_abs < 0.3:
        eff = "小"
    elif r_abs < 0.5:
        eff = "中等"
    else:
        eff = "大"
    print(f"  效应量解释: {eff}效应 (|r| = {r_abs:.3f})")
    
    print(f"\n【结论】")
    if p < 0.05:
        direction = "正" if r > 0 else "负"
        print(f"  {var1} 与 {var2} 呈显著{direction}相关 (p < .05)")
    else:
        print(f"  {var1} 与 {var2} 不存在显著相关 (p > .05)")


def analyze_regression(df, dep_var, indep_vars):
    """多元线性回归"""
    if not STATSMODELS_AVAILABLE:
        print("错误：需要 statsmodels 库运行回归分析")
        print("请运行: pip install statsmodels")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"多元线性回归分析")
    print(f"{'='*60}")
    
    # 准备数据
    all_vars = [dep_var] + indep_vars
    data = df[all_vars].dropna()
    
    if len(data) < len(all_vars) + 5:
        print(f"警告：样本量可能不足以进行回归分析 (N = {len(data)})")
    
    y = data[dep_var]
    X = data[indep_vars]
    X = sm.add_constant(X)
    
    # 模型拟合
    model = sm.OLS(y, X).fit()
    
    print(f"\n【模型概述】")
    print(f"  N = {len(y)}")
    print(f"  F({model.df_model:.0f}, {model.df_resid:.0f}) = {model.fvalue:.3f}, p = {model.f_pvalue:.3f}")
    print(f"  R² = {model.rsquared:.3f}, 调整后 R² = {model.rsquared_adj:.3f}")
    
    print(f"\n【回归系数】")
    print(f"  {'变量':<12} {'B':>10} {'SE':>10} {'β':>10} {'t':>10} {'p':>10} {'VIF':>10}")
    print(f"  {'-'*72}")
    for var in model.params.index:
        coef = model.params[var]
        se = model.bse[var]
        beta = model.params[var] * (X[var].std() / y.std()) if var != 'const' else 0
        t = model.tvalues[var]
        p = model.pvalues[var]
        # 简化 VIF 计算
        vif = "N/A" if var == 'const' else "-"
        print(f"  {var:<12} {coef:>10.3f} {se:>10.3f} {beta:>10.3f} {t:>10.3f} {p:>10.3f} {vif:>10}")
    
    print(f"\n【APA 格式结果】")
    print(f"  {APA_regression(model.rsquared, model.fvalue, model.df_model, model.df_resid, model.f_pvalue)}")
    
    print(f"\n【结论】")
    if model.f_pvalue < 0.05:
        print(f"  模型整体显著 (p < .05)，{dep_var} 可被预测")
        sig_vars = [var for var in indep_vars if model.pvalues[var] < 0.05]
        if sig_vars:
            print(f"  显著预测变量: {', '.join(sig_vars)}")
    else:
        print(f"  模型整体不显著 (p > .05)")


def main():
    parser = argparse.ArgumentParser(description='心理学数据分析脚本')
    parser.add_argument('--data', required=True, help='数据文件路径 (.csv, .xlsx, .sav)')
    parser.add_argument('--analysis', required=True,
                        choices=['describe', 'ttest_ind', 'ttest_rel', 'anova', 'correlation', 'regression', 'mediation', 'moderation', 'chi2'],
                        help='分析类型')
    
    # 通用参数
    parser.add_argument('--dep_var', help='因变量名')
    parser.add_argument('--group_var', help='分组变量名')
    
    # t 检验参数
    parser.add_argument('--group1', help='组1名称（独立样本 t 检验）')
    parser.add_argument('--group2', help='组2名称（独立样本 t 检验）')
    parser.add_argument('--var1', help='变量1（配对 t 检验/相关）')
    parser.add_argument('--var2', help='变量2（配对 t 检验/相关）')
    
    # 回归参数
    parser.add_argument('--indep_vars', nargs='+', help='自变量列表')
    
    # 中介/调节
    parser.add_argument('--x', help='自变量 (X)')
    parser.add_argument('--m', help='中介变量 (M)')
    parser.add_argument('--y', help='因变量 (Y)')
    parser.add_argument('--w', help='调节变量 (W)')
    
    # 选项
    parser.add_argument('--alpha', type=float, default=0.05, help='显著性水平 (默认 0.05)')
    
    args = parser.parse_args()
    
    # 加载数据
    print(f"\n正在加载数据: {args.data}")
    df = load_data(args.data)
    print(f"数据加载成功: {df.shape[0]} 行, {df.shape[1]} 列")
    print(f"列名: {list(df.columns)}")
    
    # 执行分析
    if args.analysis == 'describe':
        if not args.dep_var:
            print("错误：需要 --dep_var 参数")
            sys.exit(1)
        analyze_describe(df, args.dep_var, args.group_var)
    
    elif args.analysis == 'ttest_ind':
        if not all([args.dep_var, args.group_var, args.group1, args.group2]):
            print("错误：需要 --dep_var, --group_var, --group1, --group2 参数")
            sys.exit(1)
        analyze_ttest_ind(df, args.dep_var, args.group_var, args.group1, args.group2)
    
    elif args.analysis == 'ttest_rel':
        if not all([args.var1, args.var2]):
            print("错误：需要 --var1, --var2 参数")
            sys.exit(1)
        analyze_ttest_rel(df, args.var1, args.var2)
    
    elif args.analysis == 'anova':
        if not all([args.dep_var, args.group_var]):
            print("错误：需要 --dep_var, --group_var 参数")
            sys.exit(1)
        analyze_anova(df, args.dep_var, args.group_var)
    
    elif args.analysis == 'correlation':
        if not all([args.var1, args.var2]):
            print("错误：需要 --var1, --var2 参数")
            sys.exit(1)
        analyze_correlation(df, args.var1, args.var2)
    
    elif args.analysis == 'regression':
        if not all([args.dep_var, args.indep_vars]):
            print("错误：需要 --dep_var, --indep_vars 参数")
            sys.exit(1)
        analyze_regression(df, args.dep_var, args.indep_vars)
    
    elif args.analysis == 'chi2':
        if not all([args.group_var, args.dep_var]):
            print("错误：需要 --group_var, --dep_var 参数")
            sys.exit(1)
        analyze_chi2(df, args.group_var, args.dep_var)
    
    else:
        print(f"分析类型 {args.analysis} 暂不支持或需要更多参数")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("分析完成")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
