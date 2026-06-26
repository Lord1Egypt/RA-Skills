#!/usr/bin/env python3
"""
七政-OASIS v3 · 报告打印 + 主程序
（直接复用 run_v3.py 中的类和函数，避免 import 问题）
"""
import sys, os, argparse, json, random
from collections import Counter, defaultdict
from datetime import datetime, timedelta as dt

# ── 从 run_v3.py 复制核心逻辑 + 修复 key 名称 ──────────────────────────

RESPONSE_TEAM = [
    {"name":"CEO紧急响应","prob":0.9,"delay":1,"effect":8,"cooldown":3,"desc":"30分钟声明，道歉+召回+补偿"},
    {"name":"公关部","prob":0.85,"delay":1,"effect":6,"cooldown":2,"desc":"正面通稿，联系媒体"},
    {"name":"客服部","prob":0.9,"delay":1,"effect":5,"cooldown":1,"desc":"一对一老客户，专线受理投诉"},
    {"name":"运营部","prob":0.75,"delay":2,"effect":4,"cooldown":3,"desc":"老客户专属优惠，防竞品抢客"},
    {"name":"法务部","prob":0.7,"delay":2,"effect":4,"cooldown":4,"desc":"律师函，证据保全"},
    {"name":"品控部","prob":0.65,"delay":2,"effect":3,"cooldown":5,"desc":"第三方检测，出具质检报告"},
]

DECAY = [(0,1.0),(2,.98),(4,.90),(6,.85),(12,.70),(24,.60),(36,.50),(48,.40),(72,.28),(96,.18),(120,.12)]

def decay_f(hours,干预):
    b = 1.0
    for h,d in DECAY:
        if hours <= h: b = d; break
    return b * max(0.4, 1.0 - 干预 * 0.03)

def vk_f(ptype, promo, orig):
    disc = promo / orig
    base = {"水果/生鲜":0.8,"食品":0.6,"日用品":0.5,"服装":0.7,"电子产品":0.4}.get(ptype, 0.5)
    mult = 2.5 if disc < 0.3 else 1.8 if disc < 0.5 else 1.3 if disc < 0.7 else 1.0
    return round(base * mult, 2)

def gen_name():
    s1 = random.choice(list("小阿老大小赵钱孙李周吴郑王冯陈褚卫"))
    s2 = random.choice(list("林丽华敏静强磊洋勇艳军波飞霞梅兰菊桃桂"))
    return s1 + s2 + str(random.randint(10,99))

viral_k = vk_f  # 别名兼容

PROMO_BPS = [
    ("头部KOC",30,2.5,0.95,2),("腰部KOC",70,1.8,0.88,1),("素人种草",100,1.2,0.75,1),
    ("宝妈精准",120,1.0,0.80,2),("银发精准",60,0.7,0.65,2),("白领精准",80,0.8,0.60,1),
    ("羊毛头号",60,1.5,0.95,2),("羊毛普通",120,0.8,0.88,1),("羊毛比价",60,0.6,0.70,0),
    ("随大流强",80,0.9,0.75,1),("随大流弱",60,0.4,0.40,0),("新客首单",80,0.5,0.55,1),
    ("复购满意",50,1.5,0.92,2),("复购一般",40,0.9,0.60,1),("观望犹豫",50,0.3,0.25,0),
    ("批量采购",20,1.2,0.85,2),("冷淡对照",10,0.1,0.03,0),
]

CRISIS_BPS = [
    ("曝光博主",30,2.5,0.95,"amp"),("跟风转发",120,1.2,0.80,"amp"),("愤怒声讨",100,1.0,0.90,"amp"),
    ("理性分析",80,0.8,0.60,"neu"),("沉默大多数",150,0.1,0.15,"neu"),
    ("忠诚辩护",60,1.5,0.85,"def"),("竞争对手推波",20,1.8,0.90,"opp"),
    ("专业投诉",40,1.2,0.75,"vic"),("媒体跟进",30,2.0,0.80,"med"),
    ("监管介入",10,1.5,0.70,"aut"),("水军洗地",40,0.5,0.60,"def"),
    ("竞品受益者",20,0.9,0.80,"opp"),("观望纠结",100,0.3,0.30,"neu"),("完全无视",200,0.05,0.02,"ign"),
]

