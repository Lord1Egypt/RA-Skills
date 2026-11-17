# state.md 状态文件 schema

> 本文件供 `workbuddy-skill-assistant` 技能运行时读写，从 SKILL.md 抽出单列，避免主文件臃肿。
> **当前 schema_version: 7**：只保留能指导下一步行动的健康分、12 条核心检查状态、待确认动作和经验采纳记录。旧版本文件见文末「迁移」。
> **v7 变更**：健康分与核心检查达标比是两个独立、可解释的事实输出；旧的四支柱、成熟度、利用度和派生矩阵字段仅作为迁移兼容，不再写入新状态。

## 位置（红线，务必遵守）

- **位置**：本 skill 安装目录内的 `state.md`（与 `SKILL.md`、`reports/` 同目录）。运行时先定位 `SKILL.md` 所在目录 `$SKILL_DIR`，再取 `$SKILL_DIR/state.md`。**勿写死目录名**——skillhub 装为 `workbuddy-skill-assistant__skillhub`，按 name 装为 `workbuddy-skill-assistant`，两者都要能跑。
- **cwd 无关**：自动化可能在任意 cwd 下运行，所有读/写操作一律用 `$SKILL_DIR` 拼出的**绝对路径**，禁止相对路径、禁止写死目录名。
- 本 skill 自管，存于 skill 目录内，不依赖调用方工作目录。

## 字段说明（v4 基础字段）

| 字段 | 类型 | 含义 |
|------|------|------|
| `schema_version` | int | 状态 schema 版本（当前 7）。缺失/过低 → 按「迁移」升级 |
| `first_run` | date | 首次运行日期（YYYY-MM-DD） |
| `onboarding_done` | bool | 初始化引导是否已完成（引导完成时写 `true`） |
| `user_tier` | str | 用户阶段判定结果（三级）：`beginner`（初级）/ `intermediate`（进阶·核心受众）/ `advanced`（高级）。每次检查刷新 |
| `tier_checked_at` | datetime | 上次判定用户阶段的时间戳（YYYY-MM-DDTHH:MM） |
| `last_check` | datetime | 上次检查时间戳（YYYY-MM-DDTHH:MM），静默跳过时也更新 |
| `last_user_activity` | datetime | 上次检测到的用户活动时间戳（YYYY-MM-DDTHH:MM），用于智能窗口跳过 |
| `last_report` | date | 上次落报告的日期 |
| `last_health` | int | 上轮健康评分（供趋势对比） |
| `streak` | int | 连续检查天数（轻量监护节奏统计） |
| `streak_days` | int | 连续活跃天数（有用户活动才算） |
| `checks_run` | int | 累计主动态检查次数（战绩） |
| `issues_found` | int | 累计发现问题数（战绩） |
| `issues_resolved` | int | 累计已修复问题数（战绩，交互态确认后累加） |
| `checklist_score` | int | 上轮最佳实践达标分（0–100，仅由 A 层确定性项计算，用于趋势对比） |
| `checklist_status` | str | 上轮各条 checklist 状态（紧凑 JSON，如 `{"C-mem-01":"pass","C-auto-01":"fail"}`；`pass`/`fail`/`na`） |
| `push_enabled` | bool | 是否开启推送（默认 `true`，主动态默认开启） |
| `push_channel` | str | 推送通道：`agent-mail` / `wecom` |
| `push_status` | str | `ok` / `failed` |
| `push_failed_at` | datetime | 上次推送失败时间 |
| `push_fail_reason` | str | 上次推送失败原因 |
| `pending_actions` | list | 待确认动作队列（见下） |

### 生态与经验字段

