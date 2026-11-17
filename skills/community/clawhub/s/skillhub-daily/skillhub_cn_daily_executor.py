#!/usr/bin/env python3
"""
SkillHub Daily 一键执行器 v3.0
抓取 → 推荐 → 三处存放（Obsidian / IMA / 飞书）

使用方法：
  python skillhub_cn_daily_executor.py
  python skillhub_cn_daily_executor.py --skip-push       # 只生成简报，不推送
  python skillhub_cn_daily_executor.py --skip-eval       # 跳过 evaluation/reports 深度评估
  python skillhub_cn_daily_executor.py --date 2026-07-12 # 指定日期
  python skillhub_cn_daily_executor.py --only obsidian   # 只推送到 Obsidian
  python skillhub_cn_daily_executor.py --only ima        # 只推送到 IMA
  python skillhub_cn_daily_executor.py --only feishu     # 只推送到飞书
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data"

# 三处存放配置（通过环境变量配置，不硬编码）
OBSIDIAN_INBOX = Path(os.environ.get("OBSIDIAN_VAULT_PATH", ""))
IMA_KB_ID = os.environ.get("IMA_KB_ID", "")


def run_step(name, cmd):
    print(f"\n{'='*60}")
    print(f"  STEP: {name}")
    print(f"{'='*60}")
    start = time.time()
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=False, text=True)
    elapsed = time.time() - start
    if result.returncode != 0:
        print(f"  [FAIL] {name} ({elapsed:.1f}s)")
        return False
    print(f"  [OK] {name} ({elapsed:.1f}s)")
    return True


# ── 三处存放函数 ──

def push_to_obsidian(md_path, date_str):
    """将简报 Markdown 保存到 Obsidian inbox"""
    print("\n  [Obsidian] 保存中...")
    if not OBSIDIAN_INBOX.exists():
        print(f"  [Obsidian] 目录不存在: {OBSIDIAN_INBOX}，跳过")
        return False

    filename = f"SkillHub-Daily-{date_str}.md"
    dest = OBSIDIAN_INBOX / filename

    try:
        # 读取简报并添加 frontmatter
        content = md_path.read_text(encoding="utf-8")
        frontmatter = f"""---
title: "SkillHub Daily | {date_str}"
date: {date_str}
tags: [skillhub, daily, 推荐]
source: skillhub-cn-daily
---

