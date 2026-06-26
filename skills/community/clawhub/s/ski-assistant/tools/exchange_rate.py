#!/usr/bin/env python3
"""
实时汇率换算工具（只读网络请求，不修改任何文件）
用法:
  python tools/exchange_rate.py <amount> <from> <to>
  python tools/exchange_rate.py '{"amount":7800,"from":"JPY","to":"CNY"}'

安全说明:
  - 仅向 exchangerate-api.com 发起 GET 请求，不发送任何用户数据
  - 不执行 shell、subprocess 或文件写入操作
  - 联网失败时自动降级为内置静态汇率（标注"参考汇率"）
  - 仅用户显式运行命令时触发，无后台自动联网

支持币种: CNY, JPY, KRW, CHF, EUR, CAD, USD, NZD, AUD, GBP
"""

import json
import sys
import time
import urllib.request

# 备用静态汇率（联网失败时使用）
_FALLBACK_RATES_TO_CNY = {
    "CNY": 1.0, "JPY": 0.048, "KRW": 0.0053, "CHF": 8.2,
    "EUR": 7.9, "CAD": 5.3, "USD": 7.25, "NZD": 4.4,
    "AUD": 4.8, "GBP": 9.2,
}


def get_live_rate(from_cur: str, to_cur: str):
    """获取实时汇率，返回 (rate, is_live)"""
    url = f"https://api.exchangerate-api.com/v4/latest/{from_cur}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ski-assistant/5.1"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                rate = data.get("rates", {}).get(to_cur)
                if rate:
                    return rate, True
        except Exception:
            if attempt < 2:
                time.sleep(0.5 * (attempt + 1))
    return None, False


def convert(amount: float, from_cur: str, to_cur: str) -> dict:
    from_cur, to_cur = from_cur.upper(), to_cur.upper()
    rate, is_live = get_live_rate(from_cur, to_cur)

    if rate is None:
        fr = _FALLBACK_RATES_TO_CNY.get(from_cur)
        tr = _FALLBACK_RATES_TO_CNY.get(to_cur)
        if fr and tr:
            rate, is_live = fr / tr, False
        else:
            return {"error": f"不支持的币种: {from_cur} 或 {to_cur}"}

    return {
        "from": {"amount": amount, "currency": from_cur},
        "to": {"amount": round(amount * rate, 2), "currency": to_cur},
        "rate": round(rate, 6),
        "is_live": is_live,
        "note": "实时汇率" if is_live else "参考汇率（离线备用值）",
    }


if __name__ == "__main__":
    if len(sys.argv) == 4:
        result = convert(float(sys.argv[1]), sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 2:
        p = json.loads(sys.argv[1])
        result = convert(p["amount"], p["from"], p["to"])
    else:
        print(__doc__)
        sys.exit(1)

    if "error" in result:
        print(f"错误: {result['error']}")
        sys.exit(1)
    f, t = result["from"], result["to"]
    print(f"{f['currency']} {f['amount']:,.2f} = {t['currency']} {t['amount']:,.2f}")
    print(f"汇率: 1 {f['currency']} = {result['rate']} {t['currency']}")
    print(f"来源: {result['note']}")
