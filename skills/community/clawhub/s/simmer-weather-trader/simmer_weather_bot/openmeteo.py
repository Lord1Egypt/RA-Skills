import httpx
import logging
from datetime import date
from config import OPEN_METEO_API, HTTP_TIMEOUT

logger = logging.getLogger(__name__)


async def get_openmeteo_forecast(lat: float, lon: float, target_date: date, timezone: str = "auto") -> int:
    """
    Fetches the Open-Meteo daily high temperature for the given lat/lon and target date.
    Returns an integer temperature in Fahrenheit.
    Raises an exception if the forecast cannot be retrieved.
    """
    date_str = target_date.isoformat()
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max",
        "temperature_unit": "fahrenheit",
        "timezone": timezone,
        "start_date": date_str,
        "end_date": date_str,
    }

    logger.info(f"Open-Meteo: fetching forecast for {lat},{lon} on {date_str}")

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        resp = await client.get(OPEN_METEO_API, params=params)
        if resp.status_code != 200:
            raise Exception(
                f"Open-Meteo returned HTTP {resp.status_code}: {resp.text[:200]}"
            )

        data = resp.json()

        if "error" in data and data["error"]:
            raise Exception(f"Open-Meteo error: {data.get('reason', 'unknown error')}")

        daily = data.get("daily", {})
        temps = daily.get("temperature_2m_max", [])
        dates = daily.get("time", [])

        if not temps:
            raise Exception(
                f"Open-Meteo returned no temperature data for {date_str}. "
                f"Full response keys: {list(data.keys())}"
            )

        if date_str not in dates:
            raise Exception(
                f"Open-Meteo: date {date_str} not in response dates: {dates}"
            )

        idx = dates.index(date_str)
        raw_temp = temps[idx]

        if raw_temp is None:
            raise Exception(f"Open-Meteo returned null temperature for {date_str}")

        temp_f = int(round(float(raw_temp)))
        logger.info(f"Open-Meteo: {temp_f}°F for {date_str} at {lat},{lon}")
        return temp_f
