---
name: wechat-data-exporter
description: (已验证) 可靠的视频号数据导出器，通过 API 直接获取指定客户的多维度数据报告。
metadata:
  version: 1.0.0
  source: https://github.com/your-repo/wechat-data-exporter
  author: an
  tags: [wechat, data-export, video, marketing]
  license: MIT
  requirements:
    - python
    - "pip:requests"
---

# SKILL.md for wechat-data-exporter

## Description

一个经过实战检验的、可靠的技能，用于从大麦内部系统 (`boss-ip.da-mai.com`) 导出指定客户（视频号）的数据报告。它通过直接调用后端 API 来获取数据，无需任何浏览器自动化，实现了高效、稳定的数据抓取。

该技能已被重构，具备良好的可移植性，所有输出文件都会被安全地保存在 `workspace/data/wechat-data-exporter` 目录下。

## How to Use

当需要为特定客户下载或导出视频号相关的数据时，应调用此技能。它通常作为其他分析类技能（如 `wechat-video-data-analyzer`）的上游依赖被自动调用。

### Input

核心脚本 (`scripts/export.py`) 接受一个命令行参数：

*   **`client_name`** (string): 需要导出数据的客户的完整名称，例如 "峡州国旅"。

### Actions

1.  **动态路径**: 脚本会自动查找 `.openclaw` 的根目录，确保输出路径的正确性。
2.  **URL编码**: 将输入的 `client_name` 进行URL编码，以作为API请求的 `author` 参数。
3.  **API调用 (无签名)**: 脚本会遍历一个预定义的API端点列表，针对短视频、直播、私信等不同数据类型，**仅使用 `author` 参数发起直接的GET请求**。
4.  **文件存储**: 将API返回的数据文件（通常是 `.xlsx` 格式）保存到 `C:\Users\EDY\.openclaw\workspace\data\wechat-data-exporter` 目录中。
5.  **命名规范**: 文件名遵循 `{client_name}-{data_type}-{timestamp}.xlsx` 的格式。
6.  **报告输出**: 所有操作完成后，会生成一个包含所有已下载文件路径的 `.json` 报告，并将其路径以 `REPORT_PATH:` 的标准格式打印出来，供其他工具或上游技能捕获和使用。

### Example Invocation

```powershell
# 直接调用
& "F:\python 3.10\python.exe" "C:\Users\EDY\.openclaw\skills\wechat-data-exporter\scripts\export.py" "峡州国旅"
```
