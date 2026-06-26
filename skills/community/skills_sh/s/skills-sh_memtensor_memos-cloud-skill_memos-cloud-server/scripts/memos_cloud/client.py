from __future__ import annotations

from typing import Any, Mapping, Optional

import requests

from .config import MemosConfig
from .errors import ApiError, NetworkError


DEFAULT_TIMEOUT = 30
SOURCE_VALUE = "MEMOS_CLOUD_SKILL"


class MemosClient:
    def __init__(
        self,
        config: MemosConfig,
        session: Optional[requests.Session] = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        self.config = config
        self.session = session or requests.Session()
        self.timeout = timeout

    def post(self, endpoint: str, payload: Mapping[str, Any]) -> Any:
        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"
        body = {**payload, "source": SOURCE_VALUE}
        try:
            response = self.session.post(
                url,
                headers=self.config.headers,
                json=body,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as exc:
            response = exc.response
            status_code = response.status_code if response is not None else 0
            raise ApiError(_format_http_error(exc), status_code=status_code) from exc
        except requests.exceptions.RequestException as exc:
            raise NetworkError(str(exc)) from exc


def _format_http_error(exc: requests.exceptions.HTTPError) -> str:
    response = exc.response
    if response is None:
        return "HTTP 0"

    message = f"HTTP {response.status_code}"
    try:
        response_json = response.json()
        detail = response_json.get("message", response.text)
    except ValueError:
        detail = response.text

    return f"{message} - {detail}"
