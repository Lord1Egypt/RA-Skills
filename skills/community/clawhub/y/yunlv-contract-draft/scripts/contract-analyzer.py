#!/usr/bin/env python3
"""
云旅合同分析器 - Yunlv Contract Analyzer
付款条件风险评级、贸易术语评估、条款完备性检查

命令:
  payment      - 付款条件风险评级
  trade        - 贸易术语风险评估
  completeness - 条款完备性检查
  report       - 完整风险报告
"""

import sys
import json
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

# ============ 数据模型 ============

@dataclass
class PaymentTerm:
    """付款条款"""
    name: str
    score: int      # 风险评分 0-100
    description: str
    risk_level: str
    suggestions: List[str]

@dataclass
class TradeTerm:
    """贸易术语"""
    name: str
    risk_score: int  # 风险评分
    description: str
    buyer_advantage: bool
    seller_risk: str

@dataclass
class ContractClause:
    """合同条款"""
    clause_name: str
    required: bool
    present: bool
    completeness: float  # 完整性百分比

# ============ 内置数据 ============

# 9种付款方式风险评分
PAYMENT_TERMS = {
    "T/T Prepaid": PaymentTerm(
        name="T/T Prepaid (100%预付)",
        score=5,
        description="买方在发货前100%付款，风险最低",
        risk_level="极低",
        suggestions=["鼓励客户使用此方式", "可给予一定付款折扣优惠"]
    ),
    "T/T 30% Deposit": PaymentTerm(
        name="T/T 30% Deposit + 70% BL Copy",
        score=25,
        description="30%定金，发货后凭提单副本付余款",
        risk_level="低",
        suggestions=["常见安全付款方式", "确保定金到账再生产", "余款未付前保留货权"]
    ),
    "T/T 30% Deposit + LC": PaymentTerm(
        name="T/T 30% Deposit + 70% LC at Sight",
        score=20,
        description="30%定金，70%通过即期信用证",
        risk_level="较低",
        suggestions=["信用证提供银行信用保障", "确保L/C条款清晰无软条款"]
    ),
    "LC at Sight": PaymentTerm(
        name="L/C at Sight (即期信用证)",
        score=30,
        description="买方银行在提交单证后即期付款",
        risk_level="中等",
        suggestions=["注意软条款风险", "确保单证完全符合", "选择资信好的开证行"]
    ),
    "LC 30/60/90 days": PaymentTerm(
        name="L/C 30/60/90 days",
        score=50,
        description="远期信用证，需在指定天数内付款",
        risk_level="中高",
        suggestions=["考虑福费廷或保理", "关注开证行资信", "控制交单时间节点"]
    ),
    "D/P at Sight": PaymentTerm(
        name="D/P at Sight (付款交单)",
        score=45,
        description="买方付款后才能获得单据",
        risk_level="中等",
        suggestions=["选择资信好的代收行", "避免货到目的地后无人提货"]
    ),
    "D/P 30/60 days": PaymentTerm(
        name="D/P 30/60 days after sight",
        score=60,
        description="远期付款交单",
        risk_level="较高",
        suggestions=["风险较大，建议转为D/A或预付", "了解当地法律法规"]
    ),
    "D/A": PaymentTerm(
        name="D/A (承兑交单)",
        score=75,
        description="买方承兑后即可获得单据，到期付款",
        risk_level="高",
        suggestions=["风险较高，需了解买方信用", "可结合出口信用保险", "控制赊账额度"]
    ),
    "O/A": PaymentTerm(
        name="O/A (赊账)",
        score=90,
        description="放账交易，完全依赖买方信用",
        risk_level="极高",
        suggestions=["强烈建议投保出口信用保险", "设置信用额度和账期", "定期跟进应收账款"]
    )
}

