def extract_account_balances(account_data):
    """
    兼容多种账户返回结构，统一提取为 list

    已兼容的典型结构：
    1) Spot account:
       {"balances": [...]}

    2) 某些接口直接返回:
       {"data": [...]}

    3) 某些资产接口:
       {"data": {"balances": [...]}}

    4) asset/account/by_type 或 exchange/account:
       {"data": {"accountList": [...]}}

    5) 直接就是 list
    """
    if isinstance(account_data, list):
        return account_data

    if not isinstance(account_data, dict):
        return []

    if isinstance(account_data.get("balances"), list):
        return account_data["balances"]

    if isinstance(account_data.get("accountList"), list):
        return account_data["accountList"]

    data = account_data.get("data")

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        if isinstance(data.get("balances"), list):
            return data["balances"]

        if isinstance(data.get("accountList"), list):
            return data["accountList"]

        if isinstance(data.get("list"), list):
            return data["list"]

    return []


def _get_free_value(item):
    """
    统一取“可用余额”
    """
    return (
        item.get("free")
        or item.get("normalBalance")
        or item.get("availableAmount")
        or item.get("canTransferBalance")
        or "0"
    )


def _get_locked_value(item):
    """
    统一取“冻结余额”
    """
    return (
        item.get("locked")
        or item.get("lockBalance")
        or item.get("accountLock")
        or item.get("freeze")
        or "0"
    )


def _get_total_value(item):
    """
    统一取“总余额”
    """
    return (
        item.get("totalBalance")
        or item.get("total")
        or item.get("walletBalance")
        or item.get("accountAmount")
        or None
    )


def _get_asset_name(item, default=""):
    """
    统一取币种名
    优先返回更适合展示的字段
    """
    return (
        item.get("asset")
        or item.get("coinSymbolName")
        or item.get("coinSymbol")
        or item.get("marginCoin")
        or default
    )


def filter_nonzero_balances(balances):
    result = []

    for item in balances:
        free_val = str(_get_free_value(item))
        locked_val = str(_get_locked_value(item))
        total_val = _get_total_value(item)

        try:
            free_num = float(free_val)
        except Exception:
            free_num = 0.0

        try:
            locked_num = float(locked_val)
        except Exception:
            locked_num = 0.0

        total_num = None
        if total_val is not None:
            try:
                total_num = float(str(total_val))
            except Exception:
                total_num = None

        if free_num != 0.0 or locked_num != 0.0 or (total_num is not None and total_num != 0.0):
            result.append(item)

    return result


def find_asset_balance(balances, asset):
    target = str(asset).upper()
    matched = []

    for x in balances:
        asset_name = str(x.get("asset", "")).upper()
        coin_symbol = str(x.get("coinSymbol", "")).upper()
        coin_symbol_name = str(x.get("coinSymbolName", "")).upper()
        margin_coin = str(x.get("marginCoin", "")).upper()

        if (
            asset_name == target
            or coin_symbol == target
            or coin_symbol_name == target
            or margin_coin == target
        ):
            matched.append(x)

    return matched


def get_asset_balance_summary(balances, asset):
    matched = find_asset_balance(balances, asset)

    if not matched:
        return {
            "asset": str(asset).upper(),
            "free": "0",
            "locked": "0",
            "total": "0",
        }

    item = matched[0]

    asset_name = _get_asset_name(item, asset)
    free_val = _get_free_value(item)
    locked_val = _get_locked_value(item)
    total_val = _get_total_value(item)

    if total_val is None:
        try:
            total_val = str(float(str(free_val)) + float(str(locked_val)))
        except Exception:
            total_val = "0"

    return {
        "asset": str(asset_name).upper(),
        "free": str(free_val),
        "locked": str(locked_val),
        "total": str(total_val),
    }


def to_display_balance_rows(balances):
    """
    把各种原始结构统一整理成可展示格式
    """
    rows = []

    for item in balances:
        rows.append({
            "asset": str(_get_asset_name(item, "")).upper(),
            "free": str(_get_free_value(item)),
            "locked": str(_get_locked_value(item)),
            "total": str(_get_total_value(item) if _get_total_value(item) is not None else ""),
            "raw": item,
        })

    return rows
