#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电子档案合规归档管理器
按照《电子发票全流程电子化管理指南》生成标准归档包
支持四性检测、元数据采集、归档目录生成
"""

import os
import json
import hashlib
import zipfile
import shutil
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from io import BytesIO

from unified_invoice import UnifiedInvoice, RECEIPT_TYPES


class ArchiveManager:
    """
    电子档案合规归档管理器
    
    功能：
    1. 四性检测：真实性、完整性、可用性、安全性
    2. 元数据采集：自动提取归档元数据
    3. 归档包生成：标准 ZIP 格式归档包
    4. 归档目录生成：目录索引文件
    
    参考标准：
    - 《电子发票全流程电子化管理指南》（财政部、国家档案局）
    - GB/T 18894-2016《电子文件归档与电子档案管理规范》
    """
    
    ARCHIVE_VERSION = "1.0"
    ARCHIVE_FORMAT = "einvoice-archive"
    
    def __init__(self, output_dir: str = "./archive"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.invoices: List[Dict[str, Any]] = []
        self.metadata_list: List[Dict[str, Any]] = []
        self.four_properties_report: Dict[str, Any] = {}
    
    def add_invoice(self, invoice: UnifiedInvoice, original_file: Optional[str] = None) -> 'ArchiveManager':
        """添加发票到归档列表"""
        inv_data = {
            "invoice": invoice,
            "original_file": original_file,
            "added_at": datetime.now().isoformat(),
        }
        self.invoices.append(inv_data)
        return self
    
    def four_properties_check(self, invoice_file: str, invoice: Optional[UnifiedInvoice] = None) -> Dict[str, Any]:
        """
        四性检测：真实性、完整性、可用性、安全性
        
        Args:
            invoice_file: 发票文件路径
            invoice: 已解析的发票数据（可选）
        
        Returns:
            dict: 四性检测报告
        """
        file_path = Path(invoice_file)
        
        # === 1. 真实性检测 ===
        authenticity = self._check_authenticity(file_path, invoice)
        
        # === 2. 完整性检测 ===
        completeness = self._check_completeness(file_path, invoice)
        
        # === 3. 可用性检测 ===
        usability = self._check_usability(file_path)
        
        # === 4. 安全性检测 ===
        security = self._check_security(file_path)
        
        report = {
            "file": str(file_path),
            "file_name": file_path.name,
            "check_time": datetime.now().isoformat(),
            "authenticity": authenticity,
            "completeness": completeness,
            "usability": usability,
            "security": security,
            "overall_pass": all([
                authenticity.get("pass", False),
                completeness.get("pass", False),
                usability.get("pass", False),
                security.get("pass", False),
            ]),
        }
        
        self.four_properties_report = report
        return report
    
    def _check_authenticity(self, file_path: Path, invoice: Optional[UnifiedInvoice] = None) -> Dict[str, Any]:
        """真实性检测"""
        result = {
            "property": "真实性",
            "description": "检测电子发票是否为原始真实文件，未经篡改",
            "checks": [],
            "pass": True,
        }
        
        # 检查1：文件是否存在
        result["checks"].append({
            "item": "文件存在性",
            "pass": file_path.exists(),
            "detail": f"文件路径：{file_path}" if file_path.exists() else "文件不存在",
        })
        
        # 检查2：文件是否有数字签名/印章（简化检查）
        if invoice and invoice.check_code:
            result["checks"].append({
                "item": "校验码/密码区",
                "pass": True,
                "detail": f"校验码存在：{invoice.check_code[:6]}...",
            })
        elif invoice and invoice.invoice_number:
            result["checks"].append({
                "item": "发票号码",
                "pass": True,
                "detail": f"发票号码：{invoice.invoice_number}",
            })
        else:
            result["checks"].append({
                "item": "真伪标识",
                "pass": False,
                "detail": "未检测到校验码或发票号码",
            })
        
        # 检查3：发票号码格式校验
        if invoice and invoice.invoice_number:
            if invoice.receipt_type == "full_electronic" or invoice.invoice_type == "full_electronic":
                # 全电发票 20 位
                result["checks"].append({
                    "item": "全电发票号码格式",
                    "pass": len(invoice.invoice_number) == 20,
                    "detail": f"号码长度：{len(invoice.invoice_number)} 位",
                })
            else:
                # 传统发票 8-20 位
                result["checks"].append({
                    "item": "传统发票号码格式",
                    "pass": 8 <= len(invoice.invoice_number) <= 20,
                    "detail": f"号码长度：{len(invoice.invoice_number)} 位",
                })
        
        # 综合判定
        result["pass"] = all(c.get("pass", False) for c in result["checks"])
        return result
    
    def _check_completeness(self, file_path: Path, invoice: Optional[UnifiedInvoice] = None) -> Dict[str, Any]:
        """完整性检测"""
        result = {
            "property": "完整性",
            "description": "检测电子发票文件是否完整，未损坏或缺失",
            "checks": [],
            "pass": True,
        }
        
        # 检查1：文件大小（非空）
        if file_path.exists():
            size = file_path.stat().st_size
            result["checks"].append({
                "item": "文件大小",
                "pass": size > 0,
                "detail": f"文件大小：{size} 字节",
            })
        else:
            result["checks"].append({
                "item": "文件大小",
                "pass": False,
                "detail": "文件不存在，无法检测",
            })
        
        # 检查2：关键元数据完整性
        if invoice:
            required_fields = [
                ("invoice_number", "发票号码"),
                ("billing_date", "开票日期"),
                ("total", "价税合计"),
            ]
            for field_name, field_desc in required_fields:
                value = getattr(invoice, field_name, None)
                result["checks"].append({
                    "item": f"元数据-{field_desc}",
                    "pass": value is not None,
                    "detail": f"{field_desc}：{value}" if value else f"{field_desc}缺失",
                })
        else:
            result["checks"].append({
                "item": "元数据完整性",
                "pass": False,
                "detail": "未提供发票数据，无法验证元数据完整性",
            })
        
        # 综合判定
        result["pass"] = all(c.get("pass", False) for c in result["checks"])
        return result
    
    def _check_usability(self, file_path: Path) -> Dict[str, Any]:
        """可用性检测"""
        result = {
            "property": "可用性",
            "description": "检测电子发票文件是否能正常打开、读取和使用",
            "checks": [],
            "pass": True,
        }
        
        # 检查1：文件可读性
        if file_path.exists():
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(100)
                result["checks"].append({
                    "item": "文件可读性",
                    "pass": True,
                    "detail": "文件可正常读取",
                })
            except Exception as e:
                result["checks"].append({
                    "item": "文件可读性",
                    "pass": False,
                    "detail": f"文件读取失败：{e}",
                })
        else:
            result["checks"].append({
                "item": "文件可读性",
                "pass": False,
                "detail": "文件不存在",
            })
        
        # 检查2：文件格式识别
        if file_path.exists():
            ext = file_path.suffix.lower()
            supported_formats = ['.pdf', '.png', '.jpg', '.jpeg', '.xml', '.ofd', '.tiff', '.bmp']
            result["checks"].append({
                "item": "文件格式识别",
                "pass": ext in supported_formats,
                "detail": f"文件格式：{ext}",
            })
        
        # 综合判定
        result["pass"] = all(c.get("pass", False) for c in result["checks"])
        return result
    
    def _check_security(self, file_path: Path) -> Dict[str, Any]:
        """安全性检测"""
        result = {
            "property": "安全性",
            "description": "检测电子发票文件是否安全，未被篡改或感染",
            "checks": [],
            "pass": True,
        }
        
        # 检查1：文件哈希值（SHA256）
        if file_path.exists():
            try:
                sha256_hash = hashlib.sha256()
                with open(file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        sha256_hash.update(chunk)
                hash_value = sha256_hash.hexdigest()
                result["checks"].append({
                    "item": "文件哈希校验",
                    "pass": True,
                    "detail": f"SHA256：{hash_value[:16]}...",
                })
            except Exception as e:
                result["checks"].append({
                    "item": "文件哈希校验",
                    "pass": False,
                    "detail": f"哈希计算失败：{e}",
                })
        
        # 检查2：文件不是可执行文件（防止恶意文件）
        if file_path.exists():
            dangerous_extensions = ['.exe', '.dll', '.bat', '.cmd', '.ps1', '.vbs', '.js', '.scr']
            ext = file_path.suffix.lower()
            result["checks"].append({
                "item": "文件类型安全",
                "pass": ext not in dangerous_extensions,
                "detail": f"文件类型安全：{ext}" if ext not in dangerous_extensions else f"危险文件类型：{ext}",
            })
        
        # 综合判定
        result["pass"] = all(c.get("pass", False) for c in result["checks"])
        return result
    
    def extract_metadata(self, invoice: UnifiedInvoice) -> Dict[str, Any]:
        """
        元数据采集：自动提取归档元数据
        
        根据《电子发票全流程电子化管理指南》要求，采集以下元数据：
        - 基本信息：发票号码、代码、日期、金额
        - 主体信息：购买方、销售方
        - 税务信息：税额、税率、抵扣状态
        - 归档信息：归档时间、归档人、保管期限
        """
        metadata = {
            # 基本信息
            "invoice_number": invoice.invoice_number,
            "invoice_code": invoice.invoice_code,
            "billing_date": invoice.billing_date,
            "total_amount": invoice.total,
            "amount_excluding_tax": invoice.amount,
            "tax_amount": invoice.tax_amount,
            
            # 票据类型
            "receipt_type": invoice.receipt_type,
            "receipt_type_name": self._get_receipt_type_name(invoice.receipt_type),
            
            # 主体信息
            "buyer_name": invoice.buyer_name,
            "buyer_tax_id": invoice.buyer_tax_id,
            "seller_name": invoice.seller_name,
            "seller_tax_id": invoice.seller_tax_id,
            
            # 进项税信息
            "vat_deduction_rate": invoice.vat_deduction_rate,
            "vat_deduction_amount": invoice.vat_deduction_amount,
            
            # 归档元数据
            "archive_time": datetime.now().isoformat(),
            "archive_version": self.ARCHIVE_VERSION,
            "retention_period": "30年",  # 会计档案保管期限
            
            # 原始数据摘要
            "source_format": invoice.source_format,
            "confidence": invoice.confidence,
        }
        
        self.metadata_list.append(metadata)
        return metadata
    
    def _get_receipt_type_name(self, receipt_type: str) -> str:
        """获取票据类型名称"""
        return RECEIPT_TYPES.get(receipt_type, receipt_type)
    
    def generate_archive_package(self, package_name: Optional[str] = None) -> str:
        """
        生成标准归档包（ZIP 格式）
        
        归档包结构：
        ├── metadata.json          # 元数据总表
        ├── four_properties.json   # 四性检测报告
        ├── invoices/              # 原始发票文件
        │   ├── invoice_001.pdf
        │   └── invoice_002.xml
        ├── invoice_data.json      # 结构化发票数据
        └── README.txt             # 归档说明
        
        Args:
            package_name: 归档包名称（不含扩展名）
        
        Returns:
            str: 归档包路径
        """
        if not package_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            package_name = f"einvoice_archive_{timestamp}"
        
        package_path = self.output_dir / f"{package_name}.zip"
        
        with zipfile.ZipFile(str(package_path), 'w', zipfile.ZIP_DEFLATED) as zf:
            # 1. 元数据总表
            metadata_json = json.dumps(self.metadata_list, ensure_ascii=False, indent=2)
            zf.writestr("metadata.json", metadata_json)
            
            # 2. 四性检测报告
            if self.four_properties_report:
                fp_json = json.dumps(self.four_properties_report, ensure_ascii=False, indent=2)
                zf.writestr("four_properties.json", fp_json)
            
            # 3. 结构化发票数据
            invoice_data = []
            for inv_data in self.invoices:
                inv = inv_data.get("invoice")
                if inv:
                    invoice_data.append(inv.to_dict())
            inv_json = json.dumps(invoice_data, ensure_ascii=False, indent=2)
            zf.writestr("invoice_data.json", inv_json)
            
            # 4. 原始发票文件
            for i, inv_data in enumerate(self.invoices):
                original_file = inv_data.get("original_file")
                if original_file and Path(original_file).exists():
                    arc_name = f"invoices/{Path(original_file).name}"
                    zf.write(original_file, arc_name)
            
            # 5. 归档说明
            readme = self._generate_readme()
            zf.writestr("README.txt", readme)
        
        return str(package_path)
    
    def generate_archive_index(self) -> str:
        """
        生成归档目录索引文件
        
        Returns:
            str: 索引内容（文本格式）
        """
        lines = []
        lines.append("=" * 80)
        lines.append("电子发票归档目录索引")
        lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        lines.append("")
        
        for i, metadata in enumerate(self.metadata_list, 1):
            lines.append(f"【{i}】")
            lines.append(f"  发票号码：{metadata.get('invoice_number', 'N/A')}")
            lines.append(f"  开票日期：{metadata.get('billing_date', 'N/A')}")
            lines.append(f"  价税合计：{metadata.get('total_amount', 'N/A')} 元")
            lines.append(f"  销售方　：{metadata.get('seller_name', 'N/A')}")
            lines.append(f"  购买方　：{metadata.get('buyer_name', 'N/A')}")
            lines.append(f"  票据类型：{metadata.get('receipt_type_name', 'N/A')}")
            lines.append("")
        
        lines.append("=" * 80)
        lines.append(f"共 {len(self.metadata_list)} 张发票")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _generate_readme(self) -> str:
        """生成归档说明"""
        lines = []
        lines.append("=" * 60)
        lines.append("电子发票归档包说明")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"归档版本：{self.ARCHIVE_VERSION}")
        lines.append(f"归档格式：{self.ARCHIVE_FORMAT}")
        lines.append(f"归档时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"发票数量：{len(self.invoices)} 张")
        lines.append("")
        lines.append("文件清单：")
        lines.append("  - metadata.json：发票元数据总表")
        lines.append("  - four_properties.json：四性检测报告")
        lines.append("  - invoice_data.json：结构化发票数据")
        lines.append("  - invoices/：原始发票文件")
        lines.append("")
        lines.append("参考标准：")
        lines.append("  - 《电子发票全流程电子化管理指南》")
        lines.append("  - GB/T 18894-2016 电子文件归档与电子档案管理规范")
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def process_batch(self, invoice_files: List[str], extract_data: bool = True) -> Dict[str, Any]:
        """
        批量处理归档
        
        Args:
            invoice_files: 发票文件路径列表
            extract_data: 是否提取结构化数据
        
        Returns:
            dict: 处理结果汇总
        """
        results = {
            "total": len(invoice_files),
            "success": 0,
            "failed": 0,
            "errors": [],
        }
        
        for file_path in invoice_files:
            try:
                # 四性检测报告
                self.four_properties_check(file_path)
                
                results["success"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "file": file_path,
                    "error": str(e),
                })
        
        return results


# === 便捷函数 ===

def create_archive(invoice_files: List[str], output_dir: str = "./archive") -> str:
    """
    便捷函数：创建归档包
    
    Args:
        invoice_files: 发票文件列表
        output_dir: 输出目录
    
    Returns:
        str: 归档包路径
    """
    manager = ArchiveManager(output_dir)
    
    for file_path in invoice_files:
        if Path(file_path).exists():
            manager.four_properties_check(file_path)
    
    return manager.generate_archive_package()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python archive_manager.py <path_to_invoice_file_or_dir>")
        sys.exit(1)
    
    target = sys.argv[1]
    manager = ArchiveManager()
    
    if Path(target).is_dir():
        # 目录：批量处理
        files = list(Path(target).glob("**/*"))
        files = [f for f in files if f.suffix.lower() in ('.pdf', '.png', '.jpg', '.xml', '.ofd')]
        
        for f in files:
            manager.four_properties_check(str(f))
        
        output = manager.generate_archive_package()
        print(f"归档包已生成：{output}")
        
        # 输出目录索引
        index = manager.generate_archive_index()
        print("\n" + index)
    else:
        # 单个文件
        report = manager.four_properties_check(target)
        print(json.dumps(report, ensure_ascii=False, indent=2))
