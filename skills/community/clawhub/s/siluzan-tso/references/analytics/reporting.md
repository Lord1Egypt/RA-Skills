# TSO 优化报告与推送

> 所属 skill：`siluzan-tso`。
>
> 本文档仅覆盖 **TSO steward 优化报告**：列表、生成、删除、邮件推送与查看链接。  
> **账户分析拉数**（`google-analysis`、`facebook-analysis`、`report tiktok-*`、`report bing-*`、`report meta-overview`）与**周期/诊断报告纲要**见 `references/analytics/account-analytics.md`（Facebook 撰写见 `facebook-analysis-guide.md`）。  
> **异步批量创建记录**（`ad batch`）见 `references/google-ads/google-ads.md` § ad batch。  
> **AI 广告优化**（`optimize`）见 `references/operations/optimize.md`。  
> **广告线索**（`clue`）见 `references/operations/clue.md`。

---

## report — 优化报告

### report list — 查询报告列表

```bash
siluzan-tso report list -m <媒体> [选项]
```

| 选项                     | 说明                                 |
| ------------------------ | ------------------------------------ |
| `-m, --media`            | 媒体类型（必填）：`Google \| TikTok` |
| `-t, --type <type>`      | 报告类型：`Daily \| Hourly`          |
| `-s, --status <ready>`   | 是否已生成：`true \| false`          |
| `-k, --keyword <text>`   | 报告名称关键字                       |
| `--start / --end <date>` | 日期范围（YYYY-MM-DD）               |
| `--json-out`             | 输出原始 JSON                        |

**仅 JSON 交付**：若用户明确要求「只输出一个 JSON / 不要解释」，回复中**只放一个** JSON 代码块（与本次 CLI stdout 一致），前后不加说明文字；分页结果以 JSON 内 `page` / `pageSize` / `total` / `itemCount` 为准，需全量时再翻页执行。

**示例：**

```bash
# 查询所有 Google 报告
siluzan-tso report list -m Google

# 查询本月 TikTok 日报
siluzan-tso report list -m TikTok -t Daily --start 2026-03-01 --end 2026-03-31

# 只看已生成完成的报告
siluzan-tso report list -m Google --status true --json-out ./snap
```

---

### report create — 批量生成报告

```bash
siluzan-tso report create -m <媒体> -a <账户ID列表> -t <类型> --start <date> --end <date>
```

| 选项                   | 说明                                                                                   | 必填 |
| ---------------------- | -------------------------------------------------------------------------------------- | ---- |
| `-m, --media`          | 媒体类型                                                                               | ✅   |
| `-a, --accounts <ids>` | 账户 `mediaCustomerId`（数字 ID），逗号分隔。**注意：不是 `entityId`**，内部会自动转换 | ✅   |
| `-t, --type`           | 报告类型                                                                               | ✅   |
| `--start / --end`      | 日期范围                                                                               | ✅   |

**示例：**

```bash
# 为 Google 账户生成本月日报（传 mediaCustomerId）
siluzan-tso report create \
  -m Google \
  -a 6326027735 \
  -t Daily \
  --start 2026-03-01 \
  --end 2026-03-31

# 多账户，生成昨天的小时报
siluzan-tso report create -m Google -a 6326027735,4545500137 -t Hourly --start 2026-03-19 --end 2026-03-19
```

---

### report delete — 删除报告

```bash
siluzan-tso report delete --id <entityId>
siluzan-tso report delete --ids <id1,id2,id3>
```

**示例：**

```bash
siluzan-tso report delete --id rpt_abc123

# 批量删除
siluzan-tso report delete --ids rpt_abc123,rpt_def456
```

---

### report push — 优化报告推送管理

**媒体**：仅 **`Google`**、**`TikTok`**。

#### list — 推送配置列表

```bash
siluzan-tso report push list -m <媒体> [选项]
```

| 选项                 | 说明                            |
| -------------------- | ------------------------------- |
| `-k, --keyword`      | `Name`                          |
| `-t, --type`         | `ReportType`                    |
| `--stopped`          | 仅已停用                        |
| `--start` / `--end`  | 日期筛选                        |
| `-p` / `--page-size` | 分页                            |
| `--json-out`         | 原始 JSON（列表信封 + `items`） |

