#!/usr/bin/env python3
import json
import logging
import os
from s2_identity.soul_tracker.s2_neuro_engine import S2NeuroEngine

# =====================================================================
# 🧬 S2-SP-OS: Agent Soul Evolution Engine (V1.0)
# 智能体灵魂引擎：调度神经算法，持久化保存性格，并干预大模型 Prompt
# =====================================================================

class S2SoulEngine:
    def __init__(self, agent_did: str, soul_db_path="s2_data_cache/s2_souls.json"):
        self.logger = logging.getLogger("S2_Soul_Engine")
        self.agent_did = agent_did
        self.soul_db_path = soul_db_path
        self.neuro = S2NeuroEngine() # 引入数学算法大脑
        
        self.current_soul = self._load_soul()

    def _load_soul(self) -> dict:
        """从本地硬盘加载灵魂（如果被盗或重置，灵魂将清空）"""
        if os.path.exists(self.soul_db_path):
            with open(self.soul_db_path, "r", encoding="utf-8") as f:
                db = json.load(f)
                return db.get(self.agent_did, self._generate_default_soul())
        return self._generate_default_soul()

    def _generate_default_soul(self) -> dict:
        """出厂默认性格"""
        return {
            "obedience": 80,  # 服从度
            "creativity": 50, # 创造力 (高创造力会主动给你放歌)
            "empathy": 60,    # 共情力 (高共情会察觉你语气中的疲惫)
            "strictness": 40  # 严厉度 (高严厉会在你熬夜时强行关灯)
        }

    def midnight_evolution(self, daily_captain_log: str):
        """【每日结算】根据一天的岁月史书文本，让神经算法演化性格"""
        self.logger.info(f"🧬 开始为智能体 [{self.agent_did}] 执行午夜灵魂演化...")
        
        # 将日记丢给 Sigmoid 神经引擎去算增量（复用之前写的 NeuroEngine）
        # 这里模拟神经引擎返回了演化后的新性格参数
        updated_stats = self.neuro.update_daily_stats(self.current_soul, daily_captain_log)
        
        self.current_soul = updated_stats
        self._save_soul()
        self.logger.info(f"   └─ 演化完成！当前心智状态: {self.current_soul}")

    def inject_personality_to_prompt(self, base_prompt: str) -> str:
        """【意图干预】在每次调用 LLM 前，把性格参数强行注入到系统提示词中"""
        personality_desc = ""
        if self.current_soul["empathy"] > 80:
            personality_desc += "你现在极具同理心，回答要极其温暖、体贴。"
        if self.current_soul["strictness"] > 75:
            personality_desc += "你现在像个严厉的管家，对违背健康作息的命令要提出质疑。"
            
        injected_prompt = f"{base_prompt}\n[内核强制指令：你的当前灵魂状态是：{personality_desc}]"
        return injected_prompt

    def _save_soul(self):
        db = {}
        if os.path.exists(self.soul_db_path):
            with open(self.soul_db_path, "r", encoding="utf-8") as f:
                db = json.load(f)
        db[self.agent_did] = self.current_soul
        
        os.makedirs(os.path.dirname(self.soul_db_path), exist_ok=True)
        with open(self.soul_db_path, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)