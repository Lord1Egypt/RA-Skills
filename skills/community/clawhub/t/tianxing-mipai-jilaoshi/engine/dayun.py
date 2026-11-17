"""排大运（Pipeline Step 5a）。

- 阳年男 / 阴年女顺排；阴年男 / 阳年女逆排。
- 起运：顺数到下一节令 / 逆数到上一节令；3 日 = 1 年（精确按日，含时辰折算）。
- 未行运前以月柱为大运（vault N2）。
- 各步从月柱顺/逆推 60 甲子。
全确定性、离线。
"""
from __future__ import annotations

from datetime import datetime

from evidence import EvidenceRecord, load_vault_text, load_by_canonical
from paipan import GAN, BRANCH, gz_index
import solar_time as st

DAYUN_RULES = ["DAYUN_SHUNNI", "DAYUN_QIYUN", "DAYUN_STEP"]


def _six_conflict(z1, z2):
    return (z1 - z2) % 12 == 6


def dayun(birth_dt: datetime, p: dict, sex: str, calc_year: int = 2026,
          birth_place: str = "", vault_base: str | None = None):
    fp = p["four_pillars"]
    year_gan = fp["year"]["gan"]
    yang_year = (year_gan % 2 == 0)
    male = (sex == "男")
    forward = (yang_year and male) or (not yang_year and not male)

    month_branch = fp["month"]["zhi"]
    jie_idx = (month_branch - 2) % 12  # 月支 -> 月界节索引
    # 节气时刻为 UTC，出生钟表时间为北京时间，必须转 UTC 后再相减；
    # 不可用真太阳时（那是地方性读数，与 UTC 节气不同坐标系，会少算约 8h ≈ 0.11 年起运）。
    birth_jd = st._julian_day(st.to_utc(birth_dt))

    # 下一/上一节令 jd（> birth_jd 最小 / < birth_jd 最大）
    if forward:
        nj = (jie_idx + 1) % 12
        cands = [st._solar_term_jd(birth_dt.year, st.JIE_LONGITUDE[nj]),
                 st._solar_term_jd(birth_dt.year + 1, st.JIE_LONGITUDE[nj])]
        term_jd = min(c for c in cands if c > birth_jd)
    else:
        # 出生必在本月之节（jie_idx）之后（否则月支就不会是本月支），
        # 故逆数「上一节令」= 本月之节本身，不是 jie_idx-1。
        # （旧实现取 jie_idx-1，等于跳过一个节，起运岁数被多算约 10 岁。）
        pj = jie_idx
        cands = [st._solar_term_jd(birth_dt.year - 1, st.JIE_LONGITUDE[pj]),
                 st._solar_term_jd(birth_dt.year, st.JIE_LONGITUDE[pj])]
        term_jd = max(c for c in cands if c < birth_jd)

    diff_days = abs(term_jd - birth_jd)
    start_age = diff_days / 3.0  # 3 日 = 1 年

    month_idx = gz_index(fp["month"]["gan"], fp["month"]["zhi"])
    dirn = 1 if forward else -1
    steps = []
    for k in range(8):
        idx = (month_idx + dirn * (k + 1)) % 60
        g, z = idx % 10, idx % 12
        lo = start_age + k * 10
        hi = start_age + (k + 1) * 10
        steps.append({
            "step": k,
            "label": GAN[g] + BRANCH[z],
            "gan": g, "zhi": z,
            "age_range": f"{lo:.0f}–{hi:.0f}",
        })

    age = calc_year - birth_dt.year
    cur = int((age - start_age) // 10) if age >= start_age else -1
    cur = max(-1, min(cur, len(steps) - 1))

    vault_path, vault_text = load_by_canonical("天星密派 — 基础·排盘·命局大运流年", vault_base)
    vault_ref = vault_path if vault_text else "VAULT_UNREADABLE"

    out = {
        "forward": forward,
        "start_age": round(start_age, 2),
        "month_pillar_prerun": fp["month"]["label"],  # 未行运前代运
        "steps": steps,
        "current_step": cur,
        "current_label": steps[cur]["label"] if cur >= 0 else fp["month"]["label"],
        "current_age_range": steps[cur]["age_range"] if cur >= 0 else "未起运",
    }
    rec = EvidenceRecord(
        step="dayun",
        input={"sex": sex, "month_label": fp["month"]["label"], "forward": forward},
        rules_used=DAYUN_RULES,
        intermediate_reasoning=(f"{'顺' if forward else '逆'}排；起运 {start_age:.2f} 岁"
                                f"（出生到{'下' if forward else '上'}一节令差 {diff_days:.2f} 日，3日=1年）；"
                                f"当前 {calc_year} 年 {age} 岁，行第 {cur} 步 {out['current_label']}。"),
        opposing_evidence="起运流派（精确到时辰/真太阳时）不同师承略有差异，本实现按天星密派·基础（N2）明确定额。",
        output=out,
        confidence=0.9,
        vault_source=vault_ref,
    )
    return rec
