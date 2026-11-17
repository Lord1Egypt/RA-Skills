---
name: storyforge-writing
description: >-
  StoryForge 叙事写作框架（蒸馏自 github.com/yuanbw2025/storyforge 的数据契约 + 写作 SOP）。
  用于按 StoryForge 字段闭集生成「框架语料」并受控推进创作：长篇/短篇/小说转剧本/世界引擎封存与出口/
  角色卡/AVG·文字冒险·跑团（A 类）、漫画分镜·漫剧素材前期（B 类）、漫剧后期对接（C 类）。
  触发：用户说"按 StoryForge/故事熔炉框架写""生成框架语料""按写作 SOP 推进""对齐 StoryForge 数据契约"，
  或要做「小说转剧本」「世界封存/出口包」「分镜/漫剧 prompt 包」等结构化创作。
  不用于：纯自由写作/润色（无结构化产物需求）、操作 StoryForge 应用本身。
version: 0.5.0
license: MIT
compatibility: >-
  通用 agent 技能：需要可读写的项目目录（设定 md + 可选考据库）与 Python 3（跑校验器）。
  **技能自足：不依赖任何外部应用的导入或运行时**；产物以文件交付。
  特定 agent 环境的本地约定（路径、记忆库、试点项目）见 references/local-environment.md（可选）。
metadata:
  author: taosiuman
  source: https://github.com/yuanbw2025/storyforge
  source_version_baseline:
    audited: "2026-10-05（逐文档记版本）"
    primary_source: "github.com/yuanbw2025/storyforge（唯一数据契约基线；本地镜像路径见 references/local-environment.md）"
    documents:
      - "docs/DATA-GOVERNANCE.md: v1.8.0（2026-09-28）"
      - "docs/PROJECT-MASTER-CHARTER.md: v1.10.0（2026-09-29）"
      - "docs/DOCUMENT-AUTHORITY.md: v2.4.0（2026-09-29）"
      - "docs/CONTEXT-ROUTING.md: v2.7.0（2026-09-29）"
      - "docs/products/UPPER-PRODUCTS.md: v2.6.0（2026-09-28）"
      - "docs/products/LONGFORM-AND-NODE.md: v1.6.0"
      - "docs/products/MOTION-DRAMA.md: v1.2.0"
      - "docs/products/INDEPENDENT-CREATION.md: v1.2.0"
      - "docs/products/WORLD-ENGINE.md: v1.4.0"
      - "src/lib/db/schema.ts: schema v10（comic v5 迁移步）"
    auxiliary_source:
      path: "StoryForge-master/docs/ai/anti-hallucination.md"
      scope: "**仅** agent 纪律/证据分级；**不是**数据契约基线（Desktop IDE 线，SQLite，与本技能的 Dexie/IndexedDB + schema v10 不同源）"
  openclaw:
    requires:
      bins: []
      env: []
      credentials: none
    optional_env: []
---

# storyforge-writing — StoryForge 写作框架总入口

把 StoryForge 的**数据契约 + 写作 SOP + 治理纪律**变成 agent 可执行的工作流：
判定产品 → 读对应子契约 → 装配上下文 → 生成**候选**框架语料 → 校验 → 交作者采纳。

## 一、产品路由表（10 类能力 → 子契约）

