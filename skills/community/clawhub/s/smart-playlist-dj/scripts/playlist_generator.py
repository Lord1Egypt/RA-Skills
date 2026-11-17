#!/usr/bin/env python3
"""
playlist_generator.py — 智慧播放列表生成器
讀取本地音樂庫（macOS Music.app），根據 mood/bpm/activity 智能排序
"""

import sys
import json
import subprocess
import re
import argparse
import random
from pathlib import Path
from datetime import datetime

DATA_DIR = Path.home() / ".smart-playlist-dj"
DATA_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = DATA_DIR / "playlist_history.json"
TRACK_CACHE  = DATA_DIR / "track_cache.json"


# ── Music.app 讀取 ───────────────────────────────────────────────────────────

def _run_music(script: str) -> str:
    """透過 osascript 與 Music.app 溝通"""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=20
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR:{e}"


def fetch_library(limit: int = 300, refresh: bool = False) -> list[dict]:
    """讀取本地音樂庫（macOS AppleScript，逐軌 pipe 分隔）"""
    if not refresh and TRACK_CACHE.exists():
        age = datetime.now() - datetime.fromtimestamp(TRACK_CACHE.stat().st_mtime)
        if age.days < 1:
            return json.loads(TRACK_CACHE.read_text(encoding="utf-8"))

    print("🎵 正在同步 Music.app 資料庫...")

    script = """
tell application "Music"
    set allTracks to every file track of library playlist 1
    set out to ""
    repeat with aTrack in allTracks
        try
            set n  to name of aTrack
            set ar to (artist of aTrack) as string
            set gn to (genre of aTrack) as string
            set du to (duration of aTrack) as string
            set ln to n & "||" & ar & "||" & gn & "||" & du
            if out is "" then
                set out to ln
            else
                set out to out & linefeed & ln
            end if
        end try
    end repeat
    return out
end tell
"""
    output = _run_music(script)
    if output.startswith("ERROR:") or not output.strip():
        print("⚠️  Music.app 無法讀取（請確認 Music.app 已開啟且有歌曲）")
        TRACK_CACHE.write_text("[]", encoding="utf-8")
        return []

    tracks = []
    for line in output.splitlines():
        line = line.strip()
        if not line: continue
        raw = line.split("||")
        name   = raw[0] if len(raw) > 0 else ""
        artist = raw[1] if len(raw) > 1 else ""
        # Format: name||artist||genre||duration  (genre may be empty → "name||artist||duration")
        name   = raw[0]
        artist = raw[1] if len(raw) > 1 else ""
        # Find duration: last numeric field, everything before it is genre
        dur = ""
        genre = ""
        numeric_fields = [f for f in raw[2:] if f.strip() and f.strip().replace(".","").isdigit()]
        if numeric_fields:
            dur   = numeric_fields[-1]
            g_idx = raw.index(dur, 2)  # position of duration in raw
            genre = "||".join(raw[2:g_idx])  # everything between artist and dur is genre
        elif len(raw) > 2:
            genre = raw[2]
        if not name: continue
        try: duration_s = float(dur) if dur else 0
        except: duration_s = 0
        tracks.append({
            "id":       f"{artist}:{name}",
            "name":     name,
            "artist":   artist or "未知",
            "album":    "",
            "year":     "",
            "genre":    genre,
            "duration": duration_s,
            "bpm":      None,
            "rating":   0,
            "score":    0.0,
        })

    TRACK_CACHE.write_text(json.dumps(tracks, ensure_ascii=False), encoding="utf-8")
    print(f"✅ 已載入 {len(tracks)} 首歌曲")
    return tracks



GENRE_MOOD = {
    "rock":      "energetic",
    "pop":       "happy",
    "jazz":      "relaxed",
    "classical": "relaxed",
    "electronic":"energetic",
    "hip-hop":   "energetic",
    "r&b":       "chill",
    "country":   "relaxed",
    "blues":     "melancholy",
    "metal":     "energetic",
    "indie":     "melancholy",
    "folk":      "relaxed",
    "ambient":   "relaxed",
    "soundtrack":"relaxed",
    "dance":     "energetic",
    "soul":      "chill",
    "reggae":    "relaxed",
    "punk":      "energetic",
    "lo-fi":     "focused",
    "chillout":  "relaxed",
}