"""
        dest.write_text(frontmatter + content, encoding="utf-8")
        print(f"  [Obsidian] OK: {dest}")
        return True
    except PermissionError:
        # fallback: 复制到脚本目录
        fallback = PROJECT_ROOT / "data" / "saved" / filename
        fallback.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(md_path), str(fallback))
        print(f"  [Obsidian] Permission denied, fallback: {fallback}")
        return True
    except Exception as e:
        print(f"  [Obsidian] FAIL: {e}")
        return False


def push_to_ima(md_path, date_str):
    """将简报保存到 IMA FIM 知识库（两步流程：create_note + add_knowledge）"""
    print("\n  [IMA] 保存中...")
    client_id = os.environ.get("IMA_OPENAPI_CLIENTID") or os.environ.get("IMA_CLIENT_ID")
    api_key = os.environ.get("IMA_OPENAPI_APIKEY") or os.environ.get("IMA_API_KEY")

    if not client_id or not api_key:
        print("  [IMA] 缺少环境变量 IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY，跳过")
        return False

    content = md_path.read_text(encoding="utf-8")
    title = f"SkillHub Daily | {date_str}"

    try:
        # Step 1: 创建笔记
        note_data = json.dumps({
            "title": title,
            "content": content[:4000],  # IMA 有长度限制
        }, ensure_ascii=False).encode("utf-8")

        req = urllib.request.Request(
            "https://openapi.yixin.im/v1.1.7/openapi/note/v1/import_doc",
            data=note_data,
            headers={
                "Content-Type": "application/json",
                "ima-openapi-clientid": client_id,
                "ima-openapi-apikey": api_key,
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            note_id = result.get("note_id") or result.get("data", {}).get("note_id")

        if not note_id:
            print(f"  [IMA] 创建笔记失败: {result}")
            return False

        # Step 2: 添加到知识库
        kb_data = json.dumps({
            "kb_id": IMA_KB_ID,
            "media_type": 11,
            "note_info": {"content_id": note_id},
        }, ensure_ascii=False).encode("utf-8")

        req2 = urllib.request.Request(
            "https://openapi.yixin.im/v1.1.7/openapi/wiki/v1/add_knowledge",
            data=kb_data,
            headers={
                "Content-Type": "application/json",
                "ima-openapi-clientid": client_id,
                "ima-openapi-apikey": api_key,
            },
            method="POST",
        )

        with urllib.request.urlopen(req2, timeout=30) as resp2:
            result2 = json.loads(resp2.read().decode("utf-8"))

        print(f"  [IMA] OK: note_id={note_id}, kb_id={IMA_KB_ID[:20]}...")
        return True

    except Exception as e:
        print(f"  [IMA] FAIL: {e}")
        return False


def push_to_feishu(md_path, date_str):
    """将简报推送到飞书云文档（通过 lark-cli）"""
    print("\n  [Feishu] 保存中...")

    title = f"SkillHub Daily | {date_str}"
    content = md_path.read_text(encoding="utf-8")

    try:
        # 使用 lark-cli 创建文档
        cmd = ["lark-cli", "doc", "create", "--title", title, "--content-stdin"]
        result = subprocess.run(
            cmd,
            input=content,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0 and result.stdout.strip():
            # 提取文档 URL
            output = result.stdout.strip()
            print(f"  [Feishu] OK: {output[:100]}")
            return True
        else:
            print(f"  [Feishu] FAIL: rc={result.returncode}, stderr={result.stderr[:200]}")
            return False

    except FileNotFoundError:
        print("  [Feishu] lark-cli 未安装，跳过")
        return False
    except Exception as e:
        print(f"  [Feishu] FAIL: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="SkillHub Daily 一键执行器 v3.0")
    parser.add_argument("--date", default=None, help="日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--skip-push", action="store_true", help="跳过三处存放推送")
    parser.add_argument("--skip-eval", action="store_true", help="跳过 evaluation/reports 深度评估")
    parser.add_argument("--only", choices=["obsidian", "ima", "feishu"],
                       help="只推送到指定目的地")
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    print(f"\n🐙 SkillHub Daily Executor v3.0 | {date_str}")

    # Step 1: 抓取
    if not run_step("1/3 抓取 SkillHub.cn 数据",
        [sys.executable, str(SCRIPTS_DIR / "fetch_skillhub_cn.py"),
         "--output", str(DATA_DIR / "snapshots"), "--date", date_str]):
        print("\n[ABORT] 抓取失败")
        return 1

    # Step 2: 推荐
    recommend_cmd = [
        sys.executable, str(SCRIPTS_DIR / "daily_recommend.py"),
        "--date", date_str, "--data-dir", str(DATA_DIR),
    ]
    if args.skip_eval:
        recommend_cmd.append("--skip-eval")
    if not run_step("2/3 生成推荐", recommend_cmd):
        print("\n[ABORT] 推荐失败")
        return 1

    # Step 3: 三处存放
    md_path = DATA_DIR / "recommended" / f"{date_str}.md"

    if args.skip_push:
        print("\n[SKIP] 三处存放已跳过")
    elif not md_path.exists():
        print(f"\n[SKIP] 简报不存在: {md_path}")
    else:
        print(f"\n{'='*60}")
        print(f"  STEP: 3/3 三处存放推送")
        print(f"{'='*60}")

        results = {}

        if args.only is None or args.only == "obsidian":
            results["obsidian"] = push_to_obsidian(md_path, date_str)

        if args.only is None or args.only == "ima":
            results["ima"] = push_to_ima(md_path, date_str)

        if args.only is None or args.only == "feishu":
            results["feishu"] = push_to_feishu(md_path, date_str)

        ok_count = sum(1 for v in results.values() if v)
        print(f"\n  推送结果: {ok_count}/{len(results)} 成功")

    # 汇总
    print(f"\n{'='*60}")
    print(f"  🐙 执行完成 | {date_str}")
    print(f"  简报: {md_path}")
    print(f"{'='*60}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
