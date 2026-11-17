# Alpha158 初始参考因子清单（提取自 Qlib 官方源码）

> 来源：`qlib/contrib/data/loader.py` 中 `Alpha158DL.get_feature_config()`，及 `qlib/contrib/data/handler.py` 中 `class Alpha158`。
> 表达式语言为 Qlib 算子表达式（$close 等表示字段，Ref/Mean/Std 等为算子）。
> 总因子数：**158**

## 类别分布

| 类别 | 数量 | 说明 |
| --- | --- | --- |
| kbar | 9 | 当日 K 线形态特征（硬编码） |
| price | 4 | 当日价格相对收盘价归一（OPEN/HIGH/LOW/VWAP） |
| rolling | 145 | 基于滚动窗口的 29 类算子 × 5 窗口(5/10/20/30/60) |

## kbar 类因子

| 序号 | 因子名 | Qlib 表达式 | 含义说明 |
| --- | --- | --- | --- |
| 1 | `KMID` | `($close-$open)/$open` | 当日实体涨跌幅 (收盘-开盘)/开盘 |
| 2 | `KLEN` | `($high-$low)/$open` | 当日实体长度 (最高-最低)/开盘 |
| 3 | `KMID2` | `($close-$open)/($high-$low+1e-12)` | 实体占振幅比，分母加 1e-12 防除零 |
| 4 | `KUP` | `($high-Greater($open, $close))/$open` | 上影线长度 / 开盘 |
| 5 | `KUP2` | `($high-Greater($open, $close))/($high-$low+1e-12)` | 上影线占振幅比 |
| 6 | `KLOW` | `(Less($open, $close)-$low)/$open` | 下影线长度 / 开盘 |
| 7 | `KLOW2` | `(Less($open, $close)-$low)/($high-$low+1e-12)` | 下影线占振幅比 |
| 8 | `KSFT` | `(2*$close-$high-$low)/$open` | (2*收盘-最高-最低)/开盘，影线偏离 |
| 9 | `KSFT2` | `(2*$close-$high-$low)/($high-$low+1e-12)` | 影线偏离占振幅比 |

## price 类因子

| 序号 | 因子名 | Qlib 表达式 | 含义说明 |
| --- | --- | --- | --- |
| 1 | `OPEN0` | `$open/$close` | OPEN 当日价格相对收盘价归一 |
| 2 | `HIGH0` | `$high/$close` | HIGH 当日价格相对收盘价归一 |
| 3 | `LOW0` | `$low/$close` | LOW 当日价格相对收盘价归一 |
| 4 | `VWAP0` | `$vwap/$close` | VWAP 当日价格相对收盘价归一 |

## rolling 类因子

