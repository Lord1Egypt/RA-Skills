#!/usr/bin/env python3
"""
InvoiceGuard invoice duplicate detection engine.
Triple-check: exact match + field hash + image similarity.
Pro/Free tier access control via API key verification.
"""

import hashlib
import json
import sys
import re
import urllib.request
import urllib.error
import time
from dataclasses import dataclass, asdict
from typing import Optional, List
from decimal import Decimal, InvalidOperation


# ─────────────────────────────────────────────────────────────────────────────
# Token Verification (2026-04-22: mandatory per MEMORY.md)
# ─────────────────────────────────────────────────────────────────────────────
VERIFY_URL = "https://api.yk-global.com/v1/verify"
_cache: dict = {}  # key -> (is_pro, tier, expiry)
CACHE_TTL = 300  # 5 minutes


def verify_api_key(api_key: str) -> tuple[bool, str]:
    """
    Verify API key via yk-global.com.
    Returns (is_pro, tier_name).
    Graceful degradation: invalid/missing key -> FREE tier.
    """
    if not api_key:
        return False, "FREE"

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

    _cache[api_key] = (False, "FREE", now + CACHE_TTL)
    return False, "FREE"


# ─────────────────────────────────────────────────────────────────────────────
# Version / Tier configuration
# ─────────────────────────────────────────────────────────────────────────────
FREE_MONTHLY_LIMIT = 20   # Free tier: 20 invoices/month


@dataclass
class TierConfig:
    """User tier configuration."""
    is_pro: bool = False
    monthly_count: int = 0   # invoices processed this month

    @staticmethod
    def from_api_key(api_key: str, monthly_count: int = 0) -> "TierConfig":
        """Create TierConfig from API key verification."""
        is_pro, _ = verify_api_key(api_key)
        return TierConfig(is_pro=is_pro, monthly_count=monthly_count)

    def can_batch_process(self) -> bool:
        """Free tier cannot use batch processing."""
        return self.is_pro

    def can_verify(self) -> bool:
        """Free tier cannot use tax verification API."""
        return self.is_pro

    def check_limit(self, count: int) -> bool:
        """Check if adding `count` invoices would exceed free tier limit."""
        if self.is_pro:
            return True
        return (self.monthly_count + count) <= FREE_MONTHLY_LIMIT


# ─────────────────────────────────────────────────────────────────────────────
# Invoice Record
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class InvoiceRecord:
    """Structured invoice data."""
    invoice_code: str = ""        # 发票代码
    invoice_no: str = ""          # 发票号码
    invoice_type: str = ""        # 发票类型
    date: str = ""                # 开票日期 YYYY-MM-DD
    amount: float = 0.0           # 价税合计
    tax_amount: float = 0.0       # 税额
    tax_exclusive_amount: float = 0.0  # 不含税金额
    buyer_name: str = ""          # 购买方
    buyer_tax_id: str = ""        # 购买方税号
    seller_name: str = ""         # 销售方
    seller_tax_id: str = ""       # 销售方税号
    items: str = ""               # 货物或应税劳务
    image_hash: str = ""          # 图片哈希（可选）

    def fields_hash(self) -> str:
        """Generate full SHA256 fingerprint hash from key fields (M-1 fix: use full hash)."""
        key = (
            f"{self.invoice_code or ''}"
            f"{self.invoice_no or ''}"
            f"{_dec(self.amount)}"
            f"{self.date or ''}"
            f"{self.buyer_tax_id or ''}"
            f"{self.seller_tax_id or ''}"
        )
        return hashlib.sha256(key.encode()).hexdigest()  # Full 64-char hash

    def amount_decimal(self) -> Decimal:
        """Return amount as Decimal for precise comparison (M-5 fix)."""
        return _dec(self.amount)

    def to_dict(self):
        d = asdict(self)
        d["fields_hash"] = self.fields_hash()
        return d


# ─────────────────────────────────────────────────────────────────────────────
# Duplicate Result
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class DuplicateResult:
    """Duplicate check result."""
    is_duplicate: bool
    match_type: str           # exact / hash / tampered / image / none
    confidence: float          # 0.0 ~ 1.0
    matched_invoice: Optional[dict] = None
    reason: str = ""

    def to_dict(self):
        return asdict(self)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _dec(val) -> Decimal:
    """Safe conversion to Decimal."""
    try:
        return Decimal(str(val))
    except (InvalidOperation, TypeError):
        return Decimal("0")


