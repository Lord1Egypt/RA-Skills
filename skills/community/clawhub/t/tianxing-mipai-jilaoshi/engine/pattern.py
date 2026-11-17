"""定格局（Pipeline Step 3）。

依据 vault《八字排盘校验规范》《AI 运用天星密派八字推理-能力边界》明确分流规则形式化：
- 月令生扶日主 -> 旺分支；月令克泄耗 -> 弱分支。
- 弱分支中“仍有字旺日元”才是身弱，无根且全局克泄 -> 从弱（不可直接写从弱）。
- 旺分支中“生印比月 + 日支帮扶 + (月干或时干其一帮扶) + 时支不克泄耗”-> 从旺，否则身旺
  （天星密派上册 PDF 133-134、153-159；本质“克泄耗无力则从旺”）。「时支不克泄耗」含两况：
  ① 时支帮扶日主；② 时支官杀被时干印化（官印相生，见二十律“同柱干支直接作用”），不构成有力克泄耗。
- 月令空亡看年支（上册口径）。

注意：vault 自承“格局判断无统一量化权重、阴阳局完整生成算法未给出”，
故本步对“阴阳局/量化权重/从印 vs 从比细分”标 needs_formalization，
输出为保守确定性分流，不臆造精细权重。
"""
from __future__ import annotations

from evidence import EvidenceRecord, load_vault_text, load_by_canonical
from paipan import GAN_WX, BRANCH_WX, GAN

# 十二地支藏干（天干 idx 列表）
HIDDEN = {
    0: [9], 1: [5, 9, 7], 2: [0, 2, 4], 3: [1], 4: [4, 1, 9],
    5: [2, 6, 4], 6: [3, 5], 7: [5, 3, 1], 8: [6, 8, 4], 9: [7],
    10: [4, 3, 7], 11: [8, 0],
}
WX_NAME = ["木", "火", "土", "金", "水"]

PATTERN_RULES = ["PATTERN_MONTH_SUPPORT", "PATTERN_ROOT", "PATTERN_FENLIU", "PATTERN_KONGWANG_YEAR"]


def _supports(w: int, day_wx: int) -> bool:
    """五行 w 对日主 day_wx 是否帮扶（同我=比劫 / 生我=印）。

    五行索引：木0 火1 土2 金3 水4；x 生 y <=> (x+1)%5==y；x 克 y <=> (x+2)%5==y。
    帮扶=同我/生我；泄(我生)、耗(我克)、克(克我) 均非帮扶。
    """
    return w == day_wx or (w + 1) % 5 == day_wx


def _relation(w: int, day_wx: int) -> str:
    if w == day_wx:
        return "同我(比劫)"
    if (w + 1) % 5 == day_wx:
        return "生我(印)"
    if (day_wx + 1) % 5 == w:
        return "我生(食伤,泄)"
    if (w + 2) % 5 == day_wx:
        return "克我(官杀)"
    if (day_wx + 2) % 5 == w:
        return "我克(财,耗)"
    return "?"


def _root_strength(day_wx: int, p: dict):
    fp = p["four_pillars"]
    roots = []
    for pk, label in [("year", "年"), ("month", "月"), ("day", "日"), ("hour", "时")]:
        zhi = fp[pk]["zhi"]
        hidden = HIDDEN[zhi]
        if day_wx in [GAN_WX[h] for h in hidden]:
            if pk == "day":
                roots.append((label, 2.0, "自坐根"))
            else:
                roots.append((label, 1.0, "藏根"))
    for pk in ("year", "month", "hour"):
        g = fp[pk]["gan"]
        if GAN_WX[g] == day_wx and g != fp["day"]["gan"]:
            roots.append((pk, 0.5, "天干比劫"))
    return roots


def _hour_branch_not_reverse(hour_zhi_wx: int, hour_gan_wx: int, day_wx: int) -> bool:
    """时支是否「不克泄耗」日主（从旺格条件，天星密派 PDF 153-159）。

    本质取“克泄耗无力则从旺”（PDF 133-134）。时支对日主不构成有力克泄耗即满足：
    - 时支帮扶日主（同我/生我）→ 满足；
    - 时支官杀(克我) 且 时干印(生我) → 官印相生、官杀被印化，实际不克 → 满足；
    - 其余克泄耗 → 不满足。
    依据二十律“同柱干支直接作用”：官杀生印、印生身，官杀力量被泄，不再克日主。
    """
    if _supports(hour_zhi_wx, day_wx):
        return True
    if (hour_zhi_wx + 2) % 5 == day_wx and (hour_gan_wx + 1) % 5 == day_wx:
        return True
    return False


