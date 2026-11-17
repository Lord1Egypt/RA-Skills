"""
Obsidian 存放脚本
将 ClawHub Daily 推荐简报推送到本地 Obsidian vault

使用方法：
  python scripts/push_to_obsidian.py --recommendation data/recommended/2026-07-12.json

Vault 路径（优先级：环境变量 > 默认值）：
  - 环境变量 OBSIDIAN_VAULT_PATH
  - 默认值：E:\\Obsidian\\md\\inbox\\clawhub-daily (Windows)
           ~/Obsidian/md/inbox/clawhub-daily (macOS/Linux)

文件命名：clawhub-daily_{date}_{dimension}.md
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path


def get_vault_path():
    """解析 Obsidian vault 路径"""
    env_path = os.environ.get("OBSIDIAN_VAULT_PATH")
    if env_path:
        return Path(env_path) / "clawhub-daily"
    if sys.platform == "win32":
        return Path("E:/Obsidian/md/inbox/clawhub-daily")
    return Path.home() / "Obsidian" / "md" / "inbox" / "clawhub-daily"


def safe_filename(name):
    """将字符串转为安全文件名（非字母数字/非 -_ 替换为 _）"""
    return re.sub(r"[^\w\-]", "_", name)[:50]


def build_content(rec, md_content=""):
    """构建 Obsidian 笔记内容（含 frontmatter）"""
    date = rec.get("date", "")
    dimension = rec.get("dimension", "")
    total_scanned = rec.get("total_scanned", 0)
    deduplicated = rec.get("deduplicated", 0)
    recs = rec.get("recommendations", [])

    # Frontmatter
    frontmatter = f"""---
title: "ClawHub Daily {date} - {dimension}维度"
date: {date}
dimension: {dimension}
total_scanned: {total_scanned}
recommended: {len(recs)}
deduplicated: {deduplicated}
tags:
  - clawhub-daily
  - skill-recommendation
  - {dimension}
---

"""

    # 如果有现成的 Markdown 内容，直接用
    if md_content:
        return frontmatter + md_content

    # 否则从 JSON 拼接
    lines = [f"# ClawHub Daily | {date} ({dimension}维度)\n"]
    lines.append(f"扫描 {total_scanned} 个 Skill → 推荐 {len(recs)} 个，去重 {deduplicated} 个\n")

    for i, r in enumerate(recs, 1):
        lines.append(f"\n## {i}. {r.get('display_name', 'Unknown')}\n")
        lines.append(f"- 链接: {r.get('url', '')}\n")
        lines.append(f"- 维度: {r.get('dimension', '')}\n")
        lines.append(f"- 数据: ⭐{r.get('stars', 0)} | 📥{r.get('downloads', 0)}\n")
        if r.get("chinese_one_liner"):
            lines.append(f"- 能力解读: {r['chinese_one_liner']}\n")
        if r.get("recommend_reason"):
            lines.append(f"- 推荐理由: {r['recommend_reason']}\n")
        if r.get("next_action"):
            lines.append(f"- 下一步: {r['next_action']}\n")

    return frontmatter + "\n".join(lines)


def push_to_obsidian(content, title, rec):
    """推送到 Obsidian（三级 fallback）

    Returns: (success: bool, path_or_msg: str)
    """
    vault_path = get_vault_path()
    date = rec.get("date", datetime.now().strftime("%Y-%m-%d"))
    dimension = rec.get("dimension", "all")
    filename = f"clawhub-daily_{date}_{dimension}.md"
    filepath = vault_path / filename

    # 三级 fallback
    for attempt in range(3):
        try:
            vault_path.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return True, str(filepath)
        except (PermissionError, OSError) as e:
            if attempt < 2:
                time.sleep(1)
            else:
                # Fallback 1: ASCII 文件名
                ascii_filename = f"clawhub-daily_{date}.md"
                ascii_filepath = vault_path / ascii_filename
                try:
                    with open(ascii_filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    return True, str(ascii_filepath)
                except (PermissionError, OSError):
                    # Fallback 2: 脚本目录 saved/
                    fallback_dir = Path(__file__).parent.parent / "saved"
                    fallback_dir.mkdir(parents=True, exist_ok=True)
                    fallback_path = fallback_dir / filename
                    with open(fallback_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    return True, f"vault不可写，fallback到 {fallback_path}"
    return False, "写入失败"


def main():
    parser = argparse.ArgumentParser(description="推送推荐到 Obsidian vault")
    parser.add_argument("--recommendation", required=True, help="daily_recommend.py 生成的 JSON")
    parser.add_argument("--md", default=None, help="可选：现成的 Markdown 文件路径")
    args = parser.parse_args()

    rec_path = Path(args.recommendation)
    if not rec_path.exists():
        print(f"[Error] 推荐文件不存在: {rec_path}")
        return 1

    with open(rec_path, "r", encoding="utf-8") as f:
        rec = json.load(f)

    # 读取现成 Markdown（如果有）
    md_content = ""
    if args.md:
        md_path = Path(args.md)
        if md_path.exists():
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
    else:
        # 尝试同名 .md 文件
        md_path = rec_path.with_suffix(".md")
        if md_path.exists():
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()

    content = build_content(rec, md_content)
    title = f"ClawHub Daily {rec.get('date', '')} - {rec.get('dimension', 'all')}维度"

    print(f"[Obsidian] Vault: {get_vault_path()}")
    print(f"[Obsidian] 推送 {rec.get('date', '')} ({rec.get('dimension', 'all')}) - {len(content)} 字")

    success, msg = push_to_obsidian(content, title, rec)
    if success:
        print(f"[Obsidian] 推送成功 ✓ → {msg}")
        return 0
    else:
        print(f"[Error] Obsidian 推送失败: {msg}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
