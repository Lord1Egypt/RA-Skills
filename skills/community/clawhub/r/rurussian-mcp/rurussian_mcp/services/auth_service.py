from dataclasses import asdict, dataclass
import os

from rurussian_mcp.config import DEFAULT_USER_AGENT


@dataclass
class PurchaseContext:
    email: str = ""
    plan: str = ""
    checkout_url: str = ""
    session_id: str = ""
    payment_status: str = ""


class AuthService:
    def __init__(self) -> None:
        self.api_key: str = os.getenv("RURUSSIAN_API_KEY", "")
        self.user_agent: str = DEFAULT_USER_AGENT
        self.paid_access: bool = False
        self.purchase_context = PurchaseContext()

    def authenticate(self, api_key: str, user_agent: str) -> None:
        self.api_key = api_key
        self.user_agent = user_agent
        self.paid_access = False

    def has_access(self) -> bool:
        return bool(self.api_key or self.paid_access)

    def get_headers(self, include_auth: bool = True) -> dict[str, str]:
        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json",
        }
        if include_auth and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def set_purchase_context(self, **kwargs: str) -> None:
        for key, value in kwargs.items():
            if hasattr(self.purchase_context, key) and value is not None:
                setattr(self.purchase_context, key, value)

    def set_paid_access(self, active: bool) -> None:
        self.paid_access = active
        if active:
            self.api_key = ""

    def get_api_key_preview(self) -> str:
        return self._redact(self.api_key)

    def status(self) -> dict[str, object]:
        authentication_method = "none"
        if self.api_key:
            authentication_method = "api_key"
        elif self.paid_access:
            authentication_method = "paid_checkout"
        return {
            "authenticated": self.has_access(),
            "authentication_method": authentication_method,
            "api_key_preview": self.get_api_key_preview(),
            "user_agent": self.user_agent,
            "purchase_context": asdict(self.purchase_context),
        }

    @staticmethod
    def _redact(value: str, visible: int = 4) -> str:
        if not value:
            return ""
        if len(value) <= visible * 2:
            return "*" * len(value)
        return f"{value[:visible]}{'*' * (len(value) - visible * 2)}{value[-visible:]}"


auth_service = AuthService()
