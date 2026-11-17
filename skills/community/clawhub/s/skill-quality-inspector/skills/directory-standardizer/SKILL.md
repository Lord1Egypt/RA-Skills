---
name: directory-standardizer
description: 技能目录规范化：按 superpower 五层结构校验目录布局、文件命名与路由索引完整性，固化组织目录约定
source:
  type: original
  repo: skills-repo/skill-quality-inspector
  path: skills/directory-standardizer/SKILL.md
  version: "1.0.0"
  updated: "2026-08-14"
metadata:
  category: 技能治理
  platform: 通用
  difficulty: 入门
---

# 技能目录规范化（directory-standardizer）

> 把 AI 助手变成一名"档案管理员"：superpower 架构能不能成立，先看目录摆得对不对——五层结构、命名、路由索引，一个都不能乱。

## 能力

- **五层校验**：`SKILL.md` / `references/` / `skills/` / `scripts/` / `assets/` 是否齐全且各司其职（不混层）
- **命名校验**：仓库名 kebab-case、技能目录名与 `name` 字段一致、references 文件名主题化 kebab-case
- **路由完整性**：`references/` `scripts/` `assets/` 里每个文件都在根 `SKILL.md` 被索引（无孤儿）；路由表每行指向真实路径（无悬空）
- **体量校验**：根 `SKILL.md` ≤150 行、无遗留 `TODO`、声明 `metadata.architecture: superpower`
- **修复建议**：对不达标项给出"改成什么样"的具体 diff 建议（只读，默认不改文件）

## 使用方式

```
/directory-standardizer 规范 skills-repo/<repo> 的目录结构
/directory-standardizer 检查 <repo> 有没有路由孤儿文件
```

## 工作流

1. **采集**：复用 [scripts/quality_audit.py](../../scripts/quality_audit.py) 的路由完整性 + 体量检查输出，叠加本技能的文件树校验。
2. **逐项比对**：按 [references/directory-standardization.md](../../references/directory-standardization.md) 的清单，核对五层职责边界（如 scripts 不放方法论、references 不放可独立安装能力）。
3. **定位孤儿 / 悬空**：列出未被索引的文件与指向空路径的路由行。
4. **出整改单**：每条不达标给具体修复动作（移动目录 / 补路由行 / 改名），默认不改文件，除非用户明确要修。
5. **回归**：整改后重跑 `audit_architecture.py --strict`，确认 Level 达标且无新孤儿。

## 适用场景

- 新建仓库脚手架后的目录体检
- legacy 仓库迁移到 superpower 时的结构对齐
- 定期目录整洁度巡检

## 限制

- 不做语义判断——只校验"结构对不对"，不评价"内容好不好"
- 默认只读；要真正移动 / 改名文件需用户显式授权，且不得触碰被 lock 的路径
- 仓库分类（category）与 registry 的一致性由 `quality-auditor` 负责，本技能只管目录形态