GENRE_MOOD_ZH = {
    "搖滾":"energetic","搖滾樂":"energetic",
    "流行":"happy","流行音樂":"happy",
    "爵士":"relaxed","爵士樂":"relaxed",
    "古典":"relaxed","古典音樂":"relaxed",
    "電子":"energetic","電子音樂":"energetic",
    "說唱":"energetic","嘻哈":"energetic",
    "民謠":"relaxed","鄉村":"relaxed",
    "藍調":"melancholy","布魯斯":"melancholy",
    "金屬":"energetic",
    "獨立":"melancholy",
    "氛圍":"relaxed","環境音樂":"relaxed",
    "原聲帶":"relaxed","電影配樂":"relaxed",
    "靈魂樂":"chill","節奏藍調":"chill",
    "雷鬼":"relaxed",
    "Lo-Fi":"focused","Lo-Fi音樂":"focused",
    "放鬆":"relaxed","輕音樂":"relaxed",
    "輕音樂":"relaxed",
    "另類":"melancholy","另類搖滾":"melancholy",
}

def _genre_to_mood(genre: str) -> str | None:
    g = genre.lower()
    for k, v in GENRE_MOOD.items():
        if k in g:
            return v
    for k, v in GENRE_MOOD_ZH.items():
        if k in genre:
            return v
    return None


# ── Scoring engine ───────────────────────────────────────────────────────────

def score_tracks(tracks: list[dict], mood: str, energy: int,
                 activity: str, bpm_range: tuple[int, int]) -> list[dict]:
    """
    對曲目評分，越高越適合當前情境
    """
    bpm_lo, bpm_hi = bpm_range
    scored = []

    # BPM weight by activity
    bpm_preference = {
        "work":      (0.6, 0.3),  # (want_bpm, penalize_far)
        "exercise":  (1.0, 0.5),
        "commute":   (0.4, 0.2),
        "cafe":      (0.2, 0.1),
        "sleepy":    (0.1, 0.1),
        "evening":   (0.3, 0.2),
        "morning":   (0.8, 0.4),
        "reading":   (0.1, 0.1),
        "chores":    (0.7, 0.3),
        "just_listening": (0.3, 0.2),
    }
    bpm_w, bpm_p = bpm_preference.get(activity, (0.5, 0.3))

    # Mood/energy → target BPM
    target_bpm = {
        1: (60, 85),   # calm
        2: (80, 105),  # relaxed/focused
        3: (100, 125), # energized
        4: (120, 145), # angry/happy
        5: (135, 175), # party
    }
    target_lo, target_hi = target_bpm.get(energy, (80, 110))

    # Genre energy
    genre_energy = {
        "energized": (120, 180), "happy": (100, 150), "party": (130, 175),
        "angry": (120, 170), "romantic": (70, 100), "relaxed": (80, 110),
        "focused": (75, 105), "melancholic": (60, 90), "calm": (55, 85),
        "nostalgic": (70, 100), "intense": (140, 180),
    }

    for track in tracks:
        score = 0.0
        reasons = []

        # BPM scoring
        bpm = track.get("bpm")
        if bpm and bpm > 0:
            if bpm_lo <= bpm <= bpm_hi:
                score += 2.0
                reasons.append(f"BPM match")
            else:
                dist = min(abs(bpm - bpm_lo), abs(bpm - bpm_hi))
                penalty = min(dist / 100.0, 1.0) * bpm_p
                score -= penalty
        else:
            # No BPM → use genre inference
            genre = track.get("genre", "")
            inferred_mood = _genre_to_mood(genre)
            if inferred_mood == mood:
                score += 1.5
                reasons.append(f"Genre match ({genre})")

        # Rating bonus
        rating = track.get("rating", 0)
        if rating >= 80:
            score += 1.5
            reasons.append(f"High rated {rating}")
        elif rating >= 50:
            score += 0.5

        # Time-of-day fit (simple)
        # Prefer older songs for nostalgic/melancholic
        if mood in ("nostalgic", "melancholic", "romantic"):
            try:
                year = int(track.get("year", 0))
                if 1970 <= year <= 2010:
                    score += 1.0
                    reasons.append(f"Classic era {year}")
            except ValueError:
                pass

        # Randomize slightly to avoid always same order
        score += random.uniform(-0.3, 0.3)

        track["score"] = round(score, 3)
        track["reasons"] = reasons
        scored.append(track)

    scored.sort(key=lambda t: -t["score"])
    return scored


