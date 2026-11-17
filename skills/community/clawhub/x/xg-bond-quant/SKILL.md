---
name: 小果可转债量化分析助手
description: |
  小果(微信:xg_quant)可转债量化分析助手专注于可转债量化分析工具，基于小果量化策略系统，提供可转债历史行情数据、可转债因子数据、可转债策略回测、可转债组合分析等核心功能。适用于可转债投资者、量化研究员和策略开发者。
  触发关键词：可转债量化、可转债回测、可转债分析、可转债策略、可转债数据、转债策略。
author: 小果
contact: 微信 xg_quant
version: 1.0.0
---

# 小果可转债量化分析助手

## 一、系统概述

小果可转债量化分析助手是小果量化策略回测系统的可转债专项版本，专注于为可转债投资提供一站式量化分析服务。

### 1.1 核心功能

| 功能模块 | 说明 |
| :--- | :--- |
| 📊 **可转债行情数据** | 获取可转债历史日线行情（开、高、低、收、量、额） |
| 📈 **可转债因子数据** | 提取可转债技术因子（均线、MACD、KDJ、RSI、布林带、Alpha等数百种） |
| 🔄 **可转债策略回测** | 定投、动量、资产配置、资产配置平衡、网格、海龟、综合动量、均值方差、条件因子、排序多因子等10+种策略 |
| 📊 **可转债组合分析** | 多可转债相关性矩阵、协方差矩阵、投资组合优化、组合收益分析 |

### 1.2 安装与初始化
教程 https://gitcode.com/qq_50882340/xg_quant_trader
```bash
# 安装客户端
# https://gitcode.com/qq_50882340/xg_quant_trader

教程 https://gitcode.com/qq_50882340/xg_quant_trader
```python

markdown
---
name: 小果可转债量化分析助手
description: |
  小果(微信:xg_quant)可转债量化分析助手专注于可转债量化分析工具，基于小果量化策略系统，
  提供可转债历史行情数据、可转债因子数据、可转债策略回测、可转债组合分析等核心功能。
  适用于可转债投资者、量化研究员和策略开发者。
  触发关键词：可转债量化、可转债回测、可转债分析、可转债策略、可转债数据、转债策略。
author: 小果
contact: 微信 xg_quant
version: 1.0.0
---

# 小果可转债量化分析助手

## 一、系统概述

小果可转债量化分析助手是小果量化策略回测系统的可转债专项版本，专注于为可转债投资提供一站式量化分析服务。

### 1.1 核心功能

| 功能模块 | 说明 |
| :--- | :--- |
| 📊 **可转债行情数据** | 获取可转债历史日线行情（开、高、低、收、量、额） |
| 📈 **可转债因子数据** | 提取可转债技术因子（均线、MACD、KDJ、RSI、布林带、Alpha等数百种） |
| 🔄 **可转债策略回测** | 定投、动量、资产配置、资产配置平衡、网格、海龟、综合动量、均值方差、条件因子、排序多因子等10+种策略 |
| 📊 **可转债组合分析** | 多可转债相关性矩阵、协方差矩阵、投资组合优化、组合收益分析 |

### 1.2 安装与初始化

```bash
# 安装客户端
# https://gitcode.com/qq_50882340/xg_quant_trader
python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)
二、全部函数列表
2.1 用户与认证接口
函数名	功能说明
get_user_info(user)	获取用户信息（用户名、到期时间、剩余天数）
check_password_is_av_user(user)	检查授权码是否有效
2.2 可转债行情数据接口
函数名	功能说明
get_stock_hist_data(stock, start_date, end_date)	获取可转债历史日线行情数据
2.3 可转债因子数据接口
函数名	功能说明
get_stock_factor_data(stock, start_date, end_date, columns)	获取可转债因子数据（支持数百种技术因子）
2.4 可转债策略回测接口
函数名	策略类型	功能说明
xg_dt_backtrader(...)	定投策略	定期定额投资策略回测，支持止盈/补仓
xg_mom_backtrader(...)	动量策略	基于价格动量选择强势可转债回测
xg_pz_backtrader(...)	资产配置策略	按固定权重配置多可转债组合回测
xg_zcph_backtrader(...)	资产配置平衡策略	动态再平衡维持目标权重的策略回测
xg_gd_backtrader(...)	网格策略	基于价格网格进行高抛低吸的策略回测
xg_hg_backtrader(...)	海龟策略	基于唐奇安通道突破的趋势跟踪策略回测
xg_more_mom_backtrader(...)	综合动量策略	结合指数择时与动量过滤的增强型动量策略回测
xg_mean_var_backtrader(...)	均值方差策略	基于马科维茨理论的最优资产组合再平衡策略回测
xg_condi_factor_backtrader(...)	条件因子策略	自定义因子条件与买卖信号的多因子选债策略回测
xg_rank_factor_backtrader(...)	排序多因子策略	通过因子打分排序进行可转债选择与轮动策略回测
2.5 可转债组合分析接口
函数名	功能说明
xg_stock_cov_correlation(start_date, end_date, stock_list, max_workers, method, risk_free_rate)	计算多只可转债收益率的相关性矩阵
xg_stock_cov_covariance(start_date, end_date, stock_list, max_workers, method, risk_free_rate, annualized)	计算多只可转债收益率的协方差矩阵（可年化）
xg_stock_cov_portfolio(start_date, end_date, stock_list, max_workers, method, risk_free_rate, target_return)	多可转债投资组合优化（最小方差/最大夏普/风险平价）
xg_stock_analysis(start_date, end_date, stock_list, stock_weight, index_stock, max_workers, risk_free_rate)	可转债组合收益分析（总收益/年化收益/夏普/最大回撤/Beta/Alpha等50+项指标）
2.6 数据查询接口
函数名	功能说明
get_wencai_data(query)	获取问财数据
root()	系统根路径测试
health()	系统健康检查
三、可转债策略回测参数速查
3.1 定投策略 xg_dt_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
index_stock	str	基准指数代码
cash	float	初始资金
dt_interval	int	定投间隔（交易日）
dt_type	str	定投类型：金额/份额/百分比
dt_value	float	定投金额/份额/百分比值
sell_zdf	float	止盈涨幅阈值
buy_zdf	float	补仓跌幅阈值
trade_value	float	每次交易金额
comm	float	佣金费率
3.2 动量策略 xg_mom_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
index_stock	str	基准指数代码
cash	float	初始资金
comm	float	佣金费率
mom_type	str	动量类型：百分比/金额
mom_value	float	动量值
mom_daily	int	动量计算周期（交易日）
min_mom	float	最小动量阈值
max_mom	float	最大动量阈值
buy_rank	int	买入排名
sell_zdf	float	止盈涨幅
sell_amount	float	卖出金额
3.3 资产配置策略 xg_pz_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
dt_type	str	配置类型：百分比/金额
weight_list	str	权重配置，与可转债列表一一对应
index_stock	str	基准指数代码
cash	float	初始资金
sell_zdf	float	止盈涨幅
buy_zdf	float	补仓跌幅
trade_value	float	交易金额
comm	float	佣金费率
3.4 资产配置平衡策略 xg_zcph_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
dt_type	str	配置类型：百分比/金额
weight_list	str	目标权重
deviation_list	str	偏离容忍度
interval	int	再平衡间隔（交易日）
index_stock	str	基准指数代码
cash	float	初始资金
sell_zdf	float	止盈涨幅
buy_zdf	float	补仓跌幅
trade_value	float	交易金额
comm	float	佣金费率
3.5 网格策略 xg_gd_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
index_stock	str	基准指数代码
cash	float	初始资金
gd_interval	int	网格间隔
gd_bc_type_list	str	网格类型
gd_buy_bc_list	str	买入阈值
gd_sell_bc_list	str	卖出阈值
gd_atr_ratio_list	str	ATR比例
gd_type_list	str	交易类型：金额/份额
gd_value_list	str	交易金额/份额
init_position_ratio_list	str	初始仓位
sell_zdf	float	止盈涨幅
buy_zdf	float	补仓跌幅
comm	float	佣金费率
3.6 海龟策略 xg_hg_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
index_stock	str	基准指数代码
cash	float	初始资金
comm	float	佣金费率
entry_period	int	入场周期
exit_period	int	离场周期
n_period	int	N值计算周期
risk_per_trade	float	单笔风险
risk_per_unit	float	单位风险
max_units	int	最大单位
add_unit_threshold	float	加仓阈值
sell_zdf	float	止盈涨幅
buy_zdf	float	补仓跌幅
trade_value	float	交易金额
3.7 综合动量策略 xg_more_mom_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
index_stock	str	基准指数代码
cash	float	初始资金
comm	float	佣金费率
enable_index_timing	bool	启用指数择时
index_mean_line	int	指数均线周期
index_condition_type	str	指数条件类型
mom_type	str	动量类型：百分比/金额
mom_value	float	动量值
mom_daily	int	动量计算天数
short_ma	int	短期均线
long_ma	int	长期均线
sell_zdf	float	止盈涨幅
sell_amount	float	卖出金额
interval	int	调仓间隔
3.8 均值方差策略 xg_mean_var_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
index_stock	str	基准指数代码
cash	float	初始资金
comm	float	佣金费率
lookback_days	int	计算协方差矩阵使用的历史数据天数
max_weight	float	最大单只权重
min_weight	float	最小单只权重
lambda_risk	float	风险厌恶系数
interval	int	调仓间隔（交易日）
3.9 条件因子策略 xg_condi_factor_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
index_stock	str	基准指数代码
cash	float	初始资金
comm	float	佣金费率
trader_type	str	交易类型：百分比/金额
trader_value	float	交易值
hold_stock_limit	int	持股上限
is_open_user_factor	bool	启用自定义因子
user_factor_list	str	因子列表
user_factor_cacal	str	因子计算公式
buy_condi_factor	str	买入条件
rank_factor	str	排序因子
sell_condi_factor	str	卖出条件
sell_type	str	卖出类型
sell_zdf	float	止盈涨幅
sell_value	float	卖出金额
min_hold_days	int	最少持有天数
risk_free_rate	float	无风险利率
3.10 排序多因子策略 xg_rank_factor_backtrader
参数	类型	说明
start_date	str	回测开始日期 YYYYMMDD
end_date	str	回测结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
index_stock	str	基准指数代码
cash	float	初始资金
comm	float	佣金费率
trader_type	str	交易类型：百分比/金额
trader_value	float	交易值
hold_stock_limit	int	持股上限
is_open_user_factor	bool	启用自定义因子
user_factor_list	str	因子列表
user_factor_cacal	str	因子计算公式
is_open_buy_condi	bool	启用买入条件
buy_condi_factor	str	买入条件
rank_factor	str	排序因子（含相关性和权重）
total_factor_rank	str	总因子排序：降序/升序
sell_type	str	卖出类型
sell_zdf	float	止盈涨幅
sell_value	float	卖出金额
min_hold_days	int	最少持有天数
risk_free_rate	float	无风险利率
3.11 可转债组合分析 xg_stock_analysis
参数	类型	说明
start_date	str	开始日期 YYYYMMDD
end_date	str	结束日期 YYYYMMDD
stock_list	str	可转债列表，逗号分隔
stock_weight	str	可转债权重，逗号分隔（自动归一化）
index_stock	str	基准指数代码
risk_free_rate	float	无风险利率
四、可转债因子字段参考
4.1 基础因子
字段名	说明
date	交易日期
证券代码	可转债代码
close	收盘价
open	开盘价
high	最高价
low	最低价
volume	成交量
amount	成交金额
zdf	涨跌幅
4.2 涨跌幅因子
字段名	说明
5日涨跌幅	5日涨跌幅
10日涨跌幅	10日涨跌幅
20日涨跌幅	20日涨跌幅
30日涨跌幅	30日涨跌幅
60日涨跌幅	60日涨跌幅
120日涨跌幅	120日涨跌幅
250日涨跌幅	250日涨跌幅
4.3 移动平均线因子
字段名	说明
5日均线	5日均线
10日均线	10日均线
20日均线	20日均线
30日均线	30日均线
60日均线	60日均线
120日均线	120日均线
价格距离5日均线涨跌幅	价格距离5日均线涨跌幅
价格距离10日均线涨跌幅	价格距离10日均线涨跌幅
价格距离20日均线涨跌幅	价格距离20日均线涨跌幅
价格距离30日均线涨跌幅	价格距离30日均线涨跌幅
价格距离60日均线涨跌幅	价格距离60日均线涨跌幅
价格距离120日均线涨跌幅	价格距离120日均线涨跌幅
4.4 技术指标因子
字段名	说明
MACD_DIF	MACD平滑异同平均线DIF
MACD_DEA	MACD平滑异同平均线DEA
MACD_MACD	MACD平滑异同平均线MACD
MACD_金叉	MACD金叉信号
MACD_死叉	MACD死叉信号
KDJ_K	KDJ指标K值
KDJ_D	KDJ指标D值
KDJ_J	KDJ指标J值
KDJ_KD金叉	KDJ金叉信号
KDJ_KD死叉	KDJ死叉信号
RSI1	RSI相对强弱RSI1
RSI2	RSI相对强弱RSI2
RSI3	RSI相对强弱RSI3
RSI_金叉	RSI金叉信号
RSI_死叉	RSI死叉信号
BOLL_BOLL	BOLL布林线中轨
BOLL_UB	BOLL布林线上轨
BOLL_LB	BOLL布林线下轨
CCI	CCI商品路径指标
MFI	MFI资金流量指标
MTM_MTM	MTM动量线MTM值
SKDJ_K	SKDJ慢速随机K值
SKDJ_D	SKDJ慢速随机D值
WR1	WR威廉指标WR1
PSY_PSY	PSY心理线PSY
BIAS1	BIAS乖离率BIAS1
DMI_PDI	DMI趋向指标PDI
BBI	BBI多空均线
SAR	SAR抛物线指标
Alpha001 至 Alpha191	世界金融实验室101因子（共191个）
4.5 回归动量因子
字段名	说明
3日回归动量	3日回归动量
5日回归动量	5日回归动量
7日回归动量	7日回归动量
9日回归动量	9日回归动量
12日回归动量	12日回归动量
15日回归动量	15日回归动量
18日回归动量	18日回归动量
20日回归动量	20日回归动量
23日回归动量	23日回归动量
25日回归动量	25日回归动量
28日回归动量	28日回归动量
30日回归动量	30日回归动量
35日回归动量	35日回归动量
40日回归动量	40日回归动量
45日回归动量	45日回归动量
50日回归动量	50日回归动量
60日回归动量	60日回归动量
5日回归斜率	5日回归斜率
10日回归斜率	10日回归斜率
20日回归斜率	20日回归斜率
30日回归斜率	30日回归斜率
60日回归斜率	60日回归斜率
120日回归斜率	120日回归斜率
4.6 风险因子
字段名	说明
5日标准差	5日标准差
10日标准差	10日标准差
20日标准差	20日标准差
30日标准差	30日标准差
60日标准差	60日标准差
120日标准差	120日标准差
5日夏普比率	5日夏普比率
10日夏普比率	10日夏普比率
20日夏普比率	20日夏普比率
30日夏普比率	30日夏普比率
60日夏普比率	60日夏普比率
120日夏普比率	120日夏普比率
5日最大回撤	5日最大回撤
10日最大回撤	10日最大回撤
20日最大回撤	20日最大回撤
30日最大回撤	30日最大回撤
60日最大回撤	60日最大回撤
120日最大回撤	120日最大回撤
5日年化波动率	5日年化波动率
10日年化波动率	10日年化波动率
20日年化波动率	20日年化波动率
30日年化波动率	30日年化波动率
60日年化波动率	60日年化波动率
120日年化波动率	120日年化波动率
5日Alpha	5日Alpha
10日Alpha	10日Alpha
20日Alpha	20日Alpha
30日Alpha	30日Alpha
60日Alpha	60日Alpha
120日Alpha	120日Alpha
5日Beta	5日Beta
10日Beta	10日Beta
20日Beta	20日Beta
30日Beta	30日Beta
60日Beta	60日Beta
120日Beta	120日Beta
4.7 交易信号因子
字段名	说明
六脉神剑	六脉神剑交易信号
小波段交易	小波段交易信号
大波段交易	大波段交易信号
波段超级买卖	波段超级买卖信号
4.8 主力指标
字段名	说明
ZJTJ_无庄控盘	ZJTJ庄家抬轿无庄控盘
ZJTJ_开始控盘	ZJTJ庄家抬轿开始控盘
ZJTJ_有庄控盘	ZJTJ庄家抬轿有庄控盘
ZJTJ_主力出货	ZJTJ庄家抬轿主力出货
CYW	CYW主力控盘
LHXJ_主力弃盘	LHXJ猎狐先觉主力弃盘
LHXJ_主力控盘	LHXJ猎狐先觉主力控盘
五、使用示例
5.1 获取可转债行情数据
python
result = client.get_stock_hist_data(
    stock='128136.SZ',      # 可转债代码
    start_date='20240101',
    end_date='20241231'
)
df = client._to_dataframe(result)
5.2 获取可转债因子数据
python
result = client.get_stock_factor_data(
    stock='128136.SZ',
    start_date='20240101',
    end_date='20241231',
    columns='date,证券代码,close,MACD_DIF,KDJ_K,RSI1,BOLL_BOLL'
)
df = client._to_dataframe(result)
5.3 定投策略回测
python
result = client.xg_dt_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='128136.SZ,128137.SZ',
    index_stock='000300.SH',
    cash=100000,
    dt_interval=20,
    dt_type='金额',
    dt_value=1000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    comm=0.0001
)
5.4 动量策略回测
python
result = client.xg_mom_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='128136.SZ,128137.SZ,128138.SZ',
    index_stock='000300.SH',
    cash=100000,
    mom_type='百分比',
    mom_value=1,
    mom_daily=25,
    min_mom=0,
    max_mom=5,
    buy_rank=1,
    sell_zdf=0.03,
    sell_amount=1000,
    comm=0.0001
)
5.5 资产配置策略回测
python
result = client.xg_pz_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='128136.SZ,128137.SZ,128138.SZ',
    dt_type='百分比',
    weight_list='0.4,0.4,0.2',
    index_stock='000300.SH',
    cash=100000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
5.6 均值方差策略回测
python
result = client.xg_mean_var_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='128136.SZ,128137.SZ,128138.SZ',
    index_stock='000300.SH',
    cash=100000,
    lookback_days=60,
    max_weight=0.6,
    min_weight=0.05,
    lambda_risk=2.0,
    interval=5,
    comm=0.0001
)
5.7 条件因子策略回测
python
result = client.xg_condi_factor_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='128136.SZ,128137.SZ,128138.SZ',
    index_stock='000300.SH',
    cash=100000,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"收盘价大于5日均线": "IF(df[\'close\']>MA(df[\'close\'],5),True,False)"}',
    buy_condi_factor='{"收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true}}',
    rank_factor='{"收盘价大于5日均线": "降序"}',
    sell_condi_factor='{"收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false}}',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    risk_free_rate=0.02
)
5.8 排序多因子策略回测
python
result = client.xg_rank_factor_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='128136.SZ,128137.SZ,128138.SZ',
    index_stock='000300.SH',
    cash=100000,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"均线评分": "IF(MA(df[\'close\'],3)>MA(df[\'close\'],5),25,0)+IF(MA(df[\'close\'],5)>MA(df[\'close\'],10),25,0)"}',
    is_open_buy_condi=True,
    buy_condi_factor='{"25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0}}',
    rank_factor='{"25日回归动量": {"相关性": "正相关", "权重": 1}}',
    total_factor_rank='降序',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    risk_free_rate=0.02
)
5.9 可转债组合分析
python
result = client.xg_stock_analysis(
    start_date='20240101',
    end_date='20241231',
    stock_list='128136.SZ,128137.SZ,128138.SZ',
    stock_weight='0.4,0.3,0.3',
    index_stock='000300.SH',
    risk_free_rate=0.03
)

metrics = result.get('performance_metrics', {})
print(f"总收益率: {metrics.get('total_return', 0)*100:.2f}%")
print(f"年化收益率: {metrics.get('annual_return', 0)*100:.2f}%")
print(f"夏普比率: {metrics.get('sharpe_ratio', 0):.4f}")
print(f"最大回撤: {metrics.get('max_drawdown', 0)*100:.2f}%")
5.10 相关性矩阵
python
result = client.xg_stock_cov_correlation(
    start_date='20240101',
    end_date='20241231',
    stock_list='128136.SZ,128137.SZ,128138.SZ',
    method='pearson'
)
print(result.get('correlation_matrix'))
5.11 投资组合优化
python
result = client.xg_stock_cov_portfolio(
    start_date='20240101',
    end_date='20241231',
    stock_list='128136.SZ,128137.SZ,128138.SZ',
    risk_free_rate=0.03,
    target_return=0.15
)
print(result.get('min_variance'))
print(result.get('max_sharpe'))
六、策略回测结果字段说明
字段名	说明
total_return	总收益率
annual_return	年化收益率
annual_volatility	年化波动率
sharpe_ratio	夏普比率
max_drawdown	最大回撤
max_drawdown_duration	最大回撤持续天数
win_rate	胜率
positive_ratio	正收益比例
total_trades	总交易次数
turnover_rate	换手率
alpha	Alpha系数
beta	Beta系数
information_ratio	信息比率
tracking_error	跟踪误差
calmar_ratio	卡玛比率
sortino_ratio	索提诺比率
final_cash	最终资金
equity_curve	权益曲线数据
buy_signals	买入信号记录
sell_signals	卖出信号记录
七、常见问题
7.1 可转债代码格式
市场	格式	示例
深圳	代码.SZ	128136.SZ
上海	代码.SH	110044.SH
7.2 日期格式说明
接口类型	日期格式	示例
行情/因子/回测	YYYYMMDD	20240101
7.3 策略类型可选值
策略类型	说明
定投策略	定期定额投资
动量策略	动量因子选债
资产配置策略	固定权重配置
资产配置平衡策略	动态再平衡
网格策略	网格交易
海龟策略	趋势跟踪
综合动量策略	指数择时+动量
条件因子策略	自定义因子条件
排序多因子策略	因子打分排序
均值方差策略	马科维茨最优组合
7.4 数据转换方法
方法	说明
_to_dataframe(result)	将API返回数据转换为DataFrame
python
df = client._to_dataframe(result)
print(df.head())
```
# 小果量化策略回测系统
# 一、介绍
小果量化策略回测系统是一个基于小果量化数据接口，
提供股票历史数据，基金历史数据,可转债历史数据、
股票因子数据，基金因子数据，可转债因子数据，
股票分钟数据，指数数据、财务数据以及多种量化策略回测功能。
主要功能
📊 历史行情数据获取

📈 因子数据提取

💰 财务数据查询

🔄 多种策略回测（定投、动量、资产配置、网格、海龟等）

🤖 模拟交易和社区策略
# 安装客户端
教程链接 https://gitcode.com/qq_50882340/xg_quant_trader
```
# 用户操作
## 1获取用户信息
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例49：获取用户信息
# ============================================================
"""
参数说明：
    user: str = "自己信息"     - 用户名称

返回数据：
    username         - 用户名
    expiry           - 账户到期时间
    days_until_expiry - 剩余天数
    expiry_warning   - 是否即将到期
"""

print("\n" + "=" * 60)
print("📊 获取用户信息")
print("=" * 60)

result = client.get_user_info()
print("用户信息：")
print(result)
```
## 2检查授权码有效性
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例50：检查授权码有效性
# ============================================================
"""
参数说明：
    user: str = "自己信息"     - 用户名称

返回数据：
    status           - 状态（success/failed）
    message          - 消息
    user_info        - 用户信息
"""

print("\n" + "=" * 60)
print("📊 检查授权码有效性")
print("=" * 60)

result = client.check_password_is_av_user()
print("授权码检查结果：")
print(result)
```

# 二、使用教程

## 1. 安装依赖并初始化
```python
# ============================================================
# 完整示例1：初始化客户端
# ============================================================
"""
参数说明：
    url: str = "服务器地址"     - 服务器地址
    port: int = 8888                 - 服务器端口
    user: str = "自己信息"              - 用户名
    password: str = "自己信息"          - 密码
    auth_code: str = "自己信息"         - 授权码
"""

import requests
import json
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List, Union
from datetime import datetime

from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

print("✅ 客户端初始化成功！")
print(f"📡 服务器地址: http://服务器地址:8888")
```

## 2. 获取股票历史行情数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例2：获取历史行情数据
# ============================================================
"""
参数说明：
    stock: str = '600031.SH'        - 股票代码，格式：代码.市场（SH/SZ）
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD

返回字段：
    date        - 交易日期
    open        - 开盘价
    high        - 最高价
    low         - 最低价
    close       - 收盘价
    volume      - 成交量
    amount      - 成交金额
    zdf         - 涨跌幅
    pct_chg     - 百分比变化
"""

print("\n" + "=" * 60)
print("📊 获取历史行情数据")
print("=" * 60)

# 获取单只股票历史数据
result = client.get_stock_hist_data(
    stock='513100.SH',      # 平安银行
    start_date='20240101',
    end_date='20500101'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
print(f"\n数据列: {df.columns.tolist()}")
```
## 3读取ETF基金历史行情数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例2：获取历史行情数据
# ============================================================
"""
参数说明：
    stock: str = '513100.SH'        - 股票代码，格式：代码.市场（SH/SZ）
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD

返回字段：
    date        - 交易日期
    open        - 开盘价
    high        - 最高价
    low         - 最低价
    close       - 收盘价
    volume      - 成交量
    amount      - 成交金额
    zdf         - 涨跌幅
    pct_chg     - 百分比变化
"""

