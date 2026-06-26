#!/usr/bin/env python3
"""
分析技能并生成创意用法建议
"""
import os
import sys
from analyze_skill import parse_skill_md

# 创意用法模式库
CREATIVE_PATTERNS = {
    'stock-watcher': [
        {'title': '📊 智能选股助手', 'description': '结合AI分析，自动筛选潜力股票', 'steps': ['批量添加关注的板块股票', '筛选涨幅/跌幅异常的股票', '用AI分析基本面和技术面', '生成每日选股报告'], 'value': '从手动监控升级为智能选股'},
        {'title': '🤖 自动化交易提醒', 'description': '设置条件单，自动触发买卖提醒', 'steps': ['设置价格预警', '结合cron定时检查', '通过QQ/Telegram推送通知', '记录触发历史优化策略'], 'value': '不再错过交易时机'},
        {'title': '📈 投资组合分析', 'description': '管理多只股票，分析整体收益', 'steps': ['按行业/策略分组管理', '定期导出数据到Excel', '用Python分析组合表现', '生成可视化收益图表'], 'value': '从单股监控到组合管理'}
    ],
    'github-star-manager': [
        {'title': '📚 个人知识库构建', 'description': '将starred repos整理成可搜索的知识库', 'steps': ['用AI分类所有starred repos', '提取每个repo的核心功能', '生成带标签的知识库索引', '定期更新删除过时项目'], 'value': '从收藏到知识体系'},
        {'title': '🚀 技术趋势追踪', 'description': '分析star模式，发现技术趋势', 'steps': ['按时间排序查看最近starred', '统计各技术领域的收藏量', '对比GitHub Trending', '生成个人技术雷达图'], 'value': '了解技术发展方向'}
    ],
    'novel-generator': [
        {'title': '🎬 短视频脚本生成', 'description': '将小说生成能力用于短视频创作', 'steps': ['输入热点话题或梗', '生成短故事/段子', '改编为分镜脚本', '用film-production-assistant完善'], 'value': '快速产出短视频内容'},
        {'title': '🎮 游戏剧情设计', 'description': '生成游戏任务、NPC对话、世界观', 'steps': ['设定游戏世界观', '生成主线/支线剧情', '设计角色背景故事', '用character-creator-cn完善角色'], 'value': '为独立游戏提供剧情支持'},
        {'title': '🏢 企业品牌故事', 'description': '为企业生成品牌故事和营销内容', 'steps': ['输入企业背景和产品特点', '生成品牌起源故事', '创作用户案例故事', '适配不同平台发布'], 'value': 'AI驱动的内容营销'}
    ],
    'film-production-assistant': [
        {'title': '📱 短视频工业化生产', 'description': '批量生成短视频脚本和拍摄方案', 'steps': ['用novel-generator生成故事', '改编为分镜脚本', '生成AI绘画/视频提示词', '批量生产系列内容'], 'value': '建立短视频内容工厂'},
        {'title': '🎓 教学视频制作', 'description': '将知识点转化为视频课程', 'steps': ['输入教学大纲', '设计每节课的视觉呈现', '生成配套的案例演示', '输出完整的课程制作方案'], 'value': '降低课程制作门槛'}
    ],
    'tavily-search': [
        {'title': '📰 每日资讯摘要', 'description': '自动搜集和总结每日热点', 'steps': ['设置关注领域关键词', '定时搜索最新资讯', '用summarize生成摘要', '推送到QQ/微信'], 'value': '打造个人资讯助手'},
        {'title': '🔍 竞品监控', 'description': '监控竞争对手动态', 'steps': ['设置竞品公司和产品关键词', '定期搜索新闻和动态', '整理成竞品分析报告', '发现市场机会'], 'value': '及时掌握竞争态势'}
    ],
    'summarize': [
        {'title': '📧 邮件自动摘要', 'description': '自动总结长邮件内容', 'steps': ['获取邮件内容', '提取关键信息和待办事项', '生成一句话摘要', '按优先级排序'], 'value': '提高邮件处理效率'},
        {'title': '📄 合同/协议速读', 'description': '快速理解合同关键条款', 'steps': ['上传合同文档', '提取关键条款和风险点', '对比标准模板', '生成审查清单'], 'value': '降低合同风险'}
    ],
    'character-creator-cn': [
        {'title': '🎮 NPC批量生成', 'description': '为游戏批量生成NPC角色', 'steps': ['设定游戏世界观', '批量生成不同职业NPC', '设计人物关系和任务链', '导出为游戏数据格式'], 'value': '快速填充游戏世界'},
        {'title': '📖 小说角色卡', 'description': '为小说创建详细角色档案', 'steps': ['输入角色基本信息', '生成完整背景故事', '设计性格特征和成长弧', '整理为角色卡方便写作参考'], 'value': '保持角色一致性'}
    ]
}

