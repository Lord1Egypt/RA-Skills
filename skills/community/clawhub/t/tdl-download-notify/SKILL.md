---
name: tdl-download-notify
description: TDL 下载完成后自动通过 Server 酱微信通知，包含文件名和大小信息
read_when:
  - 使用 tdl 下载 Telegram 资源
  - 需要下载完成后微信通知
  - 长时间下载任务监控
metadata: {"emoji":"📥","requires":{"python":["requests"],"bins":["tdl"]}}
allowed-tools: Bash(tdl_download_notify.py), Python(tdl_download_notify.py)
---

# TDL 下载 + Server 酱通知

下载 Telegram 资源后自动通过 Server 酱发送微信通知，包含详细的文件信息。

## 配置

### 前置条件

1. **TDL 已安装并登录**
   ```bash
   tdl --version
   tdl login
   ```

2. **Server 酱已配置**
   - SendKey: `sctp6765tcomfljakjcquc4e7mdaman`
   - 微信已关注 Server 酱公众号

### 默认下载目录

`/root/tdl_download`

可通过参数自定义。

## 使用方法

### 方式 1：命令行调用

```bash
# 基本用法
python3 /root/openclaw/Data/OpenClaw/skills/tdl-download-notify/tdl_download_notify.py <chat_id> <message_id>

# 指定下载目录
python3 .../tdl_download_notify.py 1340124720 126326 /root/downloads

# 示例：下载 Telegram 频道的某个消息
python3 tdl_download_notify.py 1340124720 126326
```

### 方式 2：在 OpenClaw 中使用

直接告诉我：
> "下载这个 Telegram 链接并通知我：https://t.me/c/1340124720/126326"

我会自动执行下载并发送微信通知。

## 通知内容

### ✅ 下载成功

```
✅ 下载完成

📥 来源：https://t.me/c/1340124720/126326
📁 目录：/root/tdl_download
📊 数量：2 个文件
💾 总大小：1.23 GB

文件列表:

📄 视频文件.mp4
   大小：800.50 MB
   时间：2026-03-18 00:15:30

📄 图片.jpg
   大小：2.35 MB
   时间：2026-03-18 00:15:32

⏱️ 耗时：2 分 15 秒
🕐 完成时间：2026-03-18 00:15:32
```

### ❌ 下载失败

```
❌ 下载失败

📥 来源：https://t.me/c/1340124720/126326
❌ 错误：message not found

⏱️ 耗时：0 分 5 秒
🕐 失败时间：2026-03-18 00:15:32
```

## 参数说明

| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `chat_id` | string | ✅ | Telegram 聊天 ID |
| `message_id` | string | ✅ | Telegram 消息 ID |
| `output_dir` | string | ❌ | 下载目录（默认：/root/tdl_download） |

## 功能特性

✅ **自动通知** - 下载完成后自动发送微信  
✅ **文件信息** - 包含文件名、大小、修改时间  
✅ **多文件支持** - 自动检测所有新下载的文件  
✅ **失败通知** - 下载失败也会通知  
✅ **耗时统计** - 显示下载耗时  
✅ **智能检测** - 自动对比下载前后的文件列表  

## 相关文件

- **脚本路径**: `/root/openclaw/Data/OpenClaw/skills/tdl-download-notify/tdl_download_notify.py`
- **Server 酱配置**: `/root/openclaw/Data/OpenClaw/skills/serverchan/serverchan.py`
- **默认下载目录**: `/root/tdl_download`

## 相关链接

- [TDL 官方文档](https://github.com/iyear/tdl)
- [Server 酱官网](https://sct.ftqq.com/)
