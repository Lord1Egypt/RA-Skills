#!/usr/bin/env python3
"""
mm - OpenClaw 专用记忆管理系统

用法:
  mm search "我上周做了什么"                    # 语义搜索（默认私人记忆）
  mm search "团队进展" --shared                # 搜索公共记忆
  mm search "技术选型" --all                   # 搜索所有记忆
  mm embed                                       # 更新向量索引
  mm stats                                      # 查看统计
  mm insight                                    # AI 自我总结
  mm insight --daily                           # 每日洞察
  mm insight --weekly                          # 每周洞察
  mm log "完成XX功能"                          # 快速记录
  mm related <chunk_id>                        # 查看关联记忆
  mm top                                        # 查看最重要记忆
  mm onboard                                    # 首次使用引导（OpenClaw专用）

OpenClaw 环境:
  MM_UID=openclaw_user                         # OpenClaw用户ID
  MM_BASE_DIR=~/.openclaw/memory              # 记忆仓库目录（推荐）
  OPENAI_API_KEY=sk-...                        # API Key (备选)
  SILICONFLOW_API_KEY=...                      # SiliconFlow Key (国内推荐)

OpenClaw 集成:
  此工具专为 OpenClaw 设计，支持:
  1. 自动 OpenClaw 用户身份识别
  2. 跨 OpenClaw 设备同步
  3. OpenClaw workspace 集成
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# 添加 scripts 目录到路径
SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

# 版本信息
VERSION = "3.5.0"


# ══════════════════════════════════════════════════════════════
#  配置管理
# ══════════════════════════════════════════════════════════════

def get_api_key():
    """
    获取 API Key，优先级：
    1. 环境变量 (OPENAI_API_KEY / SILICONFLOW_API_KEY / ZHIPU_API_KEY)
    2. ~/.memory-manager/config.json
    3. 返回空字符串（后续会提示配置）
    """
    # 1. 环境变量
    for env_var in ["OPENAI_API_KEY", "SILICONFLOW_API_KEY", "ZHIPU_API_KEY"]:
        api_key = os.environ.get(env_var)
        if api_key:
            return api_key, env_var

    # 2. 配置文件
    config_path = Path.home() / ".memory-manager" / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            api_key = config.get("api_key", "")
            backend = config.get("backend", "openai")
            env_var_map = {
                "openai": "OPENAI_API_KEY",
                "siliconflow": "SILICONFLOW_API_KEY",
                "zhipu": "ZHIPU_API_KEY"
            }
            return api_key, env_var_map.get(backend, "OPENAI_API_KEY")
        except Exception:
            pass

    return "", ""


def load_config():
    """
    加载配置，优先级：
    1. 命令行参数 (--uid, --base-dir)
    2. 环境变量 (MM_UID, MM_BASE_DIR, MM_DEFAULT_SCOPE)
    3. ~/.memory-manager/config.json
    4. ./.mm.json
    5. ~/.mm.json
    6. 默认值
    """
    # OpenClaw 优先路径
    openclaw_memory_path = str(Path.home() / ".openclaw" / "memory")
    default_memory_path = str(Path.home() / ".memory-manager" / "memory")
    
    config = {
        "uid": os.environ.get("MM_UID") or os.environ.get("USER") or os.environ.get("USERNAME") or "user",
        "base_dir": os.environ.get("MM_BASE_DIR", openclaw_memory_path if Path(openclaw_memory_path).exists() else default_memory_path),
        "scope": os.environ.get("MM_DEFAULT_SCOPE", "private"),
        "version": VERSION,
    }

    # 1. OpenClaw 配置文件（优先）
    openclaw_config_path = Path.home() / ".openclaw" / "memory" / ".memory_config.json"
    if openclaw_config_path.exists():
        try:
            with open(openclaw_config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            # 更新配置，但保留命令行参数的覆盖能力
            for key in ["uid", "base_dir", "scope", "backend"]:
                if key in file_config and key not in os.environ:
                    config[key] = file_config[key]
        except Exception:
            pass
    
    # 2. 全局配置文件
    global_config_path = Path.home() / ".memory-manager" / "config.json"
    if global_config_path.exists():
        try:
            with open(global_config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            # 更新配置，但保留命令行参数的覆盖能力
            for key in ["uid", "base_dir", "scope", "backend"]:
                if key in file_config and key not in os.environ:
                    config[key] = file_config[key]
        except Exception:
            pass

    # 2. 本地配置文件
    config_paths = [
        Path.cwd() / ".mm.json",
        Path.home() / ".mm.json",
    ]

    for path in config_paths:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                if "default" in file_config:
                    for key, value in file_config["default"].items():
                        # 环境变量优先级更高
                        env_key = f"MM_{key.upper()}" if key != "base_dir" else "MM_BASE_DIR"
                        if key not in os.environ and env_key not in os.environ:
                            config[key] = value
                elif isinstance(file_config, dict):
                    for key, value in file_config.items():
                        env_key = f"MM_{key.upper()}" if key != "base_dir" else "MM_BASE_DIR"
                        if key not in os.environ and env_key not in os.environ:
                            config[key] = value
            except Exception:
                pass

    return config


# ══════════════════════════════════════════════════════════════
#  命令实现
# ══════════════════════════════════════════════════════════════

def cmd_search(args, config):
    """语义搜索"""
    from memory_search import get_db_path, connect_db, search_vectors, format_row
    import numpy as np
    from embed_backends import get_embedding

    base_dir = args.base_dir or config["base_dir"]
    db_path = get_db_path(base_dir)

    if not os.path.exists(db_path):
        print(f"❌ 向量数据库不存在: {db_path}")
        print("   请先运行: mm embed")
        return 1

    conn = connect_db(db_path)
    scope = "shared" if args.shared else ("all" if args.all else config["scope"])

    print(f"\n🔍 搜索: \"{args.query}\"")
    print(f"   范围: {scope} | 用户: {config['uid']}\n")

    try:
        query_emb = get_embedding(args.query, db_path=db_path)
    except Exception as e:
        print(f"  ❌ 向量生成失败: {e}")
        return 1

    results, cols = search_vectors(
        conn, query_emb, config["uid"], scope, args.level, args.top_k, args.min_score
    )
    conn.close()

    if not results:
        print("  😕 没有找到相关记忆")
        return 0

    print(f"  ✅ 找到 {len(results)} 条相关记忆:\n")
    for i, (combined, sim_score, importance, row) in enumerate(results, 1):
        print(f"  ── 结果 {i}/{len(results)} ──")
        print(format_row(combined, sim_score, importance, row, cols))

    return 0


def cmd_embed(args, config):
    """更新向量索引"""
    from memory_embed import embed_all

    base_dir = args.base_dir or config["base_dir"]
    scope = "shared" if args.shared else ("all" if args.all else config["scope"])

    print(f"\n📦 正在生成向量索引...")
    print(f"   用户: {config['uid']} | 范围: {scope} | 目录: {base_dir}")

    try:
        embed_all(base_dir, config["uid"], scope, args.dry_run, args.rebuild)
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return 1

    return 0


def cmd_stats(args, config):
    """查看统计"""
    from memory_search import get_db_path, connect_db, print_stats

    base_dir = args.base_dir or config["base_dir"]
    db_path = get_db_path(base_dir)

    if not os.path.exists(db_path):
        print(f"❌ 向量数据库不存在: {db_path}")
        return 1

    conn = connect_db(db_path)
    print_stats(conn, db_path=db_path)
    conn.close()
    return 0


def cmd_insight(args, config):
    """AI 自我总结"""
    from memory_insight import generate_insight

    base_dir = args.base_dir or config["base_dir"]

    report_type = "daily" if args.daily else ("weekly" if args.weekly else "summary")

    print(f"\n🧠 正在生成{'每日' if args.daily else '每周' if args.weekly else '综合'}洞察报告...")

    try:
        report = generate_insight(base_dir, config["uid"], report_type)
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)

        # 可选：保存到记忆文件
        if args.save:
            save_path = Path(base_dir) / "users" / config["uid"] / "weekly" / f"insight_{report_type}.md"
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(f"# AI 洞察报告 - {report_type}\n\n")
                f.write(report)
            print(f"\n💾 已保存到: {save_path}")

    except Exception as e:
        print(f"  ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


def cmd_log(args, config):
    """快速记录记忆"""
    from memory_embed import parse_sections, make_content_hash, make_chunk_id
    import json
    from datetime import datetime

    base_dir = args.base_dir or config["base_dir"]
    level = args.level or "L1"  # 默认临时记忆

    # 确定保存路径
    level_dir_map = {
        "L1": "daily",
        "L2": "weekly",
        "L3": "permanent",
    }
    subdir = level_dir_map.get(level, "daily")
    save_dir = Path(base_dir) / "users" / config["uid"] / subdir
    save_dir.mkdir(parents=True, exist_ok=True)

    # 生成文件名
    now = datetime.now()
    fname = now.strftime("%Y-%m-%d.md")
    fpath = save_dir / fname

    # 追加内容
    timestamp = now.strftime("%H:%M")
    entry = f"\n## [{timestamp}] {args.text}\n\n{args.note or ''}\n"

    if fpath.exists():
        with open(fpath, "a", encoding="utf-8") as f:
            f.write(entry)
    else:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(f"# {now.strftime('%Y-%m-%d')}\n")
            f.write(entry)

    print(f"✅ 已记录: {entry[:50].strip()}...")
    print(f"   路径: {fpath}")
    print(f"   层级: {level}")

    # 可选：立即生成向量
    if args.embed:
        cmd_embed(argparse.Namespace(
            base_dir=base_dir, shared=False, all=False,
            dry_run=False, rebuild=False
        ), config)

    return 0


def cmd_related(args, config):
    """查看关联记忆"""
    from memory_search import get_db_path, connect_db
    import json

    base_dir = args.base_dir or config["base_dir"]
    db_path = get_db_path(base_dir)

    if not os.path.exists(db_path):
        print(f"❌ 向量数据库不存在")
        return 1

    conn = connect_db(db_path)
    c = conn.cursor()

    c.execute("SELECT chunk_id, title, related_ids FROM memory_embeddings WHERE chunk_id = ?", (args.chunk_id,))
    row = c.fetchone()

    if not row:
        print(f"❌ 未找到记忆: {args.chunk_id}")
        conn.close()
        return 1

    chunk_id, title, related_ids = row
    print(f"\n🔗 关联记忆: {title}\n")

    if not related_ids or related_ids == "[]":
        print("  无关联记忆")
        conn.close()
        return 0

    try:
        related = json.loads(related_ids)
    except:
        print("  关联数据损坏")
        conn.close()
        return 1

    if not related:
        print("  无关联记忆")
        conn.close()
        return 0

    placeholders = ",".join("?" * len(related))
    c.execute(f"SELECT chunk_id, title, level, importance_score FROM memory_embeddings WHERE chunk_id IN ({placeholders})", related)
    rows = c.fetchall()

    print(f"  共 {len(rows)} 条关联记忆:\n")
    for cid, t, level, imp in rows:
        imp_bar = "█" * int(imp / 10) + "░" * (10 - int(imp / 10))
        print(f"  [{level}] {t}")
        print(f"         {imp_bar} ({imp:.0f})")
        print(f"         ID: {cid}\n")

    conn.close()
    return 0


def cmd_top(args, config):
    """查看最重要记忆"""
    from memory_search import get_db_path, connect_db

    base_dir = args.base_dir or config["base_dir"]
    db_path = get_db_path(base_dir)

    if not os.path.exists(db_path):
        print(f"❌ 向量数据库不存在")
        return 1

    conn = connect_db(db_path)
    c = conn.cursor()

    scope = "shared" if args.shared else ("all" if args.all else config["scope"])
    where = f"WHERE scope = '{scope}'" if scope != "all" else ""

    c.execute(f"""
        SELECT chunk_id, title, level, importance_score, mtime
        FROM memory_embeddings
        {where}
        ORDER BY importance_score DESC
        LIMIT ?
    """, (args.n,))

    rows = c.fetchall()
    conn.close()

    if not rows:
        print("  没有记录")
        return 0

    print(f"\n⭐ Top {args.n} 最重要记忆 ({scope}):\n")
    for i, (cid, title, level, imp, mtime) in enumerate(rows, 1):
        imp_bar = "█" * int(imp / 10) + "░" * (10 - int(imp / 10))
        print(f"  {i}. [{level}] {title}")
        print(f"     {imp_bar} {imp:.0f}")
        print(f"     {cid}")
        print()

    return 0


def cmd_onboard(args, config):
    """首次使用引导（OpenClaw专用）"""
    from memory_onboard import main as onboard_main
    import sys

    print("🚀 OpenClaw 记忆系统初始化")
    print("==========================")
    
    # OpenClaw 专用配置
    if args.openclaw:
        print("📦 使用 OpenClaw 专用配置...")
        # 设置 OpenClaw 默认路径
        openclaw_path = str(Path.home() / ".openclaw" / "memory")
        print(f"   记忆存储路径: {openclaw_path}")
        
        # 传递参数
        sys.argv = ["memory_onboard.py"]
        sys.argv.extend(["--path", openclaw_path])
        if args.silent:
            sys.argv.append("--silent")
        sys.argv.append("--openclaw")  # OpenClaw 专用标记
    else:
        # 标准配置
        sys.argv = ["memory_onboard.py"]
        if args.silent:
            sys.argv.append("--silent")
        if config.get("uid"):
            sys.argv.extend(["--uid", config["uid"]])
        if config.get("base_dir"):
            sys.argv.extend(["--path", config["base_dir"]])

    onboard_main()
    return 0


def cmd_version(args, config):
    """显示版本信息"""
    print(f"Memory Manager v{VERSION} - OpenClaw 专用版")
    print(f"配置目录: {Path.home() / '.openclaw/memory'}")
    print(f"当前路径: {config.get('base_dir', '.')}")
    print(f"用户 ID: {config.get('uid', '未设置')}")
    return 0


def cmd_lint(args, config):
    """检查记忆文件规范"""
    from pathlib import Path
    import re

    base_dir = Path(args.base_dir or config["base_dir"])
    errors = []
    warnings = []

    # 规范常量
    MAX_FILENAME_LEN = 64
    MAX_FILE_SIZE = 10 * 1024  # 10KB
    FORBIDDEN_CHARS = [':', '/', '\\', '*', '?', '"', '<', '>', '|']
    REQUIRED_FIELDS = ['type:', 'created:', 'tags:', 'scope:']

    def check_file(md_file):
        nonlocal errors, warnings

        # 文件名检查
        name = md_file.name
        if len(name) > MAX_FILENAME_LEN:
            errors.append(f"{md_file}: 文件名超过 {MAX_FILENAME_LEN} 字符")
        for char in FORBIDDEN_CHARS:
            if char in name:
                errors.append(f"{md_file}: 文件名包含禁止字符 '{char}'")

        # 文件大小检查
        if md_file.stat().st_size > MAX_FILE_SIZE:
            errors.append(f"{md_file}: 文件超过 {MAX_FILE_SIZE//1024}KB")

        # Frontmatter 检查
        try:
            content = md_file.read_text(encoding="utf-8")
            if not content.startswith('---'):
                errors.append(f"{md_file}: 缺少 frontmatter")
                return

            # 提取 frontmatter
            end = content.find('---', 3)
            if end == -1:
                errors.append(f"{md_file}: frontmatter 未闭合")
                return

            fm = content[3:end]
            for field in REQUIRED_FIELDS:
                if field not in fm:
                    errors.append(f"{md_file}: 缺少必需字段 '{field}'")

            # 检查 tags 是否为空
            if 'tags: []' in fm or 'tags:' == fm.strip().split('\n')[-1].strip():
                warnings.append(f"{md_file}: tags 为空")

        except Exception as e:
            errors.append(f"{md_file}: 读取失败 - {e}")

    # 扫描所有 .md 文件
    md_files = list(base_dir.rglob("*.md"))
    print(f"\n🔍 检查 {len(md_files)} 个记忆文件...")

    for md_file in md_files:
        # 跳过非记忆文件
        if any(skip in str(md_file) for skip in [".git", "node_modules", "__pycache__"]):
            continue
        check_file(md_file)

    # 输出结果
    print(f"\n{'─' * 40}")
    if errors:
        print(f"❌ 发现 {len(errors)} 个错误:")
        for e in errors[:20]:  # 最多显示20个
            print(f"   {e}")
        if len(errors) > 20:
            print(f"   ... 还有 {len(errors) - 20} 个错误")
    else:
        print("✅ 没有错误")

    if warnings:
        print(f"\n⚠️  发现 {len(warnings)} 个警告:")
        for w in warnings[:10]:
            print(f"   {w}")
        if len(warnings) > 10:
            print(f"   ... 还有 {len(warnings) - 10} 个警告")

    return 1 if errors else 0


def cmd_new(args, config):
    """创建新记忆文件"""
    from pathlib import Path
    from datetime import datetime

    base_dir = Path(args.base_dir or config["base_dir"])
    level_map = {"daily": "L1", "weekly": "L2", "permanent": "L3"}
    subdir_map = {
        "L1": "users/{uid}/daily",
        "L2": "users/{uid}/weekly",
        "L3": "users/{uid}/permanent",
    }

    level = level_map.get(args.level, "L1")
    save_dir = base_dir / subdir_map[level].format(uid=config["uid"])

    # 创建子目录
    save_dir.mkdir(parents=True, exist_ok=True)

    # 生成文件名
    now = datetime.now()
    type_prefix = args.type or "mem"
    safe_desc = re.sub(r'[^\w\-]', '_', args.desc)[:30]
    fname = f"{type_prefix}_{safe_desc}_{now.strftime('%Y%m%d%H%M')}.md"
    fpath = save_dir / fname

    # 模板内容
    template = f"""---
