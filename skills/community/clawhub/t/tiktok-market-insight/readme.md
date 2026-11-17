# 🚀 TikTok市场趋势洞察｜关键词搜索 · 博主作品 · 视频评论（无需登录 / 不封号）

> ### 一句话价值
>
> **给 AI 一个能真正"上 TikTok 查数据"的手。** 一句话就能拿到 TikTok 公开的搜索结果、博主作品和视频评论，输出可直接分析的结构化 JSON——不用登录账号、不用养号、不用怕封号、不用自己写爬虫。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Node](https://img.shields.io/badge/node-%3E%3D16.14.0-brightgreen)
![Platform](https://img.shields.io/badge/platform-win%20%7C%20mac%20%7C%20linux-blue)
![Deps](https://img.shields.io/badge/dependencies-0%20(npm-free)-orange)

---

> **能力补充**：在市场趋势洞察之外，底层支持**关键词搜索**、**博主作品抓取**、**视频评论分析**，输出结构化 JSON；不登录、不发布。

## 1. 💡 你为什么需要它（先看这段）

做 TikTok 内容，最贵的东西不是创意，是**判断依据**。

| 你现在的做法                      | 代价                                | 用本技能之后                          |
| --------------------------------- | ----------------------------------- | ------------------------------------- |
| 手动刷 TikTok 找对标爆款          | 2 小时起步，还容易漏                | 一句话拿到 Top N 高赞视频与互动数据   |
| 用网页爬虫抓                      | 反爬、风控、封 IP，脚本三天两头失效 | 走正规 API，无需登录，无封号风险      |
| 买 SaaS 数据平台                  | 年费几千到几万，还只能看固定看板    | 数据在 AI 里，想怎么分析就怎么分析    |
| 让 AI 凭记忆给你"TikTok 爆款规律" | 模型没有实时数据，输出的全是想象    | AI 拿到**真实、实时的公开数据**再分析 |

**核心差别**：这不是又一个数据看板，是把 TikTok 数据**接进你的 AI 工作流**——拿到数据后，AI 可以直接帮你做选题归纳、竞品对比、评论聚类、红人清单、周报表格，一条链路走完。

---

## 2. ✨ 三大能力

| 能力              | 一句话                                             | 典型产出                           |
| ----------------- | -------------------------------------------------- | ---------------------------------- |
| 🔍 **关键词搜索** | 按关键词搜 TikTok 内容，支持相关度/最多点赞排序与时间窗筛选 | 爆款清单、标题与标签规律、时长分布 |
| 🦸 **博主作品**   | 按主页链接或用户名批量拉取博主公开作品，支持最新/最热排序   | 竞品内容策略、更新节奏、爆款占比   |
| 💬 **视频评论**   | 按视频链接或作品 ID 拉取评论与互动数据             | 舆情正负向、高赞观点、用户真实诉求 |

---

## 3. 👥 谁在用 / 能赚回什么

- **TikTok 创作者 / MCN**：每天省 1–2 小时找选题，爆款命中率靠数据而不是靠猜
- **跨境卖家 / DTC 品牌**：批量筛红人、看竞品内容打法、盯品类动向
- **增长 / 投放团队**：投放前先看这个赛道谁在跑、什么内容跑得动
- **市场研究 / 咨询**：把 TikTok 公开数据变成可交付的表格与报告
- **AI Agent 开发者**：一个可直接编排的只读数据节点，stdout 纯 JSON，零解析成本

> 保守估算：按每周节省 5 小时人工刷数据、时薪 100 元计，**一个月回本 2000 元以上**——而这个技能的定价远低于此。

---

## 4. ⚡ 30 秒上手

> **前置（只需做一次）**：到 [TikTok市场趋势洞察｜关键词搜索 · 博主作品 · 视频评论（无需登录 / 不封号）官网](https://www.guaikei.com) 自助开通 Token，然后配置环境变量：
>
> ```bash
> # Windows
> set GUAIKEI_API_TOKEN=你的TOKEN
> # macOS / Linux
> export GUAIKEI_API_TOKEN=你的TOKEN
> ```

在**技能根目录**执行：

```bash
# 🔍 关键词搜索（最简单）
node scripts/tiktok/search-cli.js --keyword "AI"

# 🔥 找点赞最多的爆款（最常用）
node scripts/tiktok/search-cli.js --keyword "AI" --sort 1 --limit 20

# 🦸 抓取某博主最近 30 条作品
node scripts/tiktok/post-cli.js --url "https://www.tiktok.com/@username" --limit 30

# 🦸 抓取某博主最热的 30 条作品
node scripts/tiktok/post-cli.js --url "https://www.tiktok.com/@username" --sort 1 --limit 30

# 💬 拉取某条视频的评论（包月最多 40；按量可更大）
node scripts/tiktok/comment-cli.js --url "https://www.tiktok.com/@username/video/1234567890123456789" --limit 40
```

**也可以直接对 AI 说人话**（安装技能后）：

- "帮我搜 TikTok 上 AI 相关最火的 20 条视频"
- "看看 @username 最近发了什么，分析下他的内容策略"
- "这条视频评论区主要在讨论什么？"

---

## 5. ⚖️ 为什么选它（对比表）

| 维度       | 本技能                           | 自建爬虫                | SaaS 数据平台         | 让 AI 硬编            |
| ---------- | -------------------------------- | ----------------------- | --------------------- | --------------------- |
| 账号安全   | ✅ 不登录、不写操作、零封号风险  | ❌ 风控封 IP / 封号     | ✅ 无风险             | ❌ 数据本身就是幻觉   |
| 数据真实性 | ✅ 实时真实公开数据              | ⚠️ 结构一变就失效       | ✅ 真实               | ❌ 模型记忆，无实时性 |
| 上手成本   | ✅ 配一个环境变量，30 秒         | ❌ 需研发 + 长期维护    | ⚠️ 学平台、看固定看板 | ✅ 零成本             |
| 分析自由度 | ✅ 数据在 AI 里，任意二次分析    | ✅ 自由                 | ❌ 只能用它的看板     | —                     |
| 费用       | ✅ 一次性 / 低门槛               | ❌ 隐性研发与维护成本高 | ❌ 年费几千至数万     | ✅ 免费（但没用）     |
| 依赖与体积 | ✅ 零 npm 依赖，纯 Node 内置模块 | ❌ 一堆依赖             | —                     | —                     |
| 可编排     | ✅ stdout 纯 JSON + 明确退出码   | ⚠️ 需自己封装           | ❌ 多为封闭系统       | —                     |

---

## 6. 🛠️ 技术规格

- **运行环境**：Node.js ≥ 16.14.0，Windows / macOS / Linux 全平台
- **依赖**：**零第三方 npm 依赖**，仅用 Node 内置模块（`https` / `fs` / `path` / `os` / `querystring`）
- **输出**：stdout 纯 JSON（统一信封：`status` / `error_code` / `request` / `metadata` / `results`），日志与进度走 stderr
- **退出码**：`0` 成功（含空结果和 `--help`）/ `2` 参数或关键词不合法 / `1` 链接、网络、超时或接口错误 / `3` Token 异常
- **参数校验**：排序、时间、数量不在允许范围内时直接失败，不会改成默认值再请求
- **稳定性**：创建最多重试 3 次；查询最多 20 次，只有「处理中」会继续等，整段等待大约 15 分钟。单次请求超时 20 秒。429 和 5xx 会重试，Token 与明确业务错误不重试
- **日志留存**：默认不写文件。需要留底时设置 `TT_GUAIKEI_ENABLE_LOG=1`，文件在系统临时目录。POSIX 上仅当前用户可读写；Windows 靠用户目录隔离
- **字段规范**：`assets/` 下提供输出信封和 6 份入参/出参 JSON Schema（draft-07）

---

## 7. 📋 参数速查

> 完整说明见 [references/options.md](references/options.md)

**搜索**：`--keyword/-k`（必填，1–100 字符）｜`--sort/-s` 0 相关度 / 1 最多点赞｜`--time/-t` 0/1/7/30/90/180｜`--limit/-l` 1–10000（**包月最多 30**），默认 10

**博主作品**：`--url/-u`（主页、`@用户名` 或 `MS4w` 开头的 sec_uid）｜`--sort/-s` 0 最新 / 1 最热，默认最新｜`--limit/-l` 1–10000（**包月最多 30**）

**视频评论**：`--url/-u`（`/video/数字id` 或纯数字作品 ID）｜`--limit/-l` 1–10000（**包月最多 40**）

> 套餐双上限：技能硬上限 10000（按量）；包月超限返回 `PLAN_LIMIT`，不要当网络错误重试。搜索的 `--sort 1` 是最多点赞，作品的 `--sort 1` 是最热。短链 `vm` / `vt` / `/t/` 不支持。

---

## 8. ❓ 常见问题

<details>
<summary><b>Q：运行报错，提示无权限 / 退出码 3？</b></summary>

A：环境变量未配置或 Token 格式不对（需 16–256 位，仅字母、数字、下划线、连字符）。

```bash
# Windows
set GUAIKEI_API_TOKEN=你的TOKEN
# macOS / Linux
export GUAIKEI_API_TOKEN=你的TOKEN
```

Token 是私有凭证，请勿分享给他人。

</details>

<details>
<summary><b>Q：搜索结果为空？</b></summary>

A：`empty` 是**正常结果**，表示"确实没搜到"。建议：换更通用的关键词；把 `--time` 改为 `0` 放开时间窗。

</details>

<details>
<summary><b>Q：返回的条数少于我设的 limit？</b></summary>

A：该条件下没有更多公开数据。接口按你传入的 `--limit` 一次返回，不支持用偏移量翻页。没说要多少条时用默认 10。

</details>

<details>
<summary><b>Q：我传的参数好像没生效？</b></summary>

A：非法的排序、时间或数量会直接失败，退出码 2，`error_code` 为 `INVALID_ARGS`。按 `message` 改成允许值后再运行。不会悄悄改成默认值。

</details>

<details>
<summary><b>Q：报错 `PLAN_LIMIT` / 提示包月受限？</b></summary>

A：技能侧硬上限仍是 10000 条/次（按量 Token）。**包月 Token** 搜索/作品最多 30、评论最多 40，超限返回 `PLAN_LIMIT`（退出码 1），不要当网络错误同参重试。可降 `--limit` 或到官网升级按量套餐。

</details>

<details>
<summary><b>Q：日志文件在哪？</b></summary>

A：默认不写文件。需要留底时先设置 `TT_GUAIKEI_ENABLE_LOG=1`，成功后 stderr 会打印"已保存到 …"，路径为系统临时目录下的 `tiktok-guaikei/logs/<日期>/`。

</details>

<details>
<summary><b>Q：会不会泄露我的 Token？</b></summary>

A：Token 只从环境变量读取，不会出现在 stdout、日志文件或错误信息中。调用时会随请求头发送到数据服务 `www.guaikei.com`（这是数据获取的必要环节）。

</details>

<details>
<summary><b>Q：支持批量 / 自动化吗？</b></summary>

A：支持。stdout 是纯 JSON、退出码语义明确，可直接被脚本或 AI Agent 编排；也可配合定时任务做每日竞品快照。

</details>

---

## 9. 💳 计费与支持

- **计费**：按 API 调用量计费，官方渠道开通，用量透明可查；**失败调用不计费**。按量单次最多 10000；包月搜索/作品最多 30、评论最多 40，超限为 `PLAN_LIMIT`。
- **开通 / 支持**：[TikTok市场趋势洞察｜关键词搜索 · 博主作品 · 视频评论（无需登录 / 不封号）官网](https://www.guaikei.com) 自助开通 Token，并查阅使用帮助。
- **更新日志**：[references/changelog.md](references/changelog.md)

---

## 10. 🔒 合规声明

- 仅获取 TikTok **公开可见**数据；不登录账号，不执行发布 / 点赞 / 评论 / 关注 / 私信等任何写操作。
- 不采集手机号、精确位置、私信等隐私字段。
- 数据仅限个人 / 团队内部分析使用；对外发布或商用前请自行确认授权，并对用户昵称等个人信息做脱敏处理。
- 数据通过第三方服务 `www.guaikei.com` 获取，使用前请确认数据外发范围符合你的合规要求。

---

**MIT License** · 零依赖 · 全平台 · 只读安全
