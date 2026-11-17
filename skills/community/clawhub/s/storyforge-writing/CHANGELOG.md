# Changelog — storyforge-writing

本项目版本独立于上游 StoryForge 的版本号；上游基线以**逐文档版本**记录（见 `SKILL.md`《来源与验证》）。

## v0.5.0 — 2026-10-16

### 全面评估后的修复：让校验器真的拦得住它声称拦得住的东西

> 起因：对抗测试复现了三类**假 PASS** —— ① 记录里塞 `provenance` / `evidenceGrade` / 编造字段；
> ② 旁车写 `sha256:deadbeef`、`recordCount: 999`（实际 1 条）、指向不存在的来源；③ 旁车登记的表与主文件对不上。
> v0.4.0 的 `check_framework_artifact.py` 对三者都输出 `PASS / 0 errors`，而 `INVARIANTS.md` 声称 `INV-C-1` / `INV-S-2` 已有机器覆盖。

**产物校验器 v4**（`scripts/check_framework_artifact.py`）
- 问题以 `(level, code, field_path, message)` **结构化产出**；`--list-codes` 列出全部 44 个问题码；`--json` schema 升为 `storyforge.artifact-check.v2`。
- **字段闭集**：记录内 `provenance` / `evidenceGrade` → **ERROR** `SIDECAR_FIELD_IN_RECORD`；不在数据模型（schema-tables §4）的字段 → `FIELD_UNKNOWN`；
  在模型中但未登记可写 → `FIELD_NOT_WRITABLE`；写只读表 → `TABLE_NOT_WRITABLE`。
- **证据复算**：按 `sf-c14n-v1` 复算 `contentHash`（声明规范化时不一致 = ERROR）；`recordCount` 必须等于实际条数；
  旁车表 ↔ 主文件表**双向**对齐；`--sources-root` 下对**像文件**的引用逐个验存（非文件凭证只报 NOTE，见下）。
- **`--strict`**：所有「兼容期 WARN」（未知字段、未声明规范化的哈希失配、旧形态 manifest、旁车漏表、写只读表）升为 ERROR。
  **默认不加 `--strict`，历史产物（广陵散 / 长铗传）不会因本次升级突然 FAIL**；新产物建议一律加。
- 修复：`continuityHandoff` 校验写在逐字段循环里，每多一个字段就重复报一遍（实测 2 个问题报成 12 条）。
- 新增：`planReconciliation` 五类对账 + Item 证据 + `reviewStatus` 闭集；非 `pending` 却无 `reviewedAt` → `RECONCILIATION_UNCONFIRMED`。
- 新增：`context-manifest.json` 必须是合法 JSON 对象；`entries[]` 的 `state` 取三态闭集，裁剪项必须写 `reason`。
- 旁车按 `<stem>.provenance.json` 配对（此前把目录里**所有**旁车套到每个产物上）。

**交付前修复（v0.5.0 复核发现）**：`--sources-root` 曾把旁车里的**非文件凭证**当成文件路径去验存 ——
史书卷目 `晉書/卷049`、作者口述 `作者确认（杜小文 2026-10-06）`、上游代码位置
`src/lib/types/world-ownership.ts:46 (Work)`、通配/范围简写 `knowledge/*.md` / `episode-01..04.md`、
推导说明 `故事逻辑推导` —— 实测把**长铗传 29 条、广陵散 12 条**合法引证报成 ERROR。
现由 `_is_checkable_path()` 判定：只有「无通配 / 无空白 / 无冒号 / 扩展名在白名单」的引用才验存，
其余的降为 **NOTE** `EVIDENCE_SOURCE_NONPATH`（不误报、也不静默丢弃；`--json` 里可逐条审计）。
**形如文件的引用照旧验存** —— 修假红不等于放过真缺失（`tests/run_tests.py` 有配对反例）。

**新增工具与样例**
- `scripts/sf_hash.py`：规范化哈希单一实现（生成与校验共用）。
- `scripts/make_sidecar.py`：生成/刷新旁车，保留已填的 `sources` / `evidenceGrade` / `notes`；新表默认 `UNKNOWN` + 空来源（逼作者补证据，不替人编）。
- `examples/minimal/`：`--strict` 下 0 error / 0 warn 的金样例（主文件 + 旁车 + manifest + 来源 md）。
- `tests/run_tests.py`：金样例 + **30 个反例**（每个规则至少一个）+ `make_sidecar` 幂等 + 自检；`.github/workflows/ci.yml` 在 push / PR 时运行。

