---
name: redundancy-reducer
description: 技能冗余治理：检测组织内重复/重叠的技能名、描述与路由关键词，提出合并去重建议（遵守只增不减）
source:
  type: original
  repo: skills-repo/skill-quality-inspector
  path: skills/redundancy-reducer/SKILL.md
  version: "1.0.0"
  updated: "2026-08-14"
metadata:
  category: 技能治理
  platform: 通用
  difficulty: 进阶
---

# 技能冗余治理（redundancy-reducer）

> 把 AI 助手变成一名"整理师"：组织里 30+ 仓库难免出现功能重叠的技能，本技能负责把重复暴露出来，但不能乱删——只增不减是铁律。

## 能力

- **重名检测**：跨仓库扫描 `skills/<name>/SKILL.md` 的 `name` 字段，找出全局重复标识
- **近重描述**：对 `description` 做 token 重叠（Jaccard），标记高度相似的能力叙述
- **关键词重叠**：比对各仓库根 `SKILL.md` 路由表的 grep 关键词，发现触发词打架
- **归类建议**：把重叠技能归并到"建议保留 / 建议合并 / 建议 deprecated"三档
- **去重约束**：所有去重建议都附带"只增不减"合规校验，绝不主张删除已发布路径

## 使用方式

```
/redundancy-reducer 扫描整个组织的技能重叠
/redundancy-reducer 检查 backend 与 database 两个仓库的能力重叠
```

## 工作流

1. **采集**：`python3 scripts/redundancy_scan.py --org <root> --json`，拿到重名 / 近重描述 / 关键词重叠三类候选。
2. **判重叠**：参照 [references/redundancy-reduction.md](../../references/redundancy-reduction.md) 的重叠判据（同名、语义等价、触发词打架），过滤误报。
3. **出建议**：对真重叠给出处置——能合并的提 PR（新建聚合子技能），不能合并的标记 `deprecated: true` 而非删目录。
4. **合规兜底**：任何建议都要过"只增不减"校验：被 `skills-lock.json` 锁定的路径不得改名 / 删除。
5. **落 registry**：合并 / 废弃结果同步到 `registry/repos.json`，保持账实一致。

## 适用场景

- 新仓库立项前的重叠排查（避免造出和已有仓库重复的技能）
- 组织扩张到 30+ 仓库后的定期"瘦身"巡检
- 合并两个相关领域仓库前的重叠盘点

## 限制

- 近重描述靠 token 重叠，会漏掉"换个说法说同一件事"的软重叠——仍需人工终审
- 不执行删除；`deprecated: true` 是唯一允许的"下线"方式
- 跨仓库合并涉及多仓库协调，本技能只出方案，不替你发 PR
