# 配置参考

## config.py 关键配置项

| 配置 | 默认值 | 说明 |
|------|--------|------|
| `TARGET_STOCKS` | 10只A股 | 预测目标股票池（代码→名称dict） |
| `XGB_PARAMS` | max_depth=6, lr=0.05, n=300 | XGBoost超参数 |
| `TOP_N_FEATURES` | 40 | 特征选择保留数量 |
| `CV_FOLDS` | 10 | 交叉验证折数 |
| `FETCH_DELAY` | 1.5 | API请求间隔（秒） |
| `MODEL_PATH` | models/xgb_stock_model.pkl | 模型保存路径 |
| `SCALER_PATH` | models/scaler.pkl | StandardScaler路径 |
| `FEATURE_PATH` | models/feature_names.json | 入模特征列表 |
| `REPORT_PATH` | results/model_report.json | 报告JSON |
| `PREDICTION_PATH` | results/predictions.csv | 预测结果CSV |
| `PREDICTION_HISTORY_DIR` | results/prediction_history/ | 每次预测批次快照目录 |
| `EVALUATION_PATH` | results/evaluation.csv | 评估结果CSV |

## 特征分类（102个候选）

| # | 类别 | 特征数 | 代表特征 |
|---|------|--------|----------|
| 1 | 价格收益率 | 6 | return_1/2/3/5/10/20 |
| 2 | 均线比率 | 5 | ma_ratio_5/10/20/50/100 |
| 3 | EMA比率 | 4 | ema_ratio_5/10/20/50 |
| 4 | 均线交叉 | 4 | ma_cross_5_10/5_20/10_20/10_50 |
| 5 | RSI | 3 | rsi_6/14/24 |
| 6 | MACD | 3 | macd_norm/signal_norm/hist_norm |
| 7 | KDJ | 6 | kdj_k/d/j × 9/14周期 |
| 8 | Williams %R | 2 | williams_r_14/28 |
| 9 | CCI | 2 | cci_14/20 |
| 10 | 布林带 | 2 | bb_width/bb_position |
| 11 | 成交量 | 5 | volume_ratio_5/10/20, change, change_5 |
| 12 | OBV | 2 | obv_ratio_5/20 |
| 13 | MFI | 1 | mfi_14 |
| 14 | VWAP | 1 | vwap_dev |
| 15 | 波动率 | 4 | volatility_5/10/20, ratio_5_20 |
| 16 | K线形态 | 5 | high_low_ratio, close_open_ratio, upper/lower_shadow, body_ratio |
| 17 | ATR | 2 | atr_7/14 |
| 18 | 动量 | 3 | momentum_5/10/20 |
| 19 | 收益加速度 | 1 | return_accel |
| 20 | 偏度/峰度 | 4 | skew_10/20, kurtosis_10/20 |
| 21 | 连涨跌 | 3 | consec_count/dir/signed |
| 22 | 距N日高低点 | 6 | dist_high/low × 10/20/50 |
| 23 | 滞后收益率 | 4 | return_lag_1/2/3/5 |
| 24 | 量价相关性 | 2 | vol_price_corr_10/20 |
| 25 | 枢轴点 | 3 | pivot_dev/r1_dev/s1_dev |
| 26 | ADX/DI | 3 | adx_14, plus_di_14, minus_di_14 |
| 27 | TRIX | 1 | trix |
| 28 | Chaikin | 1 | chaikin_vol |
| 29 | 价格区间位置 | 2 | range_position_10/20 |
| 30 | 时间编码 | 12 | hour/minute/weekday/month × sin/cos + raw |

## 股票池（默认10只）

| 代码 | 名称 | 板块 |
|------|------|------|
| 600436 | 片仔癀 | 沪主板 |
| 300750 | 宁德时代 | 创业板 |
| 002475 | 立讯精密 | 中小板 |
| 000568 | 泸州老窖 | 深主板 |
| 000538 | 云南白药 | 深主板 |
| 000338 | 潍柴动力 | 深主板 |
| 600031 | 三一重工 | 沪主板 |
| 600111 | 北方稀土 | 沪主板 |
| 002415 | 海康威视 | 中小板 |
| 000858 | 五粮液 | 深主板 |
