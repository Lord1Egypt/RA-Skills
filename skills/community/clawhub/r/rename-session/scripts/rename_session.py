#!/usr/bin/env python3
"""
rename_session.py - Rename (label) an OpenClaw session by editing sessions.json.

Open-source edition. Author: Evan Song <songhonglei1985@gmail.com>
Repository: https://github.com/Songhonglei/better-agent-skills
License: MIT
"""

import argparse
import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

MAX_RETRIES = 3


# ─────────────────────────── Paths / XDG ───────────────────────────

def get_history_file() -> Path:
    """Return history file path following XDG Base Directory spec.

    Priority: $XDG_DATA_HOME/rename-session/history.json > ~/.local/share/rename-session/history.json
    """
    xdg_data = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg_data) if xdg_data else Path.home() / ".local" / "share"
    return base / "rename-session" / "history.json"


def get_default_root() -> Path:
    """Default OpenClaw agents root: $RENAME_SESSION_ROOT > ~/.openclaw/agents/"""
    env_root = os.environ.get("RENAME_SESSION_ROOT")
    return Path(env_root) if env_root else Path.home() / ".openclaw" / "agents"


def detect_default_lang() -> str:
    """Detect language preference from POSIX locale env vars.

    Priority: LC_ALL > LC_MESSAGES > LANG. Returns 'zh' for any Chinese locale
    (zh_CN, zh_TW, zh_HK, ...), otherwise 'en'.
    """
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        val = os.environ.get(var, "")
        if val and val.lower() != "c":
            return "zh" if val.lower().startswith("zh") else "en"
    return "en"


def autodetect_agent(root: Path) -> str:
    """Auto-detect the unique agent directory under root.

    Returns the agent name if exactly one exists, else exits with a helpful error.
    """
    if not root.exists():
        sys.exit(f"ERROR: agents root does not exist: {root}\n"
                 f"  Hint: pass --root <path> or set $RENAME_SESSION_ROOT")
    agents = sorted([
        d.name for d in root.iterdir()
        if d.is_dir() and (d / "sessions" / "sessions.json").exists()
    ])
    if not agents:
        sys.exit(f"ERROR: no agent with sessions.json found under {root}")
    if len(agents) > 1:
        sys.exit(f"ERROR: multiple agents detected: {', '.join(agents)}\n"
                 f"  Please specify with --agent <name>")
    return agents[0]


def resolve_sessions_path(root: Path, agent: str) -> Path:
    return root / agent / "sessions" / "sessions.json"


# ─────────────────────────── Random label vocabularies ───────────────────────────

def _month_scene_zh() -> str:
    m = datetime.now().month
    pool = {
        1:  ["寒冬腊月", "瑞雪纷飞", "腊梅初绽", "岁末辞旧"],
        2:  ["早春二月", "春寒料峭", "梅花盛开", "新春伊始"],
        3:  ["早春三月", "春光明媚", "春风拂面", "桃花初绽", "春雨绵绵"],
        4:  ["春意盎然", "繁花似锦", "草长莺飞", "杏花微雨"],
        5:  ["五月天气", "绿意葱葱", "阳光明媚", "清风徐来"],
        6:  ["仲夏之初", "暖风熏人", "荷花初绽", "夏日晴好"],
        7:  ["骄阳似火", "盛夏光年", "蝉鸣阵阵", "晴空万里"],
        8:  ["流火八月", "夜凉如水", "星河灿烂", "清风送爽"],
        9:  ["金秋九月", "天高云淡", "硕果累累", "秋高气爽"],
        10: ["金风送爽", "层林尽染", "秋色正浓", "霜叶红遍"],
        11: ["深秋时节", "落叶归根", "北风渐起", "暮秋清寒"],
        12: ["隆冬将至", "岁末年初", "冬日暖阳", "银装素裹"],
    }
    return random.choice(pool.get(m, ["天朗气清", "风和日丽"]))


