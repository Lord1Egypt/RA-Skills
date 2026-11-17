#!/usr/bin/env python3
"""
养虾记副业方案生成器 v1.0
AI副业方案智能生成工具

功能：
1. 收集用户背景信息
2. 基于AI趋势推荐副业方向
3. 生成100天行动计划
4. 生成30秒自我介绍
5. 第一周行动清单

使用方式：
python3 sideproject_generator.py
"""

import json
from datetime import datetime

# 副业方向库
DIRECTION_LIBRARY = {
    "在职+内容向": {
        "方向": "小红书AI内容代运营",
        "启动难度": 2,
        "变现周期": "1-2个月",
        "推荐理由": "你有内容运营经验，AI可以大幅提升内容产出效率",
    },
    "在职+技术向": {
        "方向": "Skill开发卖钱",
        "启动难度": 3,
        "变现周期": "2-3个月",
        "推荐理由": "有技术背景，可以开发Skills在ClawHub销售",
    },
    "自由职业+内容向": {
        "方向": "AI内容工作室",
        "启动难度": 2,
        "变现周期": "1个月",
        "推荐理由": "时间灵活，适合规模化接单",
    },
    "待业+小白向": {
        "方向": "AI提示词代写",
        "启动难度": 1,
        "变现周期": "2-4周",
        "推荐理由": "门槛最低，AI帮你干活",
    },
    "创业者+服务向": {
        "方向": "企业AI培训",
        "启动难度": 3,
        "变现周期": "1-2个月",
        "推荐理由": "有客户资源，变现快",
    },
}

# 问题选项
QUESTIONS = [
    {
        "key": "work_status",
        "question": "你目前的工作状态？",
        "options": {
            "A": "在职，想找副业",
            "B": "自由职业，想拓展收入",
            "C": "创业者，想用AI提效",
            "D": "待业/学生，想入门AI",
        },
    },
    {
        "key": "time_available",
        "question": "你每周可以投入副业的时间？",
        "options": {
            "A": "每周 <5小时",
            "B": "每周5-10小时",
            "C": "每周10-20小时",
            "D": "每周 >20小时",
        },
    },
    {
        "key": "skill_background",
        "question": "你的技能背景？",
        "options": {
            "A": "技术/编程背景",
            "B": "内容/运营/营销背景",
            "C": "销售/商务背景",
            "D": "其他/无特殊技能",
        },
    },
    {
        "key": "ai_interest",
        "question": "你最想用AI做什么？",
        "options": {
            "A": "做内容（写文案/做视频/自媒体）",
            "B": "做工具（开发Skill/自动化脚本）",
            "C": "做服务（代写文案/代做数据分析）",
            "D": "还没想好",
        },
    },
    {
        "key": "resources",
        "question": "你的启动资源？",
        "options": {
            "A": "0资源，纯小白",
            "B": "有微信/私域流量",
            "C": "有自媒体账号",
            "D": "有技术/行业资源",
        },
    },
]


def collect_user_info():
    """收集用户信息"""
    print("\n" + "=" * 50)
    print("🦞 养虾记副业方案生成器 v1.0")
    print("=" * 50)
    print("请回答5个问题，我将为你生成定制化的AI副业方案\n")
    
    user_answers = {}
    
    for q in QUESTIONS:
        print(f"\n{q['question']}")
        for opt, text in q["options"].items():
            print(f"  {opt}: {text}")
        
        while True:
            choice = input("\n你的选择（A/B/C/D）: ").strip().upper()
            if choice in q["options"]:
                user_answers[q["key"]] = choice
                break
            print("请输入 A/B/C/D 中的一个")
    
    return user_answers


def recommend_direction(answers):
    """推荐副业方向"""
    # 简单规则：根据work_status + skill_background组合推荐
    status_map = {"A": "在职", "B": "自由职业", "C": "创业者", "D": "待业"}
    skill_map = {"A": "技术向", "B": "内容向", "C": "服务向", "D": "小白向"}
    
    key = f"{status_map.get(answers.get('work_status', 'A'), '在职')}+{skill_map.get(answers.get('skill_background', 'D'), '内容向')}"
    
    # 回退到默认
    if key not in DIRECTION_LIBRARY:
        key = "在职+内容向"
    
    return DIRECTION_LIBRARY.get(key, DIRECTION_LIBRARY["在职+内容向"])


