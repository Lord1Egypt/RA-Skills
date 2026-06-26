#!/usr/bin/env python3
"""
RootCraft Learning System - 质量评分器 v1.1.5
基于 4 个维度对学习内容进行评分
"""
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ScoreResult:
    """评分结果"""
    total: float
    completeness: float
    accuracy: float
    logic: float
    practicality: float
    issues: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


class QualityScorer:
    """质量评分器 - 4 维度评估"""
    
    # 评分维度及权重
    DIMENSIONS = {
        'completeness': 0.20,  # 完整性
        'accuracy': 0.30,      # 准确性
        'logic': 0.25,         # 逻辑性
        'practicality': 0.25   # 实用性
    }
    
    # 9 步学习流程的必需步骤
    REQUIRED_STEPS = [
        'goals',               # 学习目标
        'first_principles',    # 第一性原理
        'taxonomy',            # 分类学
        'feynman',             # 费曼检验
        'recursive_questions', # 递归追问
        'aha_moments',         # Aha Moment
        'resources',           # 多视角学习
        'practice',            # 实践应用
        'feedback',            # 反馈与迭代
        'review',              # 复习计划
        'mindmap'              # 思维导图
    ]
    
    # 必需的文件（与 REQUIRED_STEPS 对应）
    REQUIRED_FILES = {
        'goals': '01-goals.md',
        'first_principles': '02-first-principles.md',
        'taxonomy': '03-taxonomy.md',
        'feynman': '04-feynman.md',
        'recursive_questions': '04b-recursive-questions.md',
        'aha_moments': '04c-aha-moments.md',
        'resources': '05-resources.md',
        'practice': '06-practice.md',
        'feedback': '07-feedback.md',
        'review': '08-review.md',
        'mindmap': '09-mindmap.md'
    }
    
    # 模板占位符（如果内容只包含这些，说明是默认模板）
    TEMPLATE_MARKERS = [
        r'请填写',
        r'\[填写\]',
        r'\（填写\）',
        r'\[选择\]',
        r'\[填\]',
        r'请先',
        r'TODO',
        r'todo'
    ]
    
    def __init__(self):
        self.base_dir = "/root/.openclaw/workspace/study"
    
    def score(self, topic: str, study_path: str = None) -> ScoreResult:
        """
        对学习内容进行评分
        
        Args:
            topic: 学习主题
            study_path: 学习资料目录路径（可选，默认从主题推断）
        
        Returns:
            ScoreResult: 评分结果
        """
        if study_path is None:
            topic_sanitized = self._sanitize_topic(topic)
            study_path = f"{self.base_dir}/{topic_sanitized}"
        
        # 各维度评分
        completeness = self._check_completeness(study_path)
        accuracy = self._check_accuracy(topic, study_path)
        logic = self._check_logic(study_path)
        practicality = self._check_practicality(study_path)
        
        # 收集问题
        issues = self._collect_issues(completeness, accuracy, logic, practicality)
        
        # 加权计算总分
        total = (
            completeness['score'] * self.DIMENSIONS['completeness'] +
            accuracy['score'] * self.DIMENSIONS['accuracy'] +
            logic['score'] * self.DIMENSIONS['logic'] +
            practicality['score'] * self.DIMENSIONS['practicality']
        )
        
        return ScoreResult(
            total=round(total, 1),
            completeness=completeness['score'],
            accuracy=accuracy['score'],
            logic=logic['score'],
            practicality=practicality['score'],
            issues=issues,
            details={
                'completeness': completeness,
                'accuracy': accuracy,
                'logic': logic,
                'practicality': practicality
            }
        )
    
    def _sanitize_topic(self, topic: str) -> str:
        """将主题转换为安全的目录名"""
        return topic.replace("/", "-").replace("\\", "-").replace(":", "-").strip()
    
    def _check_completeness(self, study_path: str) -> Dict:
        """检查完整性 - 9 步是否全部覆盖"""
        import os
        
        found_files = []
        missing_files = []
        
        for step, filename in self.REQUIRED_FILES.items():
            filepath = os.path.join(study_path, filename)
            if os.path.exists(filepath):
                found_files.append(filename)
            else:
                missing_files.append(filename)
        
        # 计算得分：如果缺少文件，扣分
        total = len(self.REQUIRED_FILES)
        found = len(found_files)
        
        if total == 0:
            score = 0
        else:
            score = (found / total) * 100
        
        # 检查是否有模板内容（如果所有文件都是模板，得分更低）
        template_count = 0
        for f in found_files:
            filepath = os.path.join(study_path, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if self._is_template_content(content):
                        template_count += 1
            except:
                pass
        
        # 如果全部是模板内容，大幅扣分
        if found > 0 and template_count == found:
            score *= 0.3
        
        issues = []
        if missing_files:
            issues.append(f"缺少文件: {', '.join(missing_files)}")
        if template_count > 0:
            issues.append(f"{template_count} 个文件使用默认模板，内容需要填充")
        
        return {
            'score': round(score, 1),
            'found': found_files,
            'missing': missing_files,
            'template_count': template_count,
            'issues': issues
        }
    
    def _is_template_content(self, content: str) -> bool:
        """检查内容是否为模板占位符"""
        content_lower = content.lower()
        
        # 检查是否包含模板标记
        for marker in self.TEMPLATE_MARKERS:
            if re.search(marker, content, re.IGNORECASE):
                return True
        
        # 检查是否太短（少于 200 字符）
        if len(content.strip()) < 200:
            # 检查是否包含有效知识（而非只有标题）
            lines = [l.strip() for l in content.split('\n') if l.strip()]
            # 如果大部分是空行或标题，可能也是模板
            if len(lines) < 5:
                return True
        
        return False
    
    def _check_accuracy(self, topic: str, study_path: str) -> Dict:
        """检查准确性 - 核心概念是否正确"""
        import os
        
        issues = []
        score = 100
        
        # 检查关键文件是否存在，并进行基本的事实校验
        key_files = {
            '02-first-principles.md': ['定义', '公理', '本质'],
            '03-taxonomy.md': ['##', '分类', '层级'],
            '04-feynman.md': ['概念', '解释', 'Q:']
        }
        
        for filename, required_keywords in key_files.items():
            filepath = os.path.join(study_path, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # 检查是否包含必要的关键词
                        missing_keywords = [kw for kw in required_keywords if kw not in content]
                        if missing_keywords:
                            issues.append(f"{filename} 缺少关键词: {', '.join(missing_keywords)}")
                            score -= 10
                except:
                    pass
        
        # 检查递归追问是否是基于模板
        recursive_file = os.path.join(study_path, '04b-recursive-questions.md')
        if os.path.exists(recursive_file):
            try:
                with open(recursive_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 如果包含大量通用模板内容，准确性质疑
                    if self._is_template_content(content):
                        issues.append("递归追问使用默认模板，未针对主题生成")
                        score -= 15
            except:
                pass
        
        return {
            'score': max(0, round(score, 1)),
            'issues': issues
        }
    
    def _check_logic(self, study_path: str) -> Dict:
        """检查逻辑通顺度"""
        import os
        
        issues = []
        score = 100
        
        # 检查文件间的逻辑关联
        # 1. 第一性原理应该是其他内容的基础
        # 2. 分类学应该是递进结构
        # 3. 费曼和递归追问应该有呼应
        
        # 简单检查：相邻步骤间的标题是否有逻辑关联
        # 这里做简化处理，只检查是否存在明显的逻辑断层
        
        # 检查是否有重复内容
        try:
            files = os.listdir(study_path)
            content_hashes = {}
            for fname in files:
                if fname.endswith('.md'):
                    fpath = os.path.join(study_path, fname)
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 简单检查前100个字符作为标识
                        key = content[:100].strip()
                        if key in content_hashes:
                            issues.append(f"{fname} 与 {content_hashes[key]} 内容高度重复")
                            score -= 5
                        else:
                            content_hashes[key] = fname
        except:
            pass
        
        return {
            'score': max(0, round(score, 1)),
            'issues': issues
        }
    
    def _check_practicality(self, study_path: str) -> Dict:
        """检查实用性 - 代码是否可运行、题目是否有意义"""
        import os
        import re
        
        issues = []
        score = 100
        
        # 1. 检查实践代码
        practice_file = os.path.join(study_path, '06-practice.md')
        if os.path.exists(practice_file):
            try:
                with open(practice_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 检查是否包含代码
                    code_blocks = re.findall(r'```[\w]*\n(.*?)```', content, re.DOTALL)
                    
                    if not code_blocks:
                        issues.append("实践部分缺少代码示例")
                        score -= 20
                    else:
                        # 检查代码是否只是模板（有 import 但无实际逻辑）
                        has_real_code = False
                        for block in code_blocks:
                            # 过滤掉注释和空行
                            lines = [l.strip() for l in block.split('\n') if l.strip() and not l.strip().startswith('#')]
                            if len(lines) > 3:  # 至少有几行实际代码
                                has_real_code = True
                                break
                        
                        if not has_real_code:
                            issues.append("实践代码过于简单，只是模板")
                            score -= 15
            except:
                pass
        
        # 2. 检查试卷/题目
        exam_file = os.path.join(study_path, '08-exam.md')
        if os.path.exists(exam_file):
            try:
                with open(exam_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 检查是否有实际题目
                    questions = re.findall(r'\d+[\.、]', content)
                    if len(questions) < 3:
                        issues.append("试卷题目数量不足")
                        score -= 10
            except:
                pass
        
        # 3. 检查复习计划
        review_file = os.path.join(study_path, '08-review.md')
        if os.path.exists(review_file):
            try:
                with open(review_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 检查是否有具体的复习时间点
                    if not re.search(r'\d+[天周日月]', content):
                        issues.append("复习计划缺少具体时间点")
                        score -= 10
            except:
                pass
        
        return {
            'score': max(0, round(score, 1)),
            'issues': issues
        }
    
    def _collect_issues(self, completeness: Dict, accuracy: Dict, 
                        logic: Dict, practicality: Dict) -> List[str]:
        """收集所有问题"""
        all_issues = []
        
        for dim_result in [completeness, accuracy, logic, practicality]:
            if 'issues' in dim_result:
                all_issues.extend(dim_result['issues'])
        
        return all_issues
    
    def is_passed(self, score_result: ScoreResult, threshold: float = 80.0) -> bool:
        """判断是否通过"""
        return score_result.total >= threshold


def format_score_report(topic: str, result: ScoreResult, attempt: int = 1) -> str:
    """格式化评分报告"""
    
    def bar(score: float, width: int = 10) -> str:
        filled = int(score / 100 * width)
        return "█" * filled + "░" * (width - filled)
    
    status = "✅ 通过" if result.total >= 80 else "❌ 未通过"
    
    report = f"""📊 质量评分报告（第 {attempt} 轮）
━━━━━━━━━━━━━━━━━━━━━━━━━━
完整性: {bar(result.completeness)} {result.completeness}%
准确性: {bar(result.accuracy)} {result.accuracy}%
逻辑性: {bar(result.logic)} {result.logic}%
实用性: {bar(result.practicality)} {result.practicality}%

总分: {result.total} / 100 {status}
"""
    
    if result.issues:
        report += "\n发现问题:\n"
        for i, issue in enumerate(result.issues, 1):
            report += f"- {issue}\n"
    
    return report


if __name__ == "__main__":
    # 测试
    import sys
    
    if len(sys.argv) > 2:
        topic = sys.argv[1]
        path = sys.argv[2]
    elif len(sys.argv) > 1:
        topic = sys.argv[1]
        path = None
    else:
        topic = "测试主题"
        path = None
    
    scorer = QualityScorer()
    result = scorer.score(topic, path)
    print(format_score_report(topic, result))