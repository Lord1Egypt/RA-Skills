#!/usr/bin/env python3
"""Remove background from an image using Tekan Common Task API.

## AGENT INSTRUCTIONS — READ FIRST
- Default workflow: ALWAYS use `run` (submit + auto-poll).
  Do NOT ask the user to run query manually.
- Only use `query` when `run` has already timed out and a taskId exists,
  or when the user explicitly provides a taskId to resume.
- When using `query`, keep polling (default timeout=300s) until
  status is 'success' or 'fail'. Do NOT stop after a single check.
- Never hand a pending taskId back to the user and say "check it later".
  Always poll to completion within the timeout window.

The output `bgRemovedImageFileId` can be passed directly to
product_avatar.py --product-image-no-bg for the Product Avatar workflow.

Subcommands:
    run     Submit task AND poll until done — DEFAULT, use this first
    submit  Submit only, print taskId, exit — use for parallel batch jobs
    query   Poll an existing taskId until done (or timeout) — use for recovery

Usage:
    python remove_bg.py run    --image <fileId|path> [options]
    python remove_bg.py submit --image <fileId|path> [options]
    python remove_bg.py query  --task-id <taskId> [--timeout 300] [--interval 3] [options]
"""

import argparse
import json as json_mod
import os
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(__file__))

from shared.client import TopviewClient, TopviewError, to_tekan_credit, convert_result_credits
from shared.upload import TEKAN_S3_API_URL, product_main_image_upload, resolve_local_file

SUBMIT_PATH = "/v1/common_task/remove_background/submit"
QUERY_PATH = "/v1/common_task/remove_background/query"

# aigc-web-turbo apps/base/src/server/api/services/productAnyShoot.ts — same host as ecommerce common_task.
# Default api.tekan.cn:8095 (TEKAN_S3_API_URL), not api.topview.ai/v1. Override: TEKAN_COMMON_TASK_URL.
TEKAN_COMMON_TASK_URL = os.environ.get("TEKAN_COMMON_TASK_URL", TEKAN_S3_API_URL).rstrip("/")
TEKAN_RB_SUBMIT = "/common_task/remove_background/submit"
TEKAN_RB_DETAIL = "/common_task/remove_background/detail"

_HTTP_TIMEOUT = (15, 120)

DEFAULT_TIMEOUT = 300
DEFAULT_INTERVAL = 3


# ---------------------------------------------------------------------------
# Tekan gateway (aigc-web productAnyShoot — uid/teamId headers, /detail query)
# ---------------------------------------------------------------------------


def _tekan_uid_headers(client: TopviewClient) -> dict:
    """Match ecommerce_image._uid_headers — boards/common_task on Tekan use uid, not Topview Bearer."""
    uid = (client._uid or "").strip() or "anonymous"
    return {"uid": uid, "teamId": uid, "Content-Type": "application/json"}


def _tekan_unwrap(data: dict):
    """Same contract as TopviewClient._check: code 200 → result payload."""
    code = str(data.get("code", ""))
    if code != "200":
        raise TopviewError(code, data.get("message", str(data)))
    if "result" in data:
        return data["result"]
    if "data" in data:
        return data["data"]
    return data


def tekan_remove_background_submit(
    client: TopviewClient, body: dict, *, quiet: bool
) -> str:
    """POST {BASE}/common_task/remove_background/submit — productAnyShoot.createRemoveBackgroundTask."""
    url = f"{TEKAN_COMMON_TASK_URL}{TEKAN_RB_SUBMIT}"
    if not quiet:
        print(
            f"Submitting remove-background (Tekan {TEKAN_COMMON_TASK_URL})...",
            file=sys.stderr,
        )
    resp = requests.post(
        url,
        headers=_tekan_uid_headers(client),
        json=body,
        timeout=_HTTP_TIMEOUT,
    )
    resp.raise_for_status()
    raw = _tekan_unwrap(resp.json())
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict) and raw.get("taskId"):
        return str(raw["taskId"])
    raise RuntimeError(f"remove_background submit: unexpected result: {raw!r}")


