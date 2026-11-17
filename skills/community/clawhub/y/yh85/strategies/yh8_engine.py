#!/usr/bin/env python3
"""YH8.5 双引擎信号生成器 — Playbook路由
===================================================
趋势(ATR%>60%):
  ST(10,3) Pure → 全趋势池币种 (双引擎终局)
震荡(ATR%≤60%):
  BB(20,2) 均值回归 → 全震池币种 (纯信号直通)

2026-07-03 v1: 初始 YH8 引擎
2026-07-09 v2: 纯规则化信号直通
2026-07-10 v3: EMA50MR 2.0% + EMA7×25交叉
2026-07-10 v4: Playbook路由 — ST Pure + BB20
2026-08-05 v3.63: ST+Gann代码全量删除
"""
import os, sys, time
import numpy as np
DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(DIR))
from strategies.playbook_manager import get_playbook
from market_regime import pd_ema  # 07-21: 趋势跟随入场EMA计算

# ═══════════════ 全局默认参数 (被Playbook覆盖) ═══════════════
ATR_PERCENTILE_TRENDING = 70  # v3.62 (方案B): 60→70, 扩大震荡分类让BB20有空间产出信号
ATR_LOOKBACK = 1440  # 30m bars, ~30天
RSI_OVERSOLD_BLOCK = 20    # v3.54: RSI<20禁止做空 (回测6L/-18.36U vs 5W/+4.19U)
# RSI_OVERBOUGHT_BLOCK = 70  # v3.54: 已禁用, RSI>70做多回测为正期望+10.52U
# ── 2026-09-03: BB20 收盘确认 — 盘中瞬时碰轨假信号挡掉 ──
# 回测(62天×10币做空端): 盘中口径386笔42.7%/-1.5% vs 收盘口径312笔52.6%/+106%
# 分半验证: 前31天+58.5% / 后31天+47.5%, 方向一致
BB20_CLOSE_CONFIRM = True
# ── 2026-09-10: BB20做多 4h MTF 共识 — 4h空头趋势不抄底 (多模型共识思路) ──
# 回测(62天×10币做多端): 基线46%/累计+16.5%/回撤-19.5% vs 4hST共识 51.1%/+27%/-12%
# 分半验证: 前31天(46%→50%) / 后31天(42%→47%, 累计-1.5%→+7.5%) 两窗一致(非过拟合)
# 对比: 做空端MTF=风控旋钮(提质量降总量), ST端MTF=无效(趋势策略无需滞后确认)
BB20_LONG_MTF_CONSENSUS = True
# ── 2026-09-10: BB20做空 4h EMA 共识 — 4h多头排列不追空 (反弹期逆势做空拦截) ──
# 回测(62天×10币做空端, 收盘口径): 基线293笔/51.2%/+85.5%/每笔+0.292% vs 4hEMA过滤 81笔/60.5%/+50%/每笔+0.617%
# 分段验证: 反弹期(后段)基线48.3%胜率(负期望) → 过滤后51.7%(微正); 每笔质量翻倍
# 定位: 风控旋钮(提质量降总量), 对症「反弹行情逆势做空」当前实盘痛点(最近7天-10.12U)
#
# ── 2026-09-12 交叉回测证伪(30币×62天×市场宽度×4hEMA方向) — 该过滤器方向错误, 关闭 ──
# 关键: 4h多头排列做空信号按市场宽度分裂为正负两群:
#   上涨市(up_block+up_alert) 4h多头排列: 159笔 63.5%胜率 累计+115% 每笔+0.723% ← 最强alpha, 被误杀
#   下跌市(block/red_alert)   4h多头排列:  67笔 34.3%胜率 累计-23.5% 每笔-0.35% ← 真负期望, 该拦
# 但实盘 force_trending 在 block/red_alert 下已强制路由到ST(不产BB20做空信号),
# 故下跌市负期望场景在实盘天然不出现 → 此过滤器只剩「误杀上涨市alpha」一个作用。
# 结论: 关闭 (证伪即砍)。分半验证上涨市多头排列象限 前63.3%/后63.7% 稳定非过拟合。
BB20_SHORT_MTF_CONSENSUS = False
EMA_MR_PERIOD = 50
EMA_MR_DEVIATION = 0.02

# ═══════════════ ADX 引擎路由 (2026-08-19 幻方阿尔法因子提取) ═══════════════
# ADX 趋势强度维度：ADX>25 强趋势→ST；ADX<20 无趋势→BB20；20-25 过渡区交还 ATR/动量双维度
# 默认关闭——需先回测对比确认有效后，由用户拍板开启（不自动替换路由逻辑）
# 2026-08-19 用户拍板启用：30天14币回测胜率+3.3% / PnL+17.7% / 回撤-22.9%，全指标正向
ADX_ROUTING_ENABLED = True
ADX_TREND_THRESHOLD = 25.0   # ADX>25 → trending
ADX_RANGE_THRESHOLD = 20.0   # ADX<20 → ranging

# ═══════════════ ACF/PACF 自相关因子 (2026-08-27) ═══════════════
# 时序记忆性维度过滤 (与价格/量价/数据类因子正交):
#   ACF(1) > 阈值  = 价格正自相关 → 趋势延续(非反转后追入)
#   PACF(2) < 上限 = 二阶偏自相关不过热 → 非直线冲顶(避免追高)
# 回测依据 (60/90天×8 ST币, 双窗口交叉验证):
#   组合 ACF1>0.05 & PACF2<0 → 胜率 36-38%→51%+ / 盈亏比 1.15→2.2 / 回撤 73-88%→16-18%
# 默认关闭——需用户拍板开启 (不自动替换信号链)
ACF_PACF_FILTER_DEFAULT = False    # 总开关(默认关)
ACF1_THRESHOLD_DEFAULT = 0.05      # ACF(1) 下限
PACF2_MAX_DEFAULT = 0.0            # PACF(2) 上限(<0 = 不过热)
ACF_PACF_LOOKBACK = 20             # 收益率窗口bar数(30m)


def ema(a, s):
    a2 = 2/(s+1); o = np.zeros(len(a)); o[0] = a[0]
    for i in range(1, len(a)): o[i] = a2*a[i] + (1-a2)*o[i-1]
    return o


