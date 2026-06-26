#!/usr/bin/env python3
"""
每日五行运势分析器
根据当日天干地支与个人八字分析运势
"""

from datetime import datetime
from typing import Dict, Tuple, List
import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calculate_wuxing import (
    TIANGAN, DIZHI, TIANGAN_WUXING, DIZHI_WUXING,
    get_year_ganzhi, get_month_ganzhi, get_day_ganzhi,
    get_hour_ganzhi, get_shichen
)


def get_today_ganzhi() -> Tuple[str, str]:
    """获取今日的天干地支"""
    today = datetime.now()
    return get_day_ganzhi(today.year, today.month, today.day)


def analyze_daily_fortune(day_master: str, today_gan: str, today_zhi: str, 
                          personal_wuxing: Dict[str, int]) -> Dict:
    """分析当日运势"""
    
    day_master_wx = TIANGAN_WUXING[day_master]
    today_gan_wx = TIANGAN_WUXING[today_gan]
    today_zhi_wx = DIZHI_WUXING[today_zhi]
    
    # 五行生克关系
    sheng_relations = {
        "木": "火", "火": "土", "土": "金", 
        "金": "水", "水": "木"
    }
    ke_relations = {
        "木": "土", "土": "水", "水": "火", 
        "火": "金", "金": "木"
    }
    
    # 判断与日主的关系
    def get_relation(wx1: str, wx2: str) -> str:
        if wx1 == wx2:
            return "同"
        if sheng_relations.get(wx1) == wx2:
            return "生"  # wx1生wx2
        if sheng_relations.get(wx2) == wx1:
            return "被生"  # wx2生wx1
        if ke_relations.get(wx1) == wx2:
            return "克"  # wx1克wx2
        if ke_relations.get(wx2) == wx1:
            return "被克"  # wx2克wx1
        return "无关"
    
    gan_relation = get_relation(day_master_wx, today_gan_wx)
    
    # 运势评级
    relation_score = {
        "被生": (5, "大吉"),
        "同": (4, "吉"),
        "生": (3, "平"),
        "克": (2, "凶"),
        "被克": (2, "需注意"),
        "无关": (3, "平")
    }
    
    score, rating = relation_score.get(gan_relation, (3, "平"))
    
    # 生成宜忌
    yi_list = []
    ji_list = []
    
    if gan_relation in ["被生", "同"]:
        yi_list.extend(["签约", "求财", "出行", "社交", "学习"])
        ji_list.extend(["冒险", "冲动消费"])
    elif gan_relation == "生":
        yi_list.extend(["付出", "创作", "帮助他人", "规划"])
        ji_list.extend(["过度消耗", "强求"])
    elif gan_relation in ["克", "被克"]:
        yi_list.extend(["谨慎", "内省", "整理", "休息"])
        ji_list.extend(["重大决策", "投资", "争吵", "高风险活动"])
    else:
        yi_list.extend(["按部就班", "日常事务"])
        ji_list.extend(["激进变革"])
    
    # 幸运元素
    lucky_color = {
        "金": "白色、金色",
        "木": "绿色、青色",
        "水": "黑色、蓝色",
        "火": "红色、紫色",
        "土": "黄色、棕色"
    }
    
    lucky_direction = {
        "金": "西方",
        "木": "东方",
        "水": "北方",
        "火": "南方",
        "土": "中央"
    }
    
    return {
        "today_ganzhi": (today_gan, today_zhi),
        "today_wuxing": (today_gan_wx, today_zhi_wx),
        "day_master": day_master,
        "day_master_wuxing": day_master_wx,
        "relation": gan_relation,
        "score": score,
        "rating": rating,
        "yi": yi_list,
        "ji": ji_list,
        "lucky": {
            "color": lucky_color.get(today_gan_wx, "根据喜好"),
            "direction": lucky_direction.get(today_gan_wx, "根据情况"),
            "number": str(score)
        }
    }


def format_daily_fortune(fortune: Dict) -> str:
    """格式化每日运势"""
    
    today_gan, today_zhi = fortune["today_ganzhi"]
    today_gan_wx, today_zhi_wx = fortune["today_wuxing"]
    
    output = []
    output.append("🌟 今日五行运势 🌟")
    output.append("")
    output.append(f"📅 今日干支：{today_gan}{today_zhi}")
    output.append(f"   五行属性：{today_gan_wx} {today_zhi_wx}")
    output.append("")
    
    # 运势评级
    stars = "★" * fortune["score"] + "☆" * (5 - fortune["score"])
    output.append(f"【今日运势】{stars} {fortune['rating']}")
    output.append("")
    
    # 关系说明
    relation_desc = {
        "被生": "今日五行生助日主，得天时之利",
        "同": "今日五行与日主同气，顺势而为",
        "生": "今日需要付出努力，但会有回报",
        "克": "今日五行克制日主，需谨慎行事",
        "被克": "今日日主受制，宜守不宜攻",
        "无关": "今日五行与日主关系不大，按常进行"
    }
    output.append(f"💡 {relation_desc.get(fortune['relation'], '')}")
    output.append("")
    
    # 宜
    output.append("【宜】")
    for item in fortune["yi"]:
        output.append(f"  ✅ {item}")
    output.append("")
    
    # 忌
    output.append("【忌】")
    for item in fortune["ji"]:
        output.append(f"  ❌ {item}")
    output.append("")
    
    # 幸运元素
    output.append("【幸运元素】")
    output.append(f"  🎨 幸运色：{fortune['lucky']['color']}")
    output.append(f"  🧭 幸运方位：{fortune['lucky']['direction']}")
    output.append(f"  🔢 幸运数字：{fortune['lucky']['number']}")
    output.append("")
    
    output.append("=" * 30)
    output.append("💫 愿您今日顺遂，万事如意！")
    
    return "\n".join(output)


def generate_daily_report(day_master: str, personal_wuxing: Dict[str, int]) -> str:
    """生成完整的每日运势报告"""
    today_gan, today_zhi = get_today_ganzhi()
    fortune = analyze_daily_fortune(day_master, today_gan, today_zhi, personal_wuxing)
    return format_daily_fortune(fortune)


if __name__ == "__main__":
    # 测试用例
    if len(sys.argv) >= 2:
        day_master = sys.argv[1]
    else:
        day_master = "乙"  # 默认测试
    
    # 模拟个人五行分布
    test_wuxing = {"金": 2, "木": 3, "水": 1, "火": 1, "土": 1}
    
    report = generate_daily_report(day_master, test_wuxing)
    print(report)
