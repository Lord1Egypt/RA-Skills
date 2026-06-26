#!/usr/bin/env python3
import json, random, os, argparse
from collections import Counter, defaultdict
from datetime import datetime

RESPONSE_TEAM = [
    {"name":"CEO紧急响应","prob":0.9,"delay":1,"effect":8,"cooldown":3,"desc":"30分钟声明道歉+召回"},
    {"name":"公关部","prob":0.85,"delay":1,"effect":6,"cooldown":2,"desc":"正面通稿联系媒体"},
    {"name":"客服部","prob":0.9,"delay":1,"effect":5,"cooldown":1,"desc":"一对一老客户"},
    {"name":"运营部","prob":0.75,"delay":2,"effect":4,"cooldown":3,"desc":"老客户专属优惠防竞品"},
    {"name":"法务部","prob":0.7,"delay":2,"effect":4,"cooldown":4,"desc":"律师函证据保全"},
    {"name":"品控部","prob":0.65,"delay":2,"effect":3,"cooldown":5,"desc":"第三方检测"},
]
DECAY = [(0,1.0),(2,.98),(4,.90),(6,.85),(12,.70),(24,.60),(36,.50),(48,.40),(72,.28),(96,.18),(120,.12)]
def decay(h,i):
    b=1.0
    for h2,d in DECAY:
        if h<=h2: b=d; break
    return b*max(.4,1.0-i*.03)
def vk(pt,pp,op):
    d=pp/op
    base={"水果/生鲜":.8,"食品":.6,"日用品":.5,"服装":.7,"电子产品":.4}.get(pt,.5)
    m=2.5 if d<.3 else 1.8 if d<.5 else 1.3 if d<.7 else 1.0
    return round(base*m,2)
def gn():
    s1=random.choice(list("小阿老大小赵钱孙李周吴郑王冯陈褚卫"))
    s2=random.choice(list("林丽华敏静强磊洋勇艳军波飞霞梅兰菊桃桂"))
    return s1+s2+str(random.randint(10,99))
PROMO=[
    ("头部KOC",30,2.5,.95,2),("腰部KOC",70,1.8,.88,1),("素人种草",100,1.2,.75,1),
    ("宝妈精准",120,1.0,.80,2),("银发精准",60,.7,.65,2),("白领精准",80,.8,.60,1),
    ("羊毛头号",60,1.5,.95,2),("羊毛普通",120,.8,.88,1),("羊毛比价",60,.6,.70,0),
    ("随大流强",80,.9,.75,1),("随大流弱",60,.4,.40,0),("新客首单",80,.5,.55,1),
    ("复购满意",50,1.5,.92,2),("复购一般",40,.9,.60,1),("观望犹豫",50,.3,.25,0),
    ("批量采购",20,1.2,.85,2),("冷淡对照",10,.1,.03,0),
]
CRISIS=[
    ("曝光博主",30,2.5,.95,"amp"),("跟风转发",120,1.2,.80,"amp"),("愤怒声讨",100,1.0,.90,"amp"),
    ("理性分析",80,.8,.60,"neu"),("沉默大多数",150,.1,.15,"neu"),
    ("忠诚辩护",60,1.5,.85,"def"),("竞争对手推波",20,1.8,.90,"opp"),
    ("专业投诉",40,1.2,.75,"vic"),("媒体跟进",30,2.0,.80,"med"),
    ("监管介入",10,1.5,.70,"aut"),("水军洗地",40,.5,.60,"def"),
    ("竞品受益者",20,.9,.80,"opp"),("观望纠结",100,.3,.30,"neu"),("完全无视",200,.05,.02,"ign"),
]
def mp(n):
    t=sum(x[1] for x in PROMO); sc=n/t; o=[]; i=0
    for role,cnt,inf,prob,dem in PROMO:
        for _ in range(max(1,int(cnt*sc))):
            o.append({"i":i,"r":role,"n":gn(),"f":round(inf*random.uniform(.8,1.2),2),"p":round(min(prob*random.uniform(.85,1.1),1.0),2),"d":dem}); i+=1
    random.shuffle(o)
    for j,p in enumerate(o): p["i"]=j
    return o[:n]