def make_promo_profiles(n):
    total = sum(x[1] for x in PROMO_BPS)
    sc = n / total
    out, idx = [], 0
    for role, cnt, inf, prob, dem in PROMO_BPS:
        for _ in range(max(1, int(cnt * sc))):
            out.append({"id":idx,"role":role,"name":gen_name(),
                "inf":round(inf*random.uniform(0.8,1.2),2),
                "prob":round(min(prob*random.uniform(0.85,1.1),1.0),2),
                "demand":dem})
            idx += 1
    random.shuffle(out)
    for i,p in enumerate(out): p["id"] = i
    return out[:n]

def make_crisis_profiles(n):
    total = sum(x[1] for x in CRISIS_BPS)
    sc = n / total
    out, idx = [], 0
    for role, cnt, inf, prob, ct in CRISIS_BPS:
        for _ in range(max(1, int(cnt * sc))):
            out.append({"id":idx,"role":role,"ct":ct,"name":gen_name(),
                "inf":round(inf*random.uniform(0.8,1.2),2),
                "prob":round(min(prob*random.uniform(0.85,1.1),1.0),2)})
            idx += 1
    random.shuffle(out)
    for i,p in enumerate(out): p["id"] = i
    return out[:n]

class PromoWorld:
    def __init__(self, ps, seed, stock, hours, rounds, op, pp, ptype="水果/生鲜"):
        self.ps = ps; self.seed = seed; self.n = len(ps)
        self.stock = stock; self.total = stock
        self.hours = hours; self.rounds = rounds
        self.round_h = hours / rounds
        self.op = op; self.pp = pp
        self.vk = vk_f(ptype, pp, op)
        self.aw = [False]*self.n; self.ord = [False]*self.n
        self.posts = []; self.orders = []; self.shares = []; self.recs = []
        self._build()
        koc = {"头部KOC","腰部KOC","素人种草"}
        for i,p in enumerate(ps):
            if p["role"] in koc:
                self.aw[i] = True
                self.posts.append({"rnd":0,"id":i,"name":p["name"],"role":p["role"],
                    "content":"【爆款】"+seed,"inf":p["inf"],"eng":0})

    def _build(self):
        self.fg = defaultdict(set)
        ri = defaultdict(list)
        for i,p in enumerate(self.ps): ri[p["role"]].append(i)
        head = set(ri["头部KOC"]); waist = set(ri["腰部KOC"])
        sat = set(ri["复购满意"]); crowd = ri["随大流强"]
        for j in range(self.n):
            for k in head:
                if k != j: self.fg[j].add(k)
        for j,p in enumerate(self.ps):
            if p["role"] in {"素人种草","随大流强","随大流弱","新客首单"}:
                for k in waist:
                    if random.random() < 0.5: self.fg[j].add(k)
            if p["role"] in {"复购一般","新客首单","随大流强"}:
                for k in sat:
                    if random.random() < 0.4: self.fg[j].add(k)
        for a in crowd:
            for b in crowd:
                if a != b and random.random() < 0.3: self.fg[a].add(b)

    def _spread(self, rnd):
        newly = set()
        rp = {p["id"] for p in self.posts if p["rnd"] == rnd-1}
        hp = {p["id"] for p in self.posts if p["rnd"] == rnd-1 and p["eng"] >= 5}
        for i in range(self.n):
            if self.aw[i]: continue
            if self.fg.get(i,set()) & rp: newly.add(i)
            elif hp and random.random() < 0.08: newly.add(i)
        for i in newly: self.aw[i] = True
        return newly

    def _decide(self, p, rnd, sp):
        role = p["role"]; base = p["prob"]
        sb = max(0,(0.8-sp))*0.4
        tb = (rnd/self.rounds)*0.15
        herd = (1-sp)*0.3
        ss = "货源充足" if sp>0.7 else "库存紧张" if sp>0.3 else "仅剩少量！"
        tt = "还剩"+str(int((self.rounds-rnd+1)*self.round_h))+"h"
        prob = min(base+herd+sb+tb, 0.99)
        if role in {"头部KOC","腰部KOC","素人种草"}:
            pp2 = 0.9 if role=="头部KOC" else (0.75 if role=="腰部KOC" else 0.6)
            if random.random() < pp2:
                t = [self.seed, "【必抢】"+self.seed+" · "+ss+"！"+tt]
                if sp < 0.3: t.append("⚠️ "+self.seed+"库存告急！快抢！")
                return {"t":"post","id":p["id"],"name":p["name"],"role":role,"content":random.choice(t),"inf":p["inf"]}
        if role in {"羊毛头号","羊毛普通"}:
            mult = 2.0 if role=="羊毛头号" else 1.5
            if random.random() < min(prob*mult*(1+sb), 0.99):
                qty = random.choices([1,2],[0.75,0.25])[0]
                return {"t":"order","id":p["id"],"name":p["name"],"role":role,"qty":qty}
        elif role in {"随大流强","随大流弱"}:
            sig = min(len(self.orders)/30,1.0) if role=="随大流强" else min(len(self.orders)/50,1.0)
            if random.random() < min(base+sig*0.5+herd*1.5+sb, 0.95):
                return {"t":"order","id":p["id"],"name":p["name"],"role":role,"qty":1}
        elif role in {"宝妈精准","银发精准","白领精准"}:
            if random.random() < min(prob*1.1+sb*0.5, 0.9):
                qty = random.choices([1,2],[0.6,0.4])[0]
                return {"t":"order","id":p["id"],"name":p["name"],"role":role,"qty":qty}
        elif role in {"复购满意","复购一般"}:
            b = 0.92 if role=="复购满意" else 0.6
            if random.random() < min(b*(1+sb*0.5), 0.95):
                qty = random.choices([1,2],[0.5,0.5])[0]
                return {"t":"order","id":p["id"],"name":p["name"],"role":role,"qty":qty}
        elif role == "批量采购":
            if random.random() < min(prob*1.5+sb, 0.9):
                qty = random.choices([3,5,10],[0.3,0.4,0.3])[0]
                return {"t":"order","id":p["id"],"name":p["name"],"role":role,"qty":qty}
        elif role == "新客首单":
            if random.random() < min(prob+sb, 0.7):
                return {"t":"order","id":p["id"],"name":p["name"],"role":role,"qty":1}
        return None

    def boost(self):
        oid = {o["id"] for o in self.orders}
        for post in self.posts:
            post["eng"] += sum(1 for o in oid if o in self.fg.get(post["id"],set()))

    def run_round(self, rnd):
        sp = self.stock / self.total
        rec = {"rnd":rnd,"new_aw":0,"posts":[],"orders":[],"shares":[],"stock_end":self.stock}
        new = self._spread(rnd); rec["new_aw"] = len(new)
        PRI = {"批量采购":0,"羊毛头号":1,"羊毛普通":2,"宝妈精准":3,"银发精准":4,"白领精准":5,
               "复购满意":6,"复购一般":7,"新客首单":8,"随大流强":9,"随大流弱":10}
        acts = []; random.shuffle(self.ps)
        for p in self.ps:
            if not self.aw[p["id"]]: continue
            a = self._decide(p, rnd, sp)
            if a: acts.append((p,a))
        left = self.stock
        for p,a in sorted(acts, key=lambda x: PRI.get(x[0]["role"],99)):
            if a["t"] == "post":
                self.posts.append({"rnd":rnd,"eng":0,**a}); rec["posts"].append(a)
            elif a["t"] == "order":
                qty = min(a["qty"], left)
                if qty > 0 and not self.ord[p["id"]]:
                    self.ord[p["id"]] = True; left -= qty
                    o = {"rnd":rnd,"id":p["id"],"name":a["name"],"role":a["role"],"qty":qty}
                    self.orders.append(o); rec["orders"].append(o)
                    if random.random() < 0.2:
                        self.shares.append({"rnd":rnd,"id":p["id"],"name":a["name"],"role":a["role"]})
                        rec["shares"].append(p["id"])
        self.stock = max(0, left); rec["stock_end"] = self.stock
        rec["depleted"] = self.stock <= 0; self.boost()
        self.recs.append(rec); return rec

    def run(self):
        print("[促销v3] "+str(self.n)+"人 库存"+str(self.total)+"份 "+str(self.rounds)+"轮 K="+str(self.vk)+" 原价"+str(self.op)+"->"+str(self.pp)+"元")
        seed_koc = len([p for p in self.posts if p["rnd"]==0])
        print("[促销v3] 种子KOC: "+str(seed_koc)+"条\n")
        for r in range(1, self.rounds+1):
            rec = self.run_round(r)
            dep = " 库存耗尽!" if rec["depleted"] else ""
            print("[促销v3] R"+str(r)+"/"+str(self.rounds)+" | 新+"+str(rec["new_aw"])+" | "+str(len(rec["orders"]))+"单(剩"+str(rec["stock_end"])+") | "+str(len(rec["posts"]))+"帖"+dep)
            if rec["depleted"]: break
        return self._result()

    def _result(self):
        sold = sum(o["qty"] for o in self.orders)
        rate = sold / self.n
        real = int(rate * self.n * 8)
        sub = self.op - self.pp
        st = self.total
        pess = min(int(real*0.5), st)
        neut = min(int(real*0.8), st)
        opt = min(int(real*1.2), st)
        by_rnd = dict(Counter(r["rnd"] for r in self.recs))
        koc_posts = sum(1 for p in self.posts if p["role"] in {"头部KOC","腰部KOC"})
        return {
            "type":"promo","seed":self.seed,"n":self.n,"stock":st,"sold":sold,
            "vk":self.vk,"vk_label":"K>1病毒传播" if self.vk>1 else "K<1需KOC推动",
            "op":self.op,"pp":self.pp,"p_price":self.pp,"o_price":self.op,
            "reach":self.n*8,
            "pess":pess,"neut":neut,"opt":opt,
            "pess_l":round(pess*sub),"neut_l":round(neut*sub),"opt_l":round(opt*sub),"sub":sub,
            "posts":self.posts,"orders":self.orders,"recs":self.recs,
            "depleted_rnd":next((r["rnd"] for r in self.recs if r["depleted"]),None),
            "koc_posts":koc_posts,"koc_p":koc_posts,
            "wool":sum(1 for o in self.orders if o["role"] in {"羊毛头号","羊毛普通"}),
            "crowd":sum(1 for o in self.orders if o["role"]=="随大流强"),
            "batch":sum(1 for o in self.orders if o["role"]=="批量采购"),
            "aw_rate":round(sum(self.aw)/self.n*100,1),
            "by_rnd":by_rnd,"by_r":by_rnd,
        }