# 9种贸易术语风险评估
TRADE_TERMS = {
    "EXW": TradeTerm(
        name="EXW (Ex Works)",
        risk_score=20,
        description="卖方在其场所交货，买方承担所有风险",
        buyer_advantage=True,
        seller_risk="最低风险，但可能影响客户开发"
    ),
    "FOB": TradeTerm(
        name="FOB (Free on Board)",
        risk_score=40,
        description="卖方承担货物装上船前的费用和风险",
        buyer_advantage=False,
        seller_risk="需关注装船风险和文件准确性"
    ),
    "CFR": TradeTerm(
        name="CFR (Cost and Freight)",
        risk_score=50,
        description="卖方支付到目的港运费，风险在装船时转移",
        buyer_advantage=False,
        seller_risk="需注意卸货港选择和延误风险"
    ),
    "CIF": TradeTerm(
        name="CIF (Cost, Insurance, Freight)",
        risk_score=55,
        description="卖方支付运费和保险，货物装船后风险转移",
        buyer_advantage=False,
        seller_risk="需办理保险，关注保险条款"
    ),
    "DAP": TradeTerm(
        name="DAP (Delivered at Place)",
        risk_score=65,
        description="卖方承担除卸货外的所有费用和风险",
        buyer_advantage=True,
        seller_risk="需承担运输途中的风险"
    ),
    "DPU": TradeTerm(
        name="DPU (Delivered at Place Unpacked)",
        risk_score=70,
        description="卖方承担运送到目的地并卸货的费用和风险",
        buyer_advantage=True,
        seller_risk="需承担卸货责任和风险"
    ),
    "DDP": TradeTerm(
        name="DDP (Delivered Duty Paid)",
        risk_score=80,
        description="卖方承担所有费用和风险，包括进口关税",
        buyer_advantage=True,
        seller_risk="最高风险，需了解目的地法规"
    ),
    "FCA": TradeTerm(
        name="FCA (Free Carrier)",
        risk_score=30,
        description="卖方在指定地点交付给承运人",
        buyer_advantage=False,
        seller_risk="适用于多式联运，较为灵活"
    ),
    "CPT": TradeTerm(
        name="CPT (Carriage Paid to)",
        risk_score=45,
        description="卖方支付运费到指定目的地",
        buyer_advantage=False,
        seller_risk="需关注交货证明和风险转移点"
    )
}

# 三种合同必备条款清单
CONTRACT_CLAUSES = {
    "PI": {  # Proforma Invoice 形式发票
        "parties": {"name": "买卖双方信息", "required": True},
        "product": {"name": "产品信息(品名/规格/数量)", "required": True},
        "price": {"name": "单价和总价", "required": True},
        "terms": {"name": "贸易术语", "required": True},
        "payment": {"name": "付款方式", "required": True},
        "delivery": {"name": "交货期", "required": True},
        "port": {"name": "装卸港", "required": True},
        "package": {"name": "包装要求", "required": False},
        "quality": {"name": "质量标准", "required": True},
        "inspection": {"name": "验货条款", "required": False},
        "remark": {"name": "备注/特殊约定", "required": False}
    },
    "SC": {  # Sales Contract 销售合同
        "parties": {"name": "买卖双方完整信息", "required": True},
        "product": {"name": "产品详情", "required": True},
        "quantity": {"name": "数量及溢短装", "required": True},
        "price": {"name": "单价和总价", "required": True},
        "terms": {"name": "贸易术语", "required": True},
        "payment": {"name": "付款方式及时间", "required": True},
        "delivery": {"name": "交货期及地点", "required": True},
        "shipping": {"name": "运输方式", "required": True},
        "package": {"name": "包装及唛头", "required": True},
        "quality": {"name": "质量标准", "required": True},
        "inspection": {"name": "验货条款", "required": True},
        "claims": {"name": "索赔条款", "required": True},
        "penalty": {"name": "违约金条款", "required": True},
        "force_majeure": {"name": "不可抗力条款", "required": True},
        "arbitration": {"name": "仲裁条款", "required": True},
        "effectiveness": {"name": "合同生效条件", "required": True},
        "signatures": {"name": "双方签章", "required": True}
    },
    "MOU": {  # Memorandum of Understanding 谅解备忘录
        "purpose": {"name": "合作目的", "required": True},
        "scope": {"name": "合作范围", "required": True},
        "obligations": {"name": "双方义务", "required": True},
        "confidentiality": {"name": "保密条款", "required": True},
        "term": {"name": "协议期限", "required": True},
        "termination": {"name": "终止条款", "required": True},
        "governing_law": {"name": "适用法律", "required": True},
        "dispute": {"name": "争议解决", "required": True},
        "modification": {"name": "修改条款", "required": True},
        "signatures": {"name": "双方签章", "required": True}
    }
}

# ============ 核心函数 ============

def evaluate_payment_term(term_name: str) -> Dict:
    """付款条件风险评级"""
    # 模糊匹配
    best_match = None
    best_score = 0
    
    for key, term in PAYMENT_TERMS.items():
        # 计算匹配度
        key_words = set(key.lower().split())
        input_words = set(term_name.lower().split())
        overlap = len(key_words & input_words)
        if overlap > best_score:
            best_score = overlap
            best_match = (key, term)
    
    if best_match:
        key, term = best_match
        return {
            "input_term": term_name,
            "matched_term": key,
            "risk_score": term.score,
            "risk_level": term.risk_level,
            "description": term.description,
            "suggestions": term.suggestions,
            "recommendation": _get_payment_recommendation(term.score)
        }
    
    return {
        "input_term": term_name,
        "matched_term": None,
        "risk_score": None,
        "risk_level": "未知",
        "description": "未识别的付款方式",
        "suggestions": ["请使用标准付款术语", "建议从以下方式中选择: " + ", ".join(PAYMENT_TERMS.keys())],
        "recommendation": "请确认付款方式后重新评估"
    }

