#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import pandas as pd
import argparse


"""
Excel分组导出脚本
功能：读取Excel文件，按指定列分组，将相同组的数据导出到新文件
文件命名格式：a_b_c.xlsx（使用分组列的值组合）
"""
def export(input_file, output_dir="./output", group_columns=['渠道组', '实重区间', '周长区间']):
    """
    读取 Excel 文件，按照指定的列 a, b, c 进行分组，
    将相同组的数据导出到新文件，文件命名用 a+b+c 命名

    :param input_file: 输入的 Excel 文件路径
    :param output_dir: 输出目录
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取 Excel 文件
    df = pd.read_excel(input_file)

    # 检查必要的列是否存在
    for col in group_columns:
        if col not in df.columns:
            raise ValueError(f"Excel 文件中缺少必要的列: {col}")

    # 按照 a, b, c 列进行分组
    grouped = df.groupby(group_columns)

    # 遍历每个分组并导出
    for (a_val, b_val, c_val), group_df in grouped:
        # 生成文件名 (处理特殊字符，避免文件名非法)
        safe_a = str(a_val).replace('/', '_').replace('\\', '_').replace(':', '_')
        safe_b = str(b_val).replace('/', '_').replace('\\', '_').replace(':', '_')
        safe_c = str(c_val).replace('/', '_').replace('\\', '_').replace(':', '_')

        filename = f"{safe_a}_{safe_b}_{safe_c}.xlsx"
        output_path = os.path.join(output_dir, filename)

        # 邮编列进行去重
        group_df = group_df.drop_duplicates(subset=['邮编'])

        # 增加开始邮编列. 值等于 邮编列的值
        group_df.insert(3, '开始邮编', group_df['邮编'])
        # 增加技术邮编列. 值等于 邮编列的值
        group_df.insert(4, '结束邮编', group_df['邮编'])

        # 删除 渠道组, 实重区间, 周长区间 列
        group_df.drop(['邮编','渠道组', '实重区间', '周长区间'], axis=1, inplace=True)

        # 导出的文件需要增加 分区名称 列. 默认值 1
        group_df.insert(0, '分区名称', 1)
        # 增加国家二字码列 默认值 US
        group_df.insert(1, '国家二字码', 'US')
        # 增加城市列默认值 空
        group_df.insert(2, '城市', '')

        # 导出到新的 Excel 文件
        group_df.to_excel(output_path, index=False)

        print(f"已导出: {output_path} (共 {len(group_df)} 行数据)")

    print(f"\n分组完成！共导出 {len(grouped)} 个文件到 {output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Excel数据分组导出工具')
    parser.add_argument('--input', '-i', required=True, help='输入Excel文件路径')
    parser.add_argument('--columns', '-c', required=True, help='分组列名，用逗号分隔，如：a,b,c')
    parser.add_argument('--output-dir', '-o', default='./grouped_output', help='输出目录')


    args = parser.parse_args()

    group_columns = [col.strip() for col in args.columns.split(',')]
    export(input_file=args.input, output_dir=args.output_dir, group_columns=group_columns)


if __name__ == "__main__":
    main()