---
name: tencent-news-hotspot
display_name: 实时新闻热点
display_name_en: Tencent News Hotspot
description: 当用户要求按领域或频道汇总腾讯新闻热点精选内容时使用，例如「聚合近期财经股票热点新闻」「帮我汇总下今天的体育热点新闻」「整理下本周科技领域的重要新闻」。通过腾讯新闻 CLI 的 hotspot 命令按频道 pool_tag_id 拉取精选文章并整理输出；频道不支持、时间范围无法覆盖或无数据时如实说明。不用于实时比分、天气、早晚报、股票行情或事实核查。
description_zh: 按领域或频道汇总腾讯新闻热点精选内容，输出今日、本周或近期的精选文章清单与摘要。
description_en: Summarize Tencent News featured articles by channel or domain for today, this week or a recent range.
version: 1.0.0
shared_resources: ["tencent-news-cli"]
author: shasha
tags_zh: ["热点精选", "频道", "资讯汇总", "腾讯新闻"]
tags_en: ["hotspot", "channel", "news digest", "tencent"]
examples_zh: ["聚合近期财经股票热点新闻", "帮我汇总下今天的体育热点新闻", "整理下本周科技领域的重要新闻"]
examples_en: ["Aggregate recent finance and stock hotspot news", "Summarize today's sports hotspot news for me", "Round up this week's important tech news"]
---

# 实时新闻热点 / Tencent News Hotspot

把用户对某个领域/频道的热点汇总请求，落成一次「热点精选模块」内容查询与整理输出。热点精选是端内 27 个频道共同运营的精选内容模块，按频道 `pool_tag_id` 取数。

执行步骤：

1. 按统一环境流程检查 CLI 与 Key；无法恢复时返回其中的结构化「环境失败结果」，不继续编造内容。
2. 检查 CLI 是否有 `hotspot` 命令；没有时升级 CLI 后复查，仍没有则返回「能力缺失结果」。
3. 解析用户意图：领域/频道 → `pool_tag_id`（先跑 `hotspot channels`，见 [`references/hotspot-channels.md`](references/hotspot-channels.md)），以及时间范围（今日 / 本周 / 近期）。
4. 通过 `run-cli` 调用 `hotspot premium`；多频道请求逐频道取数后合并去重，条数不足时按 `has_more` 翻页。
5. 只整理实际返回的文章，每篇输出标题、发布时间、来源、文章链接（Markdown 超链接）与摘要；结尾给出「查看更多」引导到腾讯网。
6. 部分频道失败或无数据时，明确说明哪些已取得、哪些没有，不把失败解释成「没有热点」。

本 skill 可独立安装，不依赖 `tencent-news` skill。所有 CLI 调用均通过本包的 `run-cli`，由脚本注入当前 skill 名称和版本。

## 对话用例

| 用户问题 | 执行方式与回答要求 |
|---|---|
| 聚合近期财经股票热点新闻 | 财经 + 股票两个频道各取一次，按 `timestamp` 保留近 7 天条目后合并去重，按时间倒序展示，并写明「近期」采用的天数。 |
| 帮我汇总下今天的体育热点新闻 | 体育频道加 `--today`；当日为空时说明当日暂无精选，不去掉 `--today` 后仍称「今天」。 |
| 整理下本周科技领域的重要新闻 | 科技频道取数并按 `timestamp` 截取本自然周，回复中写明起止日期。 |

领域词可对应多个频道（如「财经股票」→ 财经 + 股票）。用户给的领域不在频道表中时，说明未在热点精选频道中找到对应频道并列出可支持的频道，不猜 `pool_tag_id`。

## 环境与能力检查

**执行业务前必须读取并遵守 [CLI 环境与失败处理](references/cli-environment.md)**，完成状态检查、安装/更新、shell 配置核实与脱敏恢复。它是环境处理的统一入口；不要重新实现 Key 检测或读取明文 Key。环境失败优先于下文业务输出格式；本轮无法恢复时返回其中的结构化「环境失败结果」，不得用其他数据源补结果。

环境就绪后仍需确认能力：`hotspot` 是较新构建才有的命令，**同一版本号的旧构建可能没有该命令**，`need_update: false` 不能证明已具备。

1. 执行 `sh scripts/run-cli.sh help`，在命令列表中查找 `hotspot`。
2. 没有 `hotspot` 时执行 `sh scripts/run-cli.sh update --force`（普通 `update` 只比较版本号，同版本不会替换旧构建），再执行 `help` 复查一次；仍没有则返回「能力缺失结果」。
3. 有 `hotspot` 时用 `sh scripts/run-cli.sh hotspot --help` 和 `sh scripts/run-cli.sh hotspot premium --help` 读取实际参数；参数与本文不一致时以实际 help 为准，并在回复中说明差异。

