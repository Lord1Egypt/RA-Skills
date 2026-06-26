#!/usr/bin/env python3
"""
优化后的需求解读技能主类
整合智能分类引擎和案例库，实现需求类型驱动的多维解读
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

class RequirementType(str, Enum):
    """需求类型枚举"""
    TECH_DEV = "技术开发"
    CONTENT_CREATION = "内容创作"
    DATA_ANALYSIS = "数据分析"
    BUSINESS_PROCESS = "业务流程"
    PROBLEM_SOLVING = "问题解决"
    CONSULTING = "咨询服务"

class UrgencyLevel(str, Enum):
    """紧急程度枚举"""
    EMERGENCY = "紧急"
    IMPORTANT = "重要"
    NORMAL = "常规"
    OPTIMIZATION = "优化"

class ComplexityLevel(str, Enum):
    """复杂度枚举"""
    SIMPLE = "简单"
    MEDIUM = "中等"
    COMPLEX = "复杂"

@dataclass
class RequirementContext:
    """需求上下文信息"""
    industry: str = "通用"
    urgency: UrgencyLevel = UrgencyLevel.NORMAL
    complexity: ComplexityLevel = ComplexityLevel.MEDIUM
    user_history: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RequirementClassification:
    """需求分类结果"""
    primary_type: RequirementType
    secondary_type: str
    confidence: float
    matched_keywords: List[str]
    context: RequirementContext
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class DimensionSet:
    """需求思考维度集合"""
    name: str
    dimensions: List[str]
    description: str = ""
    priority: int = 1

@dataclass
class CaseTemplate:
    """案例模板"""
    id: str
    title: str
    requirement_type: RequirementType
    sub_type: str
    industry: str
    structured_requirements: Dict[str, List[str]]
    interview_questions: List[str]
    best_practices: List[str]
    success_metrics: List[str]
    implementation_tips: List[str]

class OptimizedRequirementInterpreter:
    """优化后的需求解读器"""
    
    def __init__(self, case_library_file: str = None):
        # 初始化组件
        self._init_dimension_sets()
        self._load_case_library(case_library_file)
        self._init_question_templates()
        self._init_interview_strategies()
        
        # 学习系统
        self.interaction_log = []
        self.case_similarity_cache = {}
        
    def _init_dimension_sets(self):
        """初始化维度集合"""
        self.dimension_sets = {
            RequirementType.TECH_DEV: [
                DimensionSet(
                    name="核心功能",
                    dimensions=["功能定义", "模块划分", "接口设计", "数据模型"],
                    description="功能需求和实现架构"
                ),
                DimensionSet(
                    name="技术架构", 
                    dimensions=["技术栈选择", "架构风格", "部署方案", "监控运维"],
                    description="技术实现方案和基础设施"
                ),
                DimensionSet(
                    name="性能安全",
                    dimensions=["响应时间", "并发能力", "安全防护", "数据隐私"],
                    description="系统质量和安全保障"
                ),
                DimensionSet(
                    name="用户体验",
                    dimensions=["界面设计", "交互流程", "多端适配", "易用性"],
                    description="用户感知和使用体验"
                )
            ],
            
            RequirementType.CONTENT_CREATION: [
                DimensionSet(
                    name="创作目标",
                    dimensions=["营销目标", "传达信息", "受众反应", "品牌形象"],
                    description="内容创作的目的和期望效果"
                ),
                DimensionSet(
                    name="内容要素",
                    dimensions=["文字内容", "视觉元素", "设计风格", "品牌元素"],
                    description="内容的具体构成要素"
                ),
                DimensionSet(
                    name="形式规格",
                    dimensions=["尺寸比例", "文件格式", "分辨率", "技术要求"],
                    description="技术规格和形式要求"
                ),
                DimensionSet(
                    name="分发渠道",
                    dimensions=["使用场景", "平台适配", "版权合规", "多语言"],
                    description="内容应用和分发方式"
                )
            ],
            
            RequirementType.DATA_ANALYSIS: [
                DimensionSet(
                    name="分析目标",
                    dimensions=["业务问题", "分析目的", "决策支持", "效果评估"],
                    description="数据分析的核心目标"
                ),
                DimensionSet(
                    name="数据基础", 
                    dimensions=["数据来源", "数据质量", "数据规模", "数据处理"],
                    description="数据资源和处理能力"
                ),
                DimensionSet(
                    name="分析方法",
                    dimensions=["统计方法", "分析模型", "可视化方案", "算法选择"],
                    description="分析技术和工具方法"
                ),
                DimensionSet(
                    name="结果应用",
                    dimensions=["报告形式", "更新频率", "用户权限", "反馈机制"],
                    description="分析结果的应用方式"
                )
            ]
        }
        
        # 为其他类型添加通用维度
        generic_dimensions = DimensionSet(
            name="通用维度",
            dimensions=["需求目标", "实施范围", "约束条件", "成功标准", "时间要求", "资源限制"],
            description="适用于所有需求类型的通用思考维度"
        )
        
        for req_type in RequirementType:
            if req_type not in self.dimension_sets:
                self.dimension_sets[req_type] = [generic_dimensions]
    
    def _load_case_library(self, case_library_file: str):
        """加载案例库"""
        if case_library_file:
            try:
                with open(case_library_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.case_library = {}
                    
                    for case_id, case_data in data.get('cases', {}).items():
                        # 转换枚举类型
                        req_type = RequirementType(case_data['type'])
                        
                        template = CaseTemplate(
                            id=case_id,
                            title=case_data['title'],
                            requirement_type=req_type,
                            sub_type=case_data['subtype'],
                            industry=case_data['industry'],
                            structured_requirements=case_data['structured_requirements'],
                            interview_questions=case_data['interview_questions'],
                            best_practices=case_data['best_practices'],
                            success_metrics=case_data['success_metrics'],
                            implementation_tips=case_data['implementation_tips']
                        )
                        
                        self.case_library[case_id] = template
                    
                    print(f"✅ 案例库加载成功，共{len(self.case_library)}个案例")
                    
            except Exception as e:
                print(f"⚠️ 案例库加载失败: {e}")
                self.case_library = {}
        else:
            self.case_library = {}
    
    def _init_question_templates(self):
        """初始化问题模板"""
        self.question_templates = {
            RequirementType.TECH_DEV: {
                "功能定义": [
                    "这个系统的主要功能是什么？",
                    "需要支持哪些用户角色？",
                    "核心业务流程是怎样的？"
                ],
                "技术架构": [
                    "有什么技术栈偏好或限制？",
                    "需要支持多少并发用户？",
                    "对系统可用性有什么要求？"
                ],
                "用户体验": [
                    "需要在哪些设备上使用？",
                    "用户界面有什么特殊要求？",
                    "需要支持多语言吗？"
                ]
            },
            
            RequirementType.CONTENT_CREATION: {
                "创作目标": [
                    "这个内容的目的是什么？",
                    "希望传达什么核心信息？",
                    "想要观众有什么反应？"
                ],
                "内容要素": [
                    "需要包含哪些文字内容？",
                    "需要什么图片或视觉元素？",
                    "有什么颜色或设计风格偏好？"
                ],
                "分发渠道": [
                    "内容将在哪里使用？",
                    "需要适配哪些平台？",
                    "有什么版权或法律要求？"
                ]
            },
            
            RequirementType.DATA_ANALYSIS: {
                "分析目标": [
                    "想要分析什么业务问题？",
                    "最重要的分析指标是什么？",
                    "报表的主要使用者是谁？"
                ],
                "数据基础": [
                    "数据来源是什么？",
                    "数据质量如何？",
                    "数据量有多大？"
                ],
                "分析方法": [
                    "需要什么分析方法或模型？",
                    "期望的可视化效果是什么样的？",
                    "需要什么更新频率？"
                ]
            }
        }
    
    def _init_interview_strategies(self):
        """初始化访谈策略"""
        self.interview_strategies = {
            # (复杂度, 紧急程度) -> 策略名称
            (ComplexityLevel.SIMPLE, UrgencyLevel.NORMAL): "快速问答",
            (ComplexityLevel.SIMPLE, UrgencyLevel.EMERGENCY): "直接建议",
            (ComplexityLevel.MEDIUM, UrgencyLevel.NORMAL): "渐进引导",
            (ComplexityLevel.MEDIUM, UrgencyLevel.IMPORTANT): "重点聚焦",
            (ComplexityLevel.COMPLEX, UrgencyLevel.NORMAL): "分层深入",
            (ComplexityLevel.COMPLEX, UrgencyLevel.IMPORTANT): "优先级驱动",
            (ComplexityLevel.COMPLEX, UrgencyLevel.EMERGENCY): "紧急处理"
        }
    
    def classify_requirement(self, text: str, context: RequirementContext = None) -> RequirementClassification:
        """智能需求分类"""
        if context is None:
            context = RequirementContext()
        
        # 检测需求类型
        primary_type, matched_keywords = self._detect_primary_type(text)
        
        # 检测二级类型
        secondary_type = self._detect_secondary_type(text, primary_type)
        
        # 检测上下文信息
        detected_context = self._detect_context(text, context)
        
        # 计算置信度
        # 类型匹配度：基于关键词匹配数量
        keyword_count = len(matched_keywords)
        # 每个类型约有10-15个关键词
        total_possible = 12
        type_confidence = keyword_count / total_possible if total_possible > 0 else 0.5
        
        # 上下文置信度
        context_confidence = self._evaluate_context_confidence(detected_context)
        
        # 综合置信度
        total_confidence = type_confidence * 0.6 + context_confidence * 0.4
        
        return RequirementClassification(
            primary_type=primary_type,
            secondary_type=secondary_type,
            confidence=min(total_confidence, 1.0),
            matched_keywords=matched_keywords,
            context=detected_context
        )
    
    def _detect_primary_type(self, text: str) -> Tuple[RequirementType, List[str]]:
        """检测一级需求类型"""
        text_lower = text.lower()
        
        # 类型关键词映射
        type_keywords = {
            RequirementType.TECH_DEV: ["开发", "编写", "实现", "构建", "创建", "制作", "编程", "代码", "系统", "应用", "软件", "网站", "App"],
            RequirementType.CONTENT_CREATION: ["设计", "撰写", "创作", "制作", "文案", "内容", "写作", "海报", "传单", "广告", "文章", "视频", "图片", "PPT", "文档"],
            RequirementType.DATA_ANALYSIS: ["分析", "统计", "报表", "可视化", "挖掘", "预测", "建模", "数据", "图表", "指标", "趋势", "报告", "仪表盘", "大屏"],
            RequirementType.BUSINESS_PROCESS: ["流程", "工作流", "审批", "自动化", "集成", "对接", "同步", "业务", "操作", "步骤", "节点", "流转", "协调"],
            RequirementType.PROBLEM_SOLVING: ["解决", "修复", "优化", "排查", "调试", "处理", "问题", "故障", "错误", "Bug", "异常", "崩溃", "卡顿"],
            RequirementType.CONSULTING: ["咨询", "建议", "方案", "选型", "评估", "规划", "设计", "架构", "技术", "系统", "方案", "策略", "路线图"]
        }
        
        best_type = RequirementType.TECH_DEV  # 默认类型
        best_score = 0
        matched_keywords = []
        
        for req_type, keywords in type_keywords.items():
            matched = [kw for kw in keywords if kw in text_lower]
            score = len(matched)
            
            if score > best_score:
                best_score = score
                best_type = req_type
                matched_keywords = matched
        
        return best_type, matched_keywords
    
    def _detect_secondary_type(self, text: str, primary_type: RequirementType) -> str:
        """检测二级需求类型"""
        text_lower = text.lower()
        
        # 二级类型映射
        secondary_type_mapping = {
            RequirementType.TECH_DEV: {
                "Web应用开发": ["网页", "网站", "Web", "前端", "后端", "全栈", "浏览器", "在线"],
                "移动应用开发": ["App", "移动", "手机", "iOS", "Android", "小程序", "H5"],
                "桌面软件开发": ["桌面", "Windows", "macOS", "Linux", "客户端", "安装包"],
                "API接口开发": ["API", "接口", "服务", "REST", "GraphQL", "微服务"],
                "数据库设计": ["数据库", "表", "字段", "SQL", "NoSQL", "存储", "查询"]
            },
            
            RequirementType.CONTENT_CREATION: {
                "营销文案": ["营销", "促销", "广告", "推广", "宣传", "品牌", "销售"],
                "技术文档": ["文档", "说明", "手册", "指南", "教程", "API文档", "帮助"],
                "视觉设计": ["设计", "视觉", "UI", "UX", "界面", "图标", "配色", "布局"],
                "视频制作": ["视频", "剪辑", "制作", "动画", "特效", "配音", "字幕"],
                "演示文稿": ["PPT", "演示", "幻灯片", "汇报", "展示", "演讲"]
            }
        }
        
        if primary_type not in secondary_type_mapping:
            return f"{primary_type.value}通用"
        
        type_map = secondary_type_mapping[primary_type]
        best_type = f"{primary_type.value}通用"
        best_score = 0
        
        for subtype, keywords in type_map.items():
            matched = sum(1 for kw in keywords if kw in text_lower)
            if matched > best_score:
                best_score = matched
                best_type = subtype
        
        return best_type
    
    def _detect_context(self, text: str, base_context: RequirementContext) -> RequirementContext:
        """检测上下文信息"""
        text_lower = text.lower()
        
        # 检测行业
        industry_keywords = {
            "电商": ["商品", "订单", "支付", "购物车", "库存", "物流", "促销", "客户"],
            "教育": ["课程", "学生", "教师", "学习", "考试", "成绩", "教学", "培训"],
            "医疗": ["患者", "病历", "诊断", "药品", "预约", "医生", "医院", "健康"],
            "金融": ["账户", "交易", "支付", "风抖", "投资", "理财", "贷款", "保险"],
            "制造": ["生产", "设备", "质量", "工艺", "供应链", "库存", "工厂", "产品"]
        }
        
        detected_industry = "通用"
        for industry, keywords in industry_keywords.items():
            if any(kw in text_lower for kw in keywords):
                detected_industry = industry
                break
        
        # 检测紧急程度
        urgency_keywords = {
            UrgencyLevel.EMERGENCY: ["尽快", "马上", "立即", "今天", "现在", "紧急", "迫切", "急需"],
            UrgencyLevel.IMPORTANT: ["重要", "关键", "核心", "必须", "必要", "优先", "主要", "重点"],
            UrgencyLevel.NORMAL: ["常规", "普通", "一般", "日常", "计划内", "标准", "正常"],
            UrgencyLevel.OPTIMIZATION: ["优化", "改进", "提升", "增强", "完善", "美化", "优化"]
        }
        
        detected_urgency = UrgencyLevel.NORMAL
        for level, keywords in urgency_keywords.items():
            if any(kw in text_lower for kw in keywords):
                detected_urgency = level
                break
        
        # 评估复杂度
        word_count = len(text_lower.split())
        
        if word_count < 10:
            detected_complexity = ComplexityLevel.SIMPLE
        elif word_count < 30:
            detected_complexity = ComplexityLevel.MEDIUM
        else:
            detected_complexity = ComplexityLevel.COMPLEX
        
        # 合并上下文
        return RequirementContext(
            industry=detected_industry,
            urgency=detected_urgency,
            complexity=detected_complexity,
            user_history=base_context.user_history,
            constraints=base_context.constraints
        )
    
    def _evaluate_context_confidence(self, context: RequirementContext) -> float:
        """评估上下文置信度"""
        confidence_factors = []
        
        # 行业识别置信度

        if context.industry != "通用":
            confidence_factors.append(0.8)  # 识别到具体行业
        else:
            confidence_factors.append(0.3)  # 通用行业
        
        # 紧急程度识别置信度
        urgency_confidence = {
            UrgencyLevel.EMERGENCY: 0.9,
            UrgencyLevel.IMPORTANT: 0.7,
            UrgencyLevel.NORMAL: 0.5,
            UrgencyLevel.OPTIMIZATION: 0.6
        }
        confidence_factors.append(urgency_confidence.get(context.urgency, 0.5))
        
        # 复杂度评估置信度
        complexity_confidence = {
            ComplexityLevel.SIMPLE: 0.9,
            ComplexityLevel.MEDIUM: 0.7,
            ComplexityLevel.COMPLEX: 0.8
        }
        confidence_factors.append(complexity_confidence.get(context.complexity, 0.5))
        
        # 平均置信度
        return sum(confidence_factors) / len(confidence_factors)
    
    def find_similar_cases(self, classification: RequirementClassification, top_n: int = 3) -> List[CaseTemplate]:
        """查找相似案例"""
        if not self.case_library:
            return []
        
        # 计算相似度分数
        similarity_scores = []
        
        for case_id, case_template in self.case_library.items():
            # 类型相似度（主要考虑一级和二级类型）
            type_similarity = self._calculate_type_similarity(classification, case_template)
            
            # 行业相似度
            industry_similarity = 1.0 if classification.context.industry == case_template.industry else 0.3
            
            # 关键词相似度
            keyword_similarity = self._calculate_keyword_similarity(
                classification.matched_keywords,
                case_template
            )
            
            # 综合相似度
            total_similarity = (
                type_similarity * 0.5 +
                industry_similarity * 0.3 +
                keyword_similarity * 0.2
            )
            
            similarity_scores.append((total_similarity, case_template))
        
        # 按相似度排序，返回前N个
        similarity_scores.sort(key=lambda x: x[0], reverse=True)
        return [case for _, case in similarity_scores[:top_n]]
    
    def _calculate_type_similarity(self, classification: RequirementClassification, 
                                 case_template: CaseTemplate) -> float:
        """计算类型相似度"""
        # 一级类型相同
        if classification.primary_type == case_template.requirement_type:
            # 二级类型也相同或相似
            if classification.secondary_type == case_template.sub_type:
                return 1.0
            else:
                # 检查是否有部分匹配
                if any(keyword in classification.secondary_type 
                      for keyword in case_template.sub_type.split()):
                    return 0.8
                else:
                    return 0.6
        else:
            return 0.2
    
    def _calculate_keyword_similarity(self, matched_keywords: List[str], 
                                    case_template: CaseTemplate) -> float:
        """计算关键词相似度"""
        # 从案例模板中提取关键词
        case_keywords = set()
        
        # 从结构化需求中提取关键词
        for category, items in case_template.structured_requirements.items():
            for item in items:
                case_keywords.update(item.lower().split())
        
        # 计算匹配度
        if not case_keywords:
            return 0.5
        
        matched = sum(1 for kw in matched_keywords if kw in case_keywords)
        return matched / len(case_keywords)
    
    def generate_interview_plan(self, classification: RequirementClassification,
                              similar_cases: List[CaseTemplate]) -> Dict[str, Any]:
        """生成访谈计划"""
        # 确定访谈策略
        strategy = self._determine_interview_strategy(classification.context)
        
        # 选择维度
        selected_dimensions = self._select_dimensions(classification.primary_type)
        
        # 生成问题
        questions = self._generate_questions(classification, similar_cases, strategy)
        
        # 确定优先级
        priorities = self._determine_priorities(classification, similar_cases)
        
        return {
            "strategy": strategy,
            "dimensions": selected_dimensions,
            "questions": questions,
            "priorities": priorities,
            "estimated_time": self._estimate_interview_time(classification.context)
        }
    
    def _determine_interview_strategy(self, context: RequirementContext) -> str:
        """确定访谈策略"""
        key = (context.complexity, context.urgency)
        return self.interview_strategies.get(key, "渐进引导")
    
    def _select_dimensions(self, primary_type: RequirementType) -> List[str]:
        """选择维度"""
        if primary_type in self.dimension_sets:
            # 返回该类型所有维度的合并
            all_dimensions = []
            for dim_set in self.dimension_sets[primary_type]:
                all_dimensions.extend(dim_set.dimensions)
            return all_dimensions[:8]  # 限制维度数量
        
        return ["需求目标", "实施范围", "约束条件", "成功标准"]
    
    def _generate_questions(self, classification: RequirementClassification,
                          similar_cases: List[CaseTemplate], strategy: str) -> List[str]:
        """生成问题"""
        questions = []
        
        # 基础问题

        if classification.primary_type in self.question_templates:
            for category, question_list in self.question_templates[classification.primary_type].items():
                questions.extend(question_list[:2])  # 每个类别取前2个问题
        
        # 从相似案例中添加问题

        for case in similar_cases[:2]:
            questions.extend(case.interview_questions[:3])
        
        # 根据策略调整问题数量
        strategy_adjustments = {
            "快速问答": 5,
            "直接建议": 3,
            "渐进引导": 8,
            "重点聚焦": 6,
            "分层深入": 10,
            "优先级驱动": 7,
            "紧急处理": 4
        }
        
        max_questions = strategy_adjustments.get(strategy, 8)
        questions = list(dict.fromkeys(questions))  # 去重
        return questions[:max_questions]
    
    def _determine_priorities(self, classification: RequirementClassification,
                            similar_cases: List[CaseTemplate]) -> List[str]:
        """确定优先级"""
        priorities = []
        
        # 基于类型的一般优先级

        if classification.primary_type == RequirementType.TECH_DEV:
            priorities = ["核心功能", "技术架构", "用户体验", "性能安全"]
        elif classification.primary_type == RequirementType.CONTENT_CREATION:
            priorities = ["创作目标", "内容要素", "形式规格", "分发渠道"]
        elif classification.primary_type == RequirementType.DATA_ANALYSIS:
            priorities = ["分析目标", "数据基础", "分析方法", "结果应用"]
        else:
            priorities = ["需求目标", "实施范围", "约束条件", "成功标准"]
        
        return priorities
    
    def _estimate_interview_time(self, context: RequirementContext) -> int:
        """预估访谈时间（分钟）"""
        base_time = {
            (ComplexityLevel.SIMPLE, UrgencyLevel.NORMAL): 5,
            (ComplexityLevel.SIMPLE, UrgencyLevel.EMERGENCY): 3,
            (ComplexityLevel.MEDIUM, UrgencyLevel.NORMAL): 10,
            (ComplexityLevel.MEDIUM, UrgencyLevel.IMPORTANT): 8,
            (ComplexityLevel.COMPLEX, UrgencyLevel.NORMAL): 15,
            (ComplexityLevel.COMPLEX, UrgencyLevel.IMPORTANT): 12,
            (ComplexityLevel.COMPLEX, UrgencyLevel.EMERGENCY): 8
        }
        
        key = (context.complexity, context.urgency)
        return base_time.get(key, 10)
    
    def interpret_requirement(self, text: str, context: RequirementContext = None) -> Dict[str, Any]:
        """解读需求的完整流程"""
        # 步骤1: 智能分类
        classification = self.classify_requirement(text, context)
        
        # 步骤2: 查找相似案例
        similar_cases = self.find_similar_cases(classification)
        
        # 步骤3: 生成访谈计划
        interview_plan = self.generate_interview_plan(classification, similar_cases)
        
        # 步骤4: 提取最佳实践
        best_practices = self._extract_best_practices(similar_cases)
        
        # 步骤5: 生成建议
        suggestions = self._generate_suggestions(classification, similar_cases)
        
        # 步骤6: 提取思考维度
        dimensions = self._extract_dimensions(classification.primary_type)
        
        # 记录交互
        self._log_interaction(text, classification, interview_plan)
        
        # 返回综合结果
        return {
            "original_requirement": text,
            "classification": classification,
            "similar_cases": similar_cases,
            "interview_plan": interview_plan,
            "best_practices": best_practices,
            "suggestions": suggestions,
            "dimensions": dimensions,
            "confidence": classification.confidence
        }
    
    def _extract_dimensions(self, primary_type: RequirementType) -> List[str]:
        """提取基于需求类型的思考维度"""
        dimension_list = []
        
        # 从 dimension_sets 中提取维度
        if hasattr(self, 'dimension_sets') and primary_type in self.dimension_sets:
            for dim_set in self.dimension_sets[primary_type]:
                dimension_list.extend(dim_set.dimensions)
        else:
            # 默认维度
            dimension_list = ["需求目标", "实施范围", "约束条件", "成功标准"]
        
        return dimension_list
    
    def _extract_best_practices(self, similar_cases: List[CaseTemplate]) -> List[str]:
        """从相似案例中提取最佳实践"""
        practices = set()
        
        for case in similar_cases:
            practices.update(case.best_practices)
        
        return list(practices)[:5]  # 最多返回5个
    
    def _generate_suggestions(self, classification: RequirementClassification,
                            similar_cases: List[CaseTemplate]) -> List[str]:
        """生成建议"""
        suggestions = []
        
        # 基于类型的通用建议

        type_suggestions = {
            RequirementType.TECH_DEV: [
                "建议先明确技术栈和架构方案",
                "考虑系统的可扩展性和可维护性",
                "制定详细的测试计划和部署方案"
            ],
            RequirementType.CONTENT_CREATION: [
                "建议先明确目标受众和核心信息",
                "收集相关案例和设计灵感",
                "考虑多平台的适配性和一致性"
            ],
            RequirementType.DATA_ANALYSIS: [
                "建议先评估数据质量和可用性",
                "明确核心分析目标和关键指标",
                "设计清晰易懂的数据可视化方案"
            ]
        }
        
        suggestions.extend(type_suggestions.get(classification.primary_type, [
            "建议详细描述具体需求和期望效果",
            "明确约束条件和成功标准",
            "考虑实施的时间和资源限制"
        ]))
        
        # 从案例中提取建议

        for case in similar_cases[:2]:
            suggestions.extend(case.implementation_tips[:2])
        
        return list(dict.fromkeys(suggestions))[:5]  # 去重并限制数量
    
    def _log_interaction(self, text: str, classification: RequirementClassification,
                        interview_plan: Dict[str, Any]):
        """记录交互日志"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "requirement": text,
            "classification": {
                "primary_type": classification.primary_type.value,
                "secondary_type": classification.secondary_type,
                "confidence": classification.confidence
            },
            "context": {
                "industry": classification.context.industry,
                "urgency": classification.context.urgency.value,
                "complexity": classification.context.complexity.value
            },
            "interview_plan": interview_plan,
            "analysis_timestamp": classification.timestamp.isoformat()
        }
        
        self.interaction_log.append(interaction)
        
        # 保持日志大小

        if len(self.interaction_log) > 100:
            self.interaction_log = self.interaction_log[-100:]
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """获取学习洞察"""
        if not self.interaction_log:
            return {"status": "无交互数据"}
        
        # 分析交互数据

        total_interactions = len(self.interaction_log)
        
        # 类型分布

        type_distribution = {}
        for interaction in self.interaction_log:
            primary_type = interaction["classification"]["primary_type"]
            type_distribution[primary_type] = type_distribution.get(primary_type, 0) + 1
        
        # 行业分布

        industry_distribution = {}
        for interaction in self.interaction_log:
            industry = interaction["context"]["industry"]
            industry_distribution[industry] = industry_distribution.get(industry, 0) + 1
        
        # 紧急程度分布

        urgency_distribution = {}
        for interaction in self.interaction_log:
            urgency = interaction["context"]["urgency"]
            urgency_distribution[urgency] = urgency_distribution.get(urgency, 0) + 1
        
        return {
            "total_interactions": total_interactions,
            "type_distribution": type_distribution,
            "industry_distribution": industry_distribution,
            "urgency_distribution": urgency_distribution,
            "recent_interactions": self.interaction_log[-5:] if self.interaction_log else []
        }


