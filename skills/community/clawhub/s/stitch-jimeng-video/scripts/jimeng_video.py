#!/usr/bin/env python3
"""
即梦AI 视频生成3.0 1080P - 火山引擎 API
支持：图生视频-首尾帧
"""

import argparse
import json
import os
import sys
import time
import base64
from pathlib import Path

sys.path.insert(0, os.path.expanduser('~/.local/lib/python3.12/site-packages'))

from volcenginesdkcore.configuration import Configuration
from volcenginesdkcore.api_client import ApiClient
from volcenginesdkcore.universal import UniversalApi, UniversalInfo


def get_client():
    """创建 API 客户端"""
    ak = os.environ.get("VOLC_ACCESS_KEY", "")
    sk = os.environ.get("VOLC_SECRET_KEY", "")
    if not ak or not sk:
        print("错误：请设置环境变量 VOLC_ACCESS_KEY 和 VOLC_SECRET_KEY")
        sys.exit(1)

    conf = Configuration()
    conf.ak = ak
    conf.sk = sk
    conf.region = "cn-north-1"

    api_client = ApiClient(conf)
    return UniversalApi(api_client)


def submit_task(prompt, image_urls, seed=-1):
    """提交视频生成任务"""
    universal = get_client()

    info = UniversalInfo(
        method="POST",
        service="cv",
        version="2022-08-31",
        action="CVSync2AsyncSubmitTask",
        content_type="application/json"
    )

    body = {
        "req_key": "jimeng_i2v_first_tail_v30_1080",
        "prompt": prompt,
        "image_urls": image_urls,
        "seed": seed
    }

    resp = universal.do_call(info, body)
    return resp


def query_task(req_id):
    """查询任务状态"""
    universal = get_client()

    info = UniversalInfo(
        method="POST",
        service="cv",
        version="2022-08-31",
        action="CVSync2AsyncGetResult",
        content_type="application/json"
    )

    body = {
        "req_key": "jimeng_i2v_first_tail_v30_1080",
        "req_id": req_id
    }

    resp = universal.do_call(info, body)
    return resp


def download_video(url, output_path):
    """下载视频到本地"""
    import urllib.request
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    print(f"正在下载视频到 {output_path}...")
    urllib.request.urlretrieve(url, output_path)
    print(f"下载完成: {output_path}")


def upload_image(image_path):
    """将本地图片转为 base64 URL（如果需要的话）"""
    if image_path.startswith(("http://", "https://")):
        return image_path
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{data}"


def main():
    parser = argparse.ArgumentParser(description="即梦AI视频生成3.0 1080P")
    parser.add_argument("--prompt", required=True, help="视频描述")
    parser.add_argument("--first", required=True, help="首帧图片路径/URL")
    parser.add_argument("--last", required=True, help="尾帧图片路径/URL")
    parser.add_argument("--seed", type=int, default=-1, help="随机种子（默认-1随机）")
    parser.add_argument("--output", default=None, help="输出文件路径")
    parser.add_argument("--no-poll", action="store_true", help="只提交不轮询")

    args = parser.parse_args()

    if not args.output:
        workspace = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
        args.output = os.path.join(workspace, "jimeng-video", f"output_{int(time.time())}.mp4")

    # 处理图片
    first_img = upload_image(args.first)
    last_img = upload_image(args.last)

    print(f"描述: {args.prompt}")
    print(f"首帧: {args.first}")
    print(f"尾帧: {args.last}")

    # 提交任务
    try:
        result = submit_task(
            prompt=args.prompt,
            image_urls=[first_img, last_img],
            seed=args.seed
        )
        print("\n任务提交成功！")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        req_id = result.get("data", {}).get("req_id", "")
        if not req_id:
            print("未获取到 req_id")
            return

        print(f"\n任务ID: {req_id}")

        if args.no_poll:
            return

        # 轮询结果
        print("\n等待视频生成...")
        start_time = time.time()
        max_wait = 600  # 10分钟

        while time.time() - start_time < max_wait:
            time.sleep(10)
            try:
                status_result = query_task(req_id)
                status = status_result.get("data", {}).get("status", "")

                if status == "done":
                    video_url = status_result.get("data", {}).get("resp_data", {}).get("video_url", "")
                    if video_url:
                        print(f"\n视频生成完成！")
                        download_video(video_url, args.output)
                    else:
                        print(f"\n任务完成，结果:")
                        print(json.dumps(status_result, indent=2, ensure_ascii=False))
                    return
                elif status in ["failed", "expired"]:
                    print(f"\n任务失败: {status}")
                    print(json.dumps(status_result, indent=2, ensure_ascii=False))
                    return
                else:
                    elapsed = int(time.time() - start_time)
                    print(f"  [{elapsed}s] 状态: {status}")

            except Exception as e:
                print(f"  查询出错: {e}")

        print("\n超时，任务可能仍在处理中")

    except Exception as e:
        err_str = str(e)
        if "HTTP response body:" in err_str:
            body_start = err_str.find("HTTP response body:") + len("HTTP response body:")
            body_end = err_str.find("\n", body_start)
            if body_end == -1:
                body_end = len(err_str)
            response_body = err_str[body_start:body_end].strip()
            print(f"API错误: {response_body}")
        else:
            print(f"错误: {err_str[:500]}")


if __name__ == "__main__":
    main()
