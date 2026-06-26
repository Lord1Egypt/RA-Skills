#!/usr/bin/env python3
"""Common helpers for sticker-manager."""
import json
import os
from typing import Dict, List, Tuple

DEFAULT_TARGET_DIR = "~/.openclaw/workspace/stickers/library/"
DEFAULT_INBOUND_DIR = "~/.openclaw/media/inbound/"
DEFAULT_LANG = "auto"
DEFAULT_VISION_MODELS = "bailian/kimi-k2.5,openai/gpt-5-mini"
SUPPORTED_EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
SUPPORTED_GLOBS = ('*.jpg', '*.jpeg', '*.png', '*.webp', '*.gif')

MESSAGES: Dict[str, Dict[str, str]] = {
    "library_not_found": {"zh": "表情包目录不存在: {path}", "en": "Sticker library not found: {path}"},
    "library_empty": {"zh": "表情包库为空", "en": "Sticker library is empty"},
    "sticker_not_found": {"zh": "未找到 '{keyword}'。可用表情包: {available}...", "en": "No sticker found for '{keyword}'. Available stickers: {available}..."},
    "inventory_title": {"zh": "📦 表情包库:", "en": "📦 Sticker library:"},
    "usage_semantic": {"zh": "用法:\n  {cmd} tag <name> <emotions> <scenes> <keywords> [description]\n  {cmd} suggest <context> [--strategy auto|model|rules]\n  {cmd} prepare-model <context>\n  {cmd} vision-plan <image_path> [context]\n  {cmd} list", "en": "Usage:\n  {cmd} tag <name> <emotions> <scenes> <keywords> [description]\n  {cmd} suggest <context> [--strategy auto|model|rules]\n  {cmd} prepare-model <context>\n  {cmd} vision-plan <image_path> [context]\n  {cmd} list"},
    "tag_added": {"zh": "✅ 已添加标签: {name}\n   情绪: {emotions}\n   场景: {scenes}\n   关键词: {keywords}{description_line}", "en": "✅ Tags saved: {name}\n   emotions: {emotions}\n   scenes: {scenes}\n   keywords: {keywords}{description_line}"},
    "description_line": {"zh": "\n   描述: {description}", "en": "\n   description: {description}"},
    "recommendation": {"zh": "🦀 推荐: {name} (匹配度:{score}, 原因:{reasons})", "en": "🦀 Recommended: {name} (score:{score}, reasons:{reasons})"},
    "no_match": {"zh": "未找到匹配的表情包", "en": "No matching sticker found"},
    "tags_empty": {"zh": "标签库为空", "en": "Tag database is empty"},
    "tags_title": {"zh": "📦 表情包标签库:", "en": "📦 Sticker tag database:"},
    "unknown_action": {"zh": "未知操作", "en": "Unknown action"},
    "delete_success": {"zh": "已删除: {name}", "en": "Deleted: {name}"},
    "delete_missing": {"zh": "表情包不存在: {name}", "en": "Sticker not found: {name}"},
    "rename_missing": {"zh": "原表情包不存在: {name}", "en": "Original sticker not found: {name}"},
    "rename_exists": {"zh": "目标文件名已存在: {name}", "en": "Target filename already exists: {name}"},
    "rename_success": {"zh": "已重命名: {old} → {new}", "en": "Renamed: {old} → {new}"},
    "clean_none": {"zh": "没有低质量表情包需要清理", "en": "No low-quality stickers need cleanup"},
    "clean_summary": {"zh": "已清理 {count} 个低质量表情包:", "en": "Removed {count} low-quality stickers:"},
    "save_missing_inbound": {"zh": "inbound 目录不存在", "en": "Inbound directory does not exist"},
    "save_no_media": {"zh": "没有找到新图片或 GIF", "en": "No new image or GIF found"},
    "save_exists": {"zh": "文件已存在: {name}", "en": "File already exists: {name}"},
    "save_success": {"zh": "已保存: {name} ({size_kb}KB)", "en": "Saved: {name} ({size_kb}KB)"},
    "source_not_found": {"zh": "未找到可保存的来源媒体: {source}", "en": "Could not find the requested source media: {source}"},
    "history_empty": {"zh": "历史媒体为空，无法从聊天记录保存图片", "en": "No media found in recent history; cannot save from chat history"},
    "history_list_title": {"zh": "🕘 最近媒体:", "en": "🕘 Recent media:"},
    "quality_reject": {"zh": "❌ 图片质量不足，建议放弃保存\n原因：{reason}\n\n如仍要保存，请使用：保存为 [名称] --force", "en": "❌ Media quality is too low and saving is not recommended\nReason: {reason}\n\nIf you still want to save it, run: save as [name] --force"},
    "save_auto_success": {"zh": "{badge} 已保存: {name} ({size_kb}KB, 质量{score}/100)", "en": "{badge} Saved: {name} ({size_kb}KB, quality {score}/100)"},
    "quality_reason_too_small": {"zh": "文件太小 ({size}B)，可能是缩略图或低质量图片", "en": "File is too small ({size}B); it may be a thumbnail or low-quality image"},
    "quality_reason_small": {"zh": "文件较小 ({size_kb}KB)，建议找更高清版本", "en": "File is small ({size_kb}KB); consider finding a higher-quality version"},
    "unsupported_format": {"zh": "不支持的图片格式: {ext}", "en": "Unsupported media format: {ext}"},
    "vision_failure": {"zh": "未能成功识别图片语义，当前无法自动解释图片含义，也无法可靠校验图像质量或生成情绪标签。已尝试模型: {models}", "en": "Failed to interpret the image semantically. Automatic meaning extraction, reliable quality validation, and emotion tagging are unavailable. Models tried: {models}"},
}


