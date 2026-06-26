"""
文本工具模块
处理文本相关操作
"""

import re
from typing import List, Dict

def extract_keywords(text: str) -> List[str]:
    """
    提取关键词
    
    Args:
        text: 输入文本
    
    Returns:
        关键词列表
    """
    # 去重和清洗
    words = text.split()
    keywords = []
    
    for word in words:
        word = word.strip("，。！？.,!?")
        if len(word) >= 2:
            keywords.append(word)
    
    return list(set(keywords))

def normalize_color(color: str) -> str:
    """
    标准化颜色名称
    
    Args:
        color: 颜色描述
    
    Returns:
        标准颜色名称
    """
    color_map = {
        "黑": "黑色", "白": "白色", "灰": "灰色",
        "米": "米色", "杏": "杏色", "卡其": "卡其色",
        "棕": "棕色", "驼": "驼色", "咖": "咖啡色",
        "红": "红色", "粉": "粉色", "玫": "玫红",
        "橙": "橙色", "黄": "黄色",
        "绿": "绿色", "蓝": "蓝色", "藏青": "藏青色",
        "紫": "紫色", "条纹": "条纹", "格": "格纹"
    }
    
    for short, full in color_map.items():
        if short in color:
            return full
    
    return color

def normalize_category(category: str) -> str:
    """
    标准化类别名称
    
    Args:
        category: 类别描述
    
    Returns:
        标准类别名称
    """
    cat_map = {
        "外套": "outer", "大衣": "outer", "风衣": "outer", "西装": "outer",
        "上衣": "top", "T恤": "top", "衬衫": "top", "卫衣": "top", "毛衣": "top",
        "下装": "bottom", "裤子": "bottom", "裙子": "bottom", "裙": "bottom",
        "鞋": "shoes", "鞋子": "shoes",
        "配饰": "accessory", "包包": "accessory", "围巾": "accessory", "帽子": "accessory"
    }
    
    return cat_map.get(category, "top")

def format_list(items: List[str], sep: str = "、") -> str:
    """
    格式化列表为字符串
    
    Args:
        items: 列表项
        sep: 分隔符
    
    Returns:
        格式化字符串
    """
    return sep.join(str(i) for i in items)

def truncate(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 原文本
        max_length: 最大长度
        suffix: 后缀
    
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def parse_outfit_description(text: str) -> Dict[str, List[str]]:
    """
    解析穿搭描述
    
    Args:
        text: 穿搭描述文本
    
    Returns:
        分类后的单品列表
    """
    result = {"outer": [], "top": [], "bottom": [], "shoes": [], "accessory": []}
    
    # 简单关键词匹配
    keywords = {
        "outer": ["风衣", "大衣", "外套", "西装", "夹克", "羽绒服"],
        "top": ["T恤", "t恤", "衬衫", "卫衣", "毛衣", "针织衫", "背心"],
        "bottom": ["牛仔裤", "休闲裤", "西裤", "短裤", "裙子", "连衣裙", "半裙"],
        "shoes": ["运动鞋", "帆布鞋", "高跟鞋", "靴子", "皮鞋", "小白鞋", "拖鞋"],
        "accessory": ["包包", "围巾", "帽子", "项链", "耳环", "手链", "腰带"]
    }
    
    for category, words in keywords.items():
        for word in words:
            if word in text:
                result[category].append(word)
    
    return result
