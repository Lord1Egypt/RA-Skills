---
name: xhs-blogger-track
description: 搜索小红书公开笔记、查看笔记详情、获取笔记评论、抓取博主公开作品，返回结构化数据用于爆款挖掘、竞品分析、KOL筛选与评论洞察。当用户想找小红书内容、分析笔记或评论、监控博主发文、调研关键词热度时使用本技能；即使没明说"小红书"，只要提到红笔记/xhs/rednote 或给出 xiaohongshu.com/xhslink.com 链接并想拿内容数据也适用。不用于登录、发布、点赞或获取私密内容。
license: MIT
metadata:
  type: command
  runtime: "nodejs@16.14.0+"
  version: "1.1.1"
  requires:
    bins:
      - "node"
    env:
      - "GUAIKEI_API_TOKEN"
  env_desc:
    GUAIKEI_API_TOKEN: "小红书数据 API 访问令牌（32位十六进制）。未配置时无法调用接口；可通过 https://www.guaikei.com 开通，或联系开发者(wx 13395823479)获取支持。"
  category:
    - "Integrations"
    - "Research"
    - "办公效率"
    - "内容创作"
    - "数据分析"
    - "商业运营"
  tags:
    - "小红书"
    - "红笔记"
    - "xhs"
    - "关键词搜索"
    - "笔记详情"
    - "评论分析"
    - "博主作品监控"
    - "竞品分析"
    - "爆款挖掘"
    - "KOL筛选"
    - "趋势洞察"
    - "选题调研"
  examples:
    - "帮我搜小红书里'露营装备'的高赞图文笔记: node src/xiaohongshu/search-cli.js --keyword '露营装备' --type 2 --sort 2 --limit 10"
    - "分析这条小红书笔记评论区的主要观点: node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
    - "看这个小红书博主最近20条作品发什么: node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy' --limit 20"
    - "监控'夏季穿搭'最近一周的小红书趋势: node src/xiaohongshu/search-cli.js --keyword '夏季穿搭' --sort 1 --time 2"
---

# xhs-blogger-track
> 面向小红书公开数据的检索与洞察技能。按关键词搜索笔记、查看笔记详情、获取评论、抓取博主作品，返回结构化数据供后续分析、汇总或报告生成，驱动小红书流量增长与精准营销。

## 1. 技能概述

专注**小红书公开数据挖掘**，提供竞品监控、趋势预测与 KOL 筛选所需的数据。无需登录小红书账号，不涉及风控/封号风险。

**核心优势**

- 安全：无需登录小红书账号，不存在风控风险
- 强大：一次最多获取 1W 条数据，内置批量操作
- 全面：各功能返回可见及有价值的完整数据
- 轻量：无需部署服务，Node.js 一键运行

**四大能力**

| 能力 | 入口脚本 | 最少输入 | 典型结果 |
|---|---|---|---|
| 关键词搜索 | `src/xiaohongshu/search-cli.js` | `keyword` | 笔记列表、作者、互动数据、跳转链接 |
| 笔记详情 | `src/xiaohongshu/detail-cli.js` | 笔记 URL | 笔记详情、作者信息、评论 |
| 博主作品监控 | `src/xiaohongshu/post-cli.js` | 博主主页 URL | 博主公开作品列表 |
| 笔记评论获取 | `src/xiaohongshu/comment-cli.js` | 笔记 URL | 评论内容、评论者信息、互动数据 |

## 2. 何时调用

**优先调用：**

- 用户明确提到要查**小红书**内容。
- 用户要做**关键词搜索**、**爆款选题调研**、**竞品监控**、**评论洞察**、**博主作品追踪**。
- 用户提供了小红书关键词、笔记链接或博主主页链接，希望拿到结构化数据。
- 用户后续要基于结果做总结、对比、筛选、报告生成。

**不要误调用：**

