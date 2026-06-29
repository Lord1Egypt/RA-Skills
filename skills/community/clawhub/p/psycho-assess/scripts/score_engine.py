#!/usr/bin/env python3
"""
心理测评评分计算引擎
支持 PHQ-9, GAD-7, PSS-10, RSES, BFI-10 五个量表的评分计算
输出 JSON 格式的评分结果，供HTML报告模板使用

用法: python score_engine.py --scale <scale_name> --answers "<json_array>"
       python score_engine.py --all --answers "<json_object>"  # 全套测评
"""

import json
import sys


# ============================================================
# 量表配置
# ============================================================

SCALES = {
    "PHQ-9": {
        "name": "抑郁症筛查量表",
        "full_name": "PHQ-9",
        "items": 9,
        "max_score": 27,
        "options": ["完全不会", "好几天", "一半以上的天数", "几乎每天"],
        "reverse_items": [],
        "thresholds": [
            {"min": 0, "max": 4, "level": "正常范围", "severity": "无抑郁症状", "color": "#22C55E", "label": "正常范围"},
            {"min": 5, "max": 9, "level": "轻度", "severity": "轻度抑郁", "color": "#EAB308", "label": "轻度抑郁"},
            {"min": 10, "max": 14, "level": "中度", "severity": "中度抑郁", "color": "#F97316", "label": "中度抑郁"},
            {"min": 15, "max": 19, "level": "中重度", "severity": "中重度抑郁", "color": "#EF4444", "label": "中重度抑郁"},
            {"min": 20, "max": 27, "level": "重度", "severity": "重度抑郁", "color": "#DC2626", "label": "重度抑郁"},
        ],
        "interpretations": {
            "0-4": "您的PHQ-9得分为{score}分，处于正常范围。这表明您在过去两周内没有明显的抑郁症状。请继续保持健康的生活方式，包括规律作息、适度运动和良好的社交互动。",
            "5-9": "您的PHQ-9得分为{score}分，提示存在轻度抑郁症状。您可能在情绪、精力或兴趣方面有些困扰，但尚未严重影响日常生活。建议：增加户外活动、保证充足睡眠、与亲友交流感受。如症状持续两周以上，建议寻求专业心理咨询。",
            "10-14": "您的PHQ-9得分为{score}分，提示存在中度抑郁症状。这可能已经对您的日常生活、工作或人际关系产生了一定影响。强烈建议您预约心理咨询师或精神科医生进行专业评估。同时，请尝试保持规律生活，不要独自承受。",
            "15-19": "您的PHQ-9得分为{score}分，显示存在中重度抑郁症状。抑郁症状正在显著影响您的正常生活功能。请尽快寻求专业帮助——预约精神科医生或心理治疗师。如果您有自伤念头，请立即拨打心理援助热线。",
            "20-27": "您的PHQ-9得分为{score}分，显示存在重度抑郁症状。这是需要立即关注的严重情况。请立即联系精神科医生或前往医院。如果您正在经历自伤或自杀念头，请马上拨打心理援助热线：希望24热线 400-161-9995，或拨打110/120。",
        },
        "note": "PHQ-9是筛查工具，不是诊断工具。第9题（自伤念头）任何非0回答都需特别关注。",
    },
    "GAD-7": {
        "name": "广泛性焦虑障碍量表",
        "full_name": "GAD-7",
        "items": 7,
        "max_score": 21,
        "options": ["完全不会", "好几天", "一半以上的天数", "几乎每天"],
        "reverse_items": [],
        "thresholds": [
            {"min": 0, "max": 4, "level": "正常范围", "severity": "无焦虑症状", "color": "#22C55E", "label": "正常范围"},
            {"min": 5, "max": 9, "level": "轻度", "severity": "轻度焦虑", "color": "#EAB308", "label": "轻度焦虑"},
            {"min": 10, "max": 14, "level": "中度", "severity": "中度焦虑", "color": "#F97316", "label": "中度焦虑"},
            {"min": 15, "max": 21, "level": "重度", "severity": "重度焦虑", "color": "#EF4444", "label": "重度焦虑"},
        ],
        "interpretations": {
            "0-4": "您的GAD-7得分为{score}分，焦虑水平在正常范围内。这表明您在过去两周内没有明显的焦虑困扰。适度的焦虑是人体的正常应激反应，关键是与它和平共处。",
            "5-9": "您的GAD-7得分为{score}分，提示存在轻度焦虑症状。您可能经常感到紧张或担忧，但总体上还能应对。建议练习正念冥想、深呼吸放松技巧，减少咖啡因摄入。如症状持续，可寻求心理咨询。",
            "10-14": "您的GAD-7得分为{score}分，提示存在中度焦虑症状。焦虑可能已经干扰到您的睡眠、工作或人际关系。强烈建议寻求专业帮助——认知行为疗法（CBT）对焦虑症状效果显著。",
            "15-21": "您的GAD-7得分为{score}分，显示存在重度焦虑症状。焦虑正在严重影响您的生活质量。请尽快预约精神科医生进行专业评估和治疗。在等待就医期间，请尽量避免独自承受，与信任的人谈谈您的感受。",
        },
    },
    "PSS-10": {
        "name": "压力感知量表",
        "full_name": "PSS-10",
        "items": 10,
        "max_score": 40,
        "options": ["从不", "偶尔", "有时", "时常", "总是"],
        "reverse_items": [3, 4, 5, 6, 8, 9],  # 0-indexed items to reverse
        "reverse_map": {0: 4, 1: 3, 2: 2, 3: 1, 4: 0},
        "thresholds": [
            {"min": 0, "max": 13, "level": "低压力", "severity": "低压力感知", "color": "#22C55E", "label": "低压力"},
            {"min": 14, "max": 26, "level": "中等", "severity": "中等压力感知", "color": "#EAB308", "label": "中等压力"},
            {"min": 27, "max": 40, "level": "高压力", "severity": "高压力感知", "color": "#EF4444", "label": "高压力"},
        ],
        "interpretations": {
            "0-13": "您的PSS-10得分为{score}分，压力感知处于较低水平。这说明您目前能够较好地应对生活中的各种挑战，拥有良好的压力管理能力和心理弹性。",
            "14-26": "您的PSS-10得分为{score}分，压力感知处于中等水平。您正在经历一定程度的压力，这可能影响到您的情绪和精力。建议：定期运动、保证睡眠、学习时间管理技巧、建立健康的边界。",
            "27-40": "您的PSS-10得分为{score}分，压力感知处于较高水平。您正承受着较重的压力负担，这可能对身心健康产生不利影响。强烈建议：识别压力源并尝试减少不必要的压力因素，学习放松技巧，必要时寻求心理咨询帮助。",
        },
    },
    "RSES": {
        "name": "Rosenberg自尊量表",
        "full_name": "RSES",
        "items": 10,
        "max_score": 40,
        "options": ["完全不同意", "不同意", "同意", "完全同意"],
        "reverse_items": [1, 4, 5, 7, 8],  # 0-indexed
        "reverse_map": {1: 4, 2: 3, 3: 2, 4: 1},
        "thresholds": [
            {"min": 10, "max": 17, "level": "低自尊", "severity": "低自尊", "color": "#EF4444", "label": "低自尊"},
            {"min": 18, "max": 24, "level": "中等偏低", "severity": "中等偏低自尊", "color": "#F97316", "label": "中等偏低"},
            {"min": 25, "max": 31, "level": "中等", "severity": "中等自尊", "color": "#EAB308", "label": "中等自尊"},
            {"min": 32, "max": 40, "level": "高自尊", "severity": "高自尊", "color": "#22C55E", "label": "高自尊"},
        ],
        "interpretations": {
            "10-17": "您的RSES得分为{score}分，处于低自尊水平。您可能经常自我怀疑，难以认可自己的价值。低自尊往往与抑郁和焦虑相关。建议通过认知行为疗法（CBT）改善自我评价，学会挑战负面的自我认知。寻求专业心理咨询会有很大帮助。",
            "18-24": "您的RSES得分为{score}分，处于中等偏低水平。您有时会对自己不太满意，但并非全盘否定。建议练习自我肯定、记录每日成就、设定可实现的小目标来逐步建立自信。",
            "25-31": "您的RSES得分为{score}分，处于中等自尊水平。您对自己有基本的认可，但在某些方面可能仍有疑虑。这是大多数人的正常范围，建议继续保持积极的自我对话。",
            "32-40": "您的RSES得分为{score}分，处于高自尊水平。您对自己持有积极的评价，拥有健康的自我价值感。高自尊与更好的心理健康和人际关系相关。请继续保持！",
        },
    },
    "BFI-10": {
        "name": "大五人格量表（简版）",
        "full_name": "BFI-10",
        "items": 10,
        "dimensions": {
            "外向性(E)": {"items": [0, 5], "reverse": [5], "label": "Extraversion", "high": "善于社交、精力充沛、热情", "low": "内敛、安静、独处偏好"},
            "宜人性(A)": {"items": [1, 6], "reverse": [1], "label": "Agreeableness", "high": "信任他人、合作、有同情心", "low": "竞争性、怀疑、自我中心"},
            "尽责性(C)": {"items": [2, 7], "reverse": [7], "label": "Conscientiousness", "high": "自律、有条理、可靠", "low": "随性、杂乱、拖延"},
            "神经质(N)": {"items": [3, 8], "reverse": [8], "label": "Neuroticism", "high": "焦虑、情绪波动、易紧张", "low": "情绪稳定、从容、抗压力强"},
            "开放性(O)": {"items": [4, 9], "reverse": [9], "label": "Openness", "high": "好奇、创造性、喜欢新体验", "low": "务实、传统、习惯熟悉的"},
        },
        "options": ["完全不同意", "有点不同意", "中立", "有点同意", "完全同意"],
        "reverse_items": [1, 5, 7, 8, 9],  # 0-indexed items to reverse (item 1,2,8,9,10 → index 0,1,7,8,9)
        "reverse_map": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1},
    },
}


