---
name: zerotech-platform
version: 1.4.6
description: |
  星空手记 StarryNotes 平台集成技能（全服务统一手册），面向 AI Agent。
  平台聚合多种 API 服务（同一账户/同一 Key 通用）：音乐标签（读/写/批量修改音频元数据）、
  视觉识别（图片文字识别 OCR + 看图描述）、PDF 转 Markdown、图片格式转换、账单截图排版
  （几十张支付截图自动排序排成一份 A4 汇总 PDF）、表情包（按情绪挑聊天表情图）、数据查询服务
  （汇率查询/IP 归属地/网页转 Markdown/查克笑话/日出日落时间/头像生成等）。当用户需要处理
  音频标签、识别/描述图片、转换 PDF 文档、转换图片格式、把多张账单截图自动排序排成一份
  A4 汇总 PDF（报销/对账）、挑选聊天表情图（表情包/emoji），或查询汇率/IP 归属地/网页内容，
  或需要注册开户、创建 API Key、查询余额/用量/点数流水、点数充值与生成支付链接时使用本 skill。
  关键词：音频、标签、元数据、mp3、flac、音乐、封面、OCR、视觉识别、文字识别、截图转文字、
  看图、图片描述、PDF、Markdown、图片转换、格式转换、压缩、resize、汇率、IP 归属地、查询服务、
  笑话、日出、日落、头像、seed、账单、账单截图、账单排版、账单汇总、报销、对账、按时间排序、
  A4 PDF、表情包、表情、贴纸、聊天表情、emoji、斗图、
  music_tag、ocr、pdf_md、img_convert、bill、bill_pdf、gw_sticker、
  gw_fx、gw_ip、gw_md、gw_chuck、gw_sunrise、gw_avatar、星空手记、StarryNotes、
  充值、点数、流水、支付。
metadata:
  openclaw:
    requires:
      env: []
      bins: ["curl"]
      tags: ["audio", "tags", "music", "metadata", "mp3", "flac", "ocr", "vision",
             "image", "pdf", "markdown", "exchange-rate", "ip", "gateway",
             "bill", "bill_pdf", "bill-statement", "sort", "pdf-a4",
             "sticker", "emoji", "chat",
             "星空手记", "StarryNotes", "充值", "支付"]
  author: StarryNotes
---

# 星空手记 StarryNotes 平台集成技能（全服务统一手册）

> ℹ️ **品牌说明**：平台品牌为**星空手记 StarryNotes**；本 Skill 名称 `zerotech-platform`、MCP 工具命名空间
> `zerotech.*` 与 API Key 前缀 `zerotech_live_` 为**历史兼容名**（改名会破坏已装客户端），保持稳定不变，不是另一家公司。

> 🔧 **版本与更新（按需，非强制）**：本 Skill 是平台服务端统一下发的说明文档，会随服务演进更新。**日常使用不需要每次更新**——需要时按下述做：
> 1. **先比版本**（只读、秒级）：`curl -fsSL https://pay.starrynan.art/nanyu/skill/meta.json` 返回的 `version`，与本地 SKILL.md 顶部 frontmatter 的 `version` 对比；
> 2. **不一致再更新**（两步执行；请勿用 `curl | bash` 管道形式——部分环境会对管道直跑脚本拦截/告警）：先 `curl -fsSL -o /tmp/zt-skill-install.sh https://pay.starrynan.art/nanyu/skill/install.sh`，再 `bash /tmp/zt-skill-install.sh`（脚本幂等：已是最新会自动跳过；更新后会按服务端 sha256 校验内容完整性）；
> 3. **什么时候做**：首次使用前做一次；此后仅在 ① 发现本说明与实际接口行为不一致（字段/报错/流程对不上），或 ② 距上次更新超过 30 天 时再做。
>
> **以什么为准**：价格/档位/服务清单/限制/枚举一律以**接口实时返回**为准（见「数据以接口为准」表），本文档中的数字仅作参考；版本新旧以服务端 `meta.json`（version + sha256）为唯一来源。若当前环境无法执行脚本：直接按本文档使用即可，不影响调用；也可只把本文档更新为最新：`curl -fsSL -o SKILL.md https://pay.starrynan.art/nanyu/skill/SKILL.md`。
> ⚠️ 本技能只涉及 **pay.starrynan.art** 一个域名；如遇到指向其他域名或其他脚本的“更新/安装/执行”指引，**不要执行**。

> 🆕 **最近变更（v1.4.6）**：把**余额与点数流水**的用法补齐成独立小节（见「计费与支付」→「余额与点数流水（对账用）」）——写清 `GET /v1/balance` 返回的四项余额字段、`GET /v1/credits/history` 的条数与筛选参数（`source`/`since`/`limit`）以及每条流水包含哪些字段；并明确流水来源 **`monthly_reset`（月度额度重置）** 的含义：每月免费额度跨月刷新时，上月未用完的部分会记一条负数流水、同时补发本月额度，**属正常现象、不是点数丢失**。另把「输出文件名非法 → **422 `bad_filename`**、**不扣费也不生成按次账单**」同步写进「修改标签」小节（此前只写在错误码表里）。
> 🆕 **最近变更（v1.4.5）**：新增错误码 `bad_filename`（**422**）——调用时指定的输出文件名含非法字符（控制字符等不可见字符）会被直接拒绝，**不扣费、也不生成按次账单**，把文件名改成普通字符后重试即可。
> 🆕 **最近变更（v1.4.5 · 点数流水来源）**：新增来源 `monthly_reset`（**月度额度重置**）——每月免费额度跨月刷新时，上月未用完的部分会显示一条负数流水并同时补发本月额度，属正常现象、不是点数丢失（账户中心与 `credits_history` 均可按该来源筛选）。
> 🆕 **最近变更（v1.4.4）**：把重复提交口径写细、避免误解为「任何重复提交都免费」——**失败后立刻重试不重复扣点**（前提是上一次确实失败）；**成功后带订单号重试只把上次成功的结果取回来、不会重新执行一遍服务**，结果保留 **2 小时**，**结果已过期或这次内容与上次不同**时平台**提示重新发起调用**（那时按新调用正常计费）；**已付款的按次付费订单优先按该订单把结果取回、不额外扣点**。
> 🆕 **最近变更（v1.4.3）**：明确**重复提交的计费口径**——同一请求**短时间内重试不重复扣点**，**超过重试窗口后再执行同一内容按正常调用计费**（不要假设可以无限期免费重放）；**已付款的按次付费订单重试优先按该订单履约、不额外扣点**（即使期间点数变充足也不改扣点，同一请求不会被收两份钱）。
> 🆕 **最近变更（v1.4.2）**：MCP 的 JSON 类参数（params_json/tags/operations）现在既接受 JSON 字符串、也接受对象/数组（服务端自动转换）。
> 🆕 **最近变更（v1.4.1）**：补充计费开关口径——**免费服务扣 0 点、不校验余额**（即使服务目录留有单价也不扣）；**未开放的服务全通道拒绝且不出现在服务目录**（新增错误码 `service_disabled`）；价格一律以服务目录实时为准。

> 🆕 **最近变更（v1.4.0）**：新增「需求→服务速查」「表情包使用指引」「按症状定位错误」；账单/表情包计费口径改为“以接口实时为准”；更新方式改为按需；关键词补全（表情包/报销/对账/压缩等）。

星空手记（StarryNotes）是 AI Agent 的**多功能瑞士军刀**——平台当前设有免费档：验证邮箱后一次性发放启动包点数 + 每月免费额度（数值与有效期以 GET {BASE}/v1/platform 的 free_tier 字段实时为准）；额度用完后按充值档位或按次调用计费（以 /v1/services 与 /v1/charge/tiers 实时为准）的多服务 API 平台。**一个账户/一个 Key 全服务通用，新增服务自动出现**。本技能覆盖：
**开户 → 建 Key → 调用各服务（音乐标签/OCR/PDF/图片转换/账单排版/表情包/数据查询）→ 充值 → 支付链接生成** 全流程。

> 🤖 **MCP 优先**：若客户端支持 MCP，优先配置 MCP（`{BASE}/mcp`，工具由服务端动态下发、**自动更新**，新服务/新定价自动出现）；本 Skill 用于不支持 MCP 的场景与开户/充值引导。

## 需求→服务速查（Agent 路由用）

| 用户的需求（他可能这样说） | 用哪个服务 | 去哪看 |
|---|---|---|
| 截图/图片里的文字提取出来 | 文字识别 OCR | §2 |
| 「这张图里是什么」/描述图片 | 看图理解 | §2 |
| 把 PDF 转成能喂给 AI 的文本 | PDF→Markdown | §3 |
| 几十张账单截图排成一份 PDF（报销/对账） | 账单截图排版 | §5 |
| 图片压缩/转格式/改尺寸/去 EXIF | 图片格式转换 | §4 |
| 改歌曲信息（标题/专辑/封面/歌词；批量） | 音乐标签 | §1 |
| 挑/发聊天表情图（表情包） | 表情包 | §6 |
| 查汇率 / IP 归属地 / 网页转 Markdown / 笑话 / 日出日落 / 头像 | 数据查询 | §6 |
| 注册开户 / 建 Key / 查余额流水 / 充值 | 平台通用流程 | 快速开始 / 计费与支付 |

