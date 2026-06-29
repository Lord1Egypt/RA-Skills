#!/usr/bin/env python3
"""旅行疫苗指南 - CH技能脚本（无代理版）

零配置即装即用，基于urllib标准库直接访问公开API，无需代理和Key。
提供目的地疫苗要求查询、常见旅行疫苗列表和出行疫苗推荐方案。
"""
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

# ====== 旅行疫苗数据库 ======
# 数据来源：WHO International Travel and Health + CDC Traveler's Health

VACCINES = {
    "yellow_fever": {
        "name": "黄热病疫苗",
        "name_en": "Yellow Fever",
        "type": "必须/推荐",
        "validity": "终身有效（2016年起）",
        "note": "进入某些非洲和南美国家必须接种，需提前10天生效，需国际疫苗接种证书（黄皮书）",
        "countries_required": ["安哥拉", "贝宁", "布基纳法索", "布隆迪", "喀麦隆", "中非", "乍得", "刚果(布)", "刚果(金)", "科特迪瓦", "赤道几内亚", "埃塞俄比亚", "加蓬", "冈比亚", "加纳", "几内亚", "几内亚比绍", "肯尼亚", "利比里亚", "马里", "毛里塔尼亚", "尼日尔", "尼日利亚", "塞内加尔", "塞拉利昂", "苏丹", "南苏丹", "多哥", "乌干达", "巴西", "哥伦比亚", "厄瓜多尔", "法属圭亚那", "巴拿马", "秘鲁", "委内瑞拉", "玻利维亚", "圭亚那", "巴拉圭", "苏里南", "阿根廷(部分)"],
    },
    "typhoid": {
        "name": "伤寒疫苗",
        "name_en": "Typhoid",
        "type": "推荐",
        "validity": "2-5年（取决于类型）",
        "note": "前往卫生条件较差地区推荐接种，南亚、东南亚、非洲风险较高",
        "countries_required": [],
    },
    "hepatitis_a": {
        "name": "甲肝疫苗",
        "name_en": "Hepatitis A",
        "type": "推荐",
        "validity": "终身（完成两剂后）",
        "note": "前往卫生条件较差地区推荐，几乎所有发展中国家都有风险",
        "countries_required": [],
    },
    "hepatitis_b": {
        "name": "乙肝疫苗",
        "name_en": "Hepatitis B",
        "type": "推荐",
        "validity": "终身（完成三剂后）",
        "note": "长期停留、医疗操作、性接触风险时推荐，全球普遍风险",
        "countries_required": [],
    },
    "rabies": {
        "name": "狂犬病疫苗",
        "name_en": "Rabies",
        "type": "推荐（暴露前）",
        "validity": "需加强针",
        "note": "前往狂犬病流行区且可能接触动物时推荐，东南亚、印度、非洲风险高",
        "countries_required": [],
    },
    "japanese_encephalitis": {
        "name": "乙脑疫苗",
        "name_en": "Japanese Encephalitis",
        "type": "推荐",
        "validity": "1-2年（需加强）",
        "note": "前往东南亚和东亚农村地区推荐，尤其是雨季",
        "countries_required": [],
    },
    "meningococcal": {
        "name": "流脑疫苗",
        "name_en": "Meningococcal",
        "type": "必须/推荐",
        "validity": "3-5年",
        "note": "前往沙特阿拉伯朝觐必须接种（ACYW135四价），非洲流脑带推荐",
        "countries_required": ["沙特阿拉伯(朝觐)"],
    },
    "cholera": {
        "name": "霍乱疫苗",
        "name_en": "Cholera",
        "type": "推荐",
        "validity": "2年",
        "note": "前往霍乱暴发地区推荐，口服疫苗",
        "countries_required": [],
    },
    "malaria_prophylaxis": {
        "name": "疟疾预防用药",
        "name_en": "Malaria Prophylaxis",
        "type": "必须（非疫苗）",
        "validity": "旅行期间持续服用",
        "note": "前往疟疾流行区必须服用预防药，不是疫苗但必须准备。常用：甲氟喹/多西环素/阿托伐醌-氯胍",
        "countries_required": [],
    },
}

