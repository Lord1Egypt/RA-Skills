"""RPG Travel — HTML 生成（模板、样式、grid、locations、budget、图片）"""

import json
import re
from pathlib import Path

from models import (
    TripData,
    STYLES,
    DEFAULT_STYLE,
    GAME_TYPE_STYLE_MAP,
    CELL_TYPES,
    build_fliggy_link,
    TEMPLATE_FILE,
)


def extract_html_template(template_path: Path) -> str:
    content = template_path.read_text(encoding="utf-8")
    match = re.search(r"```html\n(.*?)\n```", content, re.DOTALL)
    if not match:
        raise ValueError("无法从模板文件中提取 HTML，检查 pixel-map-template.md 格式")
    return match.group(1)


def apply_style(html: str, style_key: str) -> str:
    if style_key not in STYLES:
        style_key = DEFAULT_STYLE

    style = STYLES[style_key]
    vars_css = "\n".join(f"      {k}: {v};" for k, v in style["vars"].items())

    root_pattern = re.compile(r"(:root\s*\{)(.*?)(\})", re.DOTALL)
    html = root_pattern.sub(lambda m: f":root {{\n{vars_css}\n    }}", html, count=1)
    return html


def generate_grid_cells(data: TripData) -> tuple[str, str]:
    cells = []

    cells.append(f"""      <div class="map-cell cell--start" onclick="showDetail('start')" data-key="start">
        <div class="cell-icon">🏠</div>
        <div class="cell-name">{data.departure_city}<br/>起点</div>
      </div>""")

    if data.flights:
        flight = data.flights[0]
        flight_no = flight.get("flight_no", flight.get("airline_name", "航班"))
        cells.append(f"""      <div class="map-cell cell--side" onclick="showDetail('transport')" data-key="transport">
        <div class="cell-icon">🌀</div>
        <div class="cell-name">传送门<br/>{flight_no}</div>
      </div>""")

    dungeon_count = 0
    for poi in data.pois[:4]:
        dungeon_count += 1
        cell_type = "boss" if dungeon_count == 2 else "dungeon"
        cell_info = CELL_TYPES[cell_type]
        poi_name = poi.get("poi_name", poi.get("name", f"取景地{dungeon_count}"))
        cells.append(f"""      <div class="map-cell {cell_info["type"]}" onclick="showDetail('dungeon{dungeon_count}')" data-key="dungeon{dungeon_count}">
        <div class="cell-icon">{cell_info["icon"]}</div>
        <div class="cell-name">{poi_name}<br/>{"Boss 战" if cell_type == "boss" else "主线副本"}</div>
        <div class="cell-badge cell-badge--main">{cell_info["badge"]}</div>
      </div>""")

    if data.hotels:
        hotel = data.hotels[0]
        hotel_name = hotel.get("hotel_name", hotel.get("name", "酒店"))
        cells.append(f"""      <div class="map-cell cell--save" onclick="showDetail('save')" data-key="save">
        <div class="cell-icon">💾</div>
        <div class="cell-name">{hotel_name}<br/>存档点</div>
      </div>""")

    side_count = 0
    for food in data.foods[:2]:
        side_count += 1
        food_name = food.get("name", food.get("query", f"美食{side_count}"))
        cells.append(f"""      <div class="map-cell cell--side" onclick="showDetail('food{side_count}')" data-key="food{side_count}">
        <div class="cell-icon">🍜</div>
        <div class="cell-name">{food_name}<br/>回血道具</div>
      </div>""")

    for poi in data.pois[4:6]:
        side_count += 1
        poi_name = poi.get("poi_name", poi.get("name", f"景点{side_count}"))
        cells.append(f"""      <div class="map-cell cell--side" onclick="showDetail('side{side_count}')" data-key="side{side_count}">
        <div class="cell-icon">📍</div>
        <div class="cell-name">{poi_name}<br/>支线任务</div>
        <div class="cell-badge cell-badge--side">支线</div>
      </div>""")

    total = len(cells)
    grid_cols = "repeat(4, 1fr)"

    return "\n".join(cells), grid_cols


