"""表格清洗 Skill。

清洗表格数据：移除空白行列、处理复杂表头、类型转换等。

Usage:
    python clean_table_skill.py <input_file> [output_dir]

Arguments:
    input_file: 输入文件路径 (.csv)
    output_dir: 输出目录（可选，默认为输入文件所在目录）

Example:
    python clean_table_skill.py /path/to/input.csv /path/to/output
    python clean_table_skill.py /path/to/input.csv  # 输出到 /path/to/
"""

import os
import sys
import asyncio
import argparse
from typing import Any, Dict, List

import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

from script.src import (
    remove_blank_rows_and_columns,
    process_complex_header_table,
    transfer_to_csv_in_memory,
    get_llm_service,
    process_csv,
)


class CleanTableSkill:
    """表格清洗技能。

    清洗表格数据：移除空白行列、处理复杂表头。
    输入：文件路径
    输出：清洗后的文件路径
    """

    def __init__(self, is_merge_header: bool = True, is_default_header: bool = False, remove_chars: List[str] = None):
        """初始化清洗技能。

        Args:
            is_merge_header: 是否合并多行表头
            is_default_header: 是否使用默认数字表头
            remove_chars: 需要移除的字符列表，如 [','] 移除千分位逗号
        """
        self.is_merge_header = is_merge_header
        self.is_default_header = is_default_header
        self.remove_chars = remove_chars or [',']

    async def run(self, input_file: str, output_dir: str = None) -> Dict[str, Any]:
        """执行表格清洗。

        Args:
            input_file: 输入文件路径
            output_dir: 输出目录（可选）

        Returns:
            包含以下键的字典：
                - output_file: 清洗后的文件路径
                - success: 是否成功
                - row_count: 清洗后行数
                - col_count: 清洗后列数
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
        output_file = os.path.join(output_dir, f"{base_name}_cleaned.csv")

        try:
            df = await self._load_file(input_file)

            if df.empty:
                return {
                    "output_file": "",
                    "success": False,
                    "error": "数据为空"
                }

            df = await self._clean_data(df)

            # 根据表头类型决定是否写入表头
            # 如果不是默认数字表头，则写入表头；否则不写入
            write_header = not self._is_default_numeric_header(df)
            df.to_csv(output_file, index=False, header=write_header, encoding='utf-8')

            return {
                "output_file": output_file,
                "success": True,
                "row_count": len(df),
                "col_count": len(df.columns),
                "output_dir": output_dir
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

    async def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗数据。

        Args:
            df: 输入 DataFrame

        Returns:
            清洗后的 DataFrame
        """
        df = remove_blank_rows_and_columns(df)

        if self.remove_chars:
            df = process_csv(df, self.remove_chars)

        if self.is_merge_header and not df.empty:
            llm_service = get_llm_service()
            df = await process_complex_header_table(df, llm_service)

        if not df.empty:
            df = transfer_to_csv_in_memory(df, self.is_default_header)

        return df

    def _is_default_numeric_header(self, df: pd.DataFrame) -> bool:
        """判断是否为默认数字表头 (0, 1, 2, 3...)。

        Args:
            df: 输入 DataFrame

        Returns:
            是否为默认数字表头
        """
        return all(isinstance(c, int) for c in df.columns)


async def run_skill(input_file: str, output_dir: str = None, is_merge_header: bool = True, remove_chars: List[str] = None) -> Dict[str, Any]:
    """运行表格清洗技能。

    Args:
        input_file: 输入文件路径
        output_dir: 输出目录
        is_merge_header: 是否合并多行表头
        remove_chars: 需要移除的字符列表

    Returns:
        清洗结果
    """
    skill = CleanTableSkill(is_merge_header=is_merge_header, remove_chars=remove_chars)
    return await skill.run(input_file, output_dir)


def main():
    parser = argparse.ArgumentParser(description="表格清洗 Skill")
    parser.add_argument("input_file", help="输入文件路径 (.csv)")
    parser.add_argument("output_dir", nargs="?", default=None, help="输出目录（可选）")
    parser.add_argument("--no-merge-header", action="store_true", help="不合并多行表头")
    parser.add_argument("--remove-chars", type=str, default=None, help="需要移除的字符（如 ',' 移除千分位逗号，默认 ','）")

    args = parser.parse_args()

    is_merge_header = not args.no_merge_header
    remove_chars = None
    if args.remove_chars is not None:
        remove_chars = [c for c in args.remove_chars.split(',')]

    print("=" * 60)
    print("Clean Table Skill")
    print("=" * 60)
    print(f"Input file: {args.input_file}")
    print(f"Output directory: {args.output_dir or '默认与输入同目录'}")
    print(f"Merge header: {is_merge_header}")
    print(f"Remove chars: {remove_chars or [',']}")
    print()

    result = asyncio.run(run_skill(args.input_file, args.output_dir, is_merge_header, remove_chars))

    if result["success"]:
        print(f"✓ 清洗成功！")
        print(f"  行数: {result.get('row_count', 0)}")
        print(f"  列数: {result.get('col_count', 0)}")
        print()
        print(f"输出文件: {os.path.basename(result['output_file'])}")
    else:
        print(f"✗ 清洗失败: {result.get('error', '未知错误')}")

    print("=" * 60)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
