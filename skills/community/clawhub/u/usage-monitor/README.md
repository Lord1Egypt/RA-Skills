# Usage Monitor Skill

> 通用的用量/配额监控 Skill - 支持任意服务用量面板监控

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-yellow.svg)](https://opensource.org/licenses/MIT-0)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-available-green)](https://clawhub.ai/skills/usage-monitor)

## ✨ 特性

- 🔗 **自定义 URL** - 支持任意用量/配额面板页面 URL
- 🎯 **自定义阈值** - 支持设置任意告警百分比（1-100 可配置）
- 📊 **多维度监控** - 支持多个时间维度的用量数据
- 🔔 **主动提醒** - 达到阈值时自动发送消息
- 🔒 **隐私保护** - 所有配置本地存储

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install usage-monitor

# 或手动安装
git clone https://github.com/YOUR_USERNAME/usage-monitor-skill.git
cp -r usage-monitor-skill ~/.openclaw/workspace/skills/
```

### 配置

```bash
cd skills/usage-monitor
cp config.example.json config.json
# 编辑 config.json 填写你的配置
```

### 使用

```bash
node check.js
```

## 📋 配置参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `panelUrl` | string | ✅ | - | 用量面板页面 URL |
| `alertThreshold` | number | ✅ | 80 | 告警阈值百分比（1-100） |
| `serviceName` | string | ❌ | "服务" | 服务名称 |
| `checkIntervalHours` | number | ❌ | 4 | 检查间隔（小时） |

## 🎯 适用场景

- ✅ OpenClaw Token 数量监控
- ✅ 云服务用量监控（阿里云、AWS、腾讯云等）
- ✅ API 调用配额监控
- ✅ 资源包用量监控
- ✅ 任何有用量百分比显示的面板

## 📖 文档

- [安装指南](INSTALL.md)
- [配置指南](USER-GUIDE.md)

## 📁 文件结构

```
usage-monitor/
├── SKILL.md              # Skill 定义
├── README.md             # 使用说明
├── INSTALL.md            # 快速安装指南
├── USER-GUIDE.md         # 配置指南
├── check.js              # 监控脚本
├── config.example.json   # 配置模板
├── config.schema.json    # 配置验证规则
└── usage-log.template.md # 用量日志模板
```

## 📄 许可证

MIT-0 License - 自由使用、修改和分发

---

**版本：** 2.0.0  
**最后更新：** 2026-03-15