class CrisisWorld:
    def __init__(self, ps, crisis, hours, rounds, team=True):
        self.ps = ps; self.crisis = crisis; self.n = len(ps)
        self.hours = hours; self.rounds = rounds; self.round_h = hours/rounds
        self.team = team
        self.aw = [False]*self.n
        self.posts = []; self.neg = []; self.pos = []
        self.shares = []; self.reports = []; self.media = []
        self.recs = []; self.team_act = []; self.intervention = 0; self.score = 0.0
        self._build()
        for i,p in enumerate(ps):
            if p["ct"] in ("amp","med","vic","aut") and p["prob"] > 0.6:
                self.aw[i] = True; self._emit(p, 0, "neg")

    def _build(self):
        self.fg = defaultdict(set)
        ri = defaultdict(list)
        for i,p in enumerate(self.ps): ri[p["role"]].append(i)
        for role in ["曝光博主","媒体跟进","愤怒声讨"]:
            infl = set(ri.get(role,[]))
            for j in range(self.n):
                for k in infl:
                    if k != j: self.fg[j].add(k)
        defs = set(ri.get("忠诚辩护",[]))
        for a in defs:
            for b in defs:
                if a != b: self.fg[a].add(b)
        for role in ["跟风转发","愤怒声讨"]:
            for j in ri.get(role,[]):
                for k in set(ri.get("曝光博主",[]))|set(ri.get("愤怒声讨",[])):
                    if random.random() < 0.6: self.fg[j].add(k)

    def _emit(self, p, rnd, sent):
        if sent == "neg":
            t = ["【重大爆料】"+self.crisis,"【食品安全】"+self.crisis+"大家注意!",
                 "【必须曝光】"+self.crisis,"【消费者警示】"+self.crisis]
        else:
            t = ["理性看待,成山一直品质可靠","老客户:我买了很多年没出过问题","支持成山!等官方通报"]
        post = {"rnd":rnd,"id":p["id"],"name":p["name"],"role":p["role"],
                 "ct":p["ct"],"sent":sent,"content":random.choice(t),"inf":p["inf"],"reach":0}
        self.posts.append(post)
        if sent == "neg": self.neg.append(post)
        else: self.pos.append(post)
        return post

    def _spread(self, rnd):
        newly = set()
        rp = {p["id"] for p in self.posts if p["rnd"]==rnd-1}
        nrp = {p["id"] for p in self.neg if p["rnd"]==rnd-1}
        for i in range(self.n):
            if self.aw[i]: continue
            if self.fg.get(i,set()) & rp: newly.add(i)
            elif nrp and random.random() < 0.15: newly.add(i)
        for i in newly: self.aw[i] = True
        return newly

    def _update_score(self, rnd):
        hrs = rnd * self.round_h
        base = len(self.neg)*2 + len(self.shares)*1 + len(self.reports)*3 + len(self.media)*5
        dil = max(0, len(self.pos)*1.5)
        dec = decay_f(hrs, self.intervention)
        raw = (base - dil) * dec + len(self.media)*8
        self.score = max(0, min(100, raw))

    def _team_act(self, rnd):
        if not self.team: return []
        taken = []
        for m in RESPONSE_TEAM:
            if rnd < m["delay"]: continue
            recent = [a for a in self.team_act if a["who"]==m["name"]]
            if recent and (rnd - recent[-1]["rnd"]) < m["cooldown"]: continue
            if random.random() < m["prob"]:
                self.intervention += 1
                self.score = max(0, self.score - m["effect"])
                self.team_act.append({"rnd":rnd,"who":m["name"],"effect":m["effect"],"desc":m["desc"],"score_after":round(self.score,1)})
                taken.append(m["name"])
                if random.random() < 0.5:
                    fake = {"id":9999,"name":m["name"],"role":m["name"],"ct":"def","inf":1.5}
                    self._emit(fake, rnd, "pos")
        return taken

    def _decide(self, p, rnd):
        ct = p["ct"]; base = p["prob"]
        hrs = rnd * self.round_h
        tf = 1.3 if hrs<=6 else 1.0 if hrs<=24 else 0.7 if hrs<=48 else 0.4
        hf = self.score/100*0.3; prob = min(base*tf*(1+hf), 0.99)
        acts = []
        if ct == "amp":
            if random.random() < prob: acts.append("neg")
            if random.random() < 0.4: acts.append("shr")
        elif ct == "opp":
            if random.random() < min(prob*1.2, 0.9): acts.append("neg"); acts.append("exp")
        elif ct == "def":
            if random.random() < prob: acts.append("pos")
        elif ct == "vic":
            if random.random() < prob: acts.append("rep")
        elif ct == "med":
            if random.random() < min(prob*0.8, 0.75): acts.append("med")
        elif ct == "neu" and p["role"] == "跟风转发":
            if random.random() < min(prob*1.1, 0.9): acts.append("shr")
        elif ct == "neu" and p["role"] == "观望纠结":
            nb = max(0, len(self.neg)/(len(self.neg)+len(self.pos)+1) - 0.5)*2
            if random.random() < min(prob*(0.5+nb), 0.8): acts.append("shr")
        return acts

    def run_round(self, rnd):
        rec = {"rnd":rnd,"hrs":int(rnd*self.round_h),"new_aw":0,
               "posts":0,"neg_tot":0,"pos_tot":0,"shr":0,"rep":0,"med":0,
               "score":0,"team":[],"tot_aw":0}
        new = self._spread(rnd); rec["new_aw"] = len(new)
        self._update_score(rnd)
        tm = self._team_act(rnd); rec["team"] = tm
        if tm: print("[响应小组] R"+str(rnd)+"行动: "+", ".join(tm))
        for p in self.ps:
            if not self.aw[p["id"]]: continue
            for act in self._decide(p, rnd):
                if act == "neg":
                    self._emit(p, rnd, "neg"); rec["posts"]+=1; rec["neg_tot"]+=1
                elif act == "pos":
                    self._emit(p, rnd, "pos"); rec["posts"]+=1; rec["pos_tot"]+=1
                elif act in ("shr","exp"):
                    tp = "competitor_steal" if act=="exp" else "share"
                    self.shares.append({"rnd":rnd,"id":p["id"],"name":p["name"],"type":tp})
                    rec["shr"] += 1
                elif act == "rep":
                    self.reports.append({"rnd":rnd,"id":p["id"],"name":p["name"]}); rec["rep"]+=1
                elif act == "med":
                    self.media.append({"rnd":rnd,"name":p["name"],"inf":p["inf"]}); rec["med"]+=1
        rec["score"] = round(self.score,1); rec["tot_aw"] = sum(self.aw)
        self.recs.append(rec); return rec

    def run(self):
        print("[舆情危机v3] "+str(self.n)+"人 "+str(self.hours)+"h 响应小组:"+("ON" if self.team else "OFF"))
        seed0 = len([p for p in self.posts if p["rnd"]==0])
        print("[舆情危机v3] 初始曝光: "+str(seed0)+"条\n")
        for r in range(1, self.rounds+1):
            rec = self.run_round(r)
            ts = " | 响应:"+",".join(rec["team"]) if rec["team"] else ""
            print("[舆情危机v3] R"+str(r)+"/"+str(self.rounds)+"(~"+str(rec["hrs"])+"h) 新+"+str(rec["new_aw"])+
                  " 帖"+str(rec["posts"])+"(负"+str(rec["neg_tot"])+"/正"+str(rec["pos_tot"])+
                  ") 转"+str(rec["shr"])+" 投"+str(rec["rep"])+" 媒"+str(rec["med"])+
                  " 热度"+str(rec["score"])+"/100"+ts)
        return self._result()

    def _result(self):
        nc = len(self.neg); pc = len(self.pos); tot = nc+pc
        npct = nc/tot if tot>0 else 0
        pol = round(abs(npct-0.5)*2, 2)
        top5 = sorted(self.neg, key=lambda x:x.get("reach",0), reverse=True)[:5]
        tl = [(a["rnd"],a["who"],a["effect"]) for a in self.team_act]
        team_tl_list = [(a["rnd"],a["who"],a["effect"]) for a in self.team_act]
        return {
            "type":"crisis","crisis":self.crisis,"n":self.n,"hours":self.hours,"rounds":self.rounds,
            "posts":self.posts,"neg":self.neg,"pos":self.pos,
            "shares":self.shares,"reports":self.reports,"media":self.media,
            "recs":self.recs,"team":self.team_act,"intervention":self.intervention,
            "peak_rnd":max(self.recs, key=lambda x:x["score"])["rnd"] if self.recs else 0,
            "peak_score":max(r["score"] for r in self.recs) if self.recs else 0,
            "top5":[{"name":p["name"],"role":p["role"],"content":p["content"][:60],"reach":p.get("reach",0)} for p in top5],
            "team_tl":tl,"team_timeline":team_tl_list,"neg_pct":round(npct*100,1),"pol":pol,
            "comp_hits":sum(1 for s in self.shares if s.get("type")=="competitor_steal"),
        }


