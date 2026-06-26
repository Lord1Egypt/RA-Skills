import httpx
import sys
import time
import logging
import requests
from config import (
    SIMMER_API_KEY, SIMMER_BASE_URL,
    NOAA_API_BASE, NOAA_USER_AGENT,
    OPEN_METEO_API,
    NVIDIA_API_KEY, FOURCASTNET_URL, FOURCASTNET_POLL_URL,
    HTTP_TIMEOUT,
)

logger = logging.getLogger(__name__)

SIMMER_HEADERS = {"Authorization": f"Bearer {SIMMER_API_KEY}"}


async def check_simmer(client: httpx.AsyncClient) -> dict:
    url = f"{SIMMER_BASE_URL}/api/sdk/agents/me"
    response = await client.get(url, headers=SIMMER_HEADERS)
    response.raise_for_status()
    data = response.json()

    return {
        "status": "PASS",
        "agent_id": data.get("agent_id", data.get("id", "unknown")),
        "balance": data.get("balance", "N/A"),
        "trading_enabled": data.get("limits", {}).get("simmer", True),
        "rate_limits": data.get("rate_limits", {}),
    }


async def check_simmer_markets(client: httpx.AsyncClient) -> dict:
    url = f"{SIMMER_BASE_URL}/api/sdk/markets"
    params = {"tags": "weather", "status": "active", "limit": 10}
    response = await client.get(url, headers=SIMMER_HEADERS, params=params)
    response.raise_for_status()

    raw = response.json()
    if isinstance(raw, dict):
        markets = raw.get("markets", raw.get("data", raw.get("results", [])))
    else:
        markets = raw

    if len(markets) == 0:
        raise Exception("No active weather markets found on Simmer")

    return {
        "status": "PASS",
        "markets_found": len(markets),
        "sample_question": markets[0].get("question", "N/A")[:80],
    }


async def check_noaa(client: httpx.AsyncClient) -> dict:
    url = f"{NOAA_API_BASE}/points/40.7128,-74.0060"
    headers = {"User-Agent": NOAA_USER_AGENT}
    response = await client.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    props = data.get("properties", {})
    forecast_url = props.get("forecast")

    if not forecast_url:
        raise Exception("NOAA returned no forecast URL in properties.forecast")

    return {
        "status": "PASS",
        "forecast_url": forecast_url,
        "grid_id": props.get("gridId", "N/A"),
    }


async def check_openmeteo(client: httpx.AsyncClient) -> dict:
    params = {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "daily": "temperature_2m_max",
        "temperature_unit": "fahrenheit",
        "timezone": "America/New_York",
        "forecast_days": 3,
    }
    response = await client.get(OPEN_METEO_API, params=params)
    response.raise_for_status()

    data = response.json()
    temps = data.get("daily", {}).get("temperature_2m_max", [])

    if not temps:
        raise Exception("Open-Meteo returned no temperature data in daily.temperature_2m_max")

    return {
        "status": "PASS",
        "sample_temp": f"{round(temps[0])}°F",
        "timezone": data.get("timezone", "N/A"),
    }


async def check_wunderground() -> dict:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            await page.goto(
                "https://www.wunderground.com/forecast/us/ny/new-york",
                timeout=20000, wait_until="domcontentloaded"
            )
            await page.wait_for_timeout(4000)

            temp_text = None
            selectors = [
                ".wu-unit-temperature .wu-value",
                "[data-testid='TemperatureValue']",
                ".today_nowcard-temp span",
                "span.temp",
            ]
            for sel in selectors:
                els = await page.query_selector_all(sel)
                for el in els:
                    t = (await el.inner_text()).strip().replace("°", "").replace("F", "").strip()
                    if t.lstrip("-").isdigit():
                        temp_text = t
                        break
                if temp_text:
                    break

            if not temp_text:
                import re
                content = await page.content()
                matches = re.findall(r'"temperature":\s*(\d+)', content)
                if matches:
                    temp_text = matches[0]

            if not temp_text:
                raise Exception(
                    "Wunderground page loaded but no temperature element found. "
                    "Page may have anti-scraping measures or changed DOM."
                )

            return {"status": "PASS", "sample_temp": f"{temp_text}°F"}
        finally:
            await browser.close()


