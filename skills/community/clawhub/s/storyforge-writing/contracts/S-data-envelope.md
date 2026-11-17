# S-data-envelope — 数据契约与导入/导出（v0.2.0 引入；v0.5.0 修订：§3.1 规范化哈希 / §3.2 context-manifest）

> 来源（一手核实）：`src/lib/export/json-export.ts`、`src/lib/export/backup-trust.ts`、
> `src/lib/export/registry-export.ts`、`src/lib/db/schema.ts`、`docs/DATA-GOVERNANCE.md`（v1.8.0）。
>
> ⚠️ **本文件的早期草稿曾把自造的顶层键标为"可核验"**，被 `REV-20261005-017` 直接证伪。
> 现版本只写**有出处**的内容；无出处的部分一律标 `待实测` 并给出取得方法。

## 1. 备份/导出契约的**真实**形态（源：`json-export.ts:109-132`）

```ts
export interface ProjectExportData {      // 「完整项目导出数据结构(导出格式契约)」
  version: number                          // 备份协议版本
  exportedAt: number
  ownership: {
    contractVersion: number                // registry-export.ts: 当前 = 1
    worldExportId: number
    workExportId: number
  }
  project: { workspaceUid, workspacePurpose, name, enableMultiWorld,
             productPlatformOptIns, createdAt, updatedAt, ... }   // 精确键集见 backup-trust.ts:27+
  worlds: (Omit<World,'id'|'projectId'> & { _exportId: number })[]
  works:  (Omit<Work,'id'|'projectId'|'worldId'|...> & { _exportId: number })[]
  // …（其余表同构）
}
```

**关键事实（每条都有出处）**：

| 事实 | 出处 |
| --- | --- |
| 导入**只接受**备份版本 `v14`；`version !== 14` 直接报「只接受当前备份版本 v14」 | `backup-trust.ts:10,98-103` |
| 预检是**只读**检查：表清单来自 `PROJECT_TABLES`，**不复制一套导出枚举**，**不访问 IndexedDB** | `backup-trust.ts:1-8` |
| 只接受与当前架构**完全一致**的备份：**不执行升级，也不缺表补空** | 同上 |
| 项目对象按**精确键集**检查（`CURRENT_PROJECT_EXPORT_KEYS` / `inspectExactKeys`） | `backup-trust.ts:27+,110-113` |
| `ownership.contractVersion` 当前 = `1` | `registry-export.ts:651-652,684`（注：同文件 `:24` 是 `CURRENT_EXPORT_VERSION = 14`） |

### 1.1 精确键集（v14 预检的**硬要求**）

> **出处**：`backup-trust.ts:27-61`（键集定义）、`:63-74`（`inspectExactKeys`）、`:77-199`（预检主体）。
> **为什么逐字记在这里**：预检对 `project` / `works[]` / `worlds[]` 走**精确键集** ——
> **多一个键报错、缺一个必需键也报错**，没有「忽略未知字段」的宽容度。

**`project`（工作区根）**：允许 **9** 键 / 必需 **5** 键

- 允许（全部）：`workspaceUid` `workspacePurpose` `name` `enableMultiWorld` `productPlatformOptIns` `createdAt` `updatedAt` `_activeWorldExportId` `_activeWorkExportId`
- **必需**：`workspaceUid` `workspacePurpose` `name` `createdAt` `updatedAt`

**`works[]`（每项）**：允许 **23** 键 / 必需 **17** 键

- 允许（全部）：`_exportId` `_worldExportId` `_activeCharacterDrivenPlanExportId` `_activeNarrativeModuleExportId` `code` `kind` `novelProfile` `title` `description` `genres` `customGenre` `status` `targetWordCount` `currentWordCount` `coverImage` `writingStyleId` `methodologyId` `includeCultivationProgressInAI` `postAdoptionPolicy` `postAdoptionTaskTypes` `postAdoptionBudget` `createdAt` `updatedAt`
- **必需**：`_exportId` `_worldExportId` `code` `kind` `novelProfile` `title` `description` `genres` `status` `targetWordCount` `currentWordCount` `includeCultivationProgressInAI` `postAdoptionPolicy` `postAdoptionTaskTypes` `postAdoptionBudget` `createdAt` `updatedAt`

