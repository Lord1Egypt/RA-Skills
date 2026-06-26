"""
报告生成模块

负责生成技能分析报告、健康度报告等
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from database.models import Database, HealthScore
from skill_evolver.analyzer import SkillAnalyzer, SkillAnalysisResult


class SkillReporter:
    """技能报告生成器"""
    
    def __init__(self, db: Optional[Database] = None, skills_dir: Optional[str] = None):
        self.db = db or Database()
        self.analyzer = SkillAnalyzer(skills_dir)
    
    def generate_health_report(self, skill_name: str) -> Dict[str, Any]:
        """
        生成技能健康度报告
        
        Args:
            skill_name: 技能名称
        
        Returns:
            健康度报告数据
        """
        # 获取使用统计
        usage_stats = self.db.get_usage_stats(skill_name, days=30)
        
        # 获取反馈统计
        feedback_stats = self.db.get_feedback_stats(skill_name)
        
        # 获取代码分析结果
        analysis = self.analyzer.analyze_skill(skill_name)
        
        # 计算健康度评分
        health_score = self._calculate_health_score(
            usage_stats, feedback_stats, analysis
        )
        
        # 生成报告
        report = {
            "skill_name": skill_name,
            "generated_at": datetime.now().isoformat(),
            "period_days": 30,
            "overall_score": health_score["overall"],
            "scores": {
                "reliability": health_score["reliability"],
                "performance": health_score["performance"],
                "code_quality": health_score["code_quality"],
                "user_satisfaction": health_score["user_satisfaction"]
            },
            "usage": {
                "total_calls": usage_stats["total"],
                "success_rate": self._calc_success_rate(usage_stats),
                "avg_duration_ms": usage_stats["avg_duration_ms"],
                "failed_calls": usage_stats["failed"]
            },
            "feedback": {
                "total_reviews": feedback_stats["total"],
                "avg_rating": feedback_stats["avg_rating"],
                "rating_distribution": feedback_stats["distribution"]
            },
            "code_analysis": {
                "score": analysis.score,
                "total_issues": len(analysis.issues),
                "critical_issues": sum(1 for i in analysis.issues if i.severity == "critical"),
                "warnings": sum(1 for i in analysis.issues if i.severity == "warning")
            },
            "recommendations": self._generate_recommendations(
                usage_stats, feedback_stats, analysis
            ),
            "status": self._determine_status(health_score["overall"])
        }
        
        # 保存健康度评分到数据库
        self._save_health_score(skill_name, report)
        
        return report
    
    def generate_full_report(self, skill_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        生成完整报告
        
        Args:
            skill_names: 指定技能列表，None 表示所有技能
        
        Returns:
            完整报告数据
        """
        if skill_names is None:
            skill_names = self.db.get_all_skills()
            # 也包含代码分析中发现的技能
            analysis_results = self.analyzer.analyze_all_skills()
            for result in analysis_results:
                if result.exists and result.skill_name not in skill_names:
                    skill_names.append(result.skill_name)
        
        reports = []
        for skill_name in skill_names:
            try:
                report = self.generate_health_report(skill_name)
                reports.append(report)
            except Exception as e:
                reports.append({
                    "skill_name": skill_name,
                    "error": str(e),
                    "status": "error"
                })
        
        # 计算总体统计
        valid_reports = [r for r in reports if "error" not in r]
        
        summary = {
            "total_skills": len(reports),
            "healthy_skills": sum(1 for r in valid_reports if r["status"] == "healthy"),
            "warning_skills": sum(1 for r in valid_reports if r["status"] == "warning"),
            "critical_skills": sum(1 for r in valid_reports if r["status"] == "critical"),
            "average_score": round(
                sum(r["overall_score"] for r in valid_reports) / len(valid_reports), 2
            ) if valid_reports else 0,
            "total_usage": sum(r["usage"]["total_calls"] for r in valid_reports),
            "total_feedback": sum(r["feedback"]["total_reviews"] for r in valid_reports)
        }
        
        return {
            "generated_at": datetime.now().isoformat(),
            "summary": summary,
            "skills": reports
        }
    
    def export_report(self, report: Dict[str, Any], output_path: str, format: str = "json"):
        """
        导出报告到文件
        
        Args:
            report: 报告数据
            output_path: 输出路径
            format: 格式 (json, markdown, html)
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            markdown = self._report_to_markdown(report)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
        
        elif format == "html":
            html = self._report_to_html(report)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
        
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def _calculate_health_score(
        self,
        usage_stats: Dict[str, Any],
        feedback_stats: Dict[str, Any],
        analysis: SkillAnalysisResult
    ) -> Dict[str, int]:
        """计算各项健康度评分"""
        # 可靠性评分 (基于成功率)
        total = usage_stats["total"]
        success = usage_stats["success"]
        success_rate = (success / total * 100) if total > 0 else 100
        reliability = min(100, int(success_rate))
        
        # 性能评分 (基于平均耗时，假设 <100ms 为满分)
        avg_duration = usage_stats["avg_duration_ms"]
        if avg_duration == 0:
            performance = 100
        else:
            performance = min(100, max(0, int(100 - avg_duration / 10)))
        
        # 代码质量评分
        code_quality = analysis.score
        
        # 用户满意度评分
        avg_rating = feedback_stats["avg_rating"]
        user_satisfaction = min(100, int(avg_rating * 20)) if avg_rating > 0 else 50
        
        # 综合评分 (加权平均)
        overall = int(
            reliability * 0.3 +
            performance * 0.2 +
            code_quality * 0.3 +
            user_satisfaction * 0.2
        )
        
        return {
            "reliability": reliability,
            "performance": performance,
            "code_quality": code_quality,
            "user_satisfaction": user_satisfaction,
            "overall": overall
        }
    
    def _calc_success_rate(self, usage_stats: Dict[str, Any]) -> float:
        """计算成功率"""
        total = usage_stats["total"]
        success = usage_stats["success"]
        return round(success / total * 100, 2) if total > 0 else 0.0
    
    def _generate_recommendations(
        self,
        usage_stats: Dict[str, Any],
        feedback_stats: Dict[str, Any],
        analysis: SkillAnalysisResult
    ) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于使用情况的建议
        success_rate = self._calc_success_rate(usage_stats)
        if success_rate < 80:
            recommendations.append(f"成功率较低 ({success_rate}%)，建议检查错误日志并修复问题")
        
        if usage_stats["avg_duration_ms"] > 5000:
            recommendations.append(f"平均响应时间较长 ({usage_stats['avg_duration_ms']}ms)，建议优化性能")
        
        # 基于反馈的建议
        if feedback_stats["avg_rating"] > 0 and feedback_stats["avg_rating"] < 3:
            recommendations.append(f"用户评分较低 ({feedback_stats['avg_rating']}/5)，建议收集用户反馈并改进")
        
        # 基于代码分析的建议
        critical_issues = sum(1 for i in analysis.issues if i.severity == "critical")
        if critical_issues > 0:
            recommendations.append(f"存在 {critical_issues} 个严重问题需要修复")
        
        # 添加分析器生成的建议
        recommendations.extend(analysis.suggestions)
        
        return recommendations
    
    def _determine_status(self, overall_score: int) -> str:
        """根据评分确定状态"""
        if overall_score >= 80:
            return "healthy"
        elif overall_score >= 60:
            return "warning"
        else:
            return "critical"
    
    def _save_health_score(self, skill_name: str, report: Dict[str, Any]):
        """保存健康度评分到数据库"""
        score = HealthScore(
            skill_name=skill_name,
            success_rate=report["usage"]["success_rate"],
            avg_duration_ms=report["usage"]["avg_duration_ms"],
            usage_count=report["usage"]["total_calls"],
            score=report["overall_score"],
            issues=json.dumps(report["recommendations"])
        )
        self.db.update_health_score(score)
    
    def _report_to_markdown(self, report: Dict[str, Any]) -> str:
        """将报告转换为 Markdown 格式"""
        if "error" in report:
            return f"# 错误\n\n分析 {report['skill_name']} 时出错: {report['error']}"
        
        md = f"""# {report['skill_name']} 健康度报告

