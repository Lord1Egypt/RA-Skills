#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成模块
实现各类质量报告、PDCA报告、决策报告的自动生成
支持Markdown、HTML、JSON等多种格式
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import asdict
from .utils import load_config, ensure_dir, write_text_file, logger
from .pdca_engine import Project, PDCAPhase, ProjectStatus
from .iso9001_validator import ValidationReport, ComplianceLevel
from .decision_checker import DecisionCheckReport, DecisionQuality, DecisionRiskLevel
class ReportGenerator:
    """报告生成器类"""
    def __init__(self):
        self.config = load_config()
        self.report_dir = os.path.join(os.path.dirname(__file__), '../reports')
        self.template_dir = os.path.join(os.path.dirname(__file__), '../templates')
        ensure_dir(self.report_dir)
        logger.info("报告生成器初始化完成")
    # ==================== 项目报告生成 ====================
    def generate_project_report(self, project: Project, format: str = 'markdown') -> str:
        """
        生成项目完整报告
        Args:
            project: 项目对象
            format: 报告格式：markdown/html/json
        Returns:
            报告内容
        """
        if format.lower() == 'json':
            return self._generate_project_json_report(project)
        elif format.lower() == 'html':
            markdown_content = self._generate_project_markdown_report(project)
            return self._markdown_to_html(markdown_content)
        else:  # 默认markdown
            return self._generate_project_markdown_report(project)
    def _generate_project_markdown_report(self, project: Project) -> str:
        """生成Markdown格式的项目报告"""
        # 阶段中文名称
        phase_names = {
            PDCAPhase.PLAN: "策划阶段",
            PDCAPhase.DO: "执行阶段",
            PDCAPhase.CHECK: "检查阶段",
            PDCAPhase.ACT: "处置阶段",
            PDCAPhase.COMPLETED: "已完成"
        }
        # 状态中文名称
        status_names = {
            ProjectStatus.NOT_STARTED: "未开始",
            ProjectStatus.IN_PROGRESS: "进行中",
            ProjectStatus.PENDING_REVIEW: "待审核",
            ProjectStatus.COMPLETED: "已完成",
            ProjectStatus.CANCELLED: "已取消",
            ProjectStatus.ON_HOLD: "已暂停"
        }
        # 风险等级图标
        risk_icons = {
            'low': "🟢 低风险",
            'medium': "🟡 中风险",
            'high': "🟠 高风险",
            'critical': "🔴 极高风险"
        }
        # 进度计算
        phase_progress = {
            PDCAPhase.PLAN: 25,
            PDCAPhase.DO: 50,
            PDCAPhase.CHECK: 75,
            PDCAPhase.ACT: 90,
            PDCAPhase.COMPLETED: 100
        }
        overall_progress = phase_progress.get(project.current_phase, 0)
        if project.current_phase == PDCAPhase.DO:
            execution_progress = project.do_data.get('current_progress', 0)
            overall_progress = 25 + (execution_progress * 0.25)
        report = f"""# 项目质量报告
## 一、项目基本信息
| 项目 | 详情 |
|------|------|
| 项目名称 | {project.name} |
| 项目ID | {project.id} |
| 项目类型 | {project.type} |
| 项目负责人 | {project.owner} |
| 创建时间 | {self._format_time(project.created_at)} |
| 更新时间 | {self._format_time(project.updated_at)} |
| 当前阶段 | {phase_names[project.current_phase]} |
| 当前状态 | {status_names[project.status]} |
| 整体进度 | {round(overall_progress, 1)}% |
| 质量评分 | {project.quality_score}/100 |
| 风险等级 | {risk_icons.get(project.risk_level, project.risk_level)} |
| 标签 | {', '.join(project.tags) if project.tags else '无'} |
## 二、各阶段详情
"""
        # 策划阶段
        if project.plan_data:
            report += """
### 📋 策划阶段
"""
            if 'target' in project.plan_data:
                report += f"- **项目目标**：{project.plan_data['target']}\n"
            if 'quality_standard' in project.plan_data:
                report += f"- **质量标准**：{project.plan_data['quality_standard']}\n"
            if 'resource_plan' in project.plan_data:
                report += f"- **资源配置**：{project.plan_data['resource_plan']}\n"
            if 'approved_by' in project.plan_data:
                report += f"- **审核人**：{project.plan_data['approved_by']}\n"
                report += f"- **审核时间**：{self._format_time(project.plan_data['approved_at'])}\n"
                report += f"- **审核意见**：{project.plan_data.get('approval_comment', '无')}\n"
        # 执行阶段
        if project.do_data:
            report += """
### 🏃 执行阶段
"""
            if 'current_progress' in project.do_data:
                report += f"- **执行进度**：{project.do_data['current_progress']}%\n"
            if 'execution_records' in project.do_data:
                report += f"- **执行记录数**：{len(project.do_data['execution_records'])}条\n"
            if 'has_exceptions' in project.do_data and project.do_data['has_exceptions']:
                report += f"- ⚠️ **异常情况**：发现{len(project.do_data.get('exceptions', []))}个异常\n"
            if 'completion_summary' in project.do_data:
                report += f"- **执行总结**：{project.do_data['completion_summary']}\n"
        # 检查阶段
        if project.check_data:
            report += """
### 🔍 检查阶段
"""
            if 'quality_score' in project.check_data:
                report += f"- **质量得分**：{project.check_data['quality_score']}/100\n"
            if 'problem_count' in project.check_data:
                report += f"- **发现问题**：{project.check_data['problem_count']}个\n"
            if 'problems' in project.check_data:
                report += "#### 问题清单\n"
                for i, problem in enumerate(project.check_data['problems'], 1):
                    report += f"{i}. {problem}\n"
            if 'deviations' in project.check_data:
                report += "#### 偏差分析\n"
                for deviation in project.check_data['deviations']:
                    report += f"- {deviation}\n"
        # 处置阶段
        if project.act_data:
            report += """
### ♻️ 处置阶段
"""
            if 'correction_plan' in project.act_data:
                report += f"- **整改计划**：{project.act_data['correction_plan']}\n"
            if 'improvement_measures' in project.act_data:
                report += "#### 改进措施\n"
                for measure in project.act_data['improvement_measures']:
                    report += f"- {measure}\n"
            if 'lessons_learned' in project.act_data:
                report += f"- **经验教训**：{project.act_data['lessons_learned']}\n"
            if 'best_practices' in project.act_data:
                report += "#### 最佳实践\n"
                for practice in project.act_data['best_practices']:
                    report += f"- {practice}\n"
        # 质量评分可视化
        report += """
## 三、质量评分详情
"""
        score = project.quality_score
        report += f"总得分：{score}/100\n\n"
        # 进度条
        progress_bar = '█' * int(score / 10) + '░' * (10 - int(score / 10))
        report += f"[{progress_bar}] {score}%\n\n"
        # 质量等级评价
        if score >= 90:
            report += "✅ **优秀**：项目质量优异，达到优秀标准\n"
        elif score >= 80:
            report += "✅ **良好**：项目质量良好，符合预期\n"
        elif score >= 70:
            report += "⚠️ **一般**：项目质量基本合格，存在改进空间\n"
        elif score >= 60:
            report += "❌ **较差**：项目质量较差，需要整改\n"
        else:
            report += "❌ **不合格**：项目质量严重不达标\n"
        report += """
## 四、后续建议
"""
        if project.current_phase == PDCAPhase.PLAN:
            report += "- 尽快完成策划阶段审核，进入执行阶段\n"
            report += "- 确认所有资源配置到位\n"
        elif project.current_phase == PDCAPhase.DO:
            report += f"- 加快执行进度，当前完成{project.do_data.get('current_progress', 0)}%\n"
            report += "- 及时记录执行过程中的问题和经验\n"
        elif project.current_phase == PDCAPhase.CHECK:
            report += "- 针对发现的问题制定整改措施\n"
            report += "- 完成检查阶段审核，进入处置阶段\n"
        elif project.current_phase == PDCAPhase.ACT:
            report += "- 落实改进措施，验证整改效果\n"
            report += "- 总结经验教训，沉淀到知识库\n"
        elif project.current_phase == PDCAPhase.COMPLETED:
            report += "- 项目已完成，相关经验已归档到知识库\n"
            report += "- 持续跟踪项目后续效果\n"
        # 页脚
        report += f"""
---
*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*本报告基于PDCA循环和ISO9001质量管理体系生成*
"""
        return report
    def _generate_project_json_report(self, project: Project) -> str:
        """生成JSON格式的项目报告"""
        data = asdict(project)
        # 转换枚举为字符串
        data['current_phase'] = data['current_phase'].value
        data['status'] = data['status'].value
        data['generated_at'] = datetime.now().isoformat()
        return json.dumps(data, indent=2, ensure_ascii=False)
    # ==================== ISO9001验证报告生成 ====================
    def generate_iso9001_report(self, validation_report: ValidationReport, format: str = 'markdown') -> str:
        """
        生成ISO9001验证报告
        Args:
            validation_report: 验证报告对象
            format: 报告格式
        Returns:
            报告内容
        """
        if format.lower() == 'json':
            return json.dumps(asdict(validation_report), indent=2, ensure_ascii=False)
        elif format.lower() == 'html':
            markdown_content = self._generate_iso9001_markdown_report(validation_report)
            return self._markdown_to_html(markdown_content)
        else:
            return self._generate_iso9001_markdown_report(validation_report)
    def _generate_iso9001_markdown_report(self, report: ValidationReport) -> str:
        """生成Markdown格式的ISO9001验证报告"""
        # 合规等级描述
        compliance_desc = {
            ComplianceLevel.FULLY_COMPLIANT: "✅ 完全符合",
            ComplianceLevel.PARTIALLY_COMPLIANT: "⚠️ 部分符合",
            ComplianceLevel.NON_COMPLIANT: "❌ 不符合",
            ComplianceLevel.NOT_APPLICABLE: "ℹ️ 不适用"
        }
        markdown = f"""# ISO9001质量管理体系验证报告
## 一、总体情况
| 指标 | 结果 |
|------|------|
| 总体合规等级 | {compliance_desc[report.overall_compliance]} |
| 总体得分 | {report.overall_score}/100 |
| 评估时间 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
## 二、摘要
{report.summary}
"""
        if report.required_actions:
            markdown += """
## 三、必填行动
"""
            for action in report.required_actions:
                markdown += f"- ⚠️ {action}\n"
        if report.recommendations:
            markdown += """
## 四、改进建议
"""
            for rec in report.recommendations:
                markdown += f"- 💡 {rec}\n"
        markdown += """
## 五、各原则校验详情
| 质量管理原则 | 得分 | 合规等级 | 问题数量 |
|-------------|------|----------|----------|
"""
        from .iso9001_validator import ISO9001Validator
        validator = ISO9001Validator()
        for result in report.check_results:
            principle_name = validator.QUALITY_PRINCIPLES[result.principle]['name']
            level_desc = compliance_desc[result.level]
            markdown += f"| {principle_name} | {result.score} | {level_desc} | {len(result.issues)} |\n"
        markdown += """
## 六、详细检查结果
"""
        for result in report.check_results:
            principle = validator.QUALITY_PRINCIPLES[result.principle]
            markdown += f"""
### {principle['name']}
- **得分**: {result.score}/100
- **合规等级**: {compliance_desc[result.level]}
- **原则描述**: {principle['description']}
"""
            if result.issues:
                markdown += "#### 存在问题\n"
                for issue in result.issues:
                    markdown += f"- ❌ {issue}\n"
            if result.suggestions:
                markdown += "#### 改进建议\n"
                for suggestion in result.suggestions:
                    markdown += f"- 💡 {suggestion}\n"
        markdown += """
---
*本报告基于ISO9001:2015质量管理体系标准生成*
"""
        return markdown
    # ==================== 决策校验报告生成 ====================
    def generate_decision_report(self, decision_report: DecisionCheckReport, format: str = 'markdown') -> str:
        """
        生成决策校验报告
        Args:
            decision_report: 决策校验报告对象
            format: 报告格式
        Returns:
            报告内容
        """
        if format.lower() == 'json':
            data = asdict(decision_report)
            data['quality_level'] = data['quality_level'].value
            data['risk_level'] = data['risk_level'].value
            return json.dumps(data, indent=2, ensure_ascii=False)
        elif format.lower() == 'html':
            markdown_content = self._generate_decision_markdown_report(decision_report)
            return self._markdown_to_html(markdown_content)
        else:
            return self._generate_decision_markdown_report(decision_report)
    def _generate_decision_markdown_report(self, report: DecisionCheckReport) -> str:
        """生成Markdown格式的决策校验报告"""
        # 质量等级描述
        quality_desc = {
            DecisionQuality.EXCELLENT: "✅ 优秀",
            DecisionQuality.GOOD: "✅ 良好",
            DecisionQuality.FAIR: "⚠️ 一般",
            DecisionQuality.POOR: "❌ 较差",
            DecisionQuality.INVALID: "❌ 无效"
        }
        # 风险等级描述
        risk_desc = {
            DecisionRiskLevel.LOW: "🟢 低风险",
            DecisionRiskLevel.MEDIUM: "🟡 中风险",
            DecisionRiskLevel.HIGH: "🟠 高风险",
            DecisionRiskLevel.CRITICAL: "🔴 极高风险"
        }
        passed_icon = "✅" if report.passed else "❌"
        markdown = f"""# 决策质量校验报告
## 一、基本信息
| 项 | 详情 |
|----|------|
| 校验结果 | {passed_icon} {'通过' if report.passed else '未通过'} |
| 决策ID | {report.decision_id} |
| 生成时间 | {report.generated_at} |
| 总体得分 | {report.overall_score}/100 |
| 质量等级 | {quality_desc[report.quality_level]} |
| 风险等级 | {risk_desc[report.risk_level]} |
## 二、决策内容
> {report.decision_content[:500]}{'...' if len(report.decision_content) > 500 else ''}
## 三、摘要
{report.summary}
"""
        if report.warnings:
            markdown += """
## 四、警告
"""
            for warning in report.warnings:
                markdown += f"- ⚠️ {warning}\n"
        if report.required_actions:
            markdown += """
## 五、必填行动
"""
            for action in report.required_actions:
                markdown += f"- 📋 {action}\n"
        if report.recommendations:
            markdown += """
## 六、改进建议
"""
            for rec in report.recommendations:
                markdown += f"- 💡 {rec}\n"
        markdown += """
## 七、各检查项详情
| 检查项 | 得分 | 结果 | 问题数量 | 需证据 |
|--------|------|------|----------|--------|
"""
        for result in report.check_results:
            item_passed = "✅ 通过" if result.passed else "❌ 未通过"
            need_evidence = "是" if result.evidence_required else "否"
            markdown += f"| {result.name} | {result.score} | {item_passed} | {len(result.issues)} | {need_evidence} |\n"
        markdown += """
## 八、详细检查结果
"""
        for result in report.check_results:
            markdown += f"""
### {result.name}
- **得分**: {result.score}/100
- **结果**: {'✅ 通过' if result.passed else '❌ 未通过'}
- **描述**: {result.description}
"""
            if result.issues:
                markdown += "#### 存在问题\n"
                for issue in result.issues:
                    markdown += f"- ❌ {issue}\n"
            if result.suggestions:
                markdown += "#### 改进建议\n"
                for suggestion in result.suggestions:
                    markdown += f"- 💡 {suggestion}\n"
        markdown += """
---
*本报告基于实事求是原则，通过多维度客观校验生成*
"""
        return markdown
    # ==================== 统计报告生成 ====================
    def generate_statistics_report(self, projects: List[Project], period: str = "month", format: str = 'markdown') -> str:
        """
        生成统计报告
        Args:
            projects: 项目列表
            period: 统计周期：week/month/quarter/year
            format: 报告格式
        Returns:
            统计报告内容
        """
        # 计算统计数据
        total_count = len(projects)
        completed_count = sum(1 for p in projects if p.status == ProjectStatus.COMPLETED)
        in_progress_count = sum(1 for p in projects if p.status == ProjectStatus.IN_PROGRESS)
        pending_count = sum(1 for p in projects if p.status == ProjectStatus.PENDING_REVIEW)
        avg_quality_score = sum(p.quality_score for p in projects) / total_count if total_count > 0 else 0
        # 风险分布
        risk_distribution = {
            'low': sum(1 for p in projects if p.risk_level == 'low'),
            'medium': sum(1 for p in projects if p.risk_level == 'medium'),
            'high': sum(1 for p in projects if p.risk_level == 'high'),
            'critical': sum(1 for p in projects if p.risk_level == 'critical')
        }
        # 阶段分布
        phase_distribution = {
            'plan': sum(1 for p in projects if p.current_phase == PDCAPhase.PLAN),
            'do': sum(1 for p in projects if p.current_phase == PDCAPhase.DO),
            'check': sum(1 for p in projects if p.current_phase == PDCAPhase.CHECK),
            'act': sum(1 for p in projects if p.current_phase == PDCAPhase.ACT),
            'completed': sum(1 for p in projects if p.current_phase == PDCAPhase.COMPLETED)
        }
        if format.lower() == 'json':
            stats = {
                'period': period,
                'generated_at': datetime.now().isoformat(),
                'total_count': total_count,
                'completed_count': completed_count,
                'in_progress_count': in_progress_count,
                'pending_count': pending_count,
                'avg_quality_score': round(avg_quality_score, 2),
                'risk_distribution': risk_distribution,
                'phase_distribution': phase_distribution
            }
            return json.dumps(stats, indent=2, ensure_ascii=False)
        # 生成Markdown报告
        period_names = {
            'week': '周',
            'month': '月',
            'quarter': '季度',
            'year': '年'
        }
        markdown = f"""# 质量管理{period_names.get(period, period)}度统计报告
## 一、总体概览
| 指标 | 数值 |
|------|------|
| 统计周期 | {period_names.get(period, period)}度 |
| 项目总数 | {total_count} |
| 已完成项目 | {completed_count} |
| 进行中项目 | {in_progress_count} |
| 待审核项目 | {pending_count} |
| 平均质量得分 | {round(avg_quality_score, 2)}/100 |
## 二、分布统计
### 风险分布
| 风险等级 | 数量 | 占比 |
|----------|------|------|
"""
        for level, count in risk_distribution.items():
            percentage = round(count / total_count * 100, 1) if total_count > 0 else 0
            markdown += f"| {level} | {count} | {percentage}% |\n"
        markdown += """
### 阶段分布
| 阶段 | 数量 | 占比 |
|------|------|------|
"""
        phase_names = {
            'plan': '策划阶段',
            'do': '执行阶段',
            'check': '检查阶段',
            'act': '处置阶段',
            'completed': '已完成'
        }
        for phase, count in phase_distribution.items():
            percentage = round(count / total_count * 100, 1) if total_count > 0 else 0
            markdown += f"| {phase_names[phase]} | {count} | {percentage}% |\n"
        # 质量分析
        markdown += """
## 三、质量分析
"""
        if avg_quality_score >= 90:
            markdown += "✅ 整体质量优秀，平均得分超过90分\n"
        elif avg_quality_score >= 80:
            markdown += "✅ 整体质量良好，平均得分80-90分\n"
        elif avg_quality_score >= 70:
            markdown += "⚠️ 整体质量一般，平均得分70-80分，有提升空间\n"
        elif avg_quality_score >= 60:
            markdown += "❌ 整体质量较差，平均得分60-70分，需要重点改进\n"
        else:
            markdown += "❌ 整体质量不合格，平均得分低于60分，必须立即整改\n"
        # 高风险项目提醒
        high_risk_projects = [p for p in projects if p.risk_level in ['high', 'critical']]
        if high_risk_projects:
            markdown += f"\n⚠️ **高风险项目提醒**：共发现{len(high_risk_projects)}个高风险/极高风险项目，请重点关注：\n"
            for p in high_risk_projects:
                markdown += f"- [{p.name} (ID: {p.id})] 风险等级：{p.risk_level}\n"
        # 改进建议
        markdown += """
## 四、改进建议
"""
        if avg_quality_score < 80:
            markdown += "- 建议加强项目前期策划质量，提高目标明确性和可行性\n"
        if risk_distribution['high'] + risk_distribution['critical'] > total_count * 0.2:
            markdown += "- 建议加强风险识别和评估能力，高风险项目占比过高\n"
        if pending_count > total_count * 0.3:
            markdown += "- 建议加快审核流程，待审核项目占比过高\n"
        markdown += """
---
*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        if format.lower() == 'html':
            return self._markdown_to_html(markdown)
        return markdown
    # ==================== 工具方法 ====================
    def save_report(self, content: str, filename: str, format: str = 'markdown') -> str:
        """
        保存报告到文件
        Args:
            content: 报告内容
            filename: 文件名（不含扩展名）
            format: 报告格式
        Returns:
            保存的文件路径
        """
        # 确定文件扩展名
        extensions = {
            'markdown': '.md',
            'html': '.html',
            'json': '.json'
        }
        ext = extensions.get(format.lower(), '.md')
        file_path = os.path.join(self.report_dir, f"{filename}{ext}")
        write_text_file(content, file_path)
        logger.info(f"报告已保存到: {file_path}")
        return file_path
    def _format_time(self, iso_time: str) -> str:
        """格式化ISO时间为可读格式"""
        try:
            dt = datetime.fromisoformat(iso_time)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return iso_time
    def _markdown_to_html(self, markdown_content: str) -> str:
        """简单的Markdown转HTML（简化实现）"""
        # 标题转换
        html = markdown_content
        # 一级标题
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        # 二级标题
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        # 三级标题
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        # 粗体
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        # 斜体
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        # 列表
        html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
        # 表格
        html = re.sub(r'^\| (.*?) \|$', r'<tr><td>\1</td></tr>', html, flags=re.MULTILINE)
        html = re.sub(r'(<tr>.*?</tr>)', r'<table>\1</table>', html, flags=re.DOTALL)
        # 换行
        html = html.replace('\n', '<br>')
        # 包装HTML模板
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>质量报告</title>
    <style>
        body {{ font-family: "Microsoft Yahei", Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
        h3 {{ color: #2980b9; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        table, th, td {{ border: 1px solid #ddd; }}
        th, td {{ padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        ul {{ margin: 10px 0; padding-left: 20px; }}
        li {{ margin: 5px 0; }}
        strong {{ color: #e74c3c; }}
        .footer {{ margin-top: 30px; padding-top: 10px; border-top: 1px solid #eee; color: #7f8c8d; font-size: 0.9em; }}
    </style>
</head>
<body>
    {html}
    <div class="footer">
        报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>
"""
        return full_html
# 导入re模块
import re
