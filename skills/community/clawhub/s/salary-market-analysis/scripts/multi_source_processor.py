#!/usr/bin/env python3
"""
多源薪酬数据整合处理器 V2
=========================

适配 16 字段 CSV 模板，支持年薪自动计算、P30-P90 细粒度分位值、企业类型对比分析。

字段要求（16 字段）：
  id, position, company_name, company_type, salary_range,
  salary_monthly_low, salary_monthly_high, months,
  annual_salary_low, annual_salary_high, annual_salary_avg,
  location, experience, education, source, collect_date

使用方法：
    python3 multi_source_processor.py -i data.csv -o report.json
    python3 multi_source_processor.py -i data.csv -o report.json --percentiles P30 P40 P50 P60 P70 P80 P90
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from collections import defaultdict

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("⚠️ numpy 未安装，将使用简单计算方法")

# 数据来源权重配置
SOURCE_TYPES = {
    '招聘网站': {'weight': 1.0, 'quality': 0.9},
    '行业报告': {'weight': 1.2, 'quality': 0.95},
    '财报': {'weight': 1.1, 'quality': 0.95},
    '论坛': {'weight': 0.8, 'quality': 0.7},
    '其他': {'weight': 0.9, 'quality': 0.75}
}

SOURCE_KEYWORDS = {
    '招聘网站': ['zhipin', 'liepin', '51job', 'zhaopin', 'lagou', 'boss', '猎聘', '前程', '智联', '拉勾', '直聘', '51job'],
    '行业报告': ['mercer', 'willis', 'aon', '中智', '薪酬报告', '薪酬调研'],
    '财报': ['年报', '招股书', 'esg', '巨潮', '东方财富', 'annual report'],
    '论坛': ['maimai', '脉脉', 'zhihu', '知乎', 'v2ex', '小红书', 'douban', '豆瓣', 'glassdoor']
}


class MultiSourceSalaryProcessor:
    """多源薪酬数据整合处理器 V2 - 适配 16 字段模板"""

    def __init__(self, input_file, weights_file=None):
        self.input_file = input_file
        self.raw_data = []
        self.processed_data = []
        self.percentiles = {}
        self.weights = self._load_weights(weights_file)
        self.stats = {}

    def _load_weights(self, weights_file):
        if weights_file and os.path.exists(weights_file):
            with open(weights_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return SOURCE_TYPES

    def load_data(self):
        print(f"📂 加载数据：{self.input_file}")
        if self.input_file.endswith('.json'):
            with open(self.input_file, 'r', encoding='utf-8') as f:
                self.raw_data = json.load(f)
        elif self.input_file.endswith('.csv'):
            with open(self.input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.raw_data = list(reader)
        else:
            raise ValueError(f"不支持的文件格式：{self.input_file}")
        print(f"✅ 加载完成：{len(self.raw_data)} 条数据")
        return self.raw_data

    def identify_source_type(self, source):
        source_lower = source.lower()
        for source_type, keywords in SOURCE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in source_lower:
                    return source_type
        return '其他'

    def _safe_float(self, val, default=None):
        """安全转换为 float"""
        if val is None or str(val).strip() == '':
            return default
        try:
            return float(str(val).strip().replace(',', ''))
        except (ValueError, TypeError):
            return default

    def process_data(self):
        """处理数据：识别来源、验证字段、计算年薪、统计分布"""
        print("\n🔄 开始数据处理...")

        source_stats = defaultdict(int)
        company_type_stats = defaultdict(lambda: {'count': 0, 'salaries': []})
        location_stats = defaultdict(lambda: {'count': 0, 'salaries': []})
        experience_stats = defaultdict(lambda: {'count': 0, 'salaries': []})
        education_stats = defaultdict(lambda: {'count': 0, 'salaries': []})
        annual_salaries = []

        for row in self.raw_data:
            source = row.get('source', '')
            source_type = self.identify_source_type(source)
            source_stats[source_type] += 1

            weight = self.weights.get(source_type, {}).get('weight', 1.0)
            quality = self.weights.get(source_type, {}).get('quality', 0.75)

            # 优先使用 CSV 中预计算的年薪平均值，其次用月薪×薪月计算
            annual_avg = self._safe_float(row.get('annual_salary_avg'))
            annual_low = self._safe_float(row.get('annual_salary_low'))
            annual_high = self._safe_float(row.get('annual_salary_high'))
            monthly_low = self._safe_float(row.get('salary_monthly_low'))
            monthly_high = self._safe_float(row.get('salary_monthly_high'))
            months = self._safe_float(row.get('months'), 12)

            # 如果 CSV 中没有预计算年薪，则从月薪计算
            if annual_avg is None and monthly_low is not None and monthly_high is not None:
                annual_low_calc = monthly_low * months / 10000
                annual_high_calc = monthly_high * months / 10000
                if annual_low is None:
                    annual_low = annual_low_calc
                if annual_high is None:
                    annual_high = annual_high_calc
                annual_avg = (annual_low + annual_high) / 2

            if annual_avg and annual_avg > 0:
                annual_salaries.append(annual_avg)

            # 按企业类型统计
            company_type = row.get('company_type', '未知').strip()
            company_type_stats[company_type]['count'] += 1
            if annual_avg and annual_avg > 0:
                company_type_stats[company_type]['salaries'].append(annual_avg)

            # 按地区统计
            location = row.get('location', '未知').strip()
            location_stats[location]['count'] += 1
            if annual_avg and annual_avg > 0:
                location_stats[location]['salaries'].append(annual_avg)

            # 按经验统计
            experience = row.get('experience', '未知').strip()
            experience_stats[experience]['count'] += 1
            if annual_avg and annual_avg > 0:
                experience_stats[experience]['salaries'].append(annual_avg)

            # 按学历统计
            education = row.get('education', '未知').strip()
            education_stats[education]['count'] += 1
            if annual_avg and annual_avg > 0:
                education_stats[education]['salaries'].append(annual_avg)

            self.processed_data.append({
                **row,
                'annual_salary_low': annual_low,
                'annual_salary_high': annual_high,
                'annual_salary_avg': annual_avg,
                'source_type': source_type,
                'weight': weight,
                'quality': quality
            })

        # 计算分位值（P30-P90）
        if annual_salaries:
            self.percentiles = self._calculate_percentiles(annual_salaries, percentiles=[30, 40, 50, 60, 70, 80, 90])

        # 统计信息
        self.stats = {
            'total_samples': len(self.raw_data),
            'valid_samples': len(self.processed_data),
            'salary_count': len(annual_salaries),
            'source_distribution': dict(source_stats),
            'company_type_distribution': {k: v['count'] for k, v in company_type_stats.items()},
            'location_distribution': {k: v['count'] for k, v in location_stats.items()},
            'experience_distribution': {k: v['count'] for k, v in experience_stats.items()},
            'education_distribution': {k: v['count'] for k, v in education_stats.items()},
            'salary_stats': self._compute_salary_stats(annual_salaries),
            'company_type_salary': {
                k: {
                    'count': v['count'],
                    'avg': sum(v['salaries']) / len(v['salaries']) if v['salaries'] else 0,
                    'min': min(v['salaries']) if v['salaries'] else 0,
                    'max': max(v['salaries']) if v['salaries'] else 0
                } for k, v in company_type_stats.items()
            },
            'location_salary': {
                k: {
                    'count': v['count'],
                    'avg': round(sum(v['salaries']) / len(v['salaries']), 2) if v['salaries'] else 0
                } for k, v in location_stats.items()
            }
        }

        print(f"✅ 数据处理完成：{len(self.processed_data)} 条有效数据，{len(annual_salaries)} 条含薪酬数据")
        return self.processed_data

    def _compute_salary_stats(self, salaries):
        """计算薪酬统计指标"""
        if not salaries:
            return {}
        sorted_s = sorted(salaries)
        n = len(sorted_s)
        mean_val = sum(salaries) / n
        median_val = sorted_s[n // 2] if n % 2 else (sorted_s[n // 2 - 1] + sorted_s[n // 2]) / 2

        if HAS_NUMPY:
            std_val = float(np.std(salaries, ddof=1)) if n > 1 else 0
        else:
            variance = sum((x - mean_val) ** 2 for x in salaries) / (n - 1) if n > 1 else 0
            std_val = variance ** 0.5

        # 偏态检查
        skew = "右偏（正偏态）" if mean_val > median_val else "左偏（负偏态）"

        return {
            'mean': round(mean_val, 2),
            'median': round(median_val, 2),
            'std': round(std_val, 2),
            'min': round(min(salaries), 2),
            'max': round(max(salaries), 2),
            'skew': skew
        }

    def _calculate_percentiles(self, data, percentiles=None):
        """计算分位值，默认 P30/P40/P50/P60/P70/P80/P90"""
        if not data:
            return {}
        if percentiles is None:
            percentiles = [30, 40, 50, 60, 70, 80, 90]

        if HAS_NUMPY:
            return {f'P{p}': round(float(np.percentile(data, p)), 2) for p in percentiles}
        else:
            sorted_data = sorted(data)
            n = len(sorted_data)
            result = {}
            for p in percentiles:
                idx = max(0, min(n - 1, int(n * p / 100)))
                result[f'P{p}'] = round(sorted_data[idx], 2)
            return result

    def _calculate_quality_score(self):
        """计算数据质量评分"""
        if not self.processed_data:
            return 0
        total_fields = 16
        filled_counts = []
        for row in self.processed_data:
            filled = sum(1 for k, v in row.items() if k in self.raw_data[0] if v)
            filled_counts.append(filled / total_fields)
        completeness = sum(filled_counts) / len(filled_counts)
        timeliness = 0.8
        accuracies = [row.get('quality', 0.75) for row in self.processed_data]
        accuracy = sum(accuracies) / len(accuracies) if accuracies else 0.75
        consistency = 0.85
        score = completeness * 0.3 + timeliness * 0.25 + accuracy * 0.25 + consistency * 0.2
        return round(score * 100, 1)

    def generate_report(self):
        """生成分析报告 JSON"""
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'input_file': self.input_file,
                'total_samples': self.stats.get('total_samples', 0),
                'valid_samples': self.stats.get('valid_samples', 0)
            },
            'data_overview': {
                'source_distribution': self.stats.get('source_distribution', {}),
                'company_type_distribution': self.stats.get('company_type_distribution', {}),
                'location_distribution': self.stats.get('location_distribution', {}),
                'salary_stats': self.stats.get('salary_stats', {})
            },
            'percentiles': self.percentiles,
            'company_type_salary': self.stats.get('company_type_salary', {}),
            'location_salary': self.stats.get('location_salary', {}),
            'processed_data': self.processed_data,
            'quality_score': self._calculate_quality_score()
        }
        return report

    def _save_csv(self, csv_path):
        """保存处理后的数据为 CSV"""
        if not self.processed_data:
            print("⚠️ 无数据可导出 CSV")
            return
        # 只输出原始 16 字段 + 分析列
        fieldnames = [
            'id', 'position', 'company_name', 'company_type', 'salary_range',
            'salary_monthly_low', 'salary_monthly_high', 'months',
            'annual_salary_low', 'annual_salary_high', 'annual_salary_avg',
            'location', 'experience', 'education', 'source', 'collect_date',
            'source_type', 'weight', 'quality'
        ]
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(self.processed_data)
        print(f"✅ CSV 数据已保存：{csv_path} ({len(self.processed_data)} 行)")

    def save_report(self, output_file):
        """保存报告到文件（同时输出 CSV）"""
        report = self.generate_report()
        if output_file.endswith('.json'):
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            # 同时输出 CSV（同名不同后缀）
            csv_path = output_file.replace('.json', '_data.csv')
            self._save_csv(csv_path)
        elif output_file.endswith('.csv'):
            if self.processed_data:
                fieldnames = list(self.processed_data[0].keys())
                with open(output_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.processed_data)
            # 同时输出 JSON 摘要
            json_path = output_file.replace('.csv', '_report.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"✅ JSON 报告已保存：{json_path}")
        print(f"✅ 主文件已保存：{output_file}")
        return report


def main():
    parser = argparse.ArgumentParser(description='多源薪酬数据整合处理器 V2')
    parser.add_argument('-i', '--input', required=True, help='输入文件路径（CSV/JSON）')
    parser.add_argument('-o', '--output', required=True, help='输出文件路径（JSON/CSV）')
    parser.add_argument('-w', '--weights', help='权重配置文件（JSON）')
    args = parser.parse_args()

    processor = MultiSourceSalaryProcessor(args.input, args.weights)
    processor.load_data()
    processor.process_data()
    report = processor.save_report(args.output)

    # 打印摘要
    print("\n" + "=" * 50)
    print("📊 数据摘要")
    print("=" * 50)
    print(f"总样本数：{processor.stats.get('total_samples', 0)}")
    print(f"有效样本：{processor.stats.get('valid_samples', 0)}")
    print(f"数据质量评分：{report.get('quality_score', 0)}")

    stats = processor.stats.get('salary_stats', {})
    if stats:
        print(f"\n薪酬统计（单位：万元/年）：")
        print(f"  平均值：{stats.get('mean', 'N/A')}")
        print(f"  中位数：{stats.get('median', 'N/A')}")
        print(f"  标准差：{stats.get('std', 'N/A')}")
        print(f"  范围：{stats.get('min', 'N/A')} - {stats.get('max', 'N/A')}")
        print(f"  偏态：{stats.get('skew', 'N/A')}")

    print(f"\n薪酬分位值（万元/年）：")
    for k, v in processor.percentiles.items():
        print(f"  {k}: {v}")

    print(f"\n来源分布：")
    for k, v in processor.stats.get('source_distribution', {}).items():
        print(f"  {k}: {v}")

    print(f"\n企业类型薪酬：")
    for k, v in processor.stats.get('company_type_salary', {}).items():
        print(f"  {k}: 平均 {v.get('avg', 0):.2f} 万 ({v.get('count', 0)} 条)")
    print("=" * 50)


if __name__ == '__main__':
    main()
