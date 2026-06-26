#!/usr/bin/env python3
"""SBTI人格计算器：输入30题答案，输出匹配的人格类型。"""

import sys
import json
import math

# 15维度顺序
DIM_ORDER = ['S1','S2','S3','E1','E2','E3','A1','A2','A3','Ac1','Ac2','Ac3','So1','So2','So3']

# 题目到维度的映射（Q1-Q30）
Q_DIM = ['S1','S1','S2','S2','S3','S3','E1','E1','E2','E2','E3','E3','A1','A1','A2','A2','A3','A3','Ac1','Ac1','Ac2','Ac2','Ac3','Ac3','So1','So1','So2','So2','So3','So3']

# 27种人格类型：code -> pattern
TYPES = {
    'CTRL': 'HHH-HMH-MHH-HHH-MHM',
    'ATM':  'HHH-HHM-HHH-HMH-MHL',
    'DIOS': 'MHM-MMH-MHM-HMH-LHL',
    'BOSS': 'HHH-HMH-MMH-HHH-LHL',
    'THAN': 'MHM-HMM-HHM-MMH-MHL',
    'OHNO': 'HHL-LMH-LHH-HHM-LHL',
    'GOGO': 'HHM-HMH-MMH-HHH-MHM',
    'SEXY': 'HMH-HHL-HMM-HMM-HLH',
    'LOVR': 'MLH-LHL-HLH-MLM-MLH',
    'MUM':  'MMH-MHL-HMM-LMM-HLL',
    'FAKE': 'HLM-MML-MLM-MLM-HLH',
    'OJBK': 'MMH-MMM-HHH-MMM-MMM',
    'MALO': 'MLM-LML-HLM-LMM-HML',
    'JOKR': 'MLM-MML-MLH-MML-LHL',
    'WOC':  'LML-HLM-LML-HML-MLM',
    'THNK': 'LHL-MLM-LHH-HLM-MLH',
    'SHIT': 'MLH-HMM-LML-MLM-HLL',
    'ZZZZ': 'MMM-LLM-LML-LMM-LLL',
    'POOR': 'LMM-LHL-MML-MMM-HML',
    'MONK': 'LML-MLL-LHL-MLL-HLL',
    'IMSB': 'LHL-LML-MHL-MLL-HML',
    'SOLO': 'LML-HLL-LML-HML-LHL',
    'FUCK': 'MLH-LLM-HML-LLM-MHL',
    'DEAD': 'LLL-LLL-LLL-LLL-LLL',
    'IMFW': 'LLL-LML-LLL-LLM-LML',
    'HHHH': 'HHH-HHH-HHH-HHH-HHH',
}

TYPE_NAMES = {
    'CTRL':'拿捏者','ATM':'送钱者','DIOS':'屌丝','BOSS':'领导者',
    'THAN':'感恩者','OHNO':'哦不人','GOGO':'行者','SEXY':'尤物',
    'LOVR':'多情者','MUM':'妈妈','FAKE':'伪人','OJBK':'无所谓人',
    'MALO':'吗喽','JOKR':'小丑','WOC':'握草人','THNK':'思考者',
    'SHIT':'愤世者','ZZZZ':'装死者','POOR':'贫困者','MONK':'僧人',
    'IMSB':'傻者','SOLO':'孤儿','FUCK':'草者','DEAD':'死者',
    'IMFW':'废物','HHHH':'傻乐者','DRUNK':'酒鬼🥂',
}

TYPE_INTROS = {
    'CTRL':'怎么样，被我拿捏了吧？','ATM':'你以为我很有钱吗？',
    'DIOS':'等着我屌丝逆袭。','BOSS':'方向盘给我，我来开。',
    'THAN':'我感谢苍天！我感谢大地！','OHNO':'哦不！我怎么会是这个人格？！',
    'GOGO':'gogogo~出发咯','SEXY':'您就是天生的尤物！',
    'LOVR':'爱意太满，现实显得有点贫瘠。','MUM':'或许...我可以叫你妈妈吗....?',
    'FAKE':'已经，没有人类了。','OJBK':'我说随便，是真的随便。',
    'MALO':'人生是个副本，而我只是一只吗喽。','JOKR':'原来我们都是小丑。',
    'WOC':'卧槽，我怎么是这个人格？','THNK':'已深度思考100s。',
    'SHIT':'这个世界，构石一坨。','ZZZZ':'我没死，我只是在睡觉。',
    'POOR':'我穷，但我很专。','MONK':'没有那种世俗的欲望。',
    'IMSB':'认真的么？我真的是傻逼么？','SOLO':'我哭了，我怎么会是孤儿？',
    'FUCK':'操！这是什么人格？','DEAD':'我，还活着吗？',
    'IMFW':'我真的...是废物吗？','HHHH':'哈哈哈哈哈哈。',
    'DRUNK':'烈酒烧喉，不得不醉。',
}

