#!/usr/bin/env python3
import argparse

from client import print_json, request_json


def main():
    parser = argparse.ArgumentParser(description="获取公共音色列表")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--size", type=int, default=10)
    parser.add_argument("--source", choices=["platform", "relay"], default="platform")
    args = parser.parse_args()

    result = request_json(
        "GET",
        "/openclaw/public-voices",
        query={"page": args.page, "size": args.size, "source": args.source},
    )
    print_json(result)


if __name__ == "__main__":
    main()
