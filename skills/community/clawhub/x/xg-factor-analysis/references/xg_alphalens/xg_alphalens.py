"""
小果因子分析系统
作者:小果
微信:xg_quant
"""
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, ttest_1samp, jarque_bera
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
from xg_data.xg_data import xg_data
import quantstats as qs
from scipy.stats import spearmanr
# ========== 全局设置 ==========
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']  # 纯英文字体
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import alphalens as al
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
class xg_alphalens:
    def __init__(self,
            factor_data='',
            quantiles=5, 
            periods=(1,5,10), 
            max_loss=0.95):
        '''
        小果因子分析框架
        作者:小果
        微信:xg_quant
        数据模块参考
        import pandas as pd
        import numpy as np
        import alphalens as al
        # 1. 数据生成函数
        # ============================================================
        def generate_synthetic_data(start_date='2024-01-01', end_date='2024-12-31',
                                    n_stocks=30, seed=42):
            """
            生成模拟的因子数据和价格数据
            返回: (factor_df, price_df, factor_series, factor_data)
            """
            np.random.seed(seed)
            dates = pd.date_range(start_date, end_date, freq='B')
            stocks = [f'Stock_{i:03d}' for i in range(n_stocks)]

            factor_df = pd.DataFrame(index=dates, columns=stocks)
            price_df = pd.DataFrame(index=dates, columns=stocks)

            for stock in stocks:
                trend = np.linspace(0, 1, len(dates)) * 0.3
                style = np.random.randn() * 0.5
                factor_df[stock] = np.random.randn(len(dates)) + trend + style
                ret = np.random.randn(len(dates)) * 0.02
                ret += factor_df[stock].shift(1).fillna(0) * 0.01
                price_df[stock] = 100 * (1 + ret).cumprod()

            factor_series = factor_df.stack()
            factor_series.index.names = ['date', 'asset']
            return factor_df, price_df, factor_series
        factor_df, price_df, factor_series=generate_synthetic_data()
        print(factor_df)
        print(price_df)
        print(factor_series)
        def clean_factor_data(factor_series, price_df, quantiles=5, periods=(1,5,10), max_loss=0.95):
            """数据清洗与对齐，返回 Alphalens 格式的 factor_data"""
            print("正在清洗数据...")
            factor_data = al.utils.get_clean_factor_and_forward_returns(
                factor=factor_series,
                prices=price_df,
                quantiles=quantiles,
                periods=periods,
                max_loss=max_loss,
            )
            print(f"数据清洗完成，形状: {factor_data.shape}\n")
            return factor_data
        factor_data=clean_factor_data(factor_series, price_df)
        print(factor_data)

                            Stock_000  Stock_001  Stock_002  Stock_003  ...  Stock_026  Stock_027  Stock_028  Stock_029
        2024-01-01   0.110093  -2.529983   0.083022  -1.632953  ...   1.942231   1.057527   0.183786   0.504274
        2024-01-02   0.897195  -0.853207   0.182398   1.148068  ...   1.532962  -2.310305  -0.122749  -0.064843
        2024-01-03   1.773686  -0.640420  -0.049809  -0.750113  ...  -0.039556  -2.038576   0.587019  -0.376311
        2024-01-04   0.017652  -1.803309  -0.859638  -0.824625  ...   0.665258  -0.919275  -1.693212  -0.110079
        2024-01-05   0.018818  -0.259251  -0.979807   0.187346  ...  -0.123150  -0.237824   1.478274  -0.005144
        ...               ...        ...        ...        ...  ...        ...        ...        ...        ...
        2024-12-25   0.987579   0.003547   1.068517   0.564706  ...  -0.191679   0.104973  -0.520866  -0.228298
        2024-12-26   1.319543  -0.046099   0.458469  -0.333706  ...   1.807956   0.054058   0.400666   0.685731
        2024-12-27  -0.380872   0.476041  -0.040107   0.641384  ...  -0.372881   1.995432   0.748402  -0.019568
        2024-12-30   0.487682   0.230332   0.803836  -0.862696  ...   1.904541   0.110783  -0.006551  -1.284361
        2024-12-31  -2.692910  -0.143261   1.377426   0.390739  ...   2.112700  -0.842602   0.409029   3.135493

        [262 rows x 30 columns]
                    Stock_000  Stock_001   Stock_002   Stock_003  ...   Stock_026  Stock_027   Stock_028   Stock_029
        2024-01-01   97.951225  99.859669  101.115621   99.933540  ...   96.098199  99.435846   99.924171  100.532356       
        2024-01-02   97.564275  94.015975  101.220505   97.885716  ...   98.142202  98.229354  100.304720  101.263891       
        2024-01-03   96.004835  94.021644   98.749435   98.757871  ...   98.862142  98.427353   99.779486   98.974623       
        2024-01-04  100.842047  93.810054   96.596662   94.300126  ...   93.065693  97.551889  100.401076   99.118236       
        2024-01-05   97.975480  92.627905   95.176606   92.487607  ...   90.995889  98.848893  104.118796   98.683596       
        ...                ...        ...         ...         ...  ...         ...        ...         ...         ...       
        2024-12-25  272.539526  27.476127  100.556292  147.096057  ...  274.315138  50.355926  104.078010   76.396566       
        2024-12-26  278.192811  27.835568   99.108219  149.899218  ...  281.793219  50.688182  106.212287   78.487227       
        2024-12-27  278.176941  26.945140  100.144479  146.185583  ...  293.735862  49.931971  105.232252   80.497842       
        2024-12-30  280.291990  27.869122   97.387230  142.580451  ...  303.807760  52.023912  103.619299   82.075302       
        2024-12-31  277.380216  28.702552   99.078550  143.682717  ...  299.943588  50.577639  104.251072   80.103187       

        [262 rows x 30 columns]
        date        asset
        2024-01-01  Stock_000    0.110093
                    Stock_001   -2.529983
                    Stock_002    0.083022
                    Stock_003   -1.632953
                    Stock_004   -0.713847
                                ...
        2024-12-31  Stock_025    0.742352
                    Stock_026    2.112700
                    Stock_027   -0.842602
                    Stock_028    0.409029
                    Stock_029    3.135493
        Length: 7860, dtype: float64
        正在清洗数据...
        Dropped 3.8% entries from factor data: 3.8% in forward returns computation and 0.0% in binning phase (set max_loss=0 to see potentially suppressed Exceptions).
        max_loss is 95.0%, not exceeded: OK!
        数据清洗完成，形状: (7560, 5)

                                    1D        5D       10D    factor  factor_quantile
        date       asset
        2024-01-01 Stock_000 -0.003950 -0.008367  0.049429  0.110093                3
                Stock_001 -0.058519 -0.098510 -0.158441 -2.529983                1
                Stock_002  0.001037 -0.079432 -0.059240  0.083022                3
                Stock_003 -0.020492 -0.071056 -0.051005 -1.632953                1
                Stock_004 -0.019724 -0.042090 -0.014854 -0.713847                2
        ...                        ...       ...       ...       ...              ...
        2024-12-17 Stock_025 -0.020203 -0.056604 -0.159107 -1.433412                1
                Stock_026  0.008371  0.033508  0.101387  0.430612                3
                Stock_027 -0.003978 -0.018739 -0.040694 -0.954174                1
                Stock_028  0.041493  0.039548  0.040997  0.810764                4
                Stock_029 -0.016552 -0.011229  0.044310  1.133899                5

        [7560 rows x 5 columns]
        '''
        self.factor_data=factor_data
        self.quantiles=quantiles
        self.periods=periods
        self.max_loss=max_loss
        self.al=al
        self.xg_data=xg_data()
        self.qs=qs
    def get_read_tdx_data(self,path):
        '''
        读取通达信数据
        '''
        try:
            stock_list=[]
            with open(r'{}'.format(path)) as p:
                com=p.readlines()
            for stock in com:
                if len(stock)>=6:
                    stock=stock.replace("\n", "")
                    stock_list.append(stock)
            df=pd.DataFrame()
            df['证券代码']=stock_list
            def select_stock(x):
                '''
                选择股票
                '''
                stock=str(x)
                if stock[0]=='0':
                    stock=stock[1:]
                    stock=str(stock)+'.SZ'
                elif stock[0]=='1':
                    stock=stock[1:]
                    stock=str(stock)+'.SH'
                else:
                    stock=stock[1:]
                    stock=str(stock)+'.SZ'
                return stock
            df['证券代码']=df['证券代码'].apply(lambda x:select_stock(x))
            df['名称']=df['证券代码']
        except Exception as e:
            try:
                print(e,'通达信路径有问题可能不存在',path)
                df=pd.read_excel(r'{}'.format(path))
            except Exception as e:
                print(e)
                try:
                    df=pd.read_csv(r'{}'.format(path))
                except Exception as e:
                    print(e)
                    df=pd.DataFrame()
        return df 
    #生成简单的模拟数据
    def generate_synthetic_data(self,start_date='2024-01-01', end_date='2024-12-31',
                                n_stocks=30, seed=42):
        """
        生成模拟的因子数据和价格数据
        返回: (factor_df, price_df, factor_series, factor_data)
        """
        np.random.seed(seed)
        dates = pd.date_range(start_date, end_date, freq='B')
        stocks = [f'Stock_{i:03d}' for i in range(n_stocks)]

        factor_df = pd.DataFrame(index=dates, columns=stocks)
        price_df = pd.DataFrame(index=dates, columns=stocks)

        for stock in stocks:
            trend = np.linspace(0, 1, len(dates)) * 0.3
            style = np.random.randn() * 0.5
            factor_df[stock] = np.random.randn(len(dates)) + trend + style
            ret = np.random.randn(len(dates)) * 0.02
            ret += factor_df[stock].shift(1).fillna(0) * 0.01
            price_df[stock] = 100 * (1 + ret).cumprod()

        factor_series = factor_df.stack()
        factor_series.index.names = ['date', 'asset']
        return factor_df, price_df, factor_series
    def clean_factor_data(self,factor_series, price_df, quantiles=5, periods=(1,5,10), max_loss=0.95):
        """数据清洗与对齐，返回 Alphalens 格式的 factor_data"""
        print("正在清洗数据...")
        factor_data = al.utils.get_clean_factor_and_forward_returns(
            factor=factor_series,
            prices=price_df,
            quantiles=quantiles,
            periods=periods,
            max_loss=max_loss,
        )
        print(f"数据清洗完成，形状: {factor_data.shape}\n")
        return factor_data
    def ic_detailed_statistics(self):
        """IC详细统计（输出DataFrame）"""
        print("\n>>> 信息系数 (IC) 详细统计 <<<")
        ic = al.performance.factor_information_coefficient(self.factor_data)
        ic_stats_list = []
        for col in ic.columns:
            series = ic[col].dropna()
            jb_stat, jb_p = jarque_bera(series)
            ic_stats_list.append({
                'period': col,
                'IC_mean': series.mean(),
                'IC_std': series.std(),
                'ICIR': series.mean() / series.std() if series.std() != 0 else np.nan,
                'IC_positive_ratio': (series > 0).mean(),
                'IC_abs_mean': series.abs().mean(),
                'Skewness': series.skew(),
                'Kurtosis': series.kurtosis(),
                'Jarque-Bera p-value': jb_p,
                't_stat': series.mean() / (series.std() / np.sqrt(len(series))) if series.std() != 0 else np.nan,
                'p_value': 2 * (1 - stats.t.cdf(np.abs(series.mean() / (series.std() / np.sqrt(len(series)))), df=len(series)-1)) if series.std() != 0 else np.nan
            })
        ic_summary = pd.DataFrame(ic_stats_list).set_index('period')
        print(ic_summary.round(4))
        return ic_summary


    def plot_ic_distribution(self, periods=[1,5,10]):
        """绘制IC分布直方图和Q-Q图（图片英文）"""
        ic = al.performance.factor_information_coefficient(self.factor_data)
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        for i, period in enumerate(periods):
            col = f'{period}D'
            axes[0, i].hist(ic[col].dropna(), bins=30, edgecolor='black', alpha=0.7)
            axes[0, i].axvline(0, color='r', linestyle='--')
            axes[0, i].set_title(f'IC Distribution ({period}D)')
            stats.probplot(ic[col].dropna(), dist="norm", plot=axes[1, i])
            axes[1, i].set_title(f'IC Q-Q Plot ({period}D)')
        plt.tight_layout()
        plt.show()

    def plot_ic_decay(self, periods=[1,5,10]):
        """IC衰减（自相关）图"""
        print("\n>>> IC 衰减分析 <<<")
        ic = al.performance.factor_information_coefficient(self.factor_data)
        ic_lag_acf = {}
        for period in periods:
            col = f'{period}D'
            ic_series = ic[col].dropna()
            acf_values = [ic_series.autocorr(lag) for lag in range(1, 11)]
            ic_lag_acf[period] = acf_values
        pd.DataFrame(ic_lag_acf, index=range(1,11)).plot(marker='o', title='IC Series Autocorrelation')
        plt.xlabel('Lag (days)')
        plt.ylabel('Autocorrelation')
        plt.grid(True)
        plt.show()
    def quantile_performance_metrics(self, period='1D'):
        """计算分层收益绩效指标（输出DataFrame）"""
        print(f"\n>>> 分层收益绩效 (未来{period}日) <<<")
        daily_ret_by_q = self.factor_data.groupby(['date', 'factor_quantile'])[period].mean().unstack()
        cumulative_ret = (1 + daily_ret_by_q).cumprod()

        metrics = {}
        for q in daily_ret_by_q.columns:
            series = daily_ret_by_q[q].dropna()
            cum = cumulative_ret[q]
            rolling_max = cum.expanding().max()
            drawdown = (cum / rolling_max - 1)
            max_dd = drawdown.min()
            ann_ret = (1 + series.mean())**252 - 1
            calmar = ann_ret / abs(max_dd) if max_dd != 0 else np.nan
            metrics[q] = {
                '日均收益 (bps)': series.mean() * 10000,
                '年化收益 (%)': ann_ret * 100,
                '波动率 (年化)': series.std() * np.sqrt(252) * 100,
                '夏普比率': (series.mean() / series.std()) * np.sqrt(252) if series.std() > 0 else np.nan,
                '最大回撤 (%)': max_dd * 100,
                '卡玛比率': calmar,
                '胜率 (%)': (series > 0).mean() * 100,
                '最大单日收益 (bps)': series.max() * 10000,
                '最小单日收益 (bps)': series.min() * 10000,
            }
        metrics_df = pd.DataFrame(metrics).T
        print(metrics_df.round(4))
        return daily_ret_by_q, cumulative_ret, metrics_df


    def long_short_portfolio_analysis(self,period='1D',window=60):
        """多空组合分析（Top - Bottom）并绘图"""
        daily_ret_by_q, cumulative_ret, metrics_df = self.quantile_performance_metrics(period=period)



        top_q = daily_ret_by_q.columns.max()
        bottom_q = daily_ret_by_q.columns.min()
        long_short_ret = daily_ret_by_q[top_q] - daily_ret_by_q[bottom_q]
        long_short_cum = (1 + long_short_ret).cumprod()
        rolling_ls_sharpe = long_short_ret.rolling(window).apply(
            lambda x: (x.mean()/x.std())*np.sqrt(252) if x.std()>0 else 0)

        ann_ret_ls = (1 + long_short_ret.mean())**252 - 1
        vol_ls = long_short_ret.std() * np.sqrt(252)
        sharpe_ls = ann_ret_ls / vol_ls if vol_ls != 0 else np.nan
        max_dd_ls = (long_short_cum / long_short_cum.cummax() - 1).min()
        print(f"\n>>> 多空组合 (Q{top_q} - Q{bottom_q}) 绩效 <<<")
        print(f"年化收益: {ann_ret_ls:.4%}")
        print(f"年化波动: {vol_ls:.4%}")
        print(f"夏普比率: {sharpe_ls:.4f}")
        print(f"最大回撤: {max_dd_ls:.4%}")
        print(f"胜率: {(long_short_ret>0).mean():.2%}")

        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        long_short_cum.plot(ax=axes[0], title='Long-Short Portfolio Cumulative Return')
        axes[0].set_ylabel('Cumulative Return')
        rolling_ls_sharpe.plot(ax=axes[1], title=f'{window}-Day Rolling Sharpe Ratio (Long-Short)', color='green')
        axes[1].axhline(0, linestyle='--', color='black')
        axes[1].set_ylabel('Sharpe Ratio')
        plt.tight_layout()
        plt.show()
        return long_short_ret, long_short_cum, sharpe_ls


    def monthly_return_heatmap(self,period='1D'):
        """月度分层收益热力图"""
        print("\n>>> 月度分层收益热力图 <<<")

        daily_ret_by_q, cumulative_ret, metrics_df = self.quantile_performance_metrics( period=period)

        monthly_ret = daily_ret_by_q.copy()
        monthly_ret.index = pd.to_datetime(monthly_ret.index)
        monthly_ret['year'] = monthly_ret.index.year
        monthly_ret['month'] = monthly_ret.index.month
        monthly_pivot = monthly_ret.groupby(['year', 'month']).mean()
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(monthly_pivot, annot=True, fmt='.5f', cmap='RdYlGn', center=0, ax=ax)
        ax.set_title('Monthly Average Return by Quantile (1D)')
        plt.show()
    def turnover_analysis(self,):
        """换手率分析（每日分组变动率）"""
        print("\n>>> 分组换手率分析 <<<")
        group_members = self.factor_data.reset_index().groupby(['date', 'factor_quantile'])['asset'].apply(frozenset).unstack()
        turnover_mat = pd.DataFrame(index=group_members.index)
        for q in group_members.columns:
            current = group_members[q]
            prev = current.shift(1)
            def turnover_rate(curr, prev):
                if pd.isna(curr) or pd.isna(prev):
                    return 0.0
                added = len(curr - prev)
                removed = len(prev - curr)
                total = len(curr)
                return (added + removed) / total if total > 0 else 0.0
            turnover = pd.Series(index=current.index, dtype=float)
            for dt in current.index:
                turnover[dt] = turnover_rate(current[dt], prev[dt])
            turnover_mat[f'Q{q}_turnover'] = turnover
        print("平均换手率 (每日组内成员变动比例):")
        print(turnover_mat.mean().round(4))
        turnover_mat.plot(figsize=(12,5), title='Daily Turnover by Quantile')
        plt.ylabel('Turnover Rate')
        plt.show()
        return turnover_mat
    def factor_autocorrelation_stationarity(self,):
        """因子自相关与平稳性检验"""
        print("\n>>> 因子稳定性与平稳性检验 <<<")
        factor_wide = self.factor_data['factor'].unstack()
        autocorr_list = [factor_wide[col].autocorr(lag=1) for col in factor_wide.columns]
        mean_autocorr = np.nanmean(autocorr_list)
        print(f"因子一阶自相关系数 (均值): {mean_autocorr:.4f}")
        mean_factor_series = factor_wide.mean(axis=1).dropna()
        adf_stat, p_value, usedlag, nobs, crit_values, icbest = adfuller(mean_factor_series, autolag='AIC')
        print(f"因子均值序列 ADF 检验: 统计量={adf_stat:.4f}, p-value={p_value:.4f}")
        if p_value < 0.05:
            print("  -> 因子序列平稳")
        else:
            print("  -> 因子序列非平稳")
        plt.figure(figsize=(10,4))
        plt.hist(autocorr_list, bins=20, edgecolor='black')
        plt.axvline(mean_autocorr, color='r', linestyle='--', label=f'Mean={mean_autocorr:.3f}')
        plt.title('Distribution of 1st-order Autocorrelation by Asset')
        plt.xlabel('Autocorrelation')
        plt.legend()
        plt.show()
        return mean_autocorr
    def quantile_ttest(self, periods=[1,5,10]):
        """分层收益t检验（vs 0）"""
        print("\n>>> 分层收益统计显著性检验 (t检验 vs 0) <<<")

        for period in periods:
            col = f'{period}D'
            print(f"\n预测周期 {period}天:")
            for q in range(1,6):
                rets = self.factor_data[self.factor_data['factor_quantile'] == q][col].dropna()
                t_stat, p_val = ttest_1samp(rets, 0)
                print(f"  Q{q}: 均值={rets.mean():.6f}, t={t_stat:.4f}, p={p_val:.4f}")
    def rolling_sharpe_and_drawdown(self,period='1D',window=60):
        """滚动夏普比率和滚动最大回撤"""
        print("\n>>> 分组收益滚动夏普 (60天) <<<")
        daily_ret_by_q, cumulative_ret, metrics_df = self.quantile_performance_metrics( period=period)
        rolling_sharpe = daily_ret_by_q.rolling(window).apply(
            lambda x: (x.mean()/x.std())*np.sqrt(252) if x.std()>0 else 0)
        rolling_sharpe.plot(figsize=(12,5), title=f'Rolling Sharpe Ratio ({window}-day window)')
        plt.ylabel('Sharpe Ratio')
        plt.axhline(0, color='k', linestyle='--')
        plt.show()
        rolling_max_dd = daily_ret_by_q.rolling(window).apply(
            lambda x: ((1+x).cumprod() / (1+x).cumprod().expanding().max() - 1).min())
        rolling_max_dd.plot(figsize=(12,5), title=f'Rolling {window}-day Max Drawdown')
        plt.ylabel('Max Drawdown')
        plt.show()
    def factor_vs_return_scatter(self, periods=[1,5,10], sample_frac=0.1):
        """因子值与未来收益散点图"""
        sample = self.factor_data.sample(frac=sample_frac, random_state=42)
        fig, axes = plt.subplots(1, 3, figsize=(18,5))
        for i, period in enumerate(periods):
            col = f'{period}D'
            axes[i].scatter(sample['factor'], sample[col], c=sample['factor_quantile'], cmap='viridis', alpha=0.5)
            axes[i].set_xlabel('Factor Value')
            axes[i].set_ylabel(f'Future {period}D Return')
            axes[i].set_title(f'Period {period}D | IC={sample["factor"].corr(sample[col]):.3f}')
        plt.tight_layout()
        plt.show()

    def market_regime_ic(self,):
        """市场状态分割：上涨日 vs 下跌日"""
        print("\n>>> 市场状态分割：上涨日 vs 下跌日 <<<")
        market_ret = self.factor_data.groupby('date')['1D'].mean()
        up_days = market_ret > 0
        down_days = market_ret <= 0
        ic_daily = self.factor_data.groupby('date').apply(lambda g: g['factor'].corr(g['1D']))
        ic_up_daily = ic_daily[ic_daily.index.isin(up_days[up_days].index)]
        ic_down_daily = ic_daily[ic_daily.index.isin(down_days[down_days].index)]
        print(f"上涨日平均 IC: {ic_up_daily.mean():.4f}, 下跌日平均 IC: {ic_down_daily.mean():.4f}")
        print(f"上涨日 IC 胜率: {(ic_up_daily>0).mean():.2%}, 下跌日 IC 胜率: {(ic_down_daily>0).mean():.2%}")
    def turnover_return_tradeoff(self,period='1D'):
        """换手率与收益权衡散点图"""
        print("\n>>> 换手率 vs 收益 权衡 <<<")
        turnover_mat = self.turnover_analysis()
        daily_ret_by_q, cumulative_ret, metrics_df = self.quantile_performance_metrics( period=period)
        avg_turnover = turnover_mat.mean()
        avg_ret = daily_ret_by_q.mean()
        tradeoff = pd.DataFrame({'Turnover': avg_turnover, 'Return': avg_ret})
        plt.figure(figsize=(8,6))
        sns.scatterplot(data=tradeoff, x='Turnover', y='Return', s=200, hue=tradeoff.index)
        for idx in tradeoff.index:
            plt.annotate(idx, (tradeoff.loc[idx, 'Turnover'], tradeoff.loc[idx, 'Return']))
        plt.title('Turnover vs Average Daily Return')
        plt.xlabel('Average Turnover')
        plt.ylabel('Average Daily Return (bps)')
        plt.grid(True)
        plt.show()

    def fama_macbeth_regression(self, period='1D'):
        """Fama-MacBeth 回归估计因子溢价"""
        print("\n>>> Fama-MacBeth 回归 (因子溢价) <<<")
        dates = self.factor_data.index.get_level_values('date').unique()
        betas = []
        for dt in dates:
            data_day = self.factor_data.xs(dt, level='date')
            y = data_day[period]
            X = sm.add_constant(data_day['factor'])
            model = sm.OLS(y, X, missing='drop').fit()
            betas.append(model.params)
        fm_result = pd.DataFrame(betas).mean()
        print(f"Fama-MacBeth 因子溢价 ({period}): 常数项={fm_result['const']:.6f}, 因子系数={fm_result['factor']:.6f}")
        print(f"解释: 因子值每增加1单位，未来{period}日收益变化 {fm_result['factor']*10000:.2f} bps")
        return fm_result['factor']


    def cumulative_excess_return(self,period='1D'):
        """累积超额收益（相对于等权市场）"""
        print("\n>>> 分组累积超额收益 (相对于等权市场) <<<")
        daily_ret_by_q, cumulative_ret, metrics_df = self.quantile_performance_metrics( period=period)
        market_ret = self.factor_data.groupby('date')['1D'].mean()
        market_cum = (1 + market_ret).cumprod()
        cum_excess = cumulative_ret.sub(market_cum, axis=0)
        cum_excess.plot(figsize=(12,5), title='Cumulative Excess Return by Quantile (vs Equal-Weight Market)')
        plt.ylabel('Excess Return')
        plt.axhline(0, color='k', linestyle='--')
        plt.show()


    def composite_score(self):
        """
        综合评分与结论（超详细版 V2）
        包含 28+ 项因子评估指标，每项均有原理说明、应用场景和评价
        """
        print("\n" + "=" * 80)
        print("第三部分：因子综合评分与结论（超详细版 V2）")
        print("=" * 80)

        # ---------- 1. 获取基础数据 ----------
        ic = al.performance.factor_information_coefficient(self.factor_data)   # IC序列
        ic_1d = ic['1D']
        daily_ret_by_q, cumulative_ret, metrics_df = self.quantile_performance_metrics(period='1D')
        long_short_ret, long_short_cum, sharpe_ls = self.long_short_portfolio_analysis(window=60)
        turnover_mat = self.turnover_analysis()
        ic_summary = self.ic_detailed_statistics()
        mean_autocorr = self.factor_autocorrelation_stationarity()
        fm_premium = self.fama_macbeth_regression(period='1D')

        # 提取常用数值
        ic_mean_1d = ic_summary.loc['1D', 'IC_mean']
        ic_ir_1d = ic_summary.loc['1D', 'ICIR']
        turnover_mean = turnover_mat.mean().mean()
        fm_premium_bps = fm_premium * 10000
        factor_autocorr_mean = mean_autocorr

        # ---------- 2. 新增指标：分组收益单调性（Spearman秩相关） ----------
        # 自动识别日均收益列名
        ret_col = None
        for col in metrics_df.columns:
            if '日均收益' in col and 'bps' in col:
                ret_col = col
                break
        if ret_col is None:
            ret_col = metrics_df.columns[0]   # 默认第一列
        mean_returns_bps = [metrics_df.loc[q, ret_col] for q in sorted(metrics_df.index)]
        quantile_ranks = np.arange(1, len(mean_returns_bps) + 1)
        from scipy.stats import spearmanr
        spearman_corr, spearman_p = spearmanr(quantile_ranks, mean_returns_bps)

        # ---------- 3. 极端值分析 ----------
        factor_values = self.factor_data['factor']
        high_10 = factor_values.quantile(0.9)
        low_10 = factor_values.quantile(0.1)
        high_group_ret = self.factor_data[self.factor_data['factor'] >= high_10]['1D'].mean()
        low_group_ret = self.factor_data[self.factor_data['factor'] <= low_10]['1D'].mean()
        extreme_spread = (high_group_ret - low_group_ret) * 10000

        # ---------- 4. 月度IC稳定性 ----------
        ic_monthly_mean = ic_1d.resample('M').mean()
        ic_monthly_std = ic_monthly_mean.std()

        # ---------- 5. 多空组合最大回撤持续期 ----------
        drawdown_series = (long_short_cum / long_short_cum.cummax() - 1)
        in_drawdown = (drawdown_series < 0).astype(int)
        drawdown_duration = 0
        max_duration = 0
        for val in in_drawdown:
            if val == 1:
                drawdown_duration += 1
            else:
                max_duration = max(max_duration, drawdown_duration)
                drawdown_duration = 0
        max_duration = max(max_duration, drawdown_duration)

        # ---------- 6. 分层收益夏普对比 ----------
        top_q = daily_ret_by_q.columns.max()
        bottom_q = daily_ret_by_q.columns.min()
        top_q_ret = daily_ret_by_q[top_q].dropna()
        bottom_q_ret = daily_ret_by_q[bottom_q].dropna()
        top_sharpe = (top_q_ret.mean() / top_q_ret.std()) * np.sqrt(252) if top_q_ret.std() != 0 else np.nan
        bottom_sharpe = (bottom_q_ret.mean() / bottom_q_ret.std()) * np.sqrt(252) if bottom_q_ret.std() != 0 else np.nan

        # ---------- 7. 因子值分布特征 ----------
        factor_all = factor_values.dropna()
        factor_skew = factor_all.skew()
        factor_kurt = factor_all.kurtosis()

        # ---------- 8. 滚动IC趋势 ----------
        ic_rolling_mean = ic_1d.rolling(20).mean()
        recent_ic_trend = ic_rolling_mean.iloc[-1] - ic_rolling_mean.iloc[-20] if len(ic_rolling_mean) >= 20 else 0

        # ---------- 9. 多空组合卡玛比率 ----------
        ls_ann_ret = (1 + long_short_ret.mean()) ** 252 - 1
        ls_max_dd = (long_short_cum / long_short_cum.cummax() - 1).min()
        calmar_ls = ls_ann_ret / abs(ls_max_dd) if ls_max_dd != 0 else np.nan

        # ---------- 10. 多空组合回撤修复天数 ----------
        cummax_series = long_short_cum.cummax()
        trough_date = drawdown_series.idxmin()   # 谷底日期
        recovery_date = None
        for dt in long_short_cum.index[long_short_cum.index > trough_date]:
            if long_short_cum.loc[dt] >= cummax_series.loc[trough_date]:
                recovery_date = dt
                break
        if recovery_date is not None:
            recovery_days = (recovery_date - trough_date).days
        else:
            recovery_days = np.nan

        # ---------- 11. 因子多空组合的月度胜率 ----------
        monthly_ls_ret = long_short_ret.resample('M').mean()
        monthly_win_rate = (monthly_ls_ret > 0).mean()

        # ---------- 12. 因子值与市场收益的相关性 ----------
        market_ret = self.factor_data.groupby('date')['1D'].mean()
        common_idx = long_short_ret.index.intersection(market_ret.index)
        if len(common_idx) > 5:
            from scipy.stats import pearsonr
            corr_market, p_market = pearsonr(long_short_ret.loc[common_idx], market_ret.loc[common_idx])
        else:
            corr_market, p_market = np.nan, np.nan

        # ---------- 13. IC序列的偏度与峰度 ----------
        ic_skew = ic_1d.dropna().skew()
        ic_kurt = ic_1d.dropna().kurtosis()

        # ---------- 14. IC序列的自相关（滞后1天） ----------
        ic_autocorr = ic_1d.dropna().autocorr(lag=1)

        # ---------- 15. IC的滚动波动率（20天） ----------
        ic_rolling_vol = ic_1d.rolling(20).std()
        recent_ic_vol = ic_rolling_vol.iloc[-1] if len(ic_rolling_vol) > 0 else np.nan

        # ---------- 16. 因子值的极端值比例（超出均值±3倍标准差） ----------
        factor_mean = factor_all.mean()
        factor_std = factor_all.std()
        outliers = factor_all[(factor_all < factor_mean - 3*factor_std) | (factor_all > factor_mean + 3*factor_std)]
        outlier_ratio = len(outliers) / len(factor_all)

        # ---------- 17. 因子值的滚动标准差（20天）的稳定性 ----------
        factor_wide = self.factor_data['factor'].unstack()
        rolling_std = factor_wide.rolling(20).std().mean(axis=1)  # 每日截面平均标准差
        rolling_std_vol = rolling_std.std()   # 滚动标准差的波动

        # ---------- 18. 分组换手率的稳定性 ----------
        turnover_std = turnover_mat.mean(axis=0).std()

        # ---------- 19. 分组收益中位数差异 ----------
        top_median = top_q_ret.median()
        bottom_median = bottom_q_ret.median()
        median_spread = (top_median - bottom_median) * 10000

        # ---------- 20. 分组收益t检验p值 ----------
        from scipy.stats import ttest_1samp
        t_stat, p_val_bottom = ttest_1samp(bottom_q_ret.dropna(), 0)
        t_stat, p_val_top = ttest_1samp(top_q_ret.dropna(), 0)

        # ---------- 21. 各组最大回撤深度 ----------
        group_max_dd = {}
        for q in daily_ret_by_q.columns:
            cum = (1 + daily_ret_by_q[q]).cumprod()
            dd = (cum / cum.cummax() - 1).min()
            group_max_dd[q] = dd
        worst_group_dd = min(group_max_dd.values())
        best_group_dd = max(group_max_dd.values())

        # ---------- 22. 最高组连续盈利/亏损的最大天数 ----------
        ret_sign = (top_q_ret > 0).astype(int)
        streak = 0
        max_win_streak = 0
        max_loss_streak = 0
        for s in ret_sign:
            if s == 1:
                streak = streak + 1 if streak > 0 else 1
                max_win_streak = max(max_win_streak, streak)
            else:
                streak = streak - 1 if streak < 0 else -1
                max_loss_streak = max(max_loss_streak, -streak)

        # ================== 输出所有指标（含解释） ==================
        # 原有指标 1-13
        print("\n" + "-" * 60)
        print("【1】信息系数 IC 均值（预测方向准确率）")
        print("    IC = 因子值与未来收益的相关系数，范围 [-1, 1]。正值表示因子越大未来收益越高。")
        print(f"    当前 IC 均值 = {ic_mean_1d:.4f}")
        if ic_mean_1d > 0.03:
            print("    ✅ 评价：优秀（>0.03），因子具有清晰的正向预测能力。")
        elif ic_mean_1d > 0.01:
            print("    ⚠️ 评价：一般（0.01~0.03），有一定预测作用但较弱。")
        elif ic_mean_1d > 0:
            print("    ❌ 评价：微弱（<0.01），实际预测价值很低。")
        elif ic_mean_1d > -0.01:
            print("    🔄 评价：接近零，因子基本无预测能力。")
        else:
            print("    🔄 评价：负相关，因子值越大未来收益越低（可反向使用）。")

        print("\n" + "-" * 60)
        print("【2】ICIR（信息比率，IC均值 / IC标准差）")
        print("    衡量因子预测的稳定性，越高说明每次预测的可靠性越一致。")
        print(f"    当前 ICIR = {ic_ir_1d:.4f}")
        if ic_ir_1d > 0.5:
            print("    ✅ 评价：优秀（>0.5），因子预测非常稳定，回撤风险低。")
        elif ic_ir_1d > 0.2:
            print("    ⚠️ 评价：一般（0.2~0.5），有一定稳定性但仍有波动。")
        else:
            print("    ❌ 评价：较差（<0.2），因子预测忽高忽低，不靠谱。")

        print("\n" + "-" * 60)
        print("【3】多空组合夏普比率（做多因子最大组，做空最小组）")
        print("    衡量因子区分好坏股票后，多空对冲策略的风险调整收益。夏普 > 1 优秀。")
        print(f"    当前多空夏普 = {sharpe_ls:.4f}")
        if not np.isnan(sharpe_ls):
            if sharpe_ls > 1:
                print("    ✅ 优秀（>1），因子能构造出高盈亏比的策略。")
            elif sharpe_ls > 0.5:
                print("    ⚠️ 一般（0.5~1），策略可接受但收益风险比不高。")
            else:
                print("    ❌ 较低（<0.5），直接交易该因子意义不大。")
        else:
            print("    ❌ 无法计算（可能数据不足）。")

        print("\n" + "-" * 60)
        print("【4】平均换手率（每日因子分组中股票变动比例）")
        print("    换手率越低，交易成本越低，策略越容易实现。")
        print(f"    当前平均换手率 = {turnover_mean:.4f}（每日约 {turnover_mean*100:.1f}% 的股票换出）")
        if turnover_mean < 0.3:
            print("    ✅ 低换手（<30%），交易成本友好。")
        elif turnover_mean < 0.6:
            print("    ⚠️ 中等换手（30%~60%），交易成本尚可接受。")
        else:
            print("    ❌ 高换手（>60%），频繁交易会严重侵蚀收益。")

        print("\n" + "-" * 60)
        print("【5】因子自相关系数（一阶自相关，衡量因子值的稳定性）")
        print("    数值越高，因子变化越慢，选股逻辑越连贯。")
        print(f"    当前因子自相关 = {factor_autocorr_mean:.4f}")
        if factor_autocorr_mean > 0.8:
            print("    ✅ 高稳定性（>0.8），适合低频策略。")
        elif factor_autocorr_mean > 0.5:
            print("    ⚠️ 中等稳定性（0.5~0.8），有一定持续性。")
        else:
            print("    ❌ 低稳定性（<0.5），因子频繁反转，难以跟踪。")

        print("\n" + "-" * 60)
        print("【6】Fama-MacBeth 因子溢价（单位因子值带来的日度超额收益）")
        print(f"    当前因子溢价 = {fm_premium_bps:.2f} bps")
        if fm_premium_bps > 2:
            print("    ✅ 溢价显著（>2 bps），经济意义强。")
        elif fm_premium_bps > 0.5:
            print("    ⚠️ 溢价一般（0.5~2 bps），正收益但幅度较小。")
        elif fm_premium_bps > 0:
            print("    ❌ 溢价微弱（<0.5 bps），实际交易价值低。")
        else:
            print("    ❌ 溢价为负，因子反向有效（可取负值使用）。")

        print("\n" + "-" * 60)
        print("【7】分组收益单调性检验（Spearman秩相关）")
        print("    检验因子值越大，收益是否越高（单调递增）。相关系数接近1表示单调性好。")
        print(f"    Spearman相关系数 = {spearman_corr:.4f}，p值 = {spearman_p:.4f}")
        if spearman_p < 0.05 and spearman_corr > 0.7:
            print("    ✅ 单调性很强，分组收益随因子值严格递增。")
        elif spearman_p < 0.05 and spearman_corr > 0.3:
            print("    ⚠️ 单调性一般，但统计显著。")
        elif spearman_p < 0.05 and spearman_corr < 0:
            print("    🔄 单调性反向（递减），可考虑取负因子值。")
        else:
            print("    ❌ 无显著单调性，因子区分度差。")

        print("\n" + "-" * 60)
        print("【8】极端值分析（因子值最高10% vs 最低10%）")
        print("    比较极端组的平均收益，考察因子两端是否有明显区分。")
        print(f"    最高10%因子值平均收益: {high_group_ret*10000:.2f} bps")
        print(f"    最低10%因子值平均收益: {low_group_ret*10000:.2f} bps")
        print(f"    极端多空收益差: {extreme_spread:.2f} bps")
        if extreme_spread > 5:
            print("    ✅ 极端组差异大，因子能有效捕捉极端机会。")
        elif extreme_spread > 1:
            print("    ⚠️ 极端组有一定差异，但不够突出。")
        else:
            print("    ❌ 极端组差异小，因子对极端值不敏感。")

        print("\n" + "-" * 60)
        print("【9】月度IC稳定性（月度IC均值的标准差）")
        print("    标准差越小，因子在不同月份的表现越稳定。")
        print(f"    月度IC均值的标准差 = {ic_monthly_std:.4f}")
        if ic_monthly_std < 0.05:
            print("    ✅ 非常稳定，月度IC均值波动小。")
        elif ic_monthly_std < 0.10:
            print("    ⚠️ 稳定性尚可，个别月份可能失效。")
        else:
            print("    ❌ 稳定性差，因子效果随月份剧烈波动。")

        print("\n" + "-" * 60)
        print("【10】多空组合最大回撤持续期")
        print("    最长的连续亏损天数，反映策略的“痛苦期”。")
        print(f"    最长回撤持续期 = {max_duration} 个交易日")
        if max_duration < 20:
            print("    ✅ 回撤恢复快，策略韧性好。")
        elif max_duration < 60:
            print("    ⚠️ 回撤期中等，需注意仓位管理。")
        else:
            print("    ❌ 回撤期过长，策略可能长时间失效。")

        print("\n" + "-" * 60)
        print("【11】分层收益夏普比率对比（最高组 vs 最低组）")
        print(f"    因子值最高组夏普比率: {top_sharpe:.4f}")
        print(f"    因子值最低组夏普比率: {bottom_sharpe:.4f}")
        if top_sharpe > bottom_sharpe and top_sharpe > 0.5:
            print("    ✅ 最高组夏普显著优于最低组，因子区分度高。")
        else:
            print("    ⚠️ 两组夏普差异不大，因子分层效果不明显。")

        print("\n" + "-" * 60)
        print("【12】因子值分布特征（偏度、峰度）")
        print("    偏度接近0表示对称，峰度接近3表示正态分布。极端偏离可能影响分组稳定性。")
        print(f"    偏度 = {factor_skew:.4f}，峰度 = {factor_kurt:.4f}")
        if abs(factor_skew) < 0.5 and abs(factor_kurt - 3) < 1:
            print("    ✅ 分布接近正态，分组均匀。")
        elif abs(factor_skew) > 1:
            print("    ⚠️ 偏度较大，可能存在极端值影响。")
        if factor_kurt > 5:
            print("    ⚠️ 峰度过高，因子值集中，可能降低区分度。")

        print("\n" + "-" * 60)
        print("【13】最新20日IC趋势（滚动均值变化）")
        print("    正值表示近期因子预测能力在增强，负值表示衰减。")
        print(f"    最近20日IC均值变化: {recent_ic_trend:.4f}")
        if recent_ic_trend > 0.01:
            print("    ✅ 近期IC上升，因子表现改善。")
        elif recent_ic_trend < -0.01:
            print("    ❌ 近期IC下降，因子可能正在失效。")
        else:
            print("    ⚠️ 近期IC平稳，无明显趋势。")

        # 新增指标 14-28
        print("\n" + "-" * 60)
        print("【14】多空组合卡玛比率（年化收益 / 最大回撤）")
        print("    原理：衡量单位回撤风险带来的年化收益，数值越大越好。")
        print(f"    当前卡玛比率 = {calmar_ls:.4f}")
        if calmar_ls > 1:
            print("    ✅ 优秀（>1），回撤控制好，收益风险比高。")
        elif calmar_ls > 0.5:
            print("    ⚠️ 一般（0.5~1），可接受但回撤较大。")
        else:
            print("    ❌ 较差（<0.5），回撤过大或收益不足。")

        print("\n" + "-" * 60)
        print("【15】多空组合回撤修复天数")
        print("    原理：从最大回撤谷底回到前高所需的天数，越短越好。")
        print(f"    当前修复天数 = {recovery_days} 个交易日")
        if recovery_days < 30:
            print("    ✅ 修复快，策略韧性好。")
        elif recovery_days < 90:
            print("    ⚠️ 修复较慢，需耐心持有。")
        else:
            print("    ❌ 修复极慢，可能策略失效期过长。")

        print("\n" + "-" * 60)
        print("【16】多空组合月度胜率")
        print("    原理：每月正收益的比例，衡量策略月度表现的稳定性。")
        print(f"    当前月度胜率 = {monthly_win_rate:.2%}")
        if monthly_win_rate > 0.7:
            print("    ✅ 胜率高，多数月份盈利。")
        elif monthly_win_rate > 0.5:
            print("    ⚠️ 胜率过半但仍有较多亏损月份。")
        else:
            print("    ❌ 胜率低于50%，策略不稳定。")

        print("\n" + "-" * 60)
        print("【17】多空组合与市场收益相关性")
        print("    原理：衡量因子策略是否与市场走势相关，低相关有分散化价值。")
        print(f"    当前相关系数 = {corr_market:.4f} (p={p_market:.4f})")
        if abs(corr_market) < 0.3:
            print("    ✅ 低相关，可作为市场中性策略。")
        elif abs(corr_market) < 0.6:
            print("    ⚠️ 中等相关，仍有一定分散效果。")
        else:
            print("    ❌ 高相关，策略收益主要来自市场方向。")

        print("\n" + "-" * 60)
        print("【18】IC序列的偏度与峰度")
        print("    原理：偏度≠0表示IC分布不对称，峰度>3表示有厚尾风险。")
        print(f"    偏度 = {ic_skew:.4f}，峰度 = {ic_kurt:.4f}")
        if abs(ic_skew) < 0.5 and abs(ic_kurt - 3) < 1:
            print("    ✅ IC接近正态分布，预测稳定性好。")
        else:
            print("    ⚠️ IC分布异常，可能存在极端预测值。")

        print("\n" + "-" * 60)
        print("【19】IC序列的自相关（滞后1天）")
        print("    原理：衡量今日IC与明日IC的关系，高自相关表示预测能力持续。")
        print(f"    当前IC自相关 = {ic_autocorr:.4f}")
        if ic_autocorr > 0.3:
            print("    ✅ IC具有正自相关，因子效果有持续性。")
        else:
            print("    ❌ IC自相关低，因子效果容易反转。")

        print("\n" + "-" * 60)
        print("【20】IC的滚动波动率（20天）")
        print("    原理：IC波动越小，因子越稳定。")
        print(f"    近期IC波动率 = {recent_ic_vol:.4f}")
        if recent_ic_vol < 0.1:
            print("    ✅ 低波动，预测稳定。")
        elif recent_ic_vol < 0.2:
            print("    ⚠️ 波动中等，尚可接受。")
        else:
            print("    ❌ 高波动，因子预测忽强忽弱。")

        print("\n" + "-" * 60)
        print("【21】因子值极端值比例（超出±3σ）")
        print("    原理：极端值过多可能导致分组不稳定。")
        print(f"    当前极端值比例 = {outlier_ratio:.2%}")
        if outlier_ratio < 0.01:
            print("    ✅ 极端值很少，数据质量好。")
        elif outlier_ratio < 0.05:
            print("    ⚠️ 存在一定极端值，建议缩尾处理。")
        else:
            print("    ❌ 极端值过多，需进行极值处理。")

        print("\n" + "-" * 60)
        print("【22】因子值滚动标准差的稳定性")
        print("    原理：因子截面离散度的变化程度，变化越小越稳定。")
        print(f"    滚动标准差的标准差 = {rolling_std_vol:.4f}")
        if rolling_std_vol < 0.02:
            print("    ✅ 因子离散度稳定，分组一致性高。")
        else:
            print("    ⚠️ 离散度变化大，因子区分能力时强时弱。")

        print("\n" + "-" * 60)
        print("【23】分组换手率的稳定性（各分位组换手率差异）")
        print("    原理：各组换手率差异小，说明因子在不同分位组间切换频率一致。")
        print(f"    换手率组间标准差 = {turnover_std:.4f}")
        if turnover_std < 0.05:
            print("    ✅ 各组换手率稳定，策略执行一致。")
        else:
            print("    ⚠️ 不同组换手差异大，可能在某些组过度交易。")

        print("\n" + "-" * 60)
        print("【24】分组收益中位数差异（最高组 vs 最低组）")
        print("    原理：中位数差异比均值更稳健，反映典型收益差。")
        print(f"    中位数收益差 = {median_spread:.2f} bps")
        if median_spread > 2:
            print("    ✅ 中位数差异显著，因子稳健有效。")
        else:
            print("    ❌ 中位数差异小，因子效果可能由极端值驱动。")

        print("\n" + "-" * 60)
        print("【25】分组收益t检验（最高组与最低组）")
        print("    原理：检验最高/最低组收益是否显著异于零。")
        print(f"    最高组 p值 = {p_val_top:.4f}，最低组 p值 = {p_val_bottom:.4f}")
        if p_val_top < 0.05:
            print("    ✅ 最高组收益显著大于零。")
        else:
            print("    ❌ 最高组收益不显著异于零。")
        if p_val_bottom < 0.05:
            print("    ✅ 最低组收益显著异于零。")
        else:
            print("    ❌ 最低组收益不显著异于零。")

        print("\n" + "-" * 60)
        print("【26】各组最大回撤深度对比")
        print("    原理：各组自身的最大回撤，反映极端风险。")
        print(f"    最小组 (Q{bottom_q}) 最大回撤: {group_max_dd[bottom_q]*100:.2f}%")
        print(f"    最大组 (Q{top_q}) 最大回撤: {group_max_dd[top_q]*100:.2f}%")
        if group_max_dd[top_q] > group_max_dd[bottom_q]:
            print("    ✅ 最大组回撤小于最小组，因子抗跌性好。")
        else:
            print("    ⚠️ 最大组回撤更大，高因子值股票风险也更高。")

        print("\n" + "-" * 60)
        print("【27】最高组连续盈利/亏损天数")
        print("    原理：反映策略的持续赚钱能力和风险暴露时长。")
        print(f"    最长连续盈利天数: {max_win_streak} 天")
        print(f"    最长连续亏损天数: {max_loss_streak} 天")
        if max_loss_streak < 5:
            print("    ✅ 连续亏损天数少，策略稳健。")
        else:
            print("    ⚠️ 存在较长连续亏损期，需做好风控。")

        print("\n" + "-" * 60)
        print("【28】综合评级与最终建议")
        # 综合评分（保留原有逻辑）
        score = 0
        score += min(ic_mean_1d * 100, 10) if ic_mean_1d > 0 else max(ic_mean_1d * 100, -10)
        score += min(ic_ir_1d, 5) if ic_ir_1d > 0 else max(ic_ir_1d, -5)
        score += min(sharpe_ls, 5) if not np.isnan(sharpe_ls) else 0
        score += max(0, 5 - turnover_mean * 10)
        score += factor_autocorr_mean * 5
        score += min(fm_premium_bps, 5) if fm_premium > 0 else max(fm_premium_bps, -5)

        print(f"\n📊 因子综合评分 (越高越好): {score:.2f} / 40")
        print("各维度评分明细（括号内为满分）:")
        print(f"  IC均值 ({ic_mean_1d:.4f})          → {min(ic_mean_1d*100, 10):.2f}/10")
        print(f"  ICIR ({ic_ir_1d:.4f})             → {min(ic_ir_1d, 5):.2f}/5")
        print(f"  多空夏普 ({sharpe_ls:.4f})        → {min(sharpe_ls, 5) if not np.isnan(sharpe_ls) else 0:.2f}/5")
        print(f"  换手率惩罚 ({turnover_mean:.4f})  → {max(0, 5 - turnover_mean*10):.2f}/5")
        print(f"  因子自相关 ({factor_autocorr_mean:.4f}) → {factor_autocorr_mean*5:.2f}/5")
        print(f"  因子溢价 (bps) ({fm_premium_bps:.2f}) → {min(fm_premium_bps, 5) if fm_premium>0 else max(fm_premium_bps, -5):.2f}/5")

        # 最终评级
        if score >= 30:
            grade = "A+ (极优秀)"
            advice = "强烈建议纳入策略，可直接作为主要选股因子。"
        elif score >= 25:
            grade = "A (优秀)"
            advice = "建议使用，可与其他因子简单结合。"
        elif score >= 20:
            grade = "B (良好)"
            advice = "有一定价值，需优化或组合使用。"
        elif score >= 15:
            grade = "C (及格)"
            advice = "效果较弱，仅作为辅助参考。"
        else:
            grade = "D (较差)"
            advice = "不建议单独使用，请重新审视因子定义或数据。"
        print(f"\n📝 因子诊断总结")
        print(f"  综合评级: {grade}")
        print(f"  操作建议: {advice}")

        print("\n💡 针对性优化建议：")
        if ic_ir_1d < 0.2:
            print("   - IC波动大，可尝试对因子值进行平滑或使用滚动分位数。")
        if turnover_mean > 0.6:
            print("   - 换手率过高，可延长调仓周期（如5日或10日）或使用衰减权重。")
        if factor_autocorr_mean < 0.5:
            print("   - 因子稳定性差，可考虑加入动量约束或过滤噪声。")
        if extreme_spread < 1:
            print("   - 极端组区分度低，可对因子值进行极值处理（如缩尾或标准化）。")
        if recent_ic_trend < -0.01:
            print("   - 近期IC衰减，建议暂停使用，观察市场环境变化。")
        if spearman_corr < 0.3 and spearman_p < 0.05:
            print("   - 单调性弱，可尝试非线性变换（如取对数或平方）。")
        if fm_premium_bps < 0.5 and fm_premium_bps > 0:
            print("   - 因子溢价太薄，需严格控制交易成本，或考虑杠杆放大。")
        if ic_monthly_std > 0.1:
            print("   - 月度表现不稳定，建议按月份进行参数调整或分月回测。")
        if outlier_ratio > 0.05:
            print("   - 极端值比例高，建议进行缩尾或MAD处理。")
        if max_loss_streak > 10:
            print("   - 连续亏损期较长，建议加入止损机制。")

        return score
    def create_full_tear_sheet(self):
        '''
        Alphalens 标准完整报告
        '''
        al.tears.create_full_tear_sheet(self.factor_data)

    # ============================================================
    # 3. 主流程函数（一键运行所有分析）
    # ============================================================
    def run_full_analysis(self, periods=[1,5,10]):
        """
        运行完整的因子分析流程（包含所有模块）
        参数 factor_data 是经过 clean_factor_data 处理后的数据
        """
        factor_data=self.factor_data
        # Alphalens 标准报告
        print("\n" + "="*80)
        print("第一部分：Alphalens 标准完整报告")
        print("="*80)
        al.tears.create_full_tear_sheet(factor_data)

        print("\n" + "="*80)
        print("第二部分：自定义深度分析")
        print("="*80)

        # IC 分析
        ic = al.performance.factor_information_coefficient(factor_data)
        ic_summary = self.ic_detailed_statistics()
        self.plot_ic_distribution( periods)
        self.plot_ic_decay( periods)

        # 分层收益与多空组合
        daily_ret_by_q, cumulative_ret, metrics_df = self.quantile_performance_metrics( period='1D')
        long_short_ret, long_short_cum, sharpe_ls = self.long_short_portfolio_analysis(window=60)

        # 月度热力图
        self.monthly_return_heatmap()

        # 换手率
        turnover_mat = self.turnover_analysis()

        # 因子自相关与平稳性
        mean_autocorr = self.factor_autocorrelation_stationarity()

        # t检验
        self.quantile_ttest( periods)

        # 滚动指标
        self.rolling_sharpe_and_drawdown(window=60)

        # 散点图
        self.factor_vs_return_scatter(periods, sample_frac=0.1)

        # 市场状态分割
        self.market_regime_ic()

        # 换手率与收益权衡
        self.turnover_return_tradeoff()

        # Fama-MacBeth
        fm_premium = self.fama_macbeth_regression( period='1D')

        # 累积超额收益
        self.cumulative_excess_return()

        # 综合评分
        ic_mean_1d = ic_summary.loc['1D', 'IC_mean']
        ic_ir_1d = ic_summary.loc['1D', 'ICIR']
        turnover_mean = turnover_mat.mean().mean()
        self.composite_score()

        # 保存结果
        '''
        ic.to_csv('ic_series_enhanced.csv')
        metrics_df.to_csv('quantile_performance.csv')
        print("\n关键数据已保存: ic_series_enhanced.csv, quantile_performance.csv")
        print("\n" + "="*80)
        print("分析完成！")
        print("="*80)
        '''