def generate_locations_object(data: TripData) -> str:
    locs = {}

    locs["start"] = {
        "title": f"🏠 {data.departure_city} — 冒险起点",
        "game": "冒险者从这里出发，踏上未知的旅程",
        "reality": f"现实中的 {data.departure_city}，你的出发地",
        "story": f"每一个伟大的冒险都从这里开始。就像《{data.game_name}》中主角离开家乡的那一刻，你也将跨越熟悉的边界，进入游戏中的世界。",
        "info": "准备出发！带好装备和经费",
        "buyLink": "",
    }

    if data.flights:
        f = data.flights[0]
        locs["transport"] = {
            "title": f"🌀 传送门 — {f.get('flight_no', f.get('airline_name', '航班'))}",
            "game": "使用传送魔法，瞬间跨越千里",
            "reality": f"{f.get('flight_no', '')} {f.get('dep_time', '')}-{f.get('arr_time', '')} ¥{f.get('price', '')}/人",
            "story": f"就像游戏中的快速旅行系统，你即将从 {data.departure_city} 传送到 {data.destination_city}——游戏真正开始的地方。",
            "info": f"耗时 {f.get('duration', '')}，消耗 1 回合",
            "buyLink": build_fliggy_link("flight", f),
        }

    for i, poi in enumerate(data.pois[:4], 1):
        key = f"dungeon{i}"
        poi_name = poi.get("poi_name", poi.get("name", f"取景地{i}"))
        locs[key] = {
            "title": f"{'⚔️' if i == 2 else '🏰'} {poi_name} — {'Boss 战' if i == 2 else '主线副本'}",
            "game": poi.get("game_desc", f"游戏中在这里发生了重要剧情"),
            "reality": poi.get("reality_desc", poi.get("description", "现实中的景点")),
            "story": poi.get(
                "story_connection",
                f"在《{data.game_name}》中，这里是关键剧情的发生地。主角在此经历了挑战和成长，现在轮到你亲身感受。",
            ),
            "info": f"📍 {poi.get('address', '')} | 🎫 {poi.get('ticket_price', '免费')} | ⏰ {poi.get('open_time', '全天')}",
            "buyLink": build_fliggy_link("poi", poi),
        }

    if data.hotels:
        h = data.hotels[0]
        locs["save"] = {
            "title": f"💾 {h.get('hotel_name', h.get('name', '酒店'))} — 存档点",
            "game": "在这里保存进度，回复 HP/MP",
            "reality": f"{h.get('hotel_name', h.get('name', ''))} ¥{h.get('price', '')}/晚",
            "story": "就像游戏中的存档点/旅馆，这里是你在冒险途中的安全港。休息好了，明天继续探索。",
            "info": f"📍 {h.get('address', '')} | 📶 WiFi | ☕ {h.get('breakfast', '含早餐')}",
            "buyLink": build_fliggy_link("hotel", h),
        }

    for i, food in enumerate(data.foods[:2], 1):
        key = f"food{i}"
        locs[key] = {
            "title": f"🍜 {food.get('name', food.get('query', f'美食{i}'))} — 回血道具",
            "game": "食用后 HP+50, 精力+30%",
            "reality": f"{food.get('name', '')} 人均 ¥{food.get('price', '')}",
            "story": f"游戏中的回血道具在现实中就是当地美食！也许《{data.game_name}》的主角也吃过同样的味道。",
            "info": f"📍 {food.get('address', '')} | ⭐ {food.get('rating', '')} | 🕐 {food.get('hours', '')}",
            "buyLink": build_fliggy_link("food", food),
        }

    for i, poi in enumerate(data.pois[4:6], 1):
        key = f"side{i}"
        poi_name = poi.get("poi_name", poi.get("name", f"景点{i}"))
        locs[key] = {
            "title": f"📍 {poi_name} — 支线任务",
            "game": "探索中发现的神秘地点",
            "reality": poi.get("description", "现实中的样子"),
            "story": "主线之外的意外发现。就像游戏中的隐藏任务，有时候最美的风景在计划之外。",
            "info": f"📍 {poi.get('address', '')} | 🎫 {poi.get('ticket_price', '免费')}",
            "buyLink": build_fliggy_link("poi", poi),
        }

    return json.dumps(locs, ensure_ascii=False, indent=6)


