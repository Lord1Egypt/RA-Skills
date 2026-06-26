#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from pathlib import Path
from typing import Any

from bootstrap_common import (
    BootstrapError,
    default_env_file,
    encrypt_password_via_docker,
    http_json,
    login_user,
    read_env_file,
    write_env_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="配置 RAGFlow 默认 Embedding/Chat/Rerank 模型。")
    parser.add_argument("--base-url", help="RAGFlow API 地址，默认从 .env 读取 RAGFLOW_API_URL")
    parser.add_argument("--container-name", help="容器名，默认从 .env 读取 RAGFLOW_CONTAINER_NAME")
    parser.add_argument("--email", help="管理员邮箱，默认从 .env 读取 RAGFLOW_ADMIN_EMAIL")
    parser.add_argument("--password", help="管理员密码，默认从 .env 读取 RAGFLOW_ADMIN_PASSWORD")
    parser.add_argument("--embedding-model", default="bge-m3", help="Embedding 模型名")
    parser.add_argument("--chat-model", default="Gemma4:E2B-IT", help="Chat 模型名")
    parser.add_argument("--rerank-model", default="bge-reranker-v2-m3", help="Rerank 模型名")
    parser.add_argument("--api-base", default="http://host.docker.internal:8080/v1", help="本地模型服务地址")
    parser.add_argument("--model-api-key", default="empty", help="本地模型服务 API Key")
    parser.add_argument("--max-tokens", type=int, default=8192, help="模型 max_tokens")
    parser.add_argument(
        "--env-file",
        default=str(default_env_file()),
        help="读取和更新 .env 的路径",
    )
    parser.add_argument("--json", action="store_true", dest="json_output", help="输出 JSON")
    return parser.parse_args()


def _resolve_value(args: argparse.Namespace, env: dict[str, str], arg_key: str, env_key: str, default: str) -> str:
    value = getattr(args, arg_key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return env.get(env_key, default).strip()


def add_model(jwt_token: str, base_url: str, model_type: str, model_name: str, api_base: str, api_key: str, max_tokens: int) -> dict[str, Any]:
    status, payload, _, raw = http_json(
        base_url,
        "/v1/llm/add_llm",
        method="POST",
        token=jwt_token,
        body={
            "llm_factory": "OpenAI-API-Compatible",
            "model_type": model_type,
            "llm_name": model_name,
            "api_key": api_key,
            "api_base": api_base,
            "max_tokens": max_tokens,
        },
    )
    return {"status": status, "payload": payload, "raw": raw}


def update_tenant(jwt_token: str, base_url: str, llm_id: str, embd_id: str, rerank_id: str) -> dict[str, Any]:
    status, payload, _, raw = http_json(
        base_url,
        "/v1/tenant/update",
        method="POST",
        token=jwt_token,
        body={"llm_id": llm_id, "embd_id": embd_id, "rerank_id": rerank_id},
    )
    return {"status": status, "payload": payload, "raw": raw}


def run_configure(args: argparse.Namespace) -> dict[str, Any]:
    env_path = Path(args.env_file)
    env_values = read_env_file(env_path)

    base_url = _resolve_value(args, env_values, "base_url", "RAGFLOW_API_URL", "http://127.0.0.1:9380")
    container_name = _resolve_value(args, env_values, "container_name", "RAGFLOW_CONTAINER_NAME", "docker-ragflow-cpu-1")
    email = _resolve_value(args, env_values, "email", "RAGFLOW_ADMIN_EMAIL", "admin@example.com")
    password = _resolve_value(args, env_values, "password", "RAGFLOW_ADMIN_PASSWORD", "Admin123456")

    encrypted = encrypt_password_via_docker(container_name, password)
    jwt_token = login_user(base_url, email, encrypted)

    steps = {
        "embedding": add_model(jwt_token, base_url, "embedding", args.embedding_model, args.api_base, args.model_api_key, args.max_tokens),
        "rerank": add_model(jwt_token, base_url, "rerank", args.rerank_model, args.api_base, args.model_api_key, args.max_tokens),
        "chat": add_model(jwt_token, base_url, "chat", args.chat_model, args.api_base, args.model_api_key, args.max_tokens),
    }
    tenant = update_tenant(jwt_token, base_url, args.chat_model, args.embedding_model, args.rerank_model)

    if any(step["status"] != 200 for step in steps.values()) or tenant["status"] != 200:
        raise BootstrapError("模型配置请求有失败项，请使用 --json 查看细节。")

    write_env_file(
        env_path,
        {
            "RAGFLOW_MODEL_API_BASE": args.api_base,
            "RAGFLOW_EMBEDDING_MODEL": args.embedding_model,
            "RAGFLOW_LLM_MODEL": args.chat_model,
            "RAGFLOW_RERANK_MODEL": args.rerank_model,
        },
    )

    return {
        "ok": True,
        "base_url": base_url.rstrip("/"),
        "models": {
            "embedding": args.embedding_model,
            "chat": args.chat_model,
            "rerank": args.rerank_model,
        },
        "api_base": args.api_base,
        "steps": steps,
        "tenant": tenant,
        "env_file": str(env_path.resolve()),
        "next": "可使用 scripts/datasets.py create 创建知识库，并用 scripts/create_chat.py 绑定知识库与对话模型",
    }


def print_text(payload: dict[str, Any]) -> None:
    print("默认模型配置完成")
    print(f"base_url: {payload['base_url']}")
    print(f"embedding: {payload['models']['embedding']}")
    print(f"chat: {payload['models']['chat']}")
    print(f"rerank: {payload['models']['rerank']}")
    print(f"api_base: {payload['api_base']}")
    print(f"env_file: {payload['env_file']}")
    print(f"next: {payload['next']}")


def main() -> int:
    args = parse_args()
    try:
        payload = run_configure(args)
    except BootstrapError as exc:
        if args.json_output:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        else:
            print(f"Error: {exc}")
        return 1

    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_text(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