print("\n" + "=" * 60)
print("📊 获取历史行情数据")
print("=" * 60)

# 获取单只股票历史数据
result = client.get_stock_hist_data(
    stock='513100.SH',      # 平安银行
    start_date='20240101',
    end_date='20500101'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
print(f"\n数据列: {df.columns.tolist()}")

```
## 4读取可转债历史行情数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例2：获取历史行情数据
# ============================================================
"""
参数说明：
    stock: str = '513100.SH'        - 股票代码，格式：代码.市场（SH/SZ）
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD

返回字段：
    date        - 交易日期
    open        - 开盘价
    high        - 最高价
    low         - 最低价
    close       - 收盘价
    volume      - 成交量
    amount      - 成交金额
    zdf         - 涨跌幅
    pct_chg     - 百分比变化
"""

print("\n" + "=" * 60)
print("📊 获取历史行情数据")
print("=" * 60)

# 获取单只股票历史数据
result = client.get_stock_hist_data(
    stock='128136.SZ',     
    start_date='20240101',
    end_date='20500101'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
print(f"\n数据列: {df.columns.tolist()}")

```
## 5. 获取股票因子数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例3：获取因子数据
# ============================================================
"""
参数说明：
    stock: str = '600031.SH'        - 股票代码
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD
    columns: str = 'date,close,open,high,low,volume,amount'  - 选择字段，逗号分隔

【基础因子字段】
    date                - 交易日期
    证券代码            - 股票代码
    close               - 收盘价
    open                - 开盘价
    high                - 最高价
    low                 - 最低价
    volume              - 成交量
    amount              - 成交金额
    zdf                 - 涨跌幅

【涨跌幅因子】
    5日涨跌幅           - 5日涨跌幅
    10日涨跌幅          - 10日涨跌幅
    20日涨跌幅          - 20日涨跌幅
    30日涨跌幅          - 30日涨跌幅
    60日涨跌幅          - 60日涨跌幅
    120日涨跌幅         - 120日涨跌幅
    250日涨跌幅         - 250日涨跌幅

【价格距离均线涨跌幅】
    价格距离5日均线涨跌幅   - 价格距离5日均线涨跌幅
    价格距离10日均线涨跌幅  - 价格距离10日均线涨跌幅
    价格距离20日均线涨跌幅  - 价格距离20日均线涨跌幅
    价格距离30日均线涨跌幅  - 价格距离30日均线涨跌幅
    价格距离60日均线涨跌幅  - 价格距离60日均线涨跌幅
    价格距离120日均线涨跌幅 - 价格距离120日均线涨跌幅

【均线距离涨跌幅】
    5日均线距离10日均线涨跌幅  - 5日均线距离10日均线涨跌幅
    10日均线距离20日均线涨跌幅 - 10日均线距离20日均线涨跌幅
    20日均线距离30日均线涨跌幅 - 20日均线距离30日均线涨跌幅
    30日均线距离60日均线涨跌幅 - 30日均线距离60日均线涨跌幅
    60日均线距离120日均线涨跌幅 - 60日均线距离120日均线涨跌幅

【移动平均线】
    5日均线             - 5日均线
    10日均线            - 10日均线
    20日均线            - 20日均线
    30日均线            - 30日均线
    60日均线            - 60日均线
    120日均线           - 120日均线

【均线交叉信号】
    5日10日金叉         - 5日10日均线金叉
    10日20日金叉        - 10日20日均线金叉
    20日30日金叉        - 20日30日均线金叉
    30日60日金叉        - 30日60日均线金叉
    60日120日金叉       - 60日120日均线金叉
    5日10日死叉         - 5日10日均线死叉
    10日20日死叉        - 10日20日均线死叉
    20日30日死叉        - 20日30日均线死叉
    30日60日死叉        - 30日60日均线死叉
    60日120日死叉       - 60日120日均线死叉

【价格位置判断】
    价格在5均线上        - 价格是否在5日均线上
    价格在10均线上       - 价格是否在10日均线上
    价格在20均线上       - 价格是否在20日均线上
    价格在30均线上       - 价格是否在30日均线上
    价格在60均线上       - 价格是否在60日均线上
    价格在120均线上      - 价格是否在120日均线上
    5均线在10均线上      - 5日均线是否在10日均线上
    10均线在20均线上     - 10日均线是否在20日均线上
    20均线在30均线上     - 20日均线是否在30日均线上
    30均线在60均线上     - 30日均线是否在60日均线上
    60均线在120均线上    - 60日均线是否在120日均线上

【技术指标 - KDJ】
    KDJ_K               - KDJ指标K值
    KDJ_D               - KDJ指标D值
    KDJ_J               - KDJ指标J值
    KDJ_KD金叉          - KDJ金叉信号
    KDJ_KD死叉          - KDJ死叉信号

【技术指标 - MACD】
    MACD_DIF            - MACD平滑异同平均线DIF
    MACD_DEA            - MACD平滑异同平均线DEA
    MACD_MACD           - MACD平滑异同平均线MACD
    MACD_金叉           - MACD金叉信号
    MACD_死叉           - MACD死叉信号

【技术指标 - RSI】
    RSI1                - RSI相对强弱RSI1
    RSI2                - RSI相对强弱RSI2
    RSI3                - RSI相对强弱RSI3
    RSI_金叉            - RSI金叉信号
    RSI_死叉            - RSI死叉信号

【技术指标 - BOLL布林线】
    BOLL_BOLL           - BOLL布林线中轨
    BOLL_UB             - BOLL布林线上轨
    BOLL_LB             - BOLL布林线下轨

【技术指标 - CCI】
    CCI                 - CCI商品路径指标

【技术指标 - MFI】
    MFI                 - MFI资金流量指标

【技术指标 - MTM】
    MTM_MTM             - MTM动量线MTM值
    MTM_MTMMA           - MTM动量线MTMMA值

【技术指标 - SKDJ】
    SKDJ_K              - SKDJ慢速随机K值
    SKDJ_D              - SKDJ慢速随机D值

【技术指标 - WR】
    WR1                 - WR威廉指标WR1
    WR2                 - WR威廉指标WR2
    WR_金叉             - WR金叉信号
    WR_死叉             - WR死叉信号

【技术指标 - PSY】
    PSY_PSY             - PSY心理线PSY
    PSY_PSYMA           - PSY心理线PSYMA
    PSY_金叉            - PSY金叉信号
    PSY_死叉            - PSY死叉信号

【技术指标 - BIAS乖离率】
    BIAS1               - BIAS乖离率BIAS1
    BIAS2               - BIAS乖离率BIAS2
    BIAS3               - BIAS乖离率BIAS3
    BIAS_QL_BIAS        - BIAS_QL乖离率传统版BIAS值
    BIAS_QL_BIASMA      - BIAS_QL乖离率传统版BIASMA值
    BIAS36_BIAS36       - BIAS36三六乖离BIAS36
    BIAS36_BIAS612      - BIAS36三六乖离BIAS612
    BIAS36_MABIAS       - BIAS36三六乖离MABIAS

【技术指标 - DMI】
    DMI_PDI             - DMI趋向指标PDI
    DMI_MDI             - DMI趋向指标MDI
    DMI_ADX             - DMI趋向指标ADX
    DMI_ADXR            - DMI趋向指标ADXR

【技术指标 - DMA】
    DMA_XT_DIF          - DMA_XT平均差DIF
    DMA_XT_DIFMA        - DMA_XT平均差DIFMA

【技术指标 - DPO】
    DPO_DPO             - DPO区间震荡线DPO
    DPO_MADPO           - DPO区间震荡线MADPO

【技术指标 - EMV】
    EMV_EMV             - EMV简易波动指标EMV
    EMV_MAEMV           - EMV简易波动指标MAEMV

【技术指标 - TRIX】
    TRIX_TRIX           - TRIX三重指数平均线TRIX
    TRIX_MATRIX         - TRIX三重指数平均线MATRIX

【技术指标 - UOS】
    UOS_UOS             - UOS终极指标UOS
    UOS_MAUOS           - UOS终极指标MAUOS

【技术指标 - VPT】
    VTP_VPT             - VPT量价曲线VPT
    VTP_MAVP            - VPT量价曲线MAVP

【技术指标 - WVAD】
    WVAD_WVAD           - WVAD威廉变异离散量WVAD
    WVAD_MAWVAD         - WVAD威廉变异离散量MAWVAD

【技术指标 - BRAR】
    BRAR_BR             - BRAR情绪指标BR
    BRAR_AR             - BRAR情绪指标AR

【技术指标 - CR】
    CR_CR               - CR带状能量线CR
    CR_MA1              - CR带状能量线MA1
    CR_MA2              - CR带状能量线MA2
    CR_MA3              - CR带状能量线MA3
    CR_MA4              - CR带状能量线MA4

【技术指标 - MASS】
    MASS_MASS           - MASS梅斯线MASS
    MASS_MAMASS         - MASS梅斯线MAMASS

【技术指标 - VR】
    VR_VR               - VR成交量变异率VR
    VR_MAVR             - VR成交量变异率MAVR

【技术指标 - OBV】
    OBV_OBV             - OBV累积能量线OBV
    OBV_MAOBV           - OBV累积能量线MAOBV

【技术指标 - VOL成交量】
    VOL_XT_MAVOL1       - VOL成交量MAVOL1
    VOL_XT_MAVOL2       - VOL成交量MAVOL2

【技术指标 - VRSI】
    VRSI1               - VRSI相对强弱量RSI1
    VRSI2               - VRSI相对强弱量RSI2
    VRSI3               - VRSI相对强弱量RSI3

【技术指标 - HSL换手线】
    HSL_HSL             - HSL换手线HSL
    HSL_MAHSL           - HSL换手线MAHSL

【技术指标 - ACD】
    ACD_ACD             - ACD升降线ACD
    ACD_MAACD           - ACD升降线MAACD

【技术指标 - BBI】
    BBI                 - BBI多空均线

【技术指标 - EXPMA】
    EXPMA_EXP1          - EXPMA指数平均线EXP1
    EXPMA_EXP2          - EXPMA指数平均线EXP2

【技术指标 - SAR】
    SAR                 - SAR抛物线指标

【技术指标 - AMO成交金额】
    AMO_AMOW            - AMO成交金额AMOW
    AMO_AMO1            - AMO成交金额AMO1
    AMO_AMO2            - AMO成交金额AMO2

【技术指标 - MIKE】
    MIKE_STOR           - MIKE麦克支撑压力STOR
    MIKE_MIDR           - MIKE麦克支撑压力MIDR
    MIKE_WEKR           - MIKE麦克支撑压力WEKR
    MIKE_WEKS           - MIKE麦克支撑压力WEKS
    MIKE_MIDS           - MIKE麦克支撑压力MIDS
    MIKE_STOS           - MIKE麦克支撑压力STOS

【技术指标 - ENE】
    ENE_UPPER           - ENE轨道线上轨
    ENE_LOWER           - ENE轨道线下轨
    ENE_ENE             - ENE轨道线ENE

【技术指标 - PBX瀑布线】
    PBX_PBX1            - PBX瀑布线PBX1
    PBX_PBX2            - PBX瀑布线PBX2
    PBX_PBX3            - PBX瀑布线PBX3
    PBX_PBX4            - PBX瀑布线PBX4
    PBX_PBX5            - PBX瀑布线PBX5
    PBX_PBX6            - PBX瀑布线PBX6

【技术指标 - XS薛斯通道】
    XS_SUP              - XS薛斯通道SUP
    XS_SDN              - XS薛斯通道SDN
    XS_LUP              - XS薛斯通道LUP
    XS_LDN              - XS薛斯通道LDN

【技术指标 - TQN唐奇安通道】
    TQN_周期高点        - TQN唐奇安通道周期高点
    TQN_周期低点        - TQN唐奇安通道周期低点
    TQN_平空开多        - TQN唐奇安通道平空开多信号
    TQN_平多开空        - TQN唐奇安通道平多开空信号

【技术指标 - ALLIGAT鳄鱼线】
    ALLIGAT_上唇        - ALLIGAT鳄鱼线上唇
    ALLIGAT_牙齿        - ALLIGAT鳄鱼线牙齿
    ALLIGAT_下颚        - ALLIGAT鳄鱼线下颚

【技术指标 - GMMA顾比均线】
    GMMA_MA3            - GMMA顾比均线MA3
    GMMA_MA5            - GMMA顾比均线MA5
    GMMA_MA8            - GMMA顾比均线MA8
    GMMA_MA10           - GMMA顾比均线MA10
    GMMA_MA12           - GMMA顾比均线MA12
    GMMA_MA15           - GMMA顾比均线MA15
    GMMA_MA30           - GMMA顾比均线MA30
    GMMA_MA35           - GMMA顾比均线MA35
    GMMA_MA40           - GMMA顾比均线MA40
    GMMA_MA45           - GMMA顾比均线MA45
    GMMA_MA50           - GMMA顾比均线MA50
    GMMA_MA60           - GMMA顾比均线MA60

【技术指标 - VMACD】
    VMACD_DIF           - VMACD量平滑异同平均线DIF
    VMACD_DEA           - VMACD量平滑异同平均线DEA
    VMACD_MACD          - VMACD量平滑异同平均线MACD

【技术指标 - SMACD】
    SMACD_DEA           - SMACD单线平滑异同平均线DEA
    SMACD_MACD          - SMACD单线平滑异同平均线MACD

【技术指标 - QACD】
    QACD_DIF            - QACD快速异同平均线DIF
    QACD_MACD           - QACD快速异同平均线MACD
    QACD_DDIF           - QACD快速异同平均线DDIF

【技术指标 - 成交量相关】
    连续上涨天数        - 连续上涨天数
    连续下跌天数        - 连续下跌天数

【技术指标 - 偏度峰度】
    5日偏度             - 5日偏度
    10日偏度            - 10日偏度
    20日偏度            - 20日偏度
    30日偏度            - 30日偏度
    60日偏度            - 60日偏度
    120日偏度           - 120日偏度
    5日峰度             - 5日峰度
    10日峰度            - 10日峰度
    20日峰度            - 20日峰度
    30日峰度            - 30日峰度
    60日峰度            - 60日峰度
    120日峰度           - 120日峰度

【Alpha因子 - 世界金融实验室101因子】
    Alpha001 至 Alpha191 - 世界金融实验室101因子（共191个）

【交易信号因子】
    六脉神剑            - 六脉神剑交易信号
    小波段交易          - 小波段交易信号
    大波段交易          - 大波段交易信号
    波段超级买卖        - 波段超级买卖信号

【回归分析因子】
    3日回归动量         - 3日回归动量
    5日回归动量         - 5日回归动量
    7日回归动量         - 7日回归动量
    9日回归动量         - 9日回归动量
    12日回归动量        - 12日回归动量
    15日回归动量        - 15日回归动量
    18日回归动量        - 18日回归动量
    20日回归动量        - 20日回归动量
    23日回归动量        - 23日回归动量
    25日回归动量        - 25日回归动量
    28日回归动量        - 28日回归动量
    30日回归动量        - 30日回归动量
    35日回归动量        - 35日回归动量
    40日回归动量        - 40日回归动量
    45日回归动量        - 45日回归动量
    50日回归动量        - 50日回归动量
    60日回归动量        - 60日回归动量

【回归斜率】
    5日回归斜率         - 5日回归斜率
    10日回归斜率        - 10日回归斜率
    20日回归斜率        - 20日回归斜率
    30日回归斜率        - 30日回归斜率
    60日回归斜率        - 60日回归斜率
    120日回归斜率       - 120日回归斜率

【标准差】
    5日标准差           - 5日标准差
    10日标准差          - 10日标准差
    20日标准差          - 20日标准差
    30日标准差          - 30日标准差
    60日标准差          - 60日标准差
    120日标准差         - 120日标准差

【最高最低值周期】
    5日最高值到当前周期   - 5日最高值到当前周期
    10日最高值到当前周期  - 10日最高值到当前周期
    20日最高值到当前周期  - 20日最高值到当前周期
    30日最高值到当前周期  - 30日最高值到当前周期
    60日最高值到当前周期  - 60日最高值到当前周期
    120日最高值到当前周期 - 120日最高值到当前周期
    5日最低值到当前周期   - 5日最低值到当前周期
    10日最低值到当前周期  - 10日最低值到当前周期
    20日最低值到当前周期  - 20日最低值到当前周期
    30日最低值到当前周期  - 30日最低值到当前周期
    60日最低值到当前周期  - 60日最低值到当前周期
    120日最低值到当前周期 - 120日最低值到当前周期

【Alpha系数】
    5日Alpha            - 5日Alpha
    10日Alpha           - 10日Alpha
    20日Alpha           - 20日Alpha
    30日Alpha           - 30日Alpha
    60日Alpha           - 60日Alpha
    120日Alpha          - 120日Alpha

【Beta系数】
    5日Beta             - 5日Beta
    10日Beta            - 10日Beta
    20日Beta            - 20日Beta
    30日Beta            - 30日Beta
    60日Beta            - 60日Beta
    120日Beta           - 120日Beta

【夏普比率】
    5日夏普比率         - 5日夏普比率
    10日夏普比率        - 10日夏普比率
    20日夏普比率        - 20日夏普比率
    30日夏普比率        - 30日夏普比率
    60日夏普比率        - 60日夏普比率
    120日夏普比率       - 120日夏普比率

【年化波动率】
    5日年化波动率       - 5日年化波动率
    10日年化波动率      - 10日年化波动率
    20日年化波动率      - 20日年化波动率
    30日年化波动率      - 30日年化波动率
    60日年化波动率      - 60日年化波动率
    120日年化波动率     - 120日年化波动率

【最大回撤】
    5日最大回撤         - 5日最大回撤
    10日最大回撤        - 10日最大回撤
    20日最大回撤        - 20日最大回撤
    30日最大回撤        - 30日最大回撤
    60日最大回撤        - 60日最大回撤
    120日最大回撤       - 120日最大回撤

【上涨/下跌捕获率】
    5日上涨捕获率       - 5日上涨捕获率
    10日上涨捕获率      - 10日上涨捕获率
    20日上涨捕获率      - 20日上涨捕获率
    30日上涨捕获率      - 30日上涨捕获率
    60日上涨捕获率      - 60日上涨捕获率
    120日上涨捕获率     - 120日上涨捕获率
    5日下跌捕获率       - 5日下跌捕获率
    10日下跌捕获率      - 10日下跌捕获率
    20日下跌捕获率      - 20日下跌捕获率
    30日下跌捕获率      - 30日下跌捕获率
    60日下跌捕获率      - 60日下跌捕获率
    120日下跌捕获率     - 120日下跌捕获率

【庄家/主力指标】
    ZJTJ_无庄控盘       - ZJTJ庄家抬轿无庄控盘
    ZJTJ_开始控盘       - ZJTJ庄家抬轿开始控盘
    ZJTJ_有庄控盘       - ZJTJ庄家抬轿有庄控盘
    ZJTJ_主力出货       - ZJTJ庄家抬轿主力出货
    CYW                 - CYW主力控盘
    ZLJC_JCS            - ZLJC主力进出JCS
    ZLJC_JCM            - ZLJC主力进出JCM
    ZLJC_JCL            - ZLJC主力进出JCL
    ZLMM_MMS            - ZLMM主力买卖MMS
    ZLMM_MMM            - ZLMM主力买卖MMM
    ZLMM_MML            - ZLMM主力买卖MML
    LHXJ_主力弃盘       - LHXJ猎狐先觉主力弃盘
    LHXJ_主力控盘       - LHXJ猎狐先觉主力控盘
    LYJH_机构做空能量线  - LYJH猎鹰歼狐机构做空能量线
    LYJH_机构做多能量线  - LYJH猎鹰歼狐机构做多能量线

【智能交易信号】
    BDZX_AK             - BDZX波段之星AK
    BDZX_AD1            - BDZX波段之星AD1
    BDZX_AJ             - BDZX波段之星AJ
    BDZX_买进           - BDZX波段之星买进信号
    BDZX_卖出           - BDZX波段之星卖出信号
    CYHT_SK             - CYHT财运亨通SK
    CYHT_SD             - CYHT财运亨通SD
    CYHT_卖出           - CYHT财运亨通卖出信号
    CYHT_买进           - CYHT财运亨通买进信号
    BSQJ_B买            - BSQJ买卖区间B买信号
    BSQJ_持仓           - BSQJ买卖区间持仓信号
    BSQJ_S卖            - BSQJ买卖区间S卖信号
    BSQJ_空仓           - BSQJ买卖区间空仓信号
    JFZX_多头力量       - JFZX飓风智能中线多头力量
    JFZX_空头力量       - JFZX飓风智能中线空头力量
    XJDX_J              - XJDX超级短线J
    XJDX_D              - XJDX超级短线D
    XJDX_K              - XJDX超级短线K

【其他特色指标】
    CYS                 - CYS市场盈亏
    CYR_CYR             - CYR市场强弱CYR
    CYR_MACYR           - CYR市场强弱MACYR
    CYE_CYEL            - CYE市场趋势CYEL
    CYE_CYES            - CYE市场趋势CYES
    CYS                 - CYS市场盈亏
    RAD_RADER1          - RAD威力雷达RADER1
    RAD_RADERMA         - RAD威力雷达RADERMA
    SG_XDT_QR           - SG_XDT心电图QR
    SG_XDT_MQR1         - SG_XDT心电图MQR1
    SG_XDT_MQR2         - SG_XDT心电图MQR2
    SG_NDB_DK           - SG_NDB脑电波DK
    SG_NDB_MDK1         - SG_NDB脑电波MDK1
    SG_NDB_MDK2         - SG_NDB脑电波MDK2
    SG_SMX_ZY1          - SG_SMX生命线ZY1
    SG_SMX_ZY2          - SG_SMX生命线ZY2
    SG_SMX_ZY3          - SG_SMX生命线ZY3
    SG_LB_量比          - SG_LB量比
    SG_LB_MA5           - SG_LB量比MA5
    SG_LB_MA10          - SG_LB量比MA10
    SG_PF               - SG_PF强势股评分
    SLZT_白龙           - SLZT神龙在天白龙
    SLZT_黄龙           - SLZT神龙在天黄龙
    SLZT_紫龙           - SLZT神龙在天紫龙
    SLZT_青龙           - SLZT神龙在天青龙
    SLZT_红龙           - SLZT神龙在天红龙
    SLZT_蓝龙           - SLZT神龙在天蓝龙
    ADVOL_ADVOL         - ADVOL龙系离散量ADVOL
    ADVOL_MA1           - ADVOL龙系离散量MA1
    ADVOL_MA2           - ADVOL龙系离散量MA2
    JAX_J               - JAX济安线J
    JAX_A               - JAX济安线A
    JAX_X               - JAX济安线X
    LON_LON             - LON龙系长线LON
    LON_LONMA           - LON龙系长线LONMA
    LON_LONT            - LON龙系长线LONT
    SHT_SHT             - SHT龙系短线SHT
    SHT_SHTMA           - SHT龙系短线SHTMA
    CDP_STD_CDP         - CDP_STD逆势操作CDP
    CDP_STD_AH          - CDP_STD逆势操作AH
    CDP_STD_NH          - CDP_STD逆势操作NH
    CDP_STD_NL          - CDP_STD逆势操作NL
    CDP_STD_AL          - CDP_STD逆势操作AL
"""

print("\n" + "=" * 60)
print("📈 获取因子数据")
print("=" * 60)

# 获取基础因子数据
result = client.get_stock_factor_data(
    stock='513100.SH',      # 纳指ETF
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,high,low,volume,amount'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取涨跌幅因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='159915.SZ',      # 创业板ETF
    start_date='20220101',
    end_date='20241231',
    columns='date,证券代码,5日涨跌幅,10日涨跌幅,20日涨跌幅,60日涨跌幅'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取技术指标因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,MACD_DIF,MACD_DEA,MACD_MACD,KDJ_K,KDJ_D,KDJ_J,RSI1,RSI2,RSI3,BOLL_BOLL,BOLL_UB,BOLL_LB'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（技术指标）")
print(df.head())

# 获取均线系统因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,5日均线,10日均线,20日均线,30日均线,60日均线,120日均线'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（均线系统）")
print(df.head())

# 获取Alpha因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,Alpha001,Alpha002,Alpha003,Alpha004,Alpha005'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（Alpha因子）")
print(df.head())

# 获取动量因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,3日回归动量,5日回归动量,10日回归动量,20日回归动量,30日回归动量,60日回归动量'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（动量因子）")
print(df.head())
```
## 6读取ETF基金因子数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例3：获取因子数据
# ============================================================
"""
参数说明：
    stock: str = '600031.SH'        - 股票代码
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD
    columns: str = 'date,close,open,high,low,volume,amount'  - 选择字段，逗号分隔

【基础因子字段】
    date                - 交易日期
    证券代码            - 股票代码
    close               - 收盘价
    open                - 开盘价
    high                - 最高价
    low                 - 最低价
    volume              - 成交量
    amount              - 成交金额
    zdf                 - 涨跌幅

【涨跌幅因子】
    5日涨跌幅           - 5日涨跌幅
    10日涨跌幅          - 10日涨跌幅
    20日涨跌幅          - 20日涨跌幅
    30日涨跌幅          - 30日涨跌幅
    60日涨跌幅          - 60日涨跌幅
    120日涨跌幅         - 120日涨跌幅
    250日涨跌幅         - 250日涨跌幅

【价格距离均线涨跌幅】
    价格距离5日均线涨跌幅   - 价格距离5日均线涨跌幅
    价格距离10日均线涨跌幅  - 价格距离10日均线涨跌幅
    价格距离20日均线涨跌幅  - 价格距离20日均线涨跌幅
    价格距离30日均线涨跌幅  - 价格距离30日均线涨跌幅
    价格距离60日均线涨跌幅  - 价格距离60日均线涨跌幅
    价格距离120日均线涨跌幅 - 价格距离120日均线涨跌幅

【均线距离涨跌幅】
    5日均线距离10日均线涨跌幅  - 5日均线距离10日均线涨跌幅
    10日均线距离20日均线涨跌幅 - 10日均线距离20日均线涨跌幅
    20日均线距离30日均线涨跌幅 - 20日均线距离30日均线涨跌幅
    30日均线距离60日均线涨跌幅 - 30日均线距离60日均线涨跌幅
    60日均线距离120日均线涨跌幅 - 60日均线距离120日均线涨跌幅

【移动平均线】
    5日均线             - 5日均线
    10日均线            - 10日均线
    20日均线            - 20日均线
    30日均线            - 30日均线
    60日均线            - 60日均线
    120日均线           - 120日均线

【均线交叉信号】
    5日10日金叉         - 5日10日均线金叉
    10日20日金叉        - 10日20日均线金叉
    20日30日金叉        - 20日30日均线金叉
    30日60日金叉        - 30日60日均线金叉
    60日120日金叉       - 60日120日均线金叉
    5日10日死叉         - 5日10日均线死叉
    10日20日死叉        - 10日20日均线死叉
    20日30日死叉        - 20日30日均线死叉
    30日60日死叉        - 30日60日均线死叉
    60日120日死叉       - 60日120日均线死叉

【价格位置判断】
    价格在5均线上        - 价格是否在5日均线上
    价格在10均线上       - 价格是否在10日均线上
    价格在20均线上       - 价格是否在20日均线上
    价格在30均线上       - 价格是否在30日均线上
    价格在60均线上       - 价格是否在60日均线上
    价格在120均线上      - 价格是否在120日均线上
    5均线在10均线上      - 5日均线是否在10日均线上
    10均线在20均线上     - 10日均线是否在20日均线上
    20均线在30均线上     - 20日均线是否在30日均线上
    30均线在60均线上     - 30日均线是否在60日均线上
    60均线在120均线上    - 60日均线是否在120日均线上

【技术指标 - KDJ】
    KDJ_K               - KDJ指标K值
    KDJ_D               - KDJ指标D值
    KDJ_J               - KDJ指标J值
    KDJ_KD金叉          - KDJ金叉信号
    KDJ_KD死叉          - KDJ死叉信号

【技术指标 - MACD】
    MACD_DIF            - MACD平滑异同平均线DIF
    MACD_DEA            - MACD平滑异同平均线DEA
    MACD_MACD           - MACD平滑异同平均线MACD
    MACD_金叉           - MACD金叉信号
    MACD_死叉           - MACD死叉信号

【技术指标 - RSI】
    RSI1                - RSI相对强弱RSI1
    RSI2                - RSI相对强弱RSI2
    RSI3                - RSI相对强弱RSI3
    RSI_金叉            - RSI金叉信号
    RSI_死叉            - RSI死叉信号

【技术指标 - BOLL布林线】
    BOLL_BOLL           - BOLL布林线中轨
    BOLL_UB             - BOLL布林线上轨
    BOLL_LB             - BOLL布林线下轨

【技术指标 - CCI】
    CCI                 - CCI商品路径指标

【技术指标 - MFI】
    MFI                 - MFI资金流量指标

【技术指标 - MTM】
    MTM_MTM             - MTM动量线MTM值
    MTM_MTMMA           - MTM动量线MTMMA值

【技术指标 - SKDJ】
    SKDJ_K              - SKDJ慢速随机K值
    SKDJ_D              - SKDJ慢速随机D值

【技术指标 - WR】
    WR1                 - WR威廉指标WR1
    WR2                 - WR威廉指标WR2
    WR_金叉             - WR金叉信号
    WR_死叉             - WR死叉信号

【技术指标 - PSY】
    PSY_PSY             - PSY心理线PSY
    PSY_PSYMA           - PSY心理线PSYMA
    PSY_金叉            - PSY金叉信号
    PSY_死叉            - PSY死叉信号

【技术指标 - BIAS乖离率】
    BIAS1               - BIAS乖离率BIAS1
    BIAS2               - BIAS乖离率BIAS2
    BIAS3               - BIAS乖离率BIAS3
    BIAS_QL_BIAS        - BIAS_QL乖离率传统版BIAS值
    BIAS_QL_BIASMA      - BIAS_QL乖离率传统版BIASMA值
    BIAS36_BIAS36       - BIAS36三六乖离BIAS36
    BIAS36_BIAS612      - BIAS36三六乖离BIAS612
    BIAS36_MABIAS       - BIAS36三六乖离MABIAS

【技术指标 - DMI】
    DMI_PDI             - DMI趋向指标PDI
    DMI_MDI             - DMI趋向指标MDI
    DMI_ADX             - DMI趋向指标ADX
    DMI_ADXR            - DMI趋向指标ADXR

【技术指标 - DMA】
    DMA_XT_DIF          - DMA_XT平均差DIF
    DMA_XT_DIFMA        - DMA_XT平均差DIFMA

【技术指标 - DPO】
    DPO_DPO             - DPO区间震荡线DPO
    DPO_MADPO           - DPO区间震荡线MADPO

【技术指标 - EMV】
    EMV_EMV             - EMV简易波动指标EMV
    EMV_MAEMV           - EMV简易波动指标MAEMV

【技术指标 - TRIX】
    TRIX_TRIX           - TRIX三重指数平均线TRIX
    TRIX_MATRIX         - TRIX三重指数平均线MATRIX

【技术指标 - UOS】
    UOS_UOS             - UOS终极指标UOS
    UOS_MAUOS           - UOS终极指标MAUOS

【技术指标 - VPT】
    VTP_VPT             - VPT量价曲线VPT
    VTP_MAVP            - VPT量价曲线MAVP

【技术指标 - WVAD】
    WVAD_WVAD           - WVAD威廉变异离散量WVAD
    WVAD_MAWVAD         - WVAD威廉变异离散量MAWVAD

【技术指标 - BRAR】
    BRAR_BR             - BRAR情绪指标BR
    BRAR_AR             - BRAR情绪指标AR

【技术指标 - CR】
    CR_CR               - CR带状能量线CR
    CR_MA1              - CR带状能量线MA1
    CR_MA2              - CR带状能量线MA2
    CR_MA3              - CR带状能量线MA3
    CR_MA4              - CR带状能量线MA4

【技术指标 - MASS】
    MASS_MASS           - MASS梅斯线MASS
    MASS_MAMASS         - MASS梅斯线MAMASS

【技术指标 - VR】
    VR_VR               - VR成交量变异率VR
    VR_MAVR             - VR成交量变异率MAVR

【技术指标 - OBV】
    OBV_OBV             - OBV累积能量线OBV
    OBV_MAOBV           - OBV累积能量线MAOBV

【技术指标 - VOL成交量】
    VOL_XT_MAVOL1       - VOL成交量MAVOL1
    VOL_XT_MAVOL2       - VOL成交量MAVOL2

【技术指标 - VRSI】
    VRSI1               - VRSI相对强弱量RSI1
    VRSI2               - VRSI相对强弱量RSI2
    VRSI3               - VRSI相对强弱量RSI3

【技术指标 - HSL换手线】
    HSL_HSL             - HSL换手线HSL
    HSL_MAHSL           - HSL换手线MAHSL

【技术指标 - ACD】
    ACD_ACD             - ACD升降线ACD
    ACD_MAACD           - ACD升降线MAACD

【技术指标 - BBI】
    BBI                 - BBI多空均线

【技术指标 - EXPMA】
    EXPMA_EXP1          - EXPMA指数平均线EXP1
    EXPMA_EXP2          - EXPMA指数平均线EXP2

【技术指标 - SAR】
    SAR                 - SAR抛物线指标

【技术指标 - AMO成交金额】
    AMO_AMOW            - AMO成交金额AMOW
    AMO_AMO1            - AMO成交金额AMO1
    AMO_AMO2            - AMO成交金额AMO2

【技术指标 - MIKE】
    MIKE_STOR           - MIKE麦克支撑压力STOR
    MIKE_MIDR           - MIKE麦克支撑压力MIDR
    MIKE_WEKR           - MIKE麦克支撑压力WEKR
    MIKE_WEKS           - MIKE麦克支撑压力WEKS
    MIKE_MIDS           - MIKE麦克支撑压力MIDS
    MIKE_STOS           - MIKE麦克支撑压力STOS

【技术指标 - ENE】
    ENE_UPPER           - ENE轨道线上轨
    ENE_LOWER           - ENE轨道线下轨
    ENE_ENE             - ENE轨道线ENE

【技术指标 - PBX瀑布线】
    PBX_PBX1            - PBX瀑布线PBX1
    PBX_PBX2            - PBX瀑布线PBX2
    PBX_PBX3            - PBX瀑布线PBX3
    PBX_PBX4            - PBX瀑布线PBX4
    PBX_PBX5            - PBX瀑布线PBX5
    PBX_PBX6            - PBX瀑布线PBX6

【技术指标 - XS薛斯通道】
    XS_SUP              - XS薛斯通道SUP
    XS_SDN              - XS薛斯通道SDN
    XS_LUP              - XS薛斯通道LUP
    XS_LDN              - XS薛斯通道LDN

【技术指标 - TQN唐奇安通道】
    TQN_周期高点        - TQN唐奇安通道周期高点
    TQN_周期低点        - TQN唐奇安通道周期低点
    TQN_平空开多        - TQN唐奇安通道平空开多信号
    TQN_平多开空        - TQN唐奇安通道平多开空信号

【技术指标 - ALLIGAT鳄鱼线】
    ALLIGAT_上唇        - ALLIGAT鳄鱼线上唇
    ALLIGAT_牙齿        - ALLIGAT鳄鱼线牙齿
    ALLIGAT_下颚        - ALLIGAT鳄鱼线下颚

【技术指标 - GMMA顾比均线】
    GMMA_MA3            - GMMA顾比均线MA3
    GMMA_MA5            - GMMA顾比均线MA5
    GMMA_MA8            - GMMA顾比均线MA8
    GMMA_MA10           - GMMA顾比均线MA10
    GMMA_MA12           - GMMA顾比均线MA12
    GMMA_MA15           - GMMA顾比均线MA15
    GMMA_MA30           - GMMA顾比均线MA30
    GMMA_MA35           - GMMA顾比均线MA35
    GMMA_MA40           - GMMA顾比均线MA40
    GMMA_MA45           - GMMA顾比均线MA45
    GMMA_MA50           - GMMA顾比均线MA50
    GMMA_MA60           - GMMA顾比均线MA60

【技术指标 - VMACD】
    VMACD_DIF           - VMACD量平滑异同平均线DIF
    VMACD_DEA           - VMACD量平滑异同平均线DEA
    VMACD_MACD          - VMACD量平滑异同平均线MACD

【技术指标 - SMACD】
    SMACD_DEA           - SMACD单线平滑异同平均线DEA
    SMACD_MACD          - SMACD单线平滑异同平均线MACD

【技术指标 - QACD】
    QACD_DIF            - QACD快速异同平均线DIF
    QACD_MACD           - QACD快速异同平均线MACD
    QACD_DDIF           - QACD快速异同平均线DDIF

【技术指标 - 成交量相关】
    连续上涨天数        - 连续上涨天数
    连续下跌天数        - 连续下跌天数

【技术指标 - 偏度峰度】
    5日偏度             - 5日偏度
    10日偏度            - 10日偏度
    20日偏度            - 20日偏度
    30日偏度            - 30日偏度
    60日偏度            - 60日偏度
    120日偏度           - 120日偏度
    5日峰度             - 5日峰度
    10日峰度            - 10日峰度
    20日峰度            - 20日峰度
    30日峰度            - 30日峰度
    60日峰度            - 60日峰度
    120日峰度           - 120日峰度

【Alpha因子 - 世界金融实验室101因子】
    Alpha001 至 Alpha191 - 世界金融实验室101因子（共191个）

【交易信号因子】
    六脉神剑            - 六脉神剑交易信号
    小波段交易          - 小波段交易信号
    大波段交易          - 大波段交易信号
    波段超级买卖        - 波段超级买卖信号

【回归分析因子】
    3日回归动量         - 3日回归动量
    5日回归动量         - 5日回归动量
    7日回归动量         - 7日回归动量
    9日回归动量         - 9日回归动量
    12日回归动量        - 12日回归动量
    15日回归动量        - 15日回归动量
    18日回归动量        - 18日回归动量
    20日回归动量        - 20日回归动量
    23日回归动量        - 23日回归动量
    25日回归动量        - 25日回归动量
    28日回归动量        - 28日回归动量
    30日回归动量        - 30日回归动量
    35日回归动量        - 35日回归动量
    40日回归动量        - 40日回归动量
    45日回归动量        - 45日回归动量
    50日回归动量        - 50日回归动量
    60日回归动量        - 60日回归动量

【回归斜率】
    5日回归斜率         - 5日回归斜率
    10日回归斜率        - 10日回归斜率
    20日回归斜率        - 20日回归斜率
    30日回归斜率        - 30日回归斜率
    60日回归斜率        - 60日回归斜率
    120日回归斜率       - 120日回归斜率

【标准差】
    5日标准差           - 5日标准差
    10日标准差          - 10日标准差
    20日标准差          - 20日标准差
    30日标准差          - 30日标准差
    60日标准差          - 60日标准差
    120日标准差         - 120日标准差

【最高最低值周期】
    5日最高值到当前周期   - 5日最高值到当前周期
    10日最高值到当前周期  - 10日最高值到当前周期
    20日最高值到当前周期  - 20日最高值到当前周期
    30日最高值到当前周期  - 30日最高值到当前周期
    60日最高值到当前周期  - 60日最高值到当前周期
    120日最高值到当前周期 - 120日最高值到当前周期
    5日最低值到当前周期   - 5日最低值到当前周期
    10日最低值到当前周期  - 10日最低值到当前周期
    20日最低值到当前周期  - 20日最低值到当前周期
    30日最低值到当前周期  - 30日最低值到当前周期
    60日最低值到当前周期  - 60日最低值到当前周期
    120日最低值到当前周期 - 120日最低值到当前周期

【Alpha系数】
    5日Alpha            - 5日Alpha
    10日Alpha           - 10日Alpha
    20日Alpha           - 20日Alpha
    30日Alpha           - 30日Alpha
    60日Alpha           - 60日Alpha
    120日Alpha          - 120日Alpha

【Beta系数】
    5日Beta             - 5日Beta
    10日Beta            - 10日Beta
    20日Beta            - 20日Beta
    30日Beta            - 30日Beta
    60日Beta            - 60日Beta
    120日Beta           - 120日Beta

【夏普比率】
    5日夏普比率         - 5日夏普比率
    10日夏普比率        - 10日夏普比率
    20日夏普比率        - 20日夏普比率
    30日夏普比率        - 30日夏普比率
    60日夏普比率        - 60日夏普比率
    120日夏普比率       - 120日夏普比率

【年化波动率】
    5日年化波动率       - 5日年化波动率
    10日年化波动率      - 10日年化波动率
    20日年化波动率      - 20日年化波动率
    30日年化波动率      - 30日年化波动率
    60日年化波动率      - 60日年化波动率
    120日年化波动率     - 120日年化波动率

【最大回撤】
    5日最大回撤         - 5日最大回撤
    10日最大回撤        - 10日最大回撤
    20日最大回撤        - 20日最大回撤
    30日最大回撤        - 30日最大回撤
    60日最大回撤        - 60日最大回撤
    120日最大回撤       - 120日最大回撤

【上涨/下跌捕获率】
    5日上涨捕获率       - 5日上涨捕获率
    10日上涨捕获率      - 10日上涨捕获率
    20日上涨捕获率      - 20日上涨捕获率
    30日上涨捕获率      - 30日上涨捕获率
    60日上涨捕获率      - 60日上涨捕获率
    120日上涨捕获率     - 120日上涨捕获率
    5日下跌捕获率       - 5日下跌捕获率
    10日下跌捕获率      - 10日下跌捕获率
    20日下跌捕获率      - 20日下跌捕获率
    30日下跌捕获率      - 30日下跌捕获率
    60日下跌捕获率      - 60日下跌捕获率
    120日下跌捕获率     - 120日下跌捕获率

【庄家/主力指标】
    ZJTJ_无庄控盘       - ZJTJ庄家抬轿无庄控盘
    ZJTJ_开始控盘       - ZJTJ庄家抬轿开始控盘
    ZJTJ_有庄控盘       - ZJTJ庄家抬轿有庄控盘
    ZJTJ_主力出货       - ZJTJ庄家抬轿主力出货
    CYW                 - CYW主力控盘
    ZLJC_JCS            - ZLJC主力进出JCS
    ZLJC_JCM            - ZLJC主力进出JCM
    ZLJC_JCL            - ZLJC主力进出JCL
    ZLMM_MMS            - ZLMM主力买卖MMS
    ZLMM_MMM            - ZLMM主力买卖MMM
    ZLMM_MML            - ZLMM主力买卖MML
    LHXJ_主力弃盘       - LHXJ猎狐先觉主力弃盘
    LHXJ_主力控盘       - LHXJ猎狐先觉主力控盘
    LYJH_机构做空能量线  - LYJH猎鹰歼狐机构做空能量线
    LYJH_机构做多能量线  - LYJH猎鹰歼狐机构做多能量线

【智能交易信号】
    BDZX_AK             - BDZX波段之星AK
    BDZX_AD1            - BDZX波段之星AD1
    BDZX_AJ             - BDZX波段之星AJ
    BDZX_买进           - BDZX波段之星买进信号
    BDZX_卖出           - BDZX波段之星卖出信号
    CYHT_SK             - CYHT财运亨通SK
    CYHT_SD             - CYHT财运亨通SD
    CYHT_卖出           - CYHT财运亨通卖出信号
    CYHT_买进           - CYHT财运亨通买进信号
    BSQJ_B买            - BSQJ买卖区间B买信号
    BSQJ_持仓           - BSQJ买卖区间持仓信号
    BSQJ_S卖            - BSQJ买卖区间S卖信号
    BSQJ_空仓           - BSQJ买卖区间空仓信号
    JFZX_多头力量       - JFZX飓风智能中线多头力量
    JFZX_空头力量       - JFZX飓风智能中线空头力量
    XJDX_J              - XJDX超级短线J
    XJDX_D              - XJDX超级短线D
    XJDX_K              - XJDX超级短线K

【其他特色指标】
    CYS                 - CYS市场盈亏
    CYR_CYR             - CYR市场强弱CYR
    CYR_MACYR           - CYR市场强弱MACYR
    CYE_CYEL            - CYE市场趋势CYEL
    CYE_CYES            - CYE市场趋势CYES
    CYS                 - CYS市场盈亏
    RAD_RADER1          - RAD威力雷达RADER1
    RAD_RADERMA         - RAD威力雷达RADERMA
    SG_XDT_QR           - SG_XDT心电图QR
    SG_XDT_MQR1         - SG_XDT心电图MQR1
    SG_XDT_MQR2         - SG_XDT心电图MQR2
    SG_NDB_DK           - SG_NDB脑电波DK
    SG_NDB_MDK1         - SG_NDB脑电波MDK1
    SG_NDB_MDK2         - SG_NDB脑电波MDK2
    SG_SMX_ZY1          - SG_SMX生命线ZY1
    SG_SMX_ZY2          - SG_SMX生命线ZY2
    SG_SMX_ZY3          - SG_SMX生命线ZY3
    SG_LB_量比          - SG_LB量比
    SG_LB_MA5           - SG_LB量比MA5
    SG_LB_MA10          - SG_LB量比MA10
    SG_PF               - SG_PF强势股评分
    SLZT_白龙           - SLZT神龙在天白龙
    SLZT_黄龙           - SLZT神龙在天黄龙
    SLZT_紫龙           - SLZT神龙在天紫龙
    SLZT_青龙           - SLZT神龙在天青龙
    SLZT_红龙           - SLZT神龙在天红龙
    SLZT_蓝龙           - SLZT神龙在天蓝龙
    ADVOL_ADVOL         - ADVOL龙系离散量ADVOL
    ADVOL_MA1           - ADVOL龙系离散量MA1
    ADVOL_MA2           - ADVOL龙系离散量MA2
    JAX_J               - JAX济安线J
    JAX_A               - JAX济安线A
    JAX_X               - JAX济安线X
    LON_LON             - LON龙系长线LON
    LON_LONMA           - LON龙系长线LONMA
    LON_LONT            - LON龙系长线LONT
    SHT_SHT             - SHT龙系短线SHT
    SHT_SHTMA           - SHT龙系短线SHTMA
    CDP_STD_CDP         - CDP_STD逆势操作CDP
    CDP_STD_AH          - CDP_STD逆势操作AH
    CDP_STD_NH          - CDP_STD逆势操作NH
    CDP_STD_NL          - CDP_STD逆势操作NL
    CDP_STD_AL          - CDP_STD逆势操作AL
"""

print("\n" + "=" * 60)
print("📈 获取因子数据")
print("=" * 60)

# 获取基础因子数据
result = client.get_stock_factor_data(
    stock='513100.SH',      # 纳指ETF
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,high,low,volume,amount'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取涨跌幅因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='159915.SZ',      # 创业板ETF
    start_date='20220101',
    end_date='20241231',
    columns='date,证券代码,5日涨跌幅,10日涨跌幅,20日涨跌幅,60日涨跌幅'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取技术指标因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,MACD_DIF,MACD_DEA,MACD_MACD,KDJ_K,KDJ_D,KDJ_J,RSI1,RSI2,RSI3,BOLL_BOLL,BOLL_UB,BOLL_LB'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（技术指标）")
print(df.head())

# 获取均线系统因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,5日均线,10日均线,20日均线,30日均线,60日均线,120日均线'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（均线系统）")
print(df.head())

# 获取Alpha因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,Alpha001,Alpha002,Alpha003,Alpha004,Alpha005'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（Alpha因子）")
print(df.head())

# 获取动量因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,3日回归动量,5日回归动量,10日回归动量,20日回归动量,30日回归动量,60日回归动量'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（动量因子）")
print(df.head())
```
## 7读取可转债因子数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例3：获取因子数据
# ============================================================
"""
参数说明：
    stock: str = '600031.SH'        - 股票代码
    start_date: str = '20200101'    - 开始日期，格式YYYYMMDD
    end_date: str = '20261231'      - 结束日期，格式YYYYMMDD
    columns: str = 'date,close,open,high,low,volume,amount'  - 选择字段，逗号分隔

【基础因子字段】
    date                - 交易日期
    证券代码            - 股票代码
    close               - 收盘价
    open                - 开盘价
    high                - 最高价
    low                 - 最低价
    volume              - 成交量
    amount              - 成交金额
    zdf                 - 涨跌幅

【涨跌幅因子】
    5日涨跌幅           - 5日涨跌幅
    10日涨跌幅          - 10日涨跌幅
    20日涨跌幅          - 20日涨跌幅
    30日涨跌幅          - 30日涨跌幅
    60日涨跌幅          - 60日涨跌幅
    120日涨跌幅         - 120日涨跌幅
    250日涨跌幅         - 250日涨跌幅

【价格距离均线涨跌幅】
    价格距离5日均线涨跌幅   - 价格距离5日均线涨跌幅
    价格距离10日均线涨跌幅  - 价格距离10日均线涨跌幅
    价格距离20日均线涨跌幅  - 价格距离20日均线涨跌幅
    价格距离30日均线涨跌幅  - 价格距离30日均线涨跌幅
    价格距离60日均线涨跌幅  - 价格距离60日均线涨跌幅
    价格距离120日均线涨跌幅 - 价格距离120日均线涨跌幅

【均线距离涨跌幅】
    5日均线距离10日均线涨跌幅  - 5日均线距离10日均线涨跌幅
    10日均线距离20日均线涨跌幅 - 10日均线距离20日均线涨跌幅
    20日均线距离30日均线涨跌幅 - 20日均线距离30日均线涨跌幅
    30日均线距离60日均线涨跌幅 - 30日均线距离60日均线涨跌幅
    60日均线距离120日均线涨跌幅 - 60日均线距离120日均线涨跌幅

【移动平均线】
    5日均线             - 5日均线
    10日均线            - 10日均线
    20日均线            - 20日均线
    30日均线            - 30日均线
    60日均线            - 60日均线
    120日均线           - 120日均线

【均线交叉信号】
    5日10日金叉         - 5日10日均线金叉
    10日20日金叉        - 10日20日均线金叉
    20日30日金叉        - 20日30日均线金叉
    30日60日金叉        - 30日60日均线金叉
    60日120日金叉       - 60日120日均线金叉
    5日10日死叉         - 5日10日均线死叉
    10日20日死叉        - 10日20日均线死叉
    20日30日死叉        - 20日30日均线死叉
    30日60日死叉        - 30日60日均线死叉
    60日120日死叉       - 60日120日均线死叉

【价格位置判断】
    价格在5均线上        - 价格是否在5日均线上
    价格在10均线上       - 价格是否在10日均线上
    价格在20均线上       - 价格是否在20日均线上
    价格在30均线上       - 价格是否在30日均线上
    价格在60均线上       - 价格是否在60日均线上
    价格在120均线上      - 价格是否在120日均线上
    5均线在10均线上      - 5日均线是否在10日均线上
    10均线在20均线上     - 10日均线是否在20日均线上
    20均线在30均线上     - 20日均线是否在30日均线上
    30均线在60均线上     - 30日均线是否在60日均线上
    60均线在120均线上    - 60日均线是否在120日均线上

【技术指标 - KDJ】
    KDJ_K               - KDJ指标K值
    KDJ_D               - KDJ指标D值
    KDJ_J               - KDJ指标J值
    KDJ_KD金叉          - KDJ金叉信号
    KDJ_KD死叉          - KDJ死叉信号

【技术指标 - MACD】
    MACD_DIF            - MACD平滑异同平均线DIF
    MACD_DEA            - MACD平滑异同平均线DEA
    MACD_MACD           - MACD平滑异同平均线MACD
    MACD_金叉           - MACD金叉信号
    MACD_死叉           - MACD死叉信号

【技术指标 - RSI】
    RSI1                - RSI相对强弱RSI1
    RSI2                - RSI相对强弱RSI2
    RSI3                - RSI相对强弱RSI3
    RSI_金叉            - RSI金叉信号
    RSI_死叉            - RSI死叉信号

【技术指标 - BOLL布林线】
    BOLL_BOLL           - BOLL布林线中轨
    BOLL_UB             - BOLL布林线上轨
    BOLL_LB             - BOLL布林线下轨

【技术指标 - CCI】
    CCI                 - CCI商品路径指标

【技术指标 - MFI】
    MFI                 - MFI资金流量指标

【技术指标 - MTM】
    MTM_MTM             - MTM动量线MTM值
    MTM_MTMMA           - MTM动量线MTMMA值

【技术指标 - SKDJ】
    SKDJ_K              - SKDJ慢速随机K值
    SKDJ_D              - SKDJ慢速随机D值

【技术指标 - WR】
    WR1                 - WR威廉指标WR1
    WR2                 - WR威廉指标WR2
    WR_金叉             - WR金叉信号
    WR_死叉             - WR死叉信号

【技术指标 - PSY】
    PSY_PSY             - PSY心理线PSY
    PSY_PSYMA           - PSY心理线PSYMA
    PSY_金叉            - PSY金叉信号
    PSY_死叉            - PSY死叉信号

【技术指标 - BIAS乖离率】
    BIAS1               - BIAS乖离率BIAS1
    BIAS2               - BIAS乖离率BIAS2
    BIAS3               - BIAS乖离率BIAS3
    BIAS_QL_BIAS        - BIAS_QL乖离率传统版BIAS值
    BIAS_QL_BIASMA      - BIAS_QL乖离率传统版BIASMA值
    BIAS36_BIAS36       - BIAS36三六乖离BIAS36
    BIAS36_BIAS612      - BIAS36三六乖离BIAS612
    BIAS36_MABIAS       - BIAS36三六乖离MABIAS

【技术指标 - DMI】
    DMI_PDI             - DMI趋向指标PDI
    DMI_MDI             - DMI趋向指标MDI
    DMI_ADX             - DMI趋向指标ADX
    DMI_ADXR            - DMI趋向指标ADXR

【技术指标 - DMA】
    DMA_XT_DIF          - DMA_XT平均差DIF
    DMA_XT_DIFMA        - DMA_XT平均差DIFMA

【技术指标 - DPO】
    DPO_DPO             - DPO区间震荡线DPO
    DPO_MADPO           - DPO区间震荡线MADPO

【技术指标 - EMV】
    EMV_EMV             - EMV简易波动指标EMV
    EMV_MAEMV           - EMV简易波动指标MAEMV

【技术指标 - TRIX】
    TRIX_TRIX           - TRIX三重指数平均线TRIX
    TRIX_MATRIX         - TRIX三重指数平均线MATRIX

【技术指标 - UOS】
    UOS_UOS             - UOS终极指标UOS
    UOS_MAUOS           - UOS终极指标MAUOS

【技术指标 - VPT】
    VTP_VPT             - VPT量价曲线VPT
    VTP_MAVP            - VPT量价曲线MAVP

【技术指标 - WVAD】
    WVAD_WVAD           - WVAD威廉变异离散量WVAD
    WVAD_MAWVAD         - WVAD威廉变异离散量MAWVAD

【技术指标 - BRAR】
    BRAR_BR             - BRAR情绪指标BR
    BRAR_AR             - BRAR情绪指标AR

【技术指标 - CR】
    CR_CR               - CR带状能量线CR
    CR_MA1              - CR带状能量线MA1
    CR_MA2              - CR带状能量线MA2
    CR_MA3              - CR带状能量线MA3
    CR_MA4              - CR带状能量线MA4

【技术指标 - MASS】
    MASS_MASS           - MASS梅斯线MASS
    MASS_MAMASS         - MASS梅斯线MAMASS

【技术指标 - VR】
    VR_VR               - VR成交量变异率VR
    VR_MAVR             - VR成交量变异率MAVR

【技术指标 - OBV】
    OBV_OBV             - OBV累积能量线OBV
    OBV_MAOBV           - OBV累积能量线MAOBV

【技术指标 - VOL成交量】
    VOL_XT_MAVOL1       - VOL成交量MAVOL1
    VOL_XT_MAVOL2       - VOL成交量MAVOL2

【技术指标 - VRSI】
    VRSI1               - VRSI相对强弱量RSI1
    VRSI2               - VRSI相对强弱量RSI2
    VRSI3               - VRSI相对强弱量RSI3

【技术指标 - HSL换手线】
    HSL_HSL             - HSL换手线HSL
    HSL_MAHSL           - HSL换手线MAHSL

【技术指标 - ACD】
    ACD_ACD             - ACD升降线ACD
    ACD_MAACD           - ACD升降线MAACD

【技术指标 - BBI】
    BBI                 - BBI多空均线

【技术指标 - EXPMA】
    EXPMA_EXP1          - EXPMA指数平均线EXP1
    EXPMA_EXP2          - EXPMA指数平均线EXP2

【技术指标 - SAR】
    SAR                 - SAR抛物线指标

【技术指标 - AMO成交金额】
    AMO_AMOW            - AMO成交金额AMOW
    AMO_AMO1            - AMO成交金额AMO1
    AMO_AMO2            - AMO成交金额AMO2

【技术指标 - MIKE】
    MIKE_STOR           - MIKE麦克支撑压力STOR
    MIKE_MIDR           - MIKE麦克支撑压力MIDR
    MIKE_WEKR           - MIKE麦克支撑压力WEKR
    MIKE_WEKS           - MIKE麦克支撑压力WEKS
    MIKE_MIDS           - MIKE麦克支撑压力MIDS
    MIKE_STOS           - MIKE麦克支撑压力STOS

【技术指标 - ENE】
    ENE_UPPER           - ENE轨道线上轨
    ENE_LOWER           - ENE轨道线下轨
    ENE_ENE             - ENE轨道线ENE

【技术指标 - PBX瀑布线】
    PBX_PBX1            - PBX瀑布线PBX1
    PBX_PBX2            - PBX瀑布线PBX2
    PBX_PBX3            - PBX瀑布线PBX3
    PBX_PBX4            - PBX瀑布线PBX4
    PBX_PBX5            - PBX瀑布线PBX5
    PBX_PBX6            - PBX瀑布线PBX6

【技术指标 - XS薛斯通道】
    XS_SUP              - XS薛斯通道SUP
    XS_SDN              - XS薛斯通道SDN
    XS_LUP              - XS薛斯通道LUP
    XS_LDN              - XS薛斯通道LDN

【技术指标 - TQN唐奇安通道】
    TQN_周期高点        - TQN唐奇安通道周期高点
    TQN_周期低点        - TQN唐奇安通道周期低点
    TQN_平空开多        - TQN唐奇安通道平空开多信号
    TQN_平多开空        - TQN唐奇安通道平多开空信号

【技术指标 - ALLIGAT鳄鱼线】
    ALLIGAT_上唇        - ALLIGAT鳄鱼线上唇
    ALLIGAT_牙齿        - ALLIGAT鳄鱼线牙齿
    ALLIGAT_下颚        - ALLIGAT鳄鱼线下颚

【技术指标 - GMMA顾比均线】
    GMMA_MA3            - GMMA顾比均线MA3
    GMMA_MA5            - GMMA顾比均线MA5
    GMMA_MA8            - GMMA顾比均线MA8
    GMMA_MA10           - GMMA顾比均线MA10
    GMMA_MA12           - GMMA顾比均线MA12
    GMMA_MA15           - GMMA顾比均线MA15
    GMMA_MA30           - GMMA顾比均线MA30
    GMMA_MA35           - GMMA顾比均线MA35
    GMMA_MA40           - GMMA顾比均线MA40
    GMMA_MA45           - GMMA顾比均线MA45
    GMMA_MA50           - GMMA顾比均线MA50
    GMMA_MA60           - GMMA顾比均线MA60

【技术指标 - VMACD】
    VMACD_DIF           - VMACD量平滑异同平均线DIF
    VMACD_DEA           - VMACD量平滑异同平均线DEA
    VMACD_MACD          - VMACD量平滑异同平均线MACD

【技术指标 - SMACD】
    SMACD_DEA           - SMACD单线平滑异同平均线DEA
    SMACD_MACD          - SMACD单线平滑异同平均线MACD

【技术指标 - QACD】
    QACD_DIF            - QACD快速异同平均线DIF
    QACD_MACD           - QACD快速异同平均线MACD
    QACD_DDIF           - QACD快速异同平均线DDIF

【技术指标 - 成交量相关】
    连续上涨天数        - 连续上涨天数
    连续下跌天数        - 连续下跌天数

【技术指标 - 偏度峰度】
    5日偏度             - 5日偏度
    10日偏度            - 10日偏度
    20日偏度            - 20日偏度
    30日偏度            - 30日偏度
    60日偏度            - 60日偏度
    120日偏度           - 120日偏度
    5日峰度             - 5日峰度
    10日峰度            - 10日峰度
    20日峰度            - 20日峰度
    30日峰度            - 30日峰度
    60日峰度            - 60日峰度
    120日峰度           - 120日峰度

【Alpha因子 - 世界金融实验室101因子】
    Alpha001 至 Alpha191 - 世界金融实验室101因子（共191个）

【交易信号因子】
    六脉神剑            - 六脉神剑交易信号
    小波段交易          - 小波段交易信号
    大波段交易          - 大波段交易信号
    波段超级买卖        - 波段超级买卖信号

【回归分析因子】
    3日回归动量         - 3日回归动量
    5日回归动量         - 5日回归动量
    7日回归动量         - 7日回归动量
    9日回归动量         - 9日回归动量
    12日回归动量        - 12日回归动量
    15日回归动量        - 15日回归动量
    18日回归动量        - 18日回归动量
    20日回归动量        - 20日回归动量
    23日回归动量        - 23日回归动量
    25日回归动量        - 25日回归动量
    28日回归动量        - 28日回归动量
    30日回归动量        - 30日回归动量
    35日回归动量        - 35日回归动量
    40日回归动量        - 40日回归动量
    45日回归动量        - 45日回归动量
    50日回归动量        - 50日回归动量
    60日回归动量        - 60日回归动量

【回归斜率】
    5日回归斜率         - 5日回归斜率
    10日回归斜率        - 10日回归斜率
    20日回归斜率        - 20日回归斜率
    30日回归斜率        - 30日回归斜率
    60日回归斜率        - 60日回归斜率
    120日回归斜率       - 120日回归斜率

【标准差】
    5日标准差           - 5日标准差
    10日标准差          - 10日标准差
    20日标准差          - 20日标准差
    30日标准差          - 30日标准差
    60日标准差          - 60日标准差
    120日标准差         - 120日标准差

【最高最低值周期】
    5日最高值到当前周期   - 5日最高值到当前周期
    10日最高值到当前周期  - 10日最高值到当前周期
    20日最高值到当前周期  - 20日最高值到当前周期
    30日最高值到当前周期  - 30日最高值到当前周期
    60日最高值到当前周期  - 60日最高值到当前周期
    120日最高值到当前周期 - 120日最高值到当前周期
    5日最低值到当前周期   - 5日最低值到当前周期
    10日最低值到当前周期  - 10日最低值到当前周期
    20日最低值到当前周期  - 20日最低值到当前周期
    30日最低值到当前周期  - 30日最低值到当前周期
    60日最低值到当前周期  - 60日最低值到当前周期
    120日最低值到当前周期 - 120日最低值到当前周期

【Alpha系数】
    5日Alpha            - 5日Alpha
    10日Alpha           - 10日Alpha
    20日Alpha           - 20日Alpha
    30日Alpha           - 30日Alpha
    60日Alpha           - 60日Alpha
    120日Alpha          - 120日Alpha

【Beta系数】
    5日Beta             - 5日Beta
    10日Beta            - 10日Beta
    20日Beta            - 20日Beta
    30日Beta            - 30日Beta
    60日Beta            - 60日Beta
    120日Beta           - 120日Beta

【夏普比率】
    5日夏普比率         - 5日夏普比率
    10日夏普比率        - 10日夏普比率
    20日夏普比率        - 20日夏普比率
    30日夏普比率        - 30日夏普比率
    60日夏普比率        - 60日夏普比率
    120日夏普比率       - 120日夏普比率

【年化波动率】
    5日年化波动率       - 5日年化波动率
    10日年化波动率      - 10日年化波动率
    20日年化波动率      - 20日年化波动率
    30日年化波动率      - 30日年化波动率
    60日年化波动率      - 60日年化波动率
    120日年化波动率     - 120日年化波动率

【最大回撤】
    5日最大回撤         - 5日最大回撤
    10日最大回撤        - 10日最大回撤
    20日最大回撤        - 20日最大回撤
    30日最大回撤        - 30日最大回撤
    60日最大回撤        - 60日最大回撤
    120日最大回撤       - 120日最大回撤

【上涨/下跌捕获率】
    5日上涨捕获率       - 5日上涨捕获率
    10日上涨捕获率      - 10日上涨捕获率
    20日上涨捕获率      - 20日上涨捕获率
    30日上涨捕获率      - 30日上涨捕获率
    60日上涨捕获率      - 60日上涨捕获率
    120日上涨捕获率     - 120日上涨捕获率
    5日下跌捕获率       - 5日下跌捕获率
    10日下跌捕获率      - 10日下跌捕获率
    20日下跌捕获率      - 20日下跌捕获率
    30日下跌捕获率      - 30日下跌捕获率
    60日下跌捕获率      - 60日下跌捕获率
    120日下跌捕获率     - 120日下跌捕获率

【庄家/主力指标】
    ZJTJ_无庄控盘       - ZJTJ庄家抬轿无庄控盘
    ZJTJ_开始控盘       - ZJTJ庄家抬轿开始控盘
    ZJTJ_有庄控盘       - ZJTJ庄家抬轿有庄控盘
    ZJTJ_主力出货       - ZJTJ庄家抬轿主力出货
    CYW                 - CYW主力控盘
    ZLJC_JCS            - ZLJC主力进出JCS
    ZLJC_JCM            - ZLJC主力进出JCM
    ZLJC_JCL            - ZLJC主力进出JCL
    ZLMM_MMS            - ZLMM主力买卖MMS
    ZLMM_MMM            - ZLMM主力买卖MMM
    ZLMM_MML            - ZLMM主力买卖MML
    LHXJ_主力弃盘       - LHXJ猎狐先觉主力弃盘
    LHXJ_主力控盘       - LHXJ猎狐先觉主力控盘
    LYJH_机构做空能量线  - LYJH猎鹰歼狐机构做空能量线
    LYJH_机构做多能量线  - LYJH猎鹰歼狐机构做多能量线

【智能交易信号】
    BDZX_AK             - BDZX波段之星AK
    BDZX_AD1            - BDZX波段之星AD1
    BDZX_AJ             - BDZX波段之星AJ
    BDZX_买进           - BDZX波段之星买进信号
    BDZX_卖出           - BDZX波段之星卖出信号
    CYHT_SK             - CYHT财运亨通SK
    CYHT_SD             - CYHT财运亨通SD
    CYHT_卖出           - CYHT财运亨通卖出信号
    CYHT_买进           - CYHT财运亨通买进信号
    BSQJ_B买            - BSQJ买卖区间B买信号
    BSQJ_持仓           - BSQJ买卖区间持仓信号
    BSQJ_S卖            - BSQJ买卖区间S卖信号
    BSQJ_空仓           - BSQJ买卖区间空仓信号
    JFZX_多头力量       - JFZX飓风智能中线多头力量
    JFZX_空头力量       - JFZX飓风智能中线空头力量
    XJDX_J              - XJDX超级短线J
    XJDX_D              - XJDX超级短线D
    XJDX_K              - XJDX超级短线K

【其他特色指标】
    CYS                 - CYS市场盈亏
    CYR_CYR             - CYR市场强弱CYR
    CYR_MACYR           - CYR市场强弱MACYR
    CYE_CYEL            - CYE市场趋势CYEL
    CYE_CYES            - CYE市场趋势CYES
    CYS                 - CYS市场盈亏
    RAD_RADER1          - RAD威力雷达RADER1
    RAD_RADERMA         - RAD威力雷达RADERMA
    SG_XDT_QR           - SG_XDT心电图QR
    SG_XDT_MQR1         - SG_XDT心电图MQR1
    SG_XDT_MQR2         - SG_XDT心电图MQR2
    SG_NDB_DK           - SG_NDB脑电波DK
    SG_NDB_MDK1         - SG_NDB脑电波MDK1
    SG_NDB_MDK2         - SG_NDB脑电波MDK2
    SG_SMX_ZY1          - SG_SMX生命线ZY1
    SG_SMX_ZY2          - SG_SMX生命线ZY2
    SG_SMX_ZY3          - SG_SMX生命线ZY3
    SG_LB_量比          - SG_LB量比
    SG_LB_MA5           - SG_LB量比MA5
    SG_LB_MA10          - SG_LB量比MA10
    SG_PF               - SG_PF强势股评分
    SLZT_白龙           - SLZT神龙在天白龙
    SLZT_黄龙           - SLZT神龙在天黄龙
    SLZT_紫龙           - SLZT神龙在天紫龙
    SLZT_青龙           - SLZT神龙在天青龙
    SLZT_红龙           - SLZT神龙在天红龙
    SLZT_蓝龙           - SLZT神龙在天蓝龙
    ADVOL_ADVOL         - ADVOL龙系离散量ADVOL
    ADVOL_MA1           - ADVOL龙系离散量MA1
    ADVOL_MA2           - ADVOL龙系离散量MA2
    JAX_J               - JAX济安线J
    JAX_A               - JAX济安线A
    JAX_X               - JAX济安线X
    LON_LON             - LON龙系长线LON
    LON_LONMA           - LON龙系长线LONMA
    LON_LONT            - LON龙系长线LONT
    SHT_SHT             - SHT龙系短线SHT
    SHT_SHTMA           - SHT龙系短线SHTMA
    CDP_STD_CDP         - CDP_STD逆势操作CDP
    CDP_STD_AH          - CDP_STD逆势操作AH
    CDP_STD_NH          - CDP_STD逆势操作NH
    CDP_STD_NL          - CDP_STD逆势操作NL
    CDP_STD_AL          - CDP_STD逆势操作AL
"""

print("\n" + "=" * 60)
print("📈 获取因子数据")
print("=" * 60)

# 获取基础因子数据
result = client.get_stock_factor_data(
    stock='513100.SH',      # 纳指ETF
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,high,low,volume,amount'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取涨跌幅因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='159915.SZ',      # 创业板ETF
    start_date='20220101',
    end_date='20241231',
    columns='date,证券代码,5日涨跌幅,10日涨跌幅,20日涨跌幅,60日涨跌幅'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())

# 获取技术指标因子数据
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,MACD_DIF,MACD_DEA,MACD_MACD,KDJ_K,KDJ_D,KDJ_J,RSI1,RSI2,RSI3,BOLL_BOLL,BOLL_UB,BOLL_LB'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（技术指标）")
print(df.head())

# 获取均线系统因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,5日均线,10日均线,20日均线,30日均线,60日均线,120日均线'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（均线系统）")
print(df.head())

# 获取Alpha因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='128137.SZ',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,Alpha001,Alpha002,Alpha003,Alpha004,Alpha005'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（Alpha因子）")
print(df.head())

# 获取动量因子
print("\n" + "-" * 40)
result = client.get_stock_factor_data(
    stock='513100.SH',
    start_date='20240101',
    end_date='20500101',
    columns='date,证券代码,close,3日回归动量,5日回归动量,10日回归动量,20日回归动量,30日回归动量,60日回归动量'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据（动量因子）")
print(df.head())
```
## 8. 获取财务数据 获取资产负债表
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例4：获取资产负债表（全部字段）
# ============================================================
"""
参数说明：
    table: str = '资产负债表'       - 财务表类型
    date: str = '2026-06-30'        - 报告日期，格式YYYY-MM-DD
    columns: str = 'secu_code,end_date,total_assets'  - 选择字段，逗号分隔

财务表类型：
    '资产负债表'     - 资产负债表
    '利润表'         - 利润表
    '现金流量表'     - 现金流量表
    '估值数据'       - 估值数据
    '成长能力'       - 成长能力指标
    '盈利能力'       - 盈利能力指标
    '每股指标'       - 每股指标
    '营运能力'       - 营运能力指标
    '偿债能力'       - 偿债能力指标

【资产负债表 - balance_statement 全部字段】
    secu_code                       - 股票代码
    secu_abbr                       - 股票简称
    company_type                    - 公司类型
    end_date                        - 截止日期
    publ_date                       - 公告日期
    settlement_provi                - 结算备付金
    client_provi                    - 客户备付金
    deposit_in_interbank            - 存放同业款项
    r_metal                         - 贵金属
    lend_capital                    - 拆出资金
    derivative_assets               - 衍生金融资产
    bought_sellback_assets          - 买入返售金融资产
    loan_and_advance                - 发放贷款和垫款
    insurance_receivables           - 应收保费
    receivable_subrogation_fee      - 应收代位追偿款
    reinsurance_receivables         - 应收分保账款
    receivable_unearned_r           - 应收分保未到期责任准备金
    receivable_claims_r             - 应收分保未决赔款准备金
    receivable_life_r               - 应收分保寿险责任准备金
    receivable_lt_health_r          - 应收分保长期健康险责任准备金
    insurer_impawn_loan             - 保户质押贷款
    fixed_deposit                   - 定期存款
    refundable_capital_deposit      - 存出资本保证金
    refundable_deposit              - 存出保证金
    independence_account_assets     - 独立账户资产
    other_assets                    - 其他资产
    borrowing_from_centralbank      - 向中央银行借款
    deposit_of_interbank            - 同业及其他金融机构存放款项
    borrowing_capital               - 拆入资金
    derivative_liability            - 衍生金融负债
    sold_buyback_secu_proceeds      - 卖出回购金融资产款
    deposit                         - 吸收存款
    proxy_secu_proceeds             - 代理买卖证券款
    sub_issue_secu_proceeds         - 代理承销证券款
    deposits_received               - 存入保证金
    advance_insurance               - 预收保费
    commission_payable              - 应付手续费及佣金
    reinsurance_payables            - 应付分保账款
    compensation_payable            - 应付赔付款
    policy_dividend_payable         - 应付保单红利
    insurer_deposit_investment      - 保户储金及投资款
    unearned_premium_reserve        - 未到期责任准备金
    outstanding_claim_reserve       - 未决赔款准备金
    life_insurance_reserve          - 寿险责任准备金
    lt_health_insurance_lr          - 长期健康险责任准备金
    independence_liability          - 独立账户负债
    other_liability                 - 其他负债
    cash_equivalents                - 货币资金
    client_deposit                  - 客户资金存款
    trading_assets                  - 交易性金融资产
    bill_receivable                 - 应收票据
    dividend_receivable             - 应收股利
    interest_receivable             - 应收利息
    account_receivable              - 应收账款
    other_receivable                - 其他应收款
    advance_payment                 - 预付款项
    inventories                     - 存货
    non_current_asset_in_one_year   - 一年内到期的非流动资产
    other_current_assets            - 其他流动资产
    total_current_assets            - 流动资产合计
    shortterm_loan                  - 短期借款
    impawned_loan                   - 质押借款
    trading_liability               - 交易性金融负债
    notes_payable                   - 应付票据
    accounts_payable                - 应付账款
    advance_receipts                - 预收款项
    salaries_payable                - 应付职工薪酬
    dividend_payable                - 应付股利
    taxs_payable                    - 应交税费
    interest_payable                - 应付利息
    other_payable                   - 其他应付款
    non_current_liability_in_one_year - 一年内到期的非流动负债
    other_current_liability         - 其他流动负债
    total_current_liability         - 流动负债合计
    hold_for_sale_assets            - 可供出售金融资产
    hold_to_maturity_investments    - 持有至到期投资
    investment_property             - 投资性房地产
    longterm_equity_invest          - 长期股权投资
    longterm_receivable_account     - 长期应收款
    fixed_assets                    - 固定资产
    construction_materials          - 工程物资
    constru_in_process              - 在建工程
    fixed_assets_liquidation        - 固定资产清理
    biological_assets               - 生产性生物资产
    oil_gas_assets                  - 油气资产
    intangible_assets               - 无形资产
    seat_costs                      - 交易席位费
    development_expenditure         - 开发支出
    good_will                       - 商誉
    long_deferred_expense           - 长期待摊费用
    deferred_tax_assets             - 递延所得税资产
    other_non_current_assets        - 其他非流动资产
    total_non_current_assets        - 非流动资产合计
    longterm_loan                   - 长期借款
    bonds_payable                   - 应付债券
    longterm_account_payable        - 长期应付款
    long_salaries_pay               - 长期应付职工薪酬
    specific_account_payable        - 专项应付款
    estimate_liability              - 预计负债
    deferred_tax_liability          - 递延所得税负债
    long_defer_income               - 长期递延收益
    other_non_current_liability     - 其他非流动负债
    total_non_current_liability     - 非流动负债合计
    paidin_capital                  - 实收资本（或股本）
    other_equityinstruments         - 其他权益工具
    capital_reserve_fund            - 资本公积
    surplus_reserve_fund            - 盈余公积
    retained_profit                 - 未分配利润
    treasury_stock                  - 减：库存股
    other_composite_income          - 其他综合收益
    ordinary_risk_reserve_fund      - 一般风险准备
    foreign_currency_report_conv_diff - 外币报表折算差额
    specific_reserves               - 专项储备
    se_without_mi                   - 归属母公司股东权益合计
    minority_interests              - 少数股东权益
    total_shareholder_equity        - 所有者权益合计
    total_liability_and_equity      - 负债和权益总计
    total_assets                    - 资产总计
    total_liability                 - 负债总计
    contract_liability              - 合同负债
    total_fixed_asset               - 固定资产合计
    t_constru_in_process            - 在建工程合计
"""

print("\n" + "=" * 60)
print("💰 获取资产负债表")
print("=" * 60)

result = client.get_stock_finance_data(
    table='资产负债表',
    date='2024-06-30',
    columns='secu_code,secu_abbr,end_date,total_assets,total_liability,total_shareholder_equity'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 9. 获取利润表
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例5：获取利润表（全部字段）
# ============================================================
"""
【利润表 - income_statement 全部字段】
    secu_code                       - 股票代码
    secu_abbr                       - 股票简称
    company_type                    - 公司类型
    end_date                        - 截止日期
    publ_date                       - 公告日期
    basic_eps                       - 基本每股收益
    diluted_eps                     - 稀释每股收益
    net_profit                      - 净利润
    np_parent_company_owners        - 归属于母公司所有者的净利润
    minority_profit                 - 少数股东损益
    total_operating_cost            - 营业总成本
    operating_payout                - 营业支出
    refunded_premiums               - 退保金
    compensation_expense            - 赔付支出
    amortization_expense            - 减:摊回赔付支出
    premium_reserve                 - 提取保险责任准备金
    amortization_premium_reserve    - 减:摊回保险责任准备金
    policy_dividend_payout          - 保单红利支出
    reinsurance_cost                - 分保费用
    amortization_reinsurance_cost   - 减:摊回分保费用
    insurance_commission_expense    - 保险手续费及佣金支出
    other_operating_cost            - 其他营业成本
    operating_cost                  - 营业成本
    operating_tax_surcharges        - 营业税金及附加
    operating_expense               - 销售费用
    administration_expense          - 管理费用
    financial_expense               - 财务费用
    asset_impairment_loss           - 资产减值损失
    operating_profit                - 营业利润
    non_operating_income            - 加：营业收入
    non_operating_expense           - 减：营业外支出
    non_current_assetss_deal_loss   - 其中：非流动资产处置净损失
    total_operating_revenue         - 营业总收入
    operating_revenue               - 营业收入
    net_interest_income             - 利息净收入
    interest_income                 - 其中：利息收入
    interest_expense                - 其中:利息支出
    net_commission_income           - 手续费及佣金净收入
    commission_income               - 其中：手续费及佣金收入
    commission_expense              - 其中：手续费及佣金支出
    net_proxy_secu_income           - 其中：代理买卖证券业务净收入
    net_subissue_secu_income        - 其中：证券承销业务净收入
    net_trust_income                - 其中:受托客户资产管理业务净收入
    premiums_earned                 - 已赚保费
    premiums_income                 - 保险业务收入
    reinsurance_income              - 其中：分保费收入
    reinsurance                     - 减：分出保费
    unearned_premium_reserve        - 提取未到期责任准备金
    other_operating_revenue         - 其他营业收入
    other_net_revenue               - 非营业性收入
    fair_value_change_income        - 公允价值变动净收益
    invest_income                   - 投资净收益
    invest_income_associates        - 其中:对联营合营企业的投资收益
    exchange_income                 - 汇兑收益
    total_profit                    - 利润总额
    income_tax_cost                 - 减：所得税费用
    total_composite_income          - 综合收益总额
    ci_parent_company_owners        - 归属于母公司所有者的综合收益总额
    ci_minority_owners              - 归属于少数股东的综合收益总额
    r_and_d                         - 研发费用
"""

print("\n" + "=" * 60)
print("💰 获取利润表")
print("=" * 60)

result = client.get_stock_finance_data(
    table='利润表',
    date='2024-06-30',
    columns='secu_code,secu_abbr,total_operating_revenue,operating_cost,net_profit,basic_eps'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 10. 现金流量表
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例6：获取现金流量表（全部字段）
# ============================================================
"""
【现金流量表 - cashflow_statement 全部字段】
    secu_code                       - 股票代码
    secu_abbr                       - 股票简称
    company_type                    - 公司类型
    end_date                        - 截止日期
    publ_date                       - 公告日期
    goods_sale_service_render_cash  - 销售商品、提供劳务收到的现金
    tax_levy_refund                 - 收到的税费返还
    net_deposit_increase            - 客户存款和同业存放款项净增加额
    net_borrowing_from_central_bank - 向中央银行借款净增加额
    net_borrowing_from_finance_co   - 向其他金融机构拆入资金净增加额
    interest_and_commission_cashin  - 收取利息、手续费及佣金的现金
    net_deal_trading_assets         - 处置交易性金融资产净增加额
    net_buyback                     - 回购业务资金净增加额
    net_original_insurance_cash     - 收到原保险合同保费取得的现金
    net_reinsurance_cash            - 收到再保业务现金净额
    net_insurer_deposit_investment  - 保户储金及投资款净增加额
    other_cashin_related_operate    - 收到其他与经营活动有关的现金
    subtotal_operate_cash_inflow    - 经营活动现金流入小计
    goods_and_services_cash_paid    - 购买商品、接受劳务支付的现金
    staff_behalf_paid               - 支付给职工以及为职工支付的现金
    all_taxes_paid                  - 支付的各项税费
    net_loan_and_advance_increase   - 客户贷款及垫款净增加额
    net_deposit_in_cb_and_ib        - 存放中央银行和同业款项净增加额
    net_lend_capital                - 拆出资金净增加额
    commission_cash_paid            - 支付手续费及佣金的现金
    original_compensation_paid      - 支付原保险合同赔付款项的现金
    net_cash_for_reinsurance        - 支付再保业务现金净额
    policy_dividend_cash_paid       - 支付保单红利的现金
    other_operate_cash_paid         - 支付其他与经营活动有关的现金
    subtotal_operate_cash_outflow   - 经营活动现金流出小计
    net_operate_cash_flow           - 经营活动产生的现金流量净额
    invest_withdrawal_cash          - 收回投资收到的现金
    invest_proceeds                 - 取得投资收益收到的现金
    fix_intan_other_asset_dispo_cash - 处置固定资产、无形资产和其他长期资产收回的现金净额
    net_cash_deal_sub_company       - 处置子公司及其他营业单位收到的现金净额
    other_cash_from_invest_act      - 收到其他与投资活动有关的现金
    subtotal_invest_cash_inflow     - 投资活动现金流入小计
    fix_intan_other_asset_acqui_cash - 购建固定资产、无形资产和其他长期资产支付的现金
    invest_cash_paid                - 投资支付的现金
    net_cash_from_sub_company       - 取得子公司及其他营业单位支付的现金净额
    impawned_loan_net_increase      - 质押贷款净增加额
    other_cash_to_invest_act        - 支付其他与投资活动有关的现金
    subtotal_invest_cash_outflow    - 投资活动现金流出小计
    net_invest_cash_flow            - 投资活动产生的现金流量净额
    cash_from_invest                - 吸收投资收到的现金
    cash_from_bonds_issue           - 发行债券收到的现金
    cash_from_borrowing             - 取得借款收到的现金
    other_finance_act_cash          - 收到其他与筹资活动有关的现金
    subtotal_finance_cash_inflow    - 筹资活动现金流入小计
    borrowing_repayment             - 偿还债务支付的现金
    dividend_interest_payment       - 分配股利、利润或偿付利息支付的现金
    other_finance_act_payment       - 支付其他与筹资活动有关的现金
    subtotal_finance_cash_outflow   - 筹资活动现金流出小计
    net_finance_cash_flow           - 筹资活动产生的现金流量净额
    exchan_rate_change_effect       - 汇率变动对现金及现金等价物的影响
    cash_equivalent_increase        - 现金及现金等价物净增加额
    begin_period_cash               - 加：期初现金及现金等价物余额
    end_period_cash_equivalent      - 期末现金及现金等价物余额
    net_profit                      - 净利润
    minority_profit                 - 加:少数股东损益
    assets_depreciation_reserves    - 加:资产减值准备
    fixed_asset_depreciation        - 固定资产折旧
    intangible_asset_amortization   - 收无形资产摊销
    deferred_expense_amort          - 长期待摊费用摊销
    deferred_expense_decreased      - 待摊费用减少(减:增加)
    accrued_expense_added           - 预提费用增加(减:减少)
    fix_intanther_asset_dispo_loss  - 处置固定资产、无形资产和其他长期资产的损失
    fixed_asset_scrap_loss          - 固定资产报废损失
    loss_from_fair_value_changes    - 公允价值变动损失
    financial_expense               - 财务费用
    invest_loss                     - 投资损失
    defered_tax_asset_decrease      - 递延所得税资产减少
    defered_tax_liability_increase  - 递延所得税负债增加
    inventory_decrease              - 存货的减少
    operate_receivable_decrease     - 经营性应收项目的减少
    operate_payable_increase        - 经营性应付项目的增加
    others                          - 其他
    net_operate_cash_flow_notes     - 经营活动产生的现金流量净额
    debt_to_captical                - 债务转为资本
    cbs_expiring_within_one_year    - 一年内到期的可转换公司债券
    fixed_assets_finance_leases     - 融资租入固定资产
    cash_at_end_of_year             - 现金的期末余额
    cash_at_beginning_of_year       - 减:现金的期初余额
    cash_equivalents_at_end_of_year - 加:现金等价物的期末余额
    cash_equivalents_at_beginning   - 减:现金等价物的期初余额
    net_incr_in_cash_and_equivalents - 现金及现金等价物净增加额
"""

print("\n" + "=" * 60)
print("💰 获取现金流量表")
print("=" * 60)

result = client.get_stock_finance_data(
    table='现金流量表',
    date='2024-06-30',
    columns='secu_code,secu_abbr,net_operate_cash_flow,net_invest_cash_flow,net_finance_cash_flow'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 11. 获取估值数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例7：获取估值数据（全部字段）
# ============================================================
"""
【估值数据 - valuation 全部字段】
    trading_day                     - 交易日期（固定返回）
    total_value                     - A股总市值(元)（固定返回）
    float_value                     - A股流通市值(元)（自选返回）
    naps                            - 每股净资产/(元/股)（自选返回）
    pcf                             - 市现率（自选返回）
    secu_abbr                       - 证券简称（自选返回）
    secu_code                       - 证券代码（固定返回）
    ps                              - 市销率PS（自选返回）
    ps_ttm                          - 市销率PS(TTM)（自选返回）
    pe_ttm                          - 市盈率PE(TTM)（自选返回）
    a_shares                        - A股股本（自选返回）
    a_floats                        - 可流通A股（自选返回）
    pe_dynamic                      - 动态市盈率（自选返回）
    pe_static                       - 静态市盈率（自选返回）
    b_floats                        - 可流通B股（自选返回）
    b_shares                        - B股股本（自选返回）
    h_shares                        - H股股本（自选返回）
    total_shares                    - 总股本（自选返回）
    turnover_rate                   - 换手率（自选返回）
    dividend_ratio                  - 滚动股息率（自选返回）
    pb                              - 市净率（自选返回）
    roe                             - 净资产收益率（自选返回）
"""

print("\n" + "=" * 60)
print("💰 获取估值数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='估值数据',
    date='2024-06-30',
    columns='secu_code,secu_abbr,pe_ttm,pb,total_value,roe,turnover_rate'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 12. 获取成长能力数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例8：获取成长能力数据（全部字段）
# ============================================================
"""
【成长能力 - growth_ability 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    basic_eps_yoy                   - 基本每股收益同比增长（%）
    diluted_eps_yoy                 - 稀释每股收益同比增长（%）
    operating_revenue_grow_rate     - 营业收入同比增长（%）
    np_parent_company_yoy           - 归属母公司股东的净利润同比增长（%）
    net_operate_cash_flow_yoy       - 经营活动产生的现金流量净额同比增长（%）
    oper_profit_grow_rate           - 营业利润同比增长（%）
    total_profit_grow_rate          - 利润总额同比增长（%）
    eps_grow_rate_ytd               - 每股净资产相对年初增长率（%）
    se_without_mi_grow_rate_ytd     - 归属母公司股东的权益相对年初增长率（%）
    ta_grow_rate_ytd                - 资产总计相对年初增长率（%)
    np_parent_company_cut_yoy       - 归属母公司股东的净利润(扣除)同比增长（%）
    avg_np_yoy_past_five_year       - 过去五年同期归属母公司净利润平均增幅（%）
    oper_cash_ps_grow_rate          - 每股经营活动产生的现金流量净额同比增长（%）
    naor_yoy                        - 净资产收益率(摊薄)同比增（%）
    net_asset_grow_rate             - 净资产同比增长（%）
    total_asset_grow_rate           - 总资产同比增长（%）
    sustainable_grow_rate           - 可持续增长率（%）
    net_profit_grow_rate            - 净利润同比增长（%）
"""

print("\n" + "=" * 60)
print("📈 获取成长能力数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='成长能力',
    date='2024-06-30',
    columns='secu_code,secu_abbr,operating_revenue_grow_rate,np_parent_company_yoy,oper_profit_grow_rate'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 13. 盈利能力
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例9：获取盈利能力数据（全部字段）
# ============================================================
"""
【盈利能力 - profit_ability 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    roe_avg                         - 净资产收益率%平均计算值（%）
    roe_weighted                    - 净资产收益率%加权公布值（%）
    roe                             - 净资产收益率%摊薄公布值（%）
    roe_cut                         - 净资产收益率%扣除摊薄（%）
    roe_cut_weighted                - 净资产收益率%扣除加权（%）
    roe_ttm                         - 净资产收益率_TTM（%）
    roa_ebit                        - 总资产报酬率（%）
    roa_ebit_ttm                    - 总资产报酬率_TTM（%）
    roa                             - 总资产净利率（%）
    roa_ttm                         - 总资产净利率_TTM（%）
    roic                            - 投入资本回报率（%）
    net_profit_ratio                - 销售净利率（%）
    net_profit_ratio_ttm            - 销售净利率_TTM（%）
    gross_income_ratio              - 销售毛利率（%）
    gross_income_ratio_ttm          - 销售毛利率_TTM（%）
    sales_cost_ratio                - 销售成本率（%）
    period_costs_rate               - 销售期间费用率（%）
    period_costs_rate_ttm           - 销售期间的费用率_TTM（%）
    np_to_tor                       - 净利润／营业总收入（%）
    np_to_tor_ttm                   - 净利润／营业总收入_TTM（%）
    operating_profit_to_tor         - 营业利润／营业总收入（%）
    operating_profit_to_tor_ttm     - 营业利润／营业总收入_TTM（%）
    ebit_to_tor                     - 息税前利润／营业总收入（%）
    ebit_to_tor_ttm                 - 息税前利润／营业总收入_TTM（%）
    t_operating_cost_to_tor         - 营业总成本／营业总收入（%）
    t_operating_cost_to_tor_ttm     - 营业总成本／营业总收入_TTM（%）
    operating_expense_rate          - 销售费用／营业总收入（%）
    operating_expense_rate_ttm      - 销售费用／营业总收入_TTM（%）
    admini_expense_rate             - 管理费用／营业总收入（%）
    admini_expense_rate_ttm         - 管理费用／营业总收入_TTM（%）
    financial_expense_rate          - 财务费用／营业总收入（%）
    financial_expense_rate_ttm      - 财务费用／营业总收入_TTM（%）
    asset_impa_loss_to_tor          - 资产减值损失／营业总收入（%）
    asset_impa_loss_to_tor_ttm      - 资产减值损失／营业总收入_TTM（%）
    net_profit                      - 归属母公司净利润（元）
    net_profit_cut                  - 扣除非经常性损益后的净利润（元）
    ebit                            - 息税前利润（元）
    ebitda                          - 息税折旧摊销前利润（元）
    operating_profit_ratio          - 营业利润率（%）
    total_profit_cost_ratio         - 成本费用利润率
"""

print("\n" + "=" * 60)
print("📈 获取盈利能力数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='盈利能力',
    date='2024-06-30',
    columns='secu_code,secu_abbr,roe,gross_income_ratio,net_profit_ratio'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 14. 每股指标
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例10：获取每股指标数据（全部字段）
# ============================================================
"""
【每股指标 - eps 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    basic_eps                       - 基本每股收益（元/股）
    diluted_eps                     - 稀释每股收益（元/股）
    eps                             - 每股收益_期末股本摊薄（元/股）
    eps_ttm                         - 每股收益_TTM（元/股）
    naps                            - 每股净资产（元/股）
    total_operating_revenue_ps      - 每股营业总收入（元/股）
    main_income_ps                  - 每股营业收入（元/股）
    operating_revenue_ps_ttm        - 每股营业收入_TTM（元/股）
    oper_profit_ps                  - 每股营业利润（元/股）
    ebitps                          - 每股息税前利润（元/股）
    capital_surplus_fund_ps         - 每股资本公积金（元/股）
    surplus_reserve_fund_ps         - 每股盈余公积（元/股）
    accumulation_fund_ps            - 每股公积金（元/股）
    undivided_profit                - 每股未分配利润（元/股）
    retained_earnings_ps            - 每股留存收益（元/股）
    net_operate_cash_flow_ps        - 每股经营活动产生的现金流量净额（元/股）
    net_operate_cash_flow_ps_ttm    - 每股经营活动产生的现金流量净额_TTM（元/股）
    cash_flow_ps                    - 每股现金流量净额（元/股）
    cash_flow_ps_ttm                - 每股现金流量净额_TTM（元/股）
    enterprise_fcf_ps               - 每股企业自由现金流量（元/股）
    shareholder_fcf_ps              - 每股股东自由现金流量（元/股）
"""

print("\n" + "=" * 60)
print("📈 获取每股指标数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='每股指标',
    date='2024-06-30',
    columns='secu_code,secu_abbr,basic_eps,diluted_eps,naps'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 15. 获取营运能力数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例11：获取营运能力数据（全部字段）
# ============================================================
"""
【营运能力 - operating_ability 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    oper_cycle                      - 营业周期（天/次）
    inventory_turnover_rate         - 存货周转率（次）
    inventory_turnover_days         - 存货周转天数（天/次）
    accounts_receivables_turnover_rate - 应收账款周转率（次）
    accounts_receivables_turnover_days - 应收账款周转天数（天/次）
    accounts_payables_turnover_rate - 应付账款周转率（次）
    accounts_payables_turnover_days - 应付账款周转天数（天/次）
    current_assets_turnover_rate    - 流动资产周转率（次）
    fixed_asset_turnover_rate       - 固定资产周转率（次）
    equity_turnover_rate            - 股东权益周转率（次）
    total_asset_turnover_rate       - 总资产周转率（次）
"""

print("\n" + "=" * 60)
print("📈 获取营运能力数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='营运能力',
    date='2024-06-30',
    columns='secu_code,secu_abbr,inventory_turnover_rate,accounts_receivables_turnover_rate,total_asset_turnover_rate'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 16. 获取偿债能力数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例12：获取偿债能力数据（全部字段）
# ============================================================
"""
【偿债能力 - debt_paying_ability 全部字段】
    secu_code                       - 股票代码（固定返回）
    secu_abbr                       - 股票简称（固定返回）
    publ_date                       - 公告日期（固定返回）
    end_date                        - 截止日期（固定返回）
    current_ratio                   - 流动比率
    quick_ratio                     - 速动比率
    super_quick_ratio               - 超速动比率
    debt_equity_ratio               - 产权比率（%）
    sewmi_to_total_liability        - 归属母公司股东的权益／负债合计（%）
    sewmi_to_interest_bear_debt     - 归属母公司股东的权益／带息债务（%）
    debt_tangible_equity_ratio      - 有形净值债务率（%）
    tangible_a_to_interest_bear_debt - 有形净值／带息债务（%）
    tangible_a_to_net_debt          - 有形净值／净债务（%）
    ebitda_to_t_liability           - 息税折旧摊销前利润／负债合计
    nocf_to_t_liability             - 经营活动产生现金流量净额/负债合计
    nocf_to_interest_bear_debt      - 经营活动产生现金流量净额/带息债务
    nocf_to_current_liability       - 经营活动产生现金流量净额/流动负债
    nocf_to_net_debt                - 经营活动产生现金流量净额/净债务
    interest_cover                  - 利息保障倍数（倍）
    long_debt_to_working_capital    - 长期负债与营运资金比率
    opercashinto_current_debt       - 现金流动负债比
"""

print("\n" + "=" * 60)
print("📈 获取偿债能力数据")
print("=" * 60)

result = client.get_stock_finance_data(
    table='偿债能力',
    date='2024-06-30',
    columns='secu_code,secu_abbr,current_ratio,quick_ratio,debt_equity_ratio'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 17. 读取模拟交易统计数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例13：读取模拟交易统计数据
# ============================================================
"""
参数说明：
    st_type: str = '动量策略'        - 策略类型
        可选值：'定投策略'、'动量策略'、'资产配置策略'、
               '资产配置平衡策略'、'网格策略'、'海龟策略'、
               '综合动量策略'、'条件因子策略'、'排序多因子策略'
    st_name: str = '小果动量模拟策略'  - 策略名称
"""

print("\n" + "=" * 60)
print("📊 读取模拟交易统计数据")
print("=" * 60)

result = client.get_moni_trader_data(
    st_type='动量策略',
    st_name='小果动量模拟策略'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
## 18. 读取社区交易统计数据
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例14：读取社区交易统计数据
# ============================================================
"""
参数说明：
    st_type: str = '动量策略'        - 策略类型
        可选值：'定投策略'、'动量策略'、'资产配置策略'、
               '资产配置平衡策略'、'网格策略'、'海龟策略'、
               '综合动量策略'、'条件因子策略'、'排序多因子策略'
    st_name: str = '小果动量模拟策略'  - 策略名称
"""

print("\n" + "=" * 60)
print("📊 读取社区交易统计数据")
print("=" * 60)

result = client.get_moni_trader_data_sq(
    st_type='动量策略',
    st_name='小果动量模拟策略'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条数据")
print(df.head())
```
# 三、回测接口
## 1. 定投回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例15：定投回测
# ============================================================
"""
参数说明：
    start_date: str = '20260701'     - 回测开始日期，格式YYYYMMDD
    end_date: str = '20500101'       - 回测结束日期，格式YYYYMMDD
    stock_list: str = '513100.SH,513500.SH'  - 股票列表，逗号分隔
    index_stock: str = '000300.SH'   - 基准指数代码
    cash: float = 100000             - 初始资金
    dt_interval: int = 20            - 定投间隔（交易日）
    dt_type: str = '金额'            - 定投类型：'金额'、'份额'、'百分比'
    dt_value: float = 1000           - 定投金额/份额/百分比值
    sell_zdf: float = 0.03           - 止盈涨幅阈值（如0.03表示3%）
    buy_zdf: float = -0.03           - 补仓跌幅阈值（如-0.03表示-3%）
    trade_value: float = 1000        - 每次交易金额
    comm: float = 0.0001             - 佣金费率（如0.0001表示万分之一）
"""

print("\n" + "=" * 60)
print("📊 定投回测")
print("=" * 60)

result = client.xg_dt_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    dt_interval=20,
    dt_type='金额',
    dt_value=1000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("定投回测结果：")
print(result)
```
## 2. 动量回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例16：动量回测
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    mom_type: str = '百分比'         - 动量类型：'百分比'或'金额'
    mom_value: float = 1             - 动量值（百分比或金额）
    mom_daily: int = 25              - 动量计算周期（交易日）
    min_mom: float = 0               - 最小动量阈值，低于此值不买入
    max_mom: float = 5               - 最大动量阈值，高于此值不买入
    buy_rank: int = 1                - 买入排名，1表示买排名第1的股票
    sell_zdf: float = 0.03           - 止盈涨幅
    sell_amount: float = 1000        - 卖出金额
"""

print("\n" + "=" * 60)
print("📊 动量回测")
print("=" * 60)

result = client.xg_mom_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    mom_type='百分比',
    mom_value=1,
    mom_daily=25,
    min_mom=0,
    max_mom=5,
    buy_rank=1,
    sell_zdf=0.03,
    sell_amount=1000
)
print("动量回测结果：")
print(result)
```
## 3. 资产配置回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例17：资产配置回测
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    dt_type: str = '百分比'          - 配置类型：'百分比'、'金额'
    weight_list: str = '0.4,0.4,0.2' - 权重配置，与股票列表一一对应
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    sell_zdf: float = 0.03           - 止盈涨幅
    buy_zdf: float = -0.03           - 补仓跌幅
    trade_value: float = 1000        - 交易金额
    comm: float = 0.0001             - 佣金费率
"""

print("\n" + "=" * 60)
print("📊 资产配置回测")
print("=" * 60)

result = client.xg_pz_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    dt_type='百分比',
    weight_list='0.4,0.4,0.2',
    index_stock='000300.SH',
    cash=100000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("资产配置回测结果：")
print(result)
```
## 4. 资产配置平衡回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例18：资产配置平衡回测
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    dt_type: str = '百分比'          - 配置类型
    weight_list: str = '0.35,0.35,0.3'  - 目标权重
    deviation_list: str = '0.1,0.1,0.05'  - 偏离容忍度，与股票一一对应
    interval: int = 20               - 再平衡间隔（交易日）
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    sell_zdf: float = 0.03           - 止盈涨幅
    buy_zdf: float = -0.03           - 补仓跌幅
    trade_value: float = 1000        - 交易金额
    comm: float = 0.0001             - 佣金费率
"""

print("\n" + "=" * 60)
print("📊 资产配置平衡回测")
print("=" * 60)

result = client.xg_zcph_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    dt_type='百分比',
    weight_list='0.35,0.35,0.3',
    deviation_list='0.1,0.1,0.05',
    interval=20,
    index_stock='000300.SH',
    cash=100000,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("资产配置平衡回测结果：")
print(result)
```
## 5. 网格策略回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例19：网格策略回测
# ============================================================
"""
参数说明：
    start_date: str = '20250701'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '513100.SH,513500.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    gd_interval: int = 1             - 网格间隔
    gd_bc_type_list: str = '百分比,百分比'  - 网格类型
    gd_buy_bc_list: str = '0.03,0.02'  - 买入阈值
    gd_sell_bc_list: str = '-0.02,-0.015'  - 卖出阈值
    gd_atr_ratio_list: str = '2.0,2.0'  - ATR比例
    gd_type_list: str = '金额,金额'  - 交易类型
    gd_value_list: str = '1000,1500'  - 交易金额
    init_position_ratio_list: str = '0.1,0.15'  - 初始仓位
    sell_zdf: float = 0.03           - 止盈涨幅
    buy_zdf: float = -0.03           - 补仓跌幅
    trade_value: float = 1000        - 交易金额
    comm: float = 0.0001             - 佣金费率
"""

print("\n" + "=" * 60)
print("📊 网格策略回测")
print("=" * 60)

result = client.xg_gd_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    gd_interval=1,
    gd_bc_type_list='百分比,百分比',
    gd_buy_bc_list='0.03,0.02',
    gd_sell_bc_list='-0.02,-0.015',
    gd_atr_ratio_list='2.0,2.0',
    gd_type_list='金额,金额',
    gd_value_list='1000,1500',
    init_position_ratio_list='0.1,0.15',
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000,
    comm=0.0001
)
print("网格策略回测结果：")
print(result)
```
## 6. 海龟策略回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例20：海龟策略回测
# ============================================================
"""
参数说明：
    start_date: str = '20240101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '513100.SH,513500.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    max_workers: int = 4             - 最大进程数
    entry_period: int = 20           - 入场周期
    exit_period: int = 10            - 离场周期
    n_period: int = 20               - N值计算周期
    risk_per_trade: float = 0.01     - 单笔风险
    risk_per_unit: float = 0.02      - 单位风险
    max_units: int = 4               - 最大单位
    add_unit_threshold: float = 0.5  - 加仓阈值
    sell_zdf: float = 0.03           - 止盈涨幅
    buy_zdf: float = -0.03           - 补仓跌幅
    trade_value: float = 1000        - 交易金额
"""

print("\n" + "=" * 60)
print("📊 海龟策略回测")
print("=" * 60)

result = client.xg_hg_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='513100.SH,513500.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    entry_period=20,
    exit_period=10,
    n_period=20,
    risk_per_trade=0.01,
    risk_per_unit=0.02,
    max_units=4,
    add_unit_threshold=0.5,
    sell_zdf=0.03,
    buy_zdf=-0.03,
    trade_value=1000
)
print("海龟策略回测结果：")
print(result)
```
## 7. 综合动量回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例21：综合动量回测
# ============================================================
"""
参数说明：
    start_date: str = '20250101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    max_workers: int = 4             - 最大进程数
    enable_index_timing: bool = False  - 启用指数择时
    index_mean_line: int = 20        - 指数均线周期
    index_not_trader: str = '513100.SH,518880.SH'  - 不参与择时的标的
    index_condition_type: str = '大于均线'  - 指数条件类型
    index_offset: float = 0.0        - 指数偏移
    mom_type: str = '百分比'         - 动量类型
    mom_value: float = 0.1           - 动量值
    mom_models: str = '动量1'        - 动量模型
    mom_daily: int = 25              - 动量计算天数
    period: int = 20                 - 周期
    short_ma: int = 3                - 短期均线
    long_ma: int = 20                - 长期均线
    enable_mom_filter: bool = False  - 启用动量过滤
    max_value: float = 5             - 最大值
    mini_value: float = 0            - 最小值
    max_rank: int = 1                - 最大排名
    min_rank: int = 2                - 最小排名
    enable_buy_condition: bool = False  - 启用买入条件
    enable_sell_condition: bool = False  - 启用卖出条件
    buy_condition_type: str = '涨幅'  - 买入条件类型
    buy_period: int = 20             - 买入周期
    buy_period_ratio: float = 0.1    - 买入周期比例
    buy_offset: float = 0.0          - 买入偏移
    sell_condition_type: str = '跌幅'  - 卖出条件类型
    sell_period: int = 20            - 卖出周期
    sell_period_ratio: float = -0.1  - 卖出周期比例
    sell_offset: float = 0.0         - 卖出偏移
    sell_zdf: float = 0.03           - 止盈涨幅
    sell_amount: float = 1000        - 卖出金额
    interval: int = 1                - 间隔
"""

print("\n" + "=" * 60)
print("📊 综合动量回测")
print("=" * 60)

result = client.xg_more_mom_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    enable_index_timing=False,
    index_mean_line=20,
    index_not_trader='513100.SH,518880.SH',
    index_condition_type='大于均线',
    index_offset=0.0,
    mom_type='百分比',
    mom_value=0.1,
    mom_models='动量1',
    mom_daily=25,
    period=20,
    short_ma=3,
    long_ma=20,
    enable_mom_filter=False,
    max_value=5,
    mini_value=0,
    max_rank=1,
    min_rank=2,
    enable_buy_condition=False,
    enable_sell_condition=False,
    buy_condition_type='涨幅',
    buy_period=20,
    buy_period_ratio=0.1,
    buy_offset=0.0,
    sell_condition_type='跌幅',
    sell_period=20,
    sell_period_ratio=-0.1,
    sell_offset=0.0,
    sell_zdf=0.03,
    sell_amount=1000,
    interval=1
)
print("综合动量回测结果：")
print(result)
```
## 8. 条件因子回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例22：条件因子回测
# ============================================================
"""
参数说明：
    start_date: str = '20250101'     - 回测开始日期
    end_date: str = '20261201'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    min_commission: float = 0        - 最低佣金
    trader_type: str = '百分比'      - 交易类型
    trader_value: float = 0.5        - 交易值
    hold_stock_limit: int = 2        - 持股上限
    is_open_user_factor: bool = True - 启用自定义因子
    user_factor_list: str = 'close,high,low,open,amount,volume,zdf'  - 因子列表
    user_factor_cacal: str = '{"因子名": "计算公式"}'  - 因子计算
    buy_condi_factor: str = '{"因子名": {"选择类型": "and", "选择方向": "大于", "值": 0}}'  - 买入条件
    rank_factor: str = '{"因子名": "降序"}'  - 排序因子
    sell_condi_factor: str = '{"因子名": {"选择类型": "or", "选择方向": "等于", "值": false}}'  - 卖出条件
    sell_type: str = '金额'          - 卖出类型
    sell_zdf: float = 0.03           - 止盈涨幅
    sell_value: float = 1000         - 卖出金额
    max_workers: int = 4             - 最大进程数
    interval: int = 1                - 间隔
    min_hold_days: int = 1           - 最少持有天数
    risk_free_rate: float = 0.02     - 无风险利率
    slippage: float = 0              - 滑点
    enable_limit_up_down_filter: bool = True  - 启用涨跌停过滤
    max_single_position_ratio: float = 1.0  - 最大单仓位比例
"""

print("\n" + "=" * 60)
print("📊 条件因子回测")
print("=" * 60)

result = client.xg_condi_factor_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    min_commission=0,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"收盘价大于5日均线": "IF(df[\'close\']>MA(df[\'close\'],5),True,False)", "均线评分": "IF(MA(df[\'close\'],3)>MA(df[\'close\'],5),25,0)+IF(MA(df[\'close\'],5)>MA(df[\'close\'],10),25,0)+IF(MA(df[\'close\'],10)>MA(df[\'close\'],20),25,0)+IF(MA(df[\'close\'],20)>MA(df[\'close\'],30),25,0)"}',
    buy_condi_factor='{"收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true}, "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}}',
    rank_factor='{"均线评分": "降序"}',
    sell_condi_factor='{"收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false}, "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}}',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    max_workers=4,
    interval=1,
    min_hold_days=1,
    risk_free_rate=0.02,
    slippage=0,
    enable_limit_up_down_filter=True,
    max_single_position_ratio=1.0
)
print("条件因子回测结果：")
print(result)
```
## 9. 排序多因子回测
```python
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例23：排序多因子回测
# ============================================================
"""
参数说明：
    start_date: str = '20250101'     - 回测开始日期
    end_date: str = '20261201'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    min_commission: float = 0        - 最低佣金
    trader_type: str = '百分比'      - 交易类型
    trader_value: float = 0.5        - 交易值
    hold_stock_limit: int = 2        - 持股上限
    is_open_user_factor: bool = True - 启用自定义因子
    user_factor_list: str = 'close,high,low,open,amount,volume,zdf'  - 因子列表
    user_factor_cacal: str = '{"因子名": "计算公式"}'  - 因子计算
    is_open_buy_condi: bool = True   - 启用买入条件
    buy_condi_factor: str = '{"因子名": {"选择类型": "and", "选择方向": "大于", "值": 0}}'  - 买入条件
    rank_factor: str = '{"因子名": {"相关性": "正相关", "权重": 1}}'  - 排序因子
    total_factor_rank: str = '降序'  - 总因子排序
    sell_type: str = '金额'          - 卖出类型
    sell_zdf: float = 0.03           - 止盈涨幅
    sell_value: float = 1000         - 卖出金额
    max_workers: int = 4             - 最大进程数
    interval: int = 1                - 间隔
    min_hold_days: int = 1           - 最少持有天数
    risk_free_rate: float = 0.02     - 无风险利率
    slippage: float = 0              - 滑点
    enable_limit_up_down_filter: bool = True  - 启用涨跌停过滤
    max_single_position_ratio: float = 1.0  - 最大单仓位比例
"""

