#!/usr/bin/env python3
"""
Study Buddy - 智能学习伴侣 CLI 工具
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# 数据存储目录，可通过 STUDY_BUDDY_HOME 隔离测试/演示数据
DATA_DIR = Path(os.environ.get("STUDY_BUDDY_HOME", "~/.study-buddy")).expanduser()
PROFILE_FILE = DATA_DIR / "profile.json"
PLANS_DIR = DATA_DIR / "plans"
LOGS_DIR = DATA_DIR / "logs"
WRONG_DIR = DATA_DIR / "wrong_questions"


def init_data_dir():
    """初始化数据目录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    WRONG_DIR.mkdir(parents=True, exist_ok=True)


def load_profile():
    """加载用户档案"""
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_profile(profile):
    """保存用户档案"""
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def cmd_help():
    """显示详细帮助信息"""
    print("""
📚 Study Buddy - 初高中学生家长学习陪伴助手
==================================================

核心命令：
  start              初始化学习档案（家长视角交互设置）
  today              查看今日学习任务
  checkin "内容"     学习打卡（记录学习内容和时长）
  plan               查看学习计划详情
  progress           查看学习进度统计
  report             生成学习周报
  wrong              错题本管理（add/list/review/master）
  feedback           获取学习反馈建议
  data               查看数据存储位置
  help               显示本帮助信息

常用示例：
  python3 scripts/study-buddy.py start
  python3 scripts/study-buddy.py today
  python3 scripts/study-buddy.py checkin "完成数学作业" --duration "45分钟"
  python3 scripts/study-buddy.py wrong add "二次函数求根错误" --subject "数学"
  python3 scripts/study-buddy.py report

数据存储：~/.study-buddy/（可用 STUDY_BUDDY_HOME 覆盖）
    """)


