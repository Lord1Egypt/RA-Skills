#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISO9001质量体系校验模块
实现ISO9001:2015质量管理体系要求的校验、合规性检查
"""
import os
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from .utils import load_config, logger, load_json_file
class ComplianceLevel(Enum):
    """合规性等级"""
    FULLY_COMPLIANT = "fully_compliant"  # 完全符合
    PARTIALLY_COMPLIANT = "partially_compliant"  # 部分符合
    NON_COMPLIANT = "non_compliant"  # 不符合
    NOT_APPLICABLE = "not_applicable"  # 不适用
@dataclass
class CheckResult:
    """检查结果数据结构"""
    principle: str
    requirement: str
    level: ComplianceLevel
    score: int  # 0-100
    issues: List[str]
    suggestions: List[str]
    evidence_required: bool
@dataclass
class ValidationReport:
    """验证报告数据结构"""
    overall_compliance: ComplianceLevel
    overall_score: float
    check_results: List[CheckResult]
    summary: str
    recommendations: List[str]
    required_actions: List[str]
class ISO9001Validator:
    """ISO9001质量体系校验器类"""
    # ISO9001:2015 七项质量管理原则
    QUALITY_PRINCIPLES = {
        "customer_focus": {
            "name": "以顾客为关注焦点",
            "description": "组织依存于顾客。因此，组织应当理解顾客当前和未来的需求，满足顾客要求并争取超越顾客期望。",
            "requirements": [
                "识别顾客需求和期望",
                "将顾客需求转化为质量目标",
                "测量顾客满意度并持续改进",
                "建立顾客沟通机制",
                "保护顾客信息和隐私"
            ]
        },
        "leadership": {
            "name": "领导作用",
            "description": "领导者确立组织统一的宗旨及方向。他们应当创造并保持使员工能充分参与实现组织目标的内部环境。",
            "requirements": [
                "明确质量方针和目标",
                "建立质量责任制",
                "提供必要的资源支持",
                "营造质量文化氛围",
                "定期评审质量管理体系有效性"
            ]
        },
        "engagement_of_people": {
            "name": "全员参与",
            "description": "各级人员是组织之本，只有他们的充分参与，才能使他们的才干为组织带来收益。",
            "requirements": [
                "明确各岗位职责和权限",
                "提供必要的培训和能力培养",
                "鼓励员工参与质量改进",
                "建立员工激励机制",
                "收集员工反馈和建议"
            ]
        },
        "process_approach": {
            "name": "过程方法",
            "description": "将活动和相关的资源作为过程进行管理，可以更高效地得到期望的结果。",
            "requirements": [
                "识别质量管理体系所需的过程",
                "确定过程的输入输出和相互作用",
                "制定过程控制准则和方法",
                "测量过程绩效和有效性",
                "识别过程风险并制定应对措施"
            ]
        },
        "improvement": {
            "name": "改进",
            "description": "持续改进是组织的一个永恒目标。",
            "requirements": [
                "建立持续改进机制",
                "定期评审质量目标达成情况",
                "识别改进机会并实施改进措施",
                "验证改进措施的有效性",
                "固化改进成果并推广应用"
            ]
        },
        "evidence_based_decision_making": {
            "name": "循证决策",
            "description": "有效决策是建立在数据和信息分析的基础上。",
            "requirements": [
                "收集相关数据和信息",
                "确保数据和信息的真实可靠",
                "基于数据分析做出决策",
                "评估决策的风险和影响",
                "记录决策依据和过程"
            ]
        },
        "relationship_management": {
            "name": "关系管理",
            "description": "组织与供方是相互依存的，互利的关系可增强双方创造价值的能力。",
            "requirements": [
                "识别关键供方和合作伙伴",
                "建立互利共赢的合作关系",
                "定期评估供方绩效",
                "与供方共享信息和资源",
                "共同开展改进活动"
            ]
        }
    }
    def __init__(self):
        self.config = load_config()
        self.enabled_principles = self.config['iso9001']['principles']
        self.requirements = self.config['iso9001']['requirements']
        logger.info("ISO9001校验器初始化完成")
    def validate_project(self, project_data: Dict[str, Any]) -> ValidationReport:
        """
        校验项目是否符合ISO9001质量体系要求
        Args:
            project_data: 项目完整数据，包含plan、do、check、act各阶段数据
        Returns:
            验证报告
        """
        if not self.config['iso9001']['enabled']:
            return ValidationReport(
                overall_compliance=ComplianceLevel.NOT_APPLICABLE,
                overall_score=0.0,
                check_results=[],
                summary="ISO9001校验未启用",
                recommendations=[],
                required_actions=[]
            )
        check_results = []
        total_score = 0.0
        principle_count = 0
        # 校验每个启用的质量原则
        for principle_key, enabled in self.enabled_principles.items():
            if not enabled:
                continue
            principle = self.QUALITY_PRINCIPLES[principle_key]
            principle_result = self._validate_principle(principle_key, principle, project_data)
            check_results.append(principle_result)
            total_score += principle_result.score
            principle_count += 1
        # 计算总体得分
        if principle_count > 0:
            overall_score = round(total_score / principle_count, 2)
        else:
            overall_score = 0.0
        # 确定总体合规等级
        if overall_score >= 90:
            overall_compliance = ComplianceLevel.FULLY_COMPLIANT
        elif overall_score >= 70:
            overall_compliance = ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            overall_compliance = ComplianceLevel.NON_COMPLIANT
        # 生成摘要和建议
        summary, recommendations, required_actions = self._generate_summary(check_results, overall_score)
        report = ValidationReport(
            overall_compliance=overall_compliance,
            overall_score=overall_score,
            check_results=check_results,
            summary=summary,
            recommendations=recommendations,
            required_actions=required_actions
        )
        logger.info(f"ISO9001校验完成，总体得分: {overall_score}, 合规等级: {overall_compliance.value}")
        return report
    def _validate_principle(self, principle_key: str, principle: Dict[str, Any], project_data: Dict[str, Any]) -> CheckResult:
        """
        校验单个质量原则
        Args:
            principle_key: 原则标识
            principle: 原则详细信息
            project_data: 项目数据
        Returns:
            检查结果
        """
        requirements = principle['requirements']
        total_requirements = len(requirements)
        met_requirements = 0
        issues = []
        suggestions = []
        evidence_required = False
        for requirement in requirements:
            met, issue, suggestion, need_evidence = self._check_requirement(principle_key, requirement, project_data)
            if met:
                met_requirements += 1
            else:
                issues.append(issue)
                suggestions.append(suggestion)
                if need_evidence:
                    evidence_required = True
        # 计算得分
        if total_requirements == 0:
            score = 100
        else:
            score = round((met_requirements / total_requirements) * 100)
        # 确定合规等级
        if score == 100:
            level = ComplianceLevel.FULLY_COMPLIANT
        elif score >= 70:
            level = ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            level = ComplianceLevel.NON_COMPLIANT
        return CheckResult(
            principle=principle_key,
            requirement=principle['name'],
            level=level,
            score=score,
            issues=issues,
            suggestions=suggestions,
            evidence_required=evidence_required
        )
    def _check_requirement(self, principle_key: str, requirement: str, project_data: Dict[str, Any]) -> Tuple[bool, str, str, bool]:
        """
        检查单个要求是否满足
        Args:
            principle_key: 原则标识
            requirement: 要求描述
            project_data: 项目数据
        Returns:
            (是否满足, 问题描述, 改进建议, 是否需要证据)
        """
        plan_data = project_data.get('plan_data', {})
        do_data = project_data.get('do_data', {})
        check_data = project_data.get('check_data', {})
        act_data = project_data.get('act_data', {})
        # ==================== 以顾客为关注焦点 ====================
        if principle_key == 'customer_focus':
            if requirement == "识别顾客需求和期望":
                if 'customer_requirements' in plan_data and plan_data['customer_requirements']:
                    return True, "", "", False
                else:
                    return False, "未识别和记录顾客需求和期望", "建议在策划阶段明确顾客需求、期望和验收标准", True
            elif requirement == "将顾客需求转化为质量目标":
                target = plan_data.get('target', '')
                if 'customer' in target.lower() or '用户' in target or '客户' in target:
                    return True, "", "", False
                else:
                    return False, "质量目标未体现顾客需求", "建议在质量目标中明确顾客需求的满足程度", True
            elif requirement == "测量顾客满意度并持续改进":
                if 'customer_satisfaction' in check_data and check_data['customer_satisfaction'] is not None:
                    return True, "", "", False
                else:
                    return False, "未测量和记录顾客满意度", "建议在检查阶段收集顾客反馈，测量满意度", True
            elif requirement == "建立顾客沟通机制":
                if 'communication_channels' in plan_data and plan_data['communication_channels']:
                    return True, "", "", False
                else:
                    return False, "未明确顾客沟通渠道和机制", "建议明确与顾客的沟通方式、频率和责任人", False
        # ==================== 领导作用 ====================
        elif principle_key == 'leadership':
            if requirement == "明确质量方针和目标":
                if 'quality_policy' in plan_data and 'quality_objectives' in plan_data:
                    return True, "", "", False
                else:
                    return False, "未明确质量方针和质量目标", "建议在策划阶段制定明确的质量方针和可衡量的质量目标", True
            elif requirement == "建立质量责任制":
                if 'responsibilities' in plan_data and plan_data['responsibilities']:
                    return True, "", "", False
                else:
                    return False, "未明确各角色的质量责任", "建议明确各环节责任人的质量职责和权限", True
            elif requirement == "提供必要的资源支持":
                if 'resource_plan' in plan_data and plan_data['resource_plan']:
                    return True, "", "", False
                else:
                    return False, "未制定资源计划", "建议在策划阶段明确所需的人力、财力、物力等资源配置", True
        # ==================== 过程方法 ====================
        elif principle_key == 'process_approach':
            if requirement == "识别质量管理体系所需的过程":
                if 'processes' in plan_data and plan_data['processes']:
                    return True, "", "", False
                else:
                    return False, "未识别项目所需的关键过程", "建议识别并明确项目的关键过程及其相互关系", True
            elif requirement == "确定过程的输入输出和相互作用":
                if 'process_inputs' in plan_data and 'process_outputs' in plan_data:
                    return True, "", "", False
                else:
                    return False, "未明确过程的输入、输出和接口关系", "建议明确每个过程的输入要求、输出标准和上下游接口", True
            elif requirement == "制定过程控制准则和方法":
                if 'process_controls' in plan_data and plan_data['process_controls']:
                    return True, "", "", False
                else:
                    return False, "未制定过程控制准则和方法", "建议为每个关键过程制定控制要求、检查方法和验收标准", True
        # ==================== 改进 ====================
        elif principle_key == 'improvement':
            if requirement == "建立持续改进机制":
                if 'improvement_mechanism' in plan_data or 'improvement_measures' in act_data:
                    return True, "", "", False
                else:
                    return False, "未建立持续改进机制", "建议明确持续改进的方法、流程和责任人", True
            elif requirement == "识别改进机会并实施改进措施":
                if 'improvement_measures' in act_data and act_data['improvement_measures']:
                    return True, "", "", False
                else:
                    return False, "未识别改进机会并制定改进措施", "建议在处置阶段针对发现的问题制定具体的改进措施", True
            elif requirement == "验证改进措施的有效性":
                if 'improvement_verification' in act_data and act_data['improvement_verification']:
                    return True, "", "", False
                else:
                    return False, "未验证改进措施的有效性", "建议对改进措施的实施效果进行跟踪验证", True
        # ==================== 循证决策 ====================
        elif principle_key == 'evidence_based_decision_making':
            if requirement == "收集相关数据和信息":
                if 'data_collection' in do_data and do_data['data_collection']:
                    return True, "", "", False
                else:
                    return False, "未系统收集决策所需的数据和信息", "建议在执行阶段建立数据收集机制，确保决策数据完整准确", True
            elif requirement == "确保数据和信息的真实可靠":
                if 'data_verification' in do_data and do_data['data_verification']:
                    return True, "", "", False
                else:
                    return False, "未对数据真实性进行验证", "建议建立数据验证机制，确保决策依据真实可靠", True
            elif requirement == "基于数据分析做出决策":
                if 'decision_analysis' in plan_data or 'decision_analysis' in check_data:
                    return True, "", "", False
                else:
                    return False, "决策未基于数据分析", "建议重大决策必须有数据分析支持，记录决策依据和过程", True
            elif requirement == "记录决策依据和过程":
                if 'decision_records' in plan_data or 'decision_records' in check_data:
                    return True, "", "", False
                else:
                    return False, "未记录决策依据和过程", "建议对重要决策的依据、过程和结果进行完整记录", True
        # 默认通过（对于不常用的要求）
        return True, "", "", False
    def _generate_summary(self, check_results: List[CheckResult], overall_score: float) -> Tuple[str, List[str], List[str]]:
        """
        生成校验摘要、建议和必填行动
        Args:
            check_results: 检查结果列表
            overall_score: 总体得分
        Returns:
            (摘要, 建议列表, 必填行动列表)
        """
        total_issues = sum(len(result.issues) for result in check_results)
        non_compliant_count = sum(1 for result in check_results if result.level == ComplianceLevel.NON_COMPLIANT)
        partially_compliant_count = sum(1 for result in check_results if result.level == ComplianceLevel.PARTIALLY_COMPLIANT)
        evidence_required_count = sum(1 for result in check_results if result.evidence_required)
        # 生成摘要
        if overall_score >= 90:
            summary = f"项目总体符合ISO9001质量体系要求，总体得分{overall_score}分。"
        elif overall_score >= 70:
            summary = f"项目部分符合ISO9001质量体系要求，总体得分{overall_score}分，存在{total_issues}个需要改进的问题。"
        else:
            summary = f"项目不符合ISO9001质量体系要求，总体得分{overall_score}分，存在{non_compliant_count}个严重不符合项，{partially_compliant_count}个部分符合项，共{total_issues}个问题需要整改。"
        # 生成建议
        recommendations = []
        required_actions = []
        for result in check_results:
            if result.level == ComplianceLevel.NON_COMPLIANT:
                recommendations.append(f"【严重不符合】{self.QUALITY_PRINCIPLES[result.principle]['name']}: {result.score}分，需立即整改")
                required_actions.extend(result.issues)
            elif result.level == ComplianceLevel.PARTIALLY_COMPLIANT:
                recommendations.append(f"【部分符合】{self.QUALITY_PRINCIPLES[result.principle]['name']}: {result.score}分，建议改进")
                recommendations.extend(result.suggestions)
        if evidence_required_count > 0:
            recommendations.append(f"需补充{evidence_required_count}项证据材料以证明合规性")
            required_actions.append("补充缺失的证据材料")
        # 添加通用建议
        if overall_score < 90:
            recommendations.append("建议针对不符合项制定整改计划，明确责任人、整改措施和完成时限")
            recommendations.append("建议定期开展ISO9001内部审核，持续提升质量管理水平")
        return summary, recommendations, required_actions
    def get_compliance_level_description(self, level: ComplianceLevel) -> str:
        """
        获取合规等级的中文描述
        Args:
            level: 合规等级
        Returns:
            中文描述
        """
        descriptions = {
            ComplianceLevel.FULLY_COMPLIANT: "完全符合ISO9001要求",
            ComplianceLevel.PARTIALLY_COMPLIANT: "部分符合ISO9001要求，需改进",
            ComplianceLevel.NON_COMPLIANT: "不符合ISO9001要求，需立即整改",
            ComplianceLevel.NOT_APPLICABLE: "ISO9001校验未启用"
        }
        return descriptions.get(level, "未知等级")
    def generate_validation_report_markdown(self, report: ValidationReport) -> str:
        """
        生成Markdown格式的验证报告
        Args:
            report: 验证报告对象
        Returns:
            Markdown格式的报告内容
        """
        markdown = f"""# ISO9001质量管理体系验证报告