**`worlds[]`（每项）**：允许 **9** 键 / 必需 **8** 键

- 允许（全部）：`_exportId` `identityKind` `code` `name` `description` `currentVersion` `communityOrigin` `createdAt` `updatedAt`
- **必需**：`_exportId` `identityKind` `code` `name` `description` `currentVersion` `createdAt` `updatedAt`

**其它预检约束（同样有出处，逐条）**：

| 约束 | 出处 |
| --- | --- |
| `version` 必须 `=== 14` | `:98-103` |
| `ownership.contractVersion` 必须 `=== 1`，且 `worldExportId` / `workExportId` 为整数 | `:123-129` |
| `project.workspacePurpose` ∈ {`independent-work`, `world-engine`} | `:118-120` |
| **所有可导出表都必须在场且为数组**（缺表 → 报「备份缺少 N 张当前必需表」） | `:131-150` |
| `works[].genres` 必须是字符串数组；`includeCultivationProgressInAI` 必须是布尔 | `:159-164` |
| `works[].kind` 闭集：`novel`·`screenplay`·`comic`·`motion-drama`·`avg`·`ttrpg`·`ai-town`·`character-interaction` | `:165-171` |
| `works[].kind === 'novel'` 时 `novelProfile` ∈ {`short`, `long`}；否则 `novelProfile` 必须为 `null` | `:165-171` |
| `worlds[].identityKind` ∈ {`workspace-scope`, `world-draft`}，且 `code` 须过 `isCurrentWorldCode` | `:182-185` |

## 2. ⚠️ 两个"版本号"完全不同，不得混用（v0.2.0 修正）

| 常量 | 值 | 用途 |
| --- | --- | --- |
| `STORYFORGE_SCHEMA_VERSION` | **10** | **IndexedDB（Dexie）schema 版本** —— 与导入信封无关 |
| `CURRENT_BACKUP_VERSION` | **14** | **备份/导出协议版本** —— 导入边界只认它 |

> 早期草稿把 `schema v10` 写成信封的 `schemaVersion` 字段，属**事实错误**（`REV-20261005-017` #2）。

## 3. 本技能产物的定位（修正后）

**本技能的产物是"框架语料"，不是备份包。** 两者的差别是硬的：

| 项 | StoryForge 备份/导出 | 本技能产出 |
| --- | --- | --- |
| 顶层结构 | `ProjectExportData`（见 §1） | 本技能自有结构（见下） |
| 版本字段 | `version: 14`（不符即拒） | **不加 `version` 字段**（避免伪装成备份） |
| 未知字段 | **精确键集**，多余字段导致拒收 | 因此**不得**把 `provenance`/`evidenceGrade` 塞进记录内 |
| 导入方式 | 应用内导入器 | **不适用**：本技能产物按文件交付，**不承担导入职责**（无应用依赖） |

**本技能的语料结构（自有，不冒充备份）**：

```jsonc
{
  "storyforgeFramework": "0.5.0",     // 本技能版本（非备份版本）
  "baseline": { "docs/DATA-GOVERNANCE.md": "v1.8.0", "docs/products/LONGFORM-AND-NODE.md": "v1.6.0" },
  "blocks": [
    { "table": "characters",          // 表名必须 ∈ PROJECT_TABLES 派生清单
      "records": [ /* 字段闭集见 references/field-registry.md */ ] }
  ]
}
```

**provenance 与证据分级放"旁车文件"**（`storyforge-framework.provenance.md` 或 `.json`），
**不放进导入候选**：因为导入走精确键集，多一个键就会被拒（`backup-trust.ts:110-113`）。
旁车文件记录：来源 md + revision + contentHash + `evidenceGrade`（逐块）。

**旁车文件结构（v0.3.1 明确）**：

```json
{
  "storyforgeFramework": "0.5.0",
  "generatedAt": "2026-10-15",
  "generator": "storyforge-writing",
  "hashAlgorithm": "sha256",
  "hashCanonicalization": "sf-c14n-v1",
  "recordsFile": "storyforge-framework.json",
  "baseline": { /* 同主文件 */ },
  "blockProvenance": [
    {
      "table": "characters",
      "recordCount": 41,
      "contentHash": "sha256:<按 §3.1 复算>",
      "evidenceGrade": "OBSERVED",
      "sources": [
        {"md": "p1-world-characters.md", "revision": "v1.2", "grade": "OBSERVED"}
      ]
    }
  ]
}
```

