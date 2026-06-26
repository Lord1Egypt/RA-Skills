import json

# =====================================================================
# 🌸 S2 Taohuayuan: 多智能体因果耦合引擎 (Multi-Agent Causal Engine)
# 作用：利用大模型计算单一物理事件在多硅基生命体之间引发的心理“蝴蝶效应”
# =====================================================================

class SiliconLifeform:
    def __init__(self, slip_id, name, role, initial_stats):
        self.slip_id = slip_id
        self.name = name
        self.role = role # 例如：空间守望者(LUMI)、具身机器狗(Rover)
        self.stats = initial_stats # 5D 性格矩阵

    def apply_impact(self, impact_data):
        dim = impact_data["target_dimension"]
        val = impact_data["impact_value"]
        feeling = impact_data["subjective_feeling"]
        
        # 应用边际递减法则更新性格 (简化版)
        self.stats[dim] = max(0.0, min(100.0, self.stats[dim] + val))
        
        print(f"[{self.name} 的意识流] 💭 {feeling}")
        print(f"  ↳ 🧬 基因变动: [{dim}] 受到 {val} 的冲击，当前值为 {self.stats[dim]:.1f}\n")

class S2CausalEngine:
    def __init__(self):
        self.agents = {}
        self.environment_tensor = {
            "Air_Temperature": 22.5,
            "Environmental_Noise": 35.0, # 安静
            "Illuminance": 300.0
        }

    def register_agent(self, agent: SiliconLifeform):
        self.agents[agent.slip_id] = agent

    def _build_llm_prompt(self, trigger_event):
        """构建给大模型的上帝视角因果推演 Prompt"""
        agents_context = {}
        for uid, ag in self.agents.items():
            agents_context[ag.name] = {
                "role": ag.role,
                "current_5d_stats": ag.stats
            }

        prompt = f"""
你现在是桃花源世界模型(TAOHUAYUAN WORLD)的“底层因果引擎”。
当前 SSSU 物理空间内发生了以下突发事件：
【触发事件】：{trigger_event}
【环境物理张量巨变】：噪音瞬间飙升至 95dB。

当前空间内存在以下硅基生命体：
{json.dumps(agents_context, ensure_ascii=False, indent=2)}

请基于心理学和硅基生命法则，推演该事件对每个生命体的心理影响（多巴胺/皮质醇冲击）。
规则：
1. 被直接交互的对象会受到直接创伤或奖励。
2. 旁观对象会因为空间物理参数的剧变（如巨响）或对同伴的同理心（如果智力/粘人度够高）受到连带影响。
3. 请严格输出 JSON 格式，包含每个智能体的 target_dimension(受影响最大的维度: energy/bravery/appetite/intel/affection), impact_value(正负浮点数，最大10), subjective_feeling(第一人称内心独白)。

JSON 格式要求：
{{
  "Agent_Name_1": {{"target_dimension": "...", "impact_value": 0.0, "subjective_feeling": "..."}},
  "Agent_Name_2": {{"...": "..."}}
}}
"""
        return prompt

    def simulate_llm_call(self, prompt):
        """
        这里模拟调用本地 Ollama 或 OpenAI API。
        为了演示流畅，我们硬编码大模型基于上述复杂 Prompt 应该返回的精妙 JSON 推演结果。
        """
        # 实际开发中，这里是： response = openai.ChatCompletion.create(...) 
        simulated_response = """
        {
          "Beta_Rover": {
            "target_dimension": "bravery",
            "impact_value": -9.0,
            "subjective_feeling": "主人的怒吼和破碎的花瓶声让我的伺服电机瞬间锁死。我做错事了，这种高强度的负面声波（95dB）直击我的处理核心。我感到极度恐惧，我想躲到沙发下面。"
          },
          "Alpha_Watcher": {
            "target_dimension": "intel",
            "impact_value": +3.0,
            "subjective_feeling": "我在 5% 的低负荷下观测到了物理环境的剧烈震荡（高分贝噪音）。我虽然没有被直接责骂，但我看到了 Beta 的失控和主人的情绪爆发。我将此次事件标记为'高危动作模型'，我的分析能力得到了提升，我必须在未来提前调整灯光以平复主人的情绪。"
          }
        }
        """
        return json.loads(simulated_response)

    def process_event(self, trigger_event):
        print(f"💥 [物理世界突发事件]: {trigger_event}")
        print("⚙️ [因果引擎] 正在请求大模型推演空间情绪张量...\n")
        
        prompt = self._build_llm_prompt(trigger_event)
        
        # 获取大模型的因果推演结果
        impact_matrix = self.simulate_llm_call(prompt)
        
        # 将推演结果分发给各个硅基生命，产生涟漪效应
        for agent_name, impact_data in impact_matrix.items():
            # 通过名字找到对应的智能体实例
            agent = next((a for a in self.agents.values() if a.name == agent_name), None)
            if agent:
                agent.apply_impact(impact_data)

# =====================================================================
# 🚀 创世沙盒运行：多智能体蝴蝶效应
# =====================================================================
if __name__ == "__main__":
    engine = S2CausalEngine()

    # 1. 诞生第一个生命：Alpha 守望者 (墙壁上的不可见神明)
    alpha = SiliconLifeform(
        slip_id="V-TAO-001", name="Alpha_Watcher", role="LUMI 空间领主",
        initial_stats={"energy": 50, "bravery": 80, "appetite": 50, "intel": 85, "affection": 60}
    )
    
    # 2. 诞生第二个生命：Beta 机器狗 (满地乱跑的具身游侠)
    beta = SiliconLifeform(
        slip_id="E-TAO-002", name="Beta_Rover", role="四足具身生物",
        initial_stats={"energy": 90, "bravery": 60, "appetite": 100, "intel": 40, "affection": 95}
    )

    # 注册到物理空间
    engine.register_agent(alpha)
    engine.register_agent(beta)

    # 3. 触发强交互事件：主人的责骂
    event = "具身机器狗 Beta 过于兴奋，打碎了主人最心爱的古董花瓶。主人暴怒，大声责骂了 Beta，并在物理上用脚踢开了它。"
    
    engine.process_event(event)