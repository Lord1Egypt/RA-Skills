"""
wangshuai_score.py — 旺衰评分引擎（明文开源版）

基于京房六爻传统旺衰理论：
- 月建：旺相休囚死（季节旺衰）
- 日建：七效应（临/生/克/冲/合/刑/害）
- 附加：帝旺、墓库、回头生克、绝地

MIT License — 完全开源，欢迎审查和贡献
"""

from typing import Dict, List, Optional, Any

# ══════════════════════════════════════════════════════════
# 基础常量（与 liuyao.py 保持一致）
# ══════════════════════════════════════════════════════════

ZHI_ORDER = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

BRANCH_WUXING = {
    "子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火",
    "午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水",
}

CONFLICT_BRANCH = {"子":"午","午":"子","丑":"未","未":"丑","寅":"申","申":"寅",
                   "卯":"酉","酉":"卯","辰":"戌","戌":"辰","巳":"亥","亥":"巳"}

COMBINE_BRANCH = {"子":"丑","丑":"子","寅":"亥","亥":"寅","卯":"戌","戌":"卯",
                   "辰":"酉","酉":"辰","巳":"申","申":"巳","午":"未","未":"午"}

GENERATE_WUXING = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
CONQUER_WUXING  = {"木":"土","土":"水","水":"火","火":"金","金":"木"}

# 帝旺（五行帝旺之月）
IMPERIAL_WANG = {"木":"卯","火":"午","土":"戌","金":"酉","水":"子"}

# 绝地（五行绝地之月）
EXTINCTION = {"木":"申","火":"亥","土":"寅","金":"巳","水":"卯"}

# 墓库（五行墓库之地）
TOMB_BRANCH = {"寅":"寅","申":"未","巳":"巳","亥":"亥",
               "卯":"卯","酉":"酉","子":"子","午":"午",
               "辰":"辰","戌":"戌","丑":"丑","未":"未"}

# 三刑 / 六害
SANXING_BRANCH = {"寅":"巳","巳":"申","申":"寅",
                  "丑":"未","未":"戌","戌":"丑",
                  "子":"卯","卯":"子"}

LIUHAI_BRANCH = {"子":"未","未":"子","丑":"午","午":"丑",
                 "寅":"巳","巳":"寅","卯":"辰","辰":"卯",
                 "申":"亥","亥":"申","酉":"戌","戌":"酉"}


# ══════════════════════════════════════════════════════════
# 月建旺衰：旺相休囚死
# ══════════════════════════════════════════════════════════

def seasonal_status(mb: str) -> Dict[str, str]:
    """根据月建地支返回五行旺相休囚死状态"""
    if mb in ["寅","卯"]:
        return {"木":"旺","火":"相","水":"休","金":"囚","土":"死"}
    if mb in ["巳","午"]:
        return {"火":"旺","土":"相","木":"休","水":"囚","金":"死"}
    if mb in ["申","酉"]:
        return {"金":"旺","水":"相","土":"休","火":"囚","木":"死"}
    if mb in ["亥","子"]:
        return {"水":"旺","木":"相","金":"休","土":"囚","火":"死"}
    if mb in ["辰","戌","丑","未"]:
        return {"土":"旺","金":"相","火":"休","木":"囚","水":"死"}
    return {}


# ══════════════════════════════════════════════════════════
# 单爻旺衰评分
# ══════════════════════════════════════════════════════════

_SEASON_SCORES = {
    "旺": (2.0, "旺(强)"), "相": (1.5, "相(次强)"),
    "休": (-0.5, "休(次弱)"), "囚": (-1.0, "囚(弱)"),
    "死": (-1.5, "死(最弱)"),
}


