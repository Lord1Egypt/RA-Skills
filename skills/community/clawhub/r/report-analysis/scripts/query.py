# -*- coding: utf-8 -*-
"""功能A（具体内容查询）+ 功能B（具体网格/渠道查询）演示脚本
用法:
  python query.py topic 否决门槛     # 查具体指标
  python query.py topic 终端合约
  python query.py topic app
  python query.py grid 曼弄枫        # 查网格
  python query.py chan 勐润胖仔      # 查渠道(按名称/编码模糊匹配)
"""
import sys
from analyzer import load_analyzed, summarize, by_county, by_grid, load_county_summary, fmt_wan

chans = load_analyzed()
S = summarize(chans)
CS = load_county_summary()  # 权威逐道损收（万元）


# ============ 功能A：具体内容查询 ============
TOPICS = {
    "门槛": "否决门槛",
    "否决": "否决门槛",
    "金虎": "金虎",
    "ai": "AI五件套",
    "ai5": "AI五件套",
    "会员": "88会员/99会员年包",
    "88": "88会员/99会员年包",
    "终端": "终端合约搭载",
    "合约": "终端合约搭载",
    "牵引": "重点业务牵引系数",
    "投诉": "有责投诉",
    "弱势": "弱势网格攻坚",
    "app": "APP融合率",
    "融合": "APP融合率",
    "0元": "0元渠道",
    "集中": "激励集中度",
}


def topic_gate():
    n = S["n"]
    gate_ok = n - S["gate_notdone"]
    raw = S["raw_total"]
    # 门槛损收 = 原始 - 门槛后
    gate_amt_total = sum(c["gate_amt"] for c in chans)
    gate_loss = raw - gate_amt_total
    print(f"【否决门槛】达标情况")
    print(f"  全州 {n} 家渠道中，门槛未完成 {S['gate_notdone']} 家（{S['gate_notdone_rate']:.1f}%），仅 {gate_ok} 家达档。")
    print(f"  门槛核算单道损收 {fmt_wan(abs(CS['全州']['gate_loss']) * 10000)}"
          f"（景洪 {abs(CS['景洪市']['gate_loss']):.2f}万、勐腊 {abs(CS['勐腊县']['gate_loss']):.2f}万、勐海 {abs(CS['勐海县']['gate_loss']):.2f}万），"
          f"占原始金额的 {abs(CS['全州']['gate_loss']) / (S['raw_total'] / 10000) * 100:.1f}%，是全部六道核算中损失最大的一道。")
    # 分项未完成
    zero = {"AI五件套": S["zero_ai5"], "金虎": S["zero_tiger"],
            "权益+升档": sum(1 for c in chans if c["rights_up"] == 0), "88会员/99会员年包": S["zero_member88"]}
    print("  四项门槛完成量为 0 的渠道数：")
    for k, v in zero.items():
        print(f"    - {k}: {v} 家（{v / n * 100:.1f}%）")
    zero_all = sum(1 for c in chans if c["gate_level"] == "门槛未完成"
                   and c["tiger"] == 0 and c["ai5"] == 0 and c["rights_up"] == 0 and c["member88"] == 0)
    print("  结论：门槛未完成的 369 家中，"
          f"{zero_all} 家（{zero_all / S['gate_notdone'] * 100:.0f}%）四项门槛业务完成量全部为 0（完全无业务），"
          f"其余 {S['gate_notdone'] - zero_all} 家有一定业务量但未达档位线；"
          "88会员年包是完成率最低的单品（92.9% 渠道为 0），与大面积零业务互为表里——"
          "不是某一单项卡住，而是渠道整体业务能力不足。")
    print(f"  另：达档的 28 家分布在 2~5 档（2档4家/3档7家/4档8家/5档9家），无 1 档。")
    print("  改进：按档位逐户下发四项门槛差距（如1档需 AI五件套≥20、金虎≥100、权益+升档≥1000、88会员≥500），"
          "把门槛要求前置到季度初渠道签约环节；对四项全 0 的渠道单独建帮扶台账。")


