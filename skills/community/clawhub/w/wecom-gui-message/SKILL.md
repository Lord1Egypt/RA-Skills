---
name: wecom-gui-message
description: 通过 macOS GUI 自动化给企业微信（WeCom）联系人或群发消息。使用 peekaboo + screencapture + Swift Vision OCR + cliclick 实现全流程自动化。适用于需要通过企业微信桌面端发送消息的场景，如推送日报、通知等。触发词：企微发消息、企业微信发消息、wecom message、给某人发企微消息。
---

# 企业微信 GUI 自动化发消息

通过 macOS 桌面 GUI 自动化，在企业微信中找到联系人/群聊并发送消息。

## 前置条件

- macOS（arm64, Retina 2x）
- 企业微信桌面客户端已安装（`com.tencent.WeWorkMac`）
- 已安装：peekaboo, cliclick, swift
- 系统已授权：Screen Recording + Accessibility

## 快速使用

```bash
python3 scripts/send_message.py "联系人或群名" "消息内容"
python3 scripts/send_message.py "XXX" "今日AI日报\nhttps://example.com" --wait-login
```

| 参数 | 说明 |
|------|------|
| `--wait-login` | 需登录时自动轮询等待扫码 |
| `--timeout N` | 登录等待超时秒数（默认 120） |

| Exit Code | 含义 |
|-----------|------|
| 0 | 发送成功 |
| 1 | 发送失败 |
| 2 | 需要登录（仅非 --wait-login） |

## 架构与核心流程

```
激活企微 → 调整窗口 → 登录检测 → 等待弹窗消失 → 消息列表OCR查找 → 点击目标 → 关闭侧面板 → 点击输入框 → 粘贴 → 回车发送 → 验证
```

## 关键经验（4/24 实测踩坑总结）

### 1. 截图策略：窗口截图 > 全屏截图

```python
# ✅ 正确：用 screencapture -l <window_id> 截取企微窗口
screencapture -x -l 7741 /tmp/capture.png

# ❌ 错误：全屏截图在企微非前置时 OCR 返回 0 结果
screencapture -x /tmp/capture.png
```

**原因**：`screencapture -x` 全屏截图可能截到桌面/其他窗口，OCR 结果为空。窗口截图始终只截企微内容。

### 2. 坐标换算：窗口坐标 ≠ 屏幕坐标

```python
# 窗口截图 OCR 返回窗口内坐标
# cliclick 需要屏幕坐标
# 换算公式：
screen_x = window_position_x + ocr_pixel_x / 2
screen_y = window_position_y + ocr_pixel_y / 2

# 获取窗口位置：
peekaboo window list --app "com.tencent.WeWorkMac" --json
# → bounds: {x: 0, y: 33, width: 1400, height: 883}
```

**忘记加偏移 = 点到错误位置，这是最常见的 bug！**

### 3. 搜索方式：消息列表 OCR > Cmd+F

- ❌ Cmd+F 全局搜索对外部微信联系人返回"无搜索结果"
- ✅ 切到「消息」Tab，在消息列表中 OCR 直接找目标名并点击
- 前提：目标必须在最近消息列表中（先手动发一条建立聊天记录）

### 4. 输入框定位：坐标估算

- 企微输入框无 placeholder 文字，OCR 找不到
- 输入框位置 = 窗口底部约 93% 处（工具栏 emoji/文件图标下方）
- 粘贴前先 Cmd+A → Delete 清空残留内容

### 5. 右侧面板处理

- 企微可能弹出"智能服务总结 AI+"等侧边面板
- 面板会挤压聊天区域、遮挡输入框
- 发消息前检测并按 Escape 关闭

### 6. 系统通知弹窗

- 首次启动弹出"App后台活动"和"通知"权限弹窗
- **不要点击弹窗按钮**（会打开系统设置遮挡企微）
- 点击企微窗口区域让弹窗自动消失

### 7. 中文输入

只用 `peekaboo paste --text --app bundleId`，不用 cliclick 打字。

### 8. bundleId

始终使用 `com.tencent.WeWorkMac`。

## 工具链

| 工具 | 用途 |
|------|------|
| peekaboo | paste 中文、hotkey、press、window focus/list |
| screencapture -l | 窗口截图（必须用 -l 指定窗口） |
| Swift Vision OCR | 文字识别 + 像素坐标（`scripts/ocr_screen.swift`） |
| cliclick | 屏幕坐标点击 |
| osascript | 窗口管理、App 激活/窗口调整 |
