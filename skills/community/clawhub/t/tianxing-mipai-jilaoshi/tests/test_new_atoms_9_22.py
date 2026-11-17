"""9-22 新增命理原子的注入锁（回归）：确认五条新原子经 search_atoms 进入
inference.atom_quickref 速查层，不得回退。

- 岁运应期·天干坐支受伤流年到位应期  -> 已由 test_seat_yingqi.py 锁（结构化 yingqi 字段）
- 十神运动规律                       -> 本文件锁（domain=十神运动，主题「事业」召回）
- 局外应事律                         -> 本文件锁（domain=应事律，主题「事业」召回）
- 干支双向与三字取象法               -> 本文件锁（domain=取象，主题「取象」召回）
- 取象字典 — 六十花甲子象意表         -> 本文件锁（domain=取象；修复 evidence.load_all_atoms
                                         此前因文件名前缀不符漏载，等于废原子）

注：「取象字典」文件名为「取象字典 — ...」不以「原子 — 」开头，2026-10-01 修复
load_all_atoms 过滤条件后方能载入；本测试即该修复的回归护栏。
"""
from __future__ import annotations

import os
import sys
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engine"))

from main import run

# 毛泽东 1893-12-26 8:00 湖南韶山，主题驱动检索
DT = datetime.datetime(1893, 12, 26, 8, 0)
SEX = "男"
PLACE = "湖南韶山"


def _quickref(res):
    inf = next(r for r in res["evidence_chain"] if r["step"] == "inference")["output"]
    return inf["atom_quickref"]


def _has(quickref, needle):
    return any(needle in s for s in quickref)


def test_ten_shen_yun_dong_injected():
    """十神运动规律：主题『事业』须召回（domain=十神运动 在 THEME_DOMAIN['事业']）。"""
    res = run(DT, SEX, PLACE, "事业")
    aq = _quickref(res)
    assert _has(aq, "十神运动规律"), f"事业主题未注入【十神运动】原子: {aq}"
    print("OK 十神运动规律 注入 |", next(s for s in aq if "十神运动规律" in s)[:60])


def test_ju_wai_ying_shi_injected():
    """局外应事律：主题『事业』须召回（domain=应事律）。"""
    res = run(DT, SEX, PLACE, "事业")
    aq = _quickref(res)
    assert _has(aq, "局外应事律"), f"事业主题未注入【应事律】局外应事律: {aq}"
    print("OK 局外应事律 注入 |", next(s for s in aq if "局外应事律" in s)[:60])


def test_gan_zhi_shuang_xiang_injected():
    """干支双向与三字取象法：主题『取象』须召回（domain=取象）。"""
    res = run(DT, SEX, PLACE, "取象")
    aq = _quickref(res)
    assert _has(aq, "干支双向与三字取象法"), f"取象主题未注入【取象】干支双向取象法: {aq}"
    print("OK 干支双向与三字取象法 注入 |", next(s for s in aq if "干支双向" in s)[:60])


def test_qu_xiang_zi_dian_injected():
    """取象字典：主题『取象』须召回（domain=取象；修复前因漏载而永不可见）。"""
    res = run(DT, SEX, PLACE, "取象")
    aq = _quickref(res)
    assert _has(aq, "取象字典 — 六十花甲子象意表"), \
        f"取象主题未注入【取象】取象字典（漏载缺陷复现？）: {aq}"
    print("OK 取象字典 注入 |", next(s for s in aq if "取象字典" in s)[:60])


def test_new_atoms_determinism():
    """同输入+同主题，atom_quickref 集合须稳定（不随运行漂移）。"""
    base = set(_quickref(run(DT, SEX, PLACE, "事业")))
    for i in range(1, 8):
        cur = set(_quickref(run(DT, SEX, PLACE, "事业")))
        assert cur == base, f"第 {i} 次 atom_quickref 与首次不一致:\n{cur ^ base}"
    print(f"OK 新原子速查层 8 次运行一致（事业主题 {len(base)} 条）")


if __name__ == "__main__":
    test_ten_shen_yun_dong_injected()
    test_ju_wai_ying_shi_injected()
    test_gan_zhi_shuang_xiang_injected()
    test_qu_xiang_zi_dian_injected()
    test_new_atoms_determinism()