def _get_payment_recommendation(score: int) -> str:
    """根据风险评分给出建议"""
    if score <= 20:
        return "优选付款方式，可积极推广"
    elif score <= 40:
        return "推荐使用，可适当提供优惠"
    elif score <= 60:
        return "谨慎使用，注意风险控制"
    else:
        return "高风险付款方式，建议结合保险或其他担保措施"

def evaluate_trade_term(term_name: str) -> Dict:
    """贸易术语风险评估"""
    # 精确匹配
    for key, term in TRADE_TERMS.items():
        if key.lower() == term_name.lower() or term.name.lower().startswith(term_name.lower()):
            return {
                "input_term": term_name,
                "matched_term": key,
                "full_name": term.name,
                "risk_score": term.risk_score,
                "description": term.description,
                "buyer_advantage": term.buyer_advantage,
                "seller_risk": term.seller_risk,
                "recommendation": _get_trade_recommendation(term)
            }
    
    # 模糊匹配
    for key, term in TRADE_TERMS.items():
        if term_name.lower() in term.name.lower() or key.lower() in term_name.lower():
            return {
                "input_term": term_name,
                "matched_term": key,
                "full_name": term.name,
                "risk_score": term.risk_score,
                "description": term.description,
                "buyer_advantage": term.buyer_advantage,
                "seller_risk": term.seller_risk,
                "recommendation": _get_trade_recommendation(term)
            }
    
    return {
        "input_term": term_name,
        "matched_term": None,
        "risk_score": None,
        "description": "未识别的贸易术语",
        "suggestions": ["请使用标准Incoterms 2020术语", "可用术语: " + ", ".join(TRADE_TERMS.keys())],
        "recommendation": "请确认贸易术语后重新评估"
    }

def _get_trade_recommendation(term: TradeTerm) -> str:
    """根据贸易术语给出建议"""
    if term.risk_score <= 30:
        return "卖方风险低，可优先考虑"
    elif term.risk_score <= 50:
        return "风险适中，建议完善合同条款"
    else:
        return "卖方风险较高，需评估客户和运输风险"

def check_contract_completeness(contract_type: str, present_clauses: List[str]) -> Dict:
    """条款完备性检查"""
    if contract_type.upper() not in CONTRACT_CLAUSES:
        return {
            "error": f"未知合同类型: {contract_type}",
            "valid_types": list(CONTRACT_CLAUSES.keys())
        }
    
    required_clauses = CONTRACT_CLAUSES[contract_type.upper()]
    present_set = set(clause.lower() for clause in present_clauses)
    
    results = []
    present_count = 0
    required_count = 0
    
    for clause_key, clause_info in required_clauses.items():
        is_present = clause_key.lower() in present_set
        if clause_info["required"]:
            required_count += 1
            if is_present:
                present_count += 1
        
        results.append({
            "clause_key": clause_key,
            "clause_name": clause_info["name"],
            "required": clause_info["required"],
            "present": is_present,
            "status": "完整" if is_present else ("必填" if clause_info["required"] else "可选")
        })
    
    completeness = (sum(1 for r in results if r["present"]) / len(results)) * 100 if results else 0
    required_completeness = (present_count / required_count) * 100 if required_count > 0 else 0
    
    return {
        "contract_type": contract_type,
        "total_clauses": len(results),
        "present_clauses": sum(1 for r in results if r["present"]),
        "required_clauses": required_count,
        "required_present": present_count,
        "completeness_pct": round(completeness, 1),
        "required_completeness_pct": round(required_completeness, 1),
        "clause_details": results,
        "missing_required": [r["clause_name"] for r in results if r["required"] and not r["present"]],
        "recommendation": _get_completeness_recommendation(required_completeness)
    }

def _get_completeness_recommendation(score: float) -> str:
    """根据完备性给出建议"""
    if score >= 100:
        return "条款完备，风险较低"
    elif score >= 80:
        return "条款基本完备，建议补充缺失项"
    elif score >= 60:
        return "条款存在缺失，建议完善关键条款"
    else:
        return "条款严重缺失，建议重新审阅合同结构"