def generate_buy_links_section(data: TripData) -> str:
    items = []

    if data.flights:
        f = data.flights[0]
        link = build_fliggy_link("flight", f)
        reason = f.get(
            "recommend_reason",
            f"{f.get('flight_no', '')} {f.get('dep_time', '')}出发，价格最优",
        )
        items.append(f"""      <div class="buy-item">
        <span class="buy-item-label">✈️ 去程航班</span>
        <a href="{link}" target="_blank" rel="noopener" class="buy-btn">飞猪购买</a>
        <button class="copy-btn" onclick="copyLink('{link}', this)">📋 复制</button>
        <span class="buy-reason">💡 {reason}</span>
      </div>""")

    if len(data.flights) > 1:
        f = data.flights[1]
        link = build_fliggy_link("flight", f)
        reason = f.get("recommend_reason", f"返程 {f.get('flight_no', '')}")
        items.append(f"""      <div class="buy-item">
        <span class="buy-item-label">✈️ 返程航班</span>
        <a href="{link}" target="_blank" rel="noopener" class="buy-btn">飞猪购买</a>
        <button class="copy-btn" onclick="copyLink('{link}', this)">📋 复制</button>
        <span class="buy-reason">💡 {reason}</span>
      </div>""")

    if data.hotels:
        h = data.hotels[0]
        link = build_fliggy_link("hotel", h)
        reason = h.get(
            "recommend_reason",
            f"{h.get('hotel_name', h.get('name', ''))} 评分{h.get('rating', '')}，位置便利",
        )
        items.append(f"""      <div class="buy-item">
        <span class="buy-item-label">🏨 酒店</span>
        <a href="{link}" target="_blank" rel="noopener" class="buy-btn">飞猪购买</a>
        <button class="copy-btn" onclick="copyLink('{link}', this)">📋 复制</button>
        <span class="buy-reason">💡 {reason}</span>
      </div>""")

    if data.pois:
        p = data.pois[0]
        link = build_fliggy_link("poi", p)
        reason = p.get(
            "recommend_reason", f"{p.get('poi_name', p.get('name', ''))} 必去取景地"
        )
        items.append(f"""      <div class="buy-item">
        <span class="buy-item-label">🎫 景点门票</span>
        <a href="{link}" target="_blank" rel="noopener" class="buy-btn">飞猪购买</a>
        <button class="copy-btn" onclick="copyLink('{link}', this)">📋 复制</button>
        <span class="buy-reason">💡 {reason}</span>
      </div>""")

    return "\n".join(items)


def _generate_budget_warning(data: TripData) -> str:
    from models import _parse_budget_limit

    budget_limit = _parse_budget_limit(data.budget)
    if not budget_limit:
        return ""
    flight_total = sum(float(f.get("price", 0)) for f in data.flights)
    hotel_total = sum(float(h.get("price", 0)) for h in data.hotels)
    total = flight_total * data.people_count + hotel_total * data.days
    if total <= budget_limit:
        return ""
    return f"""    <div class="budget-warning">
      ⚠️ 预算提醒：当前行程 ¥{int(total)} 超出预算上限 ¥{int(budget_limit)}<br/>
      建议：提前订票/改飞邻近城市/选择经济型住宿
    </div>"""


def _generate_lore_text(data: TripData) -> str:

    lore_templates = {
        "western": (
            f"《{data.game_name}》的故事发生在一片充满魔法与巨龙的大陆上。"
            f"这次旅行将带你走进猎魔人的世界，站在同一片土地上，感受那个'猎魔人'的残酷与浪漫。"
        ),
        "japanese": (
            f"《{data.game_name}》以日本战国时代为背景，融合了妖怪、武士与历史人物。"
            f"这次旅行将带你走进游戏中的世界，站在同一片土地上，感受那个'武士之魂'的时代。"
            f"樱花季/红叶季的日本，正是游戏中最美的模样。"
        ),
        "chinese": (
            f"《{data.game_name}》以中国神话与历史为背景，展现了壮丽的东方奇幻世界。"
            f"这次旅行将带你走进游戏中的场景，亲身感受那些只存在于传说中的山水。"
        ),
        "cyberpunk": (
            f"《{data.game_name}》描绘了一个霓虹闪烁的反乌托邦未来都市。"
            f"这次旅行将带你走进赛博朋克的世界，在钢铁森林中寻找人性的温度。"
        ),
    }
    return lore_templates.get(
        data.game_type,
        f"《{data.game_name}》的世界即将在现实中展开。"
        f"这次旅行将带你走进游戏中的场景，亲身感受虚拟与现实的交汇。",
    )


