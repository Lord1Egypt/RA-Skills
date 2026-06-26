#!/usr/bin/env python3
"""
基础数据处理器
===============

功能：
1. 加载薪酬数据
2. 基本统计分析
3. 数据导出

使用方法：
    python3 data_processor.py -i data.csv
"""

import argparse
import csv
import json
import sys


class SalaryDataProcessor:
    """薪酬数据处理器"""

    def __init__(self, input_file):
        self.input_file = input_file
        self.data = []

    def load_data(self):
        """加载数据"""
        if self.input_file.endswith('.csv'):
            with open(self.input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
        elif self.input_file.endswith('.json'):
            with open(self.input_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        print(f"✅ 加载 {len(self.data)} 条数据")
        return self.data

    def get_statistics(self):
        """获取基本统计信息"""
        if not self.data:
            return {}

        positions = {}
        for row in self.data:
            pos = row.get('position', '未知')
            if pos not in positions:
                positions[pos] = 0
            positions[pos] += 1

        return {
            'total': len(self.data),
            'positions': positions,
            'sources': list(set(row.get('source', '未知') for row in self.data))
        }

    def filter_by_location(self, location):
        """按地点过滤"""
        return [row for row in self.data if location.lower() in row.get('location', '').lower()]

    def filter_by_level(self, level):
        """按级别过滤"""
        return [row for row in self.data if level in row.get('level', '')]

    def export_json(self, output_file):
        """导出为 JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"✅ 导出到 {output_file}")


def main():
    parser = argparse.ArgumentParser(description='薪酬数据处理器')
    parser.add_argument('-i', '--input', required=True, help='输入文件')
    parser.add_argument('-l', '--location', help='按地点过滤')
    parser.add_argument('--level', help='按级别过滤')
    parser.add_argument('-o', '--output', help='输出文件')

    args = parser.parse_args()

    processor = SalaryDataProcessor(args.input)
    processor.load_data()

    if args.location:
        processor.data = processor.filter_by_location(args.location)

    if args.level:
        processor.data = processor.filter_by_level(args.level)

    stats = processor.get_statistics()
    print(f"\n📊 统计信息：")
    print(f"  总数：{stats['total']}")
    print(f"  岗位：{stats['positions']}")

    if args.output:
        processor.export_json(args.output)


if __name__ == '__main__':
    main()
