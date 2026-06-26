#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
决策质量校验引擎
实现决策的多维度校验、风险评估、可行性分析，确保决策科学严谨、实事求是
"""
import re
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from .utils import load_config, logger, calculate_risk_level
class DecisionRiskLevel(Enum):
    """决策风险等级"""
    LOW = "low"           # 低风险
    MEDIUM = "medium"     # 中风险
    HIGH = "high"         # 高风险
    CRITICAL = "critical" # 极高风险
class DecisionQuality(Enum):
    """决策质量等级"""
    EXCELLENT = "excellent"   # 优秀（90+）
    GOOD = "good"             # 良好（80-89）
    FAIR = "fair"             # 一般（70-79）
    POOR = "poor"             # 较差（60-69）
    INVALID = "invalid"       # 无效（<60）
@dataclass
class CheckItemResult:
    """检查项结果"""
    name: str
    description: str
    score: float  # 0-100
    passed: bool
    issues: List[str]
    suggestions: List[str]
    evidence_required: bool
@dataclass
class DecisionCheckReport:
    """决策检查报告"""
    decision_id: str
    decision_content: str
    overall_score: float
    quality_level: DecisionQuality
    risk_level: DecisionRiskLevel
    check_results: List[CheckItemResult]
    passed: bool
    summary: str
    recommendations: List[str]
    warnings: List[str]
    required_actions: List[str]
    generated_at: str
class DecisionChecker:
    """决策质量校验引擎类"""
    # 检查项定义
    CHECK_ITEMS = {
        "information_authenticity": {
            "name": "信息真实性校验",
            "description": "检查决策依据的信息是否真实可靠",
            "weight": 20,
            "mandatory": True,
            "pass_threshold": 60
        },
        "information_completeness": {
            "name": "信息完整性校验",
            "description": "检查决策所需的信息是否完整，是否存在关键信息缺失",
            "weight": 15,
            "mandatory": False,
            "pass_threshold": 60
        },
        "logic_consistency": {
            "name": "逻辑一致性校验",
            "description": "检查决策推理过程是否逻辑严谨、前后一致",
            "weight": 20,
            "mandatory": True,
            "pass_threshold": 60
        },
        "risk_assessment": {
            "name": "风险评估",
            "description": "检查是否充分识别和评估了潜在风险",
            "weight": 20,
            "mandatory": True,
            "pass_threshold": 60
        },
        "impact_analysis": {
            "name": "影响分析",
            "description": "检查是否全面分析了决策的短期和长期影响",
            "weight": 10,
            "mandatory": False,
            "pass_threshold": 60
        },
        "feasibility_verification": {
            "name": "可行性验证",
            "description": "检查决策在技术、资源、时间上是否可行",
            "weight": 10,
            "mandatory": False,
            "pass_threshold": 60
        },
        "compliance_check": {
            "name": "合规性检查",
            "description": "检查决策是否符合法律法规、政策要求和内部规定",
            "weight": 15,
            "mandatory": True,
            "pass_threshold": 60
        },
        "stakeholder_consideration": {
            "name": "利益相关方考虑",
            "description": "检查是否充分考虑了各利益相关方的权益和影响",
            "weight": 10,
            "mandatory": False,
            "pass_threshold": 60
        }
    }
    # 模糊表述关键词（降低可信度）
    VAGUE_KEYWORDS = [
        '可能', '大概', '也许', '差不多', '应该', '估计', '预计', '有望',
        '大概率', '可能性大', '基本上', '大致', '约', '左右', '上下',
        '尽量', '尽可能', '努力', '争取', '力争', '尝试', '探索'
    ]
    # 绝对表述关键词（需要验证）
    ABSOLUTE_KEYWORDS = [
        '绝对', '完全', '100%', '全部', '所有', '一切', '完美', '最优',
        '最好', '最大', '最小', '最快', '最慢', '唯一', '永不', '始终'
    ]
    # 风险关键词
    RISK_KEYWORDS = [
        '风险', '危险', '隐患', '问题', '困难', '挑战', '压力', '阻力',
        '不确定', '不稳定', '波动', '下滑', '下降', '亏损', '失败',
        '违约', '违规', '违法', '处罚', '诉讼', '纠纷', '事故', '灾难'
    ]
    # 合规风险关键词
    COMPLIANCE_KEYWORDS = [
        '违规', '违法', '违反', '禁止', '不得', '严禁', '查处', '处罚',
        '问责', '追责', '合规', '监管', '规定', '条例', '法律', '法规',
        '政策', '要求', '标准', '规范', '流程', '制度'
    ]
    def __init__(self):
        self.config = load_config()
        self.enabled_checks = self.config['decision_check']['check_items']
        self.pass_threshold = self.config['decision_check']['pass_score_threshold']
        self.mandatory_checks = self.config['decision_check']['mandatory_checks']
        self.weights = self.config['scoring']['decision_score_weights']
        logger.info("决策校验引擎初始化完成")
    def validate_decision(
        self, 
        decision_content: str, 
        context: Optional[Dict[str, Any]] = None,
        evidence: Optional[List[Dict[str, Any]]] = None
    ) -> DecisionCheckReport:
        """
        校验决策质量
        Args:
            decision_content: 决策内容文本
            context: 决策上下文信息，可选
            evidence: 证据材料列表，可选
        Returns:
            决策检查报告
        """
        if context is None:
            context = {}
        if evidence is None:
            evidence = []
        decision_id = self._generate_decision_id()
        check_results = []
        total_weighted_score = 0.0
        total_weight = 0.0
        all_passed = True
        # 执行每个启用的检查项
        for check_key in self.enabled_checks:
            if check_key not in self.CHECK_ITEMS:
                continue
            check_item = self.CHECK_ITEMS[check_key]
            # 执行检查
            result = self._run_check(
                check_key, 
                check_item, 
                decision_content, 
                context, 
                evidence
            )
            check_results.append(result)
            # 计算加权得分
            weight = self.weights.get(check_key, check_item.get('weight', 10))
            total_weighted_score += result.score * weight
            total_weight += weight
            # 检查是否通过
            if not result.passed:
                all_passed = False
                if check_item.get('mandatory', False):
                    logger.warning(f"强制检查项 {check_item['name']} 未通过")
        # 计算总体得分
        if total_weight > 0:
            overall_score = round(total_weighted_score / total_weight, 2)
        else:
            overall_score = 0.0
        # 确定质量等级
        if overall_score >= 90:
            quality_level = DecisionQuality.EXCELLENT
        elif overall_score >= 80:
            quality_level = DecisionQuality.GOOD
        elif overall_score >= 70:
            quality_level = DecisionQuality.FAIR
        elif overall_score >= 60:
            quality_level = DecisionQuality.POOR
        else:
            quality_level = DecisionQuality.INVALID
        # 评估风险等级
        risk_level = self._assess_risk_level(decision_content, context, check_results)
        # 确定是否通过
        passed = all_passed and overall_score >= self.pass_threshold
        # 生成摘要和建议
        summary, recommendations, warnings, required_actions = self._generate_summary(
            decision_content, overall_score, quality_level, risk_level, check_results, passed
        )
        report = DecisionCheckReport(
            decision_id=decision_id,
            decision_content=decision_content,
            overall_score=overall_score,
            quality_level=quality_level,
            risk_level=risk_level,
            check_results=check_results,
            passed=passed,
            summary=summary,
            recommendations=recommendations,
            warnings=warnings,
            required_actions=required_actions,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        logger.info(f"决策校验完成，ID: {decision_id}, 得分: {overall_score}, 质量: {quality_level.value}, 风险: {risk_level.value}, 通过: {passed}")
        return report
    def _run_check(
        self, 
        check_key: str, 
        check_item: Dict[str, Any], 
        decision_content: str, 
        context: Dict[str, Any],
        evidence: List[Dict[str, Any]]
    ) -> CheckItemResult:
        """
        运行单个检查项
        Args:
            check_key: 检查项标识
            check_item: 检查项配置
            decision_content: 决策内容
            context: 上下文
            evidence: 证据列表
        Returns:
            检查结果
        """
        issues = []
        suggestions = []
        evidence_required = False
        score = 100
        pass_threshold = check_item.get('pass_threshold', 60)
        # ==================== 信息真实性校验 ====================
        if check_key == 'information_authenticity':
            # 检查模糊表述
            vague_count = sum(1 for keyword in self.VAGUE_KEYWORDS if keyword in decision_content)
            if vague_count > 0:
                vague_words = [k for k in self.VAGUE_KEYWORDS if k in decision_content]
                issues.append(f"存在{vague_count}处模糊表述（{', '.join(vague_words)}），降低信息可信度")
                score -= min(vague_count * 5, 30)  # 最多扣30分
                suggestions.append("建议替换模糊表述为明确、具体的描述")
                evidence_required = True
            # 检查绝对表述
            absolute_count = sum(1 for keyword in self.ABSOLUTE_KEYWORDS if keyword in decision_content)
            if absolute_count > 0:
                absolute_words = [k for k in self.ABSOLUTE_KEYWORDS if k in decision_content]
                issues.append(f"存在{absolute_count}处绝对表述（{', '.join(absolute_words)}），需要验证真实性")
                score -= min(absolute_count * 3, 20)  # 最多扣20分
                suggestions.append("建议对绝对表述提供事实依据，避免夸大")
                evidence_required = True
            # 检查是否有信息来源
            if '来源' not in decision_content and '依据' not in decision_content and '数据显示' not in decision_content:
                issues.append("未注明信息来源和决策依据")
                score -= 20
                suggestions.append("建议注明关键信息的来源和决策依据")
                evidence_required = True
            # 验证证据
            if not evidence:
                issues.append("未提供任何证据材料支持决策")
                score -= 30
                suggestions.append("建议提供相关数据、资料等证据材料")
                evidence_required = True
        # ==================== 信息完整性校验 ====================
        elif check_key == 'information_completeness':
            # 检查决策要素是否完整（5W1H）
            required_elements = {
                '目标': ['目标', '目的', '要达到', '实现'],
                '措施': ['措施', '方法', '怎么做', '实施'],
                '责任人': ['责任人', '负责人', '由谁', '负责'],
                '时间': ['时间', '期限', '截止', '完成日期', '之前'],
                '验收标准': ['验收', '标准', '考核', '达标', '合格']
            }
            missing_elements = []
            for element_name, keywords in required_elements.items():
                found = any(keyword in decision_content for keyword in keywords)
                if not found:
                    missing_elements.append(element_name)
            if missing_elements:
                issues.append(f"决策要素不完整，缺少: {', '.join(missing_elements)}")
                score -= len(missing_elements) * 10
                suggestions.append("建议补充完整的5W1H要素（原因、对象、地点、时间、人员、方法）")
            # 检查是否有备选方案
            if '备选方案' not in decision_content and '方案二' not in decision_content and 'Plan B' not in decision_content:
                issues.append("未提及备选方案和应急预案")
                score -= 15
                suggestions.append("建议考虑至少1-2个备选方案，并制定风险应对预案")
            # 检查是否有假设前提
            if '假设' not in decision_content and '前提' not in decision_content and '条件' not in decision_content:
                issues.append("未明确决策的假设前提和适用条件")
                score -= 10
                suggestions.append("建议明确决策适用的前提条件和边界范围")
        # ==================== 逻辑一致性校验 ====================
        elif check_key == 'logic_consistency':
            # 检查是否有逻辑矛盾
            contradictions = self._detect_contradictions(decision_content)
            if contradictions:
                issues.append(f"存在逻辑矛盾: {'; '.join(contradictions)}")
                score -= min(len(contradictions) * 20, 50)  # 最多扣50分
                suggestions.append("建议梳理决策逻辑，消除矛盾表述")
            # 检查推理链条是否完整
            if ('因为' in decision_content or '由于' in decision_content) and ('所以' not in decision_content and '因此' not in decision_content):
                issues.append("有原因分析但没有对应结论，推理链条不完整")
                score -= 15
                suggestions.append("建议完善推理过程，明确因果关系")
            if ('如果' in decision_content or '假设' in decision_content) and ('那么' not in decision_content and '则' not in decision_content):
                issues.append("有假设条件但没有对应结论，逻辑链条断裂")
                score -= 15
                suggestions.append("建议明确不同假设下的对应结论和应对措施")
            # 检查是否有逻辑跳跃
            if '因此' in decision_content or '所以' in decision_content:
                parts = re.split(r'因此|所以', decision_content, maxsplit=1)
                if len(parts[0].strip()) < 10 or len(parts[1].strip()) < 5:
                    issues.append("推理过程过于简略，存在逻辑跳跃")
                    score -= 10
                    suggestions.append("建议详细阐述推理过程，避免逻辑跳跃")
        # ==================== 风险评估 ====================
        elif check_key == 'risk_assessment':
            # 检查是否识别了风险
            risk_count = sum(1 for keyword in self.RISK_KEYWORDS if keyword in decision_content)
            if risk_count == 0:
                issues.append("未识别任何潜在风险，风险意识不足")
                score -= 30
                suggestions.append("建议全面识别潜在的技术、市场、运营、合规等各类风险")
                evidence_required = True
            else:
                # 检查是否有风险应对措施
                if '应对' not in decision_content and '措施' not in decision_content and '预案' not in decision_content:
                    issues.append(f"识别到{risk_count}个风险点，但未制定对应的风险应对措施")
                    score -= 20
                    suggestions.append("建议针对每个识别到的风险制定具体的应对措施和应急预案")
            # 检查风险分级
            if '高风险' not in decision_content and '中风险' not in decision_content and '低风险' not in decision_content:
                issues.append("未对风险进行分级评估")
                score -= 15
                suggestions.append("建议对识别到的风险进行分级（高/中/低），并优先应对高风险项")
        # ==================== 影响分析 ====================
        elif check_key == 'impact_analysis':
            # 检查是否考虑了正面影响
            if '收益' not in decision_content and '好处' not in decision_content and '价值' not in decision_content:
                issues.append("未分析决策带来的正面影响和预期收益")
                score -= 15
                suggestions.append("建议量化分析决策的预期收益和价值")
            # 检查是否考虑了负面影响
            if '负面影响' not in decision_content and '坏处' not in decision_content and '损失' not in decision_content:
                issues.append("未分析决策可能带来的负面影响和潜在损失")
                score -= 20
                suggestions.append("建议充分评估决策可能带来的负面影响和潜在损失")
            # 检查是否考虑了长期影响
            if '长期' not in decision_content and '未来' not in decision_content and '长远' not in decision_content:
                issues.append("未考虑决策的长期影响和后续效应")
                score -= 10
                suggestions.append("建议分析决策的短期和长期影响，避免短视行为")
        # ==================== 可行性验证 ====================
        elif check_key == 'feasibility_verification':
            # 检查技术可行性
            if '技术' in decision_content and ('可行' not in decision_content and '不可行' not in decision_content):
                issues.append("提及了技术因素，但未验证技术可行性")
                score -= 15
                suggestions.append("建议对技术方案进行可行性验证，确保技术上可实现")
            # 检查资源可行性
            resource_keywords = ['人力', '人员', '资金', '预算', '设备', '系统', '资源']
            has_resource = any(key in decision_content for key in resource_keywords)
            if has_resource and '足够' not in decision_content and '充足' not in decision_content and '不足' not in decision_content:
                issues.append("提及了资源需求，但未评估资源是否充足")
                score -= 15
                suggestions.append("建议评估所需资源是否能够得到满足，包括人力、资金、设备等")
            # 检查时间可行性
            if '时间' in decision_content and '紧张' not in decision_content and '充足' not in decision_content and '足够' not in decision_content:
                issues.append("提及了时间要求，但未评估时间是否充足")
                score -= 10
                suggestions.append("建议评估时间进度是否合理，是否能够按时完成")
        # ==================== 合规性检查 ====================
        elif check_key == 'compliance_check':
            # 检查是否有合规风险
            compliance_count = sum(1 for keyword in self.COMPLIANCE_KEYWORDS if keyword in decision_content)
            if compliance_count > 0:
                # 检查是否有合规评估
                if '合规' not in decision_content and '合法' not in decision_content and '符合规定' not in decision_content:
                    issues.append(f"涉及{compliance_count}个合规相关表述，但未进行合规性评估")
                    score -= 30
                    suggestions.append("建议对决策进行合规性审查，确保符合法律法规和内部规定")
                    evidence_required = True
            # 检查是否有禁止性内容
            forbidden_keywords = ['严禁', '禁止', '不得', '不准']
            has_forbidden = any(key in decision_content for key in forbidden_keywords)
            if has_forbidden and '不违反' not in decision_content and '符合' not in decision_content:
                issues.append("提及了禁止性规定，但未明确决策是否符合规定")
                score -= 25
                suggestions.append("建议明确决策不违反相关禁止性规定，必要时寻求法务部门意见")
        # ==================== 利益相关方考虑 ====================
        elif check_key == 'stakeholder_consideration':
            # 检查是否考虑了相关方
            stakeholders = ['用户', '客户', '员工', '合作方', '供应商', '伙伴', '股东', '公众']
            considered = [s for s in stakeholders if s in decision_content]
            if len(considered) < 2:
                issues.append(f"仅考虑了{len(considered)}个利益相关方，考虑不够全面")
                score -= 15
                suggestions.append("建议全面考虑用户、员工、合作伙伴、股东等各利益相关方的权益")
            # 检查是否有沟通机制
            if '沟通' not in decision_content and '告知' not in decision_content and '通知' not in decision_content:
                issues.append("未制定与利益相关方的沟通机制")
                score -= 10
                suggestions.append("建议制定与各利益相关方的沟通计划，及时告知相关信息")
        # 确保分数在0-100之间
        score = max(0, min(100, score))
        # 判断是否通过
        passed = score >= pass_threshold
        return CheckItemResult(
            name=check_item['name'],
            description=check_item['description'],
            score=score,
            passed=passed,
            issues=issues,
            suggestions=suggestions,
            evidence_required=evidence_required
        )
    def _detect_contradictions(self, text: str) -> List[str]:
        """
        检测文本中的逻辑矛盾
        Args:
            text: 要检测的文本
        Returns:
            矛盾列表
        """
        contradictions = []
        # 常见矛盾对
        contradiction_pairs = [
            ('增加', '减少'),
            ('提高', '降低'),
            ('上升', '下降'),
            ('支持', '反对'),
            ('同意', '拒绝'),
            ('开始', '停止'),
            ('启用', '停用'),
            ('建设', '拆除'),
            ('扩大', '缩小'),
            ('加强', '削弱'),
            ('提前', '推迟'),
            ('盈利', '亏损'),
            ('增长', '下滑'),
            ('允许', '禁止'),
            ('公开', '保密'),
            ('统一', '分散'),
            ('集中', '分散'),
            ('肯定', '否定'),
            ('承认', '否认'),
            ('正确', '错误')
        ]
        # 检测矛盾对是否同时出现
        for a, b in contradiction_pairs:
            if a in text and b in text:
                # 简单的位置检测，如果在同一段落中同时出现则可能矛盾
                a_pos = text.find(a)
                b_pos = text.find(b)
                if abs(a_pos - b_pos) < 100:  # 100字符以内同时出现
                    contradictions.append(f"同时提及「{a}」和「{b}」")
        # 检测自相矛盾的表述
        if '不是' in text and '是' in text and text.index('不是') < text.index('是'):
            contradictions.append("存在「不是...是...」的矛盾表述")
        if '没有' in text and '有' in text and text.index('没有') < text.index('有'):
            contradictions.append("存在「没有...有...」的矛盾表述")
        return contradictions
    def _assess_risk_level(
        self, 
        decision_content: str, 
        context: Dict[str, Any], 
        check_results: List[CheckItemResult]
    ) -> DecisionRiskLevel:
        """
        评估决策风险等级
        Args:
            decision_content: 决策内容
            context: 上下文
            check_results: 检查结果
        Returns:
            风险等级
        """
        # 风险关键词数量
        risk_count = sum(1 for keyword in self.RISK_KEYWORDS if keyword in decision_content)
        # 未通过的强制检查项数量
        mandatory_failed = sum(1 for result in check_results if 
                              self.CHECK_ITEMS.get(result.name, {}).get('mandatory', False) and not result.passed)
        # 低分项数量
        low_score_count = sum(1 for result in check_results if result.score < 60)
        # 计算风险概率（0-10）和影响程度（0-10）
        probability = min(risk_count * 2, 10)
        impact = min((mandatory_failed * 3 + low_score_count * 2), 10)
        # 计算风险等级
        level = calculate_risk_level(probability, impact)
        return DecisionRiskLevel(level)
    def _generate_summary(
        self,
        decision_content: str,
        overall_score: float,
        quality_level: DecisionQuality,
        risk_level: DecisionRiskLevel,
        check_results: List[CheckItemResult],
        passed: bool
    ) -> Tuple[str, List[str], List[str], List[str]]:
        """
        生成校验摘要、建议、警告和必填行动
        Args:
            decision_content: 决策内容
            overall_score: 总体得分
            quality_level: 质量等级
            risk_level: 风险等级
            check_results: 检查结果列表
            passed: 是否通过
        Returns:
            (摘要, 建议列表, 警告列表, 必填行动列表)
        """
        # 计算统计数据
        total_issues = sum(len(result.issues) for result in check_results)
        failed_count = sum(1 for result in check_results if not result.passed)
        mandatory_failed = sum(1 for result in check_results if 
                              self.CHECK_ITEMS.get(result.name, {}).get('mandatory', False) and not result.passed)
        evidence_required_count = sum(1 for result in check_results if result.evidence_required)
        # 生成摘要
        quality_desc = {
            DecisionQuality.EXCELLENT: "优秀，决策科学严谨，依据充分",
            DecisionQuality.GOOD: "良好，决策质量较高，略有改进空间",
            DecisionQuality.FAIR: "一般，决策基本可行，存在一定改进空间",
            DecisionQuality.POOR: "较差，决策质量较低，存在较多问题",
            DecisionQuality.INVALID: "无效，决策存在严重问题，不可行"
        }
        risk_desc = {
            DecisionRiskLevel.LOW: "低风险",
            DecisionRiskLevel.MEDIUM: "中风险",
            DecisionRiskLevel.HIGH: "高风险",
            DecisionRiskLevel.CRITICAL: "极高风险"
        }
        if passed:
            summary = f"决策校验通过，总体得分{overall_score}分，质量{quality_desc[quality_level]}，{risk_desc[risk_level]}。共发现{total_issues}个问题，{failed_count}个检查项未通过。"
        else:
            summary = f"决策校验未通过，总体得分{overall_score}分，质量{quality_desc[quality_level]}，{risk_desc[risk_level]}。共发现{total_issues}个问题，{failed_count}个检查项未通过，其中{mandatory_failed}个为强制检查项。"
        # 生成建议
        recommendations = []
        # 生成警告
        warnings = []
        # 生成必填行动
        required_actions = []
        # 收集各类信息
        for result in check_results:
            if not result.passed:
                if self.CHECK_ITEMS.get(result.name, {}).get('mandatory', False):
                    warnings.append(f"⚠️ 强制检查项【{result.name}】未通过，得分{result.score}分")
                    required_actions.extend(result.issues)
                else:
                    recommendations.append(f"💡 建议改进【{result.name}】，当前得分{result.score}分")
                    recommendations.extend(result.suggestions)
            if result.evidence_required:
                required_actions.append(f"📑 需补充【{result.name}】相关的证据材料")
        # 添加通用建议
        if not passed:
            recommendations.append("建议针对所有未通过的检查项进行整改，重新提交校验")
        if risk_level in [DecisionRiskLevel.HIGH, DecisionRiskLevel.CRITICAL]:
            warnings.append(f"⚠️ 决策风险等级为{risk_desc[risk_level]}，建议审慎评估")
            required_actions.append("需重新进行风险评估，制定完善的风险应对措施")
        if evidence_required_count > 0:
            required_actions.append(f"共需补充{evidence_required_count}项证据材料以支持决策")
        return summary, recommendations, warnings, required_actions
    def generate_report_markdown(self, report: DecisionCheckReport) -> str:
        """
        生成Markdown格式的校验报告
        Args:
            report: 校验报告对象
        Returns:
            Markdown格式的报告
        """
        # 质量等级描述
        quality_desc = {
            DecisionQuality.EXCELLENT: "优秀",
            DecisionQuality.GOOD: "良好",
            DecisionQuality.FAIR: "一般",
            DecisionQuality.POOR: "较差",
            DecisionQuality.INVALID: "无效"
        }
        # 风险等级描述
        risk_desc = {
            DecisionRiskLevel.LOW: "低风险",
            DecisionRiskLevel.MEDIUM: "中风险",
            DecisionRiskLevel.HIGH: "高风险",
            DecisionRiskLevel.CRITICAL: "极高风险"
        }
        # 结果标识
        passed_icon = "✅" if report.passed else "❌"
        markdown = f"""# 决策质量校验报告
{passed_icon} **校验结果**: {'通过' if report.passed else '未通过'}
- **决策ID**: {report.decision_id}
- **生成时间**: {report.generated_at}
- **总体得分**: {report.overall_score}/100
- **质量等级**: {quality_desc[report.quality_level]}
- **风险等级**: {risk_desc[report.risk_level]}
## 一、决策内容摘要
> {report.decision_content[:300]}{'...' if len(report.decision_content) > 300 else ''}
## 二、各检查项详情
| 检查项 | 得分 | 结果 | 问题数量 | 需证据 |
|--------|------|------|----------|--------|
"""
        for result in report.check_results:
            item_passed = "✅ 通过" if result.passed else "❌ 未通过"
            need_evidence = "是" if result.evidence_required else "否"
            markdown += f"| {result.name} | {result.score} | {item_passed} | {len(result.issues)} | {need_evidence} |\n"
        markdown += """
