#!/usr/bin/env python3
"""报价单数据 JSON Schema 验证模块"""

import re
from typing import Dict, List, Tuple, Any
from datetime import datetime


class QuotationValidator:
    """报价单数据验证器 - 多层次验证防止示例数据/占位符数据"""
    
    # 扩展示例公司名称模式（正则）
    EXAMPLE_COMPANY_PATTERNS = [
        r'example', r'test', r'sample', r'demo', r'dummy',
        r'john doe', r'jane doe', r'xxx', r'abc',
        r'your company', r'customer name', r'company name',
        r'quadnet', r'specialized computer', r'best buy electronics',
        r'placeholder', r'temp', r'temporary',
    ]
    
    # 示例报价单号模式
    EXAMPLE_QUOTATION_PATTERNS = [
        r'^qt-test', r'^qt-000', r'^qt-123456',
        r'^test-', r'^sample-', r'^qtb-',
        r'^\d{3,4}$',  # 纯数字（太短，可能是占位符）
    ]
    
    # 测试邮箱域名（改进版：使用子字符串匹配）
    TEST_EMAIL_DOMAIN_PATTERNS = [
        r'\bexample\b', r'\btest\b', r'\bdemo\b', r'\bsample\b',
        r'\bfake\b', r'\bmock\b', r'\btempmail\b',
    ]
    
    # 公共邮箱域名（精确匹配）
    PUBLIC_EMAIL_DOMAINS = [
        'gmail.com', 'yahoo.com', 'hotmail.com', '163.com', 'qq.com',
    ]
    
    # 占位符地址模式（改进版：匹配缩写和变体）
    PLACEHOLDER_ADDRESSES = [
        r'\b\d{1,4}\s+\w+\s+(street|st\.?|st)\b',  # 匹配 Street/St./St
        r'\b\d{1,4}\s+\w+\s+(road|rd\.?|rd)\b',    # 匹配 Road/Rd./Rd
        r'\b\d{1,4}\s+\w+\s+(avenue|ave\.?|ave)\b', # 匹配 Avenue/Ave./Ave
        r'\b(your|xxx|test|sample)\s+(city|address|district|area|street|road)\b',
        r'\b\d{1,4}\s+business\s+\w+\b',  # 匹配 "123 Business St"
        r'\btest\s+address\b', r'\bsample\s+address\b',
    ]
    
    # 占位符电话模式
    PLACEHOLDER_PHONES = [
        '123456789', '000000000', '111111111', '999999999',
        'xxx-xxxx-xxxx', 'xxx-xxx-xxxx', '123-456-7890',
        '000-000-0000', '111-111-1111',
    ]
    
    def __init__(self):
        self.company_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.EXAMPLE_COMPANY_PATTERNS
        ]
        self.quotation_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.EXAMPLE_QUOTATION_PATTERNS
        ]
        self.address_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.PLACEHOLDER_ADDRESSES
        ]
        self.email_domain_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.TEST_EMAIL_DOMAIN_PATTERNS
        ]
    
    def validate_customer(self, customer_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        验证客户数据是否为真实数据
        返回：(是否有效，错误列表)
        """
        errors = []
        
        # 支持多种字段名
        company_name = customer_data.get('company_name', customer_data.get('name', ''))
        contact_email = customer_data.get('contact_email', customer_data.get('email', ''))
        address = customer_data.get('address', '')
        phone = customer_data.get('phone', customer_data.get('contact_phone', ''))
        contact = customer_data.get('contact', customer_data.get('contact_name', ''))
        
        # 1. 检查必填字段是否存在且非空
        required_fields = {
            'company_name': company_name,
            'contact_email': contact_email,
            'address': address,
        }
        
        for field_name, field_value in required_fields.items():
            if not field_value:
                errors.append(f"必填字段缺失：{field_name}")
            elif not str(field_value).strip():
                errors.append(f"字段为空：{field_name}")
            elif len(str(field_value).strip()) < 2:
                errors.append(f"字段内容过短：{field_name} = '{field_value}'")
        
        if errors:
            return False, errors
        
        # 2. 检查公司名称是否包含示例关键词
        for pattern in self.company_patterns:
            if pattern.search(company_name):
                errors.append(f"公司名称包含示例关键词：{company_name}")
                break
        
        # 3. 检查邮箱格式和域名
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, contact_email):
            errors.append(f"邮箱格式无效：{contact_email}")
        else:
            # 检查邮箱域名是否为测试域名（子字符串匹配）
            domain = contact_email.split('@')[1].lower()
            is_test_domain = False
            
            # 首先检查测试域名模式
            for pattern in self.email_domain_patterns:
                if pattern.search(domain):
                    errors.append(f"使用测试邮箱域名：{contact_email} (域名：{domain})")
                    is_test_domain = True
                    break
            
            # 然后检查公共邮箱域名（精确匹配）
            if not is_test_domain and domain in self.PUBLIC_EMAIL_DOMAINS:
                errors.append(f"使用公共邮箱域名：{contact_email} (域名：{domain}，建议使用企业邮箱)")
        
        # 4. 检查地址是否为占位符
        for pattern in self.address_patterns:
            if pattern.search(address):
                errors.append(f"地址包含占位符：{address}")
                break
        
        # 5. 检查电话是否为占位符（电话可选，但如果填写则必须有效）
        if phone:
            phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
            if phone in self.PLACEHOLDER_PHONES or phone_clean in self.PLACEHOLDER_PHONES:
                errors.append(f"电话号码为占位符：{phone}")
            elif len(phone_clean) < 7:
                errors.append(f"电话号码过短：{phone}")
        
        # 6. 检查联系人是否为占位符
        if contact:
            contact_lower = contact.lower()
            if contact_lower in ['john doe', 'jane doe', 'procurement manager', 'contact person', 'xxx', '']:
                errors.append(f"联系人姓名为占位符：{contact}")
        
        return len(errors) == 0, errors
    
    def validate_quotation_no(self, quotation_no: str) -> Tuple[bool, List[str]]:
        """验证报价单号"""
        errors = []
        
        if not quotation_no:
            errors.append("报价单号为空")
            return False, errors
        
        # 检查是否包含示例模式
        for pattern in self.quotation_patterns:
            if pattern.search(quotation_no):
                errors.append(f"报价单号包含示例模式：{quotation_no}")
                break
        
        # 检查格式是否符合 QT-YYYYMMDD-XXX
        standard_format = r'^QT-\d{8}-\d{3,}$'
        if not re.match(standard_format, quotation_no):
            errors.append(f"报价单号格式不符合标准（应为 QT-YYYYMMDD-XXX）：{quotation_no}")
        
        return len(errors) == 0, errors
    
    def validate_products(self, products: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """验证产品信息"""
        errors = []
        
        if not products:
            errors.append("产品列表为空")
            return False, errors
        
        if not isinstance(products, list):
            errors.append("产品列表格式错误（应为数组）")
            return False, errors
        
        for i, product in enumerate(products):
            if not isinstance(product, dict):
                errors.append(f"产品{i+1}格式错误（应为对象）")
                continue
            
            # 检查产品名称/描述
            name = product.get('description', product.get('name', product.get('product_name', '')))
            if not name:
                errors.append(f"产品{i+1}缺少名称/描述")
            elif name.lower() in ['test product', 'sample product', 'xxx', 'product name', '']:
                errors.append(f"产品{i+1}名称为占位符：{name}")
            elif len(str(name).strip()) < 3:
                errors.append(f"产品{i+1}名称过短：{name}")
            
            # 检查价格是否为合理数值
            price = product.get('unit_price', product.get('price', product.get('unitPrice', 0)))
            try:
                price_val = float(price)
                if price_val <= 0:
                    errors.append(f"产品{i+1}价格无效：{price}")
                elif price_val < 0.01:
                    errors.append(f"产品{i+1}价格异常低：{price}")
                elif price_val > 1000000:
                    errors.append(f"产品{i+1}价格异常高：{price}（请确认单位是否正确）")
            except (ValueError, TypeError):
                errors.append(f"产品{i+1}价格格式错误：{price}")
            
            # 检查数量
            qty = product.get('quantity', product.get('qty', 0))
            try:
                qty_val = int(qty)
                if qty_val <= 0:
                    errors.append(f"产品{i+1}数量无效：{qty}")
                elif qty_val > 10000000:
                    errors.append(f"产品{i+1}数量异常大：{qty}（请确认单位是否正确）")
            except (ValueError, TypeError):
                errors.append(f"产品{i+1}数量格式错误：{qty}")
            
            # 检查规格（可选）
            spec = product.get('specification', product.get('spec', ''))
            if spec and len(str(spec).strip()) < 3:
                errors.append(f"产品{i+1}规格过短：{spec}")
        
        return len(errors) == 0, errors
    
    def validate_trade_terms(self, trade_terms: Dict[str, Any], terms: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """验证贸易条款"""
        errors = []
        
        # 支持多种字段名
        incoterms = trade_terms.get('incoterms', terms.get('incoterms', ''))
        currency = trade_terms.get('currency', terms.get('currency', ''))
        delivery = trade_terms.get('delivery', terms.get('delivery', terms.get('lead_time', '')))
        
        # 检查贸易术语
        valid_incoterms = ['FOB', 'CIF', 'CFR', 'EXW', 'DDP', 'DAP', 'FCA', 'CPT', 'CIP']
        if incoterms:
            # 提取主要术语（例如 "FOB Shenzhen" → "FOB"）
            main_term = incoterms.split()[0].upper() if incoterms else ''
            if main_term not in valid_incoterms and incoterms:
                errors.append(f"贸易术语可能无效：{incoterms}（应为 FOB/CIF/CFR 等）")
        
        # 检查货币
        valid_currencies = ['USD', 'EUR', 'CNY', 'GBP', 'JPY', 'AUD', 'CAD', 'HKD']
        if currency and currency.upper() not in valid_currencies:
            errors.append(f"货币单位可能无效：{currency}（应为 USD/EUR/CNY 等）")
        
        # 检查交期
        if not delivery:
            errors.append("缺少交期信息")
        
        return len(errors) == 0, errors
    
    def validate_dates(self, quotation_date: str, valid_until: str) -> Tuple[bool, List[str]]:
        """验证日期格式和逻辑"""
        errors = []
        
        # 日期格式检查
        date_pattern = r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}$'
        
        if quotation_date:
            if not re.match(date_pattern, quotation_date):
                errors.append(f"报价日期格式错误：{quotation_date}（应为 YYYY-MM-DD）")
        
        if valid_until:
            if not re.match(date_pattern, valid_until):
                errors.append(f"有效期格式错误：{valid_until}（应为 YYYY-MM-DD）")
            else:
                # 检查有效期是否晚于报价日期
                try:
                    qt_date = datetime.strptime(quotation_date.replace('/', '-'), '%Y-%m-%d')
                    valid_date = datetime.strptime(valid_until.replace('/', '-'), '%Y-%m-%d')
                    if valid_date <= qt_date:
                        errors.append(f"有效期必须晚于报价日期（报价：{quotation_date}, 有效：{valid_until}）")
                except ValueError:
                    pass  # 日期解析失败已在上面报告
        
        return len(errors) == 0, errors


def validate_quotation_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    完整验证报价单数据
    
    返回：(是否有效，错误列表)
    """
    all_errors = []
    validator = QuotationValidator()
    
    # 1. 验证客户数据
    customer = data.get('customer', {})
    customer_valid, customer_errors = validator.validate_customer(customer)
    all_errors.extend(customer_errors)
    
    # 2. 验证报价单号
    quotation = data.get('quotation', {})
    quotation_no = quotation.get('quotation_no', data.get('quotationNo', ''))
    qt_valid, qt_errors = validator.validate_quotation_no(quotation_no)
    all_errors.extend(qt_errors)
    
    # 3. 验证产品数据
    products = data.get('products', [])
    products_valid, products_errors = validator.validate_products(products)
    all_errors.extend(products_errors)
    
    # 4. 验证贸易条款
    trade_terms = data.get('trade_terms', {})
    terms = data.get('terms', {})
    terms_valid, terms_errors = validator.validate_trade_terms(trade_terms, terms)
    all_errors.extend(terms_errors)
    
    # 5. 验证日期
    quotation_date = quotation.get('date', data.get('date', ''))
    valid_until = quotation.get('valid_until', data.get('validUntil', ''))
    dates_valid, dates_errors = validator.validate_dates(quotation_date, valid_until)
    all_errors.extend(dates_errors)
    
    # 6. 验证总金额计算（可选，如果提供了总额）
    if 'total_amount' in data:
        products = data.get('products', [])
        calculated_total = sum(
            float(p.get('quantity', 0)) * float(p.get('unit_price', p.get('unitPrice', 0)))
            for p in products
        )
        declared_total = float(data.get('total_amount', 0))
        if abs(calculated_total - declared_total) > 0.01:
            all_errors.append(
                f"总金额计算不匹配：声明={declared_total:.2f}, 计算={calculated_total:.2f}"
            )
    
    return len(all_errors) == 0, all_errors


if __name__ == '__main__':
    # 测试示例
    import json
    import sys
    
    test_data = {
        'customer': {
            'company_name': 'Example Customer Corp',  # 会被检测为示例数据
            'contact_email': 'contact@example.com',  # 会被检测为测试域名
            'address': '123 Business Street',  # 会被检测为占位符地址
            'phone': '123-456-7890',  # 会被检测为占位符电话
        },
        'quotation': {
            'quotation_no': 'QT-TEST-001',  # 会被检测为示例报价单号
            'date': '2026-03-27',
            'valid_until': '2026-04-26',
        },
        'products': [
            {
                'description': 'Test Product',  # 会被检测为占位符
                'quantity': 500,
                'unit_price': 8.50,
            }
        ],
        'trade_terms': {
            'incoterms': 'FOB Shenzhen',
            'currency': 'USD',
            'delivery': '15-20 days',
        }
    }
    
    print("测试验证器（使用示例数据）...")
    print("=" * 60)
    
    valid, errors = validate_quotation_data(test_data)
    
    if valid:
        print("✅ 验证通过")
    else:
        print("❌ 验证失败:")
        for err in errors:
            print(f"  - {err}")
    
    sys.exit(0 if valid else 1)
