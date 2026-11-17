# COMPAT — storyforge-writing 工作副本说明

本目录是**外部技能的受控副本**，用于优化与产出差异包。**原件的改动必须经用户逐项确认后另行执行**。

## 1. 位置与身份

| 项 | 值 |
| --- | --- |
| 原件（WSL） | `\\wsl.localhost\OpenClawGateway\home\openclaw\.openclaw\agents\main\workspace\skills\storyforge-writing` |
| 工作副本 | `work/storyforge-writing/`（本目录） |
| 原始快照 | `work/_baseline/storyforge-writing/`（v0.1.0 逐字节副本，用于出差异包） |
| 版本基线 git 仓库 | **本工作副本与原件目录都不是 git checkout**（无 `.git`），故差异以**快照对比**方式产出；**发布仓库另存**：`github.com/taosiuman/storyforge-writing`（发布动作走 `publish/` 独立 clone） |
| 上游来源 | `github.com/yuanbw2025/storyforge` → 本地主基线 `H:\storyforge-main`；辅助来源 `H:\StoryForge-master` |
| 原始版本 | v0.1.0（`source_version_baseline: 2026-09-27 (…v1.7.0)`，**已过期**） |
| 当前版本 | **v0.5.0** |

## 2. 基线判定（依据 `REV-20261005-015`）

- **主基线 = `H:\storyforge-main`**，且**改为逐文档记版本**（旧版单一日期 `2026-09-27` 已过期：
  多份权威文档落在 09-28/09-29，施工契约甚至 2026-10-04）。逐文档条目 **10 条**。
- **辅助来源 = `H:\StoryForge-master`**，**仅**用于 "agent 纪律 / 证据分级"；
  该仓库是 Desktop IDE 线（`apps/desktop`+`apps/api`、FastAPI/Tauri、**SQLite**），
  与本技能的浏览器 `Dexie/IndexedDB + schema v10` **不同源**，不得混入数据契约。

## 3. 改动清单（v0.1.0 → 现行）