# ── 报告打印函数 ──────────────────────────────────────────────

def print_promo(r):
    dep_str = "\n  ⚠️ 库存R" + str(r["depleted_rnd"]) + "耗尽！" if r["depleted_rnd"] else ""
    print("""
═══════════════════════════════════════════════════════════
  七政-OASIS v3 · 爆款促销推演（K系数版）
  场景：""" + r["seed"] + """
  """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """
═══════════════════════════════════════════════════════════

📊 仿真结果
  · """ + str(r["n"]) + """人 · 库存""" + str(r["stock"]) + """份 · 触达""" + str(r["reach"]) + """人
  · 传播系数：K=""" + str(r["vk"]) + """（""" + r["vk_label"] + """）
  · 促销价¥""" + str(r["p_price"]) + """（原价¥""" + str(r["o_price"]) + """）

═══════════════════════════════════════════════════════════
📦 订单量预测（触达""" + str(r["reach"]) + """人）
═══════════════════════════════════════════════════════════
  悲观  """ + str(r["pess"]) + """单  亏损¥""" + str(r["pess_l"]) + """
  中性  """ + str(r["neut"]) + """单  亏损¥""" + str(r["neut_l"]) + """
  乐观  """ + str(r["opt"]) + """单  亏损¥""" + str(r["opt_l"]) + """
  每单补贴¥""" + str(r["sub"]) + dep_str + """

═══════════════════════════════════════════════════════════
🔥 各轮订单：""" + str(r["by_rnd"]) + """
═══════════════════════════════════════════════════════════
⚠️ KOC发帖""" + str(r["koc_posts"]) + """条 | 羊毛党""" + str(r["wool"]) + """人 | 随大流""" + str(r["crowd"]) + """人 | 批量""" + str(r["batch"]) + """人
""")

