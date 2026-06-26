---
name: wechat-send
description: Use when 需要在 macOS 上自动给微信联系人发送消息，且要通过剪贴板粘贴规避中文输入法干扰。
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - osascript
        - pbpaste
        - pbcopy
---

# WeChat Send

## 概览

这个 skill 用来在 macOS 桌面版微信里发送消息，优先走稳定的 UI 自动化顺序：

1. 激活 WeChat 并确认它是前台应用
2. 用快捷键打开搜索或切换会话
3. 联系人名和消息正文都通过剪贴板粘贴，避免输入法拦截

## 何时使用

- 用户明确要求在 macOS 微信客户端给联系人发消息
- 直接键入中文容易被输入法干扰，必须改用剪贴板粘贴

不要在这些场景优先使用这个 skill：

- 用户只是要发网页微信消息
- 目标环境不是 macOS 桌面

## 前置依赖

- macOS 已安装并登录 WeChat
- 运行环境已授予 Accessibility 权限

## 标准工作流

### 1. 先做依赖体检

```bash
python3 scripts/wechat_auto.py doctor
```

这个检查会确认：

- `WeChat` 是否可启动
- `osascript`、`pbcopy`、`pbpaste` 是否可用

任一必需项缺失时，命令会输出错误并以非 0 退出。

### 2. 直接发送消息

从 skill 根目录执行：

```bash
scripts/send_message "文件传输助手" "测试消息"
```

需要调试信息时：

```bash
python3 scripts/wechat_auto.py send "文件传输助手" "测试消息" --debug --delay 0.8
```

## 快速命令

- 体检：

```bash
python3 scripts/wechat_auto.py doctor
```

- 发送消息：

```bash
scripts/send_message "张三" "你好，这是自动消息"
```

## 常见风险

- 没有 Accessibility 权限时，快捷键会失败
- 微信未在前台时，粘贴内容会发到错误应用
- 联系人重名时，单靠回车选中可能进入错误会话

## 参考文件

- `scripts/wechat_auto.py`
- `scripts/send_message`