print("\n" + "=" * 60)
print("📊 排序多因子回测")
print("=" * 60)

result = client.xg_rank_factor_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    min_commission=0,
    trader_type='百分比',
    trader_value=0.5,
    hold_stock_limit=2,
    is_open_user_factor=True,
    user_factor_list='close,high,low,open,amount,volume,zdf',
    user_factor_cacal='{"收盘价大于5日均线": "IF(df[\'close\']>MA(df[\'close\'],5),0,1)", "均线评分": "IF(MA(df[\'close\'],3)>MA(df[\'close\'],5),25,0)+IF(MA(df[\'close\'],5)>MA(df[\'close\'],10),25,0)+IF(MA(df[\'close\'],10)>MA(df[\'close\'],20),25,0)+IF(MA(df[\'close\'],20)>MA(df[\'close\'],30),25,0)"}',
    is_open_buy_condi=True,
    buy_condi_factor='{"25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0}, "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}}',
    rank_factor='{"25日回归动量": {"相关性": "正相关", "权重": 1}}',
    total_factor_rank='降序',
    sell_type='金额',
    sell_zdf=0.03,
    sell_value=1000,
    max_workers=4,
    interval=1,
    min_hold_days=1,
    risk_free_rate=0.02,
    slippage=0,
    enable_limit_up_down_filter=True,
    max_single_position_ratio=1.0
)
print("排序多因子回测结果：")
print(result)
```
## 10均值方差最优资产组合回测
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例42：均值方差最优资产组合回测
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 回测开始日期
    end_date: str = '20500101'       - 回测结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    index_stock: str = '000300.SH'   - 基准指数
    cash: float = 100000             - 初始资金
    comm: float = 0.0001             - 佣金费率
    max_workers: int = 4             - 最大进程数
    lookback_days: int = 60          - 计算协方差矩阵使用的历史数据天数
    max_weight: float = 0.6          - 最大单只权重
    min_weight: float = 0.05         - 最小单只权重
    lambda_risk: float = 2.0         - 风险厌恶系数
    interval: int = 5                - 调仓间隔（交易日）
"""

print("\n" + "=" * 60)
print("📊 均值方差最优资产组合回测")
print("=" * 60)

result = client.xg_mean_var_backtrader(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    index_stock='000300.SH',
    cash=100000,
    comm=0.0001,
    max_workers=4,
    lookback_days=60,
    max_weight=0.6,
    min_weight=0.05,
    lambda_risk=2.0,
    interval=5
)
print("均值方差最优资产组合回测结果：")
print(result)
```


