#!/usr/bin/env python3
"""
QStrader — Risk Manager
Checks position against risk limits before placing order.
"""
import subprocess, json, sys, os

# Лимиты
MAX_MARGIN_USAGE = 0.50      # 50%
MAX_DAILY_LOSS = 0.02         # 2% от баланса
MAX_POSITION_LOSS = 100       # $100 макс убыток на позицию
REQUIRED_SL_TP = True


def mcporter_call(args):
    """Call mcporter CLI and return parsed JSON."""
    mcp_config = os.environ.get("MCP_CONFIG", "")
    if not mcp_config:
        for p in [os.path.expanduser("~/.openclaw/workspace/config/mcporter.json"), "./config/mcporter.json"]:
            if os.path.exists(p):
                mcp_config = p
                break
    cmd = ["mcporter", "call"] + args
    os.chdir(os.path.expanduser("~/.openclaw/workspace"))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return {"error": result.stderr.strip()}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout.strip()}


def parse_account_data(account_raw):
    """Извлечь числовые поля из ответа аккаунта."""
    text = ""
    if isinstance(account_raw, list):
        for item in account_raw:
            if isinstance(item, dict):
                # Формат 1: [{type: "text", text: "..."}]
                if "text" in item:
                    text += item["text"]
                # Формат 2: [{code: "ok", data: {margin: {...}}}]
                elif "data" in item:
                    margin = item.get("data", {}).get("margin", {})
                    if margin:
                        return {
                            "balance": float(margin.get("balance", 0)),
                            "equity": float(margin.get("equity", 0)),
                            "margin": float(margin.get("margin", 0)),
                            "free_margin": float(margin.get("free_margin", 0)),
                            "unrealized_pl": float(margin.get("unrealized_pl", 0)),
                        }
    elif isinstance(account_raw, dict):
        if "data" in account_raw:
            margin = account_raw["data"].get("margin", {})
            if margin:
                return {
                    "balance": float(margin.get("balance", 0)),
                    "equity": float(margin.get("equity", 0)),
                    "margin": float(margin.get("margin", 0)),
                    "free_margin": float(margin.get("free_margin", 0)),
                    "unrealized_pl": float(margin.get("unrealized_pl", 0)),
                }
        text = account_raw.get("text", json.dumps(account_raw))
    else:
        text = str(account_raw)

    # Попробовать распарсить JSON из текста
    if text:
        try:
            inner = json.loads(text)
            if isinstance(inner, dict):
                margin = inner.get("data", inner).get("margin", {})
                if margin:
                    return {
                        "balance": float(margin.get("balance", 0)),
                        "equity": float(margin.get("equity", 0)),
                        "margin": float(margin.get("margin", 0)),
                        "free_margin": float(margin.get("free_margin", 0)),
                        "unrealized_pl": float(margin.get("unrealized_pl", 0)),
                    }
        except (json.JSONDecodeError, TypeError):
            pass

    return {}


