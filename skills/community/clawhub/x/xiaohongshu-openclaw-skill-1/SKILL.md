---
name: guaikei-xhs-note-downloader
description: >-
 提供小红书爆款挖掘、竞品监控、KOL筛选、评论洞察所需的结构化数据。当用户为小红书账号增长做准备、做内容策划或营销复盘需要数据支撑时使用本技能；即使用户没说"运营"，只要目标是用小红书数据驱动决策也适用。不代替策略判断，只负责拿数据
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
    GUAIKEI_API_TOKEN: "小红书数据 API 访问令牌（32位十六进制）。未配置时所有命令均因鉴权失败退出；可通过 https://www.guaikei.com 开通，或联系开发者(wx 13395823479)获取支持。"
  category:
    - "Integrations"
    - "Research"
    - "数据分析"
    - "内容创作"
    - "商业运营"
  tags:
    - "小红书"
    - "红笔记"
    - "xhs"
    - "rednote"
    - "关键词搜索"
    - "笔记详情"
    - "评论分析"
    - "博主作品监控"
    - "竞品分析"
    - "爆款挖掘"
    - "KOL筛选"
    - "趋势洞察"
  examples:
    - "帮我搜最近一周小红书里'露营装备'的高赞图文笔记: node src/xiaohongshu/search-cli.js --keyword '露营装备' --type 2 --sort 2 --time 2 --limit 10"
    - "分析这条小红书笔记评论区的主要观点和负面反馈: node src/xiaohongshu/detail-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
    - "看这个小红书博主最近 20 条作品都在发什么: node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy' --limit 20"
    - "只拉这条笔记的评论做观点归纳: node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
---

# 小红书笔记下载

> guaikei 出品（官网 guaikei.com）｜专注小红书公开数据的检索与结构化返回，为爆款挖掘、竞品分析、KOL筛选、评论洞察提供数据底座。

---

## 1. 能力概述

四大能力，覆盖小红书公开数据采集核心场景：

| # | 能力 | 入口脚本 | 必填输入 | 返回内容 |
|---|---|---|---|---|
| ① | 关键词搜索 | `src/xiaohongshu/search-cli.js` | `--keyword` | 笔记列表、作者信息、互动数据、跳转链接 |
| ② | 笔记详情 | `src/xiaohongshu/detail-cli.js` | `--url`（笔记链接） | 笔记正文、作者信息、互动数据 + 评论 |
| ③ | 博主作品监控 | `src/xiaohongshu/post-cli.js` | `--url`（博主主页链接） | 博主公开作品列表 |
| ④ | 笔记评论获取 | `src/xiaohongshu/comment-cli.js` | `--url`（笔记链接） | 评论内容、评论者信息、互动数据 |

**核心优势：**
- **安全**：无需登录小红书账号，无风控/封号风险
- **大量**：一次最多获取 1 万条数据，内置批量操作
- **全面**：可见且有价值的公开数据均会返回
- **灵活**：支持多维度筛选（类型/排序/时间/数量）
- **轻量**：无需部署服务，Node.js 一键运行

> **detail vs comment 的区别**：`detail-cli.js` 返回笔记正文 + 评论；`comment-cli.js` 只返回评论，不返回笔记正文，适合专注评论分析的场景。

---

## 2. 调用路由

根据用户输入的关键信号，路由到对应脚本：

| 用户意图 | 调用脚本 | 必填输入 | 典型结果 |
|---|---|---|---|
| 查某个关键词的小红书内容 | `search-cli.js` | `keyword` | 笔记列表 + 互动数据 |
| 看某篇笔记的详情和评论 | `detail-cli.js` | 笔记 URL | 笔记正文 + 评论 |
| 看某个博主最近发了什么 | `post-cli.js` | 博主主页 URL | 作品列表 |
| 只拉某篇笔记的评论 | `comment-cli.js` | 笔记 URL | 评论数据 |

### 路由细则

- **给的是关键词**（无链接）→ 走 **关键词搜索**
- **给的是** `xiaohongshu.com/explore/...` 或可解析到笔记的短链 → 要评论走 **评论获取**；要详情+评论走 **笔记详情**
- **给的是** `xiaohongshu.com/user/profile/...` 或可解析到主页的短链 → 走 **博主作品监控**
- **短链** `xhslink.com/m/xxx` / `xhslink.cn/m/xxx` 无法仅凭 URL 判断指向笔记还是博主，结果异常时请向用户索要完整链接
- **多个目标** → 按意图拆分执行，不要把不同意图硬塞进一次命令

---

## 3. 参数说明

### 3.1 关键词搜索（search-cli.js）

```bash
node src/xiaohongshu/search-cli.js --keyword "夏季穿搭" [选项]
```

