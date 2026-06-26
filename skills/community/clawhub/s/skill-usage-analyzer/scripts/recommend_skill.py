#!/usr/bin/env python3
"""
根据任务描述智能推荐技能
"""
import os
import sys
import re
from analyze_skill import parse_skill_md

# 任务关键词到技能类型的映射
TASK_KEYWORDS = {
    '股票': ['stock-watcher', 'finance', 'market'],
    '监控': ['stock-watcher', 'healthcheck', 'monitor', 'watch'],
    '定时': ['cron', 'schedule', 'timer'],
    '通知': ['qqbot', 'notify', 'alert', 'send'],
    '搜索': ['web-search', 'tavily-search', 'exa', 'search'],
    '总结': ['summarize', 'summary', 'abstract'],
    '写作': ['novel-generator', 'write', 'content', 'blog-writer'],
    '创作': ['novel-generator', 'film-production-assistant', 'create'],
    '代码': ['gh-issues', 'codereview', 'github', 'code'],
    '审查': ['codereview-roasted', 'critic-agent', 'review', 'audit'],
    '安全': ['skill-vetter', 'healthcheck', 'security', 'safe'],
    'SEO': ['seo-audit', 'ai-seo', 'schema-markup'],
    'GitHub': ['github-star-manager', 'gh-issues', 'github'],
    '小说': ['novel-generator', 'story', 'fiction'],
    '影视': ['film-production-assistant', 'video', 'movie'],
    '角色': ['character-creator-cn', 'character', 'role'],
    '浏览器': ['agent-browser', 'browser', 'web'],
    '天气': ['weather', 'forecast'],
    'SSH': ['ssh', 'remote', 'connect'],
    '文件': ['file-manager', 'files', 'organize'],
    '提示词': ['prompt-engineer-ultra', 'prompt', 'engineering'],
    '改进': ['self-improving', 'self-criticism', 'improve'],
    '技能': ['skill-vetter', 'skill-creator', 'find-skills'],
    '图片': ['qqbot-media', 'image', 'photo'],
    '视频': ['video-frames', 'video', 'clip'],
    '分析': ['analyze', 'audit', 'review', '分析'],
    '管理': ['manager', 'manage', 'organize', '管理'],
    '自动化': ['auto', 'automate', '自动'],
    '数据': ['data', 'fetch', 'get', '数据'],
    '学习': ['learn', 'study', 'tutorial', '学习']
}

def find_matching_skills(task_description, skills_dir):
    """根据任务描述找到匹配的技能."""
    task_lower = task_description.lower()
    
    # 提取关键词
    matched_keywords = []
    for keyword, skill_patterns in TASK_KEYWORDS.items():
        if keyword in task_description or keyword in task_lower:
            matched_keywords.append((keyword, skill_patterns))
    
    # 读取所有技能
    skills = {}
    if os.path.exists(skills_dir):
        for item in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, item)
            if os.path.isdir(skill_path):
                skill_md = os.path.join(skill_path, 'SKILL.md')
                if os.path.exists(skill_md):
                    data = parse_skill_md(skill_md)
                    if data:
                        skills[item] = data
    
    # 匹配技能
    matched_skills = {}
    for keyword, patterns in matched_keywords:
        for skill_name, skill_data in skills.items():
            desc = skill_data.get('description', '').lower()
            name = skill_data.get('name', skill_name).lower()
            
            # 检查是否匹配
            is_match = False
            for pattern in patterns:
                if pattern.lower() in name or pattern.lower() in desc:
                    is_match = True
                    break
            
            if is_match:
                if keyword not in matched_skills:
                    matched_skills[keyword] = []
                matched_skills[keyword].append(skill_data)
    
    return matched_skills, matched_keywords

