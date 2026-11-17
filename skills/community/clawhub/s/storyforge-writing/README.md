# storyforge-writing

把 **StoryForge**（[yuanbw2025/storyforge](https://github.com/yuanbw2025/storyforge)，MIT）的**数据契约 + 写作 SOP + 治理纪律**
蒸馏成一份 **agent 可直接执行**的写作技能：判定任务属于哪类产品 → 读对应子契约 → 生成框架语料 → 按 SOP 推进。

> 本技能包只包含**契约与工作流**，**不包含**上游应用的源代码、也不操作其浏览器运行时。

## 路由：10 类能力 → 子契约

**权威表在 [`SKILL.md`](SKILL.md) §一「产品路由表」** —— 此处**不再复制**（两处台账必然漂移；
断言 `R1`/`R2` 也只以 SKILL.md 的路由表为准）。

横切契约：`contracts/S-data-envelope.md`（数据契约与导入/导出；**全部产品适用**）。

## 基线（逐文档版本，非单一日期）

**权威表在 [`SKILL.md`](SKILL.md)「来源与验证」节**（10 份文档 + `schema.ts`）；机器可读副本是
该文件 frontmatter 的 `metadata.source_version_baseline.documents`。断言 `M2`/`B1` 只以 SKILL.md 为准。

> 旧版曾用单一日期 `2026-09-27` 作基线 —— **已过期**（多份权威文档落在 09-28/09-29）。

## 校验

命令与期望输出见 [`COMPAT.md`](COMPAT.md) §4「验收」（此处不复制，避免两套命令漂移）。

**三件工具，分工不同**（勿混用）：
- `scripts/check_consistency.py` —— 校验**技能包自身**（SKILL.md / contracts / references 的文档一致性）。
- `scripts/check_framework_artifact.py` —— 校验**生成产物**：字段闭集（含旁车字段混入记录）/ 枚举 / 外键与留痕 /
  章节编号 / 后验原语形状 / 旁车证据**复算**（contentHash · recordCount · 表集合）/ `context-manifest.json` 三态。
  问题码全集：`--list-codes`；新产物建议加 `--strict`（兼容期 WARN 升为 ERROR）。
- `scripts/make_sidecar.py` —— 按 `sf-c14n-v1` 生成/刷新旁车（保留已填的 `sources` / `evidenceGrade`）。

回归测试：`python tests/run_tests.py`（金样例 `examples/minimal/` + 每条规则的反例）；CI 见 `.github/workflows/ci.yml`。

21 项断言（摘要，非穷举）：版本戳 / frontmatter / 基线结构 / 路由表↔契约集合（精确）/ 相对路径（链接）/
被引用本地文件存在性（含反引号）/ 横切参考交叉一致 / 参考文件自述计数 / 裁剪三态术语 /
证据分级规则句 / 环境来源逐行标注 / 契约锚点 / 契约实质下限 / 基线自洽 /
provenance 单源 / 体积预算 / 问题码引用↔校验器 / 版本与断言数自洽。

## 三个必须知道的硬事实

1. **产物 ≠ 备份包**：本技能产出的"框架语料"**不含 `version` 字段**，且**不得**把 `provenance` / `evidenceGrade`
   塞进记录内 —— 应用导入走**精确键集**，多余键会被**直接拒收**；证据链放**旁车文件**。
2. **两个版本号不得混用**：`STORYFORGE_SCHEMA_VERSION = 10`（IndexedDB schema）≠
   `CURRENT_BACKUP_VERSION = 14`（备份/导入协议，非 14 即拒）。
3. **证据分级是作者/评审侧纪律**：应用不校验该字段、`adopt()` 不含它 —— **不能指望系统拦住虚构入 Canon**。

## 已知限制

见 [`COMPAT.md`](COMPAT.md) §5 与 `scripts/check_consistency.py` 顶部说明。摘要：
全表字段清单见 [`references/schema-tables.md`](references/schema-tables.md)（**§4：106 表 / 1734 项**，含取值域；
其中 4 表上游为交叉类型、未解析出字段，§4 内已逐表标注）；**AI 可写字段**清单见
[`references/field-registry.md`](references/field-registry.md)（64 表 / 528 项）；
两份 `references/*.md` 是某一时点的机械快照，上游变更后需重生成；脚本不检测上游是否更新；路由分类语义无法断言。

## 归因

- 契约蒸馏自 **[yuanbw2025/storyforge](https://github.com/yuanbw2025/storyforge)**（MIT License）——
  本仓库不包含其源代码，只包含从中提炼的契约与工作流描述。
- "agent 纪律 / 证据分级"部分参考 **StoryForge-master**（Desktop IDE 线）；
  该线与本技能的浏览器 `Dexie/IndexedDB + schema v10` **不同源**，**仅作辅助来源**、不混入数据契约。
- 许可与完整归因见 [`LICENSE`](LICENSE)。

## 版本

v0.5.0 —— 详见 [`CHANGELOG.md`](CHANGELOG.md)。