| 类别 | 改动 | 依据 |
| --- | --- | --- |
| 基线 | 单一日期 → **逐文档版本表**（**10 份**文档）+ `primary_source` / `auxiliary_source` 分列 | `REV-20261005-015` #1、#2 |
| 路由表 | 基线路由表 **8 行** → 现行 **10 行**（新增「小说转剧本」「世界引擎（封存/出口）」）；「漫剧前期」→「漫剧素材前期」；标题行数由脚本实测写入（曾误写为 12 类，`REV-20261005-017` #4） | `REV-20261005-016` #4、#7；`REV-20261005-015` #7 |
| 新增契约 | `contracts/C-screenplay.md`（小说转剧本，含忠实/改编/新增三态与完成判据） | `REV-20261005-016` #4 |
| 新增契约 | `contracts/A-world-engine.md`（worldCode / WorldRelease 字段闭集 / 出口四类 / 分享包） | `REV-20261005-016` #7 |
| 新增契约 | `contracts/S-data-envelope.md`（三注册表登记字段 / 导入导出规则 / **JSON 信封（v0.3.2 已实测，无遗留待实测项）** / 证据分级要求） | `REV-20261005-016` #1–#3 |
| 数据契约 | 三注册表补齐登记字段（`CONTEXT_SOURCES` 7 项 / `adopt()` 6 项 / `PROJECT_TABLES` 7 项）；裁剪三态修正为 `missing`/`omitted`/`partial-selection` | `REV-20261005-016` #6；`REV-20261005-015` #6 |
| 治理红线 | 新增 **证据分级**（`OBSERVED`/`INFERRED`/`UNKNOWN` + 主张与证据等量 + 逐块 provenance） | `REV-20261005-016` #8 |
| 契约加厚 | `A-longform.md`：节点模式**字段闭集**（9 项）+ 图执行前 5 项检查 + **跨模式验收 5 条**；长铗传 70→**90 集**、`scripts/act1-4`→`episode-01..04` | `REV-20261005-016` #5；`REV-20261005-015` #3 |
| 契约加厚 | `A-interactive.md`：补 `AdventureContentV2` **八能力** + 唯一权威写入 `commitAdventureAction`/`commitAdventureNarrativeChoice` + `text-adventure-production/` 入口 | `REV-20261005-015` #4 |
| 来源标注 | `C-post.md` / `B-motion-drama.md` / `SKILL.md`：凡「达芬奇」相关内容一律标注为**环境来源（`INFERRED`）**，非源仓库基线（源仓库 0 命中） | `REV-20261005-015` #5 |
| 机制 | 新增 `scripts/check_consistency.py`（**14 项断言**，含路由↔契约集合一致性、术语一致性、来源标注、契约锚点）—— 断言数轨迹：v0.2.0 = 14 → v0.2.1 +`C4` = 15 → v0.2.2 +`L2` +`V2` = 17 → v0.3.0 +`X1` +`X2` = 19 → v0.4.0 +`E1` = 20 → v0.5.0 +`D1` = **21（现行）** | 同 seedancer 模式 |
| 横切参考 | 新增 `references/schema-tables.md`（机械生成自上游 `src/lib/db/schema.ts` + `src/lib/types/*.ts`；123 张表**完整** store 规格 + 当时 21 张重点表 TS 接口 —— **该 21 表详情已于 v0.3.3 去重**，见下表）。v0.2.2 由独立复审驱动**重生成**：修正 11 处「未找到同名接口」误判、去除 §2 的 110 字符静默截断 | 2026-10-06 实测 |
| 横切参考 | 新增 `references/field-registry.md`（机械生成自上游 `src/lib/registry/field-registry.ts` + `adoption-schema.ts`）：**64 张表 / 528 项可写字段** + 25 项「AI 生成启用」子集 + **53 张集合表**写回策略（identity/去重/必需/盖章/ownerFrom）。补上 SKILL.md「三个单一事实源」中"AI 能写什么"此前只有抽象描述、无逐表清单的缺口 | 2026-10-06 实测 |
| **产物级校验（v0.3.1）** | 新增 `scripts/check_framework_artifact.py`（**由电影大师在长铗传 v0.3.0 → v0.3.1 实战修复中编写并验证**）：校验生成的 framework.json 是否符合契约 —— **6 类违规**（FK 字段类型 / 必需字段 `id`+`projectId` / 枚举闭集 / 顶层结构无 `version` / 旁车 `blockProvenance` 必须是 list / `context-manifest.json` 存在性）+ FK 悬挂与 null 警告。**与技能自检器分工**：`check_consistency.py` 校验**技能包文档自身**（20 项），本校验器校验**产物** | `REV-20261007-030`（实战驱动）|
| **大扫除（v0.3.3）** | **只清理、不加功能**（用户指定范围）：① 删两脚本无用的 `from __future__ import annotations`；② 删 `scripts/__pycache__`；③ 术语统一（`SKILL.md` / `C-post.md` 的旧称「漫剧前期」→「漫剧素材前期」）；④ 去过时表述 4 处（`COMPAT` §3 行、`S-data-envelope` §6 空转项、`README` 已知限制、`SKILL` 子契约列表）；⑤ **`A1` 锚点去耦合**（`待实测` → `精确键集`，避免清理该词时假红）；⑥ **产物校验器表名来源改 §2 单源**（原全文标题扫描 ⇒ 任何 `### 非表名` 都被当合法表 = **假 PASS**）；⑦ **去重**：`README` 路由表/基线表/校验命令（→ 指向 `SKILL` §一/来源与验证、`COMPAT` §4）、`schema-tables.md` §1（21 表详情 → 空存根，内容由 §2 + §4 覆盖，**-15.1 KB**）；⑧ git 仓库措辞澄清（工作副本无 `.git`，发布仓库另存） | 本轮大扫除扫描 + `REV` 复审 |
| **校验器 v4 + 文档瘦身（v0.5.0）** | ① 产物校验器重写：问题以 code 结构化产出；**字段闭集**（记录内 `provenance`/`evidenceGrade` = ERROR，未知字段 WARN/`--strict` ERROR）；**证据复算**（`sf-c14n-v1` 哈希 / `recordCount` / 旁车表双向对齐 / `--sources-root` 对像文件引用验存）；`continuityHandoff` 去重复报错；新增 `planReconciliation` 校验；`context-manifest.json` 结构校验；旁车按 `<stem>` 配对 ② 新增 `scripts/sf_hash.py` `scripts/make_sidecar.py` `examples/minimal/` `tests/run_tests.py` + CI ③ 契约更正：`A-characters` §1 枚举释义、`A-longform` 只读表与章节顺序、`S-data-envelope` §3.1/§3.2 ④ `SKILL.md` 21→14KB，环境约定移入 `references/local-environment.md` ⑤ 自检 +`D1`、`K1` 去下限 | 本轮全面评估（对抗测试复现：多余键 / 伪造哈希 / 错误 recordCount 均曾 PASS） |
| 契约澄清（v0.3.1） | ① `field-registry.md` §4 新增「**只读表**」章节（`temporalFacts` / `narrativeSummaryNodes` 无 FIELD_REGISTRY 条目 —— 系统生成，AI 不写）；② `S-data-envelope.md` §3 明确**旁车文件结构**（`blockProvenance` 必须 list + 5 字段齐备 + `contentHash` 建议 sha256）| 电影大师 `AUDIT-AND-FIX-REPORT.md` §4 |

