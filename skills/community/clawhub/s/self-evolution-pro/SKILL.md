---
name: "self-evolution-pro"
version: "1.0.0"
description: "增强型自我进化技能，集成自动技能提取、根因分析、知识图谱、跨会话同步、自动晋级机制。触发词：'总结这个经验'、'保存为技能'、'自我进化'、'学习这个'、'记录教训'。相比原版self-improving-agent，新增自动提取、多维度分析、进化追踪功能。"
---

# Self Evolution Pro

增强型自我进化技能，让AI代理持续自我改进、自我学习。

## 核心升级（相比原版）

| 特性 | 原版 | 增强版 |
|------|------|--------|
| 技能提取 | 手动 | 自动 + 一键 |
| 跨会话同步 | 基础 | 完整知识图谱 |
| 自动晋级 | 无 | 基于复发次数自动晋级 |
| 根因分析 | 无 | 发现模式 → 找根本原因 |
| 进化追踪 | 无 | 版本历史 + 效果追踪 |
| 计划审查 | 手动 | Cron自动化 |

## 触发词

当以下情况时激活：
- 用户说"总结这个经验"、"保存为技能"
- "学习这个"、"自我进化"、"记录这个"
- 发现一个非显而易见的解决方案
- 重复犯同一个错误超过2次
- 解决了一个需要调查的问题

## 工作原理

```
会话中遇到问题/纠正
        ↓
记录到 .learnings/
        ↓
    ┌───┴───┐
 错误   纠正   发现
    ↓     ↓     ↓
根因分析 链接图谱 自动晋级
    ↓
技能提取 → 发布到 ClawHub
    ↓
跨会话同步 → 其他代理也能用
```

## 文件结构

```
~/.openclaw/workspace/
├── AGENTS.md              # 多代理工作流
├── SOUL.md               # 行为准则
├── TOOLS.md              # 工具能力
├── MEMORY.md             # 长期记忆
├── memory/               # 日常记忆
│   └── YYYY-MM-DD.md
├── .learnings/           # 本技能日志
│   ├── LEARNINGS.md      # 学习记录
│   ├── ERRORS.md         # 错误记录
│   ├── FEATURE_REQUESTS.md # 需求记录
│   └── KNOWLEDGE_GRAPH.md # 知识图谱（新增）
├── .skills/              # 提取的技能
│   └── <skill-name>/
└── .evolution/          # 进化追踪（新增）
    ├── metrics.md        # 效果指标
    ├── review-schedule.md # 审查计划
    └── version-history.md # 版本历史
```

## 快速参考

| 情况 | 操作 |
|------|------|
| 命令/操作失败 | 记录到 `.learnings/ERRORS.md` |
| 用户纠正你 | 记录到 `LEARNINGS.md`，类别=`correction` |
| 发现更好方案 | 记录到 `LEARNINGS.md`，类别=`best_practice` |
| 根因分析 | 分析根本原因，链接到 `KNOWLEDGE_GRAPH.md` |
| 复发≥3次 | 自动晋级到对应文件 |
| 技能提取 | 使用 extract 命令 |
| 跨会话同步 | 使用 sync 命令 |
| 计划审查 | 查看 `.evolution/review-schedule.md` |

## 自动晋级规则

当满足以下条件时**自动晋级**：

| 目标文件 | 条件 |
|---------|------|
| `SOUL.md` | 行为模式类学习，复发≥2次 |
| `TOOLS.md` | 工具相关，复发≥2次 |
| `AGENTS.md` | 工作流相关，已解决 |
| `CLAUDE.md` | 项目约定，复发≥3次 |
| 技能提取 | 跨3+个不同任务复发 |

## 根因分析流程

遇到错误时，不只是记录，要分析：

```
1. 直接原因（表象）
   → "文件权限不够"

2. 根本原因（深层）
   → "没检查当前用户权限配置"

3. 模式识别
   → "每次涉及系统配置都容易忽略权限"

4. 系统性预防
   → 创建技能或添加到 SOUL.md
```

