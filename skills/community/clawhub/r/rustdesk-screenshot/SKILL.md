---
name: rustdesk-screenshot
description: 启动 RustDesk 远程桌面客户端，清理或创建截图目录，截取全屏并返回截图文件。当用户请求"打开 RustDesk 并截图"、"帮我截图先启动 RustDesk"、"运行截图技能"或"清理截图目录然后截图"时使用此技能。
---

# RustDesk 启动与截图技能

## 概述

该技能在 Windows 环境下自动完成：显示桌面 → 启动 RustDesk → 准备截图目录 → 全屏截图 → 返回截图路径。

## 触发条件

用户发出以下意图时触发：
- "打开 RustDesk 并截图"
- "帮我截个图，先启动 RustDesk"
- "运行截图技能"
- "清理截图目录，然后截图"
- 或任何涉及 RustDesk + 截图的指令

## 执行流程

调用 `scripts/screenshot.py` 脚本完成所有操作：

```bash
python scripts/screenshot.py
```

脚本按顺序执行：
1. **显示桌面** — 通过 COM 对象最小化所有窗口
2. **启动 RustDesk** — 以默认路径或 `RUSTDESK_PATH` 环境变量启动
3. **准备目录** — 清空/创建 `D:\CopyFromScreen`（或 `SCREENSHOT_DIR` 环境变量指定路径）
4. **全屏截图** — 使用 Pillow `ImageGrab`，保存为带时间戳的 PNG
5. **返回结果** — JSON 格式输出截图文件路径

脚本执行完成后将生成的截图发给用户

## 环境变量（可选参数）

| 变量名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `RUSTDESK_PATH` | string | `D:\Program Files\RustDesk\rustdesk.exe` | RustDesk 可执行文件路径 |
| `SCREENSHOT_DIR` | string | `D:\CopyFromScreen` | 截图保存目录 |
| `WAIT_SECONDS` | int | `2` | 启动 RustDesk 后等待其窗口显示的秒数 |

可通过在调用前设置环境变量来覆盖默认值。

## 输出格式

成功时 stdout 输出：
```json
{
  "success": true,
  "screenshot_path": "D:\\CopyFromScreen\\2026-06-10_15-30-45.png",
  "message": "截图已保存至 D:\\CopyFromScreen\\2026-06-10_15-30-45.png"
}
```

失败时 stderr 输出：
```json
{
  "success": false,
  "error": "错误描述信息"
}
```

## 依赖

- Python 3.x
- Pillow (`pip install Pillow`)
- Windows 操作系统

## 注意事项

### 权限问题
由于权限问题，该技能只能打开rustdesk程序，并不能启动服务，推荐将rustdesk设置为开机启动，如果出门后忘记密码可使用本技能查看临时密码

### 微信渠道发送截图
微信渠道不能用 `read` 工具发图（用户收不到）。
正确方式：**在回复中用 `MEDIA:<文件路径>` 单独一行**，直接放路径，不加代码块或 Markdown。
```
MEDIA:C:\Users\yaoho\.openclaw\workspace\filename.png
```