DIM_NAMES = {
    'S1':'自尊自信','S2':'自我清晰度','S3':'核心价值',
    'E1':'依恋安全感','E2':'情感投入度','E3':'边界与依赖',
    'A1':'世界观倾向','A2':'冒险精神','A3':'目标感',
    'Ac1':'行动力','Ac2':'果断性','Ac3':'执行力',
    'So1':'社交主动性','So2':'亲密需求','So3':'自我呈现',
}

DIM_MODELS = {
    'S1':'自我模型','S2':'自我模型','S3':'自我模型',
    'E1':'情感模型','E2':'情感模型','E3':'情感模型',
    'A1':'态度模型','A2':'态度模型','A3':'态度模型',
    'Ac1':'行动模型','Ac2':'行动模型','Ac3':'行动模型',
    'So1':'社交模型','So2':'社交模型','So3':'社交模型',
}

def score_to_level(score):
    if score <= 3:
        return 'L'
    elif score == 4:
        return 'M'
    else:
        return 'H'

def level_to_num(level):
    return {'L':1,'M':2,'H':3}[level]

def parse_pattern(pattern):
    return pattern.replace('-','')

def calculate(answers_str):
    # Parse answers
    answers = [int(x.strip()) for x in answers_str.split(',')]
    if len(answers) != 30:
        return {'error': f'需要30个答案，收到{len(answers)}个'}

    # Calculate dimension scores
    dim_scores = {}
    for i, a in enumerate(answers):
        dim = Q_DIM[i]
        dim_scores[dim] = dim_scores.get(dim, 0) + a

    # Convert to levels
    levels = {dim: score_to_level(score) for dim, score in dim_scores.items()}

    # Build user vector
    user_vector = [level_to_num(levels[dim]) for dim in DIM_ORDER]

    # Find closest type
    best_match = None
    min_distance = float('inf')

    for code, pattern in TYPES.items():
        type_vector = [level_to_num(c) for c in parse_pattern(pattern)]
        distance = sum(abs(user_vector[i] - type_vector[i]) for i in range(15))
        exact = sum(1 for i in range(15) if user_vector[i] == type_vector[i])
        similarity = max(0, round((1 - distance / 30) * 100))

        if distance < min_distance:
            min_distance = distance
            best_match = {
                'code': code,
                'name': TYPE_NAMES.get(code, code),
                'intro': TYPE_INTROS.get(code, ''),
                'distance': distance,
                'exact': exact,
                'similarity': similarity,
            }

    # Build result
    result = {
        'type': best_match,
        'dimensions': {},
        'user_pattern': '-'.join([''.join(levels[d] for d in DIM_ORDER[i*3:(i+1)*3]) for i in range(5)]),
        'ranked': [],
    }

    # Add dimension details
    for dim in DIM_ORDER:
        result['dimensions'][dim] = {
            'name': DIM_NAMES[dim],
            'model': DIM_MODELS[dim],
            'score': dim_scores[dim],
            'level': levels[dim],
        }

    # Rank top 5
    ranked = []
    for code, pattern in TYPES.items():
        type_vector = [level_to_num(c) for c in parse_pattern(pattern)]
        distance = sum(abs(user_vector[i] - type_vector[i]) for i in range(15))
        exact = sum(1 for i in range(15) if user_vector[i] == type_vector[i])
        similarity = max(0, round((1 - distance / 30) * 100))
        ranked.append({
            'code': code,
            'name': TYPE_NAMES.get(code, code),
            'distance': distance,
            'similarity': similarity,
        })
    ranked.sort(key=lambda x: x['distance'])
    result['ranked'] = ranked[:5]

    return result

def format_output(result):
    if 'error' in result:
        return f"❌ {result['error']}"

    t = result['type']
    lines = [
        f"🎉 SBTI人格：{t['code']} {t['name']}",
        f"💬 {t['intro']}",
        f"📊 匹配度：{t['similarity']}% | 完全匹配维度：{t['exact']}/15",
        f"🎯 你的Pattern：{result['user_pattern']}",
        "",
        "📐 十五维度评分：",
    ]

    # Group by model
    current_model = ''
    for dim in DIM_ORDER:
        d = result['dimensions'][dim]
        model = d['model']
        if model != current_model:
            lines.append(f"\n【{model}】")
            current_model = model
        bar = {'L':'░░','M':'▓░','H':'▓▓'}[d['level']]
        lines.append(f"  {dim} {d['name']}: {bar} {d['score']}/6 ({d['level']})")

    lines.append(f"\n🏅 Top 5匹配：")
    for i, r in enumerate(result['ranked']):
        marker = "👉 " if i == 0 else f"  {i+1}. "
        lines.append(f"{marker}{r['code']} {r['name']} ({r['similarity']}%)")

    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 calculate.py \"3,2,1,3,2,1,...\" (30个答案，逗号分隔)")
        sys.exit(1)

    result = calculate(sys.argv[1])
    print(format_output(result))