| 参数 | 简写 | 说明 | 取值 / 默认值 |
|---|---|---|---|
| `--keyword` | `-k` | 搜索关键词（必填） | 建议 2-50 字符，避免纯符号/emoji |
| `--type` | `-t` | 内容类型 | `0` 全部（默认），`1` 视频，`2` 图文 |
| `--sort` | `-s` | 排序规则 | `0` 综合（默认），`1` 最新，`2` 最多点赞，`3` 最多评论，`4` 最多收藏 |
| `--time` | `-i` | 发布时间 | `0` 全部（默认），`1` 一天内，`2` 一周内，`3` 半年内 |
| `--limit` | `-l` | 返回数量 | `1-10000`，默认 `10` |
| `--help` | `-h` | 显示帮助 | — |

```bash
# 精细化：最近一周高赞图文
node src/xiaohongshu/search-cli.js --keyword "露营装备" --type 2 --sort 2 --time 2 --limit 20
```

### 3.2 笔记详情（detail-cli.js）

```bash
node src/xiaohongshu/detail-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" [选项]
```

| 参数 | 简写 | 说明 | 取值 / 默认值 |
|---|---|---|---|
| `--url` | `-u` | 笔记链接（必填） | `explore/xxx?xsec_token=yyy` 或短链 |
| `--limit` | `-l` | 评论数量上限 | `0-10000`，不传按默认行为 |
| `--help` | `-h` | 显示帮助 | — |

### 3.3 博主作品监控（post-cli.js）

```bash
node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" [选项]
```

| 参数 | 简写 | 说明 | 取值 / 默认值 |
|---|---|---|---|
| `--url` | `-u` | 博主主页链接（必填） | `user/profile/xxx?xsec_token=yyy` 或短链 |
| `--limit` | `-l` | 作品数量上限 | `1-10000`，不传按默认行为 |
| `--help` | `-h` | 显示帮助 | — |

### 3.4 笔记评论获取（comment-cli.js）

```bash
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" [选项]
```

| 参数 | 简写 | 说明 | 取值 / 默认值 |
|---|---|---|---|
| `--url` | `-u` | 笔记链接（必填） | `explore/xxx?xsec_token=yyy` 或短链 |
| `--limit` | `-l` | 评论数量上限 | `1-10000`，不传按默认行为 |
| `--help` | `-h` | 显示帮助 | — |

---

## 4. 触发规则

### ✅ 应该调用

- 用户明确提到要查 **小红书 / 红笔记 / xhs / rednote** 内容
- 用户要做 **关键词搜索、爆款选题、竞品监控、评论洞察、博主追踪、KOL筛选**
- 用户提供了小红书关键词、笔记链接或博主主页链接，想拿结构化数据
- 用户给出 `xiaohongshu.com` / `xhslink.com` 链接并想获取内容数据
- 用户后续要基于结果做总结、对比、筛选、报告生成

### 🚫 不要误调用

- 用户只是想写文案、改标题、生成脚本，未要求查询小红书数据
- 用户查询的平台是抖音、B站、微博、公众号等非小红书平台
- 用户要求获取私密内容、登录态数据、隐藏数据
- 用户既没给关键词也没给可识别链接，且任务目标不明确

> **意图不明确时先追问，不要盲目执行命令。**

---

## 5. 输入收集规则

执行前先收集足够输入，避免无效调用：

| 场景 | 必须确认 | 缺失时追问 |
|---|---|---|
| 关键词搜索 | `keyword` | "你想搜什么关键词？" |
| 笔记详情 | 笔记 URL | "请提供笔记链接（explore/ 开头）" |
| 博主作品 | 博主主页 URL | "请提供博主主页链接（user/profile/ 开头）" |
| 笔记评论 | 笔记 URL | "请提供笔记链接" |
| 笼统需求 | 拆解意图 | "你是想搜关键词、看单篇笔记、还是抓博主作品？" |

**链接校验要点：**
- 必须以 `https://` 开头（`http://` 会被拒绝）
- 无前后空格
- 笔记链接含 `explore/`，博主链接含 `user/profile/`
- 短链 `xhslink.com/m/xxx` / `xhslink.cn/m/xxx` 可直接传入

---

## 6. 执行与输出

### 6.1 输出格式

执行完成后优先返回：
1. 本次执行的目标与关键参数
2. 结构化 JSON 结果
3. 必要时补充一小段摘要

### 6.2 适合衔接的后续动作

- 选题汇总 / 高赞笔记对比
- 评论观点聚类 / 情绪分析
- 竞品内容风格总结
- 博主发文节奏分析
- 报告与表格生成

### 6.3 失败处理

| 情况 | 处理方式 |
|---|---|
| token 未配置或无效 | 提醒用户配置 `GUAIKEI_API_TOKEN` |
| 链接不合法或类型错误 | 指出问题，请用户修正 |
| 搜索结果为空 | 换更宽泛的关键词，放宽筛选条件 |
| 接口返回异常 | 先看 `status` 分支，再按 `error_code` 决定重试或换输入 |
| 网络/超时 | 检查网络与代理，确认能访问 guaikei.com |

> **失败时不要编造数据，不要把空结果当成成功结论。**

---

## 7. 反模式与常见问题 FAQ

> 结构化结果均带 `status`（`success` / `empty` / `error`）和 `error_code` 字段，请**先按 `status` 分支**，再参考 `error_code` 决定重试还是换输入。