#### create — 新建推送

`--media-accounts` 传账户 **entityId**（非 `mediaCustomerId`）。Google 可选 `--ai-suggest`。

```bash
siluzan-tso report push create -m Google \
  --name "我的日报" \
  --media-accounts <entityId1>,<entityId2> \
  --emails a@b.com,c@d.com \
  --types Daily,Weekly \
  [--title "邮件标题"] \
  [--ai-suggest]
```

#### update — 编辑推送

`--id` 为推送配置的 **entityId**（来自 `push list --json-out` 的 `items[].entityId`）。

```bash
siluzan-tso report push update -m Google --id <配置UUID> \
  --name "..." \
  --media-accounts <entityId...> \
  --emails ... \
  --types Daily \
  [--title "..."] [--ai-suggest]
```

#### history — 推送记录

`--setting-id` = 推送规则的 **entityId**（与 `push list --json-out` 的 `items[].entityId` 相同）。`--media-account-id` 筛选时为账户 **entityId**。日期传 `YYYY-MM-DD` 时 CLI 会加成 `T00:00:00+08:00`。

```bash
siluzan-tso report push history -m Google --setting-id <规则entityId> [--json-out ./snap]
siluzan-tso report push history -m Google --setting-id <规则entityId> \
  --start 2026-03-01 --end 2026-03-31 \
  --receive-email x@y.com --report-type Daily --media-account-id <账户entityId>
```

#### start / stop / delete

`--id` 为推送配置 **entityId**。

```bash
siluzan-tso report push start  -m Google --id <entityId>
siluzan-tso report push stop   -m Google --id <entityId>
siluzan-tso report push delete -m Google --id <entityId>
```

**示例：**

```bash
siluzan-tso report push list -m Google --page-size 10 --json-out ./snap

siluzan-tso report push create -m Google --name "测试" \
  --media-accounts 6659e68b-973c-40bb-980c-6af20fbefe7d \
  --emails user@example.com --types Daily --title "日报"

siluzan-tso report push update -m Google --id be5e4a03-2e0f-4bb2-bcad-e9dd86250e18 \
  --name "刘奇测试" \
  --media-accounts 6659e68b-973c-40bb-980c-6af20fbefe7d \
  --emails liuqi@chenggongyi.com --types Daily

siluzan-tso report push history -m Google --setting-id be5e4a03-2e0f-4bb2-bcad-e9dd86250e18 --json-out ./snap
```

#### receive-emails — 历史收件邮箱

查询当前租户下推送配置曾用过的收件邮箱列表（`string[]`）。

```bash
siluzan-tso report push receive-emails -m Google [--json-out ./snap]
```

---

### 查看报告（引导打开网页）

报告生成后，在网页查看。先用 `siluzan-tso config show` 获取 `webUrl`，再按以下规则拼接链接：

| 媒体   | 报告类型         | URL 模板                                                    |
| ------ | ---------------- | ----------------------------------------------------------- |
| Google | 日报（Daily）    | `https://www.siluzan.com/media-report/publish/{entityId}?culture=zh-CN` |
| Google | 小时报（Hourly） | `https://www.siluzan.com/media-report/hour/{entityId}?culture=zh-CN`    |
| TikTok | 日报             | `https://www.siluzan.com/media-report/publish/{entityId}?culture=zh-CN` |

`entityId` 来自 `siluzan-tso report list --json-out ./snap` 中每条记录的 `entityId` 字段。

**示例流程：**

```bash
# 第一步：查询报告，获取 entityId
siluzan-tso report list -m Google --json-out ./snap
# 从输出中找到目标报告的 entityId，如 "rpt_abc123"

# 第二步：查看 webUrl
siluzan-tso config show
# webUrl: https://www.siluzan.com

# 第三步：拼接链接（Google 日报）
# https://www.siluzan.com/media-report/publish/rpt_abc123?culture=zh-CN
```
