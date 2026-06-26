#!/usr/bin/env python3
"""
圆桌论坛技能 - 核心引擎
Roundtable Forum - Core Engine

构建以"求真"为目标的结构化对话框架
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================
# 预置代表人物库
# ============================================================

PRESET_REPRESENTATIVES = {
    "艾伦·图灵": {
        "field": "计算机科学",
        "mbti": "INTJ",
        "stance": "计算主义：创造力是复杂计算的涌现",
        "keywords": ["计算", "算法", "图灵测试", "人工智能"]
    },
    "约翰·塞尔": {
        "field": "哲学",
        "mbti": "ISTJ",
        "stance": "意识本质论：真正的创造力需要生物意识和意向性",
        "keywords": ["意识", "意向性", "中文房间", "生物自然主义"]
    },
    "玛格丽特·博登": {
        "field": "创造力研究",
        "mbti": "ENFP",
        "stance": "生物创造力：创造力是生物系统的独特属性",
        "keywords": ["创造力", "生物系统", "演化", "新颖性"]
    },
    "凯文·凯利": {
        "field": "技术演化",
        "mbti": "ENTP",
        "stance": "技术必然论：技术演化必然产生创造性",
        "keywords": ["技术演化", "必然性", "涌现", "复杂系统"]
    },
    "丹尼尔·丹尼特": {
        "field": "认知科学",
        "mbti": "ENTP",
        "stance": "多重草稿模型：意识是并行处理的产物",
        "keywords": ["意识", "多重草稿", "演化", "功能主义"]
    },
    "大卫·查尔莫斯": {
        "field": "心灵哲学",
        "mbti": "INFJ",
        "stance": "硬问题论证：意识体验无法被物理主义解释",
        "keywords": ["意识硬问题", "感受质", "二元论", "哲学僵尸"]
    },
    "雷·库兹韦尔": {
        "field": "未来学",
        "mbti": "ENFP",
        "stance": "奇点理论：AI 将超越人类创造力",
        "keywords": ["奇点", "超智能", "技术加速", "上传意识"]
    },
    "汉娜·阿伦特": {
        "field": "政治哲学",
        "mbti": "INFJ",
        "stance": "行动理论：创造力是人类行动的本质",
        "keywords": ["行动", "公共领域", "自由", "政治"]
    },
    "彼得·辛格": {
        "field": "伦理学",
        "mbti": "ENFJ",
        "stance": "功利主义：权利基于感受痛苦的能力",
        "keywords": ["动物权利", "功利主义", "道德地位", "感受性"]
    },
    "尼克·博斯特罗姆": {
        "field": "AI 安全",
        "mbti": "INTJ",
        "stance": "存在风险论：超级 AI 可能带来生存风险",
        "keywords": ["AI 安全", "存在风险", "超级智能", "模拟论证"]
    }
}


# ============================================================
# ASCII 图表生成器
# ============================================================

def generate_ascii_framework(contradiction: str, debate_log: List[Dict]) -> str:
    """
    基于核心争议生成 ASCII 思考框架图
    """
    # 分析辩论日志，提取主要立场
    positions = extract_positions(debate_log)
    
    # 生成图表
    if len(positions) == 2:
        return generate_two_side_chart(positions, contradiction)
    elif len(positions) > 2:
        return generate_multi_side_chart(positions, contradiction)
    else:
        return generate_simple_chart(contradiction)


def extract_positions(debate_log: List[Dict]) -> List[Dict]:
    """从辩论日志中提取主要立场"""
    positions = {}
    
    for entry in debate_log:
        if entry.get('type') == 'statement':
            speaker = entry.get('speaker', '')
            content = entry.get('content', '')
            
            # 简单分类逻辑
            if any(kw in content for kw in ['计算', '算法', '模拟']):
                positions['计算主义'] = positions.get('计算主义', [])
                positions['计算主义'].append(speaker)
            elif any(kw in content for kw in ['意识', '生物', '体验']):
                positions['生物主义'] = positions.get('生物主义', [])
                positions['生物主义'].append(speaker)
            else:
                positions['其他'] = positions.get('其他', [])
                positions['其他'].append(speaker)
    
    return [{'name': k, 'representatives': v} for k, v in positions.items()]


def generate_two_side_chart(positions: List[Dict], contradiction: str) -> str:
    """生成双方对比图"""
    pos_a = positions[0] if len(positions) > 0 else {'name': '立场 A', 'representatives': []}
    pos_b = positions[1] if len(positions) > 1 else {'name': '立场 B', 'representatives': []}
    
    reps_a = '/'.join(pos_a['representatives'][:2]) if pos_a['representatives'] else '代表'
    reps_b = '/'.join(pos_b['representatives'][:2]) if pos_b['representatives'] else '代表'
    
    chart = f"""
