#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一发票数据结构
兼容传统纸质/电子发票和全电发票（数电票）
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime


# === 票据类型枚举 ===
RECEIPT_TYPES = {
    "vat_invoice": "增值税发票",
    "train_ticket": "火车票",
    "flight_itinerary": "飞机行程单",
    "taxi_receipt": "出租车票",
    "fixed_invoice": "定额发票",
    "toll_receipt": "通行费票据",
    "fiscal_receipt": "财政票据",
}

# === 进项税抵扣率表 ===
VAT_DEDUCTION_RATES = {
    "train_ticket": 0.09,      # 火车票 9%
    "flight_itinerary": 0.09,  # 机票 9%（不含民航发展基金）
    "toll_receipt_highway": 0.03,  # 高速通行费 3%
    "toll_receipt_bridge": 0.05,   # 桥闸通行费 5%
    "vat_invoice_13": 0.13,    # 增值税专票 13%
    "vat_invoice_6": 0.06,     # 增值税专票 6%
    "vat_invoice_3": 0.03,     # 增值税专票 3%
    "taxi_receipt": 0.03,      # 出租车电子普票 3%
    "fixed_invoice": 0.0,      # 定额发票不可抵扣
    "fiscal_receipt": 0.0,     # 财政票据不可抵扣
}


@dataclass
class UnifiedInvoice:
    """统一发票数据结构 - 兼容传统发票、全电发票及各类票据"""
    
    # === 票种标识 ===
    invoice_type: str = "traditional"  # "traditional" | "full_electronic"
    
    # === 票据类型（方向二新增）===
    receipt_type: str = "vat_invoice"  # 见 ReceiptType 枚举
    
    # === 传统发票字段 ===
    invoice_code: Optional[str] = None        # 发票代码（10-12位，全电可能为空）
    invoice_number: Optional[str] = None      # 发票号码（传统8-20位；全电20位）
    
    # === 共有字段 ===
    billing_date: Optional[str] = None        # 开票日期
    amount: Optional[float] = None            # 不含税金额
    tax_amount: Optional[float] = None        # 税额
    total: Optional[float] = None             # 价税合计
    seller_name: Optional[str] = None         # 销售方名称
    seller_tax_id: Optional[str] = None       # 销售方税号
    buyer_name: Optional[str] = None          # 购买方名称
    buyer_tax_id: Optional[str] = None        # 购买方税号
    
    # === 全电发票特有字段 ===
    check_code: Optional[str] = None          # 校验码/二维码数据
    digital_account_id: Optional[str] = None  # 税务数字账户ID
    specific_business_info: Optional[str] = None  # 特定业务信息
    
    # === 方向二新增：多类型票据字段 ===
    passenger_name: Optional[str] = None       # 乘客/乘车人姓名
    departure_station: Optional[str] = None    # 出发站/机场
    arrival_station: Optional[str] = None      # 到达站/机场
    transport_number: Optional[str] = None     # 车次号/航班号
    travel_date: Optional[str] = None          # 乘车/乘机日期
    fuel_surcharge: Optional[float] = None     # 燃油附加费
    airport_construction_fee: Optional[float] = None  # 民航发展基金
    toll_road_type: Optional[str] = None       # 通行费类型：高速/桥闸
    taxi_license_plate: Optional[str] = None   # 出租车车牌号
    taxi_mileage: Optional[float] = None       # 出租车里程(km)
    pickup_time: Optional[str] = None          # 上车时间
    dropoff_time: Optional[str] = None         # 下车时间
    vehicle_type: Optional[str] = None         # 车辆类型：客车/货车
    fixed_invoice_code: Optional[str] = None   # 定额发票代码
    fiscal_receipt_type: Optional[str] = None  # 财政票据类型
    seat_class: Optional[str] = None           # 座位等级：二等座/一等座/商务座/经济舱
    
    # === 方向三新增：智能分类与自动入账字段 ===
    expense_category: Optional[str] = None      # 费用类型（差旅费/办公费/招待费/广告费等）
    vat_deduction_rate: Optional[float] = None # 进项税抵扣率（如0.09, 0.06, 0.13）
    vat_deduction_amount: Optional[float] = None  # 可抵扣进项税额（自动计算）
    debit_account: Optional[str] = None         # 借方科目
    credit_account: Optional[str] = None        # 贷方科目
    cost_center: Optional[str] = None           # 成本中心
    department: Optional[str] = None            # 归属部门
    project: Optional[str] = None               # 归属项目
    voucher_summary: Optional[str] = None       # 记账凭证摘要
    
    # === 数电票明细行（v4.5.0 新增）===
    # 每条明细：项目名称/规格型号/单位/数量/单价/金额/税率/税额
    detail_lines: List[Dict[str, Any]] = field(default_factory=list)

    # === 附加元数据 ===
    confidence: Optional[float] = None        # 识别置信度（OCR用）
    raw_text: Optional[str] = None            # 原始文本/数据（调试用）
    source_format: Optional[str] = None       # 来源格式: pdf|png|xml|ofd
    extracted_at: Optional[str] = None        # 提取时间
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典，便于JSON序列化"""
        result = asdict(self)
        # 添加计算字段
        if self.amount is not None and self.tax_amount is not None:
            result['calculated_total'] = round(self.amount + self.tax_amount, 2)
        return result
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    def validate(self) -> List[str]:
        """返回验证错误列表，空列表表示通过"""
        errors = []
        if not self.invoice_number:
            errors.append("发票号码为空")
        if self.invoice_type == "traditional":
            if self.invoice_code and len(self.invoice_code) not in (10, 11, 12):
                errors.append(f"传统发票代码长度异常：{len(self.invoice_code)}")
        elif self.invoice_type == "full_electronic":
            # 全电发票号码20位
            if self.invoice_number and len(self.invoice_number) != 20:
                errors.append(f"全电发票号码长度异常：{len(self.invoice_number)}，应为20位")
        return errors
