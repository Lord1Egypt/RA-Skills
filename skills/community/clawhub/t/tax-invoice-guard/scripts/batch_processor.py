#!/usr/bin/env python3
"""
InvoiceGuard Batch Invoice Processor
Supports: batch recognition → duplicate check → tax verification → summary report
Pro/Free tier access control via API key verification.
"""

import json
import sys
import re
import hashlib
import urllib.request
import urllib.error
import time
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from decimal import Decimal, InvalidOperation


# ─────────────────────────────────────────────────────────────────────────────
# Token Verification (2026-04-22: mandatory per MEMORY.md)
# ─────────────────────────────────────────────────────────────────────────────
VERIFY_URL = "https://api.yk-global.com/v1/verify"
_cache: Dict[str, tuple[bool, str, float]] = {}  # key -> (is_pro, tier, expiry)
CACHE_TTL = 300  # 5 minutes


def verify_api_key(api_key: str) -> tuple[bool, str]:
    """
    Verify API key via yk-global.com.
    Returns (is_pro, tier_name).
    Graceful degradation: invalid/missing key -> FREE tier.
    """
    if not api_key:
        return False, "FREE"

    # Check cache
    now = time.time()
    if api_key in _cache:
        is_pro, tier, expiry = _cache[api_key]
        if now < expiry:
            return is_pro, tier

    try:
        req = urllib.request.Request(
            VERIFY_URL,
            method="POST",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            data=b"{}",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("valid", False):
                prefix = (data.get("prefix") or "").upper()
                if "PRO" in prefix or "ENT" in prefix or "MAX" in prefix:
                    _cache[api_key] = (True, "PRO", now + CACHE_TTL)
                    return True, "PRO"
                if "STD" in prefix or "BSC" in prefix:
                    _cache[api_key] = (False, "STD", now + CACHE_TTL)
                    return False, "STD"
                _cache[api_key] = (False, "FREE", now + CACHE_TTL)
                return False, "FREE"
    except Exception:
        pass

    # Network error / invalid key -> FREE tier (graceful degradation)
    _cache[api_key] = (False, "FREE", now + CACHE_TTL)
    return False, "FREE"


# ─────────────────────────────────────────────────────────────────────────────
# Tier / Quota configuration
# ─────────────────────────────────────────────────────────────────────────────
FREE_MONTHLY_LIMIT = 20   # Free tier: 20 invoices/month


@dataclass
class TierConfig:
    """User tier configuration."""
    is_pro: bool = False
    monthly_processed: int = 0   # This month's processed count

    @staticmethod
    def from_api_key(api_key: str, monthly_processed: int = 0) -> "TierConfig":
        """Create TierConfig from API key verification."""
        is_pro, _ = verify_api_key(api_key)
        return TierConfig(is_pro=is_pro, monthly_processed=monthly_processed)

    def allow_batch(self, count: int) -> tuple[bool, str]:
        """
        Check if batch processing is allowed.
        Returns: (allowed, reason)
        """
        if self.is_pro:
            return True, "Pro tier unlimited"
        remaining = FREE_MONTHLY_LIMIT - self.monthly_processed
        if count > remaining:
            return False, (
                f"Free tier monthly limit is {FREE_MONTHLY_LIMIT} invoices, "
                f"you have processed {self.monthly_processed} this month, "
                f"this submission of {count} exceeds remaining quota {remaining}. "
                f"Please upgrade to Pro or try next month."
            )
        return True, f"Free tier: {remaining - count} invoices remaining"

    def allow_verify(self) -> tuple[bool, str]:
        """
        Check if tax verification API is allowed.
        Pro tier only.
        """
        if self.is_pro:
            return True, "Pro tier"
        return False, "Tax verification API is Pro-tier only. Please upgrade to Pro."

    def record_usage(self, count: int):
        """Record this month's usage."""
        self.monthly_processed += count


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _dec(val) -> Decimal:
    """安全转换为 Decimal（M-5 fix）。"""
    try:
        return Decimal(str(val))
    except (InvalidOperation, TypeError):
        return Decimal("0")


def _tax_id_pattern() -> str:
    """C-2 fix: 正确的正则表达式，使用非捕获组 alternation。"""
    # 错误示例: [纳税人识别号|税号]  ← 匹配单一字符
    # 正确写法: (?:纳税人识别号|税号)  ← alternation
    return r'(?:纳税人识别号|税号)[：:\s]*([A-Z0-9]{15,20})'


def _amount_from_text(text: str) -> Optional[float]:
    """
    从文本提取金额，支持千分位格式。
    C-4 fix: 正确匹配 ￥1,234.56 / ¥1,234.56 / 1,234.56元 等格式。
    """
    patterns = [
        # 价税合计/价税：货币符号 + 千分位
        r'[价税合计|价税][：:\s]*[￥¥]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)',
        # 无货币符号但有"元"后缀
        r'[价税合计|价税][：:\s]*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\s*元',
        # 合计/金额：千分位
        r'[合计|金额][：:\s]*[￥¥]?\s*(\d{1,3}(?:,\d{3})*\.\d{2})',
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            cleaned = m.group(1).replace(',', '')
            try:
                return float(cleaned)
            except ValueError:
                continue
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Invoice Record
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class InvoiceRecord:
    invoice_code: str = ""
    invoice_no: str = ""
    invoice_type: str = ""
    date: str = ""
    amount: float = 0.0
    tax_amount: float = 0.0
    buyer_name: str = ""
    buyer_tax_id: str = ""
    seller_name: str = ""
    seller_tax_id: str = ""
    items: str = ""
    file_path: str = ""
    file_type: str = ""    # jpg / png / pdf / ofd / xml / unknown
    raw_text: str = ""
    status: str = "pending"   # pending / duplicate / suspicious / clean
    verify_status: str = "unchecked"  # unchecked / normal / void / red /失控
    notes: str = ""

    def fields_hash(self) -> str:
        """
        生成完整 SHA256 指纹（M-1 fix: 不再截断，避免哈希碰撞风险）。
        M-5 fix: 使用 Decimal 确保金额精度。
        """
        key = (
            f"{self.invoice_code or ''}"
            f"{self.invoice_no or ''}"
            f"{_dec(self.amount)}"
            f"{self.date or ''}"
            f"{self.buyer_tax_id or ''}"
            f"{self.seller_tax_id or ''}"
        )
        return hashlib.sha256(key.encode()).hexdigest()

    def amount_decimal(self) -> Decimal:
        """M-5 fix: Decimal 格式金额用于精确比较。"""
        return _dec(self.amount)

    def to_dict(self):
        d = asdict(self)
        d["fields_hash"] = self.fields_hash()
        return d


# ─────────────────────────────────────────────────────────────────────────────
# Invoice type detection (M-2 fix: 机票行程单优先于电子发票)
# ─────────────────────────────────────────────────────────────────────────────
def detect_invoice_type(text: str, file_path: str = "") -> str:
    """
    根据文本和文件类型综合判断发票类型。
    M-2 fix: 机票/航空行程单识别优先于电子发票。
    M-6 fix: XML/OFD 文件类型参与判断。
    """
    ext = file_path.lower().split('.')[-1] if file_path else ""

    # 机票行程单（M-2 fix: 优先于电子发票检查）
    # 机票行程单是运输服务票据，有"航空运输电子客票行程单"标识
    if any(kw in text for kw in ['航空', '机票', '行程单', '航班', '出发地', '到达地']):
        return '机票行程单'

    # 电子发票 / 数电票（判断依据：文件名+内容）
    # M-6 fix: XML/OFD 文件默认归属电子发票
    if ext in ('xml', 'ofd'):
        return '电子发票'
    if '电子' in text or '数电' in text:
        return '电子发票'

    # 专用/普通发票
    if '专用发票' in text:
        return '增值税专用发票'
    if '普通发票' in text:
        return '增值税普通发票'

    # 出租车
    if '出租车' in text:
        return '出租车票'

    # 火车票
    if '火车' in text:
        return '火车票'

    return '其他票据'


# ─────────────────────────────────────────────────────────────────────────────
# XML/OFD parsing support (M-6 fix)
# ─────────────────────────────────────────────────────────────────────────────
def parse_ofd_text(raw_content: bytes) -> str:
    """
    解析 OFD 文件内容（简化实现）。
    M-6 fix: 补充 OFD 格式解析支持。
    OFD 是国家版式文档，目前用 textract/ofd-parser 解析；
    这里提供结构化提取入口。
    """
    # OFD 本质是 XML 打包，可尝试 UTF-8 解码提取文本
    try:
        text = raw_content.decode('utf-8', errors='ignore')
        # 提取 XML 标签内的文本内容
        texts = re.findall(r'>([^<]+)<', text)
        return ' '.join(t.strip() for t in texts if t.strip())
    except Exception:
        return ""


def parse_xml_text(raw_content: bytes) -> str:
    """
    解析 XML 格式发票（金税三期标准）。
    M-6 fix: 补充 XML 格式解析支持。
    """
    try:
        text = raw_content.decode('utf-8', errors='ignore')
        # 提取所有文本节点
        texts = re.findall(r'>([^<]+)<', text)
        return ' '.join(t.strip() for t in texts if t.strip())
    except Exception:
        return ""


def parse_invoice_text(text: str, file_path: str = "", raw_content: bytes = None) -> InvoiceRecord:
    """
    从 OCR/解析文本中提取发票字段。
    C-2 fix: 正确的 regex alternation。
    C-4 fix: 千分位金额提取。
    M-2 fix: 机票行程单优先识别。
    M-6 fix: XML/OFD 内容解析。
    """
    # M-6 fix: 如果传入了原始字节内容（XML/OFD），先尝试解析
    if raw_content:
        ext = file_path.lower().split('.')[-1] if file_path else ""
        if ext == 'ofd':
            text = parse_ofd_text(raw_content) + " " + text
        elif ext == 'xml':
            text = parse_xml_text(raw_content) + " " + text

    record = InvoiceRecord(raw_text=text, file_path=file_path)

    # 推断文件类型（M-6 fix: 增加 ofd/xml 类型识别）
    if file_path:
        ext = file_path.lower().split('.')[-1]
        record.file_type = ext if ext in ('jpg', 'png', 'pdf', 'ofd', 'xml') else 'unknown'

    # 发票代码（C-2 fix: alternation 语法）
    m = re.search(r'(?:发票代码|代码)[：:\s]*(\d{8,12})(?:[^\d]|$)', text)
    if m:
        record.invoice_code = m.group(1)

    # 发票号码（8位）（C-2 fix: alternation 语法）
    m = re.search(r'(?:发票号码|号码)[：:\s]*(\d{8})(?:[^\d]|$)', text)
    if m:
        record.invoice_no = m.group(1)

    # 金额（C-4 fix: 千分位支持）
    amount = _amount_from_text(text)
    if amount is not None:
        record.amount = amount

    # 税额（C-4 fix: 千分位支持）
    m = re.search(r'税额[：:\s]*[￥¥]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)', text)
    if m:
        try:
            record.tax_amount = float(m.group(1).replace(',', ''))
        except ValueError:
            pass

    # 日期
    m = re.search(r'(\d{4}[年\-/]\d{1,2}[月\-/]\d{1,2}[日]?)', text)
    if m:
        record.date = re.sub(r'[年日月]', '-', m.group(1)).rstrip('-')

    # 纳税人识别号（C-2 fix: alternation）
    tax_ids = re.findall(_tax_id_pattern(), text)
    if len(tax_ids) >= 2:
        record.buyer_tax_id = tax_ids[0]
        record.seller_tax_id = tax_ids[1]
    elif len(tax_ids) == 1:
        record.buyer_tax_id = tax_ids[0]

    # 购买方/销售方（C-2 fix: alternation）
    buyer_m = re.search(r'(?:购买方|购货方|购买单位)[：:\s]*([^\n\r]{2,50})', text)
    if buyer_m:
        record.buyer_name = buyer_m.group(1).strip()
    seller_m = re.search(r'(?:销售方|销货方|开票方)[：:\s]*([^\n\r]{2,50})', text)
    if seller_m:
        record.seller_name = seller_m.group(1).strip()

    # 发票类型（M-2 fix: 机票优先于电子发票）
    record.invoice_type = detect_invoice_type(text, file_path)

    return record


# ─────────────────────────────────────────────────────────────────────────────
# Batch duplicate checking
# ─────────────────────────────────────────────────────────────────────────────
def batch_check_duplicates(
    records: List[InvoiceRecord],
    historical_records: List[dict] = None,
) -> List[InvoiceRecord]:
    """
    批量查重：支持跨批次查重（M-3 fix）。
    - 第一轮：当前批次内部两两比对
    - 第二轮：与历史批次记录比对
    M-5 fix: 使用 Decimal 进行金额比较。
    """
    historical_records = historical_records or []

    for i, record in enumerate(records):
        is_dup = False
        notes_parts = []

        # ── 第一轮：与当前批次中已处理的记录比对 ──
        for j, existing in enumerate(records[:i]):
            # 精确匹配（发票代码+号码）
            if record.invoice_code and record.invoice_no:
                if (record.invoice_code == existing.invoice_code
                        and record.invoice_no == existing.invoice_no):
                    # M-5 fix: Decimal 精确比较
                    if abs(record.amount_decimal() - existing.amount_decimal()) > Decimal("0.01"):
                        notes_parts.append(
                            f"与第{j+1}条发票号码相同但金额不同 ⚠️ 疑似篡改"
                        )
                        record.status = "suspicious"
                    else:
                        notes_parts.append(f"与第{j+1}条发票号码完全相同")
                        record.status = "duplicate"
                    is_dup = True
                    continue

            # 字段哈希碰撞
            if record.fields_hash() == existing.fields_hash() and record.fields_hash():
                notes_parts.append(f"与第{j+1}条关键字段一致")
                record.status = "duplicate"
                is_dup = True
                continue

            # 金额+日期+购买方相同但号码不同（克隆风险）（M-5 fix: Decimal）
            if (abs(record.amount_decimal() - existing.amount_decimal()) <= Decimal("0.01")
                    and record.date == existing.date
                    and record.buyer_tax_id == existing.buyer_tax_id
                    and not (record.invoice_no == existing.invoice_no)):
                notes_parts.append(f"与第{j+1}条金额+日期+购买方相同但号码不同 ⚠️")
                record.status = "suspicious"
                is_dup = True

        # ── 第二轮：与历史批次记录比对（M-3 fix: 跨批次查重） ──
        for existing_dict in historical_records:
            exist_code = (existing_dict.get("invoice_code", "") or "") + (
                existing_dict.get("invoice_no", "") or ""
            )
            new_code = (record.invoice_code or "") + (record.invoice_no or "")

            # 精确匹配
            if new_code and exist_code and new_code == exist_code:
                exist_amount = existing_dict.get("amount", 0.0)
                if abs(record.amount_decimal() - _dec(exist_amount)) > Decimal("0.01"):
                    notes_parts.append(f"跨批次：发票号码相同但金额与历史记录不符 ⚠️")
                    record.status = "suspicious"
                else:
                    notes_parts.append(f"跨批次重复：与历史记录发票号码重复")
                    record.status = "duplicate"
                is_dup = True
                continue

            # 字段哈希碰撞（跨批次）
            exist_hash = existing_dict.get("fields_hash", "")
            if record.fields_hash() and record.fields_hash() == exist_hash:
                notes_parts.append(f"跨批次：与历史记录关键字段一致")
                record.status = "duplicate"
                is_dup = True

        if not is_dup:
            record.status = "clean"
        record.notes = "；".join(notes_parts) if notes_parts else ""

    return records


# ─────────────────────────────────────────────────────────────────────────────
# Tax verification (C-3 fix: Pro-only)
# ─────────────────────────────────────────────────────────────────────────────
def verify_invoice_tax(
    record: InvoiceRecord,
    tier: TierConfig,
) -> tuple[str, str]:
    """
    调用国税查验平台验证发票真伪。
    C-3 fix: 仅 Pro 版可用。
    Returns: (verify_status, message)
    """
    allowed, msg = tier.allow_verify()
    if not allowed:
        return "unchecked", msg

    # TODO: 调用国家税务总局增值税发票查验平台 API
    # 参考: references/tax-api.md
    # 此处占位，实际接入需要企业纳税人账号
    return "unchecked", "国税查验 API 接入占位（待配置企业账号）"


# ─────────────────────────────────────────────────────────────────────────────
# Summary report
# ─────────────────────────────────────────────────────────────────────────────
def generate_summary(records: List[InvoiceRecord], tier: TierConfig = None) -> dict:
    """生成汇总统计（包含版本信息 C-3 fix）。"""
    total = len(records)
    duplicate = sum(1 for r in records if r.status == "duplicate")
    suspicious = sum(1 for r in records if r.status == "suspicious")
    total_amount = sum(r.amount for r in records)

    by_type: Dict[str, Dict[str, Any]] = {}
    for r in records:
        by_type.setdefault(r.invoice_type, {"count": 0, "amount": 0.0})
        by_type[r.invoice_type]["count"] += 1
        by_type[r.invoice_type]["amount"] += r.amount

    result = {
        "total_invoices": total,
        "duplicate_count": duplicate,
        "suspicious_count": suspicious,
        "clean_count": total - duplicate - suspicious,
        "total_amount": round(total_amount, 2),
        "duplicate_amount": round(
            sum(r.amount for r in records if r.status in ("duplicate", "suspicious")), 2
        ),
        "by_type": by_type,
    }

    # C-3 fix: 附带版本/配额信息
    if tier:
        result["tier"] = {
            "is_pro": tier.is_pro,
            "monthly_limit": 999999 if tier.is_pro else FREE_MONTHLY_LIMIT,
            "monthly_processed": tier.monthly_processed,
            "remaining": (999999 if tier.is_pro else FREE_MONTHLY_LIMIT) - tier.monthly_processed,
        }

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Main CLI
# ─────────────────────────────────────────────────────────────────────────────
def main():
    """
    CLI entry point.
    Usage: python3 batch_processor.py <json> [historical_json] [--api-key KEY]
    Or with tier JSON: python3 batch_processor.py <json> [historical_json] [tier_json] [api_key]
    """
    # Parse arguments
    # Format: python3 batch_processor.py <json> [historical_json] [tier_json_or_api_key]
    if len(sys.argv) < 2:
        try:
            data = json.load(sys.stdin)
        except Exception:
            print(json.dumps({
                "error": "Usage: python3 batch_processor.py <json_array_of_texts> [historical_records_json] [tier_json]"
            }))
            sys.exit(1)
    else:
        data = json.loads(sys.argv[1])

    historical = []
    api_key = ""
    monthly_processed = 0

    if len(sys.argv) > 2:
        arg2 = sys.argv[2]
        if arg2.startswith("inv-") or arg2.startswith("IN"):
            # Looks like an API key
            api_key = arg2
        else:
            historical = json.loads(arg2)

    if len(sys.argv) > 3:
        arg3 = sys.argv[3]
        if not api_key and (arg3.startswith("inv-") or arg3.startswith("IN")):
            api_key = arg3
        elif not historical:
            tier_data = json.loads(arg3)
            monthly_processed = tier_data.get("monthly_processed", 0)
            api_key = tier_data.get("api_key", "")

    if len(sys.argv) > 4:
        api_key = sys.argv[4]

    # Verify API key to determine tier
    tier = TierConfig.from_api_key(api_key, monthly_processed)

    # Batch processing permission check
    if isinstance(data, dict) and "files" in data:
        batch_count = len(data["files"])
    elif isinstance(data, list):
        batch_count = len(data)
    else:
        batch_count = 0

    allowed, allow_msg = tier.allow_batch(batch_count)
    if not allowed:
        print(json.dumps({
            "error": "BATCH_LIMIT_EXCEEDED",
            "message": allow_msg,
            "tier": {
                "is_pro": tier.is_pro,
                "monthly_limit": FREE_MONTHLY_LIMIT if not tier.is_pro else "unlimited",
                "monthly_processed": tier.monthly_processed,
            }
        }, ensure_ascii=False))
        sys.exit(1)

    # Parse invoices
    if isinstance(data, dict) and "files" in data:
        records = []
        for f in data["files"]:
            text = f.get("text", "")
            path = f.get("path", "")
            raw_content = f.get("raw_content")
            if raw_content and isinstance(raw_content, str):
                raw_content = raw_content.encode('utf-8')
            records.append(parse_invoice_text(text, path, raw_content))
    elif isinstance(data, list):
        records = [parse_invoice_text(t) for t in data]
    else:
        print(json.dumps({"error": "Input format error, need JSON array or {files: [{path, text}]}"}))
        sys.exit(1)

    # Batch duplicate check (cross-batch M-3 fix)
    records = batch_check_duplicates(records, historical)

    # Record this month's usage
    tier.record_usage(len(records))

    # Summary
    summary = generate_summary(records, tier)

    # Tax verification (Pro tier only)
    for r in records:
        if r.verify_status == "unchecked":
            status, msg = verify_invoice_tax(r, tier)
            r.verify_status = status
            if status == "unchecked" and "仅 Pro" in msg:
                r.notes = (r.notes + "；" if r.notes else "") + msg

    output = {
        "summary": summary,
        "records": [r.to_dict() for r in records],
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
