#!/usr/bin/env python3
"""
七政-OASIS v2 · 1000角色 + 20类分型 + 限时限量紧迫感
成山农场爆款推演专用
"""
import json, random, os, argparse
from collections import Counter, defaultdict

# ── 凭证 ──────────────────────────────────────────────
def load_key():
    p = '/workspace/.credentials/siliconflow-api.txt'
    if os.path.exists(p):
        with open(p) as f: return f.read().strip()
    return os.environ.get('SILICONFLOW_API_KEY', '')
SILICONFLOW_KEY = load_key()

# ── 背景池 ──────────────────────────────────────────────
BG = {
    "头部KOC":    ["公众号博主10万粉","抖音带货达人5万粉","小红书KOL8万粉","快手主播3万粉","社区团购群主2000人"],
    "腰部KOC":    ["微信群主500人","朋友圈2000人","小红书素人3000粉","宝妈群群主300人"],
    "素人种草":   ["全职妈妈，孩子3岁","上班族，午休刷手机","美食爱好者","社区邻居"],
    "宝妈精准":   ["二宝妈妈，大宝6岁小宝2岁","注重食品安全","孩子护眼需求","孩子加辅食阶段"],
    "银发精准":   ["65岁养生达人","退休教师","帮子女带孩子的老人","注重食疗"],
    "白领精准":   ["互联网从业者996","健身爱好者","精致妈妈","月光族"],
    "羊毛头号":   ["羊毛群群主，日均5单","专业捡漏党","同时盯20个群","有薅羊毛教程"],
    "羊毛普通":   ["上班族碎片时间抢券","有返利软件","专门蹲地推","用比价软件"],
    "羊毛比价":   ["采购经理职业病","开店老板","财务精打细算","经济学学生"],
    "随大流强":   ["普通白领朋友买啥我买啥","家庭群跟风者","朋友圈活跃用户"],
    "随大流弱":   ["社恐不主动分享","普通退休人员","偶尔看手机"],
    "新客首单":   ["第一次听说成山农场","朋友刚推荐","新搬来的邻居"],
    "复购满意":   ["买过成山5次以上","推荐过10个邻居","成山会员卡"],
    "复购一般":   ["买过1-2次体验一般","观望中","去年买过"],
    "观望犹豫":   ["一直在考虑","等更大优惠","收藏了还在比价"],
    "羊毛只看不买": ["围观抄作业","蹲折扣情报","只看不买"],
    "专业差评型": ["职业打假","专门找茬","同行竞争"],
    "批量采购":   ["公司行政采购下午茶","微商代理拿货","开店老板进货"],
    "冷淡对照组":  ["独居年轻人不做饭","极简主义者","完全不感兴趣"],
}

def gen_name():
    s1 = random.choice(["小","阿","老","大"] + list("赵钱孙李周吴郑王冯陈褚卫"))
    s2 = random.choice("林丽华敏静强磊洋勇艳军波飞霞梅兰菊桃桂")
    return f"{s1}{s2}{random.randint(10,99)}"

def make_profiles(n: int) -> list:
    with open('/workspace/skills/qizheng-oasis/configs/agent_blueprints_1000.json') as f:
        bps = [bp for bp in json.load(f) if bp['count'] > 0]
    total = sum(bp['count'] for bp in bps)
    scale = n / total
    out = []
    idx = 0
    for bp in bps:
        cnt = max(1, int(bp['count'] * scale))
        bgs = BG.get(bp['role'], ["普通消费者"])
        for _ in range(cnt):
            out.append({
                "agent_id": idx,
                "role_type": bp['role'],
                "name": gen_name(),
                "age": random.choices([25,30,35,40,45,50,55,60,65],[0.1,0.15,0.2,0.15,0.15,0.1,0.08,0.05,0.02])[0],
                "gender": random.choice(["男","女"]),
                "mbti": random.choice(bp['mbti']),
                "personality": bp['triggers'][:2],
                "background": random.choice(bgs),
                "trigger_words": bp['triggers'],
                "barrier_words": bp['barriers'],
                "influence_score": round(bp['inf'] * random.uniform(0.8, 1.2), 2),
                "action_prob": round(min(bp['prob'] * random.uniform(0.85, 1.1), 1.0), 2),
                "latent_demand": bp['demand'],
                "joined_round": 0,
            })
            idx += 1
    random.shuffle(out)
    for i, p in enumerate(out): p['agent_id'] = i
    return out[:n]

