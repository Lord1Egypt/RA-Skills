"""
Activity classifier for time-guru.
Auto-categorizes activities based on keywords.
"""
import re
from typing import Dict, Optional

# Category definitions with keywords
CATEGORIES = {
    "开发": {
        "keywords_cn": ["写代码", "编程", "开发", "debug", "调试", "修bug", "改bug", 
                        "重构", "实现", "代码", "push", "commit", "部署", "发布",
                        "写API", "前端", "后端", "测试", "单元测试", "集成测试"],
        "keywords_en": ["code", "program", "debug", "implement", "refactor", "deploy",
                        "development", "coding", "fix", "test", "commit", "push"],
    },
    "会议": {
        "keywords_cn": ["开会", "会议", "评审", "讨论", "sprint", "规划", "复盘",
                        "早会", "晚会", "standup", "sync", "对齐", "周会"],
        "keywords_en": ["meeting", "standup", "sync", "review", "planning", "retro",
                        "discussion", "call", "catch up"],
    },
    "文档": {
        "keywords_cn": ["写文档", "文档", "report", "报告", "方案", "设计文档",
                        "周报", "日报", "总结", "笔记", "API文档"],
        "keywords_en": ["document", "report", "write-up", "spec", "readme", "wiki"],
    },
    "设计": {
        "keywords_cn": ["设计", "UI", "UX", "原型", "figma", "sketch", "画图",
                        "设计稿", "交互", "视觉", "排版"],
        "keywords_en": ["design", "ui", "ux", "wireframe", "mockup", "prototype"],
    },
    "管理": {
        "keywords_cn": ["管理", "安排", "计划", "统筹", "协调", "招聘", "面试",
                        "绩效", "1-on-1", "one on one", "邮件", "审批"],
        "keywords_en": ["manage", "admin", "planning", "coordinate", "email",
                        "review", "1:1", "interview"],
    },
    "学习": {
        "keywords_cn": ["学习", "看书", "读书", "课程", "教程", "培训", "网课",
                        "阅读", "研究", "探索", "技术", "新知识", "study"],
        "keywords_en": ["learn", "study", "read", "book", "course", "training",
                        "tutorial", "research"],
    },
    "通勤": {
        "keywords_cn": ["通勤", "路上", "地铁", "公交", "开车", "骑车", "步行",
                        "上班路上", "下班路上"],
        "keywords_en": ["commute", "drive", "transit", "travel", "way to work"],
    },
    "休息": {
        "keywords_cn": ["休息", "午休", "吃饭", "午餐", "晚餐", "break", "咖啡",
                        "散步", "运动", "锻炼", "午睡", "小憩"],
        "keywords_en": ["break", "lunch", "dinner", "rest", "nap", "walk", "coffee"],
    },
    "运动": {
        "keywords_cn": ["跑步", "健身", "游泳", "瑜伽", "骑行", "打球", "运动",
                        "跑步机", "椭圆机", "力量训练", "有氧"],
        "keywords_en": ["exercise", "run", "gym", "swim", "yoga", "workout"],
    },
}


def classify_activity(description: str) -> str:
    """
    Classify an activity description into a category.
    
    Args:
        description: Text description of the activity.
        
    Returns:
        Category string (from CATEGORIES keys, or "其他" for unknown).
    """
    if not description:
        return "其他"
    
    text_lower = description.lower()
    
    scores = {}
    for category, keywords in CATEGORIES.items():
        score = 0
        for kw in keywords.get("keywords_cn", []):
            if kw.lower() in text_lower:
                score += 2
        for kw in keywords.get("keywords_en", []):
            if kw.lower() in text_lower:
                score += 2
        if score > 0:
            scores[category] = score
    
    if not scores:
        return "其他"
    
    return max(scores, key=scores.get)


def suggest_tags(description: str) -> list:
    """
    Suggest tags from an activity description.
    
    Returns list of tags (max 5).
    """
    if not description:
        return []
    
    text = description.lower()
    tags = []
    
    # Common tag patterns
    tag_patterns = [
        (r'(bug|fix|修复)', "bug-fix"),
        (r'(feature|功能|特性)', "feature"),
        (r'refactor|refactoring|重构', "refactoring"),
        (r'(api|endpoint|接口)', "api"),
        (r'(ui|ux|frontend|前端)', "frontend"),
        (r'(backend|后端|server)', "backend"),
        (r'(database|db|数据|sql)', "database"),
        (r'(test|测试)', "testing"),
        (r'(deploy|发布|部署)', "deployment"),
        (r'(doc|docs|文档)', "documentation"),
    ]
    
    seen = set()
    for pattern, tag in tag_patterns:
        if re.search(pattern, text) and tag not in seen:
            tags.append(tag)
            seen.add(tag)
    
    return tags[:5]