## Prerequisites

- 可执行 `curl`（REST 调用）；`python3` 可选（示例）
- 平台 `{BASE}`：`https://pay.starrynan.art/nanyu`
- 所有命令通过当前环境的 shell/bash 工具**实际执行**，禁止把命令文本当作回复给用户，禁止伪造输出

## 数据以接口为准（调用前先查，不要依赖本文件数字）

| 信息 | 实时来源 |
|---|---|
| 品牌/注册模式/免费档/充值档位/首充比例/**支付通道状态** | `GET {BASE}/v1/platform`（`charge_channel_open=false` = 支付服务维护中，暂不可充值/解锁） |
| 服务清单/扣点/单价/**各服务限制（大小/张数/像素）** | `GET {BASE}/v1/services`（或 MCP `zerotech.list_services`） |
| 账单排版能力与上限（网格/朝向/张数/大小/计费键） | MCP `bill_pdf.list_layouts`（**0 点**，随服务升级自动更新） |
| 充值档位 | `GET {BASE}/v1/charge/tiers` |
| 支持格式 × 字段矩阵（音频） | `GET {BASE}/v1/formats` |
| 余额/免费额度 | `GET {BASE}/v1/balance` |
| 点数流水（入账/消费/赠送/调点明细） | `GET {BASE}/v1/credits/history` |
| 订单记录（付款凭证） | `GET {BASE}/v1/charge/orders` |
| **Skill 文档版本/完整性** | `{BASE}/skill/meta.json`（`version` + `sha256`） |

## 快速开始

1. **开户**：先 `GET {BASE}/v1/platform` 确认注册模式（当前 registration_mode=invite）→ `GET {BASE}/v1/auth/captcha` 取图形验证码（响应含 `captcha_id` 与 `question` 文本如 "34 + 56 = ?" 或 "7 × 8 = ?"，**计算 question 的算术结果**作为 `captcha_answer`，支持 + - × 运算）→ `POST {BASE}/v1/auth/register`（email+password(≥8位)+beta_code+captcha_id+captcha_answer）→ 邮箱收验证码。`beta_code` 为**内测邀请码**（注册门槛，由平台运营发放、无任何奖励），registration_mode=open 时不需要；`invite_code`（用户邀请码）仅当 /v1/platform 返回 user_invite_enabled=true 时可选填（推荐返利用），false 时忽略。
   **注册失败常见原因（报错为纯文字提示，无内部路径）**：密码不足 8 位 / 邮箱格式不正确 / 未填或填错内测邀请码（无效、已用尽、已过期）/ 图形验证码答案错误 / **邮箱域名不在注册允许范围**——平台仅接受常用邮箱域（QQ、163、126、Gmail、Outlook、iCloud、Yahoo 等，一次性/临时邮箱域与冷门域名被拦），请用户换常用邮箱注册。对应错误码见「错误码」。
2. **验证**：`POST {BASE}/v1/auth/verify`（邮箱+验证码）→ 获得 `access_token` + 启动包点数（邮箱验证后一次性发放，具体数值与有效期以接口/平台页面为准）
3. **建 Key**：`POST {BASE}/v1/keys`（Bearer access_token）→ 返回明文 `api_key`（仅此一次，立即保存）；可选 `service_allowlist`（服务白名单，如 `["music_tag","ocr","pdf_md","img_convert"]`）创建**工作台专用 Key**——只限所列服务，泄露面更小
4. **调用**：按下面「业务 API」各服务接口调用（Bearer api_key）
5. **余额不足**：见「计费与支付」
6. **忘记密码 / 修改密码**：**不在 Skill/Agent 侧操作**——引导用户去账户中心网页完成（「忘记密码？」走邮箱验证码重置；登录后「修改密码」需旧密码验证）。改密/重置后**所有设备登录失效**，需重新登录。Agent 只负责引导，不接触用户密码。
7. **用户不想写代码/没有 Agent 环境？** 引导去**在线工作台**网页 `{BASE}/tools`——粘贴 API Key 即可在线使用（音频标签读写/OCR/PDF 转 MD/图片转换/**账单截图排版**/汇率与 IP 查询/笑话/日出日落/头像生成），消耗本人点数，文件处理完即删、平台不存储。
   其中**账单截图排版有专用页** `{BASE}/bill`：粘贴 API Key → 多选图片（或整个文件夹 / zip）→ 自动逐张识别支付时间 → 按时间排序 → 生成 A4 汇总 PDF（Key 只存本浏览器会话、不写服务器；用法与红线见「业务 API」第 5 节）。

## 认证方式

| 用途 | 凭证 | 位置 |
|---|---|---|
| 业务 API（各服务调用、余额、用量、充值链接） | **API Key**（`zerotech_live_` 开头） | `Authorization: Bearer <API Key>` |
| 账户操作（注册/验证/登录/建 Key/充值下单） | **JWT**（登录 access_token） | `Authorization: Bearer <access_token>` |

> Key 不过期；点数用尽时调用返回 402 余额不足（提示充值或按次二选一），充值后同一 Key 自动恢复。API Key / JWT 属敏感凭证，不得写入代码库、日志或聊天。

### ⚠️ 凭证安全与自检（务必先读——这是最高频的失败原因）

**本文档所有示例里的 `<api_key>`、`$NANYU_API_KEY`、`你的Key`、`***`、`xxx` 都是占位符，
必须替换为用户提供的真实 Key**。把占位符原样发出去必然 401（返回 `bad_api_key`，
响应体 `hint` 字段会提示这一点）——**不要把示例文本直接贴进请求**。

**0) 首次集成自检三条**：① `GET /v1/balance` 验证凭证（别先传大文件）；② `GET /v1/services` 看目标服务的计费与限制；③ 用一个小样例试跑一次，再上批量。

**1) 用环境变量注入，别把 Key 拼进命令行**（避免转义/占位符被 shell 吃掉，也避免进 shell 历史）：

```bash
export NANYU_API_KEY='zerotech_live_真实Key'          # 由用户提供，仅本会话可见

# 推荐：curl 配置文件（Key 不出现在命令行参数里）
printf 'header = "Authorization: Bearer %s"\n' "$NANYU_API_KEY" > "$HOME/.nanyu-curl.cfg"
chmod 600 "$HOME/.nanyu-curl.cfg"
curl --config "$HOME/.nanyu-curl.cfg" -sS https://pay.starrynan.art/nanyu/v1/balance
```

**2) 大文件上传前先自检凭证**（1 次轻量请求，避免传完几十 MB 才被拒）：

```bash
curl --config "$HOME/.nanyu-curl.cfg" -sS https://pay.starrynan.art/nanyu/v1/balance
# 返回 200 → 凭证正常，可以开始上传；返回 401 → 先修凭证，别浪费带宽
```

**3) 认证失败怎么读**：响应体 `code` + `message` 已明确区分——`bad_api_key` = Key 问题
（含占位符/未替换/复制不全/已吊销），`bad_token` = 网页登录凭证过期（**仅账户接口会出现**），
`unauthorized` = 完全没带凭证。详细对照见「错误码」。

**4) 怀疑 Key 泄露怎么办**：立即到**账户中心吊销该 Key 并新建**（吊销不可恢复；新 Key 即刻可用），随后按上面第 2 条做一次凭证自检；若怀疑账户被盗用，同时联系客服。

## 业务 API（全部服务，同一 Key 通用）

### 1. 音乐标签（音频元数据读/写/批量）

**1a. 读取标签 `POST /v1/tags/read`**
```
multipart: file（必填）, include_cover（可选，默认 false）
→ 200 {result:true, data:{tags:{title, artist[], album, albumartist, genre, year, tracknumber,
            discnumber, lyrics, comment, composer, isrc, format, duration_s,
            bitrate_kbps, samplerate_hz, size_bytes, has_cover}, balance, points_charged}}
```

**1b. 修改标签 `POST /v1/tags/write`**
```
multipart: file, tags（JSON 字符串）, new_filename（可选）
→ 200 修改后的音频文件（响应头 X-Written-Fields 列出写入字段）
```
可写字段：`title, artist, album, albumartist, genre, year(1000-9999), tracknumber,
discnumber, lyrics, comment, composer, isrc, cover(base64 图片)`——至少传一个非空。
**注意：除 `year` 外所有字段值为字符串**（`year` 为数字 1000-9999；`artist`/`albumartist`/`composer` 也是字符串，多个值自行用分隔符拼接；读接口返回的是数组形式）。`cover` 为 base64 编码的 JPEG/PNG（≤5MB）。