def _month_scene_en() -> str:
    m = datetime.now().month
    pool = {
        1:  ["Frosty January", "Snowy Days", "Winter Chill", "New Year Dawn"],
        2:  ["Early Spring", "Warming Days", "Plum Blossom", "February Mist"],
        3:  ["March Breeze", "Spring Bloom", "Cherry Buds", "Soft Sunshine"],
        4:  ["April Showers", "Blooming Flowers", "Lush Meadows", "Pastel Spring"],
        5:  ["May Sunshine", "Green Foliage", "Bright Morning", "Gentle Wind"],
        6:  ["Early Summer", "Warm Breeze", "Lotus Buds", "Sunny Days"],
        7:  ["Blazing July", "Peak Summer", "Cicada Song", "Clear Skies"],
        8:  ["August Heat", "Starlit Nights", "Cool Evenings", "Late Summer"],
        9:  ["Golden Autumn", "Clear Skies", "Harvest Time", "Crisp Air"],
        10: ["October Wind", "Falling Leaves", "Autumn Hues", "Red Maples"],
        11: ["Late Autumn", "Bare Branches", "Cold Winds", "Twilight Hour"],
        12: ["Winter Eve", "Year-End", "Warm Sunshine", "Snow-Covered"],
    }
    return random.choice(pool.get(m, ["Fair Weather", "Calm Days"]))


SCENE_EXTRA_ZH = [
    "天气晴朗", "多云转晴", "朝霞满天", "细雨霏霏",
    "云淡风轻", "微风徐徐", "日暖风和", "霞光万丈",
    "星光熠熠", "月明风清", "碧空如洗", "晨光熹微",
    "夕阳西下", "彩霞满天", "雨过天晴", "薄雾轻笼",
]
SCENE_EXTRA_EN = [
    "Sunny Skies", "Partly Cloudy", "Morning Glow", "Light Drizzle",
    "Light Breeze", "Warm Gentle Day", "Golden Hour", "Starry Night",
    "Moonlit Calm", "Crystal Sky", "Dawn Light", "Sunset View",
    "Vibrant Sky", "After the Rain", "Misty Morning",
]

MOOD_EMOJI = [
    "🌸", "✨", "💫", "🌟", "🎉", "🌈", "🦋",
    "🌺", "🍀", "⚡", "🔥", "🌙", "🌻", "🌼",
]

STATE_WORDS_ZH = [
    "活力四射", "元气满满", "大干一天", "欢呼雀跃",
    "斗志昂扬", "满血复活", "全力以赴", "心花怒放",
    "精神抖擞", "热情似火", "干劲十足", "意气风发",
    "踌躇满志", "全神贯注", "乘风破浪", "勇往直前",
    "运筹帷幄", "妙思泉涌", "思如泉涌", "灵感迸发",
]
STATE_WORDS_EN = [
    "Energized", "Full of Spirit", "On Fire", "Cheerful Mode",
    "Battle Ready", "Fully Recovered", "All In", "Bursting Joy",
    "Wide Awake", "Passionate", "Highly Motivated", "Ambitious",
    "Focused Mind", "Riding the Wave", "Moving Forward",
    "Strategic Mode", "Inspiration Flowing", "Creative Flow",
]

STATE_EMOJI = [
    "💻", "🎤", "💃", "🌺", "🚀", "💪", "🎯",
    "🏄", "🎸", "🌊", "🎨", "📚", "⚡", "🌟",
]


# ─────────────────────────── History (avoid repeat) ───────────────────────────

