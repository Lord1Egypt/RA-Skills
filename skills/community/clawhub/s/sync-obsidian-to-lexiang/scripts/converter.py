"""
converter.py - Obsidian Markdown 转换器

职责:
1. 将 Obsidian wikilink 格式转换为标准 Markdown 链接
2. 解析和收集文档中引用的图片/附件路径
3. 替换图片引用为乐享上传后的链接
"""

import re
import os
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class Attachment:
    """附件信息"""
    original_ref: str        # 原始引用文本 (e.g. "![[image.png]]")
    file_name: str           # 文件名 (e.g. "image.png")
    abs_path: str            # 绝对路径
    rel_path: str            # 相对于 vault 的路径
    is_image: bool           # 是否为图片
    lexiang_url: str = ""    # 上传到乐享后的 URL


@dataclass
class ConvertResult:
    """转换结果"""
    content: str                          # 转换后的 Markdown 内容
    attachments: List[Attachment] = field(default_factory=list)  # 引用的附件列表


# 图片扩展名
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico"}

# 附件扩展名（非图片的常见附件）
ATTACHMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
                         ".zip", ".rar", ".7z", ".tar", ".gz", ".mp3", ".mp4", ".wav",
                         ".mov", ".avi", ".csv", ".json", ".xml", ".txt"}

# Obsidian wikilink 图片引用: ![[image.png]] 或 ![[image.png|alt text]]
RE_WIKI_IMAGE = re.compile(r"!\[\[([^\]|]+?)(?:\|([^\]]*))?\]\]")

# Obsidian wikilink 文档引用: [[note]] 或 [[note|display text]] 或 [[note#heading]]
RE_WIKI_LINK = re.compile(r"(?<!!)\[\[([^\]|#]+?)(?:#([^\]|]*?))?(?:\|([^\]]*))?\]\]")

# 标准 Markdown 图片引用: ![alt](path)
RE_MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def is_image_file(filename: str) -> bool:
    """判断是否为图片文件"""
    _, ext = os.path.splitext(filename.lower())
    return ext in IMAGE_EXTENSIONS


def is_attachment_file(filename: str) -> bool:
    """判断是否为附件文件（图片或其他附件）"""
    _, ext = os.path.splitext(filename.lower())
    return ext in IMAGE_EXTENSIONS or ext in ATTACHMENT_EXTENSIONS


def resolve_obsidian_path(
    ref_name: str,
    current_file_dir: str,
    vault_path: str,
    attachment_folder: str = "",
) -> Optional[str]:
    """
    解析 Obsidian 引用路径，返回绝对路径。

    Obsidian 的文件查找顺序:
    1. 如果指定了附件文件夹，先在附件文件夹中查找
    2. 在当前文件所在目录查找
    3. 在 vault 根目录下递归查找
    """
    # 1. 附件文件夹
    if attachment_folder:
        att_dir = os.path.join(vault_path, attachment_folder)
        candidate = os.path.join(att_dir, ref_name)
        if os.path.isfile(candidate):
            return candidate

    # 2. 当前文件目录
    candidate = os.path.join(current_file_dir, ref_name)
    if os.path.isfile(candidate):
        return candidate

    # 3. vault 全局搜索（Obsidian 默认行为：shortest path match）
    for root, dirs, files in os.walk(vault_path):
        # 跳过 .obsidian 目录
        if ".obsidian" in root:
            continue
        if ref_name in files:
            return os.path.join(root, ref_name)

    return None


def get_obsidian_attachment_folder(vault_path: str) -> str:
    """
    从 Obsidian 配置中读取附件文件夹设置。
    配置位于: .obsidian/app.json -> attachmentFolderPath
    """
    app_json = os.path.join(vault_path, ".obsidian", "app.json")
    if os.path.exists(app_json):
        try:
            with open(app_json, "r", encoding="utf-8") as f:
                import json
                config = json.load(f)
                return config.get("attachmentFolderPath", "")
        except (json.JSONDecodeError, IOError):
            pass
    return ""