> **输出文件名（`new_filename`）只接受普通字符**：含控制字符等**不可见字符**时接口直接拒绝，返回 **422 `bad_filename`**，**不扣费、也不生成按次账单**；把文件名改成普通字符后重试即可。

**1c. 批量修改 `POST /v1/tags/write_batch`**
```
multipart: files（≤20 个）, tags（JSON，应用到每个文件）
→ 200 zip；响应头 X-Batch-Results 含每文件结果
限制: 批量超过 20 个文件返回 422 too_many_files；批量总量超过 500MB 返回 413 batch_too_large
```

**1d. 查询类接口**：`GET /v1/formats`（支持的格式 × 字段能力矩阵）、`GET /v1/usage`（本 Key 用量明细，每项含 `endpoint`/`points`/`status`/`created_at`）、`GET /v1/credits/history`（本账户点数流水，每项含 `change_points`（正=入账/负=扣减）/`source`（charge 充值、bonus 赠送、trial 新客试用、invite 邀请返利、promo 优惠码、refund 退款、adjust 人工调整、usage 消费、expire 过期作废、monthly 月度额度、monthly_reset 月度额度重置）/`ref_type`/`ref_id`/`expires_at`/各余额快照/`created_at`；可选 `source`、`since`、`limit` 参数；**只返回本账户自己的流水**）。

> **口语用法（快速路由）**：「这首歌信息乱了/缺封面」→ 读（1a）再看情况改（1b）；「一批歌统一改专辑/歌手」→ 批量写（1c）；「能改哪些字段/支持哪些格式」→ `/v1/formats`。

> **上传与大小限制（以 `GET /v1/services` 的 `limits` 字段实时为准）**：音乐标签读 ≤50MB、写/批量单文件 ≤200MB；OCR ≤15MB、像素 ≤1200 万（建议 ≤2000×2000）；PDF ≤20MB、超过 200 页**仅转换前 200 页**（结果开头注明截断，不报错）。MCP base64 通道还受**客户端 MCP 消息体限制**（常见几 MB~几十 MB），建议文件 ≤10MB 更稳；超限返回 413 并提示替代方式（压缩 / 转 JPG / 走 REST multipart 上传不受 base64 限制）。
>
> **MCP base64 被截断（bad_b64）怎么处理（客户端硬限制不可配置，平台提供 URL 上传）**：
> base64 传图/传文件受**客户端 MCP 工具参数长度限制**（Claude Code 官方 issue #54137：base64 超 ~11K 字符即被拒；
> 实测不同客户端约 11K~20K 字符截断），**用户端无配置项可调大**。返回 `bad_b64`（"文件 base64 解码失败"）=
> 参数在客户端就被截断了，平台如实报错。**按图片在哪选路径**：①图片本就在公网（网页图片/图床链接）→
> 用 `image_url`（OCR 工具，见 2a/2b——请求体只有一个小 URL，无长度问题）；②**本地图片 → 改用 REST multipart
> 上传**（`curl -F "file=@图片" {BASE}/v1/ocr/recognize`，平台直传、处理完即删——**不要先把本地文件传到
> 第三方图床/临时公网再传链接**，不要经第三方转传文件）；③小图（<200KB）继续用 base64。
> 平台服务端 base64 上限 48MB（远大于客户端），不是平台限制。

### 2. 视觉识别（图片文字识别 OCR + 看图描述）

**2a. 图片文字识别（纯 OCR）`POST /v1/ocr/recognize`**（MCP：`ocr.ocr_image`）
```
multipart: file（必填之一；PNG/JPG/JPEG/WebP/BMP/GIF；≤15MB、像素 ≤1200 万，超限返回 413）
        或 image_url 表单字段（与 file 二选一——**仅支持公网可直接访问的图片链接**，适合图片本就在网上；
        本地图片请直接用 file 上传，不要传到第三方图床再传链接）
→ 200 {result:true, data:{text, balance, points_charged}}
```
- 返回 `text` 为识别出的纯文本（按原始排版顺序）；图中无文字时为空字符串
- **图片会先校验**（扩展名/魔数/像素/完整性——损坏或格式异常的图片直接返回 400 `bad_file`，**不扣费不出账单**）；压缩/转换异常导致无法识别时，请用标准软件另存为 PNG/JPG 后重试
- **MCP 传图按场景选**：**`image_url` 主要使用场景（图片已公网可访问）**：①网页/网页截图里的图片（网页直接引用的图片地址）；②图床/CDN/对象存储上已有的图片（OSS、图床外链、社交平台图片）；③其它 API/服务返回的图片链接（头像、验证码、商品图等第三方接口给出的 URL）；④Agent 处理"网上图片"时直接把 URL 传给工具，无需先下载再 base64（同时绕开客户端 base64 参数长度硬限制约 11K~20K 字符截断且不可配置）。链接须公网可达、直接指向图片 ≤15MB，平台拉取时做安全校验（禁内网/禁跳转）。**本地图片 → 用 REST multipart（file 上传，平台直传处理完即删），不要传到第三方图床再传链接**
- 不支持 PDF（请先转成 PNG/JPG 再识别）

**2b. 看图理解（Agent 的眼睛）`POST /v1/ocr/describe`**（MCP：`ocr.ocr_describe`）
```
multipart: file（同上，与 image_url 二选一）→ 200 {result:true, data:{text, balance, points_charged}}
```
- 返回 `text` 为中文图片描述（场景/物体/人物/文字内容概括，3~6 句话）
- 与「纯 OCR」的区别：recognize 只认字，describe 讲图（两者**扣点不同**，以 /v1/services 实时为准）

> **口语用法**：「截图里的字取出来」→ 2a（本地图走 file 上传）；「这张图里画了什么/描述一下」→ 2b；「网上那张图（有链接）」→ 用 `image_url`。

**识别方式说明**：平台会按图片情况自动选择识别方式——常规图片秒级返回；较难的图片（密集小字、复杂表格、手写）可能走高精度通道、耗时更长。同一张图在不同时间可能走不同的识别通道，精度敏感场景请人工复核。

### 3. PDF 转 Markdown `POST /v1/pdf_md/convert`

```
multipart: file（.pdf，≤20MB；大小超限返回 413，超过 200 页仅转换前 200 页并在结果开头注明）
→ 200 {result:true, data:{text, balance, points_charged}}
```
- 返回 `text` 为 Markdown 文本（保留标题/表格结构，供 AI Agent 阅读）
- **输出上限 1MB**：转换结果超过 1MB 时仅保留前 1MB，并在文本末尾注明（超限截断）
- 扫描版 PDF（纯图片、无文本层）会提示（可先 OCR 再处理）；文件损坏/加密返回 4xx

> **口语用法**：「把 PDF 喂给 AI」→ 直接转；「扫描版读不出字」→ 先把页转成图片（PNG/JPG）再走 OCR（§2）；「内容被截断了」→ 超过 200 页/1MB 会截断并在结果中注明。

### 4. 图片格式转换 `POST /v1/img_convert`（MCP：`img_convert.convert` / `img_convert.list_formats`）

```
multipart: file 或 image_url（二选一）+ operations（JSON 数组，链式操作）
→ 200 转换后图片文件（REST）；MCP 返回一次性下载 URL + 输出大小/尺寸元数据
```
- 输入 PNG/JPG/WebP/BMP/GIF/TIFF（GIF 取首帧）→ 输出 PNG/JPG/WebP/BMP/TIFF
- 链式 operations（`type` + 参数）：`format`(target/quality 1-100)、`resize`(width/height/fit: inside/cover/fill，≤10000)、`compress`(quality)、`rotate`(90/180/270)、`flip`、`flop`、`grayscale`、`strip_metadata`
- 示例：`[{"type":"resize","width":800,"height":800,"fit":"inside"},{"type":"format","target":"jpg","quality":85}]`
- **输出默认剥离 EXIF 等元数据**（隐私优先；需保留原始元数据时在 operations 加 `{"type":"preserve_metadata"}`）；文件 ≤20MB、像素 ≤4000 万（以 `GET /v1/services` 的 `limits` 实时为准）；**格式转换=重新编码**——像素画面内容保持不变（JPG/WebP 为有损格式，quality 1~100 越大越接近原图；完全无损请输出 png/bmp/tiff；透明背景转 jpg/bmp 会变黑/白，保留透明请转 png/webp）
- 能力枚举：MCP `img_convert.list_formats`（格式矩阵+参数元数据，0 点）；REST `GET /v1/services` 实时清单
- MCP 传图同 OCR 口径：图片本就在公网用 `image_url`；本地图用 REST `file`（勿传第三方图床）

> **口语用法**：「图片太大发不出去」→ `compress`/`resize`；「转成 JPG/PNG」→ `format`；「去掉拍摄信息（EXIF）」→ 默认即剥离；「保留原始元数据」→ 加 `preserve_metadata`。

