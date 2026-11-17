#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记账凭证生成器
基于发票信息 + 费用分类 + 税额计算，自动生成记账凭证
支持用友/金蝶/QuickBooks 导入格式
"""

import json
import csv
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from io import StringIO

from unified_invoice import UnifiedInvoice
from smart_classifier import smart_classify


class VoucherGenerator:
    """
    记账凭证生成器
    
    输出格式：
    - JSON（默认，结构化数据）
    - CSV（兼容 Excel）
    - 用友 U8（.txt 导入格式）
    - 金蝶 KIS（.txt 导入格式）
    - QuickBooks（.iif 导入格式）
    """
    
    def __init__(self):
        self.voucher_date = datetime.now().strftime('%Y-%m-%d')
        self.voucher_number = f"PZ{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def generate(self, invoice: UnifiedInvoice) -> Dict[str, Any]:
        """
        生成记账凭证
        
        凭证结构：
        - 凭证号、日期、附件数
        - 摘要
        - 借方科目、金额
        - 贷方科目、金额
        """
        # 先进行智能分类
        invoice = smart_classify(invoice)
        
        voucher = {
            "voucher_number": self.voucher_number,
            "voucher_date": invoice.billing_date or invoice.travel_date or self.voucher_date,
            "attachment_count": 1,
            "summary": invoice.voucher_summary or "",
            "entries": [],
            "source_invoice": invoice.to_dict(),
        }
        
        # 借方分录
        debit_entry = {
            "type": "debit",
            "account": invoice.debit_account,
            "account_name": self._get_account_name(invoice.debit_account),
            "amount": invoice.total or 0.0,
            "summary": invoice.voucher_summary or "",
        }
        
        # 如果有可抵扣进项税额，拆分金额
        if invoice.vat_deduction_amount and invoice.vat_deduction_amount > 0:
            # 借方：不含税金额
            debit_entry["amount"] = round((invoice.total or 0) - invoice.vat_deduction_amount, 2)
            
            # 借方：进项税额
            tax_debit_entry = {
                "type": "debit",
                "account": "2221.01",  # 应交税费-应交增值税-进项税额
                "account_name": "应交税费-应交增值税-进项税额",
                "amount": invoice.vat_deduction_amount,
                "summary": "进项税额抵扣",
            }
            voucher["entries"].append(tax_debit_entry)
        
        voucher["entries"].append(debit_entry)
        
        # 贷方分录
        credit_entry = {
            "type": "credit",
            "account": invoice.credit_account,
            "account_name": self._get_account_name(invoice.credit_account),
            "amount": invoice.total or 0.0,
            "summary": invoice.voucher_summary or "",
        }
        voucher["entries"].append(credit_entry)
        
        return voucher
    
    def _get_account_name(self, account_code: Optional[str]) -> str:
        """根据科目代码获取科目名称"""
        if not account_code:
            return ""
        
        account_names = {
            "6602.01": "管理费用-差旅费",
            "6602.02": "管理费用-办公费",
            "6602.03": "管理费用-业务招待费",
            "6601.01": "销售费用-广告费",
            "6602.04": "管理费用-咨询费",
            "6602.05": "管理费用-交通费",
            "6602.06": "管理费用-通行费",
            "6602.07": "管理费用-福利费",
            "6602.08": "管理费用-租赁费",
            "6602.09": "管理费用-维修费",
            "6602.99": "管理费用-其他",
            "2221.01": "应交税费-应交增值税-进项税额",
            "1002": "银行存款",
            "1002.01": "银行存款-转账",
            "1001": "库存现金",
        }
        
        return account_names.get(account_code, account_code)
    
    def export_json(self, voucher: Dict[str, Any]) -> str:
        """导出为 JSON 格式"""
        return json.dumps(voucher, ensure_ascii=False, indent=2)
    
    def export_csv(self, voucher: Dict[str, Any]) -> str:
        """导出为 CSV 格式"""
        output = StringIO()
        writer = csv.writer(output)
        
        # 表头
        writer.writerow(["凭证号", "日期", "摘要", "科目代码", "科目名称", "借方金额", "贷方金额"])
        
        for entry in voucher["entries"]:
            writer.writerow([
                voucher["voucher_number"],
                voucher["voucher_date"],
                entry["summary"],
                entry["account"],
                entry["account_name"],
                entry["amount"] if entry["type"] == "debit" else "",
                entry["amount"] if entry["type"] == "credit" else "",
            ])
        
        return output.getvalue()
    
    def export_yonyou(self, voucher: Dict[str, Any]) -> str:
        """
        导出为用友 U8 导入格式
        用友凭证导入格式：日期|凭证号|摘要|科目|借方|贷方
        """
        lines = []
        
        for entry in voucher["entries"]:
            debit_amt = entry["amount"] if entry["type"] == "debit" else 0
            credit_amt = entry["amount"] if entry["type"] == "credit" else 0
            
            line = (
                f"{voucher['voucher_date']}|"
                f"{voucher['voucher_number']}|"
                f"{entry['summary']}|"
                f"{entry['account']}|"
                f"{debit_amt}|"
                f"{credit_amt}"
            )
            lines.append(line)
        
        return "\n".join(lines)
    
    def export_kingdee(self, voucher: Dict[str, Any]) -> str:
        """
        导出为金蝶 KIS 导入格式
        金蝶凭证导入格式：日期\t凭证字\t凭证号\t摘要\t科目\t借方\t贷方
        """
        lines = []
        
        for entry in voucher["entries"]:
            debit_amt = entry["amount"] if entry["type"] == "debit" else 0
            credit_amt = entry["amount"] if entry["type"] == "credit" else 0
            
            line = (
                f"{voucher['voucher_date']}\t"
                f"记\t"
                f"{voucher['voucher_number']}\t"
                f"{entry['summary']}\t"
                f"{entry['account']}\t"
                f"{debit_amt}\t"
                f"{credit_amt}"
            )
            lines.append(line)
        
        return "\n".join(lines)
    
    def export_quickbooks(self, voucher: Dict[str, Any]) -> str:
        """
        导出为 QuickBooks IIF 导入格式
        IIF 格式：TRNS, DATE, ACCNT, AMOUNT, MEMO
        """
        lines = ["!TRNS\tDATE\tACCNT\tAMOUNT\tMEMO"]
        
        for entry in voucher["entries"]:
            amount = entry["amount"] if entry["type"] == "debit" else -entry["amount"]
            
            line = (
                f"TRNS\t"
                f"{voucher['voucher_date']}\t"
                f"{entry['account_name']}\t"
                f"{amount}\t"
                f"{entry['summary']}"
            )
            lines.append(line)
        
        lines.append("ENDTRNS")
        return "\n".join(lines)


def generate_voucher(invoice: UnifiedInvoice, export_format: str = "json") -> str:
    """
    便捷函数：生成记账凭证并导出
    
    Args:
        invoice: 统一发票数据结构
        export_format: json | csv | yonyou | kingdee | quickbooks
    
    Returns:
        str: 导出的凭证内容
    """
    generator = VoucherGenerator()
    voucher = generator.generate(invoice)
    
    exporters = {
        "json": generator.export_json,
        "csv": generator.export_csv,
        "yonyou": generator.export_yonyou,
        "kingdee": generator.export_kingdee,
        "quickbooks": generator.export_quickbooks,
    }
    
    exporter = exporters.get(export_format, generator.export_json)
    return exporter(voucher)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python voucher_generator.py <path_to_invoice_json>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        invoice = UnifiedInvoice(**data)
        
        format_arg = sys.argv[2] if len(sys.argv) > 2 else "json"
        result = generate_voucher(invoice, format_arg)
        print(result)
    except Exception as e:
        print(f"生成失败: {e}", file=sys.stderr)
        sys.exit(1)
