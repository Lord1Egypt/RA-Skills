#!/usr/bin/env python3
"""SpicyAPI command line for the nsfw-ai skill. Standard library only (Python 3.9+).

Commands
  models    List models from the public catalog (no API key needed).
  schema    Show a model's live input schema and prices (needs SPICY_API_KEY).
  quote     Price an exact request without running it.
  generate  Quote, confirm, create a task, wait for it and download the result.
  status    Show a task and optionally download its outputs.
  upload    Upload a local image/video/audio file and print its spicy:// URI.
  balance   Show the account balance.
  chat      Call a text model through the OpenAI-compatible endpoint.

Every generation is billable. `generate` prints the quote and stops unless you pass
--yes (or --max-cost with a ceiling the quote fits under).
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

API_BASE = os.environ.get("SPICY_API_BASE_URL", "https://api.spicyapi.ai/api/v1").rstrip("/")
SERVICE_BASE = os.environ.get("SPICY_SERVICE_BASE_URL", "https://api.spicyapi.ai").rstrip("/")
CATALOG_URL = f"{SERVICE_BASE}/console/v1/catalog/models"
USER_AGENT = "nsfw-ai-skill/1.0 (+https://github.com/Spicy-API/nsfw-ai-skill)"
TERMINAL_STATES = {"succeeded", "failed", "canceled", "expired"}
MAX_UPLOAD_BYTES = {"image": 10 * 1024 * 1024, "video": 90 * 1024 * 1024, "audio": 90 * 1024 * 1024}


class SpicyError(RuntimeError):
    """An API or usage error with an optional business code and request id."""

    def __init__(self, message: str, code: Any = None, request_id: str | None = None):
        super().__init__(message)
        self.code = code
        self.request_id = request_id


# --------------------------------------------------------------------------- HTTP


def api_key() -> str:
    key = os.environ.get("SPICY_API_KEY", "").strip()
    if not key:
        raise SpicyError(
            "SPICY_API_KEY is not set. Create a key at https://spicyapi.ai/console and export it, "
            "e.g. `export SPICY_API_KEY=sk-spicy-...`."
        )
    return key


def http_json(method: str, url: str, body: Any = None, headers: dict[str, str] | None = None,
              auth: bool = True, timeout: int = 60) -> Any:
    hdrs = {"Accept": "application/json", "User-Agent": USER_AGENT, **(headers or {})}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        hdrs["Content-Type"] = "application/json"
    if auth:
        hdrs["Authorization"] = f"Bearer {api_key()}"
    req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
    try:
        payload = _send_with_retry(req, timeout)
    except urllib.error.HTTPError as err:
        raw = err.read().decode("utf-8", "replace")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            raise SpicyError(f"HTTP {err.code} from {url}: {raw[:300]}", code=err.code) from None
        retry = err.headers.get("Retry-After")
        msg = payload.get("msg") or payload.get("message") or raw[:300]
        if retry:
            msg += f" (retry after {retry}s)"
        raise SpicyError(msg, code=payload.get("code", err.code), request_id=payload.get("request_id")) from None
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as err:
        raise SpicyError(f"Network error calling {url}: {getattr(err, 'reason', err)}") from None
    if isinstance(payload, dict) and "code" in payload and payload["code"] not in (0, 200):
        raise SpicyError(payload.get("msg", "request failed"), code=payload["code"],
                         request_id=payload.get("request_id"))
    return payload


def _send_with_retry(req: urllib.request.Request, timeout: int, attempts: int = 3) -> Any:
    """Retry transport failures (TLS resets, timeouts). Task creation carries an
    Idempotency-Key, so repeating it can never create a second task or charge."""
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError:
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            if attempt == attempts - 1:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise AssertionError("unreachable")


def data_of(payload: Any) -> Any:
    return payload.get("data", payload) if isinstance(payload, dict) else payload


# --------------------------------------------------------------------------- helpers


def parse_value(raw: str) -> Any:
    """Turn a --set value into JSON types: 5 -> int, 0.8 -> float, true -> bool, [..] -> list."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def build_input(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if getattr(args, "input_file", None):
        payload.update(json.loads(Path(args.input_file).read_text(encoding="utf-8")))
    if getattr(args, "input", None):
        payload.update(json.loads(args.input))
    for item in getattr(args, "set", None) or []:
        if "=" not in item:
            raise SpicyError(f"--set expects key=value, got {item!r}")
        key, value = item.split("=", 1)
        payload[key.strip()] = parse_value(value)
    if getattr(args, "prompt", None):
        payload["prompt"] = args.prompt
    for field in ("image", "last_image", "video", "audio"):
        value = getattr(args, field, None)
        if value:
            payload[f"{field}_url"] = resolve_media(value)
    if getattr(args, "images", None):
        payload["image_urls"] = [resolve_media(v) for v in args.images]
    return payload


