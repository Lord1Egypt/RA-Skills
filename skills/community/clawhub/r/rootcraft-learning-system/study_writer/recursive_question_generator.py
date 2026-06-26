#!/usr/bin/env python3
"""
RootCraft Learning System - 递归追问生成器 v1.1.5
根据学习主题生成针对性的问题链
"""
import json
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class QuestionChain:
    """问题链"""
    question: str
    answer: str
    deeper_question: Optional[str] = None
    depth: int = 0


class RecursiveQuestionGenerator:
    """递归追问生成器 - 根据主题生成真实问题链"""
    
    def __init__(self):
        self.common_patterns = self._load_common_patterns()
    
    def _load_common_patterns(self) -> Dict:
        """加载常见追问模式"""
        return {
            # 基础 "为什么" 链
            "why_essential": [
                ("这个问题最根本的原因是什么？", "找到最基础的原理"),
                ("还有比这个更基础的原因吗？", "追溯到不可分割的前提"),
                ("如果这个不成立，会发生什么？", "验证假设的必要性"),
            ],
            # 定义追问
            "definition": [
                ("你能用一句话定义这个概念吗？", "确认核心定义"),
                ("这个定义中每个词确切的含义是什么？", "拆解定义要素"),
                ("有没有例外情况？", "检验边界条件"),
            ],
            # 原理追问
            "principle": [
                ("这个原理为什么有效？", "理解有效性来源"),
                ("它的前提假设是什么？", "明确适用范围"),
                ("如果前提不满足会怎样？", "理解局限性"),
            ],
            # 历史追问
            "history": [
                ("这个理论是怎么发展来的？", "理解演进过程"),
                ("关键突破是什么？", "找到核心贡献"),
                ("现在和最初有什么不同？", "理解演变"),
            ],
            # 实践追问
            "practice": [
                ("这个怎么用在实际中？", "连接实践"),
                ("常见错误有哪些？", "避免陷阱"),
                ("什么时候不适用？", "理解边界"),
            ]
        }
    
    def generate_for_topic(self, topic: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        为指定主题生成递归追问内容
        
        Args:
            topic: 学习主题
            context: 额外上下文（如核心概念列表等）
        
        Returns:
            包含问题链的字典
        """
        # 首先分析主题类型
        topic_analysis = self._analyze_topic(topic)
        
        # 生成通用追问链
        general_chains = self._generate_general_chains(topic, topic_analysis)
        
        # 生成概念特异性问题
        concept_chains = self._generate_concept_chains(topic, topic_analysis, context)
        
        # 生成领域特定问题
        domain_chains = self._generate_domain_chains(topic, topic_analysis)
        
        # 生成"连续追问"示例
        continuous_example = self._generate_continuous_example(topic, topic_analysis)
        
        return {
            "topic": topic,
            "analysis": topic_analysis,
            "general_chains": general_chains,
            "concept_chains": concept_chains,
            "domain_chains": domain_chains,
            "continuous_example": continuous_example,
            "format": "markdown"
        }
    
    def _analyze_topic(self, topic: str) -> Dict[str, Any]:
        """分析主题特征"""
        topic_lower = topic.lower()
        
        analysis = {
            "domain": "general",
            "has_theory": False,
            "has_practice": False,
            "has_math": False,
            "has_history": False,
            "keywords": []
        }
        
        # 领域识别
        domain_keywords = {
            "programming": ["编程", "代码", "程序", "python", "java", "开发", "算法"],
            "science": ["物理", "化学", "生物", "科学", "数学"],
            "ai": ["人工智能", "机器学习", "深度学习", "神经网络", "AI", "ML"],
            "investment": ["投资", "理财", "金融", "股票", "基金"],
            "design": ["设计", "UI", "UX", "美术", "插画"],
            "music": ["音乐", "作曲", "编曲", "Suno", "音频"],
            "literature": ["小说", "文学", "写作", "创作"],
            "philosophy": ["哲学", "思考", "认知", "思维"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(kw in topic_lower for kw in keywords):
                analysis["domain"] = domain
                analysis["keywords"] = keywords
                break
        
        # 特征识别
        if any(w in topic_lower for w in ["原理", "理论", "概念", "机制", "method", "technique"]):
            analysis["has_theory"] = True
        
        if any(w in topic_lower for w in ["实践", "应用", "实现", "代码", "项目", "实战"]):
            analysis["has_practice"] = True
        
        if any(w in topic_lower for w in ["数学", "公式", "证明", "推导", "计算"]):
            analysis["has_math"] = True
        
        if any(w in topic_lower for w in ["历史", "发展", "起源", "演变", "演进"]):
            analysis["has_history"] = True
        
        return analysis
    
    def _generate_general_chains(self, topic: str, analysis: Dict) -> List[Dict]:
        """生成通用问题链"""
        chains = []
        
        # 基础三问（适合任何主题）
        chains.append({
            "title": "基础三问",
            "questions": [
                {
                    "q": f"为什么学习 {topic}？",
                    "a": "【回答要点】：解决什么问题？带来什么价值？",
                    "depth": 1
                },
                {
                    "q": f"{topic} 的本质是什么？",
                    "a": "【回答要点】：最核心的定义，一句话说清楚",
                    "depth": 2
                },
                {
                    "q": f"不学 {topic} 会怎样？",
                    "a": "【回答要点】：缺失这个知识的后果",
                    "depth": 3
                }
            ]
        })
        
        # 如果有理论内容，添加原理追问
        if analysis["has_theory"]:
            chains.append({
                "title": "原理深挖",
                "questions": [
                    {
                        "q": f"{topic} 为什么有效？",
                        "a": "【回答要点】：背后的核心机制",
                        "depth": 1
                    },
                    {
                        "q": "它的前提假设是什么？",
                        "a": "【回答要点】：适用范围和条件",
                        "depth": 2
                    },
                    {
                        "q": "假设不成立时会怎样？",
                        "a": "【回答要点】：边界情况和局限性",
                        "depth": 3
                    }
                ]
            })
        
        return chains
    
    def _generate_concept_chains(self, topic: str, analysis: Dict, 
                                  context: Optional[Dict] = None) -> List[Dict]:
        """生成概念特异性问题"""
        chains = []
        
        # 基于领域生成特定概念问题
        if analysis["domain"] == "programming":
            chains.extend(self._programming_chains(topic))
        elif analysis["domain"] == "ai":
            chains.extend(self._ai_chains(topic))
        elif analysis["domain"] == "investment":
            chains.extend(self._investment_chains(topic))
        elif analysis["domain"] == "science":
            chains.extend(self._science_chains(topic))
        else:
            # 默认生成
            chains.append({
                "title": "概念澄清",
                "questions": [
                    {
                        "q": f"什么是 {topic}？",
                        "a": "【请用自己的话回答】",
                        "depth": 1
                    },
                    {
                        "q": f"{topic} 和 X 有什么区别？",
                        "a": "【对比分析】",
                        "depth": 2
                    }
                ]
            })
        
        return chains
    
    def _programming_chains(self, topic: str) -> List[Dict]:
        """编程领域的问题链"""
        return [
            {
                "title": "技术原理",
                "questions": [
                    {
                        "q": f"{topic} 的工作原理是什么？",
                        "a": "【回答要点】：核心机制、执行流程",
                        "depth": 1
                    },
                    {
                        "q": "它和其他类似技术比有什么优缺点？",
                        "a": "【回答要点】：对比分析",
                        "depth": 2
                    },
                    {
                        "q": "在什么场景下应该用它？什么时候不应该用？",
                        "a": "【回答要点】：选型依据",
                        "depth": 3
                    }
                ]
            },
            {
                "title": "实践要点",
                "questions": [
                    {
                        "q": "这个技术常见的错误用法有哪些？",
                        "a": "【回答要点】：避坑指南",
                        "depth": 1
                    },
                    {
                        "q": "如何调试和排查问题？",
                        "a": "【回答要点】：调试方法",
                        "depth": 2
                    }
                ]
            }
        ]
    
    def _ai_chains(self, topic: str) -> List[Dict]:
        """AI 领域的问题链"""
        return [
            {
                "title": "算法原理",
                "questions": [
                    {
                        "q": f"{topic} 的核心思想是什么？",
                        "a": "【回答要点】：一句话说清楚本质",
                        "depth": 1
                    },
                    {
                        "q": "它的损失函数/目标函数是什么？",
                        "a": "【回答要点】：优化目标",
                        "depth": 2
                    },
                    {
                        "q": "为什么会有效？数学依据是什么？",
                        "a": "【回答要点】：理论保证",
                        "depth": 3
                    }
                ]
            },
            {
                "title": "工程实践",
                "questions": [
                    {
                        "q": "训练 {topic} 需要什么数据？",
                        "a": "【回答要点】：数据要求",
                        "depth": 1
                    },
                    {
                        "q": "常见调参技巧有哪些？",
                        "a": "【回答要点】：超参数调试",
                        "depth": 2
                    },
                    {
                        "q": "如何避免过拟合？",
                        "a": "【回答要点】：正则化方法",
                        "depth": 3
                    }
                ]
            }
        ]
    
    def _investment_chains(self, topic: str) -> List[Dict]:
        """投资领域的问题链"""
        return [
            {
                "title": "核心理念",
                "questions": [
                    {
                        "q": f"为什么 {topic} 有效？",
                        "a": "【回答要点】：底层逻辑",
                        "depth": 1
                    },
                    {
                        "q": "它的前提假设是什么？",
                        "a": "【回答要点】：适用条件",
                        "depth": 2
                    },
                    {
                        "q": "历史验证结果如何？",
                        "a": "【回答要点】：回测数据",
                        "depth": 3
                    }
                ]
            },
            {
                "title": "风险控制",
                "questions": [
                    {
                        "q": f"使用 {topic} 的最大风险是什么？",
                        "a": "【回答要点】：风险点识别",
                        "depth": 1
                    },
                    {
                        "q": "如何控制这个风险？",
                        "a": "【回答要点】：风控措施",
                        "depth": 2
                    },
                    {
                        "q": "什么情况下应该止损/退出？",
                        "a": "【回答要点】：退出机制",
                        "depth": 3
                    }
                ]
            }
        ]
    
    def _science_chains(self, topic: str) -> List[Dict]:
        """科学领域的问题链"""
        return [
            {
                "title": "原理理解",
                "questions": [
                    {
                        "q": f"{topic} 的底层原理是什么？",
                        "a": "【回答要点】：第一性原理",
                        "depth": 1
                    },
                    {
                        "q": "如何用实验验证这个原理？",
                        "a": "【回答要点】：实验方法",
                        "depth": 2
                    },
                    {
                        "q": "这个原理的局限性在哪里？",
                        "a": "【回答要点】：适用范围",
                        "depth": 3
                    }
                ]
            }
        ]
    
    def _generate_domain_chains(self, topic: str, analysis: Dict) -> List[Dict]:
        """生成领域特定的问题链"""
        chains = []
        
        domain = analysis["domain"]
        
        if domain == "ai":
            chains.append({
                "title": "AI 行业视角",
                "questions": [
                    {
                        "q": f"{topic} 在 AI 技术栈中的位置？",
                        "a": "【回答要点】：定位和作用",
                        "depth": 1
                    },
                    {
                        "q": "目前的主流方案有哪些？",
                        "a": "【回答要点】：技术路线",
                        "depth": 2
                    },
                    {
                        "q": "未来发展趋势是什么？",
                        "a": "【回答要点】：前沿方向",
                        "depth": 3
                    }
                ]
            })
        
        return chains
    
    def _generate_continuous_example(self, topic: str, analysis: Dict) -> Dict:
        """生成一个完整的连续追问示例"""
        
        # 根据领域生成不同的连续追问示例
        if analysis["domain"] == "ai":
            example_topic = "神经网络"
        elif analysis["domain"] == "programming":
            example_topic = "递归"
        elif analysis["domain"] == "investment":
            example_topic = "复利"
        else:
            example_topic = topic
        
        # 为每个步骤生成更具体的回答提示
        answer_hints = {
            1: f"【用自己的话解释 {example_topic}】",
            2: f"【{example_topic} 解决了什么问题？】",
            3: f"【{example_topic} 的核心本质】",
            4: f"【{example_topic} 的底层原理】"
        }
        
        return {
            "title": f"连续追问示例：{example_topic}",
            "steps": [
                {
                    "question": f"什么是 {example_topic}？",
                    "answer": answer_hints[1],
                    "depth": 1
                },
                {
                    "question": f"为什么需要 {example_topic}？",
                    "answer": answer_hints[2],
                    "depth": 2
                },
                {
                    "question": "它的本质是什么？",
                    "answer": answer_hints[3],
                    "depth": 3
                },
                {
                    "question": "最基础的原理是什么？",
                    "answer": answer_hints[4],
                    "depth": 4,
                    "is_aha": True
                }
            ]
        }
    
    def render_markdown(self, data: Dict) -> str:
        """将问题链数据渲染为 Markdown 格式"""
        
        lines = ["# 递归追问链\n"]
        
        # 主题分析
        if "analysis" in data:
            analysis = data["analysis"]
            lines.append(f"## 主题分析\n")
            lines.append(f"- 领域：{analysis.get('domain', 'general')}\n")
            if analysis.get('keywords'):
                lines.append(f"- 关键词：{', '.join(analysis['keywords'])}\n")
            lines.append(f"- 理论：{'✓' if analysis.get('has_theory') else '✗'} | 实践：{'✓' if analysis.get('has_practice') else '✗'} | 数学：{'✓' if analysis.get('has_math') else '✗'}\n\n")
        
        # 通用问题链
        if "general_chains" in data:
            for chain in data["general_chains"]:
                lines.append(f"## {chain['title']}\n\n")
                for q in chain["questions"]:
                    question = q.get('q') or q.get('question', '')
                    answer = q.get('a') or q.get('answer', '')
                    depth_indicator = "  " * (q.get("depth", 1) - 1) + "└─ "
                    lines.append(f"{depth_indicator}**Q**: {question}\n")
                    lines.append(f"{depth_indicator}**A**: {answer}\n\n")
        
        # 概念特异性问题
        if "concept_chains" in data:
            for chain in data["concept_chains"]:
                lines.append(f"---\n\n## {chain['title']}\n\n")
                for q in chain["questions"]:
                    question = q.get('q') or q.get('question', '')
                    answer = q.get('a') or q.get('answer', '')
                    depth_indicator = "  " * (q.get("depth", 1) - 1) + "└─ "
                    lines.append(f"{depth_indicator}**Q**: {question}\n")
                    lines.append(f"{depth_indicator}**A**: {answer}\n\n")
        
        # 连续追问示例
        if "continuous_example" in data:
            ex = data["continuous_example"]
            lines.append(f"---\n\n## {ex['title']}\n")
            lines.append("> 连续追问示例，通过层层深入达到 Aha Moment\n\n")
            for step in ex["steps"]:
                question = step.get('question', '')
                answer = step.get('answer', '')
                is_aha = " 💡 **Aha!**" if step.get("is_aha") else ""
                lines.append(f"**Q{step['depth']}**: {question}{is_aha}\n\n")
                lines.append(f"**A{step['depth']}**: {answer}\n\n")
        
        return "".join(lines)


def generate_recursive_questions(topic: str, context: Dict = None) -> str:
    """便捷函数：生成递归追问内容（返回 Markdown 字符串）"""
    generator = RecursiveQuestionGenerator()
    data = generator.generate_for_topic(topic, context)
    return generator.render_markdown(data)


if __name__ == "__main__":
    import sys
    
    topic = sys.argv[1] if len(sys.argv) > 1 else "机器学习"
    
    print(f"# {topic} 的递归追问链\n")
    print(generate_recursive_questions(topic))