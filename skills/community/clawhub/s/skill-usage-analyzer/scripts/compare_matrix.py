#!/usr/bin/env python3
"""
对比多个相似技能，生成对比矩阵
"""
import os
import sys
from analyze_skill import parse_skill_md

def compare_skills(skill_names, skills_dir):
    """对比多个技能."""
    skills_data = []
    
    for name in skill_names:
        # 查找技能目录
        skill_path = None
        for item in os.listdir(skills_dir):
            if name.lower() in item.lower():
                potential_path = os.path.join(skills_dir, item)
                skill_md = os.path.join(potential_path, 'SKILL.md')
                if os.path.exists(skill_md):
                    skill_path = potential_path
                    break
        
        if not skill_path:
            print(f"⚠️  未找到技能: {name}")
            continue
        
        data = parse_skill_md(os.path.join(skill_path, 'SKILL.md'))
        if data:
            data['path'] = skill_path
            skills_data.append(data)
    
    if len(skills_data) < 2:
        print("❌ 需要至少2个有效技能才能对比")
        return
    
    # 生成对比矩阵
    print("\n📊 技能对比矩阵\n")
    print("=" * 80)
    
    # 基本信息对比
    print("\n📋 基本信息:\n")
    print(f"{'属性':<20}", end='')
    for skill in skills_data:
        name = skill.get('name', 'Unknown')[:15]
        print(f"{name:<20}", end='')
    print()
    print("-" * (20 + 20 * len(skills_data)))
    
    # 描述
    print(f"{'描述':<20}", end='')
    for skill in skills_data:
        desc = skill.get('description', '-')[:30]
        if len(desc) > 30:
            desc = desc[:27] + '...'
        print(f"{desc:<20}", end='')
    print()
    
    # 功能数量
    print(f"{'功能数量':<20}", end='')
    for skill in skills_data:
        count = len(skill.get('features', []))
        print(f"{count:<20}", end='')
    print()
    
    # 示例数量
    print(f"{'示例数量':<20}", end='')
    for skill in skills_data:
        count = len(skill.get('examples', []))
        print(f"{count:<20}", end='')
    print()
    
    # 配置项数量
    print(f"{'配置项数量':<20}", end='')
    for skill in skills_data:
        count = len(skill.get('config', []))
        print(f"{count:<20}", end='')
    print()
    
    # 详细功能对比
    print("\n\n🎯 功能对比:\n")
    
    # 收集所有功能
    all_features = set()
    for skill in skills_data:
        for feature in skill.get('features', []):
            # 提取功能名称（假设格式为 "名称 - 描述" 或只是 "名称"）
            feature_name = feature.split('-')[0].strip() if '-' in feature else feature[:20]
            all_features.add(feature_name)
    
    if all_features:
        print(f"{'功能':<25}", end='')
        for skill in skills_data:
            name = skill.get('name', 'Unknown')[:12]
            print(f"{name:<15}", end='')
        print()
        print("-" * (25 + 15 * len(skills_data)))
        
        for feature in sorted(all_features)[:10]:  # 最多显示10个
            print(f"{feature:<25}", end='')
            for skill in skills_data:
                skill_features = ' '.join(skill.get('features', []))
                has_feature = feature.lower() in skill_features.lower()
                mark = '✅' if has_feature else '❌'
                print(f"{mark:<15}", end='')
            print()
    
    # 优缺点分析
    print("\n\n💡 优缺点分析:\n")
    
    for i, skill in enumerate(skills_data, 1):
        name = skill.get('name', f'技能{i}')
        print(f"{i}. {name}")
        
        # 优点
        features = skill.get('features', [])
        examples = skill.get('examples', [])
        
        if len(features) > 3:
            print(f"   ✅ 优点: 功能丰富 ({len(features)}个功能)")
        if len(examples) > 2:
            print(f"   ✅ 优点: 示例充足 ({len(examples)}个示例)")
        
        # 缺点
        if len(features) == 0:
            print(f"   ⚠️  缺点: 未明确列出功能")
        if len(examples) == 0:
            print(f"   ⚠️  缺点: 缺少使用示例")
        
        # 适用场景
        desc = skill.get('description', '')
        if desc:
            print(f"   🎯 适用: {desc[:50]}...")
        print()
    
    # 推荐建议
    print("=" * 80)
    print("\n📌 选择建议:\n")
    
    # 找出功能最多的
    most_features = max(skills_data, key=lambda x: len(x.get('features', [])))
    # 找出示例最多的
    most_examples = max(skills_data, key=lambda x: len(x.get('examples', [])))
    
    print(f"  • 功能最丰富: {most_features.get('name', 'Unknown')} ({len(most_features.get('features', []))}个功能)")
    print(f"  • 示例最详细: {most_examples.get('name', 'Unknown')} ({len(most_examples.get('examples', []))}个示例)")
    
    print("\n  💡 建议:")
    print("     - 如果你是新手，选择示例最多的技能")
    print("     - 如果你需要高级功能，选择功能最丰富的技能")
    print("     - 建议先试用每个技能的基础功能，再决定使用哪个")

def main():
    if len(sys.argv) < 3:
        print("用法: python3 compare_matrix.py <技能1> <技能2> [技能3] ...")
        print("\n示例:")
        print("  python3 compare_matrix.py web-search tavily-search")
        print("  python3 compare_matrix.py stock-watcher github-star-manager")
        sys.exit(1)
    
    skill_names = sys.argv[1:]
    skills_dir = os.path.expanduser('~/.openclaw/workspace/skills')
    
    compare_skills(skill_names, skills_dir)

if __name__ == '__main__':
    main()