type: {type_prefix}
created: {now.strftime('%Y-%m-%d')}
updated: {now.strftime('%Y-%m-%d')}
tags: [{args.tag or 'untagged'}]
scope: private
author: {config["uid"]}
status: active
importance: 3
---

# {args.desc}

## 概要
{args.desc}

## 详细内容
{args.content or '（待补充）'}

## 相关记忆
- （关联记忆ID）
"""

    fpath.write_text(template, encoding="utf-8")
    print(f"✅ 创建记忆文件: {fpath}")
    print(f"   类型: {level} | 标签: {args.tag or 'untagged'}")

    return 0


def cmd_clean(args, config):
    """清理过期/无效记忆"""
    from pathlib import Path
    from datetime import datetime, timedelta

    base_dir = Path(args.base_dir or config["base_dir"])
    dry_run = args.dry_run
    deleted = []
    archived = []

    now = datetime.now()

    def process_file(md_file):
        nonlocal deleted, archived

        try:
            content = md_file.read_text(encoding="utf-8")

            # 提取 created 日期
            import re
            match = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', content)
            if not match:
                if args.orphans:
                    deleted.append(md_file)
                return

            created = datetime.strptime(match.group(1), '%Y-%m-%d')
            days_old = (now - created).days

            # 归档逻辑
            if args.archive and days_old > 180:
                archive_dir = md_file.parent.parent.parent / "archive"
                archive_dir.mkdir(exist_ok=True)
                new_path = archive_dir / md_file.name
                if not dry_run:
                    md_file.rename(new_path)
                archived.append(md_file)

            # 删除逻辑
            elif args.purge and days_old > 365:
                deleted.append(md_file)

        except Exception as e:
            pass

    # 扫描所有 .md 文件
    md_files = list(base_dir.rglob("*.md"))
    print(f"\n🧹 扫描 {len(md_files)} 个文件...")

    for md_file in md_files:
        if any(skip in str(md_file) for skip in [".git", "node_modules", "__pycache__", "/archive/"]):
            continue
        process_file(md_file)

    # 执行操作
    if dry_run:
        print(f"\n🔍 预览模式 (--dry-run):")
    else:
        print(f"\n🗑️  执行清理:")

    if archived:
        print(f"   📦 归档: {len(archived)} 个文件")
        for f in archived[:5]:
            print(f"      {f}")
        if len(archived) > 5:
            print(f"      ... 还有 {len(archived) - 5} 个")

    if deleted:
        print(f"   🗑️  删除: {len(deleted)} 个文件")
        for f in deleted[:5]:
            print(f"      {f}")
        if len(deleted) > 5:
            print(f"      ... 还有 {len(deleted) - 5} 个")

    if not archived and not deleted:
        print("   ✅ 没有需要清理的文件")

    # 实际删除
    if not dry_run and deleted:
        confirm = input(f"\n⚠️ 确认删除 {len(deleted)} 个文件? (y/N): ").strip().lower()
        if confirm == 'y':
            for f in deleted:
                f.unlink()
            print(f"✅ 已删除 {len(deleted)} 个文件")
        else:
            print("已取消")

    return 0


# ══════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="mm - Memory Manager 简化命令",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # 全局选项
    parser.add_argument("--version", action="store_true", help="显示版本")
    parser.add_argument("--base-dir", help="记忆仓库目录")
    parser.add_argument("--uid", help="用户ID")

    # 解析参数
    if len(sys.argv) > 1 and sys.argv[1] in ["lint", "new", "clean", "search", "embed", "stats", "insight", "log", "related", "top", "onboard", "version"]:
        # 子命令模式：不解析全局选项，让子命令解析器处理
        args = argparse.Namespace(version=False, base_dir=None, uid=None)
    else:
        # 全局选项模式
        args = parser.parse_args()
    
    # 显示版本
    if args.version:
        print(f"Memory Manager v{VERSION}")
        return 0

    # 显示版本
    if args.version:
        print(f"Memory Manager v{VERSION}")
        return 0

    # 解析子命令
    parser2 = argparse.ArgumentParser(prog="mm", description="mm - Memory Manager")
    subparsers = parser2.add_subparsers(dest="command", help="可用命令")

    # onboard 命令 (新用户引导)
    p_onboard = subparsers.add_parser("onboard", help="首次使用引导 (添加 --openclaw 使用 OpenClaw 专用配置)")
    p_onboard.add_argument("--silent", action="store_true", help="静默模式")
    p_onboard.add_argument("--openclaw", action="store_true", help="使用 OpenClaw 专用配置")

    # search 命令
    p_search = subparsers.add_parser("search", help="语义搜索记忆")
    p_search.add_argument("query", help="搜索内容")
    p_search.add_argument("--shared", action="store_true", help="搜索公共记忆")
    p_search.add_argument("--all", action="store_true", help="搜索所有记忆")
    p_search.add_argument("--level", nargs="*", choices=["L1", "L2", "L3"], help="限定层级")
    p_search.add_argument("--top-k", type=int, default=10)
    p_search.add_argument("--min-score", type=float, default=0.55)

    # embed 命令
    p_embed = subparsers.add_parser("embed", help="更新向量索引")
    p_embed.add_argument("--shared", action="store_true", help="仅公共记忆")
    p_embed.add_argument("--all", action="store_true", help="所有记忆")
    p_embed.add_argument("--rebuild", action="store_true", help="全量重建")
    p_embed.add_argument("--dry-run", action="store_true", help="预览")

    # stats 命令
    subparsers.add_parser("stats", help="查看统计")

    # insight 命令
    p_insight = subparsers.add_parser("insight", help="AI 自我总结")
    p_insight.add_argument("--daily", action="store_true", help="每日洞察")
    p_insight.add_argument("--weekly", action="store_true", help="每周洞察")
    p_insight.add_argument("--save", action="store_true", help="保存到记忆文件")

    # log 命令
    p_log = subparsers.add_parser("log", help="快速记录")
    p_log.add_argument("text", help="记录内容")
    p_log.add_argument("--note", default="", help="详细说明")
    p_log.add_argument("--level", choices=["L1", "L2", "L3"], help="记忆层级")
    p_log.add_argument("--embed", action="store_true", help="立即生成向量")

    # related 命令
    p_related = subparsers.add_parser("related", help="查看关联记忆")
    p_related.add_argument("chunk_id", help="记忆 ID")

    # top 命令
    p_top = subparsers.add_parser("top", help="查看最重要记忆")
    p_top.add_argument("--n", type=int, default=10, help="数量")
    p_top.add_argument("--shared", action="store_true", help="公共记忆")
    p_top.add_argument("--all", action="store_true", help="所有记忆")

    # version 命令
    subparsers.add_parser("version", help="显示版本信息")

    # lint 命令
    p_lint = subparsers.add_parser("lint", help="检查记忆文件规范")
    p_lint.add_argument("--fix", action="store_true", help="自动修复可修复的问题")

    # new 命令
    p_new = subparsers.add_parser("new", help="创建新记忆文件")
    p_new.add_argument("--type", "-t", default="mem", help="类型: idea/dec/learn/ref/proj/task/mem/daily/bug")
    p_new.add_argument("--level", "-l", default="daily", choices=["daily", "weekly", "permanent"], help="记忆层级")
    p_new.add_argument("--tag", help="标签")
    p_new.add_argument("--desc", "-d", required=True, help="简短描述")
    p_new.add_argument("--content", "-c", default="", help="详细内容")

    # clean 命令
    p_clean = subparsers.add_parser("clean", help="清理过期/无效记忆")
    p_clean.add_argument("--dry-run", action="store_true", help="预览模式")
    p_clean.add_argument("--archive", action="store_true", help="归档 180 天以上")
    p_clean.add_argument("--purge", action="store_true", help="删除 365 天以上")
    p_clean.add_argument("--orphans", action="store_true", help="删除无 created 日期的文件")

    args2 = parser2.parse_args()

    if not args2.command:
        # 没有子命令，打印帮助
        parser2.print_help()
        print("\n💡 提示: mm search <关键词> 可以直接搜索")
        return 0

    # 加载配置
    config = load_config()
    if args.uid:
        config["uid"] = args.uid
    if args.base_dir:
        config["base_dir"] = args.base_dir

    # 执行命令
    commands = {
        "search": cmd_search,
        "embed": cmd_embed,
        "stats": cmd_stats,
        "insight": cmd_insight,
        "log": cmd_log,
        "related": cmd_related,
        "top": cmd_top,
        "onboard": cmd_onboard,
        "version": cmd_version,
        "lint": cmd_lint,
        "new": cmd_new,
        "clean": cmd_clean,
    }

    if args2.command in commands:
        return commands[args2.command](args2, config)
    else:
        print(f"❌ 未知命令: {args2.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
