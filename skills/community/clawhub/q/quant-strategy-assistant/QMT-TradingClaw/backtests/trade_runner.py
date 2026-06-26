# -*- coding: utf-8 -*-
"""实盘/模拟交易执行器 - headless vnpy CTA引擎 + XtGateway + BarGenerator注入 + 账户模型"""
import sys, os, time, json, signal, argparse, importlib.util, platform, threading, string
from pathlib import Path
from datetime import datetime, timedelta, time as dtime

PROJECT_ROOT = Path(os.getenv("QUANTCLAW_ROOT", "") or os.getenv("QMT_PROJECT_ROOT", "") or str(Path(__file__).resolve().parents[1])).resolve()
sys.path.insert(0, str(PROJECT_ROOT / "vnpy_qmt"))
sys.path.insert(0, str(PROJECT_ROOT / "strategies"))
sys.path.insert(0, str(PROJECT_ROOT / "backtests"))

from vnpy.event import EventEngine, EVENT_TIMER
from vnpy.trader.engine import MainEngine
from vnpy.trader.constant import Exchange, Interval, Direction, Offset
from vnpy.trader.object import SubscribeRequest, OrderData, TradeData, AccountData, PositionData, BarData, TickData, ContractData
from vnpy.trader.event import EVENT_ACCOUNT, EVENT_POSITION, EVENT_ORDER, EVENT_TRADE
from vnpy.trader.utility import BarGenerator
from vnpy.trader.setting import SETTINGS

TRADE_STATE_FILE = "trade_state.json"
RATE = 0.0003
_running = True
_log_lines = []