def mc(n):
    t=sum(x[1] for x in CRISIS); sc=n/t; o=[]; i=0
    for role,cnt,inf,prob,ct in CRISIS:
        for _ in range(max(1,int(cnt*sc))):
            o.append({"i":i,"r":role,"ct":ct,"n":gn(),"f":round(inf*random.uniform(.8,1.2),2),"p":round(min(prob*random.uniform(.85,1.1),1.0),2)}); i+=1
    random.shuffle(o)
    for j,p in enumerate(o): p["i"]=j
    return o[:n]

class PW:
    def __init__(s,ps,seed,stock,hours,rounds,op,pp,pt):
        s.ps=ps;s.seed=seed;s.n=len(ps);s.stock=stock;s.total=stock;s.h=hours;s.R=rounds;s.rh=hours/rounds
        s.op=op;s.pp=pp;s.vk=vk(pt,pp,op);s.aw=[False]*s.n;s.od=[False]*s.n
        s.ps2=[];s.os=[];s.sh=[];s.rs=[];s._g()
        koc={"头部KOC","腰部KOC","素人种草"}
        for i,p in enumerate(ps):
            if p["r"] in koc:
                s.aw[i]=True;s.ps2.append({"rn":0,"i":i,"n":p["n"],"r":p["r"],"c":"[爆款]"+seed,"f":p["f"],"e":0})
    def _g(s):
        s.fg=defaultdict(set);ri=defaultdict(list)
        for i,p in enumerate(s.ps): ri[p["r"]].append(i)
        h=set(ri["头部KOC"]);w=set(ri["腰部KOC"]);st=set(ri["复购满意"]);cr=ri["随大流强"]
        for j in range(s.n):
            for k in h:
                if k!=j: s.fg[j].add(k)
        for j,p in enumerate(s.ps):
            if p["r"] in {"素人种草","随大流强","随大流弱","新客首单"}:
                for k in w:
                    if random.random()<.5: s.fg[j].add(k)
            if p["r"] in {"复购一般","新客首单","随大流强"}:
                for k in st:
                    if random.random()<.4: s.fg[j].add(k)
        for a in cr:
            for b in cr:
                if a!=b and random.random()<.3: s.fg[a].add(b)
    def _sp(s,rn):
        ne=set();rp={p["i"] for p in s.ps2 if p["rn"]==rn-1}
        hp={p["i"] for p in s.ps2 if p["rn"]==rn-1 and p["e"]>=5}
        for i in range(s.n):
            if s.aw[i]: continue
            if s.fg.get(i,set())&rp: ne.add(i)
            elif hp and random.random()<.08: ne.add(i)
        for i in ne: s.aw[i]=True
        return ne
    def _dc(s,p,rn,sp):
        r=p["r"];b=p["p"];sb=max(0,(.8-sp))*.4;tb=(rn/s.R)*.15;hr=(1-sp)*.3
        ss="货源充足" if sp>.7 else "库存紧张" if sp>.3 else "仅剩少量"
        tt="还剩"+str(int((s.R-rn+1)*s.rh))+"h"
        pr=min(b+hr+sb+tb,.99)
        if r in {"头部KOC","腰部KOC","素人种草"}:
            pp2=.9 if r=="头部KOC" else .75 if r=="腰部KOC" else .6
            if random.random()<pp2:
                t=[s.seed,"[必抢]"+s.seed+" "+ss+" "+tt]
                if sp<.3: t.append("[警告]"+s.seed+"库存告急!")
                return {"t":"p","i":p["i"],"n":p["n"],"r":r,"c":random.choice(t),"f":p["f"]}
        if r in {"羊毛头号","羊毛普通"}:
            m=2.0 if r=="羊毛头号" else 1.5
            if random.random()<min(pr*m*(1+sb),.99):
                qty=random.choices([1,2],[.75,.25])[0]
                return {"t":"o","i":p["i"],"n":p["n"],"r":r,"q":qty}
        elif r in {"随大流强","随大流弱"}:
            sig=min(len(s.os)/30,1.0) if r=="随大流强" else min(len(s.os)/50,1.0)
            if random.random()<min(b+sig*.5+hr*1.5+sb,.95):
                return {"t":"o","i":p["i"],"n":p["n"],"r":r,"q":1}
        elif r in {"宝妈精准","银发精准","白领精准"}:
            if random.random()<min(pr*1.1+sb*.5,.9):
                qty=random.choices([1,2],[.6,.4])[0]
                return {"t":"o","i":p["i"],"n":p["n"],"r":r,"q":qty}
        elif r in {"复购满意","复购一般"}:
            b2=.92 if r=="复购满意" else .6
            if random.random()<min(b2*(1+sb*.5),.95):
                qty=random.choices([1,2],[.5,.5])[0]
                return {"t":"o","i":p["i"],"n":p["n"],"r":r,"q":qty}
        elif r=="批量采购":
            if random.random()<min(pr*1.5+sb,.9):
                qty=random.choices([3,5,10],[.3,.4,.3])[0]
                return {"t":"o","i":p["i"],"n":p["n"],"r":r,"q":qty}
        elif r=="新客首单":
            if random.random()<min(pr+sb,.7):
                return {"t":"o","i":p["i"],"n":p["n"],"r":r,"q":1}
        return None
    def _bk(s):
        oi={o["i"] for o in s.os}
        for p in s.ps2: p["e"]+=sum(1 for o in oi if o in s.fg.get(p["i"],set()))
    def _rr(s,rn):
        sp=s.stock/s.total;rc={"rn":rn,"na":0,"ps":[],"os":[],"sh":[],"se":s.stock}
        ne=s._sp(rn);rc["na"]=len(ne)
        PR={"批量采购":0,"羊毛头号":1,"羊毛普通":2,"宝妈精准":3,"银发精准":4,"白领精准":5,
            "复购满意":6,"复购一般":7,"新客首单":8,"随大流强":9,"随大流弱":10}
        acts=[];random.shuffle(s.ps)
        for p in s.ps:
            if not s.aw[p["i"]]: continue
            a=s._dc(p,rn,sp)
            if a: acts.append((p,a))
        left=s.stock
        for p,a in sorted(acts,key=lambda x:PR.get(x[0]["r"],99)):
            if a["t"]=="p":
                s.ps2.append({"rn":rn,**a});rc["ps"].append(a)
            elif a["t"]=="o":
                qty=min(a["q"],left)
                if qty>0 and not s.od[p["i"]]:
                    s.od[p["i"]]=True;left-=qty
                    o={"rn":rn,"i":p["i"],"n":a["n"],"r":a["r"],"q":qty}
                    s.os.append(o);rc["os"].append(o)
                    if random.random()<.2:
                        s.sh.append({"rn":rn,"i":p["i"],"n":a["n"],"r":a["r"]});rc["sh"].append(p["i"])
        s.stock=max(0,left);rc["se"]=s.stock;rc["dl"]=s.stock<=0;s._bk();s.rs.append(rc);return rc
    def run(s):
        print(f"[促销v3] {s.n}人 库存{s.total}份 {s.R}轮 K={s.vk} 原价{s.op}->{s.pp}元")
        sk=len([p for p in s.ps2 if p["rn"]==0])
        print(f"[促销v3] 种子KOC: {sk}条\n")
        for r in range(1,s.R+1):
            rc=s._rr(r)
            dp=" 库存耗尽!" if rc["dl"] else ""
            print(f"[促销v3] R{r}/{s.R} | 新+{rc['na']} | {len(rc['os'])}单(剩{rc['se']}) | {len(rc['ps'])}帖{dp}")
            if rc["dl"]: break
        return s._res()
    def _res(s):
        sold=sum(o["q"] for o in s.os);rate=sold/s.n;real=int(rate*s.n*8);sub=s.op-s.pp;st=s.total
        pess=min(int(real*.5),st);neut=min(int(real*.8),st);opt=min(int(real*1.2),st)
        by_r=Counter(r["rn"] for r in s.rs)
        return {"tp":"promo","seed":s.seed,"n":s.n,"stock":st,"sold":sold,"vk":s.vk,
            "vk_tag":"K>1病毒" if s.vk>1 else "K<1需KOC",
            "op":s.op,"pp":s.pp,"reach":s.n*8,"pess":pess,"neut":neut,"opt":opt,
            "pess_l":round(pess*sub),"neut_l":round(neut*sub),"opt_l":round(opt*sub),"sub":sub,
            "posts":s.ps2,"orders":s.os,"recs":s.rs,
            "depleted_rnd":next((r["rn"] for r in s.rs if r["dl"]),None),
            "koc_p":sum(1 for p in s.ps2 if p["r"] in {"头部KOC","腰部KOC"}),
            "wool":sum(1 for o in s.os if o["r"] in {"羊毛头号","羊毛普通"}),
            "crowd":sum(1 for o in s.os if o["r"]=="随大流强"),
            "batch":sum(1 for o in s.os if o["r"]=="批量采购"),
            "aw_rate":round(s.aw.count(True)/s.n*100,1),"by_r":dict(sorted(by_r.items()))}

