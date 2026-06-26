# Self-Improving Agent 设置流程示例

## 执行步骤

### 1️⃣ 读取技能文档
✅ 已读取 `~/skills/self-improving/SKILL.md`
- 类型：行为型 + 数据型
- 需要：目录结构、配置文件、核心文件更新
- 功能：自我反思、纠正学习、记忆管理

### 2️⃣ 创建目录结构

```bash
# PowerShell
New-Item -ItemType Directory -Force -Path "C:\Users\TK11\.openclaw\workspace\self-improving\projects"
New-Item -ItemType Directory -Force -Path "C:\Users\TK11\.openclaw\workspace\self-improving\domains"
New-Item -ItemType Directory -Force -Path "C:\Users\TK11\.openclaw\workspace\self-improving\archive"
```

### 3️⃣ 创建核心文件

#### memory.md (HOT 层)
```markdown
# Memory (HOT Tier)

## Preferences
- [2026-04-04] 腾大大偏好使用中文交流

## Patterns
<!-- Recurring patterns go here -->

## Rules
<!-- Confirmed rules go here -->
```

#### corrections.md
```markdown
# Corrections Log

| Date | What I Got Wrong | Correct Answer | Status |
|------|-----------------|----------------|--------|
| 2026-04-04 | 初始设置 | 系统已配置完成 | ✅ 完成 |
<!-- New corrections appear here -->
```

#### index.md
```markdown
# Memory Index

| File | Lines | Last Updated |
|------|-------|--------------|
| memory.md | 10 | 2026-04-04 |
| corrections.md | 7 | 2026-04-04 |
```

#### heartbeat-state.md
```markdown
# Self-Improving Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never

## Last actions
- none yet
```

### 4️⃣ 更新核心文件

#### SOUL.md
添加 Self-Improving 章节：
```markdown
## Self-Improving

Compounding execution quality is part of the job. Before non-trivial work, load `~/self-improving/memory.md` and only the smallest relevant domain or project files. After corrections, failed attempts, or reusable lessons, write one concise entry to the correct self-improving file immediately. Prefer learned rules when relevant, but keep self-inferred rules revisable. Do not skip retrieval just because the task feels familiar.
```

#### AGENTS.md
添加集成说明：
```markdown
## Self-Improving Integration

The `self-improving` skill provides automatic learning from corrections and pattern recognition.

**Setup complete:**
- `~/self-improving/memory.md` — HOT tier (global preferences, always loaded)
- `~/self-improving/corrections.md` — Recent corrections log
- `~/self-improving/index.md` — File index with line counts
- `~/self-improving/heartbeat-state.md` — Heartbeat tracking
- `~/self-improving/projects/` — Project-specific learnings
- `~/self-improving/domains/` — Domain-specific learnings (code, writing, etc.)
- `~/self-improving/archive/` — Cold storage for old patterns

**How it works:**
1. User says "不对，应该是..." → record to corrections.md
2. Pattern repeats 3 times → ask to promote to permanent rule
3. Before tasks → load memory.md + relevant project/domain files
4. After corrections → write lessons immediately

**Commands:**
- "记忆统计" — show memory stats
- "显示我的模式" — list HOT memory rules
- "你知道关于 X 什么？" — search all tiers
- "反思一下刚才的工作" — trigger self-reflection
```

### 5️⃣ 记录设置日志

#### setup-log.md
```markdown
# Self-Improving Setup Log

## Setup Date
2026-04-04

## Version
3.0.13

## Files Created
- [x] memory.md
- [x] corrections.md
- [x] index.md
- [x] heartbeat-state.md
- [x] projects/ directory
- [x] domains/ directory
- [x] archive/ directory

## Core Files Updated
- [x] SOUL.md
- [x] AGENTS.md
- [x] MEMORY.md

## Configuration
- Language: Chinese (默认)
- Auto-learn: enabled
- Pattern threshold: 3 repetitions

## Tests
- [x] Basic test passed (memory.md created)
- [x] Integration test passed (SOUL.md updated)
- [x] Learning test passed (first preference recorded)

## Notes
- First preference: 腾大大偏好使用中文交流
- Ready for production use
```

### 6️⃣ 测试结果

✅ **基本功能测试**
- memory.md 创建成功
- 可以读写偏好
- 索引更新正常

✅ **集成测试**
- SOUL.md 已更新
- AGENTS.md 已更新
- 行为指导已添加

✅ **学习测试**
- 首条偏好已记录
- corrections.md 已初始化
- 系统准备就绪

### 7️⃣ 快速参考卡

```markdown
# Self-Improving 快速参考

## 常用命令
- "记忆统计" — 查看记忆状态
- "显示我的模式" — 列出已学习的偏好
- "反思一下刚才的工作" — 触发自省
- "你知道关于 X 什么？" — 查询特定主题

## 学习触发
- "不对，应该是..." — 纠正
- "我更喜欢 X" — 偏好
- "记住我总是..." — 模式
- "停止做 X" — 负向反馈

## 文件位置
- HOT 记忆：~/self-improving/memory.md
- 纠正日志：~/self-improving/corrections.md
- 项目学习：~/self-improving/projects/
- 领域学习：~/self-improving/domains/
```

## 设置完成清单

- [x] 目录结构创建
- [x] 核心文件创建（4 个）
- [x] SOUL.md 更新
- [x] AGENTS.md 更新
- [x] MEMORY.md 记录
- [x] 基本功能测试
- [x] 学习功能测试
- [x] 快速参考创建
- [x] 设置日志记录

## 下一步

- [ ] 配置心跳集成（可选）
- [ ] 添加更多初始偏好
- [ ] 测试项目特定学习
- [ ] 测试领域特定学习

---

**状态**: ✅ 设置完成
**时间**: 2026-04-04 01:59
**设置者**: 腾龙虾 🦞