def cmd_start():
    """开始学习之旅 - 交互式收集学习背景（家长视角）"""
    print("🎯 欢迎使用 Study Buddy - 初高中学生家长学习陪伴助手！")
    print("=" * 50)
    print("\n👨‍👩‍👧 本工具帮助家长科学管理孩子的学习过程")
    print("   让我们一起为孩子建立学习档案...")
    
    profile = load_profile()
    if profile:
        print(f"\n📋 发现已有学习档案：{profile.get('student_name', '孩子')} - {profile.get('subject', '未设置')}")
        overwrite = input("是否重新设置？(y/N): ").strip().lower()
        if overwrite != 'y':
            print("保持现有设置。使用 /study-buddy today 查看今日任务。")
            return
    
    print("\n请回答以下问题，为孩子创建学习档案：")
    
    # 收集学习背景
    student_name = input("\n1. 孩子姓名（昵称也可）: ").strip()
    
    print("\n2. 当前学段：")
    print("   a) 初中")
    print("   b) 高中")
    grade_level = input("请选择 (a/b): ").strip().lower()
    
    subject = input("\n3. 主要学习科目（如：数学、英语、物理）: ").strip()
    
    print("\n4. 孩子目前的基础水平：")
    print("   a) 基础薄弱，需要补基础")
    print("   b) 中等水平，稳步提升")
    print("   c) 基础较好，追求拔高")
    print("   d) 成绩优秀，冲刺竞赛/高分")
    level = input("请选择 (a/b/c/d): ").strip().lower()
    
    daily_time = input("\n5. 每天计划投入多少时间学习该科目？（如：30分钟、1小时）: ").strip()
    
    print("\n6. 孩子偏好哪种学习方式？")
    print("   a) 看视频/网课")
    print("   b) 阅读教材/参考书")
    print("   c) 做题练习")
    print("   d) 混合方式")
    learning_style = input("请选择 (a/b/c/d): ").strip().lower()
    
    print("\n7. 学习目标类型：")
    print("   a) 培养兴趣，养成习惯")
    print("   b) 巩固基础，稳步提升")
    print("   c) 应对考试，冲刺提分")
    print("   d) 竞赛准备，深度拓展")
    goal_type = input("请选择 (a/b/c/d): ").strip().lower()
    
    deadline = input("\n8. 有重要时间节点吗？（如：期中考试2026-04-15，或直接回车）: ").strip()
    
    parent_notes = input("\n9. 家长备注（可选，如孩子特点、注意事项）: ").strip()
    
    # 构建档案
    profile = {
        "student_name": student_name,
        "grade_level": grade_level,
        "subject": subject,
        "level": level,
        "daily_time": daily_time,
        "learning_style": learning_style,
        "goal_type": goal_type,
        "deadline": deadline if deadline else None,
        "parent_notes": parent_notes if parent_notes else None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    save_profile(profile)
    
    print("\n" + "=" * 50)
    print("✅ 学习档案已创建！")
    print(f"\n👤 学生: {student_name}")
    print(f"📚 学习科目: {subject}")
    print(f"⏱️  每日计划: {daily_time}")
    
    # 生成初始学习计划
    print("\n📝 正在生成个性化学习计划...")
    generate_plan(profile)
    
    print("\n💡 家长提示：")
    print("   • 使用 /study-buddy today 查看今日任务")
    print("   • 建议每天固定时间学习，培养习惯")
    print("   • 每周使用 report 功能复盘学习情况")


def generate_plan(profile):
    """基于档案生成学习计划（针对初高中学生优化）"""
    plan = {
        "subject": profile["subject"],
        "student_name": profile.get("student_name", ""),
        "created_at": datetime.now().isoformat(),
        "phases": []
    }
    
    # 根据水平生成不同阶段
    level_map = {"a": "基础巩固", "b": "稳步提升", "c": "拔高突破", "d": "冲刺高分"}
    current_level = level_map.get(profile["level"], "基础巩固")
    
    # 学段映射
    grade_map = {"a": "初中", "b": "高中"}
    grade_text = grade_map.get(profile.get("grade_level", "a"), "中学")
    
    # 生成适合初高中学生的三阶段计划
    phases = [
        {
            "name": f"阶段一：{current_level}（适应期）",
            "duration": "2周",
            "focus": "建立学习习惯，熟悉学习节奏",
            "tasks": [
                f"每天固定时间学习{profile['subject']}，时长{profile.get('daily_time', '30分钟')}",
                "完成基础概念梳理，建立知识框架",
                "家长每日陪伴打卡，记录学习情况",
                "周末回顾本周学习内容，整理笔记"
            ],
            "parent_tips": "此阶段重点是培养习惯，不要急于求成，多鼓励少批评"
        },
        {
            "name": f"阶段二：系统提升（养成期）",
            "duration": "4-6周",
            "focus": "系统学习，稳步提升",
            "tasks": [
                "按计划完成每日学习任务",
                "建立错题本，记录并定期复习错题",
                "每周进行一次小测验或练习",
                "每月生成学习报告，评估进展"
            ],
            "parent_tips": "关注错题本，帮助孩子分析错误原因，针对性改进"
        },
        {
            "name": f"阶段三：巩固冲刺（巩固期）",
            "duration": "持续",
            "focus": "复习巩固，冲刺目标",
            "tasks": [
                "复习重点难点，查漏补缺",
                "模拟测试，检验学习效果",
                "错题二次复习，确保掌握",
                "调整学习策略，冲刺目标"
            ],
            "parent_tips": "考前保持平常心，关注孩子状态，合理安排作息"
        }
    ]
    
    plan["phases"] = phases
    
    # 保存计划
    plan_file = PLANS_DIR / f"plan_{datetime.now().strftime('%Y%m%d')}.json"
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print(f"\n📋 {profile.get('student_name', '孩子')}的{profile['subject']}学习计划已生成！")
    print(f"   共 {len(phases)} 个阶段")
    for i, phase in enumerate(phases, 1):
        print(f"   {i}. {phase['name']} ({phase['duration']})")
        print(f"      重点：{phase['focus']}")
    
    return plan


def cmd_today():
    """查看今日学习任务（家长视角）"""
    profile = load_profile()
    if not profile:
        print("⚠️  还没有学习档案。请先运行 /study-buddy start")
        return
    
    student_name = profile.get('student_name', '孩子')
    subject = profile['subject']
    
    print(f"🌟 今日学习任务 - {student_name}的{subject}")
    print("=" * 50)
    
    # 获取今天的日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 检查今日是否已打卡
    today_log_file = LOGS_DIR / f"{today}.json"
    if today_log_file.exists():
        with open(today_log_file, 'r', encoding='utf-8') as f:
            log = json.load(f)
        if isinstance(log, list):
            log = log[-1]
        print(f"\n✅ 今日已完成学习")
        print(f"   内容: {log.get('content', '无记录')}")
        print(f"   时长: {log.get('duration', '未记录')}")
    else:
        print(f"\n⏳ {student_name}今日还未打卡")
    
    # 显示建议任务
    print(f"\n📋 建议今日任务（{profile.get('daily_time', '30分钟')}）：")
    
    # 根据学习阶段给出不同建议
    log_files = list(LOGS_DIR.glob("*.json"))
    total_days = len(log_files)
    
    if total_days < 7:
        print(f"   1. 【适应期】{student_name}刚开始学习，重点培养习惯")
        print(f"   2. 完成{subject}基础内容复习")
        print(f"   3. 家长陪伴记录学习情况")
    elif total_days < 30:
        print(f"   1. 【养成期】按计划完成{subject}学习任务")
        print(f"   2. 整理今日学习笔记")
        print(f"   3. 如有错题，记录到错题本")
    else:
        print(f"   1. 【巩固期】{subject}系统复习")
        print(f"   2. 完成练习/测试")
        print(f"   3. 复习错题本中的题目")
    
    # 连续打卡提示
    streak = calculate_streak()
    if streak > 0:
        print(f"\n🔥 已连续打卡 {streak} 天")
    
    # 明日重点建议
    print(f"\n📌 明日重点建议：")
    if total_days < 3:
        print(f"   • 继续保持每日学习习惯，哪怕只有15分钟")
        print(f"   • 关注{student_name}的学习状态，及时鼓励")
    elif total_days < 7:
        print(f"   • 本周目标：连续打卡7天，建立稳定节奏")
        print(f"   • 周末可回顾本周学习内容，整理笔记")
    elif total_days < 30:
        print(f"   • 养成期关键：保持节奏，不要中断")
        print(f"   • 建议每周复习一次错题本")
    else:
        print(f"   • 巩固期：定期测试，查漏补缺")
        print(f"   • 关注{profile.get('deadline', '重要节点')}的进度")
    
    print(f"\n💡 打卡命令：/study-buddy checkin \"学习内容\" --duration \"时长\"")


def cmd_checkin(content, duration=None):
    """学习打卡"""
    profile = load_profile()
    if not profile:
        print("⚠️  还没有学习档案。请先运行 /study-buddy start")
        return
    
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS_DIR / f"{today}.json"
    
    log_entry = {
        "date": today,
        "content": content,
        "duration": duration or "未记录",
        "timestamp": datetime.now().isoformat(),
        "subject": profile.get('subject', '未知')
    }
    
    # 如果已有记录，追加
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        if isinstance(existing, list):
            existing.append(log_entry)
        else:
            existing = [existing, log_entry]
        log_entry = existing
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_entry, f, ensure_ascii=False, indent=2)
    
    print("✅ 打卡成功！")
    print(f"   学习内容: {content}")
    if duration:
        print(f"   学习时长: {duration}")
    
    # 计算连续打卡天数
    streak = calculate_streak()
    if streak > 1:
        print(f"\n🔥 连续打卡 {streak} 天！继续保持！")


