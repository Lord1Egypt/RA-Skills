#!/usr/bin/env python3
"""
发现可以组合使用的技能对
"""
import os
import sys
import re
from analyze_skill import parse_skill_md

# 预定义的技能组合模式
COMBINATION_PATTERNS = [
    {
        'name': '定时监控',
        'skills': ['stock-watcher', 'cron', 'schedule'],
        'description': '定时获取数据并发送通知',
        'example': '定时检查股票价格，异常时发送QQ消息'
    },
    {
        'name': '内容创作流水线',
        'skills': ['tavily-search', 'summarize', 'novel-generator', 'film-production-assistant'],
        'description': '搜索资料→总结→创作→影视化',
        'example': '搜索热点话题→生成小说→改编剧本'
    },
    {
        'name': 'GitHub自动化',
        'skills': ['github-star-manager', 'gh-issues', 'github'],
        'description': '管理stars、自动修复issues',
        'example': '清理过时的starred repos，自动修复bug'
    },
    {
        'name': '代码审查',
        'skills': ['codereview-roasted', 'critic-agent', 'self-criticism'],
        'description': '多维度代码审查和改进',
        'example': '自动审查代码，给出改进建议'
    },
    {
        'name': 'SEO优化',
        'skills': ['seo-audit', 'ai-seo', 'schema-markup', 'programmatic-seo'],
        'description': '全面的SEO分析和优化',
        'example': '审计网站SEO→生成优化方案→批量实施'
    },
    {
        'name': '智能客服',
        'skills': ['qqbot-cron', 'qqbot-media', 'humanizer-zh'],
        'description': '定时回复+富媒体+人性化表达',
        'example': '自动回复常见问题，发送图片/语音'
    },
    {
        'name': '安全审计',
        'skills': ['skill-vetter', 'healthcheck', 'security-reports'],
        'description': '技能安全检查+系统安全加固',
        'example': '审查新安装的技能，检查系统安全'
    },
    {
        'name': '多智能体协作',
        'skills': ['novel-generator', 'film-production-assistant', 'multi-agent'],
        'description': '多个AI智能体协作完成复杂任务',
        'example': '14个智能体协作创作长篇小说'
    }
]

def find_installed_skills(skills_dir):
    """查找已安装的技能."""
    installed = set()
    if not os.path.exists(skills_dir):
        return installed
    
    for item in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, item)
        if os.path.isdir(skill_path):
            skill_md = os.path.join(skill_path, 'SKILL.md')
            if os.path.exists(skill_md):
                data = parse_skill_md(skill_md)
                if data and data.get('name'):
                    installed.add(data['name'].lower())
                    installed.add(item.lower())
    
    return installed

def find_combinations(skills_dir):
    """发现可组合的技能."""
    installed = find_installed_skills(skills_dir)
    
    print("🔍 技能组合推荐\n")
    print("=" * 60)
    
    found_combinations = []
    
    for pattern in COMBINATION_PATTERNS:
        matched_skills = []
        missing_skills = []
        
        for skill in pattern['skills']:
            skill_lower = skill.lower()
            # 检查是否已安装（模糊匹配）
            is_installed = any(skill_lower in s or s in skill_lower for s in installed)
            if is_installed:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        if len(matched_skills) >= 2:
            found_combinations.append({
                'pattern': pattern,
                'matched': matched_skills,
                'missing': missing_skills
            })
    
    if not found_combinations:
        print("\n💡 建议安装更多技能以发现有趣的组合！")
        print("\n推荐安装:")
        for pattern in COMBINATION_PATTERNS[:3]:
            print(f"  • {pattern['name']}: {', '.join(pattern['skills'])}")
        return
    
    # 显示找到的组合
    for i, combo in enumerate(found_combinations, 1):
        pattern = combo['pattern']
        print(f"\n{i}. 💡 {pattern['name']}")
        print(f"   描述: {pattern['description']}")
        print(f"   已安装: {', '.join(combo['matched'])}")
        if combo['missing']:
            print(f"   未安装: {', '.join(combo['missing'])} (建议安装)")
        print(f"   使用场景: {pattern['example']}")
    
    print("\n" + "=" * 60)
    
    # 基于描述发现潜在组合
    print("\n🔮 基于描述分析的潜在组合:\n")
    
    # 读取所有技能描述
    skill_data = {}
    for item in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, item)
        if os.path.isdir(skill_path):
            skill_md = os.path.join(skill_path, 'SKILL.md')
            if os.path.exists(skill_md):
                data = parse_skill_md(skill_md)
                if data and data.get('description'):
                    skill_data[item] = data
    
    # 简单的关键词匹配发现潜在组合
    keywords = {
        '数据': ['fetch', 'get', 'data', 'search', '查询'],
        '内容': ['write', 'create', 'generate', 'content', '创作'],
        '监控': ['watch', 'monitor', 'check', '监控', '检查'],
        '通知': ['notify', 'send', 'alert', '通知', '提醒'],
        '分析': ['analyze', 'audit', 'review', '分析', '审查']
    }
    
    potential_combos = []
    for category, words in keywords.items():
        matching_skills = []
        for name, data in skill_data.items():
            desc = data.get('description', '').lower()
            if any(word in desc for word in words):
                matching_skills.append(name)
        
        if len(matching_skills) >= 2:
            potential_combos.append({
                'category': category,
                'skills': matching_skills
            })
    
    if potential_combos:
        for combo in potential_combos[:3]:
            print(f"  • {combo['category']}相关: {', '.join(combo['skills'][:3])}")
    
    print("\n💡 提示: 使用 `npx clawhub search <关键词>` 查找更多相关技能")

def main():
    skills_dir = os.path.expanduser('~/.openclaw/workspace/skills')
    find_combinations(skills_dir)

if __name__ == '__main__':
    main()
