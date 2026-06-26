#!/usr/bin/env python3
"""
content-engine Obsidian 笔记库集成模块

连接 Obsidian 笔记库，实现草稿导入导出和双向同步，
打通笔记到内容发布的完整工作流。
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from utils import (
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    write_json_file,
)


# ============================================================
# 常量与配置
# ============================================================

SYNC_STATE_FILE = "obsidian_sync_state.json"

# Obsidian 笔记中标识为内容草稿的标签
DRAFT_TAGS = {"#content", "#draft", "#内容", "#草稿"}

# Obsidian frontmatter 中支持的字段映射
FRONTMATTER_FIELD_MAP = {
    "title": "title",
    "标题": "title",
    "tags": "tags",
    "标签": "tags",
    "platforms": "platforms",
    "平台": "platforms",
    "author": "author",
    "作者": "author",
    "summary": "summary",
    "description": "summary",
    "摘要": "summary",
    "status": "status",
    "状态": "status",
    "ce_id": "ce_id",
    "ce_status": "ce_status",
    "ce_published_at": "ce_published_at",
}


# ============================================================
# 笔记库路径管理
# ============================================================

def _get_vault_path() -> Optional[str]:
    """获取 Obsidian 笔记库路径。

    优先读取环境变量 CE_OBSIDIAN_VAULT_PATH。

    Returns:
        笔记库路径，未配置时返回 None。
    """
    vault = os.environ.get("CE_OBSIDIAN_VAULT_PATH", "")
    if not vault:
        return None
    vault = os.path.expanduser(vault)
    if not os.path.isdir(vault):
        return None
    return vault


def _get_sync_state() -> Dict[str, Any]:
    """读取同步状态数据。"""
    filepath = get_data_file(SYNC_STATE_FILE)
    data = read_json_file(filepath)
    if isinstance(data, list):
        data = {}
    if not isinstance(data, dict):
        data = {}
    data.setdefault("vault_path", "")
    data.setdefault("synced_files", {})  # {相对路径: {ce_id, last_sync, hash}}
    data.setdefault("last_sync_at", "")
    return data


def _save_sync_state(state: Dict[str, Any]) -> None:
    """保存同步状态数据。"""
    write_json_file(get_data_file(SYNC_STATE_FILE), state)


# ============================================================
# Obsidian 格式解析
# ============================================================

def _parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """解析 Obsidian 笔记的 YAML frontmatter。

    Args:
        content: 笔记原始内容。

    Returns:
        (元数据字典, 正文内容) 的元组。
    """
    metadata: Dict[str, Any] = {}
    body = content

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if match:
        fm_str = match.group(1)
        body = match.group(2).strip()

        # 简单 YAML 解析（不依赖 pyyaml）
        current_key = ""
        current_list: Optional[List[str]] = None

        for line in fm_str.split("\n"):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            # 检测列表项（以 - 开头，属于当前 key）
            if stripped.startswith("- ") and current_key and current_list is not None:
                val = stripped[2:].strip().strip("\"'")
                current_list.append(val)
                continue

            # 键值对
            if ":" in stripped:
                idx = stripped.index(":")
                raw_key = stripped[:idx].strip().lower()
                raw_val = stripped[idx + 1:].strip()

                # 映射字段名
                mapped_key = FRONTMATTER_FIELD_MAP.get(raw_key, raw_key)

                if raw_val.startswith("[") and raw_val.endswith("]"):
                    # 行内数组
                    items = [v.strip().strip("\"'") for v in raw_val[1:-1].split(",") if v.strip()]
                    metadata[mapped_key] = items
                    current_key = ""
                    current_list = None
                elif not raw_val:
                    # 可能是多行列表的开始
                    current_key = mapped_key
                    current_list = []
                    metadata[mapped_key] = current_list
                else:
                    metadata[mapped_key] = raw_val.strip("\"'")
                    current_key = ""
                    current_list = None

    return metadata, body


def _convert_wikilinks(text: str, mode: str = "plain") -> str:
    """转换 Obsidian [[wikilinks]] 为目标格式。

    Args:
        text: 包含 wikilinks 的文本。
        mode: 转换模式:
            - "plain": 转为纯文本
            - "markdown": 转为 Markdown 链接（无实际 URL）

    Returns:
        转换后的文本。
    """
    # [[显示文本|链接目标]] 格式
    text = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", _wikilink_replace(mode), text)
    # [[链接目标]] 格式
    text = re.sub(r"\[\[([^\]]+)\]\]", _simple_wikilink_replace(mode), text)
    return text


def _wikilink_replace(mode: str):
    """返回 [[display|target]] 的替换函数。"""
    def replacer(m: re.Match) -> str:
        target = m.group(1)
        display = m.group(2)
        if mode == "markdown":
            return f"[{display}]({target})"
        return display
    return replacer


def _simple_wikilink_replace(mode: str):
    """返回 [[target]] 的替换函数。"""
    def replacer(m: re.Match) -> str:
        target = m.group(1)
        if mode == "markdown":
            return f"[{target}]({target})"
        return target
    return replacer


def _extract_tags_from_body(text: str) -> List[str]:
    """从正文中提取 Obsidian #tags。

    Args:
        text: 笔记正文。

    Returns:
        标签列表（不含 # 前缀）。
    """
    # 匹配 #tag 格式，排除标题中的 #
    tags = re.findall(r"(?:^|\s)#([a-zA-Z\u4e00-\u9fff][\w\u4e00-\u9fff/-]*)", text)
    return list(dict.fromkeys(tags))  # 去重保序


def _simple_hash(content: str) -> str:
    """计算内容的简单哈希值（用于变更检测）。

    Args:
        content: 文本内容。

    Returns:
        哈希字符串。
    """
    # 使用简单的字符串哈希（避免依赖 hashlib 以外的库）
    h = 0
    for ch in content:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return format(h, "08x")


def _build_frontmatter(metadata: Dict[str, Any]) -> str:
    """构建 YAML frontmatter 字符串。

    Args:
        metadata: 元数据字典。

    Returns:
        包含 --- 分隔符的 frontmatter 字符串。
    """
    lines = ["---"]
    for key, value in metadata.items():
        if isinstance(value, list):
            if value:
                items_str = ", ".join(f'"{v}"' for v in value)
                lines.append(f"{key}: [{items_str}]")
        elif value:
            lines.append(f'{key}: "{value}"')
    lines.append("---")
    return "\n".join(lines)


# ============================================================
# 操作：连接笔记库
# ============================================================

def connect(data: Dict[str, Any]) -> None:
    """连接到 Obsidian 笔记库。

    可选字段: vault_path（笔记库路径，优先使用 CE_OBSIDIAN_VAULT_PATH 环境变量）

    Args:
        data: 包含可选笔记库路径的字典。
    """
    vault_path = data.get("vault_path") or _get_vault_path()
    if not vault_path:
        output_error(
            "未指定 Obsidian 笔记库路径。请设置环境变量 CE_OBSIDIAN_VAULT_PATH "
            "或通过 vault_path 参数指定。",
            code="CONFIG_ERROR",
        )
        return

    vault_path = os.path.expanduser(vault_path)

    if not os.path.isdir(vault_path):
        output_error(f"笔记库路径不存在: {vault_path}", code="PATH_NOT_FOUND")
        return

    # 扫描笔记库概况
    md_count = 0
    draft_count = 0
    for root, _dirs, files in os.walk(vault_path):
        for f in files:
            if f.endswith(".md"):
                md_count += 1
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, "r", encoding="utf-8") as fp:
                        content = fp.read(2000)  # 只读前 2000 字符检查标签
                    if _is_draft_note(content):
                        draft_count += 1
                except (IOError, UnicodeDecodeError):
                    continue

    # 保存连接状态
    state = _get_sync_state()
    state["vault_path"] = vault_path
    _save_sync_state(state)

    output_success({
        "message": f"已连接到 Obsidian 笔记库: {vault_path}",
        "vault_path": vault_path,
        "total_notes": md_count,
        "draft_notes": draft_count,
    })


def _is_draft_note(content: str) -> bool:
    """检查笔记内容是否标记为草稿。

    Args:
        content: 笔记内容（可以是部分内容）。

    Returns:
        True 表示是草稿笔记。
    """
    content_lower = content.lower()
    for tag in DRAFT_TAGS:
        if tag.lower() in content_lower:
            return True

    # 检查 frontmatter 中的标签
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if match:
        fm = match.group(1).lower()
        if "content" in fm or "draft" in fm or "草稿" in fm or "内容" in fm:
            return True

    return False


# ============================================================
# 操作：列出草稿
# ============================================================

def list_drafts(data: Optional[Dict[str, Any]] = None) -> None:
    """列出 Obsidian 笔记库中的草稿笔记。

    可选字段: vault_path

    Args:
        data: 可选的配置字典。
    """
    vault_path = (data.get("vault_path") if data else None) or _get_vault_path()
    if not vault_path:
        # 尝试从同步状态读取
        state = _get_sync_state()
        vault_path = state.get("vault_path")

    if not vault_path or not os.path.isdir(vault_path):
        output_error("未连接到 Obsidian 笔记库，请先执行 connect 操作", code="NOT_CONNECTED")
        return

    drafts = []
    for root, _dirs, files in os.walk(vault_path):
        for f in files:
            if not f.endswith(".md"):
                continue
            fpath = os.path.join(root, f)
            try:
                with open(fpath, "r", encoding="utf-8") as fp:
                    content = fp.read()
            except (IOError, UnicodeDecodeError):
                continue

            if not _is_draft_note(content):
                continue

            metadata, body = _parse_frontmatter(content)
            rel_path = os.path.relpath(fpath, vault_path)
            title = metadata.get("title", "")
            if not title:
                # 从文件名或 H1 标题获取
                h1_match = re.match(r"^#\s+(.+)$", body, re.MULTILINE)
                if h1_match:
                    title = h1_match.group(1).strip()
                else:
                    title = os.path.splitext(f)[0]

            tags = metadata.get("tags", [])
            body_tags = _extract_tags_from_body(body)
            all_tags = list(dict.fromkeys(tags + body_tags))

            drafts.append({
                "file": rel_path,
                "title": title,
                "tags": all_tags,
                "platforms": metadata.get("platforms", []),
                "status": metadata.get("ce_status", "未导入"),
                "ce_id": metadata.get("ce_id", ""),
                "char_count": len(body),
                "modified": _file_mtime(fpath),
            })

    # 按修改时间倒序
    drafts.sort(key=lambda d: d.get("modified", ""), reverse=True)

    output_success({
        "message": f"找到 {len(drafts)} 篇草稿笔记",
        "vault_path": vault_path,
        "drafts": drafts,
    })


def _file_mtime(filepath: str) -> str:
    """获取文件修改时间的 ISO 格式字符串。

    Args:
        filepath: 文件路径。

    Returns:
        ISO 格式时间字符串。
    """
    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%S")
    except OSError:
        return ""


# ============================================================
# 操作：导入草稿
# ============================================================

def import_draft(data: Dict[str, Any]) -> None:
    """从 Obsidian 笔记库导入一篇笔记作为内容草稿。

    必填字段: file（笔记在库中的相对路径）
    可选字段: vault_path

    解析 frontmatter 中的 title, tags, platforms 等字段。
    转换 [[wikilinks]] 为纯文本，提取 #tags 为内容标签。

    Args:
        data: 包含文件路径的字典。
    """
    file_rel = data.get("file", "")
    if not file_rel:
        output_error("笔记文件路径（file）为必填字段", code="VALIDATION_ERROR")
        return

    vault_path = data.get("vault_path") or _get_vault_path()
    if not vault_path:
        state = _get_sync_state()
        vault_path = state.get("vault_path")

    if not vault_path or not os.path.isdir(vault_path):
        output_error("未连接到 Obsidian 笔记库，请先执行 connect 操作", code="NOT_CONNECTED")
        return

    fpath = os.path.join(vault_path, file_rel)
    if not os.path.exists(fpath):
        output_error(f"笔记文件不存在: {file_rel}", code="FILE_NOT_FOUND")
        return

    try:
        with open(fpath, "r", encoding="utf-8") as f:
            raw_content = f.read()
    except (IOError, UnicodeDecodeError) as e:
        output_error(f"读取笔记失败: {e}", code="FILE_ERROR")
        return

    # 解析元数据和正文
    metadata, body = _parse_frontmatter(raw_content)

    # 转换 wikilinks
    body = _convert_wikilinks(body, "plain")

    # 提取标签
    fm_tags = metadata.get("tags", [])
    if isinstance(fm_tags, str):
        fm_tags = [t.strip() for t in fm_tags.split(",") if t.strip()]
    body_tags = _extract_tags_from_body(body)
    all_tags = list(dict.fromkeys(fm_tags + body_tags))
    # 移除草稿标记标签
    all_tags = [t for t in all_tags if t.lower() not in {"content", "draft", "内容", "草稿"}]

    # 从正文中移除 #tag（已提取到 tags 字段）
    body = re.sub(r"(?:^|\s)#([a-zA-Z\u4e00-\u9fff][\w\u4e00-\u9fff/-]*)", " ", body).strip()

    # 获取标题
    title = metadata.get("title", "")
    if not title:
        h1_match = re.match(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
            # 从正文中移除 H1 标题行
            body = re.sub(r"^#\s+.+\n*", "", body, count=1).strip()
        else:
            title = os.path.splitext(os.path.basename(file_rel))[0]

    # 平台列表
    platforms = metadata.get("platforms", [])
    if isinstance(platforms, str):
        platforms = [p.strip() for p in platforms.split(",") if p.strip()]

    # 构建导入结果
    content_data = {
        "title": title,
        "body": body,
        "summary": metadata.get("summary", ""),
        "tags": all_tags,
        "platforms": platforms,
        "author": metadata.get("author", ""),
        "source": "obsidian",
        "source_file": file_rel,
    }

    # 更新同步状态
    state = _get_sync_state()
    state["synced_files"][file_rel] = {
        "last_sync": now_iso(),
        "hash": _simple_hash(raw_content),
        "direction": "import",
    }
    state["last_sync_at"] = now_iso()
    _save_sync_state(state)

    output_success({
        "message": f"已从 Obsidian 导入笔记「{title}」",
        "content": content_data,
        "source_file": file_rel,
        "note": "请使用 content_store.py --action create 创建内容，并将上述数据作为参数传入",
    })


# ============================================================
# 操作：导出草稿
# ============================================================

def export_draft(data: Dict[str, Any]) -> None:
    """将内容导出回 Obsidian 笔记库。

    必填字段: title, body
    可选字段: file（目标文件相对路径）, vault_path, tags, platforms,
              author, summary, ce_id, ce_status, ce_published_at

    生成带 frontmatter 的 .md 文件。

    Args:
        data: 包含内容数据的字典。
    """
    title = data.get("title", "")
    body = data.get("body", "")

    if not title:
        output_error("标题（title）为必填字段", code="VALIDATION_ERROR")
        return
    if not body:
        output_error("正文（body）为必填字段", code="VALIDATION_ERROR")
        return

    vault_path = data.get("vault_path") or _get_vault_path()
    if not vault_path:
        state = _get_sync_state()
        vault_path = state.get("vault_path")

    if not vault_path or not os.path.isdir(vault_path):
        output_error("未连接到 Obsidian 笔记库，请先执行 connect 操作", code="NOT_CONNECTED")
        return

    # 确定目标文件路径
    file_rel = data.get("file", "")
    if not file_rel:
        # 自动生成文件名
        safe_title = re.sub(r"[^\w\u4e00-\u9fff-]", "-", title)
        safe_title = re.sub(r"-+", "-", safe_title).strip("-")
        file_rel = f"{safe_title}.md"

    fpath = os.path.join(vault_path, file_rel)

    # 构建 frontmatter
    fm_data = {"title": title}
    if data.get("tags"):
        tags = data["tags"]
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        fm_data["tags"] = tags
    if data.get("platforms"):
        platforms = data["platforms"]
        if isinstance(platforms, str):
            platforms = [p.strip() for p in platforms.split(",") if p.strip()]
        fm_data["platforms"] = platforms
    if data.get("author"):
        fm_data["author"] = data["author"]
    if data.get("summary"):
        fm_data["summary"] = data["summary"]
    if data.get("ce_id"):
        fm_data["ce_id"] = data["ce_id"]
    if data.get("ce_status"):
        fm_data["ce_status"] = data["ce_status"]
    if data.get("ce_published_at"):
        fm_data["ce_published_at"] = data["ce_published_at"]

    frontmatter = _build_frontmatter(fm_data)
    full_content = frontmatter + "\n\n" + body

    # 写入文件
    try:
        os.makedirs(os.path.dirname(fpath) if os.path.dirname(fpath) != "" else fpath, exist_ok=True)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(full_content)
    except IOError as e:
        output_error(f"写入笔记失败: {e}", code="FILE_ERROR")
        return

    # 更新同步状态
    state = _get_sync_state()
    state["synced_files"][file_rel] = {
        "last_sync": now_iso(),
        "hash": _simple_hash(full_content),
        "direction": "export",
        "ce_id": data.get("ce_id", ""),
    }
    state["last_sync_at"] = now_iso()
    _save_sync_state(state)

    output_success({
        "message": f"已导出内容到 Obsidian: {file_rel}",
        "file": file_rel,
        "vault_path": vault_path,
        "full_path": fpath,
    })


# ============================================================
# 操作：双向同步
# ============================================================

def sync(data: Optional[Dict[str, Any]] = None) -> None:
    """Obsidian 笔记库双向同步。

    检测笔记库中的变更，导入新草稿，更新已发布内容的状态。

    可选字段: vault_path, dry_run（仅检测不执行）

    Args:
        data: 可选的配置字典。
    """
    vault_path = (data.get("vault_path") if data else None) or _get_vault_path()
    if not vault_path:
        state = _get_sync_state()
        vault_path = state.get("vault_path")

    if not vault_path or not os.path.isdir(vault_path):
        output_error("未连接到 Obsidian 笔记库，请先执行 connect 操作", code="NOT_CONNECTED")
        return

    dry_run = data.get("dry_run", False) if data else False
    state = _get_sync_state()

    new_drafts = []      # 新发现的草稿
    modified = []        # 已同步但有变更的文件
    unchanged = []       # 未变更的文件

    # 扫描笔记库
    for root, _dirs, files in os.walk(vault_path):
        for f in files:
            if not f.endswith(".md"):
                continue
            fpath = os.path.join(root, f)
            rel_path = os.path.relpath(fpath, vault_path)

            try:
                with open(fpath, "r", encoding="utf-8") as fp:
                    content = fp.read()
            except (IOError, UnicodeDecodeError):
                continue

            if not _is_draft_note(content):
                continue

            current_hash = _simple_hash(content)
            synced_info = state["synced_files"].get(rel_path)

            if synced_info is None:
                # 新草稿
                metadata, body = _parse_frontmatter(content)
                title = metadata.get("title", "")
                if not title:
                    h1_match = re.match(r"^#\s+(.+)$", body, re.MULTILINE)
                    title = h1_match.group(1).strip() if h1_match else os.path.splitext(f)[0]
                new_drafts.append({
                    "file": rel_path,
                    "title": title,
                    "hash": current_hash,
                })
            elif synced_info.get("hash") != current_hash:
                # 已同步但有变更
                modified.append({
                    "file": rel_path,
                    "ce_id": synced_info.get("ce_id", ""),
                    "old_hash": synced_info.get("hash", ""),
                    "new_hash": current_hash,
                    "last_sync": synced_info.get("last_sync", ""),
                })
            else:
                unchanged.append(rel_path)

    if not dry_run:
        state["last_sync_at"] = now_iso()
        _save_sync_state(state)

    output_success({
        "message": f"同步检测完成: {len(new_drafts)} 新草稿, {len(modified)} 已变更, {len(unchanged)} 未变更",
        "dry_run": dry_run,
        "vault_path": vault_path,
        "new_drafts": new_drafts,
        "modified": modified,
        "unchanged_count": len(unchanged),
        "note": "新草稿请使用 import-draft 导入，变更文件请手动确认后更新" if new_drafts or modified else "所有文件已同步",
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("content-engine Obsidian 笔记库集成")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "connect": lambda: connect(data or {}),
        "import-draft": lambda: import_draft(data or {}),
        "export-draft": lambda: export_draft(data or {}),
        "list-drafts": lambda: list_drafts(data),
        "sync": lambda: sync(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