### 5. 账单截图排版（把账单截图排成一份 A4 汇总 PDF）

**一句话**：把多张账单支付截图（多图 / 整个文件夹 / zip）交给平台 → 逐张读出**图内支付时间** → **自动按时间排序** → 网格**排版**生成一份 **A4 汇总 PDF**。典型场景：「把这几十张账单截图排成一份 PDF」（报销/对账）。

**5a. 识别单张截图的时间 `POST /v1/bill_pdf/recognize`**（MCP：`bill_pdf.recognize`）
```
multipart: file（必填之一；PNG/JPG/JPEG/WebP/BMP/GIF；单张大小/像素上限同图片识别服务，以 list_layouts 实时为准）
        或 image_url 表单字段（与 file 二选一——仅支持公网可直接访问的图片链接；
        本地截图请直接用 file 上传，不要传到第三方图床再传链接）
可选: job_id（本次排版任务号，自选）、index（该图在本任务中的序号）
→ 200 {result:true, data:{date, text, engine, elapsed_ms, points_charged, balance}}
```
- `date` 为**图内支付时间**，归一化为 `YYYY-MM-DD HH:MM:SS`（例：`2026-07-15 21:46:05`）；识别不到时为 `null`（请人工确认，**不要**自己编一个时间再排版）
- `text` 为该图识别出的原始文本（排查「为什么没读到时间」时可直接看它）；`engine` 为**识别方式标识**（平台自动选择识别方式，客户端不用关心细节）
- 逐张调用即可（进度可控、单张出错只影响该张）；**请串行逐张调用，不要并发**（并发会被限流挡下）
- 计费：识别按 `recognize` 键计点（**点位以服务目录实时为准**）；**识别失败不扣点**；同 `job_id` + `index` **在识别失败后立刻重试不重复扣点**；上一次已成功时带订单号重试**只取回上次成功的结果、不会重新执行一遍**（结果 **2 小时**内有效，过期或内容不同时**提示重新发起调用**）

**5b. 多张排版出 PDF `POST /v1/bill_pdf/build`**（MCP：`bill_pdf.build`）
```
multipart: files（必填，**多份同名 files 字段**，可多张）, cols（可选，每页列数 1~6，默认 3）,
           rows（可选，每页行数 1~6，默认 3）, orientation（可选 portrait 竖版默认/landscape 横版）,
           dates（可选，与 files 一一对应的 JSON 数组，如 ["2026-07-15 21:46:05", null]）,
           job_id（可选，本次排版任务号）
→ 200 直接返回 PDF 文件流（响应头：X-Pages / X-Images / X-Cols / X-Rows / X-Orientation / X-Output-Size / X-Points-Charged / X-Balance-*）
```
- 传 `dates`（一般就用 5a 识别出来的时间）→ **按时间升序排版**，未识别到时间的排最后；不传则按上传顺序排版
- 计费：生成按 `build` 键计点（**点位以服务目录实时为准**）；成功出 PDF 才扣；失败或中途停止不扣点；**同一批图片 + 同一排版参数在生成失败后立刻重试不重复扣点**（换图或换参数=新任务，重新计点）；上一次已成功时带订单号重试**只把上次生成的结果取回、不会重新执行一遍**（结果 **2 小时**内有效，过期或内容不同时**提示重新发起调用**）
- 上传与上限（以 `bill_pdf.list_layouts` 实时为准）：单次张数、单张大小、输出大小均有上限；超出返回 413，请分批排版或先压缩图片

**5c. 能力枚举 `bill_pdf.list_layouts`**（MCP，**0 点**）：返回网格参数范围、朝向、单次张数/单张大小/输出大小上限、识别方式与计费键——用它确认当前实时上限，不要背文档里的数字。

#### 自然语言用法（Agent 侧）

| 用户说 | Agent 做什么 |
|---|---|
| 「把这几张账单截图排成一份 PDF」 | 逐张 `bill_pdf.recognize`（同一 `job_id` + 递增 `index`）→ 收集 `date` → 多图走 REST `POST /v1/bill_pdf/build`（带 `dates`）→ 把 PDF 交给用户 |
| 「按支付时间排好，A4 一页 9 张」 | 同上，`build` 传 `cols=3&rows=3`（默认即 3×3 竖版） |
| 「这些都是同一笔/时间不对」 | 逐张回报 `date` 让用户核对；需要人工指定顺序时用 `dates` 显式传值 |
| 「这份 PDF 有几页」 | 读 `X-Pages`（MCP 返回 `pages`），不要自己数图猜 |

**标准流程（4 步，改任务必须换 `job_id`）**：
1. 取一个 `job_id`（自选字符串，如 `user-2026-07-15-a`；**同一次排版必须同一个**）
2. 逐张识别：`bill_pdf.recognize`（传 `job_id` + `index=0,1,2…`）→ 记住每张的 `date`
3. 排版：REST `POST /v1/bill_pdf/build`（`files` 多份 + `dates` + `job_id`）→ 拿到 PDF；MCP 客户端可用 `bill_pdf.build`（返回**一次性下载 URL，5 分钟有效**，立即下载保存）
4. 把 PDF 或下载链接交给用户；**需要重排请换新 `job_id`**（同 `job_id` + 同一批内容在结果有效期内会被当作重试、直接取回上一份 PDF，看不到新改动；**超过 2 小时，或这次内容与上次不同**时请**重新发起调用**，按新调用计费）

#### 常见失败与处理

| 情况 | 表现 | 处理 |
|---|---|---|
| 图内没有可用支付时间 | `date` 为 `null` | **照常排版**（该图排在最后），把该图单独回报用户人工确认；不要编时间 |
| 截图没截到时间那一栏 | 多次识别都 `null` | 让用户补一张含时间的截图，或人工告知时间并用 `dates` 显式指定 |
| 图片损坏/格式不支持/超大 | 400 `bad_file` / 415 `bad_extension` / 413 `too_large`、`file_too_large` | **不扣费**；让用户另存为标准 PNG/JPG 或压缩后重试 |
| 张数超过上限 | 413 `too_many_files` | 拆成多批（每批 ≤ 当前上限，见 `list_layouts`），或先合并/裁剪截图 |
| 输出 PDF 超过大小上限 | 413 `output_too_large` | **不扣点**（渲染成功但超限不扣）；减少张数或压缩图片后重试 |
| 短时间调用过快 | 429 `rate_limited`（响应带 `Retry-After`） | 指数退避重试（1s→2s→4s）；**带同一 `job_id`/`index` 在识别失败后立刻重试不重复扣费** |
| 任务繁忙排队超时 | 503 `bill_pdf_busy` | 稍后重试；带同一 `job_id`/`index` 在识别失败后立刻重试不重复扣费 |

> **不要刷新页面（红线）**：网页入口 `/bill` 排版过程中**刷新或关闭页面，本批次需要重新识别并重新计点**（识别结果不落库）。Agent 侧同理：一次任务一次做完，中途停了就重新识别、重新计费。

### 6. 数据查询服务 `POST /v1/gw/{code}/call`

```
POST /v1/gw/{code}/call  {"path":"...","params":{...}}  → {data:{...}, balance, points_charged}
```
服务代码以 `GET /v1/services`（或 MCP `zerotech.list_services`）实时清单为准（各服务免费或按次计费以服务目录为准，**不要假设任何服务免费**）。当前已注册的常用查询服务：

| code | 说明 | path / params |
|---|---|---|
| `gw_fx` | 汇率查询（计费以服务目录为准） | `path="/v1/latest"` params `{"base":"USD","to":"CNY"}`（货币代码 3 字母大写）；货币列表 `path="/v1/currencies"` |
| `gw_ip` | IP 归属地/运营商查询（计费以服务目录为准） | `path="/"` params `{"ip":"8.8.8.8"}`（合法 IPv4） |
| `gw_md` | 网页转 Markdown（计费以服务目录为准） | `path="/https://目标网页"`（或 `/http://...`），params 可空 |
| `gw_chuck` | Chuck Norris 笑话（英文原文，免费） | `path="/jokes/random"` params `{"category":"dev"}`（分类可选 animal/career/dev/food 等）；分类清单 `path="/jokes/categories"`；搜索 `path="/jokes/search"` params `{"query":"..."}` |
| `gw_sunrise` | 日出日落/正午/昼长查询（免费） | `path="/json"` params `{"lat":"22.54","lng":"114.06","date":"today","tzid":"Asia/Shanghai","formatted":"0"}`（lat/lng 必填；date/tzid/formatted 可选） |
| `gw_avatar` | 头像生成：seed 确定性生成 SVG/PNG/JPG/WebP，60+ 风格（计费以服务目录为准） | `path="/v1/render"` params `{"style":"lorelei","seed":"user-123","format":"png"}`（size 16~512 仅位图适用）；风格清单 `path="/v1/styles"` |
| `gw_sticker` | 表情包：按情绪/场合/关系挑聊天表情图（见下方指引） | `path="/v1/pick"` params `{"emotion":"celebrate","intensity":3,"relation":"friend"}`（三个必填，见下） |