# 六、多标的量化分析接口
## 1相关性矩阵
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例45：计算多标的收益率相关性矩阵
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 开始日期
    end_date: str = '20500101'       - 结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    max_workers: int = 4             - 最大进程数
    method: str = 'pearson'          - 相关性计算方法：pearson/spearman/kendall
    risk_free_rate: float = 0.03     - 无风险利率

返回数据：
    correlation_matrix   - 相关性矩阵
    correlation_matrix_index - 矩阵索引（股票代码列表）
    covariance_matrix    - 协方差矩阵
    stock_list           - 股票列表
    method               - 使用的计算方法
"""

print("\n" + "=" * 60)
print("📊 多标的收益率相关性矩阵")
print("=" * 60)

result = client.xg_stock_cov_correlation(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    max_workers=4,
    method='pearson',
    risk_free_rate=0.03
)
print(result)
```
## 2 协方差矩阵
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例46：计算多标的收益率协方差矩阵
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 开始日期
    end_date: str = '20500101'       - 结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    max_workers: int = 4             - 最大进程数
    method: str = 'pearson'          - 相关性计算方法
    risk_free_rate: float = 0.03     - 无风险利率
    annualized: bool = True          - 是否年化协方差矩阵

返回数据：
    covariance_matrix    - 协方差矩阵
    covariance_matrix_index - 矩阵索引
    standard_deviations  - 标准差（年化）
    stock_list           - 股票列表
    annualized           - 是否年化
"""

