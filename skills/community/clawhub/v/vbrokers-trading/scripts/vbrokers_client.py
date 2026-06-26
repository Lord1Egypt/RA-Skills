#!/usr/bin/env python3
"""
华盛通 OpenAPI Python 客户端 v2.0
Gateway: http://127.0.0.1:11111
文档: https://quant-open.hstong.com/api-docs
更新: 2026-03-04 — 修正参数格式（嵌套 params 字段 + 驼峰命名）

⚠️ 重要：所有接口请求格式为：
{
    "timeout_sec": 10,
    "params": {
        // 业务参数放这里，驼峰命名
    }
}
"""

import json
import base64
import urllib.request
import urllib.error
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# ============================================================
# 配置
# ============================================================
GATEWAY_URL = "http://127.0.0.1:11111"
TIMEOUT_SEC = 10

# AES 密钥（华盛固定提供）
AES_KEY_B64 = "m+qS04/2CH1OweCnmXZ3TDZkCQS+hBzY"


# ============================================================
# 工具函数
# ============================================================
def encrypt_password(plain_password: str) -> str:
    """
    华盛密码加密：Base64.Encode(AES_ECB_PKCS5(Base64.Decode(AES_KEY), password))
    示例：'123456' → 'W1U8iZIppSE+mBMtzy9vZQ=='
    """
    aes_key = base64.b64decode(AES_KEY_B64)
    cipher = AES.new(aes_key, AES.MODE_ECB)
    padded = pad(plain_password.encode("utf-8"), AES.block_size)
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(encrypted).decode("utf-8")


def call(path: str, params: dict = None) -> dict:
    """
    发起 POST 请求到 Gateway
    格式：{"timeout_sec": N, "params": {...}}
    """
    body = {"timeout_sec": TIMEOUT_SEC}
    if params:
        body["params"] = params
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(f"{GATEWAY_URL}{path}", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=TIMEOUT_SEC + 2)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"ok": False, "err": f"HTTP {e.code}: {e.reason}", "data": None}
    except Exception as e:
        return {"ok": False, "err": str(e), "data": None}


# ============================================================
# 交易登录 / 登出
# ============================================================
def trade_login(password: str) -> dict:
    """交易登录（Gateway重启后必须调用）"""
    encrypted_pwd = encrypt_password(password)
    return call("/trade/TradeLogin", {"password": encrypted_pwd})


def trade_logout() -> dict:
    """交易登出"""
    return call("/trade/TradeLogout")


# ============================================================
# 资金 & 持仓
# ============================================================
def get_account_funds(exchange_type: str = "P") -> dict:
    """
    查询账户资金
    exchange_type: 'K'=港股, 'P'=美股, 'v'=深股通, 't'=沪股通
    返回字段: buyPowerUs(美股购买力), assetBalance(总资产), enableBalance(现金可用)
    """
    return call("/trade/TradeQueryMarginFundInfo", {"exchangeType": exchange_type})


def get_positions(exchange_type: str = "P") -> dict:
    """
    查询持仓列表（必须传 exchangeType，否则报 2001 参数错误）
    exchange_type: 'K'=港股, 'P'=美股（默认美股）
    返回字段: stockCode, stockName, currentAmount(持仓), costPrice(成本价), enableAmount(可卖数量)
    ⚠️ lastPrice/marketValue/incomeBalance 文档标注不可靠，仅供参考
    """
    return call("/trade/TradeQueryHoldsList", {"exchangeType": exchange_type})


def get_today_orders(exchange_type: str = "P", count: int = 20) -> dict:
    """查询当日委托（需传 queryCount + queryParamStr，否则报参数错误）"""
    return call("/trade/TradeQueryRealEntrustList", {
        "exchangeType": exchange_type,
        "queryCount": count,
        "queryParamStr": "0"
    })


def get_today_deals(exchange_type: str = "P", count: int = 20) -> dict:
    """查询当日成交（需传 queryCount + queryParamStr）"""
    return call("/trade/TradeQueryRealDeliverList", {
        "exchangeType": exchange_type,
        "queryCount": count,
        "queryParamStr": "0"
    })