def score_scale(scale_key, answers):
    """Calculate score for a single scale"""
    if scale_key not in SCALES:
        return {"error": f"未知量表: {scale_key}"}

    config = SCALES[scale_key]
    raw_answers = list(answers)  # copy

    if len(raw_answers) != config["items"]:
        return {"error": f"{scale_key}需要{config['items']}个回答，收到了{len(raw_answers)}个"}

    # Apply reverse scoring
    reverse_items = set(config.get("reverse_items", []))
    reverse_map = config.get("reverse_map", {})
    scored_items = []
    for i, val in enumerate(raw_answers):
        if i in reverse_items and reverse_map:
            scored_items.append(reverse_map.get(val, val))
        else:
            scored_items.append(val)

    # Special handling for BFI-10: per-dimension scoring
    if scale_key == "BFI-10":
        dimensions = {}
        for dim_name, dim_config in config["dimensions"].items():
            dim_items = dim_config["items"]
            dim_reverse = set(dim_config["reverse"])
            dim_scores = []
            for idx in dim_items:
                val = raw_answers[idx]
                if idx in dim_reverse:
                    val = reverse_map.get(val, val)
                dim_scores.append(val)
            dim_avg = round(sum(dim_scores) / len(dim_scores), 2)  # avg 1-5
            dimensions[dim_name] = {
                "score": dim_avg,
                "high_desc": dim_config["high"],
                "low_desc": dim_config["low"],
                "label": dim_config["label"],
            }
        return {
            "scale": scale_key,
            "name": config["name"],
            "dimensions": dimensions,
            "raw_answers": raw_answers,
            "scored_items": scored_items,
        }

    total_score = sum(scored_items)

    # Find matching threshold
    threshold = None
    for t in config["thresholds"]:
        if t["min"] <= total_score <= t["max"]:
            threshold = t
            break

    # Find matching interpretation
    interpretation = ""
    for key, text in config.get("interpretations", {}).items():
        parts = key.split("-")
        if len(parts) == 2:
            lo, hi = int(parts[0]), int(parts[1])
            if lo <= total_score <= hi:
                interpretation = text.format(score=total_score)
                break

    result = {
        "scale": scale_key,
        "name": config["name"],
        "total_score": total_score,
        "max_score": config["max_score"],
        "percentage": round(total_score / config["max_score"] * 100, 1),
        "threshold": threshold,
        "interpretation": interpretation,
        "raw_answers": raw_answers,
        "scored_items": scored_items,
        "options": config["options"],
    }

    # Special notes
    if "note" in config:
        result["note"] = config["note"]

    # PHQ-9 Q9 check
    if scale_key == "PHQ-9" and raw_answers[8] > 0:
        result["q9_warning"] = True

    return result


