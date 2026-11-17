#!/usr/bin/env python3
"""
mood_detector.py — 情境感知 mood detector
根據：時間 + 天氣 + 互動問答 → 輸出 mood + activity + energy 等級
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

# ── Data dir ─────────────────────────────────────────────────────────────────

DATA_DIR = Path.home() / ".smart-playlist-dj"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROFILE_FILE = DATA_DIR / "mood_profile.json"


# ── Time-based defaults ──────────────────────────────────────────────────────

def _time_mood() -> dict:
    """根據時段推斷 mood"""
    hour = datetime.now().hour
    if 5 <= hour < 9:
        return {"mood": "energized", "energy": 3, "activity": "morning", "label": "晨間喚醒 ☀️"}
    elif 9 <= hour < 12:
        return {"mood": "focused", "energy": 2, "activity": "work", "label": "專注工作 🎯"}
    elif 12 <= hour < 14:
        return {"mood": "relaxed", "energy": 2, "activity": "lunch", "label": "午餐時光 🍜"}
    elif 14 <= hour < 17:
        return {"mood": "focused", "energy": 2, "activity": "work", "label": "午後工作 🎯"}
    elif 17 <= hour < 20:
        return {"mood": "energized", "energy": 3, "activity": "exercise", "label": "健身打氣 💪"}
    elif 20 <= hour < 22:
        return {"mood": "relaxed", "energy": 2, "activity": "evening", "label": "晚間放鬆 🌆"}
    else:
        return {"mood": "calm", "energy": 1, "activity": "sleepy", "label": "睡前時光 🌙"}


# ── Weather ──────────────────────────────────────────────────────────────────

def _fetch_weather(city: str = "Taipei") -> dict:
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        current = data["current_condition"][0]
        desc = current["weatherDesc"][0]["value"]
        temp  = current["temp_C"]
        code  = int(current["weatherCode"][0])

        # Map weather code to mood influence
        rainy_codes = [1063, 1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189, 1192, 1195, 1240, 1243, 1246]
        if code in rainy_codes:
            weather_mood = "rainy"
        elif "Sunny" in desc or "Clear" in desc:
            weather_mood = "sunny"
        elif "Cloud" in desc or "Overcast" in desc:
            weather_mood = "cloudy"
        elif "Storm" in desc or "Thunder" in desc:
            weather_mood = "stormy"
        else:
            weather_mood = "neutral"

        return {"desc": desc, "temp": temp, "code": code, "weather_mood": weather_mood}
    except Exception:
        return {"desc": "未知", "temp": 25, "code": 0, "weather_mood": "neutral"}


def _weather_adjust(base: dict, weather: dict) -> dict:
    """根據天氣微調"""
    wm = weather.get("weather_mood", "neutral")
    adj = dict(base)
    if wm == "rainy":
        adj["mood"] = "nostalgic"
        adj["energy"] = max(1, adj["energy"] - 1)
        adj["label"] += " ☕ 雨聲相伴"
    elif wm == "sunny":
        adj["mood"] = "happy"
        adj["energy"] = min(5, adj["energy"] + 1)
        adj["label"] += " ☀️ 陽光正好"
    elif wm == "stormy":
        adj["mood"] = "intense"
        adj["energy"] = 5
        adj["label"] += " ⛈️ 風雨欲來"
    return adj


# ── Mood profile ─────────────────────────────────────────────────────────────

MOOD_OPTIONS = [
    ("1", "😊 開心振奮", "energized", 4),
    ("2", "😌 平靜放鬆", "relaxed", 2),
    ("3", "😔 憂鬱想念", "melancholic", 2),
    ("4", "😤 有點憤怒", "angry", 4),
    ("5", "😴 累了想休息", "calm", 1),
    ("6", "🤔 需要專注", "focused", 2),
    ("7", "🥰 甜蜜浪漫", "romantic", 3),
    ("8", "🤩 超嗨派對", "party", 5),
]


def _detect_from_questions() -> dict:
    """互動式 mood 偵測"""
    print("\n🎛️  情境 DJ — 讓我了解你現在的狀態：\n")
    print("  目前時間會自動參考，先回答幾個問題吧：\n")

    print("  你現在的心情是？")
    for num, label, *_ in MOOD_OPTIONS:
        print(f"    {num}. {label}")
    print()

    while True:
        try:
            choice = input("  選擇數字 [1-8]（直接 Enter 跳過）： ").strip()
            if not choice:
                return {}
            n = int(choice)
            if 1 <= n <= 8:
                _, label, mood, energy = MOOD_OPTIONS[n - 1]
                return {"mood": mood, "energy": energy, "label": label}
            print("  請輸入 1-8 的數字")
        except ValueError:
            print("  請輸入數字")

    return {}


def _activity_prompt() -> str | None:
    """問當下活動"""
    print("\n  現在在做什麼？")
    acts = [
        ("1", "工作 / 寫代碼", "work"),
        ("2", "運動 / 健身", "exercise"),
        ("3", "散步 / 通勤", "commute"),
        ("4", "做家事 / 整理", "chores"),
        ("5", "閱讀 / 學習", "reading"),
        ("6", "喝咖啡 / 發呆", "cafe"),
        ("7", "睡前準備", "sleepy"),
        ("8", "只是聽音樂", "just_listening"),
    ]
    for num, label, *_ in acts:
        print(f"    {num}. {label}")
    print()

    while True:
        try:
            choice = input("  選擇 [1-8]（直接 Enter 跳過）： ").strip()
            if not choice:
                return None
            n = int(choice)
            if 1 <= n <= 8:
                return acts[n-1][2]
        except ValueError:
            pass

    return None


# ── Main detector ────────────────────────────────────────────────────────────

def detect(city: str = "Taipei", force_questions: bool = False,
           skip_weather: bool = False) -> dict:
    """
    Returns a complete mood context dict:
    {mood, energy, activity, label, weather, time}
    """
    base = _time_mood()
    weather = {} if skip_weather else _fetch_weather(city)
    base = _weather_adjust(base, weather)

    if force_questions or sys.stdin.isatty():
        mood_q = _detect_from_questions()
        if mood_q:
            base.update(mood_q)
        act = _activity_prompt()
        if act:
            base["activity"] = act

    base["weather"] = weather
    base["time_label"] = _time_label()
    return base


def _time_label() -> str:
    hour = datetime.now().hour
    if hour < 6:  return "凌晨"
    elif hour < 9:  return "早晨"
    elif hour < 12: return "上午"
    elif hour < 14: return "中午"
    elif hour < 17: return "下午"
    elif hour < 20: return "傍晚"
    elif hour < 23: return "夜晚"
    return "深夜"


# ── Mood → BPM range ────────────────────────────────────────────────────────

def bpm_range(mood: str, energy: int) -> tuple[int, int]:
    """Mood + energy → BPM 範圍"""
    table = {
        "calm":      (60, 80),
        "relaxed":   (75, 95),
        "focused":   (80, 110),
        "melancholic":(60, 85),
        "romantic":  (70, 90),
        "energized": (100, 130),
        "happy":     (110, 140),
        "angry":     (120, 160),
        "party":     (130, 170),
        "nostalgic": (70, 95),
        "intense":   (140, 180),
    }
    return table.get(mood, (80, 110))


def mood_description(mood: str) -> str:
    descs = {
        "energized": "💥 充滿能量，想要爆發！",
        "happy":     "🌞 開心愉悅，陽光普照！",
        "focused":   "🎯 專注模式，進入心流！",
        "relaxed":   "🌿 輕鬆悠閒，享受當下！",
        "calm":      "🛋️ 平靜舒緩，準備休息！",
        "romantic":  "💕 浪漫甜蜜，甜甜的～",
        "melancholic":"🌧️ 憂鬱想念，有點感性",
        "angry":     "🔥 怒火中燒，需要宣洩！",
        "party":     "🎉 超嗨派對，盡情狂歡！",
        "nostalgic": "☕ 雨聲相伴，思緒萬千",
        "intense":   "⛈️ 風暴來襲，熱血沸騰！",
    }
    return descs.get(mood, "🎵 聽音樂的時光")


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🎛️ 情境 mood 偵測器")
    parser.add_argument("-c", "--city",    default="Taipei")
    parser.add_argument("-q", "--questions", action="store_true", help="強制互動問答")
    parser.add_argument("-j", "--json",    action="store_true",  help="JSON 輸出")
    parser.add_argument("--skip-weather", action="store_true")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--json"])

    ctx = detect(city=args.city, force_questions=args.questions,
                 skip_weather=args.skip_weather)

    if args.json:
        print(json.dumps(ctx, ensure_ascii=False, indent=2))
    else:
        print(f"\n🎛️  情境偵測結果")
        print(f"  時段：{ctx.get('time_label','?')}（{ctx.get('label','')}）")
        weather = ctx.get("weather", {})
        print(f"  天氣：{weather.get('desc','?')} {weather.get('temp','?')}°C")
        print(f"  Mood：{mood_description(ctx.get('mood',''))}")
        print(f"  活動：{ctx.get('activity','?')}")
        bpm_lo, bpm_hi = bpm_range(ctx.get("mood",""), ctx.get("energy",2))
        print(f"  建議 BPM：{bpm_lo} – {bpm_hi}")


if __name__ == "__main__":
    main()
