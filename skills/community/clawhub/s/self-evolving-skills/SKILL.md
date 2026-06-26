---
name: self-evolving-skills
description: Agent 自我进化机制 - 将成功的复杂任务沉淀为可复用的 Skill，实现持续学习和知识积累。
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Agent, Self-Evolution, Skills, Procedural-Memory, Knowledge-Management]
    related_skills: [plan, systematic-debugging, test-driven-development]
---

# Self-Evolving Skills - Agent 自我进化机制

本 Skill 定义了 Agent 如何通过"任务沉淀"实现自我进化：将成功完成的复杂任务提炼为可复用的 Skill，形成持续增长的程序化知识库。

> **工具无关设计**：本机制不依赖任何特定工具，你可以使用环境中已有的任何文件操作工具（如 `write_file`、`create_file`、`edit_file` 等）来创建和管理 Skill。

## 核心理念

**Skills 是 Agent 的程序化记忆** — 它们捕获"如何完成特定类型任务"的经验知识。与通用记忆（声明性事实）不同，Skills 是窄而可操作的。

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent 知识体系                                │
├─────────────────────────────────────────────────────────────────┤
│  Memory (声明性知识)          │  Skills (程序化知识)              │
│  ────────────────────────    │  ────────────────────────        │
│  • 用户偏好                   │  • 完整工作流程                   │
│  • 环境配置                   │  • 步骤化指令                     │
│  • 持久事实                   │  • 陷阱与规避                     │
│  • 工具特性                   │  • 验证方法                       │
│                              │  • 可复用脚本                     │
└─────────────────────────────────────────────────────────────────┘
```

## 何时创建 Skill（触发条件）

**必须创建 Skill 的场景：**

1. **复杂任务成功完成** — 任务涉及 5+ 次工具调用
2. **错误被克服** — 遇到并解决了非平凡的问题
3. **用户纠正被采纳** — 用户纠正了 Agent 的做法，纠正后成功
4. **发现非平凡工作流** — 发现了更好的做事方式
5. **用户明确要求** — 用户说"记住这个流程"或类似

**不应创建 Skill 的场景：**

- 简单的一次性任务（少于 3 步）
- 纯粹的信息查询
- 任务失败且未找到解决方案
- 已有相同功能的 Skill 存在

## 沉淀决策流程

```
任务完成
   ↓
┌─────────────────────────────────────────────────────────────┐
│ 自检：是否满足沉淀条件？                                       │
│                                                             │
│ □ 工具调用 ≥ 5 次？                                          │
│ □ 克服了错误/陷阱？                                          │
│ □ 用户纠正后成功？                                           │
│ □ 发现了非平凡工作流？                                       │
│ □ 用户要求保存？                                             │
│                                                             │
│ 任一条件满足 → 继续                                          │
│ 全部不满足 → 结束（不创建 Skill）                             │
└─────────────────────────────────────────────────────────────┘
   ↓ 满足条件
┌─────────────────────────────────────────────────────────────┐
│ 询问用户确认                                                  │
│                                                             │
│ "这个任务涉及了 [描述复杂度]，是否要保存为 Skill 以便将来复用？" │
└─────────────────────────────────────────────────────────────┘
   ↓ 用户同意
┌─────────────────────────────────────────────────────────────┐
│ 判断 Skill 内容形式（LLM 自主判断）                            │
│                                                             │
│ • 过程主要是概念/步骤说明？    → 只创建 SKILL.md               │
│ • 有可复用的代码逻辑？        → 添加 scripts/xxx.py           │
│ • 有固定的配置模板？          → 添加 templates/config.yaml    │
│ • 有参考文档/API 手册？       → 添加 references/api.md        │
└─────────────────────────────────────────────────────────────┘
   ↓
