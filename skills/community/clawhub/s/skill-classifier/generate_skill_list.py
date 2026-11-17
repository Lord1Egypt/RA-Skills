#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
技能列表生成主脚本
整合所有模块，支持多种输出格式、过滤选项、使用统计、依赖图、
汉化报告、更新检查、批量启停与远端推送
"""
import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import logging

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.openclaw import get_skills_from_cli, get_activated_skills, get_not_activated_skills, get_skill_status
from data.filesystem import get_dir_to_name_map
from data.meta_reader import load_all_meta, get_meta_info
from data.usage import get_usage_stats
from data.updates import check_updates
from data.deps import get_dependency_edges
from data.toggle import set_enabled, verify_with_cli
from classifier.category_map import get_category
from classifier.auto_classify import find_duplicate_skills
from exporter.markdown import export_markdown
from exporter.json_exporter import export_json
from exporter.html_exporter import export_html
from exporter import feishu, notion
from utils.diff import compare_skills, save_snapshot, get_diff_summary
from utils.config import OUTPUT_DIR, CACHE_DIR, ensure_dirs
from utils.translator import translate_description, extract_untranslated

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='OpenClaw 技能列表生成工具')

    # 输出格式
    parser.add_argument('--format', '-f',
                       choices=['markdown', 'json', 'html', 'all'],
                       default='markdown',
                       help='输出格式 (默认: markdown)')

    # 输出目录
    parser.add_argument('--output', '-o',
                       default=OUTPUT_DIR,
                       help=f'输出目录 (默认: {OUTPUT_DIR})')

    # 过滤选项
    parser.add_argument('--filter', '-F',
                       default='all',
                       choices=['all', 'activated', 'not_activated'],
                       help='技能状态过滤 (默认: all)')

    # 搜索过滤
    parser.add_argument('--search', '-s',
                       help='按关键词搜索技能名称')

    # 分类过滤
    parser.add_argument('--category', '-c',
                       help='按大类过滤技能')

    # 增量更新
    parser.add_argument('--incremental', '-i',
                       action='store_true',
                       help='仅输出变化的技能')

    # 不保存快照
    parser.add_argument('--no-snapshot',
                       action='store_true',
                       help='不保存本次快照')

    # 检测重复技能
    parser.add_argument('--check-duplicates',
                       action='store_true',
                       help='检测功能重复的技能')

    # 简洁输出
    parser.add_argument('--quiet', '-q',
                       action='store_true',
                       help='简洁输出模式')

    # 使用统计
    parser.add_argument('--usage', action='store_true',
                       help='输出中包含使用次数列（state 库/curator）')

    # 依赖关系图
    parser.add_argument('--deps', action='store_true',
                       help='生成缺失依赖关系图（md=mermaid，html=SVG）')

    # 汉化报告
    parser.add_argument('--i18n-report', action='store_true',
                       help='列出未汉化的英文词（辅助扩充词表）')

    # 更新检查
    parser.add_argument('--check-updates', action='store_true',
                       help='检查可更新技能（只报告，不自动升级）')

    # 批量启停
    parser.add_argument('--enable',
                       help='批量启用技能（逗号分隔名称，写 skills.entries.<名>.enabled）')
    parser.add_argument('--disable',
                       help='批量禁用技能（逗号分隔名称，写 skills.entries.<名>.enabled=false）')

    # 远端推送
    parser.add_argument('--push',
                       help='把本次导出的 Markdown 推送到远端文档（feishu/notion，逗号分隔）')

    return parser.parse_args()


def enrich_skill_data(skills: List[Dict[str, Any]], meta_data: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    丰富技能数据（添加版本、作者、状态、分类等）

    Args:
        skills: 原始技能列表
        meta_data: 元数据字典

    Returns:
        丰富后的技能列表
    """
    enriched = []
    dir_to_name = get_dir_to_name_map()

    for skill in skills:
        name = skill.get('name', '')

        # 尝试映射目录名到技能名
        if name in dir_to_name:
            name = dir_to_name[name]

        # 获取版本和作者
        version, author = get_meta_info(name, meta_data)

        # 获取分类
        big_category, sub_category = get_category(name)

        enriched_skill = {
            **skill,
            'name': name,
            'status': get_skill_status(skill),
            'version': version,
            'author': author,
            'big_category': big_category,
            'sub_category': sub_category,
            'description': translate_description(skill.get('description', ''))
        }
        enriched.append(enriched_skill)

    return enriched


