---
name: smart-restart-protection
description: 智能重启保护：防止无限循环，确保OpenClaw Gateway安全重启和状态恢复
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":["openclaw","bash"]}}}
---

# Smart Restart Protection

智能重启保护：防止无限循环，确保OpenClaw Gateway安全重启和状态恢复

## 概述

这个技能为 OpenClaw Gateway 提供智能重启保护机制，防止无限循环重启，确保服务在配置变更后安全恢复，并保持会话状态连续性。

## 解决的问题

1. **无限循环风险** - 防止配置错误导致的服务无限重启
2. **状态丢失** - Gateway重启后会话和工作空间状态恢复
3. **频率失控** - 限制重启频率，防止系统过载
4. **并发冲突** - 防止多个重启进程同时运行

## 使用方法

```bash
# 智能重启
./smart-restart.sh "更新配置"

# 检查状态
./check-status.sh

# 重置保护（紧急）
./reset-protection.sh
```