#!/usr/bin/env python3
"""
content-engine 内容数据管理模块

提供内容数据的 CRUD 操作，支持 JSON 文件存储、Markdown 导入导出。
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from utils import (
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    today_str,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    validate_status,
    validate_platform,
    validate_status_transition,
    format_platform_name,
    truncate_text,
    write_json_file,
    CONTENT_STATUSES,
    PLATFORMS,
)

# 延迟导入以避免循环依赖
_obsidian_sync = None
_learning_engine = None


def _get_obsidian_sync():
    """延迟导入 obsidian_sync 模块。"""
    global _obsidian_sync
    if _obsidian_sync is None:
        try:
            import obsidian_sync as _obsidian_sync
        except ImportError:
            _obsidian_sync = None
    return _obsidian_sync


def _get_learning_engine():
    """延迟导入 learning_engine 模块。"""
    global _learning_engine
    if _learning_engine is None:
        try:
            import learning_engine as _learning_engine
        except ImportError:
            _learning_engine = None
    return _learning_engine


# ============================================================
# 数据文件路径
# ============================================================

CONTENTS_FILE = "contents.json"


def _get_contents() -> List[Dict[str, Any]]:
    """读取所有内容数据。"""
    return read_json_file(get_data_file(CONTENTS_FILE))


def _save_contents(contents: List[Dict[str, Any]]) -> None:
    """保存内容数据到文件。"""
    write_json_file(get_data_file(CONTENTS_FILE), contents)


def _find_content(contents: List[Dict], content_id: str) -> Optional[Dict]:
    """根据 ID 查找内容。"""
    for c in contents:
        if c.get("id") == content_id:
            return c
    return None


# ============================================================
# CRUD 操作
# ============================================================

def create_content(data: Dict[str, Any]) -> None:
    """创建新内容。

    必填字段: title, body
    可选字段: summary, tags, platforms, status, author, scheduled_at

    Args:
        data: 内容数据字典。
    """
    if not data.get("title"):
        output_error("内容标题（title）为必填字段", code="VALIDATION_ERROR")
        return

    if not data.get("body"):
        output_error("内容正文（body）为必填字段", code="VALIDATION_ERROR")
        return

    sub = check_subscription()
    contents = _get_contents()

    # 检查内容数量限制
    if len(contents) >= sub["max_content"]:
        limit = sub["max_content"]
        if sub["tier"] == "free":
            output_error(
                f"免费版最多管理 {limit} 条内容，当前已有 {len(contents)} 条。"
                "请升级至付费版（¥99/月）以管理更多内容。",
                code="LIMIT_EXCEEDED",
            )
        else:
            output_error(
                f"已达到内容数量上限 {limit} 条。",
                code="LIMIT_EXCEEDED",
            )
        return

    # 校验状态
    status = data.get("status", "草稿")
    try:
        validate_status(status)
    except ValueError as e:
        output_error(str(e), code="VALIDATION_ERROR")
        return

    # 校验平台列表
    platforms = data.get("platforms", [])
    if isinstance(platforms, str):
        platforms = [p.strip() for p in platforms.split(",") if p.strip()]
    validated_platforms = []
    for p in platforms:
        try:
            validated_platforms.append(validate_platform(p))
        except ValueError as e:
            output_error(str(e), code="VALIDATION_ERROR")
            return

    # 检查平台数量限制
    if len(validated_platforms) > sub["max_platforms"]:
        if sub["tier"] == "free":
            output_error(
                f"免费版最多选择 {sub['max_platforms']} 个平台。"
                "请升级至付费版（¥99/月）以使用所有平台。",
                code="LIMIT_EXCEEDED",
            )
        else:
            output_error(
                f"最多选择 {sub['max_platforms']} 个平台。",
                code="LIMIT_EXCEEDED",
            )
        return

    # 校验标签
    tags = data.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    # 图片提示词（可选，由 image_prompter 生成）
    image_prompts = data.get("image_prompts", [])

    now = now_iso()
    content = {
        "id": generate_id("CT"),
        "title": data["title"],
        "body": data["body"],
        "summary": data.get("summary", ""),
        "tags": tags,
        "platforms": validated_platforms,
        "status": status,
        "author": data.get("author", ""),
        "scheduled_at": data.get("scheduled_at", ""),
        "published_at": "",
        "publish_results": {},
        "image_prompts": image_prompts,
        "created_at": now,
        "updated_at": now,
    }

    contents.append(content)
    _save_contents(contents)

    output_success({
        "message": f"内容「{truncate_text(content['title'], 30)}」已创建",
        "content": content,
    })


def update_content(data: Dict[str, Any]) -> None:
    """更新内容信息。

    必填字段: id
    可更新字段: title, body, summary, tags, platforms, status, author, scheduled_at

    Args:
        data: 包含内容 ID 和待更新字段的字典。
    """
    content_id = data.get("id")
    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    updatable_fields = ["title", "body", "summary", "tags", "platforms", "author", "scheduled_at", "image_prompts"]
    updated = False

    for field in updatable_fields:
        if field in data:
            value = data[field]
            if field == "platforms":
                if isinstance(value, str):
                    value = [p.strip() for p in value.split(",") if p.strip()]
                validated = []
                for p in value:
                    try:
                        validated.append(validate_platform(p))
                    except ValueError as e:
                        output_error(str(e), code="VALIDATION_ERROR")
                        return
                # 检查平台数量限制
                sub = check_subscription()
                if len(validated) > sub["max_platforms"]:
                    output_error(
                        f"最多选择 {sub['max_platforms']} 个平台。",
                        code="LIMIT_EXCEEDED",
                    )
                    return
                value = validated
            elif field == "tags":
                if isinstance(value, str):
                    value = [t.strip() for t in value.split(",") if t.strip()]
            content[field] = value
            updated = True

    # 状态变更需要单独处理（校验流转规则）
    if "status" in data:
        new_status = data["status"]
        try:
            validate_status(new_status)
            if new_status != content["status"]:
                validate_status_transition(content["status"], new_status)
                content["status"] = new_status
                # 如果状态变为"已发布"，记录发布时间
                if new_status == "已发布":
                    content["published_at"] = now_iso()
                updated = True
        except ValueError as e:
            output_error(str(e), code="VALIDATION_ERROR")
            return

    if not updated:
        output_error("未提供任何待更新的字段", code="VALIDATION_ERROR")
        return

    content["updated_at"] = now_iso()
    _save_contents(contents)

    output_success({
        "message": f"内容「{truncate_text(content['title'], 30)}」已更新",
        "content": content,
    })


def delete_content(data: Dict[str, Any]) -> None:
    """删除内容。

    必填字段: id

    Args:
        data: 包含内容 ID 的字典。
    """
    content_id = data.get("id")
    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    original_count = len(contents)
    contents = [c for c in contents if c.get("id") != content_id]

    if len(contents) == original_count:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    _save_contents(contents)
    output_success({"message": f"内容 {content_id} 已删除"})


def get_content(data: Dict[str, Any]) -> None:
    """获取单条内容详情。

    必填字段: id

    Args:
        data: 包含内容 ID 的字典。
    """
    content_id = data.get("id")
    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    output_success(content)


def list_contents(data: Optional[Dict[str, Any]] = None) -> None:
    """列出所有内容。

    可选过滤: status, platform, keyword, date_from, date_to

    Args:
        data: 可选的过滤条件字典。
    """
    contents = _get_contents()

    if data:
        # 按状态过滤
        status_filter = data.get("status")
        if status_filter:
            contents = [c for c in contents if c.get("status") == status_filter]

        # 按平台过滤
        platform_filter = data.get("platform")
        if platform_filter:
            platform_filter = platform_filter.lower()
            contents = [c for c in contents if platform_filter in c.get("platforms", [])]

        # 按关键词搜索（标题、正文、摘要、标签）
        keyword = data.get("keyword", "").strip()
        if keyword:
            keyword_lower = keyword.lower()
            contents = [
                c for c in contents
                if keyword_lower in c.get("title", "").lower()
                or keyword_lower in c.get("body", "").lower()
                or keyword_lower in c.get("summary", "").lower()
                or any(keyword_lower in t.lower() for t in c.get("tags", []))
            ]

        # 按日期范围过滤
        date_from = data.get("date_from", "")
        date_to = data.get("date_to", "")
        if date_from:
            contents = [c for c in contents if c.get("created_at", "") >= date_from]
        if date_to:
            contents = [c for c in contents if c.get("created_at", "") <= date_to + "T23:59:59"]

    # 按更新时间倒序排列
    contents.sort(key=lambda c: c.get("updated_at", ""), reverse=True)

    # 按状态分组统计
    status_stats = {}
    for status in CONTENT_STATUSES:
        status_stats[status] = sum(1 for c in contents if c.get("status") == status)

    # 按平台分组统计
    platform_stats = {}
    for p in PLATFORMS:
        platform_stats[format_platform_name(p)] = sum(
            1 for c in contents if p in c.get("platforms", [])
        )

    # 列表中截断正文
    display_list = []
    for c in contents:
        d = dict(c)
        d["body"] = truncate_text(d.get("body", ""), 100)
        display_list.append(d)

    output_success({
        "total": len(display_list),
        "status_stats": status_stats,
        "platform_stats": platform_stats,
        "contents": display_list,
    })


def import_content(data: Dict[str, Any]) -> None:
    """从 Markdown 文件导入内容。

    支持带 YAML frontmatter 的 Markdown 文件。
    必填字段: file_path

    Args:
        data: 包含文件路径的字典。
    """
    file_path = data.get("file_path")
    if not file_path:
        output_error("文件路径（file_path）为必填字段", code="VALIDATION_ERROR")
        return

    if not os.path.exists(file_path):
        output_error(f"文件不存在: {file_path}", code="FILE_NOT_FOUND")
        return

    sub = check_subscription()
    contents = _get_contents()

    if len(contents) >= sub["max_content"]:
        output_error(
            f"已达内容数量上限 {sub['max_content']} 条，无法导入。",
            code="LIMIT_EXCEEDED",
        )
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw = f.read()
    except IOError as e:
        output_error(f"文件读取失败: {e}", code="FILE_ERROR")
        return

    # 解析 YAML frontmatter
    title = ""
    tags = []
    platforms = []
    author = ""
    summary = ""
    body = raw

    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if frontmatter_match:
        frontmatter_str = frontmatter_match.group(1)
        body = frontmatter_match.group(2).strip()

        # 简单解析 YAML（不依赖 pyyaml）
        for line in frontmatter_str.split("\n"):
            line = line.strip()
            if line.startswith("title:"):
                title = line[len("title:"):].strip().strip("\"'")
            elif line.startswith("tags:"):
                tags_str = line[len("tags:"):].strip()
                if tags_str.startswith("[") and tags_str.endswith("]"):
                    tags = [t.strip().strip("\"'") for t in tags_str[1:-1].split(",") if t.strip()]
            elif line.startswith("platforms:"):
                plat_str = line[len("platforms:"):].strip()
                if plat_str.startswith("[") and plat_str.endswith("]"):
                    platforms = [p.strip().strip("\"'") for p in plat_str[1:-1].split(",") if p.strip()]
            elif line.startswith("author:"):
                author = line[len("author:"):].strip().strip("\"'")
            elif line.startswith("summary:") or line.startswith("description:"):
                key = "summary:" if line.startswith("summary:") else "description:"
                summary = line[len(key):].strip().strip("\"'")

    # 若未从 frontmatter 获取标题，尝试从正文第一个 # 标题获取
    if not title:
        title_match = re.match(r"^#\s+(.+)$", body, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = os.path.splitext(os.path.basename(file_path))[0]

    # 校验平台
    validated_platforms = []
    for p in platforms:
        try:
            validated_platforms.append(validate_platform(p))
        except ValueError:
            pass  # 导入时忽略无效平台

    now = now_iso()
    content = {
        "id": generate_id("CT"),
        "title": title,
        "body": body,
        "summary": summary,
        "tags": tags,
        "platforms": validated_platforms,
        "status": "草稿",
        "author": author,
        "scheduled_at": "",
        "published_at": "",
        "publish_results": {},
        "created_at": now,
        "updated_at": now,
    }

    contents.append(content)
    _save_contents(contents)

    output_success({
        "message": f"已从 {os.path.basename(file_path)} 导入内容「{truncate_text(title, 30)}」",
        "content": content,
    })


def export_content(data: Dict[str, Any]) -> None:
    """导出内容为 Markdown 格式。

    必填字段: id
    可选字段: file_path（若不指定则输出到 stdout）

    Args:
        data: 包含内容 ID 和可选文件路径的字典。
    """
    content_id = data.get("id")
    if not content_id:
        output_error("内容ID（id）为必填字段", code="VALIDATION_ERROR")
        return

    contents = _get_contents()
    content = _find_content(contents, content_id)
    if not content:
        output_error(f"未找到ID为 {content_id} 的内容", code="NOT_FOUND")
        return

    # 生成 Markdown + frontmatter
    lines = ["---"]
    lines.append(f'title: "{content["title"]}"')
    if content.get("author"):
        lines.append(f'author: "{content["author"]}"')
    if content.get("summary"):
        lines.append(f'summary: "{content["summary"]}"')
    if content.get("tags"):
        tags_str = ", ".join(f'"{t}"' for t in content["tags"])
        lines.append(f"tags: [{tags_str}]")
    if content.get("platforms"):
        plat_str = ", ".join(f'"{p}"' for p in content["platforms"])
        lines.append(f"platforms: [{plat_str}]")
    lines.append(f'status: "{content["status"]}"')
    lines.append(f'created_at: "{content["created_at"]}"')
    lines.append("---")
    lines.append("")
    lines.append(content.get("body", ""))

    markdown = "\n".join(lines)

    file_path = data.get("file_path")
    if file_path:
        try:
            os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown)
            output_success({
                "message": f"已导出内容到 {file_path}",
                "file_path": file_path,
            })
        except IOError as e:
            output_error(f"导出失败: {e}", code="EXPORT_ERROR")
    else:
        output_success({
            "markdown": markdown,
            "content_id": content_id,
        })


# ============================================================
# Obsidian 导入
# ============================================================

def import_obsidian(data: Dict[str, Any]) -> None:
    """从 Obsidian 笔记库导入草稿为内容。

    必填字段: file（笔记在库中的相对路径）
    可选字段: vault_path

    内部调用 obsidian_sync 模块解析笔记，然后自动创建内容。

    Args:
        data: 包含文件路径的字典。
    """
    obs = _get_obsidian_sync()
    if obs is None:
        output_error("Obsidian 同步模块不可用", code="MODULE_ERROR")
        return

    file_rel = data.get("file", "")
    if not file_rel:
        output_error("笔记文件路径（file）为必填字段", code="VALIDATION_ERROR")
        return

    vault_path = data.get("vault_path") or os.environ.get("CE_OBSIDIAN_VAULT_PATH", "")
    if vault_path:
        vault_path = os.path.expanduser(vault_path)

    if not vault_path:
        # 尝试从同步状态获取
        state = obs._get_sync_state()
        vault_path = state.get("vault_path", "")

    if not vault_path or not os.path.isdir(vault_path):
        output_error(
            "未连接到 Obsidian 笔记库，请先设置 CE_OBSIDIAN_VAULT_PATH 或执行 obsidian_sync connect",
            code="NOT_CONNECTED",
        )
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

    # 解析笔记
    metadata, body = obs._parse_frontmatter(raw_content)
    body = obs._convert_wikilinks(body, "plain")

    # 提取标签
    fm_tags = metadata.get("tags", [])
    if isinstance(fm_tags, str):
        fm_tags = [t.strip() for t in fm_tags.split(",") if t.strip()]
    body_tags = obs._extract_tags_from_body(body)
    all_tags = list(dict.fromkeys(fm_tags + body_tags))
    all_tags = [t for t in all_tags if t.lower() not in {"content", "draft", "内容", "草稿"}]

    # 清理正文中的标签标记
    body = re.sub(r"(?:^|\s)#([a-zA-Z\u4e00-\u9fff][\w\u4e00-\u9fff/-]*)", " ", body).strip()

    # 获取标题
    title = metadata.get("title", "")
    if not title:
        h1_match = re.match(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
            body = re.sub(r"^#\s+.+\n*", "", body, count=1).strip()
        else:
            title = os.path.splitext(os.path.basename(file_rel))[0]

    if not title or not body:
        output_error("笔记缺少标题或正文内容", code="VALIDATION_ERROR")
        return

    # 创建内容
    content_data = {
        "title": title,
        "body": body,
        "summary": metadata.get("summary", ""),
        "tags": all_tags,
        "platforms": metadata.get("platforms", []),
        "author": metadata.get("author", ""),
    }
    create_content(content_data)


# ============================================================
# 学习引擎集成：发布后记录基线数据
# ============================================================

def _record_publish_baseline(content: Dict[str, Any]) -> None:
    """发布后向学习引擎记录基线数据。

    在内容状态变为"已发布"时调用，记录初始性能数据供后续分析。

    Args:
        content: 已发布的内容字典。
    """
    le = _get_learning_engine()
    if le is None:
        return  # 学习引擎不可用时静默跳过

    for platform in content.get("platforms", []):
        try:
            le.record_performance({
                "content_id": content.get("id", ""),
                "platform": platform,
                "topic": content.get("tags", [""])[0] if content.get("tags") else "",
                "tags": content.get("tags", []),
                "title": content.get("title", ""),
                "posting_time": content.get("published_at", now_iso()),
                "format": "article",
                "length": len(content.get("body", "")),
                "metrics": {},  # 基线为空，后续由 metrics_collector 填充
            })
        except Exception:
            pass  # 记录失败不影响主流程


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("content-engine 内容数据管理")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "create": lambda: create_content(data or {}),
        "update": lambda: update_content(data or {}),
        "delete": lambda: delete_content(data or {}),
        "get": lambda: get_content(data or {}),
        "list": lambda: list_contents(data),
        "import": lambda: import_content(data or {}),
        "export": lambda: export_content(data or {}),
        "import-obsidian": lambda: import_obsidian(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