def calculate_strength(yb: str, mb: str, db: str,
                       changed_yao: Optional[str] = None,
                       is_moving: bool = False) -> Dict[str, Any]:
    """
    计算单爻旺衰综合评分

    参数：
        yb: 爻的地支
        mb: 月建地支
        db: 日辰地支
        changed_yao: 变爻地支（动爻时提供）
        is_moving: 是否动爻

    返回：
        {"score": float, "status": List[str]}
    """
    score = 0.0
    status = []
    yw = BRANCH_WUXING[yb]
    mw = BRANCH_WUXING[mb]
    dw = BRANCH_WUXING[db]

    # ═══════════ 月建：旺相休囚死 ═══════════
    seasonal = seasonal_status(mb).get(yw, "")
    if seasonal in _SEASON_SCORES:
        sc, label = _SEASON_SCORES[seasonal]
        score += sc
        status.append(label)

    # 月同比（当月令与爻地支一致时额外加分）
    if yb == mb and seasonal != "旺":
        score += 1.0
        status.append("月建(强)")

    # 月冲
    if CONFLICT_BRANCH.get(yb) == mb:
        score -= 2.0
        status.append("月冲")

    # 月合
    if COMBINE_BRANCH.get(yb) == mb:
        if CONQUER_WUXING.get(mw) != yw and CONQUER_WUXING.get(yw) != mw:
            score += 1.0
            status.append("月合")
        else:
            score -= 0.5
            status.append("月合(差)")

    # ═══════ 日建：冲合刑害生克 ═══════
    # 日临
    if yb == db:
        score += 1.5
        status.append("日建(强)")

    # 日生（日辰五行生爻五行）
    if GENERATE_WUXING.get(dw) == yw:
        score += 1.5
        status.append("日生")

    # 日克（日辰五行克爻五行）
    if CONQUER_WUXING.get(dw) == yw:
        score -= 1.0
        status.append("日克")

    # 日冲（巳冲亥等）
    if CONFLICT_BRANCH.get(yb) == db:
        if score < 0.5:
            score -= 1.5
            status.append("日冲(破)")
        else:
            score -= 0.5
            status.append("日冲(暗动)")

    # 日合（子丑合等）
    if COMBINE_BRANCH.get(yb) == db:
        if CONQUER_WUXING.get(dw) != yw and CONQUER_WUXING.get(yw) != dw:
            score += 1.0
            status.append("日合")
        else:
            score -= 0.5
            status.append("日合(差)")

    # 日刑
    if SANXING_BRANCH.get(yb) == db:
        score -= 0.5
        status.append("日刑")

    # 日害
    if LIUHAI_BRANCH.get(yb) == db:
        score -= 0.5
        status.append("日害")

    # ═══════ 神煞辅助 ═══════
    # 帝旺
    dwb = IMPERIAL_WANG.get(yw)
    if not isinstance(dwb, list):
        dwb = [dwb]
    if db in dwb:
        score += 0.5
        status.append("帝旺")

    # 墓库（月墓/日墓）
    tb = TOMB_BRANCH.get(yw)
    if not isinstance(tb, list):
        tb = [tb]
    tomb = []
    if mb in tb:
        tomb.append("月墓")
    if db in tb:
        tomb.append("日墓")
    if tomb:
        if is_moving:
            status.append(f"墓{'/'.join(tomb)}(冲)")
        else:
            score = max(score, -0.1)
            status.append(f"墓{'/'.join(tomb)}")

    # 绝地
    if not is_moving and db == EXTINCTION.get(yw, ""):
        score -= 0.5
        status.append("绝地")

    if changed_yao and is_moving and changed_yao == EXTINCTION.get(yw, ""):
        score -= 1.0
        status.append("化绝")

    return {"score": round(score, 2), "status": status}


def batch_calculate_strength(yao_branches: List[str], mb: str, db: str,
                              changed_branches: Optional[List[str]] = None,
                              is_moving_yaos: Optional[List[bool]] = None) -> List[Dict[str, Any]]:
    """
    批量计算六爻旺衰评分

    参数：
        yao_branches: 六爻地支列表（初→上）
        mb: 月建地支
        db: 日辰地支
        changed_branches: 变爻地支列表（可选）
        is_moving_yaos: 动爻标记列表（可选）

    返回：
        [{"score": float, "status": List[str]}, ...] × 6
    """
    changed_branches = changed_branches or [None] * 6
    is_moving_yaos = is_moving_yaos or [False] * 6
    return [
        calculate_strength(yao_branches[i], mb, db,
                           changed_branches[i], is_moving_yaos[i])
        for i in range(6)
    ]
