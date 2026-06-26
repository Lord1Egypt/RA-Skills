# Study Writer - 学习资料自动生成器 v1.1.5

from .study_writer import (
    generate_and_save, 
    create_study_files, 
    generate_default_content,
    quality_check,          # v1.1.1 质检模块
    print_quality_report,   # v1.1.1 质检报告
    save_exam_paper,        # v1.1.1 试卷生成
)

# v1.1.5 新增：质量评分系统
from .quality_scorer import (
    QualityScorer,
    ScoreResult,
    format_score_report
)

# v1.1.5 新增：递归追问生成器
from .recursive_question_generator import (
    RecursiveQuestionGenerator,
    generate_recursive_questions
)

__all__ = [
    # 核心生成
    "generate_and_save", 
    "create_study_files", 
    "generate_default_content",
    # 质检模块
    "quality_check",
    "print_quality_report",
    "save_exam_paper",
    # v1.1.5 新增
    "QualityScorer",
    "ScoreResult",
    "format_score_report",
    "RecursiveQuestionGenerator",
    "generate_recursive_questions",
]