使用环境中的文件操作工具创建 Skill（见下方"创建 Skill 操作指南"）
```

## Skill 存储位置

Skill 应该存储在用户可配置的目录中。常见位置：

- **用户级别**：`~/.agent/skills/` 或 `~/.hermes/skills/`
- **项目级别**：`./skills/` 或 `./.agent/skills/`
- **自定义位置**：由用户通过配置指定

如果不确定，**向用户询问**首选存储位置。

## Skill 目录结构

```
<skills-directory>/
├── <category>/                    # 可选：分类目录
│   └── <skill-name>/
│       ├── SKILL.md               # 必须：主指令文件
│       ├── references/            # 可选：参考文档
│       │   ├── api.md
│       │   └── examples.md
│       ├── templates/             # 可选：模板文件
│       │   ├── config.yaml
│       │   └── template.md
│       ├── scripts/               # 可选：可执行脚本
│       │   ├── helper.py
│       │   └── validate.sh
│       └── assets/                # 可选：其他资源
│           └── schema.json
```

## SKILL.md 格式规范

### 必须包含的 Frontmatter

```yaml
---
name: skill-name                    # 必须：小写、连字符、最多 64 字符
description: Brief description      # 必须：简短描述，最多 1024 字符
version: 1.0.0                      # 推荐：语义化版本
author: Author Name                 # 推荐：作者信息
license: MIT                        # 推荐：许可证
metadata:
  tags: [Category, Keywords]        # 推荐：标签便于搜索
  related_skills: [other-skill]     # 可选：相关 Skill
---
```

### 推荐的正文结构

```markdown
# Skill 标题

简要介绍这个 Skill 解决什么问题。

## When to Use（何时使用）

触发条件 — Agent 应该在什么情况下加载这个 Skill？

## Prerequisites（前置条件）

环境要求、依赖工具、API Key 等。

## Quick Reference（快速参考）

常用命令或 API 调用表格。

## Procedure（操作流程）

### Step 1: [步骤名称]

详细操作步骤，包含具体命令。

### Step 2: [步骤名称]

...

## Pitfalls（陷阱与规避）

| 陷阱 | 症状 | 解决方案 |
|------|------|----------|
| 问题 1 | 错误信息 | 如何解决 |

## Verification（验证方法）

如何确认任务成功完成。
```

## 内容形式决策（LLM 自主判断）

**没有硬编码规则** — Agent 根据任务性质自主决定是否创建脚本等附加文件：

| 判断因素 | 可能的结果 |
|----------|-----------|
| 代码长度超过 50 行 | 更可能单独放到 scripts/ |
| 逻辑可复用（函数级） | 更可能被脚本化 |
| 经过复杂调试 | 更可能被保存 |
| 用户明确说"保存脚本" | 强烈影响创建脚本 |
| 任务是自动化流程 | 更可能有脚本 |
| 需要配置参数 | 更可能有 templates/ |
| 涉及 API 文档 | 更可能有 references/ |

### 场景示例

**场景 1：简单流程 → 只有 SKILL.md**

```
用户："帮我配置 Git 代理"
Agent：执行了 3-4 条命令，成功了
Agent：问用户是否保存为 Skill
用户：好

→ Agent 创建 SKILL.md（包含步骤说明）
   不创建脚本（因为只是几条简单命令）
```

**场景 2：复杂流程 + 代码逻辑 → SKILL.md + 脚本**

```
用户："帮我实现一个自动化部署流水线"
Agent：写了 Python 脚本 + 调试 + 处理边界情况 + 最终成功
Agent：问用户是否保存为 Skill
用户：好

→ Agent 可能创建：
   - SKILL.md（整体流程说明）
   - scripts/deploy.py（核心部署逻辑）
   - templates/config.yaml（配置模板）
```

## 创建 Skill 操作指南

> **重要**：以下操作使用伪代码描述，请使用你环境中实际可用的文件操作工具替代。

### 创建新 Skill

**步骤 1：确定存储路径**

```
skill_path = "<skills-directory>/<category>/<skill-name>/"
```

**步骤 2：创建目录结构**

使用你的目录创建工具：
```
创建目录: <skill_path>
创建目录: <skill_path>/references/     # 如需要
创建目录: <skill_path>/templates/      # 如需要
创建目录: <skill_path>/scripts/        # 如需要
```

**步骤 3：创建 SKILL.md 主文件**

使用你的文件写入工具，内容遵循上述格式规范：
```
写入文件: <skill_path>/SKILL.md
内容: |
  ---
  name: my-new-skill
  description: Brief description of what this skill does
  version: 1.0.0
  ---

  # My New Skill

  Instructions here...
