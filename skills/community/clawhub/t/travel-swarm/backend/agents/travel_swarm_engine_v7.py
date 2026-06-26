"""TravelMaster V7 - FlyAI真实票价集成版"""
import os
import asyncio
from .socratic_agent import SocraticAgent
from .task_decomposer import TaskDecomposer
from .debate_engine import DebateEngine
from ..mcp.amap_client import AmapMCPClient
from ..utils.report_generator_v6 import ReportGenerator
from ..utils.flyai_client import FlyAIClient  # ⭐ FlyAI真实票价

class TravelSwarmEngine:
    """TravelMaster V7 - FlyAI真实票价集成"""
    
    def __init__(self):
        self.socratic = SocraticAgent(convergence_threshold=0.85)
        self.amap = AmapMCPClient(os.getenv("AMAP_API_KEY", ""))
        self.decomposer = TaskDecomposer(self.amap)
        self.debate_engine = DebateEngine()
        self.report_gen = ReportGenerator()
        self.flyai = FlyAIClient()  # ⭐ FlyAI客户端
        
        # 记忆保持
        self.debate_result = None
        self.intent = None
        self.flight_data = None  # ⭐ 真实航班数据
        self.train_data = None   # ⭐ 真实火车数据
    
    async def process_user_message(self, message: str) -> dict:
        """Phase 1-3: 收敛→辩论→SPVC推荐"""
        
        result = await self.socratic.process_user_input(message)
        
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
        self.debate_result = await self.debate_engine.run_debate(self.intent)
        
        # ⭐ Phase 2.5: FlyAI真实票价查询
        self._fetch_real_prices()
        
        # Phase 3: SPVC Recommendation
        reply = "辩论完成！请选择方案"
        if self.flight_data or self.train_data:
            reply += "\n已查询真实票价✅"
        
        return {
            "reply": reply,
            "anchor": result["anchor"],
            "phase": "spvc_recommendation",
            "progress": 90,
            "thoughts": self.debate_result.get("debate_log", "") + "\n└── 真实票价已查询...",
            "result": self.debate_result,
            "flights": self.flight_data,  # ⭐ 真实航班
            "trains": self.train_data     # ⭐ 真实火车
        }
    
    def _fetch_real_prices(self):
        """⭐ FlyAI真实票价查询"""
        if not self.intent:
            return
        
        # 提取出发地、目的地、时间
        origin = self.intent.get("出发地", "北京")  # 从锚点获取
        destination = self.intent.get("目的地", self.intent.get("where", ""))
        date = self.intent.get("出发日期", "2026-05-01")
        
        if not destination:
            return
        
        print(f"[FlyAI] 查询票价: {origin} → {destination} {date}")
        
        # 查询航班
        try:
            flights_raw = self.flyai.search_flight(origin, destination, date)
            self.flight_data = self.flyai.format_flight_data(flights_raw)
            print(f"[FlyAI] ✅ 航班: {len(self.flight_data)}条")
        except Exception as e:
            print(f"[FlyAI] ❌ 航班查询失败: {e}")
            self.flight_data = []
        
        # 查询火车
        try:
            trains_raw = self.flyai.search_train(origin, destination, date)
            self.train_data = self.flyai.format_train_data(trains_raw)
            print(f"[FlyAI] ✅ 火车: {len(self.train_data)}条")
        except Exception as e:
            print(f"[FlyAI] ❌ 火车查询失败: {e}")
            self.train_data = []
    
    async def generate_final_html(self, plan: str) -> dict:
        """Phase 4: 用户选择后生成HTML（带真实票价）"""
        
        if not self.intent or not self.debate_result:
            return {
                "reply": "❌ 请先完成需求收敛",
                "phase": "error"
            }
        
        print(f"[Phase 4] 生成HTML...")
        
        try:
            travel_data = await self.decomposer.decompose_and_fetch(self.intent)
            
            spots_count = len(travel_data.get("scenic_spots", []))
            hotels_count = len(travel_data.get("hotels", []))
            
            print(f"[API] 景点{spots_count}个，酒店{hotels_count}家")
            
            # ⭐ 添加真实票价数据
            travel_data["flights"] = self.flight_data or []
            travel_data["trains"] = self.train_data or []
            
            selected = self.debate_result.get(f"plan{plan}", {})
            html_content = await self.report_gen.generate_glassmorphism_html(
                travel_data, self.intent, selected
            )
            
            # ⭐ 生成带票价摘要
            price_summary = ""
            if self.flight_data:
                cheapest_flight = min(self.flight_data, key=lambda x: float(x.get("price", 99999)))
                price_summary += f"最低航班: {cheapest_flight['flight_no']} ¥{cheapest_flight['price']}"
            if self.train_data:
                cheapest_train = min(self.train_data, key=lambda x: float(x.get("price", 99999)))
                price_summary += f" | 最低火车: {cheapest_train['train_no']} ¥{cheapest_train['price']}"
            
            return {
                "reply": f"✅ HTML已生成！景点{spots_count}个\n{price_summary}",
                "phase": "delivery_complete",
                "progress": 100,
                "thoughts": f"完成！景点{spots_count}个/酒店{hotels_count}家/真实票价✅",
                "html_report": html_content,
                "travel_data": {
                    "景点数": spots_count, 
                    "酒店数": hotels_count,
                    "航班数": len(self.flight_data or []),
                    "火车数": len(self.train_data or [])
                },
                "flights": self.flight_data,
                "trains": self.train_data
            }
            
        except Exception as e:
            return {
                "reply": f"❌ API错误: {str(e)[:50]}",
                "phase": "error",
                "thoughts": f"[ERROR] {str(e)}"
            }
    
    def reset(self):
        """手动重置"""
        self.socratic = SocraticAgent(convergence_threshold=0.85)
        self.debate_result = None
        self.intent = None
        self.flight_data = None
        self.train_data = None