def _weighted_std(values, decay_bars=5, decay_weight=1.5):
    """时间衰减加权标准差 — P1: BB20震荡用，最近N根K线权重×W
    - 最远的 (window - decay_bars) 根K线权重 = 1.0
    - 最近 decay_bars 根K线权重从 1.0 线性递增到 decay_weight
    - 返回 (加权均值, 加权标准差)
    """
    n = len(values)
    if n <= decay_bars:
        # 窗口太小, 全部等权重
        return np.mean(values), np.std(values)
    weights = np.ones(n)
    for i in range(decay_bars):
        idx = n - decay_bars + i
        weights[idx] = 1.0 + (decay_weight - 1.0) * (i + 1) / decay_bars  # 线性递增
    wm = np.average(values, weights=weights)
    wvar = np.average((values - wm) ** 2, weights=weights)
    return wm, np.sqrt(wvar)


def _compute_atr_series(h, l, c, p=14):
    n = len(c); tr = np.zeros(n)
    tr[0] = h[0] - l[0]
    for i in range(1, n):
        tr[i] = max(h[i]-l[i], abs(h[i]-c[i-1]), abs(l[i]-c[i-1]))
    a = 2/(p+1); atr = np.zeros(n); atr[0] = tr[0]
    for i in range(1, n): atr[i] = a*tr[i] + (1-a)*atr[i-1]
    return atr


def _compute_rsi(c, period=14):
    """RSI(14)"""
    n = len(c)
    if n < period + 1:
        return 50.0
    deltas = np.diff(c[-(period+1):])
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)
    if avg_loss < 1e-10:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - 100.0 / (1.0 + rs)


def atr_percentile(h, l, c, period=14, lookback=ATR_LOOKBACK):
    """ATR百分位 - 当前ATR在历史中的位置"""
    atr = _compute_atr_series(h, l, c, period)
    now = atr[-1]
    lb = min(lookback, len(atr))
    hist = atr[-lb:]
    return (np.sum(hist < now) / lb) * 100


def _compute_adx(h, l, c, period=14):
    """Wilder ADX (Average Directional Index) — 趋势强度指标 (2026-08-19 幻方阿尔法因子)
    返回与输入等长的 adx 序列，末值即当前 ADX。
    ADX 只度量趋势强度、不区分方向；>25 强趋势，<20 无趋势/震荡，20-25 过渡。
    """
    n = len(c)
    adx = np.zeros(n)
    if n < period * 2 + 1:
        return adx

    tr = np.zeros(n)
    plus_dm = np.zeros(n)
    minus_dm = np.zeros(n)
    for i in range(1, n):
        up = h[i] - h[i - 1]
        down = l[i - 1] - l[i]
        tr[i] = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
        plus_dm[i] = up if (up > down and up > 0) else 0.0
        minus_dm[i] = down if (down > up and down > 0) else 0.0

    # Wilder 平滑（初始 = 前 period 个之和）
    tr_s = np.zeros(n); pdm_s = np.zeros(n); mdm_s = np.zeros(n)
    tr_s[period] = np.sum(tr[1:period + 1])
    pdm_s[period] = np.sum(plus_dm[1:period + 1])
    mdm_s[period] = np.sum(minus_dm[1:period + 1])
    for i in range(period + 1, n):
        tr_s[i] = tr_s[i - 1] - tr_s[i - 1] / period + tr[i]
        pdm_s[i] = pdm_s[i - 1] - pdm_s[i - 1] / period + plus_dm[i]
        mdm_s[i] = mdm_s[i - 1] - mdm_s[i - 1] / period + minus_dm[i]

    pdi = np.where(tr_s > 0, 100.0 * pdm_s / np.where(tr_s > 0, tr_s, 1.0), 0.0)
    mdi = np.where(tr_s > 0, 100.0 * mdm_s / np.where(tr_s > 0, tr_s, 1.0), 0.0)

    denom = pdi + mdi
    dx = np.where(denom > 0, 100.0 * np.abs(pdi - mdi) / np.where(denom > 0, denom, 1.0), 0.0)

    # ADX = Wilder 平滑 DX
    adx[period * 2] = np.mean(dx[period + 1:period * 2 + 1])
    for i in range(period * 2 + 1, n):
        adx[i] = (adx[i - 1] * (period - 1) + dx[i]) / period

    return adx


def classify_market(df_30m):
    """市场分型 (2026-08-19: 新增 ADX 趋势强度维度)
    
    三维度判定 (ADX 开关开启时):
      维度0: ADX 趋势强度 (幻方阿尔法因子) — ADX>25 强趋势→trending, ADX<20 无趋势→ranging
      维度1: ATR百分位 — 高波动趋势
      维度2: 价格动量 — 低波趋势
      任一维度触发 → trending, 否则 → ranging
    """
    h = df_30m['high'].values.astype(np.float64)
    l = df_30m['low'].values.astype(np.float64)
    c = df_30m['close'].values.astype(np.float64)
    
    atr_pct = atr_percentile(h, l, c)
    
    # 维度0: ADX 趋势强度 (2026-08-19 幻方阿尔法因子提取, 默认关闭待回测)
    if ADX_ROUTING_ENABLED:
        adx = _compute_adx(h, l, c, 14)[-1]
        if adx > ADX_TREND_THRESHOLD:
            return 'trending', atr_pct
        if adx < ADX_RANGE_THRESHOLD:
            return 'ranging', atr_pct
        # 20-25 过渡区 → 交还 ATR/动量双维度
    
    # 维度1: ATR百分位 (高波动趋势)
    if atr_pct > ATR_PERCENTILE_TRENDING:
        return 'trending', atr_pct
    
    # 维度2: 价格动量 (低波动趋势) — 2026-07-21 新增
    trend_strength, direction = _momentum_score(c)
    MOMENTUM_TREND_THRESHOLD = 0.45  # v3.62 (方案B): 0.35→0.45, 中等动量仍判震荡, BB20可介入
    if trend_strength > MOMENTUM_TREND_THRESHOLD:
        return 'trending', atr_pct  # 维持原ATR%用于日志, 但状态修正为trending
    
    return 'ranging', atr_pct


