#!/usr/bin/env python3
"""
七政-OASIS v3 · 分析报告模块
融合：舆情校准 + 传播系数K + 危机响应小组效果 + 竞品反应
"""
import json, random, os, argparse, math
from collections import Counter, defaultdict
from datetime import datetime

# ── 凭证 ──────────────────────────────────────────────
def load_key():
    p = '/workspace/.credentials/siliconflow-api.txt'
    if os.path.exists(p):
        with open(p) as f: return f.read().strip()
    return os.environ.get('SILICONFLOW_API_KEY', '')
SILICONFLOW_KEY = load_key()

# ═══════════════════════════════════════════════════════
#  危机响应小组（ClawTeam swarm逻辑）
# ═══════════════════════════════════════════════════════
RESPONSE_TEAM = [
    {"name":"CEO紧急响应","role":"决策者","action_prob":0.9,"delay_round":1,"effect":8,"neg_effect":0.05,"description":"30分钟内发官方声明，公开道歉+召回+补偿","cooldown":3},
    {"name":"公关部","role":"舆论管控","action_prob":0.85,"delay_round":1,"effect":6,"neg_effect":0.04,"description":"发布正面通稿，联系媒体，投放正面内容","cooldown":2},
    {"name":"法务部","role":"法律应对","action_prob":0.7,"delay_round":2,"effect":4,"neg_effect":0.02,"description":"发律师函，证据保全，准备应诉","cooldown":4},
    {"name":"客服部","role":"客户安抚","action_prob":0.9,"delay_round":1,"effect":5,"neg_effect":0.06,"description":"一对一联系老客户，专线受理投诉","cooldown":1},
    {"name":"运营部","role":"促销对冲","action_prob":0.75,"delay_round":2,"effect":4,"neg_effect":0.03,"description":"推出老客户专属优惠，对冲竞品抢客","cooldown":3},
    {"name":"品控部","role":"质量溯源","action_prob":0.65,"delay_round":2,"effect":3,"neg_effect":0.02,"description":"配合第三方检测，出具质检报告","cooldown":5},
]

# ═══════════════════════════════════════════════════════
#  真实舆情衰减曲线（新华舆情平台数据校准）
# ═══════════════════════════════════════════════════════
CRISIS_DECAY = [
    (0,1.00),(2,0.98),(4,0.90),(6,0.85),(12,0.70),
    (24,0.60),(36,0.50),(48,0.40),(72,0.28),(96,0.18),(120,0.12)
]

def get_decay(hours, intervention_rounds):
    base = 1.0
    for h, d in CRISIS_DECAY:
        if hours <= h: base = d; break
    bonus = max(0.4, 1.0 - intervention_rounds * 0.03)
    return base * bonus

# ═══════════════════════════════════════════════════════
#  爆款传播系数K（帆软爆款预测模型校准）
# ═══════════════════════════════════════════════════════
def viral_k(product_type, promo_price, original_price):
    base = {"水果/生鲜":0.8,"食品":0.6,"日用品":0.5,"服装":0.7,"电子产品":0.4}.get(product_type, 0.5)
    disc = promo_price / original_price
    mult = 2.5 if disc < 0.3 else (1.8 if disc < 0.5 else (1.3 if disc < 0.7 else 1.0))
    return round(base * mult, 2)

# ═══════════════════════════════════════════════════════
#  舆情危机仿真
# ═══════════════════════════════════════════════════════
CRISIS_BPS = [
    {"role":"曝光博主",      "count":30,  "inf":2.5,"prob":0.95,"ct":"amplifier","mbti":["ENTP","ENFP"],"triggers":["必须曝光"],"barriers":[]},
    {"role":"跟风转发",      "count":120, "inf":1.2,"prob":0.80,"ct":"amplifier","mbti":["ESFP","ENFP"],"triggers":["凑热闹"],"barriers":[]},
    {"role":"愤怒声讨",      "count":100, "inf":1.0,"prob":0.90,"ct":"amplifier","mbti":["ENFJ","ESFJ"],"triggers":["必须追责"],"barriers":[]},
    {"role":"理性分析",      "count":80,  "inf":0.8,"prob":0.60,"ct":"neutral","mbti":["INTJ","INTP"],"triggers":["等证据"],"barriers":[]},
    {"role":"沉默大多数",    "count":150, "inf":0.1,"prob":0.15,"ct":"neutral","mbti":["ISFJ","ISTP"],"triggers":["不发言"],"barriers":[]},
    {"role":"忠诚辩护",      "count":60,  "inf":1.5,"prob":0.85,"ct":"defender","mbti":["ISFJ","ESFJ"],"triggers":["维护品牌"],"barriers":[]},
    {"role":"竞争对手推波",  "count":20,  "inf":1.8,"prob":0.90,"ct":"opponent","mbti":["ENTJ","INTJ"],"triggers":["落井下石"],"barriers":[]},
    {"role":"专业投诉",      "count":40,  "inf":1.2,"prob":0.75,"ct":"victim","mbti":["ISTJ","INTJ"],"triggers":["依法维权"],"barriers":[]},
    {"role":"媒体跟进",      "count":30,  "inf":2.0,"prob":0.80,"ct":"media","mbti":["ENFJ","ENTP"],"triggers":["新闻价值"],"barriers":[]},
    {"role":"监管介入",      "count":10,  "inf":1.5,"prob":0.70,"ct":"authority","mbti":["ISTJ","ESTJ"],"triggers":["执法"],"barriers":[]},
    {"role":"水军洗地",      "count":40,  "inf":0.5,"prob":0.60,"ct":"defender","mbti":["ISTP","ISFP"],"triggers":["维护雇主"],"barriers":[]},
    {"role":"竞品受益者",   "count":20,  "inf":0.9,"prob":0.80,"ct":"opponent","mbti":["ENTJ","ESTP"],"triggers":["抢客户"],"barriers":[]},
    {"role":"观望纠结",      "count":100, "inf":0.3,"prob":0.30,"ct":"neutral","mbti":["INFP","ISFJ"],"triggers":["不确定真假"],"barriers":[]},
    {"role":"完全无视",      "count":200, "inf":0.05,"prob":0.02,"ct":"ignore","mbti":["ISTP","ISFP"],"triggers":["不感兴趣"],"barriers":[]},
]