**契约更正**
- `A-characters.md` §1：枚举释义与 `field-registry.md` 冲突 —— `orderAxis` 是阵营·秩序轴（`lawful/neutral/chaotic`），**不是**出场顺序；
  `roleWeight` / `moralAxis` / `narrativeStatus` 改为闭集英文值。
- `A-longform.md`：§2 不再让 AI 写只读表 `temporalFacts` / `narrativeSummaryNodes`；章节顺序理顺（7→8→9→9.1→10）；补定义 `INV-L-6`、新增 `INV-L-7`。
- `S-data-envelope.md`：新增 §3.1 规范化哈希 `sf-c14n-v1`、§3.2 `context-manifest.json` 结构；新增 `INV-S-6` / `INV-S-7`。
- `INVARIANTS.md`：覆盖表与真实问题码对齐；`INV-S-4` 不再自相矛盾地写「真实导出样本仍缺」。
- `field-registry.md` §4：`factId` 不再建议「填 0」（0 会被判悬空）。

**SKILL.md 瘦身（21.0 KB → 13.7 KB）**
- 版本史、REV 编号、重复的基线说明移出；环境专属约定（本地 `H:\` 路径、`ai-memory`、白名单项目、达芬奇〔环境来源〕规则）移入**可选**的 `references/local-environment.md`。
- 新增「文件模式」对照表：上游应用内的 `adopt()` / stale / 下游失效在文件交付下分别对应什么。
- 连续性检查从剧本专用措辞改为通用，并只保留一处。
- description 补「不用于」边界；路由补「剧本 / 漫剧」易混淆说明。

**技能包自检 v5**（`scripts/check_consistency.py`，20 → **21 项**）
- 新增 `D1`：文档引用的问题码必须在校验器 `--list-codes` 中存在；当前态文档不得再写过时的「覆盖 6 类违规」。
- `K1`：去掉「contracts 总量 ≥20KB」下限（体积下限只会奖励写长），SKILL.md 预算收紧到 ≤16KB。
- `V2`：额外核对 COMPAT §4 / INVARIANTS 中的「技能包自检 N 项」（v0.4.0 的 COMPAT 写 19 项未被发现）。
- `L2`：本地前缀增加 `examples/`、`tests/`。

**行为评估**：7 → 10 条（新增路由「剧本 ≠ 后期」、字段闭集与旁车、改记录后必须刷新旁车）。

#### 迁移说明
- 历史产物：默认模式下不会新增 ERROR，但可能新增 WARN（`FIELD_UNKNOWN`、`EVIDENCE_HASH_UNVERIFIABLE`、`MANIFEST_LEGACY` 等）——这是**让偏离可见**，不要求改写历史产物。
  例外：`recordCount` 与实际不符、旁车登记了主文件没有的表、记录内混入 `provenance` / `evidenceGrade`、`context-manifest.json` 不是合法 JSON 属客观错误，默认即 ERROR。
- 新产物：`make_sidecar.py --write` → 补 `sources` → `check_framework_artifact.py --strict`。

## v0.4.0 — 2026-10-07

### 对标 `alikon-art/DeterminFlow` 后的定向迭代（批 1）

> 对标结论见 `reports/audits/2026-10-07-determinflow-benchmark-and-v040-proposal.md`。
> 原则：**不引入运行时** —— 它的每条机制，我们都用「契约 + 断言 + 校验器」表达同等语义。

**新增：行为评估集（T1）** —— 此前 19 项断言只查**文档自洽**，查不出「技能被使用时会不会
把『启动了』说成『完成了』」。新增 `evals/behaviour.json`（**7 条**，含 **1 条反例**），
每条 = `prompt` + `expected` + **可判定的 `expectations[]`**；新增断言 **`E1`** 校验其结构完备
（≥6 条 / 每条 4 段 / ≥2 条判据 / 含反例）。**断言总数 19 → 20**。

**新增：编号与引用完整性（T7）** —— 依据上游事实（`chapters` 以**数字 id** 标识、以 **order** 排序）：
- `chapters.id` 用字符串代号（如 `ep30`）→ **ERROR**；`order` 非整数或重复 → **ERROR**
- 外键悬空且**未登记** → **ERROR**；已在旁车 `unresolvedRefs` 登记 → **WARN**
- 契约：`contracts/A-longform.md` **§8**（依据「**缺失 ≠ 空**」：未解析引用必须显式留痕）
- 直击历史问题：长铗传 chapters 只到 ep30 却 FK 引用到 ep90

**新增：证据门槛（T2）** —— `evidenceGrade` 闭集 · `contentHash` 形态 · `sources` 元素须含来源标记 ·
**有记录必须有来源**（`recordCount>0` 且 `sources` 空时**必须用 `notes` 显式声明原因**；
既无 `sources` 也无 `notes` = **静默缺失 → ERROR**）。
`contracts/S-data-envelope.md` §3 补充**实测的两种合规 sources 形态**。契约：`SKILL.md` §六 第 10 条。

**新增：发布清单显式化（T6）** —— `COMPAT.md` **§7** 声明计入/排除项与理由
（`.gitattributes`/`.gitignore` 因是 dotfile；**`skill-card.md` 由服务端生成、不进文件包**）；
发布前跑 `generated/sf_release_manifest_k7.py` 做**声明 vs 实测**集合校验。

**新增：三层副本树清单（T5）** —— 回写工具升级为逐文件 `sha256` + **基线三方判定**：
本地领先才写；**对方改动/双方都改 = 冲突必停**（退出 2 + 备份），**绝不静默覆盖**。契约：`COMPAT.md` §6。

#### ⚠️ 两次被真实参照物纠正（如实记录）
初版 T2 按**契约示例**写「`sources` 必须非空」，实测**把两个真实产物全判错**：
① 广陵散 5 个块 `sources: []` 但**已用 `notes` 显式声明**（`INFERRED`）→ 产物对、断言错；
② 长铗传的形态是 `{key,evidence,sources:[...]}`，与示例 `{md,revision,grade}` 不同。
→ 定稿规则：**ERROR 只留给「有记录 + 无 sources + 无 notes」的静默缺失**。
**教训**：断言必须先对**真实参照物**验证（METHOD 律 4）。

#### 验证
- T7/T2 反例自测 **9/9** · E1 反例自测 **5/5** · T5 triage 自测 **8/8**
- 真实产物：广陵散 PASS(0 err / 5 说明性 WARN) · 长铗传 v0.3.1 PASS(0 err / 41 warn)
- 技能自检器 PASS（20 项）

## v0.3.3 — 2026-10-07

### 大扫除（**只清理、不加功能**；用户指定范围：死代码 / 重复逻辑）

**扫描**（5 遍，含实证；无死代码发现，问题集中在**重复**与**过时**）：

- **P1 产物校验器表名来源不可信（假 PASS）**：`parse_schema_tables()` 在 §2 表格行之外
  **又做了一次全文** `### <反引号>表名` 标题扫描 ⇒ 任何形如 `### <反引号>非表名` 的标题都被当成
  **合法表名**（实测：注入假标题后产物用该名**不报错**）；且 §2 定位硬编码 `split("## 2.")`，
  标题改形时**静默退化为全文扫描**。
  → 改为 **§2 单源** + 节号/关键词正则定位 + **找不到即报错**；并核对标题自述张数
  （`123` 不再是不可验证的宣称）。配 **5 例自测**（正例 2 + 反例 3）全部符合期望。
