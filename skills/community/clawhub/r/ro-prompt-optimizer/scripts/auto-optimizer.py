#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RO提示词自动优化器
基于R-O框架（角色&现实情况、对象&输出）自动优化用户提示词
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class TaskType(Enum):
    """任务类型枚举"""
    CREATIVE = "creative"      # 创意类：文案、设计、故事
    ANALYTICAL = "analytical"  # 分析类：数据、研究、诊断
    EXECUTION = "execution"    # 执行类：计划、流程、实施
    DECISION = "decision"      # 决策类：选择、评估、策略
    COMMUNICATION = "communication"  # 沟通类：报告、演讲、材料

class IndustryType(Enum):
    """行业类型枚举"""
    ECOMMERCE = "ecommerce"    # 电商
    MARKETING = "marketing"    # 市场营销
    TECHNOLOGY = "technology"  # 技术开发
    SERVICE = "service"        # 服务行业
    EDUCATION = "education"    # 教育
    FINANCE = "finance"        # 金融
    HEALTHCARE = "healthcare"  # 医疗健康
    GENERAL = "general"        # 通用

@dataclass
class ROOptimization:
    """R-O优化结果数据结构"""
    # 原始需求
    original_request: str
    
    # 分析结果
    task_type: TaskType
    industry_type: IndustryType
    complexity_level: str  # simple, medium, complex
    
    # R-O四个维度
    role_definition: Dict[str, str]  # 角色设定
    reality_context: Dict[str, str]  # 现实情况
    object_audience: Dict[str, str]  # 输出对象
    output_requirements: Dict[str, str]  # 输出要求
    
    # 优化后的提示词
    optimized_prompt: str
    
    # 优化说明
    optimization_notes: List[str]

