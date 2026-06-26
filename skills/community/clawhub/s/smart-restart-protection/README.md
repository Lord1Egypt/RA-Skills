# Smart Restart Protection

![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.0.0-orange)

**智能重启保护** - 防止无限循环，确保 OpenClaw Gateway 安全重启和状态恢复

## 🎯 解决的问题

在管理 OpenClaw Gateway 时，你是否遇到过这些问题？

- 🔄 **无限循环重启** - 配置错误导致服务不断重启
- 📉 **状态丢失** - 重启后会话历史和工作空间状态丢失
- ⚡ **频率失控** - 意外频繁重启导致系统不稳定
- ⚠️ **并发冲突** - 多个重启进程同时运行导致冲突

这个技能为你提供完整的解决方案！

## ✨ 核心功能

### 🛡️ 智能保护机制
- **频率限制** - 每小时最多3次，每天最多10次重启
- **间隔保护** - 最小重启间隔5分钟
- **锁机制** - 防止并发重启进程冲突
- **状态持久化** - 完整的重启历史记录

### 🔄 安全重启流程
- **自动备份** - 重启前自动备份配置文件
- **健康检查** - 重启后验证服务状态
- **会话保护** - 确保 OpenClaw 会话持久化
- **工作空间保护** - 保持记忆文件和配置完整性

### 📊 监控和诊断
- **实时状态检查** - 一键查看系统状态
- **保护状态监控** - 显示重启限制使用情况
- **故障诊断** - 详细的错误信息和修复建议
- **审计日志** - 完整的操作记录

## 🚀 快速开始

### 安装
```bash
# 通过 ClawHub 安装
clawhub install smart-restart-protection

# 或手动安装
git clone https://github.com/your-username/smart-restart-protection.git
cd smart-restart-protection
```

### 基本使用
```bash
# 智能重启
./smart-restart.sh "更新配置"

# 检查状态
./check-status.sh

# 查看帮助
./smart-restart.sh --help
```

### OpenClaw 集成
```javascript
// 在 OpenClaw 技能中使用
await smart_restart_protection({
  action: "restart",
  reason: "系统维护",
  force: false
});

// 检查状态
const status = await smart_restart_protection({
  action: "status"
});
```

## 📖 详细文档

### 命令行工具

#### 1. smart-restart.sh
```bash
# 基本重启
./smart-restart.sh "更新 Brave Search 配置"

# 强制重启（跳过保护检查）
./smart-restart.sh "紧急修复" --force

# 无备份重启
./smart-restart.sh "快速测试" --no-backup

# 查看版本
./smart-restart.sh --version
```

#### 2. check-status.sh
```bash
# 基本状态检查
./check-status.sh

# 详细输出（JSON格式）
./check-status.sh --verbose --json

# 监控模式（每30秒刷新）
./check-status.sh --watch --interval 30

# 诊断模式
./check-status.sh --diagnose
```

#### 3. reset-protection.sh
```bash
# 重置保护状态（需要确认）
./reset-protection.sh
```

### JavaScript API

#### 重启操作
```javascript
const result = await smart_restart_protection({
  action: "restart",
  reason: "配置更新",
  force: false,          // 可选：强制跳过保护
  onSuccess: () => console.log("成功!"),
  onError: (err) => console.error("失败:", err)
});
```

#### 状态查询
```javascript
// 完整状态
const status = await smart_restart_protection({
  action: "status"
});

// 保护状态
const protection = await smart_restart_protection({
  action: "protection-status"
});

// 重启历史
const history = await smart_restart_protection({
  action: "history",
  limit: 20
});
```

#### 管理操作
```javascript
// 重置保护（紧急使用）
await smart_restart_protection({
  action: "reset-protection",
  confirm: "EMERGENCY_RESET"
});

// 清理旧备份
await smart_restart_protection({
  action: "cleanup",
  keepDays: 7
});

// 导出报告
const report = await smart_restart_protection({
  action: "export-report",
  format: "markdown"  // json, markdown
});
```

## ⚙️ 配置