def filter_skills(skills: List[Dict[str, Any]],
                 search_term: str = None,
                 category: str = None) -> List[Dict[str, Any]]:
    """
    过滤技能列表

    Args:
        skills: 技能列表
        search_term: 搜索关键词
        category: 分类过滤

    Returns:
        过滤后的技能列表
    """
    filtered = skills

    if search_term:
        search_lower = search_term.lower()
        filtered = [
            s for s in filtered
            if search_lower in s['name'].lower() or
               search_lower in s.get('description', '').lower()
        ]

    if category:
        filtered = [
            s for s in filtered
            if get_category(s['name'])[0] == category
        ]

    return filtered


def _split_names(comma: str) -> List[str]:
    return [n.strip() for n in comma.split(',') if n.strip()]


def _run_toggle(comma: str, enabled: bool, known_names) -> int:
    """执行批量启停：名称核对 → 写配置（自动备份）→ CLI 验证"""
    names = _split_names(comma)
    unknown = [n for n in names if n not in known_names]
    if unknown:
        logger.error(f"未知技能名（先在 skills list 核对）: {unknown}")
        return 1
    backup, changed = set_enabled(names, enabled)
    action = '✅ 已启用' if enabled else '🚫 已禁用'
    print(f"{action}: {', '.join(changed)}")
    print(f"   备份: {backup}")
    failed = verify_with_cli(names, enabled)
    if failed:
        print("   ⚠️ 验证未生效:")
        for f in failed:
            print(f"   - {f}")
    else:
        print("   ✅ CLI 验证通过")
    return 0


