"""RPG Travel — 数据模型、配置、工具函数"""

import json
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
TEMPLATE_FILE = PROJECT_DIR / "references" / "pixel-map-template.md"
DEFAULT_STYLE = "game-ui"
OUTPUT_DIR = Path.cwd()

STYLES = {
    "travel-journal": {
        "name": "旅行手账风",
        "vars": {
            "--bg": "#f5f0e8",
            "--canvas": "#faf6ee",
            "--border": "#8b7355",
            "--text": "#3d2b1f",
            "--text-dim": "#a08060",
            "--accent": "#c41e3a",
            "--green": "#2d8a4e",
            "--gold": "#d4a017",
            "--pixel-font": "'Noto Serif SC','Songti SC','SimSun',Georgia,serif",
        },
    },
    "parchment": {
        "name": "复古羊皮纸",
        "vars": {
            "--bg": "#2a1f14",
            "--canvas": "#3a2a1a",
            "--border": "#8b4513",
            "--text": "#d4c5a9",
            "--text-dim": "#a09070",
            "--accent": "#c41e3a",
            "--green": "#228b22",
            "--gold": "#daa520",
            "--pixel-font": "'Noto Serif SC','Songti SC',Georgia,serif",
        },
    },
    "minimal-card": {
        "name": "现代极简卡片",
        "vars": {
            "--bg": "#f8f9fa",
            "--canvas": "#ffffff",
            "--border": "#e9ecef",
            "--text": "#212529",
            "--text-dim": "#868e96",
            "--accent": "#4263eb",
            "--green": "#20c997",
            "--gold": "#fcc419",
            "--pixel-font": "-apple-system,'PingFang SC','Microsoft YaHei',sans-serif",
        },
    },
    "game-ui": {
        "name": "游戏内UI风",
        "vars": {
            "--bg": "#0d1117",
            "--canvas": "rgba(22,27,34,0.95)",
            "--border": "#30363d",
            "--text": "#c9d1d9",
            "--text-dim": "#8b949e",
            "--accent": "#58a6ff",
            "--green": "#3fb950",
            "--gold": "#d29922",
            "--pixel-font": "'SF Mono',Monaco,Consolas,monospace",
        },
    },
    "pixel-retro": {
        "name": "像素复古",
        "vars": {
            "--bg": "#1a1a2e",
            "--canvas": "#16213e",
            "--border": "#0f3460",
            "--text": "#e0e0e0",
            "--text-dim": "#888",
            "--accent": "#e94560",
            "--green": "#4ecca3",
            "--gold": "#f0c040",
            "--pixel-font": "'SF Mono',Monaco,Consolas,'Courier New',monospace",
        },
    },
    "neon-city": {
        "name": "都市霓虹",
        "vars": {
            "--bg": "#0a0a1a",
            "--canvas": "#1a0a2e",
            "--border": "#2a1a4e",
            "--text": "#e0e0e0",
            "--text-dim": "#888",
            "--accent": "#ff2d55",
            "--green": "#00ff88",
            "--gold": "#ffd700",
            "--pixel-font": "'SF Mono',Monaco,Consolas,monospace",
        },
    },
    "japanese": {
        "name": "和风武士",
        "vars": {
            "--bg": "#1a1a2e",
            "--canvas": "#2a1a1e",
            "--border": "#3a2a2e",
            "--text": "#e0e0e0",
            "--text-dim": "#888",
            "--accent": "#ff6b6b",
            "--green": "#4ecdc4",
            "--gold": "#d4a574",
            "--pixel-font": "'Noto Serif SC','Hiragino Sans',sans-serif",
        },
    },
    "chinese": {
        "name": "中国古风",
        "vars": {
            "--bg": "#1a0a0a",
            "--canvas": "#2a1a1a",
            "--border": "#3a2a1a",
            "--text": "#e0d5c5",
            "--text-dim": "#a09080",
            "--accent": "#c41e3a",
            "--green": "#2d8a4e",
            "--gold": "#d4a017",
            "--pixel-font": "'Noto Serif SC','Songti SC','SimSun',serif",
        },
    },
    "scifi": {
        "name": "科幻未来",
        "vars": {
            "--bg": "#0a0a1a",
            "--canvas": "#0a1a2a",
            "--border": "#1a2a3a",
            "--text": "#e0e0e0",
            "--text-dim": "#888",
            "--accent": "#00d4ff",
            "--green": "#00ff88",
            "--gold": "#ffffff",
            "--pixel-font": "'SF Mono',Monaco,Consolas,monospace",
        },
    },
}

