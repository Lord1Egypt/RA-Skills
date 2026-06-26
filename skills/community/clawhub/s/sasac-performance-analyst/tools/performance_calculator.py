#!/usr/bin/env python3
"""
SASAC Performance Calculator - 国资委绩效计算引擎
基于2025年版《企业绩效评价标准值》的五档线性插值评分系统

Author: 王东杰 (Wang Dongjie)
License: MIT
Version: 2.0.0
"""

import json
import os
from typing import Dict, List, Optional, Tuple, Union

# ─── Metric Definitions ───────────────────────────────────────────

METRIC_DEFS = {
    # 盈利回报维度 (Profitability)
    "roe":        {"name": "净资产收益率",       "unit": "%",  "dim": "盈利回报", "higher_better": True},
    "opm":        {"name": "营业收入利润率",     "unit": "%",  "dim": "盈利回报", "higher_better": True},
    "roa":        {"name": "总资产报酬率",       "unit": "%",  "dim": "盈利回报", "higher_better": True},
    "cash_cov":   {"name": "盈余现金保障倍数",   "unit": "倍", "dim": "盈利回报", "higher_better": True},
    # 资产运营维度 (Operations)
    "tat":        {"name": "总资产周转率",       "unit": "次", "dim": "资产运营", "higher_better": True},
    "art":        {"name": "应收账款周转率",     "unit": "次", "dim": "资产运营", "higher_better": True},
    "cat":        {"name": "流动资产周转率",     "unit": "次", "dim": "资产运营", "higher_better": True},
    "two_gold":   {"name": "两金占流动资产比重", "unit": "%",  "dim": "资产运营", "higher_better": False},
    # 风险防控维度 (Risk)
    "dar":        {"name": "资产负债率",         "unit": "%",  "dim": "风险防控", "higher_better": False},
    "cash_debt":  {"name": "现金流动负债比率",   "unit": "%",  "dim": "风险防控", "higher_better": True},
    "int_debt":   {"name": "带息负债比率",       "unit": "%",  "dim": "风险防控", "higher_better": False},
    "icr":        {"name": "已获利息倍数",       "unit": "倍", "dim": "风险防控", "higher_better": True},
    # 持续发展维度 (Growth)
    "rd":         {"name": "研发经费投入强度",   "unit": "%",  "dim": "持续发展", "higher_better": True},
    "lp":         {"name": "全员劳动生产率",     "unit": "万元/人", "dim": "持续发展", "higher_better": True},
    "eva":        {"name": "经济增加值率",       "unit": "%",  "dim": "持续发展", "higher_better": True},
    "soc":        {"name": "国有资本保值增值率", "unit": "%",  "dim": "持续发展", "higher_better": True},
    # 补充指标 (Supplementary)
    "ocf_ratio":  {"name": "营业现金比率",       "unit": "%",  "dim": "补充指标", "higher_better": True},
    "soc_return": {"name": "国有资本回报率",     "unit": "%",  "dim": "补充指标", "higher_better": True},
    "ebitda":     {"name": "EBITDA率",           "unit": "%",  "dim": "补充指标", "higher_better": True},
    "cost_per":   {"name": "百元收入支付的成本费用", "unit": "元", "dim": "补充指标", "higher_better": False},
    "inv_turn":   {"name": "存货周转率",         "unit": "次", "dim": "补充指标", "higher_better": True},
    "quick":      {"name": "速动比率",           "unit": "倍", "dim": "补充指标", "higher_better": True},
    "profit_g":   {"name": "利润总额增长率",     "unit": "%",  "dim": "补充指标", "higher_better": True},
    "rev_g":      {"name": "营业总收入增长率",   "unit": "%",  "dim": "补充指标", "higher_better": True},
}

DIMENSION_WEIGHTS = {
    "盈利回报": 0.30,
    "资产运营": 0.20,
    "风险防控": 0.25,
    "持续发展": 0.25,
}

LEVEL_NAMES = ["优秀值", "良好值", "中等值", "较低值", "较差值"]
LEVEL_SCORES = [100, 80, 60, 40, 20]

GRADE_MAP = [
    (85, "A+ 卓越"),
    (70, "A 优秀"),
    (55, "B 良好"),
    (40, "C 中等"),
    (25, "D 较低"),
    (0,  "E 较差"),
]


# ─── Data Loading ─────────────────────────────────────────────────

