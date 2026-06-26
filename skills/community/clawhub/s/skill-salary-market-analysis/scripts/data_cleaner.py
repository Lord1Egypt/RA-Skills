#!/usr/bin/env python3
"""
数据清洗工具
=============

功能：
1. 去除重复数据
2. 处理缺失值
3. 标准化格式
4. 识别异常值

使用方法：
    python3 data_cleaner.py -i data.csv -o clean_data.csv
"""

import argparse
import csv
import re
from collections import defaultdict


class SalaryDataCleaner:
    """薪酬数据清洗器"""

    def __init__(self, input_file):
        self.input_file = input_file
        self.data = []
        self.clean_data = []
        self.stats = {'removed': 0, 'fixed': 0}

    def load_data(self):
        """加载数据"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.data = list(reader)
        print(f"📂 加载 {len(self.data)} 条数据")

    def remove_duplicates(self):
        """去除重复数据"""
        seen = set()
        unique_data = []
        for row in self.data:
            # 基于岗位、公司、薪酬判断重复
            key = f"{row.get('position', '')}|{row.get('company_name', '')}|{row.get('salary_range', '')}"
            if key not in seen:
                seen.add(key)
                unique_data.append(row)
            else:
                self.stats['removed'] += 1

        self.data = unique_data
        print(f"✅ 去重完成：去除 {self.stats['removed']} 条重复数据")

    def standardize_salary(self):
        """标准化薪酬格式"""
        for row in self.data:
            salary = row.get('salary_range', '')
            if not salary:
                continue

            # 统一格式：15k-25k
            salary = salary.strip().lower()

            # 处理"万/年"
            if '万' in salary and '年' in salary:
                match = re.search(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)', salary)
                if match:
                    min_val = float(match.group(1)) * 10 / 12
                    max_val = float(match.group(2)) * 10 / 12
                    row['salary_range'] = f"{min_val:.0f}k-{max_val:.0f}k"
                    self.stats['fixed'] += 1

            # 处理单一薪资
            match = re.search(r'^(\d+(?:\.\d+)?)k$', salary)
            if match:
                val = float(match.group(1))
                row['salary_range'] = f"{val:.0f}k-{val:.0f}k"
                self.stats['fixed'] += 1

        print(f"✅ 薪酬标准化：修复 {self.stats['fixed']} 条")

    def handle_missing_values(self):
        """处理缺失值"""
        # 16 字段模板：position, company_name, salary_range 为必填
        required_fields = ['position', 'company_name', 'salary_range']

        cleaned = []
        for row in self.data:
            # 如果岗位和薪酬都为空则跳过
            if all(not row.get(f) for f in required_fields):
                self.stats['removed'] += 1
                continue
            cleaned.append(row)

        self.data = cleaned
        print(f"✅ 缺失值处理：去除 {self.stats['removed']} 条无效数据")

    def remove_outliers(self):
        """识别并移除异常值（使用 IQR 方法）"""
        # 提取薪酬中位值
        salaries = []
        for row in self.data:
            match = re.search(r'(\d+(?:\.\d+)?)', row.get('salary_range', ''))
            if match:
                salaries.append(float(match.group(1)))

        if len(salaries) < 4:
            return

        salaries_sorted = sorted(salaries)
        n = len(salaries_sorted)
        q1 = salaries_sorted[n // 4]
        q3 = salaries_sorted[3 * n // 4]
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        cleaned = []
        for row in self.data:
            match = re.search(r'(\d+(?:\.\d+)?)', row.get('salary_range', ''))
            if match:
                val = float(match.group(1))
                if lower_bound <= val <= upper_bound:
                    cleaned.append(row)
                else:
                    self.stats['removed'] += 1
            else:
                cleaned.append(row)

        self.data = cleaned
        print(f"✅ 异常值处理：移除 {self.stats['removed']} 条")

    def save(self, output_file):
        """保存清洗后的数据"""
        if not self.data:
            print("⚠️ 无数据可保存")
            return

        fieldnames = self.data[0].keys()
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)

        print(f"✅ 清洗完成：{len(self.data)} 条数据已保存到 {output_file}")

    def clean(self):
        """执行完整清洗流程"""
        self.load_data()
        self.remove_duplicates()
        self.handle_missing_values()
        self.standardize_salary()
        self.remove_outliers()
        return self.data


def main():
    parser = argparse.ArgumentParser(description='薪酬数据清洗工具')
    parser.add_argument('-i', '--input', required=True, help='输入文件')
    parser.add_argument('-o', '--output', required=True, help='输出文件')

    args = parser.parse_args()

    cleaner = SalaryDataCleaner(args.input)
    cleaner.clean()
    cleaner.save(args.output)


if __name__ == '__main__':
    main()
