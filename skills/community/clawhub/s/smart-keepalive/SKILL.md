# Smart Keepalive | 智能 Keepalive

**Description:** 定时抓取资讯素材并自动发送「保活简报 keepalive」（双关 keepalive + 资讯简报），默认走 OpenClaw CLI；也支持 Hermes/其他环境通过自定义命令接入发送与润色（`KEEPALIVE_AGENT_COMMAND` / `KEEPALIVE_SEND_COMMAND`），含可选作息附录与 launchd/cron 定时部署辅助。

**何时读本文：** 用户要配置/调试 OpenClaw **定时 keepalive**、飞书或微信定时消息、`smart-keepalive.py` / `smart-keepalive.sh`、资讯简报、`prompts/`、`--doctor` / `--install-launchd` / `--install-cron`。

## 职责划分（SKILL.md / 脚本 / 提示词）

| 内容 | 放哪里 | 说明 |
|------|--------|------|
| **定时无人值守时谁决定「拉哪路素材」** | **`smart-keepalive.py`** | 加权抽样、去重、状态落盘、HTTP 抓取只能由脚本执行；**SKILL.md 不能替代运行**，否则 cron 无法读 Markdown 来拉取素材。 |
| **管线顺序、环境变量、`theme_tag` 含义、基准权重数字、状态 JSON 字段** | **`SKILL.md`（本文）** | 给人与 Agent 的**单一事实说明**；改脚本逻辑后**同步改本节**，避免脚本顶部长注释与文档漂移。 |
| **成稿语气、版式、列表格式、标题弱化、占位句丢弃等** | **`prompts/rewrite-main.md`** 等 | 由 `openclaw agent` 执行；**不要用脚本再写一套润色规则**。其中 **凡来自各信息源的条目标题均须与素材一致、禁止 agent 改写**（见 `rewrite-main.md` 第 6 条）。作息见 **`prompts/wellness.md`**；文末彩蛋见 **`prompts/status-footer.md`**。 |

- **原则**：能写在提示词里指导模型的，**不写进 Python**；必须在无模型时完成的（抓取、随机、写文件），**不写进 SKILL 当「假实现」**。
- **脚本只做**：拉取素材 → 填模板变量 →（默认）`openclaw agent` 生成正文 /（可选）`KEEPALIVE_AGENT_COMMAND` 自定义润色 →（默认）`openclaw message send` /（可选）`KEEPALIVE_SEND_COMMAND` 自定义发送。换素材 URL、权重常量或管线行为时改 Python，并**改本文对应表/段落**。

**仅部署 skill 目录不会创建系统定时任务**；周期发送需 launchd/cron（`--install-launchd` / `--install-cron` 可生成给 OpenClaw 的提示词）。

---

## 主消息版式：保活简报 keepalive

与 **`prompts/rewrite-main.md`** 保持一致：

1. **固定标题行**：`zh` / `en` 均为 `**保活简报 keepalive**`（Markdown 加粗）。
2. **第二段（一行）**：`zh` 为 `时段问候｜ 以下是{栏目}`（`｜` 与 `以下是` 之间一个空格）；`en` 为 `时段问候 — Below: {栏目}`。栏目名与 `{{THEME_HINT}}` 对齐；**不在列表前再单独起一行栏目**。
3. **正文**：有序列表；作息关怀由脚本改写为「问候与关怀同行 → 空行 → 单独栏目行 → 列表」，见 `smart-keepalive.py` 中 `insert_wellness_after_greeting`。
4. **文末状态彩蛋（可选）**：未设置 `KEEPALIVE_STATUS_FOOTER` 时，由 `openclaw agent` 按 `prompts/status-footer.md` 生成一句；提示词要求以 **`IDENTITY.md` 中的 `NAME`** 为助手称呼（脚本会尝试从 `~/.openclaw/agents/<agentId>/IDENTITY.md` 注入 `{{AGENT_NAME}}`，可用 `KEEPALIVE_AGENT_NAME` 覆盖）。失败用脚本内短句兜底。若将 `KEEPALIVE_STATUS_FOOTER` 设为非空字符串则**固定使用该文案**（不调用 agent）；`0` / `off` 关闭文末行。可用 `KEEPALIVE_STATUS_STYLE_GUIDE` 微调语气。

占位句丢弃、凌晨优先新鲜条目、「晚报」标题弱化等规则均在提示词中，**勿在脚本里再写一套**。

---

## 实现流程（供排查）

