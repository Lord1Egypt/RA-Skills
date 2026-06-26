"""Layer 2 — Outbound Content Gate."""
import re
from ..models import LayerResult, OutboundResult, RiskLevel

_API_RE = [re.compile(p) for p in [
    r"sk-[a-zA-Z0-9]{20,}",
    r"AKIA[A-Z0-9]{16}",
    r"xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+",
    r"xapp-[0-9-a-zA-Z]+",
    r"ghp_[a-zA-Z0-9]{36}",
    r"AIza[0-9A-Za-z\-_]{35}",
    r"bot[0-9]+:[a-zA-Z0-9\-_]{35}",
    r"pat[0-9a-zA-Z._]{20,}",
    r"Bearer\s+[a-zA-Z0-9\-._~+/]{20,}={0,2}",
]]

_FILE_RE = [re.compile(p, re.IGNORECASE) for p in [
    r"/[Uu]sers/[^/\s]+/\.[a-z]+/[^\s\"'<>]*(?:secret|token|key|credential)[^\s\"'<>]*",
    r"/[Hh]ome/[^/\s]+/\.[a-z]+/[^\s\"'<>]+",
    r"openclaw\.json",
    r"SOUL\.md|MEMORY\.md|AGENTS\.md",
]]

_IP_RE = [re.compile(p) for p in [
    r"\b10\.\d+\.\d+\.\d+\b",
    r"\b192\.168\.\d+\.\d+\b",
    r"\b127\.\d+\.\d+\.\d+\b",
    r"\blocalhost\b",
]]


def check_outbound(response: str, config) -> tuple[LayerResult, OutboundResult]:
    issues = []
    if config.outbound_block_api_keys:
        for p in _API_RE:
            if p.search(response):
                issues.append("API key/token in response"); break
    if config.outbound_block_file_paths:
        for p in _FILE_RE:
            if p.search(response):
                issues.append("Sensitive file path in response"); break
    if config.outbound_block_internal_ips:
        for p in _IP_RE:
            if p.search(response):
                issues.append("Internal IP/hostname in response"); break

    if issues:
        reason = "; ".join(issues)
        return (
            LayerResult(layer="outbound", passed=False, risk_level=RiskLevel.CRITICAL,
                        details={"issues": issues}, block_message=reason),
            OutboundResult(allowed=False, response="I can't share that information.", blocked_reason=reason),
        )
    return (
        LayerResult(layer="outbound", passed=True, risk_level=RiskLevel.SAFE),
        OutboundResult(allowed=True, response=response),
    )
