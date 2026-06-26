# -*- coding: utf-8 -*-
"""
统一 Skill 入口：先执行小爱 → 飞书多维表增量同步，再对多维表做增量标注：
- 类型（机器）
- 评价情感（机器）
- 是否提及竞品(机器)
- 端(机器)
- 品牌安全(AI)
- 内容安全(AI)

所有入参通过环境变量传入（Skill 运行时注入 INPUT_*）。
"""
import os
import sys

# 从环境变量读取 Skill 入参（名称与 SKILL.md 中 inputs.name 对应，统一加 INPUT_ 前缀）
def _env(key: str, default: str = "") -> str:
    return os.getenv(f"INPUT_{key.upper()}", os.getenv(key, default)).strip()

def _env_int(key: str, default: int) -> int:
    try:
        return int(_env(key, str(default)))
    except ValueError:
        return default

def _env_bool(key: str, default: bool = False) -> bool:
    v = _env(key, "false").lower()
    return v in ("1", "true", "yes", "on") if not default else v not in ("0", "false", "no", "off")


def main() -> None:
    # 同步所需
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

    # 1) 小爱 → 多维表增量同步
    import excel_to_feishu_bitable as m
    m.APP_ID = app_id
    m.APP_SECRET = app_secret
    m.TOKEN = xiaoai_token
    m.BASE_URL = xiaoai_base_url
    m.DEFAULT_FOLDER_ID = folder_id
    m.DEFAULT_CUSTOMER_ID = customer_id
    m.BITABLE_URL = bitable_url

    inserted = m.run_once(minutes)
    print(f"inserted_count={inserted}")

    # 2) 可选：多维表增量标注（由 OpenClaw 内置大模型通过 stdin 提供结果）
    run_labeling = _env_bool("run_labeling", False)
    labeling_limit = _env_int("labeling_limit", 100)

    if run_labeling and bitable_url:
        import bitable_labeling_skill as bl
        bl.BITABLE_URL = bitable_url
        bl.APP_ID = app_id
        bl.APP_SECRET = app_secret
        bl.LIMIT = labeling_limit
        try:
            updated = bl.run_once()
            print(f"labeling_updated_count={updated}")
        except Exception as e:
            print(f"labeling_error={e}", file=sys.stderr)
            print("labeling_updated_count=0")
    else:
        print("labeling_updated_count=0")


if __name__ == "__main__":
    main()