def topic_tiger():
    n = S["n"]
    done = n - S["zero_tiger"]
    total_tiger = sum(c["tiger"] for c in chans)
    print(f"【金虎】完成情况")
    print(f"  全州 {n} 家渠道中，金虎完成量为 0 的 {S['zero_tiger']} 家（{S['zero_tiger'] / n * 100:.1f}%），仅 {done} 家有产出。")
    print(f"  金虎合计完成 {total_tiger:.0f} 个。")
    print(f"  金虎是否决门槛四项之一，1档门槛 100 个、2档 50 个。当前八成渠道为 0，直接拖垮门槛达档。")
    print("  改进：金虎与合约机/靓号等高价值产品强绑定，渠道主推；对连续两季度金虎为 0 的渠道做帮扶或退出评估。")


def topic_ai5():
    n = S["n"]
    done = n - S["zero_ai5"]
    total = sum(c["ai5"] for c in chans)
    print(f"【AI五件套】完成情况")
    print(f"  全州 {n} 家渠道中，AI五件套完成量为 0 的 {S['zero_ai5']} 家（{S['zero_ai5'] / n * 100:.1f}%），仅 {done} 家有产出。")
    print(f"  合计完成 {total:.0f} 套。")
    print(f"  1档门槛需 20 套、2档需 15 套。当前绝大多数渠道为零，是门槛未完成第二大成因。")
    print("  改进：把 AI 五件套列入渠道月度必做动作，按周通报进度；对头部渠道试点 AI 产品体验区拉动转化。")


def topic_member():
    n = S["n"]
    done = n - S["zero_member88"]
    print(f"【88会员/99会员年包】完成情况")
    print(f"  全州 {n} 家渠道中，年包完成量为 0 的 {S['zero_member88']} 家（{S['zero_member88'] / n * 100:.1f}%），仅 {done} 家完成。")
    print(f"  门槛未完成 369 家与年包为 0 的 369 家完全重合——年包空白是门槛未达档的第一直接原因。")
    print("  改进：年包更适合柜台开口推荐，需给渠道做话术+激励培训；考虑将年包任务分解到人、按周排名。")


def topic_term():
    n = S["n"]
    avg = S["avg_term"]
    print(f"【终端合约搭载】情况")
    print(f"  全州终端合约率均值 {avg:.1f}%，合约率为 0 的渠道 {S['zero_term']} 家（{S['zero_term'] / n * 100:.1f}%）。")
    print(f"  终端合约搭载单道核算损收 {fmt_wan(abs(CS['全州']['term_loss']) * 10000)}"
          f"（县汇总口径：勐海 {CS['勐海县']['term_loss']:.2f}万、勐腊 {CS['勐腊县']['term_loss']:.2f}万；"
          f"景洪 +{CS['景洪市']['term_loss']:.2f}万，因其合约率高的渠道获得系数加成）。")
    print("  改进：优先清点 '办了终端但没搭合约' 的渠道，逐户给目标；合约率 0 的渠道主推合约机政策。")


def topic_focus():
    n = S["n"]
    print(f"【重点业务牵引系数】分布")
    print(f"  0.81（最低档）: {S['coef081']} 家（{S['coef081'] / n * 100:.1f}%）")
    print(f"  0.9           : {S['coef09']} 家（{S['coef09'] / n * 100:.1f}%）")
    print(f"  1.0（满档）   : {S['coef1']} 家（{S['coef1'] / n * 100:.1f}%）")
    print(f"  重点业务牵引单道损收 {fmt_wan(abs(CS['全州']['focus_loss']) * 10000)}"
          f"（景洪 {abs(CS['景洪市']['focus_loss']):.2f}万、勐海 {abs(CS['勐海县']['focus_loss']):.2f}万、勐腊 {abs(CS['勐腊县']['focus_loss']):.2f}万）。")
    print(f"  结论：74.8% 渠道处于最低档 0.81，即存量/产品运营积分占比未达标，重点业务发展严重不均衡。")
    print("  改进：对 0.81 档渠道逐户核对存量运营积分、产品运营积分缺口；把牵引系数作为季度中预警指标而非季末结果。")


