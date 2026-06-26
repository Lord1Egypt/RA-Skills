---
name: QClaw Config Guardian
slug: qclaw-config-guardian
version: 1.0.0
description: QClaw 配置守护者。自动备份 cron 任务、通道配置，检测版本变化，升级后自动恢复。触发关键词：备份配置、恢复配置、检查配置、版本升级。
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
keywords:
  - config
  - backup
  - restore
  - cron
  - upgrade
  - migration
license: MIT

# Config Guardian - 配置守护者

自动保护 QClaw/OpenClaw 关键配置，避免版本升级导致任务中断。

## 快速使用

由 AI Agent 执行，无需手动命令：

| 场景 | Agent 行为 |
|------|-----------|
| "备份配置" | 1) 调用 `cron list` 获取任务列表 2) 执行 `backup_config.py` 并将 cron 数据写入 |
| "检查配置" | 1) 调用 `cron list` 获取任务列表 2) 执行 `check_config.py --report` 3) 交叉分析 |
| "恢复配置" | 1) 读取 `latest.json` 2) 对比当前配置 3) 逐项恢复 |
| QClaw 升级后 | 心跳检测版本变化 → 自动备份 → 推送通知 |

### Agent 执行流程

备份时，Agent 应：
1. 调用 `cron` tool (`action: list`, `includeDisabled: true`) 获取所有 cron 任务
2. 将结果保存为临时 JSON 文件
3. 执行 `python3 scripts/backup_config.py --cron-data /tmp/cron_jobs.json`
4. 将备份文件复制到备份目录

检查时，Agent 应：
1. 调用 `cron` tool 获取当前 cron 任务
2. 执行 `python3 scripts/check_config.py --report`
3. 交叉验证 API 返回的任务配置与本地备份

## 触发关键词

当用户提到以下内容时触发此技能：
- "备份配置" / "保存配置"
- "恢复配置" / "配置丢失"
- "检查配置" / "配置异常"
- "版本升级" / "任务失败"

## 保护的关键配置

| 配置项 | 说明 | 恢复方式 |
|--------|------|----------|
| `channels.*` | 通道配置（微信、QQ等） | 自动恢复 |
| `channel-defaults.json` | 通道默认目标映射 | 自动恢复 |
| `cron jobs` | 定时任务配置 | 检测异常 + 提示修复 |
| `plugins.entries.*` | 插件启用状态 | 提示确认 |

## 已知问题模式

### 问题：delivery.channel 缺失

**症状**：cron 任务报错
```
Channel is required when multiple channels are configured: qqbot, openclaw-weixin, wechat-access
```

**原因**：多通道配置下需要显式指定 channel

**修复**：更新 cron job 的 delivery 配置
```json
{
  "delivery": {
    "mode": "announce",
    "channel": "openclaw-weixin",
    "to": "从 channel-defaults.json 读取"
  }
}
```

### 问题：target 格式错误

**症状**：Unknown target 错误

**原因**：混用了不同通道的 target 格式

**修复**：
- `openclaw-weixin` 通道：target 格式为 `xxx@im.wechat`
- `wechat-access` 通道：target 为纯数字 userId

## 备份位置

```
~/.qclaw/config-backups/
├── 2026-04-03_11-15-21_v0.2.1/
│   └── backup.json           # 完整备份
├── 2026-04-02_10-00-00_v0.2.0/
│   └── backup.json
├── latest.json               # 最新备份
└── last-version.txt          # 最后备份版本
```

## 自动检测机制

1. **首次运行**：自动备份当前配置
2. **版本变化**：检测到 QClaw 升级后自动备份 + 提示检查
3. **心跳集成**：可加入 HEARTBEAT.md 定期检查

## 跨平台支持

自动检测并适配：
- macOS：`~/.qclaw/` + PlistBuddy 读版本
- Windows：`%APPDATA%/QClaw/` + 注册表读版本
- Linux：`~/.config/qclaw/`

## 贡献到 ClawHub

此技能已设计为通用版本，可直接贡献到 ClawHub：

1. Fork [ClawHub 仓库](https://github.com/openclaw/clawhub)
2. 将 `config-guardian/` 目录复制到 `skills/`
3. 提交 PR

### 贡献前检查清单

- [ ] 无硬编码路径（已动态检测）
- [ ] 无用户特定配置（已移除）
- [ ] 跨平台兼容（macOS/Windows/Linux）
- [ ] 有清晰的使用文档
- [ ] 有错误处理和降级方案

## 开发计划

- [ ] 自动修复 cron job delivery 配置
- [ ] Webhook 通知（升级后推送微信）
- [ ] 配置迁移脚本（版本间自动迁移）
- [ ] GUI 配置对比工具
