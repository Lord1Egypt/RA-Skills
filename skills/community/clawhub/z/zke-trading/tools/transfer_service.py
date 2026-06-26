from typing import Any, Dict, List, Optional


VALID_ACCOUNT_TYPES = {"EXCHANGE", "FUTURE"}


def _normalize_account_type(value: str) -> str:
    # 兼容 AI 习惯：有时 AI 会传空字符串 "" 而不是 None
    if value is None or str(value).strip() == "":
        raise ValueError("账户类型不能为空，必须为 EXCHANGE 或 FUTURE。")

    v = str(value).strip().upper()

    if v not in VALID_ACCOUNT_TYPES:
        raise ValueError(f"无效账户类型: {value}，只允许 EXCHANGE / FUTURE")
    return v


def _normalize_transfer_result(result: Any) -> Dict[str, Any]:
    """
    统一整理划转返回
    """
    if not isinstance(result, dict):
        return {
            "success": False,
            "transfer_id": None,
            "raw": result,
        }

    data = result.get("data")
    transfer_id = None

    if isinstance(data, dict):
        t_id = data.get("transferId")
        # 【AI 优化】强制将划转 ID 转为字符串，防止长整数精度丢失
        transfer_id = str(t_id) if t_id is not None else None

    code = result.get("code")
    msg = result.get("msg")

    return {
        "success": str(code) == "0" if code is not None else True,
        "code": code,
        "msg": msg,
        "transfer_id": transfer_id,
        "raw": result,
    }


def _extract_transfer_rows(result: Any) -> List[Dict[str, Any]]:
    """
    统一提取划转记录列表
    """
    if isinstance(result, list):
        return result

    if not isinstance(result, dict):
        return []

    data = result.get("data")

    if isinstance(data, dict):
        if isinstance(data.get("list"), list):
            return data["list"]

    if isinstance(result.get("list"), list):
        return result["list"]

    return []


def transfer_between_accounts(
    api,
    coin_symbol: Any,
    amount: Any,
    from_account: Any,
    to_account: Any,
) -> Dict[str, Any]:
    """
    现货 / 合约 之间划转
    """
    from_acc = _normalize_account_type(str(from_account))
    to_acc = _normalize_account_type(str(to_account))

    if from_acc == to_acc:
        raise ValueError("fromAccount 和 toAccount 不能相同。")

    if coin_symbol is None or str(coin_symbol).strip() == "":
        raise ValueError("coin_symbol 不能为空。")

    if amount is None or str(amount).strip() == "":
        raise ValueError("amount 不能为空。")

    # 【修复】去除了强制的 .upper()，原样传递
    safe_coin = str(coin_symbol).strip()
    safe_amount = str(amount).strip()

    result = api.asset_transfer(
        coin_symbol=safe_coin,
        amount=safe_amount,
        from_account=from_acc,
        to_account=to_acc,
    )

    normalized = _normalize_transfer_result(result)
    normalized["request"] = {
        "coinSymbol": safe_coin,
        "amount": safe_amount,
        "fromAccount": from_acc,
        "toAccount": to_acc,
    }
    return normalized


def transfer_spot_to_futures(api, coin_symbol: Any, amount: Any) -> Dict[str, Any]:
    """
    现货 -> 合约
    """
    return transfer_between_accounts(
        api=api,
        coin_symbol=coin_symbol,
        amount=amount,
        from_account="EXCHANGE",
        to_account="FUTURE",
    )


def transfer_futures_to_spot(api, coin_symbol: Any, amount: Any) -> Dict[str, Any]:
    """
    合约 -> 现货
    """
    return transfer_between_accounts(
        api=api,
        coin_symbol=coin_symbol,
        amount=amount,
        from_account="FUTURE",
        to_account="EXCHANGE",
    )


def query_transfer_history(
    api,
    transfer_id: Optional[Any] = None,
    coin_symbol: Optional[Any] = None,
    from_account: Optional[Any] = None,
    to_account: Optional[Any] = None,
    start_time: Optional[Any] = None,
    end_time: Optional[Any] = None,
    page: Optional[Any] = 1,
    limit: Optional[Any] = 20,
) -> Dict[str, Any]:
    """
    查询划转记录
    """
    # 兼容 AI 参数传递，清理空字符串
    from_acc_clean = from_account if from_account is not None and str(from_account).strip() != "" else None
    to_acc_clean = to_account if to_account is not None and str(to_account).strip() != "" else None

    norm_from = _normalize_account_type(from_acc_clean) if from_acc_clean else None
    norm_to = _normalize_account_type(to_acc_clean) if to_acc_clean else None

    if not norm_from or not norm_to:
        raise ValueError("查询划转记录时必须提供 from_account 和 to_account，例如 EXCHANGE FUTURE。")

    # 确保安全类型转换，去除强制 upper()
    safe_transfer_id = str(transfer_id).strip() if transfer_id is not None and str(transfer_id).strip() != "" else None
    safe_coin = str(coin_symbol).strip() if coin_symbol is not None and str(coin_symbol).strip() != "" else None

    # 【核心修复】使用显式 None 和空字符串判断，完美保护合法的 0 值
    safe_start_time = int(start_time) if start_time is not None and str(start_time).strip() != "" else None
    safe_end_time = int(end_time) if end_time is not None and str(end_time).strip() != "" else None
    safe_page = int(page) if page is not None and str(page).strip() != "" else 1
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 20

    result = api.asset_transfer_query(
        transfer_id=safe_transfer_id,
        coin_symbol=safe_coin,
        from_account=norm_from,
        to_account=norm_to,
        start_time=safe_start_time,
        end_time=safe_end_time,
        page=safe_page,
        limit=safe_limit,
    )

    rows = _extract_transfer_rows(result)

    clean = []
    for item in rows:
        # 【AI 优化】对所有可能产生长整数 ID 的字段进行强制字符串化
        t_id = item.get("transferId")
        clean.append({
            "transfer_id": str(t_id) if t_id is not None else None,
            "from_account": item.get("fromAccount"),
            "to_account": item.get("toAccount"),
            "coin_symbol": item.get("coinSymbol"),
            "amount": item.get("amount"),
            "status": item.get("status"),
            "create_time": item.get("createTime"),
            "raw": item,
        })

    return {
        "query": {
            "transferId": safe_transfer_id,
            "coinSymbol": safe_coin,
            "fromAccount": norm_from,
            "toAccount": norm_to,
            "startTime": safe_start_time,
            "endTime": safe_end_time,
            "page": safe_page,
            "limit": safe_limit,
        },
        "records": clean,
        "count": len(clean),
        "raw": result,
    }
