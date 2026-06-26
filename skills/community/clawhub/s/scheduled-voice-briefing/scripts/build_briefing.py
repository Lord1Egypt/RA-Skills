#!/usr/bin/env python3
"""
Assemble a bounded briefing text from a structured config.

This public example focuses on content assembly only and does not bundle
provider-specific playback, local workspace assumptions, or external API integrations.
"""

from __future__ import annotations
import argparse
import json
from datetime import datetime
from pathlib import Path

WEEKDAYS_ZH = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
WEATHER_DESC_ZH = {
    "Light rain shower": "小阵雨",
    "Patchy rain nearby": "附近有零星小雨",
    "Partly Cloudy": "多云间晴",
    "Partly cloudy": "多云间晴",
    "Sunny": "晴",
    "Overcast": "阴天",
    "Clear": "晴朗",
    "Clear ": "晴朗",
}


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_weather_desc(desc: str) -> str:
    return WEATHER_DESC_ZH.get(desc, desc)


def build_text(config: dict, now: datetime) -> str:
    speaker = config.get("speaker", {})
    schedules = config.get("schedules", [])
    modules = schedules[0].get("modules", []) if schedules else []
    tone = speaker.get("tone", "calm")
    weekday = WEEKDAYS_ZH[now.isoweekday() - 1]

    briefing = schedules[0].get("briefing", {}) if schedules else {}
    weather = briefing.get("weather", {}) if isinstance(briefing, dict) else {}
    opening = briefing.get("opening") or "早上好。"
    closing = briefing.get("closing") or "祝你今天顺利。"
    custom_text = briefing.get("customText") if briefing.get("includeCustomText") else ""

    parts: list[str] = []
    parts.append(opening)
    parts.append(f"今天是{now.month}月{now.day}日，{weekday}。")

    if "environment_brief" in modules:
        if isinstance(weather, dict) and weather:
            location = weather.get("location", "当前所在城市")
            current_temp = weather.get("tempC")
            raw_desc = weather.get("desc", "天气情况正常")
            desc = normalize_weather_desc(str(raw_desc))
            max_temp = weather.get("maxTempC")
            min_temp = weather.get("minTempC")
            summary = weather.get("summary", "")
            weather_sentence = f"现在为你播报{location}的天气。"
            if current_temp is not None:
                weather_sentence += f" 当前大约{current_temp}度，{desc}。"
            if max_temp is not None and min_temp is not None:
                weather_sentence += f" 今天最高{max_temp}度，最低{min_temp}度。"
            if summary:
                weather_sentence += f" {summary}。"
            parts.append(weather_sentence)
        else:
            parts.append("现在为你播报天气信息。")

    if "schedule_brief" in modules:
        parts.append("下面是今天的日程摘要。")

    tone_map = {
        "calm": "我会用温和、清晰的方式继续播报。",
        "energetic": "我会用更有精神的方式继续播报。",
        "gentle": "我会用更轻柔的方式继续播报。",
    }
    parts.append(tone_map.get(tone, "我会用自然、清晰的方式继续播报。"))

    if custom_text:
        parts.append(str(custom_text).strip())
    parts.append(closing)
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--now")
    args = parser.parse_args()
    now = datetime.fromisoformat(args.now) if args.now else datetime.now()
    config = load_config(Path(args.config))
    print(build_text(config, now))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