class SASACDatabase:
    """国资委绩效评价标准值数据库"""
    
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.data_dir = data_dir
        self._domestic = None
        self._international = None
        self._index = {}
        # Eagerly load to build index
        _ = self.domestic
        _ = self.international
    
    @property
    def domestic(self) -> List[dict]:
        if self._domestic is None:
            self._load_domestic()
        return self._domestic
    
    @property
    def international(self) -> List[dict]:
        if self._international is None:
            self._load_international()
        return self._international
    
    def _load_domestic(self):
        path = os.path.join(self.data_dir, 'sasac_2025_standards.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self._domestic = data['tables']
        self._build_index(self._domestic, prefix='domestic')
    
    def _load_international(self):
        path = os.path.join(self.data_dir, 'international_standards.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self._international = data['tables']
        self._build_index(self._international, prefix='intl')
    
    def _build_index(self, tables, prefix='domestic'):
        for t in tables:
            key = f"{prefix}:{t['industry']}:{t['size']}"
            self._index[key] = t
    
    def get_benchmark(self, industry: str, size: str = "全行业", 
                      intl: bool = False) -> Optional[dict]:
        """获取行业标准值"""
        prefix = 'intl' if intl else 'domestic'
        key = f"{prefix}:{industry}:{size}"
        if key in self._index:
            return self._index[key]
        # Fuzzy match
        for k, v in self._index.items():
            if v['industry'] == industry and v['size'] == size:
                if (prefix == 'intl') == v.get('intl', False):
                    return v
        return None
    
    def get_industries(self, intl: bool = False) -> List[str]:
        """获取所有行业名称"""
        tables = self.international if intl else self.domestic
        return sorted(set(t['industry'] for t in tables))
    
    def get_sectors(self, intl: bool = False) -> Dict[str, set]:
        """获取行业大类→行业集合映射"""
        tables = self.domestic if not intl else self.international
        sectors = {}
        for t in tables:
            sectors.setdefault(t['sector'], set()).add(t['industry'])
        return sectors
    
    def get_sizes_for_industry(self, industry: str, intl: bool = False) -> List[str]:
        """获取某行业的可用规模分类"""
        tables = self.international if intl else self.domestic
        return sorted(set(t['size'] for t in tables if t['industry'] == industry))


# ─── Scoring Engine ────────────────────────────────────────────────

def linear_interpolation(value: float, benchmark: List[float], 
                          higher_better: bool = True) -> Tuple[float, str]:
    """
    五档线性插值评分
    
    Args:
        value: 企业实际值
        benchmark: [优秀值, 良好值, 中等值, 较低值, 较差值]
        higher_better: True=越高越好(如ROE), False=越低越好(如资产负债率)
    
    Returns:
        (score: 0-100, level_name: str)
    """
    excellent, good, medium, low, poor = benchmark
    
    # For "lower is better" metrics, reverse the interpretation
    if not higher_better:
        # Lower values are better, so reverse the benchmark order
        # poor is the worst (highest), excellent is the best (lowest)
        excellent, good, medium, low, poor = poor, low, medium, good, excellent
    
    if value >= excellent:
        return 100.0, "优秀"
    elif value >= good:
        if excellent != good:
            ratio = (value - good) / (excellent - good)
        else:
            ratio = 1.0
        return 80.0 + ratio * 20.0, "良好"
    elif value >= medium:
        if good != medium:
            ratio = (value - medium) / (good - medium)
        else:
            ratio = 1.0
        return 60.0 + ratio * 20.0, "中等"
    elif value >= low:
        if medium != low:
            ratio = (value - low) / (medium - low)
        else:
            ratio = 1.0
        return 40.0 + ratio * 20.0, "较低"
    elif value >= poor:
        if low != poor:
            ratio = (value - poor) / (low - poor)
        else:
            ratio = 1.0
        return 20.0 + ratio * 20.0, "较差"
    else:
        return 0.0, "较差"


def score_to_grade(score: float) -> str:
    """将分数映射为等级"""
    for threshold, grade in GRADE_MAP:
        if score >= threshold:
            return grade
    return "E 较差"


# ─── Evaluation Functions ──────────────────────────────────────────

def evaluate_indicator(industry: str, size: str, indicator_key: str,
                        value: float, db: SASACDatabase,
                        intl: bool = False) -> dict:
    """
    单指标对标评估
    
    Args:
        industry: 行业名称
        size: 规模分类
        indicator_key: 指标英文key（如"roe"）
        value: 企业实际值
        db: SASAC数据库实例
        intl: 是否国际标准值
    
    Returns:
        对标结果字典
    """
    table = db.get_benchmark(industry, size, intl)
    if table is None:
        return {"error": f"未找到行业标准值: {industry}/{size}"}
    
    if indicator_key not in table['data']:
        return {"error": f"指标 {indicator_key} 在该行业标准值中不可用"}
    
    benchmark = table['data'][indicator_key]
    if not benchmark or len(benchmark) != 5:
        return {"error": f"指标 {indicator_key} 标准值数据不完整"}
    
    meta = METRIC_DEFS.get(indicator_key, {})
    higher_better = meta.get("higher_better", True)
    
    score, level = linear_interpolation(value, benchmark, higher_better)
    
    excellent = benchmark[0]
    gap_to_excellent = ((excellent - value) / abs(excellent) * 100) if excellent != 0 else 0
    
    return {
        "indicator": meta.get("name", indicator_key),
        "indicator_key": indicator_key,
        "value": value,
        "unit": meta.get("unit", ""),
        "benchmark": dict(zip(LEVEL_NAMES, benchmark)),
        "level": level,
        "score": round(score, 2),
        "gap_to_excellent_pct": round(gap_to_excellent, 1),
        "dimension": meta.get("dim", "未知"),
        "higher_better": higher_better,
    }


def full_diagnosis(industry: str, size: str, data: dict, 
                   db: SASACDatabase, intl: bool = False) -> dict:
    """
    全面绩效诊断
    
    Args:
        industry: 行业名称
        size: 规模分类
        data: {指标key: 实际值} 字典（支持英文key和中文name）
        db: SASAC数据库实例
        intl: 是否国际标准值
    
    Returns:
        完整诊断结果
    """
    # Build name-to-key mapping
    name_to_key = {v["name"]: k for k, v in METRIC_DEFS.items()}
    
    # Normalize data keys
    normalized = {}
    for k, v in data.items():
        if k in METRIC_DEFS:
            normalized[k] = v
        elif k in name_to_key:
            normalized[name_to_key[k]] = v
    
    # Evaluate each indicator
    results = {}
    dimension_scores = {}
    dimension_indicators = {}
    
    for key, value in normalized.items():
        result = evaluate_indicator(industry, size, key, value, db, intl)
        if "error" not in result:
            results[key] = result
            dim = result["dimension"]
            dimension_scores.setdefault(dim, []).append(result["score"])
            dimension_indicators.setdefault(dim, []).append(key)
    
    # Calculate dimension average scores
    dim_avg = {}
    for dim, scores in dimension_scores.items():
        dim_avg[dim] = round(sum(scores) / len(scores), 2)
    
    # Calculate composite score (only core dimensions)
    composite = 0
    total_weight = 0
    for dim, weight in DIMENSION_WEIGHTS.items():
        if dim in dim_avg:
            composite += dim_avg[dim] * weight
            total_weight += weight
    
    if total_weight > 0:
        composite = round(composite / total_weight * 100 / 100, 2)  # normalize
        # Actually just use the weighted sum directly since weights sum to 1.0
        composite = round(sum(dim_avg.get(d, 0) * w for d, w in DIMENSION_WEIGHTS.items() 
                              if d in dim_avg), 2)
        # Renormalize if not all dimensions present
        actual_weight = sum(w for d, w in DIMENSION_WEIGHTS.items() if d in dim_avg)
        if actual_weight < 1.0 and actual_weight > 0:
            composite = round(composite / actual_weight, 2)
    
    # Identify strengths and weaknesses
    strengths = [d for d, s in dim_avg.items() if s >= 60]
    weaknesses = [d for d, s in dim_avg.items() if s < 50]
    
    return {
        "industry": industry,
        "size": size,
        "composite_score": composite,
        "grade": score_to_grade(composite),
        "dimension_scores": dim_avg,
        "indicator_results": results,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "evaluated_indicators": len(results),
        "total_indicators": len(normalized),
    }


# ─── Enterprise Size Classification ───────────────────────────────

def classify_size(employees: int, revenue_million: float, 
                  total_assets_million: float) -> str:
    """
    根据国家统计局标准判定企业规模
    
    Args:
        employees: 从业人员数
        revenue_million: 营业收入（百万元）
        total_assets_million: 资产总额（百万元）
    
    Returns:
        "大型企业" / "中型企业" / "小型企业"
    """
    if employees >= 1000 and revenue_million >= 400:
        return "大型企业"
    elif employees >= 300 and revenue_million >= 20:
        return "中型企业"
    else:
        return "小型企业"


# ─── CLI Entry Point ───────────────────────────────────────────────

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='国资委绩效计算引擎')
    parser.add_argument('--industry', '-i', required=True, help='行业名称')
    parser.add_argument('--size', '-s', default='全行业', help='规模分类')
    parser.add_argument('--indicator', '-m', required=True, help='指标key')
    parser.add_argument('--value', '-v', type=float, required=True, help='实际值')
    parser.add_argument('--intl', action='store_true', help='使用国际标准值')
    parser.add_argument('--list-industries', action='store_true', help='列出所有行业')
    parser.add_argument('--list-metrics', action='store_true', help='列出所有指标')
    
    args = parser.parse_args()
    
    db = SASACDatabase()
    
    if args.list_industries:
        print("=== 国内行业 ===")
        for ind in db.get_industries(False):
            print(f"  {ind}")
        print("\n=== 国际行业 ===")
        for ind in db.get_industries(True):
            print(f"  {ind}")
        return
    
    if args.list_metrics:
        for key, meta in METRIC_DEFS.items():
            print(f"  {key:12s} | {meta['name']:20s} | {meta['dim']} | {meta['unit']}")
        return
    
    result = evaluate_indicator(args.industry, args.size, args.indicator, 
                                args.value, db, args.intl)
    
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"📊 对标结果")
        print(f"  指标: {result['indicator']} ({result['indicator_key']})")
        print(f"  实际值: {result['value']} {result['unit']}")
        print(f"  对标等级: {result['level']}")
        print(f"  得分: {result['score']}/100")
        print(f"  标准值: 优秀={result['benchmark']['优秀值']}, "
              f"良好={result['benchmark']['良好值']}, "
              f"中等={result['benchmark']['中等值']}, "
              f"较低={result['benchmark']['较低值']}, "
              f"较差={result['benchmark']['较差值']}")
        print(f"  距优秀值差距: {result['gap_to_excellent_pct']}%")


if __name__ == '__main__':
    main()