def generate_full_report(
    payment_term: str,
    trade_term: str,
    contract_type: str = "SC",
    present_clauses: List[str] = None
) -> Dict:
    """生成完整风险报告"""
    if present_clauses is None:
        present_clauses = []
    
    payment_eval = evaluate_payment_term(payment_term)
    trade_eval = evaluate_trade_term(trade_term)
    completeness = check_contract_completeness(contract_type, present_clauses)
    
    # 加权计算总风险
    payment_weight = 0.4
    trade_weight = 0.3
    completeness_weight = 0.3
    
    # 完备性转换为风险分（100-完备性）
    completeness_risk = 100 - completeness.get("completeness_pct", 50)
    
    if payment_eval.get("risk_score") is not None and trade_eval.get("risk_score") is not None:
        total_risk = (
            payment_eval["risk_score"] * payment_weight +
            trade_eval["risk_score"] * trade_weight +
            completeness_risk * completeness_weight
        )
    else:
        total_risk = None
    
    # 风险等级
    if total_risk is not None:
        if total_risk <= 30:
            risk_level = "低风险"
        elif total_risk <= 50:
            risk_level = "中等风险"
        elif total_risk <= 70:
            risk_level = "较高风险"
        else:
            risk_level = "高风险"
    else:
        risk_level = "评估不完整"
    
    return {
        "summary": {
            "total_risk_score": round(total_risk, 1) if total_risk else None,
            "risk_level": risk_level,
            "payment_risk": payment_eval.get("risk_level", "未知"),
            "trade_risk": "低" if trade_eval.get("risk_score", 100) <= 30 else ("中" if trade_eval.get("risk_score", 100) <= 50 else "高"),
            "completeness": f"{completeness.get('completeness_pct', 0)}%"
        },
        "payment_analysis": payment_eval,
        "trade_term_analysis": trade_eval,
        "completeness_check": completeness,
        "recommendations": _generate_recommendations(payment_eval, trade_eval, completeness)
    }

def _generate_recommendations(payment_eval: Dict, trade_eval: Dict, completeness: Dict) -> List[str]:
    """生成综合建议"""
    recommendations = []
    
    # 付款建议
    if payment_eval.get("risk_score", 100) > 60:
        recommendations.append("建议结合出口信用保险降低收款风险")
        recommendations.append("可考虑要求买方提供第三方担保")
    
    # 贸易术语建议
    if trade_eval.get("risk_score", 0) > 60:
        recommendations.append("考虑调整贸易术语以降低卖方风险")
        recommendations.append("若使用DDP/DAP，需充分了解目的地合规要求")
    
    # 完备性建议
    missing = completeness.get("missing_required", [])
    if missing:
        recommendations.append(f"建议补充以下必填条款: {', '.join(missing)}")
    
    if not recommendations:
        recommendations.append("合同条款整体风险可控，建议持续跟进执行")
    
    return recommendations

# ============ CLI 入口 ============

def main():
    parser = argparse.ArgumentParser(
        description="云旅合同分析器 - 外贸合同风险评估工具"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # payment命令
    p_pay = subparsers.add_parser('payment', help='付款条件风险评级')
    p_pay.add_argument('--term', required=True, help='付款方式名称')
    
    # trade命令
    p_trade = subparsers.add_parser('trade', help='贸易术语风险评估')
    p_trade.add_argument('--term', required=True, help='贸易术语(如FOB/CIF)')
    
    # completeness命令
    p_comp = subparsers.add_parser('completeness', help='条款完备性检查')
    p_comp.add_argument('--type', required=True, help='合同类型: PI/SC/MOU')
    p_comp.add_argument('--clauses', help='已包含条款(逗号分隔)')
    
    # report命令
    p_report = subparsers.add_parser('report', help='完整风险报告')
    p_report.add_argument('--payment', required=True, help='付款方式')
    p_report.add_argument('--trade', required=True, help='贸易术语')
    p_report.add_argument('--contract-type', default='SC', help='合同类型')
    p_report.add_argument('--clauses', help='已包含条款(逗号分隔)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'payment':
        result = evaluate_payment_term(args.term)
    elif args.command == 'trade':
        result = evaluate_trade_term(args.term)
    elif args.command == 'completeness':
        clauses = args.clauses.split(',') if args.clauses else []
        result = check_contract_completeness(args.type, clauses)
    elif args.command == 'report':
        clauses = args.clauses.split(',') if args.clauses else []
        result = generate_full_report(
            payment_term=args.payment,
            trade_term=args.trade,
            contract_type=args.contract_type,
            present_clauses=clauses
        )
    else:
        print(f"未知命令: {args.command}")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
