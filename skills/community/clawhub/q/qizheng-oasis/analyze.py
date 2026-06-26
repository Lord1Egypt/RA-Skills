#!/usr/bin/env python3
"""
Step3: 结果分析器（天玑）
"""
import json, argparse, os
from collections import Counter

def analyze_result(sim_result):
    orders = sim_result['orders']
    posts = sim_result['posts']
    shares = sim_result['shares']
    recs_all = sim_result['round_records']
    profiles = sim_result['profiles']
    n = sim_result['n_agents']

    # ── 角色维度 ────────────────────────────────────
    role_orders = Counter(o['role'] for o in orders)
    role_posters = Counter(p['role'] for p in posts)

    # ── 时间线 ──────────────────────────────────────
    orders_per_round = Counter(r['round'] for r in recs_all)
    aware_per_round = [(r['round'], r['newly_aware_count'], r['total_aware']) for r in recs_all]

    # ── 传播阶段 ───────────────────────────────────
    first_rec = recs_all[0]
    total_aware_pct = recs_all[-1]['total_aware'] / n
    if total_aware_pct < 0.3:
        stage = "初期（信息刚扩散，仍有大量潜在用户未触达）"
    elif total_aware_pct < 0.6:
        stage = "爆发前期（传播链正在建立，即将进入高速扩散）"
    elif total_aware_pct < 0.8:
        stage = "爆发期（羊群效应已形成，规模扩散中）"
    else:
        stage = "饱和期（大部分目标用户已触达，扩散减缓）"

    # ── 羊群触发检测 ─────────────────────────────────
    herd_round = None
    prev_cnt = 0
    for rr in recs_all:
        cur = orders_per_round.get(rr['round'], 0)
        if prev_cnt > 3 and cur > prev_cnt * 1.5:
            herd_round = rr['round']
            break
        prev_cnt = cur

    # ── 推算（库存500份基准）──────────────────────────
    sim_orders = len(orders)
    inventory = 500
    cost, price = 16.0, 9.9
    subsidy = cost - price

    proj = {
        "inventory": inventory,
        "pessimistic_orders": min(int(sim_orders * 0.6), inventory),
        "neutral_orders": min(sim_orders, inventory),
        "optimistic_orders": min(int(sim_orders * 1.8), inventory),
        "pessimistic_loss": round(min(int(sim_orders * 0.6), inventory) * subsidy, 0),
        "neutral_loss": round(min(sim_orders, inventory) * subsidy, 0),
        "optimistic_loss": round(min(int(sim_orders * 1.8), inventory) * subsidy, 0),
        "subsidy_per_order": subsidy,
        "cost_basis": cost,
        "sell_price": price,
    }

    # ── 热门帖子 ─────────────────────────────────────
    top_posts = sorted(posts, key=lambda p: p.get('engagement', 0), reverse=True)[:3]

    # ── 风险 ────────────────────────────────────────
    koc_posts = role_posters.get('KOC种草型', 0)
    wool_orders = role_orders.get('羊毛党型', 0)
    cold_risk = "低" if koc_posts >= 5 and wool_orders >= 5 else "高"
    stockout_risk = "高" if proj['optimistic_orders'] >= inventory else "低"

    # ── 建议 ────────────────────────────────────────
    recs = []
    if koc_posts < 8:
        recs.append({"priority": "高", "issue": f"KOC发帖量不足（仅{koc_posts}条）",
                      "action": "私聊3~5位种子KOC直接发样品或返现激励"})
    if wool_orders < 10:
        recs.append({"priority": "中", "issue": f"羊毛党参与率偏低（{wool_orders}人下单）",
                      "action": "在羊毛党聚集的优惠券群/返利群定向投放"})
    if herd_round:
        recs.append({"priority": "高", "issue": f"羊群效应在第{herd_round}轮触发",
                      "action": "触发前加大投放，触发后减少支出让自然流量接手"})
    if stockout_risk == "高":
        recs.append({"priority": "高", "issue": f"乐观订单（{proj['optimistic_orders']}）接近/超过库存上限",
                      "action": "设置超卖预案：超出部分引导到次日预售或退款"})
    else:
        recs.append({"priority": "低", "issue": "库存充足",
                      "action": "可考虑追加投放，将库存利用率提升至80%以上"})

    # ── 时间线字符串 ───────────────────────────────
    timeline_str = " → ".join(
        f"R{rr['round']}新+{rr['newly_aware_count']}"
        for rr in recs_all
    )

    # ── 最终分析结果 ────────────────────────────────
    return {
        "scenario": sim_result['seed_event'],
        "n_agents": n,
        "metrics": {
            "total_orders": sim_orders,
            "total_posts": len(posts),
            "total_shares": len(shares),
            "awareness_rate": round(total_aware_pct * 100, 1),
            "unique_buyers": len({o['agent_id'] for o in orders}),
            "conversion_rate": round(len({o['agent_id'] for o in orders}) / recs_all[-1]['total_aware'] * 100, 1)
        },
        "projection": proj,
        "transmission": {
            "stage": stage,
            "herd_triggered_round": herd_round,
            "peak_order_round": orders_per_round.most_common(1)[0][0] if orders_per_round else 0,
            "orders_by_round": dict(orders_per_round),
            "timeline_str": timeline_str,
            "awareness_detail": [
                {"round": rr['round'], "new_aware": rr['newly_aware_count'], "total_aware": rr['total_aware']}
                for rr in recs_all
            ],
            "top_posts": [
                {"agent": p['agent_name'], "role": p['role'],
                 "content": p['content'][:50], "engagement": p.get('engagement', 0)}
                for p in top_posts
            ]
        },
        "role_breakdown": {
            "orders_by_role": dict(role_orders),
            "posts_by_role": dict(role_posters)
        },
        "risks": {
            "cold_risk": cold_risk,
            "stockout_risk": stockout_risk,
            "koc_posts": koc_posts,
            "wool_orders": wool_orders
        },
        "recommendations": recs
    }


