"""
对话健康评分 + 自适应策略
借鉴 capability-evolver 的思想，应用于对话场景
"""

from typing import Dict, List
from datetime import datetime


class ConversationHealth:
    """对话健康管理"""
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
    
    def calculate_score(self, user_id: str) -> Dict:
        """
        计算对话健康评分（0-100）
        
        指标：
        1. 用户满意度（30分）：基于纠正次数
        2. 回复质量（30分）：基于验证置信度
        3. 任务完成率（20分）：基于完成标记
        4. 响应速度（20分）：基于平均响应时间
        """
        history = self.memory.load_history(user_id)
        
        if not history:
            return {
                "score": 100,
                "level": "excellent",
                "strategy": "balanced"
            }
        
        # 指标1：用户满意度（基于纠正次数）
        correction_count = self._count_corrections(history)
        correction_rate = correction_count / max(len(history) / 2, 1)  # 每轮对话
        satisfaction_score = max(0, 30 - correction_rate * 30)
        
        # 指标2：回复质量（基于验证置信度）
        # 注：需要从历史中提取置信度，这里简化为检测问题回复
        problem_replies = self._count_problem_replies(history)
        quality_rate = 1 - (problem_replies / max(len(history) / 2, 1))
        quality_score = quality_rate * 30
        
        # 指标3：任务完成率（简化：检测是否有"完成"、"好的"等确认）
        completion_count = self._count_completions(history)
        completion_rate = completion_count / max(len(history) / 2, 1)
        completion_score = min(20, completion_rate * 20)
        
        # 指标4：响应速度（简化：假设都在合理范围）
        speed_score = 20  # 简化处理
        
        # 总分
        total_score = satisfaction_score + quality_score + completion_score + speed_score
        
        # 评级
        if total_score >= 85:
            level = "excellent"
        elif total_score >= 70:
            level = "good"
        elif total_score >= 50:
            level = "fair"
        else:
            level = "poor"
        
        # 选择策略
        strategy = self._choose_strategy(total_score)
        
        return {
            "score": round(total_score, 1),
            "level": level,
            "strategy": strategy,
            "breakdown": {
                "satisfaction": round(satisfaction_score, 1),
                "quality": round(quality_score, 1),
                "completion": round(completion_score, 1),
                "speed": round(speed_score, 1)
            }
        }
    
    def _count_corrections(self, history: List[Dict]) -> int:
        """统计用户纠正次数"""
        correction_keywords = [
            "不对", "不是", "错了", "应该是", "其实是",
            "[用户纠正]"
        ]
        count = 0
        for msg in history:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if any(kw in content for kw in correction_keywords):
                    count += 1
        return count
    
    def _count_problem_replies(self, history: List[Dict]) -> int:
        """统计问题回复（过短、重复、无关）"""
        count = 0
        for msg in history:
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                # 检测过短回复
                if len(content) < 10:
                    count += 1
                # 检测"不知道"类回复（正常，但如果太多说明能力不足）
                elif any(kw in content for kw in ["不知道", "不清楚", "无法回答"]):
                    count += 0.5
        return int(count)
    
    def _count_completions(self, history: List[Dict]) -> int:
        """统计任务完成次数"""
        completion_keywords = [
            "完成", "好的", "明白", "收到", "谢谢",
            "成功", "已处理", "已解决"
        ]
        count = 0
        for msg in history:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if any(kw in content for kw in completion_keywords):
                    count += 1
        return count
    
    def _choose_strategy(self, score: float) -> str:
        """
        根据健康评分选择策略
        
        策略：
        - repair-only: 危机模式，只修复关键问题
        - harden: 加固模式，提升可靠性
        - balanced: 平衡模式，可靠性 + 功能
        - innovate: 创新模式，主动扩展
        """
        if score < 50:
            return "repair-only"
        elif score < 70:
            return "harden"
        elif score < 85:
            return "balanced"
        else:
            return "innovate"
    
    def apply_strategy(self, strategy: str, context: Dict) -> Dict:
        """
        应用策略到 Context
        
        Args:
            strategy: 策略名称
            context: 当前 Context
        
        Returns:
            调整后的 Context
        """
        if strategy == "repair-only":
            # 危机模式：最小化，只回答问题
            context["system_prompt"] = "你是 Smart Agent Bot。简洁回答用户问题，不扩展，不主动建议。"
            context["history"] = []  # 不传历史，减少干扰
            
        elif strategy == "harden":
            # 加固模式：加强验证
            context["validation_level"] = "strict"
            # System Prompt 强调准确性
            if "system_prompt" in context:
                context["system_prompt"] += "\n\n【重要】确保回复准确，不确定的不要说。"
        
        elif strategy == "balanced":
            # 平衡模式：标准配置（不修改）
            pass
        
        elif strategy == "innovate":
            # 创新模式：主动提供建议
            if "system_prompt" in context:
                context["system_prompt"] += "\n\n【主动性】可以主动提供相关建议和扩展信息。"
        
        return context


# 使用示例
if __name__ == "__main__":
    # 模拟测试
    class MockMemory:
        def load_history(self, user_id):
            return [
                {"role": "user", "content": "你好"},
                {"role": "assistant", "content": "你好！有什么可以帮你的吗？"},
                {"role": "user", "content": "Python 是什么？"},
                {"role": "assistant", "content": "Python 是一种编程语言"},
                {"role": "user", "content": "不对，我问的是 Python 这条蛇"},
                {"role": "assistant", "content": "抱歉，Python 蟒蛇是一种大型蛇类"},
                {"role": "user", "content": "好的，谢谢"},
                {"role": "assistant", "content": "不客气！"}
            ]
    
    health = ConversationHealth(MockMemory())
    result = health.calculate_score("test_user")
    
    print(f"健康评分: {result['score']}")
    print(f"评级: {result['level']}")
    print(f"策略: {result['strategy']}")
    print(f"详细: {result['breakdown']}")