def extract_attachments(
    content: str,
    file_abs_path: str,
    vault_path: str,
    attachment_folder: str = "",
) -> List[Attachment]:
    """
    从 Markdown 内容中提取所有附件引用。
    """
    attachments = []
    current_dir = os.path.dirname(file_abs_path)
    seen = set()

    # 1. 解析 wikilink 图片引用: ![[image.png]]
    for match in RE_WIKI_IMAGE.finditer(content):
        ref_name = match.group(1).strip()
        if ref_name in seen:
            continue
        seen.add(ref_name)

        abs_path = resolve_obsidian_path(ref_name, current_dir, vault_path, attachment_folder)
        if abs_path and os.path.isfile(abs_path):
            rel_path = os.path.relpath(abs_path, vault_path)
            attachments.append(Attachment(
                original_ref=match.group(0),
                file_name=ref_name,
                abs_path=abs_path,
                rel_path=rel_path,
                is_image=is_image_file(ref_name),
            ))

    # 2. 解析标准 Markdown 图片引用: ![alt](path)
    for match in RE_MD_IMAGE.finditer(content):
        img_path = match.group(2).strip()
        # 跳过网络链接
        if img_path.startswith(("http://", "https://", "//")):
            continue
        # 跳过已处理过的
        base_name = os.path.basename(img_path)
        if base_name in seen:
            continue
        seen.add(base_name)

        abs_path = resolve_obsidian_path(img_path, current_dir, vault_path, attachment_folder)
        if not abs_path:
            # 尝试直接解析相对路径
            candidate = os.path.normpath(os.path.join(current_dir, img_path))
            if os.path.isfile(candidate):
                abs_path = candidate

        if abs_path and os.path.isfile(abs_path):
            rel_path = os.path.relpath(abs_path, vault_path)
            attachments.append(Attachment(
                original_ref=match.group(0),
                file_name=base_name,
                abs_path=abs_path,
                rel_path=rel_path,
                is_image=is_image_file(base_name),
            ))

    return attachments


def convert_wikilinks(
    content: str,
    attachment_map: Optional[Dict[str, str]] = None,
) -> str:
    """
    将 Obsidian wikilink 转换为标准 Markdown。

    Args:
        content: 原始 Markdown 内容
        attachment_map: 附件映射 { 文件名: 乐享URL }

    Returns:
        转换后的 Markdown 内容
    """
    if attachment_map is None:
        attachment_map = {}

    # 1. 转换 wikilink 图片: ![[image.png]] → ![image.png](url)
    def replace_wiki_image(match):
        ref_name = match.group(1).strip()
        alt_text = match.group(2) or ref_name
        alt_text = alt_text.strip()

        # 查找乐享上传后的 URL
        url = attachment_map.get(ref_name, ref_name)
        return f"![{alt_text}]({url})"

    content = RE_WIKI_IMAGE.sub(replace_wiki_image, content)

    # 2. 转换 wikilink 文档链接: [[note]] → [note](note)
    def replace_wiki_link(match):
        note_name = match.group(1).strip()
        heading = match.group(2) or ""
        display = match.group(3) or ""
        display = display.strip()

        if not display:
            display = note_name
            if heading:
                display = f"{note_name} > {heading}"

        # 文档链接保留原文名称（无法映射到乐享 URL）
        link_target = note_name
        if heading:
            link_target = f"{note_name}#{heading}"

        return f"[{display}]({link_target})"

    content = RE_WIKI_LINK.sub(replace_wiki_link, content)

    # 3. 替换标准 Markdown 图片中已上传的附件
    if attachment_map:
        def replace_md_image(match):
            alt_text = match.group(1)
            img_path = match.group(2).strip()
            if img_path.startswith(("http://", "https://", "//")):
                return match.group(0)
            base_name = os.path.basename(img_path)
            url = attachment_map.get(base_name)
            if url:
                return f"![{alt_text}]({url})"
            return match.group(0)

        content = RE_MD_IMAGE.sub(replace_md_image, content)

    return content


