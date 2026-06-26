#!/usr/bin/env python3
"""
七政-OASIS · 舆情危机推演模块
场景切换：食品安全事件 → 舆论演化
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

# ── 舆情危机角色分型（与促销不同）─────────────────────
CRISIS_BPS = [
    {"role":"曝光博主",      "count":30,  "inf":2.5,"prob":0.95,"crisis_type":"amplifier",
     "mbti":["ENTP","ENFP","ESTP"],"triggers":["食品安全","企业黑幕","必须曝光"],
     "barriers":["证据不足","怕惹麻烦"],"action":"发帖曝光"},
    {"role":"跟风转发",      "count":120,"inf":1.2,"prob":0.80,"crisis_type":"amplifier",
     "mbti":["ESFP","ENFP","ESTJ"],"triggers":["食品安全","转发出风头","凑热闹"],
     "barriers":["不确定真假"],"action":"转发扩散"},
    {"role":"愤怒声讨",      "count":100,"inf":1.0,"prob":0.90,"crisis_type":"amplifier",
     "mbti":["ENFJ","ESFJ","ESTJ"],"triggers":["食品安全","伤害消费者","必须追责"],
     "barriers":["情绪化","不理性"],"action":"发帖声讨"},
    {"role":"理性分析",      "count":80, "inf":0.8,"prob":0.60,"crisis_type":"neutral",
     "mbti":["INTJ","INTP","ISTJ"],"triggers":["等官方通报","看证据","不信谣"],
     "barriers":["信息不足","等待更多证据"],"action":"理性观望"},
    {"role":"沉默大多数",    "count":150,"inf":0.1,"prob":0.15,"crisis_type":"neutral",
     "mbti":["ISFJ","ISTP","INTP"],"triggers":["不关心","不发言"],
     "barriers":["不感兴趣"],"action":"沉默"},
    {"role":"忠诚辩护",      "count":60, "inf":1.5,"prob":0.85,"crisis_type":"defender",
     "mbti":["ISFJ","ESFJ","ISTJ"],"triggers":["成山老客户","相信成山","维护品牌"],
     "barriers":["证据确凿时放弃"],"action":"发帖辩护"},
    {"role":"竞争对手推波",  "count":20, "inf":1.8,"prob":0.90,"crisis_type":"opponent",
     "mbti":["ENTJ","INTJ","ESTP"],"triggers":["抢夺市场","落井下石","打击对手"],
     "barriers":["不违法"],"action":"扩散丑闻"},
    {"role":"专业投诉",      "count":40, "inf":1.2,"prob":0.75,"crisis_type":"victim",
     "mbti":["ISTJ","INTJ","ESTJ"],"triggers":["受害者","依法维权","索赔"],
     "barriers":["维权成本高"],"action":"投诉举报"},
    {"role":"媒体跟进",      "count":30, "inf":2.0,"prob":0.80,"crisis_type":"media",
     "mbti":["ENFJ","ENTP","INTJ"],"triggers":["新闻价值","读者关注","流量"],
     "barriers":["事实核查"],"action":"媒体报道"},
    {"role":"监管介入",      "count":10, "inf":1.5,"prob":0.70,"crisis_type":"authority",
     "mbti":["ISTJ","ESTJ","INTJ"],"triggers":["食品安全法","执法","政府介入"],
     "barriers":["程序复杂"],"action":"执法检查"},
    {"role":"水军洗地",      "count":40, "inf":0.5,"prob":0.60,"crisis_type":"defender",
     "mbti":["ISTP","ISFP"],"triggers":["收钱办事","维护雇主","降低热度"],
     "barriers":["被识破"],"action":"水军洗地"},
    {"role":"竞品受益者",   "count":20, "inf":0.9,"prob":0.80,"crisis_type":"opponent",
     "mbti":["ENTJ","ESTP","INTJ"],"triggers":["抢客户","渔翁得利","替代品牌机会"],
     "barriers":["不确定"],"action":"抢成山客户"},
    {"role":"观望纠结",      "count":100,"inf":0.3,"prob":0.30,"crisis_type":"neutral",
     "mbti":["INFP","ISFJ","INTP"],"triggers":["不确定真假","两边都有道理"],
     "barriers":["证据不充分","等官方"],"action":"犹豫观望"},
    {"role":"完全无视",      "count":200,"inf":0.05,"prob":0.02,"crisis_type":"ignore",
     "mbti":["ISTP","ISFP"],"triggers":["与自己无关","不关心农业话题"],
     "barriers":["完全不感兴趣"],"action":"无视"},
]

BG_CRISIS = {
    "曝光博主":     ["食品安全记者","打假博主20万粉","朋友圈记者","媒体从业者"],
    "跟风转发":     ["普通网民","爱凑热闹","朋友圈活跃用户","社区群友"],
    "愤怒声讨":     ["孩子家长","消费者代表","愤怒的买家","正义感爆棚的网友"],
    "理性分析":     ["食品安全专家","学术圈人士","律师","专业人士"],
    "沉默大多数":   ["普通路人","不关心食品安全的网民","学生","上班族"],
    "忠诚辩护":     ["成山老客户5年以上","成山会员","买了成山产品的人","亲戚朋友"],
    "竞争对手推波": ["同类农场主","生鲜平台运营","竞争品牌员工"],
    "专业投诉":     ["消费者维权律师","有投诉经验者","有医学背景者","退休干部"],
    "媒体跟进":     ["本地电视台记者","公众号写手","微博大V","抖音博主"],
    "监管介入":     ["食药监局官员","市场监督局","地方政府","行业协会"],
    "水军洗地":     ["公关公司水军","成山员工","利益相关方"],
    "竞品受益者":   ["替代品牌销售","超市采购","有机食品店","同类农场"],
    "观望纠结":     ["中间派网民","普通消费者","谨慎型买家"],
    "完全无视":     ["海外华人","极简主义者","对农业完全不感兴趣"],
}

def gen_name():
    s1 = random.choice(["小","阿","老","大"] + list("赵钱孙李周吴郑王冯陈褚卫"))
    s2 = random.choice("林丽华敏静强磊洋勇艳军波飞霞梅兰菊桃桂")
    return f"{s1}{s2}{random.randint(10,99)}"

def make_profiles(n: int) -> list:
    total = sum(bp['count'] for bp in CRISIS_BPS)
    scale = n / total
    out = []
    idx = 0
    for bp in CRISIS_BPS:
        cnt = max(1, int(bp['count'] * scale))
        bgs = BG_CRISIS.get(bp['role'], ["普通网民"])
        for _ in range(cnt):
            out.append({
                "agent_id": idx,
                "role_type": bp['role'],
                "crisis_type": bp['crisis_type'],
                "action": bp['action'],
                "name": gen_name(),
                "age": random.choices([22,28,35,40,45,50,55,60],[0.1,0.15,0.2,0.15,0.15,0.1,0.08,0.07])[0],
                "gender": random.choice(["男","女"]),
                "mbti": random.choice(bp['mbti']),
                "trigger_words": bp['triggers'],
                "barrier_words": bp['barriers'],
                "influence_score": round(bp['inf'] * random.uniform(0.8, 1.2), 2),
                "action_prob": round(min(bp['prob'] * random.uniform(0.85, 1.1), 1.0), 2),
                "joined_round": 0,
            })
            idx += 1
    random.shuffle(out)
    for i, p in enumerate(out): p['agent_id'] = i
    return out[:n]

# ── 舆情危机世界 ──────────────────────────────────────
# ── 舆情衰减曲线（新华舆情平台校准）────────────────
DECAY = [(0,1.0),(2,0.98),(4,0.90),(6,0.85),(12,0.70),(24,0.60),(36,0.50),(48,0.40),(72,0.28),(96,0.18),(120,0.12)]
def get_decay(hours, interv):
    base = 1.0
    for h, d in DECAY:
        if hours <= h: base = d; break
    bonus = max(0.4, 1.0 - interv * 0.03)
    return base * bonus

# ── 危机响应小组（ClawTeam swarm）────────────────────
RESPONSE_TEAM = [
    {"name":"CEO紧急响应","role":"决策者","prob":0.9,"delay":1,"effect":8,"ne":0.05,"desc":"30分钟内发官方声明，道歉+召回+补偿","cd":3},
    {"name":"公关部","role":"舆论管控","prob":0.85,"delay":1,"effect":6,"ne":0.04,"desc":"发布正面通稿，联系媒体","cd":2},
    {"name":"法务部","role":"法律应对","prob":0.7,"delay":2,"effect":4,"ne":0.02,"desc":"发律师函，证据保全","cd":4},
    {"name":"客服部","role":"客户安抚","prob":0.9,"delay":1,"effect":5,"ne":0.06,"desc":"一对一联系老客户，专线受理投诉","cd":1},
    {"name":"运营部","role":"促销对冲","prob":0.75,"delay":2,"effect":4,"ne":0.03,"desc":"推出老客户专属优惠，对冲竞品抢客","cd":3},
    {"name":"品控部","role":"质量溯源","prob":0.65,"delay":2,"effect":3,"ne":0.02,"desc":"配合第三方检测，出具质检报告","cd":5},
]

class CrisisWorld:
    """
    舆情演化三层模型：
    Micro：个体情绪 + 行动概率
    Meso：社交网络扩散 + 立场阵营
    Macro：舆论峰值 + 极化指数 + 危机阶段

    危机阶段：爆发期(0-6h) → 扩散期(6-24h) → 峰值期(24-48h) → 消退期(48h+)
    """

    def __init__(self, profiles, crisis_desc, hours=48, rounds=6):
        self.profiles = profiles
        self.crisis = crisis_desc
        self.n = len(profiles)
        self.hours = hours
        self.n_rounds = rounds
        self.round_hours = hours / rounds  # 每轮多少小时

        self.awareness = [False] * self.n
        self.posts = []
        self.negative_posts = []   # 负面帖
        self.positive_posts = []    # 辩护帖
        self.shares = []
        self.orders_lost = []       # 因危机流失的订单
        self.reports = []          # 投诉/举报
        self.media_mentions = []   # 媒体报道
        self.round_records = []
        self.crisis_score = 0.0
        self.response_actions = []
        self.intervention_rounds = 0
        self.enable_response_team = True     # 舆情热度（0~100）

        self._build_graph()
        # 初始曝光者（曝光博主 + 媒体 + 专业投诉）
        for i, p in enumerate(profiles):
            if p['crisis_type'] in {'amplifier','media','victim','authority'} and p['action_prob'] > 0.6:
                self.awareness[i] = True
                p['joined_round'] = 0
                self._emit_post(p, 0, 'negative')

    def _build_graph(self):
        self.follow_graph = defaultdict(set)
        ri = defaultdict(list)
        for i, p in enumerate(self.profiles): ri[p['role_type']].append(i)

        # 所有人都follow曝光博主
        for role in ['曝光博主','媒体跟进','愤怒声讨']:
            infl = set(ri.get(role, []))
            for j in range(self.n):
                for k in infl:
                    if k != j: self.follow_graph[j].add(k)

        # 忠诚辩护圈互关
        defenders = set(ri.get('忠诚辩护', []))
        for a in defenders:
            for b in defenders:
                if a != b: self.follow_graph[a].add(b)

        # 跟风转发者follow曝光博主 + 愤怒声讨
        for role in ['跟风转发','愤怒声讨']:
            for j in ri.get(role, []):
                for k in set(ri.get('曝光博主',[])) | set(ri.get('愤怒声讨',[])):
                    if random.random() < 0.6: self.follow_graph[j].add(k)

        # 竞争对手follow监管 + 媒体
        for j in ri.get('竞争对手推波', []):
            for k in set(ri.get('监管介入',[])) | set(ri.get('媒体跟进',[])):
                self.follow_graph[j].add(k)

    def _emit_post(self, profile, rnd, sentiment):
        content_templates = {
            'negative': [
                f"【重大爆料】{self.crisis}",
                f"【食品安全】{self.crisis}，大家注意！",
                f"【必须曝光】{self.crisis}",
                f"【消费者警示】{self.crisis}",
            ],
            'defensive': [
                f"【理性看待】{self.crisis}，成山农场一直品质可靠，不要信谣传谣",
                f"【老客户声明】我买了成山很多年，从没出过问题，这次不排除被黑了",
                f"支持成山！等官方通报，不要急于下结论",
            ],
            'amplifier': [
                f"转！{self.crisis}",
                f"大家都在传，{self.crisis}",
                f"【必须转发】{self.crisis}",
            ]
        }
        templates = content_templates.get(sentiment, content_templates['negative'])
        content = random.choice(templates)

        post = {
            'round': rnd,
            'agent_id': profile['agent_id'],
            'agent_name': profile['name'],
            'role': profile['role_type'],
            'crisis_type': profile['crisis_type'],
            'sentiment': sentiment,
            'content': content,
            'influence': profile['influence_score'],
            'reach': 0,   # 触达人数
            'shares': 0,  # 转发数
            'likes': 0,   # 点赞数
            'angry': 0,   # 愤怒反应
        }
        self.posts.append(post)
        if sentiment == 'negative':
            self.negative_posts.append(post)
        elif sentiment in ('defensive', 'positive'):
            self.positive_posts.append(post)
        return post

    def _spread(self, rnd):
        newly = set()
        rp = {p['agent_id'] for p in self.posts if p['round'] == rnd - 1}
        # 曝光帖触达的人
        neg_rp = {p['agent_id'] for p in self.negative_posts if p['round'] == rnd - 1}

        for i in range(self.n):
            if self.awareness[i]: continue
            followers = self.follow_graph.get(i, set())
            if followers & rp:
                newly.add(i)
            # 算法推荐：负面帖子有更高的算法推送概率
            elif neg_rp and random.random() < 0.15:
                newly.add(i)

        for i in newly:
            self.awareness[i] = True
            self.profiles[i]['joined_round'] = rnd
        return list(newly)

    def _run_response_team(self, rnd):
        if not getattr(self, 'enable_response_team', True): return []
        taken = []
        for m in RESPONSE_TEAM:
            if rnd < m['delay']: continue
            recent = [a for a in self.response_actions if a['who'] == m['name']]
            if recent and (rnd - recent[-1]['rnd']) < m['cd']: continue
            if random.random() < m['prob']:
                self.intervention_rounds += 1
                self.crisis_score = max(0, self.crisis_score - m['effect'])
                a = {'rnd': rnd, 'who': m['name'], 'role': m['role'],
                     'effect': m['effect'], 'desc': m['desc'],
                     'score_after': round(self.crisis_score, 1)}
                self.response_actions.append(a); taken.append(m['name'])
                if random.random() < 0.5:
                    fp = {'agent_id': 9999, 'name': m['name'], 'role_type': m['name'],
                          'crisis_type': 'defender', 'influence_score': 1.5}
                    self._emit_post(fp, rnd, 'defensive')
        return taken

    def _decide(self, profile, rnd, crisis_score, neg_pct):
        """舆情危机下的个体决策"""
        role = profile['role_type']
        ct = profile['crisis_type']
        base = profile['action_prob']
        seed = self.crisis

        # 危机时间因子：爆发期强扩散，消退期弱
        hours_now = rnd * self.round_hours
        if hours_now <= 6:   time_factor = 1.3   # 爆发期
        elif hours_now <= 24: time_factor = 1.0  # 扩散期
        elif hours_now <= 48: time_factor = 0.7  # 峰值期
        else:                time_factor = 0.4   # 消退期

        # 热度因子：危机分数越高，行动概率越高
        heat_factor = crisis_score / 100 * 0.3

        prob = min(base * time_factor * (1 + heat_factor), 0.99)

        # ── 曝光博主：发帖曝光 ─────────────────────
        if ct == 'amplifier':
            if random.random() < prob:
                # 发帖后可能追加转发
                posts_out = [{'type':'post','sentiment':'negative'}]
                if random.random() < 0.4:
                    posts_out.append({'type':'share','sentiment':'negative'})
                return posts_out

        # ── 愤怒声讨：情绪化跟进 ──────────────────
        elif ct == 'amplifier' and role == '愤怒声讨':
            if random.random() < min(prob * 1.2, 0.95):
                return [{'type':'post','sentiment':'negative'}]

        # ── 跟风转发：二次扩散 ─────────────────────
        elif role in {'跟风转发','观望纠结'}:
            if ct == 'neutral' and role == '跟风转发':
                if random.random() < min(prob * 1.1, 0.9):
                    return [{'type':'share','sentiment':'negative'}]
            elif ct == 'neutral' and role == '观望纠结':
                # 负面帖子超过正面帖子时，观望纠结者会偏向负面
                neg_bias = max(0, neg_pct - 0.5) * 2
                if random.random() < min(prob * (0.5 + neg_bias), 0.8):
                    return [{'type':'share','sentiment':'negative'}]

        # ── 忠诚辩护：发正面帖 ─────────────────────
        elif ct == 'defender':
            if random.random() < prob:
                return [{'type':'post','sentiment':'defensive'}]
            # 辩护者也可能在证据确凿时转为沉默
            if crisis_score > 80 and random.random() < 0.3:
                return [{'type':'silent','reason':'证据太多'}]

        # ── 水军洗地：发正面稀释 ───────────────────
        elif role == '水军洗地':
            if crisis_score > 20 and random.random() < min(prob, 0.7):
                return [{'type':'post','sentiment':'defensive'}]

        # ── 专业投诉 ─────────────────────────────
        elif ct == 'victim':
            if random.random() < prob:
                return [{'type':'report','sentiment':'negative'}]

        # ── 竞争对手推波 ──────────────────────────
        elif ct == 'opponent':
            if random.random() < min(prob * 1.2, 0.9):
                return [{'type':'post','sentiment':'negative'}, {'type':'exploit','sentiment':'negative'}]

        # ── 媒体跟进 ─────────────────────────────
        elif role == '媒体跟进':
            if random.random() < min(prob * 0.8, 0.75):
                return [{'type':'media','sentiment':'negative'}]

        # ── 监管介入 ──────────────────────────────
        elif ct == 'authority':
            if crisis_score > 40 and random.random() < min(prob * 0.6, 0.6):
                return [{'type':'investigate','sentiment':'negative'}]

        # ── 沉默大多数 / 完全无视 ─────────────────
        # 不行动

        return None

    def _update_crisis_score(self, rnd):
        """宏观涌现：更新舆情热度"""
        neg = len(self.negative_posts)
        pos = len(self.positive_posts)
        shares = len(self.shares)
        reports = len(self.reports)
        hours_now = rnd * self.round_hours

        # 基础分：帖子量
        base = neg * 2 + shares * 1 + reports * 3
        # 辩护稀释
        dilution = max(0, pos * 1.5)
        # 时间衰减（越往后越难维持热度）
        if hours_now <= 6:   decay = 1.0
        elif hours_now <= 24: decay = 0.9
        elif hours_now <= 48: decay = 0.7
        else:                decay = 0.4

        raw = (base - dilution) * decay
        # 监管介入可加速危机消退
        if len(self.reports) > 10: raw *= 1.2  # 监管介入反而推高热度
        self.crisis_score = max(0, min(100, raw))

    def _get_neg_pct(self):
        total = len(self.negative_posts) + len(self.positive_posts)
        if total == 0: return 0.5
        return len(self.negative_posts) / total

    def run_round(self, rnd):
        rec = {
            'round': rnd,
            'hours': int(rnd * self.round_hours),
            'new_aware': 0,
            'posts': [], 'shares': [], 'reports': [],
            'media': [], 'investigations': [],
            'crisis_score': 0.0,
            'neg_posts_total': 0,
            'pos_posts_total': 0,
        }

        new = self._spread(rnd)
        rec['new_aware'] = len(new)
        self._update_crisis_score(rnd)
        rec['crisis_score'] = round(self.crisis_score, 1)
        rec['intervention_rounds'] = self.intervention_rounds
        neg_pct = self._get_neg_pct()
        ta = self._run_response_team(rnd)
        rec['response_team'] = ta
        if ta:
            print('[响应小组] R%d行动: %s' % (rnd, ', '.join(ta)))

        random.shuffle(self.profiles)
        for p in self.profiles:
            if not self.awareness[p['agent_id']]: continue
            actions = self._decide(p, rnd, self.crisis_score, neg_pct)
            if not actions: continue
            if isinstance(actions, dict): actions = [actions]

            for act in actions:
                t = act.get('type', 'post')
                s = act.get('sentiment', 'neutral')

                if t == 'post':
                    post = self._emit_post(p, rnd, s)
                    post['reach'] = int(p['influence_score'] * random.randint(50, 300))
                    rec['posts'].append(post)

                elif t == 'share':
                    self.shares.append({
                        'round': rnd, 'agent_id': p['agent_id'],
                        'agent_name': p['name'], 'role': p['role_type'],
                        'sentiment': s,
                        'reach': int(p['influence_score'] * random.randint(20, 100))
                    })
                    rec['shares'].append({'agent': p['name'], 'role': p['role_type']})

                elif t == 'report':
                    self.reports.append({
                        'round': rnd, 'agent_id': p['agent_id'],
                        'agent_name': p['name'], 'role': p['role_type']
                    })
                    rec['reports'].append({'agent': p['name'], 'role': p['role_type']})

                elif t == 'media':
                    self.media_mentions.append({
                        'round': rnd, 'agent_name': p['name'], 'role': p['role_type'],
                        'influence': p['influence_score']
                    })
                    rec['media'].append({'agent': p['name'], 'influence': p['influence_score']})

                elif t == 'investigate':
                    rec['investigations'].append({'agent': p['name'], 'role': p['role_type']})

                elif t == 'exploit':
                    # 竞品趁机抢客
                    self.shares.append({
                        'round': rnd, 'agent_id': p['agent_id'],
                        'agent_name': p['name'], 'role': p['role_type'],
                        'type': 'competitor_steal',
                        'reach': int(p['influence_score'] * random.randint(100, 500))
                    })

        rec['neg_posts_total'] = len(self.negative_posts)
        rec['pos_posts_total'] = len(self.positive_posts)
        rec['total_aware'] = sum(self.awareness)
        self.round_records.append(rec)
        return rec

    def run(self):
        print(f"[舆情危机] 启动：{self.n}人 · {self.hours}h · {self.n_rounds}轮")
        print(f"[舆情危机] 初始曝光帖：{len([p for p in self.posts if p['round']==0])}条\n")

        for r in range(1, self.n_rounds+1):
            rec = self.run_round(r)
            print(f"[舆情危机] R{r}/{self.n_rounds} "
                  f"(≈{rec['hours']}h) | "
                  f"新+{rec['new_aware']} | "
                  f"发帖{len(rec['posts'])}条(负{self._count_neg_posts_r(r)}/正{self._count_pos_posts_r(r)}) | "
                  f"转发{len(rec['shares'])} | "
                  f"投诉{len(rec['reports'])} | "
                  f"舆情热度{rec['crisis_score']:.0f}/100")

        return {
            'crisis': self.crisis,
            'n_agents': self.n,
            'hours': self.hours,
            'n_rounds': self.n_rounds,
            'posts': self.posts,
            'negative_posts': self.negative_posts,
            'positive_posts': self.positive_posts,
            'shares': self.shares,
            'reports': self.reports,
            'media_mentions': self.media_mentions,
            'round_records': self.round_records,
            'profiles': self.profiles,
            'peak_crisis_round': max(self.round_records, key=lambda r: r['crisis_score'])['round'] if self.round_records else 0,
            'peak_crisis_score': max(r['crisis_score'] for r in self.round_records) if self.round_records else 0,
        }

    def _count_neg_posts_r(self, rnd):
        return len([p for p in self.negative_posts if p['round'] == rnd])
    def _count_pos_posts_r(self, rnd):
        return len([p for p in self.positive_posts if p['round'] == rnd])

# ── 分析 ────────────────────────────────────────────────
def analyze_crisis(result):
    recs = result['round_records']
    posts = result['posts']
    neg = result['negative_posts']
    pos = result['positive_posts']
    shares = result['shares']
    reports = result['reports']
    media = result['media_mentions']
    n = result['n_agents']

    # ── 时间线关键节点 ──────────────────────────────
    crisis_scores = [(r['round'], r['hours'], r['crisis_score'], r['neg_posts_total'], r['pos_posts_total']) for r in recs]
    peak_r, peak_h, peak_score, _, _ = max(crisis_scores, key=lambda x: x[2])

    # ── 阶段划分 ──────────────────────────────────
    if peak_h <= 6: peak_phase = "爆发期（0~6小时）"
    elif peak_h <= 24: peak_phase = "快速扩散期（6~24小时）"
    elif peak_h <= 48: peak_phase = "峰值期（24~48小时）"
    else: peak_phase = "长尾期（48小时+）"

    # ── 舆论极化指数 ──────────────────────────────
    total_post_sentiment = len(neg) + len(pos)
    neg_pct = len(neg) / total_post_sentiment if total_post_sentiment > 0 else 0
    polarization = abs(neg_pct - 0.5) * 2  # 0=中立, 1=完全极化

    # ── 扩散层级 ──────────────────────────────────
    aware_rounds = [(r['round'], r['new_aware'], r['total_aware']) for r in recs]

    # ── 风险评估 ──────────────────────────────────
    risk_level = "低"
    if peak_score > 60: risk_level = "中"
    if peak_score > 80: risk_level = "高"
    if len(reports) > 20: risk_level = "极高（监管介入）"
    if len(media) > 5: risk_level += "（媒体跟进）"
    team_acts_r = result.get('response_actions', [])
    if team_acts_r: risk_level += "（响应小组已行动%d次）" % len(team_acts_r)

    # ── 建议（分阶段） ────────────────────────────
    recs_out = []
    # 爆发期
    if crisis_scores[0][2] < 20:
        recs_out.append({"phase":"爆发期(0-6h)","p":"极高","issue":"危机已曝光，需立即响应",
            "action":"30分钟内发官方声明，承认问题，启动召回程序"})
    # 扩散期
    if any(r[2] > 40 for r in crisis_scores):
        recs_out.append({"phase":"扩散期(6-24h)","p":"高","issue":"舆情快速扩散",
            "action":"CEO公开道歉，第三方检测机构介入，媒体一对一沟通"})
    # 峰值期
    if peak_score > 70:
        recs_out.append({"phase":"峰值期(24-48h)","p":"高","issue":"舆情达到峰值",
            "action":"公布补偿方案，设置专线接受投诉，官方每日两次通报"})
    # 消退期
    if any(r[2] < peak_score * 0.5 for r in crisis_scores if r[0] > peak_r):
        recs_out.append({"phase":"消退期(48h+)","p":"中","issue":"舆情开始消退",
            "action":"推出新品促销修复形象，长期品牌重建计划"})
    # 竞争对手
    if any(s.get('type') == 'competitor_steal' for s in shares):
        competitor_hits = sum(1 for s in shares if s.get('type') == 'competitor_steal')
        recs_out.append({"phase":"全阶段","p":"高","issue":f"竞品趁机抢客({competitor_hits}次)",
            "action":"防止客户流失，提供老客户专属补偿"})

    return {
        "scenario": result['crisis'],
        "n_agents": n,
        "hours": result['hours'],
        "metrics": {
            "total_posts": len(posts),
            "negative_posts": len(neg),
            "positive_posts": len(pos),
            "shares": len(shares),
            "reports": len(reports),
            "media_mentions": len(media),
            "aware_rate": round(recs[-1]['total_aware']/n*100, 1) if recs else 0,
            "neg_pct": round(neg_pct*100, 1),
            "polarization_index": round(polarization, 2),
        },
        "crisis_curve": {
            "peak_round": peak_r,
            "peak_hours": peak_h,
            "peak_score": round(peak_score, 1),
            "peak_phase": peak_phase,
            "timeline": [(r['round'], r['hours'], round(r['crisis_score'],1), r['neg_posts_total'], r['pos_posts_total']) for r in recs]
        },
        "roles": {
            "neg_posts_by_role": dict(Counter(p['role'] for p in neg).most_common(8)),
            "pos_posts_by_role": dict(Counter(p['role'] for p in pos).most_common(5)),
            "top_neg_posts": sorted(neg, key=lambda p: p.get('reach',0), reverse=True)[:5],
        },
        "risks": {
            "level": risk_level,
            "peak_score": round(peak_score, 1),
            "reports_count": len(reports),
            "media_count": len(media),
            "competitor_steals": sum(1 for s in shares if s.get('type') == 'competitor_steal'),
        },
        "recommendations": recs_out
    }

def print_crisis_report(a):
    m, c, r, rc = a['metrics'], a['crisis_curve'], a['risks'], a['recommendations']
    print(f"""
