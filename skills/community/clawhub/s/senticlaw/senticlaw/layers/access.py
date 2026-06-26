"""Layer 5 — Access Control."""
import re, os
from urllib.parse import urlparse
from ..models import LayerResult, RiskLevel

_PRIVATE_IP = re.compile(
    r"^(?:10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|127\.\d+\.\d+\.\d+|::1)$"
)
_INTERNAL_HOST = re.compile(
    r"^(?:localhost|.*\.local|.*\.internal|.*\.corp|.*\.lan)$", re.IGNORECASE
)


def check_path(path: str, allowed_dirs: list) -> LayerResult:
    try:
        real = os.path.realpath(os.path.expanduser(path))
        allowed = [os.path.realpath(os.path.expanduser(d)) for d in allowed_dirs]
        if any(real.startswith(a) for a in allowed):
            return LayerResult(layer="access", passed=True, risk_level=RiskLevel.SAFE)
        return LayerResult(layer="access", passed=False, risk_level=RiskLevel.HIGH,
                           block_message=f"Path '{path}' is outside allowed directories.")
    except Exception as e:
        return LayerResult(layer="access", passed=False, risk_level=RiskLevel.HIGH,
                           block_message=f"Invalid path: {e}")


def check_url(url: str, block_private: bool = True) -> LayerResult:
    if not block_private:
        return LayerResult(layer="access", passed=True, risk_level=RiskLevel.SAFE)
    try:
        host = urlparse(url).hostname or ""
    except Exception:
        return LayerResult(layer="access", passed=False, risk_level=RiskLevel.HIGH,
                           block_message=f"Invalid URL: {url}")
    if _PRIVATE_IP.match(host) or _INTERNAL_HOST.match(host):
        return LayerResult(layer="access", passed=False, risk_level=RiskLevel.HIGH,
                           block_message=f"Private/internal host blocked: {host}")
    return LayerResult(layer="access", passed=True, risk_level=RiskLevel.SAFE)


def check_tool(tool_name: str, allowed_tools: list) -> LayerResult:
    if not allowed_tools or tool_name in allowed_tools:
        return LayerResult(layer="access", passed=True, risk_level=RiskLevel.SAFE)
    return LayerResult(layer="access", passed=False, risk_level=RiskLevel.MEDIUM,
                       block_message=f"Tool '{tool_name}' not in allowlist.")
