#!/usr/bin/env python3

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

from common import trim_string


RETRYABLE_STATUSES = {408, 409, 425, 429, 500, 502, 503, 504}
VALID_SAMPLE_RATES = {8000, 16000, 24000, 48000}
VALID_RESPONSE_FORMATS = {"wav", "mp3", "flac", "opus", "pcm"}


class StepTTSError(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None, body: str = "") -> None:
        super().__init__(message)
        self.status = status
        self.body = body


class StepTTSClient:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = "https://api.stepfun.com/v1",
        request_interval_ms: int = 6500,
        max_retries: int = 3,
        timeout_sec: int = 60,
    ) -> None:
        if not trim_string(api_key):
            raise RuntimeError("缺少 Step API key")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.request_interval_ms = max(0, int(request_interval_ms))
        self.max_retries = max(1, int(max_retries))
        self.timeout_sec = max(1, int(timeout_sec))
        self.last_request_at = 0.0

    def normalize_model_name(self, model: str) -> str:
        return trim_string(model) or "stepaudio-2.5-tts"

    def sanitize_extra_payload(self, extra_payload: dict[str, Any] | None) -> dict[str, Any]:
        if not isinstance(extra_payload, dict):
            return {}

        payload = dict(extra_payload)
        if "voice_label" in payload:
            raise RuntimeError("stepaudio-2.5-tts 当前不支持 voice_label，请改用 instruction / inline context")
        if "instruction" in payload:
            raise RuntimeError("请不要在 extra_payload 里传 instruction；脚本会使用独立的 instruction 字段")
        return payload

    def enforce_request_interval(self) -> None:
        if self.request_interval_ms <= 0:
            return
        now = time.time()
        elapsed_ms = (now - self.last_request_at) * 1000
        wait_ms = self.request_interval_ms - elapsed_ms
        if wait_ms > 0:
            time.sleep(wait_ms / 1000)
        self.last_request_at = time.time()

    def validate_request(
        self,
        *,
        model: str,
        input_text: str,
        voice_id: str,
        instruction: str = "",
        sample_rate: int,
        response_format: str,
    ) -> None:
        if not trim_string(model):
            raise RuntimeError("TTS model 不能为空")
        if not trim_string(input_text):
            raise RuntimeError("TTS input 不能为空")
        if len(input_text) > 1000:
            raise RuntimeError(f"TTS input 过长（{len(input_text)} 字符），Step 当前上限为 1000")
        if not trim_string(voice_id):
            raise RuntimeError("TTS voice_id 不能为空")
        if trim_string(instruction) and len(trim_string(instruction)) > 200:
            raise RuntimeError(f"TTS instruction 过长（{len(trim_string(instruction))} 字符），建议控制在 200 以内")
        if int(sample_rate) not in VALID_SAMPLE_RATES:
            raise RuntimeError(f"TTS sample_rate 不支持: {sample_rate}；当前允许 {sorted(VALID_SAMPLE_RATES)}")
        if trim_string(response_format).lower() not in VALID_RESPONSE_FORMATS:
            raise RuntimeError(f"TTS response_format 不支持: {response_format}；当前允许 {sorted(VALID_RESPONSE_FORMATS)}")

    def synthesize(
        self,
        *,
        model: str,
        input_text: str,
        voice_id: str,
        instruction: str = "",
        sample_rate: int,
        response_format: str,
        extra_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        resolved_model = self.normalize_model_name(model)
        self.validate_request(
            model=resolved_model,
            input_text=input_text,
            voice_id=voice_id,
            instruction=instruction,
            sample_rate=sample_rate,
            response_format=response_format,
        )

        payload: dict[str, Any] = {
            "model": resolved_model,
            "input": input_text,
            "voice": voice_id,
            "sample_rate": int(sample_rate),
            "response_format": response_format.lower(),
        }
        if trim_string(instruction):
            payload["instruction"] = trim_string(instruction)
        sanitized_extra_payload = self.sanitize_extra_payload(extra_payload)
        if sanitized_extra_payload:
            payload.update(sanitized_extra_payload)

        last_error: StepTTSError | None = None
        for attempt in range(1, self.max_retries + 1):
            self.enforce_request_interval()
            try:
                request = urllib.request.Request(
                    self.base_url + "/audio/speech",
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    method="POST",
                )
                with urllib.request.urlopen(request, timeout=self.timeout_sec) as response:
                    audio_bytes = response.read()
                    return {
                        "audio_bytes": audio_bytes,
                        "resolved_model": resolved_model,
                        "request_payload": payload,
                        "content_type": response.headers.get("Content-Type") or "",
                    }
            except urllib.error.HTTPError as error:
                body = error.read().decode("utf-8", errors="replace")
                last_error = StepTTSError(
                    f"Step TTS 请求失败: HTTP {error.code}",
                    status=error.code,
                    body=body,
                )
                if error.code in RETRYABLE_STATUSES and attempt < self.max_retries:
                    time.sleep(min(2 ** (attempt - 1), 8))
                    continue
                raise last_error from error
            except urllib.error.URLError as error:
                last_error = StepTTSError(f"Step TTS 网络错误: {error.reason}")
                if attempt < self.max_retries:
                    time.sleep(min(2 ** (attempt - 1), 8))
                    continue
                raise last_error from error

        assert last_error is not None
        raise last_error
