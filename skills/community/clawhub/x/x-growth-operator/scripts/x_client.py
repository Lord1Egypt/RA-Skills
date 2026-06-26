from __future__ import annotations

from dataclasses import dataclass


@dataclass
class XClientConfig:
    mode: str = "import"


class XClient:
    """
    Placeholder adapter for future live X integration.

    First version of this skill uses imported opportunity JSON so it remains
    testable inside OpenClaw without external credentials.
    """

    def __init__(self, config: XClientConfig | None = None):
        self.config = config or XClientConfig()

    def describe_mode(self) -> str:
        return self.config.mode
