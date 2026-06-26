import pandas as pd
import numpy as np


def get_feature_metadata():
    """Return Chinese names, engineering logic, and category for each feature."""
    metadata = {}

    def add(name, chinese_name, logic, category):
        metadata[name] = {
            "chinese_name": chinese_name,
            "logic": logic,
            "category": category,
        }

    for p in [1, 2, 3, 5, 10, 20]:
        add(f"return_{p}", f"{p}日收益率", f"close.pct_change({p})", "价格收益")
    for p in [5, 10, 20, 50, 100]:
        add(f"ma_ratio_{p}", f"收盘价相对{p}日均线偏离率", f"close / MA{p} - 1", "均线偏离")
    for p in [5, 10, 20, 50]:
        add(f"ema_ratio_{p}", f"收盘价相对{p}日EMA偏离率", f"close / EMA{p} - 1", "EMA偏离")

    add("ma_cross_5_10", "5日与10日均线差", "(MA5 - MA10) / close", "均线交叉")
    add("ma_cross_5_20", "5日与20日均线差", "(MA5 - MA20) / close", "均线交叉")
    add("ma_cross_10_20", "10日与20日均线差", "(MA10 - MA20) / close", "均线交叉")
    add("ma_cross_10_50", "10日与50日均线差", "(MA10 - MA50) / close", "均线交叉")

    for p in [6, 14, 24]:
        add(f"rsi_{p}", f"RSI({p})", f"{p}期涨跌幅构造 RSI", "RSI")

    add("macd_norm", "MACD线归一化", "(EMA12 - EMA26) / close", "MACD")
    add("macd_signal_norm", "MACD信号线归一化", "MACD signal / close", "MACD")
    add("macd_hist_norm", "MACD柱体归一化", "(MACD - Signal) / close", "MACD")

    for p in [9, 14]:
        add(f"kdj_k_{p}", f"KDJ-K({p})", f"{p}期 RSV 的平滑 K 值", "KDJ")
        add(f"kdj_d_{p}", f"KDJ-D({p})", "K 值二次平滑得到 D 值", "KDJ")
        add(f"kdj_j_{p}", f"KDJ-J({p})", "3 * K - 2 * D", "KDJ")

    for p in [14, 28]:
        add(f"williams_r_{p}", f"威廉指标%R({p})", f"-{p}期区间内收盘位置", "威廉指标")
    for p in [14, 20]:
        add(f"cci_{p}", f"顺势指标CCI({p})", f"({p}期典型价格 - 均值) / 平均绝对偏差", "CCI")

    add("bb_width", "布林带宽度", "(布林上轨 - 布林下轨) / 布林中轨", "布林带")
    add("bb_position", "布林带位置", "(close - 下轨) / (上轨 - 下轨)", "布林带")

    add("volume_ratio_5", "5日量比", "volume / volume_ma5", "成交量")
    add("volume_ratio_10", "10日量比", "volume / volume_ma10", "成交量")
    add("volume_ratio_20", "20日量比", "volume / volume_ma20", "成交量")
    add("volume_change", "单日成交量变化率", "volume.pct_change()", "成交量")
    add("volume_change_5", "5日成交量变化率", "volume.pct_change(5)", "成交量")
    add("obv_ratio_5", "OBV相对5日均值偏离", "(OBV - OBV_MA5) / |OBV_MA5|", "OBV")
    add("obv_ratio_20", "OBV相对20日均值偏离", "(OBV - OBV_MA20) / |OBV_MA20|", "OBV")
    add("mfi_14", "资金流量指标MFI(14)", "14期正负资金流比构造 MFI", "MFI")
    add("vwap_dev", "VWAP偏离率", "(close - VWAP20) / VWAP20", "VWAP")

    for p in [5, 10, 20]:
        add(f"volatility_{p}", f"{p}日收益波动率", f"return.rolling({p}).std()", "波动率")
    add("volatility_ratio_5_20", "短长波动率比", "volatility_5 / volatility_20", "波动率")

    add("high_low_ratio", "日内振幅比", "(high - low) / close", "K线形态")
    add("close_open_ratio", "开收盘涨跌幅", "(close - open) / open", "K线形态")
    add("upper_shadow", "上影线比例", "(high - max(open, close)) / close", "K线形态")
    add("lower_shadow", "下影线比例", "(min(open, close) - low) / close", "K线形态")
    add("body_ratio", "实体占比", "|close - open| / (high - low)", "K线形态")

    for p in [7, 14]:
        add(f"atr_{p}", f"ATR({p})归一化", f"TR 的 {p}期均值 / close", "ATR")
    for p in [5, 10, 20]:
        add(f"momentum_{p}", f"{p}日动量", f"close / close.shift({p}) - 1", "动量")
    add("return_accel", "收益加速度", "当日收益率的一阶差分", "动量")

    for p in [10, 20]:
        add(f"skew_{p}", f"{p}日收益偏度", f"return.rolling({p}).skew()", "分布统计")
        add(f"kurtosis_{p}", f"{p}日收益峰度", f"return.rolling({p}).kurt()", "分布统计")

    add("consec_count", "连续涨跌计数", "同方向连续涨跌段内的累计长度", "连续性")
    add("consec_dir", "连续涨跌方向", "sign(close.diff())", "连续性")
    add("consec_signed", "带方向连续计数", "consec_count * consec_dir", "连续性")

    for p in [10, 20, 50]:
        add(f"dist_high_{p}", f"距{p}日高点距离", f"(close - rolling_high_{p}) / close", "区间位置")
        add(f"dist_low_{p}", f"距{p}日低点距离", f"(close - rolling_low_{p}) / close", "区间位置")
    for lag in [1, 2, 3, 5]:
        add(f"return_lag_{lag}", f"滞后{lag}日收益率", f"return.shift({lag})", "滞后收益")
    for p in [10, 20]:
        add(f"vol_price_corr_{p}", f"{p}日量价相关系数", f"close.rolling({p}).corr(volume)", "量价关系")

    add("pivot_dev", "枢轴点偏离率", "(close - Pivot) / Pivot", "枢轴点")
    add("pivot_r1_dev", "相对阻力位R1偏离率", "(close - R1) / close", "枢轴点")
    add("pivot_s1_dev", "相对支撑位S1偏离率", "(close - S1) / close", "枢轴点")
    add("adx_14", "ADX趋势强度", "14期方向指标差值平滑", "ADX")
    add("plus_di_14", "+DI(14)", "14期正方向指标", "ADX")
    add("minus_di_14", "-DI(14)", "14期负方向指标", "ADX")
    add("trix", "TRIX三重指数平滑动量", "EMA三次平滑后的一阶收益率", "TRIX")
    add("chaikin_vol", "Chaikin波动率", "(高低价差EMA10).pct_change(10)", "Chaikin波动率")

    for p in [10, 20]:
        add(f"range_position_{p}", f"{p}日区间位置", f"(close - rolling_low_{p}) / (rolling_high_{p} - rolling_low_{p})", "区间位置")

    add("hour", "小时", "datetime.dt.hour", "时间编码")
    add("minute", "分钟", "datetime.dt.minute", "时间编码")
    add("weekday", "星期序号", "datetime.dt.weekday", "时间编码")
    add("month", "月份", "datetime.dt.month", "时间编码")
    add("hour_sin", "小时正弦编码", "sin(2π * hour / 24)", "时间编码")
    add("hour_cos", "小时余弦编码", "cos(2π * hour / 24)", "时间编码")
    add("minute_sin", "分钟正弦编码", "sin(2π * minute / 60)", "时间编码")
    add("minute_cos", "分钟余弦编码", "cos(2π * minute / 60)", "时间编码")
    add("weekday_sin", "星期正弦编码", "sin(2π * weekday / 5)", "时间编码")
    add("weekday_cos", "星期余弦编码", "cos(2π * weekday / 5)", "时间编码")
    add("month_sin", "月份正弦编码", "sin(2π * month / 12)", "时间编码")
    add("month_cos", "月份余弦编码", "cos(2π * month / 12)", "时间编码")

    return metadata


