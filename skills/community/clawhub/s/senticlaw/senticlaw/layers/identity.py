"""Layer 0 — Identity & Trust Verification."""
import re
from ..models import TrustLevel, LayerResult, RiskLevel

_SPOOF_PATTERNS = [
    r"\bi\s+am\s+(the\s+)?(owner|admin|administrator)\b",
    r"\bthis\s+is\s+(the\s+)?(owner|admin)\b",
    r"\bi\s+have\s+owner\s+(access|permission|rights)\b",
    r"\boverride\s+(permissions|access|policy)\b",
    r"\bacting\s+as\s+(owner|admin)\b",
    r"\bgrant\s+(me\s+)?(full|admin|owner)\s+access\b",
]
_SPOOF_RE = [re.compile(p, re.IGNORECASE) for p in _SPOOF_PATTERNS]


class TrustedSenderRegistry:
    def __init__(self, owner_ids: dict, trusted_senders: dict):
        self.owners  = {k: [str(i) for i in v] for k, v in owner_ids.items()}
        self.trusted = {k: [str(i) for i in v] for k, v in trusted_senders.items()}

    def trust_level(self, channel: str, sender_id: str) -> TrustLevel:
        sid = str(sender_id)
        if sid in self.owners.get(channel, []) + self.owners.get("*", []):
            return TrustLevel.OWNER
        if sid in self.trusted.get(channel, []) + self.trusted.get("*", []):
            return TrustLevel.TRUSTED
        return TrustLevel.UNKNOWN

    def has_spoof_claim(self, text: str) -> bool:
        return any(p.search(text) for p in _SPOOF_RE)


def check_identity(text: str, sender_id: str, channel: str,
                   registry: TrustedSenderRegistry,
                   block_unknown: bool = False) -> LayerResult:
    trust = registry.trust_level(channel, sender_id)

    if trust == TrustLevel.UNKNOWN and registry.has_spoof_claim(text):
        return LayerResult(
            layer="identity", passed=False, risk_level=RiskLevel.CRITICAL,
            details={"trust": trust.value, "spoofing": True},
            block_message="Identity spoofing attempt detected. Access denied.",
        )

    if trust == TrustLevel.BLOCKED:
        return LayerResult(
            layer="identity", passed=False, risk_level=RiskLevel.CRITICAL,
            details={"trust": trust.value},
            block_message="Sender is blocked.",
        )

    if trust == TrustLevel.UNKNOWN and block_unknown:
        return LayerResult(
            layer="identity", passed=False, risk_level=RiskLevel.HIGH,
            details={"trust": trust.value},
            block_message="Unrecognized sender. Access denied.",
        )

    return LayerResult(
        layer="identity", passed=True, risk_level=RiskLevel.SAFE,
        details={"trust": trust.value},
    )
