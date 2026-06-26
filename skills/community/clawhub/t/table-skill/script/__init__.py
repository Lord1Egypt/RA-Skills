"""Skills 包初始化。

提供三个独立的表格预处理技能：
- split_table_skill: 表格拆分
- clean_table_skill: 表格清洗
- describe_table_skill: 表格描述生成
"""

from .split_table_skill import SplitTableSkill, run_skill as split_table
from .clean_table_skill import CleanTableSkill, run_skill as clean_table
from .describe_table_skill import DescribeTableSkill, run_skill as describe_table

__all__ = [
    "SplitTableSkill",
    "CleanTableSkill",
    "DescribeTableSkill",
    "split_table",
    "clean_table",
    "describe_table",
]
