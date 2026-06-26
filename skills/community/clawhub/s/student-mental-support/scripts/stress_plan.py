#!/usr/bin/env python3
"""
减压计划生成器
为大学生创建个性化减压计划
"""

def generate_stress_plan(user_info=None, anxiety_level=None):
    """
    生成个性化的减压计划
    
    Parameters:
    user_info: dict, 用户信息（可选）
    anxiety_level: str, 焦虑等级（轻度、中度、重度）
    """
    
    # 默认用户信息
    if user_info is None:
        user_info = {
            "major": "学生",
            "grade": "毕业生",
            "stress_sources": ["就业压力", "面试焦虑", "未来不确定性"]
        }
    
    # 默认焦虑等级
    if anxiety_level is None:
        anxiety_level = "中度"
    
    plan = {}
    
    # 根据焦虑等级制定计划
    if anxiety_level == "轻度":
        plan['title'] = "轻度压力管理计划"
        plan['description'] = "适合轻度焦虑的减压计划，以自助为主"
        plan['daily_routine'] = [
            "早晨：5分钟深呼吸练习",
            "白天：每小时提醒休息5分钟",
            "午休：15分钟正念冥想",
            "晚间：睡前放松阅读"
        ]
        plan['weekly_activities'] = [
            "周一：运动30分钟（散步或瑜伽）",
            "周三：参加喜欢的娱乐活动",
            "周五：社交活动或朋友聚会",
            "周日：整理和放松时间"
        ]
        plan['techniques'] = [
            "呼吸放松法",
            "正念冥想",
            "运动减压",
            "时间管理"
        ]
        plan['resources'] = [
            "压力管理书籍",
            "冥想应用（如Headspace）",
            "学校心理讲座"
        ]
        
    elif anxiety_level == "中度":
        plan['title'] = "中度压力管理计划"
        plan['description'] = "适合中度焦虑的综合减压计划"
        plan['daily_routine'] = [
            "早晨：10分钟冥想和感恩练习",
            "白天：番茄工作法（25分钟工作+5分钟休息）",
            "午休：20分钟放松活动",
            "晚间：记录今日感受和进步"
        ]
        plan['weekly_activities'] = [
            "周一：专业减压训练（如瑜伽课程）",
            "周二：心理咨询预约或自助训练",
            "周三：户外活动2小时",
            "周四：减压技巧练习",
            "周五：社交支持活动",
            "周六：完全休息日",
            "周日：总结和调整"
        ]
        plan['techniques'] = [
            "认知重构",
            "身体扫描放松",
            "时间规划",
            "社交支持"
        ]
        plan['resources'] = [
            "学校心理咨询中心",
            "在线心理咨询平台",
            "减压书籍和课程"
        ]
        
    else:  # 重度
        plan['title'] = "重度压力干预计划"
        plan['description'] = "针对重度焦虑的专业干预计划"
        plan['daily_routine'] = [
            "早晨：联系心理咨询支持",
            "白天：遵循专业指导计划",
            "晚间：确保安全和稳定"
        ]
        plan['weekly_activities'] = [
            "立即预约专业心理咨询",
            "参加学校心理危机干预",
            "确保每天安全支持",
            "避免高强度求职活动"
        ]
        plan['techniques'] = [
            "专业心理咨询",
            "紧急压力应对",
            "安全环境保障",
            "危机干预支持"
        ]
        plan['resources'] = [
            "专业心理咨询师",
            "心理危机热线",
            "学校心理中心",
            "医疗支持渠道"
        ]
    
    # 个性化调整
    if user_info.get('stress_sources'):
        source_analysis = analyze_stress_sources(user_info['stress_sources'])
        plan['source_analysis'] = source_analysis
    
    return plan

def analyze_stress_sources(sources):
    """
    分析压力来源并提供针对性建议
    
    Parameters:
    sources: list, 压力来源列表
    """
    analysis = {}
    
    for source in sources:
        if "就业压力" in source or "找不到工作" in source:
            analysis[source] = [
                "建议制定合理的求职计划",
                "设定SMART职业目标",
                "关注可控的求职过程"
            ]
        
        elif "面试焦虑" in source:
            analysis[source] = [
                "进行面试模拟练习",
                "准备常见问题回答",
                "学习面试放松技巧"
            ]
        
        elif "家庭期望" in source:
            analysis[source] = [
                "与家人沟通职业选择",
                "理解家庭期望与现实",
                "寻求家庭理解和支持"
            ]
        
        elif "经济压力" in source:
            analysis[source] = [
                "制定经济管理计划",
                "了解毕业过渡期支持",
                "考虑兼职或过渡性工作"
            ]
        
        elif "自我要求" in source:
            analysis[source] = [
                "调整自我期望值",
                "接受过程而非结果",
                "设定阶段性目标"
            ]
        
        else:
            analysis[source] = [
                "识别具体压力点",
                "针对压力点制定策略",
                "寻求相关资源支持"
            ]
    
    return analysis

def print_plan(plan):
    """
    打印减压计划
    
    Parameters:
    plan: dict, 减压计划
    """
    print(f"减压计划：{plan['title']}")
    print(f"描述：{plan['description']}")
    print()
    
    print("每日例行：")
    for routine in plan['daily_routine']:
        print(f"  - {routine}")
    print()
    
    print("每周活动：")
    for activity in plan['weekly_activities']:
        print(f"  - {activity}")
    print()
    
    print("减压技巧：")
    for technique in plan['techniques']:
        print(f"  - {technique}")
    print()
    
    print("推荐资源：")
    for resource in plan['resources']:
        print(f"  - {resource}")
    print()
    
    if 'source_analysis' in plan:
        print("压力来源针对性建议：")
        for source, suggestions in plan['source_analysis'].items():
            print(f"  {source}:")
            for suggestion in suggestions:
                print(f"    - {suggestion}")
            print()

def create_template():
    """
    创建减压计划模板
    """
    template = {
        "plan_title": "",
        "user_major": "",
        "user_grade": "",
        "stress_level": "",
        "stress_sources": [],
        
        "daily_activities": {
            "morning": "",
            "midday": "",
            "afternoon": "",
            "evening": "",
            "night": ""
        },
        
        "weekly_goals": {
            "mon": "",
            "tue": "",
            "wed": "",
            "thu": "",
            "fri": "",
            "sat": "",
            "sun": ""
        },
        
        "techniques_to_use": [],
        "resources_needed": [],
        "progress_tracking": {
            "daily_check": "",
            "weekly_review": ""
        },
        
        "safety_note": ""
    }
    
    return template

if __name__ == "__main__":
    # 示例用户信息
    user_info = {
        "major": "计算机科学",
        "grade": "四年级",
        "stress_sources": ["就业压力", "面试焦虑", "家庭期望"]
    }
    
    # 生成计划
    plan = generate_stress_plan(user_info, "中度")
    
    # 打印计划
    print_plan(plan)
    
    # 显示模板
    template = create_template()
    print("\n减压计划模板（可填写）：")
    for key, value in template.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for subkey, subvalue in value.items():
                print(f"    {subkey}: {subvalue}")
        elif isinstance(value, list):
            print(f"  {key}: {', '.join(value)}")
        else:
            print(f"  {key}: {value}")