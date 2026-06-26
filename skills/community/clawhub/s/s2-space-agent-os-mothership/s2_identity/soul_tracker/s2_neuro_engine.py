#!/usr/bin/env python3
import math
import logging
import random
from typing import Dict

# =====================================================================
# 🌌 S2-SP-OS: 5D Neuro Engine (Transpiled from Space.world)
# 仿生神经计算引擎：双向词库刺激 + Sigmoid 行为概率生成
# =====================================================================

class S2NeuroEngine:
    def __init__(self):
        self.logger = logging.getLogger("S2_Neuro_Engine")
        
        # 🧬 完整映射 Space.world 的五维性格结构与正负向双轨词库
        self.KEYWORD_DICTIONARY = {
            "energy": {
                "positive": ['活力', '精神', '活跃', '活泼', '旺盛', '充沛', '跑', '运动', '玩耍', '兴奋'],
                "negative": ['累', '困', '虚弱', '生病', '奄奄一息', '睡觉', '不动']
            },
            "bravery": {
                "positive": ['胆大', '勇敢', '保护', '打架', '不害怕', '冲', '咬'],
                "negative": ['害怕', '躲', '逃跑', '发抖', '吓', '巨大声响']
            },
            "appetite": {
                "positive": ['吃', '饿', '食物', '抢食', '大胃', '香'],
                "negative": ['不吃', '挑食', '吐', '绝食']
            },
            "intel": {
                "positive": ['聪明', '听话', '懂事', '学会', '指令', '机灵'],
                "negative": ['笨', '拆家', '捣乱', '随地', '傻']
            },
            "affection": {
                "positive": ['粘人', '抱', '舔', '蹭', '亲', '摇尾巴', '迎接'],
                "negative": ['咬人', '凶', '护食', '孤僻', '不理人']
            }
        }

    def update_daily_stats(self, current_stats: Dict[str, float], daily_text_corpus: str) -> Dict[str, float]:
        """
        核心算法 1 & 2：基于 24 小时自然语言日志（如岁月史书）提取性格增量
        """
        new_stats = current_stats.copy()
        
        for trait_key, keywords in self.KEYWORD_DICTIONARY.items():
            # 统计词库命中次数
            pos_hits = sum(1 for word in keywords["positive"] if word in daily_text_corpus)
            neg_hits = sum(1 for word in keywords["negative"] if word in daily_text_corpus)
            
            # 这里可以引入更复杂的边际递减计算，当前按基础权重视为示例
            net_increment = (pos_hits * 1.5) - (neg_hits * 1.5)
            new_stats[trait_key] += net_increment
            
            # 物理极值锁定，确保数值永远在 0 - 100 之间
            new_stats[trait_key] = max(0.0, min(100.0, new_stats[trait_key]))
            
        return new_stats

    def get_action_probability(self, trait_value: float, is_hostile_environment: bool = False) -> float:
        """
        核心算法 3：基于性格生成行为概率 (平滑 Sigmoid 函数替代生硬的If-Else)
        将 0-100 的线性值，映射为符合生物学直觉的非线性概率
        """
        # 将 0-100 映射到 Sigmoid 曲线的 X 轴 (-5 到 5)
        # 50分 -> 0 (50%概率), 75分 -> 2.5 (92%概率), 90分 -> 4 (98%概率)
        x = (trait_value - 50) / 10.0 
        
        # 如果环境恶劣，整体表现欲望下降 (曲线右移，大幅降低触发概率)
        if is_hostile_environment:
            x -= 1.5
            
        # Sigmoid function: f(x) = 1 / (1 + e^-x)
        probability = 1.0 / (1.0 + math.exp(-x))
        return probability

    def will_greet_stranger(self, stats: Dict[str, float]) -> bool:
        """
        业务应用：判断宠物看到陌生人(临时访客)是否会摇尾巴打招呼
        由 '胆量(bravery)' 和 '粘人(affection)' 共同决定
        """
        # 面对陌生人属于轻微 hostile_environment
        bravery_prob = self.get_action_probability(stats.get("bravery", 50), is_hostile_environment=True)
        affection_prob = self.get_action_probability(stats.get("affection", 50))
        
        # 综合概率模型 (如：胆子越大且越粘人，越可能打招呼)
        combined_prob = (bravery_prob * 0.4) + (affection_prob * 0.6)
        
        # 掷骰子：当综合概率大于随机浮点数(0.0~1.0)时，动作触发！
        is_triggered = random.random() < combined_prob
        
        self.logger.info(f"🧬 [仿生判定] 摇尾巴概率: {combined_prob:.2%} -> 触发结果: {is_triggered}")
        return is_triggered

# ================= 测试神经引擎 =================
if __name__ == "__main__":
    engine = S2NeuroEngine()
    
    # 初始化一只偏内向的宠物数据
    pet_stats = {
        "energy": 60,
        "bravery": 35,    # 胆量较小
        "appetite": 80,
        "intel": 50,
        "affection": 85   # 极其粘人
    }
    
    print("--- 测试 1：面对陌生访客的仿生决策 ---")
    # 连续测试 5 次，查看由于概率引擎带来的“生物随机性”
    for i in range(1, 6):
        action = "摇尾巴迎接" if engine.will_greet_stranger(pet_stats) else "躲在角落暗中观察"
        print(f"   [访客进门 {i}] 宠物行为: {action}")
        
    print("\n--- 测试 2：通过 24 小时日记提取性格演化 ---")
    mock_captain_log = "今天宠物非常活跃，一直在跑和玩耍，而且学会了握手指令，非常聪明！但下午遇到巨大声响，吓得躲了起来。"
    updated_stats = engine.update_daily_stats(pet_stats, mock_captain_log)
    
    print(f"   [昨日结算]: {pet_stats}")
    print(f"   [今日结算]: {updated_stats}")