def add_technical_features(df):
    """Calculate technical indicator features from OHLCV data.

    Expects columns: open, close, high, low, volume, datetime/date
    """
    df = df.copy()
    close = df["close"].astype(float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    volume = df["volume"].astype(float)
    open_price = df["open"].astype(float)
    returns = close.pct_change()

    # ======== 1. Price Returns ========
    for p in [1, 2, 3, 5, 10, 20]:
        df[f"return_{p}"] = close.pct_change(p)

    # ======== 2. Moving Average Ratios ========
    for p in [5, 10, 20, 50, 100]:
        ma = close.rolling(p).mean()
        df[f"ma_ratio_{p}"] = close / ma - 1

    # ======== 3. EMA Ratios ========
    for p in [5, 10, 20, 50]:
        ema = close.ewm(span=p, adjust=False).mean()
        df[f"ema_ratio_{p}"] = close / ema - 1

    # ======== 4. MA Cross Signals ========
    ma5 = close.rolling(5).mean()
    ma10 = close.rolling(10).mean()
    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()
    df["ma_cross_5_10"] = (ma5 - ma10) / (close + 1e-10)
    df["ma_cross_5_20"] = (ma5 - ma20) / (close + 1e-10)
    df["ma_cross_10_20"] = (ma10 - ma20) / (close + 1e-10)
    df["ma_cross_10_50"] = (ma10 - ma50) / (close + 1e-10)

    # ======== 5. RSI ========
    for p in [6, 14, 24]:
        delta = close.diff()
        gain = delta.where(delta > 0, 0.0).rolling(p).mean()
        loss = (-delta.where(delta < 0, 0.0)).rolling(p).mean()
        rs = gain / (loss + 1e-10)
        df[f"rsi_{p}"] = 100 - (100 / (1 + rs))

    # ======== 6. MACD ========
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    macd_signal = macd_line.ewm(span=9, adjust=False).mean()
    macd_hist = macd_line - macd_signal
    df["macd_norm"] = macd_line / close
    df["macd_signal_norm"] = macd_signal / close
    df["macd_hist_norm"] = macd_hist / close

    # ======== 7. KDJ ========
    for p in [9, 14]:
        low_n = low.rolling(p).min()
        high_n = high.rolling(p).max()
        rsv = (close - low_n) / (high_n - low_n + 1e-10) * 100
        k = rsv.ewm(com=2, adjust=False).mean()
        d = k.ewm(com=2, adjust=False).mean()
        j = 3 * k - 2 * d
        df[f"kdj_k_{p}"] = k
        df[f"kdj_d_{p}"] = d
        df[f"kdj_j_{p}"] = j

    # ======== 8. Williams %R ========
    for p in [14, 28]:
        high_n = high.rolling(p).max()
        low_n = low.rolling(p).min()
        df[f"williams_r_{p}"] = (high_n - close) / (high_n - low_n + 1e-10) * -100

    # ======== 9. CCI ========
    tp = (close + high + low) / 3.0
    for p in [14, 20]:
        tp_ma = tp.rolling(p).mean()
        tp_md = tp.rolling(p).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
        df[f"cci_{p}"] = (tp - tp_ma) / (0.015 * tp_md + 1e-10)

    # ======== 10. Bollinger Bands ========
    bb_ma = close.rolling(20).mean()
    bb_std = close.rolling(20).std()
    bb_upper = bb_ma + 2 * bb_std
    bb_lower = bb_ma - 2 * bb_std
    df["bb_width"] = (bb_upper - bb_lower) / (bb_ma + 1e-10)
    df["bb_position"] = (close - bb_lower) / (bb_upper - bb_lower + 1e-10)

    # ======== 11. Volume Features ========
    vol_ma5 = volume.rolling(5).mean()
    vol_ma10 = volume.rolling(10).mean()
    vol_ma20 = volume.rolling(20).mean()
    df["volume_ratio_5"] = volume / (vol_ma5 + 1e-10)
    df["volume_ratio_10"] = volume / (vol_ma10 + 1e-10)
    df["volume_ratio_20"] = volume / (vol_ma20 + 1e-10)
    df["volume_change"] = volume.pct_change()
    df["volume_change_5"] = volume.pct_change(5)

    # ======== 12. OBV (On-Balance Volume) ========
    obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
    obv_ma5 = obv.rolling(5).mean()
    obv_ma20 = obv.rolling(20).mean()
    df["obv_ratio_5"] = (obv - obv_ma5) / (obv_ma5.abs() + 1e-10)
    df["obv_ratio_20"] = (obv - obv_ma20) / (obv_ma20.abs() + 1e-10)

    # ======== 13. MFI (Money Flow Index) ========
    mf = tp * volume
    mf_pos = mf.where(tp.diff() > 0, 0.0)
    mf_neg = mf.where(tp.diff() <= 0, 0.0)
    for p in [14]:
        mf_ratio = mf_pos.rolling(p).sum() / (mf_neg.rolling(p).sum() + 1e-10)
        df[f"mfi_{p}"] = 100 - (100 / (1 + mf_ratio))

    # ======== 14. VWAP deviation ========
    cum_vol = volume.rolling(20).sum()
    cum_tp_vol = (tp * volume).rolling(20).sum()
    vwap = cum_tp_vol / (cum_vol + 1e-10)
    df["vwap_dev"] = (close - vwap) / (vwap + 1e-10)

    # ======== 15. Volatility ========
    for p in [5, 10, 20]:
        df[f"volatility_{p}"] = returns.rolling(p).std()
    # Volatility ratio (short/long)
    df["volatility_ratio_5_20"] = (
        returns.rolling(5).std() / (returns.rolling(20).std() + 1e-10)
    )

    # ======== 16. Price Range ========
    df["high_low_ratio"] = (high - low) / (close + 1e-10)
    df["close_open_ratio"] = (close - open_price) / (open_price + 1e-10)
    df["upper_shadow"] = (high - np.maximum(close, open_price)) / (close + 1e-10)
    df["lower_shadow"] = (np.minimum(close, open_price) - low) / (close + 1e-10)
    df["body_ratio"] = (close - open_price).abs() / (high - low + 1e-10)

    # ======== 17. ATR ========
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    for p in [7, 14]:
        df[f"atr_{p}"] = tr.rolling(p).mean() / (close + 1e-10)

    # ======== 18. Momentum / ROC ========
    for p in [5, 10, 20]:
        df[f"momentum_{p}"] = close / close.shift(p) - 1

    # ======== 19. Price acceleration ========
    df["return_accel"] = returns.diff()

    # ======== 20. Rolling skewness & kurtosis ========
    for p in [10, 20]:
        df[f"skew_{p}"] = returns.rolling(p).skew()
        df[f"kurtosis_{p}"] = returns.rolling(p).kurt()

    # ======== 21. Consecutive up/down count ========
    direction = np.sign(close.diff())
    groups = (direction != direction.shift()).cumsum()
    df["consec_count"] = direction.groupby(groups).cumcount() + 1
    df["consec_dir"] = direction  # +1 or -1
    df["consec_signed"] = df["consec_count"] * df["consec_dir"]

    # ======== 22. Distance from N-period high/low ========
    for p in [10, 20, 50]:
        df[f"dist_high_{p}"] = (close - high.rolling(p).max()) / (close + 1e-10)
        df[f"dist_low_{p}"] = (close - low.rolling(p).min()) / (close + 1e-10)

    # ======== 23. Lag features (return lags) ========
    for lag in [1, 2, 3, 5]:
        df[f"return_lag_{lag}"] = returns.shift(lag)

    # ======== 24. Volume-price correlation ========
    for p in [10, 20]:
        df[f"vol_price_corr_{p}"] = close.rolling(p).corr(volume)

    # ======== 25. Pivot points ========
    pivot = (high.shift(1) + low.shift(1) + close.shift(1)) / 3
    df["pivot_dev"] = (close - pivot) / (pivot + 1e-10)
    r1 = 2 * pivot - low.shift(1)
    s1 = 2 * pivot - high.shift(1)
    df["pivot_r1_dev"] = (close - r1) / (close + 1e-10)
    df["pivot_s1_dev"] = (close - s1) / (close + 1e-10)

    # ======== 26. Average Directional Index (ADX approx) ========
    plus_dm = high.diff()
    minus_dm = -low.diff()
    plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
    minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)
    atr14 = tr.rolling(14).mean()
    plus_di = 100 * plus_dm.rolling(14).mean() / (atr14 + 1e-10)
    minus_di = 100 * minus_dm.rolling(14).mean() / (atr14 + 1e-10)
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di + 1e-10)
    df["adx_14"] = dx.rolling(14).mean()
    df["plus_di_14"] = plus_di
    df["minus_di_14"] = minus_di

    # ======== 27. TRIX ========
    ema1 = close.ewm(span=12, adjust=False).mean()
    ema2 = ema1.ewm(span=12, adjust=False).mean()
    ema3 = ema2.ewm(span=12, adjust=False).mean()
    df["trix"] = ema3.pct_change() * 100

    # ======== 28. Chaikin Volatility ========
    hl_ema = (high - low).ewm(span=10, adjust=False).mean()
    df["chaikin_vol"] = hl_ema.pct_change(10)

    # ======== 29. Price position in range ========
    for p in [10, 20]:
        pmax = high.rolling(p).max()
        pmin = low.rolling(p).min()
        df[f"range_position_{p}"] = (close - pmin) / (pmax - pmin + 1e-10)

    # ======== 30. Time Features ========
    df = df.copy()
    dt_col = None
    if "datetime" in df.columns:
        dt_col = "datetime"
    elif "date" in df.columns:
        dt_col = "date"
    if dt_col:
        dt = pd.to_datetime(df[dt_col])
        df["hour"] = dt.dt.hour
        df["minute"] = dt.dt.minute
        df["weekday"] = dt.dt.weekday
        df["month"] = dt.dt.month
        # Cyclical encoding
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
        df["minute_sin"] = np.sin(2 * np.pi * df["minute"] / 60)
        df["minute_cos"] = np.cos(2 * np.pi * df["minute"] / 60)
        df["weekday_sin"] = np.sin(2 * np.pi * df["weekday"] / 5)
        df["weekday_cos"] = np.cos(2 * np.pi * df["weekday"] / 5)
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    return df