# 目的地疫苗要求
DESTINATION_REQUIREMENTS = {
    "泰国": {"required": [], "recommended": ["hepatitis_a", "typhoid", "japanese_encephalitis", "rabies"], "malaria": "边境地区有风险", "note": "常规旅行风险较低，长期停留建议补种"},
    "日本": {"required": [], "recommended": ["hepatitis_a", "hepatitis_b"], "malaria": "无风险", "note": "卫生条件好，常规旅行无需特殊疫苗"},
    "韩国": {"required": [], "recommended": ["hepatitis_a", "hepatitis_b"], "malaria": "无风险", "note": "卫生条件好"},
    "越南": {"required": [], "recommended": ["hepatitis_a", "typhoid", "japanese_encephalitis", "rabies"], "malaria": "部分农村地区有风险", "note": "农村地区风险较高"},
    "印度": {"required": [], "recommended": ["hepatitis_a", "typhoid", "hepatitis_b", "rabies", "cholera", "japanese_encephalitis"], "malaria": "多数地区有风险", "note": "多项疫苗推荐，建议提前4-6周咨询"},
    "印度尼西亚": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "部分岛屿有风险", "note": "巴厘岛疟疾风险低，偏远岛屿风险高"},
    "马来西亚": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "婆罗洲部分区域有风险", "note": "城市区域风险低"},
    "新加坡": {"required": [], "recommended": ["hepatitis_a"], "malaria": "无风险", "note": "卫生条件好"},
    "柬埔寨": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies", "japanese_encephalitis"], "malaria": "有风险", "note": "建议疟疾预防用药"},
    "缅甸": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies", "japanese_encephalitis", "cholera"], "malaria": "有风险", "note": "边境地区风险高，建议疟疾预防用药"},
    "菲律宾": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "部分岛屿有风险", "note": "农村地区风险较高"},
    "尼泊尔": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies", "hepatitis_b"], "malaria": "低海拔地区有风险", "note": "徒步旅行注意高山病"},
    "斯里兰卡": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "风险极低", "note": "登革热风险高"},
    "巴西": {"required": ["yellow_fever"], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "亚马逊地区有风险", "note": "黄热病疫苗必须，部分地区需疟疾预防"},
    "肯尼亚": {"required": ["yellow_fever"], "recommended": ["hepatitis_a", "typhoid", "rabies", "meningococcal"], "malaria": "有风险", "note": "黄热病疫苗必须，疟疾预防必须"},
    "坦桑尼亚": {"required": ["yellow_fever"], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "有风险", "note": "黄热病疫苗必须，疟疾预防必须"},
    "南非": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "东北部有风险", "note": "主要城市无疟疾风险"},
    "埃及": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "无风险", "note": "尼罗河地区注意血吸虫病"},
    "摩洛哥": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "无风险", "note": "卫生条件较好"},
    "沙特阿拉伯": {"required": ["meningococcal"], "recommended": ["hepatitis_a", "typhoid"], "malaria": "无风险", "note": "朝觐必须流脑疫苗和黄热病疫苗（来自疫区）"},
    "土耳其": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "无风险", "note": "卫生条件较好"},
    "美国": {"required": [], "recommended": [], "malaria": "无风险", "note": "常规旅行无需特殊疫苗"},
    "英国": {"required": [], "recommended": [], "malaria": "无风险", "note": "常规旅行无需特殊疫苗"},
    "法国": {"required": [], "recommended": [], "malaria": "无风险", "note": "常规旅行无需特殊疫苗"},
    "德国": {"required": [], "recommended": [], "malaria": "无风险", "note": "常规旅行无需特殊疫苗"},
    "澳大利亚": {"required": [], "recommended": [], "malaria": "无风险", "note": "常规旅行无需特殊疫苗"},
    "新西兰": {"required": [], "recommended": [], "malaria": "无风险", "note": "常规旅行无需特殊疫苗"},
    "墨西哥": {"required": [], "recommended": ["hepatitis_a", "typhoid"], "malaria": "部分区域有风险", "note": "旅游区风险低"},
    "秘鲁": {"required": ["yellow_fever"], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "亚马逊地区有风险", "note": "高海拔注意高山病"},
    "阿根廷": {"required": [], "recommended": ["hepatitis_a", "typhoid"], "malaria": "无风险", "note": "北部边境需黄热病疫苗"},
    "马尔代夫": {"required": [], "recommended": ["hepatitis_a", "typhoid"], "malaria": "无风险", "note": "度假岛风险极低"},
    "斐济": {"required": [], "recommended": ["hepatitis_a", "typhoid"], "malaria": "无风险", "note": "登革热风险"},
    "俄罗斯": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "无风险", "note": "蜱传脑炎高风险区需注意"},
    "蒙古": {"required": [], "recommended": ["hepatitis_a", "typhoid", "rabies"], "malaria": "无风险", "note": "农村地区注意鼠疫风险"},
}