print("\n" + "=" * 60)
print("📊 多标的收益率协方差矩阵")
print("=" * 60)

result = client.xg_stock_cov_covariance(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    max_workers=4,
    method='pearson',
    risk_free_rate=0.03,
    annualized=True
)
print(result)
```
## 3投资组合优化
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例47：多标的投资组合优化
# ============================================================
"""
参数说明：
    start_date: str = '20260101'     - 开始日期
    end_date: str = '20500101'       - 结束日期
    stock_list: str = '159915.SZ,513100.SH,518880.SH'  - 股票列表
    max_workers: int = 4             - 最大进程数
    method: str = 'pearson'          - 相关性计算方法
    risk_free_rate: float = 0.03     - 无风险利率
    target_return: float = None      - 目标收益率（年化），可选

返回组合：
    min_variance         - 最小方差组合
    max_sharpe           - 最大夏普比率组合
    risk_parity          - 风险平价组合
    equal_weight         - 等权重组合（基准）
    target_return_portfolio - 目标收益组合（如果指定target_return）

每个组合包含：
    weights              - 各标的权重
    expected_return      - 预期收益率（年化）
    volatility           - 波动率（年化）
    sharpe_ratio         - 夏普比率
"""

print("\n" + "=" * 60)
print("📊 多标的投资组合优化")
print("=" * 60)

# 不指定目标收益率
result = client.xg_stock_cov_portfolio(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    max_workers=4,
    method='pearson',
    risk_free_rate=0.03,
    target_return=None
)
print("投资组合优化结果：")
print(result)

# 指定目标收益率
print("\n" + "-" * 40)
print("指定目标收益率 15%")
result = client.xg_stock_cov_portfolio(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,513100.SH,518880.SH',
    max_workers=4,
    method='pearson',
    risk_free_rate=0.03,
    target_return=0.15
)
print(result)
```
## 4股票组合分析接口
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例48：小果股票分析系统 - 组合收益分析
# ============================================================
"""
参数说明：
    start_date: str = '20240101'     - 开始日期
    end_date: str = '20261231'       - 结束日期
    stock_list: str = '159915.SZ,518880.SH,510300.SH'  - 股票列表
    stock_weight: str = '0.4,0.3,0.3'  - 股票权重（自动归一化）
    index_stock: str = '000300.SH'   - 基准指数
    max_workers: int = 4             - 最大进程数
    risk_free_rate: float = 0.03     - 无风险利率

返回数据结构：
    summary              - 基本摘要信息（日期范围、股票数量等）
    performance_metrics  - 完整绩效指标（50+项）
    annual_performance   - 年度绩效
    rolling_metrics      - 滚动指标（60日窗口）
    period_returns       - 周期收益（日/周/月/年）
    equity_curve         - 权益曲线（每日净值）
    weight_info          - 个股权重信息
    raw_data             - 原始日度数据

绩效指标包括：
    total_return         - 总收益率
    annual_return        - 年化收益率
    annual_std           - 年化波动率
    sharpe_ratio         - 夏普比率
    max_drawdown         - 最大回撤
    max_drawdown_duration - 最大回撤持续天数
    win_rate             - 胜率
    positive_ratio       - 正收益比例
    beta                 - Beta系数
    alpha                - Alpha系数
    information_ratio    - 信息比率
    tracking_error       - 跟踪误差
    calmar_ratio         - 卡玛比率
    sortino_ratio        - 索提诺比率
"""