def get_all_feature_columns():
    """Return the full list of feature column names."""
    cols = []
    # Price returns
    for p in [1, 2, 3, 5, 10, 20]:
        cols.append(f"return_{p}")
    # MA ratios
    for p in [5, 10, 20, 50, 100]:
        cols.append(f"ma_ratio_{p}")
    # EMA ratios
    for p in [5, 10, 20, 50]:
        cols.append(f"ema_ratio_{p}")
    # MA cross
    cols.extend(["ma_cross_5_10", "ma_cross_5_20", "ma_cross_10_20", "ma_cross_10_50"])
    # RSI
    for p in [6, 14, 24]:
        cols.append(f"rsi_{p}")
    # MACD
    cols.extend(["macd_norm", "macd_signal_norm", "macd_hist_norm"])
    # KDJ
    for p in [9, 14]:
        cols.extend([f"kdj_k_{p}", f"kdj_d_{p}", f"kdj_j_{p}"])
    # Williams %R
    for p in [14, 28]:
        cols.append(f"williams_r_{p}")
    # CCI
    for p in [14, 20]:
        cols.append(f"cci_{p}")
    # BB
    cols.extend(["bb_width", "bb_position"])
    # Volume
    cols.extend(["volume_ratio_5", "volume_ratio_10", "volume_ratio_20",
                 "volume_change", "volume_change_5"])
    # OBV
    cols.extend(["obv_ratio_5", "obv_ratio_20"])
    # MFI
    cols.append("mfi_14")
    # VWAP
    cols.append("vwap_dev")
    # Volatility
    for p in [5, 10, 20]:
        cols.append(f"volatility_{p}")
    cols.append("volatility_ratio_5_20")
    # Price range
    cols.extend(["high_low_ratio", "close_open_ratio",
                 "upper_shadow", "lower_shadow", "body_ratio"])
    # ATR
    for p in [7, 14]:
        cols.append(f"atr_{p}")
    # Momentum
    for p in [5, 10, 20]:
        cols.append(f"momentum_{p}")
    # Acceleration
    cols.append("return_accel")
    # Skew & kurtosis
    for p in [10, 20]:
        cols.extend([f"skew_{p}", f"kurtosis_{p}"])
    # Consecutive
    cols.extend(["consec_count", "consec_dir", "consec_signed"])
    # Distance from high/low
    for p in [10, 20, 50]:
        cols.extend([f"dist_high_{p}", f"dist_low_{p}"])
    # Return lags
    for lag in [1, 2, 3, 5]:
        cols.append(f"return_lag_{lag}")
    # Volume-price correlation
    for p in [10, 20]:
        cols.append(f"vol_price_corr_{p}")
    # Pivot
    cols.extend(["pivot_dev", "pivot_r1_dev", "pivot_s1_dev"])
    # ADX
    cols.extend(["adx_14", "plus_di_14", "minus_di_14"])
    # TRIX
    cols.append("trix")
    # Chaikin Volatility
    cols.append("chaikin_vol")
    # Range position
    for p in [10, 20]:
        cols.append(f"range_position_{p}")
    # Time
    cols.extend([
        "hour", "minute", "weekday", "month",
        "hour_sin", "hour_cos", "minute_sin", "minute_cos",
        "weekday_sin", "weekday_cos", "month_sin", "month_cos",
    ])
    return cols


def create_label(df):
    """Create binary label: 1 if next period close > current close, else 0."""
    df = df.copy()
    df["label"] = (df["close"].shift(-1) > df["close"]).astype(int)
    return df