def calculate_streak():
    """计算连续打卡天数"""
    streak = 0
    today = datetime.now()
    
    for i in range(365):  # 最多查一年
        check_date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        log_file = LOGS_DIR / f"{check_date}.json"
        if log_file.exists():
            streak += 1
        else:
            if i > 0:  # 如果不是今天，中断
                break
    
    return streak


def cmd_progress():
    """查看学习进度"""
    profile = load_profile()
    if not profile:
        print("⚠️  还没有学习档案。请先运行 /study-buddy start")
        return
    
    print(f"📊 学习进度报告 - {profile['subject']}")
    print("=" * 50)
    
    # 统计学习天数
    log_files = list(LOGS_DIR.glob("*.json"))
    total_days = len(log_files)
    
    # 统计本周学习
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    week_logs = [f for f in log_files if datetime.strptime(f.stem, '%Y-%m-%d') >= week_start]
    week_days = len(week_logs)
    
    # 连续打卡
    streak = calculate_streak()
    
    print(f"\n📈 统计数据：")
    print(f"   累计学习天数: {total_days} 天")
    print(f"   本周学习: {week_days} 天")
    print(f"   连续打卡: {streak} 天")
    
    # 显示最近的学习记录
    print(f"\n📝 最近学习记录：")
    recent_logs = sorted(log_files, reverse=True)[:5]
    for log_file in recent_logs:
        with open(log_file, 'r', encoding='utf-8') as f:
            log = json.load(f)
        if isinstance(log, list):
            log = log[-1]
        date = log.get('date', log_file.stem)
        content = log.get('content', '无记录')[:30]
        print(f"   {date}: {content}...")
    
    # 简单进度条
    print(f"\n⏳ 学习进度: {'█' * min(total_days, 20)}{'░' * (20 - min(total_days, 20))} {total_days}天")
    
    # 阶段提示
    print(f"\n📍 当前阶段：")
    if total_days < 7:
        print(f"   【适应期】重点：培养学习习惯，建立每日节奏")
        print(f"   建议：固定学习时间，哪怕只有15分钟，关键是坚持")
    elif total_days < 30:
        print(f"   【养成期】重点：巩固学习方法，形成稳定节奏")
        print(f"   建议：保持每日学习，开始整理笔记和错题")
    else:
        print(f"   【巩固期】重点：系统复习，查漏补缺")
        print(f"   建议：定期回顾错题，进行阶段性测试")
    
    # 家长提示
    print(f"\n👨‍👩‍👧 家长提示：")
    if streak >= 7:
        print(f"   太棒了！已连续打卡{streak}天，请继续保持！")
    elif streak >= 3:
        print(f"   不错！已连续{streak}天，再坚持几天就能养成习惯！")
    elif total_days == 0:
        print(f"   还没有学习记录，建议今天开始第一次打卡！")
    else:
        print(f"   学习节奏需要保持，建议固定每日学习时间")


