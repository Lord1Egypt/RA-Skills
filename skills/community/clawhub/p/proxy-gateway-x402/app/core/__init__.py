"""
Proxy Gateway - Core Module
"""

from .config import Settings, get_settings
from .exceptions import (
    ProxyGatewayException,
    AuthenticationError,
    FreeTrialExhaustedError,
    InsufficientBalanceError,
    InvalidUserIdError,
    InvalidTxHashError,
    DepositAlreadyProcessedError,
    ProxyNotAvailableError,
    TransactionFailedError,
)
from .security import (
    validate_user_id,
    validate_api_key,
    validate_tx_hash,
    validate_url,
    sanitize_user_id,
    generate_api_key,
    generate_client_id,
    mask_sensitive_string,
)

__all__ = [
    "Settings",
    "get_settings",
    "ProxyGatewayException",
    "AuthenticationError",
    "FreeTrialExhaustedError",
    "InsufficientBalanceError",
    "InvalidUserIdError",
    "InvalidTxHashError",
    "DepositAlreadyProcessedError",
    "ProxyNotAvailableError",
    "TransactionFailedError",
    "validate_user_id",
    "validate_api_key",
    "validate_tx_hash",
    "validate_url",
    "sanitize_user_id",
    "generate_api_key",
    "generate_client_id",
    "mask_sensitive_string",
]