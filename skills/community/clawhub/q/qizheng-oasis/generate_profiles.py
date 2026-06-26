#!/usr/bin/env python3
"""
Step1: 角色生成器（天枢）
输入场景描述 → 生成100个Agent Profile
用法:
  python3 generate_profiles.py --scenario "成山农场9.9元/斤虾爆款" --n_agents 100
"""

import json
import argparse
import random
import os
from datetime import datetime

# ── 凭证读取 ──────────────────────────────────────────
def load_credentials():
    """读取SiliconFlow API Key"""
    cred_path = '/workspace/.credentials/siliconflow-api.txt'
    if os.path.exists(cred_path):
        with open(cred_path) as f:
            return f.read().strip()
    return os.environ.get('SILICONFLOW_API_KEY', '')

SILICONFLOW_KEY = load_credentials()
SILICONFLOW_URL = 'https://api.siliconflow.cn/v1/chat/completions'

# ── Blueprint 加载 ────────────────────────────────────
def load_blueprints():
    with open('/workspace/skills/qizheng-oasis/configs/agent_blueprints.json') as f:
        return json.load(f)

# ── Profile 生成 ──────────────────────────────────────
def generate_profiles_via_llm(scenario: str, n_agents: int, blueprints: list) -> list:
    """用LLM一次性生成100个角色的详细画像"""
    import urllib.request

    # 构建角色分布说明
    role_dist = []
    for bp in blueprints:
        role_dist.append(f"  - {bp['role']}：{bp['count']}人，特征：{','.join(bp['traits'])}，购买触发词：{bp['buying_triggers']}")

    prompt = f"""你是一个用户画像生成器。请根据以下场景，生成{n_agents}个真实买家角色。

场景：{scenario}

角色类型分布（共{n_agents}人）：
{chr(10).join(role_dist)}

请为每个角色生成一个JSON对象，字段如下：
- agent_id: 编号 0~{n_agents-1}
- role_type: 角色类型（从上面7种选一个，按比例分布）
- name: 中文昵称，要自然真实
- age: 年龄 22~55
- gender: 男/女
- mbti: MBTI类型（从对应分布中选）
- personality: 3个关键词描述性格
- background: 一句话描述背景（如：家有小学生的白领/退休老人/微商代理）
- trigger_words: 最能打动这个人的3个词
- barrier_words: 最阻碍购买的因素
- influence_score: 影响力 0.1~2.0（KOC类给2.0，普通买家0.5~0.8）
- action_prob: 看到这个促销后采取行动的初始概率 0.0~1.0
- latent_demand: 是否有潜在需求（0=不需要，1=可买可不买，2=强烈需求）

输出要求：
1. 严格按照角色类型比例分布
2. 每个角色要独特、有差异，避免重复
3. 以JSON数组形式输出，不要加markdown代码块，只输出纯JSON
"""

    payload = json.dumps({
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
        "max_tokens": 8192
    }).encode()

    req = urllib.request.Request(
        SILICONFLOW_URL,
        data=payload,
        headers={
            'Authorization': f'Bearer {SILICONFLOW_KEY}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())
        content = result['choices'][0]['message']['content'].strip()
        # 尝试去掉可能的markdown包装
        if content.startswith('```'):
            lines = content.split('\n')
            content = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])
        return json.loads(content)


def generate_profiles_fallback(scenario: str, n_agents: int, blueprints: list) -> list:
    """如果LLM调用失败，使用规则生成"""
    profiles = []
    idx = 0
    for bp in blueprints:
        for _ in range(bp['count']):
            profiles.append({
                "agent_id": idx,
                "role_type": bp['role'],
                "name": f"用户{idx+1}",
                "age": random.randint(22, 55),
                "gender": random.choice(["男", "女"]),
                "mbti": random.choice(bp['mbti_distribution']),
                "personality": bp['traits'][:3],
                "background": f"普通买家，特征：{bp['traits'][0]}",
                "trigger_words": bp['buying_triggers'][:3],
                "barrier_words": bp['buying_barriers'][:2],
                "influence_score": bp['influence'],
                "action_prob": bp['activation_prob'],
                "latent_demand": 1 if bp['activation_prob'] > 0.6 else 0
            })
            idx += 1
    return profiles[:n_agents]


def main():
    parser = argparse.ArgumentParser(description='天枢·角色生成器')
    parser.add_argument('--scenario', required=True, help='场景描述')
    parser.add_argument('--n_agents', type=int, default=100, help='角色数量')
    parser.add_argument('--output', required=True, help='输出JSON路径')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    blueprints = load_blueprints()
    print(f"[天枢] 场景：{args.scenario}")
    print(f"[天枢] 生成 {args.n_agents} 个角色...")

    try:
        profiles = generate_profiles_via_llm(args.scenario, args.n_agents, blueprints)
        print(f"[天枢] LLM生成完成，共 {len(profiles)} 个角色")
    except Exception as e:
        print(f"[天枢] LLM调用失败({e})，使用规则生成...")
        profiles = generate_profiles_fallback(args.scenario, args.n_agents, blueprints)

    # 保存
    output_data = {
        "scenario": args.scenario,
        "generated_at": datetime.now().isoformat(),
        "n_agents": len(profiles),
        "profiles": profiles
    }
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    # 统计
    from collections import Counter
    role_counts = Counter(p['role_type'] for p in profiles)
    print(f"[天枢] 角色分布：{dict(role_counts)}")
    print(f"[天枢] 已保存至：{args.output}")

if __name__ == '__main__':
    main()