## 4. 验收

```bash
python scripts/check_consistency.py     # 技能包自检（21 项）；期望：RESULT: PASS (0 fail, 0 warn)
python scripts/check_framework_artifact.py --strict <framework.json>   # 产物校验；期望：TOTAL ERRORS: 0
python tests/run_tests.py               # 回归（金样例 + 反例）；期望：RESULT: N/N passed
```

记录：`generated/storyforge_consistency_p3*.out`（父仓库）。
产物校验实测（2026-10-07）：`广陵散/storyforge-framework.json` → **PASS（18 表 / 0 errors）**；
`长铗传/framework-v0.3.1/*.json` → PASS（27 表 / 0 errors / 41 warnings）。

## 5. 已知限制（如实声明）

1. ~~**JSON 信封的确切字段名仍为 `待实测`**~~ —— ✅ **已解决（2026-10-07，TD-5）**：
   ① 各表**完整字段名与取值域** → `references/schema-tables.md` **§4 全表字段清单**（106 表 / 1734 项）；
   ② 导出数组的**全字段** → `S-data-envelope.md` **§1.1 精确键集**（`project` 9/5 · `works[]` 23/17 · `worlds[]` 9/8）。
   两项均由**读上游源码**取得并**逐条标注出处**；`S-data-envelope.md` §5 **已无遗留 `待实测` 项**。
2. **字段清单的覆盖面（如实声明）**：§4 覆盖 **106 张导出表**，其中 **4 张未解析出字段**
   （上游为交叉类型别名，或接口不在 `src/lib/types/`）—— 这 4 张在 §4 内**逐表标注**「请直接读源文件（本节不推断）」。
   ✅ **AI 可写字段**的逐表清单 → `references/field-registry.md`（64 表 / 528 项）；
   该清单只表示"**允许写入**"，**不**蕴含"可自由生成"（还受作用域/依赖/政策约束）。
3. 契约内容与上游文档的**逐字一致性**不由脚本校验（需人工或上游对比）。
4. 上游文档若再次更新，需人工重读并更新版本表（脚本不检测上游变化）；
   同理两份 `references/*.md` 是**某个时点**的机械快照，上游变更后需重生成。
5. 路由表的**分类语义**（某个产品该归 A 还是 C）无法断言，属判断项。
6. `L2` 只验 `references|contracts|scripts` 三类**本地前缀**的引用存在性；
   裸文件名与上游路径（`src/`、`docs/`）不在其内。
7. `X1`/`X2` 只做**技能内部**自洽（表集合交叉、自述计数）；
   **不**校验 `field-registry.md` 是否仍与上游 `field-registry.ts` 一致（无上游访问能力）。
8. **§4 全表字段清单的生成器已缺失**（v0.3.3，如实声明）：`schema-tables.md` §4 是**机械生成**的，但生成器 `work/regen_sec4_fields.py` 已被另一会话的清理**误删且不可恢复**（`INC-20261007-001`）→ **§4 当前无法重生成**：上游若更新，须**先重建生成器**（逻辑：读 `json-export.ts` 的 `ProjectExportData` 取权威「表→类型」映射 + 解析 `src/lib/types/*.ts` 接口/别名，含继承链展开与取值域提取；旧版实现可参考 `generated/gen_schema_tables*.py` 的接口解析部分，但**其写死 21 张重点表、会复活 §1**，不可直接使用）。手改 §4 时由隐藏断言 `X2` 兜底（自述计数 / §4 ⊆ §2）。
9. **产物校验器的覆盖面边界**（v0.3.1，如实声明）：
   - 它**不**校验"内容是否被编造"（那是证据分级 `OBSERVED`/`INFERRED`/`UNKNOWN` 的职责）；
     v0.5.0 起它**会**复算 `contentHash`（`sf-c14n-v1`）、核对 `recordCount` 与旁车表集合，并在给出 `--sources-root` 时验证来源文件存在（**非文件凭证**如史书卷目 / 作者口述 / 上游代码位置 / 通配简写
    只报 NOTE `EVIDENCE_SOURCE_NONPATH`，不算缺陷 —— 见 §5.10）；
   - 它**不**校验 FK 指向的**语义正确性**（只查"该 id 在**全部表的 id 并集**里存在"，不查"这条引用关系对不对"，
     也**不**校验"id 指向的是不是同一张表"）；
   - 它**不**校验枚举映射的**保真度**（如 `protagonist→main` 是否合理，属判断项）；
   - 悬挂检查**与"该表是否有 `id` 字段"无关**：只要 FK 值是 int 且不属于全表 id 并集就报 `dangling`
     （由独立复审 `REV-20261007-030` F3 更正此前"整表无 id 则跳过"的错误表述）；
   - 旁车键名**非规范**（如历史产物的 `blocks`）只报 **WARN**，不算 error —— 契约规范键名见 `S-data-envelope.md` §3。

  > **已知不一致（`REV-20261007-030` F1）**：`S-data-envelope.md` §3 规定的旁车键名是 `blockProvenance`，
  > 但**广陵散**的历史旁车用的是 `blocks`。校验器对该键报 WARN 而非 ERROR（不改历史产物）；
  > 新产物应统一用 `blockProvenance`。

