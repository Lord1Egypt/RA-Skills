"""排流年 + 作用路线（Pipeline Step 5b）。

流年干支：与年柱同公式 (year - 1984) % 60。
作用路线：
- 确定性“六冲”标记（子午/丑未/寅申/卯酉/巳亥/辰戌），对命局四柱地支。
- 确定性“坐支应期”（LIUNIAN_SEAT_YINGQI）：大运天干冲/合命局某字（或坐支受伤），
  须流年该字天干「到位」且流年地支「契合大运天干作用方向」才出结果（双条件）。
  来源：[[17-七星九元命理]] 下册02 计算规律（毛泽东/蒋介石/袁宝璟案例）。
其余越组合作用（合/会/临/失脱/发动/二次同向）vault 无统一量化，
交 inference / conflict_detector 处理并标 needs_formalization。
"""
from __future__ import annotations

from evidence import EvidenceRecord, load_vault_text, load_by_canonical
from paipan import GAN, BRANCH, GAN_WX, BRANCH_WX, gz_index

LIUNIAN_RULES = ["LIUNIAN_GANZHI", "LIUNIAN_CHONG", "LIUNIAN_SEAT_YINGQI"]

SIX_CHONG = [(0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11)]  # (支, 支+6)

WX_CHAR = ["木", "火", "土", "金", "水"]  # 与 paipan.GAN_WX / BRANCH_WX 同编码（0木1火2土3金4水）

# 天干六冲（序号差 6）/ 五合（序号和 5 或 9/11/13 模10 互补）
GAN_CHONG = {(0, 6), (1, 7), (2, 8), (3, 9)}
GAN_HE = {(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)}


def _conflict_pairs(z):
    return [b for (a, b) in SIX_CHONG if z in (a, b)]


def _sheng(a, b):  # a 生 b？
    return (a + 1) % 5 == b


def _ke(a, b):  # a 克 b？
    return (a + 2) % 5 == b


def _wx(c):
    return WX_CHAR[c]


def _relation(G, g):
    """大运天干 G 与命局天干 g 的冲/合关系（越组合作用）。"""
    if (G, g) in GAN_CHONG or (g, G) in GAN_CHONG:
        return "冲"
    if (G, g) in GAN_HE or (g, G) in GAN_HE:
        return "合"
    return None


def _zhi_hurt_gan(z, g):
    """地支 z 对天干 g 是否使其受伤（z 克 g，或 g 生 z 而泄）。"""
    return _ke(BRANCH_WX[z], GAN_WX[g]) or _sheng(GAN_WX[g], BRANCH_WX[z])


def _yingqi_basis(z, X, X_seat, G, Z, rel):
    """流年地支 z 是否契合大运天干 G 对 X 的作用方向，返回依据串或 None。

    双条件之地支侧，四种契合口径（b1–b4）：
      b1 流年支克 X（直接伤）
      b2 流年支冲 X 坐支（间接伤其根）—— 毛泽东 庚申运冲甲、甲戌年戌冲辰(甲根)
      b3 流年支生助大运天干 G（作用方增力）
      b4 合且流年支与 X 同类（X 根到位，合中带克）—— 蒋介石 甲辰运合己、己丑年丑为己根
    """
    zw, Xx, Gx = BRANCH_WX[z], GAN_WX[X], GAN_WX[G]
    if _ke(zw, Xx):  # b1
        return f"流年支{BRANCH[z]}({_wx(zw)})克{GAN[X]}({_wx(Xx)})→X受伤"
    if X_seat is not None and (z - X_seat) % 12 == 6:  # b2
        return f"流年支{BRANCH[z]}冲{GAN[X]}坐支{BRANCH[X_seat]}"
    if _sheng(zw, Gx) or zw == Gx:  # b3
        return f"流年支{BRANCH[z]}({_wx(zw)})生助大运天干{GAN[G]}({_wx(Gx)})"
    if rel == "合" and zw == Xx:  # b4
        return f"流年支{BRANCH[z]}({_wx(zw)})为{GAN[X]}同类根，合中带克到位"
    return None


def _build_hit(G, Z, rel, X, pos, ly, lz, basis, theory_yong, theory_ji, src, day_master):
    # 日主（日干）受伤恒为凶（日元无救），与五行用忌分类无关；
    # 用忌映射仅适用于非日主之字。
    if X == day_master:
        ji = "凶（日主受伤）"
    else:
        Xw = _wx(GAN_WX[X])
        if Xw in theory_yong:
            ji = "凶（用神受作用）"
        elif Xw in theory_ji:
            ji = "吉（忌神受作用）"
        else:
            ji = "中性"
    return {
        "大运": GAN[G] + BRANCH[Z],
        "作用": f"{GAN[G]}{rel}{GAN[X]}({pos}{src})",
        "流年": GAN[ly] + BRANCH[lz],
        "依据": basis,
        "吉凶": ji,
    }


