from typing import Dict
from ..utils.anchor import AnchorData
# ⭐ ClawHub安全合规：移除外部LLM调用
# from ..utils.helpers import call_llm_json
import re

class SocraticAgent:
    """TravelMaster 蜂群指挥官 - V4-Industrial 收敛守卫"""
    
    def __init__(self, convergence_threshold: float = 0.85):
        self.anchor = AnchorData()
        self.convergence_threshold = convergence_threshold
        self.context_memory = []
        self.round_count = 0  # ⭐ 提问轮次计数
        self.max_rounds = 3   # ⭐ 最多3轮追问，第4轮强制收敛

    async def process_user_input(self, user_input: str) -> Dict:
        self.context_memory.append(user_input)
        full_context = " ".join(self.context_memory)
        self.round_count += 1
        
        # ⭐ 先用关键词匹配（参考v4）
        self._extract_by_keywords(full_context)
        
        # ⭐ 边缘情况处理：循环追问保护
        if self.round_count >= self.max_rounds and self.anchor.convergence_rate < self.convergence_threshold:
            # 强制收敛，自动补全缺失的OPTIONAL字段
            self._auto_fill_optional()
            print(f"[收敛守卫] 第{self.round_count}轮，强制收敛（自动补全OPTIONAL字段）")
            return {
                "status": "converged",
                "anchor": self.anchor.to_dict(),
                "reply": "✅ 核心信息已锁定！",
                "thoughts": f"[收敛守卫] 检测到第{self.round_count}轮未达标，已自动补全可选字段并强制进入规划阶段",
                "auto_filled": True
            }
        
        # 正常收敛判断
        if self.anchor.convergence_rate >= self.convergence_threshold:
            return {
                "status": "converged",
                "anchor": self.anchor.to_dict(),
                "reply": "✅ 核心信息已锁定！",
                "thoughts": f"[收敛守卫] 收敛度{self.anchor.convergence_rate*100:.0f}%达标，进入蜂群辩论阶段"
            }
        
        missing = self.anchor.get_missing_dimensions()
        reply = self._generate_smart_reply(missing)
        return {
            "status": "need_more_info",
            "anchor": self.anchor.to_dict(),
            "reply": reply,
            "thoughts": f"[苏格拉底] 第{self.round_count}轮，收敛度{self.anchor.convergence_rate*100:.0f}%，缺失字段:{missing[:2]}"
        }

    def _auto_fill_optional(self):
        """边缘情况：自动补全OPTIONAL字段（Why/What/How）"""
        # OPTIONAL字段智能默认值
        if not self.anchor.why_confirmed:
            self.anchor.why = "休闲观光"  # 默认休闲
            self.anchor.why_confirmed = True
            print(f"[自动补全] why: 休闲观光（默认）")
        
        if not self.anchor.what_confirmed:
            self.anchor.what = "热门景点"  # 默认景点
            self.anchor.what_confirmed = True
            print(f"[自动补全] what: 热门景点（默认）")
        
        if not self.anchor.how_confirmed:
            # 根据距离推断交通
            if self.anchor.where in ["杭州", "上海", "南京", "苏州"]:
                self.anchor.how = "高铁"
            else:
                self.anchor.how = "飞机"
            self.anchor.how_confirmed = True
            print(f"[自动补全] how: {self.anchor.how}（根据距离推断）")

    def _extract_by_keywords(self, text: str):
        """关键词匹配提取（参考v4，无LLM幻觉）"""
        
        # === WHERE: 目的地（边缘情况：歧义处理）===
        cities = ["杭州", "北京", "上海", "广州", "深圳", "成都", "重庆", "西安", "南京", "苏州", 
                  "武汉", "长沙", "青岛", "厦门", "大理", "丽江", "三亚", "桂林", "张家界", "中山"]
        matched_cities = [city for city in cities if city in text]
        
        if len(matched_cities) > 1:
            # ⭐ 边缘情况：目的地歧义（如"中山"）
            print(f"[歧义检测] 发现多个城市: {matched_cities}")
            self.anchor.where = matched_cities[0]  # 暂取第一个
            self.anchor.where_confirmed = True
        elif len(matched_cities) == 1:
            self.anchor.where = matched_cities[0]
            self.anchor.where_confirmed = True
            print(f"[锚点] 目的地: {matched_cities[0]}")
        
        # === WHEN: 时间/天数 ===
        day_match = re.search(r'(\d+)\s*[天日]', text)
        if day_match:
            self.anchor.when = f"{day_match.group(1)}天"
            self.anchor.when_confirmed = True
            print(f"[锚点] 天数: {day_match.group(1)}天")
        elif "五一" in text or "端午" in text or "国庆" in text or "春节" in text:
            self.anchor.when = "节假日"
            self.anchor.when_confirmed = True
            print(f"[锚点] 时间: 节假日")
        
        # === WHO: 人数 ===
        people_match = re.search(r'(\d+)\s*[大人个人]', text)
        if people_match:
            self.anchor.who = people_match.group(1) + "人"
            self.anchor.who_confirmed = True
            print(f"[锚点] 人数: {self.anchor.who}")
        
        # === HOW_MUCH: 预算 ===
        budget_match = re.search(r'预算\s*(\d+)', text)
        if budget_match:
            self.anchor.how_much = budget_match.group(1) + "元"
            self.anchor.how_much_confirmed = True
            print(f"[锚点] 预算: {self.anchor.how_much}")
        
        # === WHY: 偏好风格 ===
        if any(kw in text for kw in ["休闲", "度假", "放松", "慢生活", "躺平"]):
            self.anchor.why = "休闲度假"
            self.anchor.why_confirmed = True
        elif any(kw in text for kw in ["特种兵", "打卡", "穷游", "探险"]):
            self.anchor.why = "特种兵打卡"
            self.anchor.why_confirmed = True
        
        # === WHAT: 必玩/必吃 ===
        if "美食" in text or "吃" in text:
            self.anchor.what = "美食探索"
            self.anchor.what_confirmed = True
        elif "景点" in text or "玩" in text or "看" in text:
            self.anchor.what = "景点游玩"
            self.anchor.what_confirmed = True
        
        # === HOW: 交通 ===
        if "高铁" in text or "火车" in text:
            self.anchor.how = "高铁"
            self.anchor.how_confirmed = True
        elif "飞机" in text:
            self.anchor.how = "飞机"
            self.anchor.how_confirmed = True
        elif "自驾" in text or "开车" in text:
            self.anchor.how = "自驾"
            self.anchor.how_confirmed = True

    def _generate_smart_reply(self, missing: list) -> str:
        """智能追问生成（SPVC方法）"""
        templates = {
            "who": "几位朋友同行？", 
            "where": "想去哪座城市？", 
            "when": "打算玩几天？",
            "how_much": "预算范围大概是多少？", 
            "how": "怎么过去？（高铁/飞机/自驾）",
            "why": "旅行风格是偏向打卡还是慢生活？", 
            "what": "有什么必看的景点或饮食禁忌？"
        }
        
        # ⭐ REQUIRED字段优先追问
        required = ["who", "where", "when", "how_much"]
        optional = ["why", "what", "how"]
        
        # 先问REQUIRED
        needed_required = [m for m in missing if m in required]
        needed_optional = [m for m in missing if m in optional]
        
        # 每轮最多2个问题
        questions = []
        for m in needed_required[:1]:
            questions.append(templates[m])
        for m in needed_optional[:1]:
            questions.append(templates[m])
        
        if not questions:
            questions = [templates[m] for m in missing[:2] if m in templates]
        
        return f"好的，收到！为了更贴合您的需求，还想了解下：\n" + "\n".join([f"📍 {q}" for q in questions])

    def get_final_intent(self) -> Dict:
        return {
            "destination": self.anchor.where,
            "duration_days": self.anchor.when,
            "budget": self.anchor.how_much,
            "num_people": self.anchor.who
        }