def print_report(analysis):
    m = analysis['metrics']
    p = analysis['projection']
    t = analysis['transmission']
    r = analysis['risks']

    header = f"""
═══════════════════════════════════════════
  七政-OASIS 市场推演报告
  场景：{analysis['scenario']}
  生成：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
═══════════════════════════════════════════

📊 仿真概况
  · 模拟规模：{analysis['n_agents']}个角色（发帖{m['total_posts']}条/订单{m['total_orders']}单/转发{m['total_shares']}次）
  · 知晓率：{m['awareness_rate']}% | 转化率：{m['conversion_rate']}%
  · 独立下单用户：{m['unique_buyers']}人

═══════════════════════════════════════════
📦 订单量预测（库存{p['inventory']}份基准）
═══════════════════════════════════════════

  悲观（冷场）  {p['pessimistic_orders']}单   亏损 ¥{p['pessimistic_loss']:.0f}
  中性（正常）  {p['neutral_orders']}单   亏损 ¥{p['neutral_loss']:.0f}
  乐观（爆款）  {p['optimistic_orders']}单   亏损 ¥{p['optimistic_loss']:.0f}

  每单补贴：¥{p['subsidy_per_order']}/单（成本{p['cost_basis']}元×售价{p['sell_price']}元）

═══════════════════════════════════════════
🔥 传播分析：{t['stage']}
═══════════════════════════════════════════

  传播轮次：{t['timeline_str']}
  羊群触发：第{t['herd_triggered_round'] or '未'}轮
  订单峰值：第{t['peak_order_round']}轮

  热门帖子TOP3："""
    print(header)

    for i, post in enumerate(t['top_posts'], 1):
        print(f"  {i}. 【{post['role']}·{post['agent']}】{post['content']}...  互动+{post['engagement']}")

    print(f"""
═══════════════════════════════════════════
⚠️ 风险评估
═══════════════════════════════════════════

  冷场风险：{r['cold_risk']}（KOC发帖{r['koc_posts']}条 / 羊毛党下单{r['wool_orders']}人）
  爆仓风险：{r['stockout_risk']}""")

    if r['cold_risk'] == "高":
        print("  → 冷场预警：请提前联系KOC确认发帖")
    if r['stockout_risk'] == "高":
        print("  → 爆仓预警：设置超卖退款预案")

    recs = analysis['recommendations']
    if recs:
        print(f"""
═══════════════════════════════════════════
💡 行动建议
═══════════════════════════════════════════""")
        for rec in recs:
            print(f"  【{rec['priority']}】{rec['issue']}")
            print(f"  → {rec['action']}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--result', required=True)
    ap.add_argument('--output', default=None)
    args = ap.parse_args()

    with open(args.result, encoding='utf-8') as f:
        sim_result = json.load(f)

    analysis = analyze_result(sim_result)
    print_report(analysis)

    # 保存JSON
    json_out = args.result.replace('.json', '_analysis.json')
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    if args.output:
        import io, sys
        buf = io.StringIO()
        sys.stdout = buf
        print_report(analysis)
        sys.stdout = sys.__stdout__
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(buf.getvalue())

    print(f"[天玑] 分析完成 → {json_out}")


if __name__ == '__main__':
    main()
