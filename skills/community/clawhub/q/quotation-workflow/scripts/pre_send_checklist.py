#!/usr/bin/env python3
"""发送前强制检查清单 - 代码化验证，不可绕过

使用方式：
    from pre_send_checklist import PreSendChecklist
    
    checklist = PreSendChecklist(quotation_data, customer_data)
    passed, results = checklist.run_all_checks()
    
    if not passed:
        print("❌ 检查未通过，禁止发送")
        sys.exit(1)
"""

import json
import sys
from typing import Dict, List, Tuple, Any
from datetime import datetime, timedelta


class PreSendChecklist:
    """发送前强制检查清单（代码化，不可绕过）"""
    
    def __init__(self, quotation_data: Dict[str, Any], customer_data: Dict[str, Any]):
        self.quotation = quotation_data
        self.customer = customer_data
        self.check_results: List[Dict[str, Any]] = []
    
    def _add_result(self, item: str, passed: bool, message: str, critical: bool = True):
        """添加检查结果"""
        self.check_results.append({
            'item': item,
            'passed': passed,
            'message': message,
            'critical': critical,  # 关键检查项失败会阻断流程
        })
    
    def check_customer_from_okki(self) -> bool:
        """检查客户数据是否来自 OKKI（而非手动输入）"""
        okki_customer_id = self.customer.get('okki_customer_id')
        
        if not okki_customer_id:
            self._add_result(
                '客户来源',
                False,
                '客户数据未关联 OKKI 客户 ID（建议：从 OKKI 导入客户数据）',
                critical=False  # 暂时设为非关键，等 OKKI 集成完成后改为 True
            )
            return False
        
        # TODO: 调用 OKKI API 验证客户是否存在
        # okki_client = OKKIClient()
        # try:
        #     okki_customer = okki_client.get_company(okki_customer_id)
        #     self._add_result('客户来源', True, f'客户已验证 OKKI ID: {okki_customer_id}')
        #     return True
        # except Exception as e:
        #     self._add_result('客户来源', False, f'OKKI 验证失败：{e}')
        #     return False
        
        self._add_result('客户来源', True, f'客户已关联 OKKI ID: {okki_customer_id}')
        return True
    
    def check_email_domain_match(self) -> bool:
        """检查客户邮箱域名是否与公司域名匹配"""
        email = self.customer.get('contact_email', self.customer.get('email', ''))
        
        if not email or '@' not in email:
            self._add_result('邮箱格式', False, '邮箱格式无效')
            return False
        
        # 检查常见公共邮箱域名（可能是占位符）
        public_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', '163.com', 'qq.com']
        domain = email.split('@')[1].lower()
        
        if domain in public_domains:
            self._add_result(
                '邮箱域名',
                False,
                f'使用公共邮箱域名：{domain}（建议使用企业邮箱）',
                critical=False
            )
            return False
        
        self._add_result('邮箱域名', True, f'邮箱域名有效：{domain}')
        return True
    
    def check_products_not_empty(self) -> bool:
        """检查产品列表非空"""
        products = self.quotation.get('products', [])
        
        if not products:
            self._add_result('产品列表', False, '产品列表为空')
            return False
        
        if not isinstance(products, list):
            self._add_result('产品列表', False, '产品列表格式错误（应为数组）')
            return False
        
        self._add_result('产品列表', True, f'包含 {len(products)} 个产品')
        return True
    
    def check_total_amount_calculated(self) -> bool:
        """检查总金额是否正确计算"""
        products = self.quotation.get('products', [])
        
        try:
            calculated_total = sum(
                float(p.get('quantity', 0)) * float(p.get('unit_price', p.get('unitPrice', 0)))
                for p in products
            )
        except (ValueError, TypeError) as e:
            self._add_result('总金额计算', False, f'计算失败：{e}')
            return False
        
        declared_total = float(self.quotation.get('total_amount', 0))
        
        if declared_total > 0 and abs(calculated_total - declared_total) > 0.01:
            self._add_result(
                '总金额计算',
                False,
                f'总金额不匹配：声明={declared_total:.2f}, 计算={calculated_total:.2f}'
            )
            return False
        
        self._add_result('总金额计算', True, f'计算正确：${calculated_total:,.2f}')
        return True
    
    def check_quotation_no_format(self) -> bool:
        """检查报价单号格式"""
        import re
        
        quotation = self.quotation.get('quotation', {})
        quotation_no = quotation.get('quotation_no', self.quotation.get('quotationNo', ''))
        
        if not quotation_no:
            self._add_result('报价单号', False, '报价单号为空')
            return False
        
        # 标准格式：QT-YYYYMMDD-XXX
        standard_format = r'^QT-\d{8}-\d{3,}$'
        if not re.match(standard_format, quotation_no):
            self._add_result(
                '报价单号格式',
                False,
                f'格式不符合标准：{quotation_no}（应为 QT-YYYYMMDD-XXX）',
                critical=False
            )
            return False
        
        self._add_result('报价单号格式', True, f'格式正确：{quotation_no}')
        return True
    
    def check_dates_valid(self) -> bool:
        """检查日期有效性"""
        quotation = self.quotation.get('quotation', {})
        quotation_date = quotation.get('date', self.quotation.get('date', ''))
        valid_until = quotation.get('valid_until', self.quotation.get('validUntil', ''))
        
        if not quotation_date:
            self._add_result('报价日期', False, '报价日期为空')
            return False
        
        try:
            qt_date = datetime.strptime(quotation_date.replace('/', '-'), '%Y-%m-%d')
            
            # 检查报价日期是否晚于今天（可能是未来日期）
            today = datetime.now()
            if qt_date.date() > today.date():
                self._add_result(
                    '报价日期',
                    False,
                    f'报价日期是未来日期：{quotation_date}',
                    critical=False
                )
            else:
                self._add_result('报价日期', True, f'日期有效：{quotation_date}')
            
            # 检查有效期
            if valid_until:
                valid_date = datetime.strptime(valid_until.replace('/', '-'), '%Y-%m-%d')
                if valid_date <= qt_date:
                    self._add_result(
                        '有效期',
                        False,
                        f'有效期必须晚于报价日期（报价：{quotation_date}, 有效：{valid_until}）'
                    )
                    return False
                
                # 检查有效期是否合理（通常 30-90 天）
                days_valid = (valid_date - qt_date).days
                if days_valid < 7:
                    self._add_result(
                        '有效期长度',
                        False,
                        f'有效期过短：{days_valid} 天（建议至少 7 天）',
                        critical=False
                    )
                elif days_valid > 180:
                    self._add_result(
                        '有效期长度',
                        False,
                        f'有效期过长：{days_valid} 天（建议不超过 90 天）',
                        critical=False
                    )
                else:
                    self._add_result('有效期', True, f'{days_valid} 天（至 {valid_until}）')
            else:
                self._add_result('有效期', False, '有效期为空', critical=False)
                
        except ValueError as e:
            self._add_result('日期格式', False, f'日期格式错误：{e}')
            return False
        
        return True
    
    def check_customer_info_complete(self) -> bool:
        """检查客户信息完整性"""
        required_fields = {
            'company_name': '客户公司名称',
            'contact': '联系人姓名',
            'address': '客户地址',
        }
        
        missing = []
        for field, label in required_fields.items():
            value = self.customer.get(field, self.customer.get(field.replace('_', ''), ''))
            if not value or not str(value).strip():
                missing.append(label)
        
        if missing:
            self._add_result(
                '客户信息完整性',
                False,
                f'缺少必填信息：{", ".join(missing)}'
            )
            return False
        
        self._add_result('客户信息完整性', True, '所有必填信息已填写')
        return True
    
    def check_attachments_ready(self, attachment_paths: List[str] = None) -> bool:
        """检查附件是否就绪"""
        if not attachment_paths:
            self._add_result('附件检查', False, '未提供附件路径列表', critical=False)
            return False
        
        from pathlib import Path
        
        missing = []
        for path in attachment_paths:
            if not Path(path).exists():
                missing.append(path)
        
        if missing:
            self._add_result(
                '附件检查',
                False,
                f'附件文件不存在：{", ".join(missing)}'
            )
            return False
        
        self._add_result('附件检查', True, f'{len(attachment_paths)} 个附件就绪')
        return True
    
    def run_all_checks(self, attachment_paths: List[str] = None) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        运行所有检查
        
        返回：(是否全部通过，检查结果列表)
        """
        print("🔍 运行发送前检查清单...")
        print("=" * 60)
        
        # 运行所有检查
        self.check_customer_from_okki()
        self.check_email_domain_match()
        self.check_products_not_empty()
        self.check_total_amount_calculated()
        self.check_quotation_no_format()
        self.check_dates_valid()
        self.check_customer_info_complete()
        self.check_attachments_ready(attachment_paths)
        
        # 统计结果
        total = len(self.check_results)
        passed = sum(1 for r in self.check_results if r['passed'])
        failed = total - passed
        critical_failed = sum(1 for r in self.check_results if not r['passed'] and r['critical'])
        
        # 打印结果
        for result in self.check_results:
            icon = "✅" if result['passed'] else "❌"
            critical_mark = " ⚠️" if not result['passed'] and result['critical'] else ""
            print(f"{icon} {result['item']}: {result['message']}{critical_mark}")
        
        print("=" * 60)
        print(f"总计：{passed}/{total} 通过", end="")
        
        if failed > 0:
            print(f" ({failed} 失败", end="")
            if critical_failed > 0:
                print(f", {critical_failed} 关键失败", end="")
            print(")")
        else:
            print()
        
        # 判断是否通过
        all_passed = critical_failed == 0
        
        if all_passed:
            print("✅ 发送前检查通过")
        else:
            print("❌ 发送前检查未通过，请修复问题后再发送")
        
        return all_passed, self.check_results
    
    def print_summary(self):
        """打印检查摘要"""
        if not self.check_results:
            return
        
        print("\n📋 检查摘要:")
        for result in self.check_results:
            icon = "✅" if result['passed'] else "❌"
            print(f"  {icon} {result['item']}: {result['message']}")


def main():
    """测试检查清单"""
    import json
    
    # 测试数据
    test_quotation = {
        'quotation': {
            'quotation_no': 'QT-20260327-001',
            'date': '2026-03-27',
            'valid_until': '2026-04-26',
        },
        'products': [
            {
                'description': 'HDMI 2.1 Cable',
                'quantity': 500,
                'unit_price': 8.50,
            }
        ],
        'total_amount': 4250.00,
    }
    
    test_customer = {
        'company_name': 'Test Customer Corp',
        'contact': 'John Smith',
        'contact_email': 'john@testcustomer.com',
        'address': '456 Business Road, Tech City',
        'phone': '+1-555-123-4567',
        'okki_customer_id': '12345',
    }
    
    checklist = PreSendChecklist(test_quotation, test_customer)
    passed, results = checklist.run_all_checks()
    
    sys.exit(0 if passed else 1)


if __name__ == '__main__':
    main()
