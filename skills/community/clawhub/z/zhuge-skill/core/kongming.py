"""孔明评语 — 把卦象推演结果转为自然语言决策建议"""
from typing import Dict, Optional
from core.llm import LLMClient


def template_verdict(hex_result: Dict, odds: Dict = None) -> str:
    """模板化评语（不需要 LLM）"""
    yang = hex_result["yang_count"]
    name = hex_result["hexagram_name"]

    if yang >= 5:
        return f"{name}卦五阳临尊，全维度优势，可重仓主胜"
    elif yang == 4:
        return f"{name}卦四阳两阴，主队明显占优，跟进主胜"
    elif yang == 3:
        if odds and odds.get("home_implied", 0) > 0.5:
            return f"{name}卦三阳三阴但赔率倾主胜，谨慎跟进"
        return f"{name}卦势均力敌，建议看平或小球"
    elif yang == 2:
        return f"{name}卦客势略胜，谨慎客胜或大冷"
    elif yang == 1:
        return f"{name}卦五阴临尊反向，看冷门客胜"
    else:
        return f"{name}卦全阴大凶，强烈反向"


def make_decision(hex_result: Dict, odds: Dict = None) -> Dict:
    """从卦象推演 → 决策建议"""
    yang = hex_result["yang_count"]
    home_implied = odds.get("home_implied", 0.5) if odds else 0.5

    # 1x2 决策
    if yang >= 4:
        sel_1x2 = "home"
    elif yang <= 1:
        sel_1x2 = "away"
    elif yang == 2:
        sel_1x2 = "away"
    else:  # yang == 3
        if home_implied > 0.5:
            sel_1x2 = "home"
        elif odds and 1 - 1 / odds.get("away_odd", 99) / (
            1 / odds.get("home_odd", 99) + 1 / odds.get("draw_odd", 99) + 1 / odds.get("away_odd", 99)
        ) > 0.4:
            sel_1x2 = "away"
        else:
            sel_1x2 = "draw"

    # 信心
    if yang >= 5 or yang <= 1:
        confidence = "高"
    elif yang == 4 or yang == 2:
        confidence = "中"
    else:
        confidence = "低"

    return {
        "1x2": sel_1x2,
        "confidence": confidence,
        "verdict": template_verdict(hex_result, odds),
    }


def llm_verdict(hex_result: Dict, match_info: Dict, decision: Dict,
                provider: str = None) -> Optional[str]:
    """让 LLM 写一段更生动的孔明评语（可选）"""
    client = LLMClient(provider=provider)
    if not client.enabled:
        return None

    system = (
        "你是诸葛亮，三国时期蜀汉丞相，以谋略和洞察著称。"
        "现在你被赋予分析现代足球比赛的任务。"
        "请用简练的古风（接近《出师表》的语气，但允许少量现代术语）"
        "对一场比赛给出 80-150 字的评语，包含：形势判断、关键风险、建议。"
    )
    prompt = f"""比赛：{match_info.get('match', '?')}
卦象：{hex_result['hexagram_name']}（{hex_result['yang_count']}/6 阳）
六爻评分：{hex_result.get('yao_summary', {})}
推演判语：{hex_result['verdict']}
推荐：{decision['1x2']} （信心：{decision['confidence']}）

请以诸葛亮的口吻给出战前推演。"""

    text = client.chat(prompt, system=system, max_tokens=300)
    return text
