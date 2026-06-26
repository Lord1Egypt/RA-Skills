#!/usr/bin/env python3
"""
小红书内容生成器核心脚本
Usage: python3 xhs_generator.py <主题> [领域]
"""

import sys
import json

# 预置内容模板
TEMPLATES = {
    "育儿": {
        "hooks": [
            "花了{X}年，做了{Y}件事。回头看，真正起作用的只有{Z}件。",
            "从崩溃到从容，我只做了这一个改变。",
            "大数据告诉我：{topic}，{X}%的家长都踩过这个坑。",
            "{X}岁娃的{topic}复盘，血泪教训总结。"
        ],
        "structures": [
            "痛点引入 → 误区分析 → 解决方案 → 互动引导",
            "数据对比 → 核心方法 → 实操步骤 → 效果展示",
            "真实经历 → 踩坑过程 → 转折发现 → 经验总结"
        ],
        "tags": ["#育儿经验", "#科学育儿", "#家长必读", "#孩子教育"]
    },
    "知识": {
        "hooks": [
            "用了{X}年，才悟透这个道理。",
            "{topic}的本质，一句话说清楚。",
            "{X}个{topic}技巧，第{Y}个最关键。",
            "从{topic}小白到入门，我只用了{X}天。"
        ],
        "structures": [
            "问题提出 → 原理解析 → 方法讲解 → 行动建议",
            "误区澄清 → 正确认知 → 实操指南 → 资源推荐"
        ],
        "tags": ["#学习方法", "#知识分享", "#自我提升", "#干货"]
    },
    "生活": {
        "hooks": [
            "{X}平米的{topic}，我整理了{Y}遍才满意。",
            "这个{topic}方法，让我省了{X}小时/周。",
            "被问爆的{topic}，今天一次性说清楚。",
            "{topic}{X}年，我的{N}个心得。"
        ],
        "structures": [
            "场景描述 → 问题呈现 → 解决方案 → 效果对比",
            "前后对比 → 方法详解 → 避坑指南 → 互动提问"
        ],
        "tags": ["#生活小技巧", "#居家好物", "#生活方式", "#实用"]
    }
}

# 标题生成公式
TITLE_FORMULAS = [
    "{topic}我做了{X}件事，数据显示只有这{Y}件真正有用",
    "{topic}｜这{Y}个方法让我{X}个月{result}",
    "{topic}避坑指南｜{Y}个家长常犯的错误",
    "从{before}到{after}，我只做对了这一件事",
    "{X}年{topic}经验，总结了这{Y}条血泪教训",
    "{topic}？别再{wrong_way}了，试试这个",
    "被问了{X}遍的{topic}，今天一次性说清楚",
    "{topic}｜{Y}招让你{result}"
]

def generate_title(topic, field="育儿"):
    """生成标题"""
    import random
    formula = random.choice(TITLE_FORMULAS)
    
    # 根据领域填充变量
    fillers = {
        "育儿": {"X": "一", "Y": "3", "result": "省心", "before": "焦虑", "after": "从容", "wrong_way": "盲目报班"},
        "知识": {"X": "3", "Y": "5", "result": "效率翻倍", "before": "迷茫", "after": "清晰", "wrong_way": "死记硬背"},
        "生活": {"X": "10", "Y": "5", "result": "轻松搞定", "before": "混乱", "after": "有序", "wrong_way": "瞎折腾"}
    }
    
    f = fillers.get(field, fillers["育儿"])
    title = formula.format(topic=topic, **f)
    return title

def generate_content(topic, field="育儿"):
    """生成正文"""
    import random
    
    template = TEMPLATES.get(field, TEMPLATES["育儿"])
    
    # 选择hook
    hook = random.choice(template["hooks"])
    hook = hook.format(topic=topic, X="一", Y="3", Z="3", N="5")
    
    # 构建正文结构
    content = f"""{hook}

❌ 先说误区/坑
很多家长在{topic}上花了很多时间和精力，但效果却不明显。常见的问题有：
• 盲目跟风，没有针对性
• 急于求成，忽略基础
• 方法不对，事倍功半

✅ 真正有效的方法

1️⃣ 【核心方法1】
简单可操作，坚持就有效果。

2️⃣ 【核心方法2】
循序渐进，不急不躁。

3️⃣ 【核心方法3】
从实际出发，因人而异。

💡 关键要点
• 不要追求完美，先做起来
• 给自己和孩子时间
• 及时调整，不断优化

{topic}不是一蹴而就的，需要耐心和坚持。

你有{topic}的经验吗？评论区聊聊👇
"""
    return content

def generate_tags(field="育儿"):
    """生成标签"""
    template = TEMPLATES.get(field, TEMPLATES["育儿"])
    base_tags = template["tags"]
    return " ".join(base_tags[:4])

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 xhs_generator.py <主题> [领域]")
        print("Example: python3 xhs_generator.py '幼小衔接' 育儿")
        sys.exit(1)
    
    topic = sys.argv[1]
    field = sys.argv[2] if len(sys.argv) > 2 else "育儿"
    
    title = generate_title(topic, field)
    content = generate_content(topic, field)
    tags = generate_tags(field)
    
    result = {
        "title": title,
        "content": content,
        "tags": tags,
        "field": field
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
