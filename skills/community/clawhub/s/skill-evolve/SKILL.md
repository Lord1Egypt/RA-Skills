---
name: skill_evolve
description: 自进化技能管理器 — 复杂任务后自动将经验固化为 SKILL.md，下次同类任务直接复用
---

# 自进化技能管理器

## 核心理念

每当你完成一个**非平凡任务**（non-trivial），就把经验固化成可复用的 Skill，下次同类任务直接调用，避免从零推理。

## 自进化触发条件

满足以下任一条件时，**必须**考虑创建或更新 Skill：

1. **复杂任务成功**（≥5 个工具调用）
2. **踩坑后找到正确路径**（错误 → 排查 → 解决）
3. **用户纠正**（"不是这样" → 找到正确方法）
4. **发现 nontrivial 工作流**（多个步骤串联的流程）
5. **配置/环境特殊性**（只有这个机器/环境才有的坑）

## 操作指南

### 1. 创建新 Skill

当发现新工作流时，用 `write` 工具创建：

```bash
# 目录结构
~/.openclaw/workspace/skills/<category>/<skill-name>/SKILL.md
```

SKILL.md 标准格式：

```markdown
---
name: <skill_name>
description: 一句话描述这个技能做什么
version: 1.0.0
triggers:
  - "触发条件1"
  - "触发条件2"
---

# 技能标题

## When to Use
什么情况下用这个技能。

## Procedure
1. 步骤一
2. 步骤二

## Pitfalls
- 已知失败模式和应对

## Verification
如何验证成功。
```

### 2. 更新现有 Skill

用 `edit` 工具进行增量修改（避免全量替换）：

```markdown
# patch 场景示例
## Pitfalls
- 原来只有1条，新发现1条 → edit 在对应 section 追加

# edit 场景示例  
## Procedure
整个流程变了 → 全量替换
```

### 3. 删除过时 Skill

当 Skill 不再适用或有更好的替代时，删除它：

```bash
rm -rf ~/.openclaw/workspace/skills/<category>/<skill-name>/
```

### 4. 查看已有 Skills

```bash
# 列出所有 Skills
ls ~/.openclaw/workspace/skills/

# 查看特定 Skill
cat ~/.openclaw/workspace/skills/<category>/<skill-name>/SKILL.md
```

## 决策树：要不要创建 Skill？

```
这个任务以后还会遇到吗？
  ├─ 否 → 不用创建
  └─ 是 → 涉及 ≥2 个步骤？
            ├─ 否 → 不用创建（太简单）
            └─ 是 → 这个流程容易忘吗？
                      ├─ 否 → 不用创建
                      └─ 是 → ✓ 创建 Skill
```

## 经验固化时机示例

### 场景 1：踩坑
```
你尝试连接 MySQL，密码里有特殊字符，一直失败
排查后发现：密码需要 URL encode
解决后 → 创建 skill: mysql_special_char_password
```

### 场景 2：用户纠正
```
用户说"这个命令不对，应该是..."
纠正后 → 检查同类任务是否有类似问题
        → 如果有普遍性 → 创建/更新 Skill
```

### 场景 3：环境特殊性
```
这台服务器 SSH 端口不是 22，而是 2222
发现后 → 创建/更新 Skill 记录这个环境特殊性
```

## Skill 命名规范

| 类型 | 命名格式 | 示例 |
|------|---------|------|
| 单工具 | `<tool>_<brief>` | `mysql_connect_prod` |
| 多工具流程 | `<domain>_<task>` | `deploy_k8s_rolling_update` |
| 环境坑 | `<env>_<issue>` | `aws_ssh_port_2222` |
| 最佳实践 | `<domain>_<best_practice>` | `git_commit_conventional` |

## Category 参考

- `devops/` — 部署、运维、环境
- `debug/` — 排错、调试
- `workflow/` — 工作流程
- `platform/` — 平台集成（飞书、GitHub等）
- `learned/` — 经验教训（从错误中学习）

## 容量管理

Skill 也有"错题本"的概念——不是越多越好，而是**精炼、可操作**：

- **好**：简洁、步骤清晰、一看就懂
- **坏**：大段叙述、过于通用、缺乏具体性

如果一个 Skill 超过 200 行，考虑拆分成多个。