## 取数与整理

调用契约（v1.0.18 build 2026-10-20T17:40:37 实测）：

```sh
sh scripts/run-cli.sh hotspot channels                                   # 频道与 pool_tag_id
sh scripts/run-cli.sh hotspot premium --channel 科技 --limit 20 --format json
sh scripts/run-cli.sh hotspot premium 体育 --today --limit 10
```

- `--channel`：必填，支持中文名（科技）、别名（tech）或 `pool_tag_id`（65546964）；也可作为位置参数写在 `premium` 之后。
- `--today`：仅输出今天发布的精选内容。
- `--limit`：每页条数，1–50，默认 20。`--page`：页码，从 0 开始。`--format`：`text`（默认）或 `json`；需要解析字段时用 `json`。
- **时间范围**：CLI 只有 `--today`，没有日期区间参数。本周 / 近期先取数，再用条目的 `timestamp`（Unix 秒）截取对应区间，不足时按 `has_more` 翻页；回复必须写明实际采用的起止日期或天数。
- 频道不确定时先跑 `hotspot channels`，以 CLI 返回的频道与 `pool_tag_id` 为准。
- 多频道逐个取数后按 `id` 去重，按 `timestamp` 倒序输出。

输出字段（`--format json`）：`base_rsp.code`、`base_rsp.msg`、`news_list[]`（`id`、`title`、`timestamp`、`abstract`、`url`、`user_info.nick`、`cover_image`、`video_info`、`schema_url`）、`has_more`（1 表示还有下一页）。

整理输出时每篇文章固定输出五项，顺序如下：

1. **标题** — `title`
2. **发布时间** — `timestamp` 转北京时间，格式 `YYYY-MM-DD HH:mm`
3. **来源** — `user_info.nick`
4. **文章链接** — `url`，**必须写成 Markdown 超链接**、链接文本用文章标题：`[标题](url)`（标题含 `[`、`]` 时用 `\` 转义）。不要输出裸 URL，裸 URL 在部分客户端不会渲染成可点击链接。
5. **摘要** — `abstract`；原文较长时保留开头一段（约 60–80 字）并以 `…` 结尾，不改写事实、不补充接口未返回的信息

只使用接口实际返回的字段。实测发现部分条目（专题/运营位）**没有 `timestamp` 或 `user_info`**：发布时间写「接口未返回发布时间」、来源写「接口未返回来源」，不猜时间、不把它排到列表最前；`abstract` 为空时摘要写「接口未返回摘要」，不用标题或正文推测补足。

结尾「查看更多」统一引导腾讯网，写成 `[查看更多](https://www.qq.com)`，不拼造频道地址、不写成裸 URL。

**回复中不向用户解释接口内部原因**：不要出现「接口未下发频道 id」「接口不支持某参数」这类说明，只给结果与链接；接口限制只在本文档与 `references/` 中记录。

## 能力缺失结果

CLI 已就绪但当前构建没有 `hotspot` 命令时返回：

```json
{
  "success": false,
  "status": "capability_missing",
  "capability": "hotspot",
  "query": "帮我汇总下今天的体育热点新闻",
  "cliVersion": "从 run-cli version 实际读取",
  "data": null,
  "error": {
    "code": "CLI_CAPABILITY_MISSING",
    "message": "当前 CLI 构建未提供 hotspot 命令，尚未执行热点精选查询。"
  },
  "nextSteps": ["执行 run-cli update --force 后重新检查 help；仍不支持时联系 CLI 维护人确认支持版本。"]
}
```

其他业务失败（超时、网络、参数不支持、频道无数据）按 [`references/cli-integration.md`](references/cli-integration.md) 的失败规则处理；只输出脱敏原因，不回显内部日志、traceid 或 Key。

## References

- 统一环境流程与失败处理（业务调用前必读）：[`references/cli-environment.md`](references/cli-environment.md)
- 频道 `pool_tag_id`、别名与时间范围规则：[`references/hotspot-channels.md`](references/hotspot-channels.md)
- CLI 接入、调用契约与验证证据：[`references/cli-integration.md`](references/cli-integration.md)
- 手动安装：[`references/installation-guide.md`](references/installation-guide.md)
- 手动更新：[`references/update-guide.md`](references/update-guide.md)
- 本地 Key 配置：[`references/env-setup-guide.md`](references/env-setup-guide.md)
- 打包与分发：[`references/packaging.md`](references/packaging.md)