def topic_complaint():
    print(f"【有责投诉考核】情况")
    print(f"  当期有责投诉值为 '/'（未出数），主表按 '先按不扣罚计' 处理，投诉考核损收暂为 0。")
    print(f"  该项数据质量待季度末补齐后复核，存在追溯扣罚风险。")
    print("  改进：与投诉主管部门确认出数时间；对上半年投诉集中的渠道提前预警。")


def topic_weakgrid():
    n = S["n"]
    signed = S["signed"]
    print(f"【弱势网格攻坚】参与情况")
    print(f"  全州签约弱势网格攻坚协议的渠道 {signed} 家（签约率 {signed / n * 100:.1f}%）。")
    print(f"  签约后 4 项业务完成量为 0 的 {S['signed_zero_done']} 家（占签约数的 {S['signed_zero_done'] / signed * 100:.1f}%）。")
    print("  结论：参与度本身偏低，且签约渠道中仍有近两成 4 项业务零完成，协议形同虚设。")
    print("  改进：签约前评估渠道承接能力，签约后按月跟踪 4 项业务；零完成渠道按协议执行扣罚并取消下季签约资格。")


def topic_app():
    print(f"【APP融合率】情况（三类新装）")
    print(f"  新入网 APP 融合率均值 {S['avg_newnet_fuse']:.1f}%，"
          f"新终端 {S['avg_newterm_fuse']:.1f}%，宽带 {S['avg_bb_fuse']:.1f}%。")
    print(f"  按 30% 达标线（系数 1.1）、20% 基准线（1.0）、低于 20% 按 0.8 扣减的规则，"
          f"当前新终端(15.2%)、宽带(17.1%)两类明显低于达标线。")
    print(f"  APP 融合系数为 0.8（扣减档）的渠道占比：{sum(1 for c in chans if abs(c['app_coef'] - 0.8) < 0.001) / S['n'] * 100:.1f}%。")
    print(f"  APP融合率单道损收 {fmt_wan(abs(CS['全州']['app_loss']) * 10000)}"
          f"（景洪 {abs(CS['景洪市']['app_loss']):.2f}万、勐海 {abs(CS['勐海县']['app_loss']):.2f}万、勐腊 {abs(CS['勐腊县']['app_loss']):.2f}万）。")
    print("  改进：装宽带/办终端时把 APP 开通做成默认动作（弹窗+话术），主抓新终端与宽带两条融合率最低的线。")


def topic_zero():
    n = S["n"]
    neg = sum(1 for c in chans if c["final"] < 0)
    print(f"【0元渠道 / 激励集中度】")
    print(f"  最终核算金额为 0 的渠道 {S['zero_final']} 家（{S['zero_final_rate']:.1f}%），"
          f"另有 {neg} 家最终金额为负（扣罚超过可发额，按 0 计）——合计近九成渠道本季颗粒无收。")
    got = [c for c in chans if c["final"] > 0]
    got.sort(key=lambda c: -c["final"])
    top5 = got[:5]
    print(f"  有激励的渠道仅 {len(got)} 家，头部前 5 名合计 {fmt_wan(sum(c['final'] for c in top5))}：")
    for c in top5:
        print(f"    - {c['name']}（{c['county']}-{c['grid']}）{fmt_wan(c['final'])}")
    print("  结论：激励高度集中，头部与尾部断层；大量渠道投入产出失衡，需警惕下季参与意愿下降。")
    print("  改进：对零激励渠道做分层（纯业务差 vs 门槛差），业务差的给帮扶，门槛差的下季前置宣贯。")


