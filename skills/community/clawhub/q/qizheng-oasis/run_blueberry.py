#!/usr/bin/env python3
"""
成山农场蓝莓9.9元爆款 - 一键推演脚本
跳过LLM，直接用规则生成profile + 仿真 + 分析
"""
import json, random, os, subprocess
from datetime import datetime

os.makedirs('/workspace/data/qizheng-oasis', exist_ok=True)

# ── 角色生成（规则版，无LLM）──────────────────────────────
blueprints = [
    {"role": "KOC种草型",     "count": 15, "inf": 2.0, "prob": 0.85, "demand": 1,
     "mbti": ["ENFJ","ESFP","ENTP","ENFP"],
     "triggers": ["低价","新鲜","健康","宝宝辅食"],
     "barriers": ["品质不确定","物流怕坏"]},
    {"role": "精准需求型",    "count": 25, "inf": 0.8, "prob": 0.70, "demand": 2,
     "mbti": ["ISFJ","ISTJ","ESFJ","INFJ"],
     "triggers": ["花青素","护眼","有机","宝宝爱吃蓝莓"],
     "barriers": ["价格不够低","怕酸"]},
    {"role": "羊毛党型",      "count": 20, "inf": 0.9, "prob": 0.88, "demand": 1,
     "mbti": ["ESTP","ESFP","ENTP","ISTP"],
     "triggers": ["绝对低价","限时","囤货"],
     "barriers": ["要拉人才能优惠","怕吃不完"]},
    {"role": "随大流型",      "count": 15, "inf": 0.6, "prob": 0.50, "demand": 1,
     "mbti": ["ESFJ","ISFJ","ENFJ","INFJ"],
     "triggers": ["朋友圈多人买","KOC推荐","群里下单截图"],
     "barriers": ["不知道值不值","没吃过蓝莓"]},
    {"role": "竞品比价型",    "count": 10, "inf": 0.5, "prob": 0.35, "demand": 0,
     "mbti": ["INTJ","INTP","ISTJ","INFJ"],
     "triggers": ["全网最低价","确认品质"],
     "barriers": ["超市更便宜","进口蓝莓更好"]},
    {"role": "冷淡对照组",    "count": 5,  "inf": 0.2, "prob": 0.08, "demand": 0,
     "mbti": ["INTP","INTJ","ISTP"],
     "triggers": ["刚好需要","价格低到离谱"],
     "barriers": ["不感兴趣","不信任网购生鲜"]},
    {"role": "忠实复购型",    "count": 10, "inf": 1.2, "prob": 0.82, "demand": 2,
     "mbti": ["ISFJ","ESFJ","ENFJ","ISTJ"],
     "triggers": ["成山出品必买","护眼营养","孩子爱吃"],
     "barriers": ["价格比上次贵","口感不稳定"]},
]

# 蓝莓专属背景池
blueberry_backgrounds = {
    "KOC种草型":     ["全职妈妈，200人购物群","社区团购群主500人","美食博主1万粉","小区便利店老板娘"],
    "精准需求型":    ["二宝妈妈，大宝5岁","孩子上小学，用眼多要护眼","白领，每天盯电脑8小时","退休老人，养生达人"],
    "羊毛党型":      ["某平台羊毛群，日均3单","上班族，午休抢优惠","退休大爷，研究各种券","大学生，预算有限"],
    "随大流型":      ["普通白领，购物看心情","家庭主妇，朋友推啥买啥","年轻情侣，跟风消费","朋友圈微商代理"],
    "竞品比价型":    ["采购经理，专业比价","IT工程师，购物前必做攻略","财务，精打细算","开店老板，进货比价"],
    "冷淡对照组":    ["独居老人，不会用智能手机","极简主义者，只买必需品","公务员，对网购无感","学生，没兴趣"],
    "忠实复购型":    ["成山老客户，买过5次以上","社区会员，介绍10个邻居","有机食品爱好者","健康饮食践行者"],
}

names_pool = ["小林","小王","阿杰","小赵","老李","阿芳","阿华","小陈","阿强","小美",
               "阿伟","小雪","阿峰","小霞","阿龙","小慧","阿超","小燕","阿鹏","小琴",
               "阿勇","小萍","阿林","小英","阿坤","小娜","阿军","小莲","阿东","小燕",
               "阿辉","小凤","阿祥","小云","阿健","小红","阿凯","小青","阿宇","小霞",
               "阿飞","小洁","阿龙","小玲","阿旭","阿睿","小雨","阿天","小萌","阿然",
               "阿博","小泽","阿晖","小颖","阿鑫","小倩","阿琪","阿豪","小雅","阿杰"]

profiles = []
idx = 0
for bp in blueprints:
    for _ in range(bp['count']):
        name = random.choice(names_pool) + str(random.randint(1,99))
        bgs = blueberry_backgrounds.get(bp['role'], ["普通消费者"])
        profiles.append({
            "agent_id": idx,
            "role_type": bp['role'],
            "name": name,
            "age": random.randint(22, 55),
            "gender": random.choice(["男", "女"]),
            "mbti": random.choice(bp['mbti']),
            "personality": list(bp['triggers'][:3]),
            "background": random.choice(bgs),
            "trigger_words": bp['triggers'],
            "barrier_words": bp['barriers'],
            "influence_score": round(bp['inf'] * random.uniform(0.85, 1.15), 2),
            "action_prob": round(min(bp['prob'] * random.uniform(0.9, 1.1), 1.0), 2),
            "latent_demand": bp['demand']
        })
        idx += 1

random.shuffle(profiles)
for i, p in enumerate(profiles): p['agent_id'] = i

profiles_data = {
    "scenario": "成山农场蓝莓9.9元/斤爆款促销",
    "generated_at": datetime.now().isoformat(),
    "n_agents": len(profiles),
    "profiles": profiles
}

with open('/workspace/data/qizheng-oasis/profiles_blueberry.json', 'w', encoding='utf-8') as f:
    json.dump(profiles_data, f, ensure_ascii=False, indent=2)
print(f"[天枢] ✅ 100个角色生成完毕: {profiles_data['n_agents']}人")

# ── 仿真 ─────────────────────────────────────────────
r2 = subprocess.run(
    ['python3', '/workspace/skills/qizheng-oasis/run_simulation.py',
     '--profiles', '/workspace/data/qizheng-oasis/profiles_blueberry.json',
     '--rounds', '3',
     '--seed', '成山农场蓝莓上新·9.9元/斤·限时抢，限500份',
     '--output', '/workspace/data/qizheng-oasis/result_blueberry.json'],
    capture_output=True, text=True, timeout=55
)
lines = r2.stdout.strip().split('\n')
print("STEP2:", '\n'.join(lines[-18:]))
if r2.returncode != 0: print("ERR:", r2.stderr[-200:])

# ── 分析 ─────────────────────────────────────────────
r3 = subprocess.run(
    ['python3', '/workspace/skills/qizheng-oasis/analyze.py',
     '--result', '/workspace/data/qizheng-oasis/result_blueberry.json'],
    capture_output=True, text=True, timeout=15
)
print(r3.stdout)
if r3.returncode != 0: print("ANA ERR:", r3.stderr[-200:])

with open('/workspace/data/qizheng-oasis/report_blueberry.txt', 'w', encoding='utf-8') as f:
    f.write(r3.stdout)
print("[完成] /workspace/data/qizheng-oasis/report_blueberry.txt")