def generate_generic_creative_usage(skill_data):
    """为没有预设创意用法的技能生成通用建议."""
    name = skill_data.get('name', 'Unknown')
    desc = skill_data.get('description', '').lower()
    
    ideas = []
    
    if any(k in desc for k in ['search', 'fetch', 'get', 'data', '搜索', '获取', '数据']):
        ideas.append({'title': '📊 自动化数据收集', 'description': f'定时使用{name}收集数据，建立个人数据库', 'steps': ['设置定时任务（cron）', '自动执行数据收集', '存储到数据库/文件', '定期分析和可视化'], 'value': '从手动查询到自动化数据流'})
    
    if any(k in desc for k in ['write', 'create', 'generate', 'content', '写作', '创作', '生成']):
        ideas.append({'title': '🚀 内容生产流水线', 'description': f'将{name}整合到内容创作工作流', 'steps': ['用搜索技能获取素材', f'用{name}生成初稿', '用审查技能优化', '批量发布到多平台'], 'value': '10倍提升内容产出效率'})
    
    if any(k in desc for k in ['analyze', 'review', 'audit', 'check', '分析', '审查', '检查']):
        ideas.append({'title': '🔍 智能质量监控', 'description': f'定期使用{name}进行自动化审查', 'steps': ['设置审查规则和阈值', '定时执行自动化检查', '生成审查报告', '追踪问题修复进度'], 'value': '从事后检查到预防性监控'})
    
    if any(k in desc for k in ['manage', 'organize', '管理', '组织', '整理']):
        ideas.append({'title': '📁 智能分类系统', 'description': f'结合AI自动化{name}的管理流程', 'steps': ['导入待管理的数据', '用AI自动分类和标签', '设置自动化规则', '定期优化分类策略'], 'value': '从人工整理到智能管理'})
    
    if not ideas:
        ideas = [
            {'title': '🔗 技能组合增强', 'description': f'将{name}与其他技能组合使用', 'steps': ['分析技能的核心能力', '寻找互补的其他技能', '设计组合使用流程', '自动化整个流程'], 'value': '1+1>2的技能协同效应'},
            {'title': '⏰ 定时自动化', 'description': f'设置定时任务自动执行{name}', 'steps': ['确定执行频率', '使用cron设置定时任务', '配置结果通知', '监控执行状态'], 'value': '从手动操作到无人值守'},
            {'title': '📊 效果追踪', 'description': f'记录和分析{name}的使用效果', 'steps': ['记录每次使用的时间和结果', '定期汇总使用数据', '分析使用频率和效果', '优化使用策略'], 'value': '用数据驱动技能使用优化'}
        ]
    
    return ideas

def analyze_creative_usage(skill_name, skills_dir):
    """分析技能的创意用法."""
    skill_path = None
    actual_name = None
    
    for item in os.listdir(skills_dir):
        if skill_name.lower() in item.lower():
            potential_path = os.path.join(skills_dir, item)
            skill_md = os.path.join(potential_path, 'SKILL.md')
            if os.path.exists(skill_md):
                skill_path = potential_path
                actual_name = item
                break
    
    if not skill_path:
        print(f"❌ 未找到技能: {skill_name}")
        return
    
    data = parse_skill_md(os.path.join(skill_path, 'SKILL.md'))
    if not data:
        print(f"❌ 无法解析技能: {skill_name}")
        return
    
    name = data.get('name', actual_name)
    
    print(f"\n💡 {name} 创意用法指南\n")
    print("=" * 70)
    
    ideas = []
    for key in CREATIVE_PATTERNS:
        if key.lower() in name.lower():
            ideas = CREATIVE_PATTERNS[key]
            break
    
    if not ideas:
        ideas = generate_generic_creative_usage(data)
        print("\n🎨 基于技能特性分析的创意用法:\n")
    else:
        print("\n🎯 精选创意用法:\n")
    
    for i, idea in enumerate(ideas, 1):
        print(f"{i}. {idea['title']}")
        print(f"   💭 {idea['description']}")
        print("   步骤:")
        for j, step in enumerate(idea['steps'], 1):
            print(f"      {j}. {step}")
        print(f"   ✅ 价值: {idea['value']}")
        print()
    
    print("=" * 70)
    print("\n💡 进阶建议:\n")
    print("  1. 尝试将本技能与其他技能组合使用")
    print("  2. 设置定时任务，实现自动化")
    print("  3. 记录使用效果，持续优化")
    print("  4. 使用 compare_matrix.py 对比类似技能")
    print("  5. 使用 find_combinations.py 发现技能组合")

def main():
    if len(sys.argv) < 2:
        print("用法: python3 creative_usage.py <技能名称>")
        print("\n示例:")
        print("  python3 creative_usage.py stock-watcher")
        print("  python3 creative_usage.py novel-generator")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    skills_dir = os.path.expanduser('~/.openclaw/workspace/skills')
    
    analyze_creative_usage(skill_name, skills_dir)

if __name__ == '__main__':
    main()
