from __future__ import annotations

from dataclasses import dataclass


DIMENSION_LABELS = {
    "resource_state": "资源状态",
    "internal_friction": "内部摩擦",
    "external_pressure": "外部压力",
    "alliance_dependency": "联盟依赖",
    "trust_risk": "信任风险",
    "change_pressure": "变革强度",
    "control_pressure": "控制权压力",
    "personnel_pressure": "用人调整压力",
    "time_pressure": "时间压力",
    "legitimacy_pressure": "合法性压力",
    "execution_resistance": "执行阻力",
    "action_bias": "行动取向",
}

VALUE_PHRASES = {
    "resource_state": {
        "scarce": "资源偏弱",
        "balanced": "资源不占明显优势",
        "strong": "资源较强",
    },
    "internal_friction": {
        "low": "内部摩擦低",
        "medium": "内部存在掣肘",
        "high": "内部摩擦高",
    },
    "external_pressure": {
        "low": "外部压力低",
        "medium": "外部压力存在",
        "high": "外部压力高",
    },
    "alliance_dependency": {
        "low": "不依赖联盟",
        "medium": "部分依赖联盟",
        "high": "高度依赖联盟",
    },
    "trust_risk": {
        "low": "信任风险低",
        "medium": "信任风险存在",
        "high": "低信任合作",
    },
    "change_pressure": {
        "low": "变革压力低",
        "medium": "存在调整压力",
        "high": "变革压力高",
    },
    "control_pressure": {
        "low": "控制权压力低",
        "medium": "控制权存在争议",
        "high": "控制权压力高",
    },
    "personnel_pressure": {
        "low": "用人调整压力低",
        "medium": "存在人事调整压力",
        "high": "用人调整压力高",
    },
    "time_pressure": {
        "low": "时间压力低",
        "medium": "时间窗口有限",
        "high": "时间压力高",
    },
    "legitimacy_pressure": {
        "low": "合法性压力低",
        "medium": "合法性需要兼顾",
        "high": "合法性压力高",
    },
    "execution_resistance": {
        "low": "执行阻力低",
        "medium": "执行阻力存在",
        "high": "执行阻力高",
    },
    "action_bias": {
        "neutral": "行动取向未明",
        "advance": "倾向主动推进",
        "consolidate": "倾向先稳住",
        "ally": "倾向借力结盟",
        "replace": "倾向调整人或权",
        "mixed": "同时存在推进与稳局压力",
    },
}

LEVEL_DIMENSIONS = {
    "internal_friction",
    "external_pressure",
    "alliance_dependency",
    "trust_risk",
    "change_pressure",
    "control_pressure",
    "personnel_pressure",
    "time_pressure",
    "legitimacy_pressure",
    "execution_resistance",
}

DIMENSION_WEIGHTS = {
    "resource_state": 4,
    "internal_friction": 4,
    "external_pressure": 4,
    "alliance_dependency": 4,
    "trust_risk": 4,
    "change_pressure": 4,
    "control_pressure": 4,
    "personnel_pressure": 4,
    "time_pressure": 3,
    "legitimacy_pressure": 3,
    "execution_resistance": 4,
    "action_bias": 3,
}

