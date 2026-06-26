#!/usr/bin/env python3
import argparse

from client import print_json, request_json


def main():
    parser = argparse.ArgumentParser(description="查询 OpenClaw 业务任务详情")
    parser.add_argument("--task-id", type=int, required=True)
    parser.add_argument("--sync", action="store_true", help="查询前先向平台同步一次任务状态")
    args = parser.parse_args()

    query = {"sync": "true"} if args.sync else None
    result = request_json("GET", f"/openclaw/tasks/{args.task_id}", query=query)
    print_json(result)


if __name__ == "__main__":
    main()
