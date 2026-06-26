# 本机写审计与补偿写（TSO）

## 术语

- **补偿写**：再次调用写接口，把资源字段写回「写前快照」中的状态；**不是**数据库或平台的事务回滚 API。
- **真值在磁盘**：检索与定位一律通过 `siluzan-tso audit list` / `audit show` 读 `~/.siluzan/write-audit/tso/*.jsonl`，**不要**依赖对话中的历史列表。
- **resourceKey**：写审计在变异请求时由 `host+pathname` 派生，**同一资源的多次写共享同一 key**——`restore-plan` 据此扫描"目标 audit 之后该资源还有哪些写"，让你看见回退会顺带覆盖什么。

## 写操作必填 commit

凡发往业务网关的 `POST`/`PUT`/`PATCH`/`DELETE`（经 `apiFetch` / `apiDeleteRaw`）必须提供其一：

- 命令行：`--commit "说明"`（可出现在任意位置，与 `grep` 解析一致）

二者同时存在时 **命令行优先**。缺省则 CLI **stderr 报错并退出**，不发起 HTTP。

`audit list`、`audit show`、`audit restore-plan` 不产生业务写，不要求 commit。`audit restore-apply` 须加 `--i-confirm` 与 `--ack-subsequent-writes`；若仍未传 commit，会自动使用 `compensate:restore:<auditId>` 作为本条补偿写的说明。

## 可选 runId

批量脚本可设 `SILUZAN_AUDIT_RUN_ID`，与审计字段 `runId` 一并写入，便于 `audit list --run-id` 过滤。

## 写前快照（白名单）

仅当 PUT/PATCH 命中以下 **Google 广告网关** 路径时，CLI 会在写前自动 `GET` 同 URL（去 query），快照存于 `write-audit/tso/snapshots/<auditId>.json`，审计行含 `preSnapshotRef`：

1. `/SemManagement/...` —— 历史在用的优化/系列侧接口
2. `/campaignmanagement/campaign/{accountId}/{campaignId}` —— 广告系列单资源详情（`ad campaign-status / campaign-delete / campaign-edit` 走这里）

未命中时审计行只有 `preSnapshotSkipped`、不会阻断主请求；`restore-plan` 也会返回 `supportability.code = "no_snapshot"` 并给出"人工反向写"的 hint。

明确**未纳入**白名单的资源（业务代码绕开了"单资源 GET"，要么端点不可靠、要么 GET shape 与 PUT body 不对齐——盲目 apply 会写错形状）：

- `/adgroupnmanagement/adgroup/{acc}/{id}`（业务走 list + filter）
- `/admanagement/campaign/{acc}/{adId}`（业务走 list + filter）
- `/keywordmanagement/Keyword/{acc}/batch`（批量 PUT，body 是数组）
- `/negativekeywordmanagement/negativekeyword/{acc}/{id}`（业务走 list + filter）
- `/campaignmanagement/` 下的 `v2/list/...`、`v2/(targeted|excluded)locations/...`、`criterion/...`、`geolocations/...`

POST 创建型与 DELETE 删除型 **整体**不在快照白名单内，`restore-plan` 会给出 `unsupported_method_post` / `unsupported_method_delete` 的明确诊断与下一步建议。

## restore-plan 输出结构（Agent 决策依据）

```jsonc
{
  "auditDir": "...",
  "plan": {
    "auditId": "...",
    "resourceKey": "googleapi.mysiluzan.com/SemManagement/...",
    "supportability": {
      "code": "ready_put_patch | audit_not_found | v1_record_no_audit_id | not_success_write | no_snapshot | snapshot_missing_or_invalid | unsupported_method_post | unsupported_method_delete | unsupported_method_other",
      "reason": "一句话原因",
      "hint": "仅 unsupported 时给出的人/Agent 下一步建议",
    },
    "willMutate": true,
    "target": {
      "ts": "...",
      "method": "PUT",
      "pathname": "...",
      "outcome": "success",
      "commit": "...",
      "invokedCommand": "...",
      "httpStatus": 200,
    },
    "snapshot": {
      "capturedAt": "...",
      "originalMethod": "PUT",
      "originalUrl": "...",
      "bodyUtf8Length": 1234,
      "bodySha256Prefix": "...",
    },
    "subsequentWrites": [
      {
        "auditId": "...",
        "ts": "...",
        "method": "PUT",
        "outcome": "success",
        "pathname": "...",
        "commit": "...",
        "hasSnapshot": true,
      },
    ],
    "guardChecks": { "ackSubsequentWrites": 0 },
    "steps": [
      {
        "order": 1,
        "method": "PUT",
        "url": "...",
        "body": {
          /* snapshot.body */
        },
        "bodyUtf8Length": 1234,
        "bodySha256Prefix": "...",
      },
    ],
  },
}
```

要点：

- `supportability.code` 是分流路标，Agent 必须据此判断是否进入 apply 分支。
- `subsequentWrites` 列出 **同 resourceKey、ts > target.ts** 的全部写（成功+失败）。`guardChecks.ackSubsequentWrites` 则是其中**成功**的数量——`restore-apply` 会要求显式确认。
- `steps` 仅在 `supportability.code === "ready_put_patch"` 时非空，单步 PUT/PATCH 重放 `snapshot.body`。

## restore-apply 守卫

```
siluzan-tso audit restore-apply \
  --id <auditId> \
  --i-confirm \
  --ack-subsequent-writes <plan.guardChecks.ackSubsequentWrites>
```

- `--i-confirm`：人/Agent 已读 plan，承担覆盖风险。
- `--ack-subsequent-writes <N>`：必须等于 plan 显示的成功后续写数量。**apply 时会再 build 一次上下文**：如果 N 与最新扫描结果不一致（说明 plan→apply 期间又发生了新写），CLI 会拒绝执行——这是防 TOCTOU 的关键守卫。

## 自主回退工作流（Agent / 人类）

1. **定位 audit**：`siluzan-tso audit list --days 14 --match "关键词" --json-out ./snap`。
2. **看完整审计行**：`siluzan-tso audit show --id <auditId> --json-out ./snap`，确认 `preSnapshotFileReadable === true`。
3. **生成回退计划**：`siluzan-tso audit restore-plan --id <auditId> --json-out ./snap`。
   - 检查 `plan.supportability.code === "ready_put_patch"`。
   - **必读** `plan.subsequentWrites`：若存在成功的后续写，意味着回退会覆盖那些更晚的修改；按需可先用 `siluzan-tso audit list --resource-key "<plan.resourceKey>" --json-out ./snap` 把同资源全量历史拉出来交叉确认。
   - 决定是接受这个覆盖，还是放弃回退/换另一种修复路径。
4. **执行**：`siluzan-tso audit restore-apply --id <auditId> --i-confirm --ack-subsequent-writes <N>`，N 来自 plan.guardChecks.ackSubsequentWrites。

**禁止**跳过 `restore-plan` 直接 `restore-apply`。
**禁止**根据 `commit` 文本编造请求体；**必须以** `restore-plan` 输出的 `steps[].body` 为准。
**禁止**在 `subsequentWrites` 非空且未与用户确认的情况下，盲目用 plan 中的数字 ack 后强行 apply。

## v1 历史审计

旧版 JSONL 无 `auditId`/`commit`/`preSnapshotRef`，`restore-plan` 会返回 `supportability.code === "v1_record_no_audit_id"` / `audit_not_found`，无法 `restore-apply`，仅可作 `audit show` 参考。