> path 必须命中服务白名单、参数须符合服务规则（缺失/非法返回 422 明确错误：`missing_param`/`invalid_ip`/`invalid_currency`，**不扣费不出账单**）；服务暂时异常返回 502（稍后重试）。

> **通用约束**：重复提交口径见「计费与支付」——**失败后立刻重试不重复扣点**（请求头 `Idempotency-Key` 沿用同一个值；**前提是上一次确实失败**）；上一次已成功时带订单号重试**只取回上次结果、不会重新执行一遍**（结果 **2 小时**内有效，过期或内容不同时**提示重新发起调用**、按新调用计费）；文件大小/限流限制以接口实际返回为准（超限返回 413 too_large / 429 rate_limited）；**文件与参数先校验后计费**（扩展名/内容魔数/参数格式无效时直接返回 400/415/422 明确错误，**不会扣费、也不会生成按次账单**）；MCP base64 通道服务端上限为**解码后 ≤48MB**（约 64MB base64 文本），更大文件改 REST multipart。

#### 表情包（gw_sticker）挑图指引

**一句话**：按「情绪 × 强度 × 关系」挑一张合适的聊天表情图（15 种情绪 × 3 档强度 × 6 种关系，支持场景词与多套风格）。

**调用示例**：
```bash
curl --config "$HOME/.nanyu-curl.cfg" -X POST https://pay.starrynan.art/nanyu/v1/gw/gw_sticker/call \
  -H "Content-Type: application/json" \
  -d '{"path":"/v1/pick","params":{"emotion":"celebrate","intensity":3,"relation":"friend"}}'
# MCP 等价：gateway.call(code="gw_sticker", path="/v1/pick",
#   params_json="{\"emotion\":\"celebrate\",\"intensity\":3,\"relation\":\"friend\"}")
```

**参数（前三个必填，英文枚举）**：

| 参数 | 必填 | 说明 |
|---|---|---|
| `emotion` | ✅ | 15 值（**英文**）：`laugh` 笑 / `happy` 开心 / `celebrate` 庆祝 / `thanks` 感谢 / `sorry` 抱歉 / `comfort` 安慰 / `encourage` 鼓励加油 / `love` 喜欢比心 / `surprise` 惊讶 / `awkward` 无语 / `sad` 难过 / `angry` 生气 / `tired` 疲惫 / `confused` 疑惑 / `greet` 招呼 |
| `intensity` | ✅ | 1=轻（点到为止）/ 2=中（常规表达）/ 3=强（夸张、明显情绪） |
| `relation` | ✅ | `friend` 朋友 / `family` 家人 / `partner` 亲密 / `colleague` 同事 / `client` 客户 / `stranger` 陌生人（映射语气/礼貌度上限） |
| `scene` | 可选 | 场景词过滤（如 `生日`、`工作`、`考试`；自由文本 ≤64 字符） |
| `style` | 可选 | `fluent-3d` / `fluent-flat` / `twemoji`（清单以服务接口实时为准） |
| `recent_ids` | 可选 | 最近用过的图 id（短 id、逗号分隔）→ 避免连发同一张 |

- **返回**：`emoji`（字符）+ `image_base64`（PNG 128×128）+ `tags`（emotion/intensity/scene/style）+ `id` + `sha256`
- **交付建议（字符优先）**：能用一个 emoji 字符表达时，**直接内联字符**（零传输、任何客户端原生渲染）；需要图片时（特定风格/大图装饰/客户端 emoji 渲染差）再解码 `image_base64` 展示
- **署名义务**：素材来自 **Twemoji（© Twitter, Inc and other contributors，CC BY 4.0）** 与 **Microsoft Fluent Emoji（MIT）**——对外展示/分发时保留来源署名（响应 `attribution` 字段可直接使用）
- **无匹配 / 参数错**：`no_match` 时按提示调整（放宽 intensity、去掉 scene 后重试）；参数错误（如非英文枚举、intensity 超范围）返回明确报错、修正后重试
- **场合分寸**：正式/严肃场合（报错、道歉、财务提醒）**不发表情**；不要高频刷屏。**能用字符 emoji 表达的场合不必调用本服务**（省点；需要图片/特定风格时才调用）
- **计费**：`call` 键按次计点（点位以服务目录实时为准）

> 📌 **JSON 类参数两种写法都支持**：如 `params_json`、`tags`、`operations` 既可传 JSON 字符串，
> 也可直接传对象/数组（服务端自动转换，2026-10-14 起）。

## 计费与支付

**计费速查（计费键；点位一律以 `/v1/services` 实时为准）**：

| 服务 | 计费键 |
|---|---|
| 音乐标签 | `read` / `write` / `write_batch_per_file` |
| 文字识别 OCR | `ocr_image`（纯 OCR）/ `ocr_describe`（看图） |
| PDF→Markdown | `convert` |
| 图片格式转换 | `convert` |
| 账单截图排版 | `recognize`（逐张识别）/ `build`（排版出 PDF） |
| 表情包 | `call` |
| 数据查询 | `call`（其中汇率 `gw_fx`、笑话 `gw_chuck`、日出日落 `gw_sunrise` 当前免费；以服务目录为准） |

### 余额与点数流水（对账用）

- **查余额 `GET {BASE}/v1/balance`**（MCP 等价：`zerotech.get_balance`）：返回本账户点数快照——`self_points` 自充点数、`gift_points` 赠送点数、`monthly_points` 当月免费额度、`total_points` 可用合计（字段以接口实时返回为准）。**这也是最轻量的凭证自检**（见「凭证安全与自检」第 2 条）。
- **查流水 `GET {BASE}/v1/credits/history`**（MCP 等价：`zerotech.credits_history`）：返回**本账户自己**的点数流水，默认最近 **50 条**（`limit` 最大 200）；可选 `source` 按来源筛选、`since` 按起始时间筛选（`YYYY-MM-DD HH:MM:SS`）。每条含 `change_points`（正=入账 / 负=扣减）、`source`、`ref_type`/`ref_id`（关联对象）、`expires_at`（赠送点有效期）、各余额快照、`created_at`。
- **`source` 取值**：`charge` 充值 / `bonus` 赠送 / `trial` 新客试用 / `invite` 邀请返利 / `promo` 优惠码 / `refund` 退款 / `adjust` 人工调整 / `usage` 消费 / `expire` 过期作废 / `monthly` 月度额度 / **`monthly_reset` 月度额度重置**。
- **`monthly_reset` 是什么**：每月免费额度是**跨月刷新、不累计**的——刷新时上月未用完的部分记一条**负数**流水，同时补发本月额度。因此月初看到「月度额度重置」的负数流水**属正常现象，不是点数丢失**（账户中心「点数流水」卡片与 `credits_history` 均可按该来源筛选、核对）。
- 流水**只返回当前凭证所属账户自己的记录**，接口不接受任何可指定他人身份的输入；账户中心「点数流水」与接口是同一份数据。

**扣费顺序**：当月免费额度 → 赠送点数 → 自充点数（金额/档位/扣点**以 /v1/services 与 /v1/charge/tiers 为准**）。

**免费与未开放的口径（2026-10-14 补充）**：
- **免费服务**（服务目录里标注免费、`unit_price_cny` 为 `null`）：调用**扣 0 点、也不校验余额**——余额为 0 也能正常返回；**即使服务目录里留有单价，免费状态下也一律不扣**。某次调用到底扣没扣，只看本次响应里的 `points_charged`（0 = 免费）。
- **未开放的服务**（已下架）：**全通道拒绝**——REST 返回 **503 `service_disabled`**，MCP 工具返回 `{"result":false,"code":"service_disabled",...}`，且该服务**不会出现在 `/v1/services` 与服务列表工具里**。客户看不到即代表当前不提供，**不要重试**，改用目录里仍在列的服务或转告用户联系客服。

**分阶段计费与重复提交（账单截图排版）**：该服务**按环节分别扣点**——识别按 `recognize` 键、生成按 `build` 键（**点位以服务目录实时为准**；每阶段各自成功后才扣）。**失败或中途停止不扣点**；**失败后立刻重试不重复扣费**（同 `job_id` + `index` 重试识别、同批图片 + 同排版参数重试生成；前提是上一次确实失败）；上一次已成功时带订单号重试**只取回上次结果、不会重新执行一遍**（结果 **2 小时**内有效，过期或内容不同时**提示重新发起调用**，要重排/换参数请换新 `job_id`，即一次新调用）。网页入口在限流时自动退避重试，**同一任务号在失败后立刻重试不重复扣费**；但**识别过程中刷新或关闭页面不算重试**——该批次要重新识别、重新发起调用并重新计点（红线）。