# ============================================================
# 下单 / 撤单
# ============================================================
def place_order(
    stock_code: str,
    exchange_type: str,    # 'K'=港股, 'P'=美股
    entrust_bs: str,       # '1'=买入, '2'=卖出
    amount: int,
    price: float,
    entrust_type: str = "3",     # '3'=限价单, '5'=市价单(美股)
    session_type: str = "1",     # '0'=普通盘中, '1'=支持盘前盘后(美股)
) -> dict:
    """
    下单委托
    示例 - 买入 PANW 1股 限价 $150（盘前盘后）:
        place_order("PANW", "P", "1", 1, 150.00)
    示例 - 卖出 PANW 1股 限价 $165（盘前盘后）:
        place_order("PANW", "P", "2", 1, 165.00)
    示例 - 港股买入 腾讯 100股 限价 380:
        place_order("00700", "K", "1", 100, 380.0, session_type="0")
    """
    return call("/trade/TradeEntrust", {
        "exchangeType": exchange_type,
        "stockCode": stock_code,
        "entrustAmount": str(amount),
        "entrustPrice": str(price),
        "entrustBs": entrust_bs,
        "entrustType": entrust_type,
        "sessionType": session_type,
    })


def cancel_order(
    stock_code: str,
    exchange_type: str,
    entrust_id: str,
    amount: int = None,
    price: float = None,
) -> dict:
    """
    撤单
    entrust_id: 下单时返回的委托编号
    """
    params = {
        "exchangeType": exchange_type,
        "stockCode": stock_code,
        "entrustId": entrust_id,
    }
    if amount:
        params["entrustAmount"] = str(amount)
    if price:
        params["entrustPrice"] = str(price)
    return call("/trade/TradeCancelEntrust", params)


def cancel_all_orders(exchange_type: str) -> dict:
    """批量撤单（撤某市场所有订单）"""
    return call("/trade/TradeBatchCancelEntrust", {"exchangeType": exchange_type})


# ============================================================
# 行情（HTTP 直接查询，无需 WebSocket）
# ============================================================
# dataType 对照：20000=美股，10000=港股，30000=A股
# mktTmType: -1=盘前，1=盘中，-2=盘后，-3=夜盘

def get_quote(stock_code: str, data_type: int = 20000, session: int = None) -> dict:
    """
    HTTP 实时报价（已验证可用）
    POST /hq/BasicQot
    data_type: 20000=美股，10000=港股，30000=A股
    session: -1=盘前，1=盘中，-2=盘后，-3=夜盘，None=自动
    返回: lastPrice, openPrice, highPrice, lowPrice, lastClosePrice, volume, turnover
    示例: get_quote("PANW")         # 美股 PANW
           get_quote("00700", 10000) # 港股腾讯
    """
    params = {
        "security": [{"dataType": data_type, "code": stock_code}],
        "needDelayFlag": "0"
    }
    if session is not None:
        params["mktTmType"] = session
    return call("/hq/BasicQot", params)


def get_quotes_batch(stock_codes: list, data_type: int = 20000, session: int = None) -> list:
    """
    批量实时报价
    session (mktTmType): -1=盘前, 1=盘中, -2=盘后, -3=夜盘, None=默认(收盘价)
    ⚠️ 必须按当前时段传入正确 session，否则默认返回昨日收盘价！
    返回: [{"code", "last", "prev", "pct", "high", "low", "volume", "trade_time"}, ...]
    示例: get_quotes_batch(["PANW","CRWD","ZS"], session=-1)  # 盘前价格
    """
    securities = [{"dataType": data_type, "code": code} for code in stock_codes]
    params = {"security": securities, "needDelayFlag": "0"}
    if session is not None:
        params["mktTmType"] = session
    r = call("/hq/BasicQot", params)
    if not r.get("ok"):
        return []
    results = []
    for q in r.get("data", {}).get("basicQot", []):
        code = q["security"]["code"]
        last = q.get("lastPrice", 0)
        prev = q.get("lastClosePrice", 0)
        pct = (last - prev) / prev * 100 if prev else 0
        results.append({"code": code, "last": last, "prev": prev, "pct": round(pct, 2),
                         "high": q.get("highPrice"), "low": q.get("lowPrice"),
                         "volume": q.get("volume"),
                         "trade_time": q.get("tradeTime", ""),
                         "mkt_type": q.get("mktTmType")})
    return results


