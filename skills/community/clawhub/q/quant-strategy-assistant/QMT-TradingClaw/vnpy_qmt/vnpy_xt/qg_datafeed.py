from datetime import datetime, timedelta, time
from math import isnan
from typing import Optional, Callable
from pandas import DataFrame, concat as pd_concat
import qgdata as qg
from vnpy.trader.setting import SETTINGS
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData, TickData, HistoryRequest
from vnpy.trader.utility import ZoneInfo
from vnpy.trader.datafeed import BaseDatafeed

CHINA_TZ = ZoneInfo("Asia/Shanghai")
GATEWAY_NAME = "QG"
try:
    from qg_constants import QGDATA_RECHARGE_URL, classify_qgdata_error
except ImportError:
    import sys as _sys, os as _os; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "backtests"))
    from qg_constants import QGDATA_RECHARGE_URL, classify_qgdata_error
PAGE_SIZE = 5000 #qgdata单次最大返回条数

EXCHANGE_VT2QG: dict[Exchange, str] = { #VeighNa交易所 -> qgdata后缀(仅A股市场)
    Exchange.SSE: "SH", Exchange.SZSE: "SZ", Exchange.BSE: "BJ",
}
EXCHANGE_QG2VT: dict[str, Exchange] = {v: k for k, v in EXCHANGE_VT2QG.items()} #反向映射

INTERVAL_VT2QG_API: dict[Interval, str] = { #VeighNa周期 -> qgdata接口名
    Interval.MINUTE: "stk_mins", Interval.HOUR: "stk_mins",
    Interval.DAILY: "daily", Interval.WEEKLY: "weekly",
}
INTERVAL_VT2QG_FREQ: dict[Interval, str] = { #VeighNa周期 -> qgdata freq参数(仅stk_mins)
    Interval.MINUTE: "5min", Interval.HOUR: "60min",  #MINUTE默认5分钟线（A股最常用的分钟级别）
}
_MINUTE_FREQ_OVERRIDE: str = ""  #运行时可覆盖：如设为"1min"则加载1分钟线

def _safe_float(val, default: float = 0.0) -> float: #安全的float转换，处理None/NaN/空字符串
    if val is None:
        return default
    try:
        f = float(val)
        return default if isnan(f) else f
    except (ValueError, TypeError):
        return default

def _vt_symbol_to_qg(symbol: str, exchange: Exchange) -> Optional[str]: #合约代码转qgdata格式，不支持的交易所返回None
    suffix = EXCHANGE_VT2QG.get(exchange)
    return f"{symbol}.{suffix}" if suffix else None

def _parse_daily_dt(trade_date: str) -> datetime: #日线日期字符串 -> datetime
    dt = datetime.strptime(str(trade_date).split(" ")[0].replace("-", "")[:8], "%Y%m%d")
    return dt.replace(hour=15, tzinfo=CHINA_TZ)

def _parse_mins_dt(trade_time: str) -> datetime: #分钟线时间字符串 -> datetime
    s = str(trade_time).replace("-", "").replace(":", "").replace(" ", "")
    if len(s) >= 14: dt = datetime.strptime(s[:14], "%Y%m%d%H%M%S")
    elif len(s) >= 12: dt = datetime.strptime(s[:12], "%Y%m%d%H%M")
    else: dt = datetime.strptime(s[:8], "%Y%m%d")
    return dt.replace(tzinfo=CHINA_TZ)