def resolve_media(value: str) -> str:
    """Public URLs and spicy:// URIs pass through; local files are uploaded first."""
    if value.startswith(("http://", "https://", "spicy://")):
        return value
    path = Path(value).expanduser()
    if not path.is_file():
        raise SpicyError(f"Not a URL and not a local file: {value}")
    return upload_file(path)["uri"]


def upload_file(path: Path) -> dict[str, Any]:
    content_type = mimetypes.guess_type(path.name)[0] or ""
    if content_type == "audio/x-wav":
        content_type = "audio/wav"
    kind = content_type.split("/")[0]
    if kind not in MAX_UPLOAD_BYTES:
        raise SpicyError(f"Unsupported file type {content_type or 'unknown'} for {path.name}. "
                         "Use JPEG/PNG/WebP/GIF, MP4/WebM or MP3/WAV.")
    size = path.stat().st_size
    if size > MAX_UPLOAD_BYTES[kind]:
        raise SpicyError(f"{path.name} is {size / 1048576:.1f} MiB; the {kind} limit is "
                         f"{MAX_UPLOAD_BYTES[kind] // 1048576} MiB.")
    ticket = data_of(http_json("POST", f"{API_BASE}/common/upload-url",
                               {"contentType": content_type, "bytes": size}))
    put = urllib.request.Request(ticket["uploadUrl"], data=path.read_bytes(), method=ticket.get("method", "PUT"),
                                 headers={**ticket.get("headers", {}), "Content-Length": str(size)})
    try:
        with urllib.request.urlopen(put, timeout=300):
            pass
    except urllib.error.HTTPError as err:
        raise SpicyError(f"Upload PUT failed with HTTP {err.code}: {err.read()[:200]!r}") from None
    committed = data_of(http_json("POST", f"{API_BASE}/files/{urllib.parse.quote(ticket['fileId'])}/commit", {}))
    print(f"uploaded {path.name} -> {committed['uri']}", file=sys.stderr)
    return committed


def quote(model: str, payload: dict[str, Any]) -> dict[str, Any]:
    return data_of(http_json("POST", f"{API_BASE}/jobs/quote", {"model": model, "input": payload}))


def get_task(task_id: str) -> dict[str, Any]:
    url = f"{API_BASE}/jobs/recordInfo?taskId={urllib.parse.quote(task_id)}"
    return data_of(http_json("GET", url))


def wait_for(task_id: str, timeout: int, interval: float = 3.0) -> dict[str, Any]:
    deadline = time.time() + timeout
    task = get_task(task_id)
    while task.get("state") not in TERMINAL_STATES or any(a.get("pending") for a in assets_of(task)):
        if time.time() > deadline:
            print(f"still {task.get('state')} after {timeout}s; check later with: status {task_id}", file=sys.stderr)
            return task
        time.sleep(interval)
        interval = min(interval * 1.5, 15.0)
        task = get_task(task_id)
    return task


def assets_of(task: dict[str, Any]) -> list[dict[str, Any]]:
    return (task.get("output") or {}).get("assets") or []


def download(task: dict[str, Any], out_dir: str) -> list[str]:
    target = Path(out_dir).expanduser()
    target.mkdir(parents=True, exist_ok=True)
    saved = []
    for i, asset in enumerate(assets_of(task)):
        url = asset.get("url")
        if not url:
            continue
        ext = mimetypes.guess_extension(asset.get("mime") or "") or Path(urllib.parse.urlparse(url).path).suffix or ".bin"
        path = target / f"{task['taskId']}_{i}{ext}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=300) as resp, open(path, "wb") as fh:
            fh.write(resp.read())
        saved.append(str(path))
    return saved