class CW:
    def __init__(s,ps,crisis,hours,rounds,team=True):
        s.ps=ps;s.crisis=crisis;s.n=len(ps);s.h=hours;s.R=rounds;s.rh=hours/rounds;s.team=team
        s.aw=[False]*s.n;s.ps2=[];s.ng=[];s.ps3=[];s.sh=[];s.rp=[];s.md=[]
        s.rs=[];s.ta=[];s.inte=0;s.sc=0.0;s._g()
        for i,p in enumerate(ps):
            if p["ct"] in ("amp","med","vic","aut") and p["p"]>.6:
                s.aw[i]=True;s._em(p,0,"ng")
    def _g(s):
        s.fg=defaultdict(set);ri=defaultdict(list)
        for i,p in enumerate(s.ps): ri[p["r"]].append(i)
        for role in ["曝光博主","媒体跟进","愤怒声讨"]:
            inf=set(ri.get(role,[]))
            for j in range(s.n):
                for k in inf:
                    if k!=j: s.fg[j].add(k)
        ds=set(ri.get("忠诚辩护",[]))
        for a in ds:
            for b in ds:
                if a!=b: s.fg[a].add(b)
        for role in ["跟风转发","愤怒声讨"]:
            for j in ri.get(role,[]):
                for k in set(ri.get("曝光博主",[]))|set(ri.get("愤怒声讨",[])):
                    if random.random()<.6: s.fg[j].add(k)
    def _em(s,p,rn,sent):
        if sent=="ng":
            t=["[重大爆料]"+s.crisis,"[食品安全]"+s.crisis+"大家注意!","[必须曝光]"+s.crisis,"[消费者警示]"+s.crisis]
        else:
            t=["理性看待,成山一直品质可靠","老客户:我买了很多年没出过问题","支持成山!等通报"]
        post={"rn":rn,"i":p["i"],"n":p["n"],"r":p["r"],"ct":p["ct"],"sent":sent,"c":random.choice(t),"f":p["f"],"rk":0}
        s.ps2.append(post)
        if sent=="ng": s.ng.append(post)
        else: s.ps3.append(post)
        return post
    def _sp(s,rn):
        ne=set();rp={p["i"] for p in s.ps2 if p["rn"]==rn-1}
        nrp={p["i"] for p in s.ng if p["rn"]==rn-1}
        for i in range(s.n):
            if s.aw[i]: continue
            if s.fg.get(i,set())&rp: ne.add(i)
            elif nrp and random.random()<.15: ne.add(i)
        for i in ne: s.aw[i]=True
        return ne
    def _sc(s,rn):
        h=rn*s.rh;base=len(s.ng)*2+len(s.sh)*1+len(s.rp)*3+len(s.md)*5
        dil=max(0,len(s.ps3)*1.5);dec=decay(h,s.inte)
        raw=(base-dil)*dec+len(s.md)*8;s.sc=max(0,min(100,raw))
    def _tm(s,rn):
        if not s.team: return []
        tk=[]
        for m in RESPONSE_TEAM:
            if rn<m["delay"]: continue
            rc=[a for a in s.ta if a["n"]==m["name"]]
            if rc and (rn-rc[-1]["rn"])<m["cooldown"]: continue
            if random.random()<m["prob"]:
                s.inte+=1;s.sc=max(0,s.sc-m["effect"])
                s.ta.append({"rn":rn,"n":m["name"],"e":m["effect"],"d":m["desc"],"sa":round(s.sc,1)})
                tk.append(m["name"])
                if random.random()<.5:
                    fake={"i":9999,"n":m["name"],"r":m["name"],"ct":"def","f":1.5}
                    s._em(fake,rn,"ps")
        return tk
    def _dc(s,p,rn):
        ct=p["ct"];b=p["p"];h=rn*s.rh
        tf=1.3 if h<=6 else 1.0 if h<=24 else .7 if h<=48 else .4
        hf=s.sc/100*.3;pr=min(b*tf*(1+hf),.99);ac=[]
        if ct=="amp":
            if random.random()<pr: ac.append("ng")
            if random.random()<.4: ac.append("sh")
        elif ct=="opp":
            if random.random()<min(pr*1.2,.9): ac.append("ng");ac.append("exp")
        elif ct=="def":
            if random.random()<pr: ac.append("ps")
        elif ct=="vic":
            if random.random()<pr: ac.append("rp")
        elif ct=="med":
            if random.random()<min(pr*.8,.75): ac.append("md")
        elif ct=="neu" and p["r"]=="跟风转发":
            if random.random()<min(pr*1.1,.9): ac.append("sh")
        elif ct=="neu" and p["r"]=="观望纠结":
            nb=max(0,len(s.ng)/(len(s.ng)+len(s.ps3)+1)-.5)*2
            if random.random()<min(pr*(.5+nb),.8): ac.append("sh")
        return ac
    def _rr(s,rn):
        rc={"rn":rn,"h":int(rn*s.rh),"na":0,"ps":0,"ng_tot":0,"ps_tot":0,"sh":0,"rp":0,"md":0,"sc":0,"ta":[],"aw":0}
        ne=s._sp(rn);rc["na"]=len(ne);s._sc(rn)
        tm=s._tm(rn);rc["ta"]=tm
        if tm: print("[响应小组] R"+str(rn)+"行动: "+", ".join(tm))
        for p in s.ps:
            if not s.aw[p["i"]]: continue
            for act in s._dc(p,rn):
                if act=="ng": s._em(p,rn,"ng");rc["ps"]+=1;rc["ng_tot"]+=1
                elif act=="ps": s._em(p,rn,"ps");rc["ps"]+=1;rc["ps_tot"]+=1
                elif act in ("sh","exp"):
                    tp="competitor" if act=="exp" else "share"
                    s.sh.append({"rn":rn,"i":p["i"],"n":p["n"],"t":tp});rc["sh"]+=1
                elif act=="rp": s.rp.append({"rn":rn,"i":p["i"],"n":p["n"]});rc["rp"]+=1
                elif act=="md": s.md.append({"rn":rn,"n":p["n"],"f":p["f"]});rc["md"]+=1
        rc["sc"]=round(s.sc,1);rc["aw"]=sum(s.aw);s.rs.append(rc);return rc
    def run(s):
        print(f"[舆情危机v3] {s.n}人 {s.h}h 响应小组:{'ON' if s.team else 'OFF'}")
        s0=len([p for p in s.ps2 if p["rn"]==0])
        print(f"[舆情危机v3] 初始曝光: {s0}条\n")
        for r in range(1,s.R+1):
            rc=s._rr(r)
            ts=" | 响应:"+",".join(rc["ta"]) if rc["ta"] else ""
            print(f"[舆情危机v3] R{r}/{s.R}(~{rc['h']}h) 新+{rc['na']} 帖{rc['ps']}(负{rc['ng_tot']}/正{rc['ps_tot']}) 转{rc['sh']} 投{rc['rp']} 媒{rc['md']} 热度{rc['sc']}/100{ts}")
        return s._res()
    def _res(s):
        nc=len(s.ng);pc=len(s.ps3);tot=nc+pc
        npct=nc/tot if tot>0 else 0
        pol=round(abs(npct-.5)*2,2)
        top5=sorted(s.ng,key=lambda x:x.get("rk",0),reverse=True)[:5]
        tl=[(a["rn"],a["n"],a["e"]) for a in s.ta]
        return {"tp":"crisis","crisis":s.crisis,"n":s.n,"h":s.h,"R":s.R,
            "posts":s.ps2,"ng":s.ng,"ps3":s.ps3,"sh":s.sh,"rp":s.rp,"md":s.md,
            "recs":s.rs,"ta":s.ta,"inte":s.inte,
            "peak_rnd":max(s.rs,key=lambda x:x["sc"])["rn"] if s.rs else 0,
            "peak_sc":max(r["sc"] for r in s.rs) if s.rs else 0,
            "top5":[{"n":p["n"],"r":p["r"],"c":p["c"][:60],"rk":p.get("rk",0)} for p in top5],
            "tl":tl,"npct":round(npct*100,1),"pol":pol,
            "comp":sum(1 for x in s.sh if x.get("t")=="competitor")}