def _momentum_score(c):
    """
    价格动量评分 (0~1) + 方向 (+1=多头, -1=空头)
    
    三因子等权:
      a) 趋势斜率: 线性回归20bar斜率/价格 (0~0.35)
      b) EMA对齐: EMA50相对EMA144方向 + 价格偏移动量 (0~0.35)
      c) 方向一致性: 近12bar中同向占比 (0~0.30)
    """
    n = len(c)
    if n < 60:
        return 0.0, 0
    
    price = c[-1]
    
    # a) 线性回归斜率 (最后24bar = 12小时)
    lookback = min(24, n)
    x = np.arange(lookback, dtype=np.float64)
    y = c[-lookback:]
    slope, _ = np.polyfit(x, y, 1)
    slope_pct = (slope * lookback) / price
    slope_score = min(abs(slope_pct) / 0.025, 1.0) * 0.35  # 2.5%变动=满分 (降低以适应缓涨)
    slope_dir = 1 if slope > 0 else -1
    
    # b) EMA50 vs EMA144 对齐 + 价格偏离动量
    ema50 = pd_ema(c, 50)
    ema144 = pd_ema(c, 144)
    ema50_slope = (ema50[-1] - ema50[-6]) / max(ema50[-6], 1e-8)
    
    ema_score = 0.0
    ema_dir = 0
    ema_aligned = False  # EMA完整对齐标记
    if ema50[-1] > ema144[-1] and ema50_slope > 0:
        ema_dir = 1
        ema_aligned = True
        ema_score = min(abs(ema50_slope) / 0.005, 1.0) * 0.25  # 0.5%坡度=满分
        if price > ema50[-1]:
            ema_score += 0.10
    elif ema50[-1] < ema144[-1] and ema50_slope < 0:
        ema_dir = -1
        ema_aligned = True
        ema_score = min(abs(ema50_slope) / 0.005, 1.0) * 0.25
        if price < ema50[-1]:
            ema_score += 0.10
    else:
        ema_dir = 1 if ema50_slope > 0 else (-1 if ema50_slope < 0 else 0)
    
    # c) 方向一致性: 近12bar中同向k线占比
    consistency_lookback = 12
    up_bars = sum(1 for i in range(1, consistency_lookback + 1)
                  if c[-(i)] > c[-(i+1)])
    max_dir_bars = max(up_bars, consistency_lookback - up_bars)
    consistency_score = (max_dir_bars / consistency_lookback - 0.5) * 2 * 0.30
    consistency_score = max(consistency_score, 0)
    consistency_dir = 1 if up_bars >= (consistency_lookback - up_bars) else -1
    
    # d) 自动趋势认定: EMA对齐 + 60%以上同向k线 + 价格在EMA50同侧
    auto_trend = False
    if ema_aligned:
        same_side = (ema_dir == 1 and price > ema50[-1]) or (ema_dir == -1 and price < ema50[-1])
        if same_side and max_dir_bars >= consistency_lookback * 0.6:
            auto_trend = True
    
    # 综合评分
    total_score = slope_score + ema_score + consistency_score
    if auto_trend:
        total_score = max(total_score, 0.40)  # 自动趋势保证超过阈值
    
    # 方向判定
    dirs = [(slope_dir, 0.35), (ema_dir, 0.35), (consistency_dir, 0.30)]
    long_weight = sum(w for d, w in dirs if d == 1)
    short_weight = sum(w for d, w in dirs if d == -1)
    if long_weight > 0.5:
        direction = 1
    elif short_weight > 0.5:
        direction = -1
    else:
        direction = 0
    
    return total_score, direction


# ═══════════════ 纯ST(10,3) 无Gann 趋势 ═══════════════

def _supertrend(h, l, c, period=10, mult=3.0):
    """计算SuperTrend序列 → trend, fu, fl"""
    n = len(c); atrv = _compute_atr_series(h, l, c, period)
    mid = (h + l) / 2
    upper = mid + mult * atrv; lower = mid - mult * atrv
    fu = np.zeros(n); fl = np.zeros(n); trend = np.zeros(n)
    fu[period] = upper[period]; fl[period] = lower[period]
    trend[period] = 1  # start bullish
    for i in range(period + 1, n):
        fu[i] = upper[i] if (upper[i] < fu[i-1] or c[i-1] > fu[i-1]) else fu[i-1]
        fl[i] = lower[i] if (lower[i] > fl[i-1] or c[i-1] < fl[i-1]) else fl[i-1]
        if trend[i-1] <= 0 and c[i] > fu[i-1]:
            trend[i] = 1
        elif trend[i-1] >= 0 and c[i] < fl[i-1]:
            trend[i] = -1
        else:
            trend[i] = trend[i-1]
    return trend, fu, fl


# ═══════════════ ACF/PACF 计算 (Levinson-Durbin) ═══════════════

def _acf(series, k):
    """lag-k 自相关系数 ρ(k) = corr(x_t, x_{t-k})"""
    series = np.asarray(series, dtype='float64')
    n = len(series)
    if n <= k:
        return 0.0
    m = series.mean()
    var = np.sum((series - m) ** 2)
    if var < 1e-14:
        return 0.0
    return np.sum((series[:n - k] - m) * (series[k:] - m)) / var


def _pacf(series, maxlag=3):
    """返回 lag 1..maxlag 的偏自相关系数列表 (Levinson-Durbin 递推)
    注: PACF(1) ≡ ACF(1) 恒等, 偏自相关增量从 PACF(2) 起。
    """
    series = np.asarray(series, dtype='float64')
    ac = [_acf(series, k) for k in range(maxlag + 1)]  # ac[0]=1
    pacfs = []
    phi = [ac[1]]
    pacfs.append(phi[0])
    for p in range(2, maxlag + 1):
        num = ac[p] - sum(phi[j] * ac[p - 1 - j] for j in range(p - 1))
        den = 1.0 - sum(phi[j] * ac[j + 1] for j in range(p - 1))
        phipp = num / den if abs(den) > 1e-12 else 0.0
        phi = [phi[j] - phipp * phi[p - 2 - j] for j in range(p - 1)] + [phipp]
        pacfs.append(phipp)
    return pacfs


def acf_pacf_gate(c, acf1_thr=ACF1_THRESHOLD_DEFAULT, pacf2_max=PACF2_MAX_DEFAULT,
                  lookback=ACF_PACF_LOOKBACK):
    """ACF/PACF 自相关过滤门 (ST趋势引擎)。
    返回 (passed, acf1_val, pacf2_val)。
    - ACF(1) > acf1_thr: 正自相关, 趋势延续而非反转后追入
    - PACF(2) < pacf2_max: 二阶偏自相关不过热, 非直线冲顶
    """
    c = np.asarray(c, dtype='float64')
    if len(c) < lookback + 2:
        return True, 0.0, 0.0
    win = c[-(lookback + 1):]
    r = np.diff(win) / win[:-1]
    if len(r) < 10:
        return True, 0.0, 0.0
    acf1 = _acf(r, 1)
    pacf2 = _pacf(r, 2)[1]  # _pacf 返回 [lag1, lag2], 取 lag2
    passed = (acf1 > acf1_thr) and (pacf2 < pacf2_max)
    return passed, float(acf1), float(pacf2)


