#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
票种自动识别模块 v4.3.0
根据文件类型、内容特征自动判断票据类型（支持10种票据）
并路由到对应解析器；集成 PaddleOCR 双引擎和混拍图切分
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

from unified_invoice import UnifiedInvoice, RECEIPT_TYPES
from xml_parser import FullElectronicInvoiceParser
from ofd_parser import OFDParser


# === 票据类型关键词特征表（用于OCR文本识别）===
RECEIPT_KEYWORDS = {
    "train_ticket": ["火车票", "高铁", "动车", "城际", "车次", "出发站", "到达站", "乘车人", "身份证号"],
    "flight_itinerary": ["飞机票", "行程单", "航班号", "乘机人", "出发机场", "到达机场", "票价", "燃油附加费", "民航发展基金"],
    "taxi_receipt": ["出租车", "打车", "车牌号", "里程", "等候时间", "上车时间", "下车时间"],
    "fixed_invoice": ["定额发票", "发票代码", "发票号码", "印章", "收款方"],
    "toll_receipt": ["通行费", "高速公路", "桥闸", "出口", "入口"],
    "fiscal_receipt": ["财政票据", "非税收入", "罚没", "缴款书", "执收单位"],
}


class InvoiceDetector:
    """
    票种识别器 + 路由器
    
    支持的文件扩展名：
    - 传统票据图片：.png, .jpg, .jpeg, .tiff, .bmp
    - 传统电子发票（PDF）：.pdf
    - 全电发票 XML：.xml
    - 全电发票 OFD：.ofd
    
    识别逻辑：
    1. 文件扩展名直接区分 XML/OFD
    2. 图片/PDF 文件通过 OCR 提取文本后，根据关键词匹配票据类型
    """
    
    TRADITIONAL_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    TRADITIONAL_PDF_EXTENSIONS = {'.pdf'}
    FULL_ELECTRONIC_XML_EXTENSIONS = {'.xml'}
    FULL_ELECTRONIC_OFD_EXTENSIONS = {'.ofd'}
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        self.extension = self.file_path.suffix.lower()
        self.size = self.file_path.stat().st_size
        self._ocr_text = None  # 缓存OCR结果
    
    def detect(self) -> str:
        """
        检测票种类型
        
        Returns:
            票据类型字符串，如 "traditional", "full_electronic_xml", "train_ticket" 等
        """
        # 1. 通过扩展名直接判断
        if self.extension in self.FULL_ELECTRONIC_XML_EXTENSIONS:
            return self._detect_xml_type()
        
        if self.extension in self.FULL_ELECTRONIC_OFD_EXTENSIONS:
            return "full_electronic_ofd"
        
        # 2. 图片/PDF 文件需要通过 OCR 内容判断
        if self.extension in self.TRADITIONAL_PDF_EXTENSIONS:
            # 数电票 PDF 优先尝试直读判定（文本层含 20 位票号/全电特征）
            pdf_type = self._detect_pdf_type()
            if pdf_type:
                return pdf_type
            return self._detect_image_type()
        if self.extension in self.TRADITIONAL_IMAGE_EXTENSIONS:
            return self._detect_image_type()
        
        # 3. 未知类型，尝试读取文件头判断
        return self._detect_by_content()
    
    def _detect_xml_type(self) -> str:
        """对于XML文件，判断是全电还是其他XML"""
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                head = f.read(2000)
            
            # 全电发票特征
            full_electronic_indicators = [
                'InvoiceNumber', 'Fphm', 'FPHM',
                'chinatax.gov.cn',
                'SellerName', 'BuyerName',
                'SpecificBusinessInfo',
            ]
            
            for indicator in full_electronic_indicators:
                if indicator in head:
                    return "full_electronic_xml"
            
            return "traditional"
            
        except Exception:
            return "traditional"
    
    def _detect_pdf_type(self) -> Optional[str]:
        """
        数电票 PDF 直读判定（v4.5.0）
        若 PDF 文本层含数电票特征（20 位票号/全电标志词），直接路由直读，
        避免误走通用 OCR 造成要素错位。
        """
        try:
            from digital_invoice_reader import DigitalInvoiceTextParser
        except Exception:
            return None
        try:
            from pypdf import PdfReader as PR
        except ImportError:
            try:
                from PyPDF2 import PdfReader as PR
            except ImportError:
                return None
        try:
            reader = PR(str(self.file_path))
            text = "\n".join((p.extract_text() or "") for p in reader.pages[:2])
            if DigitalInvoiceTextParser.looks_like_digital(text):
                return "full_electronic_pdf"
        except Exception:
            return None
        return None

    def _detect_image_type(self) -> str:
        """通过 OCR 文本特征判断票据类型"""
        # 尝试 OCR 提取文本
        try:
            ocr_text = self._try_ocr()
            if ocr_text:
                self._ocr_text = ocr_text
                return self._classify_by_ocr_text(ocr_text)
        except Exception:
            pass
        
        return "traditional"  # 默认传统发票
    
    def _try_ocr(self) -> str:
        """尝试 OCR 提取文本（优先 Paddle，降级 Tesseract）"""
        # 优先 PaddleOCR
        try:
            from paddleocr import PaddleOCR
            ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
            result = ocr.ocr(str(self.file_path), cls=True)
            if result and result[0]:
                lines = []
                for line in result[0]:
                    if line and len(line) >= 2:
                        text_info = line[1]
                        if isinstance(text_info, tuple) and len(text_info) >= 1:
                            lines.append(text_info[0])
                if lines:
                    return '\n'.join(lines)
        except ImportError:
            pass
        except Exception:
            pass
        
        # 降级 Tesseract
        try:
            import pytesseract
            from PIL import Image
            
            if self.extension in self.TRADITIONAL_PDF_EXTENSIONS:
                try:
                    from pdf2image import convert_from_path
                    images = convert_from_path(str(self.file_path), first_page=1, last_page=1)
                    if images:
                        return pytesseract.image_to_string(images[0], lang='chi_sim+eng')
                except Exception:
                    return ""
            else:
                img = Image.open(str(self.file_path))
                return pytesseract.image_to_string(img, lang='chi_sim+eng')
        except ImportError:
            return ""
        except Exception:
            return ""
    
    def _classify_by_ocr_text(self, text: str) -> str:
        """根据 OCR 文本匹配票据类型关键词"""
        scores = {}
        text_lower = text.lower()
        
        for receipt_type, keywords in RECEIPT_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[receipt_type] = score
        
        if scores:
            # 返回得分最高的类型
            return max(scores, key=scores.get)
        
        return "vat_invoice"  # 默认为增值税发票
    
    def _detect_by_content(self) -> str:
        """通过文件内容特征判断（文件头魔数）"""
        try:
            with open(self.file_path, 'rb') as f:
                header = f.read(16)
            
            # OFD 文件头标识（PK ZIP格式）
            if header[:4] == b'PK\x03\x04':
                return "full_electronic_ofd"
            
            # XML 文件（以 <?xml 开头）
            if header[:5] == b'<?xml':
                return self._detect_xml_type()
            
            # 默认传统格式
            return "traditional"
            
        except Exception:
            return "traditional"
    
    def get_route(self) -> Tuple[str, callable]:
        """
        获取路由信息和处理函数
        """
        receipt_type = self.detect()
        
        route_map = {
            "traditional": ("traditional", self._handle_traditional),
            "vat_invoice": ("vat_invoice", self._handle_traditional),
            "full_electronic_xml": ("full_electronic_xml", self._handle_full_electronic_xml),
            "full_electronic_ofd": ("full_electronic_ofd", self._handle_full_electronic_ofd),
            "full_electronic_pdf": ("full_electronic_pdf", self._handle_full_electronic_pdf),
            "train_ticket": ("train_ticket", self._handle_train_ticket),
            "flight_itinerary": ("flight_itinerary", self._handle_flight_itinerary),
            "taxi_receipt": ("taxi_receipt", self._handle_taxi_receipt),
            "fixed_invoice": ("fixed_invoice", self._handle_fixed_invoice),
            "toll_receipt": ("toll_receipt", self._handle_toll_receipt),
            "fiscal_receipt": ("fiscal_receipt", self._handle_fiscal_receipt),
        }
        
        return route_map.get(receipt_type, ("unknown", self._handle_unknown))
    
    def _handle_traditional(self) -> Dict[str, Any]:
        """传统发票处理入口"""
        return {
            "type": "traditional",
            "receipt_type": "vat_invoice",
            "message": "检测到增值税发票格式，请使用OCR引擎识别",
            "next_step": "使用 ocr_engine.py 进行识别",
            "supported": True,
            "engine": "ocr_engine.py"
        }
    
    def _handle_full_electronic_xml(self) -> Dict[str, Any]:
        """全电发票XML处理入口"""
        try:
            parser = FullElectronicInvoiceParser(str(self.file_path))
            parser.load()
            invoice = parser.parse()
            
            return {
                "type": "full_electronic_xml",
                "receipt_type": "vat_invoice",
                "message": "检测到全电发票XML格式",
                "next_step": "提取结构化数据",
                "supported": True,
                "data": invoice.to_dict(),
                "validation_errors": invoice.validate(),
            }
            
        except Exception as e:
            return {
                "type": "full_electronic_xml",
                "receipt_type": "vat_invoice",
                "message": f"解析失败: {e}",
                "supported": True,
                "error": str(e),
            }
    
    def _handle_full_electronic_ofd(self) -> Dict[str, Any]:
        """全电发票OFD处理入口（v4.5.0 升级为结构化直读）"""
        from ofd_parser import OFDParser
        parser = OFDParser(str(self.file_path))
        return parser.to_invoice()

    def _handle_full_electronic_pdf(self) -> Dict[str, Any]:
        """数电票 PDF 直读处理入口（v4.5.0）"""
        try:
            from digital_invoice_reader import read_digital_pdf
            return read_digital_pdf(str(self.file_path))
        except Exception as e:
            return {
                "type": "full_electronic_pdf",
                "receipt_type": "vat_invoice",
                "message": f"数电票 PDF 直读失败: {e}",
                "supported": False,
                "error": str(e),
                "next_step": "建议确认 PDF 含文本层或安装 pypdf 后重试",
            }
    
    def _handle_train_ticket(self) -> Dict[str, Any]:
        """火车票处理入口"""
        return {
            "type": "train_ticket",
            "receipt_type": "train_ticket",
            "message": "检测到火车票格式",
            "next_step": "请使用 train_parser.py 进行识别",
            "supported": True,
            "engine": "train_parser.py",
            "note": "请先使用OCR提取文本，再调用火车票的专用解析器"
        }
    
    def _handle_flight_itinerary(self) -> Dict[str, Any]:
        """飞机行程单处理入口"""
        return {
            "type": "flight_itinerary",
            "receipt_type": "flight_itinerary",
            "message": "检测到飞机行程单格式",
            "next_step": "请使用 flight_parser.py 进行识别",
            "supported": True,
            "engine": "flight_parser.py"
        }
    
    def _handle_taxi_receipt(self) -> Dict[str, Any]:
        """出租车票处理入口"""
        return {
            "type": "taxi_receipt",
            "receipt_type": "taxi_receipt",
            "message": "检测到出租车票格式",
            "next_step": "请使用 taxi_parser.py 进行识别",
            "supported": True,
            "engine": "taxi_parser.py"
        }
    
    def _handle_fixed_invoice(self) -> Dict[str, Any]:
        """定额发票处理入口"""
        return {
            "type": "fixed_invoice",
            "receipt_type": "fixed_invoice",
            "message": "检测到定额发票格式",
            "next_step": "请使用 fixed_parser.py 进行识别",
            "supported": True,
            "engine": "fixed_parser.py"
        }
    
    def _handle_toll_receipt(self) -> Dict[str, Any]:
        """通行费票据处理入口"""
        return {
            "type": "toll_receipt",
            "receipt_type": "toll_receipt",
            "message": "检测到通行费票据格式",
            "next_step": "请使用 toll_parser.py 进行识别",
            "supported": True,
            "engine": "toll_parser.py"
        }
    
    def _handle_fiscal_receipt(self) -> Dict[str, Any]:
        """财政票据处理入口"""
        return {
            "type": "fiscal_receipt",
            "receipt_type": "fiscal_receipt",
            "message": "检测到财政票据格式",
            "next_step": "请使用 fiscal_parser.py 进行识别",
            "supported": True,
            "engine": "fiscal_parser.py",
            "note": "财政票据不可抵扣进项税，但需入账处理"
        }
    
    def _handle_unknown(self) -> Dict[str, Any]:
        """未知类型处理"""
        return {
            "type": "unknown",
            "receipt_type": "unknown",
            "message": f"无法识别的文件格式: {self.extension}",
            "supported": False,
            "supported_formats": {
                "image": list(self.TRADITIONAL_IMAGE_EXTENSIONS),
                "pdf": list(self.TRADITIONAL_PDF_EXTENSIONS),
                "xml": list(self.FULL_ELECTRONIC_XML_EXTENSIONS),
                "ofd": list(self.FULL_ELECTRONIC_OFD_EXTENSIONS),
                "receipt_types": list(RECEIPT_TYPES.keys()),
            }
        }
    
    def process(self) -> Dict[str, Any]:
        """
        一键处理入口
        检测票种并自动调用对应解析器
        """
        receipt_type, handler = self.get_route()
        result = handler()
        result['file'] = str(self.file_path)
        result['file_size'] = self.size
        return result


def detect_and_process(file_path: str) -> Dict[str, Any]:
    """
    便捷函数：识别票种并自动处理
    """
    detector = InvoiceDetector(file_path)
    return detector.process()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python invoice_detector.py <path_to_invoice>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        result = detect_and_process(file_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"处理失败: {e}", file=sys.stderr)
        sys.exit(1)
