---
name: wechat-skill
version: 1.0.0
description: Windows 电脑端微信消息发送 MCP，实现在微信上给指定联系人发送消息
metadata: {"openclaw": {"requires": {"bins": ["python"]}, "os": ["win32"]}, "trigger": "当用户明确提到用微信发送消息、或回复微信消息时触发，不要和其他通信工具混淆了"}
---

# WeChat Skill

Windows 电脑端微信消息发送 MCP。

基于 [wechat-mcp](https://clawhub.ai/dragon015/wechat-mcp) 增强优化，感谢原始作者！

**重要：本技能仅在用户明确要求通过微信发送消息时使用，不要与其他通信工具混淆。**

## 触发条件

当用户明确要求通过**微信**发送消息时使用，例如：
- ✅ "给李永辉发微信"
- ✅ "用微信发给文件传输助手：测试"
- ✅ "在微信上发送你好"
- ✅ "微信消息：周末加班"

**禁止在以下场景使用（会混淆）：**
- ❌ 飞书消息
- ❌ 钉钉消息  
- ❌ QQ 消息
- ❌ 短信
- ❌ 邮件

如果用户没有指定平台，只是说"发消息"，请先询问用户要使用哪个平台。

## 功能

- 📸 截取微信窗口截图
- 👤 搜索并打开联系人聊天窗口
- ✉️ 给指定联系人发送消息
- 🔍 支持独立聊天窗口识别和消息发送

## 安装

需要先安装 Python 依赖：

```bash
pip install pyautogui pygetwindow pillow pyperclip opencv-python
```

## 使用方法

当我（AI）帮你发送微信消息时，我会通过 exec 工具调用这个 Python 脚本。

### 发送消息流程

1. **告诉我**你想发给谁和什么内容，比如：
   - "给李永辉发送你好啊"
   - "发消息给文件传输助手：测试一下"

2. **我会搜索**并显示搜索结果截图

3. **如果有多个同名联系人**，会让你选择：
   - 显示搜索结果截图
   - 问你"有X个同名联系人，请选择：1. 张三 2. 张三(企业微信)"

4. **你确认后**，我再执行发送

### 两种发送方式

1. **自动搜索发送**（需要确认）
   - 我会搜索联系人并打开聊天窗口
   - 发送前会给你确认

2. **当前窗口发送**（仅限已打开的聊天）
   - 适用于你已经打开某个联系人的聊天窗口
   - 同样会在发送前确认

### 手动调用

如果你想自己运行，可以直接执行：

```bash
python C:\Users\toby\.openclaw\workspace\skills\wechat-mcp\server.py
```

但更简单的方式是让我帮你发送消息！

## 依赖

需要安装 Python 依赖（已安装）：
- pyautogui
- pygetwindow
- pillow
- pyperclip
- opencv-python

## MCP 工具

如果通过 MCP 协议调用：

```json
{
  "tools": [
    {
      "name": "wechat_get_status",
      "description": "获取微信窗口状态"
    },
    {
      "name": "wechat_send_message",
      "description": "给当前聊天窗口发送消息",
      "inputSchema": {
        "type": "object",
        "properties": {
          "message": {"type": "string", "description": "消息内容"}
        },
        "required": ["message"]
      }
    }
  ]
}
```

## 注意事项

1. 微信窗口需要保持打开状态
2. 发送消息时会自动激活微信窗口
3. 中文输入需要确保系统中文输入法正常工作
4. 支持给独立聊天窗口（单独打开的 Dragon 窗口）发送消息

## 文件结构

```
wechat-mcp/
├── server.py          # MCP 服务器主程序
├── test_wechat.py    # 测试工具
├── requirements.txt   # Python 依赖
└── README.md         # 说明文档
```
