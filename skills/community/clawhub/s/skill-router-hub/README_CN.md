# Skill Router / 技能路由器

> 让 Claude 自动路由到正确的专项技能，并在每次回答末尾报告技能使用情况。
> *Automatically route Claude to the right specialized skill — with a usage report at the end of every answer.*

---

## 这是什么

每个用户的 Claude 都安装了不同的 skills（你可能从 [anthropics/skills](https://github.com/anthropics/skills) 或其他来源安装了很多）。问题是——Claude 不一定会主动用它们。

Skill Router 解决了三件事：

1. **索引** — 列出你所有的技能，让 Claude 知道「我有这些能力」
2. **路由** — 根据你的问题自动匹配并加载最合适的技能
3. **审计** — 每次回答末尾报告实际用了哪些技能，让你知道技能有没有被浪费

```
用户提问 → Skill Router 匹配技能 → 加载专项技能 → 完成回答 → 汇报技能使用
```

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/skill-router.git
cd skill-router
```

### 2. 自动生成索引

```bash
python scripts/generate.py
```

这会扫描你本地的 `~/.claude/skills/` 目录，读取每个技能的 name 和 description，自动分类并生成完整的技能索引表。

### 3. 安装到 Claude

```bash
# Linux / macOS
cp SKILL.md ~/.claude/skills/skill-router/SKILL.md

# Windows
xcopy SKILL.md "%USERPROFILE%\.claude\skills\skill-router\SKILL.md*" /Y
```

### 4. 验证

打开 Claude Code 或 Claude，输入任意问题——回答末尾应该出现技能使用报告。

---

## 工作原理

```
                   ┌──────────────────────────┐
                   │  你的 skills 目录          │
                   │  ~/.claude/skills/        │
                   │  ├── golang-patterns/     │
                   │  ├── frontend-design/     │
                   │  ├── deep-research/       │
                   │  └── ... (N 个)            │
                   └──────────┬───────────────┘
                              │
                   ┌──────────▼───────────────┐
                   │  generate.py              │
                   │  - 读取每个 SKILL.md       │
                   │  - 提取 name + desc      │
                   │  - 自动分类               │
                   └──────────┬───────────────┘
                              │
                   ┌──────────▼───────────────┐
                   │  skill-router/SKILL.md    │
                   │  ├── 技能索引表             │
                   │  ├── 调度规则              │
                   │  └── 汇报指令              │
                   └──────────────────────────┘
```

`generate.py` 读的是你本地的 skills，生成的索引表只包含**你实际安装的那些**。所以每个人的 Skill Router 都是独一无二的。

### 自动分类规则

脚本根据每个 skill 的 name + description 中的关键词自动分类：

| 类别 | 匹配关键词 |
|------|---------------|
| 规划与架构 | architect, blueprint, hexagonal |
| 代码质量 | code review, onboarding, refactor |
| Git & 版本控制 | git, github, commit, branch |
| API & 后端 | api, rest, backend, middleware |
| 数据库 | database, sql, migration, orm |
| DevOps & 部署 | docker, deploy, ci/cd, pipeline |
| 测试 | test, e2e, playwright, benchmark |
| 前端 | react, vue, ui, css, accessibility |
| 移动端 | android, ios, flutter, mobile |
| 语言专项 | golang, java, python, rust, cpp |
| AI / Agent | agent, llm, rag, prompt, eval |
| 内容创作 | writing, blog, article, content |
| 研究 | research, scraper, crawl |
| 安全 | security, hipaa, compliance |
| 系统工具 | context, token, optimization |

未匹配到任何规则的自动归入「其他」。

---

## 日常使用

### 添加新 skill 后更新索引

```bash
cd skill-router
python scripts/generate.py
# 然后重新复制到 skills 目录
```

### 自定义技能目录

```bash
python scripts/generate.py --skills-dir /path/to/your/.claude/skills
```

### 自定义输出路径

```bash
python scripts/generate.py --output ~/custom-router/SKILL.md
```

### 手动维护索引

如果你不想用自动生成，直接在 `SKILL.md` 中编辑 `<!-- SKILL_INDEX_START -->` 和 `<!-- SKILL_INDEX_END -->` 之间的内容即可。格式自由——关键词列表、表格、触发短语等都可以，Claude 都能理解。

---

## 技能使用报告

安装后，每次 Claude 回答完问题，末尾会出现：

```
---
**Skill Usage Report：**
- golang-patterns — 已加载 — 用户提到了 Go 并发
- coding-standards — 已加载 — 涉及代码审查
- deep-research — 未触发 — 匹配但本次无需研究
```

这样你就能知道：哪些技能真的在被用？哪些装了但从来没触发过？

---

## 设计理念

| 你负责 | Skill Router 负责 |
|----------|--------------------------|
| 决定装哪些技能 | 自动发现你装了什么 |
| 决定怎样组织技能 | 按关键词自动分类 |
| 决定要不要用某个技能 | 根据问题自动路由 |
| 想知道用了哪些技能 | 每次回答末尾汇报 |

你只负责**安装和维护技能**，剩下的索引、匹配、汇报全部自动。

---

## License

MIT