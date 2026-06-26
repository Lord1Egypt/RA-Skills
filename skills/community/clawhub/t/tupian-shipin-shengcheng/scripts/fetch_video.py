#!/usr/bin/env python3
import argparse
import sys

from client import ConfigError, print_json, request_json


def build_parser():
    parser = argparse.ArgumentParser(description="Fetch a VEO, Banana, or Sora task result through the platform API.")
    parser.add_argument("--task-id", required=True, help="Task id returned by the generate endpoint.")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        payload = request_json("GET", f"/veo2/custom_video/fetch/{args.task_id}")
        print_json(payload)
        return 0
    except (ConfigError, RuntimeError) as exc:
        sys.stderr.write(f"{exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