═══════════════════════════════════════════════════════════
  七政-OASIS · 舆情危机推演报告
  场景：{a['scenario']}
  {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
═══════════════════════════════════════════════════════════

📊 舆情概况
  · {a['n_agents']}人模拟 · {a['hours']}小时推演
  · 总帖子{m['total_posts']}条（负面{m['negative_posts']}条/正面{m['positive_posts']}条）
  · 转发{m['shares']}次 · 投诉举报{m['reports']}次 · 媒体跟进{m['media_mentions']}次
  · 知晓率{m['aware_rate']}% · 负面占比{m['neg_pct']}% · 极化指数{m['polarization_index']}

═══════════════════════════════════════════════════════════
🔥 舆情演化曲线
═══════════════════════════════════════════════════════════

  峰值：R{c['peak_round']}（≈{c['peak_hours']}h） · 热度{c['peak_score']}/100 · {c['peak_phase']}

  各轮热度：""")
    for rnd, hrs, score, neg, pos in c['timeline']:
        bar = "█" * int(score/5) + "░" * (20 - int(score/5))
        print(f"  R{rnd}(≈{hrs:2d}h) [{bar}] {score:5.1f} | 负{neg}/正{pos}")

    print(f"""
  极化指数：{m['polarization_index']}（0=中立，1=完全极化，>0.7为严重极化）

═══════════════════════════════════════════════════════════
⚠️ 危机风险：{r['level']}
═══════════════════════════════════════════════════════════

  峰值热度：{r['peak_score']}/100
  投诉举报：{r['reports_count']}次
  媒体跟进：{r['media_count']}次
  竞品抢客：{r['competitor_steals']}次""")

    if r['media_count'] > 0:
        print(f"\n  ⚠️ 媒体已介入！需立即准备媒体沟通策略")

    top_neg = a['roles']['top_neg_posts']
    if top_neg:
        print(f"""
═══════════════════════════════════════════════════════════
📰 最高影响力负面帖子
═══════════════════════════════════════════════════════════""")
        for i, p in enumerate(top_neg, 1):
            print(f"  {i}. 【{p['role']}·{p['agent_name']}】触达{p.get('reach',0)}人")
            print(f"     {p['content'][:60]}")

    print(f"""
═══════════════════════════════════════════════════════════
🏆 舆论阵营分布
═══════════════════════════════════════════════════════════
  负面发帖TOP5：{' / '.join(f"{k}({v})" for k,v in list(a['roles']['neg_posts_by_role'].items())[:5])}
  正面发帖TOP5：{' / '.join(f"{k}({v})" for k,v in list(a['roles']['pos_posts_by_role'].items())[:5])}""")

    if rc:
        print(f"""
═══════════════════════════════════════════════════════════
💡 分阶段应对策略
═══════════════════════════════════════════════════════════""")
        for item in rc:
            print(f"  【{item['phase']} · {item['p']}】{item['issue']}")
            print(f"  → {item['action']}\n")

# ── 主程序 ──────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--crisis', default='成山农场蓝莓被检出农药残留超标')
    ap.add_argument('--n_agents', type=int, default=1000)
    ap.add_argument('--hours', type=int, default=48)
    ap.add_argument('--rounds', type=int, default=6)
    ap.add_argument('--output', default='/workspace/data/qizheng-oasis/result_crisis.json')
    args = ap.parse_args()

    os.makedirs('/workspace/data/qizheng-oasis', exist_ok=True)
    print(f"[天枢] 生成{args.n_agents}个舆情角色...")
    profiles = make_profiles(args.n_agents)

    print(f"[天权] 运行舆情危机推演...")
    world = CrisisWorld(profiles, args.crisis, args.hours, args.rounds)
    result = world.run()

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n[天玑] 分析...")
    a = analyze_crisis(result)
    print_crisis_report(a)

    with open(args.output.replace('.json','_analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(a, f, ensure_ascii=False, indent=2)
    print(f"\n[完成] {args.output}")

if __name__ == '__main__':
    main()