def tekan_remove_background_poll_detail(
    client: TopviewClient,
    task_id: str,
    *,
    timeout: float,
    interval: float,
    quiet: bool,
) -> dict:
    """GET {BASE}/common_task/remove_background/detail?taskId= — productAnyShoot.queryRemoveBackgroundTaskDetail."""
    url = f"{TEKAN_COMMON_TASK_URL}{TEKAN_RB_DETAIL}"
    if not quiet:
        print(
            f"Polling remove-background detail (timeout={timeout}s, interval={interval}s)...",
            file=sys.stderr,
        )
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            raise TimeoutError(
                f"Task {task_id} did not complete within {timeout}s"
            )
        resp = requests.get(
            url,
            headers=_tekan_uid_headers(client),
            params={"taskId": task_id},
            timeout=_HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        result = _tekan_unwrap(resp.json())
        if not isinstance(result, dict):
            raise RuntimeError(f"remove_background detail: expected object, got {result!r}")
        status = str(result.get("status", "")).lower()
        if not quiet:
            print(f"  [{elapsed:.0f}s] status: {status}", file=sys.stderr)
        if status == "success":
            return result
        if status in ("failed", "fail"):
            raise TopviewError(
                "TASK_FAILED", result.get("errorMsg", "Task failed")
            )
        time.sleep(interval)


# ---------------------------------------------------------------------------
# Helpers (api.topview.ai — legacy fileId + /query)
# ---------------------------------------------------------------------------

def build_body(args, file_id: str) -> dict:
    body = {"productImageFileId": file_id}
    if args.notice_url:
        body["noticeUrl"] = args.notice_url
    return body


def do_submit(client: TopviewClient, body: dict, quiet: bool) -> str:
    if not quiet:
        print("Submitting remove-background task...", file=sys.stderr)
    result = client.post(SUBMIT_PATH, json=body)
    task_id = result["taskId"]
    if not quiet:
        print(f"Task submitted. taskId: {task_id}", file=sys.stderr)
    return task_id


def do_poll(
    client: TopviewClient,
    task_id: str,
    timeout: float,
    interval: float,
    quiet: bool,
    *,
    query_path: str = QUERY_PATH,
) -> dict:
    if not quiet:
        print(
            f"Polling task {task_id} (timeout={timeout}s, interval={interval}s)...",
            file=sys.stderr,
        )
    return client.poll_task(
        query_path,
        task_id,
        interval=interval,
        timeout=timeout,
        verbose=not quiet,
    )


def download_file(url: str, output: str, quiet: bool) -> None:
    import requests as req

    if not quiet:
        print(f"Downloading result to {output}...", file=sys.stderr)

    resp = req.get(url, stream=True)
    resp.raise_for_status()

    with open(output, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    if not quiet:
        size_kb = os.path.getsize(output) / 1024
        print(f"Downloaded: {output} ({size_kb:.1f} KB)", file=sys.stderr)


def run_remove_background(
    image_ref: str,
    client: TopviewClient,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    interval: float = DEFAULT_INTERVAL,
    quiet: bool = False,
) -> dict:
    """Submit remove_background (productImageFileId) and poll /query until success."""
    file_id = resolve_local_file(image_ref, quiet=quiet, client=client)
    body = {"productImageFileId": file_id}
    task_id = do_submit(client, body, quiet)
    return do_poll(client, task_id, timeout, interval, quiet)


def run_remove_background_product_main_web(
    image_ref: str,
    client: TopviewClient,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    interval: float = DEFAULT_INTERVAL,
    quiet: bool = False,
) -> dict:
    """商品主图去背景 — 与 aigc-web `productAnyShoot` + ProductMainImageEcomm 一致。

    - 上传 S3：`product_main_image_upload`（同 useRemoveBackground 路径前缀）
    - 提交：`POST {TEKAN_COMMON_TASK_URL}/common_task/remove_background/submit`
      body: ``productImagePath``, ``projectId``, ``taskSource: product_anyfit``（与 tRPC 一致）
    - 轮询：`GET .../common_task/remove_background/detail?taskId=``（与 queryRemoveBackgroundTaskDetail 一致）
    - 网关：`api.tekan.cn:8095`（与 ecommerce_image 其它 common_task 相同），非 api.topview.ai/v1
    """
    uid = getattr(client, "_uid", None) or ""
    if os.path.isfile(image_ref):
        info = product_main_image_upload(image_ref, uid, quiet=quiet)
        s3_path = info["s3Path"]
    else:
        s3_path = str(image_ref).strip()

    body = {
        "productImagePath": s3_path,
        "projectId": "",
        "taskSource": "product_anyfit",
    }
    task_id = tekan_remove_background_submit(client, body, quiet=quiet)
    if not quiet:
        print(f"Task submitted. taskId: {task_id}", file=sys.stderr)
    return tekan_remove_background_poll_detail(
        client,
        task_id,
        timeout=timeout,
        interval=interval,
        quiet=quiet,
    )


def print_result(result: dict, args) -> None:
    convert_result_credits(result)
    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
        return

    status = result.get("status", "unknown")
    cost = result.get("costCredit", 0)
    file_id = result.get("bgRemovedImageFileId", "")
    image_url = result.get("bgRemovedImagePath", "")
    w = result.get("bgRemovedImageWidth", "")
    h = result.get("bgRemovedImageHeight", "")

    print(f"status: {status}  cost: {cost} credits")
    if file_id:
        print(f"  bgRemovedImageFileId: {file_id}")
    if image_url:
        print(f"  bgRemovedImagePath:   {image_url}")
        if args.output:
            download_file(image_url, args.output, args.quiet)
    if w and h:
        print(f"  dimensions:           {w}x{h}")

    mask_id = result.get("maskImageFileId", "")
    mask_url = result.get("maskImagePath", "")
    if mask_id:
        print(f"  maskImageFileId:      {mask_id}")
    if mask_url:
        print(f"  maskImagePath:        {mask_url}")


# ---------------------------------------------------------------------------
# Argument definitions
# ---------------------------------------------------------------------------

def add_submit_args(p):
    p.add_argument("--image", required=True,
                   help="Product image fileId or local path")
    p.add_argument("--notice-url", default=None,
                   help="Webhook URL for task completion notification")


def add_poll_args(p):
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Max polling time in seconds (default: {DEFAULT_TIMEOUT})")
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                   help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL})")