def gen_name():
    s1 = random.choice(["小","阿","老","大"] + list("赵钱孙李周吴郑王冯陈褚卫"))
    s2 = random.choice("林丽华敏静强磊洋勇艳军波飞霞梅兰菊桃桂")
    return f"{s1}{s2}{random.randint(10,99)}"

def make_crisis_profiles(n):
    total = sum(bp['count'] for bp in CRISIS_BPS)
    scale = n / total
    out, idx = [], 0
    for bp in CRISIS_BPS:
        cnt = max(1, int(bp['count'] * scale))
        for _ in range(cnt):
            out.append({"agent_id":idx,"role_type":bp['role'],"crisis_type":bp['ct'],
                "name":gen_name(),"age":random.randint(22,55),
                "gender":random.choice(["男","女"]),"mbti":random.choice(bp['mbti']),
                "trigger_words":bp['triggers'],"barrier_words":bp['barriers'],
                "influence_score":round(bp['inf']*random.uniform(0.8,1.2),2),
                "action_prob":round(min(bp['prob']*random.uniform(0.85,1.1),1.0),2),"joined_round":0})
            idx += 1
    random.shuffle(out)
    for i, p in enumerate(out): p['agent_id'] = i
    return out[:n]

class CrisisWorldV3:
    """舆情危机 + 危机响应小组 + 真实数据校准"""
    def __init__(self, profiles, crisis_desc, hours=48, rounds=6, enable_response_team=True):
        self.profiles = profiles
        self.crisis = crisis_desc
        self.n = len(profiles)
        self.hours = hours
        self.n_rounds = rounds
        self.round_hours = hours / rounds
        self.enable_response_team = enable_response_team

        self.awareness = [False] * self.n
        self.posts = []
        self.neg_posts = []
        self.pos_posts = []
        self.shares = []
        self.reports = []
        self.media = []
        self.round_records = []
        self.response_actions = []  # 响应小组的行动记录
        self.intervention_rounds = 0  # 有效干预轮次
        self.crisis_score = 0.0

        self._build_graph()
        for i, p in enumerate(profiles):
            if p['crisis_type'] in {'amplifier','media','victim','authority'} and p['action_prob'] > 0.6:
                self.awareness[i] = True
                p['joined_round'] = 0
                self._emit(p, 0, 'neg')

    def _build_graph(self):
        self.follow_graph = defaultdict(set)
        ri = defaultdict(list)
        for i, p in enumerate(self.profiles): ri[p['role_type']].append(i)
        for role in ['曝光博主','媒体跟进','愤怒声讨']:
            infl = set(ri.get(role,[]))
            for j in range(self.n):
                for k in infl:
                    if k != j: self.follow_graph[j].add(k)
        defenders = set(ri.get('忠诚辩护',[]))
        for a in defenders:
            for b in defenders:
                if a != b: self.follow_graph[a].add(b)
        for role in ['跟风转发','愤怒声讨']:
            for j in ri.get(role,[]):
                for k in set(ri.get('曝光博主',[])) | set(ri.get('愤怒声讨',[])):
                    if random.random() < 0.6: self.follow_graph[j].add(k)

    def _emit(self, profile, rnd, sentiment):
        templates = {
            'neg': [f"【重大爆料】{self.crisis}", f"【食品安全】{self.crisis}，大家注意！",
                    f"【必须曝光】{self.crisis}", f"【消费者警示】{self.crisis}"],
            'pos': [f"理性看待，成山一直品质可靠，不要信谣", f"老客户声明：我买了很多年从没出过问题",
                    f"支持成山！等官方通报"]
        }
        post = {'round':rnd,'agent_id':profile['agent_id'],'agent_name':profile['name'],
            'role':profile['role_type'],'crisis_type':profile['crisis_type'],
            'sentiment':sentiment,'content':random.choice(templates.get(sentiment,[])),
            'influence':profile['influence_score'],'reach':0,'shares':0,'likes':0,'angry':0}
        self.posts.append(post)
        if sentiment == 'neg': self.neg_posts.append(post)
        else: self.pos_posts.append(post)
        return post

    def _spread(self, rnd):
        newly = set()
        rp = {p['agent_id'] for p in self.posts if p['round'] == rnd - 1}
        neg_rp = {p['agent_id'] for p in self.neg_posts if p['round'] == rnd - 1}
        for i in range(self.n):
            if self.awareness[i]: continue
            followers = self.follow_graph.get(i, set())
            if followers & rp: newly.add(i)
            elif neg_rp and random.random() < 0.15: newly.add(i)
        for i in newly:
            self.awareness[i] = True
            self.profiles[i]['joined_round'] = rnd
        return list(newly)

    def _update_crisis_score(self, rnd):
        hours_now = rnd * self.round_hours
        neg = len(self.neg_posts)
        pos = len(self.pos_posts)
        reports = len(self.reports)
        media_c = len(self.media)

        base = neg * 2 + len(self.shares) * 1 + reports * 3 + media_c * 5
        dilution = max(0, pos * 1.5)
        decay = get_decay(hours_now, self.intervention_rounds)
        raw = (base - dilution) * decay + media_c * 8
        self.crisis_score = max(0, min(100, raw))

    def _run_response_team(self, rnd):
        """ClawTeam swarm逻辑：公司响应小组的自主行动"""
        if not self.enable_response_team:
            return []
        actions_taken = []
        for member in RESPONSE_TEAM:
            if rnd < member['delay_round']: continue
            if random.random() < member['action_prob']:
                # 冷却检查
                recent = [a for a in self.response_actions if a['who'] == member['name']]
                if recent and (rnd - recent[-1]['round']) < member['cooldown']:
                    continue
                # 干预效果
                self.intervention_rounds += 1
                effect = member['effect']
                self.crisis_score = max(0, self.crisis_score - effect)
                self.response_actions.append({
                    'round': rnd,
                    'who': member['name'],
                    'role': member['role'],
                    'effect': effect,
                    'neg_effect': member['neg_effect'],
                    'description': member['description'],
                    'crisis_score_after': round(self.crisis_score, 1)
                })
                actions_taken.append(member['name'])
                # 干预同时产出正面帖子（稀释负面）
                if random.random() < 0.5:
                    fake_profile = {"agent_id":9999,"name":member['name'],"role_type":member['role'],
                        "crisis_type":"defender","influence_score":1.5}
                    self._emit(fake_profile, rnd, 'pos')
        return actions_taken

    def _decide(self, profile, rnd, crisis_score, neg_pct):
        role, ct = profile['role_type'], profile['crisis_type']
        base = profile['action_prob']
        hours_now = rnd * self.round_hours
        tf = 1.3 if hours_now <= 6 else (1.0 if hours_now <= 24 else (0.7 if hours_now <= 48 else 0.4))
        hf = crisis_score / 100 * 0.3
        prob = min(base * tf * (1 + hf), 0.99)
        actions = []

        if ct == 'amplifier':
            if random.random() < prob:
                actions.append({'type':'post','s':'neg'})
                if random.random() < 0.4: actions.append({'type':'share','s':'neg'})
        elif ct == 'opponent':
            if random.random() < min(prob * 1.2, 0.9):
                actions.append({'type':'post','s':'neg'})
                actions.append({'type':'exploit','s':'neg'})
        elif ct == 'defender':
            if random.random() < prob:
                actions.append({'type':'post','s':'pos'})
        elif ct == 'victim':
            if random.random() < prob:
                actions.append({'type':'report','s':'neg'})
        elif ct == 'media':
            if random.random() < min(prob * 0.8, 0.75):
                actions.append({'type':'media','s':'neg'})
        elif ct == 'neutral' and role == '跟风转发':
            if random.random() < min(prob * 1.1, 0.9):
                actions.append({'type':'share','s':'neg'})
        elif ct == 'neutral' and role == '观望纠结':
            nb = max(0, neg_pct - 0.5) * 2
            if random.random() < min(prob * (0.5 + nb), 0.8):
                actions.append({'type':'share','s':'neg'})

        return actions

    def boost(self):
        oid = {o['agent_id'] for o in self.reports}
        for post in self.posts:
            post['reach'] += sum(1 for o in oid if o in self.follow_graph.get(post['agent_id'], set()))

    def run_round(self, rnd):
        rec = {'round':rnd,'hours':int(rnd*self.round_hours),'new_aware':0,
               'posts':[],'shares':[],'reports':[],'media':[],'investigations':[],
               'crisis_score':0.0,'response_team':[],'neg_total':0,'pos_total':0,'total_aware':0}
        new = self._spread(rnd)
        rec['new_aware'] = len(new)
        self._update_crisis_score(rnd)
        rec['crisis_score'] = round(self.crisis_score, 1)
        neg_pct = len(self.neg_posts)/(len(self.neg_posts)+len(self.pos_posts)+1)

        # 危机响应小组行动
        team_actions = self._run_response_team(rnd)
        rec['response_team'] = team_actions
        if team_actions:
            print(f"[响应小组] R{rnd}行动: {', '.join(team_actions)}")

        random.shuffle(self.profiles)
        for p in self.profiles:
            if not self.awareness[p['agent_id']]: continue
            for act in self._decide(p, rnd, self.crisis_score, neg_pct):
                t, s = act['type'], act.get('s','neg')
                if t == 'post':
                    post = self._emit(p, rnd, s)
                    post['reach'] = int(p['influence_score'] * random.randint(50,300))
                    rec['posts'].append({'agent':p['name'],'role':p['role_type']})
                elif t == 'share':
                    self.shares.append({'round':rnd,'agent_id':p['agent_id'],'agent_name':p['name'],'role':p['role_type'],'type':'share','reach':int(p['influence_score']*random.randint(20,100))})
                    rec['shares'].append({'agent':p['name'],'role':p['role_type']})
                elif t == 'report':
                    self.reports.append({'round':rnd,'agent_id':p['agent_id'],'agent_name':p['name'],'role':p['role_type']})
                    rec['reports'].append({'agent':p['name']})
                elif t == 'media':
                    self.media.append({'round':rnd,'agent_name':p['name'],'influence':p['influence_score']})
                    rec['media'].append({'agent':p['name']})
                elif t == 'exploit':
                    self.shares.append({'round':rnd,'agent_id':p['agent_id'],'agent_name':p['name'],'role':p['role_type'],'type':'competitor_steal','reach':int(p['influence_score']*random.randint(100,500))})

        rec['neg_total'] = len(self.neg_posts)
        rec['pos_total'] = len(self.pos_posts)
        rec['total_aware'] = sum(self.awareness)
        self.round_records.append(rec)
        return rec

    def run(self):
        print(f"[舆情危机v3] {self.n}人 · {self.hours}h · {self.n_rounds}轮 · 响应小组:{'ON' if self.enable_response_team else 'OFF'}")
        print(f"[舆情危机v3] 初始曝光帖: {len([p for p in self.posts if p['round']==0])}条\n")
        for r in range(1, self.n_rounds+1):
            rec = self.run_round(r)
            print(f"[舆情危机v3] R{r}/{(rec['hours']}h) 新+{rec['new_aware']} "
                  f"| 帖{len(rec['posts'])}(负{rec['neg_total']}/正{rec['pos_total']}) "
                  f"| 转{len(rec['shares'])} | 投{len(rec['reports'])} | 媒{len(rec['media'])} "
                  team_str = ", ".join(rec["response_team"]) if rec["response_team"] else ""
                  print(f"[舆情危机v3] R{r}/{rec.get('hours','?')}h 新+{rec['new_aware']} | 帖{len(rec['posts'])}(负{rec['neg_total']}/正{rec['pos_total']}) | 转{len(rec['shares'])} | 投{len(rec['reports'])} | 媒{len(rec['media'])} | 热度{rec['crisis_score']:.0f}/100{team_str and ' | 响应:' + team_str or ''}")
        return self._build_result()


    def _build_result(self):
        return {
            'crisis': self.crisis, 'n_agents': self.n, 'hours': self.hours, 'n_rounds': self.n_rounds,
            'posts': self.posts, 'neg_posts': self.neg_posts, 'pos_posts': self.pos_posts,
            'shares': self.shares, 'reports': self.reports, 'media': self.media,
            'round_records': self.round_records,
            'response_team_actions': self.response_actions,
            'intervention_rounds': self.intervention_rounds,
            'profiles': self.profiles,
            'peak_crisis_round': max(self.round_records, key=lambda r: r['crisis_score'])['round'] if self.round_records else 0,
            'peak_crisis_score': max(r['crisis_score'] for r in self.round_records) if self.round_records else 0,
        }

# ═══════════════════════════════════════════════════════
#  促销仿真
# ═══════════════════════════════════════════════════════
PROMO_BPS = [
    {"role":"头部KOC",     "count":30,  "inf":2.5,"prob":0.95,"demand":2,"mbti":["ENFJ","ENTP"],"triggers":["爆款首发","限时特价"],"barriers":["品控不稳"]},
    {"role":"腰部KOC",     "count":70,  "inf":1.8,"prob":0.88,"demand":1,"mbti":["ENFJ","ESFP"],"triggers":["真实体验","产品故事"],"barriers":["性价比不够"]},
    {"role":"素人种草",    "count":100, "inf":1.2,"prob":0.75,"demand":1,"mbti":["ESFP","ENFP"],"triggers":["好看好吃","买过都说好"],"barriers":["怕不好吃"]},
    {"role":"宝妈精准",    "count":120, "inf":1.0,"prob":0.80,"demand":2,"mbti":["ISFJ","ESFJ"],"triggers":["孩子爱吃","有机安全"],"barriers":["怕不新鲜","怕农药"]},
    {"role":"银发精准",    "count":60,  "inf":0.7,"prob":0.65,"demand":2,"mbti":["ISTJ","ISFJ"],"triggers":["养生健康","熟人推荐"],"barriers":["不会用手机买"]},
    {"role":"白领精准",    "count":80,  "inf":0.8,"prob":0.60,"demand":1,"mbti":["INTJ","ISTJ"],"triggers":["品质生活","方便快捷"],"barriers":["不知道怎么吃"]},
    {"role":"羊毛头号",    "count":60,  "inf":1.5,"prob":0.95,"demand":2,"mbti":["ESTP","ESFP"],"triggers":["全网最低","限时特价"],"barriers":["需要拉人"]},
    {"role":"羊毛普通",    "count":120, "inf":0.8,"prob":0.88,"demand":1,"mbti":["ESTP","ISTP"],"triggers":["好价","限时"],"barriers":["买多了浪费"]},
    {"role":"羊毛比价",    "count":60,  "inf":0.6,"prob":0.70,"demand":0,"mbti":["INTJ","INTP"],"triggers":["全网最低","对比优势"],"barriers":["超市更便宜"]},
    {"role":"随大流强",    "count":80,  "inf":0.9,"prob":0.75,"demand":1,"mbti":["ESFJ","ENFJ"],"triggers":["朋友圈晒单","KOC推荐"],"barriers":["没人买就放弃"]},
    {"role":"随大流弱",    "count":60,  "inf":0.4,"prob":0.40,"demand":0,"mbti":["ISFJ","ISTJ"],"triggers":["刚好需要"],"barriers":["没有社交信号"]},
    {"role":"新客首单",    "count":80,  "inf":0.5,"prob":0.55,"demand":1,"mbti":["ENFP","ISFP"],"triggers":["新用户优惠","尝鲜"],"barriers":["不信任"]},
    {"role":"复购满意",    "count":50,  "inf":1.5,"prob":0.92,"demand":2,"mbti":["ISFJ","ESFJ"],"triggers":["成山出品必买","孩子爱吃"],"barriers":["价格比上次贵"]},
    {"role":"复购一般",    "count":40,  "inf":0.9,"prob":0.60,"demand":1,"mbti":["ISFJ","ISTJ"],"triggers":["价格够低就买"],"barriers":["体验一般"]},
    {"role":"观望犹豫",    "count":50,  "inf":0.3,"prob":0.25,"demand":0,"mbti":["INTJ","INTP"],"triggers":["确认价格见底"],"barriers":["还会不会更低"]},
    {"role":"批量采购",    "count":20, "inf":1.2,"prob":0.85,"demand":2,"mbti":["ENTJ","ESTJ"],"triggers":["公司团购","走量优惠"],"barriers":["价格不够低"]},
    {"role":"冷淡对照",    "count":10, "inf":0.1,"prob":0.03,"demand":0,"mbti":["INTP","INTJ"],"triggers":["价格低到离谱"],"barriers":["不需要"]},
]

def make_promo_profiles(n):
    total = sum(bp['count'] for bp in PROMO_BPS)
    scale = n / total
    out, idx = [], 0
    for bp in PROMO_BPS:
        cnt = max(1, int(bp['count'] * scale))
        for _ in range(cnt):
            out.append({"agent_id":idx,"role_type":bp['role'],"name":gen_name(),
                "age":random.choices([25,30,35,40,45,50,55,60,65],[0.1,0.15,0.2,0.15,0.15,0.1,0.08,0.05,0.02])[0],
                "gender":random.choice(["男","女"]),"mbti":random.choice(bp['mbti']),
                "trigger_words":bp['triggers'],"barrier_words":bp['barriers'],
                "influence_score":round(bp['inf']*random.uniform(0.8,1.2),2),
                "action_prob":round(min(bp['prob']*random.uniform(0.85,1.1),1.0),2),
                "latent_demand":bp['demand'],"joined_round":0})
            idx += 1
    random.shuffle(out)
    for i, p in enumerate(out): p['agent_id'] = i
    return out[:n]

class PromoWorldV3:
    """爆款促销 + 传播系数K + 外推公式升级"""
    def __init__(self, profiles, seed, stock, promo_hours, rounds, original_price=26.0, promo_price=9.9, product_type="水果/生鲜"):
        self.profiles = profiles; self.seed = seed; self.n = len(profiles)
        self.total_stock = stock; self.stock = stock
        self.promo_hours = promo_hours; self.n_rounds = rounds
        self.round_hours = promo_hours / rounds
        self.original_price = original_price; self.promo_price = promo_price
        self.viral_k = viral_k(product_type, promo_price, original_price)
        self.awareness = [False]*self.n; self.ordered = [False]*self.n
        self.posts = []; self.orders = []; self.shares = []; self.round_records = []
        self._build_graph()
        koc = {'头部KOC','腰部KOC','素人种草'}
        for i, p in enumerate(profiles):
            if p['role_type'] in koc:
                self.awareness[i] = True; p['joined_round'] = 0
                self.posts.append({'round':0,'agent_id':i,'agent_name':p['name'],'role':p['role_type'],
                    'type':'seed_post','content':f"【爆款】{seed}",'influence':p['influence_score'],'engagement':0})

    def _build_graph(self):
        self.follow_graph = defaultdict(set)
        ri = defaultdict(list)
        for i, p in enumerate(self.profiles): ri[p['role_type']].append(i)
        head = set(ri['头部KOC']); waist = set(ri['腰部KOC'])
        sat = set(ri['复购满意']); crowd = ri['随大流强']
        for j in range(self.n):
            for k in head:
                if k != j: self.follow_graph[j].add(k)
        for j, p in enumerate(self.profiles):
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
            followers = self.follow_graph.get(i, set())
            if followers & rp: newly.add(i)
            elif hp and random.random() < 0.08: newly.add(i)
        for i in newly:
            self.awareness[i] = True; self.profiles[i]['joined_round'] = rnd
        return list(newly)

    def _decide(self, profile, rnd, stock_pct):
        role = profile['role_type']; inf = profile['influence_score']
        base = profile['action_prob']; seed = self.seed
        sb = max(0,(0.8-stock_pct))*0.4
        tb = (rnd/self.n_rounds)*0.15
        herd = (1-stock_pct)*0.3
        sp = "货源充足" if stock_pct>0.7 else ("库存紧张" if stock_pct>0.3 else "仅剩少量！")
        tp = f"还剩{int((self.n_rounds-rnd+1)*self.round_hours)}h"
        prob = min(base + herd + sb + tb, 0.99)

        if role in {'头部KOC','腰部KOC','素人种草'}:
            pp = 0.9 if role=='头部KOC' else (0.75 if role=='腰部KOC' else 0.6)
            if random.random() < pp:
                txts = [f"{seed}", f"【必抢】{seed} · {sp}！{tp}"]
                if stock_pct < 0.3: txts.append(f"⚠️ {seed}库存告急！快抢！")
                return {'type':'post','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'content':random.choice(txts),'influence':inf,'engagement':0}
        if role in {'羊毛头号','羊毛普通'}:
            mult = 2.0 if role=='羊毛头号' else 1.5
            if random.random() < min(prob*mult*(1+sb), 0.99):
                qty = random.choices([1,2],[0.75,0.25])[0]
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':qty,'trigger':'羊毛党'}
        elif role in {'随大流强','随大流弱'}:
            sig = min(len(self.orders)/30,1.0) if role=='随大流强' else min(len(self.orders)/50,1.0)
            if random.random() < min(base+sig*0.5+herd*1.5+sb, 0.95):
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':1,'trigger':'随大流'}
        elif role in {'宝妈精准','银发精准','白领精准'}:
            if random.random() < min(prob*1.1+sb*0.5, 0.9):
                qty = random.choices([1,2],[0.6,0.4])[0]
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':qty,'trigger':'精准'}
        elif role in {'复购满意','复购一般'}:
            b = 0.92 if role=='复购满意' else 0.6
            if random.random() < min(b*(1+sb*0.5), 0.95):
                qty = random.choices([1,2],[0.5,0.5])[0]
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':qty,'trigger':'复购'}
        elif role == '批量采购':
            if random.random() < min(prob*1.5+sb, 0.9):
                qty = random.choices([3,5,10],[0.3,0.4,0.3])[0]
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':qty,'trigger':'批量'}
        elif role == '新客首单':
            if random.random() < min(prob+sb, 0.7):
                return {'type':'order','agent_id':profile['agent_id'],'agent_name':profile['name'],
                    'role':role,'quantity':1,'trigger':'新客'}
        return None

    def boost(self):
        oid = {o['agent_id'] for o in self.orders}
        for post in self.posts:
            post['engagement'] += sum(1 for o in oid if o in self.follow_graph.get(post['agent_id'], set()))

    def run_round(self, rnd):
        sp = self.stock/self.total_stock

    def run_round(self, rnd):
        sp = self.stock / self.total_stock
        rec = {'round':rnd,'stock_start':self.stock,'sp_start':round(sp*100,1),
               'posts':[],'orders':[],'shares':[],'new_aware':0,'total_aware':sum(self.awareness)}
        new = self._spread(rnd); rec['new_aware'] = len(new)
        PRIORITY = {'批量采购':0,'羊毛头号':1,'羊毛普通':2,'宝妈精准':3,'银发精准':4,'白领精准':5,'复购满意':6,'复购一般':7,'新客首单':8,'随大流强':9,'随大流弱':10}
        actions = []; random.shuffle(self.profiles)
        for p in self.profiles:
            if not self.awareness[p['agent_id']]: continue
            a = self._decide(p, rnd, sp)
            if a: actions.append((p, a))
        stock_left = self.stock
        for p, a in sorted(actions, key=lambda x: PRIORITY.get(x[0]['role_type'],99)):
            if a['type'] == 'post':
                self.posts.append({**a,'round':rnd}); rec['posts'].append(a)
            elif a['type'] == 'order':
                qty = min(a.get('quantity',1), stock_left)
                if qty > 0 and not self.ordered[p['agent_id']]:
                    self.ordered[p['agent_id']] = True; stock_left -= qty
                    orec = {'round':rnd,'agent_id':p['agent_id'],'agent_name':a['agent_name'],'role':a['role'],'quantity':qty,'trigger':a.get('trigger','')}
                    self.orders.append(orec); rec['orders'].append(orec)
                    if random.random() < 0.2:
                        s = {'round':rnd,'agent_id':p['agent_id'],'agent_name':a['agent_name'],'role':a['role']}
                        self.shares.append(s); rec['shares'].append(p['agent_id'])
        self.stock = stock_left; self.boost()
        rec['stock_end'] = max(0, self.stock); rec['depleted'] = self.stock <= 0
        self.round_records.append(rec); return rec

    def run(self):
        print(f"[促销v3] {self.n}人 · 库存{self.total_stock}份 · {self.n_rounds}轮 · K={self.viral_k} · ¥{self.promo_price}/原价¥{self.original_price}")
        print(f"[促销v3] 种子KOC发帖：{len([p for p in self.posts if p['round']==0])}条\n")
        for r in range(1, self.n_rounds+1):
            rec = self.run_round(r)
            print(f"[促销v3] R{r}/{self.n_rounds} | 新+{rec['new_aware']} | 订单{len(rec['orders'])}单(剩{rec['stock_end']}份) | 发帖{len(rec['posts']}条}" + (" ← 库存耗尽！" if rec['depleted'] else ""))
            if rec['depleted']: break
        return self._build_result()

    def _build_result(self):
        total_sold = sum(o.get('quantity',1) for o in self.orders)
        sim_rate = total_sold / self.n
        real_est = int(sim_rate * self.n * 8)
        stock = self.total_stock
        sub = self.original_price - self.promo_price
        pess = min(int(real_est*0.5), stock)
        neut = min(int(real_est*0.8), stock)
        opt = min(int(real_est*1.2), stock)
        return {
            'type':'promo', 'seed':self.seed, 'n_agents':self.n, 'total_stock':stock,
            'total_sold':total_sold, 'viral_k':self.viral_k,
            'original_price':self.original_price, 'promo_price':self.promo_price,
            'promo_hours':self.promo_hours, 'n_rounds':self.n_rounds,
            'posts':self.posts, 'orders':self.orders, 'shares':self.shares,
            'round_records':self.round_records,
            'stock_depleted_round':next((r['round'] for r in self.round_records if r['depleted']),None),
            'profiles':self.profiles,
            'projection':{'pess':pess,'neut':neut,'opt':opt,'pess_loss':round(pess*sub),'neut_loss':round(neut*sub),'opt_loss':round(opt*sub),'sub':sub,'real_reach':self.n*8}
        }

# ═══════════════════════════════════════════════════════
#  分析报告生成
# ═══════════════════════════════════════════════════════
def analyze_promo_v3(result):
    orders, posts = result['orders'], result['posts']
    recs = result['round_records']
    n, stock = result['n_agents'], result['total_stock']
    p = result['projection']
    r_orders = Counter(o['role'] for o in orders)
    by_r = Counter(r['round'] for r in recs)
    total_sold = result['total_sold']
    depleted = result.get('stock_depleted_round') is not None
    herd_r = None; prev = 0
    for rr in recs:
        cur = by_r.get(rr['round'],0)
        if prev > 20 and cur > prev*1.3: herd_r = rr['round']; break
        prev = cur
    recs_out = []
    koc_p = Counter(p['role'] for p in posts).get('头部KOC',0)+Counter(p['role'] for p in posts).get('腰部KOC',0)
    wool = r_orders.get('羊毛头号',0)+r_orders.get('羊毛普通',0)
    crowd = r_orders.get('随大流强',0)
    batch = r_orders.get('批量采购',0)
    if koc_p < 50: recs_out.append({"p":"高","issue":f"KOC发帖不足({koc_p}条)","action":"私聊5位头部KOC发样品"})
    if wool < 100: recs_out.append({"p":"中","issue":f"羊毛党激活不足({wool}人)","action":"在返利群定向投放"})
    if herd_r: recs_out.append({"p":"高","issue":f"羊群效应R{herd_r}触发","action":"触发前追加投放，触发后控成本"})
    if depleted: recs_out.append({"p":"高","issue":"库存提前耗尽！","action":"立即补货或推预售锁客"})
    elif p['neut'] < stock*0.4: recs_out.append({"p":"中","issue":"库存大量剩余","action":"延长时间或加大投放"})
    if result['viral_k'] > 1: recs_out.append({"p":"高","issue":f"传播系数K={result['viral_k']}>1，病毒传播临界点已过","action":"追加库存迎接爆发"})
    top5 = sorted(posts, key=lambda x: x.get('engagement',0), reverse=True)[:5]
    return {
        'scenario': result['seed'], 'type':'promo', 'n_agents': n,
        'metrics': {'total_orders':len(orders),'total_sold':total_sold,'total_posts':len(posts),'unique_buyers':len({o['agent_id'] for o in orders}),'awareness_rate':round(recs[-1]['total_aware']/n*100,1) if recs else 0,'viral_k':result['viral_k'],'price_ratio':f"{result['promo_price']/result['original_price']*100:.0f}%"},
        'projection': p,
        'transmission': {'by_round':dict(sorted(by_r.items())),'herd':herd_r,'peak':by_r.most_common(1)[0][0] if by_r else 0,'depleted':depleted,'stock_depleted_round':result.get('stock_depleted_round'),'top5':[{"agent":x['agent_name'],"role":x['role'],"content":x.get('content','')[:60],"eng":x.get('engagement',0)} for x in top5]},
        'roles': {'buy_top5':r_orders.most_common(5),'post_top5':Counter(p['role'] for p in posts).most_common(5)},
        'risks': {'stockout':"高" if depleted else ("中" if p['neut']>=stock*0.8 else "低"),'koc_p':koc_p,'wool':wool,'crowd':crowd,'batch':batch},
        'recommendations': recs_out
    }

def analyze_crisis_v3(result):
    recs = result['round_records']
    neg, pos = result['neg_posts'], result['pos_posts']
    shares, reports, media = result['shares'], result['reports'], result['media']
    team_actions = result.get('response_team_actions',[])
    n = result['n_agents']
    total = len(neg)+len(pos)
    neg_pct = len(neg)/total if total>0 else 0
    pol = abs(neg_pct-0.5)*2
    peak_r = result.get('peak_crisis_round',0)
    peak_s = result.get('peak_crisis_score',0)
    phase = "快速扩散期" if peak_s>60 else ("峰值期" if peak_s>40 else "初期")
    aware_rates = [(r['round'],r['hours'],r['crisis_score'],r['neg_total'],r['pos_total']) for r in recs]
    top5 = sorted(neg, key=lambda x: x.get('reach',0), reverse=True)[:5]
    interventions = [a for a in team_actions if a['round']==peak_r] if team_actions else []
    risks = {"level":"极高" if peak_s>80 else ("高" if peak_s>60 else "中"),"peak_score":round(peak_s,1),"reports":len(reports),"media":len(media),"competitor_steals":sum(1 for s in shares if s.get('type')=='competitor_steal'),"intervention_effect":len(team_actions)}
    recs_out = []
    if peak_s > 60: recs_out.append({"phase":"扩散期(6-24h)","p":"高","issue":"舆情快速扩散","action":"CEO道歉+第三方检测介入+媒体沟通"})
    if peak_s > 80: recs_out.append({"phase":"峰值期(24-48h)","p":"高","issue":"舆情达峰值","action":"每日2次官方通报+补偿方案+投诉专线"})
    competitor_hits = sum(1 for s in shares if s.get('type')=='competitor_steal')
    if competitor_hits > 0: recs_out.append({"phase":"全阶段","p":"高","issue":f"竞品趁机抢客{competitor_hits}次","action":"老客户专属补偿，防止流失"})
    if team_actions: recs_out.append({"phase":f"响应小组已行动{len(team_actions)}次","p":"中","issue":"干预有效","action":"继续执行预案，保持每日通报"})
    return {
        'scenario': result['crisis'], 'type':'crisis', 'n_agents': n, 'hours': result['hours'],
        'metrics': {'total_posts':len(neg)+len(pos),'neg_posts':len(neg),'pos_posts':len(pos),'shares':len(shares),'reports':len(reports),'media':len(media),'aware_rate':round(recs[-1]['total_aware']/n*100,1) if recs else 0,'neg_pct':round(neg_pct*100,1),'polarization':round(pol,2),'intervention_rounds':result.get('intervention_rounds',0),'response_team_actions':len(team_actions)},
        'crisis_curve': {'peak_round':peak_r,'peak_score':round(peak_s,1),'phase':phase,'timeline':aware_rates,'response_timeline':[(a['round'],a['who'],a['effect']) for a in team_actions]},
        'roles': {'neg_posts_by_role':dict(Counter(p['role'] for p in neg).most_common(8)),'pos_posts_by_role':dict(Counter(p['role'] for p in pos).most_common(5)),'top5':[{"agent":x['agent_name'],"role":x['role'],"content":x['content'][:60],"reach":x.get('reach',0)} for x in top5]},
        'risks': risks,
        'recommendations': recs_out
    }

def print_report(a):
    t = a['type']
    if t == 'promo':
        m, p, tr, r = a['metrics'], a['projection'], a['transmission'], a['risks']
        print(f"""
═══════════════════════════════════════════════════════════
  七政-OASIS v3 · 爆款促销推演（传播系数K版）
  场景：{a['scenario']}
  {datetime.now().strftime('%Y-%m-%d %H:%M')}
═══════════════════════════════════════════════════════════

📊 仿真结果
  · {a['n_agents']}人 · 库存{p['pess']*8}份(外推) · K={m['viral_k']}（K>1=病毒传播临界）
  · 售出{p['pess']*8}份（去重{m['unique_buyers']}人下单）{' ← 库存耗尽' if tr['depleted'] else ''}
  · 知晓率{m['awareness_rate']}% · 价格比{m['price_ratio']}

═══════════════════════════════════════════════════════════
📦 订单量预测（触达{p['real_reach']}人）
═══════════════════════════════════════════════════════════
  悲观  {p['pess']}单  亏损¥{p['pess_loss']:.0f}
  中性  {p['neut']}单  亏损¥{p['neut_loss']:.0f}
  乐观  {p['opt']}单  亏损¥{p['opt_loss']:.0f}
  每单补贴¥{p['sub']} · 爆仓概率：{r['stockout']}

═══════════════════════════════════════════════════════════
🔥 传播分析
═══════════════════════════════════════════════════════════
  传播系数K={m['viral_k']}（{'K>1病毒传播已触发' if m['viral_k']>1 else 'K<1无病毒传播，需靠KOC推动'})
  各轮：{tr['by_round']}
  羊群R{tr['herd'] or '未'}触发 · 峰值R{tr['peak']}
  {' ← 库存R'+str(tr['stock_depleted_round'])+'耗尽' if tr['depleted'] else ''}

  热门帖子：""")
        for i,x in enumerate(tr['top5'],1): print(f"  {i}. 【{x['role']}·{x['agent']}】{x['content'][:50]}  互动+{x['eng']}")
        print(f"""
  下单：{' / '.join(f"{r[0]}({r[1]})" for r in tr['buy_top5'])}
  发帖：{' / '.join(f"{r[0]}({r[1]})" for r in tr['post_top5'])}

═══════════════════════════════════════════════════════════
⚠️ 风险
═══════════════════════════════════════════════════════════
  爆仓：{r['stockout']} | KOC发帖{r['koc_p']}条 | 羊毛党{r['wool']}人 | 随大流{r['crowd']}人 | 批量{r['batch']}人""")
        if a['recommendations']:
            print("\n💡 建议：")
            for rc in a['recommendations']: print(f"  【{rc['p']}】{rc['issue']} → {rc['action']}")

    elif t == 'crisis':
        m, cc, r = a['metrics'], a['crisis_curve'], a['risks']
        print(f"""
═══════════════════════════════════════════════════════════
  七政-OASIS v3 · 舆情危机推演（响应小组版）
  场景：{a['scenario']}
  {datetime.now().strftime('%Y-%m-%d %H:%M')}
═══════════════════════════════════════════════════════════

📊 舆情概况
  · {a['n_agents']}人 · {a['hours']}h · 响应小组行动{m['response_team_actions']}次
  · 帖子{m['total_posts']}条（负{m['neg_posts']}/正{m['pos_posts']}）
  · 转发{len(a.get('shares',[]))}次 | 投诉{m['reports']}次 | 媒体{m['media']}次
  · 知晓率{m['aware_rate']}% | 负面占比{m['neg_pct']}% | 极化指数{m['polarization']}
  · 干预有效轮次：{m['intervention_rounds']}轮

═══════════════════════════════════════════════════════════
🔥 舆情演化曲线（新华数据校准）
═══════════════════════════════════════════════════════════
  峰值：R{cc['peak_round']}（≈{cc['timeline'][-1][1] if cc['timeline'] else '?'}h） · 热度{cc['peak_score']}/100 · {cc['phase']}
  响应小组介入：{m['response_team_actions']}次""")
        if cc['response_timeline']:
            print(f"  干预时间线：{', '.join(f'R{round_}:{who}(-{eff}°)' for round_,who,eff in cc['response_timeline'])}")
        print("  各轮热度：")
        for rnd, hrs, score, neg, pos in cc['timeline']:
            bar = "█"*int(score/5)+"░"*(20-int(score/5))
            print(f"  R{rnd}(≈{hrs:2d}h) [{bar}] {score:5.1f} | 负{neg}/正{pos}")

        print(f"""
═══════════════════════════════════════════════════════════
⚠️ 危机风险：{r['level']}
═══════════════════════════════════════════════════════════
  峰值热度：{r['peak_score']}/100
  投诉举报：{r['reports']}次 | 媒体跟进：{r['media']}次
  竞品抢客：{r['competitor_steals']}次""")

        top5 = a['roles']['top5']
        if top5:
            print(f"""
═══════════════════════════════════════════════════════════
📰 高影响力负面帖子TOP5
═══════════════════════════════════════════════════════════""")
            for i, x in enumerate(top5, 1):
                print(f"  {i}. 【{x['role']}·{x['agent']}】触达{x['reach']}人")
                print(f"     {x['content']}")

        print(f"""
═══════════════════════════════════════════════════════════
🏆 舆论阵营
═══════════════════════════════════════════════════════════
  负面：{' / '.join(f"{k}({v})" for k,v in list(a['roles']['neg_posts_by_role'].items())[:5])}
  正面：{' / '.join(f"{k}({v})" for k,v in list(a['roles']['pos_posts_by_role'].items())[:5])}""")

        if a['recommendations']:
            print(f"""
═══════════════════════════════════════════════════════════
💡 分阶段应对
═══════════════════════════════════════════════════════════""")
            for rc in a['recommendations']:
                print(f"  【{rc['phase']} · {rc['p']}】{rc['issue']}")
                print(f"  → {rc['action']}")

# ═══════════════════════════════════════════════════════
#  主程序
# ═══════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['promo','crisis'], required=True, help='promo=爆款促销 | crisis=舆情危机')
    ap.add_argument('--scenario', default='成山农场蓝莓9.9元/斤爆款')
    ap.add_argument('--n_agents', type=int, default=1000)
    ap.add_argument('--stock', type=int, default=500)
    ap.add_argument('--hours', type=int, default=24)
    ap.add_argument('--rounds', type=int, default=4)
    ap.add_argument('--original_price', type=float, default=26.0)
    ap.add_argument('--promo_price', type=float, default=9.9)
    ap.add_argument('--product_type', default='水果/生鲜')
    ap.add_argument('--enable_response_team', type=lambda x: x.lower()=='true', default=True)
    ap.add_argument('--output', default='/workspace/data/qizheng-oasis/result_v3.json')
    args = ap.parse_args()
    os.makedirs('/workspace/data/qizheng-oasis', exist_ok=True)

    if args.mode == 'promo':
        print(f"[天枢v3] 生成{args.n_agents}个角色...")
        profiles = make_promo_profiles(args.n_agents)
        print(f"[天权v3] 运行爆款促销推演...")
        world = PromoWorldV3(profiles, args.scenario, args.stock, args.hours, args.rounds, args.original_price, args.promo_price, args.product_type)
        result = world.run()
        a = analyze_promo_v3(result)
    else:
        print(f"[天枢v3] 生成{args.n_agents}个舆情角色...")
        profiles = make_crisis_profiles(args.n_agents)
        print(f"[天权v3] 运行舆情危机推演（响应小组{'ON' if args.enable_response_team else 'OFF'}）...")
        world = CrisisWorldV3(profiles, args.scenario, args.hours, args.rounds, args.enable_response_team)
        result = world.run()
        a = analyze_crisis_v3(result)

    with open(args.output,'w',encoding='utf-8') as f:
        json.dump(result if 'result' in dir() else {}, f, ensure_ascii=False, indent=2)

    print(f"\n[天玑v3] 分析报告：")
    print_report(a)

    json_out = args.output.replace('.json','_analysis.json')
    with open(json_out,'w',encoding='utf-8') as f:
        json.dump(a, f, ensure_ascii=False, indent=2)
    print(f"\n[完成] {args.output}")

if __name__ == '__main__':
    main()
