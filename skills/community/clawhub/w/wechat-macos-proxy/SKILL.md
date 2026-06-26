---
name: wechat-macos-proxy
description: "macOS 微信消息自动化工具。通过 GUI 自动化实现：发送消息给指定联系人、读取聊天内容、监控新消息。适用于需要自动化微信操作的场景，如定时发送、批量回复、消息备份等。依赖 peekaboo 进行屏幕截图和 UI 交互。仅支持 macOS。开源地址：https://github.com/chairmanmiao/wechat-macos-proxy"
metadata:
  author: 昆昆猪
  version: 1.1.1
  requires:
    - peekaboo (brew install steipete/tap/peekaboo)
    - jq
  os: [darwin]
  tags: [wechat, automation, messaging, macos, gui]
  github: https://github.com/chairmanmiao/wechat-macos-proxy
---

# WeChat macOS Proxy

让 AI 帮你操作微信。通过 macOS GUI 自动化技术，实现无需 API 的微信消息收发。

## 适用场景

- **定时发送** - 定时给客户/朋友发送消息、提醒
- **自动回复** - 监控消息并自动回复常见问题
- **消息读取** - 代读微信消息，AI 总结内容
- **批量操作** - 批量发送节日祝福、通知等

## 快速开始

### 1. 安装依赖

```bash
brew install steipete/tap/peekaboo jq
```

### 2. 授权（首次使用）

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
# 添加 peekaboo 并开启屏幕录制权限

open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
# 添加终端并开启辅助功能权限
```

### 3. 发送第一条消息

```bash
# 确保微信已打开
~/.openclaw/skills/wechat-macos-proxy/scripts/wechat_proxy.sh send "文件传输助手" "Hello from AI"
```

## 命令详解

### `send` - 发送消息

```bash
wechat_proxy.sh send "联系人名称" "消息内容"

# 示例
wechat_proxy.sh send "张三" "晚上一起吃饭吗？"
wechat_proxy.sh send "工作群" "今天的报告已发邮箱"
```

**注意**：联系人名称必须完全匹配微信中的显示名。

### `read` - 读取最新消息

```bash
wechat_proxy.sh read "联系人名称"

# 示例
wechat_proxy.sh read "李四"
```

读取后会截图保存到 `/tmp/wechat_proxy/`，可使用 AI 分析消息内容。

### `check` - 检查新消息

```bash
wechat_proxy.sh check
```

快速检查聊天列表是否有新消息（红点检测）。

### `listen` - 监听模式（实验性）

```bash
wechat_proxy.sh listen    # 启动监听
wechat_proxy.sh stop      # 停止监听
```

持续监控新消息，配合配置可实现自动回复。

### `test` - 测试连接

```bash
wechat_proxy.sh test
```

验证微信连接、权限和截图功能是否正常。

### `batch-send` - 批量发送

```bash
wechat_proxy.sh batch-send <csv文件路径>

# 示例 - 先创建 CSV 文件
cat > ./contacts.csv << EOF
张三,晚上一起吃饭吗？
李四,明天会议改到下午3点
王五,项目文档已发邮箱
EOF

# 批量发送
wechat_proxy.sh batch-send ./contacts.csv
```

**CSV 格式**: 每行一条记录 `联系人名称,消息内容`，自动间隔 2 秒避免触发风控。

### `export` - 导出聊天记录

```bash
wechat_proxy.sh export "联系人名称" [消息数量]

# 示例
wechat_proxy.sh export "张三" 50    # 导出最近 50 条
wechat_proxy.sh export "工作群"     # 默认导出 30 条
```

**导出内容**: Markdown 索引文件 + 多张截图（滚动截取历史消息）。

## 配置说明

编辑 `~/.openclaw/skills/wechat-macos-proxy/scripts/config.sh`：

```bash
# 回复模式
MODE="semi"                      # auto(全自动) | semi(建议) | manual(仅通知)
AUTO_REPLY_THRESHOLD=0.85        # 自动回复置信度阈值
CHECK_INTERVAL=5                 # 监听检查间隔（秒）
```

## 工作原理

1. **激活微信** - 使用 AppleScript 将微信带到前台
2. **搜索联系人** - Cmd+F 搜索并打开聊天
3. **截图分析** - 使用 peekaboo 截图识别 UI 元素
4. **模拟操作** - 模拟点击、输入、发送等操作

## 限制说明

| 限制 | 说明 |
|------|------|
| 窗口可见性 | 微信窗口不能最小化，可放在后台或另一桌面 |
| 内容识别 | 只能读取文字消息，图片/语音/视频无法识别 |
| 界面依赖 | 微信界面大幅更新时可能需要调整脚本 |
| 速率限制 | 频繁操作可能触发微信风控，建议间隔 1-2 秒 |

## 故障排除

### 权限问题
```bash
# 检查权限状态
peekaboo permissions

# 如果显示未授权，手动添加：
# 系统设置 -> 隐私与安全 -> 屏幕录制 -> 添加 peekaboo
```

### 找不到联系人
- 确保联系人名称完全匹配（包括 emoji）
- 尝试使用备注名而非昵称
- 检查微信中是否有同名联系人

### 消息发送失败
- 检查微信窗口是否在最前
- 增加 `sleep` 延迟时间
- 查看日志：`tail -f /tmp/wechat_proxy/wechat_proxy.log`

## 更新日志

- **v1.1.0** (2025-03-15)
  - 新增 `batch-send` 命令：批量发送消息（支持 CSV 文件）
  - 新增 `export` 命令：导出聊天记录为 Markdown + 截图
  - 优化批量操作间隔，避免触发微信风控

- **v1.0.1** (2025-03-15)
  - 优化文档描述、添加快速开始指南

- **v1.0.0** (2025-03-15)
  - 初始版本
  - 支持 send/read/check/listen 命令
  - 基于 peekaboo 的 GUI 自动化

## 相关链接

- [peekaboo 文档](https://peekaboo.boo)
- [ClawHub 页面](https://clawhub.ai/skills/wechat-macos-proxy)

---

**⚠️ 免责声明**：此工具仅供学习和自动化个人微信使用，请遵守微信用户协议，不要用于 spam、骚扰或违反平台规则的操作。