def main():
    """主函数"""
    args = parse_args()

    # 输出目录：原始输入含 .. 路径段直接拒绝，规范化后自动创建
    if '..' in args.output.replace('\\', '/').split('/'):
        logger.error(f"非法输出目录（不允许 .. 路径段）: {args.output}")
        return 1
    out_dir = os.path.normpath(args.output)
    ensure_dirs([out_dir, CACHE_DIR])
    args.output = out_dir

    if not args.quiet:
        print("📦 OpenClaw 技能列表生成工具")
        print("=" * 50)

    # 1. 获取数据
    if not args.quiet:
        print("\n🔍 正在获取技能数据...")

    cli_skills = get_skills_from_cli()
    if cli_skills is None:
        logger.error("无法获取技能列表，请检查 OpenClaw 是否正常安装")
        return 1

    # 2. 互斥动作：批量启停（写主配置，改完即退出）
    if args.enable or args.disable:
        known = {s.get('name', '') for s in cli_skills}
        rc = 0
        if args.enable:
            rc = _run_toggle(args.enable, True, known)
        if rc == 0 and args.disable:
            rc = _run_toggle(args.disable, False, known)
        return rc

    # 3. 互斥动作：更新检查（只报告，不升级）
    if args.check_updates:
        rows = check_updates(cli_skills)
        print(f"\n🔄 更新检查（共 {len(rows)} 项）")
        for r in rows:
            mark = {'up_to_date': '✅', 'outdated': '⬆️ ', 'managed': '🔧'}.get(r['status'], '❓')
            print(f"   {mark} [{r['track']}] {r['skill']}: {r['detail']}")
        if not rows:
            print("   未发现需要关注的技能")
        return 0

    # 4. 加载元数据
    meta_data = load_all_meta()

    # 5. 丰富数据
    all_skills = enrich_skill_data(cli_skills, meta_data)

    if not args.quiet:
        print(f"   共获取 {len(all_skills)} 个技能")

    # 6. 使用统计与依赖边（按需）
    usage_stats = get_usage_stats() if args.usage else None
    if args.usage and not args.quiet:
        print(f"   使用统计: {len(usage_stats)} 条")
    deps_edges = get_dependency_edges(all_skills) if args.deps else None

    # 7. 汉化报告（不中断导出）
    if args.i18n_report:
        words = extract_untranslated([s.get('description', '') for s in all_skills])
        report_path = os.path.join(args.output, "未汉化词表.txt")
        Path(report_path).write_text('\n'.join(words), encoding='utf-8')
        print(f"\n🌍 未汉化英文词 {len(words)} 个，已写入 {report_path}")
        if not args.quiet:
            print("   " + ' '.join(words[:30]) + (' ...' if len(words) > 30 else ''))

    # 8. 检测重复技能
    if args.check_duplicates:
        if not args.quiet:
            print("\n🔍 检测重复技能...")
        duplicates = find_duplicate_skills(all_skills)
        if duplicates:
            print(f"\n⚠️  发现 {len(duplicates)} 组可能重复的技能:")
            for s1, s2, reason in duplicates:
                print(f"   - {s1['name']} ↔ {s2['name']}: {reason}")
        else:
            print("   未发现重复技能")

    # 9. 增量更新检查
    if args.incremental:
        if not args.quiet:
            print("\n📊 计算增量变化...")
        diff = compare_skills(all_skills)
        print("\n" + get_diff_summary(diff))
        # 只保留变化的技能
        changed_names = {s['name'] for s in diff['added'] + diff['changed']}
        all_skills = [s for s in all_skills if s['name'] in changed_names]
        if not all_skills:
            if not args.quiet:
                print("\n✅ 无变化，无需更新")
            return 0

    # 10. 按状态过滤
    if args.filter == 'activated':
        skills_to_export = get_activated_skills(all_skills)
    elif args.filter == 'not_activated':
        skills_to_export = get_not_activated_skills(all_skills)
    else:
        skills_to_export = all_skills

    # 11. 自定义过滤
    skills_to_export = filter_skills(
        skills_to_export,
        search_term=args.search,
        category=args.category
    )

    if not args.quiet:
        print(f"\n📝 将导出 {len(skills_to_export)} 个技能")

    # 12. 导出
    output_files = []
    md_files: Dict[str, str] = {}

    if args.format in ['markdown', 'all']:
        if args.filter in ['all', 'activated']:
            md_path = os.path.join(args.output, "已激活技能列表.md")
            activated = get_activated_skills(skills_to_export)
            export_markdown(activated, "已激活技能列表", True, True, md_path,
                            usage=usage_stats, deps_edges=deps_edges)
            output_files.append(md_path)
            md_files["已激活技能列表"] = md_path
            if not args.quiet:
                print(f"   ✅ Markdown (已激活): {md_path}")

        if args.filter in ['all', 'not_activated']:
            md_path = os.path.join(args.output, "未激活技能列表.md")
            not_activated = get_not_activated_skills(skills_to_export)
            export_markdown(not_activated, "未激活技能列表", False, True, md_path,
                            usage=usage_stats, deps_edges=deps_edges)
            output_files.append(md_path)
            md_files["未激活技能列表"] = md_path
            if not args.quiet:
                print(f"   ✅ Markdown (未激活): {md_path}")

    if args.format in ['json', 'all']:
        json_path = os.path.join(args.output, "技能列表.json")
        export_json(skills_to_export, "技能列表", True, True, json_path,
                    usage=usage_stats, deps_edges=deps_edges)
        output_files.append(json_path)
        if not args.quiet:
            print(f"   ✅ JSON: {json_path}")

    if args.format in ['html', 'all']:
        if args.filter in ['all', 'activated']:
            html_path = os.path.join(args.output, "已激活技能列表.html")
            activated = get_activated_skills(skills_to_export)
            export_html(activated, "已激活技能列表", True, html_path,
                        usage=usage_stats, deps_edges=deps_edges)
            output_files.append(html_path)
            if not args.quiet:
                print(f"   ✅ HTML (已激活): {html_path}")

        if args.filter in ['all', 'not_activated']:
            html_path = os.path.join(args.output, "未激活技能列表.html")
            not_activated = get_not_activated_skills(skills_to_export)
            export_html(not_activated, "未激活技能列表", False, html_path,
                        usage=usage_stats, deps_edges=deps_edges)
            output_files.append(html_path)
            if not args.quiet:
                print(f"   ✅ HTML (未激活): {html_path}")

    # 13. 远端推送（依赖本次导出的 Markdown）
    if args.push:
        targets = _split_names(args.push)
        unknown_targets = [t for t in targets if t not in ('feishu', 'notion')]
        if unknown_targets:
            logger.error(f"未知推送目标: {unknown_targets}（仅支持 feishu/notion）")
            return 1
        if not md_files:
            logger.error("推送需要 Markdown 输出，请使用 -f markdown 或 -f all")
            return 1
        print("\n⚠️  隐私提示：推送会把技能清单（名称/描述/来源/调用量）发送到第三方服务（飞书/Notion）")
        for target in targets:
            push = feishu.push_markdown if target == 'feishu' else notion.push_markdown
            for title, path in md_files.items():
                url = push(path, title)
                print(f"   ✅ {target} «{title}»: {url}")

    # 14. 保存快照
    if not args.no_snapshot:
        save_snapshot(all_skills)
        if not args.quiet:
            print(f"\n💾 已保存快照")

    if not args.quiet:
        print("\n" + "=" * 50)
        print(f"✅ 完成！共导出 {len(output_files)} 个文件")
        for f in output_files:
            print(f"   - {f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