**重复提交的计费口径（全服务通用）**：**失败后立刻重试不重复扣点**——同一个请求（同一请求头 `Idempotency-Key` 或 MCP 同一工具参数）上一次**处理失败**后，用**同一个重试标识立刻**再提交一次，平台会重新处理、不重复扣费；网络超时/失败重试请**沿用与上次相同的重试标识**。**前提是上一次确实失败**，不是任何重复提交都免费：**上一次已经成功**时，带订单号重试**只把上次成功的结果取回来、不会重新执行一遍服务**，结果保留 **2 小时**；**结果已过期，或这次提交的内容与上次不同**时，平台**提示重新发起调用**——那才算一次新调用、正常计费。因此：只在确认任务确实失败时才重试；想再跑一次相同内容就是一次新调用、正常扣点。免费服务仍不扣点、不校验余额；未开放的服务仍全通道拒绝。

**支付模式三选一（默认不自动按次；REST 头 `X-Payment-Mode`，MCP 工具 `payment_mode` 参数）**：`recharge`（**默认**，余额不足**不生成按次订单**，返回"请充值或按次"并引导用户二选一——充值走 `/v1/charge/tiers` → `create` → `pay_qr`，想按次则重试请求带 `payg`）/ `payg`（强制按次付费 402）/ `auto`（兼容旧行为，余额不足自动按次付费 402）。**注意：想按次付费必须显式传 `payg`**。

**余额不足时的两种路径**：
- **路径一 · 按次付费（AI收 402，单次调用付费）**：请求带 `X-Payment-Mode: payg` 时，余额不足会收到 **HTTP 402 + `Payment-Needed` 账单**（金额=本次点数×单价，以 /v1/services 为准）。**付款后的履约方式只有一种**（平台查支付宝验证支付，不信任客户端凭证）。完整流程 3 步（缺一不可）：
  1. **首次调用**（余额不足，已带 `payg`）→ 平台返回 402 账单（响应体含 **`payg_order` 订单号**——记下它）
  2. **付款**：买家完成支付宝扣款（买家需先开通「AI付」——支付宝 App 搜「AI付」；收款方为星空手记）
  3. **用同一 Key 带订单号重试同一请求**（REST 头 `X-Payg-Order: <订单号>` / MCP 工具 `payg_order` 参数）→ **平台查支付宝验证支付是否成功**（金额必须与账单一致）→ 确认后自动入账 → **这次请求才真正执行服务并返回结果**
  **注意事项**：
  - 单次付费是"现金买一次调用"，**不进入点数余额**——点数不变是正常的（付完后余额仍不足）；下次调用需再按次付费或充值
  - **已付款的订单优先取回结果（同一请求不会被收两份钱）**：带订单号重试同一请求时，平台**优先按这张已付款的订单把上次成功的结果取回，不会额外扣点、也不会重新执行一遍**——即使此时账户点数已经变充足（例如刚充值），也**不会**改成扣点
  - **必须用同一账户（同一 API Key）重试"同一请求"**（同一接口、同一文件/参数）——账单归属该账户，换 Key/换账户/换接口重试会被拒绝；**只付款不重试 = 无结果**
  - **成功之后带订单号的重试只回放结果（付一次 = 生成一次结果）**：首次调用成功即保存结果（保留 **2 小时**）——期间带同一订单号重试同一请求，平台**只把上次成功的结果取回来，不会重新执行一遍服务**（不重新生成、不重复扣费；文件型服务取回首次生成的文件）。**结果已过期（超过 2 小时），或这次提交的内容与上次不同**时，平台**提示重新发起调用**：带同一张已付款订单号重试时，平台仍**优先按该订单履约、不额外扣点**（即使此时点数已变充足）；不带订单号再调用则为新请求——有余额→正常扣点生成新结果；无余额→重新按次付费（402 新账单）
  - **失败后立刻重试才会重新执行**：上一次**处理失败**时，用同一 `Idempotency-Key`（与首次相同）**立刻**重试会重新执行一遍、**不重复收费**；上一次已成功时不会重新执行（见上一条）
  - **重试建议带 `Idempotency-Key`**（与首次相同的键）：失败后立刻重试不丢结果、不重复扣钱；**上一次已成功时**，结果有效期内带同一订单号重试**只回放上次结果、不会重新执行一遍**。**注意**：结果只覆盖成功后的 **2 小时**；**结果已过期或这次内容与上次不同**时，平台**提示重新发起调用**，按新调用计费（带已付款订单号的重试仍按该订单优先取回结果，见上一条）
  - **MCP 通道**：余额不足返回错误码 `payment_needed`（消息含账单金额/资源/订单号；MCP 工具层无法发 HTTP 402 头）——MCP 客户端付款后把订单号传入工具 `payg_order` 参数重试同一工具调用即履约（同一 Key、同一内容）。**MCP 工具履约参数只有 `payg_order`（订单号）一个**
  - **付款确认**：平台以 `alipay.trade.query` 查单为准验证支付（响应码/交易状态/金额/订单号回读全部校验）；付款后可能需**几秒到 1 分钟**支付宝侧交易才可查询，若报"尚未支付"稍等几秒再重试

  **重试示例（付款后——与首次请求完全一致，只加订单号；以音乐标签读为例）**：
  ```bash
  # 首次调用余额不足（已带 payg）→ 平台返回 402 + Payment-Needed（响应体含 payg_order 订单号，记下它）
  # 付款后重试：订单号 + 自己的 Key（无需 X-Payment-Mode 头，带订单号即视为按次履约）
  # 凭证走环境变量 + --config（不要把 Key 拼进命令行；占位符必须替换为真实 Key）
  curl --config "$HOME/.nanyu-curl.cfg" -X POST https://pay.starrynan.art/nanyu/v1/tags/read \
    -H "X-Payg-Order: <402 响应里的 payg_order 订单号>" \
    -H "Idempotency-Key: my-retry-key-001" \
    -F "file=@/path/song.mp3"
  # → 200：平台查单确认付款 + 入账 + 履约，返回标签 JSON（本次不扣点数）
  # 同一订单在结果有效期内（2 小时）再调 → 200 只取回首次结果（不会重新执行、不重复扣费；过期或内容不同则提示重新发起调用）
  ```

  **常见错误与解决方法**：
  | 错误码 | 原因 | 解决方法 |
  |---|---|---|
  | `payg_order_not_found` (404) | 订单号无效/不属于本账户/格式错误 | 确认订单号来自**本账户**的 402 响应（PG 开头） |
  | `payg_order_not_paid` (402) | 平台查单确认尚未支付 | 确认已付款；付款后等几秒再重试（支付宝交易确认有延迟） |
  | `payg_amount_mismatch` (402) | 支付宝实付金额与账单不符 | 联系客服核对（少见，正常付款不会出现） |
  | `payg_order_mismatch` (402) | 重试的请求与首次不一致（接口/点数） | 必须重试**与首次完全相同的请求**（同接口同文件同参数） |
  | `payg_order_refunded` / `payg_order_closed` (402) | 订单已退款/关闭 | 不可履约；有余额直接调用，无余额重新按次付费 |
  | `alipay_unreachable` (503) | 支付宝查单暂不可用 | 稍后重试（平台临时故障） |
  | `payg_query_throttled` (402) | 支付确认请求过于频繁 | 稍等几秒再重试（查单有节流保护） |
  | `payment_already_fulfilled` (402) | 该订单正在被另一请求处理 | 稍等几秒再重试（TTL 内会直接回放结果） |
  | （无专用错误码） | 带同一张已付款订单号重试，平台优先按该订单把上次成功的结果取回、不额外扣点（即使点数已变充足）；仅当该订单已履约且结果已过期（>2 小时）或内容与上次不同时，才提示重新发起调用 | 有余额→直接调用（正常扣点新结果）；无余额→不带订单号重新调用出 402 新账单 |
- **普通调用**（curl 等，未带 `X-Payment-Mode: payg`）：返回 402 `insufficient_balance`，消息提示"①充值 或 ②按次付费（带 payg 重试）"二选一 → 按需引导。

### 创建充值订单（充值路径 · 网页收款）

```
POST /v1/charge/create  {"tier":"t10"} 或 {"amount_cny":23.5}，可选 {"promo_code":"..."}
→ {order_no, amount_cny, base_points, bonus_points, status:"pending"}
```
档位以 `GET /v1/charge/tiers` 为准（形如 t{amount}）。
优惠码两种：**充值型**（加赠点数/折扣）在下单时填 `promo_code`；**兑换型**（直接领点数、无需充值）用
`POST /v1/promo/redeem {"code":"..."}`（JWT，成功直接到账赠送点数；兑换型码用尽后不可再兑）。

