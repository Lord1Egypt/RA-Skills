#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理Excel文件
处理tmp文件夹中所有.xlsx文件
"""

import os
import sys
import glob
from testcase_filter import process_excel

def main():
    # 指定输入文件夹
    input_dir = r"C:\Users\yanghua1\.claude\skills\testcase-filter\tmp"

    # 获取所有.xlsx文件
    excel_files = glob.glob(os.path.join(input_dir, "*.xlsx"))

    if not excel_files:
        print("未找到任何.xlsx文件")
        return

    print(f"找到 {len(excel_files)} 个Excel文件：")
    for file in excel_files:
        print(f"  {os.path.basename(file)}")

    # 为每个文件创建输出文件
    for input_file in excel_files:
        # 获取文件名（不含扩展名）
        filename = os.path.splitext(os.path.basename(input_file))[0]

        # 创建输出文件名
        output_file = os.path.join(input_dir, f"{filename}_筛选后.xlsx")

        print(f"\n处理: {os.path.basename(input_file)}")
        print(f"输出: {os.path.basename(output_file)}")

        try:
            result = process_excel(input_file, output_file)
            print(f"处理完成！处理了 {result['processed']} 个sheet，跳过了 {result['skipped']} 个sheet")
        except Exception as e:
            print(f"处理失败: {str(e)}")

    print(f"\n所有文件处理完成！")

if __name__ == '__main__':
    main()