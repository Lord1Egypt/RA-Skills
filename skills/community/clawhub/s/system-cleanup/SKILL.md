# 系统清理技能 (System Cleanup Skill)

## 简介
一个用于定期清理和维护OpenClaw系统的技能，包括清理临时文件、备份文件、日志文件，以及优化系统性能。

## 适用场景
当用户要求执行系统清理、维护、优化或清理磁盘空间时使用此技能。

## 核心功能

### 1. 配置文件备份清理
- 清理旧的 `.bak`, `.backup`, `.clobbered` 备份文件
- 保留最新的2-3个备份文件
- 清理vim交换文件 (`.swp`, `.swx`)

### 2. 临时文件清理
- 清理 `/tmp` 目录中的OpenClaw相关临时文件
- 清理工作空间中的临时文件
- 清理超过指定时间的缓存文件

### 3. 会话管理
- 检查并清理旧的会话文件
- 清理超过7天的会话记录
- 检查会话文件大小并报告

### 4. 磁盘使用分析
- 分析OpenClaw目录的磁盘使用情况
- 识别最大的文件/目录
- 提供清理建议

### 5. 系统状态检查
- 检查Gateway服务状态
- 验证服务配置
- 检查安全警告

## 使用指南

### 基本命令
```bash
# 检查当前系统状态
openclaw gateway status

# 清理旧的备份文件
find ~/.openclaw -name "*.bak.*" -name "*.backup.*" -name "*.clobbered.*" -mtime +7 -delete

# 清理临时文件
find ~/.openclaw -name "*.swp" -name "*.swx" -delete
find /tmp -name "*openclaw*" -mtime +1 -delete 2>/dev/null
```

### 维护脚本
在技能目录中已包含一个维护脚本：
- `scripts/cleanup.sh` - 系统清理脚本

### 定期清理
建议每周执行一次系统清理，或在磁盘空间不足时执行。

## 配置选项

### 保留策略
- 备份文件：保留最新的3个
- 日志文件：保留最近7天
- 会话文件：保留最近14天

### 安全设置
- 不删除当前使用的文件
- 先列出待删除文件，再确认删除
- 可配置安全级别

## 示例执行步骤

```bash
# 1. 检查系统状态
openclaw gateway status

# 2. 分析磁盘使用
du -sh ~/.openclaw
du -sh ~/.openclaw/* 2>/dev/null | sort -h

# 3. 列出可清理的文件
find ~/.openclaw -name "*.bak.*" -type f 2>/dev/null | sort

# 4. 执行清理（谨慎操作）
# find ~/.openclaw -name "*.bak.*" -mtime +7 -delete
```

## 注意事项

⚠️ **重要提示**
1. 在删除任何文件前，先列出文件确认
2. 确保不删除当前正在使用的文件
3. 保留足够的备份文件供恢复使用
4. 清理前建议备份重要数据

## 集成建议

### 与HEARTBEAT集成
可将系统清理作为定期心跳任务的一部分，每周执行一次。

### 与cron集成
可设置定期清理任务：
```bash
# 每周一早上3点执行清理
0 3 * * 1 /path/to/system-cleanup/scripts/cleanup.sh
```

## 版本历史
- v1.0 (2026-03-27): 基础系统清理功能