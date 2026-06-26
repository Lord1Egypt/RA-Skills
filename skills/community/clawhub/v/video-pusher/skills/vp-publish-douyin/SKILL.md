---
name: vp-publish-douyin
description: |
  抖音视频发布技能。自动上传视频、填写标题/正文/标签，等待用户手动点击发布，发布完毕后提醒用户关闭浏览器。
  当用户要求发布视频到抖音时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - uv
    emoji: "🎵"
    os:
      - darwin
      - linux
      - win32
---

# 抖音视频发布

## 技能边界（强制）

只能通过以下命令发布，不得使用其他工具：

```bash
uv run python skills/vp-publish-douyin/publish_douyin.py \
  --file <视频路径> \
  --title "标题" \
  --description "正文" \
  --tags "标签1 标签2" \
  --group "账号组名"
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--file` | 是 | 视频文件绝对路径（mp4/mov/avi） |
| `--title` | 是 | 视频标题，填入独立标题输入框 |
| `--description` | 否 | 正文内容 |
| `--tags` | 否 | 标签，空格分隔，自动加 `#` 前缀 |
| `--group` | 是 | 账号组名称，必须已通过 vp-accounts 登录抖音 |

## 前置检查

```bash
uv run python skills/vp-accounts/vp_accounts.py status "A组" douyin
# exit 0 = 已登录；exit 1 = 未登录，需先 login
```

## 发布流程

1. 浏览器打开抖音创作者平台
2. 自动上传视频（等待约 8 秒处理）
3. 自动填写标题、正文、标签（每个标签输入后按 Escape 关闭下拉框）
4. **用户检查内容后手动点击【发布】按钮**
5. **关闭浏览器窗口**，脚本自动退出
