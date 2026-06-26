from __future__ import annotations

from dataclasses import dataclass

from .config import Settings


@dataclass(slots=True)
class ApprovalDecision:
    allowed: bool
    reason: str


class ApprovalGate:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def check(self, action: str) -> ApprovalDecision:
        if action == "draft_reply":
            return ApprovalDecision(True, "Draft generation is allowed.")
        if self.settings.civic_enabled:
            return ApprovalDecision(
                False,
                "Civic is marked enabled, but outbound actions are still blocked until the real approval flow is wired.",
            )
        return ApprovalDecision(
            False,
            "Outbound actions are blocked. Configure a real Civic approval flow before posting on behalf of a user.",
        )
