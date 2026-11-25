# 腾讯新闻 CLI 接入：热点精选（hotspot）

本文件记录本 skill 依赖 `tencent-news-cli` 的接入事实与验证证据。核实日期 **2026-10-21**。

## 1. 工具与来源

| 项目 | 内容 |
|---|---|
| 可执行名称 | `tencent-news-cli`（Windows 为 `tencent-news-cli.exe`） |
| 用途 | 查询腾讯新闻各类内容：热点榜、新闻搜索、早晚报、天气、赛事、股票、频道热点精选等 |
| 本次依赖的子命令 | `hotspot`（含 `premium`、`channels` 两个子命令） |
| 包装与分发 | 本仓库 `packages/news-cli`（npm 包装器，仅下载/转发二进制，不含业务实现） |
| 业务接口背景 | 需求方给出的接口文档入口 `https://openapi.inews.woa.com/docs/premium_list`（前端渲染页，本次未取到正文，未据此推断字段；一切以 CLI 实际返回为准） |
| 适用系统 | macOS（arm64/amd64）、Linux（arm64/amd64）、Windows x64 |
| 运行时 | 需要 `TENCENT_NEWS_APIKEY`；非交互，命令输出文本或 JSON |

## 2. 安装与版本

- 分发给用户的安装命令（formal / hub 渠道）：
  - macOS / Linux：`curl -fsSL https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.sh | sh`
  - Windows PowerShell：`irm https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1 | iex`
- 版本核实：`sh scripts/run-cli.sh version` 读取 `current_version`、`build_date`、`need_update`。
- **支持 `hotspot` 的构建**：test 渠道 `v1.0.18`，`build_date: 2026-10-20T17:40:37`，linux-amd64 二进制 SHA-256 `e635820dcb63bb05b6867de13b2d6f740aa50573d831217c5e2b65dcc20f42c9`（与 `test/checksums.txt` 一致，文件 `Last-Modified: Tue, 20 Oct 2026 09:42:33 GMT`）。
- **版本号不足以判断能力**：同为 `v1.0.18` 的旧构建（`build_date: 2026-10-19T19:17:10`）**没有** `hotspot`；`version` 对两个构建都返回 `need_update: false`。判断依据是 `run-cli help` 的命令列表，不是版本号。
- 升级到最新构建：`sh scripts/run-cli.sh update --force`（普通 `update` 只比较版本号，同版本不替换）。

## 3. 下载渠道与凭据

| 项目 | formal（hub） | test |
|---|---|---|
| CDN 根地址 | `https://mat1.gtimg.com/qqcdn/qqnews/cli/hub` | `https://mat1.gtimg.com/qqcdn/qqnews/cli/test` |
| SHA-256 清单 | `hub/checksums.txt` | `test/checksums.txt` |
| API Key 获取页 | `https://news.qq.com/exchange?scene=appkey` | `https://test.news.qq.com/exchange?scene=appkey&testApi=1` |
| 消耗流水 | `https://news.qq.com/exchange?scene=points` | `https://test.news.qq.com/exchange?scene=points&testApi=1` |

- 测试 Key 链接必须保留 `testApi=1`；去掉该参数即使用正式环境 Key。
- 测试 Key 增加积分联系 `tatianasun` 并提供账号 `news_suid`（见仓库 Wiki 协作联系人表）。
- 不保存、不回显任何 Key；`apikey-get` 的原始输出不得写入日志或回复。

## 4. 新增能力：变化范围与可用状态