def show_promo(r):
    vk_v=r["vk"];pt=r["pess"];nt=r["neut"];ot=r["opt"]
    st=r["stock"];sb=r["sub"];vk_t=r["vk_tag"]
    aw=r["aw_rate"];kc=r["koc_p"];wl=r["wool"];cr=r["crowd"];bt=r["batch"]
    by_r=r["by_r"];dep=r.get("depleted_rnd")
    now=datetime.now().strftime("%Y-%m-%d %H:%M")
    d_str=" <-库存R"+str(dep)+"耗尽!" if dep else ""
    print()
    print("="*66)
    print("  七政-OASIS v3 爆款促销推演（传播系数K版）")
    print("  "+r["seed"])
    print("  "+now)
    print("="*66)
    print()
    print("  模拟："+str(r["n"])+"人 库存"+str(st)+"份 触达"+str(r["reach"])+"人")
    print("  传播系数：K="+str(vk_v)+" ("+vk_t+")")
    print("  促销价："+str(r["pp"])+"元（原价"+str(r["op"])+"元）售出"+str(r["sold"])+"份 知晓率"+str(aw)+"%")
    print()
    print("="*66)
    print("  订单量预测")
    print("="*66)
    print("  悲观 "+str(pt)+"单  亏损¥"+str(r["pess_l"]))
    print("  中性 "+str(nt)+"单  亏损¥"+str(r["neut_l"]))
    print("  乐观 "+str(ot)+"单  亏损¥"+str(r["opt_l"]))
    print("  每单补贴¥"+str(sb)+d_str)
    print()
    print("="*66)
    print("  各轮订单："+str(by_r))
    print()
    print("  风险：爆仓"+("高" if dep else "低")+" | KOC"+str(kc)+"帖 | 羊毛"+str(wl)+"人 | 随大流"+str(cr)+"人 | 批量"+str(bt)+"人")
    print("="*66)

