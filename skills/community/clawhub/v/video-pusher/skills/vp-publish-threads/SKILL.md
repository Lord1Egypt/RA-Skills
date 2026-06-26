---
name: vp-publish-threads
description: |
  Threads 发布技能。自动填写文案并可选上传媒体，等待用户手动点击发帖。支持纯文字发布。
  当用户要求发布内容到 Threads 时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - uv
    emoji: "🧵"
    os:
      - darwin
      - linux
      - win32
---

# Threads 发布

## 技能边界（强制）

只能通过以下命令发布，不得使用其他工具：

```bash
# 纯文字发布
uv run python skills/vp-publish-threads/publish_threads.py \
  --title "帖子内容" \
  --group "账号组名"

# 带媒体发布
uv run python skills/vp-publish-threads/publish_threads.py \
  --file <图片或视频路径> \
  --title "帖子内容" \
  --description "补充说明" \
  --tags "标签1 标签2" \
  --group "账号组名"
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--file` | 否 | 图片或视频绝对路径，省略则纯文字发布 |
| `--title` | 是 | 帖子正文开头（Threads 无独立标题字段） |
| `--description` | 否 | 补充正文，追加在 title 后 |
| `--tags` | 否 | 标签，空格分隔，自动加 `#` 前缀 |
| `--group` | 是 | 账号组名称，必须已通过 vp-accounts 登录 Threads |

## 前置检查

```bash
uv run python skills/vp-accounts/vp_accounts.py status "A组" threads
# exit 0 = 已登录；exit 1 = 未登录，需先 login
```

## 发布流程

1. 浏览器打开 threads.com
2. 自动点击【创建】按钮打开发帖对话框
3. 自动填写文案（title + description + tags）
4. 若提供 `--file`，自动上传媒体文件
5. **用户检查内容后手动点击【发帖】按钮**
6. **关闭浏览器窗口**，脚本自动退出
