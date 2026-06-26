#!/usr/bin/env python3
"""
视频封面设计助手
提供封面文案、构图、配色等全方位设计方案
"""

import random

# 视频类型配置
VIDEO_TYPES = {
    "教程": {
        "style": "知识型、实用性",
        "colors": ["蓝色系", "绿色系", "白色系"],
        "elements": ["知识感", "专业感", "清晰"]
    },
    "娱乐": {
        "style": "轻松、有趣、吸引力",
        "colors": ["红色系", "橙色系", "紫色系"],
        "elements": ["趣味性", "情绪感", "活泼"]
    },
    "种草": {
        "style": "精致、真实、亲和",
        "colors": ["粉色系", "浅绿系", "暖色系"],
        "elements": ["美感", "真实感", "温暖"]
    },
    "剧情": {
        "style": "戏剧性、冲突感",
        "colors": ["深色系", "对比色", "电影感"],
        "elements": ["戏剧性", "冲突感", "悬念"]
    },
    "美食": {
        "style": "食欲感、温暖感",
        "colors": ["暖色系", "橙色系", "红色系"],
        "elements": ["食欲感", "新鲜感", "诱人"]
    }
}

# 平台尺寸配置
PLATFORM_SIZES = {
    "抖音": {"ratio": "9:16", "main_text": "左上/居中", "desc": "竖屏视频封面"},
    "快手": {"ratio": "9:16", "main_text": "居中", "desc": "竖屏视频封面"},
    "B站": {"ratio": "16:9", "main_text": "下方", "desc": "横屏视频封面"},
    "小红书": {"ratio": "3:4", "main_text": "居中偏上", "desc": "竖屏图文封面"},
    "视频号": {"ratio": "6:7", "main_text": "居中", "desc": "近似正方形"}
}

# 配色方案库
COLOR_PALETTES = {
    "红色系": {
        "primary": "#FF4757",
        "secondary": "#FF6B81",
        "text": "#FFFFFF",
        "shadow": "#C0392B",
        "scene": "高能量、紧迫感、促销"
    },
    "橙色系": {
        "primary": "#FF7F50",
        "secondary": "#FFA502",
        "text": "#FFFFFF",
        "shadow": "#E67E22",
        "scene": "活力、温暖、正能量"
    },
    "蓝色系": {
        "primary": "#3742FA",
        "secondary": "#70A1FF",
        "text": "#FFFFFF",
        "shadow": "#2C3E50",
        "scene": "专业、可信、冷静"
    },
    "紫色系": {
        "primary": "#8E44AD",
        "secondary": "#A29BFE",
        "text": "#FFFFFF",
        "shadow": "#6C3483",
        "scene": "神秘、高级、独特"
    },
    "绿色系": {
        "primary": "#2ECC71",
        "secondary": "#7BED9F",
        "text": "#FFFFFF",
        "shadow": "#27AE60",
        "scene": "健康、自然、成长"
    },
    "粉色系": {
        "primary": "#FD79A8",
        "secondary": "#FDCB6E",
        "text": "#FFFFFF",
        "shadow": "#E84393",
        "scene": "少女心、温馨、种草"
    },
    "黄色系": {
        "primary": "#F1C40F",
        "secondary": "#F39C12",
        "text": "#2C3E50",
        "shadow": "#D4AC0D",
        "scene": "警示、强调、突出"
    },
    "白色系": {
        "primary": "#FFFFFF",
        "secondary": "#F8F9FA",
        "text": "#2C3E50",
        "shadow": "#BDC3C7",
        "scene": "简洁、专业、知识感"
    }
}

# 主标题模板
MAIN_TITLE_TEMPLATES = [
    "这个{skill}太牛了！",
    "{number}个{skill}技巧，建议收藏",
    "学会这个{skill}，{benefit}翻倍",
    "难怪别人{result}，原来秘密是{skill}",
    "{skill}的正确姿势！",
    "这才是真正的{skill}！",
    "{skill}全攻略，一篇搞懂",
    "手把手教你{skill}，建议收藏",
    "终于找到了！{skill}的正确方法",
    "{skill}保姆级教程，建议收藏"
]

# 副标题模板
SUB_TITLE_TEMPLATES = [
    "看完少走3年弯路",
    "学会了你也能{result}",
    "新手必看的{skill}指南",
    "第3个技巧太关键了",
    "看完{topic}问题全搞定",
    "建议收藏备用",
    "越早知道越好",
    "吐血整理，建议收藏",
    "{number}分钟学会",
    "看这一篇就够了"
]


def generate_cover_design(topic, video_type="教程", platform="抖音", has_person=True):
    """生成封面设计方案"""
    
    # 获取配置
    type_config = VIDEO_TYPES.get(video_type, VIDEO_TYPES["教程"])
    platform_config = PLATFORM_SIZES.get(platform, PLATFORM_SIZES["抖音"])
    
    # 选择配色
    available_colors = type_config["colors"]
    selected_color_name = random.choice(available_colors)
    color_palette = COLOR_PALETTES.get(selected_color_name, COLOR_PALETTES["红色系"])
    
    # 生成文案
    main_title = generate_main_title(topic, type_config)
    sub_title = generate_sub_title(topic, type_config)
    tags = generate_tags(topic)
    
    # 生成构图建议
    composition = generate_composition(platform, has_person)
    
    # 生成元素清单
    elements = generate_elements(video_type, has_person)
    
    return {
        "topic": topic,
        "platform": platform,
        "platform_config": platform_config,
        "video_type": video_type,
        "text": {
            "main_title": main_title,
            "sub_title": sub_title,
            "tags": tags
        },
        "color": {
            "name": selected_color_name,
            "palette": color_palette,
            "scene": color_palette["scene"]
        },
        "composition": composition,
        "elements": elements
    }