| 字段 | 类型 | 含义 |
|------|------|------|
| `catalog_version` | str | 已加载主题积木清单版本（来自 `skill-catalog/core.md` 或 `themes/<theme>.md` 头部），用于漂移检测 |
| `last_catalog_sync` | date | 上次维护 skill 目录的日期；仅维护者工具使用 |
| `ecosystem_coverage_score` | int | 兼容字段；不再作为运行时综合评分 |
| `recommendations_made` | int | 累计给出的 skill 推荐数 |
| `recommendations_adopted` | int | 用户明确采纳的推荐数 |
| `recommendations_rejected` | int | 用户明确拒绝的推荐数 |
| `adoption_rate` | float | 采纳率 = adopted / made，仅作经验参考 |
| `last_self_evolution` | date | 上次经验整理日期 |
| `learnings_count` | int | 累计经验事件数 |

> 已移除（v2 → v3）：`level` / `points` / `badges` / `plan_day` / `plan_started`。游戏化与 30 天带练不再保留。

### v7 变更（精简状态）

| 字段 | 类型 | 含义 |
|------|------|------|
| `health_score` | int | 环境健康分；只表达可观测配置/风险扣分，不与达标比合成 |
| `checklist_score` | int | 12 条核心检查达标率（0–100），用于跨轮趋势 |
| `checklist_status` | str | 各 checklist 项状态的紧凑 JSON |

> v7 不再维护四支柱、成熟度、雷达图或利用度分级历史；自动化/连接器是否真在用仍作为具体 checklist 项的证据与 pass/fail/na 判定。

## 用户阶段判定（user_tier）

由 `scripts/usage_diag.py --json --state <state.md>` 的 `classify_user_tier()` 确定性计算，输出 `tier` + `tier_reasons`（另附 `profile_ready` 画像完整度布尔值，内部用）；agent 只读结果，不自作判断。

**初级用户（beginner）** —— 任一信号命中即判定：
1. `onboarding_done == false`（state.md）
2. 画像不完整：SOUL.md 或 USER.md 缺失 / 过薄（<200 字）
3. 完全未起步：已装 skill = 0 **且** ACTIVE 自动化 = 0

**高级用户（advanced）** —— 初级不命中，且以下**全部**满足：
1. 画像完整（SOUL.md / USER.md 均存在且 ≥200 字）
2. 已装 skill ≥ 15
3. ACTIVE 自动化 ≥ 2
4. 记忆日志新鲜（近 7 天内有更新）

**进阶用户（intermediate）** —— 其余（本 skill 的核心受众）。

> 旧值映射：历史 state.md 中的 `new` → `beginner`、`advanced` → `intermediate`；每次检查由脚本重算刷新，无需手工迁移。

## pending_actions 结构

每条待确认项：

```yaml
- id: a1                      # 唯一 id，交互态确认/移除时引用
  type: install_skill        # 动作类型（见下方「action_type 词汇表」）
  title: 安装 skill-map 可视化 skill 生态   # 给人看的标题
  payload:                    # 动作所需参数
    slug: "@user_7ba94f9e/skill-map"
    source: skillhub
    reason: "checklist C-skill-01 未达标 · skill 精简"
  status: pending             # pending（待确认） / done（已执行） / skipped（用户跳过）
  from_checklist: C-skill-01  # 可选：来源 checklist 项 id，用于追溯
```

> 采纳闭环：下轮检查对比上轮 `pending_actions`——`status: done` 的项计入 `issues_resolved`，
> 并在报告中给"上轮采纳情况"。

## action_type 词汇表（checklist → pending_actions 的协议）

> **定位**：checklist 是「检测器」，`pending_actions` 是「执行器」，`type` 是两者之间的桥。
> 达标检查检出未达标项 → 把该项的 `actions[]` 展开为带 `type` 的待确认项入队 → 交互态确认后执行。
> `install_skill` / `invoke_skill` 的具体目标 skill（slug + 安装 prompt）见 `references/best-practices/toolbox.md`。

