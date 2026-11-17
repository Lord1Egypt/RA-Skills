#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能分类器
根据发票/票据内容自动匹配会计科目、计算进项税额、确定费用归属
"""

import re
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from unified_invoice import UnifiedInvoice, VAT_DEDUCTION_RATES


# === 会计科目对照表 ===
ACCOUNT_MAPPING = {
    # 借方科目
    "debit": {
        "差旅费": "6602.01",      # 管理费用-差旅费
        "办公费": "6602.02",      # 管理费用-办公费
        "业务招待费": "6602.03",  # 管理费用-业务招待费
        "广告费": "6601.01",      # 销售费用-广告费
        "咨询费": "6602.04",      # 管理费用-咨询费
        "交通费": "6602.05",      # 管理费用-交通费
        "通行费": "6602.06",      # 管理费用-通行费
        "招待费": "6602.03",
        "福利费": "6602.07",      # 管理费用-福利费
        "租赁费": "6602.08",      # 管理费用-租赁费
        "维修费": "6602.09",      # 管理费用-维修费
        "其他费用": "6602.99",    # 管理费用-其他
    },
    # 贷方科目
    "credit": {
        "default": "1002",       # 银行存款
        "cash": "1001",          # 库存现金
        "transfer": "1002.01",   # 银行存款-转账
    }
}

# === 费用分类关键词规则 ===
EXPENSE_RULES = [
    {"category": "差旅费", "keywords": ["酒店", "住宿", "机票", "火车票", "高铁", "动车", "打车", "出租车", "滴滴"]},
    {"category": "差旅费", "keywords": ["机票", "行程单", "航班"]},
    {"category": "办公费", "keywords": ["办公用品", "文具", "打印", "复印", "耗材", "电脑", "鼠标", "键盘"]},
    {"category": "业务招待费", "keywords": ["餐饮", "食品", "招待", "餐厅", "饭店", "酒楼"]},
    {"category": "广告费", "keywords": ["广告", "推广", "宣传", "营销", "品牌", "投放"]},
    {"category": "咨询费", "keywords": ["咨询", "顾问", "法律", "审计", "税务代理"]},
    {"category": "交通费", "keywords": ["打车", "出租车", "滴滴", "公交", "地铁"]},
    {"category": "通行费", "keywords": ["通行费", "高速", "桥闸", "过路费"]},
    {"category": "福利费", "keywords": ["福利", "员工", "生日", "节日", "体检"]},
    {"category": "租赁费", "keywords": ["租赁", "房租", "物业", "水电"]},
    {"category": "维修费", "keywords": ["维修", "修理", "维护", "保养"]},
]

# === 默认摘要模板 ===
SUMMARY_TEMPLATES = {
    "差旅费": "{date} {departure}至{arrival}差旅费",
    "办公费": "{date}办公用品采购",
    "业务招待费": "{date}业务招待费",
    "广告费": "{date}广告宣传费",
    "咨询费": "{date}咨询顾问费",
    "交通费": "{date}市内交通费",
    "通行费": "{date}车辆通行费",
    "福利费": "{date}员工福利",
    "租赁费": "{date}租赁费",
    "维修费": "{date}维修费",
    "财政票据": "{date}财政票据入账",
    "其他费用": "{date}费用支出",
}


class SmartClassifier:
    """智能分类器"""
    
    def __init__(self):
        self.expense_rules = EXPENSE_RULES
        self.account_mapping = ACCOUNT_MAPPING
        self.summary_templates = SUMMARY_TEMPLATES
    
    def classify(self, invoice: UnifiedInvoice) -> UnifiedInvoice:
        """
        对发票进行智能分类
        自动填充：expense_category, debit_account, credit_account, voucher_summary
        """
        # 1. 费用类型分类
        if not invoice.expense_category:
            invoice.expense_category = self._classify_expense(invoice)
        
        # 2. 会计科目匹配
        invoice.debit_account = self.account_mapping["debit"].get(
            invoice.expense_category, "6602.99"  # 默认其他费用
        )
        invoice.credit_account = self.account_mapping["credit"]["default"]
        
        # 3. 生成凭证摘要
        if not invoice.voucher_summary:
            invoice.voucher_summary = self._generate_summary(invoice)
        
        return invoice
    
    def _classify_expense(self, invoice: UnifiedInvoice) -> str:
        """根据发票内容分类费用类型"""
        # 根据票据类型直接判断
        if invoice.receipt_type == "train_ticket":
            return "差旅费"
        elif invoice.receipt_type == "flight_itinerary":
            return "差旅费"
        elif invoice.receipt_type == "taxi_receipt":
            return "交通费"
        elif invoice.receipt_type == "toll_receipt":
            return "通行费"
        elif invoice.receipt_type == "fiscal_receipt":
            return "财政票据"
        
        # 传统发票：根据销售方名称和商品名称匹配
        text = f"{invoice.seller_name or ''} {invoice.raw_text or ''}"
        
        for rule in self.expense_rules:
            for keyword in rule["keywords"]:
                if keyword in text:
                    return rule["category"]
        
        return "其他费用"
    
    def _generate_summary(self, invoice: UnifiedInvoice) -> str:
        """生成记账凭证摘要"""
        template = self.summary_templates.get(
            invoice.expense_category, "{date}费用支出"
        )
        
        date_str = invoice.billing_date or invoice.travel_date or ""
        departure = invoice.departure_station or ""
        arrival = invoice.arrival_station or ""
        
        summary = template.format(
            date=date_str,
            departure=departure,
            arrival=arrival
        )
        
        return summary


def smart_classify(invoice: UnifiedInvoice) -> UnifiedInvoice:
    """便捷函数：对发票进行智能分类"""
    classifier = SmartClassifier()
    return classifier.classify(invoice)


if __name__ == '__main__':
    # 测试
    invoice = UnifiedInvoice(
        receipt_type="train_ticket",
        transport_number="G123",
        total=500.0,
        departure_station="北京",
        arrival_station="上海",
        travel_date="2026-08-01"
    )
    
    result = smart_classify(invoice)
    print(result.to_json())
