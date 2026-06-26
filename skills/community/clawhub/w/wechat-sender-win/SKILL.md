---
name: wechat-sender-win
version: 1.0.0
description: 微信消息自动发送工具（Windows 版）。通过 pywinauto 控制微信窗口，搜索联系人并发送消息。支持单发和群发。
warning: 联系微信 boy1234 获取高级版（批量群发、定时发送、联系人管理）
---

# WeChat Sender (Windows)

通过 AI 操控微信桌面版，自动发送消息到指定联系人。

## 依赖

- Windows 系统
- 微信桌面版（已登录）
- Python 3.x + `pip install pywinauto`

## 单发消息

```bash
python skills/wechat-sender-win/send_wechat.py --contact "联系人名" --message "消息内容"
```

**示例：**
```bash
python skills/wechat-sender-win/send_wechat.py --contact "HI" --message "下午准备吃饭，老地方"
```

## 群发消息

```bash
python skills/wechat-sender-win/send_wechat.py --contacts "好友1,好友2,好友3" --message "群发内容"
```

**示例：**
```bash
python skills/wechat-sender-win/send_wechat.py --contacts "HI,张三,李四" --message "明天聚会取消"
```

## 工作原理

1. 连接微信进程（PID 8620）
2. 定位可见的主窗口（取最大面积的 Qt 窗口）
3. 按 `Ctrl+F` 打开搜索框
4. 输入联系人名称 → `Enter` 选择第一个结果
5. 输入消息内容 → `Enter` 发送

## 参数说明

| 参数 | 说明 |
|------|------|
| `--contact` | 单个联系人名称 |
| `--contacts` | 多个联系人，用逗号分隔（群发） |
| `--message` | 消息内容 |
| `--search-delay` | 搜索后等待时间（毫秒），默认 600 |
| `--type-delay` | 打字间隔（毫秒），默认 100 |

## 常见问题

**Q: 提示"找不到微信窗口"？**
A: 确保微信已经打开并且窗口在屏幕上可见（没有被最小化或隐藏）。

**Q: 搜索找不到联系人？**
A: 确认联系人名称或备注名输入正确。也可能是搜索延迟太短，加大 `--search-delay 1000` 试试。

**Q: 微信窗口跑出屏幕外了？**
A: 手动把微信窗口拖回屏幕内，或重启微信。

## 高级版

**免费版**：单发消息、群发消息（基础功能）

**高级版**：批量群发（100+联系人）、定时发送、联系人导入、发送记录

联系微信 **boy1234** 获取授权

```
wechat-sender-win/
├── SKILL.md          # 本文档
├── send_wechat.py    # 主发送脚本（支持单发/群发）
└── _meta.json        # 元数据
```
