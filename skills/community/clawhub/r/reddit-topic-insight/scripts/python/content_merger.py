#!/usr/bin/env python3
"""
内容合并脚本

功能：
- 读取 pieces/angle-*.md 文件
- 按角度编号排序拼接
- 生成 content.md
- 附加来源帖子表格（标题、URL、score、评论数）

设计原则：
- 纯确定性操作，不使用任何 AI 组件
- 保证输出顺序和格式一致性
- 避免对 SubAgent 产出的内容做任何修改

用法：
    python3 content_merger.py \
        --pieces-dir <pieces 目录路径> \
        --posts-file <posts_detail.json 路径> \
        --output <输出文件路径>
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def load_json_file(file_path: str) -> dict[str, Any]:
    """加载 JSON 文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def discover_pieces(pieces_dir: str) -> list[tuple[int, str]]:
    """
    发现并排序 piece 文件

    文件名格式：angle-{n}.md（n 为两位数字编号）
    返回按编号排序的 (编号, 文件路径) 元组列表
    """
    pattern = re.compile(r"^angle-(\d+)\.md$")
    pieces: list[tuple[int, str]] = []

    if not os.path.isdir(pieces_dir):
        logger.error(f"pieces 目录不存在: {pieces_dir}")
        return pieces

    for filename in os.listdir(pieces_dir):
        match = pattern.match(filename)
        if match:
            angle_num = int(match.group(1))
            file_path = os.path.join(pieces_dir, filename)
            pieces.append((angle_num, file_path))

    # 按角度编号排序
    pieces.sort(key=lambda x: x[0])
    return pieces


def read_piece_content(file_path: str) -> str:
    """读取单个 piece 文件内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError as e:
        logger.warning(f"读取文件失败: {file_path}: {e}")
        return ""


def build_source_table(posts_data: dict[str, Any]) -> str:
    """
    构建来源帖子 Markdown 表格

    包含：序号、标题、子版块、热度分、评论数、链接
    """
    posts = posts_data.get("posts", [])
    if not posts:
        return ""

    lines = [
        "## 📊 数据来源",
        "",
        "| # | 标题 | 子版块 | 热度分 | 评论数 | 链接 |",
        "|---|------|--------|--------|--------|------|"
    ]

    for i, post in enumerate(posts, 1):
        title = post.get("title", "无标题")
        # 截断标题避免表格变形
        if len(title) > 50:
            title = title[:47] + "..."
        # 转义 Markdown 表格中的管道字符
        title = title.replace("|", "\\|")

        subreddit = f"r/{post.get('subreddit', '?')}"
        heat_score = post.get("heat_score", 0)
        num_comments = post.get("num_comments", 0)
        url = post.get("url", "#")

        lines.append(
            f"| {i} | {title} | {subreddit} | {heat_score} | {num_comments} | [链接]({url}) |"
        )

    return "\n".join(lines)


def merge_content(
    pieces: list[tuple[int, str]],
    posts_data: dict[str, Any],
    topic: str
) -> str:
    """
    合并所有 piece 文件为最终的 content.md

    结构：
    1. 报告头部（主题、生成时间、统计信息）
    2. 各角度内容（按编号排序）
    3. 来源表格
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 报告头部
    header = f"""# {topic} — Reddit 主题洞察报告

> 生成时间：{timestamp}
> 数据来源：Reddit
> 覆盖角度：{len(pieces)} 个
> 涵盖平台：X / 小红书 / 公众号

---"""

    # 拼接各角度内容
    sections = [header]
    for angle_num, file_path in pieces:
        content = read_piece_content(file_path)
        if content:
            sections.append(content)
            sections.append("\n---")
        else:
            logger.warning(f"角度 {angle_num} 内容为空，跳过")

    # 来源表格
    source_table = build_source_table(posts_data)
    if source_table:
        sections.append(source_table)

    return "\n\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(description="内容合并脚本")
    parser.add_argument(
        "--pieces-dir",
        required=True,
        help="pieces 目录路径"
    )
    parser.add_argument(
        "--posts-file",
        required=True,
        help="posts_detail.json 路径"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="输出文件路径"
    )
    args = parser.parse_args()

    # 发现 piece 文件
    pieces = discover_pieces(args.pieces_dir)
    if not pieces:
        logger.error("未找到任何 piece 文件，请先完成 Step 6（成品生产）")
        sys.exit(1)

    logger.info(f"发现 {len(pieces)} 个 piece 文件:")
    for num, path in pieces:
        logger.info(f"  角度 {num}: {os.path.basename(path)}")

    # 加载帖子数据（用于来源表格）
    posts_data = load_json_file(args.posts_file)
    topic = posts_data.get("metadata", {}).get("topic", "未知主题")

    # 合并内容
    final_content = merge_content(pieces, posts_data, topic)

    # 确保输出目录存在
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 写入文件
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(final_content)

    logger.info(f"合并完成！最终文件: {args.output}")
    logger.info(f"共合并 {len(pieces)} 个角度，总计 {len(final_content)} 字符")


if __name__ == "__main__":
    main()