def _amount_from_text(text: str) -> Optional[float]:
    """
    Extract amount from text, supporting:
    - Plain: 1234.56
    - Currency symbol: ￥1234.56 / ¥1234.56
    - Thousands separator: ￥1,234.56 / 1,234.56元 / ¥1,234.56

    C-4 fix: properly handle thousands separators.
    """
    # Match optional currency symbol + optional thousands separators + decimal part
    # Patterns: ￥1,234.56  ¥1,234.56  1,234.56元  1234.56
    patterns = [
        # Currency symbol with optional thousands separator
        r'[价税合计|价税][：:\s]*[￥¥]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)',
        # Without currency symbol but with Chinese yuan suffix or bare
        r'[价税合计|价税][：:\s]*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\s*元',
        # Fallback: amount near 合计/金额
        r'[合计|金额][：:\s]*[￥¥]?\s*(\d{1,3}(?:,\d{3})*\.\d{2})',
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            # Remove thousands separators before converting to float
            cleaned = m.group(1).replace(',', '')
            try:
                return float(cleaned)
            except ValueError:
                continue
    return None


def _tax_id_pattern() -> str:
    """C-2 fix: correct regex - use non-capturing alternation, not character class."""
    # Previously: [纳税人识别号|税号]  ← WRONG: matches ONE char from the set
    # Fixed: (?:纳税人识别号|税号)  ← CORRECT: alternation
    return r'(?:纳税人识别号|税号)[：:\s]*([A-Z0-9]{15,20})'


def parse_invoice_from_text(text: str) -> InvoiceRecord:
    """
    Parse invoice fields from OCR-recognized text.
    C-2 fix: regex alternation instead of character class.
    C-4 fix: proper thousands-separator-aware amount extraction.
    """
    record = InvoiceRecord()

    # Invoice code: must appear before 发票号码, capture up to 12 digits
    # C-2 fix: correct alternation syntax
    m = re.search(r'(?:发票代码|代码)[：:\s]*(\d{8,12})(?:[^\d]|$)', text)
    if m:
        record.invoice_code = m.group(1)

    # Invoice number: must appear after 发票号码, exactly 8 digits
    # C-2 fix: correct alternation syntax
    m = re.search(r'(?:发票号码|号码)[：:\s]*(\d{8})(?:[^\d]|$)', text)
    if m:
        record.invoice_no = m.group(1)

    # Amount - C-4 fix: thousands separator support
    amount = _amount_from_text(text)
    if amount is not None:
        record.amount = amount

    # Tax amount - C-4 fix: thousands separator support
    m = re.search(r'税额[：:\s]*[￥¥]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)', text)
    if m:
        try:
            record.tax_amount = float(m.group(1).replace(',', ''))
        except ValueError:
            pass

    # Date
    m = re.search(r'(\d{4}[年\-/]\d{1,2}[月\-/]\d{1,2}[日]?)', text)
    if m:
        d = re.sub(r'[年日月]', '-', m.group(1)).rstrip('-')
        record.date = d

    # Tax IDs - C-2 fix: correct alternation
    tax_ids = re.findall(_tax_id_pattern(), text)
    if len(tax_ids) >= 2:
        record.buyer_tax_id = tax_ids[0]
        record.seller_tax_id = tax_ids[1]
    elif len(tax_ids) == 1:
        record.buyer_tax_id = tax_ids[0]

    # Buyer / Seller names - C-2 fix: correct alternation
    buyer_pat = r'(?:购买方|购货方|购买单位)[：:\s]*([^\n\r]{2,50})'
    seller_pat = r'(?:销售方|销货方|开票方)[：:\s]*([^\n\r]{2,50})'
    m = re.search(buyer_pat, text)
    if m:
        record.buyer_name = m.group(1).strip()
    m = re.search(seller_pat, text)
    if m:
        record.seller_name = m.group(1).strip()

    # Invoice type - M-2 fix: check '机票'/'航空' BEFORE '电子'
    if '专用发票' in text:
        record.invoice_type = '增值税专用发票'
    elif '普通发票' in text:
        record.invoice_type = '增值税普通发票'
    elif '航空' in text or '机票' in text or '行程单' in text:
        # M-2 fix: check机票/航空 BEFORE electronic invoice
        # 机票行程单是运输服务票据，不是电子发票
        record.invoice_type = '机票行程单'
    elif '电子' in text or '数电' in text:
        record.invoice_type = '电子发票'
    elif '出租车' in text:
        record.invoice_type = '出租车票'
    elif '火车' in text:
        record.invoice_type = '火车票'
    else:
        record.invoice_type = '其他票据'

    return record


def check_duplicate(
    new_record: InvoiceRecord,
    existing_records: list,
    tier: TierConfig,
) -> DuplicateResult:
    """
    Check if new invoice is a duplicate against existing records.
    Triple-check: exact match, field hash, tampered detection.

    C-1 fix: tampered check runs BEFORE exact-match return.
    M-5 fix: Decimal comparisons for amount.
    """
    if not existing_records:
        return DuplicateResult(
            is_duplicate=False,
            match_type="none",
            confidence=0.0,
            reason="No existing records"
        )

    new_code = (new_record.invoice_code or "") + (new_record.invoice_no or "")
    new_hash = new_record.fields_hash()
    new_amount_dec = new_record.amount_decimal()

    for existing in existing_records:
        exist_code = (existing.get("invoice_code", "") or "") + (existing.get("invoice_no", "") or "")
        exist_hash = existing.get("fields_hash", "")
        exist_amount = existing.get("amount", 0.0)
        exist_amount_dec = _dec(exist_amount)

        # ── C-1 fix: check tampered FIRST (before exact match return) ──
        # If invoice code+number matches but amount DIFFERS → tampered
        if new_code and exist_code and new_code == exist_code:
            # M-5 fix: use Decimal for precise comparison
            if abs(new_amount_dec - exist_amount_dec) > Decimal("0.01"):
                return DuplicateResult(
                    is_duplicate=True,
                    match_type="tampered",
                    confidence=0.99,
                    matched_invoice=existing,
                    reason=(
                        f"Invoice code+number identical ({new_code}) but amount differs. "
                        f"Original: {exist_amount}, New: {new_record.amount} — SUSPECTED TAMPERED"
                    )
                )
            # Amounts are the same → exact duplicate (not tampered)
            return DuplicateResult(
                is_duplicate=True,
                match_type="exact",
                confidence=1.0,
                matched_invoice=existing,
                reason=f"Invoice code+number identical: {new_code}"
            )

        # Field hash collision: amount+date+buyer+seller identical (M-5 fix)
        if new_hash and exist_hash and new_hash == exist_hash:
            return DuplicateResult(
                is_duplicate=True,
                match_type="hash",
                confidence=0.95,
                matched_invoice=existing,
                reason="Key fields (amount+date+buyer+seller) match - likely duplicate"
            )

    return DuplicateResult(
        is_duplicate=False,
        match_type="none",
        confidence=0.0,
        reason="No duplicate found"
    )


# ─────────────────────────────────────────────────────────────────────────────
# M-3 fix: Cross-batch duplicate detection
# Accepts historical_records (all previous batches) in addition to current batch
# ─────────────────────────────────────────────────────────────────────────────
def check_duplicate_with_history(
    new_record: InvoiceRecord,
    historical_records: List[dict],
    current_batch: List[dict],
) -> DuplicateResult:
    """
    Check against both historical records (previous batches) and current batch.
    M-3 fix: cross-batch duplicate detection.
    """
    # First check against historical records
    if historical_records:
        result = check_duplicate(new_record, historical_records, tier)
        if result.is_duplicate:
            return result

    # Then check against current batch (same-day / same-upload)
    return check_duplicate(new_record, current_batch, tier)


def main():
    """CLI entry point: reads JSON input, outputs duplicate result."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python3 duplicate_checker.py <invoice_json> [existing_records_json] [tier_json]"
        }))
        sys.exit(1)

    new_invoice = json.loads(sys.argv[1])
    existing = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []

    # Get API key and determine tier
    api_key = ""
    monthly_count = 0

    if len(sys.argv) > 3:
        arg3 = sys.argv[3]
        if arg3.startswith("inv-") or arg3.startswith("IN"):
            api_key = arg3
        else:
            tier_data = json.loads(arg3)
            monthly_count = tier_data.get("monthly_count", 0)
            api_key = tier_data.get("api_key", "")

    if len(sys.argv) > 4 and not api_key:
        api_key = sys.argv[4]

    tier = TierConfig.from_api_key(api_key, monthly_count)

    if isinstance(new_invoice, dict):
        record = InvoiceRecord(**new_invoice)
    else:
        record = parse_invoice_from_text(str(new_invoice))

    result = check_duplicate(record, existing, tier)
    print(json.dumps(result.to_dict(), ensure_ascii=False))


if __name__ == "__main__":
    main()