def _generate_tips(data: TripData) -> str:
    tips = [
        {"icon": "🎫", "label": "签证", "value": f"提前办理日本旅游签证（如需）"},
        {"icon": "💴", "label": "货币", "value": "日元，建议带信用卡+少量现金"},
        {"icon": "🚃", "label": "交通", "value": "JR Pass / ICOCA卡，京都巴士一日券"},
        {"icon": "📱", "label": "网络", "value": "提前购买日本流量卡或租赁WiFi"},
        {"icon": "🎮", "label": "装备", "value": f"重温《{data.game_name}》关键章节"},
        {"icon": "📸", "label": "拍照", "value": "带上相机，记录游戏与现实的对比"},
    ]
    items = []
    for t in tips:
        items.append(
            f'        <div class="tip-item">\n'
            f'          <div class="tip-icon">{t["icon"]}</div>\n'
            f"          <div>\n"
            f'            <div class="tip-label">{t["label"]}</div>\n'
            f'            <div class="tip-value">{t["value"]}</div>\n'
            f"          </div>\n"
            f"        </div>"
        )
    return "\n".join(items)


def _get_bg_image(data: TripData) -> str:
    # Fetch game background image — read-only GET, no auth, no user data sent
    # Fallback chain: Steam → HDQWalls → PAKUTASO → Wikimedia
    app_ids = {
        "western": "292030",
        "japanese": "1325200",
        "chinese": "2358720",
        "cyberpunk": "1091500",
        "modern": "2288800",
    }
    app_id = app_ids.get(data.game_type, "")
    if app_id:
        try:
            import urllib.request

            url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                d = json.loads(resp.read().decode())
                screenshots = d.get(app_id, {}).get("data", {}).get("screenshots", [])
                if screenshots:
                    return screenshots[0].get("path_full", "")
        except Exception:
            pass

    # HDQWalls — public game wallpapers, HEAD request only
    hdqwalls = {
        "western": "https://images.hdqwalls.com/wallpapers/the-witcher-3-wild-hunt-4k-game-2023-8k.jpg",
        "chinese": "https://images.hdqwalls.com/wallpapers/black-myth-wukong-2024-game-5k.jpg",
        "cyberpunk": "https://images.hdqwalls.com/wallpapers/cyberpunk-2077-4k-game-2020-8k.jpg",
    }
    hdq_url = hdqwalls.get(data.game_type, "")
    if hdq_url:
        try:
            import urllib.request

            req = urllib.request.Request(
                hdq_url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD"
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    return hdq_url
        except Exception:
            pass

    # PAKUTASO — Japanese stock photos, HEAD request only
    pakutaso = {
        "japanese": "https://user0514.cdnw.net/shared/img/thumb/16redsugar723.jpg",
    }
    paku_url = pakutaso.get(data.game_type, "")
    if paku_url:
        try:
            import urllib.request

            req = urllib.request.Request(
                paku_url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD"
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    return paku_url
        except Exception:
            pass

    # Wikimedia Commons — public domain fallback images
    fallbacks = {
        "japanese": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Himeji_Castle_The_keep_towers.jpg/1920px-Himeji_Castle_The_keep_towers.jpg",
        "western": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Gda%C5%84sk_-_D%C5%82uga.jpg/1920px-Gda%C5%84sk_-_D%C5%82uga.jpg",
        "chinese": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Zhangjiajie_National_Forest_Park.jpg/1920px-Zhangjiajie_National_Forest_Park.jpg",
        "cyberpunk": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Tokyo_night.jpg/1920px-Tokyo_night.jpg",
    }
    return fallbacks.get(data.game_type, fallbacks["japanese"])


def _get_reality_image(data: TripData) -> str:
    images = {
        "western": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Gda%C5%84sk_-_D%C5%82uga.jpg/440px-Gda%C5%84sk_-_D%C5%82uga.jpg",
        "japanese": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Kiyomizu-dera_in_Kyoto.jpg/440px-Kiyomizu-dera_in_Kyoto.jpg",
        "chinese": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Zhangjiajie_National_Forest_Park.jpg/440px-Zhangjiajie_National_Forest_Park.jpg",
        "cyberpunk": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Tokyo_night.jpg/440px-Tokyo_night.jpg",
    }
    return images.get(
        data.game_type,
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Gda%C5%84sk_-_D%C5%82uga.jpg/440px-Gda%C5%84sk_-_D%C5%82uga.jpg",
    )


def generate_html(data: TripData) -> str:
    from node_builder import _generate_nodes, _get_checkpoint_keys

    html = extract_html_template(TEMPLATE_FILE)

    style_key = (
        data.style
        if data.style in STYLES
        else GAME_TYPE_STYLE_MAP.get(data.game_type, DEFAULT_STYLE)
    )
    html = apply_style(html, style_key)

    replacements = {
        "[游戏名]": data.game_name,
        "[日期]": data.date_range
        or __import__("datetime").datetime.now().strftime("%Y-%m-%d"),
        "[等级]": data.player_level,
        "[出发城市]": data.departure_city,
        "[取景地城市]": data.destination_city,
        "[预算]": data.budget or "待定",
        "[LORE_TEXT]": _generate_lore_text(data),
        "[TIPS_ITEMS]": _generate_tips(data),
        "[BG_IMAGE_URL]": _get_bg_image(data),
    }
    for old, new in replacements.items():
        html = html.replace(old, str(new))

    nodes_html = _generate_nodes(data)
    html = html.replace(
        "      <!-- NODES_START -->\n      <!-- NODES_END -->",
        nodes_html,
        1,
    )

    checkpoint_keys = _get_checkpoint_keys(data)
    html = html.replace(
        "[CHECKPOINT_KEYS]", ", ".join(f'"{k}"' for k in checkpoint_keys)
    )

    flight_total = sum(float(f.get("price", 0)) for f in data.flights)
    hotel_total = sum(float(h.get("price", 0)) for h in data.hotels)

    def _parse_price(val):
        try:
            return float(re.sub(r"[^\d.]", "", str(val)) or "0")
        except ValueError:
            return 0.0

    budget_replacements = {
        "[FLIGHT_TOTAL]": str(int(flight_total)),
        "[HOTEL_TOTAL]": str(int(hotel_total)),
        "[NIGHTS]": str(data.days - 1),
        "[POI_TOTAL]": str(
            int(sum(_parse_price(p.get("ticket_price", 0)) for p in data.pois))
        ),
        "[FOOD_TOTAL]": str(
            int(sum(_parse_price(f.get("price", 0)) for f in data.foods))
        ),
        "[TOTAL]": str(int(flight_total * data.people_count + hotel_total * data.days)),
    }
    for old, new in budget_replacements.items():
        html = html.replace(old, new)

    html = html.replace("<!-- BUDGET_WARNING -->", _generate_budget_warning(data))

    cells, grid_cols = generate_grid_cells(data)
    html = html.replace("<!-- GRID_CELLS -->", cells)
    html = html.replace(
        "var gridCols = 'repeat(4, 1fr)';", f"var gridCols = '{grid_cols}';"
    )
    html = html.replace("/* LOCATIONS_JS */", generate_locations_object(data))
    html = html.replace("<!-- BUY_LINKS -->", generate_buy_links_section(data))

    reality_img = _get_reality_image(data)
    html = html.replace("[GAME_IMAGE_URL]", reality_img)
    html = html.replace("[REALITY_IMAGE_URL]", reality_img)

    return html
