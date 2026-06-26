import httpx
import logging
from datetime import date
from config import NOAA_API_BASE, NOAA_USER_AGENT, HTTP_TIMEOUT

logger = logging.getLogger(__name__)


async def get_noaa_forecast(lat: float, lon: float, target_date: date) -> int:
    """
    Fetches the NOAA high temperature forecast for the given lat/lon and target date.
    Returns an integer temperature in Fahrenheit.
    Raises an exception if the forecast cannot be retrieved.
    """
    headers = {"User-Agent": NOAA_USER_AGENT}

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        points_url = f"{NOAA_API_BASE}/points/{lat},{lon}"
        logger.info(f"NOAA: fetching grid point from {points_url}")

        resp = await client.get(points_url, headers=headers)
        if resp.status_code != 200:
            raise Exception(
                f"NOAA points API returned HTTP {resp.status_code}: {resp.text[:200]}"
            )

        points_data = resp.json()
        props = points_data.get("properties", {})
        forecast_url = props.get("forecast")

        if not forecast_url:
            raise Exception("NOAA /points response missing 'properties.forecast' URL")

        logger.info(f"NOAA: fetching forecast from {forecast_url}")
        resp2 = await client.get(forecast_url, headers=headers)
        if resp2.status_code != 200:
            raise Exception(
                f"NOAA forecast URL returned HTTP {resp2.status_code}: {resp2.text[:200]}"
            )

        forecast_data = resp2.json()
        periods = forecast_data.get("properties", {}).get("periods", [])

        if not periods:
            raise Exception("NOAA forecast returned zero periods")

        target_str = target_date.isoformat()
        logger.info(f"NOAA: searching {len(periods)} periods for date {target_str}")

        daytime_temp = None
        for period in periods:
            start = period.get("startTime", "")
            is_daytime = period.get("isDaytime", False)
            temp = period.get("temperature")
            temp_unit = period.get("temperatureUnit", "F")

            if target_str in start and is_daytime and temp is not None:
                if temp_unit == "C":
                    temp = round((temp * 9 / 5) + 32)
                daytime_temp = int(round(temp))
                logger.info(f"NOAA: found daytime high {daytime_temp}°F for {start}")
                return daytime_temp

        for period in periods:
            start = period.get("startTime", "")
            temp = period.get("temperature")
            temp_unit = period.get("temperatureUnit", "F")

            if target_str in start and temp is not None:
                if temp_unit == "C":
                    temp = round((temp * 9 / 5) + 32)
                daytime_temp = int(round(temp))
                logger.info(f"NOAA: found period temp {daytime_temp}°F for {start}")
                return daytime_temp

        available_dates = list({p.get("startTime", "")[:10] for p in periods})
        raise Exception(
            f"NOAA: no forecast period found for date {target_str}. "
            f"Available dates: {available_dates}"
        )
