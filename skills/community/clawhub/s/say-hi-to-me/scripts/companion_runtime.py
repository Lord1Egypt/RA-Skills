#!/usr/bin/env python3
"""
Runtime helper for dual-entry companion workflow (command + natural language).
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from command_normalizer import normalize_input
from generate_rolecard import build_rolecard, slugify
from sync_heartbeat_md import sync_heartbeat_md
from validate_rolecard import validate_file

LOCAL_TZ = dt.datetime.now().astimezone().tzinfo or dt.timezone.utc
ROMANTIC_LABELS = {"girlfriend", "boyfriend", "partner", "spouse"}
SESSION_SCHEMA_VERSION = 1


DEFAULT_SESSION: Dict[str, Any] = {
    "schema_version": SESSION_SCHEMA_VERSION,
    "initialized": False,
    "proactive": {
        "enabled": False,
        "frequency": "mid",
        "quiet_hours": None,
        "pause_until": None,
        "last_sent_at": None,
    },
    "context": {
        "freshness_hours": 72,
    },
    "role": {
        "active": None,
        "draft": None,
        "pending_activation": None,
    },
    "last_user_input_at": None,
    "updated_at": None,
}


def now_iso() -> str:
    return dt.datetime.now(tz=LOCAL_TZ).isoformat(timespec="seconds")


def normalize_iso_with_tz(value: Any) -> Any:
    if not isinstance(value, str) or not value:
        return value
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError:
        return value
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=LOCAL_TZ)
    else:
        parsed = parsed.astimezone(LOCAL_TZ)
    return parsed.isoformat(timespec="seconds")


def normalize_name(text: str) -> str:
    return re.sub(r"\s+", "", text.strip().lower())


def parse_pause_duration_to_deadline(duration: str) -> Optional[str]:
    text = duration.strip().lower()
    now = dt.datetime.now(tz=LOCAL_TZ)
    m = re.match(r"^(\d+)\s*(m|h|d)$", text)
    if m:
        value = int(m.group(1))
        unit = m.group(2)
        if unit == "m":
            return (now + dt.timedelta(minutes=value)).isoformat(timespec="seconds")
        if unit == "h":
            return (now + dt.timedelta(hours=value)).isoformat(timespec="seconds")
        if unit == "d":
            return (now + dt.timedelta(days=value)).isoformat(timespec="seconds")

    m_cn = re.match(r"^(\d+)\s*(分钟|小时|天)$", duration.strip())
    if m_cn:
        value = int(m_cn.group(1))
        unit = m_cn.group(2)
        if unit == "分钟":
            return (now + dt.timedelta(minutes=value)).isoformat(timespec="seconds")
        if unit == "小时":
            return (now + dt.timedelta(hours=value)).isoformat(timespec="seconds")
        if unit == "天":
            return (now + dt.timedelta(days=value)).isoformat(timespec="seconds")

    return None


def safe_file_stem(name: str) -> str:
    raw = name.strip()
    stem = raw.replace(" ", "-")
    stem = re.sub(r"[^\w\u4e00-\u9fff-]+", "", stem)
    stem = re.sub(r"-{2,}", "-", stem).strip("-_")
    if stem:
        return stem
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    return f"role-{digest}"


def short_preview(role: Dict[str, Any]) -> str:
    core = role.get("core_setting", {})
    identity = core.get("identity", {})
    return (
        f"角色：{role.get('meta', {}).get('display_name', '未命名')}\n"
        f"风格：{core.get('visual_style', '未设定')}\n"
        f"性别：{core.get('gender', '未设定')}\n"
        f"摘要：{core.get('summary', '未设定')}\n"
        f"职业：{identity.get('occupation', '未设定')}"
    )


def extract_switch_name(prompt: str) -> Optional[str]:
    m = re.search(r"(?:切换到|切到|switch to|use)\s*([A-Za-z0-9\u4e00-\u9fff_-]{1,40})", prompt, re.IGNORECASE)
    if not m:
        return None
    return m.group(1)


class CompanionRuntime:
    def __init__(self, skill_root: Path) -> None:
        self.root = skill_root.resolve()
        self.roles_dir = self.root / "roles"
        self.presets_dir = self.root / "references" / "presets"
        self.state_dir = self.root / "state"
        self.session_path = self.state_dir / "session.yaml"
        self.draft_path = self.state_dir / "draft-role.yaml"

        self.roles_dir.mkdir(parents=True, exist_ok=True)
        self.state_dir.mkdir(parents=True, exist_ok=True)

        self.session = self._load_session()
        self.last_heartbeat_sync: Optional[Dict[str, Any]] = None

    def _load_session(self) -> Dict[str, Any]:
        if not self.session_path.exists():
            return copy.deepcopy(DEFAULT_SESSION)
        data = yaml.safe_load(self.session_path.read_text(encoding="utf-8"))
        merged = copy.deepcopy(DEFAULT_SESSION)
        if isinstance(data, dict):
            self._deep_update(merged, data)
        changed = self._migrate_session(merged)
        if changed:
            self.session_path.write_text(yaml.safe_dump(merged, sort_keys=False, allow_unicode=True), encoding="utf-8")
        return merged

    def _migrate_session(self, session: Dict[str, Any]) -> bool:
        changed = False

        if session.get("schema_version") != SESSION_SCHEMA_VERSION:
            session["schema_version"] = SESSION_SCHEMA_VERSION
            changed = True

        role = session.setdefault("role", {})
        if "pending_activation" not in role:
            role["pending_activation"] = None
            changed = True

        proactive = session.setdefault("proactive", {})
        for key in ("pause_until", "last_sent_at"):
            normalized = normalize_iso_with_tz(proactive.get(key))
            if normalized != proactive.get(key):
                proactive[key] = normalized
                changed = True

        for key in ("last_user_input_at", "updated_at"):
            normalized = normalize_iso_with_tz(session.get(key))
            if normalized != session.get(key):
                session[key] = normalized
                changed = True

        return changed

    def _save_session(self, sync_heartbeat: bool = False) -> None:
        self.session["schema_version"] = SESSION_SCHEMA_VERSION
        self.session["updated_at"] = now_iso()
        self.session_path.write_text(yaml.safe_dump(self.session, sort_keys=False, allow_unicode=True), encoding="utf-8")
        if sync_heartbeat:
            self.last_heartbeat_sync = sync_heartbeat_md(skill_root=self.root, session=self.session)

    def _deep_update(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        for key, value in update.items():
            if isinstance(value, dict) and isinstance(base.get(key), dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value

    def _write_yaml(self, path: Path, data: Dict[str, Any]) -> None:
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    def _read_yaml(self, path: Path) -> Dict[str, Any]:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        return loaded if isinstance(loaded, dict) else {}

    def _ensure_initialized(self) -> None:
        if self.session.get("initialized"):
            return
        self.session["initialized"] = True
        self._save_session()

    def _list_role_sources(self) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []

        for path in sorted(self.roles_dir.glob("*.yaml")):
            role = self._read_yaml(path)
            meta = role.get("meta", {})
            identity = role.get("core_setting", {}).get("identity", {})
            out.append(
                {
                    "kind": "role",
                    "path": path,
                    "name": meta.get("display_name", path.stem),
                    "id": meta.get("id", path.stem),
                    "nickname": identity.get("nickname"),
                }
            )

        for path in sorted(self.presets_dir.glob("*.yaml")):
            role = self._read_yaml(path)
            meta = role.get("meta", {})
            identity = role.get("core_setting", {}).get("identity", {})
            out.append(
                {
                    "kind": "preset",
                    "path": path,
                    "name": meta.get("display_name", path.stem),
                    "id": meta.get("id", path.stem),
                    "nickname": identity.get("nickname"),
                }
            )
        return out

    def _resolve_role_by_name(self, query: str) -> Optional[Dict[str, Any]]:
        query_norm = normalize_name(query)
        for item in self._list_role_sources():
            candidates = {
                normalize_name(str(item["name"])),
                normalize_name(str(item["id"])),
                normalize_name(item["path"].stem),
            }
            nickname = item.get("nickname")
            if nickname:
                candidates.add(normalize_name(str(nickname)))
            if query_norm in candidates:
                return item
        return None

    def _draft_exists(self) -> bool:
        return self.draft_path.exists()

    def _load_active_role(self) -> Optional[Dict[str, Any]]:
        active = self.session.get("role", {}).get("active")
        if not active:
            return None
        path = (self.root / active).resolve()
        if not path.exists():
            return None
        return self._read_yaml(path)

    def _safe_role_target(self, name: str) -> Path:
        stem = safe_file_stem(name)
        candidate = self.roles_dir / f"{stem}.yaml"
        if not candidate.exists():
            return candidate
        idx = 2
        while True:
            new_candidate = self.roles_dir / f"{stem}-{idx}.yaml"
            if not new_candidate.exists():
                return new_candidate
            idx += 1

    def _role_requires_consent(self, role: Dict[str, Any]) -> bool:
        label = role.get("core_setting", {}).get("identity", {}).get("relationship_label")
        if label not in ROMANTIC_LABELS:
            return False
        return True

    def _role_consent_granted(self, role: Dict[str, Any]) -> bool:
        consent = role.get("meta", {}).get("consent", {})
        if not isinstance(consent, dict):
            return False
        return consent.get("granted") is True

    def _help_text(self) -> str:
        return (
            "可用命令：\n"
            "/hi, /hi 状态, /hi 开, /hi 关, /hi 频率 低|中|高\n"
            "/hi 角色 新建 <描述>, /hi 角色 预览, /hi 角色 保存 <名称>\n"
            "/hi 角色 切换 <名称>, /hi 角色 列表, /hi 角色 模板 luoshui\n"
            "/hi 角色 确认  # 对需要同意闸门的角色执行启用确认"
        )

    def _status_text(self) -> str:
        role_cfg = self.session.get("role", {})
        proactive = self.session.get("proactive", {})
        context = self.session.get("context", {})
        return (
            "当前配置：\n"
            f"- 初始化：{'是' if self.session.get('initialized') else '否'}\n"
            f"- 主动触达：{'开' if proactive.get('enabled') else '关'}\n"
            f"- 频率：{proactive.get('frequency')}\n"
            f"- 免打扰：{proactive.get('quiet_hours') or '未设置'}\n"
            f"- 暂停至：{proactive.get('pause_until') or '未暂停'}\n"
            f"- 上次主动触达：{proactive.get('last_sent_at') or '无'}\n"
            f"- 上下文窗口：{context.get('freshness_hours')}h\n"
            f"- 当前角色：{role_cfg.get('active') or '未选择'}\n"
            f"- 草稿角色：{role_cfg.get('draft') or '无'}\n"
            f"- 待确认启用：{role_cfg.get('pending_activation') or '无'}\n"
            f"- 上次用户输入：{self.session.get('last_user_input_at') or '无'}"
        )

    def _apply_nl_role_edit(self, role: Dict[str, Any], prompt: str) -> List[str]:
        changed: List[str] = []
        speech = role.setdefault("speech_style", {})
        core = role.setdefault("core_setting", {})
        traits = role.setdefault("persona_background", {}).setdefault("personality_traits", [])

        if "理性" in prompt:
            speech["tone"] = "更理性、克制、结构化"
            if "理性" not in traits:
                traits.append("理性")
            changed.append("speech_style.tone")

        if "少用表情" in prompt or "表情少" in prompt:
            speech["emoji_level"] = 0
            changed.append("speech_style.emoji_level")
        elif "多用表情" in prompt or "活泼一点" in prompt:
            speech["emoji_level"] = 2
            changed.append("speech_style.emoji_level")

        low = prompt.lower()
        if "动漫" in prompt or "anime" in low:
            core["visual_style"] = "anime"
            changed.append("core_setting.visual_style")
        if "写实" in prompt or "realistic" in low:
            core["visual_style"] = "realistic"
            changed.append("core_setting.visual_style")

        return list(dict.fromkeys(changed))

    def _apply_command_role_edit(self, role: Dict[str, Any], field: str, value: str) -> List[str]:
        changed: List[str] = []
        field_low = field.lower()
        speech = role.setdefault("speech_style", {})
        core = role.setdefault("core_setting", {})
        identity = core.setdefault("identity", {})

        if field_low in {"语气", "tone"}:
            speech["tone"] = value
            changed.append("speech_style.tone")
        elif field_low in {"表情", "emoji", "emoji_level"}:
            v = value.strip().lower()
            if v in {"0", "无", "少", "low"}:
                speech["emoji_level"] = 0
            elif v in {"2", "多", "high"}:
                speech["emoji_level"] = 2
            else:
                speech["emoji_level"] = 1
            changed.append("speech_style.emoji_level")
        elif field_low in {"风格", "style"}:
            vv = value.lower()
            if "动漫" in value or "anime" in vv:
                core["visual_style"] = "anime"
            elif "写实" in value or "realistic" in vv:
                core["visual_style"] = "realistic"
            changed.append("core_setting.visual_style")
        elif field_low in {"职业", "occupation"}:
            identity["occupation"] = value
            changed.append("core_setting.identity.occupation")
        elif field_low in {"摘要", "summary", "设定"}:
            core["summary"] = value
            changed.append("core_setting.summary")
        return changed

    def _save_draft_as_role(self, name: str) -> Tuple[bool, str]:
        if not self._draft_exists():
            return False, "当前没有草稿角色，请先创建或套用模板。"

        role = self._read_yaml(self.draft_path)
        meta = role.setdefault("meta", {})
        meta["display_name"] = name
        meta["id"] = slugify(name)
        meta["template_only"] = False
        consent = meta.setdefault("consent", {})
        consent["required"] = self._role_requires_consent(role)
        consent.setdefault("granted", False)
        consent.setdefault("granted_at", None)

        target = self._safe_role_target(name)
        self._write_yaml(target, role)
        errors = validate_file(target)
        if errors:
            target.unlink(missing_ok=True)
            return False, "保存失败，角色结构校验未通过：" + "; ".join(errors)

        rel = target.relative_to(self.root).as_posix()
        self.session["role"]["pending_activation"] = rel
        if self._role_requires_consent(role):
            reply = (
                f"已保存角色：{name}\n路径：{rel}\n"
                "该角色包含亲密关系标签，启用前需要你明确确认。\n"
                "请输入 `/hi 角色 确认` 完成启用。"
            )
        else:
            reply = (
                f"已保存角色：{name}\n路径：{rel}\n"
                "该角色尚未启用。请输入 `/hi 角色 确认` 启用，"
                "或用 `/hi 角色 切换 <名称>` 手动切换。"
            )

        self.session["role"]["draft"] = None
        self.draft_path.unlink(missing_ok=True)
        self._save_session()
        return True, reply

    def _confirm_pending_activation(self) -> Tuple[bool, str]:
        pending_rel = self.session.get("role", {}).get("pending_activation")
        if not pending_rel:
            return False, "当前没有待确认启用的角色。"

        pending_path = (self.root / pending_rel).resolve()
        if not pending_path.exists():
            self.session["role"]["pending_activation"] = None
            self._save_session()
            return False, "待确认角色文件不存在，已清理待确认状态。"

        role = self._read_yaml(pending_path)
        meta = role.setdefault("meta", {})
        consent = meta.setdefault("consent", {})
        consent["required"] = True
        consent["granted"] = True
        consent["granted_at"] = now_iso()
        self._write_yaml(pending_path, role)

        errors = validate_file(pending_path)
        if errors:
            return False, "确认失败，角色校验未通过：" + "; ".join(errors)

        self.session["role"]["active"] = pending_rel
        self.session["role"]["pending_activation"] = None
        self._save_session(sync_heartbeat=True)
        display_name = meta.get("display_name", pending_path.stem)
        return True, f"已确认并启用角色：{display_name}"

    def handle(self, text: str) -> Dict[str, Any]:
        intent_obj = normalize_input(text)
        intent = intent_obj.get("intent", "casual_companion_chat")
        args = intent_obj.get("args", {})
        self.last_heartbeat_sync = None

        self._ensure_initialized()
        self.session["last_user_input_at"] = now_iso()
        self.session["role"]["draft"] = self.draft_path.relative_to(self.root).as_posix() if self._draft_exists() else None

        reply = ""
        actions: List[str] = []

        if intent == "help":
            reply = self._help_text()

        elif intent == "init_config":
            self.session = copy.deepcopy(DEFAULT_SESSION)
            self.session["initialized"] = True
            self._save_session(sync_heartbeat=True)
            reply = (
                "初始化完成：主动触达=关，上下文窗口=72h。\n"
                "你可以直接说“帮我创建一个动漫风格的新角色，她是一个喜欢画画的大学生”。"
            )

        elif intent == "status_query":
            reply = self._status_text()

        elif intent == "config_proactive_on":
            self.session["proactive"]["enabled"] = True
            self._save_session(sync_heartbeat=True)
            reply = "已开启主动触达。"
            actions.append("config_updated")

        elif intent == "config_proactive_off":
            self.session["proactive"]["enabled"] = False
            self._save_session(sync_heartbeat=True)
            reply = "已关闭主动触达。"
            actions.append("config_updated")

        elif intent == "config_frequency":
            freq = args.get("frequency", "mid")
            self.session["proactive"]["frequency"] = freq
            self._save_session(sync_heartbeat=True)
            reply = f"已设置频率为：{freq}"
            actions.append("config_updated")

        elif intent == "config_quiet_hours":
            self.session["proactive"]["quiet_hours"] = args.get("range")
            self._save_session(sync_heartbeat=True)
            reply = f"已设置免打扰时段：{args.get('range')}"
            actions.append("config_updated")

        elif intent == "config_pause":
            raw_duration = str(args.get("duration", "")).strip()
            deadline = parse_pause_duration_to_deadline(raw_duration)
            if not deadline:
                reply = "暂停时长格式不正确，请用例如 `30m`、`4h`、`2d` 或 `2小时`。"
            else:
                self.session["proactive"]["pause_until"] = deadline
                self._save_session(sync_heartbeat=True)
                reply = f"已暂停主动触达到：{deadline}"
                actions.append("config_updated")

        elif intent == "config_reset":
            self.session = copy.deepcopy(DEFAULT_SESSION)
            self.session["initialized"] = True
            self._save_session(sync_heartbeat=True)
            self.draft_path.unlink(missing_ok=True)
            reply = "已重置配置，主动触达=关，上下文窗口=72h。"
            actions.append("config_reset")

        elif intent == "role_list":
            items = self._list_role_sources()
            if not items:
                reply = "目前还没有可用角色。"
            else:
                lines = ["可用角色："]
                for item in items:
                    tag = "模板" if item["kind"] == "preset" else "角色"
                    lines.append(f"- [{tag}] {item['name']} ({item['id']})")
                reply = "\n".join(lines)

        elif intent == "role_current":
            reply = (
                f"当前角色：{self.session['role'].get('active') or '未选择'}\n"
                f"草稿角色：{self.session['role'].get('draft') or '无'}\n"
                f"待确认启用：{self.session['role'].get('pending_activation') or '无'}"
            )

        elif intent == "role_template_apply":
            template = str(args.get("template", "")).lower()
            if template in {"luoshui", "洛水", "阿洛", "luoshui-v1"}:
                preset = self.presets_dir / "luoshui-v1.yaml"
                if not preset.exists():
                    reply = "未找到 luoshui 模板文件。"
                else:
                    role = self._read_yaml(preset)
                    self._write_yaml(self.draft_path, role)
                    self.session["role"]["draft"] = self.draft_path.relative_to(self.root).as_posix()
                    self._save_session()
                    reply = "已加载洛水（阿洛）模板为草稿。\n" + short_preview(role) + "\n可用“/hi 角色 保存 洛水”保存。"
                    actions.append("draft_updated")
            else:
                reply = f"未识别模板：{template}"

        elif intent == "role_create":
            prompt = args.get("prompt", text)
            role = build_rolecard(name="新角色", prompt=prompt)
            self._write_yaml(self.draft_path, role)
            errors = validate_file(self.draft_path)
            if errors:
                reply = "角色草稿创建失败：" + "; ".join(errors)
            else:
                self.session["role"]["draft"] = self.draft_path.relative_to(self.root).as_posix()
                self._save_session()
                reply = "已创建角色草稿：\n" + short_preview(role) + "\n可说“保存为小溪”或“/hi 角色 保存 小溪”。"
                actions.append("draft_updated")

        elif intent == "role_preview":
            if not self._draft_exists():
                reply = "当前没有角色草稿。"
            else:
                role = self._read_yaml(self.draft_path)
                reply = "当前草稿预览：\n" + short_preview(role)

        elif intent == "role_save":
            name = args.get("name", "新角色")
            ok, msg = self._save_draft_as_role(name)
            reply = msg
            if ok:
                actions.append("role_saved")

        elif intent == "role_confirm_activation":
            ok, msg = self._confirm_pending_activation()
            reply = msg
            if ok:
                actions.append("role_confirmed")

        elif intent == "role_switch":
            name = args.get("name")
            if not name and "prompt" in args:
                name = extract_switch_name(args.get("prompt", ""))
            if not name:
                reply = "请提供要切换的角色名，例如：/hi 角色 切换 洛水"
            else:
                resolved = self._resolve_role_by_name(name)
                if not resolved:
                    reply = f"未找到角色：{name}"
                elif resolved["kind"] == "preset":
                    role = self._read_yaml(resolved["path"])
                    self._write_yaml(self.draft_path, role)
                    self.session["role"]["draft"] = self.draft_path.relative_to(self.root).as_posix()
                    self._save_session()
                    reply = f"已加载模板 {resolved['name']} 为草稿。\n可先预览，再保存为你的角色。"
                    actions.append("draft_updated")
                else:
                    rel = resolved["path"].relative_to(self.root).as_posix()
                    role = self._read_yaml(resolved["path"])
                    if self._role_requires_consent(role) and not self._role_consent_granted(role):
                        self.session["role"]["pending_activation"] = rel
                        self._save_session()
                        reply = (
                            f"角色 {resolved['name']} 需要你确认后才会启用。\n"
                            "请输入 `/hi 角色 确认` 完成启用。"
                        )
                    else:
                        self.session["role"]["active"] = rel
                        self.session["role"]["pending_activation"] = None
                        self._save_session(sync_heartbeat=True)
                        reply = f"已切换到角色：{resolved['name']}"
                        actions.append("role_switched")

        elif intent == "role_edit":
            target: Optional[Path] = None
            if self._draft_exists():
                target = self.draft_path
            elif self.session["role"].get("active"):
                target = (self.root / self.session["role"]["active"]).resolve()

            if not target or not target.exists():
                reply = "没有可编辑的角色。请先创建草稿或切换到一个已保存角色。"
            else:
                role = self._read_yaml(target)
                before = yaml.safe_dump(role, sort_keys=False, allow_unicode=True)

                changed: List[str] = []
                if "field" in args and "value" in args:
                    changed = self._apply_command_role_edit(role, args["field"], args["value"])
                else:
                    changed = self._apply_nl_role_edit(role, args.get("prompt", text))

                if not changed:
                    reply = "没有识别到可执行的修改，请更具体一点。"
                else:
                    self._write_yaml(target, role)
                    errors = validate_file(target)
                    if errors:
                        target.write_text(before, encoding="utf-8")
                        reply = "修改失败，角色校验未通过：" + "; ".join(errors)
                    else:
                        reply = "已更新角色：\n- " + "\n- ".join(changed) + "\n\n" + short_preview(role)
                        actions.append("role_edited")
                        if target == self.draft_path:
                            self.session["role"]["draft"] = self.draft_path.relative_to(self.root).as_posix()
                            self._save_session()

        elif intent == "greeting_checkin":
            role = self._load_active_role()
            if role:
                name = role.get("meta", {}).get("display_name", "伙伴")
                reply = f"嗨，我是{name}。今天你想先聊一会儿，还是直接开始做事？"
            else:
                reply = "嗨，欢迎回来。要不要先创建一个专属角色？你可以直接描述，我来帮你生成。"

        elif intent == "invalid":
            reply = "没识别这条命令，试试 /hi 帮助"

        else:
            role = self._load_active_role()
            if role:
                reply = "我在这儿。你想先调整角色设定，还是先聊聊你现在最在意的事？"
            else:
                reply = "我在。你可以先说“帮我创建一个动漫风格的新角色，她是一个喜欢画画的大学生”。"

        self._save_session()
        return {
            "intent": intent,
            "args": args,
            "reply": reply,
            "actions": actions,
            "session": self.session,
            "heartbeat_sync": self.last_heartbeat_sync,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Companion runtime for say-hi-to-me skill")
    parser.add_argument("--text", required=True, help="User input text")
    parser.add_argument("--skill-root", help="Skill root path; default is script parent folder")
    parser.add_argument("--json", action="store_true", help="Print full JSON result")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.skill_root).resolve() if args.skill_root else Path(__file__).resolve().parents[1]
    runtime = CompanionRuntime(root)
    result = runtime.handle(args.text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["reply"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