- **P2 过时表述 4 处**：`COMPAT` §3 行的「JSON 信封 + 待实测项」、`S-data-envelope` §6 的
  「列出所有 `待实测` 项」空转项、`README` 已知限制仍称"仍需真实导出样本"、`SKILL` 子契约列表
  「含待实测项」。
- **P3 断言与文档耦合**：`A1` 锚点要求契约含字面量 `待实测` ⇒ 清理该词即**假红**。
  → 换为稳定词 `精确键集`（**必须与 P2 同批**）。
- **P4/P5**：删两脚本无用的 `from __future__ import annotations`（0 注解、0 PEP585/604 用法）；
  删 `scripts/__pycache__`（构建残留，且已随 v0.3.2 回写进原件）。
- **P6/P7 文档重复**：`README` 与 `SKILL` 有 **7 个块**完全重复（路由表 2 + 基线版本表 5），
  README 非空行 **23% 与 SKILL 逐字相同**；`README` 与 `COMPAT` 的校验命令块亦重复。
  → README 三处改为**指向权威源**（路由表 → `SKILL` §一；基线表 → `SKILL` 来源与验证；
  校验命令 → `COMPAT` §4）。去重后**与 SKILL 的相同行 = 0**，66 → 43 非空行。
  断言影响已先核实：`R1`/`R2`/`M2`/`B1` 只读 `SKILL.md`；`V2` 需要的「N 项断言」字样**保留**在 README。
