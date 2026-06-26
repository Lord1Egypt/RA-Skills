"""RPG Travel — 节点卡片生成（combat, rest, shop, transport, plot）"""

from models import TripData


def _plot_section(event: dict) -> str:
    plot_summary = event.get("plot_summary", "")
    dialogues = event.get("dialogues", [])
    related_locs = event.get("related_locations", [])
    if not plot_summary and not dialogues and not related_locs:
        return ""
    html_parts = [
        '          <div class="node-plot">',
        '            <div class="node-plot-title">📖 剧情概要</div>',
    ]
    if plot_summary:
        html_parts.append(
            f'            <div class="node-plot-summary">{plot_summary}</div>'
        )
    for d in dialogues:
        speaker = d.get("speaker", "")
        text = d.get("text", "")
        html_parts.append(f'            <div class="node-dialogue">')
        html_parts.append(
            f'              <div class="node-dialogue-speaker">🗣️ {speaker}</div>'
        )
        html_parts.append(
            f'              <div class="node-dialogue-text">"{text}"</div>'
        )
        html_parts.append(f"            </div>")
    if related_locs:
        loc_tags = "".join(
            f'<span class="node-related-loc">📍 {loc}</span>' for loc in related_locs
        )
        html_parts.append(
            f'            <div class="node-related-locations">{loc_tags}</div>'
        )
    html_parts.append("          </div>")
    return "\n".join(html_parts)


def _combat_node(event: dict, day: dict) -> str:
    link = event.get("link", "")
    price = event.get("price", "")
    key = f"poi_{event.get('name', '')}_{day.get('date', '')}"
    pic = event.get("pic_url", event.get("picUrl", ""))
    game_pic = event.get("game_pic_url", event.get("gamePicUrl", ""))
    poi_name = event.get("name", "")

    # Fallback: if no game screenshot, use the reality image for both sides
    game_img_src = game_pic if game_pic else pic
    real_img_src = pic

    game_img = (
        f'            <div class="node-img" onclick="openLightbox(this)">\n'
        f'              <img src="{game_img_src}" alt="游戏中" onerror="this.style.display=\'none\'" />\n'
        f'              <div class="node-img-label">🎮 游戏中</div>\n'
        f"            </div>"
    )
    real_img = (
        f'            <div class="node-img" onclick="openLightbox(this)">\n'
        f'              <img src="{real_img_src}" alt="实景" onerror="this.style.display=\'none\'" />\n'
        f'              <div class="node-img-label">🌍 实景</div>\n'
        f"            </div>"
    )

    img_html = (
        '          <div class="node-images">\n'
        + game_img
        + "\n"
        + real_img
        + "\n          </div>"
    )
    plot_html = _plot_section(event)
    return f"""      <div class="node node--combat">
        <div class="node-dot"></div>
        <div class="node-card">
          <div class="node-header">
            <span class="node-icon">⚔️</span>
            <span class="node-name">{event.get("name", "")}</span>
            <span class="node-badge node-badge--main">主线副本</span>
          </div>
          <div class="node-time">{day.get("date", "")} {event.get("time", "")} · 预计 {
        event.get("duration", "2小时")
    }</div>
{img_html}
          <div class="node-desc">
            <div class="desc-game">
              <div class="desc-label">🎮 游戏中</div>
              {event.get("game_desc", "")}
            </div>
            <div class="desc-reality">
              <div class="desc-label">🌍 现实中</div>
              {event.get("reality_desc", "")}
            </div>
          </div>
{plot_html}
          <div class="node-story">
            <strong>📖 剧情关联</strong><br/>
            {event.get("story_connection", event.get("story", ""))}
          </div>
          {
        f'''<div class="buy-card">
            <div class="buy-info">
              <div class="buy-name">{event.get('name', '')} 门票/体验</div>
              <div class="buy-reason">💡 {event.get('recommend_reason', '必去取景地')}</div>
            </div>
            {f'<div class="buy-price">¥{price}</div>' if price else ''}
            <div class="buy-actions">
              {f'<a href="{link}" target="_blank" rel="noopener" class="buy-btn">🛒 飞猪购买</a>' if link else ''}
              {f'<button class="copy-btn" onclick="copyLink(\'{link}\', this)">📋 复制</button>' if link else ''}
            </div>
          </div>'''
        if link
        else ""
    }
          <button class="checkin-btn" data-checkin="{key}" onclick="checkin(this, '{
        key
    }')">📍 打卡解锁</button>
        </div>
      </div>"""


def _transport_node(event: dict, day: dict) -> str:
    link = event.get("link", "")
    price = event.get("price", "")
    return f"""      <div class="node node--transport">
        <div class="node-dot"></div>
        <div class="node-card">
          <div class="node-header">
            <span class="node-icon">✈️</span>
            <span class="node-name">{event.get("name", "")}</span>
            <span class="node-badge" style="color:var(--accent)">传送门</span>
          </div>
          <div class="node-time">{day.get("date", "")} {event.get("time", "")} · {event.get("desc", "")}</div>
          <div class="buy-card">
            <div class="buy-info">
              <div class="buy-name">{event.get("desc", "")}</div>
              <div class="buy-reason">💡 {event.get("recommend_reason", "推荐航班")}</div>
            </div>
            {f'<div class="buy-price">¥{price}<small>/人</small></div>' if price else ""}
            <div class="buy-actions">
              {f'<a href="{link}" target="_blank" rel="noopener" class="buy-btn">🛒 飞猪购买</a>' if link else ""}
              {f'<button class="copy-btn" onclick="copyLink(\'{link}\', this)">📋 复制</button>' if link else ""}
            </div>
          </div>
        </div>
      </div>"""