1. **`build_keepalive_brief()`**：只组装素材原始行（可含链接），不做面向用户的「业务级」润色。内部顺序概览：先算**综合乘数**（时段 × 轮换 × 节假日 × 跨日新鲜度）→ **盲盒**（`KEEPALIVE_BRIEF_CHAOS`，命中则**不参与**上述乘数，在今日仍可用源上均匀随机试拉，成功即返回）→ 否则 **基准权重 × 综合乘数** 后加权随机 → 主抽中源失败则**同轮乱序**试其余源 → **热点兜底**（多轮打乱顺序重试；轮数上限 `KEEPALIVE_BRIEF_HOT_FALLBACK_ROUNDS`，默认 `4`）。去重与 `tag_meta` 见下「简报素材随机」。
2. **主正文**：读 `rewrite-main.md`，填入 `{{BRIEF}}`、`{{LOCAL_TIME}}`、`{{HOUR}}`、`{{MINUTE}}`、`{{LOCALE}}`、`{{STYLE_GUIDE}}`，调用 `openclaw agent`；若提示词缺失则用脚本内 **`FALLBACK_REWRITE_PROMPT`**（与主提示词同版式摘要）。
3. **Agent 失败时**：用 **`format_smart_report_fallback()`** 仅保证与「保活简报 keepalive」**结构一致**（标题 + 问候 + 正文），详细措辞仍以提示词为准。
4. **作息附录**（可选）：`KEEPALIVE_REST_REMINDER=1` 时读 `wellness.md` + agent；失败用脚本内短句兜底。
5. **文末状态**：`resolve_status_footer_line`（`prompts/status-footer.md` + agent，或 `KEEPALIVE_STATUS_FOOTER` 固定文案）。
6. **发送**：默认 `openclaw message send`（遇 `Unknown channel` 重试一次）；若设置 `KEEPALIVE_SEND_COMMAND`，则改走自定义发送命令。

日志里 `body=` 仍为素材标签（如 `zhihu-daily`、`hots-multi`）。

---

## Gotchas

- **改推送语气或版式**：先改 **`prompts/rewrite-main.md`**，而不是改脚本。
- **改选材策略的「说法」、环境变量说明、与用户对齐预期**：改 **`SKILL.md`**；**改实际权重/URL/随机逻辑**：改 **`smart-keepalive.py`** 并同步 **SKILL.md** 中的表与段落。
- **OpenClaw 把素材标题改了**：属 **agent 未遵守提示词**；主提示词已要求 **各信息源条目标题与原文一致**（`rewrite-main.md` 第 6 条）。若仍发生，可在 **`KEEPALIVE_STYLE_GUIDE`** 中再强调一句「禁止改写列表内标题」，或检查是否走了错误提示词/旧版 skill。
- **`KEEPALIVE_STYLE_GUIDE` / `KEEPALIVE_WELLNESS_STYLE_GUIDE` / `KEEPALIVE_STATUS_STYLE_GUIDE`**：注入主提示词 / 作息 / 文末状态彩蛋。
- **无 target（默认）**：未配置时 CLI 自动路由到当前会话（推荐）；仅在你明确需要固定收件人时再配置 `target`。
- **定时任务找不到 CLI**：优先设 `KEEPALIVE_CLI_BIN`（兼容 `OPENCLAW_BIN`），或按 `--doctor` 修 PATH；若你使用 `KEEPALIVE_AGENT_COMMAND` + `KEEPALIVE_SEND_COMMAND`，可不依赖 `openclaw` 二进制。

---

## Hermes 兼容（关键）

如果 Hermes 环境没有 `openclaw agent` / `openclaw message send`，可直接用两个环境变量接入：

- `KEEPALIVE_AGENT_COMMAND`：自定义“润色/改写”命令（读取 `KEEPALIVE_PROMPT`，输出正文到 stdout）。
- `KEEPALIVE_SEND_COMMAND`：自定义“发送”命令（读取 `KEEPALIVE_MESSAGE` / `KEEPALIVE_CHANNEL` / `KEEPALIVE_TARGET`）。

可选：

- `KEEPALIVE_CLI_BIN`：指定默认 CLI（二进制可设为 `hermes` 或绝对路径）。

示例（仅示意，按你的 Hermes 命令改）：

```bash
export KEEPALIVE_CLI_BIN=hermes
export KEEPALIVE_AGENT_COMMAND='hermes ai --agent "$KEEPALIVE_AGENT_ID" --prompt "$KEEPALIVE_PROMPT"'
export KEEPALIVE_SEND_COMMAND='hermes message send --message "$KEEPALIVE_MESSAGE" --channel "${KEEPALIVE_CHANNEL:-}" --target "${KEEPALIVE_TARGET:-}"'
```

