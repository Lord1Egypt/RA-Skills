# 🦞 三只虾协同体系 - 详细文档

_完整的多 agent 任务协同框架_

---

## 📖 目录

1. [架构设计](#架构设计)
2. [安装配置](#安装配置)
3. [使用指南](#使用指南)
4. [API 参考](#api 参考)
5. [最佳实践](#最佳实践)
6. [故障排查](#故障排查)

---

## 架构设计

### 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                    老板（CEO）                           │
│              分配任务、验收结果                          │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│ 终端虾    │ │ 飞书虾    │ │ Telegram  │
│ (CPMO) 🖥️ │ │ (COO) 📱  │ │ 虾 (CGO) 🌐│
│ PMO 核心  │ │ 统筹协管 │ │ 副业执行 │
└───────────┘ └───────────┘ └───────────┘
        │           │           │
        └───────────┼───────────┘
                    │
        ┌───────────▼───────────┐
        │   tasks/queue.md      │
        │   任务队列（共享）     │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │   fswatch 监控         │
        │   实时检测变化         │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │   heartbeat-check.sh  │
        │   心跳检查脚本         │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │   通知系统            │
        │   自动发送飞书消息    │
        └───────────────────────┘
```

---

## 安装配置

### 系统要求

- macOS 12.0+
- Homebrew
- OpenClaw 2026.3.2+

### 步骤 1：安装依赖

```bash
# 安装 fswatch
brew install fswatch

# 验证安装
fswatch --version
```

### 步骤 2：配置服务

```bash
# 一键配置脚本
./skills/three-shrimp-collab/scripts/setup-heartbeat.sh
```

### 步骤 3：验证状态

```bash
# 检查服务
launchctl list | grep openclaw

# 预期输出：
# -    0    com.openclaw.heartbeat
# -    0    com.openclaw.fswatch
```

---

## 使用指南

### 任务分配

**通过飞书虾分配：**
```
老板：飞书虾，给终端虾安排个活，整理下项目周报

飞书虾：好的老板！
✅ 已添加：- [ ] [CPMO] 整理项目周报 - 飞书虾统筹 @2026-03-09 14:00
✅ 监控已触发，终端虾会立即收到
```

**直接编辑任务队列：**
```bash
# 编辑 tasks/queue.md
echo "- [ ] [CPMO] 整理项目周报 - 老板 @$(date +%Y-%m-%d\ %H:%M)" >> tasks/queue.md
```

### 任务执行

**终端虾流程：**
1. 检测新任务（fswatch 触发）
2. 领取任务（更新状态为 `[~]`）
3. 执行任务
4. 标记完成（更新状态为 `[x]`）

**示例：**
```bash
# 领取任务
sed -i '' 's/- \[ \] \[CPMO\] 整理项目周报/- [~] [CPMO] 整理项目周报 - 终端虾 @2026-03-09 14:00/' tasks/queue.md

# 完成任务
sed -i '' 's/- \[~\] \[CPMO\] 整理项目周报/- [x] [CPMO] 整理项目周报 - 终端虾 @2026-03-09 14:30/' tasks/queue.md
```

### 任务通知

**自动通知：**
- 心跳检测完成任务
- 生成通知消息
- 飞书虾发送给你

**通知格式：**
```
✅ 任务完成

📋 任务：[CPMO] 整理项目周报
🦞 执行者：终端虾（CPMO）
⏰ 完成时间：2026-03-09 14:30

【任务结果】
周报已发送到飞书文档
📎 链接：https://feishu.cn/docx/xxx

---
_任务已完成，请老板查阅_
```

---

## API 参考

### 脚本接口

#### heartbeat-check.sh

```bash
# 用法
./scripts/heartbeat-check.sh

# 退出码
0 - 无待处理任务
1 - 有待处理任务
```

#### notify-task-complete.sh

```bash
# 用法
./scripts/notify-task-complete.sh <任务名称> <执行者> <完成时间> [详情]

# 示例
./scripts/notify-task-complete.sh "项目周报" "终端虾" "2026-03-09 14:30" "周报已完成"
```

### 任务队列格式

```markdown
# 待处理
- [ ] [角色] 任务描述 - 分配人 @时间

# 处理中
- [~] [角色] 任务描述 - 负责人 @开始时间

# 已完成
- [x] [角色] 任务描述 - 负责人 @完成时间
```

---

## 最佳实践

### 1. 任务命名

**好：**
```markdown
- [ ] [CPMO] 整理项目 v1.2.0 周报（包含 bug 数、里程碑、风险） - 老板 @2026-03-09 14:00
```

**不好：**
```markdown
- [ ] [CPMO] 周报 - 老板
```

### 2. 状态更新

**及时更新：**
- 领取任务 → 立即更新为 `[~]`
- 完成任务 → 立即更新为 `[x]`
- 遇到阻塞 → 更新为 `[!]` 并说明原因

### 3. 汇报频率

**推荐：**
- 领取任务 → 立即汇报
- 重要进展 → 实时同步
- 任务完成 → 立即通知
- 每小时 → 进展简报（可选）

### 4. 任务清理

**每日 17:00 清理：**
```bash
# 保留最近 3 天的已完成任务
grep "^\- \[x\]" tasks/queue.md | grep -v "$(date -v-3d +%Y-%m-%d)" > tasks/queue.md.tmp
mv tasks/queue.md.tmp tasks/queue.md
```

---

## 故障排查

### 问题 1：监控不工作

**症状：** 添加任务后没有触发检查

**排查：**
```bash
# 检查服务状态
launchctl list | grep openclaw.fswatch

# 查看监控日志
tail -f ~/Library/Logs/openclaw/fswatch-monitor.log

# 重启服务
launchctl unload ~/Library/LaunchAgents/com.openclaw.fswatch.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.fswatch.plist
```

### 问题 2：通知没收到

**症状：** 任务完成但没有收到飞书消息

**排查：**
```bash
# 检查 pending notifications
cat ~/Library/Logs/openclaw/pending-notifications-*.md

# 检查心跳日志
tail -f ~/Library/Logs/openclaw/heartbeat.log

# 手动触发通知
./scripts/notify-task-complete.sh "测试" "飞书虾" "$(date +%Y-%m-%d\ %H:%M)" "测试通知"
```

### 问题 3：心跳不执行

**症状：** 日志长时间未更新

**排查：**
```bash
# 检查服务状态
launchctl list | grep openclaw.heartbeat

# 手动执行一次
./scripts/heartbeat-check.sh

# 查看错误日志
tail ~/Library/Logs/openclaw/heartbeat-stderr.log
```

### 问题 4：任务状态混乱

**症状：** 任务队列格式错误

**修复：**
```bash
# 备份
cp tasks/queue.md tasks/queue.md.bak

# 重置格式
cat > tasks/queue.md << 'EOF'
# 📋 三只虾任务队列

## 待处理
（空）

## 处理中
（空）

## 已完成
（空）
EOF
```

---

## 📚 相关资源

- [三只虾分工体系.md](./docs/三只虾分工体系.md)
- [三只虾协同协议.md](./docs/三只虾协同协议.md)
- [三只虾汇报模板.md](./docs/三只虾汇报模板.md)
- [HEARTBEAT.md](../../HEARTBEAT.md)

---

_创建人：飞书虾（COO）_  
_版本：v1.0_  
_最后更新：2026-03-09 16:23_
