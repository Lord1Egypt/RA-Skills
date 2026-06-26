#!/usr/bin/env python3
"""
任务分析器 - 小龙虾工作流 MVP 核心组件

功能：
1. 解析用户输入的任务描述
2. 评估任务复杂度
3. 生成结构化任务概要
4. 判断是否需要分层处理
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TaskSummary:
    """任务概要数据结构"""
    task_id: str
    original_description: str
    title: str
    description: str
    objectives: List[str]
    constraints: List[str]
    expected_outputs: List[str]
    complexity_score: int  # 1-10分
    estimated_hours: float
    deadline: Optional[str]
    requires_decomposition: bool
    keywords: List[str]
    created_at: str
    updated_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    def to_markdown(self) -> str:
        """生成Markdown格式的任务概要"""
        md = f"""# 任务概要: {self.title}

## 基本信息
- **任务ID**: {self.task_id}
- **创建时间**: {self.created_at}
- **最后更新**: {self.updated_at}
- **复杂度评分**: {self.complexity_score}/10
- **预计耗时**: {self.estimated_hours} 小时
- **需要分层处理**: {'是' if self.requires_decomposition else '否'}

## 原始描述
{self.original_description}

## 任务描述
{self.description}

## 目标
{chr(10).join(f'- {obj}' for obj in self.objectives)}

## 约束条件
{chr(10).join(f'- {constraint}' for constraint in self.constraints)}

## 预期输出
{chr(10).join(f'- {output}' for output in self.expected_outputs)}

## 关键词
{', '.join(self.keywords)}

## 处理建议
{self.get_recommendation()}
"""
        return md
    
    def get_recommendation(self) -> str:
        """根据复杂度提供处理建议"""
        if self.complexity_score >= 7:
            return "✅ **建议使用完整的小龙虾分层工作流**：任务复杂，需要分解为多个阶段和步骤。"
        elif self.complexity_score >= 4:
            return "⚠️ **建议使用简化分层流程**：任务中等复杂，可能需要分解为2-3个主要步骤。"
        else:
            return "🔧 **可直接执行**：任务较简单，可直接调用API或执行命令完成。"


class TaskAnalyzer:
    """任务分析器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化分析器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.complexity_keywords = self.config.get('complexity_keywords', [])
        logger.info(f"任务分析器初始化完成，加载 {len(self.complexity_keywords)} 个复杂度关键词")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            'complexity_keywords': [
                '系统设计', '架构迁移', '大规模数据处理', '完整方案',
                '复杂系统', '多步骤', '长期项目', '开发', '实现',
                '构建', '创建', '设计', '分析', '研究', '调查'
            ]
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                # 合并配置
                default_config.update(user_config)
            except Exception as e:
                logger.warning(f"加载配置文件失败，使用默认配置: {e}")
        
        return default_config
    
    def _generate_task_id(self, task_description: str) -> str:
        """生成任务ID"""
        # 使用时间戳和任务描述的哈希前4位
        import hashlib
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_hash = hashlib.md5(task_description.encode()).hexdigest()[:4]
        return f"task_{timestamp}_{task_hash}"
    
    def _calculate_complexity(self, task_description: str) -> int:
        """计算任务复杂度（1-10分）"""
        score = 1
        
        # 1. 长度分析
        word_count = len(task_description.split())
        if word_count > 100:
            score += 3
        elif word_count > 50:
            score += 2
        elif word_count > 20:
            score += 1
        
        # 2. 关键词匹配
        matched_keywords = []
        for keyword in self.complexity_keywords:
            if keyword.lower() in task_description.lower():
                matched_keywords.append(keyword)
                score += 1
        
        # 3. 特殊模式检测
        patterns = [
            (r'\d+\s*个(步骤|阶段|部分)', 2),  # 包含数字个步骤
            (r'(首先|然后|接着|最后)', 1),     # 序列词
            (r'(需要|要求|必须).{10,}', 1),    # 需求描述
            (r'(设计|开发|实现|构建).{10,}', 2), # 开发任务
        ]
        
        for pattern, pattern_score in patterns:
            if re.search(pattern, task_description):
                score += pattern_score
        
        # 4. 约束条件检测
        constraint_indicators = ['时间', '预算', '资源', '限制', '约束', '要求']
        for indicator in constraint_indicators:
            if indicator in task_description:
                score += 1
                break
        
        # 限制在1-10分之间
        return min(max(score, 1), 10)
    
    def _estimate_hours(self, complexity: int, description: str) -> float:
        """根据复杂度估算耗时（小时）"""
        # 基础估算
        base_hours = complexity * 0.5
        
        # 根据关键词调整
        adjustment = 1.0
        if any(word in description for word in ['简单', '快速', '小任务']):
            adjustment = 0.5
        elif any(word in description for word in ['复杂', '大型', '完整', '系统']):
            adjustment = 2.0
        
        estimated = base_hours * adjustment
        return round(estimated, 1)
    
    def _extract_keywords(self, description: str) -> List[str]:
        """提取关键词"""
        # 简单实现：提取名词性词汇
        words = re.findall(r'\b[\u4e00-\u9fa5]{2,5}\b', description)
        
        # 过滤常见虚词
        stop_words = ['然后', '接着', '最后', '这个', '那个', '一些', '一种']
        keywords = [word for word in words if word not in stop_words]
        
        # 去重，取前10个
        unique_keywords = list(dict.fromkeys(keywords))
        return unique_keywords[:10]
    
    def _analyze_with_model(self, task_description: str) -> Dict[str, Any]:
        """
        使用大模型分析任务（MVP占位实现）
        
        实际实现应调用DeepSeek R1或其他模型API
        """
        # 这里是占位实现，实际应调用模型API
        # 返回模拟的分析结果
        return {
            'title': task_description[:30] + ('...' if len(task_description) > 30 else ''),
            'description': f"任务：{task_description[:100]}...",
            'objectives': ['完成用户指定的任务', '保证质量', '按时交付'],
            'constraints': ['资源有限', '时间紧迫'],
            'expected_outputs': ['完整的解决方案', '相关文档']
        }
    
    def analyze(self, task_description: str, 
                deadline: Optional[str] = None) -> TaskSummary:
        """
        分析任务并生成任务概要
        
        Args:
            task_description: 任务描述文本
            deadline: 截止时间（可选，格式：YYYY-MM-DD HH:MM）
            
        Returns:
            TaskSummary: 任务概要对象
        """
        logger.info(f"开始分析任务: {task_description[:50]}...")
        
        # 生成任务ID
        task_id = self._generate_task_id(task_description)
        
        # 计算复杂度
        complexity_score = self._calculate_complexity(task_description)
        
        # 估算耗时
        estimated_hours = self._estimate_hours(complexity_score, task_description)
        
        # 提取关键词
        keywords = self._extract_keywords(task_description)
        
        # 判断是否需要分层处理
        requires_decomposition = complexity_score >= 4
        
        # 使用模型分析（占位）
        model_analysis = self._analyze_with_model(task_description)
        
        # 当前时间
        now = datetime.now().astimezone().isoformat()
        
        # 创建任务概要
        summary = TaskSummary(
            task_id=task_id,
            original_description=task_description,
            title=model_analysis['title'],
            description=model_analysis['description'],
            objectives=model_analysis['objectives'],
            constraints=model_analysis['constraints'],
            expected_outputs=model_analysis['expected_outputs'],
            complexity_score=complexity_score,
            estimated_hours=estimated_hours,
            deadline=deadline,
            requires_decomposition=requires_decomposition,
            keywords=keywords,
            created_at=now,
            updated_at=now
        )
        
        logger.info(f"任务分析完成: ID={task_id}, 复杂度={complexity_score}/10, 需要分层={requires_decomposition}")
        
        return summary


