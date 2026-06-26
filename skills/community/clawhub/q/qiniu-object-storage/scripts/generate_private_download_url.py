# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json

from common import build_private_download_url, build_public_url, load_config

DEFAULT_OBJECT_KEY = "doubao/example-video.mp4"
DEFAULT_EXPIRES_IN = 600


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成七牛私有下载签名链接")
    parser.add_argument(
        "--key",
        default=DEFAULT_OBJECT_KEY,
        help="对象 key，默认使用当前测试视频",
    )
    parser.add_argument(
        "--expires-in",
        type=int,
        default=DEFAULT_EXPIRES_IN,
        help="有效期秒数，默认 600 秒",
    )
    parser.add_argument(
        "--domain",
        help="下载域名，默认读取环境变量 QINIU_PUBLIC_DOMAIN",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.expires_in <= 0:
        raise ValueError("--expires-in 必须大于 0")

    config = load_config()
    base_url = build_public_url(args.domain or config["public_domain"], args.key)
    private_url = build_private_download_url(
        access_key=config["access_key"],
        secret_key=config["secret_key"],
        base_url=base_url,
        expires_in=args.expires_in,
    )

    print(
        json.dumps(
            {
                "storage_provider": "qiniu",
                "bucket": config["bucket"],
                "object_key": args.key,
                "access_mode": "private",
                "base_url": base_url,
                "private_url": private_url,
                "delivery_url": private_url,
                "expires_in": args.expires_in,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