| type | 含义 | 边界 |
|---|---|---|
| `install_skill` | 装一个新 skill | 交互态确认；安装前汇总来源/版本/风险；目标与安装 prompt 见 `toolbox.md` |
| `invoke_skill` | 调一个已装 skill 执行（如 skill-check-pro 体检、skill-map 可视化） | 交互态确认；目标见 `toolbox.md` |
| `fix_config` | 修一个配置 / bug（models.json、frontmatter、死链等） | 交互态确认 |
| `reconnect` | 重连 / 配置连接器 | 交互态确认 |
| `enable_automation` | 建 / 启用自动化 | 交互态确认 |
| `write_memory` | 写 SOUL / USER / MEMORY | 交互态确认；主动态绝不写记忆 |
| `run_script` | 跑只读脚本（usage_diag 诊断、渲染报告） | 两态皆可（无副作用） |
| `guide` | 手把手引导（无副作用，教操作） | 交互态 |
| `ask` | 抛问让用户自评 / 确认（checklist B/C 层「无法判定」前的必经步） | 交互态；幂等入队 |
| `upgrade_skill` | 升级一个已装 skill（slug + 新版本；来自 `skillhub upgrade --check-only`） | 交互态确认；批量检查一次，逐条确认 |
| `recommend_skill` | 按画像倾斜主题推荐的未装积木（slug + 二维评分 + workflow_set） | 交互态确认；人工标注优先于自动推断 |
| `maintain_catalog` | 同步/维护主题积木（`skill_catalog.py sync`） | 交互态确认；仅改清单自身 frontmatter，不碰其他 |
| `prune_skill` | 建议移除僵尸/低频 skill（生态检查检出） | 交互态确认；永不主动删除 |
| `revise_skill` | skill 修订提案（模块 ④-3 编译产出：工坊积木/卡路径 + 修订要点 + task_recipe） | 交互态确认后交 skill-rebuild / skill-md-refactor 执行；工坊只编译不改 skill 文件；被拒提案入台账留存 |

## 采纳闭环战绩（精简版，取代 v2 成长系统）

只保留「建议→改善」可见的战绩，不做积分/等级/徽章：

**地基战绩（达标检查）**：

| 字段 | 何时累加 |
|------|----------|
| `checks_run` | 每轮主动态检查 +1 |
| `issues_found` | 每轮 + 本次 issue_count |
| `issues_resolved` | 交互态确认修复 N 项 → +N |

**生态战绩（skill 生态与采纳闭环 · v5 新增）**：

| 字段 | 何时累加 |
|------|----------|
| `recommendations_made` | 模块 ③-4 每推 1 条推荐 +1 |
| `recommendations_adopted` | 交互态确认安装 ③-4 推荐 +1 |
| `recommendations_rejected` | 交互态跳过/拒收 ③-4 推荐 +1 |
| `adoption_rate` | = adopted / made（报告呈现「采纳率」） |

> 报告用一句话呈现："本轮第 N 次检查 · 累计发现 X 项 · 已修复 Y 项 · 连续 Z 天 · 技能推荐采纳率 R%"。

## 完整示例（v7）

```yaml
schema_version: 7
first_run: 2026-08-07
onboarding_done: true
user_tier: intermediate
tier_checked_at: 2026-08-20T11:00
last_check: 2026-08-20T11:00
last_user_activity: 2026-08-20T08:30
last_report: 2026-08-20
last_health: 100
checklist_score: 67
checklist_status: '{"C-mem-01":"pass","C-auto-01":"pass","C-skill-01":"fail","C-skill-02":"fail","C-mem-02":"pass","C-conn-01":"na"}'
streak: 3
streak_days: 2
checks_run: 24
issues_found: 8
issues_resolved: 5
push_enabled: true
push_channel: agent-mail
push_status: ok
push_failed_at: 
push_fail_reason: 
# skill 生态与采纳字段（v5 新增）
catalog_version: 0.1.0-draft
last_catalog_sync: 2026-08-24
ecosystem_coverage_score: 78
recommendations_made: 12
recommendations_adopted: 7
recommendations_rejected: 5
adoption_rate: 0.58
last_self_evolution: 2026-08-20
learnings_count: 18
pending_actions:
  - id: a1
    type: install_skill
    title: 安装 skill-map 可视化 skill 生态
    payload: {slug: "@user_7ba94f9e/skill-map", source: skillhub, reason: "C-skill-01 未达标"}
    from_checklist: C-skill-01
    status: pending
  - id: a2
    type: reconnect
    title: 重连 disconnected 的 qq-mail 连接器
    payload: {connector: qq-mail}
    status: pending
```