def cmd_feedback():
    """获取学习反馈建议"""
    profile = load_profile()
    if not profile:
        print("⚠️  还没有学习档案。请先运行 /study-buddy start")
        return
    
    print(f"💡 学习反馈 - {profile['subject']}")
    print("=" * 50)
    
    # 基于简单规则的反馈
    streak = calculate_streak()
    log_files = list(LOGS_DIR.glob("*.json"))
    total_days = len(log_files)
    
    print("\n🎯 学习建议：")
    
    if streak >= 7:
        print("   ✅ 太棒了！你已经连续打卡一周以上，学习习惯正在养成！")
    elif streak >= 3:
        print("   👍 不错！连续打卡3天以上，继续保持这个节奏！")
    elif total_days == 0:
        print("   💪 刚开始学习？建议从每天15分钟开始，逐步建立习惯。")
    else:
        print("   📌 建议每天固定时间学习，哪怕只有15分钟，也比长时间中断好。")
    
    # 根据学习风格给建议
    style_map = {
        "a": "视频学习",
        "b": "阅读学习",
        "c": "实践学习",
        "d": "混合学习"
    }
    style = style_map.get(profile.get('learning_style', 'd'), '混合学习')
    print(f"\n📝 基于你的偏好（{style}）：")
    
    if profile.get('learning_style') == 'a':
        print("   - 推荐在B站、YouTube找优质教程")
        print("   - 看视频时做笔记，暂停思考")
    elif profile.get('learning_style') == 'b':
        print("   - 找一本经典教材系统学习")
        print("   - 建立自己的知识库/笔记系统")
    elif profile.get('learning_style') == 'c':
        print("   - 边学边做，从简单项目开始")
        print("   - 遇到问题再回头查资料")
    else:
        print("   - 结合多种方式：看视频+做练习+读文档")
        print("   - 根据内容灵活调整学习方式")
    
    print("\n🌟 下一步行动：")
    print("   1. 完成今日学习任务")
    print("   2. 记录学习心得")
    print("   3. 周末回顾本周所学")