若 Hermes 暂时没有“agent 改写”能力，可把 `KEEPALIVE_AGENT_COMMAND` 指向一个“原样回传 prompt”或固定文本的脚本，主流程会自动兜底到脚本内版式。
- **简报时段**：`_brief_time_bucket()` 使用**本机本地时间**；若服务器在 UTC，时段会与预期不一致，可改系统时区或用同一时区的机器跑定时任务。

---

## 资讯源（脚本仅负责抓取）

**简报素材随机（`build_keepalive_brief()`）**：

- **每源每日至多一次（默认）**：某一素材源**成功选用**后，同一日历日内后续轮次不再抽中该源（加权池与热点兜底均遵守，避免「随机一次、兜底又一次」重复出现）。
  - **状态文件**：`~/.smart-keepalive/brief-sources.json`（JSON，**原子写入**；可用 `KEEPALIVE_BRIEF_STATE_FILE` 改路径）。字段与脚本一致：`date`（与 `used` 对齐的「今日」）、`used`（当日已成功选用过的源标签列表）、`tag_meta`（各源 `last`/`prior` 日期，用于跨日新鲜度 ×0.5）。
  - **审计日志**：与状态文件同目录，文件名为 `<状态主文件名>-audit.log`（默认状态文件为 `brief-sources.json` 时即 `brief-sources-audit.log`），**只追加、不自动轮转**；可用 `KEEPALIVE_BRIEF_AUDIT_LOG=0` 关闭。
  - **主日志**：默认再写一行到 `LOG_FILE` 或 `~/.openclaw/logs/smart-keepalive.log`（与定时任务主日志一致）；可用 `KEEPALIVE_BRIEF_LOG_TO_MAIN=0` 关闭。
  - 关闭去重：`KEEPALIVE_BRIEF_DAILY_ONCE=0`。
- **时段权重（默认开启）**：同一时段内仍是**加权随机**（非固定顺序）。在**尚未被今日用过**的源上，先按基准权重再乘本地时段系数，并与下述「轮换 / 节假日 / 新鲜度」**连乘**后归一化抽样；另有 **盲盒**与 **约 10% 兜底**（见上流程）。关闭：`KEEPALIVE_BRIEF_TIME_WEIGHTS=0`。
  - **0:00–6:00**：国外大报/国际向乘数高。
  - **6:00–10:00**：新闻向乘数高。
  - **10:00–17:00**：科技/热榜向乘数高。
  - **17:00–24:00**：社区/科技类乘数高。
- **4 小时轮换 + 早/晚强制**（默认）：`pick_rotating_theme()` 在非早/晚时段给不同栏目组加权；**早晨**再强化新闻类、**晚间**再强化社区/科技类。关闭：`KEEPALIVE_BRIEF_ROTATION=0`。
- **跨日新鲜度**：状态文件 `tag_meta` 记录各源最近选用日；若**连续两个日历日**都选中同一源，**次日**该源额外 ×0.5（一次）。关闭：`KEEPALIVE_BRIEF_FRESHNESS=0`。
- **节假日**：**周末**及 `KEEPALIVE_BRIEF_EXTRA_HOLIDAYS` 所列日期略提高知乎、少数派。关闭：`KEEPALIVE_BRIEF_HOLIDAY_BOOST=0`。
- **盲盒随机**：默认 **10%** 概率走「均匀随机」试源（仍尊重今日去重），`theme_tag` 为 `brief-chaos`。关闭或调概率：`KEEPALIVE_BRIEF_CHAOS=0`（关闭）或 `0.05` 等。

**加权池**（与脚本 `base_weighted` / `BRIEF_TAG_KEYS` 一致）：基准权重之和 **0.90**，余量 **0.10** 为热点兜底（`BRIEF_FALLBACK_WEIGHT`）；再与时段/轮换/节假日/新鲜度等**连乘**后，在**当日仍可用**源上归一化加权随机。