def get_klines(stock_code: str, data_type: int = 20000,
               cyc_type: int = 2, limit: int = 20,
               start_date: int = None) -> list:
    """
    实时K线（已验证可用）
    POST /hq/KL
    cyc_type: 2=日线，5=1分钟，6=5分钟，7=15分钟，8=30分钟，9=60分钟
    limit: 日K=条数，分钟K=天数
    示例: get_klines("PANW")           # PANW 20日日线
           get_klines("PANW", cyc_type=9, limit=3) # 最近3天60分钟线
    """
    import datetime
    if start_date is None:
        start_date = int(datetime.date.today().strftime("%Y%m%d"))
    r = call("/hq/KL", {
        "security": {"dataType": data_type, "code": stock_code},
        "startDate": start_date,
        "direction": 0,       # 0=往左（向历史）
        "exRightFlag": 0,     # 0=不复权
        "cycType": cyc_type,
        "limit": limit
    })
    if not r.get("ok"):
        return []
    return r.get("data", {}).get("kline", [])


def get_overnight_list() -> list:
    """获取夜盘可交易股票列表"""
    r = call("/hq/UsOverNightTradeCodes", {})
    if r.get("ok"):
        return r.get("data", {}).get("securityCodes", [])
    return []


# ============================================================
# 止损辅助（Quant 核心功能）
# ============================================================
def check_stop_loss(
    stock_code: str,
    exchange_type: str = "P",
    cost_price: float = None,
    stop_loss_pct: float = 0.08,
    take_profit_pct: float = 0.10,
) -> dict:
    """
    检查是否触达止损/止盈线
    ⚠️ 行情接口为推送协议，无法直接 HTTP 查询实时价格
       当前使用持仓 lastPrice 字段（非交易时间不更新，仅供参考）
    返回: {'action': 'hold'/'stop_loss'/'take_profit', 'current_price': X, 'pnl_pct': X}
    """
    result = get_positions(exchange_type)
    if not result.get("ok"):
        return {"error": result.get("err")}

    holds_list = result.get("data", {}).get("holdsList", [])

    for pos in holds_list:
        if pos.get("stockCode", "").upper() == stock_code.upper():
            cost = float(pos.get("costPrice", cost_price or 0))
            last_price_str = pos.get("lastPrice", "0")
            current = float(last_price_str) if last_price_str else 0

            if current <= 0:
                return {
                    "action": "unknown",
                    "error": "持仓 lastPrice 为 0，可能是非交易时间或行情未推送",
                    "cost_price": cost,
                    "note": "行情接口需 WebSocket 订阅，HTTP 不支持直接查询"
                }

            pnl_pct = (current - cost) / cost
            stop_loss_price = cost * (1 - stop_loss_pct)
            take_profit_price = cost * (1 + take_profit_pct)

            action = "hold"
            if current <= stop_loss_price:
                action = "stop_loss"
            elif current >= take_profit_price:
                action = "take_profit"

            return {
                "action": action,
                "current_price": current,
                "cost_price": cost,
                "pnl_pct": round(pnl_pct * 100, 2),
                "stop_loss_price": round(stop_loss_price, 2),
                "take_profit_price": round(take_profit_price, 2),
                "data_source": "position_lastPrice (not real-time during market close)",
            }

    return {"action": "not_found", "error": f"未找到 {stock_code} 持仓"}


# ============================================================
# 便捷打印
# ============================================================
def pretty(result: dict, title: str = "") -> dict:
    if title:
        print(f"\n{'='*50}")
        print(f"  {title}")
        print(f"{'='*50}")
    if result.get("ok"):
        print("✅ 成功")
        data = result.get("data")
        if data:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 失败: {result.get('err', '未知错误')}")
    return result


# ============================================================
# 快速测试
# ============================================================
if __name__ == "__main__":
    print("华盛通 OpenAPI 客户端 v2.0")
    print(f"Gateway: {GATEWAY_URL}")
    print()

    # 美股账户资金
    pretty(get_account_funds("P"), "美股账户资金")

    # 全部持仓
    pretty(get_positions(), "当前持仓")

    # PANW 实时行情
    pretty(get_quote("PANW", "P"), "PANW 实时行情")

    # PANW 止损检查
    print("\n" + "="*50)
    print("  PANW 止损检查")
    print("="*50)
    check = check_stop_loss("PANW", "P", cost_price=149.69, stop_loss_pct=0.08, take_profit_pct=0.10)
    print(json.dumps(check, ensure_ascii=False, indent=2))
