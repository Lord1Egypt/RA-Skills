#!/usr/bin/env python3
"""
访谈大纲生成器
用法: python3 interview_generator.py --goal <访谈主题> --count <问题数量> [--persona <用户画像描述>]
"""

import argparse
import sys
from datetime import datetime

# 访谈主题模板库
TOPIC_TEMPLATES = {
    "活动平台": ["报名流程", "活动发现方式", "信息获取习惯", "参与障碍"],
    "校园服务": ["使用频率", "服务满意度", "改进建议", "期望功能"],
    "教育产品": ["学习目标", "使用场景", "付费意愿", "替代方案"],
    "健康医疗": ["就医流程", "等待体验", "信息获取", "医患沟通"],
}

# 通用访谈问题类型
GENERAL_QUESTION_TYPES = [
    ("开场暖身", "请您简单介绍一下自己，以及您平时如何[相关行为]？"),
    ("行为习惯", "能描述一下您上一次[相关行为]的情况吗？"),
    ("动机挖掘", "促使您[相关行为]的主要原因是？"),
    ("痛点探索", "在这个过程中，您觉得最麻烦或最不方便的是什么？"),
    ("情感体验", "当[场景]时，您通常会有什么感受？"),
    ("期望需求", "如果可以改变[某方面]，您最希望改进什么？"),
    ("推荐建议", "您会给朋友推荐[产品/服务]吗？为什么？"),
    ("结束收尾", "还有什么关于[主题]的事情想补充吗？"),
]


def generate_interview_outline(goal: str, count: int = 8, persona: str = "") -> str:
    """生成访谈大纲"""
    
    output = f"""# 访谈大纲

**访谈主题**: {goal}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**用户画像**: {persona if persona else '待定义'}

---

## 访谈前准备

- [ ] 确认访谈时间和地点
- [ ] 准备知情同意书
- [ ] 测试录音设备
- [ ] 打印访谈大纲
- [ ] 准备小礼品（可选）

---

## 开场白（5分钟）

您好，感谢您参加本次访谈。我是[访谈员姓名]，今天大概需要30-45分钟。

**访谈目的**：了解您关于{goal}的真实体验和想法

**说明事项**：
- 没有正确答案，您的真实想法最重要
- 访谈过程中可以随时提问
- 如不想回答某问题，可以跳过
- 希望您能说出正在想的事情（出声思考）
- 需要您授权录音，仅用于研究分析

**确认**：您还有其他问题吗？我们开始吧。

---

## 正文访谈问题（共{count}个问题）

"""
    
    # 根据主题选择相关问题类型
    relevant_types = GENERAL_QUESTION_TYPES
    
    for i, (qtype, question_template) in enumerate(relevant_types[:count], 1):
        filled_question = question_template.replace("[相关行为]", goal).replace("[主题]", goal)
        output += f"""### {i}. [{qtype}]

**问题**：{filled_question}

**追问提示**：
- 能具体说说吗？
- 能举个例子吗？
- 为什么这样想？

**记录要点**：
- 回答内容：
- 表情/情绪：
- 特殊表述：

---
"""
    
    output += f"""## 结束语（5分钟）

**总结确认**：今天聊了很多，我总结一下我听到的[简要复述]，是这样吗？

**最终提问**：还有什么想补充的吗？

**致谢**：非常感谢您的时间！您的分享对我们帮助很大。

---

## 访谈后记录

| 项目 | 内容 |
|------|------|
| 访谈时长 | 分钟 |
| 访谈日期 | {datetime.now().strftime('%Y-%m-%d')} |
| 访谈员 | |
| 访谈地点 | |
| 关键洞察 | |
| 下一步 | |

---

## 使用说明

1. **访谈顺序**：按大纲顺序进行，但可根据实际灵活调整
2. **追问原则**：多问"为什么"和"能举个例子吗"，挖掘深层原因
3. **记录方式**：建议录音+手写笔记结合
4. **访谈人数**：建议5-8人，可发现80%以上的重要洞察
5. **数据分析**：访谈结束后24小时内整理访谈记录
"""
    
    return output


def main():
    parser = argparse.ArgumentParser(description="访谈大纲生成器")
    parser.add_argument("--goal", required=True, help="访谈主题/目标")
    parser.add_argument("--count", type=int, default=8, help="问题数量（默认8个）")
    parser.add_argument("--persona", default="", help="用户画像描述（可选）")
    parser.add_argument("--output", help="输出文件路径（可选，默认输出到标准输出）")
    
    args = parser.parse_args()
    
    if args.count < 3 or args.count > 15:
        print("问题数量建议控制在3-15个之间", file=sys.stderr)
        args.count = max(3, min(15, args.count))
    
    outline = generate_interview_outline(args.goal, args.count, args.persona)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(outline)
        print(f"✅ 访谈大纲已保存到: {args.output}")
    else:
        print(outline)


if __name__ == "__main__":
    main()