| 基准权重 | 数据源 | 日志 `theme_tag` |
|---------|--------|-------------------|
| 0.09 | 知乎日报（AnyFeeder） | `zhihu-daily` |
| 0.09 | 南方周末推荐（AnyFeeder `infzm/recommends`） | `infzm-recommends` |
| 0.09 | 每日环球视野（AnyFeeder） | `idaily-today` |
| 0.09 | 少数派（直连） | `sspai-feed` |
| 0.09 | 果壳科学人（AnyFeeder `guokr/scientific`） | `guokr-scientific` |
| 0.09 | 法广中文网（AnyFeeder `rfi/cn`，法国国际广播电台中文） | `rfi-cn` |
| 0.09 | 新华社新闻·新华网（AnyFeeder `newscn/whxw`） | `xinhua-whxw` |
| 0.09 | 36氪（直连） | `36kr-feed` |
| - | 中央气象台每日天气提示（网页提炼，仅城市天气补充行，不参与主抽样） | `nmc-weather-daily` |

**其它 `theme_tag`（脚本返回，供 `{{THEME_HINT}}`）**：

| `theme_tag` | 含义 |
|-------------|------|
| `brief-chaos` | 盲盒路径（`KEEPALIVE_BRIEF_CHAOS`），均匀试源 |
| `hots-multi` / `hots-single` | 热点兜底合并后多条 / 单条 |
| `hots-default` | 兜底仍无可用条目 |

- **兜底**：约 **10%** 概率落入热点池，或加权池**全部抓取失败**时 → 见上 `hots-*`。

**热点兜底**（`run_theme(4)` / `run_theme_hot_fallback`）：多路源（南方周末推荐 / 新华社 / 法广中文网 / 果壳科学人 / 36氪 / 中央气象台每日天气提示 / 虎嗅）；外层轮数上限由 `KEEPALIVE_BRIEF_HOT_FALLBACK_ROUNDS` 控制（默认 `4`，允许 `1`–`32`），每轮随机顺序（与 `_brief_time_bucket` 偏好组合），先跳过当日已用源再全员重试；合并正文后洗牌，最多取 5 条。

`pick_time_preferred_theme()` 仅供 `run_theme` 演示链；简报轮换见 `_brief_rotation_multipliers()` + `pick_rotating_theme()`。`run_theme(1|2|3)` 为按主题编号调用时的**源链**。

| theme | 含义（`run_theme` 源链） |
|-------|---------------------------|
| 1 | 知乎日报 → 新华社新闻 → 南方周末推荐 → 每日环球视野 → 法广中文网 → 果壳科学人 → 少数派 → 36氪 → 虎嗅 |
| 2 | 每日环球视野 → 法广中文网 → 知乎日报 → 南方周末推荐 → 少数派 → 新华社新闻 → 果壳科学人 → 36氪 |
| 3 | 少数派 → 虎嗅 |
| 4 | 同上热点兜底 |

**素材 URL（脚本内已配置；经抽检停更或不可用的源已移除）**  

| 名称 | URL |
|------|-----|
| 知乎日报 | `https://plink.anyfeeder.com/zhihu/daily` |
| 南方周末推荐 | `https://plink.anyfeeder.com/infzm/recommends` |
| 每日环球视野 | `https://plink.anyfeeder.com/idaily/today` |
| 果壳科学人 | `https://plink.anyfeeder.com/guokr/scientific` |
| 法广中文网 | `https://plink.anyfeeder.com/rfi/cn` |
| 新华社新闻（新华网） | `https://plink.anyfeeder.com/newscn/whxw` |
| 36氪 | `https://36kr.com/feed` |
| 少数派 | `https://sspai.com/feed` |
| 虎嗅（兜底） | `https://www.huxiu.com/` |
| 中央气象台国内天气预报（北京入口） | `https://www.nmc.cn/publish/forecast/ABJ/beijing.html` |

新闻/科技源多为 AnyFeeder `plink` 直链。天气源可用 `KEEPALIVE_NMC_WEATHER_URL` 覆盖默认 URL（用于镜像或临时替换）；脚本会从该 URL 自动推导同域名的 `/rest/*` 实时接口，确保“展示页与实时数据”同源。天气城市优先取 `KEEPALIVE_WEATHER_CITY`，否则取 `config.json.weatherCity`（由 `--setup` 初始化）。

---

## 快速开始

```bash
cd ~/.openclaw/skills/smart-keepalive
python3 smart-keepalive.py --setup
bash smart-keepalive.sh
python3 smart-keepalive.py --doctor
```

---

## 配置优先级（发送目标）

