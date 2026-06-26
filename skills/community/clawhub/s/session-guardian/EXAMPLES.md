# Session Guardian v1.0 - 使用示例

本文档提供 Session Guardian v1.0 的完整使用示例，帮助你快速上手。

---

## 目录

1. [基础使用](#基础使用)
2. [计划文件管理](#计划文件管理)
3. [Session 隔离检查](#session-隔离检查)
4. [GatewayRestart 恢复](#gatewayrestart-恢复)
5. [实战案例](#实战案例)

---

## 基础使用

### 安装与部署

```bash
# 1. 安装 skill
clawhub install session-guardian

# 2. 进入 skill 目录
cd ~/.openclaw/workspace/skills/session-guardian

# 3. 一键部署
bash scripts/install.sh

# 输出示例：
# [INFO] 创建备份目录...
# [SUCCESS] 备份目录已创建
# [INFO] 添加系统 crontab...
# [SUCCESS] 增量备份任务已添加（每5分钟）
# [SUCCESS] 快照任务已添加（每小时）
# [INFO] 添加 OpenClaw cron...
# [SUCCESS] 每日总结任务已添加
# [SUCCESS] Session Guardian 安装完成！
```

### 验证安装

```bash
# 查看系统 crontab
crontab -l | grep session-guardian

# 输出示例：
# */5 * * * * bash /path/to/incremental-backup.sh
# 0 * * * * bash /path/to/hourly-snapshot.sh
# 0 */6 * * * bash /path/to/health-check.sh

# 查看 OpenClaw cron
openclaw cron list

# 输出示例：
# ID: abc123
# Name: Session Guardian 每日总结
# Schedule: 0 2 * * *
# Status: active
```

### 手动运行备份

```bash
# 增量备份
bash scripts/incremental-backup.sh

# 快照
bash scripts/hourly-snapshot.sh

# 健康检查
bash scripts/health-check.sh

# 查看备份
ls -lh Assets/SessionBackups/
```

---

## 计划文件管理

### 示例1：创建简单任务

```bash
# 创建任务
bash scripts/plan-manager.sh create "修复登录bug"

# 输出：
# [SUCCESS] 计划文件已创建: temp/修复登录bug-plan.md
# [INFO] 请编辑文件填写详细内容

# 编辑计划文件
vim temp/修复登录bug-plan.md
```

**计划文件内容**：

```markdown
# 修复登录bug - 任务计划

**创建时间**: 2026-03-03 14:00
**预计完成**: 2026-03-03 16:00
**负责人**: 开发军团-全栈开发
**状态**: 进行中

---

## 任务目标

修复用户登录时偶发的 500 错误

---

## 子任务清单

### 阶段1: 问题定位
- [ ] 1.1 复现问题
- [ ] 1.2 查看错误日志
- [ ] 1.3 定位根本原因

### 阶段2: 修复与测试
- [ ] 2.1 编写修复代码
- [ ] 2.2 本地测试
- [ ] 2.3 部署到测试环境

### 阶段3: 上线
- [ ] 3.1 代码审查
- [ ] 3.2 部署到生产环境
- [ ] 3.3 监控验证

---

## 当前进度

**状态**: 进行中
**当前阶段**: 阶段1
**完成度**: 0/9

---

## 下一步行动

1. 在测试环境复现问题
2. 查看 Sentry 错误日志
3. 分析数据库查询日志

---

## 风险与阻塞

- 风险1: 问题难以复现
  - 缓解: 增加日志记录，收集更多信息

---

**最后更新**: 2026-03-03 14:00
```

### 示例2：更新任务进度

```bash
# 完成子任务 1.1
bash scripts/plan-manager.sh update "修复登录bug" "1.1"

# 输出：
# [SUCCESS] 子任务 1.1 已标记为完成
# [INFO] 当前完成度: 1/9

# 完成子任务 1.2
bash scripts/plan-manager.sh update "修复登录bug" "1.2"

# 完成子任务 1.3
bash scripts/plan-manager.sh update "修复登录bug" "1.3"

# 查看进度
bash scripts/plan-manager.sh show "修复登录bug"
```

### 示例3：管理多个任务

```bash
# 创建多个任务
bash scripts/plan-manager.sh create "开发新功能A"
bash scripts/plan-manager.sh create "开发新功能B"
bash scripts/plan-manager.sh create "性能优化"

# 列出所有任务
bash scripts/plan-manager.sh list

# 输出示例：
# [INFO] 当前计划文件:
#
# 📋 修复登录bug
#    状态: 进行中 | 完成度: 3/9 | 更新: 2026-03-03 14:30
#
# 📋 开发新功能A
#    状态: 待办 | 完成度: 0/6 | 更新: 2026-03-03 14:35
#
# 📋 开发新功能B
#    状态: 待办 | 完成度: 0/6 | 更新: 2026-03-03 14:36
#
# 📋 性能优化
#    状态: 进行中 | 完成度: 2/8 | 更新: 2026-03-03 14:40
#
# [INFO] 共 4 个计划文件
```

### 示例4：归档已完成任务

```bash
# 任务完成后归档
bash scripts/plan-manager.sh archive "修复登录bug"

# 输出：
# [SUCCESS] 计划文件已归档: Assets/Projects/修复登录bug-plan-20260303.md

# 查看归档
ls -lh Assets/Projects/
```

---

## Session 隔离检查

### 示例1：检查所有 agent

```bash
# 运行检查
bash scripts/session-isolation-check.sh check

# 输出示例：
# [INFO] 开始检查Session隔离状态...
# [WARNING] [dev-lead] AGENTS.md缺少Session隔离规则
# [WARNING] [track-lead] AGENTS.md缺少Session隔离规则
# [WARNING] [finance-lead] AGENTS.md缺少Session隔离规则
# [WARNING] 发现 15 个潜在问题
```

### 示例2：验证单个 agent

```bash
# 验证 main agent
bash scripts/session-isolation-check.sh validate main

# 输出示例：
# [INFO] 验证 [main] 的Session隔离...
# [SUCCESS] ✓ AGENTS.md包含Session隔离规则
# [SUCCESS] ✓ Session文件数量正常: 3
# [SUCCESS] ✓ Session文件大小正常
# [SUCCESS] [main] Session隔离验证通过
```

### 示例3：生成详细报告

```bash
# 生成报告
bash scripts/session-isolation-check.sh report

# 输出：
# [INFO] 生成Session隔离报告...
# [SUCCESS] 报告已生成: Assets/SessionBackups/session-isolation-report-20260303-143000.md

# 查看报告
cat Assets/SessionBackups/session-isolation-report-20260303-143000.md
```

**报告示例**：

```markdown
# Session隔离检查报告

**生成时间**: 2026-03-03 14:30:00

---

## 检查结果

### [main]
- ✅ AGENTS.md包含Session隔离规则
- ✅ Session文件数量: 3
- ✅ Session文件大小正常

### [dev-lead]
- ❌ AGENTS.md缺少Session隔离规则
- ⚠️ Session文件数量: 12（建议清理）
- ✅ Session文件大小正常

### [track-lead]
- ❌ AGENTS.md缺少Session隔离规则
- ✅ Session文件数量: 5
- ❌ 发现 1 个过大的Session文件（>1MB）

---

## 总结

- 总计检查: 16 个agent
- 通过检查: 1 个agent
- 通过率: 6.3%

---

## 建议

1. 为所有agent的AGENTS.md添加Session隔离规则
2. 定期清理过大的Session文件（>1MB）
3. 定期清理旧的Session文件（>30天）
4. 使用Session Guardian的健康检查功能自动维护
```

---

## GatewayRestart 恢复

### 示例1：模拟 Gateway 重启

```bash
# 1. 创建一些未完成任务
bash scripts/plan-manager.sh create "测试任务A"
bash scripts/plan-manager.sh create "测试任务B"

# 2. 重启 Gateway
openclaw gateway restart

# 3. 运行健康检查（自动检测重启）
bash scripts/health-check.sh

# 输出示例：
# [INFO] === 检查 Gateway 状态 ===
# [INFO] Gateway 运行正常
# [ALERT] 检测到 Gateway 重启（时间: 2026-03-03 14:35:00）
# [INFO] === 检查恢复文件 ===
# [INFO] 没有恢复文件
# [INFO] === 检查未完成任务 ===
# [ALERT] 发现 2 个进行中的计划文件
# [INFO]   任务: 测试任务A | 状态: 进行中
# [INFO]   任务: 测试任务B | 状态: 进行中
```

### 示例2：查看健康报告

```bash
# 查看最新的健康报告
cat Assets/SessionBackups/health-report-*.txt | tail -50

# 输出示例：
# # Session Guardian 健康检查报告
# 生成时间: 2026-03-03 14:35:30
#
# ## 检查项目
# 1. Session 文件大小
# 2. Agent 配置完整性
# 3. 磁盘空间
# 4. Gateway 状态
# 5. 计划文件健康度
#
# ## 告警信息
# [ALERT] 检测到 Gateway 重启（时间: 2026-03-03 14:35:00）
# [ALERT] 发现 2 个进行中的计划文件
```

---

## 实战案例

### 案例1：多智能体协作项目

**场景**：建设智能巡检产品，涉及多个 agent 协作

```bash
# 1. 创建项目计划
bash scripts/plan-manager.sh create "智能巡检产品v1.0"

# 2. 编辑计划文件
vim temp/智能巡检产品v1.0-plan.md

# 3. 分配任务给不同 agent
# - 安防AI产品军团：流程设计
# - 开发军团UI设计师：界面设计
# - 开发军团全栈开发：代码实现

# 4. 每个 agent 完成任务后更新进度
bash scripts/plan-manager.sh update "智能巡检产品v1.0" "1.1"
bash scripts/plan-manager.sh update "智能巡检产品v1.0" "1.2"

# 5. 定期检查 Session 隔离（防止跨 agent 混淆）
bash scripts/session-isolation-check.sh check

# 6. 项目完成后归档
bash scripts/plan-manager.sh archive "智能巡检产品v1.0"
```

### 案例2：多渠道运营

**场景**：同时使用 Web 和钉钉，需要防止跨渠道泄露

```bash
# 1. 定期检查 Session 隔离
bash scripts/session-isolation-check.sh check

# 2. 生成报告（每周一次）
bash scripts/session-isolation-check.sh report

# 3. 如果发现问题，手动清理过大的 session 文件
# 健康检查会自动清理，但也可以手动清理
find ~/.openclaw/agents/*/sessions -name "*.jsonl" -size +1M -delete

# 4. 在 AGENTS.md 中添加 Session 隔离规则
# 参考 SKILL.md 中的"Session 隔离规则"章节
```

### 案例3：长期项目管理

**场景**：项目周期3个月，需要持续追踪进度

```bash
# 1. 创建项目计划
bash scripts/plan-manager.sh create "Q1产品迭代"

# 2. 每周更新进度
bash scripts/plan-manager.sh show "Q1产品迭代"
bash scripts/plan-manager.sh update "Q1产品迭代" "1.1"

# 3. 每月生成 Session 隔离报告
bash scripts/session-isolation-check.sh report

# 4. 每周运行健康检查
bash scripts/health-check.sh

# 5. 项目完成后归档
bash scripts/plan-manager.sh archive "Q1产品迭代"

# 6. 查看归档的项目
ls -lh Assets/Projects/
```

---

## 常见问题

### Q1: 计划文件太多，如何清理？

```bash
# 清理超过30天的计划文件
bash scripts/plan-manager.sh clean

# 输出：
# [INFO] 清理超过30天的计划文件...
# [INFO] 删除旧计划: 测试任务A
# [INFO] 删除旧计划: 测试任务B
# [SUCCESS] 已清理 2 个旧计划文件
```

### Q2: 如何查看所有备份？

```bash
# 查看备份目录
ls -lh Assets/SessionBackups/

# 输出示例：
# drwxr-xr-x  incremental/     # 增量备份
# drwxr-xr-x  hourly/          # 快照
# drwxr-xr-x  daily/           # 每日总结
# drwxr-xr-x  large-sessions/  # 过大的 session 文件备份
# -rw-r--r--  backup.log       # 备份日志
# -rw-r--r--  health-check.log # 健康检查日志
```

### Q3: 如何恢复数据？

```bash
# 从增量备份恢复
bash scripts/restore.sh --source incremental

# 从快照恢复（1小时前）
bash scripts/restore.sh --source hourly --timestamp 2026-03-03-14

# 恢复特定 agent
bash scripts/restore.sh --source incremental --agent track-lead
```

---

## 下一步

- 阅读完整文档：`SKILL.md`
- 查看发布说明：`RELEASE-v1.0.md`
- 加入社区讨论：https://github.com/cyber-axin/session-guardian

---

**Session Guardian v1.0** - 让你的 AI 对话永不丢失，任务状态永不混淆 🛡️
