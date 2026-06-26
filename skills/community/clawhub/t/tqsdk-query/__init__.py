import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Union

from tqsdk import TqApi, TqAuth
from .tqsdk_client import TqSdkClient  # 可选封装


def handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Skill 入口函数，由 Clawdbot 调用。
    params 包含用户传入的所有参数（按 SKILL.md 定义）。
    返回一个字典，包含 result 或 error。
    """
    # 从环境变量读取天勤账号
    username = os.environ.get("TQ_USERNAME")
    password = os.environ.get("TQ_PASSWORD")
    
    if not username or not password:
        return {"text": "错误：未设置天勤账号。请设置环境变量 TQ_USERNAME 和 TQ_PASSWORD。"}
    
    action = params.get("action")
    symbol = params.get("symbol")
    
    # 处理多合约符号（支持逗号分隔）
    symbols = [s.strip() for s in symbol.split(",")] if symbol else []
    
    # 根据 action 调用不同逻辑
    if action == "get_quote":
        return asyncio.run(_get_quote(username, password, symbols))
    elif action == "get_kline_serial":
        duration = params.get("duration_seconds", 60)
        data_length = params.get("data_length", 200)
        return asyncio.run(_get_kline_serial(username, password, symbols, duration, data_length))
    elif action == "get_kline_data":
        duration = params.get("duration_seconds", 3600)
        start_dt = datetime.fromisoformat(params["start_dt"]) if params.get("start_dt") else None
        end_dt = datetime.fromisoformat(params["end_dt"]) if params.get("end_dt") else None
        if not start_dt or not end_dt:
            return {"text": "错误：历史数据查询需要提供 start_dt 和 end_dt 参数。"}
        return asyncio.run(_get_kline_data(username, password, symbols[0], duration, start_dt, end_dt))
    else:
        return {"text": f"未知操作: {action}。支持的操作: get_quote, get_kline_serial, get_kline_data"}


async def _get_quote(username: str, password: str, symbols: List[str]) -> Dict:
    """
    获取实时盘口数据
    """
    api = TqApi(auth=TqAuth(username, password))
    try:
        quotes = []
        for sym in symbols:
            quote = api.get_quote(sym)
            # 等待至少一次更新确保数据有效
            await api.wait_update()
            quotes.append({
                "symbol": sym,
                "last_price": quote.last_price,
                "ask_price1": quote.ask_price1,
                "ask_volume1": quote.ask_volume1,
                "bid_price1": quote.bid_price1,
                "bid_volume1": quote.bid_volume1,
                "volume": quote.volume,
                "open_interest": quote.open_interest,
                "datetime": str(quote.datetime),
                "highest": quote.highest,
                "lowest": quote.lowest,
                "open": quote.open,
                "close": quote.close,
                "pre_settlement": quote.pre_settlement,
            })
        # 构造可读文本
        text_lines = []
        for q in quotes:
            text_lines.append(
                f"{q['symbol']}: 最新价 {q['last_price']} | 买一 {q['bid_price1']}/{q['bid_volume1']} | "
                f"卖一 {q['ask_price1']}/{q['ask_volume1']} | 成交量 {q['volume']} | 时间 {q['datetime']}"
            )
        return {"text": "\n".join(text_lines), "result": quotes}
    finally:
        await api.close()


async def _get_kline_serial(username: str, password: str, symbols: List[str], duration: int, length: int) -> Dict:
    """
    获取实时K线序列（动态更新，返回最新N条）
    """
    api = TqApi(auth=TqAuth(username, password))
    try:
        # 如果 symbols 是单个，get_kline_serial 返回 DataFrame；多个时返回带后缀的 DataFrame
        if len(symbols) == 1:
            klines = api.get_kline_serial(symbols[0], duration, data_length=length)
        else:
            klines = api.get_kline_serial(symbols, duration, data_length=length)
        
        await api.wait_update()  # 确保至少获取一次数据
        
        # 将最后一条K线数据转换为字典
        last = klines.iloc[-1].to_dict()
        # 将 numpy 类型转为 Python 原生类型
        for k, v in last.items():
            if hasattr(v, 'item'):
                last[k] = v.item()
            elif isinstance(v, (int, float, str)):
                pass
            else:
                last[k] = str(v)
        # 构造可读文本
        text = f"最新{'' if len(symbols)==1 else '多合约'}K线（周期{duration}秒）：\n"
        text += f"时间 {last.get('datetime', 'N/A')} | 开 {last.get('open')} 高 {last.get('high')} "
        text += f"低 {last.get('low')} 收 {last.get('close')} | 成交量 {last.get('volume')}"
        return {"text": text, "result": {"last_kline": last, "data_length": len(klines)}}
    finally:
        await api.close()


async def _get_kline_data(username: str, password: str, symbol: str, duration: int,
                          start_dt: datetime, end_dt: datetime) -> Dict:
    """
    获取历史K线数据（静态）
    """
    api = TqApi(auth=TqAuth(username, password))
    try:
        data = api.get_kline_data_series(
            symbol=symbol,
            duration_seconds=duration,
            start_dt=start_dt,
            end_dt=end_dt
        )
        # 将 DataFrame 转换为记录列表
        records = data.to_dict(orient="records")
        # 处理时间戳
        for rec in records:
            if "datetime" in rec:
                rec["datetime"] = str(rec["datetime"])
        count = len(records)
        text = f"获取到 {count} 条 {symbol} 的{'' if count else '无'}历史K线（周期{duration}秒）"
        if count > 0:
            latest = records[-1]
            text += f"，最新一条：时间 {latest.get('datetime')} 收 {latest.get('close')}"
        return {"text": text, "result": {"count": count, "data": records}}
    except Exception as e:
        return {"text": f"获取历史K线失败: {str(e)}", "error": str(e)}
    finally:
        await api.close()