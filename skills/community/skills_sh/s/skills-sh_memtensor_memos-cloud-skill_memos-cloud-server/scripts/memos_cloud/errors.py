from __future__ import annotations

import json
import sys
from typing import Any, Dict, Optional


class MemosCloudError(Exception):
    """Base error that can be rendered as the skill's JSON error contract."""

    def __init__(self, error: str, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.error = error
        self.message = message
        self.status_code = status_code

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "error": self.error,
            "message": self.message,
        }
        if self.status_code is not None:
            payload["status_code"] = self.status_code
        return payload


class ConfigurationError(MemosCloudError):
    def __init__(self, message: str):
        super().__init__("Configuration Error", message)


class ValidationError(MemosCloudError):
    def __init__(self, message: str):
        super().__init__("Validation Error", message)


class ApiError(MemosCloudError):
    def __init__(self, message: str, status_code: int):
        super().__init__("API Error", message, status_code=status_code)


class NetworkError(MemosCloudError):
    def __init__(self, message: str):
        super().__init__("Network Error", message)


class FilePayloadError(MemosCloudError):
    def __init__(self, error: str, message: str):
        super().__init__(error, message)


def print_error(error: MemosCloudError) -> None:
    print(json.dumps(error.to_payload()), file=sys.stderr)
