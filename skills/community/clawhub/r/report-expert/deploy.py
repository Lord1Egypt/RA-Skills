#!/usr/bin/env python3
"""报告专家 — CLI 入口

v2.0.0: 仅 Cloudflare Pages 部署模式。
五模块架构：adapter(适配) → report(生产) → html_lint(检查修复) → site(维护部署) → verify(验证)
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "deploy":
        cmd_deploy()
    elif cmd == "produce":
        cmd_produce()
    elif cmd == "publish":
        cmd_publish()
    elif cmd == "add":
        cmd_add()
    elif cmd == "remove":
        cmd_remove()
    elif cmd == "rebuild_index":
        cmd_rebuild_index()
    elif cmd == "update":
        cmd_update()
    elif cmd == "verify":
        cmd_verify()
    elif cmd == "sync":
        cmd_sync()
    elif cmd == "check":
        cmd_check()
    else:
        print(f"❌ 未知命令: {cmd}")
        print_usage()
        sys.exit(1)


def print_usage():
    print("报告专家 v2.0.0 — Cloudflare Pages 部署")
    print("五模块架构: adapter(适配) → report(生产) → html_lint(检查修复) → site(维护部署) → verify(验证)")
    print()
    print("完整流程命令:")
    print("  deploy <category> <source> [--title T] [--desc D]  适配+生产+部署+验证")
    print()
    print("分步命令（按模块）：")
    print()
    print("  [输入适配]")
    print("  produce <category> <source> [--title T] [--desc D]  自动适配输入类型并生产")
    print("  （支持 .html / .md / URL / 纯文本，自动检测类型）")
    print()
    print("  [小站维护]")
    print("  publish                                                部署 dist 到 CF")
    print("  sync                                                   从 CF 线上同步缺失文件到 dist")
    print("  add <filename> --title T --desc D --category C [--url U]  添加外部页面")
    print("  remove <category/filename>                             删除页面+索引+部署")
    print("  rebuild_index                                         重建索引+首页")
    print("  update                                                 用最新模板更新所有页面")
    print()
    print("  [验证修复]")
    print("  verify                                                 验证部署结果")
    print("  verify <category> <filename>                           验证指定报告页")
    print()
    print("  [配置]")
    print("  check                                                  检查配置是否齐全")


def _parse_title_desc(start_idx):
    """从 sys.argv[start_idx:] 解析 --title 和 --desc 参数"""
    title = desc = None
    i = start_idx
    while i < len(sys.argv):
        if sys.argv[i] == '--title':
            if i+1 < len(sys.argv): title = sys.argv[i+1]; i += 2
            else: print("❌ --title 需要值"); sys.exit(1)
        elif sys.argv[i] == '--desc':
            if i+1 < len(sys.argv): desc = sys.argv[i+1]; i += 2
            else: print("❌ --desc 需要值"); sys.exit(1)
        else:
            print(f"⚠️ 未知参数: {sys.argv[i]}")
            i += 1
    return title, desc


# ── 完整流程 ──

def cmd_deploy():
    if len(sys.argv) < 4:
        print("❌ 用法: deploy <category> <source> [--title T] [--desc D]")
        print("   source 支持: .html / .md 文件路径, URL, 纯文本文件")
        sys.exit(1)
    from lib.adapter import adapt
    from lib.site import full_deploy
    category = sys.argv[2]
    source = sys.argv[3]
    title, desc = _parse_title_desc(4)
    try:
        html_content, adapted_title, input_type = adapt(source, title)
        if not title:
            title = adapted_title
        print(f"  📥 输入类型: {input_type}")
        source_stem = Path(source).stem if not source.startswith('http') else 'web-report'
        tmp_dir = BASE_DIR / "dist" / category
        tmp_dir.mkdir(parents=True, exist_ok=True)
        tmp_path = tmp_dir / f"_adapted_{source_stem}.html"
        tmp_path.write_text(html_content, 'utf-8')
        result = full_deploy(category, str(tmp_path), title, desc)
        tmp_path.unlink(missing_ok=True)
        if not result:
            print("❌ 部署失败")
            sys.exit(1)
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"❌ {e}")
        sys.exit(1)


# ── 报告生产 ──

def cmd_produce():
    if len(sys.argv) < 4:
        print("❌ 用法: produce <category> <source> [--title T] [--desc D]")
        print("   source 支持: .html / .md 文件路径, URL, 纯文本文件")
        sys.exit(1)
    from lib.adapter import adapt
    from lib.report import produce
    category = sys.argv[2]
    source = sys.argv[3]
    title, desc = _parse_title_desc(4)
    try:
        html_content, adapted_title, input_type = adapt(source, title)
        if not title:
            title = adapted_title
        print(f"  📥 输入类型: {input_type}")
        # Write adapted HTML to temp file with meaningful name
        import tempfile
        # Use source file stem as the temp file prefix for meaningful naming
        source_stem = Path(source).stem if not source.startswith('http') else 'web-report'
        tmp_dir = BASE_DIR / "dist" / category
        tmp_dir.mkdir(parents=True, exist_ok=True)
        tmp_path = tmp_dir / f"_adapted_{source_stem}.html"
        tmp_path.write_text(html_content, 'utf-8')
        produce(category, str(tmp_path), title, desc)
        # Clean up temp file
        tmp_path.unlink(missing_ok=True)
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"❌ {e}")
        sys.exit(1)


# ── 小站维护 ──

def cmd_publish():
    from lib.site import publish
    publish()


def cmd_add():
    if len(sys.argv) < 3:
        print("❌ 用法: add <filename> --title T --desc D --category C [--url U]")
        sys.exit(1)
    from lib.site import add_to_index
    filename = sys.argv[2]
    title = desc = category = url = None
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--title' and i+1 < len(sys.argv): title = sys.argv[i+1]; i += 2
        elif sys.argv[i] == '--desc' and i+1 < len(sys.argv): desc = sys.argv[i+1]; i += 2
        elif sys.argv[i] == '--category' and i+1 < len(sys.argv): category = sys.argv[i+1]; i += 2
        elif sys.argv[i] == '--url' and i+1 < len(sys.argv): url = sys.argv[i+1]; i += 2
        else: i += 1
    if not title or not category:
        print("❌ --title 和 --category 是必须的")
        sys.exit(1)
    if not desc:
        print("⚠️ --desc 未提供，将使用空描述")
    add_to_index(filename, title, desc, category, url)


def cmd_remove():
    """删除页面：从索引移除 + 删除 dist 文件 + 重建索引 + 部署"""
    if len(sys.argv) < 3:
        print("❌ 用法: remove <category/filename>")
        print("   示例: remove analysis/2026-06-17-test-report.html")
        sys.exit(1)
    from lib.site import remove_from_index, rebuild_index, publish
    filename = sys.argv[2]
    ok = remove_from_index(filename)
    if ok:
        rebuild_index()
        publish()


def cmd_rebuild_index():
    from lib.site import rebuild_index
    rebuild_index()


def cmd_update():
    from lib.site import update_pages
    update_pages()


# ── 验证修复 ──

def cmd_verify():
    from lib.verify import verify_deployment
    from lib.config import SITE_URL
    print(f"🔍 验证部署站点: {SITE_URL}")
    if len(sys.argv) >= 4:
        category = sys.argv[2]
        filename = sys.argv[3]
        verify_deployment(category, filename)
    else:
        verify_deployment()


def cmd_sync():
    from lib.site import sync_from_cf
    synced, missing = sync_from_cf()
    if synced:
        from lib.site import rebuild_index
        rebuild_index()

def cmd_check():
    from lib.config import check_config
    check_config()


if __name__ == "__main__":
    main()