def generate_100day_plan(direction):
    """生成100天行动计划"""
    return {
        "第一阶段（1-30天）启动": {
            "Week 1-2": "环境搭建 + 基础学习（OpenClaw部署、养虾记第1章）",
            "Week 3-4": "第一个小作品产出（发第一条内容/做一个简单Skill）",
        },
        "第二阶段（31-60天）打磨": {
            "Week 5-6": "产品/服务打磨 + 收集反馈",
            "Week 7-8": "小范围测试（邀请朋友试用）",
        },
        "第三阶段（61-100天）变现": {
            "Week 9-12": "正式推广 + 收入0→1突破",
        },
    }


def generate_self_intro(name="[你的名字]"):
    """生成30秒自我介绍"""
    return f"""我是{name}，目前从事[你的主业]。最近在探索AI副业，已完成第一个AI作品/内容。

如果你也对AI副业感兴趣，欢迎交流！"""


def generate_week1_plan():
    """生成第一周行动清单"""
    return [
        {"day": 1, "任务": "注册OpenClaw账号 + 部署第一个AI助手", "预计耗时": "30分钟"},
        {"day": 2, "任务": "学习养虾记第1章", "预计耗时": "1小时"},
        {"day": 3, "任务": "完成第一个自动化任务", "预计耗时": "1小时"},
        {"day": 4, "任务": "在知乎/小红书关注5个对标账号", "预计耗时": "30分钟"},
        {"day": 5, "任务": "尝试发第一条内容/帖子", "预计耗时": "1小时"},
        {"day": 6, "任务": "复盘 + 调整方向", "预计耗时": "1小时"},
        {"day": 7, "任务": "制定下周计划", "预计耗时": "30分钟"},
    ]


def generate_proposal(answers, direction):
    """生成完整的副业方案"""
    plan_100day = generate_100day_plan(direction)
    week1 = generate_week1_plan()
    
    output = f"""
# 🎯 你的AI副业方案

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 一、推荐方向

**{direction['方向']}**

- 启动难度：{'⭐' * direction['启动难度']}
- 预计变现周期：{direction['变现周期']}
- 推荐理由：{direction['推荐理由']}

---

## 二、100天行动计划

### 第一阶段（1-30天）：启动
{plan_100day['第一阶段（1-30天）启动']['Week 1-2']}
{plan_100day['第一阶段（1-30天）启动']['Week 3-4']}

### 第二阶段（31-60天）：打磨
{plan_100day['第二阶段（31-60天）打磨']['Week 5-6']}
{plan_100day['第二阶段（31-60天）打磨']['Week 7-8']}

### 第三阶段（61-100天）：变现
{plan_100day['第三阶段（61-100天）变现']['Week 9-12']}

---

## 三、30秒自我介绍

```
{generate_self_intro()}
```

---

## 四、第一周行动清单

| Day | 任务 | 预计耗时 |
|-----|------|----------|
"""
    
    for item in week1:
        output += f"| {item['day']} | {item['任务']} | {item['预计耗时']} |\n"
    
    output += """
---

## 五、风险提示

1. **时间不够**：先保证主业，副业时间弹性安排
2. **迟迟不行动**：从最小行动开始，先完成再完美
3. **中途放弃**：设置里程碑奖励，完成Week 4目标后给自己奖励

---

*养虾记副业方案生成器 v1.0*
"""
    
    return output


def main():
    """主函数"""
    try:
        # 1. 收集用户信息
        answers = collect_user_info()
        
        # 2. 推荐方向
        direction = recommend_direction(answers)
        
        # 3. 生成方案
        proposal = generate_proposal(answers, direction)
        
        # 4. 输出
        print("\n" + "=" * 50)
        print("🎉 方案生成完成！")
        print("=" * 50)
        print(proposal)
        
        # 5. 保存到文件
        output_file = "my_ai_sideproject_plan.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(proposal)
        print(f"\n📄 方案已保存到: {output_file}")
        
    except KeyboardInterrupt:
        print("\n\n👋 已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")


if __name__ == "__main__":
    main()