def cmd_plan():
    """查看/管理学习计划"""
    profile = load_profile()
    if not profile:
        print("⚠️  还没有学习档案。请先运行 /study-buddy start")
        return
    
    print(f"📋 学习计划 - {profile['subject']}")
    print("=" * 50)
    
    # 加载最新计划
    plan_files = sorted(PLANS_DIR.glob("*.json"), reverse=True)
    if not plan_files:
        print("\n⏳ 还没有学习计划。正在生成...")
        generate_plan(profile)
        plan_files = sorted(PLANS_DIR.glob("*.json"), reverse=True)
    
    if plan_files:
        with open(plan_files[0], 'r', encoding='utf-8') as f:
            plan = json.load(f)
        
        print(f"\n📅 计划创建时间: {plan.get('created_at', '未知')[:10]}")
        print(f"📚 学习主题: {plan.get('subject', profile['subject'])}")
        print(f"🎯 阶段数量: {len(plan.get('phases', []))}")
        
        # 计算当前阶段
        log_files = list(LOGS_DIR.glob("*.json"))
        total_days = len(log_files)
        
        print(f"\n📊 各阶段详情：")
        for i, phase in enumerate(plan.get('phases', []), 1):
            # 简单估算当前阶段
            is_current = False
            if i == 1 and total_days < 14:
                is_current = True
            elif i == 2 and 14 <= total_days < 42:
                is_current = True
            elif i == 3 and total_days >= 42:
                is_current = True
            
            marker = "👉" if is_current else "  "
            print(f"\n{marker} 阶段{i}: {phase.get('name', '未命名')}")
            print(f"     时长: {phase.get('duration', '未设定')}")
            print(f"     任务:")
            for task in phase.get('tasks', []):
                print(f"       • {task}")
        
        print(f"\n💡 提示：使用 /study-buddy today 查看今日具体任务")