## 三、详细检查结果
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
## 四、总结与建议
### 摘要
"""
        markdown += report.summary + "\n"
        if report.warnings:
            markdown += "\n### ⚠️ 警告\n"
            for warning in report.warnings:
                markdown += f"- {warning}\n"
        if report.required_actions:
            markdown += "\n### 📋 必填行动\n"
            for action in report.required_actions:
                markdown += f"- {action}\n"
        if report.recommendations:
            markdown += "\n### 💡 改进建议\n"
            for rec in report.recommendations:
                markdown += f"- {rec}\n"
        markdown += """
---
*本报告基于实事求是原则生成，所有结论均基于多维度客观校验*
"""
        return markdown
    def _generate_decision_id(self) -> str:
        """生成唯一决策ID"""
        return f"DEC-{uuid.uuid4().hex[:16].upper()}"
    def save_report(self, report: DecisionCheckReport, path: str) -> bool:
        """
        保存报告到文件
        Args:
            report: 报告对象
            path: 保存路径
        Returns:
            是否保存成功
        """
        try:
            import json
            data = asdict(report)
            # 转换枚举为字符串
            data['quality_level'] = data['quality_level'].value
            data['risk_level'] = data['risk_level'].value
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"决策报告已保存到: {path}")
            return True
        except Exception as e:
            logger.error(f"保存决策报告失败: {e}")
