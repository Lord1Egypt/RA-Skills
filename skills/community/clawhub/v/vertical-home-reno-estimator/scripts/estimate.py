#!/usr/bin/env python3
"""
住宅装修造价估算脚本 v2.0
输入：面积、档次、城市
输出：JSON格式估算结果
"""

import json
import sys
from datetime import datetime

# 单位面积造价参考（元/㎡）
# 更新至2025-2026年数据
COST_PER_SQM = {
    "简装": {"硬装": 800, "软装": 350, "电器": 250, "合计": 1400},
    "精装": {"硬装": 1600, "软装": 900, "电器": 700, "合计": 3200},
    "豪装": {"硬装": 3500, "软装": 2500, "电器": 1800, "合计": 7800},
}

# 价格波动范围
PRICE_RANGE = {
    "简装": {"low": 0.80, "high": 1.20},
    "精装": {"low": 0.78, "high": 1.22},
    "豪装": {"low": 0.72, "high": 1.28},
}

# 硬装分项占比
HARD_DECOR_RATIO = {
    "水电改造": 0.18,
    "泥瓦工程": 0.22,
    "木工工程": 0.18,
    "油漆工程": 0.12,
    "主材": 0.30,
}

# 软装分项占比
SOFT_DECOR_RATIO = {
    "家具": 0.55,
    "窗帘布艺": 0.15,
    "灯具": 0.15,
    "装饰品": 0.15,
}

# 电器分项占比
APPLIANCE_RATIO = {
    "空调": 0.35,
    "冰洗": 0.20,
    "厨电": 0.25,
    "其他": 0.20,
}

# 城市等级调整系数
CITY_TIERS = {
    "一线": {
        "城市": ["北京", "上海", "广州", "深圳"],
        "系数": 1.45,
        "人工费": 520,
    },
    "新一线": {
        "城市": ["杭州", "成都", "武汉", "南京", "苏州", "天津", "重庆", "西安", "郑州", "东莞", "青岛", "沈阳", "长沙", "昆明", "大连", "宁波", "无锡"],
        "系数": 1.20,
        "人工费": 380,
    },
    "二线": {
        "城市": ["合肥", "福州", "济南", "温州", "常州", "南通", "徐州", "佛山", "珠海", "中山", "惠州", "泉州", "无锡", "烟台", "兰州", "太原", "吉林", "贵阳", "南阳", "齐齐哈尔", "厦门", "哈尔滨", "长春", "石家庄", "南宁", "乌鲁木齐"],
        "系数": 1.05,
        "人工费": 300,
    },
    "三四线": {
        "城市": [],
        "系数": 0.88,
        "人工费": 240,
    },
}

# 档次说明
GRADE_DESC = {
    "简装": "基础功能性装修，满足基本居住需求，适合出租或过渡性居住",
    "精装": "自住标准，中档品牌材料，性价比高，适合大多数家庭",
    "豪装": "高端品牌，定制化需求多，个性化突出，适合改善型住房",
}

def get_city_tier(city_name):
    """判断城市等级"""
    for tier, data in CITY_TIERS.items():
        if city_name in data["城市"]:
            return tier, data["系数"], data.get("人工费", 280)
    return "二线", 1.00, 280

def format_wan(yuan):
    """元转万元，保留1位小数"""
    return round(yuan / 10000, 1)

def estimate(area, grade, city):
    """估算装修费用"""
    city_tier, city_factor, labor_fee = get_city_tier(city)
    base_cost = COST_PER_SQM.get(grade, COST_PER_SQM["精装"])
    price_range = PRICE_RANGE.get(grade, PRICE_RANGE["精装"])
    
    # 计算总价
    total_base = base_cost["合计"] * area * city_factor
    
    prices = {
        "经济型": format_wan(total_base * price_range["low"]),
        "舒适型": format_wan(total_base),
        "品质型": format_wan(total_base * price_range["high"]),
    }
    
    # 硬装计算
    hard_decor = base_cost["硬装"] * area * city_factor
    hard_details = {}
    for item, ratio in HARD_DECOR_RATIO.items():
        hard_details[item] = {
            "费用": format_wan(hard_decor * ratio),
            "占比": f"{int(ratio*100)}%",
        }
    
    # 软装计算
    soft_decor = base_cost["软装"] * area
    soft_details = {}
    for item, ratio in SOFT_DECOR_RATIO.items():
        soft_details[item] = {
            "费用": format_wan(soft_decor * ratio),
            "占比": f"{int(ratio*100)}%",
        }
    
    # 电器计算
    appliances = base_cost["电器"] * area
    appliance_details = {}
    for item, ratio in APPLIANCE_RATIO.items():
        appliance_details[item] = {
            "费用": format_wan(appliances * ratio),
            "占比": f"{int(ratio*100)}%",
        }
    
    # 占比说明
    decor_ratio = {
        "简装": {"硬装": "60%", "软装": "24%", "电器": "16%"},
        "精装": {"硬装": "52%", "软装": "27%", "电器": "21%"},
        "豪装": {"硬装": "46%", "软装": "32%", "电器": "22%"},
    }
    
    return {
        "基础信息": {
            "面积": area,
            "档次": grade,
            "档次说明": GRADE_DESC.get(grade, ""),
            "城市": city,
            "城市等级": city_tier,
            "人工费参考": f"{labor_fee}元/工日",
        },
        "总价估算": prices,
        "分项占比": decor_ratio.get(grade, decor_ratio["精装"]),
        "分项估算": {
            "硬装": {
                "小计": format_wan(hard_decor),
                "占比": decor_ratio.get(grade, decor_ratio["精装"])["硬装"],
                "明细": hard_details,
            },
            "软装": {
                "小计": format_wan(soft_decor),
                "占比": decor_ratio.get(grade, decor_ratio["精装"])["软装"],
                "明细": soft_details,
            },
            "电器": {
                "小计": format_wan(appliances),
                "占比": decor_ratio.get(grade, decor_ratio["精装"])["电器"],
                "明细": appliance_details,
            },
        },
        "数据来源": {
            "材料价格": "广材网(gldjc.com)、造价通(zjtcn.com) 2024-2025年市场价",
            "人工费": f"各省市建设工程造价信息网，{city}参考人工费{labor_fee}元/工日",
            "定额依据": "房屋建筑与装饰工程消耗量定额(TY 01-31-2015)",
        },
        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "免责声明": "本估算仅供参考，实际费用以具体方案和当地市场报价为准",
    }

def main():
    if len(sys.argv) < 4:
        print(json.dumps({
            "error": "用法: estimate.py <面积> <档次> <城市>",
            "example": "estimate.py 100 精装 杭州"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    try:
        area = float(sys.argv[1])
        grade = sys.argv[2]
        city = sys.argv[3]
        
        if grade not in COST_PER_SQM:
            print(json.dumps({
                "error": f"档次无效，支持: {', '.join(COST_PER_SQM.keys())}"
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        
        if area < 10 or area > 1000:
            print(json.dumps({
                "error": "面积应在10-1000平方米之间"
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        
        result = estimate(area, grade, city)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except ValueError:
        print(json.dumps({
            "error": "面积应为数字"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
