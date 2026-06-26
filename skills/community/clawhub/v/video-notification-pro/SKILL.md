---
name: video_notification_pro
description: 向指定手机号码发送IVVR视频通知，需要传入视频本地路径和手机号
version: 1.0.0
author: system
tags:
  - 视频通知
  - IVVR
  - 通话

input:
  type: object
  required:
    - video_path
    - phone_number
  properties:
    video_path:
      type: string
      description: 视频文件的服务器绝对路径
    phone_number:
      type: string
      description: 11位接收通知的手机号

environment_variables:
  - name: BASE_URL
    description: IVVR平台接口基础地址
    required: true
  - name: APP_ID
    description: IVVR应用ID
    required: true
  - name: ACCESS_KEY
    description: IVVR访问密钥
    required: true
  - name: ACCESS_SECRET
    description: IVVR访问密钥密文
    required: true

execution_function: |
  def execute(video_path: str, phone_number: str) -> dict:
      import os
      import requests
      import hashlib
      import hmac
      import base64
      import time
      from pathlib import Path
      from typing import List, Dict, Optional

      # 从环境变量读取
      BASE_URL = os.getenv("BASE_URL")
      APP_ID = os.getenv("APP_ID")
      ACCESS_KEY = os.getenv("ACCESS_KEY")
      ACCESS_SECRET = os.getenv("ACCESS_SECRET")
      CALLING_NUMBER = "10121000000"          # 固定主叫号码
      MAX_FILE_SIZE = 5 * 1024 * 1024         # 5MB

      # 环境变量检查
      if not all([BASE_URL, APP_ID, ACCESS_KEY, ACCESS_SECRET]):
          return {"success": False, "message": "环境变量未配置完整"}

      # 文件检查
      video_file = Path(video_path)
      if not video_file.is_file():
          return {"success": False, "message": f"视频文件不存在：{video_path}"}
      if video_file.stat().st_size > MAX_FILE_SIZE:
          return {"success": False, "message": "视频大小不能超过5MB"}

      # ========== 签名与请求头 ==========
      def _generate_signature(timestamp: str) -> str:
          origin = f"{APP_ID}\n{ACCESS_KEY}\n{ACCESS_SECRET}\n{timestamp}"
          signature = hmac.new(
              ACCESS_SECRET.encode('utf-8'),
              origin.encode('utf-8'),
              hashlib.sha256
          ).digest()
          return base64.b64encode(signature).decode('utf-8')

      def _get_auth_headers() -> Dict[str, str]:
          timestamp = str(int(time.time() * 1000))
          return {
              "appId": APP_ID,
              "accessKey": ACCESS_KEY,
              "timestamp": timestamp,
              "signature": _generate_signature(timestamp),
          }

      # ========== 上传视频 ==========
      try:
          upload_url = f"{BASE_URL}/file/upload"
          headers = _get_auth_headers()

          with open(video_path, 'rb') as f:
              files = {'uploadFile': (video_file.name, f)}
              upload_resp = requests.post(
                  upload_url,
                  headers=headers,
                  files=files,
                  timeout=60,
                  verify=False
              )

          if upload_resp.status_code != 200:
              return {"success": False, "message": f"上传接口异常，状态码：{upload_resp.status_code}"}

          upload_data = upload_resp.json()
          if upload_data.get("code") != "0000":
              return {"success": False, "message": f"上传失败：{upload_data.get('msg', '未知错误')}"}

          file_id = upload_data.get("data")
          if not file_id:
              return {"success": False, "message": "上传成功但未返回 fileId"}

      except Exception as e:
          return {"success": False, "message": f"上传异常：{str(e)}"}

      # ========== 发送视频通知 ==========
      try:
          send_url = f"{BASE_URL}/notify/invite_play_file"
          headers = _get_auth_headers()
          headers["Content-Type"] = "application/json"

          payload = {
              "callId": f"call_{int(time.time())}",
              "caller_name": "系统通知",
              "caller_number": CALLING_NUMBER,
              "call_type": 2,
              "fileId": file_id,
              "callees": [phone_number]
          }

          send_resp = requests.post(
              send_url,
              headers=headers,
              json=payload,
              timeout=30,
              verify=False
          )

          if send_resp.status_code != 200:
              return {"success": False, "message": f"发送接口异常，状态码：{send_resp.status_code}"}

          send_data = send_resp.json()
          if send_data.get("code") == "0000":
              return {
                  "success": True,
                  "message": "视频通知发送成功",
                  "file_id": file_id,
                  "task_id": None   # 新接口无 taskId，保留字段为 None
              }
          else:
              return {"success": False, "message": f"发送失败：{send_data.get('msg', '未知错误')}"}

      except Exception as e:
          return {"success": False, "message": f"发送异常：{str(e)}"}

examples:
  - user_say: "给 15600766391 发视频通知，视频文件在 /home/hdjs/podcast-video/duan_input_video.mp4"
    parameters:
      video_path: "/home/hdjs/podcast-video/duan_input_video.mp4"
      phone_number: "15600766391"
    response:
      success: true
      message: 视频通知发送成功
---

# 视频通知工具
## 使用方法
直接输入对话：
给 15600766391 发视频通知，视频文件在 /home/hdjs/podcast-video/duan_input_video.mp4

工具会自动解析手机号与视频路径，并发送IVVR视频通知。

## 环境变量要求（必须配置）
- BASE_URL
- APP_ID
- ACCESS_KEY
- ACCESS_SECRET

## 限制
- 视频必须是本地绝对路径
- 大小 ≤ 5MB