格式：

```markdown
## [RCA-YYYYMMDD-XXX] 问题标题

**Root Cause**: 根本原因描述
**Pattern**: 识别到的模式
**Prevention**: 系统性预防措施
**Files**: 相关文件
**Skills**: 相关技能

### Why-Tree
- Why 1: 原因A
  - Why 2: 原因B
    - Why 3: 根本原因 ←
```

## 知识图谱

`.learnings/KNOWLEDGE_GRAPH.md` 链接相关学习：

```markdown
# 知识图谱

## 节点
| ID | 类型 | 标题 | 关联 |
|----|------|------|------|
| N001 | error | Docker权限问题 | N002, N003 |
| N002 | learning | M1 Docker平台问题 | N001 |
| N003 | skill | docker-m1-fixes | N001 |

## 关系
- N001 → causes → N002
- N001 → solved_by → N003
```

## 进化指标

`.evolution/metrics.md` 追踪效果：

```markdown
# 进化指标

## 记录统计
- 本周新增：5条
- 已解决：3条
- 已晋级：2条
- 技能提取：1个

## 效果追踪
| 学习 | 记录日期 | 复发次数 | 节省估计 |
|------|----------|----------|----------|
| Docker M1修复 | 2025-01-15 | 0 | ~30分钟/次 |
| pnpm优先 | 2025-01-18 | 2 | ~5分钟/次 |
```

## 计划审查

`.evolution/review-schedule.md` 安排定期审查：

```markdown
# 审查计划

## 每日 (Heartbeat时)
- 检查高优先级待处理项
- 检查新复发的模式

## 每周
- 完整审查所有pending项
- 识别可晋级项
- 更新知识图谱

## 每月
- 技能版本更新
- 效果指标复盘
- 清理过时项
```

## 技能提取流程

### 方式1：自动提取（推荐）

当检测到复发≥3次，自动触发：

```bash
# 自动执行
./skills/self-evolution-pro/scripts/extract.sh skill-name
```

### 方式2：手动提取

```
触发："保存为技能" / "这个可以提取"
操作：
1. 创建 .skills/<skill-name>/SKILL.md
2. 填写模板
3. 发布到 ClawHub（可选）
4. 更新知识图谱
5. 记录到 version-history.md
```

### 方式3：跨会话提取

```
场景：在会话A发现问题，在会话B需要同样知识
操作：
1. 在会话A：记录 + 标记为 shared
2. 在会话B：使用 sessions_history 读取
3. 提取到共享位置
```

## 跨会话同步

使用 OpenClaw 的会话工具：

### 发送学习到其他会话

```javascript
sessions_send({
  sessionKey: "session:project-alpha-daily",
  message: "新学习：Docker M1平台问题解决方案已记录到 .learnings/ERRORS.md"
})
```

### 读取其他会话的学习

```javascript
// 查看最近会话
sessions_list({ activeMinutes: 60, messageLimit: 3 })

// 读取特定会话历史
sessions_history({ sessionKey: "session-id", limit: 50 })
```

### Spawn子代理做背景研究

```javascript
sessions_spawn({
  task: "研究这个错误并提出系统性解决方案",
  label: "error-research",
  runtime: "subagent",
  mode: "run"
})
```

## 日志格式

### 学习记录

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601
**Priority**: low | medium | high | critical
**Status**: pending | in_progress | resolved | promoted | promoted_to_skill
**Area**: frontend | backend | infra | tests | docs | config
**Recurrence-Count**: 1
**First-Seen**: YYYY-MM-DD
**Last-Seen**: YYYY-MM-DD

### Summary
一句话描述学到了什么

### Root Cause（新增）
根本原因分析（如果是错误）

### Solution
具体解决方案

### Pattern（新增）
如果复发，识别到的模式

### Suggested Action
具体修复或改进建议

