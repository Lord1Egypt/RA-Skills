#!/usr/bin/env python3
"""
Step2: 仿真引擎（天权）
OASIS三层模型驱动：
  Micro（个体决策）→ Meso（社交网络）→ Macro（宏观涌现）
用法:
  python3 run_simulation.py --profiles profiles.json --rounds 3 --seed "种子事件"
"""

import json
import argparse
import os
import random
import urllib.request
from datetime import datetime
from collections import defaultdict

# ── 凭证 ──────────────────────────────────────────────
def load_credentials():
    cred_path = '/workspace/.credentials/siliconflow-api.txt'
    if os.path.exists(cred_path):
        with open(cred_path) as f:
            return f.read().strip()
    return os.environ.get('SILICONFLOW_API_KEY', '')

SILICONFLOW_KEY = load_credentials()
SILICONFLOW_URL = 'https://api.siliconflow.cn/v1/chat/completions'

# ── 仿真状态 ──────────────────────────────────────────
class OASISWorld:
    """OASIS仿真世界的核心状态"""

    def __init__(self, profiles: list, seed_event: str):
        self.profiles = profiles
        self.seed_event = seed_event
        self.n = len(profiles)

        # Social Graph（Meso层）
        self.follow_graph = defaultdict(set)  # agent_id -> set of followed agent_ids
        self.influence_weight = defaultdict(float)  # agent_id -> 被多少真实用户follow
        self._build_social_graph()

        # Action History（宏观记录）
        self.round_records = []
        self.posts = []  # 产生的帖子/评价
        self.orders = []  # 订单记录
        self.shares = []  # 转发记录
        self.awareness = [False] * self.n  # 是否已知晓此事件
        self.ordered = [False] * self.n      # 是否已下单（防止重复下单）

        # 第一轮：KOC知晓
        for i, p in enumerate(profiles):
            if p['role_type'] == 'KOC种草型':
                self.awareness[i] = True
                self.posts.append({
                    'round': 0,
                    'agent_id': i,
                    'agent_name': p['name'],
                    'role': p['role_type'],
                    'type': 'seed_post',
                    'content': f"【爆款上新】{seed_event}",
                    'influence': p['influence_score'],
                    'engagement': 0
                })

    def _build_social_graph(self):
        """构建社交网络（Meso层）：按角色类型建立follow关系"""
        for i, p in enumerate(self.profiles):
            rt = p['role_type']
            inf = p['influence_score']

            if rt == 'KOC种草型':
                # KOC被所有人follow
                for j in range(self.n):
                    if j != i:
                        self.follow_graph[j].add(i)
                self.influence_weight[i] = inf * 10

            elif rt == '忠实复购型':
                # 复购型有小圈子，被其他复购和精准型follow
                for j, pj in enumerate(self.profiles):
                    if j != i and pj['role_type'] in ['忠实复购型', '精准需求型']:
                        if random.random() < 0.3:
                            self.follow_graph[j].add(i)

            elif rt == '随大流型':
                # 随大流型follow精准需求型和KOC
                for j, pj in enumerate(self.profiles):
                    if pj['role_type'] in ['KOC种草型', '精准需求型', '忠实复购型']:
                        if random.random() < 0.4:
                            self.follow_graph[j].add(i)

            else:
                # 普通用户随机follow
                for j in range(self.n):
                    if j != i and random.random() < 0.1:
                        self.follow_graph[j].add(i)

    def get_aware_agents(self, round_num: int) -> list:
        """获取第round_num轮新知晓的agent"""
        aware = []
        for i in range(self.n):
            if self.awareness[i]:
                aware.append(i)
        return aware

    def spread_via_social_graph(self):
        """信息通过社交网络扩散（Meso层传导）"""
        newly_aware = []
        current_round = len(self.round_records)
        # 当前轮已发帖的人
        current_round_posters = {p['agent_id'] for p in self.posts if p['round'] == current_round}

        for i in range(self.n):
            if not self.awareness[i]:
                followers = self.follow_graph.get(i, set())
                # 如果我follow的人里有在本轮发帖的，我就知道这件事了
                if followers & current_round_posters:
                    newly_aware.append(i)

        # 热门帖子引发随机知晓（非关注链，模拟算法推荐）
        hot_posts = [p for p in self.posts if p.get('engagement', 0) > 2]
        if hot_posts and random.random() < 0.15:
            cold_agents = [i for i in range(self.n) if not self.awareness[i]]
            if cold_agents:
                newly_aware.append(random.choice(cold_agents))

        for i in set(newly_aware):
            self.awareness[i] = True
        return list(set(newly_aware))

    def run_round(self, round_num: int) -> dict:
        """运行单轮仿真（Micro层：每个aware agent做决策）"""
        record = {
            'round': round_num,
            'posts': [],
            'orders': [],
            'shares': [],
            'newly_aware_count': 0,
            'total_aware': sum(self.awareness)
        }

        # 社交扩散
        new_aware = self.spread_via_social_graph()
        record['newly_aware_count'] = len(new_aware)

        # 每个aware agent做决策
        for i, p in enumerate(self.profiles):
            if not self.awareness[i]:
                continue

            action = self._agent_decision(p, round_num)
            if not action:
                continue

            if action['type'] == 'post':
                self.posts.append({**action, 'round': round_num})
                record['posts'].append(action)
            elif action['type'] == 'order':
                # 防重复下单：每人每场景最多1单
                if not self.ordered[action['agent_id']]:
                    self.ordered[action['agent_id']] = True
                    self.orders.append({**action, 'round': round_num})
                    record['orders'].append(action)
            elif action['type'] == 'share':
                self.shares.append({**action, 'round': round_num})
                record['shares'].append(action)

        self.round_records.append(record)
        return record

    def _agent_decision(self, profile: dict, round_num: int) -> dict | None:
        """Micro层：单个agent的决策逻辑（规则+LLM混合）"""
        role = profile['role_type']
        inf = profile['influence_score']
        action_prob = profile['action_prob']

        # 基础行动概率（随轮次衰减或增强）
        round_factor = 1.0 if round_num == 0 else (1.2 if round_num == 1 else 0.9)

        # ── 帖子内容库（从seed_event动态生成）────────────────
        # 从seed中提取关键信息
        seed = self.seed_event
        # 生成通用内容模板
        post_templates = {
            'KOC种草型': [
                f"买了！{seed}，这价格真的绝",
                f"刚抢到，{seed}，质量很好已经到手了",
                f"【爆款上新】{seed}",
            ],
            '精准需求型': [
                f"正好需要，下单了，试试看",
                f"下单了，看评价不错，先买一份试试",
                f"{seed}，有机品质这个价格很划算，买了",
            ],
            '羊毛党型': [
                f"{seed}，已下单！手慢无",
                f"速度冲！{seed}，限时抢",
                f"又蹲到一个好价，已购入",
            ],
            '随大流型': [
                f"群里好多人买，我也来一份试试",
                f"看到大家都买，我也买一单",
                f"朋友推荐，买了试试",
            ],
            '忠实复购型': [
                f"成山农场新品已下单，老顾客放心买",
                f"回购第三年了，新品必须支持",
                f"成山农场出品，必属精品",
            ]
        }

        # ── 决策树（规则优先，快速返回）──────────────
        if role == 'KOC种草型':
            # KOC几乎必定发帖，不一定下单
            if random.random() < 0.85:
                return {
                    'type': 'post',
                    'agent_id': profile['agent_id'],
                    'agent_name': profile['name'],
                    'role': role,
                    'content': random.choice(post_templates.get(role, ['已购买'])),
                    'influence': inf,
                    'engagement': 0
                }
            if random.random() < profile['latent_demand'] * 0.5:
                return {
                    'type': 'order',
                    'agent_id': profile['agent_id'],
                    'agent_name': profile['name'],
                    'role': role,
                    'quantity': random.choice([1, 2])
                }

        elif role == '羊毛党型':
            # 羊毛党快速下单，可能顺手发帖
            if random.random() < action_prob * round_factor:
                order = {
                    'type': 'order',
                    'agent_id': profile['agent_id'],
                    'agent_name': profile['name'],
                    'role': role,
                    'quantity': random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
                }
                if random.random() < 0.4:
                    return {
                        'type': 'post',
                        'agent_id': profile['agent_id'],
                        'agent_name': profile['name'],
                        'role': role,
                        'content': random.choice(post_templates.get(role, ['已下单'])),
                        'influence': inf,
                        'engagement': 0
                    }
                return order

        elif role == '精准需求型':
            # 精准需求型看帖子后决定是否下单
            relevant_posts = [p for p in self.posts if p.get('engagement', 0) > 0 or p['role'] in ['KOC种草型', '忠实复购型']]
            if relevant_posts or random.random() < 0.2:
                if random.random() < action_prob * round_factor:
                    return {
                        'type': 'order',
                        'agent_id': profile['agent_id'],
                        'agent_name': profile['name'],
                        'role': role,
                        'quantity': random.choices([1, 2], weights=[0.7, 0.3])[0]
                    }
                elif random.random() < 0.3:
                    return {
                        'type': 'share',
                        'agent_id': profile['agent_id'],
                        'agent_name': profile['name'],
                        'role': role,
                        'to_group': True
                    }

        elif role == '随大流型':
            # 随大流型：看购买人数决定
            order_count = len(self.orders)
            social_signal = min(order_count / 30, 1.0)
            effective_prob = min(action_prob + social_signal * 0.4, 1.0)
            if random.random() < effective_prob:
                if order_count > 5 and random.random() < 0.5:
                    return {
                        'type': 'order',
                        'agent_id': profile['agent_id'],
                        'agent_name': profile['name'],
                        'role': role,
                        'quantity': 1
                    }

        elif role == '忠实复购型':
            if random.random() < action_prob * round_factor:
                return {
                    'type': 'order',
                    'agent_id': profile['agent_id'],
                    'agent_name': profile['name'],
                    'role': role,
                    'quantity': random.choice([1, 2])
                }
                if random.random() < 0.4:
                    return {
                        'type': 'post',
                        'agent_id': profile['agent_id'],
                        'agent_name': profile['name'],
                        'role': role,
                        'content': random.choice(post_templates.get(role, ['复购支持'])),
                        'influence': inf,
                        'engagement': 0
                    }

        elif role == '竞品比价型':
            # 比价型：犹豫，等待更多信息
            if round_num >= 2 and random.random() < action_prob * 0.5:
                return {
                    'type': 'order',
                    'agent_id': profile['agent_id'],
                    'agent_name': profile['name'],
                    'role': role,
                    'quantity': 1
                }

        return None

    def boost_engagement(self):
        """宏观涌现：帖子互动量更新（模拟社会认同效应）"""
        for post in self.posts:
            # 后续随大流型用户的加入会推高KOC帖子的互动
            orderers_in_network = sum(
                1 for o in self.orders
                if o['agent_id'] in self.follow_graph.get(post['agent_id'], set())
            )
            post['engagement'] = orderers_in_network