def scan_st_pure(h, l, c, params, continuation=False, trend_follow=False):
    """ST(10,3) 纯信号趋势 → signal or None
    continuation=True: 允许趋势延续入场(回调ST线附近)
    trend_follow=True: 允许趋势跟随入场(EMA对齐+回调, 不需ST线接近)
    """
    n = len(c)
    if n < 100: return None
    
    st_period = params.get('st_period', 10)
    st_mult = params.get('st_mult', 3.0)
    
    trend, fu, fl = _supertrend(h, l, c, st_period, st_mult)
    price = c[-1]
    _trail = {'strategy': 'st_pure'}  # P0
    
    # SuperTrend翻转检测
    st_flip = ((trend[-1] == 1 and trend[-2] <= 0) or
               (trend[-1] == -1 and trend[-2] >= 0))
    _trail['st_flip_signal'] = {'passed': st_flip, 'trend_now': int(trend[-1]), 'trend_prev': int(trend[-2])}
    
    ema50 = pd_ema(c, 50)
    ema144 = pd_ema(c, 144)
    ema453 = pd_ema(c, 453)
    
    if st_flip:
        side = 'long' if trend[-1] == 1 else 'short'
        # A: EMA453硬方向过滤 (2026-07-21)
        ema453_pass = not ((side == 'long' and price < ema453[-1]) or (side == 'short' and price > ema453[-1]))
        _trail['ema453_direction'] = {'passed': ema453_pass, 'price_vs_ema': 'above' if price > ema453[-1] else 'below', 'side': side}
        if not ema453_pass:
            return None
        entry_mode = 'flip'
    elif continuation and trend[-1] != 0:
        # 趋势延续: 已确立方向中回踩ST线入场 (2026-07-17)
        # B: 稳定性从3bar→5bar (2026-07-21)
        stable = all(trend[-i] == trend[-1] for i in range(1, min(6, n)))
        _trail['stability'] = {'passed': stable, 'bars': min(6, n)-1}
        if not stable:
            return None
        side = 'long' if trend[-1] == 1 else 'short'
        # A: EMA453硬方向过滤
        ema453_pass = not ((side == 'long' and price < ema453[-1]) or (side == 'short' and price > ema453[-1]))
        _trail['ema453_direction'] = {'passed': ema453_pass, 'price_vs_ema': 'above' if price > ema453[-1] else 'below', 'side': side}
        if not ema453_pass:
            return None
        st_line = fl[-1] if side == 'long' else fu[-1]
        pct_dist = abs(price - st_line) / price * 100
        _trail['st_proximity'] = {'passed': pct_dist <= 3.0, 'dist_pct': round(pct_dist, 2), 'threshold': '<3.0'}
        if pct_dist > 3.0:
            return None
        entry_mode = 'continuation'
    elif trend_follow and trend[-1] != 0:
        # ── 趋势跟随入场 V1 (2026-07-21) ──
        # 条件: EMA对齐确认 + ST方向一致 + 回调至EMA50附近
        side = 'long' if trend[-1] == 1 else 'short'
        
        # 1. ST方向已稳定5+bar (2026-07-21: 3→5)
        stable = all(trend[-i] == trend[-1] for i in range(1, min(6, n)))
        _trail['stability'] = {'passed': stable, 'bars': min(6, n)-1}
        if not stable:
            return None
        
        # A: EMA453硬方向过滤
        ema453_pass = not ((side == 'long' and price < ema453[-1]) or (side == 'short' and price > ema453[-1]))
        _trail['ema453_direction'] = {'passed': ema453_pass, 'price_vs_ema': 'above' if price > ema453[-1] else 'below', 'side': side}
        if not ema453_pass:
            return None
        
        # 2. EMA对齐确认方向 (仅需EMA50>EMA144, EMA453过于滞后不作为硬条件)
        ema_align_pass = True
        if side == 'long':
            if not (ema50[-1] > ema144[-1]):
                ema_align_pass = False
            if price > ema453[-1] * 1.15:
                ema_align_pass = False  # 偏离EMA453超15%, 追高风险
        else:
            if not (ema50[-1] < ema144[-1]):
                ema_align_pass = False
            if price < ema453[-1] * 0.85:
                ema_align_pass = False
        _trail['ema_alignment'] = {'passed': ema_align_pass, 'ema50': round(float(ema50[-1]), 2), 'ema144': round(float(ema144[-1]), 2), 'ema453': round(float(ema453[-1]), 2)}
        if not ema_align_pass:
            return None
        
        # 3. 价格回调至EMA50附近 (偏离<5%)
        ema50_dev = abs(price - ema50[-1]) / ema50[-1] * 100
        _trail['ema50_deviation'] = {'passed': ema50_dev <= 5.0, 'value': round(ema50_dev, 1), 'threshold': '<5.0'}
        if ema50_dev > 5.0:
            return None
        
        # 4. RSI不追极端 (放宽至85)
        rsi_val = _compute_rsi(c, 14)
        rsi_pass = not ((side == 'long' and rsi_val > 85) or (side == 'short' and rsi_val < 15))
        _trail['rsi_trend_follow'] = {'passed': rsi_pass, 'value': round(rsi_val, 1), 'threshold': '<85(long) / >15(short)'}
        if not rsi_pass:
            return None
        
        # 5. 价格不在20bar极高点 (距离高点>1%才入场, 等微小回调)
        recent_high = np.max(c[-20:])
        not_at_high = True
        if side == 'long' and price > recent_high * 0.99:
            not_at_high = False
        recent_low = np.min(c[-20:])
        if side == 'short' and price < recent_low * 1.01:
            not_at_high = False
        _trail['not_at_extreme'] = {'passed': not_at_high, 'recent_high': round(float(recent_high), 2), 'recent_low': round(float(recent_low), 2)}
        if not not_at_high:
            return None
        
        entry_mode = 'trend_follow'
    else:
        _trail['signal'] = {'passed': False, 'reason': 'no ST event'}
        return None
    
    # C: ATR百分位过滤 - 低波动横盘不参与趋势 (2026-07-21)
    # 2026-10-01: 门槛从硬编码50改为可配置atr_pct_floor, 牛市放宽至45让趋势引擎多干活
    atr_pct = atr_percentile(h, l, c, 14)
    atr_floor = params.get('atr_pct_floor', 50)
    rsi_val2 = _compute_rsi(c, 14)  # 用于RSI极端区日志
    _trail['atr_percentile'] = {'passed': atr_pct >= atr_floor, 'value': round(atr_pct, 1), 'threshold': f'>={atr_floor}'}
    _trail['rsi_extreme'] = {'passed': not (side == 'short' and rsi_val2 < RSI_OVERSOLD_BLOCK), 'value': round(rsi_val2, 1), 'threshold': f'>{RSI_OVERSOLD_BLOCK} for short'}
    if atr_pct < atr_floor:
        return None
    if side == 'short' and rsi_val2 < RSI_OVERSOLD_BLOCK:
        return None
    
    # D: 追单时机过滤 (2026-08-14) 规则A+B
    # 规则A: 做空别追短期超跌(1h跌>0.4%→反弹止损) | 规则B: EMA50附近趋势不明朗不追(偏离-0.3%~+0.8%)
    chg_1h_pct = (price / c[-3] - 1) * 100 if len(c) >= 3 else 0.0
    ema50_dev_pct = (price - ema50[-1]) / ema50[-1] * 100 if ema50[-1] > 0 else 0.0
    _trail['timing_filter'] = {'chg_1h_pct': round(chg_1h_pct, 3), 'ema50_dev_pct': round(ema50_dev_pct, 3), 'passed': True}
    if side == 'short' and chg_1h_pct < -0.4:
        _trail['timing_filter'].update({'passed': False, 'reason': f'做空追空太深(1h跌{chg_1h_pct:.2f}%<-0.4%)'})
        return None
    if -0.3 <= ema50_dev_pct <= 0.8:
        _trail['timing_filter'].update({'passed': False, 'reason': f'EMA50附近趋势不明(偏离{ema50_dev_pct:.2f}%)'})
        return None
    
    # E: ACF/PACF 自相关过滤 (2026-08-27) — 默认关, 由 playbook 参数开关
    # ACF(1)>阈值=趋势延续; PACF(2)<上限=不过热。组合回测胜率36-38%→51%+
    if params.get('acf_pacf_filter', ACF_PACF_FILTER_DEFAULT):
        acf1_thr = params.get('acf1_threshold', ACF1_THRESHOLD_DEFAULT)
        pacf2_max = params.get('pacf2_max', PACF2_MAX_DEFAULT)
        acf_passed, acf1_val, pacf2_val = acf_pacf_gate(c, acf1_thr, pacf2_max)
        _trail['acf_pacf_filter'] = {
            'passed': acf_passed, 'acf1': round(acf1_val, 3), 'pacf2': round(pacf2_val, 3),
            'acf1_threshold': acf1_thr, 'pacf2_max': pacf2_max,
        }
        if not acf_passed:
            return None
    
    _trail['overall'] = 'PASSED'
    
    # TP/SL = ST固定3.0%/1.5% (2026-08-21: 量比放量过滤回测最优, TP2%截断趋势利润)
    tp = price * (1 + 0.03) if side == 'long' else price * (1 - 0.03)
    sl_price = price * (1 - 0.015) if side == 'long' else price * (1 + 0.015)
    
    return {
        'action': 'open', 'side': side,
        'entry': float(price),
        'stop_loss': float(sl_price),
        'take_profit': float(tp),
        'meta': {
            'st_value': float(fu[-1] if side == 'short' else fl[-1]),
            'st_flip_bar': 1,
            'entry_mode': entry_mode,
            'ema50_dev': round(abs(price - ema50[-1]) / ema50[-1] * 100, 1) if len(ema50) > 0 else 0,
            '_decision_trail': _trail,  # P0: CoT决策追踪
        }
    }