生成时间: {report['generated_at']}

## 总体评分: {report['overall_score']}/100

状态: {'🟢 健康' if report['status'] == 'healthy' else '🟡 警告' if report['status'] == 'warning' else '🔴 严重'}

## 详细评分

| 维度 | 评分 |
|------|------|
| 可靠性 | {report['scores']['reliability']}/100 |
| 性能 | {report['scores']['performance']}/100 |
| 代码质量 | {report['scores']['code_quality']}/100 |
| 用户满意度 | {report['scores']['user_satisfaction']}/100 |

## 使用情况 (过去30天)

- 总调用次数: {report['usage']['total_calls']}
- 成功率: {report['usage']['success_rate']}%
- 失败次数: {report['usage']['failed_calls']}
- 平均响应时间: {report['usage']['avg_duration_ms']}ms

## 用户反馈

- 总评价数: {report['feedback']['total_reviews']}
- 平均评分: {report['feedback']['avg_rating']}/5

## 代码分析

- 代码质量评分: {report['code_analysis']['score']}/100
- 问题总数: {report['code_analysis']['total_issues']}
- 严重问题: {report['code_analysis']['critical_issues']}
- 警告: {report['code_analysis']['warnings']}

## 改进建议

"""
        for i, rec in enumerate(report['recommendations'], 1):
            md += f"{i}. {rec}\n"
        
        return md
    
    def _report_to_html(self, report: Dict[str, Any]) -> str:
        """将报告转换为 HTML 格式"""
        if "error" in report:
            return f"<h1>错误</h1><p>分析 {report['skill_name']} 时出错: {report['error']}</p>"
        
        status_color = {
            "healthy": "#28a745",
            "warning": "#ffc107",
            "critical": "#dc3545"
        }
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{report['skill_name']} 健康度报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .score {{ font-size: 48px; font-weight: bold; color: {status_color.get(report['status'], '#666')}; }}
        .status {{ display: inline-block; padding: 5px 15px; border-radius: 20px; color: white; background: {status_color.get(report['status'], '#666')}; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f5f5f5; }}
        .section {{ margin: 30px 0; }}
    </style>
</head>
<body>
    <h1>{report['skill_name']} 健康度报告</h1>
    <p>生成时间: {report['generated_at']}</p>
    
    <div class="section">
        <div class="score">{report['overall_score']}/100</div>
        <span class="status">{report['status'].upper()}</span>
    </div>
    
    <div class="section">
        <h2>详细评分</h2>
        <table>
            <tr><th>维度</th><th>评分</th></tr>
            <tr><td>可靠性</td><td>{report['scores']['reliability']}/100</td></tr>
            <tr><td>性能</td><td>{report['scores']['performance']}/100</td></tr>
            <tr><td>代码质量</td><td>{report['scores']['code_quality']}/100</td></tr>
            <tr><td>用户满意度</td><td>{report['scores']['user_satisfaction']}/100</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>使用情况 (过去30天)</h2>
        <table>
            <tr><th>指标</th><th>数值</th></tr>
            <tr><td>总调用次数</td><td>{report['usage']['total_calls']}</td></tr>
            <tr><td>成功率</td><td>{report['usage']['success_rate']}%</td></tr>
            <tr><td>失败次数</td><td>{report['usage']['failed_calls']}</td></tr>
            <tr><td>平均响应时间</td><td>{report['usage']['avg_duration_ms']}ms</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>改进建议</h2>
        <ol>
"""
        for rec in report['recommendations']:
            html += f"            <li>{rec}</li>\n"
        
        html += """        </ol>
    </div>
</body>
</html>"""
        
        return html
