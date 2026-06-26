def extract_accounts(data):
    if isinstance(data, dict):
        account_list = data.get("account", [])
        if isinstance(account_list, list):
            return account_list
    return []


def get_all_margin_coins(accounts):
    result = []

    for item in accounts:
        coin = str(item.get("marginCoin", "")).upper()
        if coin and coin not in result:
            result.append(coin)

    return result


def get_account_by_margin_coin(accounts, margin_coin: str):
    target = str(margin_coin or "").upper()

    for item in accounts:
        if str(item.get("marginCoin", "")).upper() == target:
            return item

    return None


def get_margin_coin_summary(accounts, margin_coin: str):
    target = str(margin_coin or "").upper()

    for item in accounts:
        if str(item.get("marginCoin", "")).upper() == target:
            return {
                "marginCoin": item.get("marginCoin", target),
                "accountNormal": item.get("accountNormal", 0),
                "accountLock": item.get("accountLock", 0),
                "partPositionNormal": item.get("partPositionNormal", 0),
                "totalPositionNormal": item.get("totalPositionNormal", 0),
                "achievedAmount": item.get("achievedAmount", 0),
                "unrealizedAmount": item.get("unrealizedAmount", 0),
                "totalEquity": item.get("totalEquity", 0),
                "partEquity": item.get("partEquity", 0),
                "totalCost": item.get("totalCost", 0),
                "sumMarginRate": item.get("sumMarginRate", 0),
                "positionVos": item.get("positionVos", []) or []
            }

    return {
        "marginCoin": target,
        "accountNormal": 0,
        "accountLock": 0,
        "partPositionNormal": 0,
        "totalPositionNormal": 0,
        "achievedAmount": 0,
        "unrealizedAmount": 0,
        "totalEquity": 0,
        "partEquity": 0,
        "totalCost": 0,
        "sumMarginRate": 0,
        "positionVos": []
    }


def flatten_positions(accounts):
    result = []

    for acc in accounts:
        margin_coin = acc.get("marginCoin")

        for contract in (acc.get("positionVos") or []):
            contract_name = contract.get("contractName")
            contract_symbol = contract.get("contractSymbol")

            for pos in (contract.get("positions") or []):
                item = dict(pos)
                item["_marginCoin"] = margin_coin
                item["_contractName"] = contract_name
                item["_contractSymbol"] = contract_symbol
                result.append(item)

    return result


def filter_nonzero_positions(positions):
    result = []

    for pos in positions:
        try:
            volume = float(pos.get("volume", 0) or 0)
        except Exception:
            volume = 0.0

        if volume != 0.0:
            result.append(pos)

    return result
