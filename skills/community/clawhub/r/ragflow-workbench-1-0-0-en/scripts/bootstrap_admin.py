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
    get_or_create_api_token,
    login_user,
    register_user,
    write_env_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="初始化管理员账号并自动生成 RAGFlow API Key。")
    parser.add_argument("--base-url", default="http://127.0.0.1:9380", help="RAGFlow API 地址")
    parser.add_argument("--container-name", default="docker-ragflow-cpu-1", help="RAGFlow 容器名")
    parser.add_argument("--nickname", default="admin", help="管理员昵称")
    parser.add_argument("--email", default="admin@example.com", help="管理员邮箱")
    parser.add_argument("--password", default="Admin123456", help="管理员密码")
    parser.add_argument("--token-name", default="ragflow-skill-key", help="要创建/复用的 API Token 名称")
    parser.add_argument(
        "--env-file",
        default=str(default_env_file()),
        help="输出 .env 文件路径，默认写入技能目录下 .env",
    )
    parser.add_argument("--json", action="store_true", dest="json_output", help="输出 JSON")
    return parser.parse_args()


def run_bootstrap(args: argparse.Namespace) -> dict[str, Any]:
    encrypted = encrypt_password_via_docker(args.container_name, args.password)

    register_result = register_user(args.base_url, args.nickname, args.email, encrypted)
    jwt_token = login_user(args.base_url, args.email, encrypted)
    api_key = get_or_create_api_token(args.base_url, jwt_token, args.token_name)

    env_updates = {
        "RAGFLOW_API_URL": args.base_url.rstrip("/"),
        "RAGFLOW_API_KEY": api_key,
        "RAGFLOW_CONTAINER_NAME": args.container_name,
        "RAGFLOW_ADMIN_EMAIL": args.email,
        "RAGFLOW_ADMIN_PASSWORD": args.password,
    }
    write_env_file(Path(args.env_file), env_updates)

    return {
        "ok": True,
        "base_url": args.base_url.rstrip("/"),
        "email": args.email,
        "token_name": args.token_name,
        "api_key": api_key,
        "register_status": register_result["status"],
        "register_response": register_result["payload"],
        "env_file": str(Path(args.env_file).resolve()),
        "next": "运行 scripts/configure_default_models.py 配置默认模型",
    }


def print_text(payload: dict[str, Any]) -> None:
    print("管理员初始化完成")
    print(f"base_url: {payload['base_url']}")
    print(f"email: {payload['email']}")
    print(f"token_name: {payload['token_name']}")
    print(f"api_key: {payload['api_key']}")
    print(f"env_file: {payload['env_file']}")
    print(f"next: {payload['next']}")


def main() -> int:
    args = parse_args()
    try:
        payload = run_bootstrap(args)
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