GAME_TYPE_STYLE_MAP = {
    "western": "parchment",
    "japanese": "japanese",
    "chinese": "chinese",
    "cyberpunk": "neon-city",
    "scifi": "scifi",
    "pixel": "pixel-retro",
    "modern": "minimal-card",
    "default": "game-ui",
}

CELL_TYPES = {
    "start": {"type": "cell--start", "icon": "🏠", "badge": None},
    "transport": {"type": "cell--side", "icon": "🌀", "badge": None},
    "dungeon": {"type": "cell--main", "icon": "🏰", "badge": "主线"},
    "boss": {"type": "cell--main", "icon": "⚔️", "badge": "Boss"},
    "side": {"type": "cell--side", "icon": "📍", "badge": "支线"},
    "save": {"type": "cell--save", "icon": "💾", "badge": None},
    "food": {"type": "cell--side", "icon": "🍜", "badge": None},
    "shop": {"type": "cell--side", "icon": "🛒", "badge": None},
}


def _parse_budget_limit(budget_str: str) -> float | None:
    if not budget_str:
        return None
    if "5000以内" in budget_str:
        return 5000.0
    match = re.search(r"(\d+)-(\d+)", budget_str)
    if match:
        return float(match.group(2))
    return None


class TripData:
    """行程数据容器 — AI 收集的数据最终填入这个结构"""

    def __init__(self, data: dict):
        self.game_name = data.get("game_name", "")
        self.style = data.get("style", DEFAULT_STYLE)
        self.departure_city = data.get("departure_city", "")
        self.destination_city = data.get("destination_city", "")
        self.player_level = data.get("player_level", "新手")
        self.budget = data.get("budget", "")
        self.date_range = data.get("date_range", "")
        self.days = data.get("days", 2)
        self.people_count = data.get("people_count", 1)
        self.game_type = data.get("game_type", "default")

        self.flights = data.get("flights", [])
        self.hotels = data.get("hotels", [])
        self.pois = data.get("pois", [])
        self.foods = data.get("foods", [])
        self.itinerary = data.get("itinerary", [])

    def validate(self) -> list[str]:
        errors = []
        if not self.game_name:
            errors.append("缺少 game_name")
        if not self.departure_city:
            errors.append("缺少 departure_city")
        if not self.destination_city:
            errors.append("缺少 destination_city")
        if not self.flights:
            errors.append("缺少 flights（至少需要一个航班）")
        if not self.hotels:
            errors.append("缺少 hotels（至少需要一个酒店）")
        if not self.pois:
            errors.append("缺少 pois（至少需要一个景点）")
        if not self.itinerary:
            errors.append("缺少 itinerary（至少需要一天行程）")
        for i, f in enumerate(self.flights):
            if not f.get("flight_no"):
                errors.append(f"flights[{i}] 缺少 flight_no")
            if not f.get("dep_time"):
                errors.append(f"flights[{i}] 缺少 dep_time")
            if not f.get("arr_time"):
                errors.append(f"flights[{i}] 缺少 arr_time")
            if not f.get("dep_city_name"):
                errors.append(f"flights[{i}] 缺少 dep_city_name")
            if not f.get("arr_city_name"):
                errors.append(f"flights[{i}] 缺少 arr_city_name")
            jump = (
                f.get("jumpUrl")
                or f.get("jump_url")
                or f.get("detailUrl")
                or f.get("itemId")
            )
            if not jump:
                errors.append(f"flights[{i}] 缺少 jumpUrl/detailUrl/itemId（飞猪链接）")
        for i, h in enumerate(self.hotels):
            if not h.get("hotel_name") and not h.get("name"):
                errors.append(f"hotels[{i}] 缺少 hotel_name")
            if not h.get("address"):
                errors.append(f"hotels[{i}] 缺少 address")
            if not h.get("price"):
                errors.append(f"hotels[{i}] 缺少 price")
            detail = h.get("detailUrl") or h.get("jumpUrl") or h.get("itemId")
            if not detail:
                errors.append(f"hotels[{i}] 缺少 detailUrl/jumpUrl/itemId（飞猪链接）")
            h["picUrl"] = h.get("mainPic") or h.get("picUrl") or h.get("pic_url") or ""
        for i, p in enumerate(self.pois):
            if not p.get("poi_name") and not p.get("name"):
                errors.append(f"pois[{i}] 缺少 poi_name")
            if not p.get("address"):
                errors.append(f"pois[{i}] 缺少 address")
            if not p.get("game_desc"):
                errors.append(f"pois[{i}] 缺少 game_desc（游戏中的场景描述）")
            if not p.get("reality_desc"):
                errors.append(f"pois[{i}] 缺少 reality_desc（现实中的样子）")
            if not p.get("story_connection"):
                errors.append(f"pois[{i}] 缺少 story_connection（剧情关联）")
            p["picUrl"] = p.get("picUrl") or p.get("pic_url") or ""
        for i, f in enumerate(self.foods):
            if not f.get("name"):
                errors.append(f"foods[{i}] 缺少 name")
            if not f.get("price"):
                errors.append(f"foods[{i}] 缺少 price")
            f["picUrl"] = f.get("picUrl") or f.get("pic_url") or ""
        for i, day in enumerate(self.itinerary):
            if not day.get("date"):
                errors.append(f"itinerary[{i}] 缺少 date")
            if not day.get("events"):
                errors.append(f"itinerary[{i}] 缺少 events")
            for j, ev in enumerate(day.get("events", [])):
                if not ev.get("type"):
                    errors.append(f"itinerary[{i}].events[{j}] 缺少 type")
                if not ev.get("name"):
                    errors.append(f"itinerary[{i}].events[{j}] 缺少 name")
                if not ev.get("time") and ev.get("type") != "food":
                    errors.append(f"itinerary[{i}].events[{j}] 缺少 time")
                if ev.get("type") == "transport" and not ev.get("link"):
                    is_first = i == 0 and j == 0
                    is_last = (
                        i == len(self.itinerary) - 1
                        and j == len(day.get("events", [])) - 1
                    )
                    if is_first or is_last:
                        errors.append(
                            f"itinerary[{i}].events[{j}] transport 缺少 link（飞猪链接）"
                        )
                if ev.get("type") == "hotel" and not ev.get("link"):
                    errors.append(
                        f"itinerary[{i}].events[{j}] hotel 缺少 link（飞猪链接）"
                    )
                if ev.get("type") == "poi" and not ev.get("game_desc"):
                    errors.append(f"itinerary[{i}].events[{j}] poi 缺少 game_desc")
                if ev.get("type") == "poi" and not ev.get("story_connection"):
                    errors.append(
                        f"itinerary[{i}].events[{j}] poi 缺少 story_connection"
                    )
        return errors


def build_fliggy_link(item_type: str, item: dict) -> str:
    item_id = item.get("itemId") or item.get("item_id")
    if item_id:
        return f"https://market.fliggy.com/item.htm?itemId={item_id}"

    jump_url = (
        item.get("jumpUrl")
        or item.get("jump_url")
        or item.get("detailUrl")
        or item.get("detail_url")
    )
    if jump_url:
        return jump_url

    if item_type == "flight":
        return (
            f"https://www.fliggy.com/flight/list.htm"
            f"?depCityName={item.get('dep_city_name', '')}"
            f"&arrCityName={item.get('arr_city_name', '')}"
            f"&depDate={item.get('dep_date', '')}"
        )
    elif item_type == "hotel":
        return (
            f"https://www.fliggy.com/hotel/list.htm"
            f"?cityName={item.get('city_name', '')}"
            f"&keyword={item.get('hotel_name', '')}"
        )
    elif item_type == "poi":
        return (
            f"https://www.fliggy.com/ticket/list.htm?keyword={item.get('poi_name', '')}"
        )
    elif item_type == "food":
        return (
            f"https://www.fliggy.com/search/list.htm"
            f"?keyword={item.get('query', item.get('name', ''))}"
        )
    return "#"
