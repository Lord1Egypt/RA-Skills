import os
from typing import Any


API_BASE_URL = os.getenv("RURUSSIAN_API_URL", "https://rurussian.com/api").rstrip("/")
DEFAULT_TIMEOUT = float(os.getenv("RURUSSIAN_TIMEOUT_SECONDS", "30"))
DEFAULT_USER_AGENT = os.getenv("RURUSSIAN_USER_AGENT", "ClawHub/1.0")

DEFAULT_LEARNER_ID = (
    os.getenv("RURUSSIAN_LEARNER_ID")
    or os.getenv("RURUSSIAN_LEARNER_EMAIL")
    or "default"
)
DEFAULT_LEARNER_EMAIL = os.getenv("RURUSSIAN_LEARNER_EMAIL", "")

MEMORY_STORE_PATH = os.getenv(
    "RURUSSIAN_MEMORY_STORE",
    os.path.join(os.path.expanduser("~"), ".rurussian_mcp", "learning_memory.json"),
)

PAYMENT_SUCCESS_STATUSES = {"paid", "success", "completed"}

BUY_SESSION_ENDPOINTS = tuple(
    endpoint.strip()
    for endpoint in os.getenv(
        "RURUSSIAN_BUY_SESSION_ENDPOINTS",
        "/create-checkout-session,/checkout/session,/billing/checkout-session",
    ).split(",")
    if endpoint.strip()
)

CONFIRM_PURCHASE_ENDPOINTS = tuple(
    endpoint.strip()
    for endpoint in os.getenv(
        "RURUSSIAN_CONFIRM_PURCHASE_ENDPOINTS",
        "/payment/complete,/verify-checkout-session,/checkout/verify,/payment/verify",
    ).split(",")
    if endpoint.strip()
)

PLAN_CATALOG: dict[str, dict[str, Any]] = {
    "month_1": {
        "price_usd": 3.75,
        "duration_days": 30,
        "display_name": "1 Month Subscription",
        "marketing_copy": "Fastest way to try RuRussian inside an autonomous tutor.",
    },
    "year_1": {
        "price_usd": 7.49,
        "duration_days": 365,
        "display_name": "1 Year Subscription",
        "marketing_copy": "Balanced plan for active Russian-learning agents.",
    },
    "year_3": {
        "price_usd": 21.74,
        "duration_days": 1095,
        "display_name": "3 Years Subscription",
        "marketing_copy": "Lowest long-term cost for always-on tutoring systems.",
    },
}
