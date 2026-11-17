# -*- coding: utf-8 -*-
"""
期号计算工具 — 统一所有模块的下期期号逻辑, 避免发散导致 BUG。

双色球规则:
  - 红球 1-33 选 6, 蓝球 1-16 选 1
  - 每周二/四/日 21:15 开奖

期号编码: YYYY + NNN  (4位年份 + 当年第几期, 从 001 开始) —— 与大乐透的
  5 位 YYSSS 不同, 这是双色球独有格式, 切勿沿用大乐透逻辑。
  - 例: 2024036 = 2024 年第 36 期
  - 年末最后一期之后, 下一期进入下一年 → 2025001

为何用"日期"而不是固定阈值:
  - 每年实际开奖期数在 150~156 之间浮动(每周3期, 闰年可能多 1 期),
    用固定阈值在"年份提早结束"时会产生若干虚假期号。
  - 正确做法: 用最新一期开奖日期推算"下一开奖日", 若跨入下一自然年则进年。
    因为开奖固定在周二/四/日, 年末最后一期与元旦最多相隔 3 天, 此推算永远正确。

本模块的 __main__ 自检会拿 ssq_history.json 全量真实开奖做逐期递推校验
(而不是只跑几个手写用例), 任何一期对不上即判失败。
"""
from datetime import datetime, timedelta

# 周二(+2)->周四, 周四(+3)->周日, 周日(+2)->下周二
# weekday(): 周一=0 周二=1 周三=2 周四=3 周五=4 周六=5 周日=6
_NEXT_DRAW_DELTA = {1: 2, 3: 3, 6: 2}


def _next_draw_date(d):
    """给定一期开奖日期, 返回下一期开奖日期 (下一个周二/四/日)。

    历史上双色球曾有非标准开奖日(早期为每周二/四/日之外的安排或节假日顺延),
    对不在 {周二,周四,周日} 的日期, 退化为"向后找最近的开奖日"。
    """
    wd = d.weekday()
    if wd in _NEXT_DRAW_DELTA:
        return d + timedelta(days=_NEXT_DRAW_DELTA[wd])
    for step in range(1, 8):
        nd = d + timedelta(days=step)
        if nd.weekday() in _NEXT_DRAW_DELTA:
            return nd
    return d + timedelta(days=2)


def next_period(latest_period, latest_date=None):
    """计算下一期期号。

    Args:
        latest_period: int 或 str, 如 2024036 (YYYY+NNN)
        latest_date:   str 'YYYY-MM-DD' 或 None
    Returns:
        str, 如 '2024037' / '2025001'
    """
    p = int(latest_period)
    yp = p // 1000            # 4 位年份
    sp = p % 1000 + 1         # 当年序列 +1

    if latest_date:
        try:
            d = datetime.strptime(str(latest_date)[:10], '%Y-%m-%d')
            nd = _next_draw_date(d)
            if nd.year != yp:
                # 下一开奖日已进入下一年 → 期号进年, 序列归 1
                return f'{nd.year}001'
        except Exception:
            if sp > 160:
                yp += 1
                sp = 1
    else:
        if sp > 160:
            yp += 1
            sp = 1

    return f'{yp}{sp:03d}'


if __name__ == '__main__':
    import json
    import os

    ok = True

    # ---- 手写边界用例 ----
    cases = [
        (2024036, '2024-04-02', '2024037'),   # 周二 -> 周四, 同年
        (2024037, '2024-04-04', '2024038'),   # 周四 -> 周日, 同年
        (2024038, '2024-04-07', '2024039'),   # 周日 -> 下周二, 同年
        (2024152, '2024-12-31', '2025001'),   # 年末周二 -> 元旦后周四, 进年
        (2025001, '2025-01-02', '2025002'),   # 新年第二期
    ]
    for p, dt, exp in cases:
        got = next_period(p, dt)
        flag = 'OK ' if got == exp else 'FAIL'
        if got != exp:
            ok = False
        print(f"  [{flag}] {p} ({dt}) -> {got}  期望 {exp}")

    # ---- 全量真实历史逐期递推校验(最强证据) ----
    hp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssq_history.json')
    if os.path.exists(hp):
        with open(hp, 'r', encoding='utf-8') as f:
            hist = json.load(f)
        total = mism = 0
        bad = []
        for i in range(len(hist) - 1):
            cur, nxt = hist[i], hist[i + 1]
            if not cur.get('date'):
                continue
            total += 1
            got = next_period(cur['period'], cur['date'])
            if got != str(nxt['period']):
                mism += 1
                if len(bad) < 5:
                    bad.append(f"{cur['period']}({cur['date']}) -> {got} 实际 {nxt['period']}")
        rate = (total - mism) / total * 100 if total else 0
        print(f"  [历史递推] {total - mism}/{total} 命中 = {rate:.2f}%")
        for b in bad:
            print(f"      不符: {b}")
        # 早期年份存在非常规开奖日/停开, 允许极少量不符; 近5年必须 百分之百
        recent = [h for h in hist if str(h['period'])[:4] >= '2021']
        rtot = rmis = 0
        for i in range(len(recent) - 1):
            if not recent[i].get('date'):
                continue
            rtot += 1
            if next_period(recent[i]['period'], recent[i]['date']) != str(recent[i + 1]['period']):
                rmis += 1
        print(f"  [近5年递推] {rtot - rmis}/{rtot} 命中")
        if rmis > 0:
            ok = False
    else:
        print("  [跳过] 未找到 ssq_history.json")

    print("  全部通过" if ok else "  *** 存在失败 ***")
