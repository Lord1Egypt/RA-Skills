#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自媒体爆款标题生成器
根据内容主题和平台自动生成多个高点击率标题
"""

import sys
import json
import random
from typing import List, Dict

# 标题模板库
TEMPLATES = {
    "xiaohongshu": [
        "{age}岁{status}，我靠这{num}个{method}{result}💰",
        "后悔没早{action}！这个{thing}让我{benefit}✨",
        "{city}{time}，我{achievement}💪",
        "从{state1}到{state2}，我只做了这{num}件事",
        "{num}个{method}，{time}内{result}🔥",
        "真的绝了！{price}的东西比{high_price}的还好用",
        "{target}必看！这些{thing}太香了💖",
    ],
    "wechat": [
        "从{state1}到{state2}，我只做对了这{num}件事",
        "为什么你总是{pain_point}？这{num}个{thing}正在毁掉你",
        "{authority}研究：{action}，{benefit}",
        "{num}个{method}，帮你{solve_pain}",
        "揭秘：{phenomenon}背后的真相",
        "{target}的{num}个{method}，建议收藏",
    ],
    "douyin": [
        "你知道吗？{percent}%的人都不知道这个{thing}",
        "没想到！{low_price}块的东西比{high_price}块的还好用",
        "一定要看！这个视频可能帮你{benefit}",
        "{num}个{method}，让你{result}",
        "如果你现在{emotion}，一定要看完这个视频",
        "千万别{wrong_action}，否则{bad_result}",
    ],
    "zhihu": [
        "{target}如何{goal}？有哪些可行的路径？",
        "{experience}是一种怎样的体验？",
        "为什么越来越多的{target}{phenomenon}？",
        "有哪些{adjective}的{thing}推荐？",
        "{num}年{field}经验，我来回答这个问题",
        "如何评价{phenomenon}？",
    ],
    "bilibili": [
        "【全程高能】我花了{time}，{achievement}",
        "史上最强{thing}教程！看完你就是大神",
        "【第{num}期】挑战用{price}元{action}，结果...",
        "从入门到精通：{field}学习全攻略",
        "{age}岁{target}{achievement}，我做到了",
        "我尝试了{num}种{method}，最后只推荐这{action}",
    ],
}

# 数据填充库
DATA = {
    "age": ["25", "28", "30", "35"],
    "status": ["存款为 0", "一事无成", "月入 3 千", "刚毕业", "裸辞"],
    "num": ["3", "5", "7", "10"],
    "method": ["副业", "技巧", "方法", "习惯", "项目"],
    "result": ["月入 3 万", "存下 50 万", "瘦 10 斤", "逆袭人生", "实现自由"],
    "action": ["买", "学", "做", "开始", "坚持"],
    "thing": ["神器", "方法", "技巧", "习惯", "项目", "东西"],
    "benefit": ["每天多睡 1 小时", "省下一辆车", "瘦了 20 斤", "月入过万", "改变人生"],
    "city": ["上海", "北京", "深圳", "杭州"],
    "time": ["打工 5 年", "毕业 3 年", "北漂 8 年", "深漂 6 年"],
    "achievement": ["攒下第一个 50 万", "买了第一套房", "月入 10 万", "实现财务自由"],
    "state1": ["月薪 3 千", "胖 120 斤", "存款为 0", "职场小白"],
    "state2": ["月入 10 万", "瘦到 90 斤", "存款 50 万", "部门主管"],
    "price": ["10", "20", "50", "9.9"],
    "high_price": ["1000", "500", "200"],
    "target": ["上班族", "学生党", "宝妈", "女生", "普通人"],
    "pain_point": ["存不下钱", "没时间", "学不会", "没效果"],
    "authority": ["哈佛", "斯坦福", "清华", "北大", "专家"],
    "percent": ["90", "95", "99", "80"],
    "emotion": ["很累", "很迷茫", "很焦虑", "很辛苦"],
    "wrong_action": ["这样存钱", "盲目努力", "乱花钱", "熬夜"],
    "bad_result": ["越存越穷", "一事无成", "身体垮掉", "后悔莫及"],
    "goal": ["月入过万", "实现财务自由", "学会编程", "减肥成功"],
    "experience": ["工作 5 年存款为 0", "30 岁未婚", "裸辞创业", "北漂 10 年"],
    "phenomenon": ["选择不婚不育", "躺平", "提前退休", "离开大城市"],
    "adjective": ["相见恨晚", "实用", "靠谱", "高效"],
    "field": ["Python", "Excel", "写作", "剪辑", "英语"],
}


def generate_titles(topic: str = None, platform: str = "all", count: int = 5) -> Dict:
    """
    生成标题
    
    Args:
        topic: 内容主题
        platform: 目标平台
        count: 生成数量
    
    Returns:
        生成的标题列表和说明
    """
    results = {}
    
    platforms = list(TEMPLATES.keys()) if platform == "all" else [platform]
    
    for plat in platforms:
        if plat not in TEMPLATES:
            continue
            
        templates = TEMPLATES[plat]
        titles = []
        
        for _ in range(count):
            template = random.choice(templates)
            title = template
            
            # 填充变量
            for key, values in DATA.items():
                placeholder = "{" + key + "}"
                if placeholder in title:
                    title = title.replace(placeholder, random.choice(values), 1)
            
            titles.append(title)
        
        results[plat] = titles
    
    return {
        "topic": topic or "通用",
        "platform": platform,
        "titles": results,
        "tips": [
            "标题前几个字最关键（移动端展示限制）",
            "用数字增加具体性和可信度",
            "制造反差和悬念吸引点击",
            "避免违规词和敏感词",
            "多测试不同标题找最优"
        ]
    }


def main():
    # 默认参数
    topic = ""
    platform = "all"
    count = 5
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        try:
            params = json.loads(sys.argv[1])
            topic = params.get('topic', '')
            platform = params.get('platform', 'all')
            count = params.get('count', 5)
        except json.JSONDecodeError:
            topic = sys.argv[1]
    
    # 生成标题
    result = generate_titles(topic, platform, count)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
