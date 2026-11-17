# planning — AI 内容规划

> 对应 CSO Web 端 `/planning` 页面。基于企业知识库生成、查看、再生成和导出**月度内容规划**——含依据知识库、发布频次、规划逻辑以及图文/视频分表的可评审方案。
>
> 通用数据纪律（`--json-out`、写入确认、交付自检）见 `references/core/agent-conventions.md`。
> 知识库确定（`<knowledge_base_selection>`、跳过 list/enterprises）见 `references/core/knowledge-base-resolution.md`。

---

## 判断任务类型

**先读本节，再决定读哪一章。** 不要把只读查询误当成生成流程。

| 用户意图                           | 动作                                                                                                                                                                                  | 阅读范围                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 生成或再生成规划                   | 执行完整生成工作流；生成、再生成、取消或删除均为**写入操作**，执行前取得明确确认                                                                                                      | 本章 + 下方 **[生成工作流](#生成工作流)** 全章                                  |
| 只查看已有规划、任务状态或企业列表 | 只读查询，无需额外确认                                                                                                                                                                | **跳过 [生成工作流](#生成工作流)**；按需读 [命令速查](#命令速查) 与对应命令小节 |
| 讨论产品方案、字段或示例           | 仅输出方案，不调用生成命令                                                                                                                                                            | **跳过 [生成工作流](#生成工作流)**                                              |
| 指定某个知识库文件夹或文件         | 说明原生规划按企业 ID 读取企业知识，不能在 `planning generate` 中指定 `folder-id` 或 `source-id`；只有用户明确要求限定或核验素材来源时，才另行使用 RAG 检索（见 `references/rag.md`） | 视情况读 RAG 文档；**不进入生成工作流**                                         |

---

## 生成工作流

> **门禁**：仅当上一节判定为「生成或再生成规划」时阅读本章。**只读查询、导出已有规划、讨论方案**等任务**不得**阅读本章，也**不得**执行 `planning generate` / `planning regenerate`。

### 目标与固定链路

**上下文中已有 `<knowledge_base_selection>`（用户已选具体知识库，见 `references/core/knowledge-base-resolution.md`）时：**

```
收集月份 / 类型 / 频次 → 确认摘要 → generate [--watch] → 验证结果
```

**尚未确定知识库企业 ID 时：**

```
用户选择企业 → 解析知识库企业 ID → 收集月份 / 类型 / 频次 → 确认摘要 → generate [--watch] → 验证结果
```

界面和对话中向用户展示**企业名称**；调用接口时使用**知识库企业 ID**（`comid`，与 `planning enterprises` 返回的 `id` / `folders[].id` 同口径）。不要把组织 `belong-to-id` 当作知识库企业 ID。

### 用户已选知识库

见 **`references/core/knowledge-base-resolution.md`**（解析 `<knowledge_base_selection>`、默认跳过 `planning enterprises`、语义对齐、例外与 ID 映射）。

规划域：`comid=` → `--enterprise-id`，库名 → `--enterprise-name`。无已选库时走下方「解析企业」与 `planning enterprises`。

### 生成前收集信息

#### 必填

1. **知识库企业**：按 `references/core/knowledge-base-resolution.md` 确定 ID 与名称；无已选库时优先接收企业名称，再经 `planning enterprises` 解析。
2. **规划月份**：格式 `YYYY-MM`。
3. **内容类型**：`post`（图文）和/或 `video`（视频）。
4. **发布频次**：每周几条或每月几条。

#### 选填

- 营销目标
- 核心产品
- 目标市场
- 关键节点或活动
- 内容语调
- 合作总月数（6 / 12 / 24）及合作开始月份

缺少选填项时允许由企业知识库与模型推断，**不要阻塞生成**。缺少必填项时，只询问尚缺的信息。

### 两种「企业 ID」勿混用

业务上都叫「企业 ID」，CLI 里对应**两个不同字段**，混用会导致查不到企业或生成失败。

| 名称              | 出现位置                                                                      | 含义                                                           | 用于                                                                 |
| ----------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------- |
| **知识库企业 ID** | `<knowledge_base_selection>` 中的 `comid=`；或 `planning enterprises` 的 `id` | 知识库里的企业目录 ID（**comid**）                             | `planning generate --enterprise-id`、`planning list --enterprise-id` |
| **组织归属 ID**   | `planning enterprises --belong-to-id`                                         | 当前登录账号所属组织（类似 RAG 的 `belongToId` / `companyId`） | **仅**查询企业目录时的筛选参数                                       |

**需要解析企业时（无 `<knowledge_base_selection>`）：**

1. 跑 `planning enterprises`（一般**不要**传 `--belong-to-id`，除非明确要按组织筛选）。
2. 从输出表格列「知识库企业ID」/「企业名称」，或 `--json-out` 落盘数据的 `folders[].id` / `folders[].name`，取 ID 与名称。
3. 将二者分别填入 `planning generate --enterprise-id` 与 `--enterprise-name`。

**禁止：** 把 `--belong-to-id`、RAG 用的 `belongToId` / `companyId` 当作 `--enterprise-id`。

### TaskID 与 PlanID

| 标识       | 来源                                                                                                                                | 用途                                                                   |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **TaskID** | `planning generate` / `planning regenerate` stdout；`planning list` 表格「TaskID」列                                                | `planning watch`、`planning task cancel/retry/delete`                  |
| **PlanID** | `planning watch` 或 `generate/regenerate --watch` 完成时 stdout「规划ID」；`planning list --json-out` 落盘数据中的 `list[].plan.id` | `planning get`、`planning regenerate`、`planning export txt --plan-id` |

`planning list` **表格只显示 TaskID**，不显示 PlanID。未加 `--watch` 时，需 `planning watch <taskId>` 等到完成后从 stdout 取 PlanID，或对 list 使用 `--json-out` 读 `plan.id`。

### 执行步骤

**CLI 命令链：**

```
[可选 enterprises] → generate [--watch] → get → export txt
                       └─ 或 generate 后 planning watch <taskId>
```

**Agent 步骤：**

1. **检查环境**：确认 `siluzan-cso` 已安装；401 时引导 `siluzan-cso login`（见 `references/setup.md`）。不要展示或记录令牌。
2. **确定企业**：按 `references/core/knowledge-base-resolution.md`；无已选库时跑 `planning enterprises` 按名称匹配（`--json-out` 落盘、多个近似匹配让用户选、无匹配则停止且禁止猜 ID）。
3. **确认生成摘要**：写入前展示一行摘要并取得明确确认，例如：

   > 海科佳｜2026-07｜图文 + 视频｜每周 2 条｜目标：获取海外询盘｜重点产品：智能挂面生产线

   同时说明系统将根据所选知识库企业 ID 读取该企业知识并生成规划。

4. **生成并监控**：把每周频次映射为 `--freq-unit week --freq-count N`，每月频次映射为 `--freq-unit month --freq-count N`（**须同时提供**）。只传用户提供或已明确确认的选填参数，**不要把空字符串作为参数传入**。
5. **验证结果**：从 watch 完成输出或 `planning get <planId> --json-out` 核对（见下文「验证清单」）。未通过时先说明具体问题，征得确认后执行 `planning regenerate <planId> --watch`。

### 示例：生成月度规划

```bash
# Step 1（无已选库时）：见 references/core/knowledge-base-resolution.md → planning enterprises
# 有 <knowledge_base_selection> 时跳过本步，comid/库名取自该段
siluzan-cso planning enterprises
# 可选：按组织筛选目录（勿将此值用于 generate）
# siluzan-cso planning enterprises --belong-to-id <组织归属ID>

# Step 2：发起生成任务（id/name 来自 <knowledge_base_selection>，或 Step 1）
siluzan-cso planning generate \
  --enterprise-id <comid> \
  --enterprise-name "<企业名称>" \
  --year-month 2026-07 \
  --content-types post,video \
  --freq-unit week \
  --freq-count 2 \
  --marketing-goal "获取海外询盘" \
  --key-products "智能挂面生产线" \
  --target-markets 中亚,东南亚 \
  --partnership-total-months 12 \
  --watch

# Step 3：监控生成进度（未加 --watch 时；TaskID 来自 generate stdout）
siluzan-cso planning watch <taskId>
# 完成后 stdout 会打印「规划ID: <planId>」

# Step 4：查看规划详情（PlanID 来自 Step 3 完成输出，或 generate --watch 完成输出）
siluzan-cso planning get <planId>
# 需要完整 JSON 时加 --json-out <目录或 *.json>

# Step 5：导出为 TXT 文件（--plan-id 与 --input 二选一；-o/--output 可省略则自动命名）
siluzan-cso planning export txt --plan-id <planId> -o plan.txt
```

### 验证清单

生成完成后核对：

- 企业与月份正确。
- 所选图文/视频类型完整。
- 条数与频次一致。
- 内容确实体现该企业的产品、行业、应用场景、客户或展会信息，而非通用空话。
- 不编造知识库没有支持的认证、参数、客户或案例。
- 规划逻辑体现企业所属行业及 B2B 决策特点。

### 输出结构（面向用户交付）

#### 规划总体信息

- 企业
- 规划月份
- 内容类型
- 发布频次
- **依据知识库**：概括本次实际使用的企业资料类型（官网、品牌手册、产品特性、应用场景、展会或客户案例等）。不要宣称使用了未验证的资料。
- **规划逻辑**：优先说明企业行业、目标受众和 B2B 决策特征，再说明「建立认知 → 强化专业与信任 → 引导合作」的内容节奏。

#### 单条内容字段

图文和视频分别成表，每条包含：

| 字段     | 要求                                               |
| -------- | -------------------------------------------------- |
| 周次     | 每周 2 条时使用「第一周-1、第一周-2」等格式        |
| 方向分类 | 如品牌认知、产品价值、专业知识、案例背书           |
| 主题     | 可直接用于评审的选题标题                           |
| 内容方向 | 说明该主题具体讲什么，不写「结合知识库」等内部措辞 |
| 目标受众 | 明确到工厂老板、采购经理、经销商、技术负责人等     |

不要增加平台列；平台分发不属于当前规划维度。图文与视频均被选择时必须分成两张表。

### 内容质量规则

- 把规划定位为供企业内部运营或代运营团队评审的**月度半成品**，规划到主题和方向，不直接扩写整篇文案或完整脚本。
- 用企业真实名称、真实业务和真实产品，避免「企业 A」「某产品」等占位表达。
- 让图文侧重专业解释、选型和决策支持；让视频侧重流程、场景、设备运转和直观传播。
- 避免每条内容重复同一个卖点；覆盖认知、专业、信任和转化阶段。
- 对外可见的「内容方向」中**不得**出现「根据知识库」「结合知识库」「AI 生成」等内部过程词。
- 当知识不足时明确指出缺口，不用行业常识冒充企业事实。

---

## 命令速查

| 命令                            | 说明                                                             |
| ------------------------------- | ---------------------------------------------------------------- |
| `planning enterprises`          | 查询企业目录（无 `<knowledge_base_selection>` 时生成前先选企业） |
| `planning content-types`        | 查询可用内容类型（post / video）                                 |
| `planning generate`             | 创建规划生成任务                                                 |
| `planning watch <taskId>`       | 监听生成任务进度（SSE 实时推送）                                 |
| `planning list`                 | 查询规划任务列表                                                 |
| `planning get <planId>`         | 获取规划详情                                                     |
| `planning regenerate <planId>`  | 对已有规划重新生成                                               |
| `planning task cancel <taskId>` | 取消任务                                                         |
| `planning task retry <taskId>`  | 重试失败/取消的任务                                              |
| `planning task delete <taskId>` | 删除任务                                                         |
| `planning export txt`           | 导出规划为 TXT（Markdown 表格格式）                              |

---

## planning enterprises — 查询企业目录

```bash
# 默认：列出可选企业（取输出 id 用于 generate）
siluzan-cso planning enterprises

# 落盘完整数据（id 在 folders[].id），脚本读盘见 references/core/tips.md
siluzan-cso planning enterprises --json-out ./snap-cso

# 按组织归属筛选（高级用法；该 ID 不可用于 generate）
siluzan-cso planning enterprises --belong-to-id <组织归属ID>
```

| 参数             | 说明                                                                                     |
| ---------------- | ---------------------------------------------------------------------------------------- |
| `--belong-to-id` | 组织归属 ID（`companyId`），仅传给素材库 querylist 做筛选；**不是** generate 用的企业 ID |
| `--page-size`    | 目录条数上限（默认 100）                                                                 |

> 上下文中已有 `<knowledge_base_selection>` 时，生成流程**不必**调用本命令；仅在没有已选库或需核对名称时使用。

---

## generate 主要参数

| 参数                             | 必填 | 说明                                                                                                                       |
| -------------------------------- | ---- | -------------------------------------------------------------------------------------------------------------------------- |
| `--enterprise-id`                | ✅   | 知识库企业 ID（`<knowledge_base_selection>` 中的 `comid=`，或 `planning enterprises` 的 `id`；**不是** `--belong-to-id`）  |
| `--enterprise-name`              | ✅   | 企业名称（`<knowledge_base_selection>` 中的库名，或 `planning enterprises` 的 `name`，须与 `--enterprise-id` 配套）        |
| `--year-month`                   | ✅   | 规划月份，格式 `YYYY-MM`                                                                                                   |
| `--content-types`                | ✅   | 内容类型，支持逗号或空格：`post`（图文）/ `video`（视频）                                                                  |
| `--freq-unit`                    | —    | 发布频率单位：`week` / `month`；与 `--freq-count` **须同时提供**（只传其一 CLI 报错）                                      |
| `--freq-count`                   | —    | 发布频率数量（正整数）；与 `--freq-unit` **须同时提供**                                                                    |
| `--marketing-goal`               | —    | 营销目标（自然语言描述）                                                                                                   |
| `--key-products`                 | —    | 重点产品                                                                                                                   |
| `--target-markets`               | —    | 目标市场 `string[]`：`全球` **单独选**；或从 `中亚`、`非洲`、`拉美`、`中东`、`独联体`、`东南亚` 多选（**不可与全球同选**） |
| `--key-events`                   | —    | 重要节点/活动                                                                                                              |
| `--content-tone`                 | —    | 内容风格（如「专业严肃」/「轻松活泼」）                                                                                    |
| `--partnership-total-months`     | —    | 合作总月数：`6` / `12` / `24`（默认 12）                                                                                   |
| `--partnership-start-year-month` | —    | 合作开始月份 `YYYY-MM`（与规划月相同时不会传给接口）                                                                       |
| `--watch`                        | —    | 生成后自动监听进度，无需单独执行 watch                                                                                     |
| `--watch-timeout <seconds>`      | —    | 监听超时秒数（默认 300）                                                                                                   |

---

## planning list — 查询任务列表

```bash
# 查所有规划任务
siluzan-cso planning list

# 按企业筛选（知识库企业 ID；可用 <knowledge_base_selection> 中的 comid，不是 belongToId）
siluzan-cso planning list --enterprise-id <id>

# 按月份筛选
siluzan-cso planning list --year-month 2026-05

# 分页（默认 page-index=1，page-size=10）
siluzan-cso planning list --page-index 1 --page-size 20

# 落盘完整列表（含 list[].plan.id 等；表格 stdout 不含 PlanID）
siluzan-cso planning list --json-out ./snap-cso
```

| 参数              | 说明                            |
| ----------------- | ------------------------------- |
| `--enterprise-id` | 知识库企业 ID（同 generate）    |
| `--year-month`    | 规划月份 `YYYY-MM`              |
| `--page-index`    | 页码（默认 1）                  |
| `--page-size`     | 每页条数（默认 10）             |
| `--json-out`      | 落盘完整列表；stdout 仅一行摘要 |

表格列：**TaskID**、状态、企业ID、规划月、内容类型。

---

## planning watch — 监听任务进度

```bash
siluzan-cso planning watch <taskId>
siluzan-cso planning watch <taskId> --timeout 600
```

| 参数        | 说明                                  |
| ----------- | ------------------------------------- |
| `<taskId>`  | 必填，来自 generate/regenerate stdout |
| `--timeout` | 监听超时秒数（默认 300）              |

完成后 stdout 打印 **规划ID**；失败/取消/超时会 exit 1。

> `generate --watch` / `regenerate --watch` 使用 **`--watch-timeout`**（非本命令的 `--timeout`）。

---

## planning regenerate — 再生成

```bash
siluzan-cso planning regenerate <planId>
siluzan-cso planning regenerate <planId> --watch
siluzan-cso planning regenerate <planId> --watch --watch-timeout 600
```

| 参数              | 说明                                   |
| ----------------- | -------------------------------------- |
| `<planId>`        | 必填，已有规划 ID                      |
| `--watch`         | 提交后自动监听直到完成/失败            |
| `--watch-timeout` | 监听超时秒数（默认 300；需 `--watch`） |

再生成 stdout 返回新 **TaskID**；加 `--watch` 时完成后可能打印新 **规划ID**。

---

## planning get — 规划详情字段

`planning get <planId> --json-out <路径>` 落盘完整规划对象（stdout 仅一行摘要，脚本读盘见 `references/core/tips.md`）。以下仅列**写稿、排期、复用规划**时真正需要关注的字段（Cosmos `_rid` / `_etag` / `PartitionKey` 等存储字段可忽略）。

### 规划主体

| 字段                       | 说明                                                                                    |
| -------------------------- | --------------------------------------------------------------------------------------- |
| `id`                       | 规划 ID，再生成、导出时引用                                                             |
| `enterpriseIds`            | 企业 ID 列表（通常一项）                                                                |
| `enterpriseName`           | 企业名称                                                                                |
| `yearMonth`                | 规划月份 `YYYY-MM`                                                                      |
| `contentTypes`             | 已规划体裁：`post`（图文）、`video`（视频）                                             |
| `frequency`                | 发布频次：`perWeek` 或 `perMonth`（与 generate 的 `--freq-unit` / `--freq-count` 对应） |
| `targetMarkets`            | 目标市场 `string[]`；`全球` 与区域项互斥，规则同 `--target-markets`                     |
| `strategyBrief`            | 用户侧策略简报原文，本月叙事与重点的**总纲**                                            |
| `contextUsed`              | 生成时采用的背景摘要（含知识库/业务语境），写稿前建议先读                               |
| `planRationale`            | 本月排期逻辑（周次节奏、阶段目标），export txt 会写入「规划逻辑」                       |
| `postItems` / `videoItems` | 图文 / 视频选题表，见下表                                                               |

### 长期合作周期（影响阶段化叙事）

生成时可传 `--partnership-total-months`（6/12/24）与可选 `--partnership-start-year-month`；详情里会回显当前处于合作周期的哪一段：

| 字段                        | 说明                                                     |
| --------------------------- | -------------------------------------------------------- |
| `partnershipTotalMonths`    | 合作总月数（6 / 12 / 24）                                |
| `partnershipStartYearMonth` | 合作起始月 `YYYY-MM`                                     |
| `partnershipMonthIndex`     | 当前是合作第几个月（从 1 起）                            |
| `partnershipPhaseSlot`      | 阶段槽位（长周期内分段策略用，与总月数配合理解本月侧重） |

### 选题行（`postItems` / `videoItems` 每项）

| 字段                 | 说明                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------- |
| `week`               | 排期周次，如 `第一周(4月1日-7日)-1`（同周多条以 `-1`、`-2` 区分）                     |
| `contentDirection`   | 方向分类（案例、TCO、展会等标签）                                                     |
| `topic`              | 选题标题                                                                              |
| `mainDirection`      | 本条内容的撰写/拍摄要点与转化导向                                                     |
| `targetAudience`     | 目标受众                                                                              |
| `referenceMaterials` | 建议引用的素材或资料线索；**仅 `--json-out` 落盘数据可见**，`export txt` 表格不含此列 |

按 `week` 排序即可还原月度节奏；写具体稿件时优先组合 `mainDirection` + `referenceMaterials`，并对照 `planRationale` 与 `strategyBrief` 保持口径一致。

---

## planning export txt — 导出

```bash
# 从服务端拉取规划并导出（常用）
siluzan-cso planning export txt --plan-id <planId> -o <文件路径>

# 从本地 JSON 导出（如 planning get --json-out 落盘文件）
siluzan-cso planning export txt --input <本地规划.json> -o <文件路径>

# 省略 -o/--output 时按「内容选题方向规划_<企业>_<月份>.txt」自动命名
siluzan-cso planning export txt --plan-id <planId>
```

| 参数           | 说明                                        |
| -------------- | ------------------------------------------- |
| `--plan-id`    | 规划 ID（与 `--input` 二选一）              |
| `--input`      | 本地规划 JSON 文件（与 `--plan-id` 二选一） |
| `-o, --output` | 导出路径；省略则自动命名                    |

导出内容为 Markdown 表格 TXT，含「依据知识库」（`contextUsed`）、「规划逻辑」（`planRationale`）及图文/视频表（表头：周次、方向分类、主题、内容方向、目标受众）。

---

## 导出与交付

用户要求导出时执行 `planning export txt`（见上节）。导出后确认文件存在且包含总体信息、规划逻辑以及图文/视频表。最终回复简洁报告：企业、月份、内容类型、频次、规划 ID 和导出路径。

---

## 错误处理

| 情况           | 处理                                                          |
| -------------- | ------------------------------------------------------------- |
| `400`          | 检查企业 ID、月份、内容类型和频次参数                         |
| `401`          | 要求重新登录                                                  |
| `500`          | 稍后重试；持续失败时报告服务端异常，**不伪造规划结果**        |
| 企业目录无结果 | 停止生成，提示先把企业加入知识库企业目录                      |
| 生成超时       | 查询 `planning list` 确认后台任务状态，**不重复提交同一任务** |