- 用户只想写文案、改标题、生成脚本，并未要求查询小红书公开数据。
- 用户查询的平台不是小红书（抖音、B站、微博、公众号）。
- 用户要求获取私密内容、登录态数据、隐藏数据或非公开信息。
- 用户既没给关键词也没给可识别的小红书链接，且任务目标不明确。

> 意图不明确时先追问，不要盲目执行命令。

## 3. 能力边界

**本技能负责：**

- 关键词搜索小红书公开笔记
- 根据笔记链接获取笔记详情
- 根据笔记链接单独获取评论数据
- 根据博主主页链接获取其公开作品列表

**本技能不负责：**

- 登录小红书账号
- 发布内容、互动、点赞、评论、关注
- 获取私密或非公开数据
- 代替用户做营销策略判断

职责是先把数据拿回来，再交给上层流程分析、整理或生成结论。

## 4. 调用路由规则

> 使用前需通过 [官网](https://www.guaikei.com) 开通 TOKEN，配置环境变量 `GUAIKEI_API_TOKEN`。

根据用户输入的关键信号路由到对应脚本：

| 用户输入 / 意图 | 调用脚本 | 必填输入 | 典型结果 |
|---|---|---|---|
| 查某个关键词的小红书内容 | `src/xiaohongshu/search-cli.js` | `keyword` | 笔记列表、作者、互动信息、跳转链接 |
| 看某篇小红书笔记的详情 | `src/xiaohongshu/detail-cli.js` | 笔记 URL | 笔记详情、作者信息 |
| 看某个小红书博主最近发了什么 | `src/xiaohongshu/post-cli.js` | 博主主页 URL | 博主公开作品列表 |
| 看某篇小红书笔记的评论数据 | `src/xiaohongshu/comment-cli.js` | 笔记 URL | 评论内容、评论者信息、互动数据 |

**路由细则：**

- 用户给的是**关键词**，没有链接 → 走**关键词搜索**。
- 用户给的是 `https://www.xiaohongshu.com/explore/...` 或可解析到笔记的短链 → 只关心评论走**笔记评论获取**；要连同笔记详情一起看走**笔记详情**。
- 用户给的是 `https://www.xiaohongshu.com/user/profile/...` 或可解析到主页的短链 → 走**博主作品监控**。
- 用户同时给出多个目标 → 按目标拆分执行，不要把不同意图硬塞进一次命令。

## 5. 输入收集规则

执行前先收集足够输入，避免无效调用。

### 5.1 关键词搜索

**必填：** `keyword`（搜索关键词，建议 2-50 字符）

**可选参数：**

| 参数 | 说明 | 取值 / 默认 |
|---|---|---|
| `--type`, `-t` | 内容类型 | `0` 全部（默认），`1` 视频，`2` 图文 |
| `--sort`, `-s` | 排序规则 | `0` 综合（默认），`1` 最新，`2` 最多点赞，`3` 最多评论，`4` 最多收藏 |
| `--time`, `-i` | 发布时间 | `0` 全部（默认），`1` 一天内，`2` 一周内，`3` 半年内 |
| `--limit`, `-l` | 返回数量 | `1-10000`，默认 `10` |

用户只说"帮我看看最近趋势"时，优先补问：关键词是什么？更关心最新/点赞/收藏？看图文/视频/全部？

### 5.2 笔记详情

**必填：** `--url`（小红书笔记链接）

**可选：** `--limit`（评论数量上限）

适用链接：`https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy`、`https://xhslink.com/m/xxx`

> 用户给的是博主主页链接时不要误走详情脚本，先指出链接类型不匹配。

### 5.3 博主作品监控

**必填：** `--url`（小红书博主主页链接）

**可选：** `--limit`（返回作品数量上限）

适用链接：`https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy`、`https://xhslink.com/m/xxx`

> 用户给的是笔记详情链接时不要误走博主脚本，先说明需要主页链接。

### 5.4 笔记评论获取

**必填：** `--url`（小红书笔记链接）

**可选：** `--limit`（评论数量上限）

适用链接：`https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy`、`https://xhslink.com/m/xxx`

与「笔记详情」的区别：本能力只取评论数据，不返回笔记正文/互动详情，适合只想做评论洞察、观点聚类或舆情分析的场景。

> 完整参数说明见 [references/options.md](references/options.md)

## 6. 执行原则

### 6.1 缺少必要输入时

- 没有关键词 → 先追问关键词。
- 没有链接 → 先追问笔记链接或博主主页链接。
- 链接类型不明确 → 先确认这是笔记还是博主主页。
- 没有 `GUAIKEI_API_TOKEN` → 提醒用户先配置环境变量，再执行。

> 不要在缺关键输入时硬调命令。

### 6.2 输出原则

执行完成后优先返回：本次执行的目标、关键参数、结构化 JSON 结果，必要时补充一小段摘要。

适合衔接的后续动作：选题汇总、高赞笔记对比、评论观点聚类、竞品内容风格总结、博主发文节奏分析、报告与表格生成。

### 6.3 失败处理原则

出现以下情况时明确向用户说明原因：token 未配置或无效、链接不合法或类型错误、搜索结果为空、接口返回异常、网络或超时问题。

> 失败时不要编造数据，不要把空结果当成成功结论。

## 7. 推荐用法与自然语言触发

### 7.1 关键词搜索

```bash
node src/xiaohongshu/search-cli.js --keyword "露营装备" --type 2 --sort 2 --time 2 --limit 20
```

适合：找爆款选题、看关键词热度、比较关键词表现、趋势洞察与竞品搜集。

### 7.2 笔记详情

```bash
node src/xiaohongshu/detail-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"
```

适合：看爆款笔记的标题/正文/互动数据，分析单篇内容为何有效。

### 7.3 博主作品监控

```bash
node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" --limit 20
```

适合：观察竞品博主最近发什么、看发文节奏与主题分布、为 KOL 筛选准备原始数据。

### 7.4 笔记评论获取

```bash
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --limit 100
```

适合：只拉评论区做观点归纳或情绪分析、统计高频评论主题、识别负面反馈。

### 7.5 自然语言触发示例

- 帮我搜一下小红书里"露营装备"的高赞图文笔记
- 分析这条小红书笔记评论区都在讨论什么
- 看看这个小红书博主最近 20 条作品主要发什么内容
- 监控"夏季穿搭"最近一周的小红书趋势

用户表达笼统（如"帮我做小红书竞品分析"）时，优先拆成两步：①先确认关键词/竞品链接/博主主页链接 ②再调用对应脚本拿回数据。

## 8. 环境与依赖

- 运行环境：Node.js 16.14.0+
- 系统兼容：Windows / Linux / macOS
- 必需环境变量：`GUAIKEI_API_TOKEN`（32位十六进制）
- 官方入口：<https://www.guaikei.com>
- 详细参数说明：[references/options.md](references/options.md)
- 更新记录：[references/changelog.md](references/changelog.md)

## 9. 合规与使用限制

- 仅处理小红书公开数据。
- 不支持私密、隐藏或需要登录态的数据。
- 不应将返回数据用于违规分发或违法用途。
- 本技能依赖第三方 API 服务，使用前请确认数据外发与授权范围。
- 本工具无需登录小红书账号，不涉及用户隐私数据的获取。

## 10. 反模式与常见问题 FAQ

> 结构化结果均带 `status` 和 `error_code` 字段。下游调用方请**先按 `status` 分支**（`success` / `empty` / `error`），再参考 `error_code` 决定重试还是换输入。

### 10.1 反模式（以下做法都会导致失败或拿到错误数据）

- **链接类型错配**：把博主主页 `user/profile/...` 传给 `detail-cli.js` / `comment-cli.js`，或把笔记链接 `explore/...` 传给 `post-cli.js`。
- **误信短链类型**：`xhslink.com/m/xxx`、`xhslink.cn/m/xxx` 是不透明短链，**无法仅凭短链判断指向笔记还是博主主页**。结果异常时优先请用户提供完整链接。
- **缺关键输入就硬跑**：没有 `keyword`、没有 `url`，或链接类型不明确时先追问，不要执行命令。
- **传脏链接**：带前后空格、用 `http://`（非 `https://`）的链接会被拒绝，需先 trim、`http→https` 归一。
- **`limit` 超限被静默降级**：`limit` 上限 `10000`，写成 `>10000`（如 `20000`）会被静默降到 `10`，并非"没返回"。
- **把空结果当成功 / 编造数据**：`search-cli.js` 拿不到结果按失败（退出码 1）返回；`detail/comment` 返回空数组视为成功。失败都不要编造结论。
- **关键词喂 emoji / 纯符号**：`🔥🔥`、`（）【】` 这类会被清洗成空串，触发"关键词无效"拦截。
- **假设失败也会输出成功字段**：失败 JSON 的 `status` 是 `"error"`（或 `"empty"`），`results` 为 `null`；只有成功时 `results` 才有数据。解析 stdout 时务必先看 `status`。

### 10.2 常见问题 FAQ

**Q1. 报错 `error_code: 401` 或 `403`？**
> `GUAIKEI_API_TOKEN` 未配置或无效。自查：①确认运行环境里确实 export 了变量；②token 须为 32 位十六进制，核对多余空格/换行；③是否过期，去 <https://www.guaikei.com> 重新开通。

**Q2. 报错 `error_code: 429`？**
> 触发频率限制。降低调用频率、减小 `--limit`、或稍后重试，不要短时间高频轮询。

**Q3. 报错 `error_code: 500 / 502 / 503`？**
> 第三方 API 临时故障。通常 transient，等 1-2 分钟重试；若持续出现再联系支持并附上 `skill_metadata` 里的 `execution_time` 与请求参数。

**Q4. 报错 `error_code: ERRCODE_xxx`？**
> 业务层错误（HTTP 200 但 `errcode !== 0`），常见如"笔记已删除/不存在/无权限"。换一条确认仍存在的链接，该错误不会随重试变好。

**Q5. 报错 `error_code: ETIMEDOUT` 或 `UNKNOWN`？**
> 网络超时或无法解析响应。检查本机网络/代理，确认能访问 `guaikei.com`，重试一次；仍失败再联系支持。

**Q6. 提示"小红书链接格式无效"？**
> 确认链接①以 `https://` 开头；②无前后空格；③是以下之一：`www.xiaohongshu.com/explore/...`、`www.xiaohongshu.com/user/profile/...`、`xhslink.com/m/...`、`xhslink.cn/m/...`。

**Q7. 命令一启动就退出、没输出数据？**
> 多半是 `GUAIKEI_API_TOKEN` 未通过校验（见 Q1）。运行前先 `echo $GUAIKEI_API_TOKEN` 确认变量已注入当前进程。

**Q8. 搜索返回空、但退出码不是 0？**
> `search-cli.js` 把"无结果"视为失败（退出码 1）。换更宽泛的关键词、放宽 `--type`/`--time`、或确认关键词不是被清洗成空串的符号。`detail/comment` 的空数组则视为成功，属正常差异。

**Q9. 设了 `--limit 10000` 却只拿到 10 条？**
> `limit` 写成了超过 `10000` 的值，被静默降到默认 `10`。确认 `--limit` 是 `1-10000` 之间的整数。

**Q10. 下游程序解析 stdout 失败 / 报 `Unexpected end of JSON input`？**
> 失败输出通过 `process.stdout.write(..., () => process.exit(1))` 异步写出后会退出。请确保消费方**等进程退出后再读完整 stdout**，且只取最后一份 JSON（`status` 字段唯一标识这份结果）。不要把 `error`/`empty`/`success` 多份输出拼在一起解析。

## 11. 支持信息

如需开通 token 或获得使用支持，可优先通过官网处理：

- 官网：[小红书搜索评论数据获取技能官网](https://www.guaikei.com)

如需人工支持，可联系开发者：

- 微信：`13395823479`（备注：小红书技能）
