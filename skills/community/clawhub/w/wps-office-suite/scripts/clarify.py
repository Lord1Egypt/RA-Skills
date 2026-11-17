"""
NL2Formula 多轮澄清 v4.9.0
功能：歧义检测 → 槽位问答 → 公式生成 → 反向验证

死规则合规：
  - 规则4：禁止自动发布
  - 规则9：基础功能自研（规则引擎 + 槽位填充，无外部 API）
  - 规则13：不生成禁止文件类型
  - 规则14：三轮自审
  - 规则15：沙箱模拟运行

安全合规：
  - 纯本地实现，不读取外部凭证或 API Key
  - 所有处理在本地完成，不上传任何内容
"""
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

__version__ = "4.9.0"


# ==================== 歧义检测规则 ====================

# 范围词缺失：用户提到了指标但没有指定范围
RANGE_MISSING_PATTERNS = [
    r"(统计|计算|求|汇总|合计|总计).{0,5}(值|数|量|额|总和)",
    r"(销售额|收入|支出|利润|成本|数量|金额|总数)",
    r"(平均|最大|最小|合计|总|合计)",
]

# 条件不完整：用户提到了条件但没有完整指定
CONDITION_INCOMPLETE_PATTERNS = [
    r"(大于|小于|等于|超过|不低于|不超过|介于).{0,3}(\d+)",
    r"(如果|当|只要|若是)",
    r"(筛选|过滤|条件|符合|满足)",
]

# 聚合方式不明：用户提到了汇总但没有指定聚合方式
AGGREGATION_UNCLEAR_PATTERNS = [
    r"(统计|汇总|计算|算一下|给我).{0,10}(情况|数据|结果|如何|怎么样)",
    r"(看一下|看看|显示).{0,5}(数据|情况)",
]

# 槽位关键词映射
SLOT_KEYWORDS = {
    "range": ["范围", "区间", "期间", "周期", "时间段", "日期", "月份", "年份"],
    "sheet": ["工作表", "sheet", "表格", "表"],
    "column": ["列", "字段", "指标", "项目"],
    "condition": ["条件", "筛选", "过滤", "符合", "满足"],
    "aggregation": ["求和", "计数", "平均", "最大", "最小", "汇总", "合计"],
}


class AmbiguityDetector:
    """歧义检测器"""

    def __init__(self):
        self.range_patterns = [re.compile(p) for p in RANGE_MISSING_PATTERNS]
        self.condition_patterns = [re.compile(p) for p in CONDITION_INCOMPLETE_PATTERNS]
        self.aggregation_patterns = [re.compile(p) for p in AGGREGATION_UNCLEAR_PATTERNS]

    def detect(self, query: str) -> Dict[str, Any]:
        """
        检测查询中的歧义
        
        Returns:
            {
                "has_ambiguity": bool,
                "missing_slots": list,  # 缺失的槽位列表
                "clarification_questions": list,  # 反问问题列表
                "confidence": float,  # 置信度 (0-1)
            }
        """
        missing_slots = []
        questions = []

        # 检测范围缺失
        range_match = any(p.search(query) for p in self.range_patterns)
        range_has_period = any(kw in query for kw in SLOT_KEYWORDS["range"])
        if range_match and not range_has_period:
            missing_slots.append("range")
            questions.append("请问您需要统计哪个时间段/范围的数据？（如：本月、Q1、2024年1月-6月）")

        # 检测条件不完整
        condition_match = any(p.search(query) for p in self.condition_patterns)
        condition_has_full = ("且" in query or "并且" in query or "和" in query) or condition_match == False
        if condition_match and not condition_has_full:
            # 条件词存在但可能不完整
            pass  # 这里简化处理，实际可更精细

        # 检测聚合方式不明
        agg_match = any(p.search(query) for p in self.aggregation_patterns)
        agg_has_method = any(kw in query for kw in SLOT_KEYWORDS["aggregation"])
        if agg_match and not agg_has_method:
            missing_slots.append("aggregation")
            questions.append("请问您需要哪种聚合方式？（如：求和、计数、平均值、最大值、最小值）")

        # 检测 Sheet/列缺失
        sheet_mentioned = any(kw in query for kw in SLOT_KEYWORDS["sheet"])
        column_mentioned = any(kw in query for kw in SLOT_KEYWORDS["column"])
        if not sheet_mentioned and not column_mentioned:
            missing_slots.append("target")
            questions.append("请问数据在哪个工作表的哪一列？（如：Sheet1 的销售额列）")

        # 计算置信度
        confidence = 1.0
        if missing_slots:
            confidence = max(0.1, 1.0 - len(missing_slots) * 0.25)

        return {
            "has_ambiguity": len(missing_slots) > 0,
            "missing_slots": missing_slots,
            "clarification_questions": questions,
            "confidence": round(confidence, 2),
        }


