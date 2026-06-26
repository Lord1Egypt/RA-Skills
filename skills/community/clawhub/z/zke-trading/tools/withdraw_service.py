import time
import uuid
from typing import Optional, Any, Dict, List


def _gen_withdraw_order_id() -> str:
    ts = int(time.time() * 1000)
    rand = uuid.uuid4().hex[:8]
    return f"wd_{ts}_{rand}"


def apply_withdraw(
    api,
    coin: str,
    address: str,
    amount: Any,
    memo: Optional[Any] = None,
    withdraw_order_id: Optional[Any] = None,
):
    """
    发起提现
    """
    # 兼容 AI：处理空字符串
    safe_wo_id = str(withdraw_order_id).strip() if withdraw_order_id is not None and str(withdraw_order_id).strip() != "" else _gen_withdraw_order_id()
    safe_memo = str(memo).strip() if memo is not None and str(memo).strip() != "" else None
    
    # 【修复】去除了 .upper()，忠实传递原本的币种格式
    safe_coin = str(coin).strip()

    body = {
        "symbol": safe_coin,
        "address": str(address).strip(),
        "amount": str(amount).strip(),
        "withdrawOrderId": safe_wo_id,
    }

    if safe_memo:
        body["label"] = safe_memo

    result = api.withdraw_apply(body)

    return {
        "coin": safe_coin,
        "address": address,
        "amount": amount,
        "memo": safe_memo,
        "withdraw_order_id": safe_wo_id,
        "result": result
    }


def withdraw_history(
    api,
    coin: Optional[Any] = None,
    withdraw_id: Optional[Any] = None,
    withdraw_order_id: Optional[Any] = None,
    start_time: Optional[Any] = None,
    end_time: Optional[Any] = None,
    page: Optional[Any] = None,
    limit: Optional[Any] = 20,
) -> List[Dict[str, Any]]:
    """
    查询提现记录
    """
    params = {}

    # 【修复】防空参的同时，去除了 .upper()
    if coin is not None and str(coin).strip() != "":
        params["symbol"] = str(coin).strip()

    if withdraw_id is not None and str(withdraw_id).strip() != "":
        params["withdrawId"] = str(withdraw_id).strip()

    if withdraw_order_id is not None and str(withdraw_order_id).strip() != "":
        params["withdrawOrderId"] = str(withdraw_order_id).strip()

    if start_time is not None and str(start_time).strip() != "":
        params["startTime"] = str(start_time).strip()

    if end_time is not None and str(end_time).strip() != "":
        params["endTime"] = str(end_time).strip()

    if page is not None and str(page).strip() != "":
        params["page"] = int(page)

    result = api.withdraw_history(params)

    rows = []

    if isinstance(result, dict):
        data = result.get("data")
        if isinstance(data, dict):
            if isinstance(data.get("withdrawList"), list):
                rows = data["withdrawList"]
            elif isinstance(data.get("list"), list):
                rows = data["list"]
        elif isinstance(data, list):
            rows = data
        elif isinstance(result.get("list"), list):
            rows = result["list"]
    elif isinstance(result, list):
        rows = result

    clean = []

    for r in rows:
        # 【核心防御】强制提取字符串 ID，防止 JS 精度丢失
        w_id = r.get("id")
        wo_id = r.get("withdrawOrderId")
        tx_id = r.get("txId") or r.get("txid")
        
        clean.append({
            "coin": r.get("symbol"),
            "amount": r.get("amount"),
            "address": r.get("address"),
            "withdraw_id": str(w_id) if w_id is not None else None,
            "withdraw_order_id": str(wo_id) if wo_id is not None else None,
            "txid": str(tx_id) if tx_id is not None else None,
            "fee": r.get("fee"),
            "status": r.get("status"),
            "info": r.get("info"),
            "time": r.get("applyTime") or r.get("ctime") or r.get("time"),
            "raw": r
        })

    # 【核心防御】强制把 limit 转为整数，防止 AI 传字符串 "20" 导致切片失效
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 20
    
    if safe_limit > 0:
        return clean[:safe_limit]

    return clean
