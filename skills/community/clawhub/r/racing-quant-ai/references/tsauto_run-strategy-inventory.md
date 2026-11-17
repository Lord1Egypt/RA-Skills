# 用户自研量化仓库 tsauto_run 策略储备清单

> 仓库地址：https://gitee.com/warwickInv/tsauto_run（私有）
> 梳理时间：2026-06-01
> 仓库整体架构：数据ETL → 因子工程 → ML多因子模型 → 策略应用 → 运维辅助

---

## 一、数据ETL层（6个模块）

| 模块 | 路径 | 数据内容 | 频率 |
|------|------|----------|------|
| 行情+技术指标 | `get_base_data_Price_and_TAindex/` | 日线OHLCV、TA技术指标（含ETF版） | 日频 |
| 估值指标 | `get_base_data_valuation/` | PE/PB/PS等估值数据 | 日频 |
| 市场指数 | `get_base_data_market_index/` | 宽基指数行情 | 日频 |
| 利润表 | `get_base_data_Financial_IS/` | IS财务数据 | 季频 |
| 资产负债表 | `get_base_data_Financial_BS/` | BS财务数据 | 季频 |
| 现金流量表 | `get_base_data_Financial_CFS/` | CFS财务数据 | 季频 |
| 财务指标 | `get_base_data_Financial_FinIdx/` | 综合财务指标 | 季频 |
| 拥挤度成分 | `get_base_data_stk_crowd_compts/` | 个股拥挤度指标 | 日频 |

数据源：Tushare，存储：SQLite（`E:/TSauto_DataBase/`）

## 二、因子工程层

### 因子库构建（`get_base_get_factors/`）
- `fun_get_base_get_factors_v2.py` / `v2_1.py` — 因子计算核心函数库
- `data_label_preupd.py` — 收益率标签预更新
- `mini_rsp_stock_factor.py` — 迷你响应式因子查询
- `df_model_ic_ind.png` / `各特征IC趋势监控表.png` — IC监控可视化

### 因子处理Pipeline（`ml_general/src/feat_layer.py`）
五步法：中位数去极值 → 均值填充缺失 → 行业中性化 → 因子中性化 → 标准化
筛选阈值：缺失率<0.99、IV>0.01、因子间相关性<0.7

## 三、ML多因子模型家族（核心策略储备，`ml_weekly/`）

### 周频多因子模型变体

| 模型变体 | 文件 | 核心差异 |
|----------|------|----------|
| 基础4周 | `multifactor_model_wkly_all_4w.py` | 回看4周，基准模型 |
| 1周 | `_all_1w.py` | 回看1周，短窗口 |
| 16周 | `_all_16w.py` | 回看16周，长窗口 |
| 16周+回归 | `_all_16w_reg.py` | 回归版（非分类） |
| 16周+滞后1+权重调整 | `_all_16w_pdtlag1_wadj.py` | 预测滞后1期+样本权重 |
| 4周+滞后1+权重调整 | `_all_4w_pdtlag1_wadj.py` | 同上4周版 |
| 4周+滞后1+权重调整+相关性v2 | `_all_4w_pdtlag1_wadj_dtlcorrv2.py` | 去相关性升级 |
| 4周+TSCV | `_all_4w_tscv.py` | 时序交叉验证 |
| 4周+滞后1+TSCV+排名标签 | `_all_4w_rklz_tscv.py` | 排名标签+TSCV |
| 4周+权重调整 | `_all_4w_wadj.py` | 样本权重调整 |
| 4周+行业增强 | `_all_4w_addind.py` | 加入行业特征 |
| 4周+细粒度远期+市值 | `_all_4w_dtlfar_cap.py` | 细分远期+市值约束 |
| 日频远期 | `_rqfar.py` | 日频远期因子 |
| 日频远期+小市值+Alpha101+8周 | `_rqfar_sub_cap0.1_alp101_8w.py` | 小市值子集+Alpha101 |
| 中证1800+16周+滞后1 | `_sub_1800_16w_pdtlag1.py` | 中证1800成分股 |
| 低换手500+8周 | `_sub_underturn_500_8w.py` | 低换手率股票池 |