class QgDatafeed(BaseDatafeed):
    """qgdata数据服务接口 - VeighNa回测首选数据源（仅支持A股市场：SSE/SZSE/BSE）"""

    def __init__(self):
        self.username: str = SETTINGS.get("datafeed.username", "")
        self.password: str = SETTINGS.get("datafeed.password", "")
        self.inited: bool = False
        self.pro = None

    def init(self, output: Callable = print) -> bool:
        if self.inited:
            return True
        try:
            token = self.password or self.username #优先用password字段存token
            if not token:
                output(f"qgdata数据服务初始化失败：未配置token，请在datafeed.password中填写。获取Token: {QGDATA_RECHARGE_URL}")
                return False
            qg.set_token(token)
            self.pro = qg.pro_api(timeout=30.0)
            df = self.pro.trade_cal(exchange="SSE", limit=1) #验证连接
            if df is None or df.empty:
                output(f"qgdata数据服务初始化失败：连接验证未通过。充值/获取Token: {QGDATA_RECHARGE_URL}")
                return False
        except Exception as ex:
            _, user_msg = classify_qgdata_error(ex)
            output(f"qgdata数据服务初始化失败: {user_msg}")
            return False
        self.inited = True
        return True

    def _fetch_all(self, api_name: str, **kwargs) -> DataFrame: #自动分页拉取全量数据
        frames = []
        offset = 0
        while True:
            df = self.pro.query(api_name, limit=PAGE_SIZE, offset=offset, **kwargs)
            if df is None or df.empty:
                break
            frames.append(df)
            if len(df) < PAGE_SIZE:
                break
            offset += PAGE_SIZE
        return DataFrame() if not frames else pd_concat(frames, ignore_index=True)

    def query_bar_history(self, req: HistoryRequest, output: Callable = print) -> Optional[list[BarData]]:
        history: list[BarData] = []
        if not self.inited and not self.init(output):
            return history
        api_name = INTERVAL_VT2QG_API.get(req.interval)
        if not api_name:
            output(f"qgdata查询历史数据失败：不支持的时间周期{req.interval.value}")
            return history
        ts_code = _vt_symbol_to_qg(req.symbol, req.exchange)
        if not ts_code: #交易所不在qgdata支持范围
            output(f"qgdata仅支持A股市场(SSE/SZSE/BSE)，不支持{req.exchange.value}，请切换至迅投研(XT)数据源")
            return history
        start_str = req.start.strftime("%Y%m%d")
        end_str = req.end.strftime("%Y%m%d")
        try:
            if api_name == "stk_mins": #分钟级数据
                freq = _MINUTE_FREQ_OVERRIDE if (_MINUTE_FREQ_OVERRIDE and req.interval == Interval.MINUTE) else INTERVAL_VT2QG_FREQ[req.interval]
                df = self._fetch_all(api_name, ts_code=ts_code, freq=freq, start_date=start_str, end_date=end_str,
                    fields="ts_code,trade_time,open,high,low,close,vol,amount", order_by="trade_time", sort="asc")
            elif api_name == "weekly": #周线数据
                df = self._fetch_all(api_name, ts_code=ts_code, start_date=start_str, end_date=end_str,
                    fields="ts_code,trade_date,open,high,low,close,vol,amount,pre_close,change", order_by="trade_date", sort="asc")
            else: #日线数据
                df = self._fetch_all(api_name, ts_code=ts_code, start_date=start_str, end_date=end_str,
                    fields="ts_code,trade_date,open,high,low,close,vol,amount,pre_close,change", order_by="trade_date", sort="asc")
        except Exception as ex:
            _, user_msg = classify_qgdata_error(ex)
            output(f"qgdata查询历史数据异常: {user_msg}")
            return history
        if df is None or df.empty:
            return history
        is_mins = api_name == "stk_mins"
        for _, row in df.iterrows():
            dt = _parse_mins_dt(row["trade_time"]) if is_mins else _parse_daily_dt(row["trade_date"])
            if req.interval == Interval.DAILY: #日线过滤未完成的当日数据
                if dt.date() == datetime.now().date() and datetime.now().time() < time(hour=15):
                    continue
            bar = BarData(
                symbol=req.symbol, exchange=req.exchange, datetime=dt, interval=req.interval,
                open_price=_safe_float(row.get("open")), high_price=_safe_float(row.get("high")),
                low_price=_safe_float(row.get("low")), close_price=_safe_float(row.get("close")),
                volume=_safe_float(row.get("vol")), turnover=_safe_float(row.get("amount")),
                open_interest=0, gateway_name=GATEWAY_NAME,
            )
            history.append(bar)
        return history

    def query_tick_history(self, req: HistoryRequest, output: Callable = print) -> Optional[list[TickData]]:
        output("qgdata数据源暂不支持Tick数据查询，请使用迅投研(XT)数据源获取Tick数据")
        return []
