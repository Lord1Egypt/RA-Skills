#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全电发票 XML Schema 解析器
针对国家税务总局全电发票（数电票）XML 格式的解析
"""

import sys
import re
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import xml.etree.ElementTree as ET

from unified_invoice import UnifiedInvoice


class FullElectronicInvoiceParser:
    """
    全电发票 XML 解析器
    
    全电发票 XML 遵循国家税务总局制定的 Schema，
    包含票据头、票据项目、购买方、销售方等核心数据。
    """
    
    # 常见的全电发票 XML 命名空间
    NAMESPACES = {
        'root': 'http://www.chinatax.gov.cn',
        'inv': 'http://www.chinatax.gov.cn/invoice',
        'tax': 'http://www.chinatax.gov.cn/tax',
    }
    
    def __init__(self, xml_path: str):
        self.xml_path = Path(xml_path)
        self.tree = None
        self.root = None
        self.raw_data = {}
        
    def load(self) -> 'FullElectronicInvoiceParser':
        """加载并解析XML文件"""
        if not self.xml_path.exists():
            raise FileNotFoundError(f"XML文件不存在: {self.xml_path}")
        
        try:
            self.tree = ET.parse(str(self.xml_path))
            self.root = self.tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"XML解析失败: {e}")
        
        return self
    
    def _find_text(self, element, tag: str, use_namespace: bool = False) -> Optional[str]:
        """安全获取子元素文本"""
        if use_namespace:
            for ns in self.NAMESPACES.items():
                found = element.find(f'{{{ns[1]}}}{tag}')
                if found is not None and found.text:
                    return found.text.strip()
        else:
            # 尝试直接查找
            found = element.find(f'.//{tag}')
            if found is not None and found.text:
                return found.text.strip()
            
            # 尝试无命名空间查找
            for child in element.iter():
                if child.tag.split('}')[-1] == tag:
                    if child.text:
                        return child.text.strip()
        return None
    
    def _find_all_text(self, element, tag: str) -> list:
        """获取所有匹配元素的文本"""
        results = []
        for child in element.iter():
            if child.tag.split('}')[-1] == tag:
                if child.text:
                    results.append(child.text.strip())
        return results
    
    def parse(self) -> UnifiedInvoice:
        """解析XML并返回统一数据结构"""
        if self.root is None:
            raise RuntimeError("请先调用load()加载XML文件")
        
        invoice = UnifiedInvoice(
            invoice_type="full_electronic",
            source_format="xml",
            extracted_at=datetime.now().isoformat()
        )
        
        # 收集原始数据用于调试
        self.raw_data = self._iter_to_dict(self.root)
        
        # 提取核心字段
        self._extract_invoice_base(invoice)
        self._extract_parties(invoice)
        self._extract_amounts(invoice)
        self._extract_tax_details(invoice)
        
        # 存储原始XML文本
        invoice.raw_text = json.dumps(self.raw_data, ensure_ascii=False)
        
        return invoice
    
    def _iter_to_dict(self, element) -> Dict[str, Any]:
        """递归将XML元素转为字典"""
        tag = element.tag.split('}')[-1]
        result = {}
        
        if element.text and element.text.strip():
            result['_text'] = element.text.strip()
        
        for key, value in element.attrib.items():
            result[f'@{key.split("}")[-1]}'] = value
        
        for child in element:
            child_tag = child.tag.split('}')[-1]
            child_dict = self._iter_to_dict(child)
            
            if child_tag in result:
                if not isinstance(result[child_tag], list):
                    result[child_tag] = [result[child_tag]]
                result[child_tag].append(child_dict)
            else:
                result[child_tag] = child_dict
        
        return result
    
    def _extract_invoice_base(self, invoice: UnifiedInvoice):
        """提取发票基本信息"""
        root = self.root
        
        # 全电发票号码（20位数字）
        number = self._find_text(root, 'InvoiceNumber')
        if not number:
            number = self._find_text(root, 'Fphm')
        if not number:
            number = self._find_text(root, 'FPHM')
        invoice.invoice_number = number
        
        # 开票日期
        billing_date = self._find_text(root, 'BillingDate')
        if not billing_date:
            billing_date = self._find_text(root, 'Kprq')
        if not billing_date:
            billing_date = self._find_text(root, 'KPRQ')
        invoice.billing_date = self._normalize_date(billing_date)
        
        # 发票代码（全电票可能没有代码）
        code = self._find_text(root, 'InvoiceCode')
        if not code:
            code = self._find_text(root, 'Fpdm')
        if not code:
            code = self._find_text(root, 'FPDM')
        invoice.invoice_code = code
        
        # 校验码
        check = self._find_text(root, 'CheckCode')
        if not check:
            check = self._find_text(root, 'Yzm')
        if not check:
            check = self._find_text(root, 'YZM')
        invoice.check_code = check
        
        # 税务数字账户ID
        digital_id = self._find_text(root, 'DigitalAccountId')
        if not digital_id:
            digital_id = self._find_text(root, 'TaxDigitalId')
        invoice.digital_account_id = digital_id
        
        # 特定业务信息
        business_info = self._find_text(root, 'SpecificBusinessInfo')
        invoice.specific_business_info = business_info
    
    def _extract_parties(self, invoice: UnifiedInvoice):
        """提取买卖方信息"""
        root = self.root
        
        # 销售方
        seller_name = (
            self._find_text(root, 'SellerName') or
            self._find_text(root, 'Xfmc') or
            self._find_text(root, 'XFMC') or
            self._search_in_subtree(root, 'seller', 'name')
        )
        invoice.seller_name = seller_name
        
        seller_tax_id = (
            self._find_text(root, 'SellerTaxID') or
            self._find_text(root, 'Xfsh') or
            self._find_text(root, 'XFSH') or
            self._search_in_subtree(root, 'seller', 'tax')
        )
        invoice.seller_tax_id = seller_tax_id
        
        # 购买方
        buyer_name = (
            self._find_text(root, 'BuyerName') or
            self._find_text(root, 'Gfmc') or
            self._find_text(root, 'GFMC') or
            self._search_in_subtree(root, 'buyer', 'name')
        )
        invoice.buyer_name = buyer_name
        
        buyer_tax_id = (
            self._find_text(root, 'BuyerTaxID') or
            self._find_text(root, 'Gfsh') or
            self._find_text(root, 'GFSH') or
            self._search_in_subtree(root, 'buyer', 'tax')
        )
        invoice.buyer_tax_id = buyer_tax_id
    
    def _extract_amounts(self, invoice: UnifiedInvoice):
        """提取金额信息"""
        root = self.root
        
        amount = (
            self._find_text(root, 'Amount') or
            self._find_text(root, 'Hjje') or
            self._find_text(root, 'HJJE') or
            self._find_text(root, 'TotalAmountExcludingTax')
        )
        invoice.amount = self._safe_float(amount)
        
        tax_amount = (
            self._find_text(root, 'TaxAmount') or
            self._find_text(root, 'Hjse') or
            self._find_text(root, 'HJSE') or
            self._find_text(root, 'TotalTaxAmount')
        )
        invoice.tax_amount = self._safe_float(tax_amount)
        
        total = (
            self._find_text(root, 'Total') or
            self._find_text(root, 'Kphjje') or
            self._find_text(root, 'TotalAmountIncludingTax')
        )
        invoice.total = self._safe_float(total)
        
        # 如果价税合计为空，自动计算
        if invoice.total is None and invoice.amount is not None and invoice.tax_amount is not None:
            invoice.total = round(invoice.amount + invoice.tax_amount, 2)
    
    # === 数电票明细行标签映射（v4.5.0 新增）===
    _DETAIL_NAME_TAGS = {'ProjectName', 'Xmmc', 'XMMC', '项目名称', 'ItemName',
                         'GoodsName', 'Spmc', 'SPMC', 'Goods'}
    _DETAIL_SPEC_TAGS = {'Specification', 'Ggxh', 'GGXH', '规格型号', 'Spec', 'Gg'}
    _DETAIL_UNIT_TAGS = {'Unit', 'Dw', 'DW', '单位', 'MeasureUnit', 'Jldw', 'JLDW'}
    _DETAIL_QTY_TAGS = {'Quantity', 'Sl', 'SL', '数量', 'Qty', 'Xmsl', 'XMSL'}
    _DETAIL_PRICE_TAGS = {'UnitPrice', 'Dj', 'DJ', '单价', 'Price', 'Xmdj', 'XMDJ'}
    _DETAIL_AMOUNT_TAGS = {'Amount', 'Je', 'JE', '金额', 'DetailAmount', 'Xmje', 'XMJE',
                           'ProjectAmount', 'Hjje', 'HJJE'}
    _DETAIL_RATE_TAGS = {'TaxRate', 'Slv', 'SLV', '税率', 'TaxRates', 'TaxRateNew'}
    _DETAIL_TAX_TAGS = {'TaxAmount', 'Se', 'SE', '税额', 'Tax', 'Xmse', 'XMSE'}

    def _extract_tax_details(self, invoice: UnifiedInvoice):
        """提取数电票明细行项目（项目名称/规格/单位/数量/单价/金额/税率/税额）"""
        lines = []
        for elem in self.root.iter():
            if elem is self.root:
                continue
            child_tags = {c.tag.split('}')[-1] for c in elem if c is not None}

            def _child(tags):
                for c in elem:
                    if c.tag.split('}')[-1] in tags:
                        if c.text and c.text.strip():
                            return c.text.strip()
                return None

            # 仅当该节点同时含「名称」与「金额」子节点时，视为一条明细行
            name = _child(self._DETAIL_NAME_TAGS)
            amount = _child(self._DETAIL_AMOUNT_TAGS)
            if not name or not amount:
                continue

            line = {
                "name": name,
                "spec": _child(self._DETAIL_SPEC_TAGS),
                "unit": _child(self._DETAIL_UNIT_TAGS),
                "quantity": self._safe_float(_child(self._DETAIL_QTY_TAGS)),
                "unit_price": self._safe_float(_child(self._DETAIL_PRICE_TAGS)),
                "amount": self._safe_float(amount),
                "tax_rate": self._safe_rate(_child(self._DETAIL_RATE_TAGS)),
                "tax_amount": self._safe_float(_child(self._DETAIL_TAX_TAGS)),
            }
            lines.append(line)

        # 去重（同一父容器可能同时被父与子匹配，保留叶子级）
        invoice.detail_lines = self._dedup_lines(lines)

    @staticmethod
    def _dedup_lines(lines: list) -> list:
        """按字段集合去重，避免父子节点双重命中"""
        seen = set()
        out = []
        for ln in lines:
            key = tuple((k, ln.get(k)) for k in
                        ("name", "amount", "tax_amount", "quantity"))
            if key in seen:
                continue
            seen.add(key)
            out.append(ln)
        return out

    def _safe_rate(self, value: Optional[str]) -> Optional[float]:
        """税率安全转换：支持 0.13 / 13% / 13 等写法"""
        if not value:
            return None
        s = value.strip().replace('%', '').replace('％', '')
        try:
            f = float(s)
        except ValueError:
            return None
        if f > 1 and f <= 100:
            return round(f / 100.0, 4)
        return round(f, 4)
    
    def _search_in_subtree(self, root, party_type: str, field_type: str) -> Optional[str]:
        """在子树中搜索字段（如 seller subtree）"""
        # 遍历所有元素找到seller/buyer相关节点
        for elem in root.iter():
            tag = elem.tag.split('}')[-1].lower()
            if party_type in tag:
                for child in elem.iter():
                    child_tag = child.tag.split('}')[-1].lower()
                    if field_type == 'name' and ('name' in child_tag or 'mc' in child_tag):
                        if child.text:
                            return child.text.strip()
                    elif field_type == 'tax' and ('tax' in child_tag or 'sh' in child_tag or 'id' in child_tag):
                        if child.text:
                            return child.text.strip()
        return None
    
    def _normalize_date(self, date_str: Optional[str]) -> Optional[str]:
        """将日期标准化为 YYYY-MM-DD 格式"""
        if not date_str:
            return None
        
        # 尝试多种格式
        formats = [
            '%Y年%m月%d日',
            '%Y-%m-%d',
            '%Y%m%d',
            '%Y/%m/%d',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        return date_str
    
    def _safe_float(self, value: Optional[str]) -> Optional[float]:
        """安全转换为浮点数"""
        if not value:
            return None
        # 去除货币符号和千位分隔符
        cleaned = value.replace(',', '').replace('¥', '').replace('￥', '').strip()
        try:
            return round(float(cleaned), 2)
        except ValueError:
            return None


def parse_full_electronic_invoice(xml_path: str) -> dict:
    """
    便捷函数：解析全电发票XML文件
    返回统一数据结构的字典形式
    """
    parser = FullElectronicInvoiceParser(xml_path)
    parser.load()
    invoice = parser.parse()
    return invoice.to_dict()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python xml_parser.py <path_to_xml>")
        sys.exit(1)
    
    xml_path = sys.argv[1]
    try:
        result = parse_full_electronic_invoice(xml_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"解析失败: {e}", file=sys.stderr)
        sys.exit(1)