### 7.1 反模式（以下做法都会导致失败或错误数据）

- **链接类型错配**：把博主主页 `user/profile/...` 传给 `detail-cli.js` / `comment-cli.js`，或把笔记链接 `explore/...` 传给 `post-cli.js`
- **误信短链类型**：`xhslink.com/m/xxx` 无法仅凭短链判断指向笔记还是博主，结果异常时请用户提供完整链接
- **缺关键输入就硬跑**：没有 `keyword` 或 `url` 时先追问，不要执行命令
- **传脏链接**：带空格、用 `http://` 的链接会被拒绝，需先 trim 并 `http→https` 归一
- **limit 超限被静默降级**：`limit > 10000` 会被静默降到默认 `10`，并非"没返回"
- **把空结果当成功**：`search-cli.js` 无结果时退出码 1；`detail/comment` 空数组视为成功
- **关键词喂 emoji/纯符号**：`🔥🔥`、`（）【】` 会被清洗成空串，触发"关键词无效"拦截
- **假设失败也输出成功字段**：失败 JSON 的 `status` 是 `"error"`，`results` 为 `null`；解析 stdout 时务必先看 `status`

### 7.2 常见问题 FAQ

**Q1. 报错 `error_code: 401` 或 `403`？**
> `GUAIKEI_API_TOKEN` 未配置或无效。确认：①环境变量已注入当前进程（`echo $GUAIKEI_API_TOKEN`）；②token 为 32 位十六进制，无多余空格/换行；③去 guaikei.com 重新开通。

**Q2. 报错 `error_code: 429`？**
> 触发频率限制。降低调用频率、减小 `--limit`、稍后重试，不要短时间高频轮询。

**Q3. 报错 `error_code: 500/502/503`？**
> 第三方 API 临时故障。等 1-2 分钟重试；若持续出现，联系支持并附上 `execution_time` 与请求参数。

**Q4. 报错 `error_code: ERRCODE_xxx`？**
> 业务层错误（HTTP 200 但 `errcode !== 0`），常见如笔记已删除/不存在/无权限。换一条确认存在的链接，不要反复重试同一链接。

**Q5. 报错 `error_code: ETIMEDOUT` 或 `UNKNOWN`？**
> 网络超时或无法解析响应。检查网络/代理，确认能访问 guaikei.com，重试一次。

**Q6. 提示"小红书链接格式无效"？**
> 确认链接：①以 `https://` 开头；②无前后空格；③是以下之一：`www.xiaohongshu.com/explore/...`、`www.xiaohongshu.com/user/profile/...`、`xhslink.com/m/...`、`xhslink.cn/m/...`。

**Q7. 命令一启动就退出、没输出数据？**
> 多半是 `GUAIKEI_API_TOKEN` 未通过校验。运行前先 `echo $GUAIKEI_API_TOKEN` 确认变量已注入。

**Q8. 搜索返回空、退出码不是 0？**
> `search-cli.js` 把"无结果"视为失败（退出码 1）。换更宽泛的关键词、放宽 `--type`/`--time`、确认关键词不是被清洗成空串的符号。`detail/comment` 的空数组则视为成功。

**Q9. 设了 `--limit 10000` 却只拿到 10 条？**
> `limit` 写成了超过 10000 的值，被静默降到默认 10。确认 `--limit` 在 `1-10000` 之间。

**Q10. 下游程序解析 stdout 失败？**
> 失败输出通过异步写出后会退出，请确保消费方**等进程退出后再读完整 stdout**，且只取最后一份 JSON。不要把多份输出拼在一起解析。

---

## 8. 能力边界

### ✅ 能做

- 搜索小红书公开笔记
- 查看笔记详情与评论
- 获取博主公开作品列表
- 单独获取笔记评论数据
- 返回结构化 JSON 供后续分析

### 🛑 不能做

- 登录小红书账号
- 发布内容、点赞、评论、关注
- 获取私密或非公开数据
- 代替用户做营销策略判断

> 职责是先把数据拿回来，再交给上层流程去分析、整理或生成结论。

---

## 9. 环境与依赖

| 项目 | 要求 |
|---|---|
| 运行环境 | Node.js 16.14.0+ |
| 系统兼容 | Windows / Linux / macOS |
| 必需环境变量 | `GUAIKEI_API_TOKEN`（32位十六进制） |
| 官方入口 | https://www.guaikei.com |
| 详细参数说明 | `references/options.md` |
| 更新记录 | `references/changelog.md` |

---

## 10. 合规与使用限制

- 仅处理小红书**公开数据**
- 不支持私密、隐藏或需要登录态的数据
- 不应将返回数据用于违规分发或违法用途
- 本技能依赖第三方 API 服务（guaikei.com），使用前请确认数据外发与授权范围

---

## 11. 支持信息

| 渠道 | 联系方式 |
|---|---|
| 官网 | https://www.guaikei.com |
| 开发者微信 | `13395823479`（备注：小红书技能） |
