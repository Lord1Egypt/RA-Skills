#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from typing import Any

from common import (
    ConfigError,
    DataError,
    ScriptError,
    add_runtime_config_arguments,
    configure_stdio_utf8,
    current_timestamp,
    ensure_success,
    format_json,
    get_default_dataset_id,
    request_json,
    resolve_runtime_config,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="创建对话并绑定知识库、LLM、Rerank。")
    parser.add_argument("name", help="对话名称")
    parser.add_argument("--dataset-ids", help="逗号分隔的知识库 ID 列表 (默认为主知识库)")
    parser.add_argument("--llm-id", required=True, help="LLM 模型 ID/名称")
    parser.add_argument("--rerank-id", help="Rerank 模型 ID/名称")
    parser.add_argument("--system", help="系统提示词")
    parser.add_argument("--empty-response", help="无检索结果时回复")
    parser.add_argument("--json", action="store_true", dest="json_output", help="输出 JSON")
    add_runtime_config_arguments(parser)
    return parser.parse_args(argv)


def parse_ids(raw_value: str) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for item in raw_value.split(","):
        value = item.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        ids.append(value)
    if not ids:
        raise ConfigError("--dataset-ids 至少要有一个有效 ID")
    return ids


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.name.strip():
        raise ConfigError("name 不能为空")

    prompt_config: dict[str, Any] = {}
    if args.rerank_id:
        prompt_config["rerank_id"] = args.rerank_id
    if args.system:
        prompt_config["system"] = args.system
    if args.empty_response:
        prompt_config["empty_response"] = args.empty_response

    # Resolve dataset_ids
    dataset_ids: list[str] = []
    if args.dataset_ids:
        dataset_ids = parse_ids(args.dataset_ids)
    else:
        default_id = get_default_dataset_id()
        if default_id:
            dataset_ids = [default_id]
        else:
            raise ConfigError("--dataset-ids is required, and no default dataset is set.")

    payload: dict[str, Any] = {
        "name": args.name.strip(),
        "dataset_ids": dataset_ids,
        "llm_id": args.llm_id.strip(),
    }
    if prompt_config:
        payload["prompt_config"] = prompt_config
    return payload


def create_chat(args: argparse.Namespace, *, base_url: str, api_key: str) -> dict[str, Any]:
    payload = ensure_success(
        request_json(
            f"{base_url}/api/v1/chats",
            api_key,
            method="POST",
            body=json.dumps(build_payload(args)).encode("utf-8"),
            content_type="application/json",
        )
    )
    data = payload.get("data")
    if not isinstance(data, dict):
        raise DataError("创建对话响应缺少 data 对象")
    return {
        "created_at": current_timestamp(),
        "chat": data,
    }


def main(argv: list[str] | None = None) -> int:
    configure_stdio_utf8()
    args = parse_args(argv)
    try:
        base_url, api_key = resolve_runtime_config(args)
        result = create_chat(args, base_url=base_url, api_key=api_key)
    except ScriptError as exc:
        if args.json_output:
            print(format_json({"created_at": current_timestamp(), "error": str(exc)}))
        else:
            print(f"Error: {exc}")
        return 1

    if args.json_output:
        print(format_json(result))
    else:
        chat = result["chat"]
        print(f"Created at: {result['created_at']}")
        print(f"Chat name: {chat.get('name')}")
        print(f"Chat id: {chat.get('id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