def show_crisis(r):
    pk=r["peak_sc"];nc=r["npct"];pl=r["pol"]
    cp=r["comp"];it=r["inte"];tl=r["tl"];rs=r["recs"]
    risk="极高" if pk>80 else "高" if pk>60 else "中"
    now=datetime.now().strftime("%Y-%m-%d %H:%M")
    print()
    print("="*66)
    print("  七政-OASIS v3 舆情危机推演（响应小组版）")
    print("  "+r["crisis"])
    print("  "+now)
    print("="*66)
    print()
    print("  模拟："+str(r["n"])+"人 "+str(r["h"])+"h 干预"+str(it)+"轮")
    print("  帖子"+str(len(r["ng"])+len(r["ps3"]))+"条(负"+str(len(r["ng"]))+"/正"+str(len(r["ps3"]))+")")
    print("  转发"+str(len(r["sh"]))+" 投诉"+str(len(r["rp"]))+" 媒体"+str(len(r["md"])))
    print("  负面"+str(nc)+"% 极化指数"+str(pl)+" (>0.7=严重)")
    print()
    print("="*66)
    print("  舆情演化曲线（新华数据校准）")
    print("="*66)
    print("  峰值：R"+str(r["peak_rnd"])+" 热度"+str(pk)+"/100 风险:"+risk)
    if tl:
        items=", ".join("R"+str(rn)+":"+n+"(-"+str(e)+")" for rn,n,e in tl)
        print("  响应小组干预："+items)
    print("  各轮热度：")
    for rec in rs:
        bar=chr(9608)*int(rec["sc"]/5)+chr(9617)*(20-int(rec["sc"]/5))
        print("  R"+str(rec["rn"])+"(~"+str(rec["h"])+"h) ["+bar+"] "+str(rec["sc"]).rjust(5)+" | 负"+str(rec["ng_tot"])+"/正"+str(rec["ps_tot"]))
    print()
    print("="*66)
    print("  风险："+risk+" | 峰值"+str(pk)+"/100 | 竞品抢客"+str(cp)+"次")
    print("  投诉"+str(len(r["rp"]))+"次 | 媒体"+str(len(r["md"]))+"次")
    if r["top5"]:
        print()
        print("  高影响力帖子TOP5：")
        for i,p in enumerate(r["top5"],1):
            print("  "+str(i)+". ["+p["r"]+"/"+p["n"]+"] "+p["c"]+" (触达"+str(p["rk"])+"人)")
    nr=Counter(p["r"] for p in r["ng"]).most_common(5)
    pr2=Counter(p["r"] for p in r["ps3"]).most_common(3)
    print()
    print("  负面阵营TOP："+"/".join(a[0]+"("+str(a[1])+")" for a in nr))
    print("  正面阵营TOP："+"/".join(a[0]+"("+str(a[1])+")" for a in pr2))
    print()
    print("  建议：")
    if pk>60: print("  [扩散期] CEO道歉+第三方检测+媒体沟通")
    if pk>80: print("  [峰值期] 每日2次通报+补偿方案+投诉专线")
    if cp>0: print("  [全阶段] 竞品趁机抢客"+str(cp)+"次 -> 老客户专属补偿")
    if len(r["ta"])>0: print("  [有效] 响应小组已行动"+str(len(r["ta"]))+"次")
    print("="*66)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=["promo","crisis"],required=True)
    ap.add_argument("--scenario",default="成山农场蓝莓9.9爆款")
    ap.add_argument("--n",type=int,default=1000)
    ap.add_argument("--stock",type=int,default=500)
    ap.add_argument("--hours",type=int,default=24)
    ap.add_argument("--rounds",type=int,default=4)
    ap.add_argument("--op",type=float,default=26.0)
    ap.add_argument("--pp",type=float,default=9.9)
    ap.add_argument("--ptype",default="水果/生鲜")
    ap.add_argument("--team",default="true")
    ap.add_argument("--out",default="/workspace/data/qizheng-oasis/result_v3.json")
    a=ap.parse_args()
    os.makedirs("/workspace/data/qizheng-oasis",exist_ok=True)
    if a.mode=="promo":
        print("[天枢v3] 生成"+str(a.n)+"个角色...")
        ps=mp(a.n)
        print("[天权v3] 运行爆款促销推演...")
        w=PW(ps,a.scenario,a.stock,a.hours,a.rounds,a.op,a.pp,a.ptype)
        r=w.run()
        show_promo(r)
    else:
        team=a.team.lower()=="true"
        print("[天枢v3] 生成"+str(a.n)+"个舆情角色...")
        ps=mc(a.n)
        print("[天权v3] 运行舆情危机推演（响应小组:"+("ON" if team else "OFF")+"）...")
        w=CW(ps,a.scenario,a.hours,a.rounds,team)
        r=w.run()
        show_crisis(r)
    with open(a.out,"w",encoding="utf-8") as f:
        json.dump(r,f,ensure_ascii=False,indent=2)
    print()
    print("[完成] "+a.out)

if __name__=="__main__":
    main()
