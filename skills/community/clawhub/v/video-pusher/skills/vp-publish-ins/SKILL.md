---
name: vp-publish-ins
description: |
  Instagram 发布技能。自动上传图片/视频，经过多步骤流程（裁剪→滤镜→Caption）后等待用户手动点击分享。
  当用户要求发布内容到 Instagram 时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - uv
    emoji: "📸"
    os:
      - darwin
      - linux
      - win32
---

# Instagram 发布

## 技能边界（强制）

只能通过以下命令发布，不得使用其他工具：

```bash
uv run python skills/vp-publish-ins/publish_ins.py \
  --file <图片或视频路径> \
  --title "Caption 内容" \
  --description "补充说明" \
  --tags "标签1 标签2" \
  --group "账号组名"
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `--file` | 否 | 图片或视频绝对路径 |
| `--title` | 是 | Caption 开头文字（Instagram 无独立标题字段） |
| `--description` | 否 | 补充 Caption 内容 |
| `--tags` | 否 | 标签，空格分隔，自动加 `#` 前缀 |
| `--group` | 是 | 账号组名称，必须已通过 vp-accounts 登录 Instagram |

## 前置检查

```bash
uv run python skills/vp-accounts/vp_accounts.py status "A组" ins
# exit 0 = 已登录；exit 1 = 未登录，需先 login
```

## 发布流程

1. 浏览器打开 Instagram 主页
2. 自动点击【新帖子】(aria-label="新帖子") 按钮
3. 若提供 `--file`，自动上传文件
4. 脚本自动点击【下一步】完成裁剪和滤镜步骤
5. 在 Caption 页自动填写文案（title + description + tags）
6. **用户检查内容后手动点击【分享】按钮**
7. **关闭浏览器窗口**，脚本自动退出