- **channel**：`KEEPALIVE_CHANNEL` → 本地 `config.json.defaultChannel` →（可选）`openclaw.json` 默认。
- **target**：`KEEPALIVE_TARGET` → 本地 `config.json.defaultTarget` →（可选）`openclaw.json` 默认。
- **默认行为**：若没有 target，且未显式配置 channel，则清空 channel，交给 CLI 自动路由到当前会话。
- **显式 channel 生效**：若通过 `KEEPALIVE_CHANNEL` 或本地 `config.json.defaultChannel` 明确设置了 channel，即使 target 为空也会保留该 channel。
- **可选兼容**：设置 `KEEPALIVE_FOLLOW_OPENCLAW_DEFAULTS=1` 才会回退到 `openclaw.json` 默认 target/channel。

---

## 环境变量（精简）

| 变量 | 作用 |
|------|------|
| `OPENCLAW_HOME` / `OPENCLAW_CONFIG` | 根目录与配置 |
| `LOG_FILE` | 主任务日志路径（默认 `~/.openclaw/logs/smart-keepalive.log`）；简报 `[brief-sources]` 摘要亦写此文件（可关，见 `KEEPALIVE_BRIEF_LOG_TO_MAIN`） |
| `SKILL_DIR` | skill 目录（用于找 `prompts/`） |
| `KEEPALIVE_CHANNEL` / `KEEPALIVE_TARGET` | 渠道与目标 |
| `KEEPALIVE_FOLLOW_OPENCLAW_DEFAULTS` | 设为 `1` 时，缺省回退到 `openclaw.json` 默认 channel/target（默认关闭） |
| `KEEPALIVE_REST_REMINDER` | `1` 开启作息附录 |
| `KEEPALIVE_AGENT_ID` / `KEEPALIVE_SESSION_ACTIVE_MINUTES` | 凌晨活跃判定 |
| `KEEPALIVE_STYLE_GUIDE` / `KEEPALIVE_WELLNESS_STYLE_GUIDE` | 注入主提示词 / 作息提示词 |
| `KEEPALIVE_NMC_WEATHER_URL` | 覆盖中央气象台天气页面 URL（默认 `https://www.nmc.cn/publish/forecast/ABJ/beijing.html`）；同时决定实时接口域名来源 |
| `KEEPALIVE_WEATHER_CITY` | 覆盖天气城市（优先于 `config.json.weatherCity`；`--setup` 会提示填写，默认北京） |
| `KEEPALIVE_APPEND_WEATHER` | `1`（默认）每次发送追加天气行；`0`/`off`/`false` 关闭天气追加 |
| `KEEPALIVE_WEATHER_STRICT_REALTIME` | `1`（默认）仅信任 `/rest/weather` 实时温度；若实时接口不可用则不追加天气；`0` 可回退页面解析 |
| `KEEPALIVE_BRIEF_DAILY_ONCE` | `1`（默认）每源每日最多成功选用一次；`0`/`off`/`false` 关闭 |
| `KEEPALIVE_BRIEF_STATE_FILE` | 简报「今日已用源」状态 JSON 路径（默认 `~/.smart-keepalive/brief-sources.json`） |
| `KEEPALIVE_BRIEF_AUDIT_LOG` | `1`（默认）向同目录 `brief-sources-audit.log` 追加选用记录；`0` 关闭 |
| `KEEPALIVE_BRIEF_LOG_TO_MAIN` | `1`（默认）向 `LOG_FILE` 或 `~/.openclaw/logs/smart-keepalive.log` 追加一行摘要；`0` 关闭 |
| `KEEPALIVE_BRIEF_TIME_WEIGHTS` | `1`（默认）按本地时段调整加权池相对权重；`0` 关闭（仅基准权重） |
| `KEEPALIVE_BRIEF_ROTATION` | `1`（默认）4h 槽轮换 + 早新闻/晚热搜强制倾向；`0` 关闭 |
| `KEEPALIVE_BRIEF_FRESHNESS` | `1`（默认）连续两日选同一源则次日 ×0.5；`0` 关闭 |
| `KEEPALIVE_BRIEF_HOLIDAY_BOOST` | `1`（默认）周末与额外节假日略提知乎/少数派；`0` 关闭 |
| `KEEPALIVE_BRIEF_EXTRA_HOLIDAYS` | 逗号分隔 `YYYY-MM-DD`，与周末一并视为「节假日」偏好 |
| `KEEPALIVE_BRIEF_CHAOS` | `0.1`（默认）盲盒均匀随机概率；`0` 关闭 |
| `KEEPALIVE_BRIEF_HOT_FALLBACK_ROUNDS` | `4`（默认）热点兜底外层轮数上限（每轮内两轮尝试：先跳过当日已用源再全量重试）；`1`–`32`；调高更易凑到素材但可能拉长总耗时 |
| `KEEPALIVE_STATUS_FOOTER` | 未设置→`openclaw agent` 按 `prompts/status-footer.md` 生成一句；非空→固定文案；`0`/`off` 关闭 |
| `KEEPALIVE_STATUS_STYLE_GUIDE` | 注入文末状态提示词（与 `KEEPALIVE_WELLNESS_STYLE_GUIDE` 类似） |
| `KEEPALIVE_AGENT_NAME` | 覆盖从 `IDENTITY.md` 读取的 **NAME**（注入文末彩蛋提示词） |
| `KEEPALIVE_CLI_BIN` | 默认 CLI 可执行文件（可设为 `openclaw` / `hermes` 或绝对路径） |
| `OPENCLAW_BIN` | 兼容旧变量；未设 `KEEPALIVE_CLI_BIN` 时生效 |
| `KEEPALIVE_AGENT_COMMAND` | 自定义改写命令（`$KEEPALIVE_PROMPT` / `$KEEPALIVE_AGENT_ID` / `$KEEPALIVE_CLI_BIN`） |
| `KEEPALIVE_SEND_COMMAND` | 自定义发送命令（`$KEEPALIVE_MESSAGE` / `$KEEPALIVE_CHANNEL` / `$KEEPALIVE_TARGET` / `$KEEPALIVE_CLI_BIN`） |