# ── 核心仿真 ────────────────────────────────────────────
class OasisV2:
    def __init__(self, profiles, seed, stock, promo_hours, rounds):
        self.profiles = profiles
        self.seed = seed
        self.n = len(profiles)
        self.total_stock = stock
        self.stock = stock
        self.promo_hours = promo_hours
        self.n_rounds = rounds
        self.round_hours = promo_hours / rounds
        self.awareness = [False] * self.n
        self.ordered = [False] * self.n
        self.posts = []
        self.orders = []
        self.shares = []
        self.round_records = []
        self._build_graph()
        # 种子KOC发帖
        koc = {'头部KOC','腰部KOC','素人种草'}
        for i, p in enumerate(profiles):
            if p['role_type'] in koc:
                self.awareness[i] = True
                p['joined_round'] = 0
                self.posts.append({'round':0,'agent_id':i,'agent_name':p['name'],
                    'role':p['role_type'],'type':'seed_post',
                    'content':f"【爆款】{seed} · 库存{self.stock}份",
                    'influence':p['influence_score'],'engagement':0})

    def _build_graph(self):
        self.follow_graph = defaultdict(set)
        ri = defaultdict(list)
        for i, p in enumerate(self.profiles): ri[p['role_type']].append(i)
        head = set(ri['头部KOC'])
        waist = set(ri['腰部KOC'])
        sat = set(ri['复购满意'])
        crowd = ri['随大流强']
        for j, p in enumerate(self.profiles):
            for k in head:
                if k != j: self.follow_graph[j].add(k)
            if p['role_type'] in {'素人种草','随大流强','随大流弱','新客首单'}:
                for k in waist:
                    if random.random() < 0.5: self.follow_graph[j].add(k)
            if p['role_type'] in {'复购一般','新客首单','随大流强'}:
                for k in sat:
                    if random.random() < 0.4: self.follow_graph[j].add(k)
        for a in crowd:
            for b in crowd:
                if a != b and random.random() < 0.3: self.follow_graph[a].add(b)

    def _spread(self, rnd):
        newly = set()
        rp = {p['agent_id'] for p in self.posts if p['round'] == rnd - 1}
        hp = {p['agent_id'] for p in self.posts if p['round'] == rnd-1 and p['engagement'] >= 5}
        for i in range(self.n):
            if self.awareness[i]: continue
            if self.follow_graph.get(i, set()) & rp:
                newly.add(i)
            elif hp and random.random() < 0.08:
                newly.add(i)
        for i in newly:
            self.awareness[i] = True
            self.profiles[i]['joined_round'] = rnd
        return list(newly)

    def _decide(self, profile, rnd, stock_pct):
        """
        纯决策函数：只决定是否行动，返回行动意图，不修改任何状态。
        """
        role = profile['role_type']
        inf = profile['influence_score']
        base = profile['action_prob']
        stock_boost = max(0, (0.8 - stock_pct)) * 0.4
        time_boost = (rnd / self.n_rounds) * 0.15
        herd = (1 - stock_pct) * 0.3
        seed = self.seed
        sp = "货源充足" if stock_pct>0.7 else ("库存紧张" if stock_pct>0.3 else "仅剩少量！")
        tp = f"还剩{int((self.n_rounds-rnd+1)*self.round_hours)}小时"
        prob = min(base + herd + stock_boost + time_boost, 0.99)

        # KOC发帖
        if role in {'头部KOC','腰部KOC','素人种草'}:
            pp = 0.9 if role=='头部KOC' else (0.75 if role=='腰部KOC' else 0.6)
            if random.random() < pp:
                txts = [f"{seed}", f"【必抢】{seed} · {sp}！{tp}"]
                if stock_pct < 0.3: txts.append(f"⚠️ {seed}库存告急！快抢！")
                return {'type':'post','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'content':random.choice(txts),'influence':inf,'engagement':0}

        # 羊毛党意图
        if role in {'羊毛头号','羊毛普通'}:
            mult = 2.0 if role=='羊毛头号' else 1.5
            if random.random() < min(prob * mult * (1+stock_boost), 0.99):
                qty = random.choices([1,2],[0.75,0.25])[0]
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':qty,'trigger':'羊毛党'}

        # 随大流意图
        elif role in {'随大流强','随大流弱'}:
            signal = min(len(self.orders)/30, 1.0) if role=='随大流强' else min(len(self.orders)/50, 1.0)
            if random.random() < min(base + signal*0.5 + herd*1.5 + stock_boost, 0.95):
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':1,'trigger':'随大流'}

        # 精准需求意图
        elif role in {'宝妈精准','银发精准','白领精准'}:
            if random.random() < min(prob * 1.1 + stock_boost*0.5, 0.9):
                qty = random.choices([1,2],[0.6,0.4])[0]
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':qty,'trigger':'精准'}

        # 复购意图
        elif role in {'复购满意','复购一般'}:
            b = 0.92 if role=='复购满意' else 0.6
            if random.random() < min(b*(1+stock_boost*0.5), 0.95):
                qty = random.choices([1,2],[0.5,0.5])[0]
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':qty,'trigger':'复购'}

        # 批量采购意图
        elif role == '批量采购':
            if random.random() < min(prob*1.5+stock_boost, 0.9):
                qty = random.choices([3,5,10],[0.3,0.4,0.3])[0]
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':qty,'trigger':'批量'}

        # 新客意图
        elif role == '新客首单':
            if random.random() < min(prob + stock_boost, 0.7):
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':1,'trigger':'新客'}

        return None



    def boost(self):
        order_ids = {o['agent_id'] for o in self.orders}
        for post in self.posts:
            post['engagement'] += sum(1 for oid in order_ids if oid in self.follow_graph.get(post['agent_id'], set()))

    def run_round(self, rnd):
        sp = self.stock / self.total_stock
        rec = {'round':rnd,'stock_start':self.stock,'sp_start':round(sp*100,1),
               'posts':[],'orders':[],'shares':[],'new_aware':0,'total_aware':sum(self.awareness)}
        new = self._spread(rnd)
        rec['new_aware'] = len(new)

        # 收集所有行动，再批量扣库存（避免单agent清空全部库存）
        round_actions = []
        random.shuffle(self.profiles)  # 随机顺序，避免同类集中
        for p in self.profiles:
            if not self.awareness[p['agent_id']]: continue
            a = self._decide(p, rnd, sp)
            if a: round_actions.append((p, a))

        # 按角色优先级排序下单：批量采购→羊毛党→精准→复购→新客→随大流
        ORDER_PRIORITY = {'批量采购':0,'羊毛头号':1,'羊毛普通':2,'宝妈精准':3,'银发精准':4,'白领精准':5,'复购满意':6,'复购一般':7,'新客首单':8,'随大流强':9,'随大流弱':10}

        stock_left = self.stock
        for p, a in sorted(round_actions, key=lambda x: ORDER_PRIORITY.get(x[0]['role_type'], 99)):
            if a['type'] == 'post':
                self.posts.append({**a,'round':rnd})
                rec['posts'].append(a)
            elif a['type'] == 'order':
                qty = min(a.get('quantity', 1), stock_left)
                if qty > 0 and not self.ordered[p['agent_id']]:
                    self.ordered[p['agent_id']] = True
                    stock_left -= qty
                    order_record = {'round':rnd,'agent_id':p['agent_id'],'agent_name':a['agent_name'],
                        'role':a['role'],'quantity':qty,'trigger':a.get('trigger','')}
                    self.orders.append(order_record)
                    rec['orders'].append(order_record)
                    if random.random() < 0.2:
                        s = {'round':rnd,'agent_id':p['agent_id'],'agent_name':a['agent_name'],'role':a['role']}
                        self.shares.append(s)
                        rec['shares'].append(p['agent_id'])

        self.stock = stock_left
        self.boost()
        rec['stock_end'] = max(0, self.stock)
        rec['depleted'] = self.stock <= 0
        self.round_records.append(rec)
        return rec

    def run(self):
        print(f"[v2] 启动：{self.n}人 · 库存{self.total_stock}份 · {self.n_rounds}轮 · {self.promo_hours}h")
        print(f"[v2] 种子KOC发帖：{len([p for p in self.posts if p['round']==0])}条\n")
        for r in range(1, self.n_rounds+1):
            before = self.stock
            rec = self.run_round(r)
            print(f"[v2] R{r}/{self.n_rounds} | 新知晓+{rec['new_aware']} | "
                  f"订单{len(rec['orders'])}单(剩{rec['stock_end']}份) | 发帖{len(rec['posts'])}条"
                  + (" ← 库存耗尽！" if rec['depleted'] else ""))
            if rec['depleted']: break
        return {
            'seed_event': self.seed, 'n_agents': self.n,
            'total_stock': self.total_stock, 'n_rounds': self.n_rounds,
            'posts': self.posts, 'orders': self.orders, 'shares': self.shares,
            'round_records': self.round_records,
            'stock_depleted_round': next((r['round'] for r in self.round_records if r['depleted']), None),
            'profiles': self.profiles
        }

# ── 分析 ────────────────────────────────────────────────
def analyze_v2(res):
    orders, posts, recs = res['orders'], res['posts'], res['round_records']
    n, stock = res['n_agents'], res['total_stock']
    sub = 16.0 - 9.9
    r_orders = Counter(o['role'] for o in orders)
    r_posts = Counter(p['role'] for p in posts)
    by_r = Counter(r['round'] for r in recs)
    total_sold = sum(o.get('quantity',1) for o in orders)
    depleted = res.get('stock_depleted_round') is not None

    # 外推：仿真转化率 × 8倍真实触达
    sim_rate = total_sold / n
    real_est = int(sim_rate * n * 8)
    pess = min(int(real_est*0.5), stock)
    neut = min(int(real_est*0.8), stock)
    opt = min(int(real_est*1.2), stock)

    # 羊群检测
    herd = None
    prev = 0
    for rr in recs:
        cur = by_r.get(rr['round'], 0)
        if prev > 20 and cur > prev * 1.3:
            herd = rr['round']; break
        prev = cur

    # 时间线
    tl = " → ".join(f"R{rr['round']}新+{rr['new_aware']}(剩{rr['stock_end']})" for rr in recs)
    top5 = sorted(posts, key=lambda p: p.get('engagement',0), reverse=True)[:5]

    koc_p = r_posts.get('头部KOC',0) + r_posts.get('腰部KOC',0)
    wool = r_orders.get('羊毛头号',0) + r_orders.get('羊毛普通',0)
    crowd = r_orders.get('随大流强',0)
    batch = r_orders.get('批量采购',0)

    recs_out = []
    if koc_p < 50: recs_out.append({"p":"高","issue":f"KOC发帖不足({koc_p}条)","action":"私聊5位头部KOC发样品"})
    if wool < 100: recs_out.append({"p":"中","issue":f"羊毛党激活不足({wool}人)","action":"在返利群定向投放"})
    if herd: recs_out.append({"p":"高","issue":f"羊群效应R{herd}触发","action":"触发前追加投放，触发后控成本"})
    if depleted: recs_out.append({"p":"高","issue":"库存提前耗尽！","action":"立即补货或推预售锁客"})
    elif neut < stock*0.4: recs_out.append({"p":"中","issue":"库存剩余>60%","action":"延长时间或加大投放"})

    return {
        "scenario": res['seed_event'], "n_agents": n, "total_stock": stock,
        "metrics": {
            "total_orders": len(orders), "total_units_sold": total_sold,
            "total_posts": len(posts),
            "unique_buyers": len({o['agent_id'] for o in orders}),
            "awareness_rate": round(recs[-1]['total_aware']/n*100,1) if recs else 0,
            "conversion_rate": round(len({o['agent_id'] for o in orders})/(recs[-1]['total_aware'] if recs else 1)*100,1),
        },
        "projection": {
            "inventory": stock, "stock_depleted": depleted,
            "stock_depleted_round": res.get('stock_depleted_round'),
            "pess": pess, "neut": neut, "opt": opt,
            "pess_loss": round(pess*sub,0), "neut_loss": round(neut*sub,0), "opt_loss": round(opt*sub,0),
            "sub": sub, "real_reach": n*8,
        },
        "transmission": {
            "by_round": dict(sorted(by_r.items())),
            "timeline": tl, "herd": herd,
            "peak": by_r.most_common(1)[0][0] if by_r else 0,
            "depleted": depleted,
            "top5": [{"agent":p['agent_name'],"role":p['role'],"content":p['content'][:60],"eng":p.get('engagement',0)} for p in top5]
        },
        "roles": {
            "buy_top5": r_orders.most_common(5),
            "post_top5": r_posts.most_common(5),
        },
        "risks": {
            "stockout": "高" if depleted else ("中" if neut>=stock*0.8 else "低"),
            "koc_p": koc_p, "wool": wool, "crowd": crowd, "batch": batch,
        },
        "recommendations": recs_out
    }

def print_v2(a):
    m, p, t, r = a['metrics'], a['projection'], a['transmission'], a['risks']
    dw = f" ⚠️ 库存在R{p.get('stock_depleted_round','?')}耗尽！" if p.get('stock_depleted_round') else ""
    print(f"""
═══════════════════════════════════════════════════════════
  七政-OASIS v2 · 1000角色爆款推演
  场景：{a['scenario']}
  {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
═══════════════════════════════════════════════════════════

📊 仿真结果
  · {a['n_agents']}人 × {a['total_stock']}份库存 · 触达预估{p['real_reach']}人
  · 售出{p['inventory']-max(0, max(t['by_round'].values()))}份（去重{m['unique_buyers']}人下单）{dw}
  · 知晓率{m['awareness_rate']}% · 转化率{m['conversion_rate']}%

═══════════════════════════════════════════════════════════
📦 订单量预测
═══════════════════════════════════════════════════════════
  悲观  {p['pess']}单  亏损¥{p['pess_loss']:.0f}
  中性  {p['neut']}单  亏损¥{p['neut_loss']:.0f}
  乐观  {p['opt']}单  亏损¥{p['opt_loss']:.0f}
  每单补贴¥{p['sub']} · 爆仓概率：{r['stockout']}

═══════════════════════════════════════════════════════════
🔥 传播分析
═══════════════════════════════════════════════════════════
  {t['timeline']}
  羊群R{t['herd'] or '未'}触发 · 峰值R{t['peak']} · 各轮{t['by_round']}
  TOP帖子：""")
    for i, x in enumerate(t['top5'], 1):
        print(f"  {i}. 【{x['role']}·{x['agent']}】{x['content']}  互动+{x['eng']}")

    print(f"""
═══════════════════════════════════════════════════════════
🏆 角色贡献
═══════════════════════════════════════════════════════════
  下单：{' / '.join(f"{r[0]}({r[1]}单)" for r in a['roles']['buy_top5'])}
  发帖：{' / '.join(f"{r[0]}({r[1]}条)" for r in a['roles']['post_top5'])}

═══════════════════════════════════════════════════════════
⚠️ 风险
═══════════════════════════════════════════════════════════
  爆仓：{r['stockout']} | KOC发帖{r['koc_p']}条 | 羊毛党{r['wool']}人 | 随大流{r['crowd']}人 | 批量{r['batch']}人""")
    if a['recommendations']:
        print("\n💡 建议：")
        for rec in a['recommendations']:
            print(f"  【{rec['p']}】{rec['issue']} → {rec['action']}")

# ── 主程序 ──────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scenario', default='成山农场蓝莓9.9元/斤爆款限时抢')
    ap.add_argument('--n_agents', type=int, default=1000)
    ap.add_argument('--stock', type=int, default=500)
    ap.add_argument('--hours', type=int, default=24)
    ap.add_argument('--rounds', type=int, default=4)
    ap.add_argument('--output', default='/workspace/data/qizheng-oasis/result_v2.json')
    args = ap.parse_args()

    os.makedirs('/workspace/data/qizheng-oasis', exist_ok=True)
    print(f"[天枢v2] 生成{args.n_agents}个角色...")
    profiles = make_profiles(args.n_agents)

    print(f"[天权v2] 运行仿真...")
    world = OasisV2(profiles, args.scenario, args.stock, args.hours, args.rounds)
    result = world.run()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n[天玑v2] 分析...")
    a = analyze_v2(result)
    print_v2(a)

    with open(args.output.replace('.json','_analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(a, f, ensure_ascii=False, indent=2)
    print(f"\n[完成] {args.output}")

if __name__ == '__main__':
    main()
