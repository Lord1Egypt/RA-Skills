"""表头合并 Skill。

使用 LLM 智能检测并合并多行表头，将复杂表头扁平化为单行表头。

Usage:
    python merge_header_skill.py <input_file> [output_dir]

Arguments:
    input_file: 输入文件路径 (.csv)
    output_dir: 输出目录（可选，默认为输入文件所在目录）

Example:
    python merge_header_skill.py /path/to/input.csv /path/to/output
    python merge_header_skill.py /path/to/input.csv  # 输出到 /path/to/
"""

import os
import sys
import asyncio
import argparse
from typing import Any, Dict

import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

from script.src import (
    remove_blank_rows_and_columns,
    process_complex_header_table,
    get_llm_service,
)


class MergeHeaderSkill:
    """表头合并技能。

    使用 LLM 智能检测多行表头并合并为单行表头。
    输入：文件路径
    输出：合并表头后的文件路径
    """

    def __init__(self):
        """初始化表头合并技能。"""
        pass

    async def run(self, input_file: str, output_dir: str = None) -> Dict[str, Any]:
        """执行表头合并。

        Args:
            input_file: 输入文件路径
            output_dir: 输出目录（可选）

        Returns:
            包含以下键的字典：
                - output_file: 合并表头后的文件路径
                - success: 是否成功
                - row_count: 处理后行数
                - col_count: 处理后列数
                - header_rows_detected: 检测到的表头行数
        """
        if not os.path.exists(input_file):
            return {
                "output_file": "",
                "success": False,
                "error": f"文件不存在：{input_file}"
            }

        if not input_file.lower().endswith('.csv'):
            return {
                "output_file": "",
                "success": False,
                "error": f"不支持的文件格式：{input_file}，仅支持 .csv 文件"
            }

        if output_dir is None:
            output_dir = os.path.dirname(os.path.abspath(input_file))

        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}_merged_header.csv")

        try:
            df = await self._load_file(input_file)

            if df.empty:
                return {
                    "output_file": "",
                    "success": False,
                    "error": "数据为空"
                }

            df, header_rows = await self._merge_header(df)

            df.to_csv(output_file, index=False, encoding='utf-8')

            return {
                "output_file": output_file,
                "success": True,
                "row_count": len(df),
                "col_count": len(df.columns),
                "header_rows_detected": header_rows
            }
        except Exception as e:
            return {
                "output_file": "",
                "success": False,
                "error": str(e)
            }

    async def _load_file(self, file_path: str) -> pd.DataFrame:
        """加载 CSV 文件。

        Args:
            file_path: 文件路径

        Returns:
            DataFrame
        """
        try:
            return pd.read_csv(file_path, header=None)
        except:
            return pd.read_csv(file_path, encoding='gbk', header=None)

    async def _merge_header(self, df: pd.DataFrame) -> tuple:
        """合并多行表头。

        Args:
            df: 输入 DataFrame

        Returns:
            (合并后的 DataFrame, 检测到的表头行数)
        """
        df = remove_blank_rows_and_columns(df)

        if df.empty:
            return df, 0

        llm_service = get_llm_service()
        df_merged = await process_complex_header_table(df, llm_service)

        header_rows = len(df) - len(df_merged) + 1
        if header_rows < 1:
            header_rows = 1

        return df_merged, header_rows


async def run_skill(input_file: str, output_dir: str = None) -> Dict[str, Any]:
    """运行表头合并技能。

    Args:
        input_file: 输入文件路径
        output_dir: 输出目录

    Returns:
        合并结果
    """
    skill = MergeHeaderSkill()
    return await skill.run(input_file, output_dir)


def main():
    parser = argparse.ArgumentParser(description="表头合并 Skill")
    parser.add_argument("input_file", help="输入文件路径 (.csv)")
    parser.add_argument("output_dir", nargs="?", default=None, help="输出目录（可选）")

    args = parser.parse_args()

    print("=" * 60)
    print("Merge Header Skill")
    print("=" * 60)
    print(f"Input file: {args.input_file}")
    print(f"Output directory: {args.output_dir or '默认与输入同目录'}")
    print()

    result = asyncio.run(run_skill(args.input_file, args.output_dir))

    if result["success"]:
        print(f"✓ 合并成功！")
        print(f"  行数：{result.get('row_count', 0)}")
        print(f"  列数：{result.get('col_count', 0)}")
        print(f"  检测到表头行数：{result.get('header_rows_detected', 1)}")
        print()
        print(f"输出文件：{os.path.basename(result['output_file'])}")
    else:
        print(f"✗ 合并失败：{result.get('error', '未知错误')}")

    print("=" * 60)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
