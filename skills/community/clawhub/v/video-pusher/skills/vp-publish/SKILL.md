---
name: vp-publish
description: |
  多平台一键发布编排技能。检查各平台登录状态，依次调用平台发布脚本完成发布。
  当用户要求同时发布到多个平台、或一键发布时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - uv
    emoji: "📤"
    os:
      - darwin
      - linux
      - win32
---

# 多平台一键发布

## 技能边界（强制）

通过调用各平台子技能完成发布，所有命令均使用 `uv run python`，工作目录为项目根目录。

## 使用方式

告诉 Claude：
> "发布 /path/to/video.mp4 到抖音和小红书，使用 A组 账号，标题是 xxx，正文是 yyy，标签是 医美 玻尿酸"

Claude 会：
1. 确认发布参数（文件、标题、正文、标签、账号组、目标平台）
2. 检查各平台登录状态，未登录则询问是先登录还是跳过
3. 依次为每个平台启动浏览器完成发布
4. 汇报所有平台发布结果

## 工作流程

### 第一步：确认参数

发布前必须明确以下参数：
- 视频/图片文件绝对路径
- 标题（必填）
- 正文（选填）
- 标签（选填，空格分隔）
- 账号组名称
- 目标平台列表

### 第二步：检查登录状态

```bash
uv run python skills/vp-accounts/vp_accounts.py status "A组" douyin
# exit 0 = 已登录，继续；exit 1 = 未登录，询问用户
```

对每个目标平台执行此检查。未登录时询问用户：跳过该平台，还是先登录。

### 第三步：依次发布

每个平台启动浏览器后，**等待用户在浏览器完成发布并关闭浏览器窗口**，再启动下一个平台。

```bash
uv run python skills/vp-publish-douyin/publish_douyin.py \
  --file <path> --title <title> --description <desc> \
  --tags "<tags>" --group "<group>"
```

## 支持平台

| 平台 | platform 值 | 文件必填 | 说明 |
|------|-------------|---------|------|
| 抖音 | `douyin` | 是 | 视频 mp4/mov/avi |
| 小红书 | `xhs` | 是 | 视频或图片 |
| 视频号 | `shipinhao` | 是 | 视频，需微信扫码登录 |
| Threads | `threads` | 否 | 支持纯文字 |
| Instagram | `ins` | 否 | 多步骤流程 |

## 安装（首次）

```bash
uv sync
uv run playwright install chromium
```
