# -*- coding: utf-8 -*-
"""
独立标注 Skill 入口：仅对飞书多维表做增量 AI 标注，不执行同步。
标注字段：类型（机器）、评价情感（机器）、是否提及竞品(机器)、端(机器)、品牌安全(AI)、内容安全(AI)。
所有入参通过环境变量传入（Skill 运行时注入 INPUT_*）。
"""
import os
import sys


def _env(key: str, default: str = "") -> str:
    return os.getenv(f"INPUT_{key.upper()}", os.getenv(key, default)).strip()


def _env_int(key: str, default: int) -> int:
    try:
        return int(_env(key, str(default)))
    except ValueError:
        return default


def main() -> None:
    bitable_url = _env("bitable_url")
    app_id = _env("app_id")
    app_secret = _env("app_secret")
    limit = _env_int("limit", 100)
    openai_api_key = _env("openai_api_key")
    openai_base_url = _env("openai_base_url")
    openai_model = _env("openai_model")

    if not all([bitable_url, app_id, app_secret]):
        print("missing_required=bitable_url,app_id,app_secret", file=sys.stderr)
        sys.exit(1)

    # 现在 OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL 都是必填
    if not all([openai_api_key, openai_base_url, openai_model]):
        print("missing_required=openai_api_key,openai_base_url,openai_model - 全部必填，不可省略", file=sys.stderr)
        sys.exit(1)

    import bitable_labeling_skill as bl
    bl.BITABLE_URL = bitable_url
    bl.APP_ID = app_id
    bl.APP_SECRET = app_secret
    bl.LIMIT = limit
    bl.OPENAI_API_KEY = openai_api_key
    bl.OPENAI_BASE_URL = openai_base_url.rstrip("/")
    bl.OPENAI_MODEL = openai_model

    try:
        updated = bl.run_once()
        print(f"labeling_updated_count={updated}")
    except Exception as e:
        print(f"labeling_error={e}", file=sys.stderr)
        print("labeling_updated_count=0")
        sys.exit(1)


if __name__ == "__main__":
    main()