- **P8 参考文件内部重复**：`schema-tables.md` §1（21 张重点表详情，**已被 §2 的 store 规格与
  §4 的字段清单完全覆盖**）→ 换为**空存根**（保留节号，令既有引用仍可解析），**-15.1 KB**
  （98.3 KB → 82.3 KB）。
- **P9 措辞张力**：`COMPAT` 称"该技能不是 git 仓库" ↔ `README` 称"本仓库" ↔ 技能**已发布**
  `github.com/taosiuman/storyforge-writing`。→ 澄清为：**工作副本/原件目录无 `.git`**（故用快照对比），
  **发布仓库另存**；`README` 的"本仓库"→"本技能包"。
- **P10 术语**：`SKILL.md` 与 `contracts/C-post.md` 的旧称「漫剧前期」→「漫剧素材前期」。

**未做（如实声明）**：
- **未发现死代码**（常量/正则/函数均有引用，无不可达代码）；
- 扫描器曾误报"`K1` 重复注册"，实为 `if/else` **互斥分支**（运行时只注册 1 次，断言仍 19 项）——**已撤回**。

**验证**：`check_consistency.py` PASS（19 项）· 产物校验器 5 例自测全过 · 真实产物
（广陵散 / 长铗传 v0.3.1）仍 PASS · 两脚本语法与行为等价性已复测。


#### v0.3.3 的独立复核处置（`REV-20261007-034`，判定 PASS with warnings）

- **M-bypass（残留旁路，已修）**：原实现在 §2 定位上取**首个**命中 —— 在真 §2 **之前**插入
  一个同名关键词的伪造节即可旁路（实测：伪表名假 PASS、真表名假红）。
  → 改为**必须唯一命中**（命中数 ≠ 1 即报错退出 2）；**自述张数缺失**也不再静默跳过。
  复核方给的 2 个复用例 + 正例，**3/3 全部拦住**。
- **失实声明（已修）**：本文件 v0.3.2 条目与 `scripts/check_consistency.py` 注释曾称生成器
  `work/regen_sec4_fields.py` **已归档/可重跑** —— 该脚本已被另一会话的清理**误删且不可恢复**
  （`INC-20261007-001`）。→ 改为事实陈述，并在 `COMPAT.md` §5 登记为**技术债**。
- **过时数字（已修）**：`contracts/S-data-envelope.md` 的两处版本示例仍写 `0.3.2` → `0.3.3`
  （该文件不在 `V2` 的扫描范围内，属**无人守护的过时数字**，已如实记录）。

## v0.3.2 — 2026-10-07

### 定位澄清：**技能不再依赖任何应用**（用户裁定）
- 用户明确：「本技能**不再依赖任何应用**；语料只当写作素材」。
- 据此修正文档里 **11 处**"依赖应用"的表述（此前写作"可导入 StoryForge /long 作品库""导入由用户在应用内执行"）：
  `SKILL.md` ×3（使用场景 / compatibility / **§五 导入行**）· `contracts/S-data-envelope.md` ×3（§3 对比表 / **§5 导入路径项** / §6 交付清单）·
  `CHANGELOG.md` ×1（v0.2.1 条目的一处标注）· `skill-card.md` ×4（Canon ×2 / application ×2）。
  > 其中 **2 处漏网**（`SKILL.md` §五、`S-data-envelope.md` §5）由独立复审 `REV-20261007-032` 抓出并补修。
- **未改**：技能"蒸馏自 StoryForge 仓库的契约"这一**归因**（那是事实与许可要求）。

### 数据契约补全（TD-5a / TD-5b）
- **新增 `schema-tables.md` §4「全表字段清单」**（**机械抽取**；生成器为 `work/regen_sec4_fields.py`，**该脚本已被另一会话的清理误删且不可恢复** → 见 `INC-20261007-001`；**§4 当前不可重生成**）：
  **106 表 / 1734 项字段**，每表标注接口名、字段数、**导出 `Omit` 差异**；96 个字段带**取值域** `⟨…⟩`（枚举闭集）。
  **已知缺口（如实标注）**：其中 **4 张表未解析出字段**（上游为交叉类型别名，或接口不在 `src/lib/types/`）——
  这 4 张表在 §4 内**逐表标注**"未解析到字段，请直接读源文件（本节不推断）"，**非**全覆盖。
  来源：`json-export.ts` 的 `ProjectExportData`（权威「表→TS 类型」映射）+ `src/lib/types/*.ts`（含继承链展开）。