def pattern(birth_dt, p: dict, vault_base: str | None = None):
    day_wx = GAN_WX[p["day_master"]]
    fp = p["four_pillars"]
    month_zhi = fp["month"]["zhi"]
    mw = BRANCH_WX[month_zhi]

    if mw == day_wx:
        support = "比劫(助)"
    elif (mw + 1) % 5 == day_wx:
        support = "生我(印,助)"
    else:
        support = "克泄耗(不助)"

    roots = _root_strength(day_wx, p)
    total = sum(r[1] for r in roots)

    congwang = None
    if "不助" not in support:  # 旺分支：检验是否升级为从旺格
        branch = "旺"
        day_zhi_wx = BRANCH_WX[fp["day"]["zhi"]]
        hour_zhi_wx = BRANCH_WX[fp["hour"]["zhi"]]
        c_day = _supports(day_zhi_wx, day_wx)
        c_gan = _supports(GAN_WX[fp["month"]["gan"]], day_wx) or \
                _supports(GAN_WX[fp["hour"]["gan"]], day_wx)
        c_hour = _hour_branch_not_reverse(hour_zhi_wx, GAN_WX[fp["hour"]["gan"]], day_wx)  # 时支不克泄耗
        congwang = {
            "day_branch_supports": c_day,
            "month_or_hour_gan_supports": c_gan,
            "hour_branch_not_reverse": c_hour,
            "hour_branch_relation": _relation(hour_zhi_wx, day_wx),
        }
        if c_day and c_gan and c_hour:
            branch = "从旺"
            pattern_name = "从旺"
        else:
            pattern_name = "身旺"
        if total == 0:
            pattern_name += "(弱根,需复核)"
    else:
        branch = "弱"
        # 依据本文件顶部规则：弱分支「仍有字旺日元」即身弱，只有无根且全局克泄才从弱。
        # 旧实现用 total>=2 的权重阈值硬切，与本规则冲突（2026-09-06 修正）。
        #
        # 【未实现：反断格】本分支只按「月令不助 + 有根」定身弱，未实现天星密派身旺格
        # 形式②③（PDF 137-144），遇下列情形必须人工按 11 条复核，不得直接采信本函数：
        #   ②反断格：月令克泄耗日干，但月支被「两次」受克或冲（须年支参加）且日支为印比 → 反断身旺；
        #     反断两硬条件（PDF 75）：克月令必须有年支参加 + 日元坐支必须帮扶，缺一不反断。
        #     月令仅一次受克 → 不反断（11 条之 7）。
        #   ③月令空亡、年支为印比 + 一字生助 → 身旺。
        # 另：旺衰可直接查《天星密派 — 定格·取用·运算规律》「日元旺衰表」（PDF 121），
        # 例：甲×午＝弱、甲×亥＝旺，比本函数的五行推导更权威。
        pattern_name = "身弱" if total > 0 else "从弱"

    reasoning = (f"月支{fp['month']['label'][1]}五行对日主为{support}，进入{branch}分支；"
                 f"根气合计 {total:.1f}（" + "；".join(f"{r[0]}柱{r[2]}" for r in roots) + "）。"
                 + (f"从旺三条件：日支帮扶={congwang['day_branch_supports']}、"
                    f"月干或时干帮扶={congwang['month_or_hour_gan_supports']}、"
                    f"时支不克泄耗={congwang['hour_branch_not_reverse']}"
                    f"（时支{fp['hour']['label'][1]}对日主为{congwang['hour_branch_relation']}）。"
                    if congwang else "")
                 + ("有强根旺日元 -> 身弱非从弱。" if branch == '弱' and pattern_name == '身弱' else ""))

    vault_path, vault_text = load_by_canonical("天星密派 — 核心方法·格局七神阴阳局", vault_base)
    vault_ref = vault_path if vault_text else "VAULT_UNREADABLE"

    out = {
        "month_support": support,
        "branch": branch,
        "roots": [{"pillar": r[0], "weight": r[1], "note": r[2]} for r in roots],
        "root_total": total,
        "pattern": pattern_name,
    }
    if congwang:
        out["congwang_check"] = congwang
    rec = EvidenceRecord(
        step="pattern",
        input={"day_master": GAN[p["day_master"]], "month_zhi": fp["month"]["label"][1]},
        rules_used=PATTERN_RULES,
        intermediate_reasoning=reasoning,
        opposing_evidence="体系自承格局无统一量化权重；阴阳局完整生成算法未给出，本分流为保守确定性口径。",
        output=out,
        confidence=0.9,
        vault_source=vault_ref,
        needs_formalization=True,
    )
    return rec