### 月频多因子模型（`get_base_get_factors/`）
- `multifactor_model_mthly_far_v1_1of3.py` — 月频版v1（691行）
- `multifactor_model_mthly_far_v2_1of3.py` — 月频版v2

### 多模块集成模型
- `multi-mudule-far_model_wkly_all_4w.py` — 多因子模块集成（4周版）
- `multi-mudule-far_model_wkly.py` — 多因子模块集成（通用版）
- `stacking_model.py` — Stacking集成：XGB+LGB+CatBoost→二级融合

### 通用ML框架（`ml_general/`）
四层解耦：config.py → main.py → data_layer/feat_layer/model_layer/eval_layer
模型注册表：ICIR → LR(逻辑回归) → XGB(固定参数) → LGB(贝叶斯优化)

### 实验变体汇总（从factor_imp_screener.py提取）
```
全市场系列:  train_4/8/12/16_pdt_1
增强系列:    _wadj / _dtlfar_cap / _addind
分段系列:    low_cap_0.1 / low_PB_0.3 / underturn_500
成分股系列:  index_1000 / index_zz1000 / index_1800 / index_gz2000 / index_cyb_all
子模块系列:  alpha101 / mai / energy / obos / fin_growth / fin_eod
```

## 四、策略应用层

### 择时策略（`run_time_selection/`）
| 策略 | 文件 | 算法 |
|------|------|------|
| EMA择时 | `ema5_13_399006.py` | EMA(5,13)金叉死叉 |
| RSRS择时 | `RSRSstd18_600_7m7_399006.py` | RSRS标准分择时(18日窗口,600日标准化) |
| MACD择时 | `MACD_399006.py` | MACD信号择时 |
| GFTD神奇九转 | `GFTD_Series.py` | GFTD九转计数择时 |
| BBL布林带 | `BBL.py` | 布林带择时 |

运行入口：`run_time_selection.py` → 批量生成图表 → 邮件推送

### 技术-标的匹配（`stg_sec_matching/`）
- `stg_func.py` — 9个技术策略函数库（单指标5+多指标4）
- `run_sec_timing_matching.py` — 批量遍历标的×策略，筛选最优"标的-信号"对
- `ts_evaluate_v2.py` — 回测评估引擎（含交易成本、多空支持）

单指标：双均线、EMA、RSI、MACD、KDJ、神奇九转、RSRS
多指标：双均线+RSI、EMA+MACD、RSI+MACD、KDJ+神奇九转

### 指数估值（`run_index_valuation/`）
- 覆盖：沪深300、中证500、中证1000、创业板指
- 方法：1250日（≈5年）PB/PE分位数

### 行业三维模型（`run_industry_3d_model/`）
- 维度：拥挤度×趋势×繁荣度三维散点图
- 行业：申万一级/二级

### 行业概念趋势T+1（`run_industry_concept_trend_Tplus1/`）
- 申万二级行业趋势追踪+概念板块动量

## 五、运维辅助

| 模块 | 功能 |
|------|------|
| `ml_weekly/ops_tools/daily_nv_monitoring.py` | 组合净值日频监控 |
| `ml_weekly/ops_tools/net_buy_sell.py` | 持仓调仓：卖跌出Top排名、买新Top补齐 |
| `ml_weekly/risk_exposure/barra_corr.py` | 模型分 vs Barra风格因子相关性监控 |
| `ml_weekly/time_selection/antidir_rate.py` | 逆向因子比率择时（ML版择时） |
| `ml_weekly/feats_ic_monitoring.py` | 因子IC/IR监控 |
| `ml_weekly/feats_screen_multi_k.py` | 多窗口因子筛选（按IR排序+去相关） |
| `ml_weekly/factor_imp_screener.py` | 基于feature_importance的特征筛选 |

## 六、基础设施层（`common_set/`）
- `quick_usage.py`（541行）— Tushare/AkShare数据接口工具库
- `evaluate.py` — 策略评估指标体系
- `function_time_selection.py` — 择时工具箱（EMA信号+ATR止盈止损）
- `auth_pswd.py` — Tushare授权密钥