| 项目 | 现状 |
|---|---|
| 变化范围 | 原有 `hot` 只支持 `--limit`（默认 10）的通用热点榜，不支持按频道取精选。新增 `hotspot` 命令：`premium` 按频道取精选内容池，`channels` 列出频道与 `pool_tag_id`。 |
| 实现来源 | 需求单：[TAPD 1010045201139017106](https://tapd.woa.com/tapd_fe/10045201/story/detail/1010045201139017106)。CLI 源码仓库的 MR / 提交未提供；可核实的发布产物为 [test 渠道 SHA-256 清单](https://mat1.gtimg.com/qqcdn/qqnews/cli/test/checksums.txt)（`skill.json` 的 `cli.changeRef` 指向此处）。 |
| 可用状态 | **test 渠道已上线**（2026-10-21 实测成功）。formal / hub 渠道是否包含**未核实**，不作为默认前提。 |
| 接入验证 | 已完成：`channels`、`premium`（json / text、`--today`、`--page`）真实调用成功，见第 7 节。 |
| 维护联络 | CLI 实现与命令问题联系 `quonliu`；skill 搭建与本仓库 MR 联系 `corinli`。均来自仓库 Wiki，不是本 skill 负责人，不自动发送消息。 |

本 skill 负责人为 `shasha`。

## 5. 调用契约

```
run-cli hotspot channels
run-cli hotspot premium [--channel <频道>] [频道] [--today] [--limit N] [--page N] [--format json|text]
```

| 参数 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `--channel` | string | 是 | 无 | 中文名（科技）、别名（tech）或 `pool_tag_id`（65546964）；也可作为 `premium` 后的位置参数 |
| `--today` | bool | 否 | false | 仅输出今天发布的精选内容 |
| `--limit` | int | 否 | 20 | 每页条数，取值 1–50 |
| `--page` | int | 否 | 0 | 页码，从 0 开始；`--page 1` 返回下一页不同条目 |
| `--format` | string | 否 | text | `text` 或 `json`；需要解析字段时用 `json` |

- 全局 `--caller` 由 `run-cli` 注入，调用时不要重复传。
- **没有**日期区间参数：本周 / 近期只能用返回的 `timestamp` 自行截取，并配合 `--page` 翻页。
- 频道清单以 `hotspot channels` 当次返回为准；本仓库 [`hotspot-channels.md`](hotspot-channels.md) 的表格为已核对的兜底副本。

## 6. 输出契约与失败处理

`--format json` 结构（实测）：

| 字段 | 说明 |
|---|---|
| `base_rsp.code` / `base_rsp.msg` | 0 / `success` 为成功 |
| `base_rsp.timestamp`、`base_rsp.trace_id` | 服务端时间与链路 id（不回显给用户） |
| `news_list[].id` | 文章 id，如 `20261021A039S600` |
| `news_list[].title`、`abstract` | 标题与摘要 |
| `news_list[].timestamp` | 发布 Unix 秒，用于时间范围过滤与排序 |
| `news_list[].url` | 原文链接（`text` 输出会带 `?scene=news-skill`） |
| `news_list[].user_info.nick` | 来源名称 |
| `news_list[].cover_image`、`video_info`、`schema_url` | 封面图、视频信息、端内 schema |
| `has_more` | 1 表示还有下一页 |

`--format text` 输出为「标题 / 摘要 / 来源 / 发布时间 / 链接」的编号列表，末尾提示「还有更多内容，可使用 --page N 继续查询」。

**字段可能缺失**：实测专题/运营位类条目没有 `timestamp`（或为 0）与 `user_info`（财经频道 2026-10-21 的「2026外滩年会」、科技频道的「又是一年双十一」即如此）。解析时用可选取值，`timestamp` 缺失的条目不参与时间过滤与倒序排头，回复中标注「接口未返回发布时间」。

- **接口未下发频道 id**：因此「查看更多」统一引导腾讯网，输出为 `[查看更多](https://www.qq.com)`；不拼造频道地址。该限制只记在本文档，**不在给用户的回复中解释**。
- **链接呈现**：`url` 必须以 Markdown 超链接输出（`[标题](url)`）。只输出裸 URL 时部分客户端不会渲染成可点击链接，这是本 skill 曾出现的输出缺陷，已写入 SKILL.md 强制要求。
- **失败处理**：
  - `unknown command "hotspot"` → `CLI_CAPABILITY_MISSING`，`update --force` 后复查一次，仍无则停止，不用 `hot` 等命令冒充。
  - 401/403、无效 Key → `API_KEY_UNAUTHORIZED`，由用户本地重新配置，不解释为无数据。
  - 超时或网络错误 → 保留真实类别，可重试一次。
  - 频道无数据（如 `--today` 当日为空）→ 说明该频道当次无精选，不扩大范围后仍按原范围表述。
- **操作影响**：只读查询，不写数据、不发消息、不发布内容、不修改用户配置。

## 7. 验证证据（2026-10-21）

| 动作 | 结果 |
|---|---|
| 下载 test linux-amd64 二进制并比对 `checksums.txt` | SHA-256 `e635820d…42c9` 一致，体积 8,712,376 字节 |
| 该构建 `version` | `v1.0.18`、`build_date: 2026-10-20T17:40:37`、`need_update: false` |
| 平台已安装的旧构建 `version` | `v1.0.18`、`build_date: 2026-10-19T19:17:10`，SHA-256 `0cbd95c9…4e1a`，**无 `hotspot`** |
| `hotspot --help` | 含 `premium`、`channels` 两个子命令，说明「覆盖要闻、国际、科技、体育、财经等 27 个频道」 |
| `hotspot channels` | 返回 27 个频道及 `pool_tag_id`、别名，与需求单频道表逐一一致 |
| `hotspot premium --channel 科技 --limit 3 --format json` | `base_rsp.code: 0`，返回 3 条 `news_list`，`has_more: 1` |
| `hotspot premium 科技 --today --limit 3`（text） | 返回 3 条带标题/摘要/来源/时间/链接，提示可翻页 |
| `hotspot premium --channel 科技 --limit 1 --page 1 --format json` | 返回与第 0 页不同的下一条，翻页可用 |
| 三道示例问题的真实作答（财经+股票近期、体育 --today、科技本周） | 均 `base_rsp.code: 0` 并返回条目；财经 10 条、股票 9 条、体育 --today 9 条、科技 20 条，`has_more` 均为 1 |
| 字段缺失观察 | 财经「2026外滩年会」、科技「又是一年双十一」无 `timestamp` / `user_info` |
| `cli-state.sh status`（指向最新构建） | `cliExists: true`、`apiKey.status: configured` |

未验证项：formal / hub 渠道是否已发布 `hotspot`；macOS、Windows、Linux ARM64 构建的实际运行（本次仅 Linux x64）；`--limit` 边界与鉴权失败的具体返回；CLI 源码仓库变更链接。

## 8. 待补项

1. CLI 源码仓库中该命令的 MR / 提交（替换 `skill.json` 的 `cli.changeRef`）。
2. formal / hub 渠道是否包含 `hotspot`，以及面向用户分发时的最低可用版本。
3. 接口文档 `premium_list` 的字段说明（若能访问），用于确认 `abstract` 截断规则等边界。
