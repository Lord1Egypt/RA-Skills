import json
from typing import Any, Iterable
from urllib.parse import parse_qs, urlparse

import httpx

from rurussian_mcp.config import (
    API_BASE_URL,
    BUY_SESSION_ENDPOINTS,
    CONFIRM_PURCHASE_ENDPOINTS,
    DEFAULT_TIMEOUT,
    PAYMENT_SUCCESS_STATUSES,
)
from rurussian_mcp.services.auth_service import auth_service


class BackendClient:
    def __init__(self, api_base_url: str = API_BASE_URL, timeout: float = DEFAULT_TIMEOUT) -> None:
        self.api_base_url = api_base_url.rstrip("/")
        self.timeout = timeout

    async def get_word_data(self, word: str) -> dict[str, Any]:
        return await self._request_json("GET", f"/word/{word}", include_auth=True)

    async def get_saved_sentences(self, email: str) -> dict[str, Any]:
        return await self._request_json(
            "GET",
            "/rusvibe/sentences",
            params={"email": email},
            include_auth=True,
        )

    async def generate_sentences(
        self,
        word: str,
        forms: list[dict[str, Any]],
        *,
        cache_only: bool = False,
        wait_seconds: int = 0,
        poll_interval_ms: int = 1000,
    ) -> dict[str, Any]:
        return await self._request_json(
            "POST",
            "/generate_sentences",
            json_payload={
                "verb": word,
                "forms": forms,
                "cache_only": cache_only,
                "wait_seconds": wait_seconds,
                "poll_interval_ms": poll_interval_ms,
            },
            include_auth=True,
        )

    async def generate_zakuska(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request_json(
            "POST",
            "/zakuska/generate",
            json_payload=payload,
            include_auth=True,
            timeout=max(self.timeout, 60.0),
        )

    async def analyze_sentence(self, sentence: str, email: str = "") -> dict[str, Any]:
        payload: dict[str, str] = {"sentence": sentence}
        if email:
            payload["email"] = email

        async with httpx.AsyncClient(timeout=max(self.timeout, 60.0)) as client:
            response = await client.post(
                f"{self.api_base_url}/analyze_sentence",
                json=payload,
                headers=auth_service.get_headers(include_auth=True),
            )
            response.raise_for_status()
            lines = response.text.strip().splitlines()
            chunks: list[dict[str, Any]] = []
            text_chunks: list[str] = []
            for line in lines:
                if not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str == "[DONE]":
                    continue
                try:
                    chunk = json.loads(data_str)
                except json.JSONDecodeError:
                    chunk = {"chunk": data_str}
                chunks.append(chunk)
                chunk_text = chunk.get("chunk")
                if isinstance(chunk_text, str) and chunk_text:
                    text_chunks.append(chunk_text)
            return {
                "analysis_chunks": chunks,
                "analysis_text": "".join(text_chunks).strip(),
            }

    async def translate_text(
        self,
        text: str,
        source_lang: str = "Russian",
        target_lang: str = "English",
    ) -> dict[str, Any]:
        return await self._request_json(
            "POST",
            "/translate",
            json_payload={
                "text": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
            },
            include_auth=True,
        )

    async def create_purchase_session(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = await self._try_endpoints("POST", BUY_SESSION_ENDPOINTS, payload)
        checkout_url = self._extract_first_present(
            response,
            ("url", "checkout_url", "checkoutUrl", "session_url"),
        )
        session_id = self._extract_first_present(response, ("session_id", "sessionId", "id"))
        if not session_id:
            session_id = self._extract_session_id_from_url(checkout_url)
        return {
            "checkout_url": checkout_url,
            "session_id": session_id,
            "raw_response": response,
        }

    async def confirm_purchase(self, session_id: str) -> dict[str, Any]:
        payload = {"session_id": session_id, "include_api_key": True}
        try:
            response = await self._try_endpoints("POST", CONFIRM_PURCHASE_ENDPOINTS, payload)
        except RuntimeError:
            response = await self._try_endpoints("GET", CONFIRM_PURCHASE_ENDPOINTS, payload)

        status_value = self._extract_first_present(response, ("status", "payment_status", "result"))
        api_key = self._extract_first_present(response, ("api_key", "apiKey", "key", "token"))
        return {
            "confirmed": bool(api_key) or self._is_payment_confirmed(status_value),
            "payment_status": status_value or "unknown",
            "api_key": api_key,
            "raw_response": response,
        }

    async def _request_json(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_payload: dict[str, Any] | None = None,
        include_auth: bool,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        url = self._normalize_endpoint(path)
        async with httpx.AsyncClient(timeout=timeout or self.timeout) as client:
            if method == "GET":
                response = await client.get(
                    url,
                    params=params,
                    headers=auth_service.get_headers(include_auth=include_auth),
                )
            else:
                response = await client.post(
                    url,
                    json=json_payload or {},
                    headers=auth_service.get_headers(include_auth=include_auth),
                )
            response.raise_for_status()
            return self._safe_json(response)

    async def _try_endpoints(
        self,
        method: str,
        endpoint_candidates: Iterable[str],
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        last_error = "No compatible backend endpoint responded successfully."
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for endpoint in endpoint_candidates:
                url = self._normalize_endpoint(endpoint)
                try:
                    if method == "GET":
                        response = await client.get(url, params=payload, headers=auth_service.get_headers(False))
                    else:
                        response = await client.post(url, json=payload, headers=auth_service.get_headers(False))
                    if response.status_code < 400:
                        return self._safe_json(response)
                    error_payload = self._safe_json(response)
                    error_text = self._extract_first_present(error_payload, ("error", "detail", "message"))
                    if error_text:
                        last_error = error_text
                except Exception as exc:  # pragma: no cover - network fallback
                    last_error = str(exc)
                    continue
        raise RuntimeError(last_error)

    def _normalize_endpoint(self, endpoint: str) -> str:
        endpoint = endpoint.strip()
        if endpoint.startswith("https://") or endpoint.startswith("http://"):
            return endpoint
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        return f"{self.api_base_url}{endpoint}"

    @staticmethod
    def _safe_json(response: httpx.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except Exception:
            return {"text": response.text}
        if isinstance(payload, dict):
            return payload
        return {"data": payload}

    @staticmethod
    def _extract_first_present(data: dict[str, Any], keys: Iterable[str]) -> str:
        for key in keys:
            value = data.get(key)
            if isinstance(value, str) and value:
                return value
        return ""

    @staticmethod
    def _extract_session_id_from_url(url: str) -> str:
        if not url:
            return ""
        parsed = urlparse(url)
        values = parse_qs(parsed.query).get("session_id", [])
        return values[0] if values else ""

    @staticmethod
    def _is_payment_confirmed(status_value: str) -> bool:
        return (status_value or "").strip().lower() in PAYMENT_SUCCESS_STATUSES


backend_client = BackendClient()
