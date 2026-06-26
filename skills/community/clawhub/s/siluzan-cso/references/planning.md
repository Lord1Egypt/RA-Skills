# planning — AI 内容规划

> 对应 CSO Web 端 `/planning` 页面，AI 自动生成月度内容规划方案，支持任务进度监控、规划详情查看与导出。

---

## 工作流程

```
enterprises → generate → watch（监控进度）→ get（查看详情）→ export txt
```

---

## ⚠️ 两种「企业 ID」勿混用

业务上都叫「企业 ID」，CLI 里对应**两个不同字段**，混用会导致查不到企业或生成失败。

| 名称              | 出现位置                                            | 含义                                                           | 用于                                                                 |
| ----------------- | --------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------- |
| **知识库企业 ID** | `planning enterprises` 返回的 `id` / `folders[].id` | 知识库里的企业目录 ID                                          | `planning generate --enterprise-id`、`planning list --enterprise-id` |
| **组织归属 ID**   | `planning enterprises --belong-to-id`               | 当前登录账号所属组织（类似 RAG 的 `belongToId` / `companyId`） | **仅**查询企业目录时的筛选参数                                       |

**执行 generate 前必须：**

1. 先跑 `planning enterprises`（一般**不要**传 `--belong-to-id`，除非明确要按组织筛选）。
2. 从输出表格或 `--json-out` 落盘数据取 **知识库企业 ID**（`id` / `folders[].id`）与 **企业名称**（`name` / `folders[].name`）。
3. 将二者分别填入 `planning generate --enterprise-id` 与 `--enterprise-name`。

**禁止：** 把 `--belong-to-id`、`account me` 的 `companyId`、或 RAG 用的 `belongToId` 当作 `--enterprise-id`。

---

## 命令速查

| 命令                            | 说明                                |
| ------------------------------- | ----------------------------------- |
| `planning enterprises`          | 查询企业目录（生成前先选企业）      |
| `planning content-types`        | 查询可用内容类型（post / video）    |
| `planning generate`             | 创建规划生成任务                    |
| `planning watch <taskId>`       | 监听生成任务进度（SSE 实时推送）    |
| `planning list`                 | 查询规划任务列表                    |
| `planning get <planId>`         | 获取规划详情                        |
| `planning regenerate <planId>`  | 对已有规划重新生成                  |
| `planning task cancel <taskId>` | 取消任务                            |
| `planning task retry <taskId>`  | 重试失败/取消的任务                 |
| `planning task delete <taskId>` | 删除任务                            |
| `planning export txt`           | 导出规划为 TXT（Markdown 表格格式） |

---

## 示例：生成月度规划

```bash
# Step 1：查企业列表，从返回的 id 列（或 JSON 的 folders[].id）取知识库企业 ID
siluzan-cso planning enterprises
# 可选：按组织筛选目录（勿将此值用于 generate）
# siluzan-cso planning enterprises --belong-to-id <组织归属ID>

# Step 2：发起生成任务（id/name 均来自 Step 1，不是 belongToId）
siluzan-cso planning generate \
  --enterprise-id <folders[].id> \
  --enterprise-name "<folders[].name>" \
  --year-month 2026-05 \
  --content-types post,video \
  --marketing-goal "提升品牌曝光" \
  --key-products "新品 A" \
  --target-markets 中亚,东南亚 \
  --freq-unit week --freq-count 3

# Step 3：监控生成进度（taskId 来自 generate 输出）
siluzan-cso planning watch <taskId>

# Step 4：查看规划详情（planId 来自 list 输出）
siluzan-cso planning get <planId>

# Step 5：导出为 TXT 文件
siluzan-cso planning export txt --plan-id <planId> --output plan.md
```

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

---

## generate 主要参数

| 参数                | 必填 | 说明                                                                                                                       |
| ------------------- | ---- | -------------------------------------------------------------------------------------------------------------------------- |
| `--enterprise-id`   | ✅   | 知识库企业 ID（`planning enterprises` 返回的 `id`，**不是** `--belong-to-id`）                                             |
| `--enterprise-name` | ✅   | 企业名称（`planning enterprises` 返回的 `name`，须与 `--enterprise-id` 同行）                                              |
| `--year-month`      | ✅   | 规划月份，格式 `YYYY-MM`                                                                                                   |
| `--content-types`   | ✅   | 内容类型，逗号分隔：`post`（图文）/ `video`（视频）                                                                        |
| `--marketing-goal`  | —    | 营销目标（自然语言描述）                                                                                                   |
| `--key-products`    | —    | 重点产品                                                                                                                   |
| `--target-markets`  | —    | 目标市场 `string[]`：`全球` **单独选**；或从 `中亚`、`非洲`、`拉美`、`中东`、`独联体`、`东南亚` 多选（**不可与全球同选**） |
| `--key-events`      | —    | 重要节点/活动                                                                                                              |
| `--content-tone`    | —    | 内容风格（如"专业严肃"/"轻松活泼"）                                                                                        |
| `--freq-unit`       | —    | 发布频率单位：`week` / `month`                                                                                             |
| `--freq-count`      | —    | 发布频率数量（与 `--freq-unit` 同时使用）                                                                                  |
| `--watch`           | —    | 生成后自动监听进度，无需单独执行 watch                                                                                     |

---

## planning list — 查询任务列表

```bash
# 查所有规划任务
siluzan-cso planning list

# 按企业筛选（同样用 enterprises 返回的 id，不是 belongToId）
siluzan-cso planning list --enterprise-id <folders[].id>

# 按月份筛选
siluzan-cso planning list --year-month 2026-05
```

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

生成时需传 `--partnership-total-months`（6/12/24）与可选 `--partnership-start-year-month`；详情里会回显当前处于合作周期的哪一段：

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