def query_topic(keyword):
    matched = [k for k in TOPICS if k.lower() in keyword.lower()]
    if not matched:
        print(f"未识别内容 '{keyword}'。可查：门槛/否决、金虎、AI五件套、会员、终端合约、牵引系数、投诉、弱势网格、APP融合率、0元渠道")
        return
    topic = TOPICS[matched[0]]
    fn = {"否决门槛": topic_gate, "金虎": topic_tiger, "AI五件套": topic_ai5,
          "88会员/99会员年包": topic_member, "终端合约搭载": topic_term,
          "重点业务牵引系数": topic_focus, "有责投诉": topic_complaint,
          "弱势网格攻坚": topic_weakgrid, "APP融合率": topic_app,
          "0元渠道": topic_zero}[topic]
    print(f"\n================ 功能A · 内容查询：{topic} ================")
    fn()


# ============ 功能B：具体网格/渠道查询 ============
def query_grid(name):
    grids = by_grid(chans)
    hit = [g for g in grids if name in g["grid"]]
    if not hit:
        print(f"未找到网格 '{name}'。现有网格示例：曼弄枫、铂金、度假、嘎栋、滨江、勐捧镇、勐遮镇、勐腊县城区网格")
        return
    g = hit[0]
    print(f"\n================ 功能B · 网格查询：{g['county']}-{g['grid']}网格 ================")
    print(f"渠道数 {g['n']} 家 | 原始金额 {fmt_wan(g['raw'])} | 最终金额 {fmt_wan(g['final'])} "
          f"| 损失 {fmt_wan(g['loss'])}（{g['loss_rate']:.0f}%）| 门槛未完成 {g['gate_notdone']} 家 | 0元 {g['zero_final']} 家")
    # 网格内损失构成
    raw = g["raw"]
    amt_stages = {
        "否决门槛后": sum(c["gate_amt"] for c in g["chans"]),
        "终端合约后": sum(c["term_amt"] for c in g["chans"]),
        "重点业务后": sum(c["focus_amt"] for c in g["chans"]),
        "弱势网格后": sum(c["weakgrid_amt"] for c in g["chans"]),
        "APP融合后": sum(c["final"] for c in g["chans"]),
    }
    print("  损失构成（逐道核算累计扣减）：")
    prev = raw
    for k, v in amt_stages.items():
        print(f"    {k}: {fmt_wan(v)}（本道扣 {fmt_wan(prev - v)}）")
        prev = v
    # 网格内渠道明细 TOP 损失
    print("  网格内损失最大的渠道：")
    for c in sorted(g["chans"], key=lambda x: -x["loss"])[:5]:
        print(f"    - {c['name']}：原始{fmt_wan(c['raw'])} → 最终{fmt_wan(c['final'])}，"
              f"门槛'{c['gate_level']}'，金虎{c['tiger']:.0f}，AI五件套{c['ai5']:.0f}，"
              f"88会员{c['member88']:.0f}，合约率{c['term_ratio'] * 100:.0f}%")
    # 改进建议
    print("  完成情况与改进建议：")
    if g["gate_notdone"] / g["n"] > 0.8:
        print(f"    ① 门槛未完成占比 {g['gate_notdone'] / g['n'] * 100:.0f}%——先逐户补四项门槛（重点是88会员年包、AI五件套），"
              f"这是本网格最大的止血点。")
    if g["zero_final"] / g["n"] > 0.7:
        print(f"    ② 0元渠道占比 {g['zero_final'] / g['n'] * 100:.0f}%——对零激励渠道逐个做原因归类，纯业务缺口的上帮扶资源，"
              f"门槛缺口的季初宣贯。")
    zero_term = sum(1 for c in g["chans"] if c["term_ratio"] == 0)
    print(f"    ③ 终端合约率为0的 {zero_term} 家——主推合约机搭载。")
    low_fuse = sum(1 for c in g["chans"] if c["newterm_fuse"] < 15 or c["bb_fuse"] < 15)
    print(f"    ④ 新终端或宽带融合率低于15%的 {low_fuse} 家——办机装宽时默认开APP。")