| 序号 | 因子名 | Qlib 表达式 | 含义说明 |
| --- | --- | --- | --- |
| 1 | `ROC5` | `Ref($close, 5)/$close` | 过去5日收盘价变化率/最新收盘（变动率） |
| 2 | `ROC10` | `Ref($close, 10)/$close` | 过去10日收盘价变化率/最新收盘（变动率） |
| 3 | `ROC20` | `Ref($close, 20)/$close` | 过去20日收盘价变化率/最新收盘（变动率） |
| 4 | `ROC30` | `Ref($close, 30)/$close` | 过去30日收盘价变化率/最新收盘（变动率） |
| 5 | `ROC60` | `Ref($close, 60)/$close` | 过去60日收盘价变化率/最新收盘（变动率） |
| 6 | `MA5` | `Mean($close, 5)/$close` | 过去5日收盘价简单移动平均/最新收盘 |
| 7 | `MA10` | `Mean($close, 10)/$close` | 过去10日收盘价简单移动平均/最新收盘 |
| 8 | `MA20` | `Mean($close, 20)/$close` | 过去20日收盘价简单移动平均/最新收盘 |
| 9 | `MA30` | `Mean($close, 30)/$close` | 过去30日收盘价简单移动平均/最新收盘 |
| 10 | `MA60` | `Mean($close, 60)/$close` | 过去60日收盘价简单移动平均/最新收盘 |
| 11 | `STD5` | `Std($close, 5)/$close` | 过去5日收盘价标准差/最新收盘（波动率） |
| 12 | `STD10` | `Std($close, 10)/$close` | 过去10日收盘价标准差/最新收盘（波动率） |
| 13 | `STD20` | `Std($close, 20)/$close` | 过去20日收盘价标准差/最新收盘（波动率） |
| 14 | `STD30` | `Std($close, 30)/$close` | 过去30日收盘价标准差/最新收盘（波动率） |
| 15 | `STD60` | `Std($close, 60)/$close` | 过去60日收盘价标准差/最新收盘（波动率） |
| 16 | `BETA5` | `Slope($close, 5)/$close` | 过去5日收盘价的线性回归斜率/最新收盘 |
| 17 | `BETA10` | `Slope($close, 10)/$close` | 过去10日收盘价的线性回归斜率/最新收盘 |
| 18 | `BETA20` | `Slope($close, 20)/$close` | 过去20日收盘价的线性回归斜率/最新收盘 |
| 19 | `BETA30` | `Slope($close, 30)/$close` | 过去30日收盘价的线性回归斜率/最新收盘 |
| 20 | `BETA60` | `Slope($close, 60)/$close` | 过去60日收盘价的线性回归斜率/最新收盘 |
| 21 | `RSQR5` | `Rsquare($close, 5)` | 过去5日收盘价线性回归 R²（趋势线性度） |
| 22 | `RSQR10` | `Rsquare($close, 10)` | 过去10日收盘价线性回归 R²（趋势线性度） |
| 23 | `RSQR20` | `Rsquare($close, 20)` | 过去20日收盘价线性回归 R²（趋势线性度） |
| 24 | `RSQR30` | `Rsquare($close, 30)` | 过去30日收盘价线性回归 R²（趋势线性度） |
| 25 | `RSQR60` | `Rsquare($close, 60)` | 过去60日收盘价线性回归 R²（趋势线性度） |
| 26 | `RESI5` | `Resi($close, 5)/$close` | 过去5日线性回归残差/最新收盘 |
| 27 | `RESI10` | `Resi($close, 10)/$close` | 过去10日线性回归残差/最新收盘 |
| 28 | `RESI20` | `Resi($close, 20)/$close` | 过去20日线性回归残差/最新收盘 |
| 29 | `RESI30` | `Resi($close, 30)/$close` | 过去30日线性回归残差/最新收盘 |
| 30 | `RESI60` | `Resi($close, 60)/$close` | 过去60日线性回归残差/最新收盘 |
| 31 | `MAX5` | `Max($high, 5)/$close` | 过去5日最高价最大值/最新收盘 |
| 32 | `MAX10` | `Max($high, 10)/$close` | 过去10日最高价最大值/最新收盘 |
| 33 | `MAX20` | `Max($high, 20)/$close` | 过去20日最高价最大值/最新收盘 |
| 34 | `MAX30` | `Max($high, 30)/$close` | 过去30日最高价最大值/最新收盘 |
| 35 | `MAX60` | `Max($high, 60)/$close` | 过去60日最高价最大值/最新收盘 |
| 36 | `MIN5` | `Min($low, 5)/$close` | 过去5日最低价最小值/最新收盘 |
| 37 | `MIN10` | `Min($low, 10)/$close` | 过去10日最低价最小值/最新收盘 |
| 38 | `MIN20` | `Min($low, 20)/$close` | 过去20日最低价最小值/最新收盘 |
| 39 | `MIN30` | `Min($low, 30)/$close` | 过去30日最低价最小值/最新收盘 |
| 40 | `MIN60` | `Min($low, 60)/$close` | 过去60日最低价最小值/最新收盘 |
| 41 | `QTLU5` | `Quantile($close, 5, 0.8)/$close` | 过去5日收盘价 80% 分位/最新收盘 |
| 42 | `QTLU10` | `Quantile($close, 10, 0.8)/$close` | 过去10日收盘价 80% 分位/最新收盘 |
| 43 | `QTLU20` | `Quantile($close, 20, 0.8)/$close` | 过去20日收盘价 80% 分位/最新收盘 |
| 44 | `QTLU30` | `Quantile($close, 30, 0.8)/$close` | 过去30日收盘价 80% 分位/最新收盘 |
| 45 | `QTLU60` | `Quantile($close, 60, 0.8)/$close` | 过去60日收盘价 80% 分位/最新收盘 |
| 46 | `QTLD5` | `Quantile($close, 5, 0.2)/$close` | 过去5日收盘价 20% 分位/最新收盘 |
| 47 | `QTLD10` | `Quantile($close, 10, 0.2)/$close` | 过去10日收盘价 20% 分位/最新收盘 |
| 48 | `QTLD20` | `Quantile($close, 20, 0.2)/$close` | 过去20日收盘价 20% 分位/最新收盘 |
| 49 | `QTLD30` | `Quantile($close, 30, 0.2)/$close` | 过去30日收盘价 20% 分位/最新收盘 |
| 50 | `QTLD60` | `Quantile($close, 60, 0.2)/$close` | 过去60日收盘价 20% 分位/最新收盘 |
| 51 | `RANK5` | `Rank($close, 5)` | 当日收盘在 past5日中的分位排名 |
| 52 | `RANK10` | `Rank($close, 10)` | 当日收盘在 past10日中的分位排名 |
| 53 | `RANK20` | `Rank($close, 20)` | 当日收盘在 past20日中的分位排名 |
| 54 | `RANK30` | `Rank($close, 30)` | 当日收盘在 past30日中的分位排名 |
| 55 | `RANK60` | `Rank($close, 60)` | 当日收盘在 past60日中的分位排名 |
| 56 | `RSV5` | `($close-Min($low, 5))/(Max($high, 5)-Min($low, 5)+1e-12)` | 未成熟随机值，价格在5日高低区间的位置 |
| 57 | `RSV10` | `($close-Min($low, 10))/(Max($high, 10)-Min($low, 10)+1e-12)` | 未成熟随机值，价格在10日高低区间的位置 |
| 58 | `RSV20` | `($close-Min($low, 20))/(Max($high, 20)-Min($low, 20)+1e-12)` | 未成熟随机值，价格在20日高低区间的位置 |
| 59 | `RSV30` | `($close-Min($low, 30))/(Max($high, 30)-Min($low, 30)+1e-12)` | 未成熟随机值，价格在30日高低区间的位置 |
| 60 | `RSV60` | `($close-Min($low, 60))/(Max($high, 60)-Min($low, 60)+1e-12)` | 未成熟随机值，价格在60日高低区间的位置 |
| 61 | `IMAX5` | `IdxMax($high, 5)/5` | 过去5日最高价距今日天数 / 5（Aroon 上扬） |
| 62 | `IMAX10` | `IdxMax($high, 10)/10` | 过去10日最高价距今日天数 / 10（Aroon 上扬） |
| 63 | `IMAX20` | `IdxMax($high, 20)/20` | 过去20日最高价距今日天数 / 20（Aroon 上扬） |
| 64 | `IMAX30` | `IdxMax($high, 30)/30` | 过去30日最高价距今日天数 / 30（Aroon 上扬） |
| 65 | `IMAX60` | `IdxMax($high, 60)/60` | 过去60日最高价距今日天数 / 60（Aroon 上扬） |
| 66 | `IMIN5` | `IdxMin($low, 5)/5` | 过去5日最低价距今日天数 / 5（Aroon 下探） |
| 67 | `IMIN10` | `IdxMin($low, 10)/10` | 过去10日最低价距今日天数 / 10（Aroon 下探） |
| 68 | `IMIN20` | `IdxMin($low, 20)/20` | 过去20日最低价距今日天数 / 20（Aroon 下探） |
| 69 | `IMIN30` | `IdxMin($low, 30)/30` | 过去30日最低价距今日天数 / 30（Aroon 下探） |
| 70 | `IMIN60` | `IdxMin($low, 60)/60` | 过去60日最低价距今日天数 / 60（Aroon 下探） |
| 71 | `IMXD5` | `(IdxMax($high, 5)-IdxMin($low, 5))/5` | 最高/最低出现日的时间差 / 5 |
| 72 | `IMXD10` | `(IdxMax($high, 10)-IdxMin($low, 10))/10` | 最高/最低出现日的时间差 / 10 |
| 73 | `IMXD20` | `(IdxMax($high, 20)-IdxMin($low, 20))/20` | 最高/最低出现日的时间差 / 20 |
| 74 | `IMXD30` | `(IdxMax($high, 30)-IdxMin($low, 30))/30` | 最高/最低出现日的时间差 / 30 |
| 75 | `IMXD60` | `(IdxMax($high, 60)-IdxMin($low, 60))/60` | 最高/最低出现日的时间差 / 60 |
| 76 | `CORR5` | `Corr($close, Log($volume+1), 5)` | 收盘价与对数成交量5日相关性 |
| 77 | `CORR10` | `Corr($close, Log($volume+1), 10)` | 收盘价与对数成交量10日相关性 |
| 78 | `CORR20` | `Corr($close, Log($volume+1), 20)` | 收盘价与对数成交量20日相关性 |
| 79 | `CORR30` | `Corr($close, Log($volume+1), 30)` | 收盘价与对数成交量30日相关性 |
| 80 | `CORR60` | `Corr($close, Log($volume+1), 60)` | 收盘价与对数成交量60日相关性 |
| 81 | `CORD5` | `Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 5)` | 价变率与量变率对数5日相关性 |
| 82 | `CORD10` | `Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 10)` | 价变率与量变率对数10日相关性 |
| 83 | `CORD20` | `Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 20)` | 价变率与量变率对数20日相关性 |
| 84 | `CORD30` | `Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 30)` | 价变率与量变率对数30日相关性 |
| 85 | `CORD60` | `Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 60)` | 价变率与量变率对数60日相关性 |
| 86 | `CNTP5` | `Mean($close>Ref($close, 1), 5)` | 过去5日上涨天数占比 |
| 87 | `CNTP10` | `Mean($close>Ref($close, 1), 10)` | 过去10日上涨天数占比 |
| 88 | `CNTP20` | `Mean($close>Ref($close, 1), 20)` | 过去20日上涨天数占比 |
| 89 | `CNTP30` | `Mean($close>Ref($close, 1), 30)` | 过去30日上涨天数占比 |
| 90 | `CNTP60` | `Mean($close>Ref($close, 1), 60)` | 过去60日上涨天数占比 |
| 91 | `CNTN5` | `Mean($close<Ref($close, 1), 5)` | 过去5日下跌天数占比 |
| 92 | `CNTN10` | `Mean($close<Ref($close, 1), 10)` | 过去10日下跌天数占比 |
| 93 | `CNTN20` | `Mean($close<Ref($close, 1), 20)` | 过去20日下跌天数占比 |
| 94 | `CNTN30` | `Mean($close<Ref($close, 1), 30)` | 过去30日下跌天数占比 |
| 95 | `CNTN60` | `Mean($close<Ref($close, 1), 60)` | 过去60日下跌天数占比 |
| 96 | `CNTD5` | `Mean($close>Ref($close, 1), 5)-Mean($close<Ref($close, 1), 5)` | 过去5日涨跌天数差 |
| 97 | `CNTD10` | `Mean($close>Ref($close, 1), 10)-Mean($close<Ref($close, 1), 10)` | 过去10日涨跌天数差 |
| 98 | `CNTD20` | `Mean($close>Ref($close, 1), 20)-Mean($close<Ref($close, 1), 20)` | 过去20日涨跌天数差 |
| 99 | `CNTD30` | `Mean($close>Ref($close, 1), 30)-Mean($close<Ref($close, 1), 30)` | 过去30日涨跌天数差 |
| 100 | `CNTD60` | `Mean($close>Ref($close, 1), 60)-Mean($close<Ref($close, 1), 60)` | 过去60日涨跌天数差 |
| 101 | `SUMP5` | `Sum(Greater($close-Ref($close, 1), 0), 5)/(Sum(Abs($close-Ref($close, 1)), 5)+1e-12)` | 涨幅和/总绝对涨跌（类 RSI 上升） |
| 102 | `SUMP10` | `Sum(Greater($close-Ref($close, 1), 0), 10)/(Sum(Abs($close-Ref($close, 1)), 10)+1e-12)` | 涨幅和/总绝对涨跌（类 RSI 上升） |
| 103 | `SUMP20` | `Sum(Greater($close-Ref($close, 1), 0), 20)/(Sum(Abs($close-Ref($close, 1)), 20)+1e-12)` | 涨幅和/总绝对涨跌（类 RSI 上升） |
| 104 | `SUMP30` | `Sum(Greater($close-Ref($close, 1), 0), 30)/(Sum(Abs($close-Ref($close, 1)), 30)+1e-12)` | 涨幅和/总绝对涨跌（类 RSI 上升） |
| 105 | `SUMP60` | `Sum(Greater($close-Ref($close, 1), 0), 60)/(Sum(Abs($close-Ref($close, 1)), 60)+1e-12)` | 涨幅和/总绝对涨跌（类 RSI 上升） |
| 106 | `SUMN5` | `Sum(Greater(Ref($close, 1)-$close, 0), 5)/(Sum(Abs($close-Ref($close, 1)), 5)+1e-12)` | 跌幅和/总绝对涨跌（类 RSI 下降） |
| 107 | `SUMN10` | `Sum(Greater(Ref($close, 1)-$close, 0), 10)/(Sum(Abs($close-Ref($close, 1)), 10)+1e-12)` | 跌幅和/总绝对涨跌（类 RSI 下降） |
| 108 | `SUMN20` | `Sum(Greater(Ref($close, 1)-$close, 0), 20)/(Sum(Abs($close-Ref($close, 1)), 20)+1e-12)` | 跌幅和/总绝对涨跌（类 RSI 下降） |
| 109 | `SUMN30` | `Sum(Greater(Ref($close, 1)-$close, 0), 30)/(Sum(Abs($close-Ref($close, 1)), 30)+1e-12)` | 跌幅和/总绝对涨跌（类 RSI 下降） |
| 110 | `SUMN60` | `Sum(Greater(Ref($close, 1)-$close, 0), 60)/(Sum(Abs($close-Ref($close, 1)), 60)+1e-12)` | 跌幅和/总绝对涨跌（类 RSI 下降） |
| 111 | `SUMD5` | `(Sum(Greater($close-Ref($close, 1), 0), 5)-Sum(Greater(Ref($close, 1)-$close, 0), 5))/(Sum(Abs($close-Ref($close, 1)), 5)+1e-12)` | 涨跌强度差比（类 RSI 差值） |
| 112 | `SUMD10` | `(Sum(Greater($close-Ref($close, 1), 0), 10)-Sum(Greater(Ref($close, 1)-$close, 0), 10))/(Sum(Abs($close-Ref($close, 1)), 10)+1e-12)` | 涨跌强度差比（类 RSI 差值） |
| 113 | `SUMD20` | `(Sum(Greater($close-Ref($close, 1), 0), 20)-Sum(Greater(Ref($close, 1)-$close, 0), 20))/(Sum(Abs($close-Ref($close, 1)), 20)+1e-12)` | 涨跌强度差比（类 RSI 差值） |
| 114 | `SUMD30` | `(Sum(Greater($close-Ref($close, 1), 0), 30)-Sum(Greater(Ref($close, 1)-$close, 0), 30))/(Sum(Abs($close-Ref($close, 1)), 30)+1e-12)` | 涨跌强度差比（类 RSI 差值） |
| 115 | `SUMD60` | `(Sum(Greater($close-Ref($close, 1), 0), 60)-Sum(Greater(Ref($close, 1)-$close, 0), 60))/(Sum(Abs($close-Ref($close, 1)), 60)+1e-12)` | 涨跌强度差比（类 RSI 差值） |
| 116 | `VMA5` | `Mean($volume, 5)/($volume+1e-12)` | 过去5日成交量移动平均/最新成交量 |
| 117 | `VMA10` | `Mean($volume, 10)/($volume+1e-12)` | 过去10日成交量移动平均/最新成交量 |
| 118 | `VMA20` | `Mean($volume, 20)/($volume+1e-12)` | 过去20日成交量移动平均/最新成交量 |
| 119 | `VMA30` | `Mean($volume, 30)/($volume+1e-12)` | 过去30日成交量移动平均/最新成交量 |
| 120 | `VMA60` | `Mean($volume, 60)/($volume+1e-12)` | 过去60日成交量移动平均/最新成交量 |
| 121 | `VSTD5` | `Std($volume, 5)/($volume+1e-12)` | 过去5日成交量标准差/最新成交量 |
| 122 | `VSTD10` | `Std($volume, 10)/($volume+1e-12)` | 过去10日成交量标准差/最新成交量 |
| 123 | `VSTD20` | `Std($volume, 20)/($volume+1e-12)` | 过去20日成交量标准差/最新成交量 |
| 124 | `VSTD30` | `Std($volume, 30)/($volume+1e-12)` | 过去30日成交量标准差/最新成交量 |
| 125 | `VSTD60` | `Std($volume, 60)/($volume+1e-12)` | 过去60日成交量标准差/最新成交量 |
| 126 | `WVMA5` | `Std(Abs($close/Ref($close, 1)-1)*$volume, 5)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, 5)+1e-12)` | 量加权价变波动率 / 5日均值 |
| 127 | `WVMA10` | `Std(Abs($close/Ref($close, 1)-1)*$volume, 10)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, 10)+1e-12)` | 量加权价变波动率 / 10日均值 |
| 128 | `WVMA20` | `Std(Abs($close/Ref($close, 1)-1)*$volume, 20)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, 20)+1e-12)` | 量加权价变波动率 / 20日均值 |
| 129 | `WVMA30` | `Std(Abs($close/Ref($close, 1)-1)*$volume, 30)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, 30)+1e-12)` | 量加权价变波动率 / 30日均值 |
| 130 | `WVMA60` | `Std(Abs($close/Ref($close, 1)-1)*$volume, 60)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, 60)+1e-12)` | 量加权价变波动率 / 60日均值 |
| 131 | `VSUMP5` | `Sum(Greater($volume-Ref($volume, 1), 0), 5)/(Sum(Abs($volume-Ref($volume, 1)), 5)+1e-12)` | 放量和/总绝对量变（量 RSI 上升） |
| 132 | `VSUMP10` | `Sum(Greater($volume-Ref($volume, 1), 0), 10)/(Sum(Abs($volume-Ref($volume, 1)), 10)+1e-12)` | 放量和/总绝对量变（量 RSI 上升） |
| 133 | `VSUMP20` | `Sum(Greater($volume-Ref($volume, 1), 0), 20)/(Sum(Abs($volume-Ref($volume, 1)), 20)+1e-12)` | 放量和/总绝对量变（量 RSI 上升） |
| 134 | `VSUMP30` | `Sum(Greater($volume-Ref($volume, 1), 0), 30)/(Sum(Abs($volume-Ref($volume, 1)), 30)+1e-12)` | 放量和/总绝对量变（量 RSI 上升） |
| 135 | `VSUMP60` | `Sum(Greater($volume-Ref($volume, 1), 0), 60)/(Sum(Abs($volume-Ref($volume, 1)), 60)+1e-12)` | 放量和/总绝对量变（量 RSI 上升） |
| 136 | `VSUMN5` | `Sum(Greater(Ref($volume, 1)-$volume, 0), 5)/(Sum(Abs($volume-Ref($volume, 1)), 5)+1e-12)` | 缩量和/总绝对量变（量 RSI 下降） |
| 137 | `VSUMN10` | `Sum(Greater(Ref($volume, 1)-$volume, 0), 10)/(Sum(Abs($volume-Ref($volume, 1)), 10)+1e-12)` | 缩量和/总绝对量变（量 RSI 下降） |
| 138 | `VSUMN20` | `Sum(Greater(Ref($volume, 1)-$volume, 0), 20)/(Sum(Abs($volume-Ref($volume, 1)), 20)+1e-12)` | 缩量和/总绝对量变（量 RSI 下降） |
| 139 | `VSUMN30` | `Sum(Greater(Ref($volume, 1)-$volume, 0), 30)/(Sum(Abs($volume-Ref($volume, 1)), 30)+1e-12)` | 缩量和/总绝对量变（量 RSI 下降） |
| 140 | `VSUMN60` | `Sum(Greater(Ref($volume, 1)-$volume, 0), 60)/(Sum(Abs($volume-Ref($volume, 1)), 60)+1e-12)` | 缩量和/总绝对量变（量 RSI 下降） |
| 141 | `VSUMD5` | `(Sum(Greater($volume-Ref($volume, 1), 0), 5)-Sum(Greater(Ref($volume, 1)-$volume, 0), 5))/(Sum(Abs($volume-Ref($volume, 1)), 5)+1e-12)` | 量能涨跌强度差比 |
| 142 | `VSUMD10` | `(Sum(Greater($volume-Ref($volume, 1), 0), 10)-Sum(Greater(Ref($volume, 1)-$volume, 0), 10))/(Sum(Abs($volume-Ref($volume, 1)), 10)+1e-12)` | 量能涨跌强度差比 |
| 143 | `VSUMD20` | `(Sum(Greater($volume-Ref($volume, 1), 0), 20)-Sum(Greater(Ref($volume, 1)-$volume, 0), 20))/(Sum(Abs($volume-Ref($volume, 1)), 20)+1e-12)` | 量能涨跌强度差比 |
| 144 | `VSUMD30` | `(Sum(Greater($volume-Ref($volume, 1), 0), 30)-Sum(Greater(Ref($volume, 1)-$volume, 0), 30))/(Sum(Abs($volume-Ref($volume, 1)), 30)+1e-12)` | 量能涨跌强度差比 |
| 145 | `VSUMD60` | `(Sum(Greater($volume-Ref($volume, 1), 0), 60)-Sum(Greater(Ref($volume, 1)-$volume, 0), 60))/(Sum(Abs($volume-Ref($volume, 1)), 60)+1e-12)` | 量能涨跌强度差比 |

## 备注

- `1e-12` 用于防止除零；`Greater`/`Less`/`Ref`/`Mean`/`Std`/`Slope`/`Rsquare`/`Resi`/`Max`/`Min`/`Quantile`/`Rank`/`IdxMax`/`IdxMin`/`Corr`/`Sum`/`Abs` 均为 Qlib 内置算子。
- 标签（label）默认配置：`Ref($close, -2)/Ref($close, -1) - 1` -> `LABEL0`（未来 2 日收益率）。
- Alpha158 与 Alpha360 的区别：Alpha360 为原始价量数据（近 60 日 6 字段归一，共 360 维），Alpha158 为构造后的 158 维特征。
- **Qlib 中不存在 Alpha300**，仅有 Alpha158 与 Alpha360。