def generate_main_title(topic, config):
    """生成主标题"""
    template = random.choice(MAIN_TITLE_TEMPLATES)
    
    # 提取关键词
    keywords = topic.replace("如何", "").replace("怎么", "").replace("教程", "").strip()
    skills = ["技巧", "方法", "操作", "攻略", "秘诀"]
    
    replacements = {
        "{topic}": topic,
        "{skill}": keywords or "这个",
        "{benefit}": random.choice(["效率", "效果", "成绩", "收益"]),
        "{result}": random.choice(["涨粉", "爆火", "出圈", "赚钱"]),
        "{number}": str(random.randint(3, 7))
    }
    
    for key, value in replacements.items():
        template = template.replace(key, value)
    
    return template


def generate_sub_title(topic, config):
    """生成副标题"""
    template = random.choice(SUB_TITLE_TEMPLATES)
    
    replacements = {
        "{topic}": topic.split("的")[0] if "的" in topic else topic,
        "{skill}": topic.replace("教程", "").strip(),
        "{result}": random.choice(["涨粉", "爆火", "出圈"]),
        "{number}": str(random.randint(3, 10))
    }
    
    for key, value in replacements.items():
        template = template.replace(key, value)
    
    return template


def generate_tags(topic):
    """生成标签词"""
    # 提取话题标签
    base_tags = ["#视频干货", "#实用技巧", "#建议收藏"]
    
    # 添加主题相关标签
    topic_tags = [f"#{topic[:4]}"] if len(topic) >= 4 else []
    
    return base_tags + topic_tags


def generate_composition(platform, has_person):
    """生成构图建议"""
    compositions = []
    
    if has_person:
        compositions.append("人物放在右下方黄金分割点（视觉焦点）")
        compositions.append("面部朝向画面中心，形成视觉引导")
        compositions.append("保持人物与文字区域适当留白")
    else:
        compositions.append("产品/内容主体居中或左三分线位置")
        compositions.append("右侧预留文字放置区域")
    
    compositions.append(f"背景采用{platform_config.get('ratio', '9:16')}比例")
    compositions.append("背景简洁，避免杂乱元素干扰")
    
    return compositions


def generate_elements(video_type, has_person):
    """生成封面元素清单"""
    elements = []
    
    # 人物表情
    if has_person:
        expressions = ["惊讶😲", "开心😄", "认真🧐", "坚定💪", "微笑😊"]
        elements.append({
            "name": "人物表情",
            "priority": 3,
            "requirement": f"选择{random.choice(expressions)}表情，引发好奇"
        })
    
    # 主标题
    elements.append({
        "name": "主标题",
        "priority": 3,
        "requirement": "白色黑边字，左上角或居中，字号要大"
    })
    
    # 副标题
    elements.append({
        "name": "副标题",
        "priority": 2,
        "requirement": "黄色或白色字，放在主标题下方"
    })
    
    # 背景
    elements.append({
        "name": "背景",
        "priority": 2,
        "requirement": "简洁纯色或简单场景，避免喧宾夺主"
    })
    
    # 装饰元素
    if video_type == "娱乐":
        elements.append({
            "name": "装饰元素",
            "priority": 1,
            "requirement": "可添加飘落元素/光效/emoji装饰"
        })
    
    return elements


def format_output(design):
    """格式化输出"""
    output = [
        "## 🖼️ 视频封面设计方案",
        f"### 视频主题：{design['topic']}",
        f"### 视频类型：{design['video_type']} | 目标平台：{design['platform']}",
        f"### 封面尺寸：{design['platform_config']['ratio']} ({design['platform_config']['desc']})",
        "",
        "---",
        "",
        "### 1. 封面文案",
        f"**主标题（大字）**：{design['text']['main_title']}",
        f"**副标题（小字）**：{design['text']['sub_title']}",
        f"**标签词**：{' '.join(design['text']['tags'])}",
        "",
        "### 2. 配色方案",
        f"- **主色调**：{design['color']['name']} ({design['color']['palette']['primary']})",
        f"- **辅色**：{design['color']['palette']['secondary']}",
        f"- **文字色**：{design['color']['palette']['text']}",
        f"- **适用场景**：{design['color']['scene']}",
        "",
        "### 3. 构图建议"
    ]
    
    for i, comp in enumerate(design['composition'], 1):
        output.append(f"{i}. {comp}")
    
    output.extend(["", "### 4. 封面元素清单", "", "| 元素 | 优先级 | 具体要求 |", "|------|--------|----------|"])
    
    for elem in design['elements']:
        stars = "⭐" * elem['priority']
        output.append(f"| {elem['name']} | {stars} | {elem['requirement']} |")
    
    output.extend([
        "",
        "---",
        "",
        "### 💡 实操建议"
    ])
    
    if design['platform'] in ["抖音", "快手"]:
        output.extend([
            "1. 真人出镜时，确保面部光线充足",
            "2. 文字不要遮挡主体人物",
            "3. 封面风格保持与账号整体风格一致",
            "4. 发布前用小号测试不同封面点击率"
        ])
    else:
        output.extend([
            "1. 横版视频注意文字在移动端的可读性",
            "2. 封面可添加视频章节时间标注",
            "3. B站封面可添加UP主头像水印"
        ])
    
    return "\n".join(output)


if __name__ == "__main__":
    # 测试
    design = generate_cover_design("视频剪辑技巧", "教程", "抖音", has_person=True)
    print(format_output(design))