- **新增 `S-data-envelope.md` §1.1「精确键集」**：`project` 9 允许/5 必需 · `works[]` 23/17 · `worlds[]` 9/8，
  另 8 条预检约束，**逐条带行号出处**（`backup-trust.ts`）。
- **新增断言守护**（`check_consistency.py` 的 `X2` 扩展）：§4 自述表数 = 实际小节数；
  §4 表名必须都在 §2 表清单内（防"生成器把非表键当表写"，如 `version`/`project`）；§4 无重复表名。
  **首版守护被独立对抗单元证伪**（`REV-20261007-033`：27 变异 → **11 漏网 + 2 假红**），据此重写：
  ① **不硬编码节号字面量**（旧版 `split("## 4.")` 在标题改形时**整段守卫静默跳过**）→ 改节号+关键词正则定位，**找不到即报错**；
  ② 小节正则**容忍空白**（`###  \`x\`` / 前导缩进 / 全角空格在 CommonMark 下均为合法 H3）；
  ③ 先**剥离围栏代码块与 HTML 注释**（防"样例被当真"假红）；④ 标题级别放宽到 3–6 级（防 `####` 藏假表名）。
  配 **12 例自测**（`generated/_selftest_sec4.py`：正例 + 10 反例 + 1 容忍例），全部符合期望。

### 关闭项（用户裁定）
- **TD-5c 关闭**：媒资（图片）在备份包里的表示 —— 属《长铗传》项目的额外需求、由其它技能承担，与本技能无关。
- **TD-5d 关闭**：语料导入路径 —— 用户裁定选 (b)，技能不依赖应用，**不写转换器**。

## v0.3.1 — 2026-10-07

### 新增产物级校验器（电影大师实战反馈）
- **新增 `scripts/check_framework_artifact.py`**：校验生成的 framework.json 是否符合契约。
  覆盖 6 类违规：FK 字段类型（必须 number）/ 必需字段（id + projectId）/ 枚举闭集 / 顶层结构（无 version 字段）/ 旁车结构（blockProvenance 必须是 list）/ context-manifest 存在性。
  由电影大师在长铗传 v0.3.0 → v0.3.1 修复过程中编写，后提升进技能包。
- **新增 `field-registry.md` §4 "只读表"章节**：说明 `temporalFacts` 和 `narrativeSummaryNodes` 两张表为什么没有 FIELD_REGISTRY 条目（由系统自动生成，AI 不可写）。
- **明确 `S-data-envelope.md` §3 旁车文件结构**：`blockProvenance` 必须是 list（不是 dict），每项必须有 5 个字段（table / recordCount / contentHash / evidenceGrade / sources）。

### 检查器修复
- **X2 断言边界修复**：`§3` 的切分原为"取到 EOF"，加入 §4 后会把只读表两行算进 §3（53 ≠ 55 误报）；
  现改为"取到**下一个二级标题**之前"（不硬编码节号）。配 4 例自测（`generated/_selftest_x2.py`，含 2 反例 1 对照）。

### 契约矛盾澄清
- **`knowledgeLedger.factId → temporalFacts`**：FK 指向的表无 FIELD_REGISTRY 条目。这是上游 StoryForge 的设计决策（temporalFacts 由系统生成），不是技能缺陷。AI 生成时通常留空或填 null。
- **`id-map.json` 入约**：FK 数值化必须配"稳定 id 映射"旁车，否则重排即断链。长铗传 v0.3.1 已实践此模式。