def get_target_dir() -> str:
    return os.path.expanduser(os.environ.get('STICKER_MANAGER_DIR', DEFAULT_TARGET_DIR))


def get_inbound_dir() -> str:
    return os.path.expanduser(os.environ.get('STICKER_MANAGER_INBOUND_DIR', DEFAULT_INBOUND_DIR))


def get_lang(value: str | None = None) -> str:
    raw = (value or os.environ.get('STICKER_MANAGER_LANG') or DEFAULT_LANG).lower()
    if raw in ('zh', 'zh-cn', 'cn', 'chinese'):
        return 'zh'
    if raw in ('en', 'en-us', 'en-gb', 'english'):
        return 'en'
    if raw == 'auto':
        lang_env = os.environ.get('LANG', '').lower()
        if 'zh' in lang_env:
            return 'zh'
    return 'en'


def t(key: str, lang: str | None = None, **kwargs) -> str:
    chosen = get_lang(lang)
    entry = MESSAGES.get(key, {})
    template = entry.get(chosen) or entry.get('en') or key
    return template.format(**kwargs)


def has_supported_ext(name: str) -> bool:
    return os.path.splitext(name)[1].lower() in SUPPORTED_EXTS


def list_media_files(base_dir: str | None = None) -> List[Tuple[str, float, int]]:
    directory = base_dir or get_inbound_dir()
    if not os.path.exists(directory):
        return []
    media_files = []
    for f in os.listdir(directory):
        filepath = os.path.join(directory, f)
        if os.path.isfile(filepath) and has_supported_ext(f):
            media_files.append((filepath, os.path.getmtime(filepath), os.path.getsize(filepath)))
    media_files.sort(key=lambda x: (-x[1], os.path.basename(x[0]).lower()))
    return media_files


def resolve_media_source(source: str | None = None, history_index: int | None = None, inbound_dir: str | None = None) -> str | None:
    media_files = list_media_files(inbound_dir)
    if not media_files:
        return None
    if source:
        expanded = os.path.expanduser(source)
        if os.path.isabs(expanded) and os.path.exists(expanded):
            return expanded
        for filepath, _mtime, _size in media_files:
            if os.path.basename(filepath) == source or os.path.basename(filepath).startswith(source):
                return filepath
    if history_index is not None:
        if 1 <= history_index <= len(media_files):
            return media_files[history_index - 1][0]
        return None
    return media_files[0][0]


def get_vision_models() -> List[str]:
    raw = os.environ.get('STICKER_MANAGER_VISION_MODELS', DEFAULT_VISION_MODELS)
    return [item.strip() for item in raw.split(',') if item.strip()]


def build_vision_plan(image_path: str, context: str = '', lang: str | None = None) -> Dict:
    return {
        'image_path': image_path,
        'context': context,
        'language': get_lang(lang),
        'models': get_vision_models(),
        'prompt': 'Analyze the sticker image semantically: subject, emotion, scene, whether it expresses doubt/suspicion, and whether the image quality is sufficient for sticker use.',
        'fallback_message': t('vision_failure', lang, models=', '.join(get_vision_models())),
    }


def build_vision_plan_json(image_path: str, context: str = '', lang: str | None = None) -> str:
    return json.dumps(build_vision_plan(image_path, context, lang), ensure_ascii=False, indent=2)