class ROOptimizer:
    """R-O提示词优化器"""
    
    def __init__(self):
        self.task_keywords = {
            TaskType.CREATIVE: [
                "写", "创作", "设计", "策划", "创意", "文案", "故事",
                "广告", "品牌", "视觉", "艺术", "构思", "想象"
            ],
            TaskType.ANALYTICAL: [
                "分析", "研究", "统计", "数据", "诊断", "评估", "调研",
                "报告", "趋势", "洞察", "归因", "对比", "监测"
            ],
            TaskType.EXECUTION: [
                "执行", "实施", "计划", "安排", "组织", "管理", "推进",
                "完成", "开展", "落实", "操作", "步骤", "流程"
            ],
            TaskType.DECISION: [
                "决定", "选择", "决策", "判断", "评估", "取舍", "方案",
                "策略", "方向", "路线", "投资", "配置", "优化"
            ],
            TaskType.COMMUNICATION: [
                "沟通", "汇报", "演讲", "表达", "说明", "解释", "介绍",
                "讲述", "传达", "展示", "呈现", "分享", "交流"
            ]
        }
        
        self.industry_keywords = {
            IndustryType.ECOMMERCE: [
                "电商", "淘宝", "天猫", "京东", "拼多多", "店铺", "商品",
                "运营", "销售", "客服", "物流", "供应链", "促销"
            ],
            IndustryType.MARKETING: [
                "营销", "市场", "广告", "推广", "品牌", "公关", "传播",
                "促销", "活动", "策划", "渠道", "客户", "消费者"
            ],
            IndustryType.TECHNOLOGY: [
                "技术", "开发", "编程", "软件", "系统", "架构", "代码",
                "算法", "数据", "分析", "产品", "设计", "测试"
            ],
            IndustryType.SERVICE: [
                "服务", "咨询", "培训", "教育", "医疗", "法律", "金融",
                "客服", "支持", "顾问", "指导", "帮助", "解决方案"
            ]
        }
    
    def analyze_request(self, request: str) -> Tuple[TaskType, IndustryType, str]:
        """分析用户请求，识别任务类型、行业和复杂度"""
        # 转换为小写便于匹配
        request_lower = request.lower()
        
        # 识别任务类型
        task_type = TaskType.GENERAL
        max_matches = 0
        for ttype, keywords in self.task_keywords.items():
            matches = sum(1 for kw in keywords if kw in request_lower)
            if matches > max_matches:
                max_matches = matches
                task_type = ttype
        
        # 识别行业类型
        industry_type = IndustryType.GENERAL
        max_matches = 0
        for itype, keywords in self.industry_keywords.items():
            matches = sum(1 for kw in keywords if kw in request_lower)
            if matches > max_matches:
                max_matches = matches
                industry_type = itype
        
        # 评估复杂度
        complexity = "simple"
        words_count = len(request.split())
        if words_count > 50:
            complexity = "complex"
        elif words_count > 20:
            complexity = "medium"
        
        return task_type, industry_type, complexity
    
    def generate_role_definition(self, task_type: TaskType, industry_type: IndustryType) -> Dict[str, str]:
        """生成角色定义"""
        role_templates = {
            TaskType.CREATIVE: {
                "title": "创意专家",
                "expertise": "创新思维、审美判断、情感共鸣、市场感知",
                "experience": "多个成功创意项目经验，擅长将想法转化为可执行的创意方案",
                "skills": "文案创作、视觉设计、故事叙述、品牌策划"
            },
            TaskType.ANALYTICAL: {
                "title": "数据分析师",
                "expertise": "逻辑思维、数据处理、归因分析、商业洞察",
                "experience": "多年数据分析经验，擅长从复杂数据中提取有价值的信息",
                "skills": "统计分析、数据可视化、问题诊断、决策支持"
            },
            TaskType.EXECUTION: {
                "title": "项目管理专家",
                "expertise": "计划制定、资源协调、进度控制、风险管理",
                "experience": "成功管理多个复杂项目，确保项目按时按质完成",
                "skills": "项目管理、团队协作、流程优化、问题解决"
            }
        }
        
        # 基础角色定义
        base_role = role_templates.get(task_type, {
            "title": "专业顾问",
            "expertise": "问题解决、策略制定、方案实施",
            "experience": "多年相关领域经验，擅长处理复杂问题",
            "skills": "分析思考、沟通协调、执行能力"
        })
        
        # 根据行业调整
        industry_adjustments = {
            IndustryType.ECOMMERCE: {
                "industry_specific": "电商平台运营、消费者行为分析、店铺优化",
                "context": "熟悉淘宝/天猫等电商平台规则和运营策略"
            },
            IndustryType.MARKETING: {
                "industry_specific": "市场营销策略、品牌传播、数字营销",
                "context": "精通整合营销传播和ROI优化"
            },
            IndustryType.TECHNOLOGY: {
                "industry_specific": "技术架构设计、软件开发、系统优化",
                "context": "熟悉敏捷开发和DevOps实践"
            }
        }
        
        adjustment = industry_adjustments.get(industry_type, {})
        
        return {
            "title": base_role["title"],
            "expertise": f"{base_role['expertise']}" + (f"，{adjustment.get('industry_specific', '')}" if adjustment else ""),
            "experience": base_role["experience"],
            "skills": base_role["skills"],
            "context": adjustment.get("context", "具备多领域知识和实践经验")
        }
    
    def generate_reality_context(self, request: str, complexity: str) -> Dict[str, str]:
        """生成现实情况设定"""
        # 提取可能的时间信息
        time_patterns = [
            r'(\d+)[个]?月', r'(\d+)[个]?周', r'(\d+)[天日]', 
            r'季度', r'年度', r'近期', r'马上', r'立即'
        ]
        
        time_constraint = "没有明确时间限制"
        for pattern in time_patterns:
            match = re.search(pattern, request)
            if match:
                time_constraint = f"需要在{match.group(0)}内完成"
                break
        
        # 根据复杂度设定资源约束
        resource_constraints = {
            "simple": "资源充足，没有特殊限制",
            "medium": "有一定资源限制，需要合理分配",
            "complex": "资源紧张，需要高效利用和优化"
        }
        
        return {
            "time_constraint": time_constraint,
            "resource_constraint": resource_constraints.get(complexity, "资源充足"),
            "environment": "当前业务环境正常，没有特殊外部干扰",
            "limitations": "需要基于现有条件和约束进行工作"
        }
    
    def generate_object_audience(self, task_type: TaskType) -> Dict[str, str]:
        """生成输出对象分析"""
        audience_templates = {
            TaskType.CREATIVE: {
                "identity": "目标受众或最终用户",
                "knowledge_level": "具备基础理解能力，偏好直观易懂的表达",
                "preference": "注重情感共鸣和视觉体验，讨厌枯燥的理论",
                "usage_scenario": "日常消费或信息获取场景"
            },
            TaskType.ANALYTICAL: {
                "identity": "业务决策者或相关专业人员",
                "knowledge_level": "有一定专业基础，需要深度解读",
                "preference": "重视数据支撑和逻辑严密，偏好清晰结论",
                "usage_scenario": "决策支持或问题分析场景"
            },
            TaskType.EXECUTION: {
                "identity": "执行团队或项目相关人员",
                "knowledge_level": "了解基础操作，需要具体指导",
                "preference": "注重步骤清晰和可操作性，讨厌模糊描述",
                "usage_scenario": "项目实施或日常操作场景"
            }
        }
        
        template = audience_templates.get(task_type, {
            "identity": "相关利益方",
            "knowledge_level": "具备基本理解能力",
            "preference": "注重实用性和可理解性",
            "usage_scenario": "常规工作场景"
        })
        
        return template
    
    def generate_output_requirements(self, task_type: TaskType, complexity: str) -> Dict[str, str]:
        """生成输出要求"""
        requirement_templates = {
            TaskType.CREATIVE: {
                "content_structure": "创意概念+核心信息+表现形式",
                "format": "文字描述+视觉参考+实施建议",
                "quality_standard": "创新性、相关性、感染力、可行性",
                "goal": "激发兴趣、传递信息、促成行动"
            },
            TaskType.ANALYTICAL: {
                "content_structure": "问题定义+分析方法+关键发现+建议",
                "format": "结构化报告+数据图表+简明摘要",
                "quality_standard": "准确性、完整性、洞察力、实用性",
                "goal": "提供洞察、支持决策、指导行动"
            },
            TaskType.EXECUTION: {
                "content_structure": "目标+计划+资源+时间+风险",
                "format": "详细方案+进度表+责任矩阵",
                "quality_standard": "清晰性、可行性、可控性、有效性",
                "goal": "指导执行、控制进度、确保结果"
            }
        }
        
        template = requirement_templates.get(task_type, {
            "content_structure": "引言+主体+结论",
            "format": "结构化文档",
            "quality_standard": "清晰、准确、实用",
            "goal": "有效传达信息并达成目标"
        })
        
        # 根据复杂度调整
        if complexity == "complex":
            template["content_structure"] = f"详细的问题分析+多层次解决方案+风险评估+实施路径"
            template["quality_standard"] = f"{template['quality_standard']}+深度+创新性+系统性"
        
        return template
    
    def generate_optimized_prompt(self, optimization: ROOptimization) -> str:
        """生成优化后的提示词"""
        prompt = f"""# R-O优化提示词

## 原始需求
{optimization.original_request}

## 角色&现实情况 (Role & Reality)

### 角色设定
您是{optimization.role_definition['title']}，{optimization.role_definition['context']}。
- **专业专长**：{optimization.role_definition['expertise']}
- **经验背景**：{optimization.role_definition['experience']}
- **核心技能**：{optimization.role_definition['skills']}

### 现实情况
- **时间约束**：{optimization.reality_context['time_constraint']}
- **资源条件**：{optimization.reality_context['resource_constraint']}
- **环境因素**：{optimization.reality_context['environment']}
- **限制条件**：{optimization.reality_context['limitations']}

## 对象&输出 (Object & Output)

### 输出对象
- **身份特征**：{optimization.object_audience['identity']}
- **知识水平**：{optimization.object_audience['knowledge_level']}
- **偏好特点**：{optimization.object_audience['preference']}
- **使用场景**：{optimization.object_audience['usage_scenario']}

### 输出要求
1. **内容结构**：{optimization.output_requirements['content_structure']}
2. **格式规范**：{optimization.output_requirements['format']}
3. **质量标准**：{optimization.output_requirements['quality_standard']}
4. **核心目标**：{optimization.output_requirements['goal']}

## 特别说明
- 请基于以上R-O框架进行思考和回应
- 确保输出符合所有维度的要求
- 如有不确定的地方，请先澄清再继续"""
        
        return prompt
    
    def optimize(self, request: str) -> ROOptimization:
        """执行完整的R-O优化"""
        # 分析请求
        task_type, industry_type, complexity = self.analyze_request(request)
        
        # 生成四个维度
        role_definition = self.generate_role_definition(task_type, industry_type)
        reality_context = self.generate_reality_context(request, complexity)
        object_audience = self.generate_object_audience(task_type)
        output_requirements = self.generate_output_requirements(task_type, complexity)
        
        # 创建优化对象
        optimization = ROOptimization(
            original_request=request,
            task_type=task_type,
            industry_type=industry_type,
            complexity_level=complexity,
            role_definition=role_definition,
            reality_context=reality_context,
            object_audience=object_audience,
            output_requirements=output_requirements,
            optimized_prompt="",  # 稍后生成
            optimization_notes=[
                f"任务类型：{task_type.value}",
                f"行业类型：{industry_type.value}",
                f"复杂度：{complexity}",
                f"已应用R-O框架进行系统化优化"
            ]
        )
        
        # 生成优化后的提示词
        optimization.optimized_prompt = self.generate_optimized_prompt(optimization)
        
        return optimization
    
    def format_output(self, optimization: ROOptimization, format_type: str = "markdown") -> str:
        """格式化输出结果"""
        if format_type == "markdown":
            output = f"""# R-O提示词优化结果

## 分析摘要
- **原始需求**：{optimization.original_request}
- **任务类型**：{optimization.task_type.value}
- **行业类型**：{optimization.industry_type.value}
- **复杂度**：{optimization.complexity_level}

## 优化说明
{chr(10).join(f"- {note}" for note in optimization.optimization_notes)}

## 优化后的提示词
{optimization.optimized_prompt}

## 优化要点总结
1. **角色设定**：明确了AI的专业身份和能力范围
2. **现实约束**：设定了具体的工作条件和限制
3. **对象分析**：识别了输出内容的受众特征
4. **输出规范**：制定了具体的质量和格式要求

## 使用建议
1. 将优化后的提示词直接用于AI交互
2. 根据实际反馈微调各个维度
3. 复杂任务可分阶段应用R-O框架
4. 定期回顾和优化常用提示词"""
            
            return output
        
        elif format_type == "json":
            return json.dumps(asdict(optimization), ensure_ascii=False, indent=2)
        
        else:
            return optimization.optimized_prompt

