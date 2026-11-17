#!/usr/bin/env python3
"""
music_player.py — Music.app 播放控制
支援：播放/暫停/上一首/下一首/隨機/播放指定曲目
"""

import sys
import subprocess
import re
import argparse
from pathlib import Path
from datetime import datetime

DATA_DIR = Path.home() / ".smart-playlist-dj"
DATA_DIR.mkdir(parents=True, exist_ok=True)
QUEUE_FILE = DATA_DIR / "current_queue.json"


# ── osascript helper ────────────────────────────────────────────────────────

def _run(script: str, timeout: int = 10) -> str:
    try:
        r = subprocess.run(["osascript", "-e", script],
                          capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception as e:
        return f"ERROR:{e}"


def _tstr(track: dict) -> str:
    n  = track.get("name", "?")
    a  = track.get("artist", "?")
    al = track.get("album", "")
    dur = track.get("duration", 0)
    m = int(dur // 60)
    s = int(dur % 60)
    return f"🎵 {n} — {a}" + (f" [{al}]" if al else "") + f" ({m}:{s:02d})"


# ── Player state ─────────────────────────────────────────────────────────────

STATE_SCRIPT = """
tell application "Music"
    set s to player state as string
    set t to current track
    set n to name of t
    set a to artist of t
    set p to album of t
    set d to duration of t
    set pos to player position as string
    set vol to sound volume as string
    return s & "||" & n & "||" & a & "||" & p & "||" & d & "||" & pos & "||" & vol
end tell
"""

def get_state() -> dict:
    out = _run(STATE_SCRIPT)
    if out.startswith("ERROR:") or "||" not in out:
        return {"state": "stopped", "name": "", "artist": "", "album": "",
                "duration": 0, "position": 0, "volume": 50}

    parts = out.split("||")
    state, name, artist, album, dur, pos, vol = (parts + ["", "", "", "", "0", "0", "50"])[:7]
    try:
        duration = float(dur)
        position = float(pos)
    except ValueError:
        duration = 0.0
        position = 0.0

    return {
        "state": state, "name": name, "artist": artist,
        "album": album, "duration": duration,
        "position": position, "volume": int(vol),
    }


# ── Playback controls ────────────────────────────────────────────────────────

def play():
    """播放 / 繼續播放"""
    _run('tell application "Music" to play')
    return "▶️  播放中"

def pause():
    _run('tell application "Music" to pause')
    return "⏸️  已暫停"

def toggle():
    s = get_state()
    if s["state"] == "playing":
        return pause()
    return play()

def next_track():
    _run('tell application "Music" to next track')
    s = get_state()
    return f"⏭️  下一首：{s['name']} — {s['artist']}"

def prev_track():
    _run('tell application "Music" to previous track')
    s = get_state()
    return f"⏮️  上一首：{s['name']} — {s['artist']}"

def stop():
    _run('tell application "Music" to stop')
    return "⏹️  已停止"

def set_volume(level: int):
    level = max(0, min(100, level))
    _run(f'tell application "Music" to set sound volume to {level}')
    return f"🔊 音量：{level}%"

def shuffle_on():
    _run('tell application "Music" to set shuffle enabled to true')
    return "🔀 隨機播放：開"

def shuffle_off():
    _run('tell application "Music" to set shuffle enabled to false')
    return "🔀 隨機播放：關"

def repeat_all():
    _run('tell application "Music" to set song repeat to all')
    return "🔁 循環：全部"

def repeat_off():
    _run('tell application "Music" to set song repeat to off')
    return "🔁 循環：關"

def seek(seconds: float):
    _run(f'tell application "Music" to set player position to {seconds}')
    return f"⏱️  跳到 {int(seconds)} 秒"


# ── Queue management ─────────────────────────────────────────────────────────

QUEUE_SCRIPT = """
tell application "Music"
    set qt to queue
    set result to ""
    repeat with tr in qt
        set n to name of tr
        set a to artist of tr
        if result is "" then
            set result to n & " - " & a
        else
            set result to result & "\\n" & n & " - " & a
        end if
    end repeat
    return result
end tell
"""

def get_queue() -> list[str]:
    out = _run(QUEUE_SCRIPT)
    if out.startswith("ERROR:") or not out.strip():
        return []
    return [l.strip() for l in out.split("\n") if l.strip()]


def now_playing() -> str:
    s = get_state()
    if s["state"] == "stopped":
        return "⏹️  目前沒有播放"

    # Progress bar
    dur  = s["duration"]
    pos  = s["position"]
    bar_len = 24
    if dur > 0:
        filled = int(bar_len * pos / dur)
        bar = "█" * filled + "░" * (bar_len - filled)
    else:
        bar = "░" * bar_len

    m_pos = int(pos // 60)
    s_pos = int(pos % 60)
    m_dur = int(dur // 60)
    s_dur = int(dur % 60)

    lines = [
        "",
        f"  🎧 現在播放中",
        "",
        f"  🎵 {s['name']}",
        f"  👤 {s['artist']}",
        f"  💿 {s['album']}",
        "",
        f"  [{bar}]",
        f"  {m_pos:02d}:{s_pos:02d} / {m_dur:02d}:{s_dur:02d}",
        f"  🔊 音量：{s['volume']}%",
        "",
        "  🎛️  操作：play / pause / next / prev / stop / vol [0-100]",
        "",
    ]
    return "\n".join(lines)


# ── Play from library by search ───────────────────────────────────────────────

def play_search(query: str) -> str:
    """在 Music.app 中搜尋並播放"""
    script = f'''
tell application "Music"
    set searchResults to search library playlist 1 for "{query}"
    if (count of searchResults) > 0 then
        play track 1 of searchResults
        return "▶️  播放：「{query}」"
    else
        return "❌ 找不到：「{query}」"
    end if
end tell
'''
    return _run(script)


# ── Main CLI ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🎧 Music.app 播放控制")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("play",    help="播放")
    p = sub.add_parser("pause",   help="暫停")
    p = sub.add_parser("toggle",  help="切換播放/暫停")
    p = sub.add_parser("next",    help="下一首")
    p = sub.add_parser("prev",    help="上一首")
    p = sub.add_parser("stop",    help="停止")
    p = sub.add_parser("now",     help="現在播放")
    p = sub.add_parser("queue",   help="待播清單")
    p = sub.add_parser("shuffle-on",  help="隨機開")
    p = sub.add_parser("shuffle-off", help="隨機關")
    p = sub.add_parser("repeat-all",  help="循環全部")
    p = sub.add_parser("repeat-off",  help="循環關")
    p = sub.add_parser("queue-clear", help="清除待播")

    p = sub.add_parser("play-search", help="搜尋播放")
    p.add_argument("query", help="搜尋關鍵字")

    p = sub.add_parser("vol",    help="設定音量")
    p.add_argument("level", type=int, choices=range(0, 101))

    p = sub.add_parser("seek",   help="跳到秒數")
    p.add_argument("seconds", type=float)

    args = parser.parse_args(sys.argv[1:] if len(sys.argv) > 1 else ["now"])

    def log(msg=""): print(msg)

    cmd = args.cmd

    if cmd == "play":          log(play())
    elif cmd == "pause":       log(pause())
    elif cmd == "toggle":      log(toggle())
    elif cmd == "next":        log(next_track())
    elif cmd == "prev":        log(prev_track())
    elif cmd == "stop":        log(stop())
    elif cmd == "now":         log(now_playing())
    elif cmd == "queue":
        q = get_queue()
        if not q: log("📭 待播清單是空的")
        else:
            log("\n🎶 待播清單：\n")
            for i, t in enumerate(q, 1): log(f"  {i}. {t}")
    elif cmd == "shuffle-on":  log(shuffle_on())
    elif cmd == "shuffle-off": log(shuffle_off())
    elif cmd == "repeat-all":  log(repeat_all())
    elif cmd == "repeat-off":  log(repeat_off())
    elif cmd == "play-search": log(play_search(args.query))
    elif cmd == "vol":         log(set_volume(args.level))
    elif cmd == "seek":        log(seek(args.seconds))
    elif cmd == "queue-clear":
        _run('tell application "Music" to clear queue')
        log("🗑️  待播清單已清除")


if __name__ == "__main__":
    main()
