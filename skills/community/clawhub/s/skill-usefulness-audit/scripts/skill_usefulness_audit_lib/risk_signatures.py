from __future__ import annotations

from .risk_signatures_encoding import ENCODING_RISK_RULES
from .risk_signatures_execution import EXECUTION_RISK_RULES
from .risk_signatures_network import NETWORK_RISK_RULES
from .risk_signatures_sensitive import SENSITIVE_RISK_RULES


RISK_RULES = (
    *EXECUTION_RISK_RULES,
    *SENSITIVE_RISK_RULES,
    *NETWORK_RISK_RULES,
    *ENCODING_RISK_RULES,
)
