#!/usr/bin/env python3
"""
小红书评论策略生成器
Usage: python3 comment_generator.py <笔记内容> [人设]
"""

import sys
import json

# 评论模板
COMMENT_TEMPLATES = {
    "共情型": [
        "太理解了！我也是这样，{experience}。后来{solution}，现在好多了。",
        "抱抱！{situation}真的不容易。我之前也经历过，{encouragement}",
        "看完太有共鸣了...{personal_story}。共勉！💪"
    ],
    "经验分享型": [
        "{agreement}！我自己试过{method}，效果挺明显的。关键是{key_point}。",
        "这个方法不错！我再补充一点：{additional_tip}。希望对有帮助～",
        "实践过，确实有效！{result}。建议{recommendation}。"
    ],
    "提问互动型": [
        "{appreciation}！想请教一下：{question}？",
        "很有启发！{situation}你是怎么处理的？",
        "谢谢分享！{topic}方面，你还有其他建议吗？"
    ],
    "幽默风趣型": [
        "哈哈太真实了！{funny_observation}😂",
        "{relatable_comment}，简直是我本人了！",
        "看完笑出声，{humorous_twist}"
    ]
}

def generate_comments(note_content, persona="普通用户", count=3):
    """生成评论"""
    import random
    
    comments = []
    styles = list(COMMENT_TEMPLATES.keys())
    
    for i in range(min(count, len(styles))):
        style = styles[i]
        template = random.choice(COMMENT_TEMPLATES[style])
        
        # 根据笔记内容填充变量
        comment = template.format(
            experience="试了很多方法",
            solution="找到合适的方式",
            situation="",
            encouragement="加油！",
            personal_story="",
            agreement="说得对",
            method="",
            key_point="坚持",
            additional_tip="",
            result="",
            recommendation="可以试试",
            appreciation="很有用",
            question="",
            topic="",
            funny_observation="",
            relatable_comment="",
            humorous_twist=""
        )
        
        comments.append({
            "style": style,
            "comment": comment
        })
    
    return comments

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 comment_generator.py '<笔记内容>' [人设]")
        print("Example: python3 comment_generator.py '孩子写作业拖拉怎么办' 育儿博主")
        sys.exit(1)
    
    note_content = sys.argv[1]
    persona = sys.argv[2] if len(sys.argv) > 2 else "普通用户"
    
    comments = generate_comments(note_content, persona)
    
    result = {
        "note": note_content[:50] + "...",
        "persona": persona,
        "comments": comments
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
