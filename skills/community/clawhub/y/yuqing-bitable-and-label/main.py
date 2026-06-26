import argparse
import os
from typing import Optional

import excel_to_feishu_bitable as m


def skill_run_once(
    minutes: int,          # 往前补偿的分钟数（相对于当前时间）
    folder_id: int,        # 小爱接口的 folder_id，用于限定数据范围
    customer_id: str,      # 小爱接口的 customer_id，用于区分不同客户
    app_id: str,           # 飞书开放平台应用的 APP_ID
    app_secret: str,       # 飞书开放平台应用的 APP_SECRET
    xiaoai_token: str,     # 调用小爱接口用的 token（Bearer 后面的部分）
    bitable_url: str,      # 目标飞书多维表视图链接（含 base/app_token 和 table 参数）
    xiaoai_base_url: str = "http://wisers-data-service.wisersone.com.cn",  # 小爱 API 基础域名
) -> int:
    """
    Skill 入口：执行一次从小爱到飞书多维表的增量同步。

    - minutes: 往前补偿的分钟数（基于当前时间）
    - folder_id: 小爱接口的 folder_id
    - customer_id: 小爱接口的 customer_id
    - bitable_url: 目标飞书多维表的完整 URL（包含 base/app_token 和 table 参数）

    返回本次实际写入的记录数。
    """
    # 覆盖全局配置，适配当前调用参数
    m.APP_ID = app_id
    m.APP_SECRET = app_secret
    m.TOKEN = xiaoai_token
    m.BASE_URL = xiaoai_base_url
    m.DEFAULT_FOLDER_ID = folder_id
    m.DEFAULT_CUSTOMER_ID = customer_id
    m.BITABLE_URL = bitable_url

    # 复用原脚本中的 run_once 逻辑
    return m.run_once(minutes)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="XiaoAi -> Feishu Bitable incremental sync (OpenClaw Skill entry)"
    )
    parser.add_argument(
        "--minutes",  # 往前补偿的分钟数
        type=int,
        default=60,
        help="往前补偿的分钟数（默认 60 分钟）",
    )
    parser.add_argument(
        "--folder_id",  # 小爱接口的 folder_id
        type=int,
        required=True,
        help="小爱接口 folder_id",
    )
    parser.add_argument(
        "--customer_id",  # 小爱接口的 customer_id
        type=str,
        required=True,
        help="小爱接口 customer_id",
    )
    parser.add_argument(
        "--app_id",  # 飞书应用 APP_ID
        type=str,
        required=True,
        help="飞书应用 APP_ID",
    )
    parser.add_argument(
        "--app_secret",  # 飞书应用 APP_SECRET
        type=str,
        required=True,
        help="飞书应用 APP_SECRET",
    )
    parser.add_argument(
        "--xiaoai_token",  # 小爱接口 token（Bearer 后面的部分）
        type=str,
        required=True,
        help="小爱接口 token（Bearer 后面的部分）",
    )
    parser.add_argument(
        "--bitable_url",  # 飞书多维表视图链接（含 base/app_token 和 table 参数）
        type=str,
        required=True,
        help="飞书多维表视图链接（包含 base/app_token 和 table 参数）",
    )
    parser.add_argument(
        "--xiaoai_base_url",  # 小爱 API 基础域名（可选）
        type=str,
        default="http://wisers-data-service.wisersone.com.cn",
        help="小爱 API 基础域名（可选，默认 http://wisers-data-service.wisersone.com.cn）",
    )
    # 同步完成后是否执行多维表增量标注（类型（机器）、评价情感（机器））
    parser.add_argument(
        "--run_labeling",
        action="store_true",
        help="同步完成后执行增量标注，标注结果由 OpenClaw 内置大模型通过 stdin 提供",
    )
    parser.add_argument(
        "--labeling_limit",
        type=int,
        default=100,
        help="本次标注最多处理的记录数（默认 100）",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inserted = skill_run_once(
        minutes=args.minutes,
        folder_id=args.folder_id,
        customer_id=args.customer_id,
        app_id=args.app_id,
        app_secret=args.app_secret,
        bitable_url=args.bitable_url,
        xiaoai_token=args.xiaoai_token,
        xiaoai_base_url=args.xiaoai_base_url,
    )
    print(f"inserted_count={inserted}")

    # 同步完成后可选：对多维表做增量标注（由 OpenClaw 内置大模型通过 stdin 提供结果）
    if getattr(args, "run_labeling", False):
        os.environ["BITABLE_URL"] = args.bitable_url
        os.environ["APP_ID"] = args.app_id
        os.environ["APP_SECRET"] = args.app_secret
        os.environ["LIMIT"] = str(args.labeling_limit)
        import bitable_labeling_skill as bl
        bl.BITABLE_URL = args.bitable_url
        bl.APP_ID = args.app_id
        bl.APP_SECRET = args.app_secret
        bl.LIMIT = args.labeling_limit
        updated = bl.run_once()
        print(f"labeling_updated_count={updated}")


if __name__ == "__main__":
    main()