# 测试函数
def test_optimized_interpreter():
    """测试优化后的解读器"""
    print("🧪 优化需求解读器测试")
    print("=" * 60)
    
    # 创建解读器
    script_dir = Path(__file__).parent
    case_library_path = script_dir / "case_library.json"
    interpreter = OptimizedRequirementInterpreter(str(case_library_path))
    
    # 测试用例

    test_cases = [
        "请为我设计一个蛋糕促销的海报",
        "开发一个在线商城系统",
        "分析上个月的销售数据并生成报表",
        "优化网站加载速度，现在太慢了",
        "咨询一下应该选择哪个前端框架"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 测试用例 {i}: {test_case}")
        print("-" * 40)
        
        # 解读需求

        result = interpreter.interpret_requirement(test_case)
        
        # 输出结果摘要

        print(f"📊 分类结果:")
        print(f"  一级类型: {result['classification'].primary_type.value}")
        print(f"  二级类型: {result['classification'].secondary_type}")
        print(f"  置信度: {result['confidence']:.1%}")
        print(f"  行业背景: {result['classification'].context.industry}")
        print(f"  紧急程度: {result['classification'].context.urgency.value}")
        print(f"  复杂度: {result['classification'].context.complexity.value}")
        
        print(f"\n🔍 相似案例:")
        for case in result['similar_cases']:
            print(f"  - {case.title} ({case.sub_type})")
        
        print(f"\n❓ 访谈计划:")
        print(f"  策略: {result['interview_plan']['strategy']}")
        print(f"  预估时间: {result['interview_plan']['estimated_time']}分钟")
        print(f"  问题数量: {len(result['interview_plan']['questions'])}个")
        
        print(f"\n💡 最佳实践:")
        for practice in result['best_practices'][:3]:
            print(f"  - {practice}")
        
        print(f"\n✅ 建议:")
        for suggestion in result['suggestions'][:3]:
            print(f"  - {suggestion}")
    
    # 获取学习洞察

    print("\n" + "=" * 60)
    print("📈 学习洞察:")
    insights = interpreter.get_learning_insights()
    
    print(f"总交互次数: {insights['total_interactions']}")
    print(f"类型分布:")
    for req_type, count in insights.get('type_distribution', {}).items():
        print(f"  {req_type}: {count}次")
    
    print(f"行业分布:")
    for industry, count in insights.get('industry_distribution', {}).items():
        print(f"  {industry}: {count}次")
    
    print("\n✅ 测试完成")


if __name__ == "__main__":
    test_optimized_interpreter()