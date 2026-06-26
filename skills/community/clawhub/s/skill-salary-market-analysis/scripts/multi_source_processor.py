#!/usr/bin/env python3
"""
多源薪酬数据整合处理器 V3 (支持海外薪酬分析)
=============================================

适配 16/24 字段 CSV 模板，支持：
- 年薪自动计算
- P30-P90 细粒度分位值
- 企业类型对比分析
- 多币种自动换算（USD/EUR/GBP/JPY/SGD 等）
- PPP 购买力平价调整（基于国别薪酬系数矩阵 v2.0）
- 按国家/地区分组的全球薪酬对比

使用方法：
    # 国内薪酬分析（默认）
    python3 multi_source_processor.py -i data.csv -o report.json

    # 海外薪酬分析（自动换算到 USD）
    python3 multi_source_processor.py -i data.csv -o report.json --target-currency USD

    # PPP 购买力平价调整（以中国为基准）
    python3 multi_source_processor.py -i data.csv -o report.json --with-ppp

    # 指定 PPP 对标国家
    python3 multi_source_processor.py -i data.csv -o report.json --with-ppp --ppp-base-country US
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
    '招聘网站': ['zhipin', 'liepin', '51job', 'zhaopin', 'lagou', 'boss', '猎聘', '前程', '智联', '拉勾', '直聘', '51job', 'linkedin', 'glassdoor', 'indeed', 'payscale'],
    '行业报告': ['mercer', 'willis', 'aon', '中智', '薪酬报告', '薪酬调研', 'robert half', 'michael page'],
    '财报': ['年报', '招股书', 'esg', '巨潮', '东方财富', 'annual report', 'sec filing', '10-k'],
    '论坛': ['maimai', '脉脉', 'zhihu', '知乎', 'v2ex', '小红书', 'douban', '豆瓣', 'glassdoor', 'reddit', 'blind']
}

# 汇率表（2026-05 基准，1 单位外币 = ? 人民币）
EXCHANGE_RATES_TO_CNY = {
    'CNY': 1.0, 'USD': 7.20, 'EUR': 7.85, 'GBP': 9.15,
    'JPY': 0.048, 'KRW': 0.0052, 'SGD': 5.40, 'HKD': 0.92,
    'TWD': 0.22, 'THB': 0.21, 'MYR': 1.62, 'INR': 0.086,
    'VND': 0.00029, 'PHP': 0.126, 'IDR': 0.00045,
    'AUD': 4.72, 'CAD': 5.25, 'CHF': 8.10, 'AED': 1.96,
    'BRL': 1.28, 'MXN': 0.38, 'ZAR': 0.39,
    'NZD': 4.35, 'SEK': 0.70, 'NOK': 0.69, 'DKK': 1.05,
    'RUB': 0.082,
}

# PPP 综合系数（基准：中国大陆 = 1.00）
PPP_COEFFICIENTS = {
    '中国': 1.00, 'China': 1.00, 'CN': 1.00, '中国大陆': 1.00,
    '瑞士': 3.57, 'Switzerland': 3.57, 'CH': 3.57,
    '美国': 2.58, 'USA': 2.58, 'US': 2.58, 'United States': 2.58,
    '新加坡': 2.53, 'Singapore': 2.53, 'SG': 2.53,
    '中国香港': 1.99, 'Hong Kong': 1.99, 'HK': 1.99,
    '英国': 1.96, 'UK': 1.96, 'GB': 1.96, 'United Kingdom': 1.96,
    '阿联酋': 1.94, 'UAE': 1.94, 'AE': 1.94, '迪拜': 1.94, 'Dubai': 1.94,
    '欧洲': 1.90, 'Europe': 1.90, 'EU': 1.90, '欧元区': 1.90,
    '德国': 1.90, 'Germany': 1.90, 'DE': 1.90,
    '法国': 1.90, 'France': 1.90, 'FR': 1.90,
    '日本': 1.64, 'Japan': 1.64, 'JP': 1.64,
    '韩国': 1.63, 'Korea': 1.63, 'KR': 1.63, 'South Korea': 1.63,
    '中国台湾': 1.45, 'Taiwan': 1.45, 'TW': 1.45,
    '马来西亚': 0.90, 'Malaysia': 0.90, 'MY': 0.90,
    '泰国': 0.74, 'Thailand': 0.74, 'TH': 0.74,
    '越南': 0.65, 'Vietnam': 0.65, 'VN': 0.65,
    '菲律宾': 0.60, 'Philippines': 0.60, 'PH': 0.60,
    '印尼': 0.58, 'Indonesia': 0.58, 'ID': 0.58,
    '印度': 0.58, 'India': 0.58, 'IN': 0.58,
    '澳大利亚': 2.20, 'Australia': 2.20, 'AU': 2.20,
    '加拿大': 2.10, 'Canada': 2.10, 'CA': 2.10,
    '巴西': 0.75, 'Brazil': 0.75, 'BR': 0.75,
    '墨西哥': 0.65, 'Mexico': 0.65, 'MX': 0.65,
    '南非': 0.55, 'South Africa': 0.55, 'ZA': 0.55,
    '新西兰': 2.00, 'New Zealand': 2.00, 'NZ': 2.00,
    '瑞典': 2.00, 'Sweden': 2.00, 'SE': 2.00,
    '挪威': 2.10, 'Norway': 2.10, 'NO': 2.10,
    '丹麦': 1.95, 'Denmark': 1.95, 'DK': 1.95,
    '俄罗斯': 0.50, 'Russia': 0.50, 'RU': 0.50,
}

# 国家/地区 → 货币映射
COUNTRY_TO_CURRENCY = {
    '中国': 'CNY', 'China': 'CNY', 'CN': 'CNY', '中国大陆': 'CNY',
    '美国': 'USD', 'USA': 'USD', 'US': 'USD', 'United States': 'USD',
    '英国': 'GBP', 'UK': 'GBP', 'GB': 'GBP', 'United Kingdom': 'GBP',
    '德国': 'EUR', 'Germany': 'EUR', 'DE': 'EUR', '法国': 'EUR', 'France': 'EUR',
    'FR': 'EUR', '日本': 'JPY', 'Japan': 'JPY', 'JP': 'JPY',
    '韩国': 'KRW', 'Korea': 'KRW', 'KR': 'KRW', 'South Korea': 'KRW',
    '新加坡': 'SGD', 'Singapore': 'SGD', 'SG': 'SGD',
    '香港': 'HKD', 'Hong Kong': 'HKD', 'HK': 'HKD', '中国香港': 'HKD',
    '台湾': 'TWD', 'Taiwan': 'TWD', 'TW': 'TWD', '中国台湾': 'TWD',
    '泰国': 'THB', 'Thailand': 'THB', 'TH': 'THB',
    '马来西亚': 'MYR', 'Malaysia': 'MYR', 'MY': 'MYR',
    '印度': 'INR', 'India': 'INR', 'IN': 'INR',
    '越南': 'VND', 'Vietnam': 'VND', 'VN': 'VND',
    '菲律宾': 'PHP', 'Philippines': 'PHP', 'PH': 'PHP',
    '印尼': 'IDR', 'Indonesia': 'IDR', 'ID': 'IDR',
    '澳大利亚': 'AUD', 'Australia': 'AUD', 'AU': 'AUD',
    '加拿大': 'CAD', 'Canada': 'CAD', 'CA': 'CAD',
    '瑞士': 'CHF', 'Switzerland': 'CHF', 'CH': 'CHF',
    '阿联酋': 'AED', 'UAE': 'AED', 'AE': 'AED', '迪拜': 'AED', 'Dubai': 'AED',
    '巴西': 'BRL', 'Brazil': 'BRL', 'BR': 'BRL',
    '墨西哥': 'MXN', 'Mexico': 'MXN', 'MX': 'MXN',
    '南非': 'ZAR', 'South Africa': 'ZAR', 'ZA': 'ZAR',
    '新西兰': 'NZD', 'New Zealand': 'NZD', 'NZ': 'NZD',
    '瑞典': 'SEK', 'Sweden': 'SEK', 'SE': 'SEK',
    '挪威': 'NOK', 'Norway': 'NOK', 'NO': 'NOK',
    '丹麦': 'DKK', 'Denmark': 'DKK', 'DK': 'DKK',
    '俄罗斯': 'RUB', 'Russia': 'RUB', 'RU': 'RUB',
}


class MultiSourceSalaryProcessor:
    """多源薪酬数据整合处理器 V3 - 支持海外薪酬分析 + 多币种 + PPP"""

    def __init__(self, input_file, weights_file=None, target_currency='CNY',
                 enable_ppp=False, ppp_base_country='中国'):
        self.input_file = input_file
        self.raw_data = []
        self.processed_data = []
        self.percentiles = {}
        self.weights = self._load_weights(weights_file)
        self.stats = {}
        self.target_currency = target_currency.upper()
        self.enable_ppp = enable_ppp
        self.ppp_base_country = ppp_base_country

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

    def convert_currency(self, amount, from_currency, to_currency=None):
        """货币换算：通过 CNY 作为中间货币"""
        if to_currency is None:
            to_currency = self.target_currency
        from_upper = from_currency.upper()
        to_upper = to_currency.upper()
        if from_upper == to_upper:
            return amount
        rate_from = EXCHANGE_RATES_TO_CNY.get(from_upper)
        if rate_from is None:
            return amount  # 无法换算，返回原值
        amount_cny = amount * rate_from
        rate_to = EXCHANGE_RATES_TO_CNY.get(to_upper, 1.0)
        return amount_cny / rate_to

    def auto_detect_country(self, row):
        """自动推断国家/地区"""
        country = row.get('country', '').strip()
        if country:
            return country
        location = row.get('location', '').strip()
        if not location:
            return ''
        for key in PPP_COEFFICIENTS.keys():
            if key in location:
                return key
        return ''

    def auto_detect_currency(self, row, country):
        """自动推断货币"""
        currency = row.get('currency', '').strip().upper()
        if currency and currency in EXCHANGE_RATES_TO_CNY:
            return currency
        if country:
            return COUNTRY_TO_CURRENCY.get(country, 'CNY')
        return 'CNY'

    def calculate_ppp_adjusted(self, salary_cny, from_country):
        """购买力平价调整：返回在基准国家达到同等购买力需要的 CNY"""
        from_coeff = PPP_COEFFICIENTS.get(from_country, 1.0)
        to_coeff = PPP_COEFFICIENTS.get(self.ppp_base_country, 1.0)
        if from_coeff == 0:
            return salary_cny
        return salary_cny / from_coeff * to_coeff

    def process_data(self):
        """处理数据：识别来源、币种换算、年薪计算、PPP 调整、统计分布"""
        print(f"\n🔄 开始数据处理... (目标货币: {self.target_currency})")
        if self.enable_ppp:
            print(f"📊 PPP 购买力对标: {self.ppp_base_country}")

        source_stats = defaultdict(int)
        company_type_stats = defaultdict(lambda: {'count': 0, 'salaries': []})
        location_stats = defaultdict(lambda: {'count': 0, 'salaries': []})
        country_stats = defaultdict(lambda: {'count': 0, 'salaries_cny': [], 'salaries_target': []})
        experience_stats = defaultdict(lambda: {'count': 0, 'salaries': []})
        education_stats = defaultdict(lambda: {'count': 0, 'salaries': []})
        annual_salaries = []
        annual_salaries_usd = []

        for row in self.raw_data:
            source = row.get('source', '')
            source_type = self.identify_source_type(source)
            source_stats[source_type] += 1

            weight = self.weights.get(source_type, {}).get('weight', 1.0)
            quality = self.weights.get(source_type, {}).get('quality', 0.75)

            # 自动推断国家和货币
            country = self.auto_detect_country(row)
            currency = self.auto_detect_currency(row, country)
            row['country'] = country
            row['currency'] = currency

            # 优先使用 CSV 中预计算的年薪平均值
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

            # 货币换算到目标货币
            if currency and currency.upper() != self.target_currency and annual_avg:
                annual_avg = self.convert_currency(annual_avg, currency)
                if annual_low:
                    annual_low = self.convert_currency(annual_low, currency)
                if annual_high:
                    annual_high = self.convert_currency(annual_high, currency)

            # 统一换算到 USD（用于全球对标）
            salary_usd = None
            if annual_avg:
                salary_usd = self.convert_currency(annual_avg, self.target_currency, 'USD')

            # PPP 购买力平价调整
            ppp_adjusted = None
            if self.enable_ppp and country and annual_avg:
                salary_cny = self.convert_currency(annual_avg, self.target_currency, 'CNY')
                ppp_adjusted = self.calculate_ppp_adjusted(salary_cny, country)

            if annual_avg and annual_avg > 0:
                annual_salaries.append(annual_avg)
                if salary_usd:
                    annual_salaries_usd.append(salary_usd)

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

            # 按国家/地区统计（海外薪酬新增）
            if country:
                salary_cny_for_country = self.convert_currency(annual_avg, self.target_currency, 'CNY')
                country_stats[country]['count'] += 1
                if annual_avg > 0:
                    country_stats[country]['salaries_cny'].append(salary_cny_for_country)
                    country_stats[country]['salaries_target'].append(annual_avg)

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
                'annual_salary_low': round(annual_low, 2) if annual_low else annual_low,
                'annual_salary_high': round(annual_high, 2) if annual_high else annual_high,
                'annual_salary_avg': round(annual_avg, 2) if annual_avg else annual_avg,
                'annual_salary_usd': round(salary_usd, 2) if salary_usd else None,
                'ppp_adjusted': round(ppp_adjusted, 2) if ppp_adjusted else None,
                'source_type': source_type,
                'weight': weight,
                'quality': quality
            })

        # 计算分位值
        if annual_salaries:
            self.percentiles = self._calculate_percentiles(annual_salaries)

        # 统计信息
        self.stats = {
            'total_samples': len(self.raw_data),
            'valid_samples': len(self.processed_data),
            'salary_count': len(annual_salaries),
            'source_distribution': dict(source_stats),
            'company_type_distribution': {k: v['count'] for k, v in company_type_stats.items()},
            'location_distribution': {k: v['count'] for k, v in location_stats.items()},
            'country_distribution': {k: v['count'] for k, v in country_stats.items()},
            'experience_distribution': {k: v['count'] for k, v in experience_stats.items()},
            'education_distribution': {k: v['count'] for k, v in education_stats.items()},
            'salary_stats': self._compute_salary_stats(annual_salaries),
            'salary_stats_usd': self._compute_salary_stats(annual_salaries_usd) if annual_salaries_usd else {},
            'company_type_salary': {
                k: {
                    'count': v['count'],
                    'avg': round(sum(v['salaries']) / len(v['salaries']), 2) if v['salaries'] else 0,
                    'min': round(min(v['salaries']), 2) if v['salaries'] else 0,
                    'max': round(max(v['salaries']), 2) if v['salaries'] else 0
                } for k, v in company_type_stats.items()
            },
            'location_salary': {
                k: {
                    'count': v['count'],
                    'avg': round(sum(v['salaries']) / len(v['salaries']), 2) if v['salaries'] else 0
                } for k, v in location_stats.items()
            },
            'country_salary': {
                k: {
                    'count': v['count'],
                    'avg_cny': round(sum(v['salaries_cny']) / len(v['salaries_cny']), 2) if v['salaries_cny'] else 0,
                    'avg_target': round(sum(v['salaries_target']) / len(v['salaries_target']), 2) if v['salaries_target'] else 0,
                    'ppp_coefficient': PPP_COEFFICIENTS.get(k, 1.0)
                } for k, v in country_stats.items()
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
        """计算分位值"""
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
        total_fields = len(self.raw_data[0].keys()) if self.raw_data else 20
        filled_counts = []
        for row in self.processed_data:
            filled = sum(1 for v in row.values() if v)
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
                'target_currency': self.target_currency,
                'ppp_enabled': self.enable_ppp,
                'ppp_base_country': self.ppp_base_country,
                'total_samples': self.stats.get('total_samples', 0),
                'valid_samples': self.stats.get('valid_samples', 0)
            },
            'data_overview': {
                'source_distribution': self.stats.get('source_distribution', {}),
                'company_type_distribution': self.stats.get('company_type_distribution', {}),
                'location_distribution': self.stats.get('location_distribution', {}),
                'country_distribution': self.stats.get('country_distribution', {}),
                'salary_stats': self.stats.get('salary_stats', {}),
                'salary_stats_usd': self.stats.get('salary_stats_usd', {})
            },
            'percentiles': self.percentiles,
            'company_type_salary': self.stats.get('company_type_salary', {}),
            'location_salary': self.stats.get('location_salary', {}),
            'country_salary': self.stats.get('country_salary', {}),
            'processed_data': self.processed_data,
            'quality_score': self._calculate_quality_score()
        }
        return report

    def _save_csv(self, csv_path):
        """保存处理后的数据为 CSV"""
        if not self.processed_data:
            print("⚠️ 无数据可导出 CSV")
            return
        fieldnames = list(self.processed_data[0].keys())
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(self.processed_data)
        print(f"✅ CSV 数据已保存：{csv_path} ({len(self.processed_data)} 行)")

    def save_report(self, output_file):
        """保存报告到文件"""
        report = self.generate_report()
        if output_file.endswith('.json'):
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            csv_path = output_file.replace('.json', '_data.csv')
            self._save_csv(csv_path)
        elif output_file.endswith('.csv'):
            if self.processed_data:
                fieldnames = list(self.processed_data[0].keys())
                with open(output_file, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.processed_data)
            json_path = output_file.replace('.csv', '_report.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"✅ JSON 报告已保存：{json_path}")
        print(f"✅ 主文件已保存：{output_file}")
        return report


def main():
    parser = argparse.ArgumentParser(
        description='多源薪酬数据整合处理器 V3（支持海外薪酬分析）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
    # 国内薪酬分析
    python3 multi_source_processor.py -i data.csv -o report.json

    # 海外薪酬分析（自动换算到 USD）
    python3 multi_source_processor.py -i data.csv -o report.json --target-currency USD

    # PPP 购买力平价调整
    python3 multi_source_processor.py -i data.csv -o report.json --with-ppp
        """)
    parser.add_argument('-i', '--input', required=True, help='输入文件路径（CSV/JSON）')
    parser.add_argument('-o', '--output', required=True, help='输出文件路径（JSON/CSV）')
    parser.add_argument('-w', '--weights', help='权重配置文件（JSON）')
    parser.add_argument('--target-currency', default='CNY', help='目标货币（CNY/USD，默认 CNY）')
    parser.add_argument('--with-ppp', action='store_true', help='计算 PPP 购买力平价调整')
    parser.add_argument('--ppp-base-country', default='中国', help='PPP 对标基准国家（默认中国）')
    args = parser.parse_args()

    processor = MultiSourceSalaryProcessor(
        args.input, args.weights,
        target_currency=args.target_currency,
        enable_ppp=args.with_ppp,
        ppp_base_country=args.ppp_base_country
    )
    processor.load_data()
    processor.process_data()
    report = processor.save_report(args.output)

    print("\n" + "=" * 60)
    print("📊 数据摘要")
    print("=" * 60)
    print(f"总样本数：{processor.stats.get('total_samples', 0)}")
    print(f"有效样本：{processor.stats.get('valid_samples', 0)}")
    print(f"目标货币：{processor.target_currency}")
    print(f"数据质量评分：{report.get('quality_score', 0)}")

    stats = processor.stats.get('salary_stats', {})
    if stats:
        unit = "万美元/年" if processor.target_currency == 'USD' else "万元/年"
        print(f"\n薪酬统计（单位：{unit}）：")
        print(f"  平均值：{stats.get('mean', 'N/A')}")
        print(f"  中位数：{stats.get('median', 'N/A')}")
        print(f"  标准差：{stats.get('std', 'N/A')}")
        print(f"  范围：{stats.get('min', 'N/A')} - {stats.get('max', 'N/A')}")
        print(f"  偏态：{stats.get('skew', 'N/A')}")

    # USD 统计
    stats_usd = processor.stats.get('salary_stats_usd', {})
    if stats_usd:
        print(f"\n💵 全球对标（USD）：")
        print(f"  平均值：${stats_usd.get('mean', 'N/A')} 万")
        print(f"  中位数：${stats_usd.get('median', 'N/A')} 万")

    print(f"\n薪酬分位值：")
    for k, v in processor.percentiles.items():
        print(f"  {k}: {v}")

    print(f"\n来源分布：")
    for k, v in processor.stats.get('source_distribution', {}).items():
        print(f"  {k}: {v}")

    print(f"\n企业类型薪酬：")
    for k, v in processor.stats.get('company_type_salary', {}).items():
        print(f"  {k}: 平均 {v.get('avg', 0):.2f} ({v.get('count', 0)} 条)")

    # 海外薪酬分析
    country_salary = processor.stats.get('country_salary', {})
    if country_salary:
        curr_label = "CNY"
        print(f"\n🌍 国家/地区薪酬对比（单位：万元{curr_label}/年）：")
        for k, v in sorted(country_salary.items(), key=lambda x: x[1].get('avg_cny', 0), reverse=True):
            ppp_str = f" | PPP 系数 {v.get('ppp_coefficient', 1.0)}" if v.get('ppp_coefficient') != 1.0 else ""
            print(f"  {k}: {v.get('avg_cny', 0):.2f} 万 | USD {v.get('avg_target', 0):.2f} 万{ppp_str} ({v.get('count', 0)} 条)")
    print("=" * 60)


if __name__ == '__main__':
    main()
