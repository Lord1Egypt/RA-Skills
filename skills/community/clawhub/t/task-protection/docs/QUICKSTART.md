# 🎯 任务闭环管理 - 快速上手指南

> 5 分钟了解如何使用任务保障系统

---

## 🚀 快速开始

### 场景 1: 脚本任务（周期性/系统任务）

```bash
#!/bin/bash
source /home/admin/.openclaw/workspace/scripts/task-utils.sh

# 1. 初始化
TASK_ID="my_task_$(date +%Y%m%d_%H%M%S)"
task_init "$TASK_ID" "任务名称" "任务描述"

# 2. 开始执行
task_start "$TASK_ID"

# 3. 记录过程
task_log "$TASK_ID" "INFO" "正在执行..."

# 4. 完成任务
task_complete "$TASK_ID" "执行成功"
# 或
task_fail "$TASK_ID" "错误信息" "错误类型"
```

### 场景 2: AI 直接执行的任务

**Alfred 委托任务时**：

1. AI 在回复中登记任务
2. 执行任务
3. 反馈结果 + 状态文件位置

**示例**：
```
📋 任务登记：
- ID: task_20260314_0948_write_article
- 名称：撰写安慰文章
- 状态：执行中

...（执行过程）...

✅ 任务完成！
📋 详情:
  - 完成时间：09:48
  - 耗时：45 秒
  - 状态：成功

📄 状态文件：memory/tasks/task_20260314_0948_write_article.json
```

---

## 📁 核心文件

| 文件 | 用途 | 说明 |
|------|------|------|
| `scripts/task-utils.sh` | 工具函数库 | 包含 9 个核心函数 |
| `memory/task-registry.json` | 任务注册表 | 所有任务的索引 |
| `memory/tasks/*.json` | 任务状态 | 每个任务独立状态文件 |
| `logs/tasks/*.log` | 任务日志 | 详细执行日志 |
| `docs/task-protection.md` | 完整文档 | 框架详细说明 |
| `docs/task-dashboard.html` | 监控面板 | 可视化查看任务 |

---

## 🎯 9 个核心函数

### 1. task_init - 初始化任务
```bash
task_init "task_001" "发送邮件" "向团队发送周报"
```

### 2. task_start - 开始执行
```bash
task_start "task_001"
```

### 3. task_log - 记录日志
```bash
task_log "task_001" "INFO" "邮件发送中..."
task_log "task_001" "WARN" "网络延迟"
task_log "task_001" "ERROR" "发送失败"
```

### 4. task_stage - 更新阶段
```bash
task_stage "task_001" "准备内容" "running"
task_stage "task_001" "准备内容" "done"
```

### 5. task_complete - 完成任务
```bash
task_complete "task_001" "邮件已发送"
```

### 6. task_fail - 失败处理
```bash
task_fail "task_001" "发送超时" "timeout"
```

### 7. task_retry - 重试任务
```bash
task_retry "task_001" 3 60  # 最多 3 次，间隔 60 秒
```

### 8. task_status - 查询状态
```bash
task_status "task_001"
```

### 9. task_list - 列出任务
```bash
task_list
```

---

## 📊 故障类型（8 类）

| 类型 | 说明 | 处理方式 |
|------|------|----------|
| `command_not_found` | 命令不存在 | 检查 PATH 或安装 |
| `authentication_failed` | 认证失败 | 检查配置/凭证 |
| `network_error` | 网络错误 | 重试或检查网络 |
| `timeout` | 执行超时 | 增加超时或优化 |
| `resource_not_found` | 资源不存在 | 检查路径或创建 |
| `permission_denied` | 权限不足 | 检查权限设置 |
| `validation_error` | 验证失败 | 检查输入数据 |
| `unknown_error` | 未知错误 | 人工排查 |

---

## 🔧 现有系统任务

| 任务 | 频率 | 脚本 | 状态 |
|------|------|------|------|
| 📰 每日新闻推送 | 每天 7:00 | `daily-news.sh` | ✅ 已迁移 |
| 🏥 系统健康检查 | 每天 8:00, 20:00 | `system-health-check.sh` | ✅ 已迁移 |
| 🔍 每小时任务扫描 | 每小时 | `check-tasks.sh` | ✅ 已迁移 |
| 📤 Git 自动推送 | 每 5 分钟 | `git-auto-commit.sh` | ⏳ 待迁移 |
| 💾 每日本地备份 | 每天 22:00 | (新建) | ⏳ 待创建 |
| 📊 周报统计 | 每周日 23:00 | `weekly-task-report.sh` | ✅ 已创建 |

---

## 📱 监控方式

### 方式 1: 命令行查询
```bash
# 查看所有任务
task_list

# 查看特定任务
task_status "task_001"

# 查看日志
tail -50 logs/tasks/task_001.log
```

### 方式 2: 监控面板
```bash
# 在浏览器打开
open docs/task-dashboard.html
```

### 方式 3: 查看注册表
```bash
# 查看任务注册表
cat memory/task-registry.json | jq '.tasks'
```

---

## ✅ 任务保障检查清单

**任务执行前**：
- [ ] 是否已登记到注册表？
- [ ] 是否创建了状态文件？
- [ ] 优先级是否明确？

**任务执行中**：
- [ ] 关键步骤是否记录日志？
- [ ] 阶段更新是否及时？
- [ ] 错误是否捕获？

**任务完成后**：
- [ ] 状态是否更新（success/failed）？
- [ ] 是否向 Alfred 反馈？
- [ ] 失败是否有原因分析？

---

## 🎓 最佳实践

### ✅ 推荐做法

1. **任务 ID 唯一**：使用时间戳 `task_$(date +%Y%m%d_%H%M%S)`
2. **及时登记**：任务开始前登记，不要事后补
3. **详细日志**：关键决策和操作都要记录
4. **完整反馈**：完成/失败都通知 Alfred
5. **故障分析**：失败时自动分析原因

### ❌ 避免做法

1. **事后补登记**：失去了追踪意义
2. **只记录成功**：失败也要记录
3. **模糊错误**：错误信息要具体
4. **无反馈**：完成任务不通知
5. **过度追踪**：简单问答不需要登记

---

## 📚 文档索引

| 文档 | 用途 |
|------|------|
| `docs/task-protection.md` | 完整框架说明 |
| `docs/task-protection-examples.md` | 详细使用示例 |
| `docs/task-trigger-criteria.md` | 触发标准 |
| `docs/ai-task-registration.md` | AI 任务登记指南 |
| `docs/task-dashboard.html` | 监控面板 |
| `QUICKSTART.md` | 本文档 |

---

## 🆘 常见问题

### Q: 什么任务需要登记？
**A**: 周期性任务、关键操作、对外交互、Alfred 委托、长时间运行的任务需要登记。简单问答不需要。

### Q: 任务失败了怎么办？
**A**: 使用 `task_fail` 自动分析原因，通知 Alfred，并提供补救方案。

### Q: 如何查看历史任务？
**A**: 查看 `memory/tasks/` 目录下的 JSON 文件，或使用 `task_list` 命令。

### Q: 周报在哪里？
**A**: `articles/任务周报-YYYY-Www.md`，每周日自动生成。

### Q: 如何添加新任务？
**A**: 使用 `ai-task-register.sh` 脚本，或手动更新 `memory/task-registry.json`。

---

## 🔄 持续改进

**每周回顾**：
- 查看周报统计
- 分析失败模式
- 优化重试策略

**每月优化**：
- 清理过期任务
- 更新文档
- 优化流程

---

**维护者**: 虾球 🦐  
**版本**: 1.0  
**最后更新**: 2026-03-14

_有任何问题随时问我！_