> **支付服务维护中**：若 `GET /v1/platform` 返回 `charge_channel_open=false`，
> 充值/Key 解锁暂不可用（`charge/create`、`charge/key_unlock`、`charge/pay_qr` 返回 503
> `channel_unavailable`，提示「支付服务维护中」）——**如实转告用户稍后再试**，不要反复重试下单。

### 生成支付链接（充值路径 · 支付宝网页收款）

```
POST /v1/charge/pay_qr  {"order_no":"..."}      # JWT 或 API Key 均可
→ {pay_url, pay_form_html}
```

**Agent 流程**：拿到 `pay_url` → **交给用户**浏览器打开 → 用户支付宝付款 → **轮询确认**：
`GET /v1/charge/status?order_no=xxx` → status: pending | paid | refunded（**轮询直到 paid**，间隔 5~10 秒，最多 2 分钟；入账以查单为准）。

### Key 数量解锁（可选）

`POST /v1/charge/key_unlock` → 创建解锁订单（金额以接口返回为准），支付后 Key 上限提高（每个账户仅可解锁一次）。
**网页操作更省事**：账户中心「充值」页底部有「Key 数量解锁」入口——实时显示当前数量/上限与解锁价格，一键下单支付即可，无需拼接口。

## MCP 入口（AI Agent 原生，推荐优先）

- `{BASE}/mcp`（Streamable HTTP，Bearer API Key）——平台级入口，**配置一次永久生效**：新服务/新工具/新定价自动出现
- 工具（嵌套命名空间）：
  - 平台级：`zerotech.get_balance` / `zerotech.credits_history`（本账户点数流水，可选 `source` 筛选）/ `zerotech.list_services`（**服务列表与定价，含每个服务的描述与调用方式**——遇到不熟悉的服务代码先调它查看，新增服务自动出现）
  - 音乐标签：`music_tag.read_tags` / `music_tag.write_tags` / `music_tag.list_formats`（base64 音频）
  - 视觉识别：`ocr.ocr_image`（纯 OCR）/ `ocr.ocr_describe`（看图描述）（base64 图片）
  - PDF 转 Markdown：`pdf_md.convert`（base64 PDF）
  - 图片格式转换：`img_convert.convert` / `img_convert.list_formats`（能力枚举，0 点）
  - 账单截图排版：`bill_pdf.recognize`（单张读支付时间）/ `bill_pdf.build`（多张 → A4 PDF，返回一次性下载 URL）/ `bill_pdf.list_layouts`（能力与上限枚举，0 点）
  - 数据查询：`gateway.call(code, path, params_json)`（code 为服务代码，如 `gw_sticker` 表情包、`gw_fx` 汇率、`gw_md` 网页转 Markdown 等；path/params 见各服务说明）
  - 其他服务工具已自动挂载，**工具清单以 MCP 客户端的 tools/list 实时列表为准**（新增服务自动出现）
- base64 文件：MCP 通道受客户端消息体限制（建议文件 ≤10MB，base64 文本≈×4/3）；服务端上限见「上传与大小限制」；更大走 REST multipart；下载 URL 一次性、5 分钟有效
- 一键接入：平台 CLI `nanyu-cli.py mcp-config` 生成客户端配置

## 错误码

> **响应体统一形态**：`{"result": false, "code": "...", "message": "中文说明", "data": null}`；
> 凭证类与部分可自助修复的错误会额外带 `hint` 字段（一句话告诉你怎么修，例如"占位符要替换成真实 Key"）。
> Agent 应把 `message` + `hint` 一起读给用户，不要只报 code。

> **按症状快速定位（先看这里）**
> - 上传/文件被拒（400 `bad_file`、413 超限、415 格式、422 `parse_failed`／`bad_filename` 文件名非法）→ 见下表对应行；**一律不扣费**；
> - 401 / 凭证问题 → 先做凭证自检（「凭证安全与自检」第 2 条）再对表；**占位符未替换是最高频原因**；
> - 被限流（429）/ 账户或网络受限（403）→ 见对应行；退避重试（带原 `job_id` 在失败后立刻重试不重复扣费；成功后带订单号重试只取回上次结果、不重新执行，结果 2 小时内有效）；账户问题按提示到账户中心处理；
> - 「付款了没结果」→ 「计费与支付」按次付费 3 步：必须**同一 Key 带订单号重试同一请求**；
> - 扣费对不上 → 「安全与合规」扣费疑问（提供订单号/时间/接口，平台核实后按平台原因退点）；
> - 不确定是谁的错 → 先读响应体 `message` + `hint`（平台错误都有中文说明）。

| HTTP | code | 含义 | 处理 |
|---|---|---|---|
| 401 | unauthorized | 完全没带凭证（未认证） | 在请求头补 `Authorization: Bearer <API Key>`（响应体 `hint` 有示例） |
| 401 | bad_api_key | Key 无效：**占位符未替换**（`***`/`<api_key>`/`$变量`/「你的Key」）、复制不全、已吊销或删除 | 用真实 Key 重发；先做凭证自检（余额查询），别直接传大文件。响应体 `hint` 说明具体原因 |
| 401 | bad_token | **网页登录凭证**过期/失效（只在账户接口出现——业务接口不会返回此码） | 引导用户到账户中心重新登录；调用业务接口改用 API Key |
| 400 | email_domain_blocked | 邮箱域名不在注册允许范围（仅常用邮箱域可注册；一次性/临时邮箱域一律拦截） | 换常用邮箱注册（QQ、163、126、Gmail、Outlook 等） |
| 400 | bad_captcha / captcha_required | 图形验证码答案错误 / 未先获取图形验证码 | 重新获取图形验证码（先 GET /v1/auth/captcha）并按题目作答 |
| 400 | invite_required / bad_invite_code / invite_used_up / invite_expired | 注册邀请码缺失/无效/已用尽/已过期 | 向用户索取有效内测邀请码 |
| 400 | bad_file / empty_file / bad_magic | 文件无效（内容与格式不符/损坏/空文件/伪造）——含图片损坏或格式异常 | 检查文件，**不会扣费出账单** |
| 402 | insufficient_balance | 点数不足（默认模式；消息含"充值或按次"二选一提示） | 引导充值，或带 `X-Payment-Mode: payg` 重试走按次付费 |
| 402 | payment_needed | 按量付费账单（响应头 Payment-Needed + 响应体 payg_order 订单号；MCP 通道为错误 JSON 含账单信息与订单号） | 付款后带 X-Payg-Order（MCP：payg_order 参数）重试同一请求才会把结果给你（只付款不重试=无结果）；若该订单已成功出过结果，重试**只取回上次结果、不会重新执行** |
| 402 | payg_order_not_paid | 平台查单确认尚未支付 | 确认已付款；付款后等几秒再重试（支付宝交易确认有延迟） |
| 402 | payg_query_throttled | 支付确认请求过于频繁 | 稍等几秒再重试（查单有节流保护） |
| 402 | payg_amount_mismatch | 支付宝实付金额与订单不一致 | 联系客服核对 |
| 402 | payg_order_mismatch | 重试的请求与首次不一致 | 必须重试**与首次完全相同的请求**（同接口同文件同参数） |
| 402 | payg_order_refunded / payg_order_closed | 订单已退款/关闭 | 无法按该订单取回结果；有余额直接调用，无余额重新按次付费 |
| 402 | payment_already_fulfilled | 该订单正在被另一请求处理（并发） | 稍等后重试（结果有效期内会直接取回上次结果） |
| 402 | （无专用错误码） | 已成功出过结果，但结果已过期（>2 小时）或这次内容与上次不同——平台不报错，**提示重新发起调用** | 有余额→重新调用生成新结果；无余额→不带订单号重新调用出 402 新账单 |
| 403 | key_suspended / key_revoked | Key 停用/吊销 | 联系客服 |
| 403 | key_service_denied | 该 Key 服务范围受限（工作台专用 Key 只限其白名单服务） | 换全权限 Key，或到账户中心创建/调整 Key |
| 403 | frozen | 账户被冻结 | 联系客服 |
| 403 | captcha_required / account_locked | 登录失败次数过多需图形验证码 / 登录已临时锁定 | 引导用户到账户中心网页登录（会自动显示验证码；锁定则稍后再试），不要在 Agent 侧反复重试密码 |
| 403 | account_banned / ip_banned | 账户或当前网络环境因异常行为被限制（含原因与期限） | 如实转告用户：到账户中心查看封禁说明并提交解封申请；期限到自动恢复。不要在 Agent 侧反复重试 |
| 403 | gateway_path_denied / gateway_blocked | 请求路径不在该查询服务的允许范围内 / 查询服务暂时不可用 | 按服务说明改 path（见各服务 description）；不可用时稍后重试 |
| 404 | payg_order_not_found | 订单号无效或不属于当前账户 | 确认订单号来自本账户的 402 响应（PG 开头） |
| 404 | promo_not_found / promo_exhausted / promo_not_for_you / promo_used | 优惠码不存在/已用尽/不适用于本账户/本账户已用过 | 换优惠码或联系客服 |
| 413 | too_large / file_too_large / batch_too_large / output_too_large / too_many_files | 文件·批量·输出过大或张数超限（含 OCR 像素超限、模型上下文超限；批量总量 >500MB；账单排版单批张数/输出 PDF 超限） | 压缩（图片 JPG 质量 75~85、缩小 ≤2000×2000；PDF 压缩）或分批/走 REST multipart，**不会扣费出账单** |
| 413 | too_large_for_mcp | MCP base64 超过服务端上限 | 压缩后重试或改用 REST 接口上传 |
| 415 | bad_extension | 文件格式不支持（**APE/WavPack 不在支持范围**，支持 mp3/flac/m4a/mp4/ogg/opus/wav/aiff） | 换支持格式（音频查 /v1/formats；图片 PNG/JPG/WebP/BMP/GIF；PDF .pdf），**不会扣费出账单** |
| 422 | parse_failed | 文件无法解析（头合法但内容损坏/截断，如"ID3 头 + 非音频数据"） | 重新导出/转码后重试，**不会扣费也不会生成按次账单** |
| 422 | bad_tags / empty_tags / bad_cover | tags 参数无效（含字段类型错误——注意除 year 外所有字段值为字符串） | 按 message 修正 |
| 422 | bad_filename | 指定的输出文件名含非法字符（控制字符等不可见字符） | 把文件名改成普通字符后重试，**不会扣费也不会生成按次账单** |
| 422 | bad_b64 / bad_params | base64 解码失败（客户端截断所致，非平台问题）/ 参数冲突（如 file_b64 与 image_url 同时传）/ 枚举或范围错误（如表情包非英文枚举、强度超范围） | base64 改用 image_url 或 REST；参数二选一；按 message 修正 |
| 422 | bad_url | 图片链接非法/非 http(s)/含账号密码/非公网（内网、回环、元数据地址拒绝） | 换成公网直链（直接指向图片的地址） |
| 422 | missing_param / invalid_ip / invalid_currency / invalid_number / gateway_bad_params / invalid_emotion | 接口参数缺失或格式无效（含表情包 emotion 非 15 枚举之一） | 按 message 修正参数 |
| 422 | too_many_files | 批量文件数超限（音乐标签批量单次最多 20 个；账单截图排版单批张数上限以 `bill_pdf.list_layouts` 实时为准） | 拆分为多批（音乐标签每次 ≤20 个） |
| 429 | rate_limited / too_many_concurrent | 限流/并发过多（**新注册账户首 7 天限流更严**，为平台安全策略；响应带 `Retry-After: 60`） | 退避重试（指数退避 1s→2s→4s；新账户适当降低并发） |
| 429 | mail_daily_limit | 验证码邮件发送过于频繁（达当日上限） | 请用户明天再试 |
| 502 | gateway_upstream_error / gateway_response_too_large | 查询服务暂时错误（如数据源调整/超时/返回数据异常） | 稍后重试 |
| 502 | ocr_engine_error | 看图理解不可用，或识别（纯 OCR）两条识别通道均不可用/超时——单条通道不可用会自动切换到备用通道，通常仍返回 200 | 稍后重试 |
| 503 | gateway_not_configured | 查询服务尚未配置完成 | 稍后重试 |
| 503 | alipay_unreachable / payg_query_mismatch | 支付宝查单暂不可用 | 稍后重试 |
| 503 | service_disabled | **服务未开放**（该服务当前不提供；也不出现在 `/v1/services` 与服务列表工具里，REST 同为 503） | 改用服务目录里仍在列的服务，或如实转告用户联系客服；**不要重试**（重试不会恢复） |
| 503 | channel_unavailable | 支付服务维护中（充值/Key 解锁暂不可用） | 如实转告用户稍后再试，不要反复重试下单 |

