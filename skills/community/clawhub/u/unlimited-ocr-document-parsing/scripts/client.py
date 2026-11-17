"""Provider clients for the Unlimited-OCR Agent Skill."""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator, Optional
from urllib.parse import urlparse

import httpx

BAIDU_OAUTH_URL = "https://aip.baidubce.com/oauth/2.0/token"
BAIDU_SUBMIT_URL = "https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task"
BAIDU_QUERY_URL = "https://aip.baidubce.com/rest/2.0/brain/online/v2/unlimited-ocr-parser/task/query"
LOCAL_DEFAULT_BASE_URL = "http://127.0.0.1:10000"
DEFAULT_MODEL = "Unlimited-OCR"
MAX_SOURCE_BYTES = 100 * 1024 * 1024
MAX_ARTIFACT_BYTES = 64 * 1024 * 1024
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


class SkillError(RuntimeError):
    """Expected, sanitized failure returned to an Agent caller."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def positive_float(raw: str | float, name: str, maximum: float) -> float:
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise SkillError("CONFIG_ERROR", f"{name} must be a number") from exc
    if not 0 < value <= maximum:
        raise SkillError("CONFIG_ERROR", f"{name} must be greater than 0 and at most {maximum:g}")
    return value


def positive_int(raw: str | int, name: str, maximum: int) -> int:
    try:
        value = int(raw)
    except (TypeError, ValueError) as exc:
        raise SkillError("CONFIG_ERROR", f"{name} must be an integer") from exc
    if not 0 < value <= maximum:
        raise SkillError("CONFIG_ERROR", f"{name} must be between 1 and {maximum}")
    return value


def safe_endpoint(raw: str, name: str, *, allow_loopback_http: bool = True) -> str:
    try:
        parsed = urlparse(raw)
    except ValueError as exc:
        raise SkillError("CONFIG_ERROR", f"{name} must be a valid URL") from exc
    if parsed.username or parsed.password:
        raise SkillError("CONFIG_ERROR", f"{name} must not contain embedded credentials")
    is_loopback_http = allow_loopback_http and parsed.scheme == "http" and parsed.hostname in LOOPBACK_HOSTS
    if parsed.scheme != "https" and not is_loopback_http:
        raise SkillError("CONFIG_ERROR", f"{name} must use HTTPS (loopback HTTP is allowed)")
    if not parsed.hostname:
        raise SkillError("CONFIG_ERROR", f"{name} must include a hostname")
    return raw.rstrip("/")


def public_https_url(raw: str, name: str = "file_url") -> str:
    value = safe_endpoint(raw, name, allow_loopback_http=False)
    return value


def source_file(path_value: str) -> Path:
    path = Path(path_value).expanduser().resolve()
    if not path.exists():
        raise SkillError("INPUT_ERROR", f"file not found: {path_value}")
    if not path.is_file():
        raise SkillError("INPUT_ERROR", "file_path must identify a regular file")
    size = path.stat().st_size
    if size == 0:
        raise SkillError("INPUT_ERROR", "input file is empty")
    if size > MAX_SOURCE_BYTES:
        raise SkillError("INPUT_ERROR", "input file exceeds the 100 MiB safety limit")
    return path


def envelope(provider: str, text: str, result: Any, artifacts: dict[str, str]) -> dict[str, Any]:
    return {"ok": True, "provider": provider, "text": text, "result": result, "artifacts": artifacts, "error": None}


def error_envelope(provider: str, error: Exception) -> dict[str, Any]:
    if isinstance(error, SkillError):
        code, message = error.code, str(error)
    elif isinstance(error, httpx.TimeoutException):
        code, message = "TIMEOUT", "Unlimited-OCR request timed out"
    elif isinstance(error, httpx.HTTPError):
        code, message = "HTTP_ERROR", "Unlimited-OCR HTTP request failed"
    else:
        code, message = "UNEXPECTED_ERROR", str(error)
    return {"ok": False, "provider": provider, "text": "", "result": None, "artifacts": {}, "error": {"code": code, "message": message}}


def _json_response(response: httpx.Response, operation: str) -> dict[str, Any]:
    if response.status_code < 200 or response.status_code >= 300:
        raise SkillError("HTTP_ERROR", f"{operation} failed with HTTP {response.status_code}")
    try:
        value = response.json()
    except (ValueError, json.JSONDecodeError) as exc:
        raise SkillError("RESPONSE_ERROR", f"{operation} returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise SkillError("RESPONSE_ERROR", f"{operation} returned an unexpected response shape")
    return value


def _api_success(value: dict[str, Any], operation: str) -> dict[str, Any]:
    code = value.get("error_code", 0)
    if code not in (0, "0", None):
        detail = str(value.get("error_msg") or "unknown API error")[:500]
        raise SkillError("API_ERROR", f"{operation} failed ({code}): {detail}")
    return value


@dataclass(frozen=True)
class BaiduSettings:
    api_key: str
    secret_key: str
    access_token: str
    oauth_url: str
    submit_url: str
    query_url: str
    timeout_seconds: float
    poll_interval_seconds: float

    @classmethod
    def from_env(cls, *, timeout_seconds: float, poll_interval_seconds: float) -> "BaiduSettings":
        access_token = env("UNLIMITED_OCR_ACCESS_TOKEN")
        api_key = env("UNLIMITED_OCR_API_KEY")
        secret_key = env("UNLIMITED_OCR_SECRET_KEY")
        if not access_token and (not api_key or not secret_key):
            raise SkillError("CONFIG_ERROR", "configure UNLIMITED_OCR_API_KEY and UNLIMITED_OCR_SECRET_KEY, or UNLIMITED_OCR_ACCESS_TOKEN")
        return cls(
            api_key=api_key,
            secret_key=secret_key,
            access_token=access_token,
            oauth_url=safe_endpoint(env("UNLIMITED_OCR_OAUTH_URL", BAIDU_OAUTH_URL), "UNLIMITED_OCR_OAUTH_URL"),
            submit_url=safe_endpoint(env("UNLIMITED_OCR_SUBMIT_URL", BAIDU_SUBMIT_URL), "UNLIMITED_OCR_SUBMIT_URL"),
            query_url=safe_endpoint(env("UNLIMITED_OCR_QUERY_URL", BAIDU_QUERY_URL), "UNLIMITED_OCR_QUERY_URL"),
            timeout_seconds=positive_float(timeout_seconds, "timeout_seconds", 7200),
            poll_interval_seconds=positive_float(poll_interval_seconds, "poll_interval_seconds", 60),
        )


def _access_token(client: httpx.Client, settings: BaiduSettings) -> str:
    if settings.access_token:
        return settings.access_token
    response = client.post(settings.oauth_url, params={
        "grant_type": "client_credentials",
        "client_id": settings.api_key,
        "client_secret": settings.secret_key,
    })
    value = _json_response(response, "OAuth token request")
    token = value.get("access_token")
    if not isinstance(token, str) or not token:
        detail = str(value.get("error_description") or value.get("error") or "access_token missing")[:500]
        raise SkillError("AUTH_ERROR", f"OAuth token request failed: {detail}")
    return token


def _download(client: httpx.Client, raw_url: str, label: str) -> bytes:
    url = safe_endpoint(raw_url, label)
    with client.stream("GET", url) as response:
        if response.status_code < 200 or response.status_code >= 300:
            raise SkillError("HTTP_ERROR", f"{label} download failed with HTTP {response.status_code}")
        chunks: list[bytes] = []
        size = 0
        for chunk in response.iter_bytes():
            size += len(chunk)
            if size > MAX_ARTIFACT_BYTES:
                raise SkillError("RESPONSE_ERROR", f"{label} exceeds the 64 MiB download limit")
            chunks.append(chunk)
    return b"".join(chunks)


def parse_baidu(
    *,
    file_path: Optional[str],
    file_url: Optional[str],
    timeout_seconds: float = 1200,
    poll_interval_seconds: float = 5,
    transport: Optional[httpx.BaseTransport] = None,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    settings = BaiduSettings.from_env(timeout_seconds=timeout_seconds, poll_interval_seconds=poll_interval_seconds)
    has_path, has_url = bool(file_path and file_path.strip()), bool(file_url and file_url.strip())
    if has_path == has_url:
        raise SkillError("INPUT_ERROR", "provide exactly one of file_path or file_url")

    data: dict[str, str]
    if has_path:
        path = source_file(file_path or "")
        data = {"file_data": base64.b64encode(path.read_bytes()).decode("ascii"), "file_name": path.name}
    else:
        url = public_https_url(file_url or "")
        name = Path(urlparse(url).path).name or "document.pdf"
        data = {"file_url": url, "file_name": name}

    client_timeout = httpx.Timeout(settings.timeout_seconds, connect=min(30.0, settings.timeout_seconds))
    with httpx.Client(timeout=client_timeout, transport=transport, trust_env=False, follow_redirects=False) as client:
        token = _access_token(client, settings)
        submit = _api_success(_json_response(client.post(
            settings.submit_url,
            params={"access_token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        ), "task submission"), "task submission")
        submit_result = submit.get("result")
        task_id = submit_result.get("task_id") if isinstance(submit_result, dict) else None
        if not isinstance(task_id, str) or not task_id:
            raise SkillError("RESPONSE_ERROR", "task submission response did not contain task_id")

        deadline = time.monotonic() + settings.timeout_seconds
        final_response: dict[str, Any]
        while True:
            query = _api_success(_json_response(client.post(
                settings.query_url,
                params={"access_token": token},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={"task_id": task_id},
            ), "task query"), "task query")
            query_result = query.get("result")
            if not isinstance(query_result, dict):
                raise SkillError("RESPONSE_ERROR", "task query response did not contain a result object")
            status = str(query_result.get("status") or "").lower()
            if status == "success":
                final_response = query
                break
            if status == "failed":
                detail = str(query_result.get("task_error") or "Unlimited-OCR task failed")[:500]
                raise SkillError("TASK_FAILED", detail)
            if status not in {"pending", "running"}:
                raise SkillError("RESPONSE_ERROR", f"unknown task status: {status or 'missing'}")
            if time.monotonic() + settings.poll_interval_seconds > deadline:
                raise SkillError("TIMEOUT", f"Unlimited-OCR task did not finish within {settings.timeout_seconds:g} seconds")
            sleep(settings.poll_interval_seconds)

        result = final_response["result"]
        markdown_url = result.get("markdown_url") if isinstance(result, dict) else None
        parse_result_url = result.get("parse_result_url") if isinstance(result, dict) else None
        artifacts: dict[str, str] = {}
        text = ""
        parsed_result: Any = None
        if isinstance(markdown_url, str) and markdown_url:
            artifacts["markdown_url"] = markdown_url
            text = _download(client, markdown_url, "markdown_url").decode("utf-8", errors="replace")
        if isinstance(parse_result_url, str) and parse_result_url:
            artifacts["parse_result_url"] = parse_result_url
            raw = _download(client, parse_result_url, "parse_result_url").decode("utf-8", errors="replace")
            try:
                parsed_result = json.loads(raw)
            except json.JSONDecodeError:
                parsed_result = raw
        return envelope("baidu", text, {
            "task_id": task_id,
            "status": "success",
            "response": final_response,
            "parse_result": parsed_result,
        }, artifacts)


@dataclass(frozen=True)
class LocalSettings:
    endpoint: str
    backend: str
    model: str
    api_key: str
    timeout_seconds: float
    dpi: int
    max_pages: int

    @classmethod
    def from_env(cls, *, timeout_seconds: float, backend: Optional[str], model: Optional[str]) -> "LocalSettings":
        base = safe_endpoint(env("UNLIMITED_OCR_LOCAL_BASE_URL", LOCAL_DEFAULT_BASE_URL), "UNLIMITED_OCR_LOCAL_BASE_URL")
        endpoint = base if base.endswith("/v1/chat/completions") else f"{base}/v1/chat/completions"
        selected_backend = (backend or env("UNLIMITED_OCR_LOCAL_BACKEND", "sglang")).lower()
        if selected_backend not in {"sglang", "openai"}:
            raise SkillError("CONFIG_ERROR", "local backend must be sglang or openai")
        return cls(
            endpoint=endpoint,
            backend=selected_backend,
            model=model or env("UNLIMITED_OCR_MODEL", DEFAULT_MODEL),
            api_key=env("UNLIMITED_OCR_LOCAL_API_KEY"),
            timeout_seconds=positive_float(timeout_seconds, "timeout_seconds", 7200),
            dpi=positive_int(env("UNLIMITED_OCR_PDF_DPI", "200"), "UNLIMITED_OCR_PDF_DPI", 600),
            max_pages=positive_int(env("UNLIMITED_OCR_LOCAL_MAX_PAGES", "64"), "UNLIMITED_OCR_LOCAL_MAX_PAGES", 500),
        )


def _image_part(path: Path) -> dict[str, Any]:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}}


@contextmanager
def _local_images(path: Path, settings: LocalSettings) -> Iterator[list[Path]]:
    suffix = path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        yield [path]
        return
    if suffix != ".pdf":
        raise SkillError("INPUT_ERROR", "local provider supports image files and PDFs only")
    try:
        import fitz
    except ImportError as exc:
        raise SkillError("CONFIG_ERROR", "PyMuPDF is required for local PDF parsing") from exc
    with tempfile.TemporaryDirectory(prefix="unlimited-ocr-pdf-") as directory:
        document = fitz.open(path)
        try:
            if document.page_count > settings.max_pages:
                raise SkillError("INPUT_ERROR", f"PDF has {document.page_count} pages; local limit is {settings.max_pages}")
            matrix = fitz.Matrix(settings.dpi / 72, settings.dpi / 72)
            images: list[Path] = []
            for index, page in enumerate(document):
                output = Path(directory) / f"page-{index + 1:04d}.png"
                page.get_pixmap(matrix=matrix, alpha=False).save(output)
                images.append(output)
        finally:
            document.close()
        yield images


def _stream_text(response: httpx.Response) -> str:
    if response.status_code < 200 or response.status_code >= 300:
        raise SkillError("HTTP_ERROR", f"local inference failed with HTTP {response.status_code}")
    content_type = response.headers.get("content-type", "").lower()
    if "text/event-stream" not in content_type:
        try:
            value = json.loads(response.read())
            content = value["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise SkillError("RESPONSE_ERROR", "local server returned an unexpected response") from exc
        if not isinstance(content, str):
            raise SkillError("RESPONSE_ERROR", "local server response content was not text")
        return content
    chunks: list[str] = []
    for line in response.iter_lines():
        if not line.startswith("data:"):
            continue
        data = line[len("data:"):].strip()
        if data == "[DONE]":
            break
        try:
            event = json.loads(data)
            delta = event["choices"][0].get("delta", {}).get("content", "")
        except (ValueError, KeyError, IndexError, TypeError):
            continue
        if isinstance(delta, str) and delta:
            chunks.append(delta)
    return "".join(chunks)


def parse_local(
    *,
    file_path: Optional[str],
    file_url: Optional[str],
    timeout_seconds: float = 1200,
    backend: Optional[str] = None,
    model: Optional[str] = None,
    prompt: Optional[str] = None,
    image_mode: str = "auto",
    transport: Optional[httpx.BaseTransport] = None,
) -> dict[str, Any]:
    if file_url and file_url.strip():
        raise SkillError("INPUT_ERROR", "local provider requires file_path; download remote input into the workspace first")
    if not file_path or not file_path.strip():
        raise SkillError("INPUT_ERROR", "file_path is required for the local provider")
    settings = LocalSettings.from_env(timeout_seconds=timeout_seconds, backend=backend, model=model)
    path = source_file(file_path)
    headers = {"Content-Type": "application/json"}
    if settings.api_key:
        headers["Authorization"] = f"Bearer {settings.api_key}"
    timeout = httpx.Timeout(settings.timeout_seconds, connect=min(30.0, settings.timeout_seconds))
    with _local_images(path, settings) as images:
        multi_page = len(images) > 1
        selected_mode = "base" if multi_page else ("gundam" if image_mode == "auto" else image_mode)
        if selected_mode not in {"base", "gundam"}:
            raise SkillError("INPUT_ERROR", "image_mode must be auto, base, or gundam")
        default_prompt = "Multi page parsing." if multi_page else "document parsing."
        content = [{"type": "text", "text": prompt or default_prompt}, *[_image_part(image) for image in images]]
        payload: dict[str, Any] = {
            "model": settings.model,
            "messages": [{"role": "user", "content": content}],
            "temperature": 0,
            "stream": True,
        }
        if settings.backend == "sglang":
            payload.update({"skip_special_tokens": False, "images_config": {"image_mode": selected_mode}})
        with httpx.Client(timeout=timeout, transport=transport, trust_env=False, follow_redirects=False) as client:
            with client.stream("POST", settings.endpoint, headers=headers, json=payload) as response:
                text = _stream_text(response)
        return envelope("local", text, {
            "backend": settings.backend,
            "model": settings.model,
            "image_count": len(images),
            "image_mode": selected_mode,
        }, {})


def parse_document(
    *,
    provider: str,
    file_path: Optional[str],
    file_url: Optional[str],
    timeout_seconds: float,
    poll_interval_seconds: float,
    backend: Optional[str] = None,
    model: Optional[str] = None,
    prompt: Optional[str] = None,
    image_mode: str = "auto",
) -> dict[str, Any]:
    selected = provider.strip().lower()
    try:
        if selected == "baidu":
            return parse_baidu(file_path=file_path, file_url=file_url, timeout_seconds=timeout_seconds, poll_interval_seconds=poll_interval_seconds)
        if selected == "local":
            return parse_local(file_path=file_path, file_url=file_url, timeout_seconds=timeout_seconds, backend=backend, model=model, prompt=prompt, image_mode=image_mode)
        raise SkillError("CONFIG_ERROR", "provider must be baidu or local")
    except Exception as exc:
        return error_envelope(selected or "unknown", exc)

