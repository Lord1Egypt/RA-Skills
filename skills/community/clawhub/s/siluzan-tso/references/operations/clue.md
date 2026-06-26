# 广告线索表单（clue）

> 所属 skill：`siluzan-tso`。
>
> 支持 **TikTok** 和 **Meta（Facebook）** 两种媒体。

> **注意**：线索数据直接来自媒体 API，**不支持服务端分页**，数据量大时建议 `--json-out <路径>` 落盘后自行处理。

```bash
siluzan-tso clue -m <媒体> -a <账户ID> [选项]
```

| 选项                 | 说明                                                              |
| -------------------- | ----------------------------------------------------------------- |
| `-m, --media`        | `TikTok \| Meta`（默认 TikTok）                                   |
| `-a, --account <id>` | TikTok：`advertiserId`（mediaCustomerId）；Meta：Facebook 页面 ID |
| `--region <region>`  | TikTok 专用：`eu \| us \| other \| ALL`（默认 ALL）               |
| `--start <date>`     | Meta 专用：开始日期（YYYY-MM-DD）                                 |
| `--end <date>`       | Meta 专用：结束日期（YYYY-MM-DD）                                 |
| `--json-out`         | 输出原始 JSON                                                     |

**AI 交付**：用户要求「原始 JSON / 自己筛」时，回复中须包含 **`--json-out` 命令打印的完整 JSON**（或等价完整代码块），并可按上表说明 `custom_fields` / `system_fields`（TikTok）或 `field_data`（Meta）。**禁止**用未出现在本次 CLI 输出中的账户 ID、媒体或「环境异常」类推测替代 JSON 交付。  
若本次查询失败：CLI 在 落盘 JSON 中会输出 **`{"ok":false,"error":"...","items":[]}`**（stdout），请**原样**贴出该 JSON，不要改成纯文字描述。

**时间范围（TikTok）**：用户说「最近一周」且要拉线索、未给起止日时，**不要**再按投放报表类任务做 A/B/C 反问；直接按 CLI 默认窗口执行 `clue -m TikTok -a <advertiserId> --json-out ./snap`（需自定义区间时再用 Meta 同款 `--start/--end` 仅适用于 Meta，TikTok 以接口返回为准）。

**TikTok 示例：**

```bash
# 查询 TikTok 全部区域线索
siluzan-tso clue -m TikTok -a 1234567890

# 只查欧洲区线索
siluzan-tso clue -m TikTok -a 1234567890 --region eu

# 查美国区，JSON 输出
siluzan-tso clue -m TikTok -a 1234567890 --region us --json-out ./snap
```

**Meta 示例：**

```bash
# 查询 Meta 线索（3月份）
siluzan-tso clue -m Meta -a 987654321 --start 2026-03-01 --end 2026-03-31

# JSON 输出
siluzan-tso clue -m Meta -a 987654321 --start 2026-03-01 --json-out ./snap
```

**输出字段说明（TikTok）：**

| 字段                                | 来源            |
| ----------------------------------- | --------------- |
| 姓名、邮箱、手机                    | `custom_fields` |
| 表单名、广告名、区域、时间、lead_id | `system_fields` |

**输出字段说明（Meta）：**

| 字段             | 来源         |
| ---------------- | ------------ |
| 姓名、邮箱、手机 | `field_data` |
| 表单名、创建时间 | 顶层字段     |
