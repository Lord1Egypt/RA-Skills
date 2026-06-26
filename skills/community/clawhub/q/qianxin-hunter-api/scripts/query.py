#!/usr/bin/env python3

import os
import sys
import base64
import json
import argparse
import requests


def encode_search(query: str) -> str:
    """符合 RFC 4648 标准的 base64url 编码"""
    return base64.urlsafe_b64encode(query.encode("utf-8")).decode("utf-8").rstrip("=")


class HunterClient:
    def __init__(self):
        self.api_key = os.getenv("QIANXIN_HUNTER_API_KEY")
        if not self.api_key:
            print("错误: 请先设置环境变量 QIANXIN_HUNTER_API_KEY")
            sys.exit(1)
        self.base_url = "https://hunter.qianxin.com/openApi"

    def _request(self, method, endpoint, params=None, data=None, files=None, stream=False):
        url = f"{self.base_url}/{endpoint}"
        full_params = {"api-key": self.api_key}
        if params:
            full_params.update(params)

        try:
            response = requests.request(method, url, params=full_params, data=data, files=files, timeout=30,
                                        stream=stream)
            if stream: return response
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"请求失败 [{endpoint}]: {e}")
            return None

    # 即时查询
    def search(self, args):
        params = {
            "search": encode_search(args.search),
            "page": args.page,
            "page_size": args.page_size,
            "fields": args.fields,
            "is_web": args.is_web,
            "start_time": args.start,
            "end_time": args.end
        }
        res = self._request("GET", "search", params={k: v for k, v in params.items() if v is not None})
        print(json.dumps(res, indent=4, ensure_ascii=False))

    # 提交批量任务
    def batch_submit(self, args):
        params = {
            "is_web": args.is_web,
            "start_time": args.start,
            "end_time": args.end,
            "fields": args.fields,
            "search_type": args.type,
            "assets_limit": args.limit
        }
        files = None
        if args.file:
            files = {'file': open(args.file, 'rb')}
        else:
            params["search"] = encode_search(args.search)

        res = self._request("POST", "search/batch", params={k: v for k, v in params.items() if v is not None},
                            files=files)
        print(json.dumps(res, indent=4, ensure_ascii=False))

    # 查看进度
    def batch_status(self, args):
        res = self._request("GET", f"search/batch/{args.task_id}")
        print(json.dumps(res, indent=4, ensure_ascii=False))

    # 下载文件
    def batch_download(self, args):
        response = self._request("GET", f"search/download/{args.task_id}", stream=True)
        if response and response.status_code == 200:
            filename = args.output or f"results_{args.task_id}.csv"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"文件已保存至: {filename}")
        else:
            print(f"下载失败: {response.text if response else '无响应'}")


def main():
    parser = argparse.ArgumentParser(description="Hunter API Cli")
    subparsers = parser.add_subparsers(dest="command", help="子命令类型")

    # Search 子命令
    p_search = subparsers.add_parser("search", help="即时语法查询")
    p_search.add_argument("--search", required=True, help="搜索语法")
    p_search.add_argument("--page", type=int, default=1)
    p_search.add_argument("--page_size", type=int, default=10)
    p_search.add_argument("--start")
    p_search.add_argument("--end")
    p_search.add_argument("--is_web", type=int)
    p_search.add_argument("--fields")

    # Batch 子命令
    p_batch = subparsers.add_parser("batch", help="批量任务管理")
    p_batch.add_argument("action", choices=["submit", "status", "download"], help="操作类型")
    p_batch.add_argument("--search", help="搜索语法")
    p_batch.add_argument("--file", help="上传的CSV文件路径")
    p_batch.add_argument("--type", choices=["all", "ip", "domain", "company"], default="all", help="上传文件的类型")
    p_batch.add_argument("--start")
    p_batch.add_argument("--end")
    p_batch.add_argument("--is_web", type=int)
    p_batch.add_argument("--limit", type=int, help="导出资产数量限制")
    p_batch.add_argument("--fields")
    p_batch.add_argument("--task_id", help="任务 ID")
    p_batch.add_argument("--output", help="下载保存的文件名")

    args = parser.parse_args()
    client = HunterClient()

    if args.command == "search":
        client.search(args)
    elif args.command == "batch":
        if args.action == "submit":
            client.batch_submit(args)
        elif args.action == "status":
            client.batch_status(args)
        elif args.action == "download":
            client.batch_download(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
