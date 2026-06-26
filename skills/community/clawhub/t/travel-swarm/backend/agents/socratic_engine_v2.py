#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
苏格拉底引擎 V2 - OpenClaw 核心重构
核心原则：禁止在需求不明时执行任何真正的工作

大帅指示：
- 动作快于思考 = 智障AI
- 必须先探明，再执行
- 引入收敛系数，防止错误路径
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SocraticEngine")


class ConvergenceLevel(Enum):
    """收敛等级"""
    CRITICAL = 0.3   # 危险，必须追问
    LOW = 0.5        # 低，建议追问
    MEDIUM = 0.7     # 中等，可以执行
    HIGH = 0.8       # 高，允许执行
    LOCKED = 0.95    # 锁定，直接执行


@dataclass
class AnchorData:
    """5W2H锚点数据"""
    # Who: 谁看？目标用户
    who: str = ""
    who_confirmed: bool = False
    
    # Why: 为什么？目的
    why: str = ""
    why_confirmed: bool = False
    
    # What: 什么？核心对象
    what: str = ""
    what_confirmed: bool = False
    
    # Where: 在哪？上下文
    where: str = ""
    where_confirmed: bool = False
    
    # When: 何时？时效性
    when: str = ""
    when_confirmed: bool = False
    
    # How: 怎么做？方法
    how: str = ""
    how_confirmed: bool = False
    
    # How Much: 多少？量化指标
    how_much: str = ""
    how_much_confirmed: bool = False
    
    @property
    def convergence_rate(self) -> float:
        """计算收敛系数"""
        fields = [
            self.who_confirmed, self.why_confirmed, self.what_confirmed,
            self.where_confirmed, self.when_confirmed, self.how_confirmed,
            self.how_much_confirmed
        ]
        return sum(fields) / len(fields)


@dataclass
class SocraticQuestion:
    """苏格拉底提问"""
    dimension: str  # 5W2H维度
    question: str
    options: List[str]
    importance: str  # CRITICAL / IMPORTANT / OPTIONAL
    default_value: Optional[str] = None


