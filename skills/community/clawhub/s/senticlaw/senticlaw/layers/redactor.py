"""Layer 3 — PII & Secret Redaction."""
import re, hashlib
from ..models import LayerResult, RiskLevel

_PII = {
    "email":       r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b",
    "phone_us":    r"\b(?:\+?1[\s\-.]?)?\(?\d{3}\)?[\s\-.]?\d{3}[\s\-.]?\d{4}\b",
    "ssn":         r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b",
    "credit_card": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b",
}
_SECRETS = {
    "openai_key":       r"sk-[a-zA-Z0-9]{20,}",
    "bearer_token":     r"Bearer\s+[a-zA-Z0-9\-._~+/]{20,}={0,2}",
    "password_field":   r"(?i)(?:password|passwd|secret|token)\s*[:=]\s*\S+",
    "connection_string": r"(?:mongodb|mysql|postgres(?:ql)?|redis)(?:\+[a-z]+)?://[^\s\"']+",
}

_PII_RE    = {k: re.compile(v) for k, v in _PII.items()}
_SECRET_RE = {k: re.compile(v) for k, v in _SECRETS.items()}


def redact(text: str, mode: str = "mask",
           pii: bool = True, secrets: bool = True) -> tuple[str, dict]:
    result, replacements = text, {}

    def sub(kind, match_text):
        if mode == "tokenize":
            r = f"[{kind.upper()}:{hashlib.sha256(match_text.encode()).hexdigest()[:8]}]"
        elif mode == "remove":
            r = f"[{kind.upper()}:REDACTED]"
        else:
            r = f"[{kind.upper()}:***]"
        replacements[match_text] = r
        return r

    patterns = {}
    if pii:     patterns.update(_PII_RE)
    if secrets: patterns.update(_SECRET_RE)

    for kind, pattern in patterns.items():
        result = pattern.sub(lambda m, k=kind: sub(k, m.group()), result)

    return result, replacements


def check_redactor(text: str, config) -> tuple[LayerResult, str]:
    redacted, replacements = redact(text, config.redaction_mode,
                                    config.redact_pii, config.redact_secrets)
    return (
        LayerResult(layer="redactor", passed=True,
                    risk_level=RiskLevel.MEDIUM if replacements else RiskLevel.SAFE,
                    details={"count": len(replacements)}),
        redacted,
    )