# ═══════════════ BB(20,2) 均值回归(震荡) ═══════════════

def scan_bb20_range(h, l, c, params):
    """BB(20,2) 均值回归(震荡) + EMA453方向过滤 → signal or None"""
    n = len(c)
    if n < 100: return None
    
    # EMA453 趋势方向过滤
    ema453_val = c[0]
    alpha_453 = 2.0 / 454.0
    for i in range(1, n):
        ema453_val = alpha_453 * c[i] + (1 - alpha_453) * ema453_val
    
    _trail = {'strategy': 'bb20_range'}  # P0: CoT决策追踪
    
    bb_period = params.get('bb_period', 20)
    bb_std = params.get('bb_std', 2.0)
    bb_decay_bars = params.get('bb_decay_bars', 5)      # P1: 时间衰减K线数
    bb_decay_weight = params.get('bb_decay_weight', 1.5)  # P1: 最近K线权重倍率
    
    # Bollinger Bands — P1: 使用时间衰减加权标准差
    bmid = np.zeros(n); bu = np.zeros(n); bl = np.zeros(n)
    for i in range(bb_period - 1, n):
        win = c[i - bb_period + 1:i + 1]
        mavg, s = _weighted_std(win, decay_bars=bb_decay_bars, decay_weight=bb_decay_weight)
        bmid[i] = mavg; bu[i] = mavg + bb_std * s; bl[i] = mavg - bb_std * s
    
    if bmid[-1] == 0: return None
    
    price = c[-1]
    below_bottom = price <= bl[-1]
    above_top = price >= bu[-1]
    
    # 方案A(2026-09-16): 做空回落确认 — 价格从上轨回落而非仍站在上轨之上
    # 今天INTC/SOXL/NEAR/ENA 4笔做空在强势突破位逆势接刀被+1.5%止损
    # 改为: 前一根bar触碰上轨 + 当前回落到上轨下方(回落不深) 才放行做空
    bb_short_pullback = params.get('bb_short_pullback', True)
    bb_short_pullback_pct = params.get('bb_short_pullback_pct', 0.01)
    
    short_pullback = False
    if bb_short_pullback and n >= 2:
        prev_high = h[-2]
        prev_bu = bu[-2] if bu[-2] != 0 else bu[-1]
        prev_touched = prev_high >= prev_bu  # 前一根bar最高价触碰/突破上轨
        cur_below = price < bu[-1]           # 当前价已回落到上轨下方
        near_top = price >= bu[-1] * (1 - bb_short_pullback_pct)  # 回落不深(仍紧贴上轨)
        short_pullback = prev_touched and cur_below and near_top
    
    short_trigger = short_pullback if bb_short_pullback else above_top
    
    _trail['bb_band_touch'] = {'passed': below_bottom or short_trigger, 'below_bottom': below_bottom, 'above_top': above_top, 'short_pullback': short_pullback, 'price': round(float(price), 4), 'bb_lower': round(float(bl[-1]), 4), 'bb_upper': round(float(bu[-1]), 4)}
    
    if not below_bottom and not short_trigger:
        return None
    
    side = 'long' if below_bottom else 'short'
    _trail['bb_side'] = {'side': side}
    
    # EMA20/50 趋势一致性过滤 (2026-07-25: bb20不再逆势摸顶抄底)
    ema20_val = ema(c, 20)[-1]
    ema50_val = ema(c, 50)[-1]
    if side == 'long' and ema20_val <= ema50_val:
        _trail['ema2050_align'] = {'passed': False, 'reason': 'EMA20<=EMA50, 不逆势做多', 'ema20': round(float(ema20_val), 4), 'ema50': round(float(ema50_val), 4)}
        return None  # EMA20未上穿EMA50 → 不逆势做多
    if side == 'short' and ema20_val >= ema50_val:
        _trail['ema2050_align'] = {'passed': False, 'reason': 'EMA20>=EMA50, 不逆势做空', 'ema20': round(float(ema20_val), 4), 'ema50': round(float(ema50_val), 4)}
        return None  # EMA20未下穿EMA50 → 不逆势做空
    _trail['ema2050_align'] = {'passed': True, 'ema20': round(float(ema20_val), 4), 'ema50': round(float(ema50_val), 4)}
    
    # RSI极值过滤 (v3.58 2026-08-03): 碰轨时RSI需确认超买/超卖, 过滤假碰轨
    rsi_bb_oversold = params.get('rsi_bb_oversold', 35)
    rsi_bb_overbought = params.get('rsi_bb_overbought', 65)
    rsi_val = _compute_rsi(c, 14)
    if side == 'long' and rsi_val > rsi_bb_oversold:
        _trail['rsi_bb_filter'] = {'passed': False, 'value': round(rsi_val, 1), 'threshold': f'<{rsi_bb_oversold}', 'reason': '碰下轨但RSI不够超卖'}
        return None  # 碰下轨但RSI不够超卖, 假反弹风险
    if side == 'short' and rsi_val < rsi_bb_overbought:
        _trail['rsi_bb_filter'] = {'passed': False, 'value': round(rsi_val, 1), 'threshold': f'>{rsi_bb_overbought}', 'reason': '碰上轨但RSI不够超买'}
        return None  # 碰上轨但RSI不够超买, 假回落风险
    _trail['rsi_bb_filter'] = {'passed': True, 'value': round(rsi_val, 1), 'threshold': f'<{rsi_bb_oversold}(long) / >{rsi_bb_overbought}(short)'}
    
    # EMA453方向过滤: 逆势→半仓放行(标记_counter_trend, 不再硬拦截)
    counter_trend = False
    if side == 'long' and price < ema453_val:
        counter_trend = True
    if side == 'short' and price > ema453_val:
        counter_trend = True
    _trail['ema453_direction'] = {'passed': True, 'counter_trend': counter_trend, 'price_vs_ema': 'above' if price > ema453_val else 'below', 'side': side}
    
    _trail['overall'] = 'PASSED'
    
    # TP/SL = 固定2.0%/1.5% (v3.55 统一简化)
    sl = price * (1 - 0.015) if side == 'long' else price * (1 + 0.015)
    tp = price * (1 + 0.02) if side == 'long' else price * (1 - 0.02)
    
    return {
        'action': 'open', 'side': side,
        'entry': float(price),
        'stop_loss': float(sl),
        'take_profit': float(tp),
        'meta': {
            'bb_upper': round(float(bu[-1]), 4),
            'bb_lower': round(float(bl[-1]), 4),
            'bb_mid': round(float(bmid[-1]), 4),
            'position': 'below_band' if below_bottom else 'above_band',
            '_counter_trend': counter_trend,
            'rsi': round(rsi_val, 1),
            '_decision_trail': _trail,  # P0: CoT决策追踪
        }
    }