def p(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[trade][{ts}] {msg}"
    print(line, flush=True)
    _log_lines.append(line)
    if len(_log_lines) > 2000: _log_lines.pop(0)

def _sig_handler(sig, _frame):
    global _running
    p(f"收到信号 {sig}，准备停止...")
    _running = False
signal.signal(signal.SIGINT, _sig_handler)
signal.signal(signal.SIGTERM, _sig_handler)

# ═══════════════ QMT 路径自动发现 ═══════════════
def auto_discover_qmt_path() -> str:
    """返回 QMT 安装目录（含 userdata_mini 的父目录），优先级：环境变量→进程反推→目录扫描"""
    env = os.environ.get("QMT_PATH", "")
    if env and (Path(env) / "userdata_mini").is_dir(): return env
    if platform.system() != "Windows": return ""
    try: #从运行中的 miniQMT 进程可执行路径反推安装目录
        import subprocess as _sp
        out = _sp.check_output('wmic process where "name like \'%XtMiniQmt%\' or name like \'%miniQMT%\'" get ExecutablePath /value', text=True, timeout=5, stderr=_sp.DEVNULL)
        for line in out.splitlines():
            if "=" in line:
                exe = line.split("=", 1)[1].strip()
                if exe:
                    candidate = Path(exe).parent
                    if (candidate / "userdata_mini").is_dir(): return str(candidate)
                    if (candidate.parent / "userdata_mini").is_dir(): return str(candidate.parent)
    except Exception: pass
    for drive in string.ascii_uppercase: #兜底：目录扫描
        root = Path(f"{drive}:\\")
        if not root.exists(): continue
        for parent in [root, root / "Program Files", root / "Program Files (x86)"]:
            if not parent.exists(): continue
            try:
                for item in parent.iterdir():
                    if item.is_dir() and ("qmt" in item.name.lower() or "迅投" in item.name):
                        if (item / "userdata_mini").is_dir(): return str(item)
            except PermissionError: continue
    return ""

# ═══════════════ 策略类动态加载 ═══════════════
def load_strategy_class(strategy_file: str, class_name: str):
    spec = importlib.util.spec_from_file_location("_dyn_strategy", strategy_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cls = getattr(mod, class_name, None)
    if cls is None:
        raise ImportError(f"策略文件 {strategy_file} 中未找到类 {class_name}")
    return cls

# ═══════════════ BarGenerator 注入（日线策略核心） ═══════════════
def inject_bar_generator(strategy, interval: Interval):
    """注入 tick→1min→目标周期 的 BarGenerator 链，使日线策略在 live 模式下正确运行"""
    if interval not in (Interval.DAILY, Interval.WEEKLY):
        _bg_tick = BarGenerator(strategy.on_bar)
        strategy.on_tick = lambda tick: _bg_tick.update_tick(tick)
        p(f"[inject] 分钟策略 BarGenerator 已注入 (tick→1min→on_bar)")
        return
    _real_on_bar = strategy.on_bar
    _bg_daily = BarGenerator(on_bar=lambda b: None, window=0, on_window_bar=_real_on_bar, interval=Interval.DAILY, daily_end=dtime(15, 0))
    _bg_tick = BarGenerator(on_bar=_bg_daily.update_bar)
    strategy.on_tick = lambda tick: _bg_tick.update_tick(tick)
    p(f"[inject] 日线策略 BarGenerator 已注入 (tick→1min→daily@15:00→on_bar)")

def patch_load_bar(strategy, cta_engine, vt_symbol, interval: Interval):
    """patch load_bar：强制加载日线历史，直喂策略 on_bar 初始化 ArrayManager"""
    _real_on_bar = strategy.on_bar
    def _patched(days=10, interval_arg=None, callback=None, use_database=False):
        target_interval = Interval.DAILY if interval in (Interval.DAILY, Interval.WEEKLY) else Interval.MINUTE
        cb = callback or _real_on_bar
        p(f"[load_bar] 加载 {days} 天 {target_interval.value} 历史数据...")
        bars = cta_engine.load_bar(vt_symbol, days, target_interval, cb, use_database)
        p(f"[load_bar] 获取 {len(bars)} 根 bar，逐根回放...")
        for bar in bars: cb(bar)
        p(f"[load_bar] 回放完成，ArrayManager 应已初始化")
    strategy.load_bar = _patched

# ═══════════════ LiveAccountBridge（账户模型注入） ═══════════════
def patch_live_account(cta_engine, strategy, capital: float, rate: float, mode: str = "cta", vt_symbols: list = None):
    """live 版账户模型：同步预扣/回款，注入 available_cash 等属性，复用 backtest_runner 逻辑"""
    acct = {"cash": float(capital), "real_cash": None, "last_price": 0.0, "last_prices": {}, "stats": {"orders": 0, "fills": 0}}
    def _lot_floor(vt_symbol, vol):
        digits = "".join(c for c in str(vt_symbol or "") if c.isdigit())[:6]
        if digits.startswith("688"): return int(vol) if int(vol) >= 200 else 0
        return int(int(vol) / 100) * 100
    def _inject_cta():
        pos = int(strategy.pos)
        mv = pos * acct["last_price"]
        strategy.available_cash = acct["cash"]; strategy.total_value = acct["cash"] + mv
        strategy.positions_value = mv; strategy.capital = acct["cash"]
        strategy.closable_pos = pos
    def _inject_portfolio():
        pv = 0.0; closable = {}
        for sym in (vt_symbols or []):
            pos = int(strategy.get_pos(sym)) if hasattr(strategy, 'get_pos') else 0
            px = acct["last_prices"].get(sym, 0.0)
            pv += abs(pos) * px; closable[sym] = pos
        strategy.available_cash = acct["cash"]; strategy.total_value = acct["cash"] + pv
        strategy.positions_value = pv; strategy.capital = acct["cash"]
        strategy.closable_positions = closable
    _inject = _inject_cta if mode == "cta" else _inject_portfolio
    _inject()
    _orig_send = cta_engine.send_order
    if mode == "cta":
        def _send_wrap(strat, direction, offset, price, volume, stop, lock, net):
            sym = getattr(strat, "vt_symbol", ""); vol = _lot_floor(sym, int(volume)); price_f = float(price)
            if vol <= 0: p(f"[账户] {sym} 下单{int(volume)}股不满足最小手数"); return []
            acct["last_price"] = price_f
            if direction == Direction.LONG:
                cost = price_f * vol * (1 + rate)
                if cost > acct["cash"] + 0.01:
                    affordable = _lot_floor(sym, int(acct["cash"] / (price_f * (1 + rate))))
                    if affordable <= 0: p(f"[账户] 买入{vol}股被拒：需{cost:.0f}，可用{acct['cash']:.0f}"); return []
                    p(f"[账户] 买入{vol}→{affordable}股"); vol = affordable
                result = _orig_send(strat, direction, offset, price, vol, stop, lock, net)
                if result: acct["cash"] -= price_f * vol * (1 + rate); acct["stats"]["orders"] += 1; _inject()
                return result
            else:
                result = _orig_send(strat, direction, offset, price, vol, stop, lock, net)
                if result: acct["cash"] += price_f * vol * (1 - rate); acct["stats"]["orders"] += 1; _inject()
                return result
        cta_engine.send_order = _send_wrap
    else:
        def _send_wrap_p(strat, vt_symbol, direction, offset, price, volume, lock, net):
            vol = _lot_floor(vt_symbol, int(volume)); price_f = float(price)
            if vol <= 0: p(f"[账户] {vt_symbol} 下单{int(volume)}股不满足最小手数"); return []
            acct["last_prices"][vt_symbol] = price_f
            if direction == Direction.LONG:
                cost = price_f * vol * (1 + rate)
                if cost > acct["cash"] + 0.01:
                    affordable = _lot_floor(vt_symbol, int(acct["cash"] / (price_f * (1 + rate))))
                    if affordable <= 0: p(f"[账户] {vt_symbol} 买入{vol}股被拒"); return []
                    vol = affordable
                result = _orig_send(strat, vt_symbol, direction, offset, price, vol, lock, net)
                if result: acct["cash"] -= price_f * vol * (1 + rate); acct["stats"]["orders"] += 1; _inject()
                return result
            else:
                result = _orig_send(strat, vt_symbol, direction, offset, price, vol, lock, net)
                if result: acct["cash"] += price_f * vol * (1 - rate); acct["stats"]["orders"] += 1; _inject()
                return result
        cta_engine.send_order = _send_wrap_p
    def _on_tick(event):
        tick: TickData = event.data
        if tick.last_price > 0:
            if mode == "cta":
                if tick.vt_symbol == getattr(strategy, "vt_symbol", ""): acct["last_price"] = tick.last_price
            else:
                if tick.vt_symbol in (vt_symbols or []): acct["last_prices"][tick.vt_symbol] = tick.last_price
    def _on_account(event):
        data: AccountData = event.data
        acct["real_cash"] = data.available
        drift = abs(acct["cash"] - data.available) / max(data.available, 1)
        if drift > 0.01 and acct["stats"]["orders"] > 0:
            p(f"[账户] 校正: 本地{acct['cash']:.0f} → 网关{data.available:.0f} (偏差{drift:.1%})")
            acct["cash"] = data.available; _inject()
    def _on_trade(event):
        trade: TradeData = event.data
        acct["stats"]["fills"] += 1
        if mode == "cta": acct["last_price"] = trade.price
        else: acct["last_prices"][trade.vt_symbol] = trade.price
        _inject()
        p(f"[成交] {trade.vt_symbol} {trade.direction.value} {trade.volume}@{trade.price}")
    return acct, _on_tick, _on_account, _on_trade

# ═══════════════ 探针单（验证QMT通信） ═══════════════
def probe_order(main_engine, gateway_name: str, vt_symbol: str, mock: bool = False) -> bool:
    """发100股跌停价买单→确认委托→撤单→确认撤单，验证 QMT 下单链路"""
    if mock:
        p("[探针] mock模式，跳过探针单")
        return True
    p(f"[探针] 正在验证 QMT 下单链路 ({vt_symbol})...")
    symbol, exchange_str = vt_symbol.split(".")
    exchange = Exchange[exchange_str]
    contract: ContractData = main_engine.get_contract(vt_symbol)
    if not contract:
        p(f"[探针] 找不到合约 {vt_symbol}，跳过探针（可能非交易时段）")
        return True
    from vnpy.trader.object import OrderRequest, CancelRequest
    from vnpy.trader.constant import OrderType
    try:
        from vnpy_xt.xt_gateway import symbol_limit_map
        limits = symbol_limit_map.get(vt_symbol)
    except ImportError:
        limits = None
    if limits and limits[1] > 0:
        probe_price = round(limits[1] - contract.pricetick, 2) #略低于跌停价
    else:
        probe_price = round(contract.pricetick * 100, 2) or 0.01
    req = OrderRequest(symbol=symbol, exchange=exchange, direction=Direction.LONG, type=OrderType.LIMIT, price=probe_price, volume=100, offset=Offset.NONE)
    p(f"[探针] 发送探针单: {vt_symbol} 买入100股@{probe_price}")
    vt_orderid = main_engine.send_order(req, gateway_name)
    if not vt_orderid:
        p("[探针] 探针单发送失败，QMT 通信可能异常")
        return False
    p(f"[探针] 探针单已发送: {vt_orderid}，等待 QMT 确认...")
    time.sleep(3)
    cancel_req = CancelRequest(orderid=vt_orderid.split(".")[-1], symbol=symbol, exchange=exchange)
    main_engine.cancel_order(cancel_req, gateway_name)
    p(f"[探针] 撤单已发送，等待确认...")
    time.sleep(2)
    p("[探针] ✅ QMT 下单链路验证完成（探针单已撤销）")
    return True

# ═══════════════ 状态写入 ═══════════════
def write_state(state_dir: Path, status: str, extra: dict = None):
    data = {"pid": os.getpid(), "status": status, "updated_at": datetime.now().isoformat(), "platform": platform.system(), "log_tail": _log_lines[-20:]}
    if extra: data.update(extra)
    try:
        sf = state_dir / TRADE_STATE_FILE
        sf.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        p(f"[state] 写入失败: {e}")

# ═══════════════ Mock Gateway（Linux 测试用） ═══════════════
class MockGateway:
    """最小 mock：不连真实 QMT，模拟合约查询和下单回报"""
    def __init__(self, event_engine, vt_symbols):
        self.event_engine = event_engine
        for sym in vt_symbols:
            symbol, exchange_str = sym.split(".")
            contract = ContractData(symbol=symbol, exchange=Exchange[exchange_str], name=f"Mock-{symbol}", product=None, size=1, pricetick=0.01, gateway_name="MOCK")
            contract.history_data = False
            from vnpy.trader.event import EVENT_CONTRACT
            from vnpy.event import Event
            event_engine.put(Event(EVENT_CONTRACT, contract))
    @staticmethod
    def connect(*a, **kw): pass
    @staticmethod
    def close(): pass

# ═══════════════ 主函数 ═══════════════
def main():
    global _running
    ap = argparse.ArgumentParser(description="QuantClaw 实盘/模拟交易执行器")
    ap.add_argument("--strategy-file", default="", help="策略文件（--probe-only 时可省略）")
    ap.add_argument("--strategy-class", default="")
    ap.add_argument("--symbols", required=True, help="逗号分隔 vt_symbol")
    ap.add_argument("--mode", default="cta", choices=["cta", "portfolio"])
    ap.add_argument("--interval", default="DAILY")
    ap.add_argument("--capital", type=float, default=1000000)
    ap.add_argument("--rate", type=float, default=RATE)
    ap.add_argument("--state-dir", default="")
    ap.add_argument("--mock", action="store_true", help="Linux mock模式，不连真实QMT")
    ap.add_argument("--datafeed-name", default="xt", help="datafeed: xt(默认,QgDatafeed)")
    ap.add_argument("--datafeed-token", default="")
    ap.add_argument("--qmt-path", default="", help="QMT安装目录（留空自动发现）")
    ap.add_argument("--account-id", default="", help="资金账号（留空读 QMT_ACCOUNT_ID 环境变量）")
    ap.add_argument("--probe-only", action="store_true", help="仅执行探针单验证后退出")
    args = ap.parse_args()

    vt_symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    interval = Interval(args.interval) if args.interval in [i.value for i in Interval] else Interval.DAILY
    state_dir = Path(args.state_dir) if args.state_dir else Path(".")
    state_dir.mkdir(parents=True, exist_ok=True)
    is_probe = args.probe_only
    total_steps = 2 if is_probe else 7

    p(f"========== QuantClaw Trade Runner {'(探针模式)' if is_probe else ''} ==========")
    if not is_probe: p(f"策略: {args.strategy_file} :: {args.strategy_class}")
    p(f"标的: {vt_symbols}  模式: {args.mode}  周期: {interval.value}")
    p(f"资金: {args.capital}  费率: {args.rate}  mock: {args.mock}")
    write_state(state_dir, "initializing")

    # ═══ ① 创建引擎 + 连接 QMT（最先执行，失败则后续全部无意义） ═══
    p(f"[1/{total_steps}] 创建引擎 + 连接 QMT...")
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    gateway_name = "MOCK" if args.mock else "XT"
    if args.mock:
        p("  [mock] 使用 MockGateway")
        MockGateway(event_engine, vt_symbols)
    else:
        if platform.system() != "Windows":
            p("  ⚠️ 非 Windows 系统，XtGateway 可能不可用，建议使用 --mock")
        from vnpy_xt import XtGateway
        main_engine.add_gateway(XtGateway)
        qmt_path = args.qmt_path or auto_discover_qmt_path()
        account_id = args.account_id or os.environ.get("QMT_ACCOUNT_ID", "")
        if not qmt_path:
            p("  ✗ 未找到 QMT 安装路径（--qmt-path / QMT_PATH / 自动扫描均未命中）")
            write_state(state_dir, "error", {"error": "未找到QMT路径"})
            return 1
        if not account_id:
            p("  ✗ 缺少资金账号（--account-id / QMT_ACCOUNT_ID）")
            write_state(state_dir, "error", {"error": "缺少资金账号"})
            return 1
        setting = {"token": "", "股票市场": "是", "期货市场": "否", "期权市场": "否", "仿真交易": "是", "账号类型": "股票", "QMT路径": qmt_path, "资金账号": account_id}
        p(f"  连接 XtGateway (QMT={qmt_path}, 账号=***{account_id[-4:]})...")
        main_engine.connect(setting, gateway_name)
        p("  等待网关连接 + 合约加载...")
        time.sleep(8)
    p(f"  ✓ 引擎就绪 (gateway={gateway_name})")

    # ═══ ② 探针单验证 QMT 通信（在加载策略之前，fail fast） ═══
    p(f"[2/{total_steps}] 探针单验证 QMT 通信...")
    write_state(state_dir, "probing")
    probe_ok = probe_order(main_engine, gateway_name, vt_symbols[0], mock=args.mock)
    if not probe_ok:
        p("  ⚠️ 探针单失败（可能非交易时段），继续...")

    if is_probe: #探针模式：验证完即退出
        p("探针验证完成，退出")
        try: main_engine.close()
        except: pass
        write_state(state_dir, "probe_done", {"probe_ok": probe_ok})
        return 0 if probe_ok else 1

    # ═══ ③ 加载策略类 ═══
    if not args.strategy_file or not args.strategy_class:
        p("  ✗ 缺少 --strategy-file / --strategy-class")
        write_state(state_dir, "error", {"error": "缺少策略文件/类名"})
        main_engine.close(); return 1
    p(f"[3/{total_steps}] 加载策略类...")
    strategy_cls = load_strategy_class(args.strategy_file, args.strategy_class)
    p(f"  ✓ 策略类 {args.strategy_class} 加载成功")

    # ═══ ④ 配置 datafeed + 注册策略 + 注入 ═══
    p(f"[4/{total_steps}] 配置 datafeed + 注册策略 + 注入...")
    SETTINGS["datafeed.name"] = args.datafeed_name
    if args.datafeed_token: SETTINGS["datafeed.password"] = args.datafeed_token

    from vnpy_ctastrategy import CtaStrategyApp
    cta_engine = main_engine.add_app(CtaStrategyApp)
    instance_name = "auto_trade"
    cta_engine.classes[args.strategy_class] = strategy_cls
    cta_engine.add_strategy(args.strategy_class, instance_name, vt_symbols[0], {})
    strategy = cta_engine.strategies.get(instance_name)
    if not strategy:
        p("  ✗ 策略实例创建失败")
        write_state(state_dir, "error", {"error": "策略实例创建失败"})
        main_engine.close(); return 1

    inject_bar_generator(strategy, interval)
    patch_load_bar(strategy, cta_engine, vt_symbols[0], interval)
    acct, on_tick_cb, on_account_cb, on_trade_cb = patch_live_account(cta_engine, strategy, args.capital, args.rate, args.mode, vt_symbols)
    from vnpy.trader.event import EVENT_TICK
    event_engine.register(EVENT_TICK, on_tick_cb)
    event_engine.register(EVENT_ACCOUNT, on_account_cb)
    event_engine.register(EVENT_TRADE, on_trade_cb)
    p("  ✓ datafeed + BarGenerator + AccountBridge 注入完成")

    # ═══ ⑤ 初始化策略（load_bar + ArrayManager 预热） ═══
    p(f"[5/{total_steps}] 初始化策略 (load_bar 预热)...")
    write_state(state_dir, "initializing_strategy")
    cta_engine.init_strategy(instance_name)
    time.sleep(2)
    if not strategy.inited:
        p("  等待 init 完成...")
        for _ in range(30):
            time.sleep(1)
            if strategy.inited: break
    if not strategy.inited:
        p("  ✗ 策略初始化超时")
        write_state(state_dir, "error", {"error": "策略初始化超时"})
        main_engine.close(); return 1
    p("  ✓ 策略初始化完成")

    # ═══ ⑥ 启动策略 ═══
    p(f"[6/{total_steps}] 启动策略交易...")
    cta_engine.start_strategy(instance_name)
    if not strategy.trading:
        p("  ✗ 策略启动失败")
        write_state(state_dir, "error", {"error": "策略启动失败"})
        main_engine.close(); return 1
    p("  ✓ 策略已启动，开始接收行情和交易")
    p("=" * 50)
    p("交易运行中... Ctrl+C 或 SIGTERM 停止")
    write_state(state_dir, "trading", {"strategy": args.strategy_class, "symbols": vt_symbols})

    # ═══ ⑦ 主循环保活 ═══
    _stop_flag_file = state_dir / "_stop_flag"
    last_report = time.time()
    while _running:
        time.sleep(1)
        if _stop_flag_file.exists():
            p("[stop] 检测到 _stop_flag 文件，准备停止...")
            _running = False; break
        now = time.time()
        if now - last_report >= 30:
            last_report = now
            extra = {"strategy": args.strategy_class, "symbols": vt_symbols, "account": {"cash": round(acct["cash"], 2), "real_cash": acct.get("real_cash")}, "stats": acct["stats"]}
            write_state(state_dir, "trading", extra)

    # ═══ 优雅退出 ═══
    p("正在停止策略...")
    try: cta_engine.stop_strategy(instance_name)
    except Exception as e: p(f"  stop_strategy 异常: {e}")
    p("正在关闭引擎...")
    try: main_engine.close()
    except Exception as e: p(f"  close 异常: {e}")
    if _stop_flag_file.exists():
        try: _stop_flag_file.unlink()
        except: pass
    write_state(state_dir, "stopped")
    p("✅ 交易已停止")
    return 0

if __name__ == "__main__":
    sys.exit(main())