def query_chan(kw):
    hits = [c for c in chans if kw in c["name"] or kw.lower() in c["code"].lower()]
    if not hits:
        print(f"未找到渠道 '{kw}'。可输入渠道名称关键字或编码（如 KML00080、勐润胖仔）。")
        return
    for c in hits[:3]:
        print(f"\n================ 功能B · 渠道查询：{c['name']} ================")
        print(f"  县/网格：{c['county']} - {c['grid']} | 编码 {c['code']} | 星级 {c['star']:.0f}")
        print(f"  原始兑换金额 {fmt_wan(c['raw'])} → 最终金额 {fmt_wan(c['final'])}，损失 {fmt_wan(c['loss'])}（{c['loss_rate']:.0f}%）")
        print(f"  否决门槛：{c['gate_level']}（金虎 {c['tiger']:.0f} / AI五件套 {c['ai5']:.0f} / "
              f"权益+升档 {c['rights_up']:.0f} / 88会员年包 {c['member88']:.0f}）")
        print(f"  终端：办理量 {c['term_qty']:.0f}，合约数 {c['term_contract']:.0f}，合约率 {c['term_ratio'] * 100:.0f}%")
        print(f"  重点业务牵引系数：{c['focus_coef']:.2f}（1.0满档 / 0.81最低档）")
        print(f"  弱势网格攻坚：签约'{c['weakgrid_sign']}'，4项业务完成量 {c['weakgrid_done']:.0f}")
        print(f"  APP融合：新入网 {c['newnet_fuse']:.0f}%（量{c['newnet']:.0f}）/ 新终端 {c['newterm_fuse']:.0f}%（量{c['newterm']:.0f}）/ "
              f"宽带 {c['bb_fuse']:.0f}%（量{c['bb']:.0f}），系数 {c['app_coef']:.1f}")
        # 改进建议（规则化）
        tips = []
        if c["gate_level"] == "门槛未完成":
            tips.append(f"门槛未完成：按档位补齐四项，当前最缺的是"
                        f"{'88会员年包' if c['member88'] == 0 else ''}{'、AI五件套' if c['ai5'] == 0 else ''}"
                        f"{'、金虎' if c['tiger'] == 0 else ''}{'、权益升档' if c['rights_up'] == 0 else ''}。")
        if c["term_ratio"] == 0:
            tips.append("终端合约率为0：办理的终端未搭载合约，下季每台终端落实合约办理。")
        elif c["term_ratio"] < 0.5:
            tips.append(f"终端合约率 {c['term_ratio'] * 100:.0f}% 偏低，向50%目标靠拢。")
        if c["newterm_fuse"] < 15 or c["bb_fuse"] < 15:
            tips.append("新终端/宽带APP融合率低：装机开卡时把APP开通设为默认动作。")
        if c["focus_coef"] < 1:
            tips.append(f"重点业务牵引系数 {c['focus_coef']:.2f} 未满档，需提升存量/产品运营积分占比。")
        if c["weakgrid_sign"] == "是" and c["weakgrid_done"] == 0:
            tips.append("已签约弱势网格但4项业务零完成，按协议存在扣罚风险，尽快启动攻坚。")
        if c["final"] == 0 and c["raw"] > 0:
            tips.append("本季最终激励为0，属于'有原始产出但核算全损'，优先补门槛。")
        if not tips:
            tips.append("各项指标相对均衡，保持现有打法，重点盯门槛档位维持。")
        print("  需要改进的具体内容：")
        for i, t in enumerate(tips, 1):
            print(f"    {i}. {t}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "topic"
    kw = sys.argv[2] if len(sys.argv) > 2 else "门槛"
    if mode == "grid":
        query_grid(kw)
    elif mode == "chan":
        query_chan(kw)
    else:
        query_topic(kw)
