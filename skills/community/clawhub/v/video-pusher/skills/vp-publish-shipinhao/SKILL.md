---
name: vp-publish-shipinhao
description: |
  微信视频号发布技能。自动上传视频、填写短标题/描述/标签，等待用户手动点击发表。
  当用户要求发布内容到视频号时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - uv
    emoji: "💚"
    os:
      - darwin
      - linux
      - win32
---

# 微信视频号发布

## 技能边界（强制）

只能通过以下命令发布，不得使用其他工具：

```bash
uv run python skills/vp-publish-shipinhao/publish_shipinhao.py \
  --file <视频路径> \
  --title "短标题" \
  --description "视频描述" \
  --tags "标签1 标签2" \
  --group "账号组名"
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--file` | 是 | 视频文件绝对路径 |
| `--title` | 是 | 短标题，填入"概括视频主要内容"输入框（建议 6-16 字） |
| `--description` | 否 | 视频描述，填入描述文本框 |
| `--tags` | 否 | 标签，空格分隔，自动加 `#` 前缀，追加到描述末尾 |
| `--group` | 是 | 账号组名称，必须已通过 vp-accounts 登录视频号（微信扫码） |

## 前置检查

```bash
uv run python skills/vp-accounts/vp_accounts.py status "A组" shipinhao
# exit 0 = 已登录；exit 1 = 未登录，需先 login（微信扫码）
```

## 发布流程

1. 浏览器打开微信视频号创作平台
2. 自动上传视频
3. 等待短标题输入框出现（视频处理需要时间，最多等 60 秒）
4. 自动填写短标题
5. 自动填写描述和标签
6. **用户检查内容后手动点击【发表】按钮**
7. **关闭浏览器窗口**，脚本自动退出