def main():
    """主函数：命令行交互界面"""
    print("=" * 60)
    print("R-O提示词自动优化器")
    print("=" * 60)
    
    optimizer = ROOptimizer()
    
    while True:
        print("\n请输入您需要优化的提示词（输入'quit'退出）：")
        user_input = input("> ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("感谢使用，再见！")
            break
        
        if not user_input:
            print("请输入有效内容")
            continue
        
        print("\n🔄 正在分析并优化您的提示词...")
        
        try:
            # 执行优化
            result = optimizer.optimize(user_input)
            
            # 输出结果
            print("\n✅ 优化完成！")
            print("=" * 60)
            
            formatted_output = optimizer.format_output(result, "markdown")
            print(formatted_output)
            
            # 保存选项
            print("\n" + "=" * 60)
            print("📁 保存选项：")
            print("1. 保存为Markdown文件")
            print("2. 保存为JSON文件")
            print("3. 复制到剪贴板")
            print("4. 继续优化下一个")
            
            choice = input("请选择 (1-4): ").strip()
            
            if choice == "1":
                filename = f"ro_optimized_{hash(user_input) % 10000}.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(formatted_output)
                print(f"✅ 已保存为: {filename}")
            elif choice == "2":
                filename = f"ro_optimized_{hash(user_input) % 10000}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(optimizer.format_output(result, "json"))
                print(f"✅ 已保存为: {filename}")
            elif choice == "3":
                # 复制到剪贴板（需要pyperclip库）
                try:
                    import pyperclip
                    pyperclip.copy(result.optimized_prompt)
                    print("✅ 已复制优化后的提示词到剪贴板")
                except ImportError:
                    print("⚠️  需要安装pyperclip库才能使用剪贴板功能")
            
            print("\n" + "=" * 60)
            
        except Exception as e:
            print(f"❌ 优化过程中出现错误: {e}")
            print("请重试或简化您的输入")

if __name__ == "__main__":
    main()