---

## 日志

| 文件 | 内容 |
|------|------|
| `LOG_FILE` 或默认 `~/.openclaw/logs/smart-keepalive.log` | 每次发送一条 keepalive 的全文摘要、`body=` 标签；可选含 `[brief-sources]` 选用记录 |
| `~/.smart-keepalive/brief-sources.json`（可 `KEEPALIVE_BRIEF_STATE_FILE`） | `date` / `used` / `tag_meta`（见上「状态文件」） |
| 同目录 `<主文件名>-audit.log` | 每次记入新源时追加一行（TSV），**不自动轮转**，需自行清理或 logrotate |

---

## English (short)

**Smart Keepalive** sends periodic messages via CLI. Default path is `openclaw agent` + `openclaw message send`; Hermes/other runtimes can override with `KEEPALIVE_AGENT_COMMAND` / `KEEPALIVE_SEND_COMMAND`. **Copy and layout live in `prompts/rewrite-main.md`** (fixed **保活简报 keepalive** header, time-based greeting, brief body); **`prompts/wellness.md`** covers optional wellness lines. The script fetches source items via a weighted pool (time slot, 4h rotation, holiday/freshness tweaks, optional chaos draw, daily dedup, multi-retry hot fallback), fills templates, rewrites, and sends. Edit those markdown files first when changing filters or tone.

---

## 保活与状态检查（给 Agent 的提示）

「保活简报」本质是**定时管线是否还能把一条消息推出去**；不是通用监控面板。帮用户排查或解释时，可按下面顺序，用语中性、短句。

**建议排查顺序**

1. `python3 smart-keepalive.py --doctor`（或项目内等价路径）：确认 `openclaw` 可执行、`openclaw.json` / channel、launchd 或 cron 环境等。
2. 读 `~/.openclaw/logs/smart-keepalive.log`：是否有 `ERROR`、发送失败、`Unknown channel` 重试等。
3. 手动试发：默认用 `openclaw message send --message "ping"`（按需加 `--channel` / `--target`）；若使用 Hermes/自定义发送命令，则执行你配置的 `KEEPALIVE_SEND_COMMAND` 对应试发。
4. 素材：若简报里常出现「本轮暂无可用条目」，检查网络与资讯源是否偶发失败（脚本已做重试与兜底，不必夸大成「服务宕机」）。

**文末状态彩蛋（默认）**：未设置 `KEEPALIVE_STATUS_FOOTER` 时由 **`prompts/status-footer.md`** 经 `openclaw agent` 单独生成一句，与主正文 `rewrite-main.md` 分开；可用 **`KEEPALIVE_STATUS_STYLE_GUIDE`** 微调。若仍希望主正文里顺带提管线情况，可写进 `KEEPALIVE_STYLE_GUIDE`，**不要**要求模型伪造日志里不存在的告警。

**English (for agent)**

When the user asks about “keepalive” health: clarify it means the **scheduled pipeline** (fetch → rewrite → send), not full infra monitoring. Prefer `--doctor`, `smart-keepalive.log`, then a manual send test (OpenClaw or the command configured by `KEEPALIVE_SEND_COMMAND`). Do not invent incidents not present in logs.