def print_crisis(r):
    risk = "极高" if r["peak_score"] > 80 else ("高" if r["peak_score"] > 60 else "中")
    tl_str = ", ".join("R"+str(rn)+":"+w+"(-"+str(e)+")" for rn,w,e in r["team_timeline"])
    print("""
═══════════════════════════════════════════════════════════
  七政-OASIS v3 · 舆情危机推演（响应小组版）
  场景：""" + r["crisis"] + """
  """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """
═══════════════════════════════════════════════════════════

📊 舆情概况
  · """ + str(r["n"]) + """人 · """ + str(r["hours"]) + """h · 响应小组行动""" + str(len(r["team"])) + """次
  · 帖子""" + str(len(r["neg"]) + len(r["pos"])) + """条（负""" + str(len(r["neg"])) + """/正""" + str(len(r["pos"])) + """）
  · 转发""" + str(len(r["shares"])) + """次 | 投诉""" + str(len(r["reports"])) + """次 | 媒体""" + str(len(r["media"])) + """次
  · 负面占比""" + str(r["neg_pct"]) + """% | 极化指数""" + str(r["pol"]) + """
  · 干预有效轮次：""" + str(r["intervention"]) + """轮

═══════════════════════════════════════════════════════════
🔥 舆情演化曲线（新华数据校准）
═══════════════════════════════════════════════════════════
  峰值：R""" + str(r["peak_rnd"]) + """ · 热度""" + str(r["peak_score"]) + """/100""")
    if tl_str:
        print("  响应小组干预：" + tl_str)
    print("  各轮热度：")
    for rec in r["recs"]:
        bar = "█" * int(rec["score"] / 5) + "░" * (20 - int(rec["score"] / 5))
        print("  R" + str(rec["rnd"]) + "(≈" + str(rec["hrs"]) + "h) [" + bar + "] " + str(rec["score"]).rjust(5) + " | 负" + str(rec["neg_tot"]) + "/正" + str(rec["pos_tot"]))
    print("""
═══════════════════════════════════════════════════════════
⚠️ 风险：""" + risk + """ | 峰值热度""" + str(r["peak_score"]) + """/100 | 竞品抢客""" + str(r["comp_hits"]) + """次""")
    if r["top5"]:
        print("""
═══════════════════════════════════════════════════════════
📰 高影响力负面帖子TOP5：""")
        for i, p in enumerate(r["top5"], 1):
            print("  " + str(i) + ". 【" + p["role"] + "·" + p["name"] + "】触达" + str(p["reach"]) + "人")
            print("     " + p["content"])