## 初始化约定

- 首次运行若 `state.md` 不存在，自动创建并写入（即发布包内 `state.template.md`）：
  - `schema_version: 7`
  - `first_run: <今天>`、`onboarding_done: false`
  - `user_tier: beginner`、`tier_checked_at:`（空）
  - `last_check` / `last_user_activity` 可留空或置今天
  - 战绩字段全部置 0，`checklist_score:`（空）、`checklist_status:`（空），`pending_actions: []`
  - 生态与采纳字段默认空/0：`catalog_version:`（空）、`last_catalog_sync:`（空）、`ecosystem_coverage_score:`（空）、`recommendations_made: 0`、`recommendations_adopted: 0`、`recommendations_rejected: 0`、`adoption_rate: 0`、`last_self_evolution:`（空）、`learnings_count: 0`
- 双态规则见 SKILL.md「双态规则」段：主动态只追加 pending_actions，交互态确认后才执行并从队列移除。

## 迁移

### v3 → v4（历史）

若已存在的 `state.md` 的 `schema_version` < 4：
1. 先备份：`cp state.md state.md.bak-<时间戳>`。
2. 新增字段：`checklist_score:`（空）、`checklist_status:`（空）。
3. 其余字段保留不动（v3 无弃用字段）。
4. 完成后在报告/日志标注"状态 schema 已从 v3 迁移到 v4"。

### v2 → v3（历史）

若已存在的 `state.md` 的 `schema_version` < 3：
1. 先备份：`cp state.md state.md.bak-<时间戳>`。
2. 删除弃用字段（不再保留）：`level`、`points`、`badges`、`plan_day`、`plan_started`。
3. 新增字段：`user_tier: beginner`（待下次检查刷新）、`tier_checked_at:`（空）。
4. 原 `push_*`、战绩字段、`pending_actions` 保留不动。
5. 完成后在报告/日志标注"状态 schema 已从 v2 迁移到 v3"。

### v4 → v5（当前）

若已存在的 `state.md` 的 `schema_version` < 5（v5 升级时）：
1. 先备份：`cp state.md state.md.bak-<时间戳>`。
2. 新增 v5 字段（默认空/0）：`catalog_version:`、`last_catalog_sync:`、`ecosystem_coverage_score:`、
   `recommendations_made: 0`、`recommendations_adopted: 0`、`recommendations_rejected: 0`、
   `adoption_rate: 0`、`last_self_evolution:`、`learnings_count: 0`。
3. `schema_version` 升到 5。
4. 其余 v4 字段全部保留不动。
5. 完成后在报告/日志标注"状态 schema 已从 v4 迁移到 v5（生态与采纳字段已启用）"。

### v6 → v7（当前）

若已存在的 `state.md` 的 `schema_version` < 7：
1. 先备份一次：`cp state.md state.md.bak-<时间戳>`；备份只用于迁移回滚，不纳入发布包。
2. 删除旧评分字段：`a_p1..a_p4`、`b_p1..b_p4`、`c_p1..c_p4`、`pillar_1..pillar_4`、`composite_score`、`maturity_level`、`last_utilization_check`、`score_history`。
3. 保留 `health_score`、`checklist_score`、`checklist_status`，并将 `schema_version` 升到 `7`。
4. 旧 `composite_score` 不折算为新健康分；新一轮诊断后由脚本重新写入事实字段，避免混淆两种口径。
5. 在报告/日志标注"状态 schema 已从 v6 迁移到 v7（精简评分字段）"。
