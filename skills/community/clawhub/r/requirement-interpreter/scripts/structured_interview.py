#!/usr/bin/env python3
"""
结构化访谈脚本 - 帮助用户详细描述需求
"""

import json
from typing import List, Dict, Any

class StructuredInterview:
    """结构化访谈框架"""
    
    def __init__(self):
        self.interview_frameworks = {
            "技术开发": self.technical_development_framework,
            "数据分析": self.data_analysis_framework,
            "业务流程": self.business_process_framework,
            "内容创作": self.content_creation_framework,
            "问题解决": self.problem_solving_framework
        }
        
        self.question_bank = {
            "scope_definition": [
                "这个需求的主要目标是什么？",
                "你希望解决什么具体问题？",
                "这个需求的预期成果是什么？",
                "有没有相关的成功案例或参考？"
            ],
            "functional_requirements": [
                "需要哪些具体功能？",
                "用户如何与系统交互？",
                "需要处理哪些数据？",
                "需要生成什么输出？"
            ],
            "technical_constraints": [
                "有没有技术栈限制？",
                "需要集成哪些现有系统？",
                "性能要求是什么？",
                "安全要求有哪些？"
            ],
            "user_experience": [
                "目标用户是谁？",
                "用户的使用场景是什么？",
                "界面有什么特殊要求？",
                "需要支持哪些设备或平台？"
            ],
            "success_criteria": [
                "如何判断需求是否成功实现？",
                "有没有具体的验收标准？",
                "需要什么测试验证？",
                "如何衡量效果？"
            ]
        }
    
    def technical_development_framework(self, initial_request: str) -> Dict[str, Any]:
        """技术开发需求访谈框架"""
        return {
            "需求类别": "技术开发",
            "初始需求": initial_request,
            "访谈问题": {
                "架构设计": [
                    "需要什么类型的应用（Web、移动端、桌面端）？",
                    "需要什么技术栈或框架？",
                    "架构有什么特殊要求？",
                    "需要什么数据库？"
                ],
                "功能模块": [
                    "需要哪些具体功能模块？",
                    "模块之间如何交互？",
                    "需要什么API接口？",
                    "需要什么用户权限系统？"
                ],
                "数据模型": [
                    "需要存储哪些数据？",
                    "数据之间的关系是什么？",
                    "需要什么数据验证规则？",
                    "需要什么数据迁移策略？"
                ],
                "部署运维": [
                    "需要部署到什么环境？",
                    "需要什么监控和日志？",
                    "需要什么备份策略？",
                    "有什么运维要求？"
                ]
            }
        }
    
    def data_analysis_framework(self, initial_request: str) -> Dict[str, Any]:
        """数据分析需求访谈框架"""
        return {
            "需求类别": "数据分析",
            "初始需求": initial_request,
            "访谈问题": {
                "数据源": [
                    "数据来源是什么？",
                    "数据格式是什么？",
                    "数据量有多大？",
                    "数据质量如何？"
                ],
                "分析目标": [
                    "想要发现什么模式？",
                    "需要回答什么问题？",
                    "需要什么可视化？",
                    "需要什么统计指标？"
                ],
                "处理方法": [
                    "需要什么数据清洗？",
                    "需要什么数据转换？",
                    "需要什么算法或模型？",
                    "需要什么计算资源？"
                ],
                "输出要求": [
                    "需要什么报告格式？",
                    "需要什么图表类型？",
                    "需要什么数据导出？",
                    "需要什么自动化？"
                ]
            }
        }
    
    def business_process_framework(self, initial_request: str) -> Dict[str, Any]:
        """业务流程需求访谈框架"""
        return {
            "需求类别": "业务流程",
            "初始需求": initial_request,
            "访谈问题": {
                "流程概述": [
                    "当前流程是什么？",
                    "流程中的痛点是什么？",
                    "想要优化的环节是什么？",
                    "涉及哪些部门和角色？"
                ],
                "流程步骤": [
                    "流程的起点和终点是什么？",
                    "有哪些关键决策点？",
                    "需要什么审批流程？",
                    "需要什么通知机制？"
                ],
                "数据流转": [
                    "流程中传递什么信息？",
                    "需要什么表单或文档？",
                    "需要什么数据验证？",
                    "需要什么存档要求？"
                ],
                "自动化需求": [
                    "哪些环节可以自动化？",
                    "需要什么集成接口？",
                    "需要什么异常处理？",
                    "需要什么监控报警？"
                ]
            }
        }
    
    def content_creation_framework(self, initial_request: str) -> Dict[str, Any]:
        """内容创作需求访谈框架"""
        return {
            "需求类别": "内容创作",
            "初始需求": initial_request,
            "访谈问题": {
                "创作目标": [
                    "这个内容的目的是什么？",
                    "想要传达什么核心信息？",
                    "希望观众有什么反应？",
                    "有没有参考案例或风格？"
                ],
                "内容要素": [
                    "需要包含哪些文字内容？",
                    "需要什么图片或视觉元素？",
                    "需要什么颜色或设计风格？",
                    "需要什么品牌元素（Logo、口号等）？"
                ],
                "受众定位": [
                    "目标受众是谁？",
                    "受众有什么特点或偏好？",
                    "在什么场景下使用这个内容？",
                    "如何吸引受众的注意力？"
                ],
                "格式要求": [
                    "需要的尺寸或比例是多少？",
                    "需要什么文件格式？",
                    "需要什么分辨率或质量？",
                    "有什么特殊技术要求？"
                ],
                "分发渠道": [
                    "内容将在哪里使用？",
                    "需要适配哪些平台或设备？",
                    "有什么版权或法律要求？",
                    "是否需要多语言版本？"
                ]
            }
        }
    
    def problem_solving_framework(self, initial_request: str) -> Dict[str, Any]:
        """问题解决需求访谈框架"""
        return {
            "需求类别": "问题解决",
            "初始需求": initial_request,
            "访谈问题": {
                "问题分析": [
                    "遇到了什么具体问题？",
                    "问题出现的频率如何？",
                    "问题的影响范围有多大？",
                    "已经尝试过哪些解决方案？"
                ],
                "问题原因": [
                    "可能的原因有哪些？",
                    "根本原因是什么？",
                    "有哪些相关因素？",
                    "有什么数据或证据？"
                ],
                "解决目标": [
                    "希望达到什么解决效果？",
                    "有什么具体的解决标准？",
                    "时间要求是什么？",
                    "资源限制有哪些？"
                ],
                "解决方案": [
                    "建议的解决方案是什么？",
                    "方案的可行性如何？",
                    "实施步骤有哪些？",
                    "可能的风险和应对措施？"
                ]
            }
        }
    
    def conduct_interview(self, initial_request: str, category: str = None) -> Dict[str, Any]:
        """执行结构化访谈"""
        if category and category in self.interview_frameworks:
            framework = self.interview_frameworks[category]
        else:
            # 自动识别类别
            category = self.detect_category(initial_request)
            framework = self.interview_frameworks.get(category, self.technical_development_framework)
        
        return framework(initial_request)
    
    def detect_category(self, request: str) -> str:
        """自动识别需求类别"""
        request_lower = request.lower()
        
        keywords = {
            "技术开发": ["开发", "编程", "代码", "应用", "系统", "网站", "app", "软件"],
            "数据分析": ["分析", "数据", "统计", "报表", "图表", "可视化", "挖掘"],
            "业务流程": ["流程", "业务", "工作流", "审批", "自动化", "管理"],
            "内容创作": ["内容", "写作", "创作", "文案", "设计", "图片", "视频"],
            "问题解决": ["问题", "解决", "故障", "错误", "修复", "优化"]
        }
        
        for category, words in keywords.items():
            if any(word in request_lower for word in words):
                return category
        
        return "技术开发"  # 默认类别
    
    def generate_structured_requirements(self, interview_data: Dict[str, Any], answers: Dict[str, str]) -> str:
        """生成结构化需求文档"""
        requirements = []
        requirements.append(f"# 需求文档：{interview_data['需求类别']}")
        requirements.append(f"## 初始需求\n{interview_data['初始需求']}\n")
        
        for section, questions in interview_data["访谈问题"].items():
            requirements.append(f"## {section}")
            for i, question in enumerate(questions, 1):
                answer_key = f"{section}_{i}"
                answer = answers.get(answer_key, "待确认")
                requirements.append(f"### {question}")
                requirements.append(f"{answer}\n")
        
        return "\n".join(requirements)

if __name__ == "__main__":
    # 示例使用
    interview = StructuredInterview()
    
    # 示例需求
    user_request = "帮我做一个用户管理系统"
    
    # 执行访谈
    interview_data = interview.conduct_interview(user_request)
    print("访谈框架生成完成")
    print(f"需求类别: {interview_data['需求类别']}")
    print(f"访谈问题数量: {sum(len(q) for q in interview_data['访谈问题'].values())}")
    
    # 保存访谈框架
    with open("interview_framework.json", "w", encoding="utf-8") as f:
        json.dump(interview_data, f, ensure_ascii=False, indent=2)
    print("访谈框架已保存到 interview_framework.json")