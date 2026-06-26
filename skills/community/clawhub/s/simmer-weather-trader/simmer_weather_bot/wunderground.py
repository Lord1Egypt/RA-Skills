import logging
import re
from datetime import date, datetime
from config import PLAYWRIGHT_TIMEOUT

logger = logging.getLogger(__name__)


async def get_wunderground_forecast(wunderground_path: str, target_date: date) -> int:
    """
    Uses Playwright (headless Chromium) to scrape the Wunderground 10-day forecast page.
    For today's date: returns today's high temperature.
    For future dates: scrapes the 10-day forecast table to find the correct date.
    Returns temperature in Fahrenheit.

    wunderground_path: e.g. "ny/new-york"  (no leading slash, no /forecast/us/)
    """
    from playwright.async_api import async_playwright

    is_international = "/" not in wunderground_path or wunderground_path.startswith(("italy", "spain", "israel", "england", "france", "germany", "japan"))

    if is_international:
        url = f"https://www.wunderground.com/forecast/{wunderground_path}"
    else:
        url = f"https://www.wunderground.com/forecast/us/{wunderground_path}"

    logger.info(f"Wunderground: loading {url} for date {target_date}")

    from datetime import date as date_cls
    today = date_cls.today()
    days_ahead = (target_date - today).days

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
            await page.goto(url, timeout=PLAYWRIGHT_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)

            temp_text = None

            if days_ahead <= 0:
                selectors = [
                    ".wu-unit-temperature .wu-value",
                    "[data-testid='TemperatureValue']",
                    ".today_nowcard-temp span",
                    "span.temp",
                    "div.high-temp",
                ]
                for selector in selectors:
                    els = await page.query_selector_all(selector)
                    for el in els:
                        t = (await el.inner_text()).strip().replace("°", "").replace("F", "").replace("C", "").strip()
                        if t.lstrip("-").isdigit():
                            temp_text = t
                            logger.info(f"Wunderground: today high '{t}°' via selector '{selector}'")
                            break
                    if temp_text:
                        break

            else:
                logger.info(f"Wunderground: looking for {days_ahead} days ahead in 10-day forecast")

                forecast_selectors = [
                    "table.forecast-table",
                    ".seven-day-forecast",
                    "lib-forecast-chart",
                    ".tenday",
                ]

                content = await page.content()

                date_formats = [
                    target_date.strftime("%a %b %-d"),
                    target_date.strftime("%A, %B %-d"),
                    target_date.strftime("%b %-d"),
                    target_date.strftime("%-m/%-d"),
                ]

                for fmt in date_formats:
                    pattern = re.escape(fmt) + r'.*?(\d{1,3})\s*°?[FC]?'
                    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
                    if match:
                        temp_text = match.group(1)
                        logger.info(f"Wunderground: found future date temp '{temp_text}' via date pattern '{fmt}'")
                        break

                if not temp_text:
                    json_pattern = re.findall(
                        r'"high"\s*:\s*\{[^}]*"fahrenheit"\s*:\s*(\d+)',
                        content
                    )
                    if json_pattern and len(json_pattern) > days_ahead:
                        temp_text = json_pattern[days_ahead]
                        logger.info(f"Wunderground: future high from JSON[{days_ahead}]: {temp_text}°F")
                    elif json_pattern:
                        temp_text = json_pattern[-1]
                        logger.info(f"Wunderground: future high from JSON (last): {temp_text}°F")

                if not temp_text:
                    highs_celsius = re.findall(r'"high_celsius"\s*:\s*(\d+)', content)
                    highs_f = re.findall(r'"high_fahrenheit"\s*:\s*(\d+)', content)
                    if highs_f and len(highs_f) > days_ahead:
                        temp_text = highs_f[days_ahead]
                    elif highs_f:
                        temp_text = highs_f[-1]
                    elif highs_celsius and len(highs_celsius) > days_ahead:
                        c = int(highs_celsius[days_ahead])
                        temp_text = str(round((c * 9 / 5) + 32))

                if not temp_text:
                    selectors = [
                        ".wu-unit-temperature .wu-value",
                        "[data-testid='TemperatureValue']",
                        "span.temp",
                    ]
                    for selector in selectors:
                        els = await page.query_selector_all(selector)
                        for el in els:
                            t = (await el.inner_text()).strip().replace("°", "").replace("F", "").replace("C", "").strip()
                            if t.lstrip("-").isdigit():
                                temp_text = t
                                logger.info(f"Wunderground: fallback to current temp '{t}' via selector '{selector}'")
                                break
                        if temp_text:
                            break

            if not temp_text:
                raise Exception(
                    f"Wunderground: page loaded at {url} but no temperature found for {target_date}. "
                    f"The page structure may have changed or anti-scraping blocked the request."
                )

            raw_temp = float(temp_text)

            page_content = await page.content()
            is_celsius_page = "°C" in page_content[:2000] and "°F" not in page_content[:2000]
            if raw_temp < 32 and is_celsius_page:
                raw_temp = round((raw_temp * 9 / 5) + 32)
                logger.info(f"Wunderground: converted Celsius to {raw_temp}°F")

            temp_f = int(round(raw_temp))
            logger.info(f"Wunderground: final temp = {temp_f}°F for {target_date}")
            return temp_f

        finally:
            await browser.close()
