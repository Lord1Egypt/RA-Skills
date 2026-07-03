---
name: remote-dispatch
description: "多端协同/Dispatch 远程桌面操控。受 Claude Dispatch 功能启发——手机发指令，电脑执行。将 QQBot 收到的远程指令转化为 desktop actions：截图回传、打开浏览器搜索、操作桌面应用、文件操作。需要 computer-use skill 配合使用。"
metadata:
  openclaw:
    emoji: "📱"
    requires:
      bins: [python3]
---

# Remote Dispatch 📱

> Claude Dispatch 的 OpenClaw 实现。用 QQBot 作为远程输入通道，
> computer-use 作为桌面执行层，实现手机遥控电脑。

## 架构

```
手机(QQ)
   │  发信息
   ▼
QQBot 接收
   │
   ├─→ 普通对话 → 直接回复
   │
   └─→ 远程指令 → Remote Dispatch
          │
          ├─ 📸 screenshot      → 截图 → 图片发回 QQ
          ├─ 🌐 open url        → 打开 URL → 截图回传
          ├─ 🔍 search query    → 打开浏览器搜索 → 截图回传
          ├─ 📋 clipboard       → 读取/写入剪贴板
          ├─ 🪟 window          → 聚焦/最小化/关闭窗口
          └─ 📂 file            → 打开文件/文件夹
```

## 远程指令列表

| 你说 | 执行 | 回传 |
|------|------|------|
| "帮我截个屏" | `screenshot` | 图片 |
| "打开百度搜XX" | `open https://baidu.com` + type | 截图 |
| "帮我打开Chrome" | `open chrome` | 截图 |
| "把剪贴板发给我" | `clipboard` | 文本 |
| "关掉那个窗口" | `window-focus` → `window-close` | 确认 |
| "帮我打开这个文件" | `open C:\path\to\file` | 确认 |
| "看看我现在在干嘛" | `screenshot` | 图片 |
| "帮我复制这段文字" | `clipboard-write` | 确认 |

## 使用方式

### 远程截图
```markdown
[远程] 帮我截个屏
→ 执行 screenshot → 发回图片
```

### 远程搜索
```markdown
[远程] 打开浏览器搜一下"端午节放假安排"
→ 执行 open https://baidu.com → 输入搜索词 → 截图回传
```

### 获取剪贴板
```markdown
[远程] 看看我剪贴板里有什么
→ 执行 clipboard 命令 → 发回文本内容
```

## 实现原理

```python
# dispatch.py 中的指令映射
COMMANDS = {
    "screenshot": "python screen.py screenshot --output /tmp/remote.png",
    "search": "python screen.py open --target https://baidu.com",
    "clipboard": "python screen.py clipboard",
}
```

## 注意事项

- 远程指令需要用户明确授权（不能偷偷操控电脑）
- 关键操作（关窗口、删文件）需要二次确认
- 截图回传注意隐私——只截需要的区域