QUESTION_CUES = {
    "resource_state": {
        "scarce": [
            "资源不多", "资源不够", "资源有限", "预算紧", "预算不多", "现金流紧",
            "人手不足", "弱势", "打不过", "对手更强", "寡不敌众", "头部竞争者", "强敌",
        ],
        "strong": ["资源充足", "优势明显", "我方更强", "兵强马壮"],
    },
    "internal_friction": {
        "high": [
            "派系", "内斗", "扯皮", "掣肘", "不服", "站队", "分裂", "反弹",
            "阳奉阴违", "表面支持", "拖延执行", "后方掣肘", "推进被叫停", "前后方失配",
        ],
        "medium": ["摩擦", "不同意见", "有人阻力", "有人拖延"],
    },
    "external_pressure": {
        "high": ["强敌", "头部", "对手更强", "外部压力", "竞争对手更强", "压着打", "共同敌人"],
        "medium": ["竞争", "外部对手", "对手", "挑战"],
    },
    "alliance_dependency": {
        "high": ["联盟", "盟友", "合作方", "联手", "合伙人", "伙伴", "渠道", "外部支持"],
        "medium": ["合作", "联合", "协同"],
    },
    "trust_risk": {
        "high": ["不信任", "不完全信任", "翻脸", "背刺", "目标不一致", "立场不一致", "担心合作方"],
        "medium": ["信任不足", "留后手", "合作但保留"],
    },
    "change_pressure": {
        "high": ["改革", "变法", "新制度", "制度上线", "流程再造", "转型", "重组", "组织变革"],
        "medium": ["调整", "改一改", "优化流程", "改制度"],
    },
    "control_pressure": {
        "high": ["控制权", "架空", "收权", "削权", "夺权", "中枢", "关键流程", "尾大不掉", "总部", "分支"],
        "medium": ["权限", "权力", "任命权", "统筹权"],
    },
    "personnel_pressure": {
        "high": ["换人", "换将", "撤换", "负责人不行", "换负责人", "空降", "保人", "代理负责人"],
        "medium": ["提拔", "任用", "接任", "带队"],
    },
    "time_pressure": {
        "high": ["立刻", "马上", "两个月", "本月", "短期", "窗口期", "现在就要", "尽快"],
        "medium": ["近期", "尽早", "不久后"],
    },
    "legitimacy_pressure": {
        "high": ["董事会", "授权", "名分", "合法性", "上级", "规则", "公开支持", "政治正确"],
        "medium": ["背书", "审批", "程序", "流程合法"],
    },
    "execution_resistance": {
        "high": ["拖延执行", "推不动", "中层拖延", "执行走样", "落实不下去", "执行链断", "推进被叫停", "被叫停"],
        "medium": ["执行难", "落地难", "推进阻力", "节奏失配", "前后方失配"],
    },
    "action_bias": {
        "advance": ["推进", "进攻", "扩张", "出击", "强推", "主动打", "往前推"],
        "consolidate": ["先稳", "防守", "守住", "收缩", "稳内部", "暂避锋芒", "稳基本盘"],
        "ally": ["结盟", "联手", "合作", "借力", "联合"],
        "replace": ["换人", "换将", "削权", "调权", "换负责人"],
    },
}

CASE_CUES = {
    **QUESTION_CUES,
    "internal_friction": {
        "high": QUESTION_CUES["internal_friction"]["high"] + ["贵族反扑", "内部意见分裂", "后方掣肘", "前后方节奏失配"],
        "medium": QUESTION_CUES["internal_friction"]["medium"],
    },
    "external_pressure": {
        "high": QUESTION_CUES["external_pressure"]["high"] + ["六国", "强秦", "曹操", "金国", "强邻"],
        "medium": QUESTION_CUES["external_pressure"]["medium"],
    },
    "legitimacy_pressure": {
        "high": QUESTION_CUES["legitimacy_pressure"]["high"] + ["民心", "正当性", "约法三章", "名义支持"],
        "medium": QUESTION_CUES["legitimacy_pressure"]["medium"],
    },
    "execution_resistance": {
        "high": QUESTION_CUES["execution_resistance"]["high"] + ["前后方节奏失配", "推进被叫停"],
        "medium": QUESTION_CUES["execution_resistance"]["medium"] + ["节奏失配"],
    },
}

CASE_TAG_HINTS = {
    "以弱对强": {"resource_state": "scarce", "external_pressure": "high"},
    "内部冲突": {"internal_friction": "high"},
    "改革推进": {"change_pressure": "high", "execution_resistance": "medium"},
    "联盟不稳": {"alliance_dependency": "high", "trust_risk": "high"},
    "守攻抉择": {"action_bias": "mixed"},
    "权力控制": {"control_pressure": "high", "legitimacy_pressure": "medium"},
    "用人换将": {"personnel_pressure": "high"},
    "合法性": {"legitimacy_pressure": "high"},
}


@dataclass
class StructuralProfile:
    dimensions: dict[str, str]
    matched_signals: dict[str, list[str]]

    def active_focus(self, limit: int = 4) -> list[str]:
        focus: list[tuple[int, str]] = []
        for dimension, value in self.dimensions.items():
            if dimension == "action_bias":
                if value != "neutral":
                    focus.append((DIMENSION_WEIGHTS[dimension], VALUE_PHRASES[dimension][value]))
                continue
            if value in {"high", "medium", "scarce", "strong"}:
                focus.append((DIMENSION_WEIGHTS[dimension], VALUE_PHRASES[dimension][value]))
        focus.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in focus[:limit]]


def infer_question_profile(question: str) -> StructuralProfile:
    return _infer_profile_from_text(question, QUESTION_CUES)


def infer_case_profile(case: dict) -> StructuralProfile:
    case_text = " ".join(
        [
            case["title"],
            case["summary"],
            case["objective"],
            case["chosen_action"],
            *case["visible_information"],
            *case["hidden_constraints"],
            *case["options_available"],
            *case["key_reasons"],
            *case["modern_analogy_keywords"],
        ]
    )
    profile = _infer_profile_from_text(case_text, CASE_CUES)
    for tag in case["situation_tags"]:
        hints = CASE_TAG_HINTS.get(tag, {})
        for dimension, hinted_value in hints.items():
            profile.dimensions[dimension] = _merge_value(dimension, profile.dimensions[dimension], hinted_value)
    return profile