def llm_analyze_round(world: OASISWorld, round_num: int, round_record: dict) -> str:
    """用LLM分析本轮涌现情况，给出宏观判断"""
    if not SILICONFLOW_KEY:
        return ""

    import urllib.request

    summary = f"第{round_num}轮：" \
              f"发帖{len(round_record['posts'])}条，" \
              f"订单{len(round_record['orders'])}单，" \
              f"转发{len(round_record['shares'])}次，" \
              f"新增知晓{round_record['newly_aware_count']}人，" \
              f"总知晓率{world.awareness.count(True)}/{world.n}"

    prompt = f"""你是市场分析师。以下是OASIS模拟仿真第{round_num}轮的数据：

{summary}

当前总订单：{len(world.orders)}单
总发帖：{len(world.posts)}条
社交网络传播率：{world.awareness.count(True)}/{world.n}

请分析：
1. 当前处于什么传播阶段？（初期/爆发/饱和/衰退）
2. 是否有羊群效应正在形成？（是/否，理由）
3. 还需要注意什么风险？

回复简短（≤50字），直接给出分析结论。"""

    try:
        payload = json.dumps({
            "model": "Qwen/Qwen2.5-7B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 256
        }).encode()

        req = urllib.request.Request(
            SILICONFLOW_URL,
            data=payload,
            headers={'Authorization': f'Bearer {SILICONFLOW_KEY}', 'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result['choices'][0]['message']['content'].strip()
    except Exception:
        return ""


def run_simulation(profiles: list, seed_event: str, rounds: int) -> dict:
    """运行完整仿真"""
    world = OASISWorld(profiles, seed_event)

    print(f"[天权] 仿真启动：{len(profiles)}个角色，{rounds}轮")
    print(f"[天权] 种子事件：{seed_event}")
    print(f"[天权] KOC初始发帖：{len(world.posts)}条")

    for r in range(1, rounds + 1):
        print(f"\n[天权] ── 第 {r}/{rounds} 轮 ──")
        record = world.run_round(r)
        world.boost_engagement()

        print(f"  发帖: {len(record['posts'])} | 订单: {len(record['orders'])} | "
              f"转发: {len(record['shares'])} | 新知晓: {record['newly_aware_count']}")

        if SILICONFLOW_KEY:
            insight = llm_analyze_round(world, r, record)
            if insight:
                print(f"  📊 {insight}")

    return {
        'seed_event': seed_event,
        'n_agents': len(profiles),
        'n_rounds': rounds,
        'posts': world.posts,
        'orders': world.orders,
        'shares': world.shares,
        'round_records': world.round_records,
        'final_awareness': world.awareness.count(True),
        'profiles': profiles
    }


def main():
    parser = argparse.ArgumentParser(description='天权·OASIS仿真引擎')
    parser.add_argument('--profiles', required=True, help='角色Profile JSON')
    parser.add_argument('--rounds', type=int, default=3, help='仿真轮次')
    parser.add_argument('--seed', required=True, help='种子事件')
    parser.add_argument('--output', required=True, help='输出路径')
    args = parser.parse_args()

    with open(args.profiles, encoding='utf-8') as f:
        data = json.load(f)

    profiles = data['profiles']
    result = run_simulation(profiles, args.seed, args.rounds)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 打印摘要
    total_orders = len(result['orders'])
    total_posts = len(result['posts'])
    awareness_rate = result['final_awareness'] / result['n_agents'] * 100

    print(f"\n[天权] ✅ 仿真完成")
    print(f"[天权] 总订单：{total_orders} | 总发帖：{total_posts} | 知晓率：{awareness_rate:.1f}%")
    print(f"[天权] 已保存：{args.output}")


if __name__ == '__main__':
    main()
