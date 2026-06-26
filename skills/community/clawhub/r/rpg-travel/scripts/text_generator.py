"""RPG Travel — 文本任务书生成"""

from models import TripData, _parse_budget_limit, build_fliggy_link


def generate_text_taskbook(data: TripData) -> str:
    lines = []
    sep = "━" * 33

    lines.append(sep)
    lines.append(f"🎮 游戏圣地巡礼：{data.game_name}")
    lines.append(
        f"   {data.departure_city}出发 · {data.date_range or '待定'} · {data.days}天 · 冒险者 Lv.{data.player_level}"
    )
    lines.append(sep)
    lines.append("")
    lines.append("📜 主线任务：游戏取景地朝圣")
    lines.append(sep)
    lines.append("")
    lines.append("🗺️ 世界地图概览：")
    lines.append(f"  {data.departure_city} ──(传送门:航班)──→ {data.destination_city}")

    for i, poi in enumerate(data.pois[:4], 1):
        poi_name = poi.get("poi_name", poi.get("name", f"取景地{i}"))
        difficulty = "⭐" * (i + 1)
        game_desc = poi.get("game_desc", "游戏中发生重要剧情的地点")
        reality_desc = poi.get("reality_desc", poi.get("description", "现实中的景点"))
        story = poi.get("story_connection", f"《{data.game_name}》中这里发生了关键剧情")
        lines.append(f"    ├── 🏰 主线副本{i}：{poi_name}（{difficulty}）")
        lines.append(f"    │   游戏中的样子：{game_desc}")
        lines.append(f"    │   现实中的样子：{reality_desc}")
        lines.append(f"    │   📖 剧情关联：{story}")

    lines.append("")

    if data.hotels:
        h = data.hotels[0]
        hotel_name = h.get("hotel_name", h.get("name", "酒店"))
        address = h.get("address", "")
        price = h.get("price", "")
        rating = h.get("rating", "")
        recommend = h.get("recommend_reason", "")
        lines.append(f"🏨 存档点：{hotel_name}")
        lines.append(f"   HP 回复：💤 8小时深度睡眠")
        lines.append(f"   MP 回复：☕ 免费早餐 + WiFi")
        lines.append(f"   位置：{address}")
        lines.append(f"   💰 {price}/晚 · ⭐ {rating}")
        lines.append(f"   💡 {recommend}")
        link = build_fliggy_link("hotel", h)
        lines.append(f"   🔗 预订：{link}")

    lines.append("")
    lines.append(sep)

    for i, day in enumerate(data.itinerary, 1):
        day_date = day.get("date", f"Day {i}")
        day_theme = day.get("theme", f"{'初入异世界' if i == 1 else '深入探索'}")
        lines.append("")
        lines.append(f"📅 Day {i} · {day_date} — {day_theme}")
        lines.append("━" * 33)

        for event in day.get("events", []):
            time_str = event.get("time", "")
            event_type = event.get("type", "")
            name = event.get("name", "")
            desc = event.get("desc", "")
            price = event.get("price", "")
            link = event.get("link", "")
            story = event.get("story", "")

            if event_type == "transport":
                lines.append(f"")
                lines.append(f"  {time_str}  🌀 使用传送门")
                lines.append(f"          {desc}")
                if price:
                    lines.append(f"          💰 价格：¥{price}/人")
                if link:
                    lines.append(f"          🔗 购买：{link}（一键复制）")
            elif event_type == "hotel":
                lines.append(f"")
                lines.append(f"  {time_str}  🏨 到达存档点")
                lines.append(f"          {name} · {event.get('address', '')}")
                if price:
                    lines.append(
                        f"          💰 ¥{price}/晚 · ⭐ {event.get('rating', '')}"
                    )
                lines.append(f"          💡 {event.get('recommend', '')}")
                if link:
                    lines.append(f"          🔗 预订：{link}（一键复制）")
            elif event_type == "poi":
                lines.append(f"")
                lines.append(f"  {time_str}  🏰 主线副本：{name}")
                lines.append(f"          预计耗时：{event.get('duration', '2小时')}")
                lines.append(f"          ┌────────────────────────────────────────┐")
                lines.append(f"          │ 🎮 游戏中：{event.get('game_desc', '')}")
                lines.append(f"          │ 🌍 现实中：{event.get('reality_desc', '')}")
                lines.append(
                    f"          │ 📖 剧情关联：{story or event.get('story_connection', '')}"
                )
                lines.append(f"          └────────────────────────────────────────┘")
                if link:
                    lines.append(f"          🔗 门票：{link}（一键复制）")
            elif event_type == "food":
                lines.append(f"")
                lines.append(f"  {time_str}  🍜 使用回血道具")
                lines.append(f"          {name} · 人均 ¥{price} 元")
                lines.append(f"          Buff：{event.get('buff', '精力+30%')}")
                lines.append(f"          💡 {event.get('recommend', '')}")

        lines.append("")
        lines.append(sep)

    lines.append("💰 冒险经费总览")
    lines.append(sep)

    flight_total = sum(float(f.get("price", 0)) for f in data.flights)
    hotel_total = sum(float(h.get("price", 0)) for h in data.hotels)
    lines.append(f"  传送门费用（交通）：¥{flight_total * data.people_count}")
    lines.append(f"  存档点费用（住宿）：¥{hotel_total * data.days}")
    lines.append(f"  ─────────────────────────")
    total = flight_total * data.people_count + hotel_total * data.days
    lines.append(
        f"  📊 合计：¥{total} · 人均 ¥{int(total // data.people_count) if data.people_count else int(total)}"
    )

    budget_limit = _parse_budget_limit(data.budget)
    if budget_limit and total > budget_limit:
        lines.append("")
        lines.append(
            f"  ⚠️ 预算提醒：当前行程 ¥{int(total)} 超出预算上限 ¥{int(budget_limit)}"
        )
        lines.append(f"  建议：提前订票/改飞邻近城市/选择经济型住宿")

    lines.append("")
    lines.append(sep)
    lines.append("")
    lines.append("📋 成就系统")
    lines.append(sep)
    lines.append("  □ 初入异世界 — 到达取景地城市")
    lines.append("  □ 圣地巡礼者 — 打卡所有主线副本")
    lines.append("  □ 支线达人 — 完成 3 个以上支线任务")
    lines.append("  □ 美食猎人 — 品尝当地特色料理")
    lines.append("  □ 朝圣完成 — 完成全部任务")
    lines.append("")
    lines.append("  💬 随时告诉我你的打卡进度，我来更新成就状态！")
    lines.append("  📸 旅行中拍了照片也可以发给我，我帮你记录到成就里～")

    return "\n".join(lines)