def add_output_args(p):
    p.add_argument("--output", default=None,
                   help="Download result image to this local path")
    p.add_argument("--json", action="store_true",
                   help="Output full JSON response")
    p.add_argument("-q", "--quiet", action="store_true",
                   help="Suppress status messages on stderr")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_run(args, parser):
    """Submit task then poll until done — full flow (default)."""
    client = TopviewClient()
    client.guard_credit(0, "remove_bg")
    file_id = resolve_local_file(args.image, quiet=args.quiet, client=client)
    body = build_body(args, file_id)
    task_id = do_submit(client, body, args.quiet)
    result = do_poll(client, task_id, args.timeout, args.interval, args.quiet)
    print_result(result, args)


def cmd_submit(args, parser):
    """Submit task only — print taskId and exit immediately."""
    client = TopviewClient()
    client.guard_credit(0, "remove_bg")
    file_id = resolve_local_file(args.image, quiet=args.quiet, client=client)
    body = build_body(args, file_id)
    task_id = do_submit(client, body, args.quiet)
    print(task_id)


def cmd_query(args, parser):
    """Poll an existing task by taskId until done or timeout."""
    client = TopviewClient()
    try:
        result = do_poll(
            client, args.task_id, args.timeout, args.interval, args.quiet,
        )
        print_result(result, args)
    except TimeoutError as e:
        if not args.quiet:
            print(f"Timeout reached: {e}", file=sys.stderr)
            print("Fetching last known status...", file=sys.stderr)
        last = client.get(QUERY_PATH, params={"taskId": args.task_id})
        status = last.get("status", "unknown")
        task_id = last.get("taskId", args.task_id)
        if args.json:
            print(json_mod.dumps(last, indent=2, ensure_ascii=False))
        else:
            print(f"status: {status}  taskId: {task_id}", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Tekan Remove Background — remove image background for product avatar workflow.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
AGENT WORKFLOW RULES:
  1. ALWAYS start with `run` — it submits and polls automatically.
  2. Only use `query` if `run` timed out and you have a taskId to resume.
  3. `query` polls continuously (not once) until done or --timeout.
  4. NEVER hand a pending taskId back to the user — always poll to completion.

Examples:
  # Remove background from a local image
  python remove_bg.py run --image product.png

  # Remove background and download result
  python remove_bg.py run --image product.png --output product_nobg.png

  # Use in Product Avatar workflow:
  #   1. Remove background
  FILE_ID=$(python remove_bg.py run --image product.png -q | grep bgRemovedImageFileId | awk '{print $2}')
  #   2. Replace into avatar scene
  python product_avatar.py run --product-image-no-bg $FILE_ID --avatar-id <avatarId>

  # Batch: submit without waiting
  python remove_bg.py submit --image product.png -q

  # Recovery: poll existing task
  python remove_bg.py query --task-id <taskId> --timeout 600
""",
    )

    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # -- run (default full flow) --
    p_run = sub.add_parser("run", help="[DEFAULT] Submit task and poll until done")
    add_submit_args(p_run)
    add_poll_args(p_run)
    add_output_args(p_run)

    # -- submit only --
    p_submit = sub.add_parser("submit", help="Submit task only, print taskId and exit")
    add_submit_args(p_submit)
    add_output_args(p_submit)

    # -- query / poll existing task --
    p_query = sub.add_parser("query", help="Poll existing taskId until done or timeout")
    p_query.add_argument("--task-id", required=True,
                         help="taskId returned by 'submit' or a previous 'run'")
    add_poll_args(p_query)
    add_output_args(p_query)

    args = parser.parse_args()

    handlers = {
        "run": (cmd_run, p_run),
        "submit": (cmd_submit, p_submit),
        "query": (cmd_query, p_query),
    }

    fn, p = handlers[args.subcommand]
    fn(args, p)


if __name__ == "__main__":
    main()
