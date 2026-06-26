# workspace-cleaner

检查并整理 OpenClaw workspace 目录结构，识别文件位置是否正确，讲清逻辑关系和引用关系。

## 触发条件
- "检查workspace"、"清理workspace"、"检查文件位置"

## 执行步骤

### 1. 列出workspace根目录所有文件和目录
```bash
ls -la ~/.openclaw/workspace/
```

### 2. 检查核心文件的引用关系
对每个文件执行：
```bash
grep -r "文件名" ~/.openclaw/workspace/*.md
grep -r "文件名" ~/.openclaw/cron/
```

### 3. 分类并说明逻辑关系

**核心配置层（每次对话自动加载）：**
| 文件 | 被引用次数 | 作用 |
|------|-----------|------|
| AGENTS.md | 被OpenClaw加载 | 工作流程定义 |
| SOUL.md | 被AGENTS.md引用 | 性格设定 |
| USER.md | 被AGENTS.md引用 | 用户信息 |
| MEMORY.md | 被AGENTS.md引用 | 长期记忆 |
| HEARTBEAT.md | 被AGENTS.md引用 | 心跳任务 |
| IDENTITY.md | 定义外在形象 | 名字、头像 |
| PACT.md | 被MEMORY.md引用 | 协作公约 |
| top-100.md | 被AGENTS.md引用 | 常见错误检查 |

**功能层（按需加载）：**
| 文件 | 被引用 | 作用 |
|------|--------|------|
| morning-reminder-template.md | 被cron引用 | 晨间提醒模板 |
| TOOLS.md | 被文档引用 | 工具配置 |

**记忆层（memory/）：**
| 目录 | 内容 | 逻辑 |
|------|------|------|
| memory/daily/ | 日记 | 每天对话记录 |
| memory/lessons/ | 教训 | 错误总结 |
| memory/ | 根目录文件 | 长期记忆 |

### 4. 位置异常识别

**应在 memory/ 但在 workspace/ 根目录：**
- logs/ → memory/
- .learnings/ → memory/
- memory/ 子目录外的md文件

**应在 scripts/ 但在 workspace/ 根目录：**
- bin/ → scripts/

**应在 projects/：**
- data/ → projects/

### 5. 输出报告格式

```
## 📋 Workspace 文件逻辑关系

### 核心配置（每次对话加载）
- AGENTS.md ← 被系统自动加载
  - → 引用: SOUL.md, USER.md, MEMORY.md, HEARTBEAT.md, top-100.md
- IDENTITY.md ← 定义对外形象
- PACT.md ← 协作公约

### 模板/配置（被cron引用）
- morning-reminder-template.md ← 被cron jobs引用

### ⚠️ 位置异常
| 目录/文件 | 当前位置 | 应在位置 | 被引用 | 建议 |
|-----------|---------|---------|--------|------|
| xxx | workspace/ | memory/ | 是/否 | 移动/删除 |

### ❓ 待确认
- 文件名: 问题描述
```

### 6. 询问用户
输出报告后，询问：
"以上是检查结果。要清理位置异常的文件吗？"

### 7. 根据用户反馈执行
- 用户同意 → 执行移动/删除
- 用户不同意 → 保持现状
- 用户有其他指示 → 按用户指示执行