def check_fourcastnet_sync() -> dict:
    """
    Validates FourcastNet API key by submitting a minimal job and confirming 202 acceptance.
    Does NOT wait for completion — just verifies the key is valid and job is accepted.
    """
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "NVCF-POLL-SECONDS": "5",
    }
    payload = {
        "input_id": 0,
        "variables": "t2m",
        "simulation_length": 1,
        "ensemble_size": 1,
        "noise_amplitude": 0,
    }

    session = requests.Session()
    response = session.post(FOURCASTNET_URL, headers=headers, json=payload, timeout=30)

    if response.status_code == 401:
        raise Exception("FourcastNet: API key rejected (401 Unauthorized)")
    if response.status_code == 403:
        raise Exception("FourcastNet: API key forbidden (403). Check NVIDIA_API_KEY permissions.")
    if response.status_code == 404:
        raise Exception(f"FourcastNet: endpoint not found (404). URL: {FOURCASTNET_URL}")

    if response.status_code == 200:
        return {
            "status": "PASS",
            "note": "Synchronous response (job completed immediately)",
            "job_id": "sync",
        }

    if response.status_code == 202:
        job_id = response.headers.get("nvcf-reqid", "unknown")
        return {
            "status": "PASS",
            "note": f"Job accepted and queued",
            "job_id": job_id,
        }

    raise Exception(
        f"FourcastNet unexpected status {response.status_code}: {response.text[:200]}"
    )


async def run_all_health_checks() -> bool:
    print("\n" + "=" * 60)
    print("🔍 SIMMER WEATHER BOT — STARTUP HEALTH CHECK")
    print("=" * 60)

    results = {}
    all_passed = True

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        checks = [
            ("Simmer API Auth", lambda: check_simmer(client)),
            ("Simmer Markets", lambda: check_simmer_markets(client)),
            ("NOAA Weather API", lambda: check_noaa(client)),
            ("Open-Meteo API", lambda: check_openmeteo(client)),
        ]

        for name, check_fn in checks:
            try:
                result = await check_fn()
                results[name] = result
                extras = ""
                if name == "Simmer API Auth":
                    extras = f" | Agent: {result.get('agent_id')} | Balance: {result.get('balance')}"
                elif name == "Simmer Markets":
                    extras = f" | {result.get('markets_found')} markets found"
                elif name == "NOAA Weather API":
                    extras = f" | Grid: {result.get('grid_id')}"
                elif name == "Open-Meteo API":
                    extras = f" | Sample: {result.get('sample_temp')}"
                print(f"  ✅ {name:<25} PASS{extras}")
            except Exception as e:
                results[name] = {"status": "FAIL", "error": str(e)}
                print(f"  ❌ {name:<25} FAIL — {str(e)[:120]}")
                all_passed = False

    try:
        result = await check_wunderground()
        results["Wunderground Scraper"] = result
        print(f"  ✅ {'Wunderground Scraper':<25} PASS | Sample: {result.get('sample_temp')}")
    except Exception as e:
        results["Wunderground Scraper"] = {"status": "FAIL", "error": str(e)}
        print(f"  ❌ {'Wunderground Scraper':<25} FAIL — {str(e)[:120]}")
        all_passed = False

    try:
        result = check_fourcastnet_sync()
        results["NVIDIA FourcastNet"] = result
        print(f"  ✅ {'NVIDIA FourcastNet':<25} PASS | {result.get('note')} | Job: {result.get('job_id', 'N/A')[:16]}")
    except Exception as e:
        results["NVIDIA FourcastNet"] = {"status": "FAIL", "error": str(e)}
        print(f"  ❌ {'NVIDIA FourcastNet':<25} FAIL — {str(e)[:120]}")
        all_passed = False

    print("=" * 60)

    if all_passed:
        print("🟢 ALL SYSTEMS GO — Bot is starting...")
        print("=" * 60 + "\n")
    else:
        failed = [k for k, v in results.items() if v.get("status") == "FAIL"]
        print(f"🔴 BOT STARTUP ABORTED — {len(failed)} API(s) failed:")
        for f in failed:
            print(f"   • {f}: {results[f]['error']}")
        print("=" * 60)
        print("Fix the above APIs before restarting the bot.")
        sys.exit(1)

    return True