@dataclass
class Segment:
    """图文有序片段：kind 为 'text'（markdown 文本）或 'image'（本地图片）"""
    kind: str                    # "text" | "image"
    text: str = ""               # kind=text 时的 markdown 文本
    image_abs_path: str = ""     # kind=image 时图片绝对路径
    image_alt: str = ""          # 图片 alt/caption


def split_into_segments(
    content: str,
    file_abs_path: str,
    vault_path: str,
    attachment_folder: str = "",
) -> List[Segment]:
    """
    把 markdown 按「本地图片引用」切成有序片段：text / image 交替。

    - 本地图片（![[img]] 或 ![](本地路径)，且文件存在）→ image 片段
    - 公网图片（http/https）→ 留在 text 片段（乐享 entry_import_content/convert 会自动抓取）
    - 文档 wikilink [[note]] → 在 text 片段内由 convert_wikilinks 处理

    用于图文混排：文本片段交给乐享转 block，图片片段走 block 附件上传内嵌。
    """
    current_dir = os.path.dirname(file_abs_path)

    # 收集所有「本地图片」引用的 (start, end, abs_path, alt)
    spans = []

    for m in RE_WIKI_IMAGE.finditer(content):
        ref_name = m.group(1).strip()
        alt = (m.group(2) or ref_name).strip()
        abs_path = resolve_obsidian_path(ref_name, current_dir, vault_path, attachment_folder)
        if abs_path and os.path.isfile(abs_path) and is_image_file(ref_name):
            spans.append((m.start(), m.end(), abs_path, alt))

    for m in RE_MD_IMAGE.finditer(content):
        img_path = m.group(2).strip()
        alt = m.group(1).strip()
        if img_path.startswith(("http://", "https://", "//")):
            continue  # 公网图，保留在文本里
        abs_path = resolve_obsidian_path(
            os.path.basename(img_path), current_dir, vault_path, attachment_folder)
        if not abs_path:
            candidate = os.path.normpath(os.path.join(current_dir, img_path))
            if os.path.isfile(candidate):
                abs_path = candidate
        if abs_path and os.path.isfile(abs_path) and is_image_file(img_path):
            spans.append((m.start(), m.end(), abs_path, alt))

    if not spans:
        # 无本地图片：整篇作为一个文本片段
        return [Segment(kind="text", text=content)]

    spans.sort(key=lambda x: x[0])

    segments = []
    cursor = 0
    for start, end, abs_path, alt in spans:
        if start > cursor:
            text_part = content[cursor:start]
            if text_part.strip():
                segments.append(Segment(kind="text", text=text_part))
        segments.append(Segment(kind="image", image_abs_path=abs_path, image_alt=alt))
        cursor = end
    if cursor < len(content):
        tail = content[cursor:]
        if tail.strip():
            segments.append(Segment(kind="text", text=tail))

    return segments


def has_local_images(
    content: str,
    file_abs_path: str,
    vault_path: str,
    attachment_folder: str = "",
) -> bool:
    """判断 markdown 是否引用了存在的本地图片（决定走图文混排还是纯文本导入）。"""
    segs = split_into_segments(content, file_abs_path, vault_path, attachment_folder)
    return any(s.kind == "image" for s in segs)


def convert_file(
    file_abs_path: str,
    vault_path: str,
    attachment_folder: str = "",
    attachment_map: Optional[Dict[str, str]] = None,
) -> ConvertResult:
    """
    转换单个 Obsidian Markdown 文件。

    Args:
        file_abs_path: 文件绝对路径
        vault_path: vault 根目录
        attachment_folder: 附件文件夹
        attachment_map: 已上传的附件映射

    Returns:
        ConvertResult 包含转换后的内容和附件列表
    """
    with open(file_abs_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取附件
    attachments = extract_attachments(content, file_abs_path, vault_path, attachment_folder)

    # 转换 wikilinks
    converted = convert_wikilinks(content, attachment_map)

    return ConvertResult(content=converted, attachments=attachments)
