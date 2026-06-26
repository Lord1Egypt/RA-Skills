---
name: 技术讨论管理和沉淀
slug: tech-discussion-manager
version: "0.8.0"
description: 标准化管理技术讨论全生命周期：讨论记录 → 决策沉淀 → 架构文档 → 开发规划。支持 Git 版本管理（可选）。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": [],
          },
        "install":
          [
            {
              "id": "setup-directories",
              "kind": "shell",
              "script": "mkdir -p tech-discussions/docs/discussions tech-discussions/docs/decisions tech-discussions/docs/architecture tech-discussions/docs/dev-plans tech-discussions/code-output",
              "label": "创建标准目录结构",
            },
            {
              "id": "init-index",
              "kind": "shell",
              "script": "test -f tech-discussions/docs/discussions/index.md || echo '# 技术讨论索引\n\n| 日期 | 主题 | 状态 | 标签 | 决策摘要 |\n|------|------|------|------|----------|' > tech-discussions/docs/discussions/index.md",
              "label": "初始化讨论索引",
            },
          ],
        "uninstall":
          [
            {
              "id": "cleanup-notice",
              "kind": "shell",
              "script": "echo '' && echo '📁 tech-discussions/ 目录已保留在 workspace 中。' && echo '   该目录可能包含你的讨论记录、决策文档等。' && echo '   如需删除，请手动执行：rm -rf tech-discussions/' && echo ''",
              "label": "卸载提示",
            },
          ],
      },
  }
---

# 技术讨论管理和沉淀

## 概述

管理技术讨论的全生命周期。将对话中的技术讨论结构化沉淀为可检索、可追溯的文档。

完整使用示例见 `examples.md`。

## 自定义路径

默认讨论目录为 `tech-discussions/`。如需自定义，在 TOOLS.md 中添加：

```markdown
### 技术讨论
- 讨论目录：your/custom/path/
```

Agent 执行时会优先使用 TOOLS.md 中配置的路径。未配置则使用默认路径。

## 目录结构

```
[讨论目录]/
├── docs/
│   ├── discussions/          # 讨论记录
│   │   ├── index.md          # 讨论索引（自动维护）
│   │   └── YYYY-MM-DD-主题-slug.md
│   ├── decisions/            # 决策文档
│   │   └── 项目名-decision.md
│   ├── architecture/         # 架构文档
│   │   └── 项目名-architecture.md
│   └── dev-plans/            # 开发规划
│       └── 项目名-plan.md
└── code-output/              # 代码输出
    └── 项目名/
```

所有路径相对于 workspace 根目录。

## 触发条件

**触发（满足任一）：**

1. 用户明确要求："记录讨论"、"开始技术讨论"、"技术方案评审"、"需求评审"
2. 用户提到技术决策话题："XX 选型"、"评估 XX 方案"、"架构设计"、"技术调研"
3. 用户要求回顾历史："列出讨论"、"查看讨论"、"讨论列表"

**不触发：**

- 日常闲聊中提到"讨论"一词
- 非技术话题
- 用户只是在问问题而非发起讨论

## 工作流程

### 0. 确定路径

1. 读取 TOOLS.md，检查是否有"技术讨论"章节的路径配置
2. 有 → 使用自定义路径
3. 没有 → 使用默认路径 `tech-discussions/`

后续所有步骤中的路径均基于此确定的根目录。

### 1. 开始讨论

创建文件 `[讨论目录]/docs/discussions/YYYY-MM-DD-主题-slug.md`。

文件名规范：日期 + 中文主题 + 英文 slug（简短），例如 `2026-05-09-数据库选型-db-selection.md`。

读取 `templates/discussion.md` 模板填充内容。主题从用户的第一句话中提取。

### 2. 讨论进行中

实时记录要点和决策。在关键节点更新文件：
- 达成共识时
- 做出决策时
- 用户要求保存时

不需要每句话都保存。

### 3. 结束讨论

用户说"讨论结束"、"先这样"、"记录一下结论"等时：

1. 整理讨论内容，提炼核心结论
2. 更新讨论文件状态为"已完成"
3. 更新 `docs/discussions/index.md` 索引（追加一行）

### 4. 生成决策文档（按需）

用户说"生成决策"时：

1. 从讨论中提炼技术选型和关键决策
2. 写入 `docs/decisions/项目名-decision.md`
3. 使用 `templates/decision.md` 模板

### 5. 生成架构文档（按需）

用户说"生成架构"时：

1. 基于决策文档设计系统架构
2. 写入 `docs/architecture/项目名-architecture.md`
3. 使用 `templates/architecture.md` 模板

### 6. 开发规划（按需）

用户说"开始开发"时：

1. 列出已完成的讨论，让用户选择
2. 检查是否有决策文档和架构文档，缺少的先生成
3. 生成开发规划 → `docs/dev-plans/项目名-plan.md`
4. 创建代码目录 → `code-output/项目名/`
5. 使用 `templates/dev-plan.md` 模板

### 7. 版本记录（需 Git）

用户说"记录版本"时：

1. 检查 Git 是否可用（`git status`）
2. 不可用 → 告知用户，跳过 Git 操作
3. 可用 → 询问版本号（如 v1.0.0）和说明
4. 执行 `git add` + `git commit` + `git tag`

## 索引维护

`docs/discussions/index.md` 格式：

```markdown
# 技术讨论索引

| 日期 | 主题 | 状态 | 标签 | 决策摘要 |
|------|------|------|------|----------|
| 2026-05-09 | 数据库选型 | ✅已完成 | 数据库,架构 | 选择 PostgreSQL，因为... |
| 2026-05-10 | API 设计 | 🔄进行中 | API,REST | |
```

每次讨论结束时追加一行。不要重建整个表格。

## Git 策略

- **仅在明确节点 commit**：讨论结束、生成决策/架构文档、记录版本
- **不要每次写文件都 commit**
- Git 不可用时所有基础功能正常
- commit message 格式：
  - 新建讨论：`[讨论] 主题`
  - 决策文档：`[决策] 项目名`
  - 架构文档：`[架构] 项目名`
  - 版本记录：`[版本] vX.X.X - 说明`

## 搜索历史讨论

- 查看索引：读取 `[讨论目录]/docs/discussions/index.md`
- 全文搜索：`exec grep -r "关键词" [讨论目录]/`
- 语义搜索：`memory_search`（如果讨论内容已纳入记忆系统）

## 模板变量说明

模板中的 `[占位符]` 表示需要 agent 根据实际内容填充。例如：
- `[主题]` → 实际讨论主题，如"数据库选型"
- `YYYY-MM-DD` → 实际日期，如"2026-05-09"
- `[项目名]` → 讨论主题的简短标识，如"db-selection"
