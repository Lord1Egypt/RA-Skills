# -*- coding: utf-8 -*-
"""
惠科/小爱同步 Skill 入口：仅将数据接口增量同步到飞书多维表，不执行标注。
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
    minutes = _env_int("minutes", 60)
    folder_id = _env_int("folder_id", 763579)
    customer_id = _env("customer_id", "xmxa")
    app_id = _env("app_id")
    app_secret = _env("app_secret")
    xiaoai_token = _env("xiaoai_token")
    bitable_url = _env("bitable_url")
    xiaoai_base_url = _env("xiaoai_base_url", "http://wisers-data-service.wisersone.com.cn")

    if not all([app_id, app_secret, xiaoai_token, bitable_url]):
        print("missing_required=app_id,app_secret,xiaoai_token,bitable_url", file=sys.stderr)
        sys.exit(1)

    import excel_to_feishu_bitable as m
    m.APP_ID = app_id
    m.APP_SECRET = app_secret
    m.TOKEN = xiaoai_token
    m.BASE_URL = xiaoai_base_url
    m.DEFAULT_FOLDER_ID = folder_id
    m.DEFAULT_CUSTOMER_ID = customer_id
    m.BITABLE_URL = bitable_url

    try:
        inserted = m.run_once(minutes)
        print(f"inserted_count={inserted}")
    except Exception as e:
        print(f"sync_error={e}", file=sys.stderr)
        print("inserted_count=0")
        sys.exit(1)


if __name__ == "__main__":
    main()