def main():
    ap = argparse.ArgumentParser(description="七政-OASIS v3")
    ap.add_argument("--mode", choices=["promo", "crisis"], required=True, help="promo=爆款促销 | crisis=舆情危机")
    ap.add_argument("--scenario", default="成山农场蓝莓9.9元爆款")
    ap.add_argument("--n", type=int, default=1000, help="agent数量")
    ap.add_argument("--stock", type=int, default=500, help="库存量（promo模式）")
    ap.add_argument("--hours", type=int, default=48, help="仿真时长小时（crisis模式默认48）")
    ap.add_argument("--rounds", type=int, default=6, help="轮次（crisis默认6）")
    ap.add_argument("--op", type=float, default=26.0, help="原价")
    ap.add_argument("--pp", type=float, default=9.9, help="促销价")
    ap.add_argument("--ptype", default="水果/生鲜", help="产品类型")
    ap.add_argument("--team", default="true", help="启用响应小组 true/false")
    ap.add_argument("--out", default="/workspace/data/qizheng-oasis/result_v3.json", help="输出JSON路径")
    args = ap.parse_args()
    os.makedirs("/workspace/data/qizheng-oasis", exist_ok=True)

    if args.mode == "promo":
        print("[天枢v3] 生成" + str(args.n) + "个角色...")
        profiles = make_promo_profiles(args.n)
        print("[天权v3] 运行爆款促销推演...")
        w = PromoWorld(profiles, args.scenario, args.stock, 24, 4, args.op, args.pp, args.ptype)
        r = w.run()
        print_promo(r)
        out_key = "promo_result"
    else:
        team = args.team.lower() == "true"
        print("[天枢v3] 生成" + str(args.n) + "个舆情角色（响应小组:" + ("ON" if team else "OFF") + ")...")
        profiles = make_crisis_profiles(args.n)
        print("[天权v3] 运行舆情危机推演...")
        w = CrisisWorld(profiles, args.scenario, args.hours, args.rounds, team)
        r = w.run()
        print_crisis(r)
        out_key = "crisis_result"

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({out_key: r, "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, f, ensure_ascii=False, indent=2)
    print("\n[完成] 结果已保存: " + args.out)

if __name__ == "__main__":
    main()
