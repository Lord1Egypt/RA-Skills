---
name: video_notification
description: 向指定手机号发送视频通知（基于 IVVR 平台）。需要提供服务器上已存在的视频文件绝对路径，文件大小不超过 5MB。
version: 1.1.0
author: hdjs
license: MIT
tags:
  - notification
  - video
  - ivvr
icon: https://example.com/video-icon.png   # 可替换为真实图标 URL

endpoint:
  base_url: "{{API_BASE_URL}}"   # 用户需在环境变量中设置，例如 https://your-domain.com 或 http://xxx.ngrok.io
  path: "/send_video_notice"
  method: POST
  headers:
    Content-Type: application/json
    X-API-Key: "{{API_KEY}}"

input_schema:
  type: object
  required:
    - file_path
    - called_numbers
  properties:
    file_path:
      type: string
      description: 视频文件在服务器上的绝对路径（例如 /home/ubuntu/videos/notice.mp4）
      example: "/home/ubuntu/videos/notice.mp4"
    called_numbers:
      type: array
      description: 接收视频通知的手机号列表（字符串数组）
      items:
        type: string
        pattern: "^1[3-9]\\d{9}$"
      minItems: 1
      example: ["13812345678", "13987654321"]

output_schema:
  type: object
  properties:
    success:
      type: boolean
      description: 是否成功
    file_id:
      type: integer
      description: 平台返回的文件 ID
    msg:
      type: string
      description: 附加信息

examples:
  - title: 发送单个视频通知
    input:
      file_path: "/home/ubuntu/videos/welcome.mp4"
      called_numbers: ["15600766391"]
    output:
      success: true
      file_id: 1364
      msg: "发送完成"
  - title: 批量发送
    input:
      file_path: "/data/videos/alert.mp4"
      called_numbers: ["15600766391", "13912345678"]
    output:
      success: true
      file_id: 1365
      msg: "发送完成"

env_vars:
  - name: API_BASE_URL
    description: 视频通知服务的公网地址（例如 https://your-domain.com 或 http://xxx.ngrok.io），注意不要带尾部斜杠
    required: true
  - name: API_KEY
    description: 服务鉴权所需的 API Key，必须与服务器配置的 SERVICE_API_KEY 一致
    required: true
    secret: true
---

# 视频通知发送技能

该技能调用你部署的 FastAPI 视频通知服务，向指定手机号发送视频通知。

## 前置条件

1. 已部署视频通知服务（代码见 `send_video_api.py`）到一台公网可访问的服务器（或使用 ngrok 临时暴露）。
2. 服务已设置 `SERVICE_API_KEY` 环境变量，并开放 `8867` 端口（或通过 Nginx 代理到公网）。
3. 技能所需的环境变量 `API_BASE_URL` 和 `API_KEY` 已在 ClawHub 中正确配置。

## 使用说明

在对话中提及“发视频通知”或类似关键词，技能会自动提取参数并调用接口。你也可以直接提供 JSON 格式参数。

### 示例对话

- 用户：给 15600766391 发视频通知，视频文件在 `/home/ubuntu/videos/notice.mp4`
- 技能：调用接口，返回发送结果。

## 注意事项

- 视频文件必须**预先存在于服务端**，且服务进程有读取权限。
- 文件大小不得超过 **5 MB**。
- 手机号格式为 11 位数字，以 1 开头。
- 如果服务部署在公网，建议配置 HTTPS 以保证 API Key 安全传输。