#!/usr/bin/env python3
"""ComfyUI API 客户端（仅使用 Python 标准库）。"""

from __future__ import annotations

import argparse
import copy
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

DEFAULT_API_URL = "http://host.docker.internal:8188"
DEFAULT_TIMEOUT = 30


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def api_url() -> str:
    return os.environ.get("COMFYUI_API_URL", DEFAULT_API_URL).rstrip("/")


def http_json(method: str, path: str, payload: dict[str, Any] | None = None, timeout: int = DEFAULT_TIMEOUT) -> Any:
    url = f"{api_url()}{path}"
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            if not body:
                return {}
            return json.loads(body.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"网络请求失败: {exc}") from exc


def http_download(path: str, output_path: str, timeout: int = DEFAULT_TIMEOUT) -> None:
    url = f"{api_url()}{path}"
    req = urllib.request.Request(url=url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp, open(output_path, "wb") as f:
            f.write(resp.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"下载失败 HTTP {exc.code} {exc.reason}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"下载失败: {exc}") from exc


def load_workflow(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        workflow = json.load(f)
    if not isinstance(workflow, dict):
        raise RuntimeError("workflow JSON 顶层必须是对象")
    return workflow


def submit_workflow(workflow: dict[str, Any]) -> str:
    result = http_json("POST", "/prompt", {"prompt": workflow})
    prompt_id = result.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"提交成功但未返回 prompt_id: {result}")
    return str(prompt_id)


def query_status(prompt_id: str) -> dict[str, Any]:
    history = http_json("GET", f"/history/{prompt_id}")
    item = history.get(prompt_id)
    completed = bool(item and item.get("status", {}).get("completed", False))
    return {
        "prompt_id": prompt_id,
        "completed": completed,
        "raw": item if item else history,
    }


def extract_image_items(history_item: dict[str, Any]) -> list[dict[str, str]]:
    outputs = history_item.get("outputs", {})
    items: list[dict[str, str]] = []
    for node_id, node_output in outputs.items():
        images = node_output.get("images", [])
        for image in images:
            filename = image.get("filename")
            subfolder = image.get("subfolder", "")
            image_type = image.get("type", "output")
            if filename:
                items.append(
                    {
                        "node_id": str(node_id),
                        "filename": str(filename),
                        "subfolder": str(subfolder),
                        "type": str(image_type),
                    }
                )
    return items


def download_outputs(history_item: dict[str, Any], output_dir: str, prefix: str) -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
    image_items = extract_image_items(history_item)
    saved_files: list[str] = []

    for idx, item in enumerate(image_items, start=1):
        params = urllib.parse.urlencode(
            {
                "filename": item["filename"],
                "subfolder": item["subfolder"],
                "type": item["type"],
            }
        )
        ext = os.path.splitext(item["filename"])[1] or ".png"
        save_name = f"{prefix}_{idx}{ext}"
        save_path = os.path.abspath(os.path.join(output_dir, save_name))
        http_download(f"/view?{params}", save_path)
        saved_files.append(save_path)

    return saved_files


def wait_for_completion(prompt_id: str, poll_interval: float, timeout_sec: int) -> dict[str, Any]:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        history = http_json("GET", f"/history/{prompt_id}")
        item = history.get(prompt_id)
        if item and item.get("status", {}).get("completed", False):
            return item
        time.sleep(poll_interval)
    raise RuntimeError(f"等待超时，prompt_id={prompt_id}")


def update_seed(workflow: dict[str, Any], seed: int) -> dict[str, Any]:
    new_workflow = copy.deepcopy(workflow)
    updated = False
    for node in new_workflow.values():
        if isinstance(node, dict) and node.get("class_type") == "KSampler":
            inputs = node.get("inputs", {})
            if isinstance(inputs, dict):
                inputs["seed"] = int(seed)
                updated = True
    if not updated:
        raise RuntimeError("workflow 中未找到 KSampler 节点，无法设置 seed")
    return new_workflow


def cmd_health(_: argparse.Namespace) -> int:
    try:
        stats = http_json("GET", "/system_stats")
        print(
            json.dumps(
                {
                    "ok": True,
                    "api_url": api_url(),
                    "system_stats": stats,
                },
                ensure_ascii=False,
            )
        )
        return 0
    except Exception as exc:  # noqa: BLE001
        eprint(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


def cmd_submit(args: argparse.Namespace) -> int:
    try:
        workflow = load_workflow(args.workflow)
        prompt_id = submit_workflow(workflow)
        print(json.dumps({"ok": True, "prompt_id": prompt_id}, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001
        eprint(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


def cmd_status(args: argparse.Namespace) -> int:
    try:
        status = query_status(args.prompt_id)
        status["ok"] = True
        print(json.dumps(status, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001
        eprint(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


def cmd_wait(args: argparse.Namespace) -> int:
    try:
        workflow = load_workflow(args.workflow)
        prompt_id = submit_workflow(workflow)
        history_item = wait_for_completion(prompt_id, args.poll_interval, args.timeout)
        files = download_outputs(history_item, args.output_dir, prefix=f"{prompt_id}")
        print(
            json.dumps(
                {
                    "ok": True,
                    "prompt_id": prompt_id,
                    "completed": True,
                    "output_files": files,
                },
                ensure_ascii=False,
            )
        )
        return 0
    except Exception as exc:  # noqa: BLE001
        eprint(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


def cmd_batch(args: argparse.Namespace) -> int:
    try:
        base_workflow = load_workflow(args.workflow)
        start_seed = args.seed_start if args.seed_start is not None else random.randint(1, 2**31 - 1)

        submissions: list[dict[str, Any]] = []
        for i in range(args.count):
            seed = start_seed + i
            wf = update_seed(base_workflow, seed)
            prompt_id = submit_workflow(wf)
            submissions.append({"prompt_id": prompt_id, "seed": seed})

        results: list[dict[str, Any]] = []
        for item in submissions:
            prompt_id = item["prompt_id"]
            history_item = wait_for_completion(prompt_id, args.poll_interval, args.timeout)
            files = download_outputs(history_item, args.output_dir, prefix=f"{prompt_id}_{item['seed']}")
            results.append(
                {
                    "prompt_id": prompt_id,
                    "seed": item["seed"],
                    "output_files": files,
                }
            )

        print(json.dumps({"ok": True, "count": args.count, "results": results}, ensure_ascii=False))
        return 0
    except Exception as exc:  # noqa: BLE001
        eprint(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ComfyUI API 客户端")
    sub = parser.add_subparsers(dest="command", required=True)

    p_health = sub.add_parser("health", help="检查 ComfyUI 是否在线")
    p_health.set_defaults(func=cmd_health)

    p_submit = sub.add_parser("submit", help="提交 workflow 并返回 prompt_id")
    p_submit.add_argument("--workflow", required=True, help="workflow JSON 文件路径")
    p_submit.set_defaults(func=cmd_submit)

    p_status = sub.add_parser("status", help="查询 prompt_id 状态")
    p_status.add_argument("--prompt-id", required=True, help="任务 prompt_id")
    p_status.set_defaults(func=cmd_status)

    p_wait = sub.add_parser("wait", help="提交 workflow 并等待完成")
    p_wait.add_argument("--workflow", required=True, help="workflow JSON 文件路径")
    p_wait.add_argument("--output-dir", required=True, help="下载结果的输出目录")
    p_wait.add_argument("--poll-interval", type=float, default=2.0, help="轮询间隔（秒）")
    p_wait.add_argument("--timeout", type=int, default=900, help="超时时间（秒）")
    p_wait.set_defaults(func=cmd_wait)

    p_batch = sub.add_parser("batch", help="批量提交同一 workflow 的不同 seed 变体")
    p_batch.add_argument("--workflow", required=True, help="workflow JSON 文件路径")
    p_batch.add_argument("--count", type=int, default=4, help="批量数量")
    p_batch.add_argument("--output-dir", required=True, help="下载结果的输出目录")
    p_batch.add_argument("--seed-start", type=int, default=None, help="起始 seed")
    p_batch.add_argument("--poll-interval", type=float, default=2.0, help="轮询间隔（秒）")
    p_batch.add_argument("--timeout", type=int, default=900, help="每个任务超时时间（秒）")
    p_batch.set_defaults(func=cmd_batch)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
