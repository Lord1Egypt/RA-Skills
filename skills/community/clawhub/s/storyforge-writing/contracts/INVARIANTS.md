# INVARIANTS — 不变量 ↔ 断言 对照表（v0.5.0）

> **纪律**：每份契约的「所有权 · 不变量 · 禁止项」节里，每条 `INV-*` 都必须**至少被一条断言覆盖**；
> 本表是**双向索引**：断言侧改动（增删/改名）必须同步此表。
> 断言实现位置：`scripts/check_consistency.py`（技能包自检，21 项）与
> `scripts/check_framework_artifact.py`（产物校验，`--json` 输出稳定 `code`，全集见 `--list-codes`）。
> 每个产物校验码都有正例 + 反例回归：`tests/run_tests.py`。本表引用的问题码由自检 `D1` 核对其真实存在。

## 1. 不变量 → 断言

| 不变量 | 覆盖它的断言 / 检查 | 位置 |
| --- | --- | --- |
| `INV-C-1` 字段 ∈ 登记集 | 产物校验 `FIELD_UNKNOWN` / `FIELD_NOT_WRITABLE`（默认 WARN，`--strict` ERROR）+ `TABLE_UNKNOWN`；自检 `X1` | `check_framework_artifact.py` / `check_consistency.py: X1` |
| `INV-C-2` 枚举取闭集值 | 产物校验 `ENUM_VIOLATION` | `check_framework_artifact.py` |
| `INV-C-3` 关系两端可解析 | 产物校验 `FK_DANGLING`（未登记即 ERROR） | 同上 |
| `INV-I-1` 八能力齐备 | **人工/评审**（本技能不解析 HTML 产物）—— 已声明为**未机器化** | — |
| `INV-I-2` 只经官方写入 API | **人工/评审**（属上游实现约束，非本技能产物形态） | — |
| `INV-I-3` 跑团世界只读 | 契约文字 + 人工评审 | `A-interactive.md` §2 |
| `INV-L-1` 九块覆盖 | 自检 `A1`（契约锚点）+ 人工 | `check_consistency.py: A1` |
| `INV-L-2` 章节 id 整数 / order 唯一 | 产物校验 `CHAPTER_ID_NOT_INT` / `CHAPTER_ORDER` | `check_framework_artifact.py` |
| `INV-L-3` 引用可解析或留痕 | 产物校验 `FK_DANGLING`（已登记 → WARN） | 同上 |
| `INV-L-4` 后验先于下一章 | **流程语义**，无机器断言（§9 文字 + 行为评估 `evals/behaviour.json` #1/#5） | `A-longform.md` §9 / `evals/` |
| `INV-L-5` provenance 只在旁车 | 自检 `C4` + 产物校验 `SIDECAR_FIELD_IN_RECORD` / `SIDECAR_SHAPE` | `check_consistency.py: C4` / `check_framework_artifact.py` |
| `INV-L-6` 后验原语形状（§9.1） | 产物校验 `HANDOFF_SHAPE` / `RECONCILIATION_SHAPE` / `RECONCILIATION_UNCONFIRMED` | `check_framework_artifact.py` |
| `INV-W-1` WorldRelease 不可变 | 契约文字 + 人工评审 | `A-world-engine.md` §1 |
| `INV-W-2` 出口包只读 / 新副本 | 契约文字 | `A-world-engine.md` §4 |
| `INV-W-3` 不代替上游运行时 | 自检 `C4` 的边界句 + 契约文字 | `check_consistency.py: C4` |
| `INV-BC-1` 字段闭集 | 产物校验 `TABLE_UNKNOWN` / `ENUM_VIOLATION` | `check_framework_artifact.py` |
| `INV-BC-2` B 类只视觉化 | 自检 `R1`/`R2`（路由↔契约集合）+ 人工 | `check_consistency.py: R1/R2` |
| `INV-BM-1` 主链严格顺序 | 契约文字 + 人工评审 | `B-motion-drama.md` §1 |
| `INV-BM-2` Prompt IR provider-neutral | 契约文字 | `B-motion-drama.md` §3 |
| `INV-BM-3` 完成层级两级 | 自检 `A1` 锚点（"不静默忽略"/"物料"/"Prompt IR"） | `check_consistency.py: A1` |
| `INV-BM-4` 不静默忽略 | 自检 `A1` 锚点 | 同上 |
| `INV-CP-1` 交接物带版本 + hash | 契约文字 + 人工 | `C-post.md` §2 |
| `INV-CP-2` 媒资走 Blob 纪律 | 契约文字 | `C-post.md` §5 |
| `INV-CP-3` 完成门两级 | 自检 `A1` 锚点（"完成门"） | `check_consistency.py: A1` |
| `INV-CS-1` 改编三态逐处标注 | 自检 `A1` 锚点（忠实保留/合理改编/新增假设）+ 人工 | `check_consistency.py: A1` |
| `INV-CS-2` 剧本版本不可变 | 自检 `A1` 锚点（"不可变剧本版本"） | 同上 |
| `INV-CS-3` 生产链严格顺序 | 契约文字 | `C-screenplay.md` §2 |
| `INV-S-1` 不含 `version` | 产物校验 `TOP_LEVEL_VERSION` | `check_framework_artifact.py` |
| `INV-S-2` provenance 只在旁车 | 自检 `C4` + 产物校验 `SIDECAR_FIELD_IN_RECORD`（ERROR） | 两者 |
| `INV-S-3` 有记录必须有来源（显式 ≠ 空） | 产物校验 `EVIDENCE_SILENT_ABSENT` / `EVIDENCE_ABSENT_DECLARED` / `EVIDENCE_SOURCE_MISSING`（`--sources-root`，仅对像文件的引用）/ `EVIDENCE_SOURCE_NONPATH`（非文件凭证，NOTE） | `check_framework_artifact.py` |
| `INV-S-4` 精确键集 | 契约 §1.1 + 产物校验 `FIELD_UNKNOWN`（记录级；`project`/`works[]` 信封级键集只在按备份格式交付时适用，本技能不产出） | `S-data-envelope.md` §1.1 |
| `INV-S-5` 悬空须留痕 | 产物校验 `FK_DANGLING` / `FK_DANGLING_DECLARED` | `check_framework_artifact.py` |
| `INV-S-6` 证据可复算 | 产物校验 `EVIDENCE_HASH_MISMATCH` / `EVIDENCE_HASH_UNVERIFIABLE` / `EVIDENCE_COUNT_MISMATCH` / `SIDECAR_TABLE_ORPHAN` / `SIDECAR_TABLE_UNCOVERED` | `check_framework_artifact.py` |
| `INV-S-7` context-manifest 三态 | 产物校验 `SIDECAR_MISSING` / `MANIFEST_INVALID` / `MANIFEST_LEGACY` | `check_framework_artifact.py` |
| `INV-L-7` 不写只读表 | 产物校验 `TABLE_NOT_WRITABLE`（默认 WARN，`--strict` ERROR） | `check_framework_artifact.py` |

