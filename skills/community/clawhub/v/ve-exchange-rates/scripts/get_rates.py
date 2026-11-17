#!/usr/bin/env python3
from typing import Dict, Optional
from decimal import Decimal, ROUND_HALF_UP
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta

BCV_URL = "https://www.bcv.org.ve/"
BINANCE_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
FALLBACK_URL = "https://api.exchangerate-api.com/v4/latest/USD"
UA = "Mozilla/5.0"


def fetch_text(url: str, method: str = "GET", body: Optional[bytes] = None, headers: Optional[Dict[str, str]] = None, timeout: int = 15) -> str:
    req = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def d(value) -> Decimal:
    return Decimal(str(value))


def q2(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def q3(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)


def spanish_day_month(dt: datetime) -> str:
    days = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{days[dt.weekday()]}, {dt.day:02d} {months[dt.month-1]} {dt.year}"


def fetch_bcv() -> tuple[Decimal, str, str, bool]:
    html = fetch_text(BCV_URL, headers={"User-Agent": UA}, timeout=15)
    match = re.search(r'id="dolar".*?<strong>\s*([0-9\.,]+)\s*</strong>.*?Fecha Valor:\s*<span[^>]*>([^<]+)</span>', html, re.S | re.I)
    if not match:
        raise ValueError("No se pudo extraer la tasa USD/fecha valor desde BCV")
    raw_rate = match.group(1).strip()
    date_text = re.sub(r"\s+", " ", match.group(2).strip())
    rate = d(raw_rate.replace(".", "").replace(",", "."))
    today = spanish_day_month(datetime.now())
    tomorrow = spanish_day_month(datetime.now() + timedelta(days=1))
    clean_date = date_text.lower()
    date_ok = today in clean_date or tomorrow in clean_date
    return rate, date_text, BCV_URL, date_ok


def fetch_fallback_rate() -> Decimal:
    text = fetch_text(FALLBACK_URL, headers={"User-Agent": UA}, timeout=10)
    data = json.loads(text)
    rate = data.get("rates", {}).get("VES")
    if rate is None:
        raise ValueError("Fallback sin tasa VES")
    return d(rate)


def fetch_binance_side(trade_type: str) -> tuple[Decimal, Decimal, Decimal, str]:
    payload = {
        "fiat": "VES",
        "page": 1,
        "rows": 10,
        "tradeType": trade_type,
        "asset": "USDT",
        "countries": [],
        "proMerchantAds": False,
        "shieldMerchantAds": False,
        "filterType": "tradable",
    }
    text = fetch_text(
        BINANCE_URL,
        method="POST",
        body=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA},
        timeout=15,
    )
    data = json.loads(text).get("data", [])
    prices = [d(item["adv"]["price"]) for item in data if item.get("adv", {}).get("price")]
    if not prices:
        raise ValueError("Sin ofertas Binance")
    avg = sum(prices) / d(len(prices))
    return avg, min(prices), max(prices), str(len(prices))


def main() -> int:
    print("🇻🇪 TASAS DE CAMBIO VENEZUELA")
    print("==============================")
    print()

    print("📊 Consultando tasa BCV...")
    source = "bcv.org.ve"
    date_text = ""
    date_ok = False
    try:
        bcv_rate, date_text, source, date_ok = fetch_bcv()
    except Exception:
        try:
            source = "exchange fallback"
            bcv_rate = fetch_fallback_rate()
        except Exception:
            print("❌ No se pudo obtener la tasa BCV desde bcv.org.ve ni desde la fuente de respaldo.")
            print("   No se calcularán tasas para evitar reportar un valor incorrecto.")
            print("   Intenta de nuevo más tarde o verifica el acceso a internet.")
            return 1

    print(f"✅ Tasa BCV: {bcv_rate} Bs/USD")
    print(f"🔎 Fuente BCV: {source.replace('https://www.', '').replace('https://', '').rstrip('/')}")
    if date_text:
        print(f"📅 Fecha valor BCV: {date_text}")
        if not date_ok:
            print("⚠️ Advertencia: la fecha valor BCV no coincide con hoy/mañana")
    print()

    print("📊 Consultando USDT Binance P2P...")
    try:
        buy_avg, buy_min, buy_max, buy_count = fetch_binance_side("SELL")
        sell_avg, sell_min, sell_max, sell_count = fetch_binance_side("BUY")
    except Exception:
        print("❌ No se pudo obtener el precio USDT desde Binance P2P.")
        print("   No se calculará la brecha para evitar reportar valores inventados.")
        print("   Intenta de nuevo más tarde o verifica el acceso a internet.")
        return 1

    p2p_avg = q2((buy_avg + sell_avg) / d(2))

    print(f"✅ USDT P2P (venta): {q2(buy_avg)} Bs/USDT (rango: {q3(buy_min)} - {q3(buy_max)}, {buy_count} ofertas)")
    print(f"✅ USDT P2P (compra): {q2(sell_avg)} Bs/USDT (rango: {q3(sell_min)} - {q3(sell_max)}, {sell_count} ofertas)")
    print(f"✅ USDT P2P (promedio): {p2p_avg} Bs/USDT")
    print()

    print("📈 BRECHA CAMBIARIA:")
    print("====================")
    diff = q2(p2p_avg - bcv_rate)
    gap = q2((p2p_avg - bcv_rate) / bcv_rate * d(100))
    print(f"Diferencia: {diff} Bs")
    print(f"Brecha: +{gap}%")
    print(f"→ El paralelo está {gap}% más caro que el oficial")
    print()

    print("💰 CONVERSIÓN: 100 USD (BCV) a USDT")
    print("=====================================")
    bs_100 = q2(d(100) * bcv_rate)
    usdt_equiv = q2(bs_100 / p2p_avg)
    usdt_lost = q2(d(100) - usdt_equiv)
    print(f"$100 a tasa BCV = {bs_100} Bs")
    print(f"Equivalen a: {usdt_equiv} USDT (a tasa P2P)")
    print()
    print("📊 En otras palabras:")
    print(f"   Por $100 en dólares BCV, obtienes {usdt_equiv} USDT")
    print(f"   (Pierdes {usdt_lost} USDT por la brecha cambiaria)")
    print()
    print("==============================")
    print(f"Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
