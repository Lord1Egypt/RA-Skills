#!/usr/bin/env python3
"""
不符合项规则判定脚本
功能:基于预设规则和ISO条款辅助判定不符合项性质
"""
import json
import argparse
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).parent.parent / "assets" / "nc_data.json"

# 判定规则定义
EVALUATION_RULES = {
    "major": {
        "keywords": [
            "未建立", "未形成", "缺失", "未识别", "未规定",
            "未执行", "完全未实施", "系统性", "广泛性",
            "重复发生", "同类问题再次", "历史遗留",
            "影响产品", "影响质量", "影响安全", "不符合法规"
        ],
        "patterns": [
            r"完全没", r"根本未", r"完全未", r"严重",
            r"多次", r"再次", r"重复", r"普遍"
        ]
    },
    "minor": {
        "keywords": [
            "个别", "部分", "偶尔", "单次", "局部",
            "不完整", "不充分", "轻微", "偏差",
            "未按要求", "不规范", "欠完善"
        ],
        "patterns": [
            r"一项", r"一份", r"一台", r"个别",
            r"部分", r"单一", r"偶然"
        ]
    },
    "observation": {
        "keywords": [
            "建议", "改进", "优化", "提升", "可以考虑",
            "潜在", "可能", "观察", "关注", "良好实践"
        ],
        "patterns": [
            r"建议", r"改进机会", r"潜在风险", r"可进一步"
        ]
    }
}

# ISO条款相关判定
CLAUSE_WEIGHTS = {
    "major_clauses": [
        "4.1", "4.2",  # 体系范围/质量手册
        "5.1", "5.2", "5.3",  # 领导作用
        "6.1", "6.2",  # 风险与目标
        "7.1", "7.2", "7.3",  # 资源与能力
        "8.1", "8.2", "8.3", "8.4", "8.5", "8.6", "8.7"  # 运营控制
    ],
    "high_risk_clauses": [
        "7.1.5",  # 监视测量设备
        "8.2.3",  # 产品要求的评审
        "8.4.2",  # 供方评审
        "8.5.1",  # 生产服务提供
        "8.6",  # 产品放行
        "8.7"  # 不合格输出
    ]
}

def load_data():
    """加载数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"non_conformances": []}

def score_category(text, category):
    """计算文本在某个类别的得分"""
    score = 0
    text_lower = text.lower()
    
    # 关键词匹配
    for keyword in EVALUATION_RULES[category]["keywords"]:
        if keyword.lower() in text_lower:
            score += 2
    
    # 正则模式匹配
    import re
    for pattern in EVALUATION_RULES[category]["patterns"]:
        if re.search(pattern, text):
            score += 3
    
    return score

def evaluate_by_description(description):
    """基于描述内容判定"""
    scores = {cat: score_category(description, cat) for cat in EVALUATION_RULES}
    
    max_score = max(scores.values())
    if max_score == 0:
        return "minor"  # 默认轻微不符合
    
    for cat, score in scores.items():
        if score == max_score:
            return cat
    
    return "minor"

def evaluate_by_clause(clause):
    """基于条款判定"""
    if not clause:
        return None
    
    # 检查是否为高风险条款
    for high_risk in CLAUSE_WEIGHTS["high_risk_clauses"]:
        if clause.startswith(high_risk):
            return "major"
    
    # 检查是否为重要条款
    for major in CLAUSE_WEIGHTS["major_clauses"]:
        if clause.startswith(major):
            return "minor"  # 重要条款但非高风险
    
    return None

def evaluate_nc(nc_id=None, description=None, clause=None):
    """综合判定不符合项"""
    result = {
        "nc_id": nc_id,
        "input_description": description,
        "input_clause": clause,
        "scores": {},
        "suggested_category": None,
        "reasoning": [],
        "confidence": "low"
    }
    
    data = load_data()
    
    # 如果提供了NC ID，从数据库获取
    if nc_id:
        nc_list = [nc for nc in data['non_conformances'] if nc['id'] == nc_id]
        if nc_list:
            nc = nc_list[0]
            description = description or nc['description']
            clause = clause or nc['clause']
            result['nc_id'] = nc_id
            result['nc_title'] = nc['title']
    
    # 描述判定
    if description:
        desc_scores = {cat: score_category(description, cat) for cat in EVALUATION_RULES}
        result['scores']['description'] = desc_scores
        
        desc_category = evaluate_by_description(description)
        result['reasoning'].append(f"基于描述判定为: {desc_category}")
        result['suggested_category'] = desc_category
        result['confidence'] = "medium"
    
    # 条款判定
    if clause:
        clause_category = evaluate_by_clause(clause)
        result['clause_indicator'] = clause_category
        if clause_category:
            result['reasoning'].append(f"基于条款{clause}判定为: {clause_category}")
            
            # 综合判定
            if clause_category == "major" and result['suggested_category'] != "major":
                result['suggested_category'] = "major"
                result['reasoning'].append("条款重要性提升判定级别")
            result['confidence'] = "high"
    
    return result

def evaluate(args):
    """执行判定"""
    if not args.nc_id and not args.input:
        result = {"status": "error", "message": "必须提供--nc-id或--input参数"}
        print(json.dumps(result, ensure_ascii=False))
        return result
    
    result = evaluate_nc(
        nc_id=args.nc_id,
        description=args.input,
        clause=args.clause
    )
    
    # 格式化输出
    output = {
        "status": "success",
        "suggested_category": result['suggested_category'],
        "confidence": result['confidence'],
        "reasoning": result['reasoning'],
        "details": result
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return output

def main():
    parser = argparse.ArgumentParser(description='规则辅助判定不符合项')
    parser.add_argument('--nc-id', help='不符合项ID')
    parser.add_argument('--input', help='描述文本(直接判定时使用)')
    parser.add_argument('--clause', help='ISO条款编号')
    
    args = parser.parse_args()
    evaluate(args)

if __name__ == "__main__":
    main()
