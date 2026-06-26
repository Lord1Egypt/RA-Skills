#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
技能列表生成主脚本
整合所有模块，支持多种输出格式和过滤选项
"""
import argparse
import sys
import os
from typing import List, Dict, Any
import logging

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.openclaw import get_skills_from_cli, get_activated_skills, get_not_activated_skills, get_skill_status
from data.filesystem import get_unregistered_skills, get_dir_to_name_map
from data.meta_reader import load_all_meta, get_meta_info
from classifier.category_map import get_category
from classifier.auto_classify import suggest_category, find_duplicate_skills
from exporter.markdown import export_markdown
from exporter.json_exporter import export_json
from exporter.html_exporter import export_html
from utils.diff import compare_skills, save_snapshot, is_incremental_update_needed, get_diff_summary
from utils.config import OUTPUT_DIR
from utils.translator import translate_description

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


def main():
    """主函数"""
    args = parse_args()
    
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
    
    # 2. 加载元数据
    meta_data = load_all_meta()
    
    # 3. 丰富数据
    all_skills = enrich_skill_data(cli_skills, meta_data)
    
    # 4. 添加未注册的技能（只添加 workspace 目录中存在但 OpenClaw 未识别的）
    # 注意：OpenClaw 已经扫描了所有技能，不需要重复添加，只用于分类映射参考
    
    if not args.quiet:
        print(f"   共获取 {len(all_skills)} 个技能")
    
    # 5. 检测重复技能
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
    
    # 6. 增量更新检查
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
    
    # 7. 按状态过滤
    if args.filter == 'activated':
        skills_to_export = get_activated_skills(all_skills)
    elif args.filter == 'not_activated':
        skills_to_export = get_not_activated_skills(all_skills)
    else:
        skills_to_export = all_skills
    
    # 8. 自定义过滤
    skills_to_export = filter_skills(
        skills_to_export,
        search_term=args.search,
        category=args.category
    )
    
    if not args.quiet:
        print(f"\n📝 将导出 {len(skills_to_export)} 个技能")
    
    # 9. 导出
    output_files = []
    
    if args.format in ['markdown', 'all']:
        if args.filter in ['all', 'activated']:
            md_path = os.path.join(args.output, "已激活技能列表.md")
            activated = get_activated_skills(skills_to_export)
            export_markdown(activated, "已激活技能列表", True, True, md_path)
            output_files.append(md_path)
            if not args.quiet:
                print(f"   ✅ Markdown (已激活): {md_path}")
        
        if args.filter in ['all', 'not_activated']:
            md_path = os.path.join(args.output, "未激活技能列表.md")
            not_activated = get_not_activated_skills(skills_to_export)
            export_markdown(not_activated, "未激活技能列表", False, True, md_path)
            output_files.append(md_path)
            if not args.quiet:
                print(f"   ✅ Markdown (未激活): {md_path}")
    
    if args.format in ['json', 'all']:
        json_path = os.path.join(args.output, "技能列表.json")
        export_json(skills_to_export, "技能列表", True, True, json_path)
        output_files.append(json_path)
        if not args.quiet:
            print(f"   ✅ JSON: {json_path}")
    
    if args.format in ['html', 'all']:
        if args.filter in ['all', 'activated']:
            html_path = os.path.join(args.output, "已激活技能列表.html")
            activated = get_activated_skills(skills_to_export)
            export_html(activated, "已激活技能列表", True, html_path)
            output_files.append(html_path)
            if not args.quiet:
                print(f"   ✅ HTML (已激活): {html_path}")
        
        if args.filter in ['all', 'not_activated']:
            html_path = os.path.join(args.output, "未激活技能列表.html")
            not_activated = get_not_activated_skills(skills_to_export)
            export_html(not_activated, "未激活技能列表", False, html_path)
            output_files.append(html_path)
            if not args.quiet:
                print(f"   ✅ HTML (未激活): {html_path}")
    
    # 10. 保存快照
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
