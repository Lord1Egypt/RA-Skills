#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisScratchpad - 分析过程记录与验证模块
借鉴dexter项目的自验证设计，为A股/港股分析提供质量保障

核心功能：
1. 记录每个分析步骤的输入/输出/耗时/状态
2. 数据质量验证（完整性、一致性、时效性）
3. 查询去重（防止重复API调用）
4. 分析过程可追溯（JSONL日志）
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


class AnalysisScratchpad:
    """分析过程记录器"""
    
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent.parent.parent / "memory" / "analysis_logs"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 分析步骤记录
        self.steps: List[Dict] = []
        # 查询历史（去重用）
        self.queries: List[str] = []
        # 警告信息
        self.warnings: List[str] = []
        # 数据质量评估
        self.quality_scores: Dict[str, float] = {}
        # 分析开始时间
        self.start_time = time.time()
    
    def record_step(self, category: str, stock_name: str, description: str,
                    success: bool, data: Any = None, error: str = None,
                    duration_ms: Optional[int] = None) -> Dict:
        """记录一个分析步骤
        
        Args:
            category: 步骤类别 (technical/financial/news/recommendation)
            stock_name: 股票名称
            description: 步骤描述
            success: 是否成功
            data: 返回数据（可选，用于验证）
            error: 错误信息（可选）
            duration_ms: 耗时毫秒（可选）
        
        Returns:
            步骤记录字典
        """
        step = {
            'timestamp': datetime.now().isoformat(),
            'category': category,
            'stock': stock_name,
            'description': description,
            'success': success,
            'data_keys': list(data.keys()) if isinstance(data, dict) else None,
            'error': error,
            'duration_ms': duration_ms,
        }
        self.steps.append(step)
        return step
    
    def check_query_dup(self, query: str, threshold: float = 0.7) -> Tuple[bool, Optional[str]]:
        """检查查询是否重复（Jaccard相似度）
        
        Args:
            query: 待检查的查询
            threshold: 相似度阈值（超过则认为重复）
        
        Returns:
            (is_dup, similar_query): 是否重复，相似的历史查询
        """
        query_set = set(query)
        for prev in self.queries:
            prev_set = set(prev)
            if not prev_set or not query_set:
                continue
            intersection = query_set & prev_set
            union = query_set | prev_set
            similarity = len(intersection) / len(union)
            if similarity > threshold:
                return True, prev
        
        self.queries.append(query)
        return False, None
    
    def validate_data_quality(self, category: str, stock_name: str, data: Dict) -> Dict:
        """验证数据质量
        
        Args:
            category: 数据类别 (technical/financial/news)
            stock_name: 股票名称
            data: 待验证的数据
        
        Returns:
            质量评估结果 {score, issues, passed}
        """
        issues = []
        score = 1.0
        
        # 通用检查
        if not data:
            issues.append("数据为空")
            return {'score': 0.0, 'issues': issues, 'passed': False}
        
        if isinstance(data, dict):
            # 检查是否包含错误
            if 'error' in data:
                issues.append(f"API返回错误: {data['error']}")
                score -= 0.5
            
            # 检查是否被跳过
            if data.get('skipped'):
                issues.append("数据源被跳过")
                score -= 0.3
            
            # 检查关键字段缺失
            empty_fields = [k for k, v in data.items() if v is None or v == '' or v == []]
            if empty_fields:
                issues.append(f"空字段: {empty_fields[:5]}")
                score -= 0.1 * min(len(empty_fields), 5)
        
        # 分类检查
        if category == 'technical':
            score, tech_issues = self._validate_technical(data, score)
            issues.extend(tech_issues)
        
        elif category == 'financial':
            score, fin_issues = self._validate_financial(data, score)
            issues.extend(fin_issues)
        
        elif category == 'news':
            score, news_issues = self._validate_news(data, score)
            issues.extend(news_issues)
        
        score = max(0.0, min(1.0, score))
        key = f"{category}_{stock_name}"
        self.quality_scores[key] = score
        
        if score < 0.5:
            self.warnings.append(f"⚠️ {key} 数据质量低: {score:.1%} - {issues}")
        
        return {
            'score': score,
            'issues': issues,
            'passed': score >= 0.5
        }
    
    def _validate_technical(self, data: Dict, score: float) -> Tuple[float, List[str]]:
        """验证技术分析数据"""
        issues = []
        
        required = ['price', 'trend']
        for field in required:
            if not data.get(field):
                issues.append(f"缺少关键指标: {field}")
                score -= 0.2
        
        # 检查价格合理性
        price = data.get('price')
        if price and (price <= 0 or price > 100000):
            issues.append(f"价格异常: {price}")
            score -= 0.3
        
        # 检查指标完整性
        indicators = ['macd', 'rsi', 'kdj', 'boll']
        missing = [ind for ind in indicators if not data.get(ind)]
        if missing:
            issues.append(f"缺少技术指标: {missing}")
            score -= 0.1 * len(missing)
        
        return score, issues
    
    def _validate_financial(self, data: Dict, score: float) -> Tuple[float, List[str]]:
        """验证财务数据"""
        issues = []
        
        if not data.get('skipped') and 'error' not in data:
            # 有数据但检查内容
            if len(data) <= 1:  # 只有error
                issues.append("财务数据内容过少")
                score -= 0.2
        
        return score, issues
    
    def _validate_news(self, data: Dict, score: float) -> Tuple[float, List[str]]:
        """验证资讯数据"""
        issues = []
        
        if not data.get('skipped') and 'error' not in data:
            count = len(data) if isinstance(data, dict) else 0
            if count == 0:
                issues.append("未获取到资讯")
                score -= 0.2
            elif count < 3:
                issues.append(f"资讯数量较少: {count}条")
                score -= 0.1
        
        return score, issues
    
    def get_analysis_summary(self) -> Dict:
        """获取分析摘要"""
        total_steps = len(self.steps)
        success_steps = sum(1 for s in self.steps if s['success'])
        failed_steps = total_steps - success_steps
        
        avg_quality = sum(self.quality_scores.values()) / len(self.quality_scores) if self.quality_scores else 0
        
        # 按类别统计
        category_stats = {}
        for step in self.steps:
            cat = step['category']
            if cat not in category_stats:
                category_stats[cat] = {'total': 0, 'success': 0}
            category_stats[cat]['total'] += 1
            if step['success']:
                category_stats[cat]['success'] += 1
        
        return {
            'total_steps': total_steps,
            'success_rate': success_steps / total_steps if total_steps > 0 else 0,
            'failed_steps': failed_steps,
            'avg_quality': avg_quality,
            'quality_scores': dict(self.quality_scores),
            'category_stats': category_stats,
            'warnings': self.warnings,
            'duration_sec': round(time.time() - self.start_time, 1)
        }
    
    def get_report_footer(self) -> str:
        """生成报告页脚（数据质量说明）"""
        summary = self.get_analysis_summary()
        
        lines = [
            "",
            "---",
            f"**📋 数据质量报告**",
            f"- 步骤总数: {summary['total_steps']}",
            f"- 成功率: {summary['success_rate']:.0%}",
            f"- 平均数据质量: {summary['avg_quality']:.0%}",
            f"- 分析耗时: {summary['duration_sec']}秒",
        ]
        
        # 各类别质量
        for key, score in summary['quality_scores'].items():
            status = "✅" if score >= 0.8 else ("⚠️" if score >= 0.5 else "❌")
            lines.append(f"- {status} {key}: {score:.0%}")
        
        # 警告
        if summary['warnings']:
            lines.append("")
            lines.append("**⚠️ 注意事项:**")
            for w in summary['warnings'][:5]:
                lines.append(f"  - {w}")
        
        return "\n".join(lines)
    
    def save_log(self, filename: Optional[str] = None):
        """保存分析日志为JSONL"""
        if not filename:
            filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            for step in self.steps:
                f.write(json.dumps(step, ensure_ascii=False) + '\n')
        
        # 附加摘要
        summary = self.get_analysis_summary()
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'_summary': summary}, ensure_ascii=False) + '\n')
        
        return str(filepath)
    
    def clear(self):
        """清空记录"""
        self.steps.clear()
        self.queries.clear()
        self.warnings.clear()
        self.quality_scores.clear()
        self.start_time = time.time()
