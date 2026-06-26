#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字幕识别模块 - 步骤6实现 (云端优化版)
云端抽帧 → 火山OCR识别 → 字幕位置计算
"""

import os
import sys
import json
import time

# 复用同目录下的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from client import HookHttpClient
from bridge import MScissorsBridge


# ============ 通用配置 ============

BASE_URL = "https://biyi.cxtfun.com"
PKGNAME = "com.biyi.mscissors"
OCR_SUBMIT_ENDPOINT = "/api/aipkg/submit/volcano.ocr"
OCR_QUERY_ENDPOINT = "/api/aipkg/query/volcano.ocr.result"
POS_CALC_ENDPOINT = "/api/aipkg/calc/subtitle.pos.by.ocr"


# ============ 1. 提交OCR任务 ============

def submit_ocr(client: HookHttpClient, task_id: int, frame_urls: list[str]) -> str:
    """提交火山OCR识别任务"""
    payload = {
        "task_id": task_id,
        "data_type": "url",
        "scene": "general",
        "data_list": frame_urls,
    }
    result = client.post(OCR_SUBMIT_ENDPOINT, payload)

    if result.get("err_code") != -1:
        raise RuntimeError(f"OCR提交失败: {result.get('err_message', result)}")

    client_id = result.get("data", {}).get("client_id")
    if not client_id:
        raise RuntimeError(f"OCR提交响应缺少client_id: {result}")

    print(f"[字幕识别] OCR任务提交成功，client_id={client_id}")
    return client_id


# ============ 2. 轮询OCR结果 ============

def poll_ocr_result(client: HookHttpClient, client_id: str, timeout: int = 300) -> list:
    """轮询火山OCR结果"""
    endpoint = OCR_QUERY_ENDPOINT
    start_time = time.time()
    interval = 5

    while True:
        elapsed = time.time() - start_time
        if elapsed >= timeout:
            raise TimeoutError(f"OCR轮询超时（{timeout}s），client_id={client_id}")

        result = client.post(endpoint, {"client_id": client_id})
        if result.get("err_code") != -1:
            raise RuntimeError(f"OCR查询失败: {result.get('err_message', result)}")

        data = result.get("data", {})
        state = data.get("state")

        if state == 2:
            results = data.get("results", [])
            print(f"[字幕识别] OCR识别完成，共 {len(results)} 帧")
            return results
        elif state == 3:
            raise RuntimeError(f"OCR识别失败，state=3: {data}")
        else:
            print(f"[字幕识别] OCR识别中... state={state}，已等待 {int(elapsed)}s")
            time.sleep(interval)


# ============ 3. 解析OCR结果 ============

def parse_ocr_boxes(results: list) -> list[dict]:
    """解析 OCR 返回的 results，提取字幕文字和位置"""
    boxes = []
    for frame_idx, item in enumerate(results):
        for text_info in item.get("general_result", []):
            content = text_info.get("content", "").strip()
            conf = float(text_info.get("confidence", 0))
            loc = text_info.get("location", [])

            if not content or conf < 0.5 or len(loc) < 4:
                continue

            x1, y1 = loc[0]
            x2, y2 = loc[2]
            boxes.append({
                "frame_num": frame_idx,
                "text": content,
                "x1": int(x1),
                "y1": int(y1),
                "x2": int(x2),
                "y2": int(y2),
                "cy": (y1 + y2) // 2,
                "conf": conf,
            })
    return boxes


# ============ 4. 字幕位置计算 ============

def calc_subtitle_position(client: HookHttpClient, ocr_results: list,
                           video_width: int = 1080, video_height: int = 1920) -> dict:
    """调用字幕位置精确计算接口"""
    payload = {
        "results": ocr_results,
        "video_width": video_width,
        "video_height": video_height,
    }
    result = client.post(POS_CALC_ENDPOINT, payload)

    if result.get("err_code") != -1:
        raise RuntimeError(f"字幕位置计算失败: {result.get('err_message', result)}")

    pos = result.get("data", {})
    return {
        "x": int(pos.get("x", 0)),
        "y": int(pos.get("y", 0)),
        "w": int(pos.get("w", 0)),
        "h": int(pos.get("h", 0)),
    }


# ============ 5. 主流程 (云端优化版) ============

def recognize_subtitle(video_url: str, biyi_token: str,
                      task_id: int = 0,
                      num_frames: int = 15,
                      ocr_timeout: int = 300) -> dict:
    """字幕识别完整流程 (已移除本地 ffmpeg/ffprobe 依赖)"""
    print(f"[字幕识别] 开始云端处理视频: {video_url}")

    try:
        # Step 1: 云端抽帧
        bridge = MScissorsBridge(biyi_token)
        frame_res = bridge.extract_frames(video_url, count=num_frames)
        if not frame_res.get("success"):
            raise RuntimeError(f"云端抽帧失败: {frame_res.get('error')}")
        
        frame_urls = frame_res["frames"]
        print(f"[字幕识别] 云端抽帧完成，共 {len(frame_urls)} 张")

        # Step 2: 初始化 HTTP 客户端
        client = HookHttpClient(
            base_url=BASE_URL,
            pkgname=PKGNAME,
            appsecret=biyi_token,
        )

        # Step 3: 提交 OCR 任务
        client_id = submit_ocr(client, task_id, frame_urls)

        # Step 4: 轮询 OCR 结果
        ocr_results = poll_ocr_result(client, client_id, timeout=ocr_timeout)

        # Step 5: 解析 OCR 框
        boxes = parse_ocr_boxes(ocr_results)

        # Step 6: 计算字幕位置 (宽高将在最终合成接口时由云端自动处理，此处默认 1080x1920 比例)
        # 如果需要精确的宽高，后续分析接口 analyze 也会返回
        position = {}
        if boxes:
            position = calc_subtitle_position(client, ocr_results)
            print(f"[字幕识别] 字幕位置计算完成: {position}")
        else:
            print("[字幕识别] 未识别到字幕")

        return {
            "success": True,
            "boxes": boxes,
            "position": position,
            "frame_urls": frame_urls,
            "error": None,
        }

    except Exception as e:
        print(f"[字幕识别] 错误: {e}", file=sys.stderr)
        return {
            "success": False,
            "boxes": [],
            "position": {},
            "frame_urls": [],
            "error": str(e),
        }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="字幕识别 - 云端优化版")
    parser.add_argument("--url", required=True, help="视频 URL")
    parser.add_argument("--token", required=True, help="用户 Token")
    parser.add_argument("--task-id", type=int, default=0, help="任务 ID")
    parser.add_argument("--frames", type=int, default=15, help="抽帧数量")
    args = parser.parse_args()

    result = recognize_subtitle(
        video_url=args.url,
        biyi_token=args.token,
        task_id=args.task_id,
        num_frames=args.frames
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
