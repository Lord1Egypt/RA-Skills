#!/usr/bin/env python3
"""Render a single Pan-Weather sprite (temp/precip/wind) via py-math-viz."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict
from urllib.request import urlopen

from zoneinfo import ZoneInfo

import matplotlib.pyplot as plt
import seaborn as sns


API_URL = "https://api.open-meteo.com/v1/forecast"


@dataclass
class HourlyWindow:
    time: list[str]
    temperature_2m: list[float]
    precipitation: list[float]
    precipitation_probability: list[float]
    windspeed_10m: list[float]
    cloudcover: list[float]


def fetch_hourly_data(latitude: float, longitude: float, timezone: str) -> Dict[str, list[float]]:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,precipitation_probability,windspeed_10m,cloudcover",
        "forecast_days": 2,
        "timezone": timezone,
    }
    query = "&".join(f"{key}={value}" for key, value in params.items())
    with urlopen(f"{API_URL}?{query}") as resp:
        payload = json.load(resp)
    return payload["hourly"]


def build_window(hourly: Dict[str, list[float]], timezone: str) -> HourlyWindow:
    zone = ZoneInfo(timezone)
    now = datetime.now(zone)
    end = now + timedelta(hours=24)
    selected = {key: [] for key in hourly}
    for i, timestr in enumerate(hourly["time"]):
        dt = datetime.fromisoformat(timestr)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=zone)
        if now <= dt < end:
            for key in hourly:
                selected[key].append(hourly[key][i])
        if len(selected["time"]) >= 24:
            break
    return HourlyWindow(
        time=selected["time"],
        temperature_2m=selected["temperature_2m"],
        precipitation=selected["precipitation"],
        precipitation_probability=selected["precipitation_probability"],
        windspeed_10m=selected["windspeed_10m"],
        cloudcover=selected["cloudcover"],
    )


def render(window: HourlyWindow, city_label: str, output: str, lang: str = "ru") -> None:
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)
    fig.patch.set_facecolor("#fbfbfb")

    labels = [datetime.fromisoformat(t).strftime("%H:%M") for t in window.time]

    if lang == "en":
        title_temp = f"Temperature, °C ({city_label}, next 24h)"
        title_precip = "Precipitation (mm) and probability (%)"
        title_wind = "Wind and cloud cover"
        ylabel_temp = "°C"
        ylabel_mm = "mm"
        ylabel_prob = "%"
        ylabel_wind = "m/s"
        ylabel_cloud = "%"
    else:
        title_temp = f"Температура, °C ({city_label}, след. 24ч)"
        title_precip = "Осадки (мм) и вероятность (%)"
        title_wind = "Ветер и облачность"
        ylabel_temp = "°C"
        ylabel_mm = "мм"
        ylabel_prob = "%"
        ylabel_wind = "м/с"
        ylabel_cloud = "%"

    axes[0].plot(labels, window.temperature_2m, color="#c82c2c", marker="o", linewidth=2)
    axes[0].fill_between(labels, window.temperature_2m, color="#dda0a0", alpha=0.35)
    axes[0].set_title(title_temp, loc="left")
    axes[0].set_ylabel(ylabel_temp, color="#c82c2c")
    axes[0].tick_params(axis="y", colors="#c82c2c")
    axes[0].grid(axis="y", linestyle="--", alpha=0.45)

    axes[1].bar(labels, window.precipitation, color="#5aa9f7", alpha=0.8)
    axes[1].set_ylabel(ylabel_mm, color="#5aa9f7")
    axes[1].tick_params(axis="y", colors="#5aa9f7")
    axes[1].set_title(title_precip, loc="left")
    axes[1].grid(axis="y", linestyle="--", alpha=0.45)
    twin_prob = axes[1].twinx()
    twin_prob.plot(labels, window.precipitation_probability, color="#8a2be2", marker="o", linewidth=2)
    twin_prob.set_ylabel(ylabel_prob, color="#8a2be2")
    twin_prob.tick_params(axis="y", colors="#8a2be2")
    twin_prob.set_ylim(0, max(max(window.precipitation_probability, default=0), 100) * 1.05)

    axes[2].plot(labels, window.windspeed_10m, color="#2c8a2c", marker="o", linewidth=2)
    axes[2].set_ylabel(ylabel_wind, color="#2c8a2c")
    axes[2].tick_params(axis="y", colors="#2c8a2c")
    axes[2].set_title(title_wind, loc="left")
    axes[2].grid(axis="y", linestyle="--", alpha=0.45)
    twin_cloud = axes[2].twinx()
    twin_cloud.plot(labels, window.cloudcover, color="#7f7f7f", linestyle="--", marker="s", linewidth=2)
    twin_cloud.set_ylabel(ylabel_cloud, color="#7f7f7f")
    twin_cloud.tick_params(axis="y", colors="#7f7f7f")
    twin_cloud.set_ylim(0, 110)

    for ax in axes:
        ax.set_xticks(labels[::3])
        ax.set_xticklabels(labels[::3], rotation=45)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)

    twin_prob.spines["top"].set_visible(False)
    twin_cloud.spines["top"].set_visible(False)

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, facecolor="white")
    plt.close(fig)


def summarize(window: HourlyWindow, city_label: str, lang: str = "ru") -> str:
    min_temp = min(window.temperature_2m)
    max_temp = max(window.temperature_2m)
    min_temp_time = datetime.fromisoformat(window.time[window.temperature_2m.index(min_temp)]).strftime("%H:%M")
    max_temp_time = datetime.fromisoformat(window.time[window.temperature_2m.index(max_temp)]).strftime("%H:%M")
    max_precip = max(window.precipitation)
    max_precip_time = datetime.fromisoformat(window.time[window.precipitation.index(max_precip)]).strftime("%H:%M")
    max_precip_prob = max(window.precipitation_probability)
    max_wind = max(window.windspeed_10m)
    max_wind_time = datetime.fromisoformat(window.time[window.windspeed_10m.index(max_wind)]).strftime("%H:%M")

    if lang == "en":
        return (
            f"{city_label}: {min_temp:.1f}° ({min_temp_time}) → {max_temp:.1f}° ({max_temp_time}); "
            f"max rain {max_precip:.1f} mm ({max_precip_time}, {max_precip_prob:.0f}%); "
            f"wind up to {max_wind:.1f} m/s ({max_wind_time})"
        )
    return (
        f"{city_label}: {min_temp:.1f}° ({min_temp_time}) → {max_temp:.1f}° ({max_temp_time}); "
        f"max дождь {max_precip:.1f} мм ({max_precip_time}, {max_precip_prob:.0f}%); "
        f"ветер до {max_wind:.1f} м/с ({max_wind_time})"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a 24h weather sprite via py-math-viz")
    parser.add_argument("--output", "-o", default="out/weather_all.png", help="PNG path")
    parser.add_argument("--summary", "-s", action="store_true", help="Print text summary")
    parser.add_argument("--latitude", type=float, default=55.7887)
    parser.add_argument("--longitude", type=float, default=49.1221)
    parser.add_argument("--timezone", default="Europe/Moscow")
    parser.add_argument("--city-label", default="Казань")
    parser.add_argument("--lang", choices=["ru", "en"], default="ru", help="Label language (ru/en)")
    args = parser.parse_args()

    hourly = fetch_hourly_data(args.latitude, args.longitude, args.timezone)
    window = build_window(hourly, args.timezone)
    render(window, args.city_label, args.output, lang=args.lang)
    if args.summary:
        print(summarize(window, args.city_label, lang=args.lang))


if __name__ == "__main__":
    main()