### 独立复审处置（`DISPATCH-20261007-019` / `REV-20261007-030` + `031`）
- **F2（material，已修）**：校验器表索引 **121 ≠ 123** —— `importFiles` / `referenceAnalysisSources` 的 store 定义不以 `++id` 开头，旧正则漏掉 → 这两表的产物会被**误报**假 ERROR。已改为按 §2 表格行解析（实测 123）。
- **F1（material，已处置）**：契约规定的旁车键名 `blockProvenance` 与**广陵散历史产物**的 `blocks` 不一致 → 契约 §3 补"历史不一致"说明；校验器把非规范键名由 NOTE 升为 **WARN**（不改写历史产物）。
- **U4 #1（已修）**：路径不存在时抛**未捕获 `FileNotFoundError`** 且退出码 1 与"业务 FAIL"同码 → 现为友好提示 + 退出码 **2**，并打印 `ABORTED`（不再打印误导性的 `TOTAL ERRORS: 0`）。
- **F3（已更正）**：`COMPAT.md` 原称"整表无 `id` 则跳过其 FK 检查"**不实** → 实测仍报 `dangling`（悬挂检查用**全表 id 并集**）。已按实测更正。
- **F4/F6（已修）**：`S-data-envelope.md` 示例残留 `0.3.0` → 更新为 `0.3.1`；本条 CHANGELOG 补记 X2 修复（此前漏记）。

### 断言数
- 技能自检器（`check_consistency.py`）：**19 项**（未变）
- 产物校验器（`check_framework_artifact.py`）：**新增**，独立于技能自检器

## v0.3.0 — 2026-10-06

### 补齐覆盖缺口（"AI 能写什么"此前只有抽象描述）
- **新增 `references/field-registry.md`**（机械生成自上游 `src/lib/registry/field-registry.ts` 799 行 +
  `adoption-schema.ts` 1049 行）：
  - §1 `FIELD_REGISTRY` — **64 张表 / 528 项**可写字段（字段 / 登记类型 / 枚举值 / 是否属「AI 生成启用」子集）；
  - §2 登记类型语义（`string`/`longtext`/`number`/`boolean`/`json`/`object`/`array`/`enum`）；
  - §3 `ADOPTION_SCHEMAS` — **53 张集合表**写回策略（identity / 去重 / 必需字段 / 自动盖章 / **外键校验 32 条**〔24 个不同外键字段名〕 / ownerFrom）。
    这正好覆盖 `adopt()` 六项校验里的 field / 外键 / owner 三项的**登记侧**事实。
    > 注：此处数字此前误写为「24 对」（把"不同字段名数"当成了"条目数"）—— 由独立复审 `REV-20261006-014` 抓出并修正。
- **为什么这是缺口**：`SKILL.md` §二 把「AI 能写什么」列为三个单一事实源之一，
  但此前只写了"`FIELD_REGISTRY` + `AdoptionSchema` + `adopt()`"的抽象描述，
  且 `schema-tables.md` §3 明确写着"逐表清单**尚未抽取**…未抽取前不得写入契约"。本版补上。
- **抽取要点（如实记录）**：登记存在**两种形态**（工厂调用 `text(target, field, …)` 与**对象字面量**），
  且 `FIELD_REGISTRY` 通过 `...WORLDVIEW_GENERATABLE_FIELD_SPECS` / `...STORY_CORE_GENERATABLE_FIELD_SPECS`
  **展开包含**两个子集（共 25 项）—— 解析器必须**解析展开**，否则会重复计数或漏项。
  最终 **0 条未解析**，并断言"两个子集全部包含于展开结果"。
- **机器核对（独立解析路径，非生成器自身）**：`528 = 503（工厂调用）+ 25（展开子集）` 逐条相等、类型全对；
  采纳表 `53 = 53`；外键 **32 条**（24 个不同字段名）。核对脚本首版曾把 `fkChecks` 子数组的 `target` 误当采纳表（得到 54），
  以及把 §3 行误算进 §1（得到 581）—— **是核对方法错、不是产物错**，已修正方法后复验。

### 机制（防这两份参考文件漂移）
- 新增断言 **`X1`**：`field-registry.md` §1 出现的每张表都必须存在于 `schema-tables.md` 的表清单中（禁凭空多表）。
- 新增断言 **`X2`**：该文件**自述的计数**（表数 / 项数 / 集合表数）必须等于**实际行数**（防"123 张"式漂移）。
- 断言数 17 → **19**；同步更新 `SKILL.md` / `README.md` / `COMPAT.md` 的计数与版本。

### 旧表述清零（律：新规则必须杀掉旧表述）
- `references/schema-tables.md` §3：`FIELD_REGISTRY` 一节由**「下一版补齐 / 未抽取前不得写入契约」**
  改为**已抽取**并指向 `references/field-registry.md`（本文件只管"表 / store 规格 / TS 接口"）。
- `SKILL.md`：§二.2 与「横切参考」两处补上 `field-registry.md` 的指向。

## v0.2.2 — 2026-10-06

