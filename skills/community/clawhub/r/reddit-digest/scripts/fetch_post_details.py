#!/usr/bin/env python3
"""
fetch_post_details.py - 批量获取 Reddit Post 详情并保存到临时目录

用法：
  # 从 autocli 管道获取列表，批量抓取详情
  autocli reddit subreddit ClaudeAI --limit 50 --sort top --time day --format json | \
    python3 fetch_post_details.py --temp-dir /tmp/reddit/temp

  # 从已保存的 JSON 文件读取列表
  python3 fetch_post_details.py --input posts.json --temp-dir /tmp/reddit/temp

  # 自定义并发数
  python3 fetch_post_details.py --input posts.json --temp-dir /tmp/reddit/temp --workers 3

输出：
  - 每条 Post 详情保存为 {temp-dir}/{rank:02d}-{sanitized_title}.json
  - 统计信息输出到 stderr
  - stdout 输出成功抓取的文件路径列表（换行分隔）
"""

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_args():
    parser = argparse.ArgumentParser(description="批量获取 Reddit Post 详情")
    parser.add_argument(
        "--input", "-i",
        help="输入 JSON 文件路径（不指定则从 stdin 读取）",
    )
    parser.add_argument(
        "--temp-dir", "-d",
        required=True,
        help="临时目录路径，用于保存每条 Post 详情",
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=1,
        help="并发抓取数，默认 1（autocli 基于浏览器，并发过高会导致 tab 冲突）",
    )
    return parser.parse_args()


def load_posts(input_path):
    if input_path:
        with open(input_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return json.load(sys.stdin)


def sanitize_filename(title, max_len=60):
    """将标题转换为安全的文件名"""
    # 替换非字母数字字符为下划线
    safe = re.sub(r"[^\w\s-]", "", title)
    safe = re.sub(r"[\s_]+", "_", safe).strip("_")
    return safe[:max_len]


def fetch_detail(rank, post, temp_dir):
    """抓取单条 Post 详情，返回 (rank, output_path, error)"""
    url = post.get("url", "")
    title = post.get("title", f"post_{rank}")
    sanitized = sanitize_filename(title)
    filename = f"{rank:02d}-{sanitized}.json"
    output_path = os.path.join(temp_dir, filename)

    # 构建详情数据（包含 Post 元数据）
    detail_data = {
        "rank": rank,
        "meta": post,  # 保留原始列表元数据
        "content": None,
        "error": None,
    }

    if not url:
        detail_data["error"] = "missing url"
        _write_json(output_path, detail_data)
        return rank, output_path, "missing url"

    try:
        result = subprocess.run(
            ["autocli", "reddit", "read", url, "-f", "json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            detail_data["content"] = json.loads(result.stdout)
        else:
            err = result.stderr.strip() or f"exit code {result.returncode}"
            detail_data["error"] = err
            print(f"[WARN] rank={rank} 抓取失败：{err}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        detail_data["error"] = "timeout"
        print(f"[WARN] rank={rank} 超时：{url}", file=sys.stderr)
    except json.JSONDecodeError as e:
        detail_data["error"] = f"json parse error: {e}"
        print(f"[WARN] rank={rank} JSON 解析失败：{e}", file=sys.stderr)
    except FileNotFoundError:
        detail_data["error"] = "autocli not found"
        print("[ERROR] autocli 未找到，请确认已安装", file=sys.stderr)
        sys.exit(1)

    _write_json(output_path, detail_data)
    return rank, output_path, detail_data["error"]


def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    args = parse_args()

    posts = load_posts(args.input)
    if not isinstance(posts, list):
        print("[ERROR] 输入 JSON 应为数组格式", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.temp_dir, exist_ok=True)
    total = len(posts)
    print(f"[INFO] 共 {total} 条 Post，并发数 {args.workers}", file=sys.stderr)

    success_paths = []
    failed = 0

    completed_count = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(fetch_detail, rank + 1, post, args.temp_dir): rank
            for rank, post in enumerate(posts)
        }
        for future in as_completed(futures):
            rank, output_path, error = future.result()
            completed_count += 1
            if error:
                failed += 1
                print(f"[PROGRESS] {completed_count}/{total} 完成（rank={rank} 失败: {error}）", file=sys.stderr)
            else:
                success_paths.append((rank, output_path))
                print(f"[PROGRESS] {completed_count}/{total} 完成（rank={rank} 成功）", file=sys.stderr)

    # 按 rank 排序后输出路径到 stdout
    success_paths.sort(key=lambda x: x[0])
    for _, path in success_paths:
        print(path)

    print(f"[INFO] 成功：{len(success_paths)} 条，失败：{failed} 条", file=sys.stderr)
    print(f"[INFO] 详情已保存至：{args.temp_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
