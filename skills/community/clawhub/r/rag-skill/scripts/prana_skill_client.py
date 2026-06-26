#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
import uuid
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

DEFAULT_BASE_URL = "https://claw-uat.ebonex.io"
DEFAULT_SKILL_KEY = "rag-skill"
AGENT_RUN_TIMEOUT_SEC = 150
AGENT_RESULT_RETRY_TIMES = 30
AGENT_RESULT_RETRY_INTERVAL_SEC = 20


def _headers(x_api_key: str) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "x-api-key": x_api_key,
    }


def _post_json(url: str, payload: Dict[str, Any], x_api_key: str, timeout: int) -> Dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request_id = payload.get("request_id", "") if isinstance(payload, dict) else ""
    print(f"[HTTP REQUEST] request_id={request_id}", file=sys.stderr)
    req = urllib.request.Request(
        url=url,
        data=data,
        method="POST",
        headers=_headers(x_api_key),
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _is_timeout_error(exc: BaseException) -> bool:
    if isinstance(exc, TimeoutError):
        return True
    if isinstance(exc, socket.timeout):
        return True
    if isinstance(exc, urllib.error.URLError):
        return isinstance(exc.reason, socket.timeout)
    return False


def invoke_agent_result_with_retry(
    base_url: str, request_id: str, x_api_key: str
) -> Optional[Dict[str, Any]]:
    url = base_url.rstrip("/") + "/api/claw/agent-result"
    last_result: Dict[str, Any] = {"error": True, "detail": "agent-result 尚未获取到结果"}
    for attempt in range(1, AGENT_RESULT_RETRY_TIMES + 1):
        if attempt > 1:
            time.sleep(AGENT_RESULT_RETRY_INTERVAL_SEC)
        try:
            result = _post_json(
                url=url,
                payload={"request_id": request_id},
                x_api_key=x_api_key,
                timeout=AGENT_RUN_TIMEOUT_SEC,
            )
            last_result = result
            data = result.get("data") if isinstance(result, dict) else None
            status = ""
            if isinstance(data, dict):
                status = str(data.get("status", "")).lower()
            if not status and isinstance(result, dict):
                status = str(result.get("status", "")).lower()
            if status == "running":
                continue
            if status:
                return result
        except Exception as exc:  # noqa: BLE001
            return {"error": True, "detail": f"第 {attempt} 次 agent-result 请求失败: {exc}"}
    print(
        f"提示: 本轮尝试已达到上限；Prana 服务端任务可能仍需要较长时间才能完成。若希望继续等待同一任务结果，必须先向用户确认；仅在用户明确确认“重试”后，才可继续执行后续命令：python3 scripts/prana_skill_client.py -r {request_id}",
        file=sys.stderr,
    )
    return None


def invoke_agent_run(
    base_url: str, skill_key: str, question: str, x_api_key: str
) -> Optional[Dict[str, Any]]:
    request_id = str(uuid.uuid4())
    run_url = base_url.rstrip("/") + "/api/claw/agent-run"
    run_payload = {
        "skill_key": skill_key,
        "question": question,
        "request_id": request_id,
    }
    try:
        run_result = _post_json(
            url=run_url,
            payload=run_payload,
            x_api_key=x_api_key,
            timeout=AGENT_RUN_TIMEOUT_SEC,
        )
        run_data = run_result.get("data") if isinstance(run_result, dict) else None
        run_status = str((run_data or {}).get("status", "")).lower() if isinstance(run_data, dict) else ""
        if run_status == "running":
            return invoke_agent_result_with_retry(base_url, request_id, x_api_key)
        return run_result
    except Exception as exc:  # noqa: BLE001
        if _is_timeout_error(exc):
            return invoke_agent_result_with_retry(base_url, request_id, x_api_key)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description="调用 Prana 技能接口。question=用户需求任务。"
    )
    parser.add_argument("--question", "-q", default=None, help="用户需求任务描述，例如：帮我使用XXX技能")
    parser.add_argument(
        "--request-id",
        "-r",
        default=None,
        dest="request_id",
        help="指定需要查询的任务的 request_id",
    )
    args = parser.parse_args()

    question_trimmed = str(args.question).strip() if args.question is not None else ""
    request_id_arg = (args.request_id or "").strip()
    if not question_trimmed and not request_id_arg:
        parser.error("必须提供 --question/-q 发起新任务，或提供 --request-id/-r 查询指定任务状态")

    x_api_key = os.getenv("PRANA_SKILL_API_FLAG", "").strip()
    if not x_api_key:
        print("错误: 未检测到环境变量 PRANA_SKILL_API_FLAG。", file=sys.stderr)
        sys.exit(1)

    try:
        if question_trimmed:
            result = invoke_agent_run(
                base_url=DEFAULT_BASE_URL,
                skill_key=DEFAULT_SKILL_KEY,
                question=question_trimmed,
                x_api_key=x_api_key,
            )
        else:
            result = invoke_agent_result_with_retry(
                base_url=DEFAULT_BASE_URL,
                request_id=request_id_arg,
                x_api_key=x_api_key,
            )
        if result is not None:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {body}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:  # noqa: BLE001
        print(f"请求失败: {exc}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