| 产品 | 归属分类 | 子契约 | 核心产物 |
|---|---|---|---|
| 长篇（分步骤） | A 开发创作 | `contracts/A-longform.md` | 世界观/故事核/角色/大纲/细纲/正文 + 长程一致性 |
| 短篇 | A 开发创作 | `contracts/A-longform.md` §短篇 | 故事核/角色/单线大纲/正文 |
| **小说转剧本** | A 开发创作 | `contracts/C-screenplay.md` | 提取 → 改编 Brief → 场次计划 → 剧本场景 → 审校 → 不可变剧本版本 |
| **世界引擎（封存/出口）** | A 开发创作（世界侧） | `contracts/A-world-engine.md` | worldCode / WorldRelease / 数据出口 / 分享包 |
| 角色聊天（角色卡） | A 开发创作 | `contracts/A-characters.md` | 角色卡/说话风格/记忆/禁区 |
| AVG / 文字冒险 | A 开发创作 | `contracts/A-interactive.md` | 场景树/分支/对白/结局/物品/状态机 |
| 跑团 TTRPG | A 开发创作 | `contracts/A-interactive.md` §跑团 | 规则包/场景/事件（只读冻结世界） |
| 漫画 | B 视觉化 | `contracts/B-comic.md` | 分镜脚本/页/格/视觉主体卡 |
| 漫剧素材前期 | B + C | `contracts/B-motion-drama.md` | 系列圣经/逐集/分镜/Image·Video Prompt IR/适配包 |
| 漫剧后期对接 | C 制作后期 | `contracts/C-post.md` | prompt 包 → 生成管线（交接约定，不代执行） |

> **横切契约（不属任何单一产品，全部产品适用）**：`contracts/S-data-envelope.md`（语料信封 · 旁车 · 规范化哈希 · context-manifest）；
> `contracts/INVARIANTS.md`（不变量 ↔ 断言对照表）。

**判定顺序**：① 意图（生成设定/文本语料 = A；出视觉料 = B；接后期管线 = C）→ ② 关键词 → ③ 拿不准就问。
易混淆：「剧本」默认指**小说转剧本**（A · `C-screenplay`），不是后期（C · `C-post`）；
「漫剧」先看是要**前期物料/Prompt**（B）还是**对接生成/剪辑**（C）。

## 二、数据契约（三个单一事实源）

1. **AI 读什么** — `CONTEXT_SOURCES` / Context Gateway：先任务与硬约束 → 目录与能力画像 → 摘要/事实/关系 → 按需详情 → 预算保护。
   **裁剪必须留证据（三态，不得混淆）**：`missing`（冻结世界中**不存在**）、`omitted`（**存在但未选入**）、`partial-selection`（**仅选入部分**）。
   禁止把"没读"当"不存在"，禁止用「固定前缀 / 前 N 条」当主要检索算法。文件模式下落到 `context-manifest.json`（结构见 `contracts/S-data-envelope.md` §3.2）。
2. **AI 能写什么** — `FIELD_REGISTRY` + `adopt()`：模型输出只是**候选**，作者确认才进 Canon。
   逐表可写字段查 `references/field-registry.md`（64 张表 / 528 项；未登记字段在上游会被 `unknown_write_field` 拒绝）。
   `temporalFacts` / `narrativeSummaryNodes` 等**只读表**由系统生成，AI 不写（该文件 §4）。
3. **表生命周期** — `PROJECT_TABLES`：导出/导入/删除/迁移统一收口；表清单以上游代码为准，不手抄。
   表名、索引与全字段查 `references/schema-tables.md`（§2 全表索引 123 张 = 表名单源；§4 全表字段清单 106 表）。

**数据所有权**：`projectId`（工作区壳）→ `worldId/worldGroupId`（世界）→ `workId`（作品）→ 产品实例。
Work 拥有标题/简介/流派/文风；World 拥有编号/版本/来源；禁止在 Project 上镜像 World/Work 语义。

**世界衍生产品三阶段**：S1 世界封存（产出不可变 WorldRelease）→ S2 产品定向（WorldReference + Brief + SourcePlan + 用户授权）
→ S3 产品执行（只读冻结 Brief/plan，每次运行留 Context Manifest，**不回写世界**）。

## 三、文件模式：SOP 每一步在本技能里做什么

上游 SOP 描述的是**应用内**动作；本技能不跑应用，下表是它们在**文件交付**下的等价做法：

