"""天星密派测算 pipeline 编排（四权分离：知识 / 计算 / 解释 / 裁判）。

用法：python main.py "1990-12-07 20:00" 男 山西盂县 事业财运
输出 evidence_chain（JSON），供 AI 解释权按固定 8 段模板生成命书。
"""
from __future__ import annotations

import sys
import json
from datetime import datetime

from input_audit import input_audit
from paipan import paipan, GAN
from pattern import pattern
from yongji import yongji
from dayun import dayun
from liunian import liunian
from inference import inference
from conflict_detector import detect_conflicts
from validator import validate

VAULT_BASE = "/Volumes/珑/我的AI大脑/08_命理"


def run(birth_dt: datetime, sex: str, birth_place: str, theme: str | None = None,
        calendar: str = "公历", calc_year: int = 2026, vault_base: str | None = None):
    vb = vault_base or VAULT_BASE
    chain = []
    audit_rec, p = input_audit(birth_dt, birth_place, sex, calendar, vb, theme)
    chain.append(audit_rec)
    # 出生地缺失 → 真太阳时无法校正，按需求不得排盘：短路返回暂定盘
    if p is None:
        val = validate(chain)
        return {
            "input": {
                "birth_dt": birth_dt.strftime("%Y-%m-%d %H:%M"),
                "sex": sex, "birth_place": birth_place,
                "theme": theme, "calendar": calendar, "calc_year": calc_year,
            },
            "four_pillars": None,
            "day_master": None,
            "evidence_chain": [r.to_dict() for r in chain],
            "conflicts": {"has_conflict": False, "verdict": "OK", "conflicts": []},
            "validation": val,
            "tentative": True,
        }
    pat_rec = pattern(birth_dt, p, vb)
    chain.append(pat_rec)
    yj_rec = yongji(pat_rec.output["pattern"], p["day_master"], vb)
    chain.append(yj_rec)
    dy_rec = dayun(birth_dt, p, sex, calc_year, birth_place, vb)
    chain.append(dy_rec)
    ln_rec = liunian(birth_dt, p, range(calc_year, calc_year + 5), vb,
                     dayun_out=dy_rec.output, yongji_out=yj_rec.output)
    chain.append(ln_rec)
    inf_rec = inference(chain, theme, vb)
    chain.append(inf_rec)

    conflicts = detect_conflicts(chain)
    if conflicts["has_conflict"]:
        steps = {r.step for r in chain}
        for c in conflicts["conflicts"]:
            if c["step"] in steps:
                for r in chain:
                    if r.step == c["step"]:
                        r.conflict = True
    val = validate(chain)

    return {
        "input": {
            "birth_dt": birth_dt.strftime("%Y-%m-%d %H:%M"),
            "sex": sex, "birth_place": birth_place,
            "theme": theme, "calendar": calendar, "calc_year": calc_year,
        },
        "four_pillars": p["four_pillars"],
        "day_master": GAN[p["day_master"]],
        "evidence_chain": [r.to_dict() for r in chain],
        "conflicts": conflicts,
        "validation": val,
    }


def _cli():
    if len(sys.argv) < 4:
        print('usage: python main.py "YYYY-MM-DD HH:MM" 男|女 出生地 [主题]')
        return
    dt = datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M")
    sex = sys.argv[2]
    place = sys.argv[3]
    theme = sys.argv[4] if len(sys.argv) > 4 else None
    res = run(dt, sex, place, theme)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()
