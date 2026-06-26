#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truth (求真) v1.3 - 格式化输出模块
功能：JSON结构化输出、Markdown可读输出
"""

import json
from typing import Dict, List, Union, Optional
from checker import CheckResult
from batch import BatchSummary, BatchProcessor


class OutputFormatter:
    """格式化输出"""
    
    def __init__(self):
        self.disclaimer = "⚠️ 免责声明：本结果仅供参考，不构成任何专业意见，不保证完全准确，最终真实性由用户自行判断"
    
    def format_result(self, result: CheckResult, output_format: str) -> Union[Dict, str]:
        """格式化单篇结果"""
        data = result.to_dict()
        data["disclaimer"] = self.disclaimer
        
        if output_format == "json":
            return json.dumps(data, ensure_ascii=False, indent=2)
        elif output_format == "markdown":
            return self._format_markdown(result)
        else:  # both
            return data
    
    def format_batch_result(self, results: List[CheckResult], output_format: str) -> Union[Dict, str]:
        """格式化批量结果"""
        summary = BatchSummary(results)
        data = {
            "results": [r.to_dict() for r in results],
            "summary": summary.to_dict(),
            "disclaimer": self.disclaimer
        }
        
        if output_format == "json":
            return json.dumps(data, ensure_ascii=False, indent=2)
        elif output_format == "markdown":
            return self._format_batch_markdown(results, summary)
        else:  # both
            return data
    
    def format_error(self, reason: str, output_format: str) -> Union[Dict, str]:
        """格式化错误"""
        data = {
            "error": reason,
            "disclaimer": self.disclaimer
        }
        
        if output_format == "json":
            return json.dumps(data, ensure_ascii=False)
        elif output_format == "markdown":
            return f"## 核查失败\n\n错误原因: {reason}\n\n{self.disclaimer}"
        else:
            return data
    
    def _format_markdown(self, result: CheckResult) -> str:
        """生成Markdown可读格式"""
        md = f"# 求真事实核查结果\n\n"
        md += f"## 总体信息\n"
        md += f"- 文本长度: {result.text_length} 字\n"
        md += f"- 可信度评分: **{result.credibility_score}/10**\n"
        md += f"- 结论: {result.conclusion}\n\n"
        
        md += f"## 置信度解释\n"
        exp = result.confidence_explanation
        md += exp.overall_explanation + "\n\n"
        for dim, score in exp.dimension_scores.items():
            md += f"- {dim}: {score:.1f}/10\n"
        md += "\n"
        
        if result.problematic_sentences:
            md += f"## 可能存在问题的句子\n"
            for i, item in enumerate(result.problematic_sentences, 1):
                md += f"### {i}. 位置 {item['position'] + 1}\n"
                md += f"- 句子: {item['sentence']}\n"
                md += f"- 原因: {item['reason']}\n"
                md += f"- 可信度: {item['score']:.1f}/10\n\n"
        
        if result.suggestions:
            md += f"## 改进建议\n"
            for suggestion in result.suggestions:
                md += f"- {suggestion}\n"
            md += "\n"
        
        md += f"\n{self.disclaimer}\n"
        return md
    
    def _format_batch_markdown(self, results: List[CheckResult], summary: BatchSummary) -> str:
        """生成批量结果Markdown"""
        md = f"# 求真批量事实核查结果\n\n"
        md += f"## 汇总统计\n"
        md += f"- 总文本数: {summary.total_count}\n"
        md += f"- 平均可信度评分: **{summary.average_score}/10**\n"
        md += f"- 存在问题文本数: {summary.problem_count}\n"
        md += f"- 问题占比: {summary.problem_ratio}%\n\n"

        md += "## 各文本结果\n"
        for i, result in enumerate(results, 1):
            md += f"### {i}. 评分: {result.credibility_score}/10 - {result.conclusion}\n"
            if result.problematic_sentences:
                md += f"- 问题句子数: {len(result.problematic_sentences)}\n"
            md += "\n"

        md += f"\n{self.disclaimer}\n"
        return md