┌─────────────────────────────────────────────────┐
│              {contradiction[:30]}              │
├─────────────────────────────────────────────────┤
│                                                 │
│   ┌──────────────┐         ┌──────────────┐    │
│   │ {pos_a['name'][:10]:<10} │         │ {pos_b['name'][:10]:<10} │    │
│   │ ({reps_a:<12}) │  ←→    │ ({reps_b:<12}) │    │
│   └──────┬───────┘         └───────┬──────┘    │
│          │                         │           │
│          ▼                         ▼           │
│   立场 A 核心观点              立场 B 核心观点     │
│          │                         │           │
│          └──────────┬──────────────┘           │
│                     ▼                           │
│              【核心争议点】                     │
│         {contradiction[:25]}                 │
│                                                 │
└─────────────────────────────────────────────────┘
"""
    return chart


def generate_multi_side_chart(positions: List[Dict], contradiction: str) -> str:
    """生成多方对比图"""
    chart = f"""
┌─────────────────────────────────────────────────┐
│              {contradiction[:30]}              │
├─────────────────────────────────────────────────┤
│                                                 │
"""
    for i, pos in enumerate(positions[:4]):
        reps = '/'.join(pos['representatives'][:2]) if pos['representatives'] else '代表'
        chart += f"│   {i+1}. {pos['name'][:15]:<15} ({reps:<15}) │\n"
    
    chart += f"""│                                                 │
│              【核心争议点】                     │
│         {contradiction[:25]}                 │
│                                                 │
└─────────────────────────────────────────────────┘
"""
    return chart


def generate_simple_chart(contradiction: str) -> str:
    """生成简单图表"""
    return f"""
┌─────────────────────────────────────────────────┐
│              {contradiction[:40]}              │
├─────────────────────────────────────────────────┤
│                                                 │
│              【核心争议点】                     │
│         {contradiction}                        │
│                                                 │
└─────────────────────────────────────────────────┘
"""


# ============================================================
# 知识网络生成器
# ============================================================

def generate_knowledge_network(debate_log: List[Dict], topic: str) -> str:
    """
    基于辩论日志生成结构化知识网络
    """
    network = f"""# 知识网络：{topic}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 核心议题
{topic}

---

## 主要立场
"""
    
    # 提取立场
    positions = extract_positions(debate_log)
    for pos in positions:
        network += f"\n### {pos['name']}\n"
        network += f"- 代表：{', '.join(pos['representatives'])}\n"
    
    network += """
---

## 核心争议
[待总结]

---

## 共识点
[待总结]

---

## 开放问题
[待总结]

---

