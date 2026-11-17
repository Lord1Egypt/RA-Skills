# -*- coding: utf-8 -*-
"""双色球「诚实账本」模块（本地 · 私密 · 非预测）

与大乐透 dlt_ledger 同源设计，聚焦双色球：
- 按 period 幂等记录每期花费/中奖/注数（重复跑同期限不重复计）。
- summary() 给出 期数 / 花费 / 中奖 / 净亏 / ROI / 总注数 / 公益金贡献。
- 双色球每注 2 元，约 36% 进公益金（每注≈0.72元）。
- 账本默认在生成预测时按"基本投注"自动记账；开奖后可用 --record-win 回填中奖。
- 纯标准库，数据仅存本地 JSON（ssq_ledger.json，与 ssq_history.json 同目录），
  不联网、不上传。

责任红线：本账本只记录已发生交易、不预测、不承诺中奖；
公益金数字为按官方比例估算的"贡献"，非个人收益。
"""
import json
import os
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER_PATH = os.path.join(HERE, 'ssq_ledger.json')

# 双色球官方：返奖率≈50%（理论参考线，长期每花100元约拿回50）
RETURN_RATE = 0.50
# 彩票公益金占销售额约 36%（双色球等福彩）
CHARITY_RATE = 0.36
# 基本投注每注 2 元
PRICE_PER_ZHU = 2.0


def load_ledger():
    if not os.path.exists(LEDGER_PATH):
        return []
    try:
        with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_ledger(data):
    with open(LEDGER_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record_spend(period, amount=2.0, note="auto: 预测生成(基本投注)"):
    """按 period 幂等 upsert 花费（重复跑同期限不会重复计）。"""
    period = int(period)
    amount = float(amount)
    zhu = max(1, int(round(amount / PRICE_PER_ZHU)))
    data = load_ledger()
    today = datetime.date.today().isoformat()
    for e in data:
        if int(e['period']) == period:
            e['spend'] = amount
            e['zhu'] = zhu
            e['date'] = today
            e['note'] = note
            save_ledger(data)
            return e
    data.append({
        "period": period, "date": today,
        "spend": amount, "zhu": zhu, "wins": 0.0, "note": note,
    })
    save_ledger(data)
    return data[-1]


def record_win(period, amount):
    """记录某期中奖金额（覆盖式，便于多次修正）。"""
    period = int(period)
    amount = float(amount)
    data = load_ledger()
    for e in data:
        if int(e['period']) == period:
            e['wins'] = amount
            save_ledger(data)
            return e
    data.append({
        "period": period, "date": datetime.date.today().isoformat(),
        "spend": 0.0, "zhu": 0, "wins": amount, "note": "manual: 中奖回填",
    })
    save_ledger(data)
    return data[-1]


def summary():
    """基于真实账本数据汇总。返回 dict（含 总注数 / 公益金贡献）。"""
    data = load_ledger()
    total_spend = sum(float(e.get('spend', 0)) for e in data)
    total_wins = sum(float(e.get('wins', 0)) for e in data)
    total_zhu = sum(int(e.get('zhu', 0)) for e in data)
    net = total_wins - total_spend
    periods = len(data)
    roi = (net / total_spend * 100) if total_spend > 0 else 0.0
    charity = round(total_spend * CHARITY_RATE, 2)
    theoretical_net = round(total_spend * RETURN_RATE - total_spend, 2)
    return {
        "periods": periods,
        "total_spend": round(total_spend, 2),
        "total_wins": round(total_wins, 2),
        "total_zhu": total_zhu,
        "net": round(net, 2),
        "roi": round(roi, 2),
        "charity": charity,
        "theoretical_return_rate": RETURN_RATE,
        "theoretical_net": theoretical_net,
    }


def render_ledger_html():
    """供报告内嵌的精简账本卡片（纯展示，不含导出）。"""
    s = summary()
    net_color = "#ff8a8a" if s["net"] < 0 else "#7ee0a0"
    html = (
        '<div class="fp-card" style="grid-column:1/-1;">'
        '<h3>\U0001F4D3 \u8BDA\u5B9E\u8D26\u672C \u00B7 \u4F60\u7684\u53CC\u8272\u7403\u771F\u5B9E\u76C8\u4E8F</h3>'
        '<p class="tip">\u53EA\u8BB0\u5DF2\u53D1\u751F\u7684\u4EA4\u6613\uFF0C\u4E0D\u9884\u6D4B\u3001\u4E0D\u627F\u8BFA\u3002'
        '\u62FF\u6E05\u771F\u5B9E\u4E8F\u6321\u4F4F\u52A0\u6CE8\u7684\u6192\u3002</p>'
        '<div class="fp-row" style="font-size:13px;color:#e6ebff;line-height:2;">'
        '\u7D2F\u8BA1\u671F\u6570 <b style="color:#ffd86b;">' + str(s["periods"]) + '</b> \u00B7 '
        '\u603B\u6CE8\u6570 <b style="color:#ffd86b;">' + str(s["total_zhu"]) + '</b> \u00B7 '
        '\u82B1\u8D39 <b>\u00A5' + ("%.2f" % s["total_spend"]) + '</b> \u00B7 '
        '\u4E2D\u5956 <b>\u00A5' + ("%.2f" % s["total_wins"]) + '</b> \u00B7 '
        '\u51C0\u4E8F <b style="color:' + net_color + ';">\u00A5' + ("%.2f" % s["net"]) + '</b> \u00B7 '
        '\u516C\u76CA\u91D1 <b style="color:#5ee0ff;">\u00A5' + ("%.2f" % s["charity"]) + '</b>'
        '</div>'
        '<p class="tip">\u53CD\u9988\u7387\u7406\u8BBA\u7EBF\u2248' + str(int(RETURN_RATE*100)) + '%\uff1b'
        '\u671F\u671B\u4E3A\u8D1F\u662F\u6570\u5B66\u5FC5\u7136\uff0c\u628A\u8D2D\u5F69\u5F53\u5C0F\u989D\u5A31\u4E50\u3002'
        '\u5F00\u5956\u540E\u7528 <code>python3 ssq_ledger.py --record-win \u671F\u53F7 \u91D1\u989D</code> \u56DE\u586B\u3002</p>'
        '</div>'
    )
    return html


def main():
    import argparse
    ap = argparse.ArgumentParser(description="双色球诚实账本（私密·非预测）")
    ap.add_argument("--record-spend", nargs=2, metavar=("PERIOD", "AMOUNT"), help="记录某期花费(元)")
    ap.add_argument("--record-win", nargs=2, metavar=("PERIOD", "AMOUNT"), help="回填某期中奖(元)")
    ap.add_argument("--summary", action="store_true", help="打印账本汇总")
    args = ap.parse_args()
    if args.record_spend:
        p, a = args.record_spend
        try:
            e = record_spend(p, float(a))
            print("\u2713 \u5df2\u8bb0\u5f55\u82b1\u8d39: \u671f%s = \u00a5%.2f (\u6ce8%d, note=%s)" % (p, float(a), e["zhu"], e["note"]))
        except Exception as ex:
            print("\u2717", ex)
    if args.record_win:
        p, a = args.record_win
        try:
            e = record_win(p, float(a))
            print("\u2713 \u5df2\u56de\u586b\u4e2d\u5956: \u671f%s = \u00a5%.2f" % (p, float(a)))
        except Exception as ex:
            print("\u2717", ex)
    if args.summary or not (args.record_spend or args.record_win):
        print(json.dumps(summary(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
