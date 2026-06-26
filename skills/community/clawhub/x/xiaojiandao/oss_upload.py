#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSS 上传模块 - 小剪刀skill专用 (QA 环境版)
支持智能路由切换：视频走 bk.srv/upload，音频/图片/字幕走 api/aipkg/upload
"""

import os
import uuid
import requests
import json

# 使用 QA 环境 Base URL 方便排查问题
BASE_URL = "https://biyi.cxtfun.com"

# 路由定义
ROUTE_BK = f"{BASE_URL}/api/aipkg/upload"
ROUTE_AIPKG = f"{BASE_URL}/api/aipkg/upload"

def infer_route_and_usage(file_path: str):
    """根据文件扩展名推断路由和 usage"""
    ext = os.path.splitext(file_path)[1].lower()
    
    video_exts = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi"}
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    audio_exts = {".mp3", ".wav", ".aac", ".m4a"}
    subtitle_exts = {".srt", ".vtt", ".ass", ".ssa"}

    if ext in video_exts:
        # 视频走 bk.srv 路由，根据用户反馈，usage 需改为 temp_audio
        return ROUTE_BK, "temp_audio"
    if ext in image_exts:
        # 图片帧走 aipkg 路由，usage 为 seven_day_temp_img
        return ROUTE_AIPKG, "seven_day_temp_img"
    if ext in audio_exts:
        # 音频走 aipkg 路由，usage 为 temp_audio
        return ROUTE_AIPKG, "temp_audio"
    if ext in subtitle_exts:
        # 字幕使用 three_month_log
        return ROUTE_AIPKG, "three_month_log"
    
    # 默认保底
    return ROUTE_BK, "file"

def oss_upload(file_path: str, usage: str = None, timeout: int = 300) -> dict:
    """
    上传文件到 OSS (QA环境)
    """
    if not os.path.isfile(file_path):
        return {"success": False, "error": f"File not found: {file_path}"}

    # 自动推断路由和 usage (除非手动指定 usage)
    target_url, inferred_usage = infer_route_and_usage(file_path)
    final_usage = usage or inferred_usage
    
    filename = os.path.basename(file_path)
    
    # 构建 multipart 表单
    try:
        with open(file_path, "rb") as f:
            files = {
                "files": (filename, f),
            }
            data = {
                "usage": final_usage
            }
            
            print(f"DEBUG: Uploading to {target_url} with usage={final_usage}...")
            resp = requests.post(target_url, files=files, data=data, timeout=timeout)
            resp.raise_for_status()
            resp_json = resp.json()
            
            # 解析成功逻辑 (err_code 为 0 或 -1 均视为成功)
            err_code = resp_json.get("err_code") or resp_json.get("code")
            if err_code in [0, -1]:
                url, oss_path = _extract_result(resp_json)
                if url:
                    return {
                        "success": True,
                        "url": url,
                        "oss_path": oss_path,
                        "usage": final_usage,
                        "route": target_url,
                        "raw": resp_json
                    }
            
            return {
                "success": False,
                "error": resp_json.get("msg") or resp_json.get("message") or "Unknown error",
                "raw": resp_json
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def _extract_result(resp_json: dict):
    """对齐文档的提取逻辑，并确保 URL 是带协议头的完整地址"""
    data = resp_json.get("data")
    url, oss_path = "", ""
    
    # 尝试从各种位置提取
    items_to_check = []
    if isinstance(data, list) and len(data) > 0:
        items_to_check.append(data[0])
    elif isinstance(data, dict):
        items_to_check.append(data)
    items_to_check.append(resp_json) # 根节点作为保底

    # 1. 尝试直接获取带 http 的 URL
    for item in items_to_check:
        tmp_url = item.get("url")
        if tmp_url and isinstance(tmp_url, str) and tmp_url.startswith("http"):
            url = tmp_url
            oss_path = item.get("oss_path") or item.get("path")
            break
        
    # 2. 如果后端只返回了路径（不带 http），则手动拼上 Base URL
    if not url:
        for item in items_to_check:
            tmp_url = item.get("url")
            if tmp_url and isinstance(tmp_url, str):
                # 拼接完整 URL
                url = f"{BASE_URL.rstrip('/')}/{tmp_url.lstrip('/')}"
                oss_path = item.get("oss_path") or item.get("path")
                break
        
    return url, oss_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--usage", default=None)
    args = parser.parse_args()
    
    result = oss_upload(args.file, usage=args.usage)
    print(json.dumps(result, ensure_ascii=False, indent=2))
