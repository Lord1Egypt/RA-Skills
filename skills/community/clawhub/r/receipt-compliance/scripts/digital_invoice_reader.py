#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数电票（全面数字化电子发票）直读模块 v4.5.0

提供不依赖通用 OCR 的数电票结构化直读能力：
1. PDF 文本层直读（pypdf 优先，缺失降级 pdfminer.six，再降级 OCR）
2. OFD 文字层直读（ofdparser 优先，缺失降级结构查看）
3. 票面要素正则抽取（共享 DigitalInvoiceTextParser，PDF/OFD 通用）
4. 二维码 TLV 解码核对（pyzbar 优先，缺失则跳过核对，不影响主流程）

设计约束（死规则 #9 / #10）：
- 所有第三方库均「优先 import，缺失即降级」，绝不强制塞依赖
- 纯标准库兜底，识别率不足时明确提示降级路径
"""

import io
import re
import sys
import json
import base64
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from unified_invoice import UnifiedInvoice


# ============================================================
# 一、文本层抽取（PDF / OFD 共用）
# ============================================================

class DigitalInvoiceTextParser:
    """
    数电票文本要素正则解析器
    适配主流数电票版面标签：发票号码 / 开票日期 / 价税合计 / 税额 / 税率 /
    销售方 / 购买方 / 名称 / 纳税人识别号 / 项目名称 等
    """

    # 标签 → 字段 的正则（宽松匹配中英文冒号与空格）
    _PATTERNS = {
        "invoice_number": r"(?:发票号码|发票号|No\.?|号码)[:：]?\s*([0-9]{20}|[0-9]{8,20})",
        "billing_date": r"(?:开票日期|填开日期|日期)[:：]?\s*"
                        r"(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日"
                        r"|\d{4}[-/]\d{1,2}[-/]\d{1,2})",
        "total": r"(?:价税合计|合计金额|价税总计)[:：]?\s*"
                 r"[（(]?大写[^)）]*[)）]?\s*"
                 r"(?:[￥¥¥]?\s*([\d,]+\.?\d*))?",
        "total_alt": r"(?:价税合计|合计金额)[:：]?\s*([￥¥]?\s*[\d,]+\.?\d*)",
        "tax_amount": r"(?:税额)[:：]?\s*([￥¥]?\s*[\d,]+\.?\d*)",
        "tax_rate": r"(?:税率|征收率)[:：]?\s*(\d+(?:\.\d+)?\s*%?)",
        "amount": r"(?:金额|不含税金额|合?计)[:：]?\s*([￥¥]?\s*[\d,]+\.?\d*)",
        "seller_name": r"(?:销售方)[:：]?\s*(.+?)(?:\n|$)",
        "buyer_name": r"(?:购买方)[:：]?\s*(.+?)(?:\n|$)",
        "seller_tax_id": r"(?:销售方).{0,20}?(?:纳税人识别号|识别号|税号)[:：]?\s*([A-Z0-9]{15,20})",
        "buyer_tax_id": r"(?:购买方).{0,20}?(?:纳税人识别号|识别号|税号)[:：]?\s*([A-Z0-9]{15,20})",
        "check_code": r"(?:校验码|密码区|校验)[:：]?\s*([0-9A-Za-z]{20,40})",
    }

    # 数电票特征词（用于判定是否为数电票文本）
    DIGITAL_MARKERS = ["全电发票", "数字化电子发票", "电子发票（增值税专用发票）",
                       "电子发票（普通发票）", "电子专用发票", "电子普通发票",
                       "国家税务总局", "发票号码"]

    @classmethod
    def looks_like_digital(cls, text: str) -> bool:
        """判断一段文本是否像数电票"""
        t = text or ""
        if len(re.findall(r"\d{20}", t)) >= 1:  # 出现 20 位发票号
            return True
        return any(m in t for m in cls.DIGITAL_MARKERS)

    @staticmethod
    def _clean_money(v: Optional[str]) -> Optional[float]:
        if not v:
            return None
        s = re.sub(r"[￥¥,\s]", "", v)
        try:
            return round(float(s), 2)
        except ValueError:
            return None

    @staticmethod
    def _norm_date(v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        s = v.replace(" ", "")
        for fmt_in, fmt_out in [("%Y年%m月%d日", "%Y-%m-%d"),
                                ("%Y-%m-%d", "%Y-%m-%d"),
                                ("%Y/%m/%d", "%Y-%m-%d")]:
            try:
                return datetime.strptime(s, fmt_in).strftime(fmt_out)
            except ValueError:
                continue
        return v

    @staticmethod
    def _safe_rate(v: Optional[str]) -> Optional[float]:
        if not v:
            return None
        s = v.strip().replace('%', '')
        try:
            f = float(s)
        except ValueError:
            return None
        return round(f / 100.0, 4) if f > 1 else round(f, 4)

    def parse(self, text: str) -> UnifiedInvoice:
        """从数电票文本抽取结构化数据"""
        inv = UnifiedInvoice(
            invoice_type="full_electronic",
            source_format="text",
            raw_text=text[:4000],
            extracted_at=datetime.now().isoformat(timespec="seconds"),
        )
        if not text:
            return inv

        def _search(key):
            m = re.search(self._PATTERNS[key], text, re.IGNORECASE)
            return m.group(1).strip() if m else None

        inv.invoice_number = _search("invoice_number")
        inv.billing_date = self._norm_date(_search("billing_date"))
        inv.check_code = _search("check_code")
        inv.seller_name = self._strip_tail(_search("seller_name"))
        inv.buyer_name = self._strip_tail(_search("buyer_name"))
        inv.seller_tax_id = _search("seller_tax_id")
        inv.buyer_tax_id = _search("buyer_tax_id")
        inv.tax_amount = self._clean_money(_search("tax_amount"))
        inv.tax_rate = self._safe_rate(_search("tax_rate"))

        total = self._clean_money(_search("total")) or self._clean_money(_search("total_alt"))
        inv.total = total
        amount = self._clean_money(_search("amount"))
        # 金额优先取「金额」标签；若缺失且价税合计/税额齐全，反算不含税金额
        if amount is None and total is not None and inv.tax_amount is not None:
            amount = round(total - inv.tax_amount, 2)
        inv.amount = amount

        # 明细行（按「项目名称」分行抽取）
        inv.detail_lines = self._extract_detail_lines(text)
        return inv

    @staticmethod
    def _strip_tail(v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        # 去掉尾部可能粘连的下一标签
        return re.split(r"[\n（(]", v)[0].strip()

    @staticmethod
    def _extract_detail_lines(text: str) -> List[Dict[str, Any]]:
        """按「*项目名称*」行抽取明细（数电票明细常不带结构化标签）"""
        lines: List[Dict[str, Any]] = []
        # 以 * 开头的明细行，如 *信息技术服务费* 金额
        for m in re.finditer(r"\*\s*([^*]+?)\s*\*", text):
            name = m.group(1).strip()
            if not name:
                continue
            # 取该行之后 30 字内的金额
            tail = text[m.end(): m.end() + 60]
            amt = re.search(r"([\d,]+\.\d{2})", tail)
            lines.append({
                "name": name,
                "spec": None,
                "unit": None,
                "quantity": None,
                "unit_price": None,
                "amount": DigitalInvoiceTextParser._clean_money(amt.group(1)) if amt else None,
                "tax_rate": None,
                "tax_amount": None,
            })
        return lines


# ============================================================
# 二、PDF 数电票直读
# ============================================================

class DigitalInvoicePDFReader:
    """数电票 PDF 直读：文本层优先，缺失降级 OCR，附带二维码核对"""

    def __init__(self, pdf_path: str):
        self.path = Path(pdf_path)
        if not self.path.exists():
            raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")

    def _extract_text(self) -> str:
        """优先 pypdf，其次 pdfminer.six，最后 OCR 降级"""
        # 1. pypdf
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(self.path))
            parts = [ (p.extract_text() or "") for p in reader.pages ]
            text = "\n".join(parts)
            if text.strip():
                return text
        except ImportError:
            pass
        except Exception:
            pass
        # 2. PyPDF2（旧名）
        try:
            from PyPDF2 import PdfReader as PR2
            reader = PR2(str(self.path))
            parts = [ (p.extract_text() or "") for p in reader.pages ]
            text = "\n".join(parts)
            if text.strip():
                return text
        except ImportError:
            pass
        except Exception:
            pass
        # 3. pdfminer.six
        try:
            from pdfminer.high_level import extract_text
            text = extract_text(str(self.path))
            if text.strip():
                return text
        except ImportError:
            pass
        except Exception:
            pass
        # 4. OCR 降级
        return self._ocr_fallback()

    def _ocr_fallback(self) -> str:
        """PDF 转图后用可用 OCR 引擎抽取（缺失则空）"""
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(str(self.path), first_page=1, last_page=3)
        except Exception:
            return ""
        try:
            from paddleocr import PaddleOCR
            ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
            buf = []
            for img in images:
                r = ocr.ocr(img, cls=True)
                if r and r[0]:
                    buf.append("\n".join(
                        (ln[1][0] if isinstance(ln[1], tuple) and len(ln[1]) >= 1 else "")
                        for ln in r[0]))
            return "\n".join(buf)
        except Exception:
            pass
        try:
            import pytesseract
            from PIL import Image
            buf = []
            for img in images:
                buf.append(pytesseract.image_to_string(img, lang='chi_sim+eng'))
            return "\n".join(buf)
        except Exception:
            return ""

    def _decode_qr(self) -> Optional[Dict[str, Any]]:
        """从 PDF 内嵌图片提取二维码并解码（pyzbar 优先，缺失返回 None）"""
        try:
            from pyzbar.pyzbar import decode as qr_decode
            from PIL import Image
        except ImportError:
            return None
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(self.path))
        except ImportError:
            try:
                from PyPDF2 import PdfReader
            except ImportError:
                return None
        try:
            for page in reader.pages:
                if not hasattr(page, "images"):
                    continue
                for img in page.images:
                    try:
                        data = img.data
                        im = Image.open(io.BytesIO(data)).convert("RGB")
                        for sym in qr_decode(im):
                            return parse_qr_content(sym.data.decode("utf-8", "ignore"))
                    except Exception:
                        continue
        except Exception:
            return None
        return None

    def read(self) -> Dict[str, Any]:
        """直读主入口：返回结构化 dict + 二维码核对结果"""
        text = self._extract_text()
        inv = DigitalInvoiceTextParser().parse(text)
        inv.source_format = "pdf"
        qr = self._decode_qr()
        qr_check = None
        if qr:
            qr_check = cross_check_invoice_qr(inv, qr)
            # 二维码号码优先回填（更可信）
            if qr.get("invoice_number") and not inv.invoice_number:
                inv.invoice_number = qr["invoice_number"]
        return {
            "type": "full_electronic_pdf",
            "receipt_type": "vat_invoice",
            "supported": True,
            "data": inv.to_dict(),
            "validation_errors": inv.validate(),
            "qr_check": qr_check,
            "message": "数电票 PDF 直读完成",
        }


# ============================================================
# 三、OFD 数电票直读
# ============================================================

class DigitalInvoiceOFDReader:
    """数电票 OFD 直读：ofdparser 取文字层，缺失降级结构查看"""

    def __init__(self, ofd_path: str):
        self.path = Path(ofd_path)
        if not self.path.exists():
            raise FileNotFoundError(f"OFD 文件不存在: {ofd_path}")

    def read(self) -> Dict[str, Any]:
        from ofd_parser import OFDParser
        parser = OFDParser(str(self.path))
        result = parser.parse()
        if result.get("extractable"):
            text = parser.extract_text()
            inv = DigitalInvoiceTextParser().parse(text)
            inv.source_format = "ofd"
            return {
                "type": "full_electronic_ofd",
                "receipt_type": "vat_invoice",
                "supported": True,
                "data": inv.to_dict(),
                "validation_errors": inv.validate(),
                "message": "数电票 OFD 直读完成",
            }
        # 降级：仅结构信息
        return {
            "type": "full_electronic_ofd",
            "receipt_type": "vat_invoice",
            "supported": False,
            "data": result,
            "message": "OFD 文字层不可用，请安装 ofdparser 或转为 PDF 后直读",
            "alternatives": result.get("install_hint", ""),
        }


# ============================================================
# 四、二维码 TLV / URL 解析与核对
# ============================================================

def parse_qr_content(raw: str) -> Optional[Dict[str, Any]]:
    """
    解析数电票二维码内容
    常见形态：
      - https://inv-veri.chinatax.gov.cn/...?fpdm=..&fphm=..&..  （含查验参数）
      - ofd:zip;<base64>                                      （OFD 压缩包）
      - 01:...;02:...  TLV 串
    返回结构化 dict，无法识别返回 None
    """
    if not raw:
        return None
    info: Dict[str, Any] = {}
    s = raw.strip()

    # 1. URL 带查询参数
    if "fphm=" in s or "InvoiceNo" in s or "invoiceNumber" in s:
        try:
            q = parse_qs(urlparse(s).query)
            for k, fk in (("fphm", "invoice_number"), ("InvoiceNo", "invoice_number"),
                          ("invoiceNumber", "invoice_number"),
                          ("fpdm", "invoice_code"), ("InvoiceCode", "invoice_code")):
                if k in q and q[k]:
                    info[fk] = q[k][0]
        except Exception:
            pass

    # 2. ofd:zip; base64
    if s.startswith("ofd:zip;"):
        info["qr_type"] = "ofd_zip"
        info["qr_payload"] = s
        try:
            b64 = s[len("ofd:zip;"):]
            info["ofd_bytes_len"] = len(base64.b64decode(b64))
        except Exception:
            pass

    # 3. TLV（标签:值; 分隔）
    if ";" in s and re.search(r"^\d{2}:", s):
        info["qr_type"] = "tlv"
        info["qr_payload"] = s
        for seg in s.split(";"):
            if ":" in seg:
                tag, _, val = seg.partition(":")
                info.setdefault("tlv", {})[tag] = val

    if not info:
        # 兜底：把整串当哈希留存
        info["qr_type"] = "raw"
        info["qr_payload"] = s
    return info


def cross_check_invoice_qr(inv: UnifiedInvoice, qr: Dict[str, Any]) -> Dict[str, Any]:
    """比对票面要素与二维码，给出核对结论"""
    issues = []
    if qr.get("invoice_number") and inv.invoice_number:
        if qr["invoice_number"] != inv.invoice_number:
            issues.append("发票号码与二维码不一致")
    if qr.get("invoice_code") and inv.invoice_code:
        if qr["invoice_code"] != inv.invoice_code:
            issues.append("发票代码与二维码不一致")
    return {
        "matched": len(issues) == 0,
        "issues": issues,
        "qr_type": qr.get("qr_type"),
    }


# ============================================================
# 便捷函数
# ============================================================

def read_digital_pdf(pdf_path: str) -> Dict[str, Any]:
    return DigitalInvoicePDFReader(pdf_path).read()


def read_digital_ofd(ofd_path: str) -> Dict[str, Any]:
    return DigitalInvoiceOFDReader(ofd_path).read()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python digital_invoice_reader.py <pdf|ofd> <path>")
        sys.exit(1)
    kind, path = sys.argv[1], sys.argv[2]
    if kind == "pdf":
        out = read_digital_pdf(path)
    elif kind == "ofd":
        out = read_digital_ofd(path)
    else:
        print("未知类型，仅支持 pdf / ofd"); sys.exit(1)
    print(json.dumps(out, ensure_ascii=False, indent=2))