## 一、总体情况
- **总体合规等级**: {self.get_compliance_level_description(report.overall_compliance)}
- **总体得分**: {report.overall_score}/100
- **评估时间**: {self._get_current_time()}
## 二、各原则校验详情
| 质量管理原则 | 得分 | 合规等级 | 问题数量 |
|-------------|------|----------|----------|
"""
        for result in report.check_results:
            principle_name = self.QUALITY_PRINCIPLES[result.principle]['name']
            level_desc = self.get_compliance_level_description(result.level).split('，')[0]
            markdown += f"| {principle_name} | {result.score} | {level_desc} | {len(result.issues)} |\n"
        markdown += """
## 三、详细检查结果
"""
        for result in report.check_results:
            principle = self.QUALITY_PRINCIPLES[result.principle]
            markdown += f"""
### {principle['name']}
- **得分**: {result.score}/100
- **合规等级**: {self.get_compliance_level_description(result.level)}
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
## 四、总结与建议
### 摘要
"""
        markdown += report.summary + "\n"
        if report.recommendations:
            markdown += "\n### 改进建议\n"
            for rec in report.recommendations:
                markdown += f"- {rec}\n"
        if report.required_actions:
            markdown += "\n### 必填行动\n"
            for action in report.required_actions:
                markdown += f"- ⚠️ {action}\n"
        markdown += """
---
*本报告基于ISO9001:2015质量管理体系标准生成*
"""
        return markdown
    def _get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def check_documentation_requirement(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查文件化信息要求是否满足
        Args:
            project_data: 项目数据
        Returns:
            检查结果
        """
        if not self.requirements['documented_information_required']:
            return {"compliant": True, "message": "文件化信息要求未启用"}
        required_documents = [
            "质量方针",
            "质量目标", 
            "范围",
            "程序文件",
            "过程记录",
            "绩效记录",
            "内审记录",
            "管理评审记录"
        ]
        available_documents = project_data.get('documents', [])
        missing_documents = [doc for doc in required_documents if doc not in available_documents]
        compliant = len(missing_documents) == 0
        return {
            "compliant": compliant,
            "missing_documents": missing_documents,
            "message": "文件化信息完整" if compliant else f"缺少以下文件: {', '.join(missing_documents)}"
        }
