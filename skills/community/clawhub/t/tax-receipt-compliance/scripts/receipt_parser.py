#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发票数据解析器 - 结构化处理和字段标准化
"""

import re
import json
from datetime import datetime
from pathlib import Path


class ReceiptParser:
    """发票数据解析器"""

    def __init__(self):
        self.tax_rates = {
            0.13: ['13%', '13'],
            0.09: ['9%', '9'],
            0.06: ['6%', '6'],
            0.03: ['3%', '3'],
            0.01: ['1%', '1'],
            0.0: ['免税', '不征税', '0%'],
        }

    def parse(self, ocr_result):
        """
        解析OCR识别结果，标准化字段

        Args:
            ocr_result: dict, extract_structured_data()的输出

        Returns:
            dict: 标准化后的发票数据
        """
        if not ocr_result or not ocr_result.get('success'):
            return {
                'success': False,
                'error': ocr_result.get('error', '无效的OCR结果'),
            }

        # 标准化金额字段
        amount = self._normalize_amount(ocr_result.get('amount', 0))
        tax_amount = self._normalize_amount(ocr_result.get('tax_amount', 0))
        total = self._normalize_amount(ocr_result.get('total', 0))

        # 如果合计为空，尝试计算
        if total == 0 and amount > 0 and tax_amount > 0:
            total = round(amount + tax_amount, 2)

        # 标准化日期
        date_str = self._normalize_date(ocr_result.get('invoice_date', ''))

        # 标准化税率
        tax_rate = ocr_result.get('tax_rate', 0)
        if tax_rate == 0 and amount > 0 and tax_amount > 0:
            tax_rate = round(tax_amount / amount, 4) if amount > 0 else 0

        parsed = {
            'success': True,
            'invoice_type': ocr_result.get('invoice_type', '未知'),
            'invoice_code': str(ocr_result.get('invoice_code', '')).strip(),
            'invoice_number': str(ocr_result.get('invoice_number', '')).strip(),
            'invoice_date': date_str,
            'seller_name': str(ocr_result.get('seller_name', '')).strip(),
            'buyer_name': str(ocr_result.get('buyer_name', '')).strip(),
            'amount': amount,
            'tax_rate': tax_rate,
            'tax_amount': tax_amount,
            'total': total,
            'remark': str(ocr_result.get('remark', '')).strip(),
            'confidence': ocr_result.get('confidence', 0),
            'raw_text': ocr_result.get('raw_text', ''),
            'image_path': ocr_result.get('image_path', ''),
            'parsed_at': datetime.now().isoformat(),
        }

        # 自动判断费用类型
        parsed['expense_type'] = self._determine_expense_type(parsed)

        return parsed

    def _normalize_amount(self, value):
        """标准化金额（支持更多格式）"""
        if isinstance(value, (int, float)):
            return round(float(value), 2)
        if isinstance(value, str):
            # 移除货币符号、千位分隔符、空格
            cleaned = re.sub(r'[¥￥,\s]', '', value)
            # 处理负数
            negative = cleaned.startswith('-') or cleaned.startswith('(-')
            cleaned = cleaned.replace('-', '').replace('(', '').replace(')', '')
            # 处理"万"单位
            multiplier = 1
            if '万' in cleaned:
                multiplier = 10000
                cleaned = cleaned.replace('万', '')
            try:
                amount = round(float(cleaned) * multiplier, 2)
                return -amount if negative else amount
            except (ValueError, TypeError):
                return 0.0
        return 0.0

    def _normalize_date(self, date_str):
        """标准化日期格式（支持更多格式）"""
        if not date_str:
            return ''

        # 去除首尾空白
        date_str = date_str.strip()

        # 尝试多种日期格式
        patterns = [
            (r'(\d{4})年(\d{1,2})月(\d{1,2})日', lambda m: f"{m.group(1)}年{int(m.group(2)):02d}月{int(m.group(3)):02d}日"),
            (r'(\d{4})-(\d{1,2})-(\d{1,2})', lambda m: f"{m.group(1)}年{int(m.group(2)):02d}月{int(m.group(3)):02d}日"),
            (r'(\d{4})/(\d{1,2})/(\d{1,2})', lambda m: f"{m.group(1)}年{int(m.group(2)):02d}月{int(m.group(3)):02d}日"),
            (r'(\d{4})\.(\d{1,2})\.(\d{1,2})', lambda m: f"{m.group(1)}年{int(m.group(2)):02d}月{int(m.group(3)):02d}日"),
            (r'(\d{8})', lambda m: f"{m.group(1)[:4]}年{int(m.group(1)[4:6]):02d}月{int(m.group(1)[6:8]):02d}日"),
        ]

        for pattern, formatter in patterns:
            match = re.search(pattern, date_str)
            if match:
                try:
                    result = formatter(match)
                    # 验证日期有效性
                    parts = re.findall(r'\d+', result)
                    if len(parts) == 3:
                        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                        if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                            return result
                except (ValueError, IndexError):
                    continue

        return date_str

    def _determine_expense_type(self, data):
        """根据发票内容自动判断费用类型"""
        remark = data.get('remark', '').lower()
        seller = data.get('seller_name', '').lower()

        # 关键词匹配
        type_keywords = {
            '办公用品': ['办公用品', '文具', '打印', '耗材', '纸'],
            '差旅费': ['住宿', '交通', '餐饮', '差旅', '火车票', '机票', '酒店'],
            '咨询服务': ['咨询', '顾问', '顾问费'],
            '信息技术服务': ['技术', '软件', '服务', '开发', '维护', '系统集成'],
            '培训费': ['培训', '教育', '课程'],
            '租赁费': ['租赁', '房租', '物业'],
            '广告宣传': ['广告', '宣传', '推广'],
        }

        text = remark + ' ' + seller
        for expense_type, keywords in type_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return expense_type

        return '其他费用'

    def validate(self, parsed_data):
        """
        验证发票数据的完整性和合法性

        Returns:
            dict: 验证结果
        """
        issues = []
        warnings = []

        # 必要字段检查
        if not parsed_data.get('invoice_code'):
            issues.append({'field': 'invoice_code', 'message': '发票代码缺失', 'hint': '请检查OCR识别结果或手动输入'})
        if not parsed_data.get('invoice_number'):
            issues.append({'field': 'invoice_number', 'message': '发票号码缺失', 'hint': '请检查OCR识别结果或手动输入'})
        if not parsed_data.get('invoice_date'):
            issues.append({'field': 'invoice_date', 'message': '开票日期缺失', 'hint': '请检查OCR识别结果或手动输入'})
        if parsed_data.get('total', 0) <= 0:
            issues.append({'field': 'total', 'message': '价税合计金额无效', 'hint': '金额应大于0'})

        # 发票代码格式检查
        code = parsed_data.get('invoice_code', '')
        if code and not re.match(r'^\d{10,12}$', code):
            issues.append({'field': 'invoice_code', 'message': f'发票代码格式不正确：{code}', 'hint': '应为10-12位数字'})

        # 发票号码格式检查
        number = parsed_data.get('invoice_number', '')
        if number and not re.match(r'^\d{8,20}$', number):
            issues.append({'field': 'invoice_number', 'message': f'发票号码格式不正确：{number}', 'hint': '应为8-20位数字'})

        # 金额勾稽检查
        if parsed_data.get('amount', 0) > 0 and parsed_data.get('tax_amount', 0) > 0:
            expected_total = round(parsed_data['amount'] + parsed_data['tax_amount'], 2)
            actual_total = parsed_data.get('total', 0)
            if actual_total > 0 and abs(expected_total - actual_total) > 0.01:
                issues.append({
                    'field': 'total',
                    'message': f'金额勾稽关系不匹配：金额({parsed_data["amount"]}) + 税额({parsed_data["tax_amount"]}) = {expected_total} ≠ 价税合计({actual_total})',
                    'hint': '请检查金额、税额、价税合计是否正确'
                })

        # 日期有效性检查
        date_str = parsed_data.get('invoice_date', '')
        if date_str:
            try:
                parts = re.findall(r'\d+', date_str)
                if len(parts) == 3:
                    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                    if not (1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31):
                        warnings.append(f'日期可能无效：{date_str}')
            except (ValueError, IndexError):
                warnings.append(f'日期格式异常：{date_str}')

        # 金额异常检查
        amount = parsed_data.get('amount', 0)
        if amount > 10000000:  # 1000万
            warnings.append(f'金额异常大：{amount}，请确认是否正确')
        elif amount < 0:
            warnings.append(f'金额为负数：{amount}，请确认是否正确')

        # 税率检查
        tax_rate = parsed_data.get('tax_rate', 0)
        if tax_rate > 0:
            valid_rates = [0.13, 0.09, 0.06, 0.03, 0.01, 0.0]
            if tax_rate not in valid_rates:
                warnings.append(f'税率异常：{tax_rate}，常见税率：13%、9%、6%、3%、1%、0%')

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
        }

    def to_expense_data(self, parsed_data, template_mapping=None):
        """
        转换为报销单数据格式

        Args:
            parsed_data: 标准化后的发票数据
            template_mapping: 模板字段映射

        Returns:
            dict: 报销单数据
        """
        if template_mapping is None:
            template_mapping = {
                'invoice_date': '开票日期',
                'seller_name': '销方名称',
                'amount': '金额（不含税）',
                'tax_amount': '税额',
                'total': '价税合计',
                'remark': '费用说明',
                'invoice_code': '发票代码',
                'invoice_number': '发票号码',
                'expense_type': '费用类型',
            }

        expense_data = {}
        for invoice_field, template_field in template_mapping.items():
            if invoice_field in parsed_data:
                expense_data[template_field] = parsed_data[invoice_field]

        return expense_data


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='发票数据解析器')
    parser.add_argument('--input', required=True, help='OCR识别结果JSON文件路径')
    parser.add_argument('--output', help='输出文件路径（可选）')
    parser.add_argument('--mapping', help='模板映射配置文件（可选）')

    args = parser.parse_args()

    # 读取OCR结果
    with open(args.input, 'r', encoding='utf-8') as f:
        ocr_data = json.load(f)

    # 解析
    rp = ReceiptParser()
    parsed = rp.parse(ocr_data)

    # 验证
    validation = rp.validate(parsed)
    parsed['validation'] = validation

    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {args.output}")
    else:
        print(json.dumps(parsed, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