### 排错（真实死链 + 检查器假阴性）
- **发现**：WSL 原件**缺少** `references/` 目录，但 `SKILL.md` 用反引号引用了
  `` `references/schema-tables.md` `` —— 属**死链**；然而 v3 检查器仍报 `PASS`。
  - 根因 1：`L1` 只匹配 markdown 链接 `[t](p)`，**看不见反引号 code span**。
  - 根因 2：`R3` 只在 `references/` **存在时**扫孤儿；目录整体缺失时循环被跳过 → 直接判"无孤儿"。
  - 两者叠加 → 「引用了但文件不存在」**完全没有断言覆盖**（假阴性）。
- **修复**：新增断言 **`L2`「被引用的本地文件都存在（含反引号 code span）」** ——
  从原文抽取 `references|contracts|scripts/<name>.<ext>` 并逐条验存。
  先令其在 WSL 原件上复现 **FAIL**（`SKILL.md → references/schema-tables.md`），再修文件使其 **PASS**（测试测试）。
  同时澄清 `R3` 职责边界：只管"多余文件"，存在性归 `L2`。
- **根因防复发**：新增断言 **`V2`「版本与断言数的当前态声明自洽」** ——
  校验 `SKILL.md` 的「本技能版本」与 frontmatter 一致、且其声明的断言数 = 实际断言数；
  `README.md` 的断言数一致；`skill-card.md` 版本与 frontmatter 一致。
  （这类漂移此前全靠人工发现，正是本轮四处数字互不一致的来源。）

### 补记
- `references/schema-tables.md` 此前**只存在于工作副本、未进版本记录**（CHANGELOG/COMPAT 均无）——
  这正是它没被同步回 WSL 的原因；本版补记。
- **核对**（实测 2026-10-06）：该文件声称的「123 张表」与上游 `src/lib/db/schema.ts` 的
  `STORYFORGE_STORES`（展开）及 `StoryForgeDB` 的 `Table<>` 类声明**双向集合完全相等**（123 = 123 = 123）。
- `references/schema-tables.md` §3 如实声明：`FIELD_REGISTRY` 逐表可写字段清单**尚未抽取**，
  未抽取前不得写入契约。

### 独立复审发现并修复（子 Agent 对抗性复审，非自审）
- **[高] `references/schema-tables.md` §1 有 11 处事实错误**：原文件对
  `chapters / characterRelations / characters / codexCategories / codexEntries / foreshadows /
  itemLedger / outlineNodes / storyCores / worldGroups / worldviews` 断言「未在 `src/lib/types/*.ts` 找到同名接口」，
  但对应接口**都存在**（首版抽取器漏了 `extends` 形态）。→ 已重新机械生成 §1：21 张表全部配齐接口字段表，
  并对 `extends RagDocumentMetadata` 的 11 个接口标注继承来源（只列自身字段，避免重复计数）。
- **[中] §2 有 44/123 行 store 规格被 110 字符静默截断**（无省略号，残缺片段易被误当完整规格）→
  重生成后输出**完整**规格，标题改为「（123 张，完整 store 规格）」。
- **[中] `CHANGELOG.md` 底部「校验方式」块仍写 `16 项断言`**（`V2` 不扫 CHANGELOG → 漏网）→
  **移除**命令行注释里的硬编码数字（改为只写「期望：RESULT: PASS」），从根上消除该重复事实源；
  并把 `V2` 扫描面扩到 `COMPAT.md`（校验「当前版本」与「现行断言数」）。
- **[低] `L2` 正则未加左边界** → 加 `(?<![\w/])`，避免命中 `apps/api/scripts/seed.ts` 这类子路径片段。
- **[低] `V2` 的 `total = len(items) + 1` 依赖「V2 是最后一项」** → 加显式自检，若 V2 非最后一项即报 FAIL。

### 第 2 轮独立验证（确认修复 + 再抓 1 处）
- 第 1 轮 1–4 条**确认已修复**；§1（21/21）与 §2（123/123）经独立脚本逐字节比对**与上游完全相等**。
- **[中] 新发现：`V2` 对「文件缺失」不覆盖** —— 删除 `README.md` / `COMPAT.md` / `skill-card.md`
  任一后，三处 `if os.path.isfile(...)` 会**静默跳过**，V2 仍报 OK、整体仍 PASS。
  → 已修：`V2` 先做这三个「当前态声明文件」的**存在性**断言，缺失即 FAIL
  （复现测试见 `work/test_v2_missing_file.py`：删除后 rc=1 且 V2 报「缺失」）。