def _rest_node(event: dict, day: dict) -> str:
    link = event.get("link", "")
    price = event.get("price", "")
    pic = event.get("pic_url", event.get("picUrl", ""))
    img_html = ""
    if pic:
        img_html = f"""          <div class="node-images">
            <div class="node-img" onclick="openLightbox(this)">
              <img src="{pic}" alt="酒店实景" onerror="this.style.display='none'" />
              <div class="node-img-label">🏨 实景</div>
            </div>
          </div>"""
    plot_html = _plot_section(event)
    return f"""      <div class="node node--rest">
        <div class="node-dot"></div>
        <div class="node-card">
          <div class="node-header">
            <span class="node-icon">🔥</span>
            <span class="node-name">{event.get("name", "")}</span>
            <span class="node-badge" style="color:var(--gold)">存档点</span>
          </div>
          <div class="node-time">{day.get("date", "")} · {event.get("address", "")}</div>
{img_html}
{plot_html}
          <div class="node-desc">
            <div class="desc-game">
              <div class="desc-label">💤 HP 回复</div>
              8小时深度睡眠
            </div>
            <div class="desc-reality">
              <div class="desc-label">☕ MP 回复</div>
              {event.get("breakfast", "免费早餐")} + WiFi
            </div>
          </div>
          <div class="buy-card">
            <div class="buy-info">
              <div class="buy-name">{event.get("name", "")} · {event.get("rating", "")}</div>
              <div class="buy-reason">💡 {event.get("recommend", event.get("recommend_reason", ""))}</div>
            </div>
            {f'<div class="buy-price">¥{price}<small>/晚</small></div>' if price else ""}
            <div class="buy-actions">
              {f'<a href="{link}" target="_blank" rel="noopener" class="buy-btn">🛒 飞猪购买</a>' if link else ""}
              {f'<button class="copy-btn" onclick="copyLink(\'{link}\', this)">📋 复制</button>' if link else ""}
            </div>
          </div>
        </div>
      </div>"""


def _shop_node(event: dict, day: dict) -> str:
    link = event.get("link", "")
    price = event.get("price", "")
    plot_html = _plot_section(event)
    return f"""      <div class="node node--shop">
        <div class="node-dot"></div>
        <div class="node-card">
          <div class="node-header">
            <span class="node-icon">🛒</span>
            <span class="node-name">{event.get("name", "")}</span>
            <span class="node-badge" style="color:var(--purple)">回血道具</span>
          </div>
          <div class="node-time">{day.get("date", "")} {event.get("time", "")} · {
        event.get("address", "")
    }</div>
{plot_html}
          <div class="node-desc">
            <div class="desc-game">
              <div class="desc-label">🎮 Buff 效果</div>
              {event.get("buff", "精力+30%")}
            </div>
            <div class="desc-reality">
              <div class="desc-label">🌍 现实</div>
              {event.get("recommend", "")} · ⭐ {event.get("rating", "")}
            </div>
          </div>
          {
        f'''<div class="buy-card">
            <div class="buy-info">
              <div class="buy-name">{event.get('name', '')}</div>
              <div class="buy-reason">💡 {event.get('recommend_reason', '')}</div>
            </div>
            {f'<div class="buy-price">¥{price}<small>/人</small></div>' if price else ''}
            <div class="buy-actions">
              {f'<a href="{link}" target="_blank" rel="noopener" class="buy-btn">🛒 飞猪购买</a>' if link else ''}
              {f'<button class="copy-btn" onclick="copyLink(\'{link}\', this)">📋 复制</button>' if link else ''}
            </div>
          </div>'''
        if link
        else ""
    }
        </div>
      </div>"""


def _generate_nodes(data: TripData) -> str:
    nodes = []

    pic_map = {}
    for p in data.pois:
        key = p.get("poi_name", p.get("name", ""))
        pic = p.get("picUrl") or p.get("pic_url") or p.get("mainPic") or ""
        game_pic = p.get("gamePicUrl") or p.get("game_pic_url") or ""
        pic_map[key] = {"pic": pic, "game_pic": game_pic}
    for h in data.hotels:
        key = h.get("hotel_name", h.get("name", ""))
        pic_map[key] = {
            "pic": h.get("mainPic") or h.get("picUrl") or "",
            "game_pic": "",
        }
    for f in data.foods:
        key = f.get("name", "")
        pic_map[key] = {"pic": f.get("picUrl") or "", "game_pic": ""}

    node_funcs = {
        "transport": _transport_node,
        "hotel": _rest_node,
        "poi": _combat_node,
        "food": _shop_node,
    }

    for i, day in enumerate(data.itinerary):
        nodes.append(
            f"    <!-- Day {i + 1}: {day.get('date')} -->\n"
            f'    <div class="day-divider">\n'
            f'      <span class="day-label">📅 {day.get("date")} · {day.get("theme", "")}</span>\n'
            f"    </div>"
        )

        for j, event in enumerate(day.get("events", [])):
            ev_type = event.get("type", "")
            func = node_funcs.get(ev_type)
            if func:
                nodes.append(func(event, day))

    return "\n\n".join(nodes)


def _get_checkpoint_keys(data: TripData) -> list[str]:
    keys = []
    for day in data.itinerary:
        for ev in day.get("events", []):
            if ev.get("type") == "poi":
                keys.append(f"poi_{ev.get('name', '')}_{day.get('date', '')}")
    return keys