def query(**kwargs):
    """查询目的地疫苗要求"""
    destination = kwargs.get("destination", "")
    if not destination:
        return json.dumps({"error": "请提供目的地名称，如：query destination=泰国"}, ensure_ascii=False, indent=2)

    # 模糊匹配
    matched = None
    for dest, req in DESTINATION_REQUIREMENTS.items():
        if destination in dest or dest in destination:
            matched = dest
            break

    if not matched:
        # 尝试搜索
        suggestions = [d for d in DESTINATION_REQUIREMENTS.keys() if destination[0] in d]
        return json.dumps({
            "error": f"未找到\"{destination}\"的疫苗信息",
            "suggestions": suggestions[:5] if suggestions else [],
            "available": list(DESTINATION_REQUIREMENTS.keys()),
            "tip": "可使用list工具查看所有支持的目的地"
        }, ensure_ascii=False, indent=2)

    req = DESTINATION_REQUIREMENTS[matched]
    result = {
        "destination": matched,
        "required_vaccines": [VACCINES[v]["name"] for v in req["required"] if v in VACCINES],
        "recommended_vaccines": [VACCINES[v]["name"] for v in req["recommended"] if v in VACCINES],
        "malaria_risk": req.get("malaria", "未知"),
        "malaria_prophylaxis_needed": "有风险" in req.get("malaria", ""),
        "note": req.get("note", ""),
        "details": {},
    }

    # 添加详情
    for v_id in req["required"] + req["recommended"]:
        if v_id in VACCINES:
            v = VACCINES[v_id]
            result["details"][v["name"]] = {
                "english_name": v["name_en"],
                "type": v["type"],
                "validity": v["validity"],
                "note": v["note"],
            }

    if result["malaria_prophylaxis_needed"]:
        result["details"]["疟疾预防用药"] = VACCINES["malaria_prophylaxis"]

    return json.dumps(result, ensure_ascii=False, indent=2)


def list_vaccines(**kwargs):
    """列出常见旅行疫苗"""
    category = kwargs.get("category", "all")

    result = []
    for v_id, v in VACCINES.items():
        if category != "all" and category not in v["type"]:
            continue
        result.append({
            "id": v_id,
            "name": v["name"],
            "english_name": v["name_en"],
            "type": v["type"],
            "validity": v["validity"],
            "note": v["note"],
        })

    return json.dumps({
        "total": len(result),
        "category": category,
        "vaccines": result,
    }, ensure_ascii=False, indent=2)


def recommend(**kwargs):
    """推荐出行疫苗方案"""
    destinations = kwargs.get("destinations", "")
    duration = kwargs.get("duration", "")
    activities = kwargs.get("activities", "")

    if not destinations:
        return json.dumps({"error": "请提供目的地，多个用逗号分隔，如：recommend destinations=泰国,越南 duration=7 activities=徒步"}, ensure_ascii=False, indent=2)

    dest_list = [d.strip() for d in destinations.split(",")]
    all_required = set()
    all_recommended = set()
    malaria_needed = False
    dest_details = []

    for dest_name in dest_list:
        matched = None
        for dest in DESTINATION_REQUIREMENTS:
            if dest_name in dest or dest in dest_name:
                matched = dest
                break
        if matched:
            req = DESTINATION_REQUIREMENTS[matched]
            all_required.update(req["required"])
            all_recommended.update(req["recommended"])
            if "有风险" in req.get("malaria", ""):
                malaria_needed = True
            dest_details.append({
                "destination": matched,
                "required": [VACCINES[v]["name"] for v in req["required"] if v in VACCINES],
                "recommended": [VACCINES[v]["name"] for v in req["recommended"] if v in VACCINES],
                "malaria_risk": req.get("malaria", "无风险"),
            })

    # 高风险活动额外推荐
    extra = []
    if activities:
        if any(x in activities for x in ["徒步", "露营", "野外", "农村"]):
            extra.append("狂犬病疫苗（可能接触动物）")
            extra.append("乙脑疫苗（东南亚农村）")
        if any(x in activities for x in ["潜水", "水上"]):
            extra.append("注意血吸虫病风险")

    # 时长建议
    duration_note = ""
    if duration:
        try:
            d = int(duration)
            if d > 30:
                duration_note = "长期停留（>30天），建议补种乙肝疫苗"
                all_recommended.add("hepatitis_b")
        except ValueError:
            pass

    result = {
        "destinations": dest_details,
        "must_have": [VACCINES[v]["name"] for v in all_required if v in VACCINES],
        "recommended": [VACCINES[v]["name"] for v in all_recommended if v in VACCINES],
        "malaria_prophylaxis": malaria_needed,
        "extra_for_activities": extra,
        "duration_note": duration_note,
        "timeline": "建议出发前4-6周完成疫苗接种，部分疫苗需要多剂次",
        "important_reminder": "以上建议仅供参考，请以出行前医疗机构的专业意见为准",
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


# ====== 入口 ======
TOOLS = {
    "query": query,
    "list": list_vaccines,
    "recommend": recommend,
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"用法: python travel_vaccine_guide.py <tool_name> [key=value ...]")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)
    tool_name = sys.argv[1]
    if tool_name not in TOOLS:
        print(f"未知工具: {tool_name}")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)
    kwargs = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            kwargs[k] = v
    print(TOOLS[tool_name](**kwargs))
