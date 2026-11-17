#!/usr/bin/env python3
"""
dj_main.py — 情境 DJ 主入口
一句話啟動，自動偵測情境 + 生成歌單 + 開始播放
"""

import sys
import json
import argparse
from pathlib import Path

DATA_DIR = Path.home() / ".smart-playlist-dj"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = DATA_DIR / "config.json"


# ── Config ──────────────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "city": "Taipei",
    "morning_preset": "morning",
    "work_preset": "work",
    "evening_preset": "relaxed",
    "sleepy_preset": "sleepy",
    "default_limit": 12,
    "auto_play": True,
    "auto_refresh_hours": 24,
}

def load_config() -> dict:
    if CONFIG_FILE.exists():
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return {**DEFAULT_CONFIG, **cfg}
    return DEFAULT_CONFIG.copy()

def save_config(cfg: dict):
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Scenes ──────────────────────────────────────────────────────────────────

SCENES = {
    "morning":   ("☀️ 晨間喚醒",   "energized", 3, "morning"),
    "work":      ("🎯 專注工作",   "focused",   2, "work"),
    "exercise":  ("💪 健身打氣",   "energized", 5, "exercise"),
    "commute":   ("🚶 通勤時光",   "relaxed",   2, "commute"),
    "cafe":      ("☕ 咖啡時光",   "relaxed",   2, "cafe"),
    "chill":     ("🌿 放鬆時刻",   "relaxed",   2, "evening"),
    "sleepy":    ("🌙 睡前時光",   "calm",      1, "sleepy"),
    "rainy":     ("🌧️ 雨天配咖啡", "nostalgic", 2, "cafe"),
    "party":     ("🎉 派對嗨歌",   "party",     5, "just_listening"),
    "romantic":  ("💕 浪漫時光",   "romantic",  3, "evening"),
}


# ── TTS text generator ─────────────────────────────────────────────────────

def tts_for_preset(preset: str) -> str:
    """生成適合 TTS朗讀 的文案"""
    tts_map = {
        "morning":  "早安！為你準備了充滿活力的晨間歌單，用音樂開啟美好的一天！☀️🎵",
        "work":     "專注模式啟動 🎯 讓這些音樂幫你進入心流状態...",
        "exercise": "健身時間到！💪 跟著節奏動起來！",
        "relaxed":  "放鬆一下 🌿 讓這些旋律輕輕擁抱你...",
        "sleepy":   "晚安 🌙 這些溫柔的音符會陪你慢慢入睡...",
        "rainy":    "雨聲與音樂最配了 ☕ 享受這個片刻...",
        "party":    "派對時間！🎉 今晚就是狂歡夜！",
        "romantic": "浪漫的旋律 💕 願你擁有甜蜜的時光...",
        "focused":  "專注工作中 🎯 讓我為你選一些輕柔的背景音...",
    }
    return tts_map.get(preset, f"為你選了這個歌單 🎵 享受音樂時光...")


def tts_intro(mood_label: str, weather_desc: str) -> str:
    if weather_desc != "未知":
        return f"現在是{mood_label}，天氣{weather_desc}，為你選了適合的音樂 🎧"
    return f"現在是{mood_label}，為你選了適合的音樂 🎧"


# ── Main DJ flow ────────────────────────────────────────────────────────────

def dj_flow(preset: str = None, city: str = "Taipei",
            auto_play: bool = True, limit: int = 12,
            refresh: bool = False) -> dict:
    """
    完整 DJ 流程
    """
    # 1. Load mood detector + playlist generator
    sys.path.insert(0, str(Path(__file__).parent))
    from mood_detector import detect, mood_description, bpm_range
    from playlist_generator import generate_playlist, render_playlist, fetch_library, PRESETS as PL_PRESETS

    # 2. Auto-detect context
    ctx = detect(city=city, skip_weather=False)

    # 3. Determine preset
    if preset is None:
        # Auto-select based on context
        activity = ctx.get("activity", "")
        mood     = ctx.get("mood", "")
        time_hr  = __import__("datetime").datetime.now().hour

        if activity == "morning" or (time_hr >= 5 and time_hr < 9):
            preset = "morning"
        elif activity == "work" or mood == "focused":
            preset = "work"
        elif activity == "exercise":
            preset = "exercise"
        elif activity == "sleepy" or time_hr >= 22:
            preset = "sleepy"
        elif mood == "nostalgic" or ctx.get("weather", {}).get("weather_mood") == "rainy":
            preset = "rainy"
        elif mood == "party" or mood == "angry":
            preset = "party"
        elif mood == "romantic":
            preset = "romantic"
        else:
            preset = "relaxed"
    else:
        preset = preset.lower().replace(" ", "_")

    # 4. Generate playlist
    print(f"\n🎛️  情境 DJ：自動偵測 → {preset}")

    tracks = fetch_library(limit=300, refresh=refresh)
    playlist = generate_playlist(preset=preset, limit=limit, tracks=tracks)

    # 5. Render
    output = render_playlist(playlist)

    # 6. Play
    if auto_play and tracks:
        from music_player import play_search, next_track
        first = playlist["tracks"][0] if playlist["tracks"] else None
        if first:
            # Play first track
            title = first.get("name", "")
            result = play_search(title)
            if "❌" not in result:
                print(f"\n▶️  已開始播放：{first['name']} — {first['artist']}")
            else:
                print(f"\n⚠️  無法自動播放，請手動在 Music.app 播放")

    return {
        "playlist": playlist,
        "context": ctx,
        "preset": preset,
        "tts_intro": tts_intro(ctx.get("label",""), ctx.get("weather",{}).get("desc","")),
        "tts_body":  tts_for_preset(preset),
        "rendered":  output,
    }


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🎧 情境 DJ")
    parser.add_argument("scene", nargs="?", default=None,
                        choices=list(SCENES.keys()) + ["auto", "list"],
                        help="場景（留空則自動偵測）")
    parser.add_argument("-c", "--city", default="Taipei")
    parser.add_argument("-n", "--limit", type=int, default=12)
    parser.add_argument("--no-play", action="store_true")
    parser.add_argument("-r", "--refresh", action="store_true")
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("--config", action="store_true",
                        help="設定城市等配置")
    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["auto"])

    if args.scene == "list":
        print("\n🎛️  可用場景：\n")
        for k, (label, mood, energy, act) in SCENES.items():
            print(f"  {k:<12} {label}  (mood={mood}, energy={energy})")
        return

    if args.config:
        cfg = load_config()
        print(f"\n⚙️  當前設定：")
        print(json.dumps(cfg, ensure_ascii=False, indent=2))
        city = input(f"\n  城市 [{cfg['city']}]： ").strip()
        if city:
            cfg["city"] = city
        save_config(cfg)
        print("✅ 已儲存")
        return

    preset = None if (args.scene == "auto" or args.scene is None) else args.scene

    result = dj_flow(preset=preset, city=args.city,
                     auto_play=not args.no_play,
                     limit=args.limit, refresh=args.refresh)

    if args.json:
        print(json.dumps(result["playlist"], ensure_ascii=False, indent=2))
    else:
        print(result["rendered"])

        # TTS hints
        print("─" * 56)
        print(f"\n  🔈 TTS intro：{result['tts_intro']}")
        print(f"  🔈 TTS body ：{result['tts_body']}")
        print()


if __name__ == "__main__":
    main()