def cmd_report():
    """生成学习报告"""
    profile = load_profile()
    if not profile:
        print("⚠️  还没有学习档案。请先运行 /study-buddy start")
        return
    
    print(f"📊 学习报告 - {profile['subject']}")
    print("=" * 50)
    
    # 统计数据
    log_files = list(LOGS_DIR.glob("*.json"))
    total_days = len(log_files)
    streak = calculate_streak()
    
    # 计算本周数据
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    week_logs = [f for f in log_files if datetime.strptime(f.stem, '%Y-%m-%d') >= week_start]
    week_days = len(week_logs)
    
    # 计算本月数据
    month_start = datetime.now().replace(day=1)
    month_logs = [f for f in log_files if datetime.strptime(f.stem, '%Y-%m-%d') >= month_start]
    month_days = len(month_logs)
    
    print(f"\n📈 学习概况")
    print(f"   累计学习: {total_days} 天")
    print(f"   连续打卡: {streak} 天")
    print(f"   本周学习: {week_days} 天")
    print(f"   本月学习: {month_days} 天")
    
    # 学习频率评级
    print(f"\n🏆 学习评级")
    if streak >= 30:
        print("   🌟 卓越 - 连续打卡一个月，学习习惯非常棒！")
    elif streak >= 14:
        print("   ⭐ 优秀 - 连续两周打卡，保持得很好！")
    elif streak >= 7:
        print("   👍 良好 - 连续一周打卡，习惯正在养成！")
    elif streak >= 3:
        print("   ✨ 进步 - 连续打卡3天以上，继续加油！")
    elif total_days > 0:
        print("   🌱 起步 - 已经开始学习，建议每天打卡！")
    else:
        print("   📝 未开始 - 还没有学习记录，从今天开始吧！")
    
    # 阶段评估
    print(f"\n🎯 阶段评估")
    if total_days < 7:
        print("   当前处于：适应期")
        print("   建议：建立固定的学习时间，哪怕每天只有15分钟")
    elif total_days < 30:
        print("   当前处于：养成期")
        print("   建议：保持当前节奏，逐步增加学习时长")
    elif total_days < 90:
        print("   当前处于：巩固期")
        print("   建议：开始尝试更复杂的任务，挑战自己")
    else:
        print("   当前处于：进阶期")
        print("   建议：考虑深入学习或拓展相关领域")
    
    # 周学习热力图
    print(f"\n📅 本周学习热力图")
    print("-" * 30)
    week_days_labels = ['一', '二', '三', '四', '五', '六', '日']
    week_heatmap = []
    for i in range(7):
        day_date = week_start + timedelta(days=i)
        day_file = LOGS_DIR / f"{day_date.strftime('%Y-%m-%d')}.json"
        if day_file.exists():
            week_heatmap.append('█')
        else:
            week_heatmap.append('░')
    print(f"   {'  '.join(week_days_labels)}")
    print(f"   {'  '.join(week_heatmap)}")
    print(f"   █=已学  ░=未学  本周已学 {week_days}/7 天")
    
    # 错题掌握分布
    print(f"\n📝 错题掌握分布")
    print("-" * 30)
    wrong_file = WRONG_DIR / "wrong_questions.json"
    if wrong_file.exists():
        with open(wrong_file, 'r', encoding='utf-8') as f:
            wrong_list = json.load(f)
        mastered_count = sum(1 for w in wrong_list if w.get('mastered', False))
        unmastered_count = len(wrong_list) - mastered_count
        total_wrong = len(wrong_list)
        
        if total_wrong > 0:
            mastered_bar = '●' * mastered_count + '○' * unmastered_count
            print(f"   {mastered_bar}")
            print(f"   ● 已掌握: {mastered_count} 题")
            print(f"   ○ 未掌握: {unmastered_count} 题")
            print(f"   掌握率: {mastered_count}/{total_wrong} ({mastered_count*100//total_wrong}%)")
        else:
            print("   暂无错题记录")
    else:
        print("   暂无错题记录")
    
    # 下周目标
    print(f"\n📋 下周目标")
    print(f"   目标：连续打卡 {streak + 7} 天")
    print(f"   建议：每天投入 {profile.get('daily_time', '30分钟')}")
    print(f"   重点：保持学习节奏，记录学习心得")
    
    # 生成报告文件
    report_data = {
        "generated_at": datetime.now().isoformat(),
        "subject": profile['subject'],
        "stats": {
            "total_days": total_days,
            "streak": streak,
            "week_days": week_days,
            "month_days": month_days
        },
        "rating": "卓越" if streak >= 30 else "优秀" if streak >= 14 else "良好" if streak >= 7 else "进步" if streak >= 3 else "起步"
    }
    
    report_file = DATA_DIR / f"report_{datetime.now().strftime('%Y%m%d')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 报告已保存: {report_file}")