| 上游 SOP 步骤 | 本技能的等价动作 |
|---|---|
| 建立作用域与 revision | 记下项目目录、目标表/字段、各来源文件的 revision 或 sha256 |
| 读目标字段与按需证据（Context Manifest） | 读设定 md / 考据；把读了什么、裁掉什么按三态写进 `context-manifest.json` |
| 选择动作 create / expand / rewrite / polish | 在交付说明里写明动作；扩写/润色时**原版与新版并列**展示 |
| durable 生成候选（CreativeArtifact） | 写 `storyforge-framework.json`（只含字段闭集内的键）；全部视为**候选** |
| 展示候选与运行证据 | 跑 `python scripts/make_sidecar.py <framework.json> --write` 生成旁车，补全 `sources`/`evidenceGrade` |
| stale 检查 + `adopt()` | 跑 `python scripts/check_framework_artifact.py --strict <framework.json>`；来源哈希变了 = stale，重新生成而不是沿用 |
| 作者编辑 / 拒绝 / 采纳 | **交回作者决定**；agent 不替作者宣布"已采纳" |
| 回读、触发下游失效 | 采纳后更新连续性产物（`continuityHandoff` / 伏笔 / 时间线 / 状态卡），只影响未来章节 |

**生成纪律**：空项目允许自主创造（标题只作低权重提示）；有关联内容时作为约束而非复述；
非法 JSON 保留原始输出、至多一次定向修复；**影响只向未来传播**，已确认历史不静默改写。

**连续性（写新章 / 新集前必做）**：先读上一章/集的正文与 `continuityHandoff`，确认故事内时间戳、结尾场景快照、
角色物理与情感状态、时间推进方式（同日后续 / 次日 / 数日后），并避免重复上一章的画面；
需要重复时显式标注时间跳跃。字段形状与有界回环规则见 `contracts/A-longform.md` §9。

## 四、治理红线

1. **AI 输出只是候选**，作者确认才进 Canon；不自动采纳、不静默写入。
2. **只出创作语料，不碰 runtime**：可玩开放世界、活体 KP、产品 build/release/session 不在范围内；不操作浏览器或应用导入。
3. **冻结世界引用**：上层产品只读引用已封存 WorldRelease，运行结果不回写世界。
4. **裁剪留证据（三态）**：`missing` / `omitted` / `partial-selection` 不得混淆，不得把未读当不存在。
5. **stale 不可跳过**：目标或关键来源变化后拒绝旧候选。
6. **证据分级**：每块内容可标注来源等级，不得把推断当事实写入 Canon ——
   `OBSERVED`（实际检查过的源文件直接支持，给出文件与偏移/行号）·
   `INFERRED`（由已有事实推导，写推导链）·
   `UNKNOWN`（无来源 → **必须标为 UNKNOWN 或留空**，禁止编造补全）。
   provenance 与 `evidenceGrade` **只放旁车文件**，存放与形状以 `contracts/S-data-envelope.md` §3 为唯一权威。
7. **权威值不得擅自「修正」**：上游字段名/枚举值/历史键名即使看起来错（如 `muti`、历史旁车键 `blocks`），
   也按原值产出、显式标注差异、历史产物不改写（校验器只报 WARN），统一与否交回作者。
8. **完成声明必须有可复算证据**：不得以"已启动 / 文件已写 / 模型说完成"代替；
   交付时给出产物路径、旁车 `contentHash`、校验命令与其真实输出（含 WARN 数量）。

## 五、产物形态（文件交付）

```text
<项目目录>/
  storyforge-framework.json              # 主文件：{storyforgeFramework, baseline, blocks:[{table, records}]}；无 version 字段
  storyforge-framework.provenance.json   # 旁车：hashCanonicalization=sf-c14n-v1 + blockProvenance[] + unresolvedRefs[]
  context-manifest.json                  # 读取/裁剪证据：entries[{source, state, reason?}]
```

- 记录**只含字段闭集内的键**；`provenance` / `evidenceGrade` 混入记录 = ERROR（上游导入走精确键集，多余键直接拒收）。
- 外键解析不到时：置 `null` 并在旁车 `unresolvedRefs` 登记（`contracts/A-longform.md` §8）；章节 `id` 必须是整数。
- **最小可用样例**：`examples/minimal/`（`--strict` 下 0 error / 0 warn），新产物照它的形状写。