def generate_workflow(task_description, matched_skills):
    """生成使用流程建议."""
    task_lower = task_description.lower()
    
    workflows = []
    
    # 股票监控 + 定时 + 通知
    if '股票' in task_description and ('定时' in task_description or '监控' in task_description or '通知' in task_description):
        workflows.append({
            'name': '股票定时监控通知',
            'steps': [
                '使用 stock-watcher 添加关注的股票',
                '使用 cron 设置定时任务（如每天9:30）',
                '使用 qqbot-media 或 qqbot-cron 发送价格提醒'
            ],
            'example': '每天早上开盘前自动发送自选股行情'
        })
    
    # 搜索 + 总结 + 创作
    if any(k in task_description for k in ['搜索', '资料', '内容', '写作', '创作']):
        workflows.append({
            'name': '内容创作流水线',
            'steps': [
                '使用 web-search 或 tavily-search 搜索相关资料',
                '使用 summarize 总结关键信息',
                '使用 novel-generator 或 blog-writer 创作内容',
                '使用 humanizer-zh 优化文本（可选）'
            ],
            'example': '搜索热点话题→生成深度文章'
        })
    
    # GitHub + 自动化
    if 'github' in task_lower or 'git' in task_lower:
        workflows.append({
            'name': 'GitHub自动化管理',
            'steps': [
                '使用 github-star-manager 整理 starred repos',
                '使用 gh-issues 自动修复 issues',
                '使用 cron 定期执行清理任务'
            ],
            'example': '每月自动清理过时的 starred repos'
        })
    
    # SEO + 内容
    if any(k in task_description for k in ['seo', '优化', '排名', '流量']):
        workflows.append({
            'name': 'SEO优化流程',
            'steps': [
                '使用 seo-audit 审计网站SEO问题',
                '使用 ai-seo 生成优化建议',
                '使用 schema-markup 添加结构化数据',
                '使用 blog-writer 创作SEO友好内容'
            ],
            'example': '全面优化网站SEO，提升搜索排名'
        })
    
    # 安全审计
    if any(k in task_description for k in ['安全', '审计', '检查', '风险']):
        workflows.append({
            'name': '安全审计流程',
            'steps': [
                '使用 skill-vetter 审查已安装技能的安全性',
                '使用 healthcheck 检查系统安全配置',
                '使用 self-criticism 审查代码/配置问题'
            ],
            'example': '全面检查OpenClaw环境和技能安全性'
        })
    
    return workflows

def main():
    if len(sys.argv) < 2:
        print("用法: python3 recommend_skill.py '你的任务描述'")
        print("\n示例:")
        print("  python3 recommend_skill.py '我想监控股票价格并定时发送通知'")
        print("  python3 recommend_skill.py '帮我搜索资料然后写一篇博客'")
        sys.exit(1)
    
    task_description = sys.argv[1]
    skills_dir = os.path.expanduser('~/.openclaw/workspace/skills')
    
    print(f"\n🔍 任务分析: {task_description}")
    print("=" * 60)
    
    # 匹配技能
    matched_skills, matched_keywords = find_matching_skills(task_description, skills_dir)
    
    if not matched_skills:
        print("\n💡 未找到直接匹配的技能。")
        print("\n建议:")
        print("  1. 使用 `npx clawhub search <关键词>` 搜索相关技能")
        print("  2. 简化任务描述，使用更通用的词汇")
        print("  3. 查看已安装技能: `openclaw skills list`")
        return
    
    # 显示匹配的技能
    print("\n📦 推荐技能:\n")
    
    all_matched = []
    for keyword, skills in matched_skills.items():
        print(f"  🔑 关键词 '{keyword}' 匹配:")
        for skill in skills:
            name = skill.get('name', 'Unknown')
            desc = skill.get('description', '')
            # 截断描述
            if len(desc) > 60:
                desc = desc[:60] + '...'
            print(f"     • {name}: {desc}")
            all_matched.append(skill)
        print()
    
    # 生成工作流建议
    workflows = generate_workflow(task_description, matched_skills)
    
    if workflows:
        print("💡 推荐工作流程:\n")
        for i, workflow in enumerate(workflows, 1):
            print(f"{i}. {workflow['name']}")
            print(f"   场景: {workflow['example']}")
            print("   步骤:")
            for j, step in enumerate(workflow['steps'], 1):
                print(f"     {j}. {step}")
            print()
    
    # 显示安装建议
    print("=" * 60)
    print("\n🚀 下一步:\n")
    
    unique_skills = {s.get('name', '') for s in all_matched}
    for skill_name in unique_skills:
        if skill_name:
            print(f"  安装 {skill_name}:")
            print(f"    npx clawhub install {skill_name}")
            print()
    
    print("💡 提示: 使用 `python3 analyze_skill.py /path/to/SKILL.md` 查看详细用法")

if __name__ == '__main__':
    main()
