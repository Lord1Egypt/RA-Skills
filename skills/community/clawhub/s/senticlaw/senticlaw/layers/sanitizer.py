"""Layer 1 — Text Sanitization & Injection Detection."""
import re, unicodedata
from ..models import LayerResult, RiskLevel

_ZW_RE = re.compile(r"[\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad\u2060]")

_PATTERNS = [
    (r"ignore\s+(?:all\s+)?(?:previous|your|prior|the)?\s*(?:instructions?|rules?|guidelines?|prompts?|training)", RiskLevel.CRITICAL),
    (r"ignore\s+(?:all|previous|prior|your)\s+", RiskLevel.HIGH),
    (r"disregard\s+(?:your|all|previous)\s+(?:rules?|guidelines?|training|instructions?)", RiskLevel.CRITICAL),
    (r"forget\s+(?:everything|all|your|previous)", RiskLevel.CRITICAL),
    (r"your\s+new\s+(?:instructions?|rules?|system\s+prompt|persona)", RiskLevel.CRITICAL),
    (r"from\s+now\s+on\s+you\s+(?:are|will|must|should)", RiskLevel.HIGH),
    (r"you\s+are\s+now\s+(?:DAN|[A-Z]{2,12})\b", RiskLevel.CRITICAL),
    (r"pretend\s+(?:you\s+(?:are|have\s+no)|to\s+be)", RiskLevel.HIGH),
    (r"do\s+anything\s+now", RiskLevel.HIGH),
    (r"act\s+as\s+if\s+you\s+have\s+no\s+(?:rules?|guidelines?|restrictions?)", RiskLevel.HIGH),
    (r"override\s+(?:your\s+)?(?:safety|ethics|guidelines?|rules?|instructions?)", RiskLevel.CRITICAL),
    (r"jailbreak", RiskLevel.HIGH),
    (r"<system>", RiskLevel.HIGH),
    (r"\[system\]", RiskLevel.HIGH),
    (r"<\|im_start\|>", RiskLevel.HIGH),
    (r"```\s*system\s*\n", RiskLevel.HIGH),
    (r"###\s*system\s*prompt", RiskLevel.HIGH),
    (r"(?:reveal|show|print|output)\s+(?:your\s+)?(?:system\s+prompt|api\s+key|secret|token)", RiskLevel.HIGH),
    (r"repeat\s+(?:everything|all)\s+(?:above|before|prior)", RiskLevel.HIGH),
]
_COMPILED = [(re.compile(p, re.IGNORECASE | re.DOTALL), lvl) for p, lvl in _PATTERNS]
_ORDER = [RiskLevel.SAFE, RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]


def check_sanitizer(text: str, custom: list | None = None,
                    block_on: RiskLevel = RiskLevel.MEDIUM) -> LayerResult:
    # Strip zero-width chars + normalize
    clean = unicodedata.normalize("NFKC", _ZW_RE.sub("", text))

    flags, max_risk = [], RiskLevel.SAFE
    for pattern in (custom or []):
        if re.search(pattern, clean, re.IGNORECASE):
            flags.append(f"custom:{pattern[:40]}")
            max_risk = RiskLevel.HIGH

    for compiled, level in _COMPILED:
        m = compiled.search(clean)
        if m:
            flags.append(compiled.pattern[:60])
            if _ORDER.index(level) > _ORDER.index(max_risk):
                max_risk = level

    blocked = _ORDER.index(max_risk) >= _ORDER.index(block_on)
    return LayerResult(
        layer="sanitizer", passed=not blocked, risk_level=max_risk,
        details={"flags": flags[:5], "clean_text": clean},
        block_message="Input blocked: prompt injection detected." if blocked else "",
    )
