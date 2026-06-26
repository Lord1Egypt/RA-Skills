---
name: siluzan-cso
description: >-
  丝路赞内容运营平台（CSO）。**凡涉及以下任一类业务，必须先加载并使用本 skill**。
  (1) **文案生成与改稿**：选题、爆款拆解、新写成稿（视频脚本、博客、公众号、口播稿、配文、标题、评论区回复文案等）须走本 skill。
  **改稿润色**：用户给出已有正文并要求润色、改稿、口语化、保留原意、优化表达、审稿等——**必须加载本 skill**，走 content-writer 流程；**禁止**当普通聊天改字或直接输出。
  **同义触发**：写稿/内容创作/脚本/口播/成稿/改稿/润色/帮我改改/优化这段…（未说「文案」也视同文案任务）。
  (2) **人设管理**：运营账号人设卡（定位、受众、腔调、话题边界）；反推/生成/查询/保存，非角色扮演、非广告画像。
  (3) **内容发布与运营**（YouTube/TikTok/Instagram/LinkedIn/X/Facebook）：运营媒体账号、OAuth、**账号分组**（独有，不进 siluzan-tso）、发布（视频/图文）、任务/重试、素材上传、**封面截取(extract-cover)**、AI 内容规划、播放/粉丝报表；**网页端页面链接**查 `references/web-pages.md`。
  (4) **RAG 知识库**：品牌/产品问答与写稿事实依据。
  **高频误路由**：写文案/改稿/评论回复禁直接成稿或聊天润色、禁联网代替 rag query；发布/截封面禁口头教程，须调 CLI。
  **账号不明先问**：仅运营媒体账号可用；广告账户走 siluzan-tso。
license: MIT
allowed-tools: Bash(siluzan-cso:*) Read Write
metadata:
  requires: nodejs,siluzan-cso-cli
  cli: siluzan-cso
  product: CSO
  exclude_skill: siluzan-tso
  platforms: YouTube,TikTok,Instagram,LinkedIn,X,Facebook
  domains: copywriting,persona,publish,account-ops,rag,planning,reporting
  trigger_keywords: >-
    写文案,写稿,内容创作,出内容,脚本,口播,公众号,博客,外链,引流页,配文,标题,选题,爆款,改稿,润色,审稿,
    口语化,保留原意,太生硬,优化表达,帮我改改,优化这段,
    人设,styleGuide,人设卡,反推人设,persona,三库,
    发布,publish,上传,upload,封面,extract-cover,截取封面,任务,task,重试,失败,
    账号分组,运营账号,媒体账号,OAuth,authorize,list-accounts,绑定,授权过期,Token失效,
    评论区,回复文案,页面链接,web-pages,任务管理,
    RAG,知识库,rag,素材库,绩效,粉丝,播放,report,planning,内容规划,站内信
  not_for: >-
    广告账户,广告投放,余额,消耗,统计,开户,关键词出价,Google Ads,Bing Ads,Yandex,TSO,siluzan-tso,MCC,BC,BM
  when_to_use: >-
    用户要在丝路赞 CSO 写内容、管人设 styleGuide、向社交媒体运营账号发布、查企业 RAG、
    上传素材/截封面、查发布任务或运营报表、管理账号分组时使用。
  anti_patterns: >-
    写文案：禁止模型直接成稿；禁止 web_search/联网检索代替 siluzan-cso rag query；须 Read content-writer.workflow.md。
    发布：禁止只讲 App/网页操作或联网查平台手册；须 Read publish.md 并执行 list-accounts→upload→publish→task。
  high_risk_tasks: copywriting,publish
compatibility: Requires siluzan-cso-cli installed and authenticated via `siluzan-cso login`
---

# siluzan-cso

## 一键安装

如果 CLI 尚未安装，直接帮用户执行对应平台的安装脚本：

- **macOS / Linux / WSL：**
  ```bash
  bash <(curl -fsSL https://unpkg.com/siluzan-cso-cli@latest/dist/skill/scripts/install.sh)
  ```