def cmd_wrong(action=None, content=None, subject=None):
    """错题本管理"""
    profile = load_profile()
    if not profile:
        print("⚠️  还没有学习档案。请先运行 /study-buddy start")
        return
    
    if action == "add" and content:
        # 添加错题
        wrong_entry = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "content": content,
            "subject": subject or profile['subject'],
            "added_at": datetime.now().isoformat(),
            "review_count": 0,
            "last_review": None,
            "mastered": False
        }
        
        wrong_file = WRONG_DIR / "wrong_questions.json"
        wrong_list = []
        if wrong_file.exists():
            with open(wrong_file, 'r', encoding='utf-8') as f:
                wrong_list = json.load(f)
        
        wrong_list.append(wrong_entry)
        
        with open(wrong_file, 'w', encoding='utf-8') as f:
            json.dump(wrong_list, f, ensure_ascii=False, indent=2)
        
        print("✅ 错题已记录")
        print(f"   内容: {content[:50]}..." if len(content) > 50 else f"   内容: {content}")
        print(f"   学科: {wrong_entry['subject']}")
        print(f"\n💡 使用 /study-buddy wrong list 查看所有错题")
        
    elif action == "list":
        # 列出错题
        wrong_file = WRONG_DIR / "wrong_questions.json"
        if not wrong_file.exists():
            print("📭 错题本为空")
            print("\n💡 使用 /study-buddy wrong add \"错题内容\" 添加错题")
            return
        
        with open(wrong_file, 'r', encoding='utf-8') as f:
            wrong_list = json.load(f)
        
        if not wrong_list:
            print("📭 错题本为空")
            return
        
        print(f"📚 错题本 - 共 {len(wrong_list)} 题")
        print("=" * 50)
        
        # 按掌握状态分组
        unmastered = [w for w in wrong_list if not w.get('mastered', False)]
        mastered = [w for w in wrong_list if w.get('mastered', False)]
        
        if unmastered:
            print(f"\n📝 待复习 ({len(unmastered)} 题):")
            for i, w in enumerate(unmastered[-5:], 1):  # 显示最近5题
                content = w['content'][:40] + "..." if len(w['content']) > 40 else w['content']
                review_info = f"(已复习{w.get('review_count', 0)}次)" if w.get('review_count', 0) > 0 else ""
                print(f"   {i}. [{w['subject']}] {content} {review_info}")
        
        if mastered:
            print(f"\n✅ 已掌握 ({len(mastered)} 题):")
            print(f"   共 {len(mastered)} 题已标记为掌握")
        
        print(f"\n💡 复习建议：优先复习待复习的题目")
        
    elif action == "review" and content:
        # 标记复习
        wrong_file = WRONG_DIR / "wrong_questions.json"
        if not wrong_file.exists():
            print("⚠️  错题本为空")
            return
        
        with open(wrong_file, 'r', encoding='utf-8') as f:
            wrong_list = json.load(f)
        
        # 查找并更新
        found = False
        for w in wrong_list:
            if w['id'] == content or w['content'] == content:
                w['review_count'] = w.get('review_count', 0) + 1
                w['last_review'] = datetime.now().isoformat()
                found = True
                print(f"✅ 已记录复习: {w['content'][:30]}...")
                print(f"   累计复习 {w['review_count']} 次")
                
                # 如果复习3次以上，建议标记掌握
                if w['review_count'] >= 3:
                    print(f"\n💡 这道题已复习3次，是否标记为已掌握？")
                    print(f"   使用 /study-buddy wrong master \"{w['id']}\" 标记掌握")
                break
        
        if found:
            with open(wrong_file, 'w', encoding='utf-8') as f:
                json.dump(wrong_list, f, ensure_ascii=False, indent=2)
        else:
            print("⚠️  未找到该错题")
            
    elif action == "master" and content:
        # 标记掌握
        wrong_file = WRONG_DIR / "wrong_questions.json"
        if not wrong_file.exists():
            print("⚠️  错题本为空")
            return
        
        with open(wrong_file, 'r', encoding='utf-8') as f:
            wrong_list = json.load(f)
        
        found = False
        for w in wrong_list:
            if w['id'] == content or w['content'] == content:
                w['mastered'] = True
                w['mastered_at'] = datetime.now().isoformat()
                found = True
                print(f"✅ 已标记掌握: {w['content'][:30]}...")
                break
        
        if found:
            with open(wrong_file, 'w', encoding='utf-8') as f:
                json.dump(wrong_list, f, ensure_ascii=False, indent=2)
        else:
            print("⚠️  未找到该错题")
    else:
        # 显示帮助
        print("📚 错题本管理")
        print("=" * 50)
        print("\n用法:")
        print("   /study-buddy wrong add \"错题内容\" [--subject \"学科\"]")
        print("   /study-buddy wrong list")
        print("   /study-buddy wrong review \"错题ID\"")
        print("   /study-buddy wrong master \"错题ID\"")
        print("\n示例:")
        print('   /study-buddy wrong add "二次函数求根公式应用错误"')
        print('   /study-buddy wrong list')


