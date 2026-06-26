#!/usr/bin/env python3
"""
NVIDIA FourcastNet atmospheric model — used as the AI forecast source.
Replaces the DeepSeek LLM with a deterministic global weather model.
Submits a forecast job, polls until complete, extracts 2m temperature
at the target lat/lon, then produces a structured verdict.
"""

import os
import io
import time
import zipfile
import logging
import tempfile
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone

import requests
import numpy as np

from config import (
    NVIDIA_API_KEY,
    FOURCASTNET_URL,
    FOURCASTNET_POLL_URL,
    FOURCASTNET_POLL_SECONDS,
    FOURCASTNET_MAX_POLLS,
)

logger = logging.getLogger(__name__)

_executor = ThreadPoolExecutor(max_workers=2)


def _call_fourcastnet_sync(lat: float, lon: float, target_date: date, min_temp: int, max_temp: int) -> dict:
    """
    Synchronous FourcastNet call — runs in a thread executor.
    Submits job, polls, parses netCDF zip output, returns verdict dict.
    """
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "NVCF-POLL-SECONDS": str(FOURCASTNET_POLL_SECONDS),
    }

    now_utc = datetime.now(timezone.utc)
    target_dt = datetime.combine(target_date, datetime.min.time()).replace(tzinfo=timezone.utc)
    hours_ahead = max(0, (target_dt - now_utc).total_seconds() / 3600)
    simulation_length = max(1, min(int(hours_ahead / 6) + 1, 20))

    payload = {
        "input_id": 0,
        "variables": "t2m",
        "simulation_length": simulation_length,
        "ensemble_size": 1,
        "noise_amplitude": 0,
    }

    logger.info(
        f"FourcastNet: submitting job for {lat},{lon} on {target_date} "
        f"(hours_ahead={hours_ahead:.1f}, steps={simulation_length})"
    )

    session = requests.Session()
    response = session.post(FOURCASTNET_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    if response.status_code == 200:
        logger.info("FourcastNet: synchronous response received")
        return _parse_and_verdict(response.content, lat, lon, min_temp, max_temp)

    if response.status_code != 202:
        raise Exception(f"FourcastNet unexpected initial status {response.status_code}")

    request_id = response.headers.get("nvcf-reqid")
    if not request_id:
        raise Exception("FourcastNet 202 response missing nvcf-reqid header")

    logger.info(f"FourcastNet: polling job {request_id}")
    status_url = f"{FOURCASTNET_POLL_URL}/{request_id}"

    for poll_num in range(FOURCASTNET_MAX_POLLS):
        response = session.get(status_url, headers=headers, allow_redirects=False, timeout=30)
        response.raise_for_status()

        if response.status_code == 200:
            logger.info(f"FourcastNet: job complete after {poll_num + 1} polls")
            return _parse_and_verdict(response.content, lat, lon, min_temp, max_temp)

        elif response.status_code == 302:
            asset_url = response.headers.get("Location")
            logger.info(f"FourcastNet: downloading large asset from {asset_url}")
            with requests.get(asset_url, stream=True, timeout=120) as r:
                r.raise_for_status()
                return _parse_and_verdict(r.content, lat, lon, min_temp, max_temp)

        elif response.status_code == 202:
            logger.info(f"FourcastNet: job still running (poll {poll_num + 1}/{FOURCASTNET_MAX_POLLS})")
            time.sleep(FOURCASTNET_POLL_SECONDS)

        else:
            raise Exception(f"FourcastNet unexpected poll status {response.status_code}")

    raise Exception(f"FourcastNet job timed out after {FOURCASTNET_MAX_POLLS} polls")


def _parse_and_verdict(content: bytes, lat: float, lon: float, min_temp: int, max_temp: int) -> dict:
    """
    Parses the FourcastNet zip output. Extracts 2m temperature (t2m) at the
    nearest grid point to lat/lon and converts Kelvin → Fahrenheit.
    Returns a structured verdict dict matching the original AI analyzer interface.
    """
    import netCDF4 as nc

    if len(content) < 100:
        raise Exception(f"FourcastNet response too small to be valid: {len(content)} bytes")

    try:
        zf = zipfile.ZipFile(io.BytesIO(content))
    except zipfile.BadZipFile:
        raise Exception(
            f"FourcastNet response is not a valid zip file. "
            f"First 200 bytes: {content[:200]}"
        )

    nc_files = sorted([f for f in zf.namelist() if f.endswith(".nc") or f.endswith(".nc4")])
    logger.info(f"FourcastNet zip contains {len(nc_files)} netCDF files: {nc_files}")

    if not nc_files:
        all_files = zf.namelist()
        raise Exception(
            f"No .nc files found in FourcastNet zip. "
            f"Zip contents: {all_files}"
        )

    nc_file = nc_files[-1]
    nc_data = zf.read(nc_file)

    with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as tmp:
        tmp.write(nc_data)
        tmp_path = tmp.name

    try:
        ds = nc.Dataset(tmp_path)
        logger.info(f"FourcastNet netCDF variables: {list(ds.variables.keys())}")
        logger.info(f"FourcastNet netCDF dimensions: {list(ds.dimensions.keys())}")

        lat_candidates = ["lat", "latitude", "y", "LAT", "XLAT"]
        lon_candidates = ["lon", "longitude", "x", "LON", "XLONG"]

        lats = None
        for name in lat_candidates:
            if name in ds.variables:
                lats = ds.variables[name][:]
                break

        lons = None
        for name in lon_candidates:
            if name in ds.variables:
                lons = ds.variables[name][:]
                break

        if lats is None:
            n_lat = ds.dimensions.get("lat", ds.dimensions.get("latitude", ds.dimensions.get("y"))).size
            lats = np.linspace(-90, 90, n_lat)
        if lons is None:
            n_lon = ds.dimensions.get("lon", ds.dimensions.get("longitude", ds.dimensions.get("x"))).size
            lons = np.linspace(0, 360, n_lon)

        target_lon = lon if lon >= 0 else lon + 360
        lat_idx = int(np.argmin(np.abs(np.array(lats) - lat)))
        lon_idx = int(np.argmin(np.abs(np.array(lons) - target_lon)))

        t2m_candidates = ["t2m", "T2m", "T2M", "temperature", "2m_temperature", "tas", "temp", "T"]
        t2m_var = None
        for name in t2m_candidates:
            if name in ds.variables:
                t2m_var = ds.variables[name]
                break

        if t2m_var is None:
            raise Exception(
                f"No 2m temperature variable found. "
                f"Available: {list(ds.variables.keys())}"
            )

        shape = t2m_var.shape
        logger.info(f"FourcastNet t2m shape: {shape}")

        if len(shape) == 3:
            t_raw = float(t2m_var[-1, lat_idx, lon_idx])
        elif len(shape) == 2:
            t_raw = float(t2m_var[lat_idx, lon_idx])
        elif len(shape) == 4:
            t_raw = float(t2m_var[-1, 0, lat_idx, lon_idx])
        else:
            t_raw = float(t2m_var.flatten()[-1])

        ds.close()

        if t_raw > 200:
            t_celsius = t_raw - 273.15
        else:
            t_celsius = t_raw

        t_fahrenheit = int(round((t_celsius * 9 / 5) + 32))
        logger.info(
            f"FourcastNet: extracted t2m={t_raw:.2f} → {t_celsius:.1f}°C → {t_fahrenheit}°F "
            f"at lat_idx={lat_idx}, lon_idx={lon_idx}"
        )

    finally:
        os.unlink(tmp_path)

    inside_bucket = min_temp <= t_fahrenheit <= max_temp

    verdict = "TRADE" if inside_bucket else "SKIP"
    if inside_bucket:
        reason = (
            f"FourcastNet predicts {t_fahrenheit}°F at this location, "
            f"which falls inside the market bucket [{min_temp}–{max_temp}°F]."
        )
    else:
        diff = min(abs(t_fahrenheit - min_temp), abs(t_fahrenheit - max_temp))
        reason = (
            f"FourcastNet predicts {t_fahrenheit}°F at this location, "
            f"which is {diff}°F outside the market bucket [{min_temp}–{max_temp}°F]."
        )

    return {
        "predicted_temp": t_fahrenheit,
        "sources_agree": None,
        "inside_bucket": inside_bucket,
        "simmer_edge_confirms": None,
        "verdict": verdict,
        "reason": reason,
        "model": "nvidia/fourcastnet",
    }


async def analyze_with_ai(
    market: dict,
    context: dict,
    noaa_temp: int,
    openmeteo_temp: int,
    wunderground_temp: int,
) -> dict:
    """
    Calls NVIDIA FourcastNet atmospheric model for a 4th independent temperature forecast.
    Returns a verdict dict with predicted_temp, inside_bucket, verdict, reason.
    Raises an exception if the API call fails or response cannot be parsed.
    """
    from city_map import resolve_city

    city_name = market.get("city", "")
    try:
        city_data = resolve_city(city_name)
    except ValueError:
        raise Exception(f"Cannot resolve city '{city_name}' for FourcastNet coordinates")

    lat = city_data["lat"]
    lon = city_data["lon"]
    target_date = market.get("date")
    if target_date is None:
        from datetime import date as date_cls
        target_date = date_cls.today()

    min_temp = market["min_temp"]
    max_temp = market["max_temp"]

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        _executor,
        _call_fourcastnet_sync,
        lat, lon, target_date, min_temp, max_temp
    )

    consensus = round((noaa_temp + openmeteo_temp + wunderground_temp) / 3)
    spread_3 = max(noaa_temp, openmeteo_temp, wunderground_temp) - min(noaa_temp, openmeteo_temp, wunderground_temp)

    fc_temp = result["predicted_temp"]
    all_four = [noaa_temp, openmeteo_temp, wunderground_temp, fc_temp]
    spread_4 = max(all_four) - min(all_four)
    sources_agree = spread_3 <= 1
    simmer_edge = context.get("edge", {}).get("recommendation")
    simmer_edge_confirms = simmer_edge == "TRADE"

    result["sources_agree"] = sources_agree
    result["simmer_edge_confirms"] = simmer_edge_confirms

    if not sources_agree:
        result["verdict"] = "SKIP"
        result["reason"] = (
            f"FourcastNet: {fc_temp}°F. "
            f"Source spread={spread_3}°F exceeds ±1°F limit "
            f"(NOAA={noaa_temp}, OpenMeteo={openmeteo_temp}, Wunderground={wunderground_temp}). "
            f"All sources must agree within ±1°F."
        )
    elif not result["inside_bucket"]:
        pass
    else:
        result["verdict"] = "TRADE"

    logger.info(
        f"FourcastNet verdict: {result['verdict']} | "
        f"fc_temp={fc_temp}°F | sources_agree={sources_agree} | "
        f"inside_bucket={result['inside_bucket']} | "
        f"reason={result['reason']}"
    )
    return result