## 2. 断言 → 不变量（反向：无对应不变量的断言）

| 断言 | 说明 |
| --- | --- |
| `V1` 版本戳 / `M1` frontmatter / `M2` 基线结构 | **元数据完整性**，非领域不变量 |
| `R3` references 无孤儿 / `L1`/`L2` 引用可解析 | **仓库卫生**，非领域不变量 |
| `X2` 自述计数一致 / `K1` 体积预算 | **文件自洽**，非领域不变量 |
| `D1` 问题码引用 ↔ 校验器 | 文档与校验器代码一致（防「声称有覆盖、实际没有」） |
| `B1` 基线表 ↔ frontmatter | 元数据一致性 |
| `V2` 版本与断言数自洽 | 元数据一致性 |
| `E1` 行为评估集结构 | **行为层**（对应 M8 机制；其 `expectations` 覆盖 `INV-L-4` 等流程类不变量） |

## 3. 未机器化的不变量（如实声明）

`INV-I-1` `INV-I-2` `INV-I-3` `INV-L-4` `INV-W-1` `INV-W-2` `INV-BM-1` `INV-BM-2`
`INV-CP-1` `INV-CP-2` `INV-CS-3` —— 其中**流程/实现类**由文字纪律 + 行为评估集
（`evals/behaviour.json`）覆盖；**产物形态类**（如 `INV-I-1`）依赖人工评审。
**这些不宜假装有断言。**
