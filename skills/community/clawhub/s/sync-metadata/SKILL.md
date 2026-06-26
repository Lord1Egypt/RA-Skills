---
name: sync-metadata
description: 从 package.json 同步项目元数据（名称/版本/描述/仓库地址等）到 README.md、SPEC.md 等 Markdown 文件。当用户改了版本号、项目名、描述后，或说"同步元数据""sync metadata""更新 readme 版本""sync project metadata"时使用。支持 i18n（package.nls.json），支持 dry-run 检查模式。
version: 1.0.0
metadata:
  type: project
  platform: claude-code
  author: guoqw7
  license: GPL-3.0
  tags: [metadata, sync, readme, package.json, documentation, i18n]
  openclaw:
    requires: {}
    emoji: "🔄"
    homepage: https://github.com/guoqw7/claude-skills
    user-invocable: true
---

# sync-metadata

以 `package.json` 为唯一真相源（single source of truth），将项目名称、版本、描述等元数据同步到 README.md、SPEC.md 等 Markdown 文档中。

## 工作原理

1. 读取 `package.json`，解析所有顶层字段
2. 如果有 `package.nls.json` / `package.nls.zh-CN.json`，解析 `%key%` 占位符引用
3. 在目标文件中查找 `<!-- sync:FIELD -->...<!-- /sync -->` 标记
4. 用 package.json 中的实际值替换标记间的内容
5. 报告每个文件被更新了哪些字段

## 支持的字段

以下 package.json 字段均可通过 `<!-- sync:FIELD -->` 同步：

| 标记 | 对应 package.json 字段 | 示例输出 |
|---|---|---|
| `<!-- sync:name -->` | `name` | `ai-history-auto-record` |
| `<!-- sync:displayName -->` | `displayName` 或 nls 解析后的值 | `AI History Auto Record` |
| `<!-- sync:version -->` | `version` | `0.0.1` |
| `<!-- sync:description -->` | `description` 或 nls 解析后的值 | `自动追踪并快照 AI 代码变更...` |
| `<!-- sync:license -->` | `license` | `GPL-3.0` |
| `<!-- sync:repository.url -->` | `repository.url` | `https://github.com/guoqw7/ai-history-auto-record` |
| `<!-- sync:author -->` | `author` (string 或 object.name) | `guoqw7` |

嵌套字段用点号分隔：`<!-- sync:repository.url -->`

## 使用方法

### 1. 在 Markdown 文件中添加标记

```markdown
<!-- README.md -->
# <!-- sync:displayName -->AI History Auto Record<!-- /sync -->

> <!-- sync:description -->项目描述...<!-- /sync -->

项目地址：[<!-- sync:name -->](<!-- sync:repository.url -->)
```

```markdown
<!-- SPEC.md -->
# SPEC: <!-- sync:displayName -->AI History Auto Record<!-- /sync -->

> **Version:** <!-- sync:version -->0.0.1<!-- /sync -->
```

### 2. 运行 Skill

在 Claude Code 中输入 `/sync-metadata`，或直接说"同步元数据"。

Skill 会自动：
- 扫描项目中所有 `.md` 文件里的 `<!-- sync:... -->` 标记
- 与 `package.json` 比对
- 替换过期内容
- 输出变更摘要

### 3. 仅检查（CI 模式）

说"检查元数据是否同步"或"check metadata sync"，Skill 会只检查不修改，类似 `--dry-run`。

## i18n 支持

如果项目有 `package.nls.json` 和 `package.nls.zh-CN.json`：

```json
// package.nls.json
{ "displayName": "AI History Auto Record" }

// package.nls.zh-CN.json
{ "displayName": "AI历史自动记录" }
```

则 Skill 会：
- 默认使用 `package.nls.json`（英文）
- 当用户说"同步中文元数据"时使用 `package.nls.zh-CN.json`
- 如果字段值以 `%` 开头结尾（如 `"%displayName%"`），自动从 nls 文件解析

## 执行步骤

当用户调用此 Skill 时，按以下步骤执行：

1. **读取 package.json** — 解析所有字段作为真相源
2. **读取 nls 文件（可选）** — 如果有 `package.nls.json`，解析 `%key%` 引用
3. **扫描目标文件** — 用正则 `<!-- sync:([\w.]+) -->(.*?)<!-- /sync -->` 搜索所有 `.md` 文件
4. **比对差异** — 对比标记内的当前值与 package.json 中的值
5. **输出报告** — 列出每个文件的变更，格式：

```
📦 元数据同步报告
─────────────────
README.md
  displayName: "AI History Auto Record" → ✅ 已同步
  version:     "0.0.1" → "0.1.0"        ✏️ 已更新
  description: "自动追踪..." → ✅ 已同步

SPEC.md
  version:     "0.0.1" → "0.1.0"        ✏️ 已更新
─────────────────
2 个文件，2 处更新
```

6. **用户确认后写入** — 展示变更后，征得用户确认再实际修改文件

## 最佳实践

- 版本号用 `<!-- sync:version -->` 标记，发版后一键同步
- 项目描述统一用 `<!-- sync:description -->`，改 package.json 后 README/SPEC 自动跟上
- 仓库地址用 `<!-- sync:repository.url -->`，迁移仓库后不用手动改 README
- 不要把所有内容都标记，只标记**跨文件重复的元数据**