print("\n" + "=" * 60)
print("📊 小果股票分析系统 - 组合收益分析")
print("=" * 60)

result = client.xg_stock_analysis(
    start_date='20240101',
    end_date='20241231',
    stock_list='159915.SZ,518880.SH,510300.SH',
    stock_weight='0.4,0.3,0.3',
    index_stock='000300.SH',
    max_workers=4,
    risk_free_rate=0.03
)

print("股票组合分析结果：")
print(f"状态: {result.get('status')}")
print(f"消息: {result.get('message')}")

# 提取绩效指标
metrics = result.get('performance_metrics', {})
print(f"\n📈 绩效指标:")
print(f"  总收益率: {metrics.get('total_return', 0)*100:.2f}%")
print(f"  年化收益率: {metrics.get('annual_return', 0)*100:.2f}%")
print(f"  年化波动率: {metrics.get('annual_std', 0)*100:.2f}%")
print(f"  夏普比率: {metrics.get('sharpe_ratio', 0):.4f}")
print(f"  最大回撤: {metrics.get('max_drawdown', 0)*100:.2f}%")
print(f"  胜率: {metrics.get('positive_ratio', 0)*100:.2f}%")
if 'beta' in metrics:
    print(f"  Beta: {metrics.get('beta', 0):.4f}")
if 'alpha' in metrics:
    print(f"  Alpha: {metrics.get('alpha', 0)*100:.2f}%")
```
# 七股票分钟数据
## 获取5分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例57：获取5分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '5'           - 频率（5/15/30/60）
    adjustflag: str = '2'          - 复权类型（1-不复权 2-前复权 3-后复权）
"""

print("\n" + "=" * 60)
print("📊 获取5分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_5(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='5',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条5分钟数据（mini）")
print(df.head())
```
## 2获取5分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例57：获取5分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '5'           - 频率（5/15/30/60）
    adjustflag: str = '2'          - 复权类型（1-不复权 2-前复权 3-后复权）
"""

print("\n" + "=" * 60)
print("📊 获取5分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_5(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='5',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条5分钟数据（mini）")
print(df.head())
```
## 3获取15分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例58：获取15分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '15'          - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取15分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_15(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='15',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条15分钟数据（mini）")
print(df.head()
```
## 4 获取30分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例59：获取30分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '30'          - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取30分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_30(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='30',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条30分钟数据（mini）")
print(df.head())
```
## 5获取60分钟数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例60：获取60分钟数据（mini）
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = '60'          - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取60分钟数据（mini）")
print("=" * 60)

result = client.get_mini_data_60(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='60',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条60分钟数据（mini）")
print(df.head())
```
## 6 获取日线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例61：获取日线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'd'           - 频率（d/w/m）
    adjustflag: str = '2'          - 复权类型（1-不复权 2-前复权 3-后复权）

返回字段：
    date, open, high, low, close, volume, amount
"""

print("\n" + "=" * 60)
print("📊 获取日线数据")
print("=" * 60)