class SocraticEngine:
    """
    苏格拉底引擎 - OpenClaw核心重构
    
    原则：
    1. 禁止直接执行
    2. 必须先探明需求
    3. 收敛系数<0.8禁止启动沙盒
    
    V2升级: 支持检索结果注入
    """
    
    # 工业领域关键词（联动CNC报价）
    INDUSTRIAL_KEYWORDS = {
        "cnc": ["加工", "定制", "零件", "材料", "精度", "公差"],
        "material": ["铝合金", "不锈钢", "铜", "塑料", "6061", "304"],
        "precision": ["±0.01", "±0.05", "±0.1", "高精度", "精密"],
        "quantity": ["数量", "批量", "单件", "打样"]
    }
    
    # 用户背景摘要（从MEMORY.md加载）
    USER_SUMMARY = {
        "name": "大帅",
        "resources": "2C 2G服务器，内存紧张",
        "business": "CNC报价系统，工业定制",
        "history": "74个任务，80%成功率"
    }
    
    def __init__(self):
        self.status = "IDLE"
        self.anchor_data = AnchorData()
        self.probe_history: List[Dict] = []
        self.retrieval_context: Optional[Dict] = None  # ⭐ 新增：检索上下文
    
    def set_retrieval_context(self, context: Dict):
        """
        设置检索上下文 (第二阶段新增)
        
        Args:
            context: 检索结果上下文
        """
        self.retrieval_context = context
        logger.info(f"[苏格拉底] 注入检索上下文: {context.get('intent', 'unknown')}")
        
    def start_engine(self, user_input: str) -> Dict:
        """
        [第一步]：苏格拉底+5W2H需求探明
        
        规则：禁止直接工作
        必须先调取User Summary，发起探明
        
        Returns:
            探明卡片（X-Styler渲染）
        """
        print(f"\n[苏格拉底引擎] 启动需求探明...")
        print(f"  输入: {user_input[:50]}...")
        
        # 1. 推理模糊意图
        intent_guess = self._infer_intent(user_input)
        print(f"  推理意图: {intent_guess}")
        
        # 2. 检查是否需要工业参数
        needs_industrial_params = self._check_industrial_keywords(user_input)
        
        # ⭐ 2.5 锚点自动填充（从输入提取）
        self._extract_anchors_from_input(user_input)
        print(f"  锚点填充后收敛度: {self.anchor_data.convergence_rate:.2f}")
        
        # 3. 生成5W2H提问
        questions = self._generate_5w2h_questions(
            user_input, intent_guess, needs_industrial_params
        )
        
        # 4. 记录探明历史
        self.probe_history.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "input": user_input,
            "intent": intent_guess,
            "questions": len(questions)
        })
        
        # 5. 返回探明卡片
        return {
            "status": "PROBING",
            "intent_guess": intent_guess,
            "convergence_rate": self.anchor_data.convergence_rate,
            "questions": [self._format_question(q) for q in questions],
            "message": "大帅，在动用沙盒前，需同步物理参数"
        }
    
    def _infer_intent(self, text: str) -> str:
        """推理模糊意图"""
        text_lower = text.lower()
        
        # CNC相关
        if any(kw in text for kw in ["报价", "CNC", "加工", "定制", "零件"]):
            return "cnc_quote"
        
        # 代码生成
        if any(kw in text for kw in ["写代码", "函数", "脚本", "Python"]):
            return "code_gen"
        
        # 翻译
        if any(kw in text for kw in ["翻译", "translate"]):
            return "translation"
        
        # 网页/文档
        if any(kw in text for kw in ["网页", "HTML", "创建", "生成"]):
            return "document_gen"
        
        # 查询
        if any(kw in text for kw in ["查询", "搜索", "查找"]):
            return "query"
        
        # 分析
        if any(kw in text for kw in ["分析", "统计", "计算"]):
            return "analysis"
        
        return "unknown"
    
    def _check_industrial_keywords(self, text: str) -> bool:
        """检查是否包含工业关键词"""
        for category, keywords in self.INDUSTRIAL_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return True
        return False
    
    def _extract_anchors_from_input(self, text: str):
        """
        从输入文本自动提取锚点信息
        
        填充 5W2H 维度，提升收敛度
        """
        # === WHAT: 核心对象 ===
        # 材质识别
        materials = {
            "铝合金6061": ["铝合金6061", "6061", "aluminum 6061"],
            "不锈钢304": ["不锈钢304", "304", "stainless 304"],
            "铝合金7075": ["铝合金7075", "7075"],
            "黄铜": ["黄铜", "铜", "brass"],
            "钛合金": ["钛合金", "钛", "titanium"],
        }
        for mat, keywords in materials.items():
            if any(kw in text for kw in keywords):
                self.anchor_data.what = mat
                self.anchor_data.what_confirmed = True
                print(f"  [锚点] 材质: {mat}")
                break
        
        # 报价类型识别
        if "单个零件" in text or "单件" in text:
            self.anchor_data.what = (self.anchor_data.what or "") + " 单个零件报价"
            if not self.anchor_data.what_confirmed:
                self.anchor_data.what_confirmed = True
        elif "批量" in text or "件" in text:
            self.anchor_data.what = (self.anchor_data.what or "") + " 批量报价"
            if not self.anchor_data.what_confirmed:
                self.anchor_data.what_confirmed = True
        
        # === HOW: 方法/精度 ===
        # 精度识别
        precisions = ["±0.01mm", "±0.02mm", "±0.05mm", "±0.1mm", "±0.2mm"]
        for prec in precisions:
            if prec in text:
                self.anchor_data.how = prec
                self.anchor_data.how_confirmed = True
                print(f"  [锚点] 精度: {prec}")
                break
        
        # 表面处理识别
        surface_treatments = ["阳极氧化", "镀锌", "喷砂", "抛光", "电镀", "发黑", "钝化"]
        for st in surface_treatments:
            if st in text:
                self.anchor_data.how = (self.anchor_data.how or "") + f" {st}"
                self.anchor_data.how_confirmed = True
                print(f"  [锚点] 表面处理: {st}")
                break
        
        # === HOW_MUCH: 数量 ===
        import re
        # 提取数量（如：100件、批量50）
        quantity_match = re.search(r'(\d+)\s*件', text)
        if quantity_match:
            self.anchor_data.how_much = f"{quantity_match.group(1)}件"
            self.anchor_data.how_much_confirmed = True
            print(f"  [锚点] 数量: {quantity_match.group(1)}件")
        elif "批量" in text:
            self.anchor_data.how_much = "批量"
            self.anchor_data.how_much_confirmed = True
        
        # === WHEN: 时效 ===
        if "紧急" in text or "急" in text:
            self.anchor_data.when = "紧急"
            self.anchor_data.when_confirmed = True
        elif "标准" in text:
            self.anchor_data.when = "标准"
            self.anchor_data.when_confirmed = True
        elif "宽松" in text or "不急" in text:
            self.anchor_data.when = "宽松"
            self.anchor_data.when_confirmed = True
        
        # === WHY: 目的 ===
        if "报价" in text:
            self.anchor_data.why = "获取报价"
            self.anchor_data.why_confirmed = True
        
        # === WHERE: 上下文（默认） ===
        self.anchor_data.where = "QQ私聊"
        self.anchor_data.where_confirmed = True
        
        # === WHO: 用户（默认） ===
        self.anchor_data.who = "用户"
        self.anchor_data.who_confirmed = True
        
        print(f"  [锚点] 收敛度: {self.anchor_data.convergence_rate:.2f}")
    
    def _generate_5w2h_questions(
        self, 
        text: str, 
        intent: str,
        needs_industrial: bool
    ) -> List[SocraticQuestion]:
        """生成5W2H提问 (第二阶段: 支持检索上下文)"""
        questions = []
        
        # ⭐ 检索上下文增强
        retrieval_hints = []
        if self.retrieval_context and self.retrieval_context.get('top_results'):
            top = self.retrieval_context['top_results'][0]
            retrieval_hints = self._extract_hints_from_retrieval(top, intent)
        
        # What: 核心对象（必问）
        if intent in ["cnc_quote", "document_gen", "code_gen"]:
            # ⭐ 使用检索提示优化问题
            what_question = self._generate_what_question(intent, text)
            if retrieval_hints:
                what_question += f" (参考案例提示: {', '.join(retrieval_hints[:2])})"
            
            questions.append(SocraticQuestion(
                dimension="what",
                question=what_question,
                options=self._get_what_options(intent),
                importance="CRITICAL"
            ))
        
        # How: 执行方式（重要）
        if intent in ["cnc_quote", "analysis", "query"]:
            questions.append(SocraticQuestion(
                dimension="how",
                question=self._generate_how_question(intent),
                options=self._get_how_options(intent),
                importance="IMPORTANT"
            ))
        
        # How Much: 量化指标（工业必需）
        if needs_industrial and intent == "cnc_quote":
            questions.append(SocraticQuestion(
                dimension="how_much",
                question="公差精度要求？",
                options=["±0.01mm (精密)", "±0.05mm (标准)", "±0.1mm (普通)"],
                importance="CRITICAL"
            ))
            
            questions.append(SocraticQuestion(
                dimension="what",
                question="材质锁定？",
                options=["铝合金6061", "不锈钢304", "其他材质"],
                importance="CRITICAL"
            ))
        
        # When: 时效性（可选）
        if intent in ["cnc_quote", "code_gen"]:
            questions.append(SocraticQuestion(
                dimension="when",
                question="时效要求？",
                options=["紧急 (<1小时)", "标准 (当天)", "宽松 (3天内)"],
                importance="OPTIONAL"
            ))
        
        return questions
    
    def _extract_hints_from_retrieval(self, result: Dict, intent: str) -> List[str]:
        """从检索结果提取提示"""
        hints = []
        text = result.get('text', '')
        
        if intent == "cnc_quote":
            # 提取材料关键词
            materials = ["铝合金", "不锈钢", "6061", "304", "钛合金", "铜"]
            for m in materials:
                if m in text:
                    hints.append(m)
            
            # 提取精度关键词
            if "公差" in text or "精度" in text:
                hints.append("精度要求")
        
        elif intent == "code_gen":
            langs = ["Python", "JavaScript", "Java", "SQL", "Shell"]
            for lang in langs:
                if lang in text:
                    hints.append(lang)
        
        return hints[:3]
    
    def _generate_what_question(self, intent: str, text: str) -> str:
        """生成What提问"""
        if intent == "cnc_quote":
            return "本次报价的核心对象是？"
        elif intent == "code_gen":
            return "您需要什么类型的代码？"
        elif intent == "document_gen":
            return "您想要创建什么类型的文档/网页？"
        return "请明确您的具体需求"
    
    def _get_what_options(self, intent: str) -> List[str]:
        """获取What选项"""
        if intent == "cnc_quote":
            return ["单个零件报价", "批量报价", "对比报价", "历史报价查询"]
        elif intent == "code_gen":
            return ["Python函数", "完整脚本", "API接口", "其他"]
        elif intent == "document_gen":
            return ["HTML网页", "Markdown文档", "数据报告", "其他"]
        return ["请详细描述"]
    
    def _generate_how_question(self, intent: str) -> str:
        """生成How提问"""
        if intent == "cnc_quote":
            return "优先调用哪种数据源？"
        elif intent == "analysis":
            return "分析深度？"
        return "执行偏好？"
    
    def _get_how_options(self, intent: str) -> List[str]:
        """获取How选项"""
        if intent == "cnc_quote":
            return ["GitHub开源库", "历史74组数据", "实时API", "全部对比"]
        elif intent == "analysis":
            return ["快速概览", "深度分析", "对比分析"]
        return ["自动选择", "手动指定"]
    
    def _format_question(self, q: SocraticQuestion) -> Dict:
        """格式化提问（用于X-Styler渲染）"""
        return {
            "dimension": q.dimension.upper(),
            "question": q.question,
            "options": q.options,
            "importance": q.importance,
            "color": self._get_dimension_color(q.dimension)
        }
    
    def _get_dimension_color(self, dimension: str) -> str:
        """获取维度颜色"""
        colors = {
            "what": "#1DA1F2",      # 蓝色
            "who": "#17BF63",       # 绿色
            "why": "#FFAD1F",       # 橙色
            "where": "#794BC4",     # 紫色
            "when": "#E0245E",      # 红色
            "how": "#1DA1F2",       # 蓝色
            "how_much": "#17BF63"   # 绿色
        }
        return colors.get(dimension, "#888888")
    
    def update_anchor(self, dimension: str, value: str) -> float:
        """
        更新锚点数据
        
        Returns:
            更新后的收敛系数
        """
        if dimension == "who":
            self.anchor_data.who = value
            self.anchor_data.who_confirmed = True
        elif dimension == "why":
            self.anchor_data.why = value
            self.anchor_data.why_confirmed = True
        elif dimension == "what":
            self.anchor_data.what = value
            self.anchor_data.what_confirmed = True
        elif dimension == "where":
            self.anchor_data.where = value
            self.anchor_data.where_confirmed = True
        elif dimension == "when":
            self.anchor_data.when = value
            self.anchor_data.when_confirmed = True
        elif dimension == "how":
            self.anchor_data.how = value
            self.anchor_data.how_confirmed = True
        elif dimension == "how_much":
            self.anchor_data.how_much = value
            self.anchor_data.how_much_confirmed = True
        
        return self.anchor_data.convergence_rate
    
    def can_execute(self) -> Tuple[bool, str]:
        """
        判断是否可以执行
        
        Returns:
            (是否可执行, 原因说明)
        """
        rate = self.anchor_data.convergence_rate
        
        if rate < ConvergenceLevel.CRITICAL.value:
            return False, "收敛系数过低，必须追问关键参数"
        
        if rate < ConvergenceLevel.LOW.value:
            return False, "需求不明确，建议补充信息"
        
        if rate < ConvergenceLevel.MEDIUM.value:
            return True, "需求基本明确，可以执行（建议补充细节）"
        
        if rate < ConvergenceLevel.HIGH.value:
            return True, "需求较明确，允许执行"
        
        return True, "需求锁定，直接执行"
    
    def get_status_report(self) -> Dict:
        """获取状态报告"""
        return {
            "status": self.status,
            "convergence_rate": self.anchor_data.convergence_rate,
            "anchor_summary": {
                "who": self.anchor_data.who or "未确定",
                "why": self.anchor_data.why or "未确定",
                "what": self.anchor_data.what or "未确定",
                "how": self.anchor_data.how or "未确定",
                "how_much": self.anchor_data.how_much or "未确定"
            },
            "probe_count": len(self.probe_history),
            "can_execute": self.can_execute()[0]
        }


# 测试入口
if __name__ == "__main__":
    engine = SocraticEngine()
    
    # 测试模糊输入
    result = engine.start_engine("帮我做一个报价")
    print("\n探明结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))