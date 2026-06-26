# 记忆系统架构详解

## 目录结构

```
workspace/
├── MEMORY.md              # 主索引（只读此文件，不读子目录）
├── HEARTBEAT.md           # 心跳任务清单
├── memory/                # 记忆存储根目录
│   ├── YYYY-MM-DD.md      # 每日原始会话日志
│   └── topic-*.md         # 主题记忆文件
└── openclaw-kk/           # 用户私有记忆（可选）
    └── memory/
        └── private/
```

## MEMORY.md 索引格式

```markdown
# MEMORY.md - 长期记忆

---

- [主题标题](memory/topic-file.md) 语义钩子（Hook）
- [Obsidian 规范](memory/obsidian-format.md) 格式规范
- [子代理规则](memory/2026-04-01-subagent-rule.md) 执行模式

---

_最后更新：2026-04-01_
```

## 主题文件 Frontmatter

```yaml
---
name: topic-name          # 唯一标识，英文/拼音
description: 一句话描述  # 供 memory_search 索引
type: infrastructure      # 类型标签
created: 2026-04-01       # ISO 日期
---
```

**type 可选值：**
- `infrastructure` — 系统配置、工具设置
- `security` — 安全相关
- `documentation` — 文档规范
- `reference` — 参考资料
- `automation` — 自动化工作流

## Session Startup 读取顺序

1. 读取 `SOUL.md` — Agent 角色定义
2. 读取 `USER.md` — 用户信息
3. 读取 `memory/YYYY-MM-DD.md`（今日 + 昨日）
4. 主会话时额外读取 `openclaw-kk/memory/private/MEMORY.md`

## 记忆保存时机

- 用户明确说"记住/ save this"
- 任务完成后学到的教训或重要信息
- 偏好或设置变更
- 任何"心理笔记"都必须写文件

## 定期整理（Dreams）

执行 `dream` 任务时：
1. 收集每日日志中的新信号
2. 并入已有主题文件（避免重复）
3. 相对日期 → 绝对日期
4. 修剪 MEMORY.md，删除过时条目

## 与 Obsidian 的区别

| | 本记忆系统 | Obsidian |
|---|---|---|
| 用途 | AI Agent 跨会话记忆 | 人类知识管理 |
| 格式 | 纯文本 + YAML frontmatter | Markdown + 双链 |
| 检索 | memory_search（语义） | Obsidian 本身 |
| 同步 | 文件系统 | Obsidian vault |

两者可共存：Obsidian 作为人类可读的知识库，本系统作为 AI 可解释的上下文记忆。
