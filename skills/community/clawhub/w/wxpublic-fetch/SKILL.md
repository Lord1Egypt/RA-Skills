---
name: wxpublic-fetch
description: 从微信公众号抓取文章并保存为本地 Markdown 文件。当用户提到"抓取公众号"、"获取公众号文章"、"下载微信文章"、"爬公众号"、"保存公众号内容"，或指定公众号名称和日期范围想要获取文章时，使用此 skill。抓取完成后记录所有保存的 md 文件路径，方便用户后续问答。
argument-hint: <公众号名称> [startDate yyyy-MM-dd] [endDate yyyy-MM-dd] [--output 保存目录] [--app-id <AppID>] [--secret <SecureKey>]
allowed-tools:
  - Bash
  - Write
  - Read
---

# 微信公众号文章抓取

用户调用方式示例：
```
/wxpublic-fetch 拆神
/wxpublic-fetch 拆神 2026-04-15 2026-04-21
/wxpublic-fetch 拆神 2026-04-01 2026-04-21 --output ~/articles
/wxpublic-fetch 拆神 --app-id ak_xxx --secret abc123
```

用户传入的参数：`$ARGUMENTS`

---

## 执行步骤

### 第一步：解析参数

> 告知用户：`[1/5] 正在解析参数...`

从 `$ARGUMENTS` 中提取：
- `name`（必填）：公众号名称，第一个非日期、非 `--output`、非 `--app-id`、非 `--secret` 的参数
- `startDate`（可选）：格式 `yyyy-MM-dd`，默认为今天往前 7 天
- `endDate`（可选）：格式 `yyyy-MM-dd`，默认为今天
- `--output <dir>`（可选）：文章保存目录，默认为 `~/wxpublic_articles/<name>`
- `--app-id <AppID>`（可选）：平台 AppID，若未提供则读取环境变量 `WXPUBLIC_APP_ID`
- `--secret <SecureKey>`（可选）：平台 SecureKey，若未提供则读取环境变量 `WXPUBLIC_SECURE_KEY`

如果参数不足（缺少公众号名称），告知用户正确用法并停止。
如果 `app_id` 和 `secure_key` 均为空（参数和环境变量都未设置），向用户说明：
1. 可通过 `--app-id` 和 `--secret` 参数传入，或设置环境变量 `WXPUBLIC_APP_ID` / `WXPUBLIC_SECURE_KEY`；
2. 如果尚未拥有 AppID 和 SecretKey，请前往 https://wxpub.aibana.art 注册并生成。
然后停止，等待用户提供凭证。

今天的日期可从系统获取：
```bash
date +%Y-%m-%d
```

计算 `startDate` 与 `endDate` 之间的天数差：
```bash
python3 -c "from datetime import date; print((date.fromisoformat('<endDate>') - date.fromisoformat('<startDate>')).days)"
```

如果天数差 **大于 60 天**（约 2 个月），**必须先向用户发出提示并等待确认，不得自动继续**：

> ⚠️ 您查询的时间跨度为 **X 天**（`<startDate>` ~ `<endDate>`），超过 2 个月，可能涉及大量分页请求，**产生较高费用**。是否继续？

等待用户明确回复。
- 用户回复**继续**（或"是"、"yes"、"continue" 等肯定语义）：继续执行后续步骤。
- 用户回复**取消**（或"否"、"no"、"不"等否定语义）：停止执行，告知用户已取消。

### 第二步：获取文章 URL 列表

> 告知用户：`[2/5] 正在查询「<name>」的文章列表（<startDate> ~ <endDate>）...`

脚本位于本 SKILL.md 所在目录下的 `scripts/wxpublic_list.py`，执行前先解析出绝对路径（与第四步相同方式）。

```bash
python3 "<scripts_dir>/wxpublic_list.py" "<app_id>" "<secure_key>" "<name>" "<startDate>" "<endDate>"
```

脚本将结果以 JSON 格式输出到 stdout：
```json
{
  "urls": ["https://mp.weixin.qq.com/s/...", ...],
  "date": ["2026-08-04", ...],
  "count": 3
}
```

`date` 中每一项是对应文章的发布时间（`yyyy-MM-dd`），与 `urls` 按相同下标一一对应。例如 `urls[0]` 的发布日期为 `date[0]`。

解析 stdout 中的 JSON：
- 如果包含 `"error"` 字段：
  - 若 `error` 值为 `"Insufficient balance"`，提示用户：「账户余额不足，请前往公众号技能网页 https://wxpub.aibana.art/ 充值后重试。」然后停止。
  - 其他错误则向用户报告错误详情并停止。
- 如果 `count` 为 0，告知用户该时间范围内没有找到文章并停止。
- 告知用户找到了几篇文章，即将开始处理。

### 第三步：准备保存目录

> 告知用户：`[3/5] 正在准备保存目录 <output_dir>...`

```bash
mkdir -p "<output_dir>/images"
```

### 第四步：并行抓取所有文章的 Markdown

> 告知用户：`[4/5] 正在并行抓取 <count> 篇文章并下载图片，请稍候...`

必须先将第二步返回的 `urls` 与 `date` 按下标绑定为清单，写入 `<output_dir>/.wxpublic-articles.json`：

```json
[
  {"index": 0, "url": "https://mp.weixin.qq.com/s/...", "date": "2026-08-04"}
]
```

不得只传 URL 后再按并发完成顺序对应日期；每个清单项的 `date` 必须来自同下标的 `date[index]`。

调用 `scripts/wxpublic_fetch.py`，将该清单传入。

脚本位于本 SKILL.md 所在目录下的 `scripts/wxpublic_fetch.py`。执行前先解析出绝对路径。

```bash
python3 "<scripts_dir>/wxpublic_fetch.py" "<output_dir>" --manifest "<output_dir>/.wxpublic-articles.json"
```

- url2md 并发 **5** 线程，图片下载并发 **8** 线程。
- 每篇文章调用 html2md 失败时自动重试 **1 次**；第二次仍失败才记录为失败。
- 从输出中解析 `RESULT:<json>`。每条结果包含 `index`、`url`、`date`、`ok`、`path` 和 `error`，并已按 `index` 输出。使用 `ok=true` 且 `path` 非空的记录收集成功路径，保留其 `date`；对 `ok=false` 使用同一条记录的 `url` 和 `error`。

### 第五步：汇总报告

> 告知用户：`[5/5] 正在生成汇总报告...`

所有文章处理完毕后，输出汇总：

```
✓ 已保存 N 篇文章到 <output_dir>

保存的文件：
1. 2026-08-04 | /path/to/article1.md
2. 2026-08-03 | /path/to/article2.md
...

（如有跳过）以下文章处理失败：
- https://mp.weixin.qq.com/s/... （原因）
```

**重要**：将所有成功记录的 `.md` 文件路径与 `date`、`url` 一起存入对话上下文，便于用户后续直接问"帮我总结这些文章"或"这些文章讲了什么"时，能直接读取对应文件内容作答。

---

## 注意事项

- 微信图片 URL（`mmbiz.qpic.cn`）有防盗链，下载时加上 `-L` 跟随重定向，如果失败则保留原始 URL。
- 文件名中不能含有 `/ \ : * ? " < > |` 等字符。
- 如果公众号名称包含特殊字符，在 JSON 请求体中正确转义。
- 图片文件夹 `images/` 统一放在文章保存目录下，所有文章共享该目录（避免重复下载相同图片）。
