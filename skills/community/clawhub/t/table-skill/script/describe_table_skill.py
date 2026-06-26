"""表格描述生成 Skill。

为表格生成详细的描述信息：列统计、摘要、样本数据等。

Usage:
    python describe_table_skill.py <input_file> [output_dir]

Arguments:
    input_file: 输入文件路径 (.csv)
    output_dir: 输出目录（可选，默认为输入文件所在目录）

Example:
    python describe_table_skill.py /path/to/input.csv /path/to/output
    python describe_table_skill.py /path/to/input.csv  # 输出到 /path/to/
"""

import os
import sys
import asyncio
import argparse
import json
from typing import Any, Dict

import pandas as pd

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(script_dir))

from script.src import describe_single_table, get_llm_service
class DescribeTableSkill:
    """表格描述生成技能。

    生成表格的详细描述：列统计、摘要、样本数据。
    输入：文件路径
    输出：描述文本（JSON 格式）
    """

    def __init__(self, is_abstract: bool = True):
        """初始化描述生成技能。

        Args:
            is_abstract: 是否生成 LLM 摘要，默认为 True
        """
        self.is_abstract = is_abstract

    async def run(self, input_file: str, output_dir: str = None) -> Dict[str, Any]:
        """执行表格描述生成。

        Args:
            input_file: 输入文件路径
            output_dir: 输出目录（可选）

        Returns:
            包含以下键的字典：
                - description: 描述字典
                - description_text: 描述文本（JSON 字符串）
                - output_file: JSON 文件路径（如果保存）
                - success: 是否成功
        """
        if not os.path.exists(input_file):
            return {
                "description": {},
                "description_text": "",
                "output_file": "",
                "success": False,
                "error": f"文件不存在：{input_file}"
            }

        if not input_file.lower().endswith('.csv'):
            return {
                "description": {},
                "description_text": "",
                "output_file": "",
                "success": False,
                "error": f"不支持的文件格式：{input_file}，仅支持 .csv 文件"
            }

        if output_dir is None:
            output_dir = os.path.dirname(os.path.abspath(input_file))

        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}_description.json")

        try:
            df = await self._load_file(input_file)

            if df.empty:
                return {
                    "description": {},
                    "description_text": "",
                    "output_file": "",
                    "success": False,
                    "error": "数据为空"
                }

            size_type = 'small' if len(df) * len(df.columns) < 1500 else 'large'
            
            # 尝试获取 LLM 服务，如果未配置则跳过摘要生成
            llm_service = None
            if self.is_abstract:
                try:
                    llm_service = get_llm_service()
                except ValueError:
                    # LLM 未配置，跳过摘要生成
                    pass
            
            # 只有在成功获取 LLM 服务时才生成摘要
            should_generate_abstract = self.is_abstract and llm_service is not None

            description = await describe_single_table(
                df=df,
                size_type=size_type,
                is_abstract=should_generate_abstract,
                name=base_name,
                llm_service=llm_service
            )

            description['文件路径'] = input_file
            description['表内容'] = base_name

            # 递归转换 NaN 值为 None
            description = self._convert_nan_in_data(description)
            description_text = json.dumps(description, ensure_ascii=False, indent=2, default=self._default_dump)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(description_text)

            return {
                "description": description,
                "description_text": description_text,
                "output_file": output_file,
                "success": True,
                "output_dir": output_dir
            }
        except Exception as e:
            return {
                "description": {},
                "description_text": "",
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
            return pd.read_csv(file_path, header=0)
        except:
            return pd.read_csv(file_path, encoding='gbk', header=0)

    def _default_dump(self, obj):
        """JSON 序列化兼容处理。"""
        import numpy as np
        import math
        # 处理 NaN 值
        if isinstance(obj, float) and math.isnan(obj):
            return None
        if isinstance(obj, np.floating) and np.isnan(obj):
            return None
        if isinstance(obj, (pd.Timestamp, pd.DatetimeTZDtype)):
            return str(obj)
        elif isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_json()
        return str(obj)

    def _convert_nan_in_data(self, data):
        """递归转换数据中的 NaN 值为 None。"""
        import numpy as np
        import math

        if isinstance(data, dict):
            return {k: self._convert_nan_in_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_nan_in_data(item) for item in data]
        elif isinstance(data, float) and math.isnan(data):
            return None
        elif isinstance(data, np.floating) and np.isnan(data):
            return None
        elif isinstance(data, (np.integer, np.floating, np.bool_)):
            return data.item()
        elif isinstance(data, np.ndarray):
            return self._convert_nan_in_data(data.tolist())
        return data


async def run_skill(input_file: str, output_dir: str = None, is_abstract: bool = True) -> Dict[str, Any]:
    """运行表格描述生成技能。

    Args:
        input_file: 输入文件路径
        output_dir: 输出目录
        is_abstract: 是否生成 LLM 摘要

    Returns:
        描述结果
    """
    skill = DescribeTableSkill(is_abstract=is_abstract)
    return await skill.run(input_file, output_dir)


def main():
    parser = argparse.ArgumentParser(description="表格描述生成 Skill")
    parser.add_argument("input_file", help="输入文件路径 (.csv)")
    parser.add_argument("output_dir", nargs="?", default=None, help="输出目录（可选）")
    parser.add_argument("--no-abstract", action="store_true", help="禁用 LLM 摘要生成（默认启用，如果配置了LLM）")

    args = parser.parse_args()
    
    # 默认启用摘要生成，除非指定 --no-abstract
    is_abstract = not args.no_abstract

    print("=" * 60)
    print("Describe Table Skill")
    print("=" * 60)
    print(f"Input file: {args.input_file}")
    print(f"Output directory: {args.output_dir or '默认与输入同目录'}")
    print(f"Generate abstract: {is_abstract} (如果配置了LLM)")
    print()

    result = asyncio.run(run_skill(args.input_file, args.output_dir, is_abstract))

    if result["success"]:
        print(f"✓ 描述生成成功！")
        print()
        print("描述信息:")
        description = result.get("description", {})
        print(f"  表名：{description.get('表内容', 'N/A')}")
        print(f"  行数：{description.get('数据行数', 0)}")
        print(f"  列数：{len(description.get('数据列名', []))}")
        print(f"  大小类型：{description.get('size_type', 'N/A')}")

        if description.get('表描述'):
            print()
            print(f"  摘要：{description['表描述'][:100]}...")

        print()
        print(f"输出文件：{os.path.basename(result['output_file'])}")
    else:
        print(f"✗ 描述生成失败：{result.get('error', '未知错误')}")

    print("=" * 60)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