# ============================================================
# 4. 使用示例（直接运行）
# ============================================================
if __name__ == "__main__":
    def generate_synthetic_data(start_date='2024-01-01', end_date='2024-12-31',
                            n_stocks=30, seed=42):
        """
        生成模拟的因子数据和价格数据
        返回: (factor_df, price_df, factor_series, factor_data)
        """
        np.random.seed(seed)
        dates = pd.date_range(start_date, end_date, freq='B')
        stocks = [f'Stock_{i:03d}' for i in range(n_stocks)]

        factor_df = pd.DataFrame(index=dates, columns=stocks)
        price_df = pd.DataFrame(index=dates, columns=stocks)

        for stock in stocks:
            trend = np.linspace(0, 1, len(dates)) * 0.3
            style = np.random.randn() * 0.5
            factor_df[stock] = np.random.randn(len(dates)) + trend + style
            ret = np.random.randn(len(dates)) * 0.02
            ret += factor_df[stock].shift(1).fillna(0) * 0.01
            price_df[stock] = 100 * (1 + ret).cumprod()

        factor_series = factor_df.stack()
        factor_series.index.names = ['date', 'asset']
        return factor_df, price_df, factor_series
    factor_df, price_df, factor_series=generate_synthetic_data()
    def clean_factor_data(factor_series, price_df, quantiles=5, periods=(1,5,10), max_loss=0.95):
        """数据清洗与对齐，返回 Alphalens 格式的 factor_data"""
        print("正在清洗数据...")
        factor_data = al.utils.get_clean_factor_and_forward_returns(
            factor=factor_series,
            prices=price_df,
            quantiles=quantiles,
            periods=periods,
            max_loss=max_loss,
        )
        print(f"数据清洗完成，形状: {factor_data.shape}\n")
        return factor_data
    factor_data=clean_factor_data(factor_series, price_df)
    models=xg_alphalens(factor_data=factor_data)
    models.plot_ic_distribution()