def _seat_yingqi_year(G, Z, fp, y, z, theory_yong, theory_ji):
    """某流年是否触发坐支应期（双条件：天干到位 + 地支契合）。返回命中说明列表。"""
    hits = []
    day_master = fp["day"]["gan"]
    # (A) 大运天干 G 冲/合 命局某天干 X
    for ek, ck in (("year", "年"), ("month", "月"), ("day", "日"), ("hour", "时")):
        g = fp[ek]["gan"]
        seat = fp[ek]["zhi"]
        rel = _relation(G, g)
        if not rel:
            continue
        X = g
        if y != X:                      # 天干到位（双条件之一）
            continue
        basis = _yingqi_basis(z, X, seat, G, Z, rel)
        if basis:                       # 地支契合（双条件之二）
            hits.append(_build_hit(G, Z, rel, X, ck, y, z, basis, theory_yong, theory_ji, "命局", day_master))
    # (B) 大运天干坐支受伤：本运地支 Z 伤 G，流年 G 到位 + 流年地支再伤
    #      —— 袁宝璟 甲午运甲被午伤、甲申年甲到位再被申(金)伤
    if _zhi_hurt_gan(Z, G) and y == G:
        basis = _yingqi_basis(z, G, None, G, Z, "坐支伤")
        if basis:
            hits.append(_build_hit(G, Z, "坐支伤", G, "大运", y, z, basis, theory_yong, theory_ji, "大运", day_master))
    return hits


def _dayun_pillar_at(dayun_out, p, birth_year, year):
    """给定年份对应的当前大运天干/地支（未起运前以月柱代运）。"""
    if not dayun_out:
        return None
    start_age = dayun_out.get("start_age", 0)
    steps = dayun_out.get("steps", [])
    age = year - birth_year
    if age < start_age or not steps:
        return {"gan": p["four_pillars"]["month"]["gan"],
                "zhi": p["four_pillars"]["month"]["zhi"]}
    idx = int((age - start_age) // 10)
    idx = max(0, min(idx, len(steps) - 1))
    s = steps[idx]
    return {"gan": s["gan"], "zhi": s["zhi"]}


def liunian(birth_dt, p: dict, years=range(2026, 2031), vault_base: str | None = None,
            dayun_out: dict | None = None, yongji_out: dict | None = None):
    fp = p["four_pillars"]
    dest_branches = [fp[k]["zhi"] for k in ("year", "month", "day", "hour")]
    theory_yong = (yongji_out or {}).get("theory_yong", [])
    theory_ji = (yongji_out or {}).get("theory_ji", [])
    seat_on = bool(dayun_out and yongji_out)

    items = []
    seat_summary = []
    for y in years:
        idx = (y - 1984) % 60
        g, z = idx % 10, idx % 12
        actions = []
        # 六冲（命局四柱地支）
        for pk, db in zip(("年", "月", "日", "时"), dest_branches):
            if (z - db) % 12 == 6:
                actions.append(f"{pk}支{BRANCH[db]}被流年{BRANCH[z]}冲")
        # 坐支应期（双条件确定性）
        yingqi = []
        if seat_on:
            dp = _dayun_pillar_at(dayun_out, p, birth_dt.year, y)
            if dp:
                G, Z = dp["gan"], dp["zhi"]
                for h in _seat_yingqi_year(G, Z, fp, g, z, theory_yong, theory_ji):
                    yingqi.append(h)
                    actions.append(f"坐支应期：{h['作用']}，流年{h['流年']}到位，{h['依据']}→{h['吉凶']}")
        if yingqi:
            seat_summary.append(f"{y}{GAN[g] + BRANCH[z]}:" + ";".join(
                f"{h['作用']}({h['吉凶']})" for h in yingqi))
        items.append({
            "year": y,
            "label": GAN[g] + BRANCH[z],
            "actions": actions,
            "yingqi": yingqi,
        })

    vault_path, vault_text = load_by_canonical("天星密派 — 基础·排盘·命局大运流年", vault_base)
    vault_ref = vault_path if vault_text else "VAULT_UNREADABLE"

    out = {"items": items}
    if seat_on:
        out["seat_yingqi"] = seat_summary

    chong_parts = []
    for it in items:
        cs = [a for a in it["actions"] if "被流年" in a and "冲" in a]
        if cs:
            chong_parts.append(f"{it['year']}{it['label']}:{','.join(cs)}")
    reasoning = ("流年干支按 (year-1984)%60；对命局四柱做六冲检测。"
                 + ("；".join(chong_parts) if chong_parts else "近五年无六冲。"))
    if seat_on:
        reasoning += ("；坐支应期：" + ("；".join(seat_summary) if seat_summary else "近五年无到位应期。"))

    rec = EvidenceRecord(
        step="liunian",
        input={"years": [y for y in years]},
        rules_used=LIUNIAN_RULES,
        intermediate_reasoning=reasoning,
        opposing_evidence="越组合作用（合/会/临/失脱/发动/二次同向）vault 无统一量化，未形式化；坐支应期已确定性实现（双条件）。",
        output=out,
        confidence=0.95,
        vault_source=vault_ref,
        needs_formalization=True,
    )
    return rec