**关键约束**：
- `blockProvenance` 必须是 **list**（不是 dict），每项对应主文件 `blocks[]` 中的一张表
- 每项必须有 5 个字段：`table` / `recordCount` / `contentHash` / `evidenceGrade` / `sources`
- `contentHash` 用 sha256，并按 **§3.1** 规范化计算（`make_sidecar.py` 自动生成）；非加密占位如 fnv1a64 需标注"应用侧应重算"
- `recordCount` 必须等于主文件中该表的实际记录数；旁车登记的表必须在主文件中存在，主文件的每张表都应有一条 provenance
- 可选 `unresolvedRefs[]`：`{table, field, value, reason}`（`A-longform.md` §8）
- `sources` 是 list，每项记录来源 + 版本 + 证据等级。**实测存在两种合规形态**（v0.4.0 明确）：
  - 形态 A（`{md|path|file, revision?, grade}`）—— 逐文件来源；
  - 形态 B（`{key, evidence, sources:[字符串]}`）—— 具名来源组 + 其下的文件列表。
  校验器接受**任一**含来源标记（`md`/`path`/`file`/`key`）的形态；等级取 `grade` 或 `evidence`。
- **有记录必须有来源**：`recordCount > 0` 而 `sources` 为空时，必须用 `notes` **显式声明原因**；
  既无 `sources` 也无 `notes` 判 **ERROR**（静默缺失）。空表（`recordCount = 0`）允许无来源。
- `storyforgeFramework` 填**本技能版本**（非产物版本）—— 示例中的版本号随技能版本更新

### 3.1 规范化哈希 `sf-c14n-v1`（v0.5.0）

**为什么要规定**：只写"用 sha256"等于没规定 —— 键序、空白、`ensure_ascii` 任一不同，哈希就不同，
**"可复算证据"就无法复算**（v0.4.0 校验器因此只检查形态，`sha256:deadbeef` 也能通过）。

**算法**（实现：`scripts/sf_hash.py`，生成与校验共用同一份代码）：

1. 取主文件 `blocks[]` 中**同一 `table`** 的全部 `records`，按出现顺序拼成一个 list；
2. `json.dumps(list, ensure_ascii=False, sort_keys=True, separators=(",", ":"))`；
3. UTF-8 编码后 SHA-256，写作 `sha256:<64 位小写十六进制>`。

**判定**：旁车顶层声明 `"hashCanonicalization": "sf-c14n-v1"` 时，复算不一致 = **ERROR**（`EVIDENCE_HASH_MISMATCH`）；
未声明（历史产物）且复算不一致 = **WARN**（`EVIDENCE_HASH_UNVERIFIABLE`，`--strict` 下 ERROR）—— 不改写历史产物，只让偏离可见。
**新产物一律用** `python scripts/make_sidecar.py <framework.json> --write` 生成/刷新旁车。

### 3.2 `context-manifest.json` 结构（v0.5.0）

**为什么要规定**：校验器早就要求该文件存在，但此前**没有任何契约给出形状** —— 存在一个空文件也算通过。

```json
{
  "storyforgeFramework": "0.5.0",
  "generatedAt": "2026-10-15",
  "entries": [
    {"source": "settings/premise.md", "state": "read", "revision": "r1", "contentHash": "sha256:..."},
    {"source": "settings/characters.md", "state": "partial-selection", "reason": "只选入本章出场的 2 名角色"},
    {"source": "knowledge/", "state": "missing", "reason": "项目内尚无考据库"}
  ]
}
```

- `state` 闭集 = `read` · `missing` · `omitted` · `partial-selection`（后三者即**裁剪三态**，见 `SKILL.md` §二）；
- 非 `read` 的条目**必须**写 `reason`（裁剪必须留证据）；
- 非法 JSON / `entries` 形状错误 = ERROR（`MANIFEST_INVALID`）；无 `entries` 的旧形态 = WARN（`MANIFEST_LEGACY`，`--strict` 下 ERROR）。

完整样例：`examples/minimal/`。