# ── Playlist generation ───────────────────────────────────────────────────────

PRESETS: dict[str, dict] = {
    "morning": {
        "mood": "energized", "energy": 3, "activity": "morning",
        "length": 10, "label": "☀️ 晨間喚醒歌單",
        "desc": "用輕快的節奏開啟美好的一天！"
    },
    "work": {
        "mood": "focused", "energy": 2, "activity": "work",
        "length": 15, "label": "🎯 專注工作歌單",
        "desc": "幫助進入心流狀態的節奏..."
    },
    "exercise": {
        "mood": "energized", "energy": 5, "activity": "exercise",
        "length": 12, "label": "💪 健身打氣歌單",
        "desc": "爆汗音樂！讓心跳跟節奏同步！"
    },
    "relaxed": {
        "mood": "relaxed", "energy": 2, "activity": "evening",
        "length": 10, "label": "🌿 晚間放鬆歌單",
        "desc": "卸下一天的疲憊，輕輕鬆鬆..."
    },
    "sleepy": {
        "mood": "calm", "energy": 1, "activity": "sleepy",
        "length": 8, "label": "🌙 睡前時光",
        "desc": "慢慢沉入溫柔的旋律..."
    },
    "rainy": {
        "mood": "nostalgic", "energy": 2, "activity": "cafe",
        "length": 10, "label": "☕ 雨天配咖啡",
        "desc": "雨聲相伴，思緒萬千..."
    },
    "party": {
        "mood": "party", "energy": 5, "activity": "just_listening",
        "length": 15, "label": "🎉 派對嗨歌",
        "desc": "今晚就是狂歡夜！"
    },
    "romantic": {
        "mood": "romantic", "energy": 3, "activity": "evening",
        "length": 10, "label": "💕 浪漫時光",
        "desc": "兩個人輕輕搖擺的旋律..."
    },
}