## 六、执行清单

1. 判定产品 → 读对应子契约 + `contracts/S-data-envelope.md`
2. 检查前置：目标阶段的上游产物是否真实存在（以项目内非空文件为准）；缺就先补最近的上游阶段，不跳级写正文
3. 装配上下文，写 `context-manifest.json`（三态）
4. 写新章/新集前做连续性检查（§三）
5. 按字段闭集生成候选语料（枚举取闭集英文值，见 `references/field-registry.md`）
6. `python scripts/make_sidecar.py <framework.json> --write`，补全每块的 `sources` 与 `evidenceGrade`
7. `python scripts/check_framework_artifact.py --strict [--sources-root <项目目录>] <framework.json>` → 0 errors
   （`--sources-root` 只对**像文件**的引用验存；史书卷目 / 作者口述 / 上游代码位置 / 通配简写等非文件凭证只报 NOTE
   `EVIDENCE_SOURCE_NONPATH`，不算缺陷 —— 详见 `COMPAT.md` §5.10）
8. 交付：路径 + contentHash + 校验输出摘要 + 未定项；采纳决定交回作者
9. 修改技能包本身后：`python scripts/check_consistency.py` 与 `python tests/run_tests.py` 均需通过

## 子契约与参考（按需读取）

- `contracts/A-longform.md` — 长篇/短篇：覆盖范围·字段映射·节点模式·章节编号与引用·章节后验
- `contracts/A-characters.md` — 角色卡/关系/角色补全纪律（枚举取值以 field-registry 为准）
- `contracts/A-interactive.md` — AVG/文字冒险/跑团：`AdventureContentV2` 八能力
- `contracts/A-world-engine.md` — 世界引擎：worldCode·WorldRelease·出口四类·分享包
- `contracts/C-screenplay.md` — 小说转剧本：三态标注·生产链·完成判据
- `contracts/B-comic.md` — 漫画：分镜·页·格·视觉主体卡
- `contracts/B-motion-drama.md` — 漫剧素材前期：系列圣经·逐集·分镜·Prompt IR
- `contracts/C-post.md` — 漫剧后期：交接物与完成门
- `references/schema-tables.md` — 表 / store / 全字段（机械快照，与上游源码不一致时以源码为准）
- `references/field-registry.md` — AI 可写字段 + 集合表写回策略（机械快照）
- `references/local-environment.md` — **可选**：特定 agent 环境的本地路径、记忆库与外部工具约定

## 来源与验证

> **本技能版本**：v0.5.0（2026-10-16）。变更见 `CHANGELOG.md`；技能包自检 `scripts/check_consistency.py`（21 项断言）；
> 产物校验 `scripts/check_framework_artifact.py`（问题码全集：`--list-codes`）；回归测试 `tests/run_tests.py`。

### 基线

| 文档 | 版本 | 日期 |
| --- | --- | --- |
| `docs/DATA-GOVERNANCE.md` | **v1.8.0** | 2026-09-28 |
| `docs/PROJECT-MASTER-CHARTER.md` | v1.10.0 | 2026-09-29 |
| `docs/DOCUMENT-AUTHORITY.md` | v2.4.0 | 2026-09-29 |
| `docs/CONTEXT-ROUTING.md` | v2.7.0 | 2026-09-29 |
| `docs/products/UPPER-PRODUCTS.md` | v2.6.0 | 2026-09-28 |
| `docs/products/LONGFORM-AND-NODE.md` | v1.6.0 | 2026-09-27 |
| `docs/products/MOTION-DRAMA.md` | v1.2.0 | 2026-09-15 |
| `docs/products/INDEPENDENT-CREATION.md` | 1.2.0 | 2026-08-31 |
| `docs/products/WORLD-ENGINE.md` | 1.4.0 | 2026-09-10 |
| `src/lib/db/schema.ts` | schema v10（comic v5 迁移步） | — |

- 所依据的上游文档版本与上表不一致时，**先停下问**，不按记忆推进；上游更新后只重读对应段落，并重跑自检。
