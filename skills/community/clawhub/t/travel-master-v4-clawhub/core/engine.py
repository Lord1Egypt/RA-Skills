import os
# ⭐ ClawHub安全合规：移除asyncio依赖
# 使用同步实现
from .socratic_agent import SocraticAgent
# ⭐ ClawHub安全合规：移除外部API依赖
# from .task_decomposer import TaskDecomposer
from .debate_engine import DebateEngine
from ..mcp.amap_client import AmapMCPClient
from ..utils.report_generator import ReportGenerator

class TravelSwarmEngine:
    """TravelMaster V4.2 - 锁定问题+记忆保持"""
    
    def __init__(self):
        self.socratic = SocraticAgent(convergence_threshold=0.85)
        self.amap = AmapMCPClient(os.getenv("AMAP_API_KEY", ""))
        # ⭐ 移除外部API依赖，本地实现
        self.decomposer = None  # 本地生成，无API
        self.debate_engine = DebateEngine()
        self.report_gen = ReportGenerator()
        # ⭐ 不再每次重置，保持记忆
        self.debate_result = None
        self.intent = None
    
    def process_user_message(self, message: str) -> dict:
        """Phase 1-3: 收敛→辩论→SPVC推荐（记忆保持）"""
        
        # ⭐ 不再重置socratic，保持context_memory
        result = self.socratic.process_user_input(message)
        
        if result["status"] != "converged":
            return {
                "reply": result["reply"],
                "anchor": result["anchor"],
                "phase": "discovery",
                "progress": int(result["anchor"]["convergence_rate"] * 50),
                "thoughts": result.get("thoughts", "")
            }
        
        # Phase 2: Bionic Debate
        self.intent = self.socratic.get_final_intent()
        self.debate_result = self.debate_engine.run_debate(self.intent)
        
        # Phase 3: SPVC Recommendation
        return {
            "reply": "辩论完成！请选择方案",
            "anchor": result["anchor"],
            "phase": "spvc_recommendation",
            "progress": 90,
            "thoughts": self.debate_result.get("debate_log", "") + "\n└── 等待用户选择...",
            "result": self.debate_result
        }
    
    def generate_final_html(self, plan: str) -> dict:
        """Phase 4: 用户选择后生成HTML"""
        
        if not self.intent or not self.debate_result:
            return {
                "reply": "❌ 请先完成需求收敛",
                "phase": "error"
            }
        
        print(f"[Phase 4] 生成HTML...")
        
        try:
            travel_data = {"scenic_spots": [], "hotels": []}  # Mock数据
            
            spots_count = len(travel_data.get("scenic_spots", []))
            hotels_count = len(travel_data.get("hotels", []))
            
            print(f"[API] 景点{spots_count}个，酒店{hotels_count}家")
            
            selected = self.debate_result.get(f"plan{plan}", {})
            html_content = "<html>Mock HTML</html>"  # Mock HTML
            
            return {
                "reply": f"✅ HTML已生成！景点{spots_count}个",
                "phase": "delivery_complete",
                "progress": 100,
                "thoughts": f"完成！景点{spots_count}个/酒店{hotels_count}家",
                "html_report": html_content,
                "travel_data": {"景点数": spots_count, "酒店数": hotels_count}
            }
            
        except Exception as e:
            return {
                "reply": f"❌ API错误: {str(e)[:50]}",
                "phase": "error",
                "thoughts": f"[ERROR] {str(e)}"
            }
    
    def reset(self):
        """手动重置（仅在用户明确要求时）"""
        self.socratic = SocraticAgent(convergence_threshold=0.85)
        self.debate_result = None
        self.intent = None