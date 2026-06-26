#!/usr/bin/env python3
"""
学程智伴 - 学期计划生成器
帮助大学生生成个性化学习计划
"""

import json
from datetime import datetime, timedelta

def generate_semester_plan(courses, goals, constraints):
    """
    生成学期学习计划
    
    参数:
        courses: 课程列表 [{"name": "课程名", "credits": 学分, "difficulty": "easy/medium/hard"}]
        goals: 学期目标 ["通过四六级", "学Python", ...]
        constraints: 时间约束 {"max_study_hours": 30, "preferred_time": "morning"}
    """
    
    plan = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "overview": generate_overview(courses, goals),
        "weekly_schedule": generate_weekly_schedule(courses, constraints),
        "monthly_milestones": generate_milestones(goals),
        "tips": get_study_tips()
    }
    
    return plan

def generate_overview(courses, goals):
    """生成学期概览"""
    total_credits = sum(c.get("credits", 0) for c in courses)
    hard_courses = [c["name"] for c in courses if c.get("difficulty") == "hard"]
    
    overview = f"""
📊 **学期概览**

**课程情况**
- 总学分：{total_credits}
- 课程数量：{len(courses)}门
- 难课数量：{len(hard_courses)}门

**本学期目标**
"""
    for i, goal in enumerate(goals, 1):
        overview += f"{i}. {goal}\n"
    
    if hard_courses:
        overview += f"\n⚠️ **重点关注课程**\n"
        for course in hard_courses:
            overview += f"- {course}：建议每周多花2小时预习复习\n"
    
    return overview

def generate_weekly_schedule(courses, constraints):
    """生成周计划模板"""
    max_hours = constraints.get("max_study_hours", 30)
    preferred_time = constraints.get("preferred_time", "morning")
    
    schedule = f"""
📅 **每周学习安排**

**时间分配**
- 总可用学习时间：{max_hours}小时/周
- 建议自习时段：{'早间(8-12点)' if preferred_time == 'morning' else '晚间(19-22点)'}

**推荐作息**
"""
    
    if preferred_time == "morning":
        schedule += """
🌅 **早晨黄金时段** (8:00-12:00)
- 8:00-9:30 深度学习（最难课程）
- 9:45-11:15 专业课复习
- 11:30-12:00 轻量任务（背单词/看论文）

🌤️ **下午** (14:00-17:00)
- 上课/实验
- 没课就做作业

🌙 **晚上** (19:00-22:00)
- 完成当天作业
- 复习当天课程
- 留1小时机动时间
"""
    else:
        schedule += """
🌞 **白天** (8:00-17:00)
- 上课/实验
- 利用课间处理杂事
- 下午没课可以补觉或运动

🌙 **晚间黄金时段** (19:00-22:00)
- 19:00-20:30 深度学习（最难课程）
- 20:45-22:00 专业课复习
- 22:00-22:30 轻量任务（背单词/整理笔记）
"""
    
    schedule += """
**每日小贴士**
- 💡 上课前10分钟预习，事半功倍
- 💡 下课后当天复习，记忆最牢
- 💡 每周留半天机动，应对突发
"""
    
    return schedule

def generate_milestones(goals):
    """生成月度里程碑"""
    milestones = """
🎯 **学期里程碑**

**第1-2周：适应期**
- 搞清楚每门课的要求
- 建立学习节奏
- 完成选课调整

**第3-6周：稳定期**
- 各课程正常推进
- 开始第一个小目标
"""

    # 根据目标添加个性化里程碑
    for goal in goals:
        if "四级" in goal or "六级" in goal:
            milestones += "- 背完第一轮单词，开始刷真题\n"
        if "Python" in goal or "编程" in goal:
            milestones += "- 完成编程基础学习，做2个小项目\n"
        if "考研" in goal:
            milestones += "- 确定目标院校和专业，开始基础复习\n"
        if "实习" in goal:
            milestones += "- 完善简历，投递5-10家公司\n"

    milestones += """
**第7-10周：深化期**
- 期中考试准备
- 大作业/论文启动
- 检查目标进度

**第11-14周：冲刺期**
- 重点课程强化
- 期末复习开始
- 目标收尾

**第15-16周：收官期**
- 期末考试
- 学期总结
- 下学期规划
"""
    
    return milestones

def get_study_tips():
    """学习方法建议"""
    return """
💡 **高效学习方法**

**费曼学习法**
用自己的话把知识讲一遍，讲不清楚的地方就是没懂的地方。

**间隔重复**
- 第1天学完，第2天复习
- 第4天再复习，第7天再复习
- 记忆曲线变记忆直线！

**番茄工作法**
25分钟专注 + 5分钟休息
4个番茄后休息15-30分钟

**康奈尔笔记法**
- 右边：课堂笔记
- 左边：关键词和问题
- 底部：总结

**考试周策略**
- 先抓重点，后攻难点
- 做往年真题找规律
- 背诵放在考前最后两天
"""

def export_plan(plan, filename="semester_plan.md"):
    """导出计划为Markdown文件"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 学期学习计划\n\n")
        f.write(f"生成时间：{plan['generated_at']}\n\n")
        f.write("---\n\n")
        f.write(plan["overview"])
        f.write("\n---\n\n")
        f.write(plan["weekly_schedule"])
        f.write("\n---\n\n")
        f.write(plan["monthly_milestones"])
        f.write("\n---\n\n")
        f.write(plan["tips"])

# 示例使用
if __name__ == "__main__":
    # 示例输入
    example_courses = [
        {"name": "高等数学", "credits": 5, "difficulty": "hard"},
        {"name": "大学物理", "credits": 4, "difficulty": "medium"},
        {"name": "程序设计", "credits": 3, "difficulty": "medium"},
        {"name": "英语", "credits": 2, "difficulty": "easy"}
    ]
    
    example_goals = [
        "通过四级考试",
        "学好Python编程",
        "GPA达到3.5"
    ]
    
    example_constraints = {
        "max_study_hours": 28,
        "preferred_time": "morning"
    }
    
    plan = generate_semester_plan(example_courses, example_goals, example_constraints)
    print(plan["overview"])
    print("\n" + "="*50 + "\n")
    print(plan["weekly_schedule"])
