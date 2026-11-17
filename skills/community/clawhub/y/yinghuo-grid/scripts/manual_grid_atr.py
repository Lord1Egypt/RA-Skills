#!/usr/bin/env python3
"""
萤火网格 1.0 (Firefly Grid v1.0) — 手工网格 + 马丁 + ATR 全自动闭环系统
================================================================================
针对「非策略币」手工锚仓，做动态 ATR 网格，全自动加仓/减仓/止盈止损：

- 锚仓 = 用户手动开仓，系统只识别、永不自动动它
- 网格间距 = 基于 ATR 动态计算（可 per-coin 覆盖）
- 马丁递增：递增加仓摊薄成本，封顶控敞口
- 方向：多空镜像（做多做空同一套规则，反向）
- 趋势过滤器：单边行情方向不利时暂停加仓
- 全自动执行：加仓/单格止盈/总止盈止损全部自动下单，无人工确认

用法：
  status                         查看所有网格状态（ATR/触发价/马丁阶梯）
  add <SYMBOL> <SIDE> <QTY> <ENTRY>   登记锚仓 (SIDE=long/short)
  confirm <SYMBOL> [ENTRY] [QTY]      确认手动加了一格（entry默认当前市价，qty默认按马丁名义算）
  reduce <SYMBOL>                     确认手动减了最近一格（LIFO）
  remove <SYMBOL>                     移除某币网格
  sync                              从交易所同步持仓，自动识别加/减
  run                               心跳检查：拉价格+ATR，触发则输出 alert
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import ccxt

# ===================== 规则参数 =====================
VERSION = '萤火网格1.0'    # 策略命名（2026-10-07 正式上线）

# 核心策略参数从 strategy_params.json 加载（付费订阅版提供回测调优后的真实参数）。
# 文件缺失时使用下方「演示参数」（能跑通但非实盘最优值）。
def _load_params():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'strategy_params.json')
    if os.path.exists(p):
        try:
            with open(p) as f:
                return json.load(f)
        except Exception:
            pass
    print("[GRID] ⚠️ 未找到 strategy_params.json，使用演示参数（非实盘调优值）")
    return {}

_PARAMS = _load_params()

# 基础设施参数
ATR_TIMEFRAME = _PARAMS.get('atr_timeframe', '4h')       # ATR 时间框架
ATR_PERIOD = _PARAMS.get('atr_period', 14)               # ATR 周期
MIN_SPACING_PCT = _PARAMS.get('min_spacing_pct', 0.003)  # 间距下限
FOLLOW_MULT = _PARAMS.get('follow_mult', 1.0)            # 防踏空倍数
MIN_NOTIONAL = _PARAMS.get('min_notional', 5.0)          # 最小下单名义

# 核心策略参数（回测调优值，从 config 读取，fallback 为演示值）
ATR_MULT = _PARAMS.get('atr_mult', 1.0)                  # 默认网格间距 = 1×ATR
GLOBAL_ADD_STOP_PNL = _PARAMS.get('global_add_stop_pnl', -0.20)  # 账户级熔断
TREND_EMA_PERIOD = _PARAMS.get('trend_ema_period', 200)  # 趋势线 EMA 周期（演示值）
FIRST_NOTIONAL = _PARAMS.get('first_notional', 20.0)     # 马丁首笔基准名义
MARTINGALE_TIER1 = _PARAMS.get('martingale_tier1', 1.2)  # 前 N 格马丁系数（演示值）
MARTINGALE_TIER2 = _PARAMS.get('martingale_tier2', 1.4)  # 第 N+1 格起（演示值）
TIER1_LEVELS = _PARAMS.get('tier1_levels', 3)            # 前 N 格用 tier1
MAX_LEVELS = _PARAMS.get('max_levels', 3)                # 最多加仓格数（演示值）

# ── 总止盈/止损档位 (盈亏阈值, 减仓比例=实际仓位百分比) ──
TP_LEVELS = [tuple(x) for x in _PARAMS.get('tp_levels', [(0.20, 0.50), (0.30, 1.00)])]
SL_LEVELS = [tuple(x) for x in _PARAMS.get('sl_levels', [(0.10, 0.50), (0.20, 1.00)])]

# ===================== 数据文件 =====================
DIR = Path(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = str(DIR / '.manual_grid_atr.json')
ALERT_LOG = str(DIR / '.manual_grid_alerts.log')   # 告警日志（心跳读取推送）
JOURNAL_FILE = str(DIR / '.manual_grid_journal.jsonl')  # 仓位流水账（长期记录器，可复盘/审计）


# ── 马丁名义计算（固定 20U 基准，与锚仓实际大小解耦）──
def level_multiplier(level_no: int) -> float:
    """第 level_no 格（1-based）相对首笔基准的累计倍数"""
    m = 1.0
    for i in range(1, level_no + 1):
        m *= MARTINGALE_TIER1 if i <= TIER1_LEVELS else MARTINGALE_TIER2
    return m


def level_notional(level_no: int, base: float = None) -> float:
    """第 level_no 格的名义大小。base=None 时用固定基准 FIRST_NOTIONAL"""
    if base is None:
        base = FIRST_NOTIONAL
    return base * level_multiplier(level_no)


class GridLevel:
    def __init__(self, level_id, entry, qty, notional, status='opened'):
        self.level_id = level_id
        self.entry = entry
        self.qty = qty
        self.notional = notional
        self.status = status

    def to_dict(self):
        return {'level_id': self.level_id, 'entry': self.entry, 'qty': self.qty,
                'notional': self.notional, 'status': self.status}

    @staticmethod
    def from_dict(d):
        return GridLevel(d['level_id'], d['entry'], d['qty'], d['notional'],
                         d.get('status', 'opened'))


class Grid:
    def __init__(self, symbol, side, anchor_entry, anchor_qty, anchor_notional=None,
                 mode='fixed', custom_base=None):
        self.symbol = symbol
        self.side = side                      # 'long' / 'short'
        self.anchor_entry = anchor_entry
        self.anchor_qty = anchor_qty
        self.anchor_notional = anchor_notional or (anchor_qty * anchor_entry)
        self.mode = mode                      # 'fixed'/'anchor'/'custom'
        self.custom_base = custom_base        # mode='custom' 时的自定义马丁基数
        self.levels = []                      # 已加网格仓
        self.next_level_id = 1
        self.last_alert = None                # 去重: 上次已推送的 alert key
        self.atr = None                       # 最近一次计算的 ATR
        self.tp_stage = 0                     # 止盈已执行档位 0/1/2
        self.sl_stage = 0                     # 止损已执行档位 0/1/2
        self.grid_base = None                 # 网格参考价（防踏空上移，None=用锚仓入场价）
        self.atr_mult = None                  # ATR 乘数覆盖（None=用全局 ATR_MULT；BTC=0.5）
        self.trend_filter = False             # 趋势过滤器（趋势时停加仓；BTC/ETH=False，其余=True）

    def to_dict(self):
        return {
            'symbol': self.symbol, 'side': self.side,
            'anchor_entry': self.anchor_entry, 'anchor_qty': self.anchor_qty,
            'anchor_notional': self.anchor_notional, 'mode': self.mode,
            'custom_base': self.custom_base,
            'levels': [g.to_dict() for g in self.levels],
            'next_level_id': self.next_level_id,
            'last_alert': self.last_alert, 'atr': self.atr,
            'tp_stage': self.tp_stage, 'sl_stage': self.sl_stage,
            'grid_base': self.grid_base, 'atr_mult': self.atr_mult,
            'trend_filter': self.trend_filter,
        }

    @staticmethod
    def from_dict(d):
        g = Grid(d['symbol'], d['side'], d['anchor_entry'], d['anchor_qty'],
                 d.get('anchor_notional'), d.get('mode', 'fixed'), d.get('custom_base'))
        g.levels = [GridLevel.from_dict(gl) for gl in d.get('levels', [])]
        g.next_level_id = d.get('next_level_id', 1)
        g.last_alert = d.get('last_alert')
        g.atr = d.get('atr')
        g.tp_stage = d.get('tp_stage', 0)
        g.sl_stage = d.get('sl_stage', 0)
        g.grid_base = d.get('grid_base')
        g.atr_mult = d.get('atr_mult')
        g.trend_filter = d.get('trend_filter', False)
        return g

    # ── 工具 ──
    def _base_notional(self):
        """马丁基数：fixed=固定20U，anchor=锚仓实际名义，custom=自定义数值"""
        if self.mode == 'fixed':
            return FIRST_NOTIONAL
        if self.mode == 'anchor':
            return self.anchor_notional
        return self.custom_base or FIRST_NOTIONAL

    def opened_levels(self):
        return [g for g in self.levels if g.status == 'opened']

    def _last_ref_price(self):
        """最近一仓成交价（无网格仓则为网格参考价，默认锚仓入场价）"""
        opened = self.opened_levels()
        if opened:
            return opened[-1].entry
        return self.grid_base if self.grid_base else self.anchor_entry

    def _atr_mult(self):
        """实际 ATR 乘数（BTC 单独设 0.5，其余用全局默认 1.0）"""
        return self.atr_mult if self.atr_mult is not None else ATR_MULT

    def spacing(self, atr, price):
        """网格间距 = max(实际ATR乘数×ATR, 0.3%×价格)，避免低波动币间距过小频繁触发"""
        return max(self._atr_mult() * atr, MIN_SPACING_PCT * price)

    def current_level_no(self):
        """当前已开格数 = 1(锚仓) + 已开网格仓数"""
        return 1 + len(self.opened_levels())

    def can_add(self):
        return len(self.opened_levels()) < MAX_LEVELS

    def total_qty(self):
        """总持仓量 = 锚仓 + 已开网格仓"""
        q = self.anchor_qty
        for l in self.opened_levels():
            q += l.qty
        return q

    def avg_entry(self):
        """总持仓加权平均成本（锚仓 + 已开网格仓）"""
        tq = self.anchor_qty
        tv = self.anchor_qty * self.anchor_entry
        for l in self.opened_levels():
            tq += l.qty
            tv += l.qty * l.entry
        return tv / tq if tq > 0 else self.anchor_entry

    # ── 总止盈/止损判断 ──
    def check_tp_sl(self, current_price):
        """按总持仓加权成本算盈亏%，返回应执行的减仓动作（分两档）"""
        avg = self.avg_entry()
        if avg <= 0:
            return None
        if self.side == 'long':
            pnl_pct = (current_price - avg) / avg
        else:
            pnl_pct = (avg - current_price) / avg

        if pnl_pct >= 0:
            # 止盈：先看高档30%，再看低档20%
            if pnl_pct >= TP_LEVELS[1][0] and self.tp_stage < 2:
                return {'type': 'tp', 'stage': 2, 'reduce_pct': TP_LEVELS[1][1],
                        'pnl_pct': pnl_pct, 'avg': avg, 'price': current_price}
            if pnl_pct >= TP_LEVELS[0][0] and self.tp_stage < 1:
                return {'type': 'tp', 'stage': 1, 'reduce_pct': TP_LEVELS[0][1],
                        'pnl_pct': pnl_pct, 'avg': avg, 'price': current_price}
        else:
            loss = -pnl_pct
            # 止损：先看高档20%，再看低档15%
            if loss >= SL_LEVELS[1][0] and self.sl_stage < 2:
                return {'type': 'sl', 'stage': 2, 'reduce_pct': SL_LEVELS[1][1],
                        'pnl_pct': pnl_pct, 'avg': avg, 'price': current_price}
            if loss >= SL_LEVELS[0][0] and self.sl_stage < 1:
                return {'type': 'sl', 'stage': 1, 'reduce_pct': SL_LEVELS[0][1],
                        'pnl_pct': pnl_pct, 'avg': avg, 'price': current_price}
        return None

    # ── 加仓触发判断（马丁，跌/涨 1×ATR 自动加）──
    def check_add(self, current_price, atr):
        if atr is None or atr <= 0:
            return None
        if not self.can_add():
            return None
        ref = self._last_ref_price()
        spacing = self.spacing(atr, current_price)
        if self.side == 'long':
            add_trigger = ref - spacing      # 跌 0.5×ATR(或下限) 加仓
            triggered = current_price <= add_trigger
        else:
            add_trigger = ref + spacing      # 涨 0.5×ATR(或下限) 加仓（空）
            triggered = current_price >= add_trigger
        if not triggered:
            return None
        next_no = len(self.opened_levels()) + 1
        notional = level_notional(next_no, self._base_notional())
        return {'level_no': next_no, 'notional': notional, 'trigger': add_trigger,
                'ref': ref, 'atr': atr, 'current': current_price}

    # ── 单网格止盈触发判断（涨/跌 0.5×ATR 减最近一格，保存利润 LIFO）──
    def check_reduce(self, current_price, atr):
        if atr is None or atr <= 0:
            return None
        opened = self.opened_levels()
        if not opened:
            return None
        ref = self._last_ref_price()
        spacing = self.spacing(atr, current_price)
        if self.side == 'long':
            reduce_trigger = ref + spacing   # 涨 0.5×ATR(或下限) 减仓
            triggered = current_price >= reduce_trigger
        else:
            reduce_trigger = ref - spacing   # 跌 0.5×ATR(或下限) 减仓（空）
            triggered = current_price <= reduce_trigger
        if not triggered:
            return None
        return {'trigger': reduce_trigger, 'ref': ref, 'atr': atr,
                'current': current_price, 'target': opened[-1]}


class GridManager:
    def __init__(self, quiet=False):
        self.quiet = quiet
        self.grids = {}
        self.ignored = set()                 # 忽略列表（remove 的币不再自动接管）
        self._exchange = None
        self._atr_cache = {}                 # ATR 缓存 {sym: (atr, bar_ts)}，同一根 4h bar 内不重拉
        self._trend_cache = {}               # 趋势缓存 {sym: (trend_on, bar_ts)}，同一根 4h bar 内不重拉
        self._add_pause_alerted = False      # 账户级加仓熔断告警去重
        self._load()

    # ── 交易所 ──
    def _get_exchange(self):
        if self._exchange:
            return self._exchange
        from dotenv import load_dotenv
        load_dotenv(os.path.join(DIR, '.env'))
        self._exchange = ccxt.binanceusdm({
            'apiKey': os.getenv('BINANCE_API_KEY'),
            'secret': os.getenv('BINANCE_API_SECRET'),
            'enableRateLimit': True,
            'options': {'defaultType': 'future'},
        })
        return self._exchange

    @staticmethod
    def _ex_sym(symbol):
        if '/' not in symbol:
            return symbol + '/USDT:USDT'
        return symbol + ':USDT' if ':' not in symbol else symbol

    # ── 持久化 ──
    def _save(self):
        try:
            data = {'grids': {s: g.to_dict() for s, g in self.grids.items()},
                    'ignored': sorted(self.ignored),
                    'saved_at': datetime.now(timezone.utc).isoformat()}
            with open(STATE_FILE, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[GRID] 保存失败: {e}")

    def _journal(self, action, symbol, side, price, qty, **extra):
        """追加一条仓位流水到 jsonl（长期仓位记录器：加/减/接管/清仓全部留痕）"""
        entry = {'ts': int(time.time() * 1000),
                 'time': datetime.now(timezone.utc).isoformat(),
                 'action': action, 'symbol': symbol, 'side': side,
                 'price': price, 'qty': qty}
        entry.update(extra)
        try:
            with open(JOURNAL_FILE, 'a') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"[GRID] ❌ 流水记录失败: {e}")

    def _load(self):
        try:
            if not os.path.exists(STATE_FILE):
                return
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
            for sym, d in data.get('grids', {}).items():
                self.grids[sym] = Grid.from_dict(d)
            self.ignored = set(data.get('ignored', []))
            if not self.quiet:
                print(f"[GRID] 📂 已恢复 {len(self.grids)} 个网格")
        except Exception as e:
            print(f"[GRID] 加载失败: {e}")

    # ── ATR ──
    def _fetch_atr(self, symbol):
        """拉 4h K线算 ATR14（带缓存：同一根 4h bar 内不重拉，降低 API 调用 ~99%）"""
        sym = self._ex_sym(symbol)
        now_ms = int(time.time() * 1000)
        bar_ms = (now_ms // (4 * 3600 * 1000)) * (4 * 3600 * 1000)  # 当前 4h bar 起始毫秒
        cached = self._atr_cache.get(sym)
        if cached and cached[1] == bar_ms:
            return cached[0]
        try:
            ex = self._get_exchange()
            ohlcv = ex.fetch_ohlcv(sym, ATR_TIMEFRAME, limit=ATR_PERIOD + 16)
            if len(ohlcv) < ATR_PERIOD + 2:
                return None
            highs = [c[2] for c in ohlcv]
            lows = [c[3] for c in ohlcv]
            closes = [c[4] for c in ohlcv]
            atr = self._compute_atr(highs, lows, closes, ATR_PERIOD)
            if atr is not None:
                self._atr_cache[sym] = (atr, bar_ms)
            return atr
        except Exception as e:
            print(f"[GRID] ❌ {symbol} ATR 拉取失败: {e}")
            return None

    @staticmethod
    def _compute_atr(highs, lows, closes, period=14):
        n = len(closes)
        if n < period + 1:
            return None
        trs = []
        for i in range(1, n):
            tr = max(highs[i] - lows[i],
                     abs(highs[i] - closes[i - 1]),
                     abs(lows[i] - closes[i - 1]))
            trs.append(tr)
        atr = sum(trs[:period]) / period
        for i in range(period, len(trs)):
            atr = (atr * (period - 1) + trs[i]) / period
        return atr

    @staticmethod
    def _compute_ema(values, period):
        if len(values) < period:
            return None
        k = 2.0 / (period + 1)
        ema = values[0]
        for v in values[1:]:
            ema = v * k + ema * (1 - k)
        return ema

    def _fetch_trend(self, symbol):
        """判断是否下跌趋势（close < EMA113，4h 框架）。带缓存，4h bar 内不重拉。"""
        sym = self._ex_sym(symbol)
        now_ms = int(time.time() * 1000)
        bar_ms = (now_ms // (4 * 3600 * 1000)) * (4 * 3600 * 1000)
        cached = self._trend_cache.get(sym)
        if cached and cached[1] == bar_ms:
            return cached[0]
        try:
            ex = self._get_exchange()
            ohlcv = ex.fetch_ohlcv(sym, ATR_TIMEFRAME, limit=TREND_EMA_PERIOD + 20)
            if len(ohlcv) < TREND_EMA_PERIOD:
                return False
            closes = [c[4] for c in ohlcv]
            ema = self._compute_ema(closes, TREND_EMA_PERIOD)
            if ema is None:
                return False
            trend_on = closes[-1] < ema  # close < EMA = 下跌趋势
            self._trend_cache[sym] = (trend_on, bar_ms)
            return trend_on
        except Exception as e:
            print(f"[GRID] ❌ {symbol} 趋势拉取失败: {e}")
            return False

    # ── 持仓同步 ──
    def _strategy_symbols(self):
        try:
            from strategies.playbook_manager import get_playbook
            pb = get_playbook()
            return set(pb.get_all_active_coins())
        except Exception:
            return set()

    def sync(self):
        """从交易所同步持仓：自动发现并接管所有持仓币种进网格（忽略列表除外）"""
        ex = self._get_exchange()
        try:
            positions = ex.fetch_positions()
            exchange_pos = {}
            for p in positions:
                qty = float(p.get('contracts', 0) or 0)
                if qty <= 0:
                    continue
                raw = p['symbol'].replace(':USDT', '')
                sym = raw if '/' in raw else raw + '/USDT'
                exchange_pos[sym] = {'qty': qty, 'entry': float(p.get('entryPrice', 0)),
                                     'side': p.get('side')}
        except Exception as e:
            print(f"[GRID] 同步持仓异常: {e}")
            return

        # 自动接管：发现新持仓币种 → 注册进网格（忽略列表除外）
        for sym, info in exchange_pos.items():
            if sym in self.ignored or sym in self.grids:
                continue
            side = (info.get('side') or 'long').lower()
            if side not in ('long', 'short'):
                side = 'long'
            self.grids[sym] = Grid(sym, side, info['entry'], info['qty'], mode='fixed')
            self._journal('takeover', sym, side, info['entry'], info['qty'])
            if not self.quiet:
                print(f"[GRID] 🆕 自动接管新持仓: {sym} {side.upper()} "
                      f"{info['qty']}ct @ {info['entry']}")

        for sym, info in exchange_pos.items():
            if sym not in self.grids:
                continue
            g = self.grids[sym]
            grid_qty = sum(l.qty for l in g.opened_levels())
            exchange_anchor = info['qty'] - grid_qty
            if exchange_anchor > g.anchor_qty + 1e-9:
                # 用户新增了仓位 → 识别为手动加了一格（价用当前市价近似）
                diff = exchange_anchor - g.anchor_qty
                try:
                    ticker = ex.fetch_ticker(self._ex_sym(sym))
                    price = ticker['last']
                except Exception:
                    price = info['entry']
                self._add_level_manual(sym, price, diff)
                if not self.quiet:
                    print(f"[GRID] 🔄 {sym} 检测到新增 {diff}ct，已登记为网格仓 @ {price}")
            elif exchange_anchor < g.anchor_qty - 1e-9:
                # 锚仓数量减少（用户手动减锚仓）
                g.anchor_qty = max(0.0, exchange_anchor)
                if not self.quiet:
                    print(f"[GRID] 🔄 {sym} 锚仓数量同步 → {g.anchor_qty}ct")
            else:
                g.anchor_qty = exchange_anchor

        # 清理已清仓的网格（交易所已无仓位）
        for sym in list(self.grids.keys()):
            if sym not in exchange_pos:
                g = self.grids[sym]
                if g.opened_levels():
                    # 网格仓也被清了 → 全部标记关闭
                    for l in g.levels:
                        l.status = 'closed'
                    g.levels = []
                    self._journal('clear', sym, g.side, 0, 0, note='交易所已清仓，网格重置')
                    if not self.quiet:
                        print(f"[GRID] 🧹 {sym} 交易所已清仓，网格重置")

        self._save()

    # ── 手动操作 ──
    def add_anchor(self, symbol, side, qty, entry, mode='fixed', custom_base=None):
        sym = self._norm_symbol(symbol)
        self.grids[sym] = Grid(sym, side, entry, qty, mode=mode, custom_base=custom_base)
        self._save()
        if mode == 'fixed':
            tag = '固定20U'
        elif mode == 'anchor':
            tag = '锚仓名义'
        else:
            tag = f'自定义{custom_base:.0f}U'
        print(f"[GRID] ✅ 已登记锚仓: {side.upper()} {sym} {qty}ct @ {entry} "
              f"≈{qty * entry:.1f}U [马丁基数: {tag}]")

    def confirm_add(self, symbol, entry=None, qty=None):
        sym = self._norm_symbol(symbol)
        if sym not in self.grids:
            print(f"[GRID] ❌ {sym} 无网格，请先 add 登记锚仓")
            return
        g = self.grids[sym]
        if not g.can_add():
            print(f"[GRID] ⛔ {sym} 已达加仓上限 {MAX_LEVELS} 格")
            return
        if entry is None:
            try:
                ticker = self._get_exchange().fetch_ticker(self._ex_sym(sym))
                entry = ticker['last']
            except Exception:
                print(f"[GRID] ❌ {sym} 无法获取当前价，请手动给 entry")
                return
        next_no = len(g.opened_levels()) + 1
        notional = level_notional(next_no, g._base_notional())
        if qty is None:
            qty = notional / entry
        self._add_level_manual(sym, entry, qty)
        self._save()
        print(f"[GRID] ✅ {sym} 已确认加仓第{next_no}格: {qty}ct @ {entry} "
              f"≈{qty * entry:.1f}U")

    def _add_level_manual(self, symbol, entry, qty):
        g = self.grids[symbol]
        next_no = len(g.opened_levels()) + 1
        notional = level_notional(next_no, g._base_notional())
        lid = g.next_level_id
        g.next_level_id += 1
        g.levels.append(GridLevel(lid, entry, qty, notional, 'opened'))
        g.last_alert = None  # 加仓后重置去重，等下一格触发
        return lid

    def confirm_reduce(self, symbol):
        sym = self._norm_symbol(symbol)
        if sym not in self.grids:
            print(f"[GRID] ❌ {sym} 无网格")
            return
        g = self.grids[sym]
        opened = g.opened_levels()
        if not opened:
            print(f"[GRID] ℹ️ {sym} 只剩锚仓，无网格仓可减（锚仓永不自动减）")
            return
        target = opened[-1]
        target.status = 'closed'
        g.last_alert = None
        self._save()
        print(f"[GRID] ✅ {sym} 已确认减仓第{target.level_id}格 "
              f"({target.qty}ct @ {target.entry})")

    def remove(self, symbol):
        sym = self._norm_symbol(symbol)
        if sym in self.grids:
            del self.grids[sym]
        self.ignored.add(sym)
        self._save()
        print(f"[GRID] 🗑️ 已移除 {sym} 网格（加入忽略列表，不再自动接管）")

    def unignore(self, symbol):
        sym = self._norm_symbol(symbol)
        if sym in self.ignored:
            self.ignored.discard(sym)
            self._save()
            print(f"[GRID] ✅ 已取消忽略 {sym}（下次扫描将自动接管其持仓）")
        else:
            print(f"[GRID] ℹ️ {sym} 不在忽略列表")

    def set_atr_mult(self, symbol, mult):
        """设置某币的 ATR 乘数覆盖（如 BTC 0.5，其余默认 1.0）"""
        sym = self._norm_symbol(symbol)
        if sym in self.grids:
            self.grids[sym].atr_mult = mult
            self._save()
            print(f"[GRID] ✅ 已设置 {sym} 的 ATR 乘数为 {mult}x")
        else:
            print(f"[GRID] ℹ️ {sym} 不在网格列表")

    def set_trend_filter(self, symbol, on):
        """设置某币的趋势过滤器开关（on=True 挂趋势过滤，BTC/ETH 通常 off）"""
        sym = self._norm_symbol(symbol)
        if sym in self.grids:
            self.grids[sym].trend_filter = on
            self._save()
            print(f"[GRID] ✅ 已设置 {sym} 趋势过滤器={'开启' if on else '关闭'}")
        else:
            print(f"[GRID] ℹ️ {sym} 不在网格列表")

    @staticmethod
    def _norm_symbol(symbol):
        sym = symbol.upper()
        if '/' not in sym:
            sym = sym + '/USDT'
        return sym

    # ── 心跳检查 ──
    def _auto_reduce_pct(self, symbol, grid, price, reduce_pct):
        """自动减仓：限价单 reduceOnly 平掉当前总持仓的 reduce_pct 比例"""
        ex = self._get_exchange()
        order_side = 'sell' if grid.side == 'long' else 'buy'
        qty = grid.total_qty() * reduce_pct
        try:
            qty = float(ex.amount_to_precision(self._ex_sym(symbol), qty))
            if qty <= 0:
                return False, '数量为0', 0
            ex.create_order(self._ex_sym(symbol), 'limit', order_side, qty, price,
                            params={'reduceOnly': True, 'timeInForce': 'IOC'})
            realized = self._deduct_qty(grid, qty, price)
            self._journal('reduce_pct', symbol, grid.side, price, qty, realized_pnl=round(realized, 4))
            return True, None, qty
        except Exception as e:
            return False, str(e), 0

    @staticmethod
    def _deduct_qty(grid, qty, price=None):
        """减仓后本地同步持仓：先扣最近网格仓(LIFO)，再扣锚仓。返回已实现盈亏"""
        remaining = qty
        realized = 0.0
        for l in reversed(grid.opened_levels()):
            if remaining <= 0:
                break
            if l.qty <= remaining + 1e-9:
                remaining -= l.qty
                if price:
                    realized += (price - l.entry) * l.qty if grid.side == 'long' else (l.entry - price) * l.qty
                l.qty = 0
                l.status = 'closed'
            else:
                if price:
                    realized += (price - l.entry) * remaining if grid.side == 'long' else (l.entry - price) * remaining
                l.qty -= remaining
                remaining = 0
        if remaining > 0:
            if price:
                realized += (price - grid.anchor_entry) * remaining if grid.side == 'long' else (grid.anchor_entry - price) * remaining
            grid.anchor_qty = max(0.0, grid.anchor_qty - remaining)
        return realized

    def _auto_add(self, symbol, grid, price, notional, level_no, limit_price=None):
        """自动加仓：限价单下单马丁名义（默认在触发价），成功后登记网格仓"""
        ex = self._get_exchange()
        order_side = 'buy' if grid.side == 'long' else 'sell'
        qty = notional / price
        lp = limit_price if limit_price else price
        try:
            qty = float(ex.amount_to_precision(self._ex_sym(symbol), qty))
            if qty * price < MIN_NOTIONAL:
                return False, f'名义{qty*price:.2f}U低于最小下单{MIN_NOTIONAL}U', 0
            ex.create_order(self._ex_sym(symbol), 'limit', order_side, qty, lp,
                            params={'timeInForce': 'IOC'})
            lvl = GridLevel(grid.next_level_id, lp, qty, qty * lp, 'opened')
            grid.levels.append(lvl)
            grid.next_level_id += 1
            self._journal('add', symbol, grid.side, lp, qty, level_id=lvl.level_id, notional=round(qty * lp, 4))
            return True, None, qty
        except Exception as e:
            return False, str(e), 0

    def _auto_reduce_one(self, symbol, grid, price, level, limit_price=None):
        """单网格止盈：限价单 reduceOnly 平掉最近一格（默认在触发价）"""
        ex = self._get_exchange()
        order_side = 'sell' if grid.side == 'long' else 'buy'
        lp = limit_price if limit_price else price
        try:
            qty = float(ex.amount_to_precision(self._ex_sym(symbol), level.qty))
            if qty <= 0:
                return False, '数量为0', 0
            ex.create_order(self._ex_sym(symbol), 'limit', order_side, qty, lp,
                            params={'reduceOnly': True, 'timeInForce': 'IOC'})
            pnl = (lp - level.entry) * qty if grid.side == 'long' else (level.entry - lp) * qty
            level.status = 'closed'
            level.qty = 0
            self._journal('reduce_one', symbol, grid.side, lp, qty, level_id=level.level_id,
                          entry=level.entry, realized_pnl=round(pnl, 4))
            return True, None, qty
        except Exception as e:
            return False, str(e), 0

    def _account_pnl_pct(self, price_map):
        """账户总仓位盈亏%（按持仓名义加权）"""
        total_cost = 0.0
        total_value = 0.0
        for sym, g in self.grids.items():
            price = price_map.get(sym)
            if price is None:
                continue
            q = g.total_qty()
            avg = g.avg_entry()
            if q <= 0 or avg <= 0:
                continue
            total_cost += q * avg
            total_value += q * price
        if total_cost <= 0:
            return None
        return (total_value - total_cost) / total_cost

    def run(self):
        """拉价格，检查总止盈/止损 + 单网格止盈 + 加仓。返回 alert 列表"""
        self.sync()
        if not self.grids:
            return []
        ex = self._get_exchange()
        alerts = []

        # 预扫描：拉所有币价格 + ATR（缓存），算账户总盈亏
        price_map = {}
        atr_map = {}
        for sym, g in list(self.grids.items()):
            try:
                atr = self._fetch_atr(sym)
                g.atr = atr
                ticker = ex.fetch_ticker(self._ex_sym(sym))
                price_map[sym] = ticker['last']
                atr_map[sym] = atr
            except Exception as e:
                print(f"[GRID] ❌ {sym} 获取行情失败: {e}")

        acct_pnl = self._account_pnl_pct(price_map)
        add_paused = acct_pnl is not None and acct_pnl <= GLOBAL_ADD_STOP_PNL

        for sym, g in list(self.grids.items()):
            if sym not in price_map:
                continue
            price = price_map[sym]
            atr = atr_map[sym]

            # 防踏空：网格仓清空且价格偏离参考价超 1×ATR 时，上移/下移网格基准
            if not g.opened_levels() and atr:
                ref = g._last_ref_price()
                if g.side == 'long' and price > ref + FOLLOW_MULT * atr:
                    g.grid_base = price
                    g.last_alert = None
                    print(f"[GRID] 🔺 {sym} 防踏空: 价格 {price:.6f} 超参考价 {ref:.6f}，网格基准上移")
                elif g.side == 'short' and price < ref - FOLLOW_MULT * atr:
                    g.grid_base = price
                    g.last_alert = None
                    print(f"[GRID] 🔻 {sym} 防踏空: 价格 {price:.6f} 低于参考价 {ref:.6f}，网格基准下移")

            action = g.check_tp_sl(price)
            if action is not None:
                tag = '止盈' if action['type'] == 'tp' else '止损'
                key = f"{action['type']}_{action['stage']}"
                if g.last_alert != key:
                    ok, err, reduced_qty = self._auto_reduce_pct(sym, g, price, action['reduce_pct'])
                    if ok:
                        if action['type'] == 'tp':
                            g.tp_stage = max(g.tp_stage, action['stage'])
                        else:
                            g.sl_stage = max(g.sl_stage, action['stage'])
                        line = (f"✅ 网格总{tag} | {sym} {g.side.upper()}\n"
                                f"  价格 {price:.6f} | 盈亏 {action['pnl_pct']*100:+.2f}% "
                                f"(均成本 {action['avg']:.6f})\n"
                                f"  已自动减仓 {reduced_qty:.4f}ct "
                                f"(本次减实际仓位 {action['reduce_pct']*100:.0f}%)\n"
                                f"  剩余持仓 {g.total_qty():.4f}ct")
                        alerts.append({'type': f'manual_grid_{action["type"]}', 'symbol': sym, 'content': line})
                    else:
                        line = (f"❌ 网格总{tag}失败 | {sym} {g.side.upper()}\n"
                                f"  价格 {price:.6f} | 盈亏 {action['pnl_pct']*100:+.2f}% 触发{tag}，下单失败: {err}\n"
                                f"  请手动减仓 {action['reduce_pct']*100:.0f}%")
                        alerts.append({'type': f'manual_grid_{action["type"]}_fail', 'symbol': sym, 'content': line})
                    g.last_alert = key
                continue

            # 单网格止盈（涨/跌 0.5×ATR 减最近一格，保存利润 LIFO）
            red = g.check_reduce(price, atr)
            if red is not None:
                key = f"reduce_{red['target'].level_id}"
                if g.last_alert != key:
                    ok, err, qty = self._auto_reduce_one(sym, g, price, red['target'], red['trigger'])
                    if ok:
                        line = (f"✅ 网格单格止盈 | {sym} {g.side.upper()}\n"
                                f"  价格 {price:.6f} 已触发止盈价 {red['trigger']:.6f} "
                                f"(偏离{g._atr_mult()}xATR={red['atr']:.6f})\n"
                                f"  已平掉第{red['target'].level_id}格 {qty:.4f}ct (保存利润)\n"
                                f"  剩余网格仓 {len(g.opened_levels())} 格")
                        alerts.append({'type': 'manual_grid_reduce', 'symbol': sym, 'content': line})
                    else:
                        line = (f"❌ 网格单格止盈失败 | {sym} {g.side.upper()}\n"
                                f"  价格 {price:.6f} 触发止盈，下单失败: {err}")
                        alerts.append({'type': 'manual_grid_reduce_fail', 'symbol': sym, 'content': line})
                    g.last_alert = key
                continue

            # 马丁加仓（跌/涨 0.5×ATR 自动加；账户总浮亏≥20%时暂停所有新加仓）
            if add_paused:
                if not self._add_pause_alerted:
                    line = (f"⛔ 账户级加仓熔断 | 总仓位浮亏 {acct_pnl*100:.2f}% ≥ {abs(GLOBAL_ADD_STOP_PNL)*100:.0f}%\n"
                            f"  暂停所有新加仓（保留已有仓 + 止损，不新增敞口）")
                    alerts.append({'type': 'manual_grid_add_pause', 'symbol': 'ALL', 'content': line})
                    self._add_pause_alerted = True
                continue
            self._add_pause_alerted = False
            add = g.check_add(price, atr)
            if add is not None and g.trend_filter:
                # 趋势过滤器：趋势方向不利时暂停马丁加仓（BTC/ETH 不挂）
                trend_down = self._fetch_trend(sym)
                if (g.side == 'long' and trend_down) or (g.side == 'short' and not trend_down):
                    add = None
            if add is not None:
                key = f"add_{add['level_no']}"
                if g.last_alert != key:
                    ok, err, qty = self._auto_add(sym, g, price, add['notional'], add['level_no'], add['trigger'])
                    if ok:
                        line = (f"📥 网格自动加仓 | {sym} {g.side.upper()}\n"
                                f"  价格 {price:.6f} 已触发加仓价 {add['trigger']:.6f} "
                                f"(跌{g._atr_mult()}xATR={add['atr']:.6f})\n"
                                f"  已自动加第{add['level_no']}格 {qty:.4f}ct ≈{qty*price:.1f}U")
                        alerts.append({'type': 'manual_grid_add', 'symbol': sym, 'content': line})
                    else:
                        line = (f"❌ 网格自动加仓失败 | {sym} {g.side.upper()}\n"
                                f"  价格 {price:.6f} 触发加第{add['level_no']}格，下单失败: {err}")
                        alerts.append({'type': 'manual_grid_add_fail', 'symbol': sym, 'content': line})
                    g.last_alert = key
                continue

        self._save()
        return alerts


# ── 状态展示 ──
def status(mgr):
    mgr.sync()
    if not mgr.grids:
        print("[GRID] 无网格。用 add 登记锚仓开始：")
        print("  add <SYMBOL> <long|short> <QTY> <ENTRY>")
        return
    ex = mgr._get_exchange()
    print(f"🔥 {VERSION} | 网格 {len(mgr.grids)} 币")
    for sym, g in mgr.grids.items():
        try:
            atr = mgr._fetch_atr(sym)
            g.atr = atr
            ticker = ex.fetch_ticker(mgr._ex_sym(sym))
            cur = ticker['last']
        except Exception:
            atr = g.atr
            cur = 0

        opened = g.opened_levels()
        avg = g.avg_entry()
        total_qty = g.total_qty()
        if g.side == 'long':
            pnl_pct = (cur - avg) / avg * 100 if avg > 0 else 0
        else:
            pnl_pct = (avg - cur) / avg * 100 if avg > 0 else 0

        print(f"\n{'=' * 58}")
        print(f"  {sym} | {g.side.upper()} | 现价 {cur:.6f} | 趋势过滤 {'ON' if g.trend_filter else 'OFF'}")
        print(f"  ATR({ATR_TIMEFRAME},{ATR_PERIOD}) = {atr:.6f}" if atr else f"  ATR = N/A")
        print(f"  锚仓: {g.anchor_qty}ct @ {g.anchor_entry:.6f} ≈{g.anchor_notional:.1f}U")

        if opened:
            print(f"  网格仓({len(opened)}格):")
            for l in opened:
                print(f"    第{l.level_id}格: {l.qty}ct @ {l.entry:.6f} ≈{l.notional:.1f}U")
        else:
            print(f"  网格仓: 无")

        total_notional = g.anchor_notional + sum(l.notional for l in opened)
        print(f"  总持仓 {total_qty:.4f}ct ≈{total_notional:.1f}U | 均成本 {avg:.6f} | 盈亏 {pnl_pct:+.2f}%")
        if opened and atr:
            ref = g._last_ref_price()
            red_at = ref + g._atr_mult() * atr if g.side == 'long' else ref - g._atr_mult() * atr
            print(f"  单格止盈价 {red_at:.6f} (偏离{g._atr_mult()}xATR, 减最近一格保存)")
        print(f"  止盈20%减50%仓 {'✅已执行' if g.tp_stage>=1 else '待触发'}")
        print(f"  止盈30%减100%仓(全平) {'✅已执行' if g.tp_stage>=2 else '待触发'}")
        print(f"  止损15%减50%仓 {'✅已执行' if g.sl_stage>=1 else '待触发'}")
        print(f"  止损25%减100%仓(全平) {'✅已执行' if g.sl_stage>=2 else '待触发'}")
        print(f"{'=' * 58}")
    mgr._save()


def show_journal(filters=None):
    """查看仓位流水账（长期仓位记录器）"""
    if not os.path.exists(JOURNAL_FILE):
        print("[GRID] 暂无流水记录")
        return
    rows = []
    with open(JOURNAL_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    if filters:
        sym_filter = filters[0].upper()
        if '/' not in sym_filter:
            sym_filter += '/USDT'
        rows = [r for r in rows if r.get('symbol') == sym_filter]
    if not rows:
        print("[GRID] 无匹配流水")
        return
    action_emoji = {'add': '➕加仓', 'reduce_one': '🔻单格止盈', 'reduce_pct': '🔻总止盈止损',
                    'takeover': '🆕接管', 'clear': '🧹清仓'}
    print(f"📒 萤火网格1.0 仓位流水 ({len(rows)} 条):")
    for r in rows:
        ts = r.get('time', '')
        act = action_emoji.get(r.get('action'), r.get('action'))
        pnl = r.get('realized_pnl')
        pnl_s = f" 盈亏{pnl:+.3f}U" if pnl is not None else ''
        print(f"  {ts[:19]} | {r.get('symbol')} {r.get('side','').upper()} | {act} "
              f"{r.get('qty',0)}ct @ {r.get('price',0)}{pnl_s}")


def _append_alert_log(content):
    """把告警追加到日志文件（心跳读取推送后清空）"""
    try:
        with open(ALERT_LOG, 'a') as f:
            f.write(content + '\n')
    except Exception:
        pass


def watch(mgr, interval=60):
    """常驻循环：每 interval 秒自动扫描持仓 + 检查触发（Ctrl+C 停止）"""
    import time
    print(f"[GRID] 👁️ 开始每 {interval}s 自动扫描（自动接管持仓 + 检查触发，Ctrl+C 停止）...", flush=True)
    try:
        while True:
            try:
                alerts = mgr.run()
                if alerts:
                    for a in alerts:
                        _append_alert_log(a['content'])
                        print(a['content'], flush=True)
                        print('---', flush=True)
            except Exception as e:
                print(f"[GRID] ❌ 扫描异常: {e}", flush=True)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[GRID] ⏹️ 已停止扫描", flush=True)


def main():
    args = sys.argv[1:]
    cmd = args[0].lower() if args else 'status'
    mgr = GridManager(quiet=(cmd == 'run'))
    if not args:
        status(mgr)
        return

    if cmd == 'status':
        status(mgr)
    elif cmd == 'add':
        if len(args) < 5:
            print("用法: add <SYMBOL> <long|short> <QTY> <ENTRY> [fixed|anchor|自定义基数]")
            return
        sym, side = args[1].upper(), args[2].lower()
        qty, entry = float(args[3]), float(args[4])
        if side not in ('long', 'short'):
            print("side 必须是 long 或 short")
            return
        mode = 'fixed'
        custom_base = None
        if len(args) > 5:
            m = args[5].lower()
            if m in ('fixed', 'anchor'):
                mode = m
            else:
                try:
                    custom_base = float(m)
                    mode = 'custom'
                except ValueError:
                    print("mode 必须是 fixed/anchor 或具体数字(自定义马丁基数, 如 90)")
                    return
        mgr.add_anchor(sym, side, qty, entry, mode, custom_base)
    elif cmd == 'confirm':
        sym = args[1] if len(args) > 1 else ''
        entry = float(args[2]) if len(args) > 2 else None
        qty = float(args[3]) if len(args) > 3 else None
        mgr.confirm_add(sym, entry, qty)
    elif cmd == 'reduce':
        mgr.confirm_reduce(args[1]) if len(args) > 1 else print("用法: reduce <SYMBOL>")
    elif cmd == 'remove':
        mgr.remove(args[1]) if len(args) > 1 else print("用法: remove <SYMBOL>")
    elif cmd == 'unignore':
        mgr.unignore(args[1]) if len(args) > 1 else print("用法: unignore <SYMBOL>")
    elif cmd == 'atrmult':
        if len(args) < 3:
            print("用法: atrmult <SYMBOL> <乘数>   (如 atrmult BTC 0.5)")
        else:
            mgr.set_atr_mult(args[1], float(args[2]))
    elif cmd == 'trendfilter':
        if len(args) < 3:
            print("用法: trendfilter <SYMBOL> <on|off>   (如 trendfilter XRP on)")
        else:
            mgr.set_trend_filter(args[1], args[2].lower() in ('on', 'true', '1', 'yes'))
    elif cmd == 'sync':
        mgr.sync()
    elif cmd == 'journal':
        show_journal(args[1:] if len(args) > 1 else [])
    elif cmd == 'watch':
        interval = int(args[1]) if len(args) > 1 else 60
        watch(mgr, interval)
    elif cmd == 'run':
        alerts = mgr.run()
        if alerts:
            for a in alerts:
                print(a['content'])
                print('---')
    else:
        print("用法: manual_grid_atr.py [status|add|confirm|reduce|remove|unignore|atrmult|trendfilter|sync|journal|run|watch]")


if __name__ == '__main__':
    main()