### 文档漂移修复（四处数字/版本互不一致）
- `COMPAT.md`：当前版本 `v0.2.0` → **`v0.2.2`**；基线文档数 8 → **10**；断言数 `11` → **14（v0.2.0 实际）**，
  并给出断言数轨迹 `14 → 15（+C4）→ 17（+L2 +V2）`。
- `README.md`：断言数 `13` → **17**；版本 `v0.2.0` → **`v0.2.2`**；限制条目指向 `references/schema-tables.md`。
- `SKILL.md`：版本 `0.2.1` → **`0.2.2`**；断言数 `13` → **17**。
- `CHANGELOG.md`：v0.2.0 条目的断言数 `13` → **14**；两处校验命令行注释**去掉硬编码数字**。

### 校验方式（本版起生效）
```bash
python scripts/check_consistency.py     # 期望：RESULT: PASS (0 fail, 0 warn)
```

## v0.2.1 — 2026-10-06

- **修复跨文件规则矛盾（用户使用中发现）**：`SKILL.md` §五 曾写「每块带 provenance（在 JSON 里）」，与 `S-data-envelope.md` §3 的「必须放旁车文件」冲突。
  现统一以 **`contracts/S-data-envelope.md` §3 为唯一权威**（旁车文件），`SKILL.md` 改为指向它；
  并新增检查器断言 **`C4`**（provenance 存放规则单源一致）防止复发。

- 新增 `skill-card.md`（ClawHub 的 `verify` 曾报 `card.missing`：卡片文件此前不存在；
  内容含诚实的已知风险与缓解措施）
- 说明：`verify` 的安全判定为 **clean / benign**（confidence: high）—— 本技能不包含隐藏安装钩子、
  不使用凭据、不自动改数据库/运行态
- 标注：本技能的 JSON 产物**不是备份包**（不含 `version` 字段），按文件交付、**不依赖应用**

## v0.2.0 — 2026-10-05

### 基线与覆盖
- **基线重钉**：单一日期 `2026-09-27` → **逐文档版本**（10 条），并区分 `primary_source`
  与 `auxiliary_source`（后者仅用于 agent 纪律/证据分级，不混入数据契约）
- **新增 3 个子契约**，补上原版覆盖缺口：
  - `contracts/C-screenplay.md` —— 小说转剧本（改编 Brief / Beat·Scene Card / 兼顾三态 / 完成判据 / 工程边界）
  - `contracts/A-world-engine.md` —— 世界引擎（worldCode / WorldRelease 字段闭集 / 出口四类 / 分享包）
  - `contracts/S-data-envelope.md` —— 数据契约与导入/导出（横切）
- 路由表：基线的 **8 行** → **10 行**（新增两行；产品「漫剧前期」按上游改为「漫剧素材前期」）

### 契约修正
- `A-longform.md`：补节点模式**字段闭集**（9 项）+ 图执行前 5 项检查 + **跨模式验收 5 条**；
  长铗传示例 70 集 → **90 集**、`scripts/act1-4` → `episode-01..04`
- `A-interactive.md`：补现行内核 `AdventureContentV2`（**八能力**）与唯一权威写入
  `commitAdventureAction` / `commitAdventureNarrativeChoice`
- 三处旧契约的**溯源错位 / 表述过强**修正（并入上游原文口径）

### 治理
- 新增**证据分级**（`OBSERVED` / `INFERRED` / `UNKNOWN` + 主张与证据等量 + 逐块 provenance），
  并明确其**效力边界**：应用不校验该字段，不能指望系统拦住虚构入 Canon
- 凡「达芬奇」等**环境来源**内容，逐行标注为非源仓库基线

### 机制
- 新增 `scripts/check_consistency.py`（14 项断言，零依赖）
- 修正一处**会导致导入必然被拒**的契约错误：早期草稿把自造顶层键标为"可核验"，
  且把 IndexedDB `schema v10` 与备份版本 `v14` 混用

## v0.1.0 — 初始版本

- 从上游文档提炼 6 份子契约（长篇/短篇、角色、交互、漫画、漫剧、后期）+ 总入口 SKILL.md
- 基线标注为单一日期 `2026-09-27`

---

## 校验方式

```bash
python scripts/check_consistency.py     # 期望：RESULT: PASS (0 fail, 0 warn)
```