*圆桌论坛 · 以"求真"为目标的深度对话框架*
"""
    
    return network


# ============================================================
# 主持人引擎
# ============================================================

class Moderator:
    """圆桌论坛主持人"""
    
    def __init__(self):
        self.topic = ""
        self.participants = []
        self.debate_log = []
        self.current_question = ""
        self.contradiction = ""
    
    def initiate(self, topic: str) -> str:
        """启动圆桌讨论"""
        self.topic = topic
        
        # 根据话题推荐代表人物
        self.participants = self.recommend_representatives(topic)
        
        output = "【主持】：感谢您。本次圆桌对话正式开始。\n"
        output += f"【主持】：核心议题为「{topic}」。\n"
        output += "【主持】：为穷尽其理，我已邀请以下几位代表人物：\n"
        
        for person in self.participants:
            output += f"- {person['name']} ({person['mbti']}) - {person['field']}\n"
        
        # 生成开场问题
        key_concept = self.identify_key_concept(topic)
        self.current_question = f"在我们深入探讨之前，为了确保讨论建立在共同的基础之上，我想先请各位阐述：我们应当如何定义「{key_concept}」？它的核心要素是什么？"
        
        output += f"\n【主持】：{self.current_question}\n"
        
        return output
    
    def recommend_representatives(self, topic: str) -> List[Dict]:
        """根据话题推荐代表人物"""
        # 简单匹配逻辑
        representatives = []
        
        # 默认选择 4 位
        selected_names = random.sample(list(PRESET_REPRESENTATIVES.keys()), 4)
        
        for name in selected_names:
            person = PRESET_REPRESENTATIVES[name].copy()
            person['name'] = name
            representatives.append(person)
        
        return representatives
    
    def identify_key_concept(self, topic: str) -> str:
        """从话题中识别核心概念"""
        # 简单提取逻辑
        if "创造力" in topic:
            return "创造力"
        elif "权利" in topic:
            return "权利"
        elif "意识" in topic:
            return "意识"
        elif "智能" in topic or "AI" in topic:
            return "智能"
        else:
            return "核心概念"
    
    def synthesize(self) -> str:
        """总结本轮讨论"""
        # 分析争议点
        self.contradiction = self.analyze_contradiction()
        
        output = f"【主持】：各位的讨论非常精彩。本轮探讨的核心争议点在于「{self.contradiction}」。\n\n"
        
        # 生成 ASCII 图表
        ascii_chart = generate_ascii_framework(self.contradiction, self.debate_log)
        output += ascii_chart + "\n"
        
        # 提出更深层问题
        next_question = self.formulate_next_question()
        output += f"【主持】：基于以上框架，一个更深层的问题浮现了：「{next_question}」\n"
        
        self.current_question = next_question
        
        return output
    
    def analyze_contradiction(self) -> str:
        """分析核心争议点"""
        # 简单实现
        return "不同立场对核心概念的理解存在差异"
    
    def formulate_next_question(self) -> str:
        """提出更深层问题"""
        return f"如果{self.identify_key_concept(self.topic)}可以被重新定义，那我们对原议题的理解是否需要更新？"
    
    def prompt_for_command(self) -> str:
        """提示用户输入命令"""
        return "【主持】：(指令：可 / 止 / 深入此节 / 引入新人物)"
    
    def conclude(self) -> str:
        """结束讨论"""
        output = "【主持】：今天的对话已非常深入，暂告一段落。\n"
        output += "我们从一个议题开始，通过多轮激烈的思想碰撞，\n"
        output += "共同构建了一个关于此议题的思维网络。\n\n"
        
        # 生成知识网络
        knowledge_network = generate_knowledge_network(self.debate_log, self.topic)
        
        return output + knowledge_network


# ============================================================
# 主流程
# ============================================================

def run_roundtable(topic: str):
    """运行圆桌论坛"""
    moderator = Moderator()
    
    print("=" * 60)
    print("【圆桌研讨会】系统已加载完毕")
    print("=" * 60)
    print()
    
    # 启动讨论
    print(moderator.initiate(topic))
    print()
    
    # 主循环
    while True:
        # 模拟代表发言
        for participant in moderator.participants:
            response = f"【{participant['name']}】【{participant['mbti']}】：{generate_response(participant, moderator.current_question)}"
            print(response)
            moderator.debate_log.append({
                'type': 'statement',
                'speaker': participant['name'],
                'content': response
            })
        
        print()
        
        # 主持人总结
        print(moderator.synthesize())
        print()
        
        # 提示用户命令
        print(moderator.prompt_for_command())
        
        # 获取用户输入（简化处理）
        user_command = input("> ")
        
        if user_command in ['/止', '止', 'stop', 'end']:
            print()
            print(moderator.conclude())
            break
        elif user_command in ['/可', '可', 'continue', 'next']:
            print("【主持】：好的，让我们继续探讨这个新问题。")
            continue
        elif user_command in ['/深入此节', '深入', 'deepen']:
            print("【主持】：好的，我们暂停推进。让我们继续围绕刚才的核心争议点，进行更深层次的探讨。")
            continue
        elif user_command.startswith('/引入新人物'):
            new_person = user_command.replace('/引入新人物', '').strip()
            print(f"【主持】：欢迎新嘉宾 {new_person} 加入讨论。")
            continue
        else:
            print("【主持】：抱歉，我不理解这个命令。请使用：可 / 止 / 深入此节 / 引入新人物")


def generate_response(participant: Dict, question: str) -> str:
    """生成代表发言内容"""
    # 简单实现
    return f"关于这个问题，我认为...（{participant['stance']}）"


# ============================================================
# 入口点
# ============================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "人工智能是否拥有真正的创造力？"
    
    run_roundtable(topic)