def summarize(task: dict[str, Any]) -> dict[str, Any]:
    out = {k: task.get(k) for k in ("taskId", "model", "state", "cost", "settled", "createdAt")}
    if task.get("errorCode") or task.get("errorMessage"):
        out["error"] = {"code": task.get("errorCode"), "message": task.get("errorMessage")}
    out["assets"] = [{k: a.get(k) for k in ("url", "mime", "width", "height", "durationSeconds") if a.get(k)}
                     for a in assets_of(task)]
    text = (task.get("output") or {}).get("text")
    if text:
        out["text"] = text
    return out


def emit(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


# --------------------------------------------------------------------------- commands


def cmd_models(args: argparse.Namespace) -> None:
    payload = http_json("GET", f"{CATALOG_URL}?locale=en", auth=False)
    items = data_of(payload).get("items", [])
    rows = []
    for it in items:
        if args.spicy and not it.get("mature"):
            continue
        if args.modality and it.get("modality") != args.modality:
            continue
        if args.task and not it.get("model", "").endswith("/" + args.task):
            continue
        if args.search and args.search.lower() not in (it.get("model", "") + it.get("displayName", "")).lower():
            continue
        price = it.get("price") or {}
        rows.append({
            "model": it.get("model"),
            "name": it.get("familyDisplayName") or it.get("displayName"),
            "modality": it.get("modality"),
            "spicy": bool(it.get("mature")),
            "policyTier": it.get("policyTier"),
            "from": price.get("amount"),
            "unit": price.get("unit"),
            "inputs": it.get("inputFields"),
            "page": f"https://spicyapi.ai/models/{it.get('familyPageSlug')}",
        })
    if args.json:
        emit(rows)
        return
    print(f"{len(rows)} model(s). Prices are the cheapest tier; run `schema <model>` for exact tiers.\n")
    for r in rows:
        tag = "🌶️ " if r["spicy"] else "   "
        print(f"{tag}{r['model']:<52} ${r['from']} {r['unit']:<13} [{r['policyTier']}]")


def cmd_schema(args: argparse.Namespace) -> None:
    if os.environ.get("SPICY_API_KEY", "").strip():
        model = urllib.parse.quote(args.model, safe="")
        record = data_of(http_json("GET", f"{API_BASE}/models/{model}"))
        source = "authenticated"
    else:
        # Without a key, read the public model page data. Prices there are public list prices.
        record = data_of(http_json("GET", f"{CATALOG_URL}/{args.model}?locale=en", auth=False))
        source = "public"
    if args.full:
        emit(record)
        return
    keys = ("model", "displayName", "modality", "mature", "policyTier", "available", "quantityField",
            "pricing", "price", "inputSchema", "paramNotes", "examples")
    summary = {k: record.get(k) for k in keys if record.get(k) is not None}
    summary["schemaSource"] = source
    emit(summary)


def cmd_quote(args: argparse.Namespace) -> None:
    emit(quote(args.model, build_input(args)))


def cmd_generate(args: argparse.Namespace) -> None:
    payload = build_input(args)
    if not payload:
        raise SpicyError("No input given. Use --prompt/--image/--set key=value/--input/--input-file.")
    q = quote(args.model, payload)
    print(f"quote: estimated ${q['estimatedCost']}, max charge ${q['maxCharge']} "
          f"({q['quantity']} {q['unit']}), expires {q['expiresAt']}", file=sys.stderr)
    approved = args.yes or (args.max_cost is not None and float(q["maxCharge"]) <= args.max_cost)
    if not approved:
        emit({"status": "needs_confirmation", "model": args.model, "input": payload, "quote": q,
              "next": "Re-run with --yes after the user approves this price, or pass --max-cost."})
        sys.exit(2)
    idem = args.idempotency_key or str(uuid.uuid4())
    body = {"model": args.model, "input": payload, "quoteId": q["quoteId"], "expectedCost": q["estimatedCost"]}
    created = data_of(http_json("POST", f"{API_BASE}/jobs/createTask", body, headers={"Idempotency-Key": idem}))
    print(f"task {created['taskId']} accepted (idempotency key {idem})", file=sys.stderr)
    task = created if args.no_wait else wait_for(created["taskId"], args.timeout)
    result = summarize(task)
    result["idempotencyKey"] = idem
    if task.get("state") == "succeeded" and not args.no_download:
        result["saved"] = download(task, args.out)
    emit(result)
    if task.get("state") in ("failed", "canceled", "expired"):
        sys.exit(1)


def cmd_status(args: argparse.Namespace) -> None:
    task = wait_for(args.task_id, args.timeout) if args.wait else get_task(args.task_id)
    result = summarize(task)
    if args.download and task.get("state") == "succeeded":
        result["saved"] = download(task, args.download)
    emit(result)


def cmd_upload(args: argparse.Namespace) -> None:
    emit(upload_file(Path(args.path).expanduser()))


def cmd_balance(_: argparse.Namespace) -> None:
    emit(data_of(http_json("GET", f"{API_BASE}/chat/credit")))


def cmd_chat(args: argparse.Namespace) -> None:
    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": args.message})
    payload = http_json("POST", f"{SERVICE_BASE}/v1/chat/completions",
                        {"model": args.model, "messages": messages}, timeout=180)
    print(payload["choices"][0]["message"]["content"])


# --------------------------------------------------------------------------- CLI


def add_input_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("model", help="exact model ID from the catalog, e.g. alibaba/wan-2.2-spicy/image-to-video")
    p.add_argument("--prompt", "-p", help="sets input.prompt")
    p.add_argument("--image", help="URL, spicy:// URI or local file for input.image_url (local files are uploaded)")
    p.add_argument("--images", action="append", metavar="URL_OR_FILE",
                   help="repeatable; fills input.image_urls for multi-reference models (e.g. qwen-image-2.1/edit)")
    p.add_argument("--last-image", dest="last_image", help="URL or local file for input.last_image_url")
    p.add_argument("--video", help="URL or local file for input.video_url")
    p.add_argument("--audio", help="URL or local file for input.audio_url")
    p.add_argument("--set", action="append", metavar="KEY=VALUE",
                   help="any schema field, repeatable: --set duration_seconds=5 --set resolution=720p")
    p.add_argument("--input", help="full input object as JSON")
    p.add_argument("--input-file", help="path to a JSON file with the input object")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="spicy.py", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("models", help="list catalog models (no key needed)")
    p.add_argument("--spicy", action="store_true", help="only Spicy (adult-tuned) editions")
    p.add_argument("--modality", choices=["image", "video", "text", "audio"])
    p.add_argument("--task", help="task suffix, e.g. image-to-video, text-to-image, edit, video-extend")
    p.add_argument("--search", help="substring match on model ID or name")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_models)

    p = sub.add_parser("schema", help="live input schema and prices for one model")
    p.add_argument("model")
    p.add_argument("--full", action="store_true", help="print the complete model record")
    p.set_defaults(func=cmd_schema)

    p = sub.add_parser("quote", help="price an exact request")
    add_input_flags(p)
    p.set_defaults(func=cmd_quote)

    p = sub.add_parser("generate", help="quote, create, wait and download")
    add_input_flags(p)
    p.add_argument("--yes", action="store_true", help="approve the quoted price and run")
    p.add_argument("--max-cost", type=float, help="auto-approve when the max charge (USD) is at or below this")
    p.add_argument("--out", default="./spicy-output", help="download directory (default ./spicy-output)")
    p.add_argument("--timeout", type=int, default=900, help="seconds to wait for completion (default 900)")
    p.add_argument("--no-wait", action="store_true", help="return right after the task is accepted")
    p.add_argument("--no-download", action="store_true", help="print output URLs without downloading")
    p.add_argument("--idempotency-key", help="reuse a key when retrying an uncertain request")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("status", help="show a task")
    p.add_argument("task_id")
    p.add_argument("--wait", action="store_true", help="wait until the task finishes")
    p.add_argument("--timeout", type=int, default=900)
    p.add_argument("--download", metavar="DIR", help="download outputs into DIR when succeeded")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("upload", help="upload a local file, print its spicy:// URI")
    p.add_argument("path")
    p.set_defaults(func=cmd_upload)

    p = sub.add_parser("balance", help="account balance")
    p.set_defaults(func=cmd_balance)

    p = sub.add_parser("chat", help="text model via the OpenAI-compatible endpoint")
    p.add_argument("model", help="e.g. xai/grok-4.7/chat")
    p.add_argument("message")
    p.add_argument("--system", help="optional system prompt")
    p.set_defaults(func=cmd_chat)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except SpicyError as err:
        detail = {"error": str(err)}
        if err.code is not None:
            detail["code"] = err.code
        if err.request_id:
            detail["request_id"] = err.request_id
        print(json.dumps(detail, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
