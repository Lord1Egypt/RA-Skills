#!/usr/bin/env python3
"""
YumFu Storybook Generator V3 - Rich HTML storybook from session logs.

Goals:
- single-file portable HTML with embedded images
- stronger classical storybook presentation
- decode accidental unicode-escaped strings like \u9aa8\u602a\u7cbe\u7075
- avoid empty stats sections by pulling from multiple save fields
- avoid lazy image captions like filename fragments ("Watch", "Thread")
- stay scene-bound: image + matching text in the same block
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


WORLD_LABELS = {
    "warrior-cats": {"zh": "猫武士宇宙", "en": "Warrior Cats Universe"},
    "xiaoao": {"zh": "笑傲江湖宇宙", "en": "Xiaoao Jianghu Universe"},
    "harry-potter": {"zh": "霍格沃茨宇宙", "en": "Hogwarts Universe"},
    "lotr": {"zh": "中土宇宙", "en": "Middle-earth Universe"},
    "game-of-thrones": {"zh": "冰与火之歌宇宙", "en": "A Song of Ice and Fire Universe"},
    "journey-to-west": {"zh": "西游记宇宙", "en": "Journey to the West Universe"},
}

WORLD_TITLES = {
    "warrior-cats": {"zh": "猫武士传奇", "en": "A Warrior Cats Tale"},
    "xiaoao": {"zh": "笑傲江湖传奇", "en": "A Wuxia Chronicle"},
    "harry-potter": {"zh": "霍格沃茨奇旅", "en": "A Hogwarts Adventure"},
    "lotr": {"zh": "中土战记", "en": "A Chronicle of Middle-earth"},
    "game-of-thrones": {"zh": "冰火编年", "en": "A Chronicle of Ice and Fire"},
    "journey-to-west": {"zh": "西游异闻", "en": "Journey to the West"},
}

ZH_LABELS = {
    "hp": "气血",
    "stamina": "体力",
    "level": "等级",
    "gold": "金钱",
    "silver": "银两",
    "house_points": "学院分",
    "strength": "武力",
    "dexterity": "身法",
    "constitution": "体魄",
    "intelligence": "智谋",
    "wisdom": "悟性",
    "charisma": "气势",
    "morality": "善恶",
    "reputation": "声望",
}

EN_LABELS = {
    "hp": "HP",
    "stamina": "Stamina",
    "level": "Level",
    "gold": "Gold",
    "silver": "Silver",
    "house_points": "House Points",
    "strength": "Strength",
    "dexterity": "Dexterity",
    "constitution": "Constitution",
    "intelligence": "Intelligence",
    "wisdom": "Wisdom",
    "charisma": "Charisma",
    "morality": "Morality",
    "reputation": "Reputation",
}


def decode_unicode_escapes(text: Any) -> str:
    if text is None:
        return ""
    value = str(text)
    if re.search(r"\\u[0-9a-fA-F]{4}", value):
        value = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), value)
    value = value.replace("\\n", "\n").replace("\\t", "\t")
    return value


def clean_text(text: Any) -> str:
    value = decode_unicode_escapes(text)
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    return value.strip()


def html_text(text: Any) -> str:
    return html.escape(clean_text(text), quote=True)


def first_sentence(text: str) -> str:
    raw = clean_text(text)
    if not raw:
        return ""
    raw = re.sub(r"^([⚔️🎨📍💬🏆✨🌙🐍🗡️⚡🔥🎩📅▶️]+\s*)+", "", raw).strip()
    parts = re.split(r"(?<=[。！？.!?])\s+|[\n]+", raw)
    for part in parts:
        part = part.strip().strip('"“”')
        if part:
            return part
    return raw


def truncate_title(text: str, lang: str) -> str:
    raw = first_sentence(text)
    if not raw:
        return ""
    if lang == "zh":
        raw = raw.replace("。", "").replace("！", "").replace("？", "")
        return raw[:12] + ("…" if len(raw) > 12 else "")
    words = raw.split()
    title = " ".join(words[:6])
    if len(words) > 6:
        title += "…"
    return title


def split_paragraphs(text: str) -> List[str]:
    raw = clean_text(text)
    if not raw:
        return []
    if "\n\n" in raw:
        parts = [p.strip() for p in raw.split("\n\n") if p.strip()]
    else:
        parts = [p.strip() for p in raw.split("\n") if p.strip()]
    if not parts:
        parts = [raw]
    return parts


def zh_turn_number(n: int) -> str:
    digits = "零一二三四五六七八九"
    if n <= 10:
        return "十" if n == 10 else digits[n]
    if n < 20:
        return "十" + digits[n - 10]
    tens, ones = divmod(n, 10)
    if ones == 0:
        return digits[tens] + "十"
    return digits[tens] + "十" + digits[ones]


class StorybookV3:
    def __init__(self, user_id: str, universe: str, session_id: str | None = None):
        self.user_id = user_id
        self.universe = universe
        self.base_path = Path.home() / "clawd/memory/yumfu"
        self.save_path = self.base_path / "saves" / universe / f"user-{user_id}.json"
        self.session_dir = self.base_path / "sessions" / universe / f"user-{user_id}"
        self.session_id = session_id or self._find_latest_session()
        self.session_file = self.session_dir / f"session-{self.session_id}.jsonl"

        if not self.session_file.exists():
            raise FileNotFoundError(f"Session log not found: {self.session_file}")

        if self.save_path.exists():
            self.save_data = json.loads(self.save_path.read_text(encoding="utf-8"))
        else:
            self.save_data = {"character": {"name": "Unknown Hero"}}

        self.language = "zh" if str(self.save_data.get("language", "en")).startswith("zh") else "en"

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.output_dir = self.base_path / "storybooks" / universe / f"user-{user_id}-{timestamp}"
        self.images_dir = self.output_dir / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)

    def _find_latest_session(self) -> str:
        if not self.session_dir.exists():
            raise FileNotFoundError(f"No sessions found for user {self.user_id}")
        sessions = sorted(self.session_dir.glob("session-*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not sessions:
            raise FileNotFoundError(f"No session logs found in {self.session_dir}")
        return sessions[0].stem.replace("session-", "")

    def load_session_log(self) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        with self.session_file.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
        return events

    def _resolve_image_path(self, image_ref: str) -> Optional[Path]:
        if not image_ref:
            return None
        ref_path = Path(image_ref)
        if ref_path.exists():
            return ref_path

        basename = ref_path.name
        search_roots = [
            Path.home() / ".openclaw/media/outbound/yumfu",
            Path.home() / ".openclaw/media/outbound",
            Path.home() / ".openclaw/media/tool-image-generation",
            Path.home() / "clawd/output",
        ]

        for root in search_roots:
            if not root.exists():
                continue
            exact = root / basename
            if exact.exists():
                return exact

        stem = Path(basename).stem.lower()
        stem_tokens = [tok for tok in stem.replace("_", "-").split("-") if tok]
        for root in search_roots:
            if not root.exists():
                continue
            for p in root.rglob("*"):
                if not p.is_file():
                    continue
                p_name = p.name.lower()
                p_stem = p.stem.lower()
                if basename.lower() == p_name:
                    return p
                if stem and (stem in p_stem or p_stem in stem):
                    return p
                if stem_tokens and sum(1 for tok in stem_tokens if tok in p_stem) >= max(2, min(4, len(stem_tokens))):
                    return p
        return None

    def collect_images(self, events: List[Dict[str, Any]]) -> Dict[str, Path]:
        image_map: Dict[str, Path] = {}
        for event in events:
            img_ref = event.get("image") or event.get("filename")
            if not img_ref:
                continue
            img_path = self._resolve_image_path(str(img_ref))
            if img_path and img_path.exists():
                dest = self.images_dir / img_path.name
                if not dest.exists():
                    shutil.copy2(img_path, dest)
                image_map[str(img_ref)] = dest
        return image_map

    def _image_src(self, path: Path) -> str:
        mime, _ = mimetypes.guess_type(path.name)
        mime = mime or "image/png"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{data}"

    def _label(self, key: str) -> str:
        return (ZH_LABELS if self.language == "zh" else EN_LABELS).get(key, key.replace("_", " ").title())

    def _pct(self, value: Any, max_value: Any | None = None) -> int:
        try:
            number = float(value)
        except Exception:
            return 0
        if max_value is not None:
            try:
                maximum = float(max_value)
                if maximum > 0:
                    return max(0, min(100, int(round(number / maximum * 100))))
            except Exception:
                pass
        return max(0, min(100, int(round(number))))

    def _render_stat_item(self, label: str, value_display: str, pct: int) -> str:
        return f'''
      <div class="stat-item">
        <span class="stat-label">{html_text(label)}</span>
        <span><span class="stat-value">{html_text(value_display)}</span><span class="stat-bar"><span class="stat-bar-fill" style="width:{pct}%"></span></span></span>
      </div>'''

    def _extract_stats(self) -> dict[str, Any]:
        character = self.save_data.get("character", {}) if isinstance(self.save_data.get("character"), dict) else {}
        attrs = character.get("attributes", {}) if isinstance(character.get("attributes"), dict) else {}
        stats_items: List[str] = []

        hp = character.get("hp")
        hp_max = character.get("hp_max")
        if hp is not None:
            display = f"{hp}/{hp_max}" if hp_max not in (None, "", 0) else str(hp)
            stats_items.append(self._render_stat_item(self._label("hp"), display, self._pct(hp, hp_max)))

        stamina = character.get("stamina")
        stamina_max = character.get("stamina_max")
        if stamina is not None:
            display = f"{stamina}/{stamina_max}" if stamina_max not in (None, "", 0) else str(stamina)
            stats_items.append(self._render_stat_item(self._label("stamina"), display, self._pct(stamina, stamina_max)))

        for key in ["level", "gold", "silver", "house_points", "morality"]:
            value = character.get(key, self.save_data.get(key))
            if isinstance(value, (int, float)):
                stats_items.append(self._render_stat_item(self._label(key), str(value), self._pct(value)))

        rep_value = self.save_data.get("reputation", character.get("reputation"))
        if isinstance(rep_value, (int, float)):
            stats_items.append(self._render_stat_item(self._label("reputation"), str(rep_value), self._pct(rep_value)))

        for key, value in attrs.items():
            stats_items.append(self._render_stat_item(self._label(str(key)), str(value), self._pct(value)))

        if not stats_items:
            for key, value in character.items():
                if key in {"name", "role", "house", "race", "trait", "skills", "attributes"}:
                    continue
                if isinstance(value, (int, float)):
                    stats_items.append(self._render_stat_item(self._label(str(key)), str(value), self._pct(value)))

        skills = []
        if isinstance(character.get("skills"), dict):
            for name, value in character["skills"].items():
                if isinstance(value, (int, float)):
                    skills.append(f"{decode_unicode_escapes(name)} {value}")
                else:
                    skills.append(decode_unicode_escapes(name))
        for key in ["spells_known", "potions_learned", "battle_moves_learned"]:
            value = self.save_data.get(key)
            if isinstance(value, list):
                skills.extend([decode_unicode_escapes(v) for v in value[:8]])
        skills_learned = self.save_data.get("skills_learned")
        if isinstance(skills_learned, list):
            for item in skills_learned[:8]:
                if isinstance(item, dict):
                    name = decode_unicode_escapes(item.get("name", ""))
                    mastery = item.get("mastery")
                    level = item.get("level")
                    detail_bits = []
                    if isinstance(level, (int, float)):
                        detail_bits.append(f"Lv{int(level)}")
                    if isinstance(mastery, (int, float)):
                        detail_bits.append(f"{int(mastery)}")
                    detail = " · ".join(detail_bits)
                    skills.append(f"{name}{(' ' + detail) if detail else ''}".strip())
                elif item:
                    skills.append(decode_unicode_escapes(item))
        skills = [s for s in skills if s][:10]

        items = []
        inventory = self.save_data.get("inventory")
        if isinstance(inventory, list):
            for item in inventory[:10]:
                if isinstance(item, dict):
                    items.append(decode_unicode_escapes(item.get("name", "")))
                elif item:
                    items.append(decode_unicode_escapes(item))
        items = [i for i in items if i]

        relationships = []
        rels = self.save_data.get("relationships")
        if isinstance(rels, dict):
            for name, value in rels.items():
                score = None
                note = ""
                if isinstance(value, dict):
                    for field in ["affection", "trust", "favor", "score", "value", "relationship"]:
                        if isinstance(value.get(field), (int, float)):
                            score = value.get(field)
                            break
                    note = decode_unicode_escapes(value.get("status") or value.get("description") or "")
                elif isinstance(value, (int, float)):
                    score = value
                else:
                    note = decode_unicode_escapes(value)
                relationships.append({
                    "name": decode_unicode_escapes(name),
                    "score": score,
                    "note": note,
                })
        relationships = relationships[:12]

        metrics = []
        for key in ["role", "trait", "house", "race", "faction", "year", "season", "time_of_day", "region"]:
            value = character.get(key, self.save_data.get(key))
            if value not in (None, "", [], {}):
                metrics.append(f"{self._label(key)} {decode_unicode_escapes(value)}")
        location = self.save_data.get("location")
        if location:
            metrics.append(("地点 " if self.language == "zh" else "Location ") + decode_unicode_escapes(location))
        metrics = metrics[:10]

        ending = self._extract_ending()

        return {
            "stats_items": stats_items,
            "skills": skills,
            "items": items,
            "relationships": relationships,
            "metrics": metrics,
            "ending": ending,
        }

    def _extract_ending(self) -> Optional[dict[str, str]]:
        # Prefer explicit ending metadata if the save/world writes one.
        candidates: List[tuple[str, str]] = []

        def walk(obj: Any) -> None:
            if isinstance(obj, dict):
                title = obj.get("ending") or obj.get("ending_title") or obj.get("finale") or obj.get("outcome")
                desc = obj.get("ending_description") or obj.get("description") or obj.get("epilogue") or obj.get("result")
                if isinstance(title, str):
                    candidates.append((title, desc if isinstance(desc, str) else ""))
                for value in obj.values():
                    walk(value)
            elif isinstance(obj, list):
                for value in obj[:40]:
                    walk(value)

        walk(self.save_data)
        for title, desc in candidates:
            clean_title = clean_text(title)
            if clean_title and len(clean_title) < 80:
                return {"title": clean_title, "desc": clean_text(desc)}

        achievements = self.save_data.get("achievements")
        if isinstance(achievements, list):
            for ach in reversed(achievements):
                ach_text = clean_text(ach)
                if any(token in ach_text.lower() for token in ["ending", "epilogue", "结局", "终局"]):
                    return {"title": ach_text, "desc": ""}
        return None

    def _cover_title(self, events: List[Dict[str, Any]]) -> tuple[str, str, str]:
        character = self.save_data.get("character", {}) if isinstance(self.save_data.get("character"), dict) else {}
        explicit_title = clean_text(self.save_data.get("storybook_title"))
        explicit_sub = clean_text(self.save_data.get("storybook_subtitle"))
        if explicit_title:
            title = explicit_title
            subtitle = explicit_sub or clean_text(character.get("name")) or WORLD_TITLES.get(self.universe, {}).get(self.language, self.universe)
        else:
            title = clean_text(character.get("name")) or WORLD_TITLES.get(self.universe, {}).get(self.language, self.universe.replace("-", " ").title())
            subtitle = clean_text(character.get("role") or character.get("trait") or self.save_data.get("goal") or self.save_data.get("location"))
            if not subtitle:
                subtitle = WORLD_TITLES.get(self.universe, {}).get(self.language, self.universe.replace("-", " ").title())

        badge = WORLD_LABELS.get(self.universe, {}).get(self.language, self.universe.replace("-", " ").title())
        return title, subtitle, badge

    def _scene_caption(self, event: Dict[str, Any], narrative: str = "", previous_caption: str = "") -> str:
        meta = event.get("metadata") or {}
        for key in ["image_caption", "caption", "scene_caption", "scene_title", "chapter_title", "description"]:
            candidate = clean_text(meta.get(key) if isinstance(meta, dict) else None)
            if candidate:
                return candidate
        for key in ["description", "content", "ai_storybook", "ai", "player_storybook"]:
            candidate = clean_text(event.get(key))
            if candidate:
                sent = first_sentence(candidate)
                if sent:
                    return sent
        if narrative:
            sent = first_sentence(narrative)
            if sent:
                return sent
        return previous_caption or ("画面定格于此" if self.language == "zh" else "The scene holds here.")

    def _event_title(self, event: Dict[str, Any], idx: int, caption: str) -> str:
        meta = event.get("metadata") or {}
        if isinstance(meta, dict):
            for key in ["chapter_title", "scene_title", "title"]:
                candidate = clean_text(meta.get(key))
                if candidate:
                    return candidate
        preferred = clean_text(event.get("player_storybook") or event.get("content") or event.get("player"))
        fallback = clean_text(event.get("ai_storybook") or event.get("ai"))
        raw = preferred or caption or fallback
        title = truncate_title(raw, self.language)
        if title:
            return title
        return (f"第{zh_turn_number(idx)}回" if self.language == "zh" else f"Scene {idx}")

    def _event_subtitle(self, event: Dict[str, Any]) -> str:
        meta = event.get("metadata") or {}
        if isinstance(meta, dict):
            for key in ["subtitle", "location", "scene_subtitle"]:
                candidate = clean_text(meta.get(key))
                if candidate:
                    return candidate
        content = clean_text(event.get("content"))
        if content and len(content) <= 40:
            return content
        location = clean_text(self.save_data.get("location"))
        if location:
            return location
        quest_stage = ""
        quests = self.save_data.get("quests")
        if isinstance(quests, list) and quests:
            first = quests[0]
            if isinstance(first, dict):
                quest_stage = clean_text(first.get("current_stage") or first.get("progress"))
        return quest_stage

    def _choice_label(self, player: str) -> str:
        raw = clean_text(player)
        lowered = raw.lower()
        if lowered.startswith("/yumfu "):
            raw = raw[7:].strip()
        elif lowered == "/yumfu":
            raw = "continue"
        if not raw:
            return ""
        if self.language == "zh":
            return f"⚔ 选择：{raw}"
        return f"⚔ Choice: {raw}"

    def _render_story_paragraphs(self, text: str) -> str:
        paras = split_paragraphs(text)
        if not paras:
            return ""
        rendered = "".join(f"<p>{html_text(p)}</p>" for p in paras)
        return f'<div class="story-text">{rendered}</div>'

    def _render_image_block(self, img_ref: str, images: Dict[str, Path], caption: str) -> str:
        if not img_ref or img_ref not in images:
            return ""
        img_path = images[img_ref]
        return f'''
        <div class="image-block">
            <img src="{self._image_src(img_path)}" alt="{html_text(caption)}">
            <p class="image-caption">{html_text(caption)}</p>
        </div>'''

    def _render_stats_section(self) -> str:
        data = self._extract_stats()
        stats_grid = "".join(data["stats_items"]) or ("<p class=\"empty-note\">暂无可展示的角色数值。</p>" if self.language == "zh" else "<p class=\"empty-note\">No character stats available yet.</p>")

        def render_tags(items: List[str]) -> str:
            if not items:
                return '<div class="tag-list"><span class="tag">' + ("暂无" if self.language == "zh" else "None yet") + '</span></div>'
            return '<div class="tag-list">' + ''.join(f'<span class="tag">{html_text(item)}</span>' for item in items) + '</div>'

        rel_html = ''
        if data['relationships']:
            rel_items = []
            for rel in data['relationships']:
                score = rel['score']
                if isinstance(score, (int, float)):
                    if score > 0:
                        cls = 'trust-pos'
                        score_text = f'+{int(score)}'
                    elif score < 0:
                        cls = 'trust-neg'
                        score_text = str(int(score))
                    else:
                        cls = 'trust-neu'
                        score_text = '±0' if self.language == 'zh' else '0'
                else:
                    cls = 'trust-neu'
                    score_text = rel['note'] or ('—' if self.language == 'zh' else '—')
                rel_items.append(f'<div class="trust-item"><span class="trust-name">{html_text(rel["name"])}</span><span class="trust-val {cls}">{html_text(score_text)}</span></div>')
            rel_html = ''.join(rel_items)
        else:
            rel_html = f'<div class="tag-list"><span class="tag">{"暂无 NPC 关系数据" if self.language == "zh" else "No relationship data yet"}</span></div>'

        ending_html = ''
        if data['ending']:
            ending_html = f'''
    <div class="ending-box">
      <div class="ending-title">{html_text(data['ending']['title'])}</div>
      <div class="ending-desc">{html_text(data['ending']['desc'] or ('旅程在这里收束，但余波仍未散尽。' if self.language == 'zh' else 'The journey closes here, but its aftershock remains.')).replace(chr(10), '<br>')}</div>
    </div>'''

        title = "📊 终局角色档案" if self.language == 'zh' else '📊 Final Character Archive'
        skills_label = '核心技能' if self.language == 'zh' else 'Core Skills'
        items_label = '随身道具' if self.language == 'zh' else 'Inventory'
        trust_label = 'NPC 关系 / 倾向' if self.language == 'zh' else 'NPC Relationships'
        other_label = '其他指标' if self.language == 'zh' else 'Other Metrics'

        return f'''
  <div class="stats-section">
    <h2>{title}</h2>
    <div class="stats-grid">{stats_grid}
    </div>
    <div class="skills-row">
      <div class="row-label">{skills_label}</div>
      {render_tags(data['skills'])}
    </div>
    <div class="items-row">
      <div class="row-label">{items_label}</div>
      {render_tags(data['items'])}
    </div>
    <div class="trust-row">
      <div class="row-label">{trust_label}</div>
      <div class="trust-grid">{rel_html}</div>
    </div>
    <div class="trust-row">
      <div class="row-label">{other_label}</div>
      {render_tags(data['metrics'])}
    </div>
    {ending_html}
  </div>'''

    def build_story_blocks(self, events: List[Dict[str, Any]], images: Dict[str, Path]) -> List[str]:
        blocks: List[str] = []
        turn_index = 0
        previous_caption = ""
        pending_image_block = None

        for event in events:
            event_type = event.get("type")
            if event_type == "turn":
                turn_index += 1
                player = clean_text(event.get("player"))
                player_storybook = clean_text(event.get("player_storybook")) or player
                ai_storybook = clean_text(event.get("ai_storybook")) or clean_text(event.get("ai"))
                img = event.get("image")
                caption = self._scene_caption(event, ai_storybook, previous_caption)
                previous_caption = caption or previous_caption
                title = self._event_title(event, turn_index, caption)
                subtitle = self._event_subtitle(event)
                choice = self._choice_label(player)
                heading_num = f"第 {turn_index} 回" if self.language == "zh" else f"Scene {turn_index}"
                image_html = self._render_image_block(str(img), images, caption) if img else ""
                player_para = f'<p>{html_text(player_storybook)}</p>' if player_storybook and player_storybook != player else ''
                ai_body = ''.join(f'<p>{html_text(p)}</p>' for p in split_paragraphs(ai_storybook))
                blocks.append(f'''
    <div class="turn-block" id="turn-{turn_index}">
        <div class="turn-header">
            <span class="turn-num">{html_text(heading_num)}</span>
            <h2 class="turn-title">{html_text(title)}</h2>
            <div class="turn-subtitle">{html_text(subtitle)}</div>
        </div>
        {f'<div class="choice-tag">{html_text(choice)}</div>' if choice else ''}
        {image_html}
        <div class="story-text">{player_para}{ai_body}</div>
    </div>
''')
            elif event_type == "dialogue":
                turn_index += 1
                speaker = clean_text(event.get("speaker")) or ("无名者" if self.language == "zh" else "Unknown")
                content = clean_text(event.get("content"))
                img = event.get("image")
                caption = self._scene_caption(event, content, previous_caption)
                previous_caption = caption or previous_caption
                title = speaker
                subtitle = self._event_subtitle(event)
                image_html = self._render_image_block(str(img), images, caption) if img else ""
                blocks.append(f'''
    <div class="turn-block" id="turn-{turn_index}">
        <div class="turn-header">
            <span class="turn-num">{html_text('对话' if self.language == 'zh' else 'Dialogue')}</span>
            <h2 class="turn-title">{html_text(title)}</h2>
            <div class="turn-subtitle">{html_text(subtitle)}</div>
        </div>
        {image_html}
        <div class="story-text"><p>“{html_text(content)}”</p></div>
    </div>
''')
            elif event_type == "event":
                content = clean_text(event.get("content"))
                if content:
                    blocks.append(f'<div class="event-banner">{html_text(content)}</div>')
            elif event_type == "image":
                img = event.get("filename")
                caption = self._scene_caption(event, event.get("description", ""), previous_caption)
                previous_caption = caption or previous_caption
                image_html = self._render_image_block(str(img), images, caption) if img else ""
                if image_html:
                    blocks.append(f'<div class="turn-block image-only">{image_html}</div>')
        return blocks

    def generate_html(self, events: List[Dict[str, Any]], images: Dict[str, Path]) -> str:
        title, subtitle, badge = self._cover_title(events)
        character = self.save_data.get("character", {}) if isinstance(self.save_data.get("character"), dict) else {}
        role_line_bits = []
        if clean_text(character.get("name")):
            role_line_bits.append(("角色：" if self.language == "zh" else "Hero: ") + clean_text(character.get("name")))
        for key in ["role", "trait", "house", "race"]:
            value = clean_text(character.get(key))
            if value:
                role_line_bits.append(value)
                break
        role_line = " &emsp;|&emsp; ".join(html.escape(bit) for bit in role_line_bits if bit)
        count_line = (f"共 {sum(1 for e in events if e.get('type') in {'turn','dialogue'})} 回" if self.language == "zh" else f"{sum(1 for e in events if e.get('type') in {'turn','dialogue'})} scenes")

        story_blocks = self.build_story_blocks(events, images)
        toc_links = []
        scene_num = 0
        for block in story_blocks:
            m = re.search(r'id="turn-(\d+)".*?<h2 class="turn-title">(.*?)</h2>', block, re.S)
            if not m:
                continue
            scene_num += 1
            toc_links.append(f'<a href="#turn-{m.group(1)}">{html.unescape(m.group(2))}</a>')

        footer_title = clean_text(title) or clean_text(character.get('name')) or WORLD_TITLES.get(self.universe, {}).get(self.language, self.universe)
        footer_date = datetime.now().strftime('%Y-%m-%d')
        print_label = '📄 打印 / 存 PDF' if self.language == 'zh' else '📄 Print / Save PDF'
        toc_label = '回目总览' if self.language == 'zh' else 'Contents'

        return f'''<!DOCTYPE html>
<html lang="{'zh-CN' if self.language == 'zh' else 'en'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_text(title)}{(' —— ' + html_text(subtitle)) if subtitle else ''}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');
  :root {{ --ink:#1a1008; --paper:#faf6ef; --gold:#b8872a; --red:#8b1a1a; --bone:#d4c5a9; --shadow:rgba(100,60,20,0.15); }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Noto Serif SC','STSong','SimSun',serif; background:#2a1f14; color:var(--ink); line-height:1.9; }}
  .page-wrap {{ max-width:860px; margin:0 auto; background:var(--paper); min-height:100vh; box-shadow:0 0 60px rgba(0,0,0,0.6); }}
  .cover {{ background:linear-gradient(160deg,#1a0d05 0%,#3d1f0a 50%,#1a0d05 100%); padding:5em 3em 4em; text-align:center; position:relative; overflow:hidden; border-bottom:6px solid var(--gold); }}
  .cover::before {{ content:''; position:absolute; inset:0; background:repeating-linear-gradient(45deg,transparent,transparent 20px,rgba(180,130,40,0.04) 20px,rgba(180,130,40,0.04) 21px); }}
  .cover-badge {{ display:inline-block; border:2px solid var(--gold); color:var(--gold); font-size:0.85em; letter-spacing:0.3em; padding:0.3em 1.2em; margin-bottom:2em; position:relative; }}
  .cover h1 {{ font-size:3.2em; color:#f0e0c0; font-weight:700; line-height:1.3; letter-spacing:0.05em; text-shadow:0 2px 12px rgba(0,0,0,0.8); margin-bottom:0.3em; position:relative; }}
  .cover h1 em {{ color:var(--gold); font-style:normal; }}
  .cover-sub {{ color:#c8a870; font-size:1.15em; letter-spacing:0.2em; margin-bottom:2.5em; position:relative; }}
  .cover-divider {{ width:200px; height:1px; background:linear-gradient(90deg,transparent,var(--gold),transparent); margin:1.5em auto; position:relative; }}
  .cover-meta {{ color:#907850; font-size:0.9em; letter-spacing:0.1em; position:relative; }}
  .toc {{ background:#f5efe4; border-bottom:3px solid var(--bone); padding:2em 3em; }}
  .toc h3 {{ color:var(--red); font-size:1em; letter-spacing:0.3em; margin-bottom:1.2em; border-bottom:1px solid var(--bone); padding-bottom:0.5em; }}
  .toc-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:0.4em 1em; }}
  .toc-grid a {{ color:#5a3e1b; text-decoration:none; font-size:0.88em; padding:0.2em 0; border-bottom:1px dotted var(--bone); transition:color 0.2s; }}
  .toc-grid a:hover {{ color:var(--red); }}
  .story-wrap {{ padding:1em 0; }}
  .turn-block {{ padding:3em 3.5em; border-bottom:1px solid #e8ddd0; page-break-inside:avoid; }}
  .turn-block:nth-child(even) {{ background:#fdf9f4; }}
  .turn-header {{ margin-bottom:1.2em; display:flex; align-items:baseline; gap:1em; flex-wrap:wrap; }}
  .turn-num {{ font-size:0.78em; color:var(--gold); letter-spacing:0.25em; border:1px solid var(--gold); padding:0.15em 0.6em; white-space:nowrap; flex-shrink:0; }}
  .turn-title {{ font-size:1.55em; color:var(--red); font-weight:700; flex:1; min-width:0; }}
  .turn-subtitle {{ width:100%; color:#7a5c30; font-size:0.9em; letter-spacing:0.12em; margin-top:-0.5em; }}
  .choice-tag {{ display:inline-block; background:#3d1f0a; color:#d4a84b; font-size:0.82em; padding:0.3em 1em; border-radius:2px; margin-bottom:1.8em; letter-spacing:0.08em; }}
  .image-block {{ margin:1.5em 0 2em; text-align:center; }}
  .image-block img {{ width:100%; max-width:600px; height:auto; border-radius:6px; box-shadow:0 6px 30px var(--shadow); border:3px solid var(--bone); }}
  .image-caption {{ color:#8a7050; font-size:0.9em; font-style:italic; margin-top:0.7em; letter-spacing:0.05em; }}
  .story-text p {{ margin-bottom:1em; font-size:1.05em; text-align:justify; }}
  .story-text p:last-child {{ color:#5a3e1b; font-size:0.92em; background:#f0e8d8; border-left:3px solid var(--gold); padding:0.6em 1em; margin-top:0.5em; border-radius:0 4px 4px 0; }}
  .event-banner {{ margin:1.5em 3.5em; background:linear-gradient(135deg,#5d3d12 0%,#8b1a1a 100%); color:#f6ead0; padding:1em 1.4em; border-radius:6px; text-align:center; letter-spacing:0.08em; box-shadow:0 5px 18px rgba(0,0,0,0.18); }}
  .stats-section {{ background:linear-gradient(160deg,#1a0d05 0%,#2d1505 100%); padding:3.5em 3.5em; color:#d4c5a9; border-top:4px solid var(--gold); }}
  .stats-section h2 {{ color:var(--gold); font-size:1.3em; letter-spacing:0.3em; text-align:center; margin-bottom:2em; padding-bottom:0.8em; border-bottom:1px solid #5a3e1b; }}
  .stats-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:1.5em 3em; margin-bottom:2em; }}
  .stat-item {{ display:flex; justify-content:space-between; align-items:center; padding:0.5em 0; border-bottom:1px solid #3a2a1a; }}
  .stat-label {{ color:#907850; font-size:0.9em; letter-spacing:0.1em; }}
  .stat-value {{ color:#f0d898; font-weight:600; font-size:1.05em; }}
  .stat-bar {{ width:80px; height:6px; background:#3a2a1a; border-radius:3px; overflow:hidden; display:inline-block; vertical-align:middle; margin-left:0.5em; }}
  .stat-bar-fill {{ height:100%; background:linear-gradient(90deg,var(--gold),#f0d040); border-radius:3px; }}
  .skills-row,.items-row,.trust-row {{ margin-bottom:1.5em; }}
  .row-label {{ color:var(--gold); font-size:0.82em; letter-spacing:0.25em; margin-bottom:0.6em; }}
  .tag-list {{ display:flex; flex-wrap:wrap; gap:0.5em; }}
  .tag {{ background:#3a2a1a; color:#d4a84b; padding:0.25em 0.8em; border-radius:2px; font-size:0.88em; border:1px solid #5a3e1b; }}
  .trust-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:0.7em; }}
  .trust-item {{ background:#2d1505; border:1px solid #4a3015; padding:0.6em 0.8em; border-radius:4px; display:flex; justify-content:space-between; align-items:center; }}
  .trust-name {{ color:#c8a870; font-size:0.88em; }}
  .trust-val {{ font-size:0.95em; font-weight:600; }}
  .trust-pos {{ color:#7fd87f; }} .trust-neg {{ color:#e07070; }} .trust-neu {{ color:#a0a080; }}
  .ending-box {{ text-align:center; margin-top:2em; padding:1.5em; border:1px solid var(--gold); border-radius:4px; background:rgba(180,130,40,0.07); }}
  .ending-title {{ color:var(--gold); font-size:1.1em; letter-spacing:0.2em; margin-bottom:0.5em; }}
  .ending-desc {{ color:#c8a870; font-size:0.92em; line-height:1.7; }}
  .empty-note {{ color:#a99372; font-style:italic; }}
  .footer {{ text-align:center; padding:2em; background:#1a0d05; color:#5a3e1b; font-size:0.82em; letter-spacing:0.1em; }}
  .print-btn {{ position:fixed; top:20px; right:20px; z-index:999; background:var(--red); color:#f0e0c0; border:none; padding:0.7em 1.5em; border-radius:3px; cursor:pointer; font-family:inherit; font-size:0.9em; box-shadow:0 3px 12px rgba(0,0,0,0.4); letter-spacing:0.1em; }}
  .print-btn:hover {{ background:#a02020; }}
  @media print {{ .print-btn {{ display:none; }} body {{ background:white; }} .cover {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }} }}
  @media (max-width: 600px) {{ .turn-block {{ padding:2em 1.5em; }} .cover {{ padding:3em 1.5em; }} .cover h1 {{ font-size:2.2em; }} .stats-grid {{ grid-template-columns:1fr; }} .toc {{ padding:1.5em; }} .event-banner {{ margin:1em 1.5em; }} }}
</style>
</head>
<body>
<button class="print-btn no-print" onclick="window.print()">{html_text(print_label)}</button>
<div class="page-wrap">
  <div class="cover">
    <div class="cover-badge">YumFu · {html_text(badge)}</div>
    <h1>{html_text(title)}</h1>
    <div class="cover-sub">{html_text(subtitle)}</div>
    <div class="cover-divider"></div>
    <div class="cover-meta">{role_line}<br>{html_text(count_line)}</div>
  </div>
  <div class="toc">
    <h3>{html_text(toc_label)}</h3>
    <div class="toc-grid">{''.join(toc_links) if toc_links else '<span>' + ('暂无目录' if self.language == 'zh' else 'No scenes yet') + '</span>'}</div>
  </div>
  <div class="story-wrap">
    {''.join(story_blocks)}
  </div>
  {self._render_stats_section()}
  <div class="footer">YumFu Storybook · {html_text(footer_title)} · {html_text(footer_date)}</div>
</div>
</body>
</html>'''

    def generate(self) -> Path:
        print(f"📚 Generating Storybook V3 for {clean_text(self.save_data.get('character', {}).get('name', 'Unknown')) or 'Unknown'}...")
        print(f"   Session: {self.session_id}")
        print("📖 Loading session log...")
        events = self.load_session_log()
        print(f"   Found {len(events)} events")
        print("🎨 Collecting images...")
        images = self.collect_images(events)
        print(f"   Found {len(images)} images")
        print("✍️  Creating storybook...")
        html_content = self.generate_html(events, images)
        html_file = self.output_dir / "storybook.html"
        html_file.write_text(html_content, encoding="utf-8")
        print(f"\n🎉 Storybook complete!")
        print(f"📁 Location: {self.output_dir}")
        print(f"🌐 HTML: {html_file}")
        print(f"🖼️  Images: {len(images)} files")
        return html_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate YumFu Storybook V3 from session logs")
    parser.add_argument("--user-id", required=True, help="User ID")
    parser.add_argument("--universe", required=True, help="World")
    parser.add_argument("--session-id", help="Optional session ID")
    args = parser.parse_args()

    try:
        generator = StorybookV3(user_id=args.user_id, universe=args.universe, session_id=args.session_id)
        html_file = generator.generate()
        try:
            import webbrowser
            webbrowser.open(f"file://{html_file}")
            print("\n🌐 Opened in browser!")
        except Exception:
            print(f"\n💡 Open manually: file://{html_file}")
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print(f"\n💡 Tip: Make sure session logs exist under ~/clawd/memory/yumfu/sessions/{args.universe}/user-{args.user_id}/")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