def cmd_data():
    """查看数据存储位置"""
    print("📁 Study Buddy 数据存储位置")
    print("=" * 50)
    print(f"\n数据目录: {DATA_DIR}")
    print(f"   档案文件: {PROFILE_FILE}")
    print(f"   计划目录: {PLANS_DIR}")
    print(f"   日志目录: {LOGS_DIR}")
    print(f"   错题目录: {WRONG_DIR}")
    
    # 检查数据是否存在
    if PROFILE_FILE.exists():
        print(f"\n✅ 学习档案: 已存在")
    else:
        print(f"\n⏳ 学习档案: 未创建")
    
    plan_count = len(list(PLANS_DIR.glob("*.json")))
    log_count = len(list(LOGS_DIR.glob("*.json")))
    wrong_count = 0
    wrong_file = WRONG_DIR / "wrong_questions.json"
    if wrong_file.exists():
        with open(wrong_file, 'r', encoding='utf-8') as f:
            wrong_count = len(json.load(f))
    
    print(f"📋 学习计划: {plan_count} 个")
    print(f"📝 学习记录: {log_count} 条")
    print(f"❌ 错题记录: {wrong_count} 题")


def main():
    """主入口"""
    init_data_dir()
    
    parser = argparse.ArgumentParser(
        description="Study Buddy - 智能学习伴侣",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  study-buddy start              # 开始学习之旅
  study-buddy today              # 查看今日任务
  study-buddy checkin "内容"      # 学习打卡
  study-buddy progress           # 查看进度
  study-buddy feedback           # 获取反馈
  study-buddy plan               # 查看学习计划
  study-buddy report             # 生成学习报告
  study-buddy wrong add "内容"    # 添加错题
  study-buddy wrong list         # 查看错题
  study-buddy data               # 查看数据位置
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # help 命令
    subparsers.add_parser('help', help='显示详细帮助信息')
    
    # start 命令
    subparsers.add_parser('start', help='开始学习之旅（交互式设置）')
    
    # today 命令
    subparsers.add_parser('today', help='查看今日学习任务')
    
    # checkin 命令
    checkin_parser = subparsers.add_parser('checkin', help='学习打卡')
    checkin_parser.add_argument('content', help='学习内容')
    checkin_parser.add_argument('--duration', '-d', help='学习时长（如：30分钟）')
    
    # progress 命令
    subparsers.add_parser('progress', help='查看学习进度')
    
    # feedback 命令
    subparsers.add_parser('feedback', help='获取学习反馈建议')
    
    # plan 命令 - 查看学习计划
    subparsers.add_parser('plan', help='查看学习计划详情')
    
    # report 命令 - 学习报告
    subparsers.add_parser('report', help='生成学习报告')
    
    # wrong 命令 - 错题本
    wrong_parser = subparsers.add_parser('wrong', help='错题本管理')
    wrong_subparsers = wrong_parser.add_subparsers(dest='wrong_action', help='错题本操作')
    
    # wrong add
    wrong_add = wrong_subparsers.add_parser('add', help='添加错题')
    wrong_add.add_argument('content', help='错题内容')
    wrong_add.add_argument('--subject', '-s', help='学科（可选）')
    
    # wrong list
    wrong_subparsers.add_parser('list', help='列出错题')
    
    # wrong review
    wrong_review = wrong_subparsers.add_parser('review', help='记录复习')
    wrong_review.add_argument('content', help='错题ID或内容')
    
    # wrong master
    wrong_master = wrong_subparsers.add_parser('master', help='标记掌握')
    wrong_master.add_argument('content', help='错题ID或内容')
    
    # data 命令
    subparsers.add_parser('data', help='查看数据存储位置')
    
    args = parser.parse_args()
    
    if args.command == 'help':
        cmd_help()
    elif args.command == 'start':
        cmd_start()
    elif args.command == 'today':
        cmd_today()
    elif args.command == 'checkin':
        cmd_checkin(args.content, args.duration)
    elif args.command == 'progress':
        cmd_progress()
    elif args.command == 'feedback':
        cmd_feedback()
    elif args.command == 'plan':
        cmd_plan()
    elif args.command == 'report':
        cmd_report()
    elif args.command == 'wrong':
        if hasattr(args, 'wrong_action') and args.wrong_action:
            if args.wrong_action == 'add':
                cmd_wrong('add', args.content, args.subject)
            elif args.wrong_action == 'list':
                cmd_wrong('list')
            elif args.wrong_action == 'review':
                cmd_wrong('review', args.content)
            elif args.wrong_action == 'master':
                cmd_wrong('master', args.content)
            else:
                cmd_wrong()
        else:
            cmd_wrong()
    elif args.command == 'data':
        cmd_data()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