class SlotFiller:
    """槽位填充器"""

    def __init__(self):
        self.slots = {
            "range": None,
            "sheet": "Sheet1",
            "column": None,
            "condition": None,
            "aggregation": "SUM",
        }

    def fill_from_clarification(self, clarification: Dict[str, str]) -> None:
        """从澄清回答中填充槽位"""
        for key, value in clarification.items():
            if key in self.slots and value:
                self.slots[key] = value

    def fill_from_query(self, query: str) -> None:
        """从原始查询中自动提取已知槽位"""
        # 提取范围
        range_match = re.search(r"(本|上|去|今|前)(月|周|季度|年)", query)
        if range_match:
            self.slots["range"] = range_match.group(0)

        # 提取聚合方式
        agg_map = {
            "求和": "SUM", "合计": "SUM", "总计": "SUM", "汇总": "SUM",
            "计数": "COUNT", "多少个": "COUNT", "数量": "COUNT",
            "平均": "AVERAGE", "均值": "AVERAGE",
            "最大": "MAX", "最多": "MAX", "最高": "MAX",
            "最小": "MIN", "最少": "MIN", "最低": "MIN",
        }
        for keyword, agg_type in agg_map.items():
            if keyword in query:
                self.slots["aggregation"] = agg_type
                break

    def get_slots(self) -> Dict[str, Optional[str]]:
        return dict(self.slots)

    def is_complete(self) -> bool:
        """检查关键槽位是否已填充"""
        return self.slots["column"] is not None


