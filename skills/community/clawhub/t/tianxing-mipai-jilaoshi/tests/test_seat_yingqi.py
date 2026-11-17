"""坐支应期确定性回归：毛泽东 1934 庚申运·甲戌年。

书（下册02 计算规律）明言：庚申运天干庚冲命局甲木（印/用神），
“冲的结果必须流年到位才出事”——1934 甲戌年甲木用神到位、戌冲甲根辰，长征开始。
本测试锁定该确定性结论不得回退。
"""
from __future__ import annotations

import os
import sys
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))

from main import run

DT = datetime.datetime(1893, 12, 26, 8, 0)
SEX = "男"
PLACE = "湖南韶山"
THEME = "事业"
CALC_YEAR = 1934


def _liunian_1934(res):
    ln = next(r for r in res["evidence_chain"] if r["step"] == "liunian")["output"]
    return next(it for it in ln["items"] if it["year"] == 1934)


def test_seat_yingqi_mao_1934():
    res = run(DT, SEX, PLACE, THEME, calc_year=CALC_YEAR)
    item = _liunian_1934(res)
    hits = item["yingqi"]
    assert hits, f"1934 应触发坐支应期，但 yingqi 为空: {item['actions']}"
    # 须为「庚冲甲(命局)」且吉凶=凶（甲木为用神/印）
    hit = next((h for h in hits if h["作用"] == "庚冲甲(时命局)" or h["作用"] == "庚冲甲(月命局)"), None)
    assert hit, f"未找到 庚冲甲 坐支应期命中: {hits}"
    assert "凶" in hit["吉凶"], f"甲木为用神应判凶，实际: {hit['吉凶']}"
    # 依据须指向「戌冲辰(甲根)」或「戌克甲」
    assert "戌" in hit["依据"], f"应期依据应含戌冲辰/戌克甲，实际: {hit['依据']}"
    print("OK 坐支应期: 1934 甲戌 =", hit["作用"], "|", hit["依据"], "|", hit["吉凶"])


def test_seat_yingqi_determinism():
    base = run(DT, SEX, PLACE, THEME, calc_year=CALC_YEAR)
    for i in range(1, 10):
        cur = run(DT, SEX, PLACE, THEME, calc_year=CALC_YEAR)
        assert cur == base, f"第 {i} 次与首次不一致"
    print("OK 坐支应期 10 次运行一致")


# 蒋介石：书四柱 丁亥 庚戌 己巳 庚午；1949 甲辰运·己丑年，甲合己（日主）大败去台。
CH_DT = datetime.datetime(1887, 10, 31, 12, 0)
CH_SEX = "男"
CH_PLACE = "浙江奉化"
CH_YEAR = 1949


def test_seat_yingqi_chiang_1949():
    res = run(CH_DT, CH_SEX, CH_PLACE, "事业", calc_year=CH_YEAR)
    fp = res["four_pillars"]
    assert (fp["year"]["label"], fp["month"]["label"], fp["day"]["label"], fp["hour"]["label"]) \
        == ("丁亥", "庚戌", "己巳", "庚午"), f"四柱应与书一致: {fp}"
    dyn = next(r for r in res["evidence_chain"] if r["step"] == "dayun")["output"]
    assert dyn["current_label"] == "甲辰", f"1949 应行甲辰运，实际 {dyn['current_label']}"
    ln = next(r for r in res["evidence_chain"] if r["step"] == "liunian")["output"]
    item = next(it for it in ln["items"] if it["year"] == 1949)
    hit = next((h for h in item["yingqi"] if h["作用"] == "甲合己(日命局)"), None)
    assert hit, f"1949 应触发 甲合己 坐支应期: {item['yingqi']}"
    assert "凶（日主受伤）" in hit["吉凶"], f"日主受伤须判凶，实际: {hit['吉凶']}"
    print("OK 坐支应期(合·同类根): 1949 己丑 =", hit["作用"], "|", hit["依据"], "|", hit["吉凶"])


if __name__ == "__main__":
    test_seat_yingqi_mao_1934()
    test_seat_yingqi_chiang_1949()
    test_seat_yingqi_determinism()