```

**步骤 4：添加支撑文件（如需要）**

```
# 添加脚本
写入文件: <skill_path>/scripts/helper.py
内容: |
  #!/usr/bin/env python3
  # 脚本内容...

# 添加模板
写入文件: <skill_path>/templates/config.yaml
内容: |
  key: value
  # 配置内容...

# 添加参考文档
写入文件: <skill_path>/references/api.md
内容: |
  # API Reference
  文档内容...
```

### 更新现有 Skill

**小范围修改**：使用文本替换/编辑工具

```
编辑文件: <skill_path>/SKILL.md
查找: "旧内容"
替换为: "新内容"
```

**大范围重写**：直接覆盖文件

```
写入文件: <skill_path>/SKILL.md
内容: "完整的新 SKILL.md 内容"
```

### 常见文件操作工具映射

| 操作 | 可能的工具名称 |
|------|---------------|
| 创建目录 | `mkdir`, `create_directory`, `make_dir` |
| 写入文件 | `write_file`, `create_file`, `save_file`, `write_to_file` |
| 编辑文件 | `edit_file`, `replace_in_file`, `patch_file`, `str_replace_editor` |
| 读取文件 | `read_file`, `cat`, `view_file` |
| 删除文件 | `delete_file`, `remove_file`, `rm` |
| 列出目录 | `list_dir`, `ls`, `list_files` |

## 质量标准

### 好的 Skill 特征

✅ **明确的触发条件** — 清楚说明何时应该使用
✅ **编号步骤 + 精确命令** — 不留歧义
✅ **陷阱部分** — 记录已知失败模式和解决方案
✅ **验证步骤** — 如何确认任务成功
✅ **渐进式披露** — 常用流程在前，边缘情况在后

### 差的 Skill 特征

❌ 只有模糊的描述，没有具体步骤
❌ 缺少命令或代码示例
❌ 没有错误处理指导
❌ 步骤间缺少逻辑连贯性
❌ 过于冗长（超过必要信息）

## Skill 生命周期管理

### 使用时发现问题 → 立即更新

如果加载并使用了某个 Skill，但发现：
- 步骤缺失
- 命令过时
- 遇到未记录的陷阱

**在完成任务前，使用文件编辑工具更新 Skill。**

### 定期维护

- 检查依赖版本是否过期
- 更新已知的陷阱列表
- 补充新发现的最佳实践

## 与其他知识形式的关系

| 知识类型 | 典型存储位置 | 用途 | 示例 |
|----------|-------------|------|------|
| Memory | 配置目录下的记忆文件 | 持久性事实 | "用户偏好 VSCode" |
| Skills | skills 目录 | 程序化知识 | "如何部署 K8s" |
| Session | 数据库/文件 | 历史对话 | 过去的任务记录 |
| TODO | 当前会话 | 临时任务 | 当前任务进度 |

## 总结

自我进化 Skill 机制的核心是：

1. **识别值得沉淀的任务** — 复杂度、错误克服、用户纠正
2. **用户确认** — 尊重用户意愿，不强制创建
3. **LLM 自主判断内容形式** — 没有硬编码规则
4. **工具无关** — 使用环境中任何可用的文件操作工具
5. **渐进式完善** — 使用中发现问题就更新
6. **持续积累** — 每一次成功的复杂任务都是学习机会

---

## 附录：Skill 模板

以下是一个可直接使用的 SKILL.md 模板：

```markdown
---
name: <skill-name>
description: <一句话描述这个 Skill 的用途>
version: 1.0.0
author: <作者>
metadata:
  tags: [<tag1>, <tag2>]
---

# <Skill 标题>

<简要介绍这个 Skill 解决什么问题>

## When to Use

<触发条件列表>

## Prerequisites

<环境要求、依赖>

## Quick Reference

| 操作 | 命令/方法 |
|------|----------|
| ... | ... |

## Procedure

### Step 1: <步骤名称>

<详细操作>

### Step 2: <步骤名称>

<详细操作>

## Pitfalls

| 陷阱 | 症状 | 解决方案 |
|------|------|----------|
| ... | ... | ... |

## Verification

<如何确认成功>
```