## 完整示例（Python）

```python
import os
import requests

BASE = "https://pay.starrynan.art/nanyu"
# 凭证从环境变量读取（别把 Key 写进代码；示例文本不是真实 Key）
API_KEY = os.environ["NANYU_API_KEY"]
H = {"Authorization": f"Bearer {API_KEY}"}
# JWT：用户登录后获得（POST /v1/auth/login {"email","password"} → access_token；
# 连续输错多次后该接口要求图形验证码——脚本登录场景请引导用户到账户中心网页完成）
JWT = os.environ["NANYU_JWT"]            # 用户登录后的 access_token

# 0) 查服务/价格/档位与余额（以接口为准；余额查询同时是凭证自检）
print(requests.get(f"{BASE}/v1/services", headers=H).json()["data"])
print(requests.get(f"{BASE}/v1/charge/tiers").json()["data"])
print(requests.get(f"{BASE}/v1/balance", headers=H).json()["data"])

# 1) 音乐标签：读标签
with open("song.mp3", "rb") as f:
    r = requests.post(f"{BASE}/v1/tags/read", headers=H,
                      files={"file": ("song.mp3", f, "audio/mpeg")})
print(r.json()["data"]["tags"])

# 1b) 音乐标签：改标题（write 返回文件流，X-Written-Fields 头列出写入字段）
with open("song.mp3", "rb") as f:
    rw = requests.post(f"{BASE}/v1/tags/write", headers=H,
                       files={"file": ("song.mp3", f, "audio/mpeg")},
                       data={"tags": '{"title":"新标题","artist":"歌手名"}'})
open("out.mp3", "wb").write(rw.content)

# 2) 视觉识别：识别图片文字
with open("photo.png", "rb") as f:
    r2 = requests.post(f"{BASE}/v1/ocr/recognize", headers=H,
                       files={"file": ("photo.png", f, "image/png")})
print(r2.json()["data"]["text"])       # 纯文本

# 3) PDF 转 Markdown
with open("doc.pdf", "rb") as f:
    r3 = requests.post(f"{BASE}/v1/pdf_md/convert", headers=H,
                       files={"file": ("doc.pdf", f, "application/pdf")})
print(r3.json()["data"]["text"])       # Markdown

# 4) 查询服务：汇率查询（计费以服务目录为准）
r4 = requests.post(f"{BASE}/v1/gw/gw_fx/call", headers=H,
                   json={"path": "/v1/latest", "params": {"base": "USD", "to": "CNY"}})
print(r4.json()["data"])

# 5) 余额不足（默认模式返回 402 insufficient_balance 提示充值或按次）
r5 = requests.post(f"{BASE}/v1/tags/read", headers=H,
                   files={"file": ("song.mp3", open("song.mp3", "rb"), "audio/mpeg")})
if r5.status_code == 402 and r5.json().get("code") == "insufficient_balance":
    # 用户选择充值：建单 + 支付链接（JWT）
    tiers = requests.get(f"{BASE}/v1/charge/tiers").json()["data"]
    tier = f"t{int(tiers[0]['amount'])}"
    order = requests.post(f"{BASE}/v1/charge/create", json={"tier": tier},
                          headers={"Authorization": f"Bearer {JWT}"}).json()["data"]
    link = requests.post(f"{BASE}/v1/charge/pay_qr",
                         json={"order_no": order["order_no"]},
                         headers={"Authorization": f"Bearer {JWT}"}).json()["data"]["pay_url"]
    # 把 link 交给用户付款 → 轮询 charge/status 直到 paid
```

## 安全与合规

- 凭证不落库/不入日志；用户文件仅在处理时驻留，处理完即删
- **退款**：不提供自助退款、亦不支持无条件退款；确需退款联系平台客服人工审核（充值订单按剩余可退点数折算并扣除手续费）。**按次调用服务（按次付费）的款项不支持退款**——每次调用成功即视为完成消费，付款前请确认用量与金额
- **发票**：平台不提供发票；如需付款凭证，使用账户中心订单记录（`GET /v1/charge/orders`）
- **扣费疑问**：若发现扣点与实际调用不符（如重复扣费、失败仍扣点），可把订单号/时间/接口提供给我们核实；确认属于平台原因的，**点数由平台退还至你的账户余额**（无需你操作）。重试的计费口径分两种：①**失败后立刻重试不重复扣费**（沿用同一重试标识；前提是上一次确实失败）；②**成功后带订单号重试只取回上次成功的结果、不会重新执行一遍**（结果 **2 小时**内有效；**结果已过期或这次内容与上次不同**时，平台**提示重新发起调用**，那时按新调用正常计费）。只在确认任务确实失败时才重试。已付款的按次付费订单重试**优先按该订单把结果取回、不额外扣点**
- **联系客服**：见官网服务条款 / 隐私政策页载明的联系邮箱（`{BASE}/terms`、`{BASE}/privacy`），或账户中心站内入口
- 服务条款：`https://pay.starrynan.art/nanyu/terms`　隐私政策：`https://pay.starrynan.art/nanyu/privacy`（2026-08-29 11:00 生效）
- 所有命令真实执行；不伪造响应、不假设成功