def structural_similarity(question_profile: StructuralProfile, case_profile: StructuralProfile) -> tuple[int, list[str]]:
    score = 0
    reasons: list[tuple[int, str]] = []
    for dimension, question_value in question_profile.dimensions.items():
        case_value = case_profile.dimensions.get(dimension)
        if not case_value:
            continue

        if dimension == "action_bias":
            dimension_score = _score_action_bias(question_value, case_value)
        elif dimension == "resource_state":
            dimension_score = _score_resource_state(question_value, case_value)
        else:
            dimension_score = _score_level_dimension(question_value, case_value)

        if dimension_score <= 0:
            continue

        weighted = dimension_score * DIMENSION_WEIGHTS[dimension]
        score += weighted
        reasons.append((weighted, f"{DIMENSION_LABELS[dimension]}接近：{VALUE_PHRASES[dimension][case_value]}"))

    reasons.sort(key=lambda item: item[0], reverse=True)
    return score, [reason for _, reason in reasons[:3]]


def _infer_profile_from_text(text: str, cue_library: dict[str, dict[str, list[str]]]) -> StructuralProfile:
    lowered = text.lower()
    dimensions: dict[str, str] = {
        "resource_state": "balanced",
        "internal_friction": "low",
        "external_pressure": "low",
        "alliance_dependency": "low",
        "trust_risk": "low",
        "change_pressure": "low",
        "control_pressure": "low",
        "personnel_pressure": "low",
        "time_pressure": "low",
        "legitimacy_pressure": "low",
        "execution_resistance": "low",
        "action_bias": "neutral",
    }
    matched_signals: dict[str, list[str]] = {dimension: [] for dimension in dimensions}

    for dimension, value_map in cue_library.items():
        counts = {value: 0 for value in value_map}
        for value, cues in value_map.items():
            for cue in cues:
                if cue in text or cue.lower() in lowered:
                    counts[value] += 1
                    matched_signals[dimension].append(cue)

        if dimension == "action_bias":
            dimensions[dimension] = _resolve_action_bias(counts)
        elif dimension == "resource_state":
            if counts.get("scarce", 0) > counts.get("strong", 0) and counts.get("scarce", 0) > 0:
                dimensions[dimension] = "scarce"
            elif counts.get("strong", 0) > 0:
                dimensions[dimension] = "strong"
        else:
            dimensions[dimension] = _resolve_level(counts)

    return StructuralProfile(dimensions=dimensions, matched_signals=matched_signals)


def _resolve_level(counts: dict[str, int]) -> str:
    if counts.get("high", 0) > 0:
        return "high"
    if counts.get("medium", 0) > 0:
        return "medium"
    return "low"


def _resolve_action_bias(counts: dict[str, int]) -> str:
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    if not ranked or ranked[0][1] == 0:
        return "neutral"
    if len(ranked) > 1 and ranked[1][1] > 0 and ranked[0][1] == ranked[1][1]:
        return "mixed"
    top_value = ranked[0][0]
    if top_value in {"advance", "consolidate"} and counts.get("advance", 0) > 0 and counts.get("consolidate", 0) > 0:
        return "mixed"
    return top_value


def _merge_value(dimension: str, current: str, hinted: str) -> str:
    if dimension == "action_bias":
        if current == "neutral":
            return hinted
        if current == hinted:
            return current
        if {current, hinted} <= {"advance", "consolidate"}:
            return "mixed"
        return current
    if dimension == "resource_state":
        if current == "balanced":
            return hinted
        return current
    order = ["low", "medium", "high"]
    return order[max(order.index(current), order.index(hinted))]


def _score_level_dimension(question_value: str, case_value: str) -> int:
    if question_value == "low":
        return 0
    if question_value == case_value:
        return 3 if question_value == "high" else 2
    if question_value == "medium" and case_value == "high":
        return 1
    return 0


def _score_resource_state(question_value: str, case_value: str) -> int:
    if question_value == "balanced":
        return 0
    if question_value == case_value:
        return 3
    return 0


def _score_action_bias(question_value: str, case_value: str) -> int:
    if question_value == "neutral":
        return 0
    if question_value == case_value:
        return 3
    if question_value == "mixed" and case_value in {"advance", "consolidate"}:
        return 2
    if question_value in {"advance", "consolidate"} and case_value == "mixed":
        return 1
    return 0
