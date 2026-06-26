---
name: wol-wakeup
description: 局域网唤醒 (WoL) 自动化技能。支持工作流模式和单行命令模式，多轮对话添加设备，无需大模型。使用方式：1) "帮我开机"→列表 2) "开机 - 设备名"→唤醒 3) "添加网络唤醒"→工作流 4) "列表"→查看 5) "删除 - 设备名"→删除
version: 1.0.0
author: OpenClaw Community
category: automation
tags:
  - wol
  - wake-on-lan
  - 局域网唤醒
  - 自动化
  - system-tools
metadata:
  openclaw:
    requires:
      bins: [python3]
      pip: [wakeonlan]
    tools: [message]
    hooks:
      enabled: true
      endpoint: "http://127.0.0.1:8765/hook"
---

# WoL Wakeup - 局域网唤醒技能

通过关键词匹配触发 Wake-on-LAN 唤醒设备，无需大模型推理。

## 触发规则（关键词匹配）

### 工作流模式（推荐）
支持多轮对话，逐步引导用户输入信息。

| 关键词 | 动作 |
|---|---|
| `帮我开机` / `电脑开机` / `开电脑` / `开机` | 列出可唤醒设备 |
| `开机 -` + 设备名/编号 | 唤醒指定设备 |
| `添加网络唤醒` / `添加设备` | 启动添加设备工作流（多轮对话） |
| `删除设备` / `移除设备` | 启动删除设备工作流 |
| `列表` / `设备列表` | 显示已保存设备 |

### 单行命令模式（传统）
一次性输入所有信息。

| 命令格式 | 示例 |
|---|---|
| `添加网络唤醒\|MAC\|备注` | `添加网络唤醒\|00:11:22:33:44:55\|书房电脑` |
| `删除 - 设备名` | `删除 - 旧电脑` |

## 配置

设备信息保存在 `~/.openclaw/wol/devices.json`

## 使用示例

### 查看设备列表
```
用户：帮我开机
助手：📋 已保存的 WoL 设备：
1. 我的电脑
   MAC: 00:11:22:33:44:55
   备注：书房台式机
```

### 唤醒设备
```
用户：开机 - 我的电脑
助手：✅ 已发送唤醒信号到：我的电脑 (00:11:22:33:44:55)
请等待设备启动（通常 30-60 秒）
```

或按编号：
```
用户：开机 -1
助手：✅ 已发送唤醒信号到：我的电脑 (00:11:22:33:44:55)
```

### 添加设备（工作流模式 - 推荐）
```
用户：添加网络唤醒
助手：📝 第一步：请输入设备名称（如：书房电脑）

用户：书房电脑
助手：📝 第二步：请输入 MAC 地址
      格式：00:11:22:33:44:55

用户：00:11:22:33:44:55
助手：📝 第三步：请输入备注信息（可选）
      直接回车可跳过

用户：我的台式机
助手：✅ 设备添加成功！
      名称：书房电脑
      MAC: 00:11:22:33:44:55
      备注：我的台式机
```

### 添加设备（单行命令模式）
```
用户：添加网络唤醒|00:11:22:33:44:55|书房台式机
助手：已添加设备：书房台式机 (00:11:22:33:44:55)
```

### 删除设备
```
用户：删除 - 我的电脑
助手：已删除设备：我的电脑
```

## 技术实现

### 架构
- **工作流引擎**: 支持多轮对话、状态保持、流程锁定、超时处理
- **Hook 服务**: HTTP 服务监听 OpenClaw Internal Hooks，优先匹配工作流
- **消息处理**: 工作流未匹配的消息自动放行给 AI 处理

### 组件
- `workflow_engine.py` - 工作流引擎核心
- `state_manager.py` - 会话状态管理
- `message_handler.py` - 消息处理器
- `openclaw_hook.py` - OpenClaw Hook 服务

### 数据持久化
- 设备配置：`~/.openclaw/wol/devices.json`
- 会话状态：`~/.openclaw/wol/workflows/sessions.json`

### 集成方式
通过 OpenClaw Internal Hooks 实现非侵入式集成：
```json
{
  "hooks": {
    "enabled": true,
    "token": "<安全 token>",
    "internal": {
      "enabled": true,
      "endpoint": "http://127.0.0.1:8765/hook"
    }
  }
}
```

详见 `INTEGRATION_GUIDE.md`

## 注意事项

1. 目标设备必须支持并启用 WoL 功能
2. 设备需在同一局域网或通过路由器转发
3. 首次使用需先添加设备的 MAC 地址
4. MAC 地址格式：`XX:XX:XX:XX:XX:XX`（12 位十六进制）

## 获取 MAC 地址

### Windows
```cmd
ipconfig /all
# 查找"物理地址"
```

### macOS
```bash
networksetup -listallhardwareports
# 或：ifconfig | grep ether
```

### Linux
```bash
ip link show
# 或：ifconfig -a
```

## 集成到 OpenClaw

### 快速开始

1. **启动 Hook 服务**:
```bash
cd /root/.openclaw/workspace-zhongshu/skills/wol-wakeup/scripts
python3 openclaw_hook.py --port 8765 --token <token>
```

2. **配置 OpenClaw**:
```bash
python3 update_openclaw_config.py
openclaw gateway restart
```

3. **测试**:
发送微信消息 `帮我开机` 或 `添加网络唤醒`

### 详细文档
- `INTEGRATION_GUIDE.md` - 完整集成指南
- `INTEGRATION_PLAN.md` - 技术方案设计
- `scripts/test_integration.py` - 自动化测试

### 运维命令
```bash
# 查看活跃会话
python3 wol_workflow.py list-sessions

# 清理超时会话
python3 wol_workflow.py check-timeouts

# 健康检查
curl http://127.0.0.1:8765/health
```