10. **`--sources-root` 的语义（v0.5.0 起）**：只对**像文件**的引用验存（无通配 / 无空白 / 无冒号 / 扩展名在白名单）。
    旁车 `sources` 同时承载**非文件凭证** —— 史书卷目（`晉書/卷049`）、作者口述（`作者确认（…）`）、
    上游代码位置（`src/lib/types/world-ownership.ts:46`）、通配简写（`knowledge/*.md`）—— 这些只报 NOTE
    `EVIDENCE_SOURCE_NONPATH`。root 按**项目目录**传（`SKILL.md` 执行清单 7）；传错目录会得到「真缺失」ERROR，
    这是**正确**行为（实测：长铗传按项目目录 → 0 缺失；按产物子目录 → 19 条缺失）。
11. **历史产物 `长铗传` 的 2 条真违规（如实登记，不代改）**：`chapters[3]` / `chapters[4]` 的 `planReconciliation`
    被写成**自由文本字符串**，而 `references/field-registry.md` 规定其类型为 `object`（`A-longform.md` §9.1 要求
    五类对账 + `reviewStatus`）。v4 校验器如实报 `RECONCILIATION_SHAPE`(ERROR) ×2 —— **这是校验器生效的证据，
    不是回归**。按治理红线「不改写历史产物」，此处只登记：**新产物必须用对象形态**。

## 7. 发布清单（v0.4.0 显式声明）

**起因**：2026-10-07 首次发布时，ClawHub 实际只收 **19** 个文件，
`.gitattributes` / `.gitignore` / `skill-card.md` 都不在其中 —— 当时**没有显式声明**，
导致我误判过一次 `card.missing`（见 `REL-20261007-001` §4）。

**计入发布包**（根级 6 个 + `contracts/` `references/` `scripts/` `evals/` `examples/` `tests/` 全部）：

```
SKILL.md  README.md  COMPAT.md  CHANGELOG.md  LICENSE  NOTICE.md
contracts/*.md   references/*.md   scripts/*.py   evals/*.json   examples/**   tests/*.py
```

**排除项与理由**：

| 排除 | 理由 |
| --- | --- |
| `.gitattributes` / `.gitignore` | dotfile；ClawHub 打包路径分量不许以点开头（上游 `skill_marketplace/bundle.py:21`） |
| `skill-card.md` | **card 由服务端生成**，不参与文件包 —— **包内没有它属正常**，不是缺陷 |
| `__pycache__/` `*.pyc` | 构建产物 |
| `.github/` | CI 配置（dotfile 目录，同上理由） |

**发布前必跑**：`python generated/sf_release_manifest_k7.py`
（按本节规则算出应发集合，与最近实测的线上清单比对；不一致即退出 2，**须先对齐再发布**）。

## 6. 回写规矩（升级为三层树清单）

- 本副本的改动**不自动回写**；回写前须：① 差等级独立复审通过 ② 用户逐项确认 ③ 原件备份 ④ hash 比对。
- 回写方式：**用三层树清单工具**（`python generated/sf_layers_k7.py`）——
  逐文件 `sha256` 清单 + **基线三方判定**；**冲突必停**（退出 2）并把 WSL 现状备份到 `backups/`，
  **绝不静默覆盖**（本仓已两次因静默覆盖/被覆盖吃亏：`INC-20261006-002`、`INC-20261007-001`）。
  - `--manifest` 只读看状态 ｜ `--apply` 无冲突才写 ｜ `--baseline` 人工确认后接受现状为基线
  -（原件目录无 `.git`，故不使用 `git apply`。）