def score_all(answers_dict):
    """Score all scales at once"""
    results = {}
    for scale_key in ["PHQ-9", "GAD-7", "PSS-10", "RSES", "BFI-10"]:
        if scale_key in answers_dict:
            results[scale_key] = score_scale(scale_key, answers_dict[scale_key])
        else:
            results[scale_key] = {"error": f"缺少{scale_key}的回答数据"}

    # Overall summary
    summary = generate_summary(results)
    results["_summary"] = summary

    return results


def generate_summary(results):
    """Generate cross-scale summary and integrated analysis"""
    warnings = []
    strengths = []
    recommendations = []

    # PHQ-9
    phq = results.get("PHQ-9", {})
    if "total_score" in phq:
        ts = phq["total_score"]
        if ts >= 15:
            warnings.append({"level": "high", "text": f"PHQ-9得分{ts}分，存在中重度以上抑郁症状，强烈建议寻求专业帮助。"})
            recommendations.append("预约精神科医生或心理咨询师进行专业评估")
        elif ts >= 10:
            warnings.append({"level": "medium", "text": f"PHQ-9得分{ts}分，存在中度抑郁症状，建议关注并考虑专业咨询。"})
            recommendations.append("考虑进行心理咨询，学习CBT情绪管理技巧")
        elif ts >= 5:
            warnings.append({"level": "low", "text": f"PHQ-9得分{ts}分，轻度抑郁症状，注意自我照顾。"})
        if phq.get("q9_warning"):
            warnings.append({"level": "high", "text": "PHQ-9第9题（自伤念头）非0回答，需要特别关注！"})

    # GAD-7
    gad = results.get("GAD-7", {})
    if "total_score" in gad:
        ts = gad["total_score"]
        if ts >= 15:
            warnings.append({"level": "high", "text": f"GAD-7得分{ts}分，存在重度焦虑症状，强烈建议寻求专业帮助。"})
            recommendations.append("学习正念冥想和深呼吸放松技巧")
        elif ts >= 10:
            warnings.append({"level": "medium", "text": f"GAD-7得分{ts}分，存在中度焦虑症状，建议关注情绪管理。"})
            recommendations.append("每天10分钟正念练习，减少咖啡因摄入")
        elif ts >= 5:
            warnings.append({"level": "low", "text": f"GAD-7得分{ts}分，轻度焦虑症状，注意压力调节。"})

    # PSS-10
    pss = results.get("PSS-10", {})
    if "total_score" in pss:
        ts = pss["total_score"]
        if ts >= 27:
            warnings.append({"level": "high", "text": f"PSS-10得分{ts}分，高压力感知水平，需要积极的压力管理。"})
            recommendations.append("识别并减少不必要的压力源，建立健康的边界")
        elif ts >= 14:
            warnings.append({"level": "medium", "text": f"PSS-10得分{ts}分，中等压力感知水平，建议学习压力管理技巧。"})

    # RSES
    rses = results.get("RSES", {})
    if "total_score" in rses:
        ts = rses["total_score"]
        if ts <= 17:
            warnings.append({"level": "high", "text": f"RSES得分{ts}分，低自尊水平，可能伴随自我否定倾向。"})
            recommendations.append("练习自我肯定，记录每日成就和积极体验")
        elif ts <= 24:
            warnings.append({"level": "medium", "text": f"RSES得分{ts}分，中等偏低自尊水平，建议增强自我接纳。"})
        elif ts >= 32:
            strengths.append("高自尊水平，拥有健康的自我价值感")

    # BFI-10
    bfi = results.get("BFI-10", {})
    if "dimensions" in bfi:
        dims = bfi["dimensions"]
        for dim_name, dim_data in dims.items():
            if dim_data["score"] >= 4:
                strengths.append(f"{dim_name}得分较高：{dim_data['high_desc']}")
            elif dim_data["score"] <= 2:
                if dim_name == "神经质(N)":
                    strengths.append(f"{dim_name}得分较低（情绪稳定）：{dim_data['low_desc']}")
                else:
                    score_val = dim_data["score"]
                    warnings.append({"level": "low", "text": f"{dim_name}得分仅{score_val}，{dim_data['low_desc']}"})

    # General recommendations
    if not recommendations:
        recommendations.append("保持当前的健康生活方式")
        recommendations.append("定期进行自我心理状态检查")

    recommendations.append("如症状持续两周以上或影响日常生活，请寻求专业帮助")

    return {
        "total_scales": 5,
        "warnings": warnings,
        "strengths": strengths,
        "recommendations": list(set(recommendations)),  # deduplicate
        "disclaimer": "本测评仅为自我了解工具，不构成医学诊断。如有严重情绪困扰，请及时寻求专业医疗帮助。",
        "hotlines": [
            {"name": "全国心理援助热线", "number": "400-161-9995"},
            {"name": "北京心理危机干预中心", "number": "010-82951332"},
            {"name": "希望24热线", "number": "400-161-9995"},
            {"name": "生命热线", "number": "400-821-1215"},
        ],
    }


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("心理测评评分引擎")
        print("用法:")
        print("  单个量表: python score_engine.py --scale PHQ-9 --answers '[0,1,2,1,0,1,2,1,0]'")
        print("  全套测评: python score_engine.py --all --answers '{\"PHQ-9\":[...],\"GAD-7\":[...],...}'")
        return

    try:
        if "--all" in args:
            idx = args.index("--answers")
            answers_dict = json.loads(args[idx + 1])
            result = score_all(answers_dict)
        elif "--scale" in args:
            idx = args.index("--scale")
            scale_key = args[idx + 1]
            idx2 = args.index("--answers")
            answers = json.loads(args[idx2 + 1])
            result = score_scale(scale_key, answers)
        else:
            print(json.dumps({"error": "请指定 --scale 或 --all"}, ensure_ascii=False))
            return

        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