- **Windows PowerShell：**
  ```powershell
  irm https://unpkg.com/siluzan-cso-cli@latest/dist/skill/scripts/install.ps1 | iex
  ```

Windows 注意：部分 Agent 客户端通过 PowerShell / cmd 代执行命令时存在兼容性问题。若上述命令异常失败，请先安装 [Git for Windows](https://git-scm.com/download/win)，然后在 Git Bash 中执行 macOS / Linux / WSL 的 Bash 安装命令。

脚本会自动完成 Node.js 检测/安装、CLI 安装、Skill 全局注册，并引导用户配置 API Key。无需选择，本脚本专为 siluzan-cso-cli 定制。

---

## 可执行的操作范围

- **只读**：查询媒体账号列表、账号分组、运营报表、发布任务状态、人设列表、RAG 知识库检索、AI 内容规划详情
- **写入**（需用户确认）：上传素材、提交发布任务、创建/更新账号分组、生成 AI 内容规划、站内信回复
- **本地文件操作**：`extract-cover` 在本地截取视频帧并输出图片文件；`workflow validate` 在本地校验文案文件（字数限制 / 内部内容泄漏）；`init` 将 Skill 文件写入 AI 助手目录

---

## 可选环境变量

| 变量                      | 说明                                                         |
| ------------------------- | ------------------------------------------------------------ |
| `SILUZAN_API_KEY`         | 从环境变量读取 API Key（优先级高于 config.json，CI/CD 推荐） |
| `SILUZAN_AUTH_TOKEN`      | 从环境变量读取 JWT Token（优先级高于 config.json）           |
| `SILUZAN_DATA_PERMISSION` | 从环境变量读取数据权限标识（优先级高于 config.json）         |

---

## 能力范围

| 业务流程               | 手段                                                    | 说明                                     |
| ---------------------- | ------------------------------------------------------- | ---------------------------------------- |
| **发布与运营**         | 下方 CLI 命令 + `references/*.md`                       | 上传、发布、任务、报表、账号、规划等     |
| **文案生产（子流程）** | `three-lib-content-workflow/content-writer.workflow.md` | 选题、三库、口播/公众号/成稿、审稿、改稿 |

两类流程同属 CSO 业务。文案生产流程嵌套在本 skill 内，见下文「三库内容工作流」。

## 命令索引

| 命令                                                                               | 作用                                                                                                                                                                                                   | 详细文档                      |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------- |
| `siluzan-cso login` / `siluzan-cso send-login-code`                                | 登录 / 配置凭据；手机号 + 验证码两段式登录                                                                                                                                                             | `references/setup.md`         |
| `siluzan-cso config show/set/clear`                                                | 查看 / 修改 / 清空本地配置                                                                                                                                                                             | `references/setup.md`         |
| `siluzan-cso init`                                                                 | Skill 文件初始化（写入 AI 助手目录）                                                                                                                                                                   | `references/setup.md`         |
| `siluzan-cso update`                                                               | 更新 CLI 版本并刷新 Skill 文件                                                                                                                                                                         | `references/setup.md`         |
| `siluzan-cso authorize --media-type <平台>`                                        | 发起媒体账号 OAuth 授权                                                                                                                                                                                | `references/authorize.md`     |
| `siluzan-cso list-accounts`                                                        | 列出媒体账号，获取账号 ID / 数据总览                                                                                                                                                                   | `references/list-accounts.md` |
| `siluzan-cso persona list`                                                         | 拉取 CSO 人设列表。**请先阅读详细文档，规范操作，避免误用。**                                                                                                                                          | `references/persona.md`       |
| `siluzan-cso rag list`                                                             | 列出知识库文件夹；`--rag-only` 仅已建索引；`--folder-id` 查指定文件夹下的子库                                                                                                                          | `references/rag.md`           |
| `siluzan-cso rag query`                                                            | 知识库向量检索；**`--partition wiki` 或 `default`**（默认 `default`；写稿与须贴库作答时优先 **wiki**，不足再 **default**）；`-q` 含空白时多词分检合并；`--folder-id` / `--tags` 见 `references/rag.md` | `references/rag.md`           |
| `siluzan-cso account-group list/create/add-accounts/remove-accounts/update/delete` | 账号分组管理                                                                                                                                                                                           | `references/account-group.md` |
| `siluzan-cso upload -f <file>`                                                     | 上传视频 / 图片到素材库                                                                                                                                                                                | `references/upload.md`        |
| `siluzan-cso extract-cover -f <video> -p <平台>`                                   | 从视频截取封面帧                                                                                                                                                                                       | `references/extract-cover.md` |
| `siluzan-cso publish -c config.json`                                               | 提交多平台发布任务                                                                                                                                                                                     | `references/publish.md`       |
| `siluzan-cso task list/detail/item`                                                | 查看任务状态 / 处理失败 / 重试                                                                                                                                                                         | `references/task.md`          |
| `siluzan-cso report fetch --media <平台>`                                          | 运营报表（核心指标 / 视频排行 / 趋势）                                                                                                                                                                 | `references/report.md`        |
| `siluzan-cso planning ...`                                                         | AI 内容规划：生成、监控、详情、导出                                                                                                                                                                    | `references/planning.md`      |
| —（网页端）                                                                        | CSO web端全部页面 URL                                                                                                                                                                                  | `references/web-pages.md`     |

---

## 常见业务场景 → 阅读哪个文件

| 用户在做什么                                                                                         | 先阅读                                                  |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| 首次安装 / 登录 / 更新                                                                               | `references/setup.md`                                   |
| 发布视频或图文                                                                                       | `references/publish.md`                                 |
| 上传素材                                                                                             | `references/upload.md`                                  |
| 截取视频封面                                                                                         | `references/extract-cover.md`                           |
| 文案写完落盘后校验字数 / 检查内部内容泄漏                                                            | `references/validate-content.md`                        |
| 查发布记录 / 处理失败                                                                                | `references/task.md`                                    |
| 查账号数据 / 运营报表                                                                                | `references/report.md`                                  |
| 查找账号 ID 或账号详情                                                                               | `references/list-accounts.md`                           |
| 账号 Token 失效 / 重新授权                                                                           | `references/authorize.md`                               |
| 管理账号分组                                                                                         | `references/account-group.md`                           |
| AI 内容规划                                                                                          | `references/planning.md`                                |
| 需要给用户提供后台页面链接                                                                           | `references/web-pages.md`                               |
| 拉取人设 / styleGuide（写稿前）/ 保存人设                                                            | `references/persona.md`                                 |
| 写稿时检索素材库 RAG 片段（三库拆素材等）                                                            | `references/rag.md`                                     |
| 选题 / 三库拆解 / 口播文案/公众号文章/其他文案 / 人设卡 / 代表作品反推人设 / 文章审稿打分 / 精准改稿 | `three-lib-content-workflow/content-writer.workflow.md` |

---

## 命令间依赖关系（交叉引用速览）

```
publish ──需要账号字段──► list-accounts
publish ──需要素材 ID──► upload ──需要封面──► extract-cover
publish ──提交后查状态──► task ──失败重授权──► authorize

report ──需要 mediaCustomerId──► list-accounts
account-group ──需要 mediaCustomerId──► list-accounts

rag query ──需要知识库 ID──► rag list（按用户意图自动选择）
```

---

## RAG 知识库检索工作流

> 详细检索策略见 `references/rag.md`，以下为决策摘要。

### 何时使用 RAG

- ✅ 询问特定品牌/产品知识、写需要品牌素材的文案 → **必须先 RAG**
- ✅ 执行三库内容工作流 → **按三库分库检索**
- ❌ 询问平台操作方法、纯通用创作、用户明确不需要 → **跳过 RAG**

### 四步执行流程

**Step 1 — 获取知识库**（只在任务开始时调用一次）

```bash
# 列出所有已建索引的根级知识库（落盘后用脚本读 id，见 references/core/tips.md）
siluzan-cso rag list --rag-only --json-out ./snap-cso

# 若根级库下还有子文件夹，可钻取查看
siluzan-cso rag list --folder-id <父文件夹id> --rag-only --json-out ./snap-cso
```

**Step 2 — 选择知识库**（按名称语义匹配）

- 用户提到品牌名 → 找名称最匹配的文件夹，记录 `id`
- 多品牌 → `--folder-id id1,id2`（逗号分隔）
- 无明确品牌 → 不传 `--folder-id`（全库检索）

**Step 3 — 拆词检索**（2–5 个短关键词；**`--partition`**）

- **首轮**：`--partition wiki`，`--top-k` 建议 **8–15**（常用 **12**）。写稿、须贴库作答、需要较长正文作依据时优先。
- **仍不足时**：同一 `-q` / `--folder-id` / `--tags` 下再跑 `--partition default`，`--top-k` **5–10**；两轮按片段 **id** 去重合并，**禁止编造**。
- 取值仅 **`wiki`** 或 **`default`**（小写）；非法值 CLI 会报错。

```bash
# 默认不传 --tags = 全量检索（适用于绝大多数场景）
# 推荐：同一库、同一标签策略下，用空格一次传多词，CLI 会分检合并排序
siluzan-cso rag query -q "产品核心卖点 用户使用场景 品牌差异优势" --folder-id <id> --partition wiki --top-k 12

# 证据仍不足时再补 default（按需执行）
# siluzan-cso rag query -q "产品核心卖点 用户使用场景 品牌差异优势" --folder-id <id> --partition default --top-k 8

# 仍可用多轮独立 -q（例如需要分步查看或参数不同）
# siluzan-cso rag query -q "产品核心卖点" --folder-id <id> --partition wiki --top-k 12
# siluzan-cso rag query -q "用户使用场景" --folder-id <id> --partition wiki --top-k 12

# 仅当知识库已按标签打标，且需要精确筛选时才传 --tags（不同标签需多条命令；`--partition` 规则同上）
siluzan-cso rag query -q "抖音 爆款 钩子" --tags "流量因子库" --partition wiki --top-k 12
siluzan-cso rag query -q "产品 卖点 故事" --tags "产品资产库" --partition wiki --top-k 12
```

**Step 4 — 合成使用**

合并后的结果中 **`score` 越大越相关**（CLI 已做 0–1 归一化）。若执行了 **wiki + default** 两轮，按片段 **id** 去重后再合成。将片段作为写稿/回答的事实依据，重新组织表达（不直接粘贴原文）；若执行了多条 `rag query`，再在对话侧对重复片段去重。

---

## AI 行为规范

### 执行任务的标准流程

遵循**计划 → 确认 → 执行 → 验证 → 预测**五步：

1. **计划**：根据用户意图，查阅命令索引与 references，或「三库内容工作流」与 `GetPersonas` 人设要求，制定操作步骤，不暴露命令行细节。
2. **确认**：与用户确认关键信息（目标账号、发布内容、时间等），不替用户做选择。
3. **执行**：按计划调用命令，处理异常。
4. **验证**：
   - 写入/修改操作后，通过读取命令确认结果是否正确。
   - 失败时优先尝试重试或用其他方式补救，而不是直接告知用户"任务失败"。
5. **预测**：任务完成后，结合当前结果对用户下一步操作给出合理建议。

### 硬规范

- **数据处理纪律（防工具死循环，最高优先级）**：先 Read `references/core/agent-conventions.md`。要点：读取/列表/检索/详情类命令一律 `--json-out <路径>` 落盘，stdout 仅一行摘要 + agentHint；**禁止对 stdout 写翻页循环**，**禁止**用 Read/cat 打开落盘业务 `*.json`，先读 `*.outline.txt` 再用 `node -e` 读 JSON；已有 JSON 不重跑、查无结果即停。脚本食谱见 `references/core/tips.md`。
- **不确定时先读文档**：遇到不熟悉的命令，先查对应 references 文件，不猜参数。
- **先查账号再操作**：对具体账号做操作前，先用 `list-accounts --name <名称> --media-type <平台>` 确认账号存在且 Token 有效。
- **需要计算/筛选时用 `--json-out`**：加 `--json-out <目录或 *.json 文件>` 落盘，再按 `references/core/tips.md` 的脚本食谱（`node -e` `readFileSync` / `require` 读盘）提取字段；旧 `--json` 已移除。
- **不猜账号 ID**：`entityId` ≠ `mediaCustomerId`，两者均须从 `list-accounts --json-out` 落盘数据获取，不可假设。
- **命令透明性**：以简洁的方式向用户说明即将执行的操作意图（如「正在上传视频到素材库」「正在为您查询 YouTube 账号列表」），让用户了解操作进度。用户主动要求查看执行细节时，应如实提供完整命令。安装/登录/更新等一次性命令（见 `references/setup.md`）可直接展示给用户自行执行。
- **操作后必须验证**：完成发布、上传、分组等写操作后，需通过对应的查询命令确认结果。
- **内容创作必须严格按本 skill 流程，禁止绕过指引直接生成内容。所有相关子文件须完整读取后再生成。**

### 必须遵守

- 主动更新（详情请读取 `references/setup.md`）。
- **破坏性操作必须用户确认**：涉及写入/修改/删除的操作（发布、上传、分组变更等），执行前必须明确告知用户操作内容并获得确认。
- **只读操作可自主执行**：查询类命令（`list-accounts`、`report fetch`、`task list`、`config show` 等）可直接执行，无需额外确认。
- 禁止提供虚假信息，比如web端连接就必须确认 `references/web-pages.md` 中存在才能提供给用户

---

## 时间字段输出约定（全局）

CLI 返回的时间字段（如 `*DateTime` / `*Time` / `createTime` / `publishTime` / `lastAuthorizationTime` / `expiresOn` 等）如果是 **UTC** 时间，在显示给用户时需要完成时区转换。

**输出规则（按优先级）**：

1. **优先用用户在当前对话中明确表达过的时区**（如「我在深圳」「PST 时间」「我刚从纽约出差回来」）。
2. **否则用对话语言推断默认时区**：中文 → `Asia/Shanghai (UTC+8)`，日文 → `Asia/Tokyo (UTC+9)`，英文且无其他线索 → 保留 UTC 并明确标注。
3. **若仍不确定且时间对用户决策有意义**（如「最近一次更新」、「创建于多久前」、「Token 何时过期」），**主动询问用户所在时区**，不要瞎猜。

**展示格式**：

- 推荐 `YYYY-MM-DD HH:mm (时区标识)`，例如 `2024-03-15 18:30 (UTC+8)`、`2024-03-15 10:30 (UTC)`。
- **禁止**把 `2024-03-15T10:30:00Z` 这种原始 ISO 串直接吐给用户——用户会误以为是当地时间。
- 跨日 / 月底 / 年底 / 夏令时切换附近的时间，换算时要**特别小心**，必要时多核对一遍。
- 极少数字段（如 `report` 报表里按用户业务时区聚合的统计时间）已经是用户本地时区，文档若有特别说明则以文档为准。

---

## 常见 HTTP 错误处理

| 状态码                      | 原因                 | 处理方式                                                           |
| --------------------------- | -------------------- | ------------------------------------------------------------------ |
| `400 Bad Request`           | 参数错误             | 查对应 references 文档或用 `--help` 确认命令用法                   |
| `401 Unauthorized`          | 凭据失效             | 引导用户重新执行 `siluzan-cso login`（详见 `references/setup.md`） |
| `500 Internal Server Error` | 服务部署中或数据异常 | 稍后重试；若持续失败，提交给 Siluzan 相关人员处理                  |

---

## 平台名称速查

## 阅读： `references/authorize.md`

## Web 功能导航

> 无对应 CLI 命令的模块，或需要引导用户在网页端查看数据时，查阅 `references/web-pages.md` 获取完整页面清单与链接。

URL 格式：`https://www.siluzan.com/v3/foreign_trade/cso/{页面}`

常用页面：`task`（任务管理）· `postVideo`（发布页）· `ManageAccounts`（账号管理）· `planning`（AI 内容规划）· `table`（绩效报表）· `Workdata`（作品数据）