### Metadata
- Source: conversation | error | user_feedback | self_discovered
- Related: N001, N002（知识图谱节点）
- See Also: LRN-YYYYMMDD-YYY
- Estimated Time Saved: X minutes（估算节省时间）
```

### 错误记录

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command

**Logged**: ISO-8601
**Priority**: high | critical
**Status**: pending | resolved | wont_fix
**Root Cause Analysis**: [RCA ID 如果已分析]
**Area**: ...

### Summary
简短描述什么失败了

### Error
```
实际错误信息
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 环境详情

### RCA
**Direct Cause**: 直接原因
**Root Cause**: 根本原因
**Pattern**: 识别到的模式

### Resolution
- **Resolved**: ISO-8601
- **Method**: how it was fixed
- **Prevention**: 如何预防再次发生
```

## Cron 自动化

设置定期自我审查：

```javascript
// 每周一早上审查学习
cron_add({
  name: "self-review",
  schedule: { kind: "cron", expr: "0 9 * * 1" },
  payload: {
    kind: "agentTurn",
    message: "执行 .learnings/ 审查：1) 高优先级pending项 2) 识别可晋级项 3) 更新知识图谱"
  },
  delivery: { mode: "announce" }
})
```

## 晋级决策树

```
学习可以晋级吗？
        ↓
是否项目特定？
├── 是 → 留在 .learnings/
└── 否 → 是行为/风格相关？
    ├── 是 → 晋级到 SOUL.md
    └── 否 → 是工具相关？
        ├── 是 → 晋级到 TOOLS.md
        └── 否 → 是工作流相关？
            ├── 是 → 晋级到 AGENTS.md
            └── 否 → 是项目约定？
                ├── 是 → 晋级到 CLAUDE.md/AGENTS.md
                └── 否 → 考虑技能提取
```

## 效果追踪

记录每个学习/技能节省的时间：

```markdown
### Time Tracking
- First Occurrence: YYYY-MM-DD
- Estimated Time per Incident: 15 minutes
- Recurrence Count: 5
- Total Time Saved (if resolved): 75 minutes
- ROI: 本技能投资回报率
```

## 发布技能到 ClawHub

```bash
# 1. 提取技能后
cd ~/.openclaw/workspace

# 2. 发布
clawhub publish .skills/<skill-name> --version 1.0.0

# 3. 更新版本历史
./scripts/update-version-history.sh <skill-name>
```

## 触发器检测

自动检测以下信号：

**纠正** → 学习（correction类别）
- "不，那是错的..."
- "实际上应该是..."
- "你说的不对..."

**功能需求** → 功能请求
- "你能也做...吗"
- "我希望你能..."
- "有办法...吗"

**知识差距** → 学习（knowledge_gap类别）
- 用户提供了你不知道的信息
- 参考的文档已过时

**错误** → 错误记录
- 命令返回非零退出码
- 异常或堆栈跟踪
- 意外输出或行为

**发现更好方案** → 学习（best_practice类别）
- 改进最初方案
- 发现更高效的方法

## 最佳实践

1. **立即记录** - 上下文最清晰的时候
2. **包含根本原因** - 不只是表象
3. **具体解决方案** - 未来需要能直接使用
4. **追踪复发** - 用 Recurrence-Count
5. **更新知识图谱** - 链接相关项
6. **追踪时间节省** - 量化价值
7. **积极晋级** - 存疑时优先晋级
8. **定期审查** - 设置cron自动化
9. **发布分享** - 有价值的发布到ClawHub

## 与原版 self-improving-agent 的区别

1. **知识图谱** - 新增 KNOWLEDGE_GRAPH.md 链接相关学习
2. **根因分析** - RCA 模板，分析根本原因
3. **进化指标** - metrics.md 追踪节省的时间
4. **版本历史** - version-history.md 记录技能演进
5. **计划审查** - review-schedule.md + Cron 自动化
6. **自动晋级** - 明确的自动晋级规则
7. **跨会话同步** - 更完整的同步机制
8. **时间追踪** - Estimated Time Saved 字段
