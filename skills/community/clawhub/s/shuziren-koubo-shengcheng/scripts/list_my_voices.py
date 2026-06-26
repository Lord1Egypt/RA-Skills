#!/usr/bin/env python3
import argparse

from client import print_json, request_json


def main():
    parser = argparse.ArgumentParser(description="获取当前用户的音色列表")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--size", type=int, default=10)
    args = parser.parse_args()

    result = request_json(
        "GET",
        "/openclaw/voices/mine",
        query={"page": args.page, "size": args.size},
    )
    print_json(result)


if __name__ == "__main__":
    main()