# ═══════════════ YH8引擎 V4 ═══════════════

def _h4_supertrend_dir(df_4h):
    """4h SuperTrend(10,3) 方向: +1多头 / -1空头 / 0中性
    用最后一根「已收盘」4h bar (对齐回测口径, 剔除未收盘bar)
    (2026-09-10: BB20做多 MTF 共识辅助函数)"""
    if df_4h is None or len(df_4h) < 20:
        return 0
    h = df_4h['high'].values.astype(np.float64)
    l = df_4h['low'].values.astype(np.float64)
    c = df_4h['close'].values.astype(np.float64)
    try:
        _last_open = int(df_4h.index[-1].value // 10**9)
        if time.time() - _last_open < 4 * 3600:  # 末根4h bar 未收盘则剔除
            h, l, c = h[:-1], l[:-1], c[:-1]
    except Exception:
        pass
    if len(c) < 20:
        return 0
    trend, _, _ = _supertrend(h, l, c, 10, 3.0)
    return int(trend[-1])


def _h4_ema_dir(df_4h):
    """4h EMA50 vs EMA144 方向: +1多头排列 / -1空头排列 / 0中性
    用最后一根「已收盘」4h bar (对齐回测口径, 剔除未收盘bar)
    (2026-09-10: BB20做空 MTF 共识辅助函数)"""
    if df_4h is None or len(df_4h) < 145:
        return 0
    c = df_4h['close'].values.astype(np.float64)
    try:
        _last_open = int(df_4h.index[-1].value // 10**9)
        if time.time() - _last_open < 4 * 3600:  # 末根4h bar 未收盘则剔除
            c = c[:-1]
    except Exception:
        pass
    if len(c) < 145:
        return 0
    ema50 = pd_ema(c, 50)[-1]
    ema144 = pd_ema(c, 144)[-1]
    if ema50 > ema144:
        return 1
    elif ema50 < ema144:
        return -1
    return 0


class YH8Engine:
    """YH8.5 统一TP2.0%/SL1.5% | Playbook路由 + 三情景切换"""
    
    def __init__(self):
        self.pb = get_playbook()
        self._initialized = True
        # 缓存各策略参数 (热加载)
        self._params_cache = {}
    
    def _get_params(self, strategy_id):
        """获取策略参数 (带缓存)"""
        if strategy_id not in self._params_cache:
            self._params_cache[strategy_id] = self.pb.get_params(strategy_id)
        return self._params_cache[strategy_id]
    
    def _detect_scenario(self, c):
        """检测当前市场情景
        - BTC 价格在 EMA453 上方 > 3% → bull
        - BTC 价格在 EMA453 下方 > 3% → bear
        - ±3% 内 → base
        返回: (scenario_str, deviation_pct)
        """
        if len(c) < 454:
            return 'base', 0.0
        
        price = c[-1]
        ema453 = pd_ema(c, 453)[-1]
        if ema453 <= 0:
            return 'base', 0.0
        
        deviation = (price - ema453) / ema453 * 100
        
        if deviation > 3.0:
            return 'bull', round(deviation, 2)
        elif deviation < -3.0:
            return 'bear', round(deviation, 2)
        else:
            return 'base', round(deviation, 2)
    
    def _get_scenario_params(self, strategy_id):
        """从 playbook 获取策略的情景参数组"""
        strategy_data = self.pb.data.get('strategies', {}).get(strategy_id, {})
        return strategy_data.get('scenario_params', {})
    
    def scan(self, sym, df_30m, btc_30m=None, positions=None, allowed='both', force_trending=False, df_4h=None, breadth_severity=None):
        """
        YH8.5 信号扫描 (30m ONLY)
        
        Routing:
          趋势池 → ST(10,3)+Gann (ETH/BNB) 或 ST(10,3)纯信号 (BTC/AAVE/LTC)
          震荡池 → BB(20,2) 均值回归
        
        allowed: 'range' | 'trend' | 'both'
        force_trending: 强制趋势状态 (red_alert时让全币种用ST产做空信号)
        """
        if len(df_30m) < 100:
            return None
        
        h = df_30m['high'].values.astype(np.float64)
        l = df_30m['low'].values.astype(np.float64)
        c = df_30m['close'].values.astype(np.float64)
        price = float(c[-1])
        # ── BB20 收盘确认: 末根未收盘bar用实时价, 剔除后 c[-1]=已收盘价 ──
        _last_bar_unclosed = False
        if BB20_CLOSE_CONFIRM:
            try:
                _last_utc = int(df_30m.index[-1].value // 10**9)
                _last_bar_unclosed = (time.time() - _last_utc) < 1800  # 30m未走完
            except Exception:
                _last_bar_unclosed = False
        
        # Step 1: 市场状态
        state, atr_pct = classify_market(df_30m)
        _decision_trail = {  # P0: 引擎级决策追踪
            'market_state': {'passed': True, 'state': state, 'atr_pct': round(atr_pct, 1), 'threshold': f'>{ATR_PERCENTILE_TRENDING} → trending'},
        }
        if force_trending:
            state = 'trending'  # 2026-07-17: red_alert/block强制趋势→ST做空
            _decision_trail['market_state']['forced'] = True
        
        # Step 1.5: 三情景检测 (bull/base/bear)
        scenario = 'base'
        scenario_deviation = 0.0
        if btc_30m is not None and len(btc_30m) >= 454:
            btc_c = btc_30m['close'].values.astype(np.float64)
            scenario, scenario_deviation = self._detect_scenario(btc_c)
        elif sym and sym.endswith('/USDT'):
            scenario, scenario_deviation = self._detect_scenario(c)
        _decision_trail['market_scenario'] = {'scenario': scenario, 'deviation_pct': scenario_deviation}
        
        # Step 2: 路由到对应策略
        signal = None
        strategy_id = None
        strategy_name = None
        
        if state == 'trending' and allowed in ('trend', 'both'):
            # 趋势端: 查Playbook路由
            sid = self.pb.get_coin_strategy(sym, 'trend')
            if sid == 'st_pure_trend':
                params = self._get_params('st_pure_trend')
                # 2026-10-01: 牛市下放宽ATR百分位门槛(50→45), 让ST趋势引擎在牛市多开单
                # 数据依据: 9月ST现存池4笔+21.56U/75%胜率, 但全月仅开9笔(开单量偏低)
                # 仅放宽「趋势强度判定」门槛, 不动ACF/PACF胜率核心因子与止损
                if scenario == 'bull':
                    params = dict(params)
                    params['atr_pct_floor'] = 45
                signal = scan_st_pure(h, l, c, params, continuation=True, trend_follow=not force_trending)
                strategy_id = 'st_pure_trend'
                strategy_name = 'yh85_st_pure'
        
        elif state == 'ranging' and allowed in ('range', 'both'):
            sid = self.pb.get_coin_strategy(sym, 'range')
            if sid == 'bb20_range':
                params = self._get_params('bb20_range')
                hh, ll, cc = h, l, c
                if _last_bar_unclosed and len(c) >= 101:
                    hh, ll, cc = h[:-1], l[:-1], c[:-1]
                    _decision_trail['bb20_close_confirm'] = {'dropped_unclosed_bar': True}
                signal = scan_bb20_range(hh, ll, cc, params)
                strategy_id = 'bb20_range'
                strategy_name = 'yh85_bb20'
        
        # ── 2026-08-19: ST做空高波动禁止 — atr_pct>=70 不做空 ──
        # 数据依据(实盘212笔回放): ST做空 atr 70-80 17笔-17.11U/29%胜率, >=80 19笔-4.11U
        # 高波动追空=追在下跌末端被V型反抽轧空; 仅低/中波动(<70)下跌趋势做空才稳
        if strategy_id == 'st_pure_trend' and signal is not None and signal.get('side') == 'short' and atr_pct >= 70:
            _decision_trail['short_atr_gate'] = {'passed': False, 'atr_pct': round(atr_pct, 1), 'threshold': '>=70 禁止做空'}
            print(f"🚫 [ST做空拦截] {sym} atr_pct={atr_pct:.1f}≥70 → 高波动禁止做空", file=sys.stderr, flush=True)
            signal = None
        
        # ── 2026-08-31 撤销: BB20做空 BTC牛市禁止(原08-27) — 回测证伪 ──
        # 原结论「BTC牛做空负期望」被 97笔/31天 完整过滤链回测推翻:
        #   BTC牛(EMA7/25)做空 69笔 49.3%胜率 均+0.225% (正期望)
        #   BTC牛(EMA453)做空 62笔 48.4%胜率 均+0.194% (正期望)
        # 真相: 真正负期望的是「BTC牛+市场偏跌」(bull_down 26.7%胜率-0.567%),
        #       而「BTC牛+市场普涨」(bull_up 66.7%胜率+0.833%)是最强做空场景, 一刀切误杀
        
        # ── 2026-09-10: BB20做多 4h MTF 共识 — 4h空头趋势不抄底 (多模型共识) ──
        # 回测: 胜率46%→51.1%, 累计+16.5%→+27%, 回撤-19.5%→-12%, 分半两窗一致
        if (BB20_LONG_MTF_CONSENSUS and strategy_id == 'bb20_range'
                and signal is not None and signal.get('side') == 'long'):
            h4_dir = _h4_supertrend_dir(df_4h)
            # ── 2026-10-06: 普涨市豁免 — 4hST<0在up_alert/up_block下是回调非反转 ──
            # 回测(近60天37币): 4hST<0信号 普涨市每笔+0.549%(41笔胜率59%), 普跌市每笔-0.051%
            # 故仅在普涨市豁免, 普跌市继续拦(block前30天17%胜率-0.917%是灾难)
            breadth_exempt = breadth_severity in ('up_alert', 'up_block')
            if h4_dir < 0 and not breadth_exempt:
                _decision_trail['bb20_long_mtf_consensus'] = {
                    'passed': False, 'h4_st_dir': h4_dir,
                    'reason': '4h空头趋势(SuperTrend<0), 不抄底',
                }
                print(f"🚫 [BB20做多MTF拦截] {sym} 4hST方向={h4_dir}<0 → 空头趋势不抄底", file=sys.stderr, flush=True)
                signal = None
            else:
                _decision_trail['bb20_long_mtf_consensus'] = {
                    'passed': True, 'h4_st_dir': h4_dir,
                    'breadth_exempt': bool(h4_dir < 0 and breadth_exempt),
                }
                if h4_dir < 0 and breadth_exempt:
                    print(f"✅ [BB20做多MTF豁免] {sym} 4hST方向={h4_dir}<0 但市场宽度={breadth_severity} → 普涨市回调抄底放行", file=sys.stderr, flush=True)
        
        # ── 2026-09-10: BB20做空 4h EMA 共识 — 4h多头排列不追空 (反弹期逆势做空拦截) ──
        # 回测: 胜率51.2%→60.5%, 每笔+0.292%→+0.617%(翻倍), 反弹期48.3%→51.7%(负期望拉回正)
        if (BB20_SHORT_MTF_CONSENSUS and strategy_id == 'bb20_range'
                and signal is not None and signal.get('side') == 'short'):
            h4_ema = _h4_ema_dir(df_4h)
            if h4_ema > 0:
                _decision_trail['bb20_short_mtf_consensus'] = {
                    'passed': False, 'h4_ema_dir': h4_ema,
                    'reason': '4h多头排列(EMA50>EMA144), 不逆势做空',
                }
                print(f"🚫 [BB20做空MTF拦截] {sym} 4hEMA方向={h4_ema}>0 → 多头排列不追空", file=sys.stderr, flush=True)
                signal = None
            else:
                _decision_trail['bb20_short_mtf_consensus'] = {
                    'passed': True, 'h4_ema_dir': h4_ema,
                }
        
        if signal is None:
            return None
        
        # 三情景参数覆盖: 从 playbook 读取 scenario_params
        if strategy_id:
            scenario_params = self._get_scenario_params(strategy_id)
            scenario_overrides = scenario_params.get(scenario, {})
            if scenario_overrides:
                params.update(scenario_overrides)
                _decision_trail['market_scenario']['overrides_applied'] = list(scenario_overrides.keys())
        
        # Step 3: 组装返回信号
        meta = signal.get('meta', {})
        meta.update({
            'state': state,
            'atr_pct': round(atr_pct, 1),
            'engine': 'yh85',
            'strategy_id': strategy_id,
            'price': price,
            '_scenario': scenario,  # 三情景标记
        })
        # 存储入场因子 (供复盘使用)
        meta['_entry_factors'] = {
            'atr_pct': round(atr_pct, 1),
            'price': price,
            'strategy_id': strategy_id,
            'bar_time': str(df_30m.index[-1]) if hasattr(df_30m, 'index') else '?',
        }
        
        signal['symbol'] = sym
        signal['strategy'] = strategy_name
        signal['meta'] = meta
        
        # ═══ RSI极端区过滤器 (v3.54 2026-07-30) ═══
        # 回测依据: RSI<20做空 = 6L/-18.36U vs 5W/+4.19U (净-14.17U)
        #            RSI>70做多 = 4L/-8.79U vs 5W/+19.31U (净+10.52U)
        # 决策: 仅拦截RSI<20做空; RSI>70做多暂不拦截(回测为正期望)
        rsi = _compute_rsi(c, 14)
        side = signal.get('side', '')
        _decision_trail['engine_rsi_filter'] = {'passed': not (side == 'short' and rsi < RSI_OVERSOLD_BLOCK), 'value': round(rsi, 1), 'threshold': f'>{RSI_OVERSOLD_BLOCK} for short'}
        if side == 'short' and rsi < RSI_OVERSOLD_BLOCK:
            _decision_trail['overall'] = 'BLOCKED: RSI<{}'.format(RSI_OVERSOLD_BLOCK)
            return None
        # RSI>70做多过滤器已禁用——回测9笔净+10.52U, 不做拦截
        # if side == 'long' and rsi > RSI_OVERBOUGHT_BLOCK:
        #     return None
        
        # 合并策略层CoT追踪到引擎级
        strategy_trail = signal.get('meta', {}).pop('_decision_trail', {})
        _decision_trail.update(strategy_trail)
        _decision_trail['overall'] = 'PASSED'
        signal['meta']['_decision_trail'] = _decision_trail  # P0: 完整决策链
        
        return signal
    
    def scan_all(self, sym, df_30m):
        """兼容旧接口: 返回 (signal, ml_confidence, regime)"""
        sig = self.scan(sym, df_30m, allowed='both')
        if sig is None:
            return None, 0, 'idle'
        return sig, 0.5, sig['meta'].get('state', 'trending')
    
    # ═══ Playbook代理 ═══
    def invalidate_params_cache(self):
        """清空参数缓存 (Playbook更新后调用)"""
        self._params_cache.clear()
    
    @property
    def trend_coins(self):
        return self.pb.get_trend_coins()
    
    @property
    def range_coins(self):
        return self.pb.get_range_coins()
    
    @property
    def active_coins(self):
        return self.pb.get_all_active_coins()
    
    def dashboard(self):
        return self.pb.dashboard()