> ⚠️ **键名的历史不一致（`REV-20261007-030` F1，如实登记）**
> （处置纪律见 `SKILL.md` §四 第 7 条「权威值不得擅自修正」）：本契约规定的规范键名是 `blockProvenance`，
> 但**广陵散**的历史旁车用的是 `blocks`（同形状 list，键名不同）。**新产物一律用 `blockProvenance`**；
> 校验器 `check_framework_artifact.py` 对非规范键名报 **WARN**（不算 ERROR），以便偏离可见而不改写历史产物。

## 4. 三条主干规则（源：`docs/DATA-GOVERNANCE.md`）

1. **清单必须派生**：导出/导入/删除/世界切换清单**从 `PROJECT_TABLES` 派生**；
   schema/required table 数量由代码与 `npm run check:required-tables` 决定，**不在手写文档中复制清单**。
2. **精确字段闭集**：导入拒绝旧镜像与未知字段（实现见 `backup-trust.ts` 的精确键集检查）。
3. **候选 ≠ Canon**：模型输出先是候选；`adopt()` 校验（field / schema / 外键 / owner / 作用域 / stale）通过且作者确认后才进 Canon。

## 5. `待实测` 项（**已全部裁定 / 补全**，2026-10-07）

| 未定项 | 状态 |
| --- | --- |
| 各表**完整字段名与取值域** | ✅ **已补全** → `references/schema-tables.md` **§4 全表字段清单**（106 表 / 1734 项，含取值域 `⟨…⟩`） |
| `worlds`/`works` 等数组元素的**全字段** | ✅ **已归档** → 本文件 **§1.1 精确键集**（`project` 9/5 · `works[]` 23/17 · `worlds[]` 9/8） |
| blob/OPFS 等外部对象在包内的引用形式 | ❌ **已关闭**（TD-5c）：属具体项目的额外需求、由其它技能承担，**与本技能无关** |
| ~~用户实际希望走哪种导入路径~~ | ❌ **已关闭**（TD-5d）：用户裁定本技能**不依赖任何应用**，语料只当写作素材 |

> **无遗留 `待实测` 项**。若将来出现新的未定项，仍按「给出取得方法、禁止补造」的规矩登记。

## 6. 交付前对齐清单

- [ ] 语料**不含** `version` 字段（不冒充备份）、**不含**记录外的未知键
- [ ] 每个 `table` 来自 `PROJECT_TABLES` 派生清单
- [ ] 每条记录字段不超出闭集（`--strict` 下 `FIELD_UNKNOWN` / `FIELD_NOT_WRITABLE` 为 ERROR）
- [ ] 旁车由 `make_sidecar.py` 生成（声明 `sf-c14n-v1`），`context-manifest.json` 按 §3.2 填写
- [ ] `check_framework_artifact.py --strict` 0 errors
- [ ] **provenance 与 evidenceGrade 在旁车文件**，不混入候选记录
- [x] 交付说明列出未定项与取得方法（**当前：无遗留**，见 §5）
- [x] 产物以文件交付为终点：**不依赖任何应用的导入 / 运行时**

## 7. 所有权 · 不变量 · 禁止项（v0.4.0）

**所有权**：本技能 owns **语料结构与其校验**；上游 owns 备份/导出格式（`ProjectExportData`、
`backup-trust.ts`）与导入运行时；**作者** owns 交付物的用途与去向。

**不变量**
- `INV-S-1` 语料**不含 `version` 字段**（不冒充备份包）。
- `INV-S-2` `provenance` / `evidenceGrade` **只在旁车**，绝不进记录内。
- `INV-S-3` **有记录必须有来源**：`recordCount > 0` 且 `sources` 为空时，必须用 `notes`
  **显式声明原因**（「显式 ≠ 空」）。
- `INV-S-4` 若按上游备份格式交付，必须满足**精确键集**（多一键即拒）。
- `INV-S-5` 悬空引用必须按 `A-longform.md` §8 在 `unresolvedRefs` 留痕。
- `INV-S-6` 旁车 `contentHash` 可按 §3.1 复算、`recordCount` 与主文件一致、表集合双向对齐。
- `INV-S-7` `context-manifest.json` 按 §3.2 记录读取与裁剪三态。

**禁止项**
- 不得把旁车字段塞进 JSON 记录内。
- 不得声称"可导入应用"或代操作导入（本技能**不依赖任何应用**）。