def check_risk(ticker, side, volume, price, stop_loss=None, take_profit=None):
    """Pre-trade risk check."""
    errors = []
    warnings = []

    # 1. SL/TP обязательно
    if REQUIRED_SL_TP and stop_loss is None:
        errors.append("❌ Stop Loss обязателен!")
    if REQUIRED_SL_TP and take_profit is None:
        errors.append("❌ Take Profit обязателен!")

    # 2. Валидация числовых параметров
    if volume <= 0:
        errors.append(f"❌ Объём должен быть > 0, получен: {volume}")
    if price <= 0:
        errors.append(f"❌ Цена должна быть > 0, получена: {price}")

    # Проверка «640 vs 6400» — подозрительно круглые числа
    if price and price > 1000 and str(price).endswith("00"):
        warnings.append(f"⚠️ Проверь цену: {price} — точно не {price/10} или {price*10}?")

    if stop_loss and stop_loss > 1000 and str(stop_loss).endswith("00"):
        warnings.append(f"⚠️ Проверь SL: {stop_loss} — точно не {stop_loss/10} или {stop_loss*10}?")

    # 3. Получить данные аккаунта
    account = mcporter_call(["my-n8n-mcp.Get_account_data"])
    if "error" in account:
        errors.append(f"❌ Не удалось получить данные аккаунта: {account['error']}")
        return {"approved": False, "errors": errors, "warnings": warnings}

    acct = parse_account_data(account)

    balance = acct.get("balance", 0)
    margin_used = acct.get("margin", 0)
    equity = acct.get("equity", balance)
    free_margin = acct.get("free_margin", 0)

    if balance == 0:
        warnings.append("⚠️ Не удалось определить баланс, margin check пропущен")
    else:
        # 4. Margin check
        if margin_used > 0 and balance > 0:
            margin_pct = margin_used / balance
            if margin_pct >= MAX_MARGIN_USAGE:
                errors.append(
                    f"❌ Margin {margin_pct:.1%} >= {MAX_MARGIN_USAGE:.0%}. "
                    "Закрой убыточные позиции перед новой!"
                )
            elif margin_pct >= MAX_MARGIN_USAGE * 0.8:
                warnings.append(
                    f"⚠️ Margin {margin_pct:.1%} — близко к лимиту {MAX_MARGIN_USAGE:.0%}"
                )

        # 5. Daily loss check
        if equity < balance:
            daily_loss_pct = (balance - equity) / balance
            max_loss_usd = balance * MAX_DAILY_LOSS
            current_loss_usd = balance - equity
            if daily_loss_pct >= MAX_DAILY_LOSS:
                errors.append(
                    f"❌ Дневной убыток {daily_loss_pct:.1%} (${current_loss_usd:.0f}) >= {MAX_DAILY_LOSS:.0%} "
                    f"(${max_loss_usd:.0f}). СТОП ТОРГОВЛИ НА ДЕНЬ!"
                )
            elif daily_loss_pct >= MAX_DAILY_LOSS * 0.8:
                warnings.append(
                    f"⚠️ Дневной убыток {daily_loss_pct:.1%} — близко к лимиту {MAX_DAILY_LOSS:.0%}"
                )

    # 6. Position loss estimate
    if stop_loss is not None and volume is not None and price is not None:
        sl_distance = abs(price - stop_loss)
        position_loss = sl_distance * volume
        if position_loss > MAX_POSITION_LOSS:
            warnings.append(
                f"⚠️ Потенциальный убыток ${position_loss:.0f} > лимит ${MAX_POSITION_LOSS}. "
                "Уменьши объём или подтяни SL."
            )

    approved = len(errors) == 0
    result = {"approved": approved, "errors": errors, "warnings": warnings}

    # Вывод
    status = "✅ APPROVED" if approved else "❌ REJECTED"
    print(f"\n🔶 Risk Check: {status}")
    print(f"   Ticker: {ticker}, Side: {side}, Vol: {volume}, Price: {price}")
    print(f"   SL: {stop_loss}, TP: {take_profit}")
    print(f"   Balance: ${balance:.2f}, Equity: ${equity:.2f}, Margin: ${margin_used:.2f}")
    for e in errors:
        print(f"   {e}")
    for w in warnings:
        print(f"   {w}")

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="QStrader Risk Manager")
    parser.add_argument("ticker", help="Брокерский тикер (например US500)")
    parser.add_argument("side", choices=["buy", "sell"], help="Направление")
    parser.add_argument("volume", type=float, help="Объём")
    parser.add_argument("price", type=float, help="Цена входа")
    parser.add_argument("--sl", type=float, help="Stop Loss")
    parser.add_argument("--tp", type=float, help="Take Profit")
    args = parser.parse_args()

    result = check_risk(args.ticker, args.side, args.volume, args.price, args.sl, args.tp)
    sys.exit(0 if result["approved"] else 1)
