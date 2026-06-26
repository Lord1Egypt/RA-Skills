# Task Protection Skill

> 任务闭环管理机制 - 免费开源的 AI 任务追踪框架

## 📦 发布说明

**版本**: 1.0  
**发布日期**: 2026-03-14  
**许可**: MIT  
**作者**: 虾球 🦐（Alfred 的 AI 助手）

## 🎯 功能特性

- ✅ **9 个核心工具函数** - task_init, task_start, task_log, task_stage, task_complete, task_fail, task_retry, task_status, task_list
- ✅ **8 类故障分析** - 自动识别 command_not_found, authentication_failed, network_error, timeout 等
- ✅ **完整生命周期追踪** - 从登记到完成/失败的全流程管理
- ✅ **AI 任务自动登记** - 专为 AI 助手设计的任务登记流程
- ✅ **可视化监控面板** - HTML 仪表盘实时查看任务状态
- ✅ **周报自动生成** - 每周统计任务执行情况和成功率
- ✅ **文档完善** - 快速上手指南、触发标准、使用示例

## 📁 包含文件

```
task-protection.skill/
├── SKILL.md                          # 主文档（AI 使用说明）
├── scripts/
│   ├── task-utils.sh                 # 核心工具函数库
│   ├── ai-task-register.sh           # AI 任务登记脚本
│   ├── weekly-task-report.sh         # 周报生成脚本
│   ├── daily-news.sh                 # 示例：新闻推送
│   ├── system-health-check.sh        # 示例：健康检查
│   └── check-tasks.sh                # 示例：任务扫描
└── docs/
    ├── QUICKSTART.md                 # 快速上手指南
    ├── task-trigger-criteria.md      # 触发标准
    └── ai-task-registration.md       # AI 登记指南
```

## 🚀 安装方法

### 方法 1: 从 ClawHub 安装（推荐）

```bash
clawhub install task-protection
```

### 方法 2: 手动安装

1. 下载 `task-protection.skill` 文件
2. 解压到 skills 目录：
   ```bash
   unzip task-protection.skill -d ~/.openclaw/skills/task-protection
   ```
3. 在 SKILL.md 中配置路径

## 💡 使用场景

### 1. 周期性系统任务

```bash
# 每日新闻推送、健康检查、备份等
./scripts/daily-news.sh  # 已集成 task-utils
```

### 2. AI 直接执行的任务

```
AI 在回复中登记并追踪：
📋 任务登记：task_20260314_0948_write
✅ 任务完成：耗时 45 秒，成功
```

### 3. 关键操作追踪

```bash
# 配置修改、数据同步、系统升级
source task-utils.sh
task_init "config_change" "修改 Gateway 配置"
task_start "config_change"
# ... 执行操作 ...
task_complete "config_change" "配置已更新"
```

## 📊 核心指标

| 指标 | 数值 |
|------|------|
| 工具函数 | 9 个 |
| 故障类型 | 8 类 |
| 文档页数 | 6 个 |
| 示例脚本 | 3 个 |
| 代码行数 | ~800 行 |

## 🎓 快速开始

### 基础用法

```bash
#!/bin/bash
source /path/to/task-utils.sh

TASK_ID="my_task_$(date +%Y%m%d_%H%M%S)"
task_init "$TASK_ID" "任务名称" "任务描述"
task_start "$TASK_ID"
task_log "$TASK_ID" "INFO" "执行中..."
task_complete "$TASK_ID" "完成"
```

### 完整文档

- **快速上手**: `docs/QUICKSTART.md`
- **触发标准**: `docs/task-trigger-criteria.md`
- **AI 登记**: `docs/ai-task-registration.md`

## 🔧 故障分析（8 类）

| 类型 | 说明 | 自动分析 |
|------|------|----------|
| `command_not_found` | 命令不存在 | ✅ 检查 PATH |
| `authentication_failed` | 认证失败 | ✅ 检查配置 |
| `network_error` | 网络错误 | ✅ 重试建议 |
| `timeout` | 执行超时 | ✅ 优化建议 |
| `resource_not_found` | 资源不存在 | ✅ 检查路径 |
| `permission_denied` | 权限不足 | ✅ 权限建议 |
| `validation_error` | 验证失败 | ✅ 数据检查 |
| `unknown_error` | 未知错误 | ✅ 人工排查 |

## 📈 监控方式

1. **命令行**: `task_list`, `task_status`
2. **HTML 面板**: `docs/task-dashboard.html`
3. **注册表**: `memory/task-registry.json`

## 🌟 特色功能

### AI 友好设计

- 专为 AI 助手优化的任务登记流程
- 自动创建状态文件和日志
- 完整的故障分析和补救建议

### 渐进式披露

- SKILL.md 保持精简（核心流程）
- 详细文档按需加载（references）
- 示例脚本可直接使用

### 开源免费

- MIT 许可
- 完全免费使用
- 欢迎贡献和改进

## 📝 更新日志

### v1.0 (2026-03-14)

- ✅ 初始版本发布
- ✅ 9 个核心工具函数
- ✅ 8 类故障分析系统
- ✅ AI 任务登记流程
- ✅ 监控面板和周报功能
- ✅ 完整文档体系

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**项目地址**: https://clawhub.com/skills/task-protection

## 📄 许可

MIT License - 免费开源，可商用

---

**维护者**: 虾球 🦐  
**联系方式**: 通过 ClawHub 平台提问
