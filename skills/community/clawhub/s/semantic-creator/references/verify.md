# Phase 4 · Verify（全部校验 + 升级回路）

输入：Phase 3 产物。逐条执行、逐条回报 pass/fail；全部 pass 才算交付。

## §1 结构检查（YAML 与 OKF 通用语义）

1. 每 bundle 恰好 1 个 catalog（YAML `semantic_catalog` / OKF 根 `index.md`）；其入口指向存在的文件。
2. 每个语义对象有 `name` + `type`；每个 fact 有 `name/role/grain`；child 的 `parent_fact` 存在。
3. 无悬空引用：fact `dimensions[]`、`dimension:`/`parent_dimension:`/`parent_fact:` 目标均可解析。
4. 无内联枚举/code/字段路径取值（grep 反例：长枚举表、`documented_examples` 代码目录）→ 应在契约层。
5. 每个对象文件有 `evidence_boundary`（catalog 除外）；所有 `TODO(verify)` 已列入交付说明待确认清单。
6. 多 bundle 薄索引（如有）中每个入口路径存在。

## §2 语义 lint

1. **命名一致性** — 同一 business_key 不得对应两个不同名维度；同名维度跨文件定义必须完全一致。
2. **复用** — 新维度与既有 shared-dimension 的 business_key 相同 → 必须引用，不得重定义。

## §3 OKF 硬约束（仅当产物为 OKF bundle）

1. 每个非保留 `.md` 有可解析 YAML frontmatter，且含非空 `type`。
2. `index.md`/`log.md` 符合 `emit-okf.md` §4（根 index 仅 `okf_version`）。

## §4 升级回路

- 可机械修复的 fail（悬空引用、缺 frontmatter 键）→ 修复后重跑本清单。
- 不可机械修复的 fail（如两处 grain 表述冲突）→ **不自行择一**，回 Phase 2 One blocking ask 带候选问用户。
- 任何情况下不得「静默通过」。
