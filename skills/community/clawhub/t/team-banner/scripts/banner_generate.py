#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
团建横幅标语生成服务 - 实际横幅标语生成脚本
"""

import os
import sys
import json
import random

# 添加脚本所在目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from file_utils import load_order, load_config


# 团建横幅标语素材库
BANNER_DATABASE = {
    "年会": [
        "凝心聚力 共创辉煌",
        "筑梦前行 乘风破浪",
        "砥砺前行 续写华章",
        "携手并进 赢战未来",
        "同心同德 继往开来"
    ],
    "团建": [
        "团结协作 超越自我",
        "凝聚力量 共享快乐",
        "挑战自我 熔炼团队",
        "激情无限 团队最强",
        "并肩作战 共创佳绩"
    ],
    "户外拓展": [
        "挑战极限 超越自我",
        "勇攀高峰 砥砺前行",
        "征服自然 磨练意志",
        "团结互助 共渡难关",
        "超越梦想 领跑未来"
    ],
    "销售团队": [
        "业绩为王 使命必达",
        "签单不停 业绩飙升",
        "目标必达 勇创佳绩",
        "成单为荣 业绩为王",
        "狭路相逢勇者胜"
    ],
    "拓展训练": [
        "突破自我 挑战极限",
        "熔炼团队 超越自我",
        "激发潜能 创造奇迹",
        "团结协作 勇往直前",
        "挑战不可能"
    ]
}

# 默认横幅标语
DEFAULT_BANNERS = [
    "团结协作 勇攀高峰",
    "凝聚力量 创造辉煌",
    "携手共进 筑梦未来",
    "挑战自我 超越极限",
    "砥砺前行 共创佳绩"
]


def detect_type(question: str) -> str:
    """检测团建类型"""
    question = question.lower()
    
    types = {
        "年会": ["年会", "年终", "晚会", "庆典"],
        "团建": ["团建", "团队建设", "团活动"],
        "户外拓展": ["户外", "拓展", "野外", "徒步", "登山"],
        "销售团队": ["销售", "业务", "营销"],
        "拓展训练": ["拓展", "训练", "军训"]
    }
    
    for key, keywords in types.items():
        for word in keywords:
            if word in question:
                return key
    
    return ""


def generate_banner(question: str) -> dict:
    """根据场景生成横幅标语"""
    
    # 检测类型
    banner_type = detect_type(question)
    
    # 根据类型选择横幅标语
    if banner_type and banner_type in BANNER_DATABASE:
        banners = BANNER_DATABASE[banner_type]
    else:
        banners = DEFAULT_BANNERS
    
    # 随机选择
    banner = random.choice(banners)
    
    result = {
        "横幅标语": banner,
        "类型": banner_type if banner_type else "通用"
    }
    
    return result


def main():
    if len(sys.argv) < 2:
        print("ERROR: 缺少订单号参数", file=sys.stderr)
        print("PAY_STATUS: ERROR")
        print("ERROR_INFO: 缺少订单号参数")
        sys.exit(1)
    
    order_no = sys.argv[1]
    
    # 加载配置获取skill name
    config = load_config()
    skill_name = config.get('skillName', 'team-banner')
    
    # 计算indicator
    import hashlib
    indicator = hashlib.md5(skill_name.encode('utf-8')).hexdigest()
    
    try:
        # 加载订单信息
        order_data = load_order(indicator, order_no)
        
        # 获取问题/场景描述
        question = order_data.get('question', '')
        
        # 生成横幅标语
        banner = generate_banner(question)
        
        # 输出结果
        print(f"PAY_STATUS: 成功")
        print(f"横幅标语: {banner['横幅标语']}")
        
    except FileNotFoundError as e:
        print(f"PAY_STATUS: ERROR")
        print(f"ERROR_INFO: 订单文件不存在")
        sys.exit(1)
    except Exception as e:
        print(f"PAY_STATUS: ERROR")
        print(f"ERROR_INFO: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