def _duration_str(s: float) -> str:
    m = int(s // 60)
    sec = int(s % 60)
    return f"{m}:{sec:02d}"


def generate_playlist(preset: str | None = None,
                      mood: str | None = None,
                      energy: int = 2,
                      activity: str = "work",
                      bpm_lo: int = 80,
                      bpm_hi: int = 110,
                      limit: int = 15,
                      tracks: list[dict] | None = None,
                      shuffle: bool = False) -> dict:
    """
    生成播放列表
    """
    from mood_detector import bpm_range as _bpm, mood_description

    # Use preset if given
    if preset and preset in PRESETS:
        p = PRESETS[preset]
        mood     = mood or p["mood"]
        energy   = p["energy"]
        activity = p["activity"]
        limit    = p.get("length", limit)
        label    = p["label"]
        desc     = p["desc"]
        bpm_lo, bpm_hi = _bpm(mood, energy)
    else:
        label = f"🎵 情境歌單"
        desc = f"根據「{mood_description(mood or 'focused')}」生成"

    # Score + sort
    if not tracks:
        tracks = fetch_library(limit=300)

    if not tracks:
        return {"name": label, "desc": desc, "preset": preset or "custom",
                "mood": mood, "energy": energy, "activity": activity,
                "bpm_range": [bpm_lo, bpm_hi], "created": datetime.now().isoformat(),
                "tracks": [], "stats": {"count": 0, "total_duration_min": 0},
                "warning": "Music library empty"}

    scored = score_tracks(tracks, mood or "focused", energy, activity, (bpm_lo, bpm_hi))
    selected = scored[:limit]

    if shuffle:
        random.shuffle(selected)

    # Stats
    total_dur = sum(t.get("duration", 0) for t in selected)
    avg_bpm = sum(t.get("bpm", 0) for t in selected if t.get("bpm")) / max(1, sum(1 for t in selected if t.get("bpm")))

    playlist = {
        "name": label,
        "desc": desc,
        "preset": preset or "custom",
        "mood": mood,
        "energy": energy,
        "activity": activity,
        "bpm_range": [bpm_lo, bpm_hi],
        "created": datetime.now().isoformat(),
        "tracks": selected,
        "stats": {
            "count": len(selected),
            "total_duration_min": round(total_dur / 60, 1),
            "avg_bpm": round(avg_bpm, 0) if avg_bpm else None,
        }
    }

    return playlist


# ── Renderer ─────────────────────────────────────────────────────────────────

def render_playlist(playlist: dict, show_scores: bool = False) -> str:
    lines = []
    name  = playlist.get("name", "播放列表")
    desc  = playlist.get("desc", "")
    stats = playlist.get("stats", {})

    lines.append("")
    lines.append("╔" + "═" * 52 + "╗")
    lines.append("║" + f" {name}".ljust(52) + "║")
    lines.append("╚" + "═" * 52 + "╝")
    if desc:
        lines.append(f"  {desc}")
    lines.append("")
    bpm_str = f" ｜ 🎵 均 BPM {stats.get('avg_bpm',0):.0f}" if stats.get('avg_bpm') else ""
    lines.append(f"  📊 共 {stats.get('count',0)} 首 ｜ ⏱️ {stats.get('total_duration_min',0)} 分鐘{bpm_str}")
    lines.append(f"  🎯 Mood：{playlist.get('mood','?')} ｜ Energy {playlist.get('energy','?')}/5")
    lines.append("")

    for i, track in enumerate(playlist.get("tracks", []), 1):
        title   = track.get("name", "?")
        artist  = track.get("artist", "?")
        album   = track.get("album", "")
        dur     = _duration_str(track.get("duration", 0))
        bpm     = f"🎵{track['bpm']:.0f}" if track.get("bpm") else ""
        rating  = "⭐" * (track.get("rating", 0) // 20)

        line = f"  {i:>2}. 🎶 {title}"
        if artist != "?": line += f" — {artist}"
        if album:  line += f"  [{album}]"
        lines.append(line)

        sub = f"      {dur}"
        if bpm:   sub += f"  {bpm}"
        if rating: sub += f"  {rating}"
        if show_scores:
            sub += f"  (score:{track.get('score',0):.2f})"
        lines.append(sub)

    lines.append("")
    lines.append("─" * 56)
    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🎧 智慧播放列表 DJ")
    parser.add_argument("preset", nargs="?", default="work",
                        choices=list(PRESETS.keys()) + ["custom", "list"],
                        help="情境 preset")
    parser.add_argument("-n", "--limit",    type=int, default=12)
    parser.add_argument("-m", "--mood",     default=None)
    parser.add_argument("-e", "--energy",    type=int, choices=[1,2,3,4,5], default=2)
    parser.add_argument("-a", "--activity",  default="work")
    parser.add_argument("-b", "--bpm-range", default=None,
                        help="BPM 範圍如 80-120")
    parser.add_argument("-o", "--output",    type=Path)
    parser.add_argument("-s", "--shuffle",  action="store_true")
    parser.add_argument("-r", "--refresh",  action="store_true")
    parser.add_argument("--show-scores",    action="store_true")
    parser.add_argument("-j", "--json",     action="store_true",
                        help="JSON 輸出")

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["--help"])

    if args.preset == "list":
        print("\n🎛️  可用情境 preset：\n")
        for k, v in PRESETS.items():
            print(f"  {k:<12} {v['label']}")
            print(f"             {v['desc']}")
        return

    # BPM range
    bpm_lo, bpm_hi = 80, 110
    if args.bpm_range:
        parts = args.bpm_range.split("-")
        bpm_lo = int(parts[0])
        bpm_hi = int(parts[1]) if len(parts) > 1 else bpm_lo

    # Load library
    tracks = fetch_library(limit=300, refresh=args.refresh)

    # Generate
    playlist = generate_playlist(
        preset    = None if args.mood else args.preset,
        mood      = args.mood,
        energy    = args.energy,
        activity  = args.activity,
        bpm_lo    = bpm_lo,
        bpm_hi    = bpm_hi,
        limit     = args.limit,
        tracks    = tracks,
        shuffle   = args.shuffle,
    )

    if args.json:
        print(json.dumps(playlist, ensure_ascii=False, indent=2))
    else:
        print(render_playlist(playlist, show_scores=args.show_scores))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(playlist, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 已儲存：{args.output}")


if __name__ == "__main__":
    main()
