from ..utils.minimax_client import minimax_client
import json

class WorkerBee:
    """工蜂审核员 - 不同模型分工"""
    
    def __init__(self, name: str, role: str, model_type: str):
        self.name = name
        self.role = role
        self.model_type = model_type

    async def review(self, plan_json: str) -> dict:
        prompt = "你是" + self.name + "，职责是" + self.role + "。\n审核以下行程计划，从你的专业角度给出评价。\n\n计划：" + plan_json + "\n\n返回JSON格式：\n{\"approved\": true/false, \"score\": 1-10, \"suggestion\": \"具体建议\"}\n\n审核要点：\n- 时间安排是否合理\n- 预算是否超支\n- 行程是否过于紧凑\n- 是否考虑了交通时间"
        
        # 使用专属模型
        result = await minimax_client.call(prompt, self.model_type)
        
        # 解析结果
        approved = "true" in result.lower() or "通过" in result
        return {"bee": self.name, "role": self.role, "model": self.model_type, "approved": approved, "suggestion": result}

class QueenBee:
    """蜂后仲裁 - MiniMax-M2.5"""
    
    def __init__(self):
        self.model = "MiniMax-M2.5"
        self.models = {"queen": "MiniMax-M2.5"}  # ⭐ 添加models属性
    
    async def final_decision(self, reviews: list) -> bool:
        """综合所有工蜂意见，决定是否通过"""
        approved_count = sum(1 for r in reviews if r["approved"])
        
        # 使用M2.5做最终决策
        prompt = f"""作为蜂后，你需要综合以下工蜂审核意见做出最终决策：

审核结果：
{json.dumps(reviews, ensure_ascii=False)}

通过率：{approved_count}/{len(reviews)}

请判断是否通过，返回true或false。"""
        
        decision = await minimax_client.call(prompt, "queen")
        return "true" in decision.lower() or "通过" in decision

class ReviewSwarm:
    """蜂群审核系统 - 多模型协作"""
    
    def __init__(self):
        # 三只工蜂，不同模型分工
        self.workers = [
            WorkerBee("时间蜂", "检查时间安排合理性", "worker_time"),      # MiniMax-M2.7
            WorkerBee("预算蜂", "检查费用是否超预算", "worker_budget"),     # MiniMax-M2.7-highspeed
            WorkerBee("体验蜂", "检查行程体验质量", "worker_experience"),   # MiniMax-M2.5
        ]
        self.queen = QueenBee()

    async def review_plan(self, plan: dict) -> dict:
        """蜂群审核流程"""
        plan_json = json.dumps(plan, ensure_ascii=False)
        reviews = []
        
        # 三只工蜂并行审核
        for worker in self.workers:
            review = await worker.review(plan_json)
            reviews.append(review)
        
        # 蜂后最终决策（M2.5）
        final_approved = await self.queen.final_decision(reviews)
        
        return {
            "approved": final_approved,
            "reviews": reviews,
            "summary": f"蜂群审核：{len(reviews)}只工蜂（{self.workers[0].model}+{self.workers[1].model}+{self.workers[2].model}），蜂后{self.queen.models['queen']}"
        }

import json