def load_history(history_file: Path) -> list:
    try:
        if history_file.exists():
            return json.loads(history_file.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []


def save_history(history_file: Path, history: list) -> None:
    try:
        history_file.parent.mkdir(parents=True, exist_ok=True)
        history_file.write_text(
            json.dumps(history[-10:], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


# ─────────────────────────── Random label generation ───────────────────────────

def generate_random_label(agent_name: str = "Ashley",
                          lang: str = "zh",
                          history_file: Path | None = None,
                          max_attempts: int = 20) -> str:
    if history_file is None:
        history_file = get_history_file()
    history = load_history(history_file)
    recent_two = set(history[-2:])

    if lang == "en":
        month_fn, scene_extra, state_words = _month_scene_en, SCENE_EXTRA_EN, STATE_WORDS_EN
        sep = " "
    else:
        month_fn, scene_extra, state_words = _month_scene_zh, SCENE_EXTRA_ZH, STATE_WORDS_ZH
        sep = ""

    label = ""
    for _ in range(max_attempts):
        scene = month_fn() if random.random() < 0.7 else random.choice(scene_extra)
        mood_emoji = random.choice(MOOD_EMOJI)
        state_word = random.choice(state_words)
        state_emoji = random.choice(STATE_EMOJI)
        label = f"{scene}{sep}{agent_name}{mood_emoji}{sep}{state_word}{state_emoji}"
        if label not in recent_two:
            return label
    return label


# ─────────────────────────── Core operations ───────────────────────────

def list_sessions(root: Path, agent: str) -> int:
    path = resolve_sessions_path(root, agent)
    if not path.exists():
        sys.exit(f"ERROR: sessions.json not found at {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data:
        print(f"(no sessions found under agent: {agent})")
        return 0
    print(f"# Sessions under agent '{agent}'  (total: {len(data)})")
    print(f"# {path}")
    print()
    print(f"{'SESSION KEY':<40}  LABEL")
    print("-" * 80)
    for key, sess in data.items():
        label = sess.get("label", "(no label)")
        print(f"{key:<40}  {label}")
    return 0


def verify_rename(path: Path, session_key: str, expected_label: str) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get(session_key, {}).get("label") == expected_label
    except Exception:
        return False


def rename_session(root: Path, agent: str, session_key: str,
                   new_label: str, history_file: Path) -> bool:
    path = resolve_sessions_path(root, agent)

    if not path.exists():
        print(f"ERROR: sessions.json not found at {path}", file=sys.stderr)
        return False

    data = json.loads(path.read_text(encoding="utf-8"))
    if session_key not in data:
        print(f"ERROR: session key '{session_key}' not found.", file=sys.stderr)
        print(f"Available keys: {list(data.keys())}", file=sys.stderr)
        return False

    old_label = data[session_key].get("label", "(none)")

    for attempt in range(1, MAX_RETRIES + 1):
        data = json.loads(path.read_text(encoding="utf-8"))
        data[session_key]["label"] = new_label
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        if verify_rename(path, session_key, new_label):
            print(f"OK: session '{session_key}' renamed: '{old_label}' -> '{new_label}'")
            print(f"    Path: {path}")
            print(f"    Attempts: {attempt}/{MAX_RETRIES}")
            history = load_history(history_file)
            history.append(new_label)
            save_history(history_file, history)
            return True
        else:
            print(f"WARN: attempt {attempt}: verification failed, retrying...",
                  file=sys.stderr)

    print(f"ERROR: failed to rename session after {MAX_RETRIES} attempts.", file=sys.stderr)
    print(f"  Possible reasons:", file=sys.stderr)
    print(f"  1. File permission issues (check write access to {path})", file=sys.stderr)
    print(f"  2. Disk is full or read-only", file=sys.stderr)
    print(f"  3. Another process is continuously modifying sessions.json", file=sys.stderr)
    print(f"  4. File system corruption or I/O error", file=sys.stderr)
    return False


# ─────────────────────────── CLI ───────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename a session label in OpenClaw-style sessions.json"
    )
    parser.add_argument("session_key", nargs="?",
                        help="Session key (e.g. agent:main:main). Omit when using --list.")
    parser.add_argument("new_label", nargs="?", default=None,
                        help="New label. Omit when using --random or --list.")
    parser.add_argument("--random", action="store_true",
                        help="Auto-generate a random label.")
    parser.add_argument("--list", action="store_true",
                        help="List all session keys under the agent and exit.")
    parser.add_argument("--lang", choices=["zh", "en"], default=None,
                        help="Language for --random vocabulary (default: auto-detect from $LC_ALL/$LC_MESSAGES/$LANG, fall back to en).")
    parser.add_argument("--agent-name", default="Ashley",
                        help="Agent display name used in random label (default: Ashley).")
    parser.add_argument("--agent", default=None,
                        help="Agent ID. Auto-detected from --root if unique; required when multiple.")
    parser.add_argument("--root", default=None,
                        help="Agents root directory (default: $RENAME_SESSION_ROOT or ~/.openclaw/agents).")
    args = parser.parse_args()

    root = Path(args.root) if args.root else get_default_root()
    agent = args.agent or autodetect_agent(root)

    if args.list:
        sys.exit(list_sessions(root, agent))

    if not args.session_key:
        parser.error("session_key is required (unless using --list)")

    history_file = get_history_file()

    if args.random:
        lang = args.lang or detect_default_lang()
        label = generate_random_label(
            agent_name=args.agent_name, lang=lang, history_file=history_file
        )
        print(f"Generated label: {label}")
    elif args.new_label:
        label = args.new_label
    else:
        parser.error("provide new_label or use --random")

    ok = rename_session(root, agent, args.session_key, label, history_file)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
