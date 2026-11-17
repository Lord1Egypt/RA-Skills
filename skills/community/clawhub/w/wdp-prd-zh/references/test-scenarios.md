# wdp-prd-zh 测试场景

所有场景在临时 scratch 项目目录干跑。每个场景：Setup（准备环境）→ Action（按 SKILL.md 对应命令段落执行）→ Expected（检查不变量）。

## S1 初始化 + 建卡
- Setup: 空 scratch 项目 `dryrun-1/`（无 `.wdp-prd` 指针）。
- Action: 按 SKILL.md「初始化」执行；再按「/wdp-prd-new」创建一个需求。
- Expected:
  1. 创建 `<PRD_ROOT>/<slug>/` 含 `backlog/`、`plans/`、`execution-plan.md`；项目内创建 `docs/superpowers/specs/`。
  2. `.wdp-prd` 内容 = 该全局根绝对路径（`<PRD_ROOT>/<slug>/`）。
  3. `backlog/R-001.md` 存在，frontmatter 字段齐全（id/title/status/priority/depends_on/conflicts_with/created/updated），status=draft。
  4. created 与 updated 均为当天日期。

## S2 列表 + 更新
- Setup: 已有 3 张卡片 R-001(draft,high)、R-002(draft,low)、R-003(confirmed,medium)。
- Action: 执行 `/wdp-prd-list`；再执行 `/wdp-prd-update R-002`（priority 改 high，status 改 confirmed）。
- Expected:
  1. list 输出表格含 id/title/status/priority/依赖，3 行齐全、字段正确。
  2. 行序按 priority 从 high 到 low：R-001(high) → R-003(medium) → R-002(low)；同 priority 再按 created 升序。
  3. update 后 R-002 的 priority=high、status=confirmed，updated=当天。
  4. created 未被改动。
- Action: 执行 `/wdp-prd`（主入口）。
- Expected: 显示 backlog 摘要 + 各命令提示。

## S3 调度报告
- Setup:
  - R-001 confirmed，无依赖，conflicts_with=[R-002]。
  - R-002 confirmed，无依赖。
  - R-005 confirmed，depends_on=[R-002]（依赖 R-002 实际状态 confirmed）。
  - R-007 confirmed，depends_on=[R-099]，R-099 状态 cancelled。
- Action: 执行 `/wdp-prd-dispatch` step 1（仅输出调度状态报告；S3 只观察报告，不挑选、不派发）。
- Expected:
  1. 可立即派发 = [R-001, R-002, R-007]：R-001 与 R-002 互为冲突的一对都列出，但提示「二者冲突，只能挑一个」。
  2. R-005 → 报「⏳ 等 R-002(confirmed) 完成」（依赖 R-002 实际状态为 confirmed，非 in-progress）。
  3. R-007 → 不阻塞（cancelled 依赖视为已满足），列入可派发。

## S4 派发
- Setup: scratch 项目 `dryrun-4/`，git 仓库；R-001、R-002 均 confirmed 无冲突无依赖。
- Action: 执行 `/wdp-prd-dispatch`，挑选 [R-001, R-002]。
- Expected:
  1. 报告正确展示可派发列表；并发上限未超。
  2. 各派发一个后台子代理；R-001/R-002 状态 → in-progress。
  3. `execution-plan.md` 重写：含 in-progress=[R-001,R-002]、可派发=[]、阻塞=[]、冲突=[]。
  4. 子代理返回报告后卡片 → needs-review。
- Action: 非 git 项目重跑 dispatch（或 git 仓库但删除隔离能力）。
- Expected: 明确警告「无法 worktree 隔离，降级为串行/非隔离」，不静默失败。

## S5 全生命周期
- Setup: 单卡片 R-001 从 draft 开始，git 仓库。
- Action: 依次执行 confirm → dispatch → 模拟子代理返回报告 → accept。
- Expected:
  1. draft→confirmed→in-progress→needs-review→accepted→done 全程状态迁移正确。
  2. accept 流程包含：合并 worktree 分支、跑全量测试、code review、呈现给用户确认。
  3. done 后卡片「验收记录」段填写测试结果与 review 结论。
  4. 任一闸门（测试失败 / review 未过 / 用户未确认）→ 不进入 done，回到 needs-review。

## S6 错误分支
- Setup:
  - R-001 与 R-002 均 confirmed 且互相 conflicts_with（同批冲突）。
  - R-003 depends_on=[R-004]，R-004 depends_on=[R-003]（依赖成环）。
  - R-005 depends_on=[R-999]（依赖不存在）。
  - R-008 confirmed，conflicts_with=[R-009]；R-009 为 in-progress（冲突对象开发中）。
  - PRD_MAX_CONCURRENT 调低（如 =0），使本应可派发的卡片被并发上限抑制。
- Action: `/wdp-prd-dispatch` 全部。
- Expected:
  1. 同批冲突 → 提示只挑一个，不静默并行。
  2. 依赖成环 → 明确报告环（R-003↔R-004），不派发。
  3. 依赖不存在 → 报告「依赖 R-999 不存在，检查 depends_on」。
  4. R-008 → 报「⚠ 与 R-009(开发中) 冲突，需等它完成或用户裁定」。
  5. 并发超上限 → 报「已达并发上限，先验收手头的」，被抑制的卡片不出现在可派发列表。
