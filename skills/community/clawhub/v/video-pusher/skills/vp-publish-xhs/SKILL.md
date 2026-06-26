---
name: vp-publish-xhs
description: |
  小红书视频/图片发布技能。自动上传媒体、填写标题/正文/标签，等待用户手动点击发布。
  当用户要求发布内容到小红书时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - uv
    emoji: "📕"
    os:
      - darwin
      - linux
      - win32
---

# 小红书内容发布

## 技能边界（强制）

只能通过以下命令发布，不得使用其他工具：

```bash
uv run python skills/vp-publish-xhs/publish_xhs.py \
  --file <文件路径> \
  --title "标题" \
  --description "正文" \
  --tags "标签1 标签2" \
  --group "账号组名"
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--file` | 是 | 视频或图片绝对路径（mp4/mov/avi/mkv/jpg/png） |
| `--title` | 是 | 笔记标题 |
| `--description` | 否 | 正文内容 |
| `--tags` | 否 | 标签，空格分隔，自动加 `#` 前缀 |
| `--group` | 是 | 账号组名称，必须已通过 vp-accounts 登录小红书 |

## 前置检查

```bash
uv run python skills/vp-accounts/vp_accounts.py status "A组" xhs
# exit 0 = 已登录；exit 1 = 未登录，需先 login
```

## 发布流程

1. 浏览器打开小红书创作者平台
2. 视频文件自动点击【上传视频】切换到视频模式；图片文件直接上传
3. 自动上传文件（等待约 8 秒处理）
4. 自动填写标题、正文、标签（每个标签输入后按 Escape 关闭下拉框，再输入空格使标签生效）
5. **用户检查内容后手动点击【发布】按钮**
6. **关闭浏览器窗口**，脚本自动退出