result = client.query_history_k_data_plus_d(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='d',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条日线数据")
print(df.head())
```
## 7 获取周线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例62：获取周线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'w'           - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取周线数据")
print("=" * 60)

result = client.query_history_k_data_plus_w(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='w',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条周线数据")
print(df.head())
```
## 8获取月线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例63：获取月线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.600031'     - 股票代码（mini格式）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'm'           - 频率
    adjustflag: str = '2'          - 复权类型
"""

print("\n" + "=" * 60)
print("📊 获取月线数据")
print("=" * 60)

result = client.query_history_k_data_plus_m(
    stock='sh.600031',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='m',
    adjustflag='2'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条月线数据")
print(df.head())
```
# 八指数K线数据接口
## 1获取指数日线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例64：获取指数日线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.000001'     - 指数代码（sh.000001 上证指数，sz.399001 深证成指）
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'd'           - 频率（d/w/m）
"""

print("\n" + "=" * 60)
print("📊 获取指数日线数据")
print("=" * 60)

result = client.query_history_k_data_plus_index_d(
    stock='sh.000001',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='d'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条指数日线数据")
print(df.head())
```
## 2获取指数周线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例65：获取指数周线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.000001'     - 指数代码
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'w'           - 频率
"""

print("\n" + "=" * 60)
print("📊 获取指数周线数据")
print("=" * 60)

result = client.query_history_k_data_plus_index_w(
    stock='sh.000001',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='w'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条指数周线数据")
print(df.head())
```
## 3获取指数月线数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例66：获取指数月线数据
# ============================================================
"""
参数说明：
    stock: str = 'sh.000001'     - 指数代码
    start_date: str = '2026-04-01' - 开始日期
    end_date: str = '2050-12-31'   - 结束日期
    frequency: str = 'm'           - 频率
"""

print("\n" + "=" * 60)
print("📊 获取指数月线数据")
print("=" * 60)

result = client.query_history_k_data_plus_index_m(
    stock='sh.000001',
    start_date='2026-04-01',
    end_date='2050-12-31',
    frequency='m'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条指数月线数据")
print(df.head())
```
# 九 财务数据
## 1获取盈利能力数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例1：获取盈利能力数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码，格式：sh.600031 或 sz.000001
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【盈利能力 - query_profit_data 返回字段】
    code            - 证券代码
    pubDate         - 公司发布财报的日期
    statDate        - 财报统计的季度的最后一天，如2017-03-31, 2017-06-30
    roeAvg          - 净资产收益率(平均)(%)，归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
    npMargin        - 销售净利率(%)，净利润/营业收入*100%
    gpMargin        - 销售毛利率(%)，毛利/营业收入100%=(营业收入-营业成本)/营业收入100%
    netProfit       - 净利润(元)
    epsTTM          - 每股收益，归属母公司股东的净利润TTM/最新总股本
    MBRevenue       - 主营营业收入(元)
    totalShare      - 总股本
    liqaShare       - 流通股本
"""

print("\n" + "=" * 60)
print("📊 获取盈利能力数据")
print("=" * 60)

result = client.query_profit_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条盈利能力数据")
print(df.head())

# 打印关键指标
if not df.empty:
    print("\n📈 关键盈利能力指标：")
    print(f"  净资产收益率(平均): {df['roeAvg'].iloc[0] if 'roeAvg' in df.columns else 'N/A'}")
    print(f"  销售净利率: {df['npMargin'].iloc[0] if 'npMargin' in df.columns else 'N/A'}")
    print(f"  销售毛利率: {df['gpMargin'].iloc[0] if 'gpMargin' in df.columns else 'N/A'}")
    print(f"  净利润: {df['netProfit'].iloc[0] if 'netProfit' in df.columns else 'N/A'}")
```
## 2获取营运能力数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例2：获取营运能力数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【营运能力 - query_operation_data 返回字段】
    code                - 证券代码
    pubDate             - 公司发布财报的日期
    statDate            - 财报统计的季度的最后一天
    NRTurnRatio         - 应收账款周转率(次)，营业收入/[(期初应收票据及应收账款净额+期末应收票据及应收账款净额)/2]
    NRTurnDays          - 应收账款周转天数(天)，季报天数/应收账款周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
    INVTurnRatio        - 存货周转率(次)，营业成本/[(期初存货净额+期末存货净额)/2]
    INVTurnDays         - 存货周转天数(天)，季报天数/存货周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)
    CATurnRatio         - 流动资产周转率(次)，营业总收入/[(期初流动资产+期末流动资产)/2]
    AssetTurnRatio      - 总资产周转率，营业总收入/[(期初资产总额+期末资产总额)/2]
"""

print("\n" + "=" * 60)
print("📊 获取营运能力数据")
print("=" * 60)

result = client.query_operation_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条营运能力数据")
print(df.head())

if not df.empty:
    print("\n📈 关键营运能力指标：")
    print(f"  应收账款周转率: {df['NRTurnRatio'].iloc[0] if 'NRTurnRatio' in df.columns else 'N/A'}")
    print(f"  存货周转率: {df['INVTurnRatio'].iloc[0] if 'INVTurnRatio' in df.columns else 'N/A'}")
    print(f"  总资产周转率: {df['AssetTurnRatio'].iloc[0] if 'AssetTurnRatio' in df.columns else 'N/A'}")
```
## 3获取成长能力数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例3：获取成长能力数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【成长能力 - query_growth_data 返回字段】
    code                - 证券代码
    pubDate             - 公司发布财报的日期
    statDate            - 财报统计的季度的最后一天
    YOYEquity           - 净资产同比增长率，(本期净资产-上年同期净资产)/上年同期净资产的绝对值*100%
    YOYAsset            - 总资产同比增长率，(本期总资产-上年同期总资产)/上年同期总资产的绝对值*100%
    YOYNI               - 净利润同比增长率，(本期净利润-上年同期净利润)/上年同期净利润的绝对值*100%
    YOYEPSBasic         - 基本每股收益同比增长率，(本期基本每股收益-上年同期基本每股收益)/上年同期基本每股收益的绝对值*100%
    YOYPNI              - 归属母公司股东净利润同比增长率，(本期归属母公司股东净利润-上年同期归属母公司股东净利润)/上年同期归属母公司股东净利润的绝对值*100%
"""

print("\n" + "=" * 60)
print("📊 获取成长能力数据")
print("=" * 60)

result = client.query_growth_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条成长能力数据")
print(df.head())

if not df.empty:
    print("\n📈 关键成长能力指标：")
    print(f"  净资产同比增长率: {df['YOYEquity'].iloc[0] if 'YOYEquity' in df.columns else 'N/A'}")
    print(f"  总资产同比增长率: {df['YOYAsset'].iloc[0] if 'YOYAsset' in df.columns else 'N/A'}")
    print(f"  净利润同比增长率: {df['YOYNI'].iloc[0] if 'YOYNI' in df.columns else 'N/A'}")
    print(f"  归属母公司股东净利润同比增长率: {df['YOYPNI'].iloc[0] if 'YOYPNI' in df.columns else 'N/A'}")
```
## 4 获取偿债能力数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例4：获取偿债能力数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【偿债能力 - query_balance_data 返回字段】
    code                - 证券代码
    pubDate             - 公司发布财报的日期
    statDate            - 财报统计的季度的最后一天
    currentRatio        - 流动比率，流动资产/流动负债
    quickRatio          - 速动比率，(流动资产-存货净额)/流动负债
    cashRatio           - 现金比率，(货币资金+交易性金融资产)/流动负债
    YOYLiability        - 总负债同比增长率，(本期总负债-上年同期总负债)/上年同期中负债的绝对值*100%
    liabilityToAsset    - 资产负债率，负债总额/资产总额
    assetToEquity       - 权益乘数，资产总额/股东权益总额=1/(1-资产负债率)
"""

print("\n" + "=" * 60)
print("📊 获取偿债能力数据")
print("=" * 60)

result = client.query_balance_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条偿债能力数据")
print(df.head())

if not df.empty:
    print("\n📈 关键偿债能力指标：")
    print(f"  流动比率: {df['currentRatio'].iloc[0] if 'currentRatio' in df.columns else 'N/A'}")
    print(f"  速动比率: {df['quickRatio'].iloc[0] if 'quickRatio' in df.columns else 'N/A'}")
    print(f"  资产负债率: {df['liabilityToAsset'].iloc[0] if 'liabilityToAsset' in df.columns else 'N/A'}")
```
## 5获取现金流量数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例5：获取现金流量数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【现金流量 - query_cash_flow_data 返回字段】
    code                - 证券代码
    pubDate             - 公司发布财报的日期
    statDate            - 财报统计的季度的最后一天
    CAToAsset           - 流动资产除以总资产
    NCAToAsset          - 非流动资产除以总资产
    tangibleAssetToAsset - 有形资产除以总资产
    ebitToInterest      - 已获利息倍数，息税前利润/利息费用
    CFOToOR             - 经营活动产生的现金流量净额除以营业收入
    CFOToNP             - 经营性现金净流量除以净利润
    CFOToGr             - 经营性现金净流量除以营业总收入
"""

print("\n" + "=" * 60)
print("📊 获取现金流量数据")
print("=" * 60)

result = client.query_cash_flow_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条现金流量数据")
print(df.head())

if not df.empty:
    print("\n📈 关键现金流量指标：")
    print(f"  已获利息倍数: {df['ebitToInterest'].iloc[0] if 'ebitToInterest' in df.columns else 'N/A'}")
    print(f"  经营性现金净流量/营业收入: {df['CFOToOR'].iloc[0] if 'CFOToOR' in df.columns else 'N/A'}")
```
## 6 获取杜邦指数数据
```
from xg_quant_backtrader_data.xg_quant_backtrader_data import xg_quant_backtrader_data

# 初始化客户端
client = xg_quant_backtrader_data(
    url="服务器地址",
    port=8888,
    user="自己信息",
    password="自己信息",
    auth_code="自己信息"
)

# ============================================================
# 完整示例6：获取杜邦指数数据
# ============================================================
"""
参数说明：
    code: str = 'sh.600031'      - 股票代码
    year: str = '2025'           - 年份
    quarter: str = '1'           - 季度（1/2/3/4）

【杜邦指数 - query_dupont_data 返回字段】
    code                    - 证券代码
    pubDate                 - 公司发布财报的日期
    statDate                - 财报统计的季度的最后一天
    dupontROE               - 净资产收益率，归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%
    dupontAssetStoEquity    - 权益乘数，反映企业财务杠杆效应强弱和财务风险，平均总资产/平均归属于母公司的股东权益
    dupontAssetTurn         - 总资产周转率，反映企业资产管理效率的指标，营业总收入/[(期初资产总额+期末资产总额)/2]
    dupontPnitoni           - 归属母公司股东的净利润/净利润，反映母公司控股子公司百分比
    dupontNitogr            - 净利润/营业总收入，反映企业销售获利率
    dupontTaxBurden         - 净利润/利润总额，反映企业税负水平，该比值高则税负较低
    dupontIntburden         - 利润总额/息税前利润，反映企业利息负担，该比值高则税负较低
    dupontEbittogr          - 息税前利润/营业总收入，反映企业经营利润率
"""

print("\n" + "=" * 60)
print("📊 获取杜邦指数数据")
print("=" * 60)

result = client.query_dupont_data(
    code='sh.600031',
    year='2025',
    quarter='1'
)
df = client._to_dataframe(result)
print(f"✅ 获取到 {len(df)} 条杜邦指数数据")
print(df.head())

if not df.empty:
    print("\n📈 关键杜邦指数指标：")
    print(f"  净资产收益率(ROE): {df['dupontROE'].iloc[0] if 'dupontROE' in df.columns else 'N/A'}")
    print(f"  权益乘数: {df['dupontAssetStoEquity'].iloc[0] if 'dupontAssetStoEquity' in df.columns else 'N/A'}")
    print(f"  总资产周转率: {df['dupontAssetTurn'].iloc[0] if 'dupontAssetTurn' in df.columns else 'N/A'}")
    print(f"  销售净利率: {df['dupontNitogr'].iloc[0] if 'dupontNitogr' in df.columns else 'N/A'}")
```
# 十全部代码
```
'''
作者:小果
微信:xg_quant
'''
import requests
import json
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
import urllib.parse
class xg_quant_backtrader_data:
    """
    小果量化回测系统数据api
    小果量化数据 - API对接框架
    """
    
    def __init__(
        self,
        url: str = "服务器地址",
        port: int = 8888,  # 修复：port应该是int类型
        user: str = "自己信息",
        password: str = "自己信息",
        auth_code: str = "自己信息"
    ):
        """
        初始化小果量化数据客户端
        
        Args:
            url: 服务器地址
            port: 服务器端口
            user: 用户名称
            password: 用户密码
            auth_code: 授权码
        """
        self.url = url
        self.port = port
        self.user = user
        self.password = password
        self.auth_code = auth_code
        self.base_url = f"http://{url}:{port}"
        self.session = requests.Session()
        self.timeout = 120
        
        # 设置默认请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'
        })
    
    def _get_params(self, **kwargs) -> Dict[str, Any]:
        """构建请求参数，自动添加用户认证信息"""
        params = {
            'user': self.user,
            'password': self.password,
            'auth_code': self.auth_code,
        }
        params.update(kwargs)
        return params
    
    def _request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        method: str = 'GET',
        timeout: Optional[int] = None,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            endpoint: API端点路径
            params: 请求参数
            method: 请求方法
            timeout: 超时时间
            verbose: 是否打印详细信息
        
        Returns:
            响应数据字典
        """
        if timeout is None:
            timeout = self.timeout
        
        url = f"{self.base_url}{endpoint}"
        
        # 清理参数中的None值
        clean_params = {k: v for k, v in params.items() if v is not None}
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=clean_params, timeout=timeout)
            else:
                response = self.session.post(url, params=clean_params, timeout=timeout)
            
            if verbose:
                print(f"📤 请求URL: {response.url[:100]}...")
                print(f"📤 状态码: {response.status_code}")
            
            response.raise_for_status()
            
            # 尝试解析JSON
            try:
                result = response.json()
                if verbose and result.get('status') == 'failed':
                    print(f"❌ 接口返回失败: {result.get('message', result.get('error', '未知错误'))}")
                    if 'info' in result:
                        print(f"📄 详细信息: {result.get('info')}")
                return result
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"📄 响应内容: {response.text[:500]}")
                return {"status": "failed", "error": "Invalid JSON response", "raw": response.text[:500]}
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            # 尝试获取更多错误信息
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"📄 错误详情: {error_detail}")
                    return {"status": "failed", "error": str(e), "detail": error_detail}
                except:
                    print(f"📄 响应内容: {e.response.text[:500]}")
                    return {"status": "failed", "error": str(e), "raw": e.response.text[:500]}
            return {"status": "failed", "error": str(e)}
    
    def _to_dataframe(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        将API返回的数据转换为DataFrame
        处理NaN和Infinity值
        """
        if data.get('status') == 'failed':
            print(f"⚠️ 数据获取失败: {data.get('message', data.get('error', '未知错误'))}")
            return pd.DataFrame()
        
        if 'data' in data and data['data']:
            df = pd.DataFrame(data['data'])
            # 清理数据：将NaN、Infinity替换为None
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.where(pd.notnull(df), None)
            return df
        
        return pd.DataFrame()
    
    def _to_dataframe_with_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """将API返回的数据转换为包含元信息的DataFrame"""
        if data.get('status') == 'failed':
            return {
                'status': 'failed', 
                'data': pd.DataFrame(), 
                'info': data.get('message', data.get('error', '未知错误'))
            }
        
        df = pd.DataFrame(data.get('data', []))
        # 清理数据
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.where(pd.notnull(df), None)
        
        result = {
            'status': data.get('status', 'success'),
            'data': df,
            'total': data.get('total', len(df)),
            'message': data.get('message', ''),
            'available_columns': data.get('available_columns', []),
            'selected_columns': data.get('selected_columns', []),
        }
        for key in ['stock', 'start_date', 'end_date', 'table', 'report_date']:
            if key in data:
                result[key] = data[key]
        return result

    # ============================================================
    # 一、回测接口（类方法名不带数字，但请求路径带 _1）
    # ============================================================
    
    def xg_dt_backtrader(
        self,
        start_date: str = '20260701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        dt_interval: int = 20,
        dt_type: str = '金额',
        dt_value: float = 1000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """定投回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, dt_interval=dt_interval,
            dt_type=dt_type, dt_value=dt_value, sell_zdf=sell_zdf,
            buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_dt_backtrader_1', params)
    
    def xg_mom_backtrader(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        mom_type: str = '百分比',
        mom_value: float = 1,
        mom_daily: int = 25,
        min_mom: float = 0,
        max_mom: float = 5,
        buy_rank: int = 1,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000
    ) -> Dict[str, Any]:
        """动量回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            mom_type=mom_type, mom_value=mom_value, mom_daily=mom_daily,
            min_mom=min_mom, max_mom=max_mom, buy_rank=buy_rank,
            sell_zdf=sell_zdf, sell_amount=sell_amount
        )
        return self._request('/xg_mom_backtrader_1', params)
    
    def xg_pz_backtrader(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.4,0.4,0.2',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, index_stock=index_stock,
            cash=cash, sell_zdf=sell_zdf, buy_zdf=buy_zdf,
            trade_value=trade_value, comm=comm
        )
        return self._request('/xg_pz_backtrader_1', params)
    
    def xg_zcph_backtrader(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.35,0.35,0.3',
        deviation_list: str = '0.1,0.1,0.05',
        interval: int = 20,
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置平衡策略回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, deviation_list=deviation_list,
            interval=interval, index_stock=index_stock, cash=cash,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_zcph_backtrader_1', params)
    
    def xg_gd_backtrader(
        self,
        start_date: str = '20250701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        gd_interval: int = 1,
        gd_bc_type_list: str = '百分比,百分比',
        gd_buy_bc_list: str = '0.03,0.02',
        gd_sell_bc_list: str = '-0.02,-0.015',
        gd_atr_ratio_list: str = '2.0,2.0',
        gd_atr_period_list: str = '14,14',
        gd_type_list: str = '金额,金额',
        gd_value_list: str = '1000,1500',
        init_position_ratio_list: str = '0.1,0.15',
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001,
        max_workers: int = 4
    ) -> Dict[str, Any]:
        """网格策略回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, gd_interval=gd_interval,
            gd_bc_type_list=gd_bc_type_list, gd_buy_bc_list=gd_buy_bc_list,
            gd_sell_bc_list=gd_sell_bc_list, gd_atr_ratio_list=gd_atr_ratio_list,
            gd_atr_period_list=gd_atr_period_list, gd_type_list=gd_type_list,
            gd_value_list=gd_value_list, init_position_ratio_list=init_position_ratio_list,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value,
            comm=comm, max_workers=max_workers
        )
        return self._request('/xg_gd_backtrader_1', params)
    
    def xg_hg_backtrader(
        self,
        start_date: str = '20240101',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        entry_period: int = 20,
        exit_period: int = 10,
        n_period: int = 20,
        risk_per_trade: float = 0.01,
        risk_per_unit: float = 0.02,
        max_units: int = 4,
        add_unit_threshold: float = 0.5,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000
    ) -> Dict[str, Any]:
        """海龟策略回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, entry_period=entry_period,
            exit_period=exit_period, n_period=n_period,
            risk_per_trade=risk_per_trade, risk_per_unit=risk_per_unit,
            max_units=max_units, add_unit_threshold=add_unit_threshold,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value
        )
        return self._request('/xg_hg_backtrader_1', params)
    
    def xg_more_mom_backtrader(
        self,
        start_date: str = '20250101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        enable_index_timing: bool = False,
        index_mean_line: int = 20,
        index_not_trader: str = '513100.SH,518880.SH',
        index_condition_type: str = '大于均线',
        index_offset: float = 0.0,
        mom_type: str = '百分比',
        mom_value: float = 0.1,
        mom_models: str = '动量1',
        mom_daily: int = 25,
        period: int = 20,
        short_ma: int = 3,
        long_ma: int = 20,
        enable_mom_filter: bool = False,
        max_value: float = 5,
        mini_value: float = 0,
        max_rank: int = 1,
        min_rank: int = 2,
        enable_buy_condition: bool = False,
        enable_sell_condition: bool = False,
        buy_condition_type: str = '涨幅',
        buy_period: int = 20,
        buy_period_ratio: float = 0.1,
        buy_offset: float = 0.0,
        sell_condition_type: str = '跌幅',
        sell_period: int = 20,
        sell_period_ratio: float = -0.1,
        sell_offset: float = 0.0,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000,
        interval: int = 1
    ) -> Dict[str, Any]:
        """综合动量回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, enable_index_timing=enable_index_timing,
            index_mean_line=index_mean_line, index_not_trader=index_not_trader,
            index_condition_type=index_condition_type, index_offset=index_offset,
            mom_type=mom_type, mom_value=mom_value, mom_models=mom_models,
            mom_daily=mom_daily, period=period, short_ma=short_ma,
            long_ma=long_ma, enable_mom_filter=enable_mom_filter,
            max_value=max_value, mini_value=mini_value,
            max_rank=max_rank, min_rank=min_rank,
            enable_buy_condition=enable_buy_condition,
            enable_sell_condition=enable_sell_condition,
            buy_condition_type=buy_condition_type, buy_period=buy_period,
            buy_period_ratio=buy_period_ratio, buy_offset=buy_offset,
            sell_condition_type=sell_condition_type, sell_period=sell_period,
            sell_period_ratio=sell_period_ratio, sell_offset=sell_offset,
            sell_zdf=sell_zdf, sell_amount=sell_amount, interval=interval
        )
        return self._request('/xg_more_mom_backtrader_1', params)
    
    def xg_condi_factor_backtrader(
        self,
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),True,False)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        buy_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true},
            "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}
        }''',
        rank_factor: str = '''{
            "均线评分": "降序"
        }''',
        sell_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false},
            "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}
        }''',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """条件因子回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            sell_condi_factor=sell_condi_factor,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_condi_factor_backtrader_1', params)
    
    def xg_rank_factor_backtrader(
        self,
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),0,1)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        is_open_buy_condi: bool = True,
        buy_condi_factor: str = '''{
            "25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0},
            "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}
        }''',
        rank_factor: str = '''{
            "25日回归动量": {"相关性": "正相关", "权重": 1}
        }''',
        total_factor_rank: str = '降序',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """排序多因子回测接口"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            is_open_buy_condi=is_open_buy_condi,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            total_factor_rank=total_factor_rank,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_rank_factor_backtrader_1', params)

    # ============================================================
    # 二、策略模拟交易接口（moni，不带 _1）
    # ============================================================
    
    def xg_dt_backtrader_moni(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        dt_interval: int = 20,
        dt_type: str = '金额',
        dt_value: float = 1000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """定投策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, dt_interval=dt_interval,
            dt_type=dt_type, dt_value=dt_value, sell_zdf=sell_zdf,
            buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_dt_backtrader_moni', params)
    
    def xg_mom_backtrader_moni(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        mom_type: str = '百分比',
        mom_value: float = 1,
        mom_daily: int = 25,
        min_mom: float = 0,
        max_mom: float = 5,
        buy_rank: int = 1,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000
    ) -> Dict[str, Any]:
        """动量策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            mom_type=mom_type, mom_value=mom_value, mom_daily=mom_daily,
            min_mom=min_mom, max_mom=max_mom, buy_rank=buy_rank,
            sell_zdf=sell_zdf, sell_amount=sell_amount
        )
        return self._request('/xg_mom_backtrader_moni', params)
    
    def xg_pz_backtrader_moni(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.4,0.4,0.2',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, index_stock=index_stock,
            cash=cash, sell_zdf=sell_zdf, buy_zdf=buy_zdf,
            trade_value=trade_value, comm=comm
        )
        return self._request('/xg_pz_backtrader_moni', params)
    
    def xg_zcph_backtrader_moni(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.35,0.35,0.3',
        deviation_list: str = '0.1,0.1,0.05',
        interval: int = 20,
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置平衡策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, deviation_list=deviation_list,
            interval=interval, index_stock=index_stock, cash=cash,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_zcph_backtrader_moni', params)
    
    def xg_gd_backtrader_moni(
        self,
        st_name: str = '小果网格测试策略',
        open_show: str = '是',
        start_date: str = '20250701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        gd_interval: int = 1,
        gd_bc_type_list: str = '百分比,百分比',
        gd_buy_bc_list: str = '0.03,0.02',
        gd_sell_bc_list: str = '-0.02,-0.015',
        gd_atr_ratio_list: str = '2.0,2.0',
        gd_atr_period_list: str = '14,14',
        gd_type_list: str = '金额,金额',
        gd_value_list: str = '1000,1500',
        init_position_ratio_list: str = '0.1,0.15',
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001,
        max_workers: int = 4
    ) -> Dict[str, Any]:
        """网格策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, gd_interval=gd_interval,
            gd_bc_type_list=gd_bc_type_list, gd_buy_bc_list=gd_buy_bc_list,
            gd_sell_bc_list=gd_sell_bc_list, gd_atr_ratio_list=gd_atr_ratio_list,
            gd_atr_period_list=gd_atr_period_list, gd_type_list=gd_type_list,
            gd_value_list=gd_value_list,
            init_position_ratio_list=init_position_ratio_list,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value,
            comm=comm, max_workers=max_workers
        )
        return self._request('/xg_gd_backtrader_moni', params)
    
    def xg_hg_backtrader_moni(
        self,
        st_name: str = '小果海龟测试策略',
        open_show: str = '是',
        start_date: str = '20240101',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        entry_period: int = 20,
        exit_period: int = 10,
        n_period: int = 20,
        risk_per_trade: float = 0.01,
        risk_per_unit: float = 0.02,
        max_units: int = 4,
        add_unit_threshold: float = 0.5,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000
    ) -> Dict[str, Any]:
        """海龟策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, entry_period=entry_period,
            exit_period=exit_period, n_period=n_period,
            risk_per_trade=risk_per_trade, risk_per_unit=risk_per_unit,
            max_units=max_units, add_unit_threshold=add_unit_threshold,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value
        )
        return self._request('/xg_hg_backtrader_moni', params)
    
    def xg_more_mom_backtrader_moni(
        self,
        st_name: str = '小果综合动量测试策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        enable_index_timing: bool = False,
        index_mean_line: int = 20,
        index_not_trader: str = '513100.SH,518880.SH',
        index_condition_type: str = '大于均线',
        index_offset: float = 0.0,
        mom_type: str = '百分比',
        mom_value: float = 0.1,
        mom_models: str = '动量1',
        mom_daily: int = 25,
        period: int = 20,
        short_ma: int = 3,
        long_ma: int = 20,
        enable_mom_filter: bool = False,
        max_value: float = 5,
        mini_value: float = 0,
        max_rank: int = 1,
        min_rank: int = 2,
        enable_buy_condition: bool = False,
        enable_sell_condition: bool = False,
        buy_condition_type: str = '涨幅',
        buy_period: int = 20,
        buy_period_ratio: float = 0.1,
        buy_offset: float = 0.0,
        sell_condition_type: str = '跌幅',
        sell_period: int = 20,
        sell_period_ratio: float = -0.1,
        sell_offset: float = 0.0,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000,
        interval: int = 1
    ) -> Dict[str, Any]:
        """综合动量策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, enable_index_timing=enable_index_timing,
            index_mean_line=index_mean_line, index_not_trader=index_not_trader,
            index_condition_type=index_condition_type, index_offset=index_offset,
            mom_type=mom_type, mom_value=mom_value, mom_models=mom_models,
            mom_daily=mom_daily, period=period, short_ma=short_ma,
            long_ma=long_ma, enable_mom_filter=enable_mom_filter,
            max_value=max_value, mini_value=mini_value,
            max_rank=max_rank, min_rank=min_rank,
            enable_buy_condition=enable_buy_condition,
            enable_sell_condition=enable_sell_condition,
            buy_condition_type=buy_condition_type, buy_period=buy_period,
            buy_period_ratio=buy_period_ratio, buy_offset=buy_offset,
            sell_condition_type=sell_condition_type, sell_period=sell_period,
            sell_period_ratio=sell_period_ratio, sell_offset=sell_offset,
            sell_zdf=sell_zdf, sell_amount=sell_amount, interval=interval
        )
        return self._request('/xg_more_mom_backtrader_moni', params)
    
    def xg_condi_factor_backtrader_moni(
        self,
        st_name: str = '小果条件因子测试策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),True,False)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        buy_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true},
            "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}
        }''',
        rank_factor: str = '''{
            "均线评分": "降序"
        }''',
        sell_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false},
            "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}
        }''',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """条件多因子策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            sell_condi_factor=sell_condi_factor,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_condi_factor_backtrader_moni', params)
    
    def xg_rank_factor_backtrader_moni(
        self,
        st_name: str = '小果排序多因子模拟策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),0,1)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        is_open_buy_condi: bool = True,
        buy_condi_factor: str = '''{
            "25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0},
            "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}
        }''',
        rank_factor: str = '''{
            "25日回归动量": {"相关性": "正相关", "权重": 1}
        }''',
        total_factor_rank: str = '降序',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """排序多因子策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            is_open_buy_condi=is_open_buy_condi,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            total_factor_rank=total_factor_rank,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_rank_factor_backtrader_moni', params)

    # ============================================================
    # 三、社区策略接口（moni_sq，不带 _1）
    # ============================================================
    
    def xg_dt_backtrader_moni_sq(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        dt_interval: int = 20,
        dt_type: str = '金额',
        dt_value: float = 1000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """定投策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, dt_interval=dt_interval,
            dt_type=dt_type, dt_value=dt_value, sell_zdf=sell_zdf,
            buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_dt_backtrader_moni_sq', params)
    
    def xg_mom_backtrader_moni_sq(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        mom_type: str = '百分比',
        mom_value: float = 1,
        mom_daily: int = 25,
        min_mom: float = 0,
        max_mom: float = 5,
        buy_rank: int = 1,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000
    ) -> Dict[str, Any]:
        """动量策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            mom_type=mom_type, mom_value=mom_value, mom_daily=mom_daily,
            min_mom=min_mom, max_mom=max_mom, buy_rank=buy_rank,
            sell_zdf=sell_zdf, sell_amount=sell_amount
        )
        return self._request('/xg_mom_backtrader_moni_sq', params)
    
    def xg_pz_backtrader_moni_sq(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.4,0.4,0.2',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, index_stock=index_stock,
            cash=cash, sell_zdf=sell_zdf, buy_zdf=buy_zdf,
            trade_value=trade_value, comm=comm
        )
        return self._request('/xg_pz_backtrader_moni_sq', params)
    
    def xg_zcph_backtrader_moni_sq(
        self,
        st_name: str = '小果测试',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        dt_type: str = '百分比',
        weight_list: str = '0.35,0.35,0.3',
        deviation_list: str = '0.1,0.1,0.05',
        interval: int = 20,
        index_stock: str = '000300.SH',
        cash: float = 100000,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001
    ) -> Dict[str, Any]:
        """资产配置平衡策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            dt_type=dt_type, weight_list=weight_list, deviation_list=deviation_list,
            interval=interval, index_stock=index_stock, cash=cash,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value, comm=comm
        )
        return self._request('/xg_zcph_backtrader_moni_sq', params)
    
    def xg_gd_backtrader_moni_sq(
        self,
        st_name: str = '小果网格测试策略',
        open_show: str = '是',
        start_date: str = '20250701',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        gd_interval: int = 1,
        gd_bc_type_list: str = '百分比,百分比',
        gd_buy_bc_list: str = '0.03,0.02',
        gd_sell_bc_list: str = '-0.02,-0.015',
        gd_atr_ratio_list: str = '2.0,2.0',
        gd_atr_period_list: str = '14,14',
        gd_type_list: str = '金额,金额',
        gd_value_list: str = '1000,1500',
        init_position_ratio_list: str = '0.1,0.15',
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000,
        comm: float = 0.0001,
        max_workers: int = 4
    ) -> Dict[str, Any]:
        """网格策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, gd_interval=gd_interval,
            gd_bc_type_list=gd_bc_type_list, gd_buy_bc_list=gd_buy_bc_list,
            gd_sell_bc_list=gd_sell_bc_list, gd_atr_ratio_list=gd_atr_ratio_list,
            gd_atr_period_list=gd_atr_period_list, gd_type_list=gd_type_list,
            gd_value_list=gd_value_list,
            init_position_ratio_list=init_position_ratio_list,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value,
            comm=comm, max_workers=max_workers
        )
        return self._request('/xg_gd_backtrader_moni_sq', params)
    
    def xg_hg_backtrader_moni_sq(
        self,
        st_name: str = '小果海龟测试策略',
        open_show: str = '是',
        start_date: str = '20240101',
        end_date: str = '20500101',
        stock_list: str = '513100.SH,513500.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        entry_period: int = 20,
        exit_period: int = 10,
        n_period: int = 20,
        risk_per_trade: float = 0.01,
        risk_per_unit: float = 0.02,
        max_units: int = 4,
        add_unit_threshold: float = 0.5,
        sell_zdf: float = 0.03,
        buy_zdf: float = -0.03,
        trade_value: float = 1000
    ) -> Dict[str, Any]:
        """海龟策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, entry_period=entry_period,
            exit_period=exit_period, n_period=n_period,
            risk_per_trade=risk_per_trade, risk_per_unit=risk_per_unit,
            max_units=max_units, add_unit_threshold=add_unit_threshold,
            sell_zdf=sell_zdf, buy_zdf=buy_zdf, trade_value=trade_value
        )
        return self._request('/xg_hg_backtrader_moni_sq', params)
    
    def xg_more_mom_backtrader_moni_sq(
        self,
        st_name: str = '小果综合动量测试策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        enable_index_timing: bool = False,
        index_mean_line: int = 20,
        index_not_trader: str = '513100.SH,518880.SH',
        index_condition_type: str = '大于均线',
        index_offset: float = 0.0,
        mom_type: str = '百分比',
        mom_value: float = 0.1,
        mom_models: str = '动量1',
        mom_daily: int = 25,
        period: int = 20,
        short_ma: int = 3,
        long_ma: int = 20,
        enable_mom_filter: bool = False,
        max_value: float = 5,
        mini_value: float = 0,
        max_rank: int = 1,
        min_rank: int = 2,
        enable_buy_condition: bool = False,
        enable_sell_condition: bool = False,
        buy_condition_type: str = '涨幅',
        buy_period: int = 20,
        buy_period_ratio: float = 0.1,
        buy_offset: float = 0.0,
        sell_condition_type: str = '跌幅',
        sell_period: int = 20,
        sell_period_ratio: float = -0.1,
        sell_offset: float = 0.0,
        sell_zdf: float = 0.03,
        sell_amount: float = 1000,
        interval: int = 1
    ) -> Dict[str, Any]:
        """综合动量策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, enable_index_timing=enable_index_timing,
            index_mean_line=index_mean_line, index_not_trader=index_not_trader,
            index_condition_type=index_condition_type, index_offset=index_offset,
            mom_type=mom_type, mom_value=mom_value, mom_models=mom_models,
            mom_daily=mom_daily, period=period, short_ma=short_ma,
            long_ma=long_ma, enable_mom_filter=enable_mom_filter,
            max_value=max_value, mini_value=mini_value,
            max_rank=max_rank, min_rank=min_rank,
            enable_buy_condition=enable_buy_condition,
            enable_sell_condition=enable_sell_condition,
            buy_condition_type=buy_condition_type, buy_period=buy_period,
            buy_period_ratio=buy_period_ratio, buy_offset=buy_offset,
            sell_condition_type=sell_condition_type, sell_period=sell_period,
            sell_period_ratio=sell_period_ratio, sell_offset=sell_offset,
            sell_zdf=sell_zdf, sell_amount=sell_amount, interval=interval
        )
        return self._request('/xg_more_mom_backtrader_moni_sq', params)
    
    def xg_condi_factor_backtrader_moni_sq(
        self,
        st_name: str = '小果条件因子测试策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),True,False)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        buy_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "and", "选择方向": "等于", "值": true},
            "连续上涨天数": {"选择类型": "and", "选择方向": "大于", "值": 2}
        }''',
        rank_factor: str = '''{
            "均线评分": "降序"
        }''',
        sell_condi_factor: str = '''{
            "收盘价大于5日均线": {"选择类型": "or", "选择方向": "等于", "值": false},
            "连续下跌天数": {"选择类型": "or", "选择方向": "大于", "值": 2}
        }''',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """条件多因子策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            sell_condi_factor=sell_condi_factor,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_condi_factor_backtrader_moni_sq', params)
    
    def xg_rank_factor_backtrader_moni_sq(
        self,
        st_name: str = '小果排序多因子社区策略',
        open_show: str = '是',
        start_date: str = '20250101',
        end_date: str = '20261201',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        min_commission: float = 0,
        trader_type: str = '百分比',
        trader_value: float = 0.5,
        hold_stock_limit: int = 2,
        is_open_user_factor: bool = True,
        user_factor_list: str = 'close,high,low,open,amount,volume,zdf',
        user_factor_cacal: str = '''{
            "收盘价大于5日均线": "IF(df['close']>MA(df['close'],5),0,1)",
            "均线评分": "IF(MA(df['close'],3)>MA(df['close'],5),25,0)+IF(MA(df['close'],5)>MA(df['close'],10),25,0)+IF(MA(df['close'],10)>MA(df['close'],20),25,0)+IF(MA(df['close'],20)>MA(df['close'],30),25,0)"
        }''',
        is_open_buy_condi: bool = True,
        buy_condi_factor: str = '''{
            "25日回归动量": {"选择类型": "and", "选择方向": "大于", "值": 0},
            "25日回归动量": {"选择类型": "and", "选择方向": "小于", "值": 5}
        }''',
        rank_factor: str = '''{
            "25日回归动量": {"相关性": "正相关", "权重": 1}
        }''',
        total_factor_rank: str = '降序',
        sell_type: str = '金额',
        sell_zdf: float = 0.03,
        sell_value: float = 1000,
        max_workers: int = 4,
        interval: int = 1,
        min_hold_days: int = 1,
        risk_free_rate: float = 0.02,
        slippage: float = 0,
        enable_limit_up_down_filter: bool = True,
        max_single_position_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """排序多因子策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            min_commission=min_commission, trader_type=trader_type,
            trader_value=trader_value, hold_stock_limit=hold_stock_limit,
            is_open_user_factor=is_open_user_factor,
            user_factor_list=user_factor_list,
            user_factor_cacal=user_factor_cacal,
            is_open_buy_condi=is_open_buy_condi,
            buy_condi_factor=buy_condi_factor,
            rank_factor=rank_factor,
            total_factor_rank=total_factor_rank,
            sell_type=sell_type, sell_zdf=sell_zdf, sell_value=sell_value,
            max_workers=max_workers, interval=interval,
            min_hold_days=min_hold_days, risk_free_rate=risk_free_rate,
            slippage=slippage,
            enable_limit_up_down_filter=enable_limit_up_down_filter,
            max_single_position_ratio=max_single_position_ratio
        )
        return self._request('/xg_rank_factor_backtrader_moni_sq', params)

    # ============================================================
    # 四、数据读取接口
    # ============================================================
    
    def get_moni_trader_data(
        self,
        user: str = "自己信息",
        st_type: str = '动量策略',
        st_name: str = '小果动量模拟策略'
    ) -> Dict[str, Any]:
        """读取模拟交易的统计数据"""
        params = self._get_params(user=user,st_type=st_type, st_name=st_name)
        return self._request('/get_moni_trader_data', params)
    
    def get_moni_trader_data_sq(
        self,
        user: str = "自己信息",
        st_type: str = '动量策略',
        st_name: str = '小果动量模拟策略'
    ) -> Dict[str, Any]:
        """读取社区交易的统计数据"""
        params = self._get_params(user=user,st_type=st_type, st_name=st_name)
        return self._request('/get_moni_trader_data_sq', params)
    
    
    
    def get_stock_hist_data(
        self,
        stock: str = '513100.SH',
        start_date: str = '20200101',
        end_date: str = '20261231'
    ) -> Dict[str, Any]:
        """读取标的历史行情数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date
        )
        return self._request('/get_stock_hist_data', params)
    
    def get_stock_factor_data(
        self,
        stock: str = '513100.SH',
        start_date: str = '20200101',
        end_date: str = '20261231',
        columns: str = 'date,close,open,high,low,volume,amount'
    ) -> Dict[str, Any]:
        """读取标的因子数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            columns=columns
        )
        return self._request('/get_stock_factor_data', params)
    
    def get_stock_finance_data(
        self,
        table: str = '资产负债表',
        date: str = '2026-06-30',
        columns: str = 'secu_code,end_date,total_assets'
    ) -> Dict[str, Any]:
        """读取股票财务数据"""
        params = self._get_params(
            table=table,
            date=date,
            columns=columns
        )
        return self._request('/get_stock_finance_data', params)
        # ============================================================
    # 四、策略删除接口（单个）
    # ============================================================
    
    def del_moni_trader_data(
        self,
        user: str = "自己信息",
        st_type: str = '定投策略',
        st_name: str = '小果定投模拟策略公开',
        open_show: str = '是'
    ) -> Dict[str, Any]:
        """删除模拟策略数据"""
        params = self._get_params(
            user=user,
            st_type=st_type,
            st_name=st_name,
            open_show=open_show
        )
        return self._request('/del_moni_trader_data', params)
    
    def del_moni_trader_data_sq(
        self,
        user: str = "自己信息",
        st_type: str = '定投策略',
        st_name: str = '小果定投模拟策略公开',
        open_show: str = '是'
    ) -> Dict[str, Any]:
        """删除社区策略数据"""
        params = self._get_params(
            user=user,
            st_type=st_type,
            st_name=st_name,
            open_show=open_show
        )
        return self._request('/del_moni_trader_data_sq', params)

    # ============================================================
    # 五、批量策略管理接口
    # ============================================================
    
    def del_all_moni_trader_data(
        self,
        user: str = "自己信息",
        confirm: str = '是'
    ) -> Dict[str, Any]:
        """删除全部模拟策略数据"""
        params = self._get_params(
            user=user,
            confirm=confirm
        )
        return self._request('/del_all_moni_trader_data', params)
    
    def del_all_moni_trader_data_sq(
        self,
        user: str = "自己信息",
        confirm: str = '是'
    ) -> Dict[str, Any]:
        """删除全部社区策略数据"""
        params = self._get_params(
            user=user,
            confirm=confirm
        )
        return self._request('/del_all_moni_trader_data_sq', params)
    
    def get_all_moni_trader_data(
        self,
        user: str = "自己信息"
    ) -> Dict[str, Any]:
        """读取个人模拟全部策略"""
        params = self._get_params(user=user)
        return self._request('/get_all_moni_trader_data', params)
    
    def get_all_moni_trader_data_sq(
        self,
        user: str = "自己信息"
    ) -> Dict[str, Any]:
        """读取个人社区全部策略"""
        params = self._get_params(user=user)
        return self._request('/get_all_moni_trader_data_sq', params)

    # ============================================================
    # 六、策略执行接口
    # ============================================================
    
    def xg_condi_factor_backtrader_run(
        self,
        st_name: str = '小果条件因子测试策略',
        force_rerun: bool = False,
        save_data: bool = True
    ) -> Dict[str, Any]:
        """条件多因子策略回测执行接口"""
        params = self._get_params(
            st_name=st_name,
            force_rerun=force_rerun,
            save_data=save_data
        )
        return self._request('/xg_condi_factor_backtrader_run', params)
    ############################新添加模型**************************
    # ============================================================
    # 七、均值方差策略接口
    # ============================================================
    
    def xg_mean_var_backtrader(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        lookback_days: int = 60,
        max_weight: float = 0.6,
        min_weight: float = 0.05,
        lambda_risk: float = 2.0,
        interval: int = 5
    ) -> Dict[str, Any]:
        """均值方差最优资产组合权重再平衡策略回测"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, lookback_days=lookback_days,
            max_weight=max_weight, min_weight=min_weight,
            lambda_risk=lambda_risk, interval=interval
        )
        return self._request('/xg_mean_var_backtrader_1', params)
    
    def xg_mean_var_backtrader_moni(
        self,
        st_name: str = '小果均值方差策略',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        lookback_days: int = 60,
        max_weight: float = 0.6,
        min_weight: float = 0.05,
        lambda_risk: float = 2.0,
        interval: int = 5
    ) -> Dict[str, Any]:
        """均值方差最优资产组合策略模拟交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, lookback_days=lookback_days,
            max_weight=max_weight, min_weight=min_weight,
            lambda_risk=lambda_risk, interval=interval
        )
        return self._request('/xg_mean_var_backtrader_moni', params)
    
    def xg_mean_var_backtrader_moni_sq(
        self,
        st_name: str = '小果均值方差社区策略',
        open_show: str = '是',
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        index_stock: str = '000300.SH',
        cash: float = 100000,
        comm: float = 0.0001,
        max_workers: int = 4,
        lookback_days: int = 60,
        max_weight: float = 0.6,
        min_weight: float = 0.05,
        lambda_risk: float = 2.0,
        interval: int = 5
    ) -> Dict[str, Any]:
        """均值方差最优资产组合策略社区交易接口"""
        params = self._get_params(
            st_name=st_name, open_show=open_show,
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            index_stock=index_stock, cash=cash, comm=comm,
            max_workers=max_workers, lookback_days=lookback_days,
            max_weight=max_weight, min_weight=min_weight,
            lambda_risk=lambda_risk, interval=interval
        )
        return self._request('/xg_mean_var_backtrader_moni_sq', params)

    # ============================================================
    # 八、多标的量化分析接口
    # ============================================================
    
    def xg_stock_cov_correlation(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        max_workers: int = 4,
        method: str = 'pearson',
        risk_free_rate: float = 0.03
    ) -> Dict[str, Any]:
        """多标的收益率相关性矩阵"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            max_workers=max_workers, method=method,
            risk_free_rate=risk_free_rate
        )
        return self._request('/xg_stock_cov_correlation', params)
    
    def xg_stock_cov_covariance(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        max_workers: int = 4,
        method: str = 'pearson',
        risk_free_rate: float = 0.03,
        annualized: bool = True
    ) -> Dict[str, Any]:
        """多标的收益率协方差矩阵"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            max_workers=max_workers, method=method,
            risk_free_rate=risk_free_rate, annualized=annualized
        )
        return self._request('/xg_stock_cov_covariance', params)
    
    def xg_stock_cov_portfolio(
        self,
        start_date: str = '20260101',
        end_date: str = '20500101',
        stock_list: str = '159915.SZ,513100.SH,518880.SH',
        max_workers: int = 4,
        method: str = 'pearson',
        risk_free_rate: float = 0.03,
        target_return: Optional[float] = None
    ) -> Dict[str, Any]:
        """多标的投资组合优化"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            max_workers=max_workers, method=method,
            risk_free_rate=risk_free_rate, target_return=target_return
        )
        return self._request('/xg_stock_cov_portfolio', params)

    # ============================================================
    # 九、股票组合分析接口
    # ============================================================
    
    def xg_stock_analysis(
        self,
        start_date: str = '20240101',
        end_date: str = '20261231',
        stock_list: str = '159915.SZ,518880.SH,510300.SH',
        stock_weight: str = '0.4,0.3,0.3',
        index_stock: str = '000300.SH',
        max_workers: int = 4,
        risk_free_rate: float = 0.03
    ) -> Dict[str, Any]:
        """小果股票分析系统 - 组合收益分析"""
        params = self._get_params(
            start_date=start_date, end_date=end_date, stock_list=stock_list,
            stock_weight=stock_weight, index_stock=index_stock,
            max_workers=max_workers, risk_free_rate=risk_free_rate
        )
        return self._request('/xg_stock_analysis', params)

    # ============================================================
    # 十、用户认证接口
    # ============================================================
    
    def get_user_info(
        self,
        user: str = "自己信息"
    ) -> Dict[str, Any]:
        """获取用户信息"""
        params = self._get_params(user=user)
        return self._request('/get_user_info', params)
    
    def check_password_is_av_user(
        self,
        user: str = "自己信息"
    ) -> Dict[str, Any]:
        """检查授权码有效性"""
        params = self._get_params(user=user)
        return self._request('/check_password_is_av_user', params)

    # ============================================================
    # 十一、数据查询接口（AKShare/数据库API）
    # ============================================================
    
    def get_wencai_data(
        self,
        query: str = '今日涨停'
    ) -> Dict[str, Any]:
        """获取问财数据"""
        params = self._get_params(query=query)
        return self._request('/get_wencai_data', params)
    
    def get_user_def_data(
        self,
        name: str = 'df',
        func: str = '''
import akshare as ak
df = ak.stock_info_a_code_name()
print(df)
'''
    ) -> Dict[str, Any]:
        """获取自定义数据"""
        params = self._get_params(name=name, func=func)
        return self._request('/get_user_def_data', params)
    
    def get_user_base_data(
        self,
        file_path: str = '/xg_data/全市场股票/',
        file_name: str = '全市场股票'
    ) -> Dict[str, Any]:
        """获取数据库的数据"""
        params = self._get_params(file_path=file_path, file_name=file_name)
        return self._request('/get_user_base_data', params)

    # ============================================================
    # 十二、Tick/分钟数据接口
    # ============================================================
    
    
    
    def get_mini_data_5(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = '5',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """读取5分钟数据（mini）"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/get_mini_data_5', params)
    
    def get_mini_data_15(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = '15',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """读取15分钟数据（mini）"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/get_mini_data_15', params)
    
    def get_mini_data_30(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = '30',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """读取30分钟数据（mini）"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/get_mini_data_30', params)
    
    def get_mini_data_60(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = '60',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """读取60分钟数据（mini）"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/get_mini_data_60', params)

    # ============================================================
    # 十三、K线数据接口
    # ============================================================
    
    def query_history_k_data_plus_d(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'd',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """日线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/query_history_k_data_plus_d', params)
    
    def query_history_k_data_plus_w(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'w',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """周线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/query_history_k_data_plus_w', params)
    
    def query_history_k_data_plus_m(
        self,
        stock: str = 'sh.600031',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'm',
        adjustflag: str = '2'
    ) -> Dict[str, Any]:
        """月线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjustflag
        )
        return self._request('/query_history_k_data_plus_m', params)

    # ============================================================
    # 十四、指数K线数据接口
    # ============================================================
    
    def query_history_k_data_plus_index_d(
        self,
        stock: str = 'sh.000001',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'd'
    ) -> Dict[str, Any]:
        """指数日线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency
        )
        return self._request('/query_history_k_data_plus_index_d', params)
    
    def query_history_k_data_plus_index_w(
        self,
        stock: str = 'sh.000001',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'w'
    ) -> Dict[str, Any]:
        """指数周线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency
        )
        return self._request('/query_history_k_data_plus_index_w', params)
    
    def query_history_k_data_plus_index_m(
        self,
        stock: str = 'sh.000001',
        start_date: str = '2026-04-01',
        end_date: str = '2050-12-31',
        frequency: str = 'm'
    ) -> Dict[str, Any]:
        """指数月线数据"""
        params = self._get_params(
            stock=stock,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency
        )
        return self._request('/query_history_k_data_plus_index_m', params)

    # ============================================================
    # 十五、财务数据接口
    # ============================================================
    
    def query_profit_data(
        self,
        code: str = 'sh.600031',
        year: str = '2025',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """盈利能力"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_profit_data', params)
    
    def query_operation_data(
        self,
        code: str = 'sh.600031',
        year: str = '2025',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """营运能力"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_operation_data', params)
    
    def query_growth_data(
        self,
        code: str = 'sh.600031',
        year: str = '2026',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """季频成长能力"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_growth_data', params)
    
    def query_balance_data(
        self,
        code: str = 'sh.600031',
        year: str = '2026',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """季频偿债能力"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_balance_data', params)
    
    def query_cash_flow_data(
        self,
        code: str = 'sh.600031',
        year: str = '2026',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """季频现金流量"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_cash_flow_data', params)
    
    def query_dupont_data(
        self,
        code: str = 'sh.600031',
        year: str = '2026',
        quarter: str = '1'
    ) -> Dict[str, Any]:
        """季频杜邦指数"""
        params = self._get_params(
            code=code,
            year=year,
            quarter=quarter
        )
        return self._request('/query_dupont_data', params)

    # ============================================================
    # 五、系统接口
    # ============================================================
    
    def root(self) -> Dict[str, Any]:
        """根路径"""
        return self._request('/', {})
    
    def health(self) -> Dict[str, Any]:
        """健康检查"""
        return self._request('/health', {})


# ============================================================
# 测试代码
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 小果量化数据API测试")
    print("=" * 60)
    
    # 初始化客户端（使用您提供的服务器地址）
    client = xg_quant_backtrader_data(
        url="服务器地址",
        port=8888,
        user="自己信息",
        password="自己信息",
        auth_code="自己信息"
    )
    
    print("\n" + "=" * 60)
    print("📋 一、系统接口测试")
    print("=" * 60)
    #因子数据
    df=client.get_stock_factor_data(columns='date,证券代码,5日涨跌幅')
    df=client._to_dataframe(df)
    print(df)
    #股票数据
    df=client.get_stock_hist_data()
    df=client._to_dataframe(df)
    print(df)
    #财务数据
    df=client.get_stock_finance_data()
    df=client._to_dataframe(df)
    print(df)

```

