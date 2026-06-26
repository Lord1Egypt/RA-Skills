# AI 广告优化记录（optimize）

> 所属 skill：`siluzan-tso`。

```bash
siluzan-tso optimize list    [选项]                  # 账户级优化主列表
siluzan-tso optimize records [选项]                  # 优化操作记录列表（系列粒度，见下）
siluzan-tso optimize get --id <id>                   # 单条详情
siluzan-tso optimize children --parent-id <id>       # 广告系列级明细
```

| 选项                             | 说明                                                                                                                                                                                    |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-a, --account <id>`             | 账户 `mediaCustomerId`（走接口筛选；**已脱管账户可能为空**）                                                                                                                            |
| `--match-media-customer-id <id>` | **仅 `list`**：不按接口筛账户，拉全量后自动翻页、客户端匹配 `mediaCustomerId`（适合已不在 Siluzan 托管、但历史上仍有优化批次的 Google 客户号）                                          |
| `--start / --end <date>`         | 日期范围（YYYY-MM-DD，所有日期按北京时间（UTC+8）解释，调用时自动附加 `+08:00` 时区偏移）                                                                                               |
| `--id <id>`                      | `optimize get` 专用：UUID。常见来源——**账户批次**：`optimize list --json-out ./snap` 的 `items[].id` / `entityId`；**系列级记录**：`optimize records --json-out ./snap` 的 `items[].id` |
| `--parent-id <id>`               | 父级 ID（`children` 专用；与账户批次 `list` 里 `items[].id` 一致）                                                                                                                      |
| `--json-out`                     | 输出原始 JSON（`list` / `records` / `children`）                                                                                                                                        |

## 已脱管 / 非当前托管账户：怎么查历史优化？

1. **不要用** `optimize list -a <客户号>`（后端常按当前可管账户过滤，脱管后可能 0 条）。
2. **也不要依赖** `optimize records -a <客户号>`（列表项往往没有 `mediaCustomerId`，接口侧筛选也可能无效）。
3. **应使用**：`optimize list --match-media-customer-id <Google 客户号> [--start … --end …] --json-out ./snap`，在结果里取每条批次的 **`id`**（与 **`entityId`** 相同）。
4. 用该 **`id`**：`optimize get --id <id>` 看详情；`optimize children --parent-id <id>` 看该批次下各广告系列级明细。

**示例：**

```bash
# 查询指定账户的优化建议列表（当前仍托管、接口可筛时）
siluzan-tso optimize list -a 6326027735

# 已脱管：从全量历史里筛出该 Google 客户号（自动翻页）
siluzan-tso optimize list --match-media-customer-id 3013981480 --start 2025-05-01 --json-out ./snap

# 查询所有账户本月优化记录（系列级列表）
siluzan-tso optimize records --start 2026-03-01 --end 2026-03-31

# 查询某账户广告系列级明细（parentId = 上一步 list 里某条批次的 id）
siluzan-tso optimize children --parent-id 4ced1f51-da71-4aac-84f9-4e2c4a25675f

# 单条详情（id 可为 list 批次 id 或 records 系列记录 id）
siluzan-tso optimize get --id 4ced1f51-da71-4aac-84f9-4e2c4a25675f

# JSON 输出
siluzan-tso optimize list -a 6326027735 --json-out ./snap
```

`optimize get` 输出格式化 JSON 到 stdout；字段以后端返回为准。