def test_task_analyzer():
    """测试任务分析器"""
    print("🧪 测试任务分析器...")
    
    analyzer = TaskAnalyzer()
    
    # 测试用例
    test_tasks = [
        "帮我设计一个完整的电商网站后端系统",
        "写一个Python脚本，读取CSV文件并计算平均值",
        "研究区块链技术在供应链管理中的应用，并写一份报告",
        "查一下今天的天气"
    ]
    
    for i, task in enumerate(test_tasks):
        print(f"\n{'='*50}")
        print(f"测试用例 {i+1}: {task}")
        
        summary = analyzer.analyze(task)
        
        print(f"任务ID: {summary.task_id}")
        print(f"复杂度评分: {summary.complexity_score}/10")
        print(f"预计耗时: {summary.estimated_hours} 小时")
        print(f"需要分层: {summary.requires_decomposition}")
        print(f"关键词: {', '.join(summary.keywords[:5])}")
        
        # 保存为Markdown文件（测试用）
        test_dir = "/tmp/xiaolongxia_test"
        os.makedirs(test_dir, exist_ok=True)
        md_file = os.path.join(test_dir, f"test_{i+1}_summary.md")
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(summary.to_markdown())
        
        print(f"任务概要已保存: {md_file}")
    
    print(f"\n{'='*50}")
    print("✅ 任务分析器测试完成")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_task_analyzer()
    elif len(sys.argv) > 1:
        # 命令行使用：python task_analyzer.py "任务描述"
        task_desc = sys.argv[1]
        analyzer = TaskAnalyzer()
        summary = analyzer.analyze(task_desc)
        print(summary.to_markdown())
    else:
        print("用法:")
        print("  python task_analyzer.py \"任务描述\"")
        print("  python task_analyzer.py test")
        sys.exit(1)