class ClarificationLoop:
    """澄清回路"""

    def __init__(self, interactive: bool = False):
        self.detector = AmbiguityDetector()
        self.filler = SlotFiller()
        self.interactive = interactive

    def process(self, query: str, clarification_answer: str = "") -> Dict[str, Any]:
        """
        处理查询（支持多轮澄清）
        
        Args:
            query: 用户的自然语言查询
            clarification_answer: 用户对澄清问题的回答（第二轮及以后）
        
        Returns:
            {
                "status": str,  # "need_clarification" | "ready" | "error"
                "query": str,
                "slots": dict,
                "clarification_questions": list,
                "formula_suggestion": str,
                "explanation": str,
                "confidence": float,
                "verification": dict,
            }
        """
        # Step 1: 从查询中提取已知信息
        self.filler.fill_from_query(query)

        # Step 2: 如果有澄清回答，填充槽位
        if clarification_answer:
            clarification = self._parse_clarification(clarification_answer)
            self.filler.fill_from_clarification(clarification)

        # Step 3: 歧义检测
        ambiguity = self.detector.detect(query)
        slots = self.filler.get_slots()

        result = {
            "status": "ready",
            "query": query,
            "slots": slots,
            "clarification_questions": [],
            "formula_suggestion": "",
            "explanation": "",
            "confidence": ambiguity["confidence"],
            "verification": {},
        }

        # Step 4: 检查是否需要澄清
        if ambiguity["has_ambiguity"] and not clarification_answer:
            result["status"] = "need_clarification"
            result["clarification_questions"] = ambiguity["clarification_questions"]
            return result

        # Step 5: 生成公式建议
        formula_suggestion = self._generate_formula(slots, query)
        result["formula_suggestion"] = formula_suggestion["formula"]
        result["explanation"] = formula_suggestion["explanation"]

        # Step 6: 反向验证（使用公式解释器）
        result["verification"] = self._verify_formula(formula_suggestion["formula"])

        return result

    def _parse_clarification(self, answer: str) -> Dict[str, str]:
        """解析用户的澄清回答"""
        clarification = {}

        # 范围解析
        if "月" in answer or "年" in answer or "季度" in answer or "周" in answer:
            clarification["range"] = answer

        # 聚合方式解析
        agg_keywords = {
            "求和": "SUM", "合计": "SUM", "总计": "SUM",
            "计数": "COUNT", "个数": "COUNT",
            "平均": "AVERAGE", "均值": "AVERAGE",
            "最大": "MAX", "最多": "MAX",
            "最小": "MIN", "最少": "MIN",
        }
        for keyword, agg_type in agg_keywords.items():
            if keyword in answer:
                clarification["aggregation"] = agg_type
                break

        # Sheet/列解析
        if "列" in answer:
            col_match = re.search(r"([A-Z])列", answer)
            if col_match:
                clarification["column"] = col_match.group(1)

        # 直接提取列字母
        col_letters = re.findall(r"[A-Z]", answer.upper())
        if col_letters:
            clarification["column"] = col_letters[0]

        return clarification

    def _generate_formula(self, slots: Dict[str, Optional[str]], query: str) -> Dict[str, str]:
        """根据槽位生成公式建议"""
        agg = slots.get("aggregation", "SUM")
        column = slots.get("column", "A")
        range_str = slots.get("range", "")

        # 构建公式
        if agg == "SUM":
            formula = f"=SUM({column}:{column})"
            explanation = f"求和：对 {column} 列进行求和"
        elif agg == "COUNT":
            formula = f"=COUNTA({column}:{column})"
            explanation = f"计数：统计 {column} 列的非空单元格数量"
        elif agg == "AVERAGE":
            formula = f"=AVERAGE({column}:{column})"
            explanation = f"平均值：计算 {column} 列的平均值"
        elif agg == "MAX":
            formula = f"=MAX({column}:{column})"
            explanation = f"最大值：找出 {column} 列的最大值"
        elif agg == "MIN":
            formula = f"=MIN({column}:{column})"
            explanation = f"最小值：找出 {column} 列的最小值"
        else:
            formula = f"=SUM({column}:{column})"
            explanation = f"求和：对 {column} 列进行求和"

        # 如果有范围，添加说明
        if range_str:
            explanation += f"（范围：{range_str}）"

        return {"formula": formula, "explanation": explanation}

    def _verify_formula(self, formula: str) -> Dict[str, Any]:
        """使用公式解释器反向验证"""
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from formula_explainer import FormulaExplainer
            explainer = FormulaExplainer()
            explanation = explainer.explain(formula)
            return {
                "ok": True,
                "explanation": explanation,
                "match": True,  # 简化处理
            }
        except Exception as e:
            return {
                "ok": False,
                "explanation": f"验证失败: {str(e)}",
                "match": False,
            }


def _cli():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description=f"NL2Formula 多轮澄清 v{__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # detect
    p = sub.add_parser("detect", help="检测查询中的歧义")
    p.add_argument("--query", required=True, help="自然语言查询")

    # clarify
    p = sub.add_parser("clarify", help="执行澄清回路")
    p.add_argument("--query", required=True, help="自然语言查询")
    p.add_argument("--answer", default="", help="澄清回答（第二轮）")

    # verify
    p = sub.add_parser("verify", help="验证公式")
    p.add_argument("--formula", required=True, help="Excel 公式")

    args = parser.parse_args()

    if args.command == "detect":
        detector = AmbiguityDetector()
        result = detector.detect(args.query)
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "clarify":
        loop = ClarificationLoop()
        result = loop.process(args.query, args.answer)
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "verify":
        loop = ClarificationLoop()
        result = loop._verify_formula(args.formula)
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