### 配置文件
```json
{
  "skills": {
    "entries": {
      "smart-restart-protection": {
        "enabled": true,
        "config": {
          "maxRestartsPerHour": 3,
          "maxRestartsPerDay": 10,
          "minRestartInterval": 300,
          "autoBackup": true,
          "healthCheckEnabled": true,
          "stateDir": "~/.openclaw/restart-state"
        }
      }
    }
  }
}
```

### 环境变量
```bash
# 自定义状态目录
export SRP_STATE_DIR=/custom/path

# 调整限制
export SRP_MAX_HOURLY=5
export SRP_MAX_DAILY=20
export SRP_MIN_INTERVAL=600
```

## 🏗️ 架构设计

### 目录结构
```
~/.openclaw/restart-state/
├── restarts.log          # 重启记录（JSON格式）
├── last_restart          # 最后重启时间戳
├── backups/              # 配置文件备份
│   ├── openclaw-2026-03-09-10-30-00.json.bak
│   └── openclaw-2026-03-09-10-30-00.json.bak.reason
├── logs/                 # 操作日志
│   └── 2026-03-09.log
└── reset-backups/        # 重置状态备份
```

### 保护算法
1. **时间窗口计数** - 基于滑动窗口的频率统计
2. **锁文件机制** - 使用PID文件锁防止并发
3. **健康检查链** - 多层服务状态验证
4. **自动回滚** - 失败时自动恢复备份

### 集成点
- **OpenClaw Gateway** - 服务管理和状态监控
- **会话持久化** - 利用内置会话保存机制
- **工作空间** - 保护记忆和配置文件
- **通知系统** - 可选的消息通知集成

## 🔧 故障排除

### 常见问题

#### 1. 速率限制错误
```
错误：每小时重启次数超出限制 (3/3)
解决方案：等待1小时或使用重置工具
```

#### 2. 锁文件冲突
```
错误：另一个重启进程正在运行 (PID: 12345)
解决方案：等待进程完成或手动终止
```

#### 3. 健康检查失败
```
错误：Gateway Web接口不可达
解决方案：检查Gateway服务状态和网络配置
```

#### 4. 权限问题
```
错误：配置文件备份失败: EACCES
解决方案：检查文件权限和执行权限
```

### 调试模式
```bash
# 启用详细日志
DEBUG=smart-restart:* ./smart-restart.sh "调试重启"

# 跟踪执行流程
./check-status.sh --debug --trace

# 查看日志文件
tail -f ~/.openclaw/restart-state/logs/$(date +%Y-%m-%d).log
```

## 📈 性能指标

### 关键指标
- **重启成功率** - 成功重启的比例
- **平均恢复时间** - 从重启到服务就绪的时间
- **保护触发率** - 频率限制被触发的次数
- **备份完整性** - 备份文件的完整性和可恢复性

### 监控集成
```bash
# Prometheus 指标（可选）
./check-status.sh --prometheus

# 健康检查端点
curl http://localhost:9090/health

# 性能仪表板（可选）
open http://localhost:3000/dashboard
```

## 🤝 贡献指南

### 开发环境
```bash
# 克隆仓库
git clone https://github.com/your-username/smart-restart-protection.git
cd smart-restart-protection

# 安装依赖
npm install

# 运行测试
npm test

# 代码检查
npm run lint
```

### 提交规范
1. 遵循 Conventional Commits 规范
2. 添加测试用例
3. 更新文档
4. 通过所有测试

### 代码风格
- 使用 ESLint 配置
- 遵循 JavaScript Standard Style
- 添加 JSDoc 注释
- 保持代码简洁

## 📄 许可证

MIT License

Copyright (c) 2026 龍哥 & 小包子

## 🙏 致谢

- **龍哥** - 提出需求和宝贵反馈
- **OpenClaw 社区** - 优秀的开源AI助手平台
- **所有贡献者** - 感谢你们的支持和贡献

## 📞 支持

- **问题反馈** - [GitHub Issues](https://github.com/your-username/smart-restart-protection/issues)
- **讨论区** - [OpenClaw Discord](https://discord.gg/clawd)
- **文档** - [详细文档](https://github.com/your-username/smart-restart-protection/wiki)

---

**让 OpenClaw Gateway 重启更安全、更可靠！** 🦞