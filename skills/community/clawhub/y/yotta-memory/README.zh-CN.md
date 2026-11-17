<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-memory banner" width="100%" />
</p>

<h1 align="center">元忆（yotta-memory）</h1>

<p align="center">元忆 —— 有权限边界的文件式智能体记忆：让任何 AI 智能体活过会话，而不是只活在单次对话里。</p>
<p align="center">开工 <code>recall</code> 恢复上下文、重要信息 <code>remember</code> 落盘、收工归档；记忆是落在用户自己目录里的 Markdown 文件——<b>可读、可改、可审计、可回滚</b>，零依赖、即装即用。</p>
<p align="center">FACT 共享、PREF / BOUND / COMMIT 私密隔离——<b>谁该读、谁不该读，由机制而非 AI 自觉决定</b>；一份记忆可跨智能体共用，记忆库随盘走、局域网可共享。</p>
<p align="center">「越用越懂（v0.14.0）」：<code>context</code> 一键开工上下文包——长期理解摘要优先（复用 <code>consolidate</code>）+ <code>profile</code> 用户画像（零推断）+ 近期走廊（按时间）+ 近期高价值补位 + 边界 + 承诺 + 会话闭环契约，记忆从「存储」成长为「会成长的记忆系统」。</p>
<p align="center"><b>私密区机制级加密</b>：AES-256-GCM 信封加密 + 口令派生主密钥 + 恢复钥匙；<code>yotta-memory view</code> 用户查看平台（口令解锁看全部 AI 记忆）；<code>migrate</code> 明文→密文迁移；<code>--no-encrypt</code> 可降级。跨 AI 私密从「纪律层隔离」升级为「机制层不可解」。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-memory"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-memory" /></a>
  <a href="https://github.com/YottaMeta/yotta-memory"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-memory" /></a>
  <a href="https://github.com/YottaMeta/yotta-memory/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-memory" /></a>
  <a href="https://github.com/YottaMeta/yotta-memory"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

> 📖 面向用户的操作手册见 [USER_GUIDE.md](USER_GUIDE.md)。
> 🆕 **v0.24.0（结构容量整改）**：`backup status` 按 manifest 时间选择有效备份并隔离未来时间异常；新增只读 `index --stats`，索引 v5 使用年份 gzip 分片并兼容 v4；新写入进入 `yyyy/mm/dd` 日级桶，`layout plan/apply/rollback` 支持可回滚迁移；`doctor` 增加类型压力四指标；`scan` 支持精确文件 + 规则 + 行哈希 + 有效期的例外策略，`--policy-candidates` 只生成候选、不自动启用。
> 🆕 **v0.24.1（自启服务 profile）**：`lan enable` 在目标用户上下文生成 `serve-profile.json`；Windows 计划任务、Startup 兜底、systemd 与 crontab 都引用该绝对 profile。`serve --profile <文件>` 固定 memoryHome / runtimeHome / configDir，并在路径缺失或 Windows 用户不匹配时 fail-closed，避免 S4U / 无用户环境启动落到 `C:\Users\Default\.yottamemory` 空库后返回远端 MCP 401。
> 🆕 **v0.23.2（ClawHub 门面）**：ClawHub 上的技能卡改为英文优先的双语摘要与描述（新增 `clawhub-dist/yotta-memory` 专属发布副本），README 首屏新增上面三条使用案例；命令、参数、输出与记忆库格式全部不变。
> 🆕 **v0.20.0（上下文分页 + 画像驱逐修复）**：`memory.hook` 的 PREF 驱逐空转已修复——hook / paging 决策生效时，画像段落按实时可读条目渲染并套用同一套过滤；自我接入档案不进候选、不可驱逐。新增 `context.paging`：仅在显式 `--budget` 时调用，hook 先过滤、paging 再排序与分页；`drop` 始终安全应用，`order` 仅在 `complete:true` 且未截断时应用。`context --json` 新增 `paging` 块，`--explain` 增加 `[paging]` 轨迹。配置与协议见 `references/provider-protocol.md`。
> 🆕 **v0.18.1（蒸馏溯源 + 日期绝对化 + 巩固标记 + 规则晋升建议 + 写入纪律）**：`distill` 新增分类型提取清单（事件 / 教训 / 待办 / 成长 / 规则边界 / 其他）+ 逐条 `[溯源: 文件#L<a>-L<b>]` + 实测质量指标 + 跳过与边界，`--json` 输出结构化报告；`consolidate` 摘要按条目 `created` 把「昨天 / 上周 / 本月 / 今年」写成绝对日期，归档副本写入巩固标记（`--undo` 剥离还原）；`maintain --rules` 只读给出「重复踩坑 → 建议升级为规则」（默认阈值 3，不自动写 BOUND）；记忆守则新增冲突权威顺序 6 层与写入纪律 3 条。

> 🆕 **v0.18.0（命中打点 + 容量水位 + consolidate 提案闸门 + 上下文压缩审计）**：`recall` / `explain` / `feedback --useful` / `context` 记录本地命中元数据（`hit_days` 默认保留 90 天；`hit_queries` 只存查询 8 位指纹、最多 12 槽，不存原文；随文件加密 / 备份 / 导出），`config set usage_enabled false` 或命令级 `--no-usage` 可关；只读命令与跨 owner 私密条目不写。`maintain --capacity` 只读报告容量水位、30 / 90 天活跃度、LRU / LFU 淘汰候选（冷却期 30 天 + immutable / BOUND / evergreen / pinned 豁免）与晋升建议（≥3 次命中且 ≥3 个不同查询，只出建议命令）；`archive` 默认豁免冷却期与标签常青，`--force` 可显式覆盖。`consolidate` 默认等价 `--propose`（结构化报告 + `--json`），`--apply` 交互式需确认串、非交互必须 `--yes`；首次启用显示一次数据生命周期说明。`doctor` 规模体检新增 `scale_info_*` 与逐项 `ok / info / warning` 分级（`doctor.ok` 仍只看 critical）。新增 `context --audit [--from <文件|->] [--json] [--gate N]`：核对被压缩掉的内容是否已落盘，输出未落盘清单与 `remember` 建议命令，只读、不自动补写。`archive --dry-run` 只预览不改库（不动文件 / 不建事务快照 / 不写审计），无候选时不建整库快照，`archive --json` 输出结构化报告；MCP 侧只补只读 / 预演能力（`archive.dryRun`、`maintain.capacity`、`context.audit` + 内联 `auditText`、`consolidate` 只出 propose 报告），`archive --force` 与 `consolidate --apply / --undo` 仍只在命令行。上一版 v0.17.4：`rename` 消除平铺 / 分层同序号冲突（跨布局 fail-closed + 破坏性闸门 + 审计）。
> 🆕 **v0.17.4（rename 改名）**：`yotta-memory rename <记忆 id> <YYYY-MM-DD-NNNN.md>` 给单条记忆改名，用于消除「平铺 / 分层同序号」冲突。身份键 = 类型 + owner + 文件名，跨两种布局检查；目标名被占用或文件已存在一律拒绝（fail-closed）。走破坏性闸门（doctor + 独立备份 + 事务快照），改名后重建索引并写 `rename` 审计；`--dry-run` 只预览零写入。仅 CLI 提供，MCP 工具面不变。
> 🆕 **v0.17.3（帮助可读性）**：顶层 `--help` 不再逐项重复「做什么：」前缀——每条命令与选项直接写说明正文，「什么时候用：」与「注意：」保留不变。仅帮助文案变化，命令、参数与退出码零改动。
> 🆕 **v0.17.2（私密维护的 owner 门）**：`explain` 对其它 owner 的私密条目改为直接拒绝，不再打印 subject / statement；`archive` / `maintain` 跳过不属于当前身份的私密条目（用 `--agent <id>` 声明身份，只有用户显式 `--unsafe` 才越界）。安装器加固：拒绝对符号链接目标写入，不做整目录删除。上一版 v0.17.1：`view` 删除 AI 身份时确认 ID 输入错误会立即提示「ID 不匹配，请输入完整 agent ID」，不再静默返回；用户取消仍保持静默，后端确认校验与破坏性操作闸门不变。
> 🆕 **v0.17.0（规模：文件分层 + doctor 规模体检 + 索引按需加载 + bench 基准评测）**：新写入按年/月分层——公共 `facts/<年>/<月>/`、私密 `private/<owner>/<type>/<年>/<月>/`；v0.16 及更早的平铺文件留在原位继续可读，不做自动迁移。归档保留分层，不同月份的同名文件不会互相覆盖。`doctor` 新增规模段（记忆条数 / 单目录最大文件数 / 索引总体积 / 索引冷启动耗时），阈值用 `config set scale_warn_entries` / `scale_warn_files_per_dir` / `scale_warn_index_bytes` / `scale_warn_cold_start_ms` 调整，超阈值只告警，不锁定破坏性写入。大库检索可以按年份只读对应分片：`recall --year <yyyy>` / `context --year <yyyy>`（可重复传多次，不传即全量、行为与旧版一致）。新增 `bench` 可复算基准评测：默认按库内条目确定性抽样，`--evalset <文件>` 也可指定评测集；输出 Recall@k / MRR / nDCG@k / HitRate + 95% 置信区间、库指纹与评测集指纹，`--gate <指标>=<数值>` 可接 CI，同库同评测集同参数必得同结果；全程只读，不重建索引、不写访问计数、不调用外部 embedding。上一版 v0.16.7：明文库转加密推荐交互式 `yotta-memory migrate --recovery-key-out "$env:USERPROFILE\yotta-memory-recovery.key"`，自动化使用 `YOTTA_MEMORY_PASS`；`view` 复用端口前校验 memory_home 指纹。
> 🆕 **v0.17.0（恢复探针 + 记忆库安全扫描）**：`doctor --baseline [--against <库路径>] [--template <文件>]` 与 `backup drill --probe` 在目标库 / 恢复副本上跑六类只读基线探针（身份 / 近期 / 仅源库独有 / CJK / 操作规则 / owner 范围）；条目身份键与布局无关，旧平铺 → 新年/月分层的迁移不会误报「缺失」；缺失项列出清单并非零退出（`doctor` exit 2 / `drill` 判失败），探针不硬编码任何记忆，`--template` 只加严判定。新增 `scan` 记忆库安全扫描：七类（恶意指令 / Prompt 注入 / 凭证泄漏 / 数据外泄 / 护栏绕过 / 行为操纵 / 权限提升）+ 五级分级 + `file:line` 证据，默认只报告、零网络零依赖；`--gate` 命中该级别及以上 exit 1；`--quarantine` 需 `--yes` 或交互确认，先把原文件逐字节备份到 `.memory-scan/quarantine/` 再替换命中行，`--restore` 还原；凭证片段一律打码不回显。
> 🆕 **v0.16.5（doctor JSON 契约）**：`doctor --json` 顶层新增稳定字段 `schemaVersion` / `encryption` / `migration_required`，同时保留原有 `checks` / `warnings` / `identity` 结构。
> 🆕 **v0.16.4（agent-key 提示范围）**：`--agent-key-file` 不存在时不再为公共 / 维护命令输出全局 `stderr` 警告；只有真正访问私密区才 fail-closed，并给出缺失路径、`view` / `key bind`、`key status` / `key claim` 步骤。`whoami --json`、`doctor --json`、`config get --json` 返回结构化 `identity.mode` / `identity.agentKeyStatus`。
> 🆕 **v0.16.2（首启修复）**：空加密库 `view` 可用恢复钥匙解锁；非 TTY 支持 `--password-stdin`；恢复钥匙支持 `--recovery-key-out <文件>`；`--agent-key-file` 不存在时降级未授权（公共 FACT 可读、私密 fail-closed）；空明文库可直接 `migrate` 启用加密；`view` 端口占用给明确提示。
> 🆕 **v0.16.3（迁移最短路径）**：明文库第一次转加密推荐交互式：
> `yotta-memory migrate --recovery-key-out "$env:USERPROFILE\yotta-memory-recovery.key"`
> 迁移后用 `yotta-memory view` 授权 AI；`view` 与 `yotta-memory key bind <id>` 是等价路径，随后执行 `key status` / `key claim`，再带 `--agent-key-file` 执行 `reindex` 重建加密索引并 `recall` 验证。
> 🆕 **v0.16.0（身份模型 + 稳定运行时）**：身份不再从环境变量读取。HTTP / 远程 MCP 用请求头 `Authorization` + `X-Agent-Id` + `X-Agent-Key`；stdio MCP 用显式参数 `--agent-id` + `--agent-key-file`；CLI 用 `--agent` + `--agent-key` / `--agent-key-file`。新增 `runtime install --from-current` / `use` / `rollback` / `status`，创建 `<runtimeRoot>/current` 稳定入口，受管 MCP、自启与备份任务不再写死版本目录。`doctor --runtime` 检查 CLI / current / MCP 配置 / 运行中 server / 技能副本漂移；MCP `serverInfo` 返回 `runtimePath` / `identityMode` / `toolProfile`。
> 🆕 **v0.15.0（MCP 工具分组）**：`serve --tools core|full` 控制 MCP 工具暴露面。`core` 常驻 `context / recall / search / remember`；`full` 保留现有 16 个诊断与维护工具。未指定参数时默认 `full`，保持现有配置兼容。

> 🆕 **v0.14.0（越用越懂 + CLI 诊断）**：`context` 新增「长期理解摘要」段（优先加载 `consolidate` 产物）+「近期走廊」段（按 updated / created 倒序）+「本会话闭环契约」（开工加载、进行中立即 `remember --verify`、收工前复盘）；原有近期记忆改为「近期高价值记忆（补位）」，与摘要 / focus / 走廊按文件去重。身份、长期摘要、铁律、画像、边界、承诺与闭环契约不受 `--budget` 截断；不改变存储、加密、owner 隔离与权限判定。本版同时合并 CLI 诊断修复：显式 `--agent` 优先于非受信 ambient `YOTTA_AGENT_ID`；只有 `YOTTA_MEMORY_TRUST_ENV_AGENT=1` 时环境身份才参与判定。`key status` / `key claim` 共用 AI_HOME 发现规则（显式 `--to` / `--agent-key-file` > `YOTTA_MEMORY_AGENT_HOME` / `YOTTA_MEMORY_AGENT_KEY_FILE` > Codex / OpenCode / 通用宿主默认），`key status` 始终输出 `checked` 与 `discovery`。usage 直接列出 `remember <type> <subject> <statement>` 与 `recall [关键词]`。

> 🆕 **v0.13.2（安全）**：owner ID 不是认证凭证。私密读写必须持有 `agent_key`：由用户执行 `yotta-memory view` 授权（或自行运行 `yotta-memory key bind <id>`），再配置 MCP 注入 `YOTTA_AGENT_ID` + `YOTTA_MEMORY_AGENT_KEY` + `YOTTA_MEMORY_TRUST_ENV_AGENT=1`（CLI 用 `--agent <id> --agent-key <key>` 或 `--agent-key-file <文件>`）。授权同时写临时 `keys/pending/<id>.key`，AI 新会话用 `key status <id>` / `key claim <id>` 领取到 `<AI_HOME>/.yotta-memory-agent-key` 后删除 pending；弹窗 key 供用户单独备份。legacy `keys/cache/*.key` 不再加载。仍有 owner 需要重新绑定时，`key list` 与失败的私密操作会输出 `[YTM_MIGRATION_REQUIRED]` 并列出受影响 agent；AI 只提醒步骤，由用户在 `yotta-memory view` 逐个授权；平台一次性展示 `agent_key`，已有 binding 时需先「吊销」再重新授权，旧 key 随即校验失败。

> 🆕 **v0.12.2**：可靠性收口——新增 `yotta-memory doctor` 开工检查；`maintain --apply`、`consolidate --apply`、`merge`、`archive` 与 `--purge` 在写入前自动创建事务快照，快照失败或严重异常时拒绝写入。

> 🆕 **v0.12.1**：安装与更新文档明确区分引擎 CLI（`yotta-memory`）和技能安装器（`yotta-memory-install`），并补齐可直接复制的升级命令。

> 🆕 **v0.12.0**：可靠性基线——`init` 对已有记忆库默认拒绝覆盖（用 `--attach` 接入）；`forget` 先移入 `.trash/` 并留审计；`backup create / list / doctor / restore` 支持独立盘备份、SHA-256 清单校验和只恢复到新目录。

> 🆕 **v0.10.0**：压缩遗忘——`consolidate` 周期摘要压缩（同主题旧记忆 → 带溯源摘要 + 原文归档，`--undo <batch>` 一键回滚）；近重复自动合并（`maintain --dedup` 置信度分档，`--apply` 批量执行）；分类型衰减（FACT 慢 / PREF 中 / COMMIT 任务类快 / BOUND 不衰减）；`consolidate --batches` 批次审计可查。

> 🆕 **v0.9.0**：召回质量与上下文选择——可选本地 embedding 插件、`context --focus`、`--explain` 选择解释。

> 🆕 **v0.8.5**：安全加固——MCP `distill` 不再接受 `--model`；MCP `export` / `import` 路径限记忆库内；CLI `distill --model` 不再走 shell（改为允许清单）。

> 🆕 **v0.8.2**：发布元数据修复——三次源重发带 `--name 元忆 yotta-memory`，修复 ClawHub 展示名缺失中文（原为裸 `yotta-memory`）；无功能变更。

> 🆕 **v0.8.1**：`view` 用户查看平台改为服务端分页（记忆多了一次只渲染当前页，页码上下页）；`recall` 增加候选预过滤（语义检索前先粗筛候选集，命中集不变，记忆量大时不再逐条全量语义 / 模糊 / 编辑距离）；公共 `index.json` 超过 5000 条时按年份分片（`index-<year>.json`），避免单文件膨胀。

## 使用案例

**1. 不再丢上下文。** 开工时智能体跑 `yotta-memory context`，一次拿到身份、长期摘要、近期走廊、边界与承诺；不用每个会话重新解释项目。

**2. 决策当场落盘。** 用户说「记住」时，智能体执行 `yotta-memory remember <类型> <主题> <内容> --verify` 并回读；FACT 进公共区，偏好 / 边界 / 承诺只进本智能体私密区。

**3. 收工不留半截状态。** 会话结束前写一条 COMMIT 锚点；`maintain` / `consolidate` 让记忆库长期不膨胀，`context --audit` 核对上下文被宿主压缩时是否有重要内容没落盘。

## 核心价值

多数记忆方案把「记住」做成了黑盒：数据进了数据库或云端，用户看得到内容却改不动、难以审计，更控制不了「哪个智能体能看到什么」。元忆换了一条路——把记忆还原成看得见、管得着的文件（公共 FACT 明文可审计，私密区机制级加密、用户可口令解锁）：

- **记忆就是文件**：每条记忆是一个带 YAML frontmatter 的 Markdown 文件，放在用户自己的目录里。任何编辑器都能看、能改、能删；git 直接做版本管理与回滚，团队同步与交接走同一条标准工具链。
- **隔离由机制保证**：FACT 进公共区共享，PREF / BOUND / COMMIT 进私密区、按 owner 物理分目录（`private/<owner>/<type>/`）。读取按 scope/owner 分区过滤，越界内容由 CLI 拦截、永不返回（默认静默跳过；显式跨读无授权报错拒绝）；读写一律走 CLI / MCP，禁止 shell 直读写库文件——权限由机制把关，不依赖 AI 的「自觉」。
- **零依赖、即装即用**：无守护进程、无数据库、无向量库，只需 Node.js。安装即用，数据留在本机，任何机器都能部署。
- **越用越懂（v0.14.0）**：`context` 一键生成开工上下文包——长期理解摘要优先（复用 `consolidate` 的周期摘要）+ `profile` 聚合用户画像（引擎零推断，只归组原文）+ 近期走廊（按更新时间取样）+ 近期高价值补位 + 边界 + 承诺 + 会话闭环契约；SKILL「记忆守则」注入规则层（类型红线 / 触发信号 / 了解用户 / 底线 / 宿主隔离），只注入规则与机制、不注入人格数据，出厂零数据。
- **自我学习 / 自我进化 / 自我提升（v0.8.0）**：`recall` 语义检索（同义词 / 拼音全拼+首字母 / 字段加权 / 模糊匹配，零依赖）+ 效用分融合排序；`feedback` 显式使用反馈闭环（useful / useless 调整 weight / confidence / feedback_net，越用越懂）；`maintain` 规则层自组织（统一效用分 + 年龄自动归档 / 遗忘候选 / 去重，默认 dry-run，immutable / BOUND 豁免）；`distill` 心理日志蒸馏（统计摘要 / 主题画像 / 知识地图，可选 `--model` 外部模型增强）。
- **压缩遗忘（v0.10.0）——记忆越用越精简**：`consolidate` 周期摘要压缩——把超龄 + 长期闲置 + 低效用的同主题旧记忆归纳成 **1 条带溯源的摘要**（每条原文路径都写在正文里）留在活跃区，原文整体进 `.archive/`，`--undo <batch>` 一键回滚；`maintain --dedup` 给近重复打分（≥0.85 高置信自动合并 / 0.65–0.85 建议手动），`--apply` 批量合并同归属重复组；时效分量改**分类型衰减**（FACT 慢 / PREF 中 / COMMIT 任务类快 / BOUND 永不衰减）——持久事实不被时间抹掉，过期承诺快速让位；每一步写批次审计（`--batches` 可查）。
- **可靠性基线（v0.12.0 / v0.12.2）**：`init` 遇到已有记忆库默认拒绝覆盖（`--attach` 用于接入）；`forget` 先移入 `.trash/` 并写删除审计；`backup create / list / doctor / restore` 支持独立盘备份、SHA-256 清单校验、恢复默认只写新目录；`yotta-memory doctor` 检查根目录 / 密钥库 / 索引 / 身份 / 最近备份，破坏性操作在写入前自动创建事务快照。
- **私密区加密（v0.7.0）**：私密区文件 AES-256-GCM 信封加密（口令派生主密钥 + 恢复钥匙 + 每 owner 加密索引）；`yotta-memory view` 用户查看平台（口令解锁看全部 AI 记忆）；`migrate` 明文→密文迁移；`--no-encrypt` 可降级。跨 AI 私密从「纪律层隔离」升级为「机制层不可解」。
- **便携记忆盘**：记忆库本身就是记忆引擎——装在硬盘或主机上随盘走，局域网内其它主机上的智能体可远程读写；本地零进程与局域网常驻两种模式可并存，插上硬盘即恢复全部记忆。

## 核心优势

| 优势 | 说明 |
|---|---|
| **可追溯蒸馏与规则晋升（v0.18.1）** | `distill` 分类型提取清单 + 行号溯源锚点 + 实测质量指标 + 结构化 `--json`；`consolidate` 相对日期绝对化 + 归档副本巩固标记（`--undo` 剥离还原）；`maintain --rules` 只读「重复踩坑 → 建议升级为规则」；记忆守则新增冲突权威顺序 6 层与写入纪律 3 条 |
| **数据主权在用户** | 公共 FACT 明文、可读可改可审计；私密区 AES-256-GCM 加密（用户经 `yotta-memory view` 口令解密查看）；git 可版本化，回滚 / 团队同步都走标准工具 |
| **真正的权限边界** | 公共 / 私密分区 + 按 owner 物理分目录（`private/<owner>/<type>/`）+ scope/owner 过滤 + 授权机制（grant / identity=user / `--unsafe`），越界内容由 CLI 过滤、永不返回（默认静默；显式跨读 `--all`/`--owner <其它>` 无授权时 exit 3）；`--agent <其它>` 仅作身份声明、不授予跨读。读写走 CLI / MCP，禁 shell 直读写，不靠 AI 自律 |
| **私密区机制级加密** | 私密区（PREF/BOUND/COMMIT）文件 AES-256-GCM 信封加密（口令派生主密钥 + 恢复钥匙 + 每 owner 加密索引）；没有对应 owner 密钥的 AI 即使读到密文也解不开；`yotta-memory view` 用户查看平台：口令解锁后浏览 / 搜索 / 导出全部 AI 记忆（含各 AI 私密明文） |
| **跨智能体标准** | 符合 Agent Skills 开放标准（agentskills.io）；装一次，Claude Code / Codex / Cursor / OpenCode 等 78+ 智能体可共用同一份记忆 |
| **轻量零依赖** | 无 daemon / 无数据库 / 无向量库；Node.js 自带即跑，任何机器可部署 |
| **双级存储** | 用户级 `~/.yottamemory/`（跨项目）+ 项目级 `.yottamemory/`（随项目共享 / 交接）|
| **检索与生命周期** | 语义检索（v0.8.0：同义词 / 拼音 / 字段加权 / 模糊，零依赖）+ 效用分融合排序；统一效用分（盖棺分）规则层自动归档 / 遗忘候选 / 去重（`maintain`，默认 dry-run），记忆库越用越精简 |
| **压缩遗忘（v0.10.0）** | `consolidate` 周期摘要压缩（旧记忆 → 带溯源摘要 + 原文归档，可回滚）+ 近重复自动合并（置信度 + `--apply`）+ 分类型衰减（FACT 730 / PREF 365 / COMMIT 90 天半衰，BOUND 不衰减）+ 批次审计（`--batches` / `--undo`），长期使用不膨胀、主题不丢 |
| **越用越懂（v0.14.0）** | `context` 长期摘要优先 + `profile` 画像聚合（零推断）+ 近期走廊（按时间）+ 近期高价值补位 + 边界 / 承诺 + 会话闭环契约，记忆随使用成长 |
| **容量水位与压缩审计（v0.18.0）** | 命中打点（查询只存指纹，可关）+ `maintain --capacity` 只读水位 / LRU·LFU 候选 / 晋升建议 + `consolidate` propose → `--apply --yes` 确认闸门 + `context --audit` 上下文压缩审计（未落盘决策清单）+ `archive --dry-run` 零写入预演；MCP 侧提供同一批能力的只读 / 预演子集 |
| **生态分发** | GitHub + npm 双源同步发布；npx / git clone / Download ZIP / install.sh 四种安装方式，覆盖 17+ 类智能体目录 |
| **便携记忆盘（随盘走）** | 记忆库即引擎：装在硬盘 / 主机上，插上即恢复全部记忆；引擎主机只需装 CLI 当存放点，无需装任何 AI 智能体 |
| **局域网共享与自启** | 每智能体独立 token（Bearer + X-Agent-Id + X-Agent-Key）鉴权、可吊销；`lan enable` 注册开机自启（Windows：优先计划任务，非管理员自动降级用户级 Startup 静默自启；Linux：systemd 用户单元，不可用时自动降级用户 crontab @reboot）；MCP 工具集按 core（4 个）/ full（17 个）分组暴露，管理动作（init / config / token / lan / serve）与破坏性覆盖（`archive --force`、`consolidate --apply / --undo`）不远程暴露 |
| **本地 / 局域网双模式** | 本地 `serve --stdio` 零进程、按需拉起（无常驻）；局域网 streamable HTTP 常驻——两种模式可并存、按需选用 |

## 功能详解

### 记忆模型：四分类 + 双级存储

记忆按内容性质分为四类，类别决定可见范围：

| 类型 | 含义 | 可见范围 |
|---|---|---|
| `FACT` | 事实 / 知识 / 经验（可验证、可共享）| 公共区，所有智能体可读 |
| `PREF` | 偏好 / 习惯 / 喜好 | 私密区，默认仅所属 agent 可读 |
| `BOUND` | 边界 / 规则 / 底线 | 私密区，默认仅所属 agent 可读 |
| `COMMIT` | 承诺 / 锚定 / 约定 | 私密区，默认仅所属 agent 可读 |

- **双级存储**：用户级 `~/.yottamemory/` 跨项目共享个人记忆；项目级 `.yottamemory/` 随项目一起走，天然适合交接与团队协作。recall 时项目级优先。
- **同 key 自动更新**：同一 subject + statement 重复写入只更新 `updated`，不产生重复记录。
- **元数据丰富**：每条记忆带 `confidence`（置信度）、`tags`（标签）、`immutable`（锁定不可变）、`created/updated`、`access_count` 等，供检索与生命周期管理使用。

### 权限与隔离

- **读取三态**：公共 FACT 始终可读；自身私密始终可读；其它 agent 私密默认拒绝（不返回内容）。
- **物理隔离目录**：私密记忆按 owner 存放于 `private/<owner>/<type>/`，不同智能体的私密文件物理分离；旧版根下平铺的 `prefs/` `bounds/` `commits/` 在 `reindex` 时自动迁移。
- **三种授权入口（满足任一即可读他人私密）**：
  1. `grants.json` 显式授权：`{"<userAgent>": ["<ownerAgent>", ...]}`；
  2. identity=user：`--agent user` / `--owner user`，调用方仍需持有匹配的 agent_key；
  3. 显式 `--unsafe`（用户显式授权）。
- **默认静默、显式跨读才报错**：默认 recall 遇其它 agent 私密静默跳过（不泄露「存在 N 条私密不可见」）；仅当显式跨智能体读取（`--all` / `--owner <其它>`）且无授权命中时才报错 / 警告。
- **`--agent <其它>` 不越界**：`--agent <其它agent>` 仅作身份声明 / 展示用，不授予读取他人私密；读其它智能体私密仍需 grant / identity=user / `--unsafe`。
- **隔离定位**：scope: private 保证的是 AI 之间的语义隔离（正常 recall 不会被搜到、不会主动去读）。v0.7 起私密区为机制级机密保护——文件 AES-256-GCM 信封加密，没有对应 owner 密钥的 AI 即使读到密文文件也解不开；数据主权仍在用户，作为所有者可用 `yotta-memory view` 口令解锁查看 / 导出任何记忆文件。
- **禁止 shell 直读写**：记忆读写一律走 CLI / MCP 工具；用 shell（`Get-ChildItem` / `Get-Content` / `cat` / `ls` / `type` 等）直接读改库文件会绕过 scope/owner 权限边界，读到其它智能体私密内容。

### 智能体身份（唯一 ID + 自我档案）

每个智能体有一个**全局唯一的 agent ID**：它是私密记忆（PREF / BOUND / COMMIT）的归属键，也是远端接入的身份声明（`X-Agent-Id`）；远端加密私密读写还需匹配的 `X-Agent-Key`。

- **登记（必须唯一）**：`yotta-memory iam <id>` 写入记忆库根目录 `agents.json`，**强制唯一性**——ID 已被其它主机 / 来源（含远端 token 登记）占用时拒绝，确认是同一智能体才 `--force`。
- **确认身份**：`yotta-memory whoami --agent <id>`（远端 MCP 工具 `agent_info`）；身份不从环境变量读取。
- **自我档案（强制落盘）**：`iam` 自动写一条 PREF `subject=自我接入档案`（owner=自己），statement 为 `; ` 分隔的 key:value：`agent_id / host / memory_home / mcp_mode（stdio|http）/ engine_url（仅远端）/ token（仅远端；本机不存 token）`。开工先 `recall "自我接入档案"` 找回身份与接入信息。
- **本机免网络 token**：本机 CLI / stdio 不校验 HTTP token，但私密访问仍必须 `agent_id + agent_key`；stdio MCP 用 `--agent-id` + `--agent-key-file` 显式传入，不再走身份 env。
- **私密记忆必须有 owner**：写 PREF / BOUND / COMMIT 时未声明身份会被拒绝（公共 FACT 不受影响），从机制上防止「抄别人的 ID」。

### 画像与开工上下文（v0.6.0 + v0.9.0 + v0.14.0）

- **profile**：聚合 `private/<owner>/` 下 PREF / BOUND / COMMIT 原文，按 type + subject + tags 归组，写 `profile.md`；引擎零推断，画像结论由 AI 依据「记忆守则」内部形成，不当面贴标签。
- **context**：一键生成开工上下文包——多智能体接入铁律 + 身份 + 长期理解摘要（`consolidate` 产物优先）+ 用户画像摘要 + 任务相关记忆（`--focus`）+ 近期走廊（按 updated / created 倒序）+ 近期高价值记忆（按 importance + utility 补位并去重）+ 边界提醒 + 承诺 / 锚点 + 会话闭环契约；支持 `--budget` 动态记忆字符预算与 `--explain` 选择解释。
- **记忆守则**：SKILL.md 内置规则层（类型红线 / 主动捕获触发信号 / 了解用户三阶段四手法 / 心理学底座与对齐 / 底线与边界 / 宿主隔离 / 反模式），让 AI「越用越懂」有章法。

### 检索：语义检索（v0.8.0 + v0.9.0 embedding）

- `remember` 时自动构建索引（v0.24.0 起 version=5，含字段加权与拼音 token；逻辑体积 > 4 MB 或条目数 > 5000 时按年份写入 `index-<year>.json.gz`，同时兼容 v4 平铺 / 分片；旧索引首次 recall 自动重建）；recall 默认语义检索——精确（字段加权：subject×3 / tags×2 / statement×1）+ 同义词（内置词表，可扩展）+ 拼音（全拼 / 首字母，内置 3755 常用字表）+ 模糊（编辑距离 ≤ 2）+ 子串兜底，并与效用分融合排序（0.65 × 语义 + 0.35 × 效用），零依赖。
- `recall --explain`：展示每条命中理由（精确 / 同义 / 拼音 / 模糊 + 字段）与效用分项。
- **recall 候选预过滤（v0.8.1）**：语义打分前先用索引 token 粗筛候选集（精确 / 同义 / 拼音 / 子串 / 模糊长度门槛），命中集与 v0.8.0 完全一致；`view` 查看平台按偏移分页返回，一次只取当前页。
- **可选 embedding 插件（v0.9.0）**：`recall --embedding <命令>` 或 `config set embedding_cmd <命令>`，本地子进程通过 stdin/stdout JSON 协议返回向量；结果并入同一套排序。插件失败、超时或输出非法时自动降级为零依赖词法检索。
- **向量缓存**：向量缓存在各记忆根下 `.embed/cache.json`，键为 `sha256(命令 + 文本)`；只存向量，不存明文。
- `index.json` 的 `tokens` 字段是中文分词的词频表（TF 打分用），**不是**访问凭证；鉴权令牌在记忆目录下 `.server/tokens.json`。
- 支持关键词、`--type` 过滤、`--limit` 截断、项目级优先。
- **根位置去重（v0.6.5）**：当项目级与用户级记忆库指向同一目录（如 cwd = home 或其父）时，`recall` / `context` 自动唯一化根，同一文件只展示一次。
- 命中展示会累加 `access_count` / `last_accessed`，为生命周期管理提供依据。

### 生命周期管理（v0.8.0 规则层自组织 + v0.10.0 压缩遗忘）

- **分类型衰减（v0.10.0）**：效用分「时效」分量 = `0.5^(已过天数 / 半衰)`——FACT 730 天（事实 / 知识慢衰减，不过时）、PREF 365 天（中速）、COMMIT 90 天（承诺 / 任务类快衰减）、BOUND 永不衰减（边界常驻，绝不自动归档 / 遗忘）。可用 `config set maintain_decay_halflife_<TYPE> <天>` 调整。
- `maintain`：规则层自组织——统一效用分（confidence + 使用 + 时效 + 类型 + 结构）× weight；低效用 + 超龄列为归档候选，极端低价值列为遗忘候选（默认不真删，`--purge` 才删）；`--dedup` 现在给重复组打**置信度**（≥0.85 高置信可自动合并 / 0.65–0.85 建议手动 / 其余忽略），`--dedup --apply` 自动合并同归属高置信组（写批次审计可回滚；**与归档互斥**，不会顺手归档单条旧记忆）；`--merge A,B` 手动合并。默认 dry-run；immutable / BOUND 豁免；审计写 `.archive/audit-<日期>.jsonl`。
- `consolidate`（v0.10.0）：**周期摘要压缩**——把超龄（≥180 天）+ 长期闲置（≥90 天）+ 低效用（≤0.6）的同主题旧记忆归纳成 1 条带溯源摘要（tags `consolidate`/`summary`、正文列全溯源）并留在活跃区，原文整体进 `.archive/`；默认 dry-run，`--apply` 执行并写批次 manifest + 逐条 before/after，`--undo <batch>` 一键回滚（幂等），`--batches` 查近期批次。公共摘要进 `facts/`，私密进 `private/<owner>/<type>/`。
- `archive`：按「分类型衰减效用分 + 年龄」把低价值旧记忆移入 `.archive/`（公共 `.archive/facts/`，私密 `.archive/private/<owner>/<type>/`；immutable / BOUND 豁免），记忆库不会无限膨胀。
- `feedback`（v0.8.0）：显式使用反馈闭环——useful → weight ×1.2（上限 3.0）+ confidence +0.05 + feedback_net +1；useless → weight ×0.8（下限 0.2）+ confidence −0.05 + feedback_net −1；`--undo` 回滚；审计写 `.archive/feedback-<日期>.jsonl`。
- `distill`（v0.8.0）：心理日志蒸馏——统计摘要（类型 / 年龄 / 热度 / 反馈）+ 主题画像（按 subject 聚类合并）+ 知识地图（type → tags）；可选 `--model <cmd>` 外部模型 stdin→stdout 提炼；产物入 `private/<owner>/distills/` 或 `facts/distills/`。
- `explain`（v0.8.0 + v0.10.0）：查看单条记忆效用分项（时效显示半衰）与归档 / 遗忘 / BOUND 豁免状态判定。
- `forget`：删除单条记忆（按类型目录路径或文件名）。
- `reindex`：手动改过 `.md` 后重建索引。
- `export` / `import`：整库导出为 JSON / 从 JSON 导入，可作迁移与备份中间格式。
- git：整个记忆库可纳入版本控制，回滚 / 审计 / 团队同步。

### 智能体接入

把技能装进智能体后，SKILL.md 会自动教会智能体一套工作流：**开工 `context` 主注入（身份 + 画像 + 近期记忆 + 边界 + 承诺）→ 重要信息 `remember` 落盘 → 收工归档**，并遵循「记忆守则」（类型红线 / 触发信号 / 底线 / 宿主隔离）。也可在对话中直接说「记住 XXX」「上次说到哪了」「记一笔」触发。

### 便携记忆盘（记忆库即引擎）

- **记忆库即引擎**：`serve` 把记忆目录挂成 MCP 服务，目录随盘走；引擎主机只需装 CLI 当存放点，无需装任何 AI 智能体。
- **双模式可并存**：本地 `serve --stdio` 零进程（客户端按需拉起）；局域网 streamable HTTP（默认 `0.0.0.0:8787`）+ 每智能体 token 鉴权。
- **开机自启**：`lan enable` 注册开机自启——Windows 优先计划任务（v0.22.4 起 S4U 主体后台静默、不弹窗口；默认登录自启，`--onstart` 开机即启、无登录会话也可启动，计划任务注册需管理员），非管理员自动降级为**用户级 Startup 静默自启**（免管理员，启动脚本内联启动命令、被清理也会在开机时自动重建，v0.6.3 起不再弹 80070002）；**v0.22.5 起 Electron 宿主（如 YottaCode）自动注入 ELECTRON_RUN_AS_NODE，任务不再拉起 GUI**；Linux 优先 **systemd 用户单元**（`systemctl --user`，登录自启；`--onstart` 附加 `loginctl enable-linger` 开机即启），systemd 不可用时自动降级**用户 crontab @reboot**（v0.6.4）；`lan disable` 移除，`lan status` 查询。
- **安全边界**：管理动作（init / config / token / lan / serve）不进 MCP，token 不远程暴露；远程智能体只能读写记忆，且路径限记忆库内（export/import 的 out/src 必须落在库内）、distill 不支持 `--model`（仅本地 CLI），不能改配置、不能管 token。
- 完整操作步骤见上文「局域网多机共享」章节与 [USER_GUIDE.md](USER_GUIDE.md)。

## 常见问题 FAQ（速查）

| 问题 | 答案（详见 references/faq.md） |
|---|---|
| 类型选错？ | 只提示不阻止；forget 后重写；--no-hint 关提示 |
| 私密区加密？ | init 默认加密（主口令+恢复钥匙）；明文库 migrate 升级 |
| 多智能体权限？ | FACT 公共；PREF/BOUND/COMMIT 按 owner 隔离并绑定 agent_key，由用户通过 `view`（或 `key bind`）授权 |
| 记忆找不到？ | config get 查位置 → reindex 重建索引 → recall/search |
| 忘记主口令？ | 用恢复钥匙 reset-password（无私密区锁定的预期行为） |
| 局域网怎么连？ | 引擎 lan enable + token new；客户端配 url+token |
| MCP 没加载？ | 检查 mcpServers + 重启会话；本机直连用 CLI |
| 版本不一致？ | 运行 `yotta-memory doctor --runtime`，按漂移项给出的修复命令升级并重启 |
| 记忆库在哪？ | config get；项目级 .yottamemory |
| 跨会话恢复？ | 开工跑 context + recall |
| 备份迁移？ | export / import |

## 与其他方案对比

> 以下按方案类型对比，不涉及具体产品名称。判断标准：数据主权、部署成本、权限边界、可审计性、跨智能体能力。

| 维度 | 元忆（yotta-memory） | 数据库 / 嵌入式存储类 | 向量库 / 语义检索类 | 云端托管记忆服务 |
|---|---|---|---|---|
| 存储形态 | 公共 FACT 明文文件；私密区加密（.md.enc），git 可版本化 | 二进制 / 结构化数据库文件 | 向量索引 + 模型依赖 | 厂商服务器 |
| 数据主权 | 完全在用户本地，可读可改可删（私密区经 view 平台口令解锁） | 本地，但需专用工具读写 | 本地或自托管，模型需额外部署 | 不在用户手中，受服务条款约束 |
| 权限边界 | 内置：公共 / 私密分区 + scope/owner + 授权 | 通常无内置，需自行实现 | 通常无内置，需自行实现 | 通常只有账号级权限，无记忆级细粒度 |
| 可审计 / 回滚 | 公共 FACT 明文可审计；私密区加密但用户可用 view 平台解密，git 可回滚 | 需导出工具链，回滚复杂 | 依赖快照 / 导出机制 | 依赖平台导出能力 |
| 部署与依赖 | 零依赖，Node.js 即跑 | 需数据库运行 / 嵌入式依赖 | 需向量库 + 模型，较重 | 联网 + 账号，数据出本地 |
| 跨智能体 | 符合 Agent Skills 标准，一次写入多智能体可读 | 各智能体各自接入，无统一标准 | 需各自接入，成本高 | 取决于平台支持范围 |

**结论**：元忆的核心差异点在于把「数据主权 + 权限边界 + 零依赖」三者合一——既是可审计的文件，又有机制级的读取隔离，还不引入任何重型依赖。对「本地优先、多智能体协作、长期沉淀」的场景，这是最轻的一条路。

## 安装

元忆为「CLI + 技能」双体：`yotta-memory` 命令负责读写记忆库，技能负责教智能体工作流。以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y --package @yottameta/yotta-memory yotta-memory-install --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。
- 若要读写记忆，需安装 CLI：`npm install -g @yottameta/yotta-memory`（用法见「CLI 用法」）。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-memory.git <智能体的技能目录>/yotta-memory
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-memory` 点 **Code → Download ZIP**，解压后把 `yotta-memory` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

### 两个命令，各管一件事

这个包提供两个不同的命令：

- `yotta-memory`：读写记忆库的引擎 CLI。`npx -y @yottameta/yotta-memory` 只是临时运行这个 CLI，**不会**安装技能。
- `yotta-memory-install`：技能安装器。安装或更新技能必须使用 `npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <智能体名称>`（或 `--dir <智能体技能目录>`）。

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 命令输出样例

> 以下为示意输出（以实际版本为准），让你知道执行命令后屏幕上会出现什么。

**init（初始化记忆库）**：

```text
初始化记忆库成功：~/.yottamemory
主口令已设置；恢复钥匙：xxxx-xxxx-xxxx-xxxx（请妥善保存）
```

**remember（写入记忆，带 verify 回读）**：

```text
已记录: ~/.yottamemory/facts/2026-09-01-0001.md
[verify] 已写回读 OK: facts/2026-09-01-0001.md
```

**recall（检索）**：

```text
共 3 条记忆（前 3 条）：
[FACT] 项目名: 描述……（~/.yottamemory/facts/xxx.md）
```

**context（开工上下文包）**：

```text
# 开工上下文包（yotta-memory context）
## 1. 身份
## 2. 用户画像摘要
## 2.5 长期理解摘要
## 3. 近期走廊（按时间）
## 4. 近期高价值记忆（补位）
## 5. 边界提醒（BOUND）
## 6. 承诺 / 锚点（COMMIT）
## 7. 本会话闭环契约
```

## 升级

两种升级方式对应两种安装方式：

**升级 CLI**（重新执行一次安装命令即可，不带版本号默认装最新）：
```bash
npm i -g @yottameta/yotta-memory
```

**升级技能**：按你当初的安装方式重跑对应命令，覆盖旧版技能文件夹：

```text
npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <智能体名称>
npx -y --package @yottameta/yotta-memory yotta-memory-install --dir <智能体技能目录>
bash install.sh --agent <智能体名称>
```

如果你全局安装了 CLI，`npm i -g @yottameta/yotta-memory` 会同时升级引擎和 `yotta-memory-install` 命令；之后运行 `yotta-memory-install --agent <智能体名称>` 即可刷新技能。

升级后请核对 `yotta-memory --version` 和已安装的 `yotta-memory/SKILL.md` frontmatter 中的 `version:`。

> **v0.17.0 升级提示**：升级后请用 0.17.0 引擎执行一次 `yotta-memory reindex`。0.16.7 及更早引擎不识别年/月分层目录，旧引擎重建索引会漏掉分层条目。`doctor` 会报告平铺 / 分层同序号：内容相同的两份只索引一次；内容不同的两份都保留可读并给出路径告警；新写入不复用已占用的序号。

**v0.10.0 升级提示**——升级不碰数据：无需迁移 / reindex / 重新 init。v0.10.0 没有改记忆文件格式、`facts/` 与 `private/<owner>/<type>/` 布局，也没有改索引版本，旧库打开即用。

需要知道的 4 条行为变化：

- 检索 / 上下文排序的「时效」分量改**分类型衰减**（`0.5^(已过天数/半衰)`：FACT 730 天 / PREF 365 天 / COMMIT 90 天；BOUND 永不衰减）——持久事实排序略靠前、过期任务类承诺更快让位。
- BOUND 现在**永不**被自动归档或遗忘（此前代码只豁免遗忘、没豁免归档——本版收口）。
- `maintain --dedup` 与归档**互斥**：`--dedup [--apply]` 只查重 / 自动合并，不会顺手把旧单条记忆归档。
- 归档路径只影响**今后**的操作：公共 → `.archive/facts/`，私密 → `.archive/private/<owner>/<type>/`；既有 `.archive/` 文件原地保留（不迁移、不进索引）。

新增命令为纯新增：`consolidate` / `consolidate --undo <batch>` / `consolidate --batches`。

可选升级后自检：`yotta-memory config get`（确认 `memory_home` 未变）+ `yotta-memory recall <关键词>` 仍能搜到旧记忆；想调衰减用 `config set maintain_decay_halflife_<TYPE> <天>`。

> 升级只影响命令与技能文件，**不会动你已存的记忆**（记忆是独立于安装的文件，保留在原目录）。

## CLI 用法


| 命令 | 作用 |
|---|---|
| `yotta-memory init [--project] [--dir <目录>]` | 初始化记忆库（默认用户级 `~/.yottamemory/`；--dir 显式指定位置）|
| `yotta-memory remember <type> <subject> <statement> [--owner <id>] [--source <来源>] [--weight <0..>] [--verify] [--no-hint]` | 写入记忆（同 subject+statement 自动更新；--owner 标注归属；--source 记录来源；--weight 重要性权重、去重取 max；--verify 写后回读；--no-hint 关闭类型提示）|
| `yotta-memory recall [关键词] [--type T] [--limit N] [--year <yyyy>] [--no-usage] [--agent <id>] [--owner <id>] [--all] [--unsafe] [--explain] [--semantic] [--embedding <命令>] [--embedding-timeout N]` | 检索记忆（语义+效用分排序；可选本地 embedding 插件；读取分区过滤；越界读其它智能体私密默认拒绝，需 grant / identity=user / `--unsafe`；`--agent <其它>` 仅作身份声明、不授予跨读；项目级优先；v0.17.0 起 `--year` 只读该年份分片，可重复传多次；`--no-usage` 单次关闭命中打点）|
| `yotta-memory profile [--owner <id>]` | 生成用户画像（聚合 `private/<owner>/` 原文，零推断，写 `profile.md`；跨 owner 默认拒绝）|
| `yotta-memory context [--limit N] [--owner <id>] [--budget N] [--focus <关键词>] [--year <yyyy>] [--no-usage] [--explain] [--embedding <命令>]`；审计形态 `yotta-memory context --audit [--from <文件|->] [--json] [--gate N]` | 生成开工上下文包（身份 + 铁律 + 画像 + 长期摘要 + 任务相关记忆 + 近期走廊 + 近期高价值 + 边界 + 承诺 + 会话闭环契约；--budget 控制动态记忆字符预算；--focus 任务聚焦；--year 限定年份；--explain 输出 included/dropped 选择解释；--no-usage 单次关闭打点）。`--audit` 只读核对被压缩掉的内容是否已落盘，输出未落盘清单与 remember 建议；`--gate N` 在未落盘条数超过 N 时 exit 1；无 `--from` 时审计当前上下文包的 dropped 清单 |
| `yotta-memory forget <文件>` | 删除一条记忆（按类型目录路径或文件名）|
| `yotta-memory doctor [--json] [--runtime] [--mcp-config <文件>] [--skill-dir <目录>] [--baseline [--against <库路径>] [--template <文件>]]` | 开工可靠性检查（根目录 / 密钥库 / 索引 / 身份 / 最近备份；严重异常时锁定破坏性写入；`--runtime` 检查 CLI / current / MCP 配置 / 运行中 server / 技能副本漂移；`--baseline` 追加恢复 / 迁移六类只读探针，缺失项列出清单并 exit 2）|
| `yotta-memory archive [--days 180] [--threshold 0.4]` | 归档旧记忆（分类型衰减效用分 + 年龄；immutable / BOUND 豁免；私密入 `.archive/private/<owner>/<type>/`）|
| `yotta-memory reindex` | 重建索引（手动改 .md 后校正）|
| `yotta-memory identity remove <id> [--dry-run] [--yes] [--keep-memories] [--keep-identity] [--password <口令> \| --recovery-key <钥匙>]` | 彻底删除一个 AI 身份与私密记忆（v0.17.0）：真删身份登记 / owner 密钥 / 授权绑定 / 待领取 key / 明文缓存 / `private/<id>/` 全部私密记忆 / token / grants 引用，并重建索引 + 写审计；**公共明文 FACT 保留**、其它 AI 零影响；只能由用户本人执行（加密库要主口令或恢复钥匙，明文库要显式 `--agent user`），`view` 的 AI 列表里也有「删除」按钮；破坏性闸门 = doctor + 独立备份 + 事务快照，`--dry-run` 只列清单 |
| `yotta-memory export [--out f.json]` / `import <f.json>` | 导出 / 导入 |
| `yotta-memory config set <键> <值>` / `config get` | 记忆库位置与引擎参数（`memory_home` / `embedding_cmd` / `embedding_timeout` / `maintain_archived_utility` / `maintain_decay_halflife_<TYPE>` / `consolidate_*` / `usage_enabled` / `usage_retention_days` / `usage_query_slots` / `capacity_cooldown_days` / `capacity_warn_bytes` / `capacity_candidate_limit` / `promotion_min_hits` / `promotion_min_queries` / `scale_info_*` / `context_audit_min_coverage` 等）|
| `yotta-memory whoami --agent <id>` | 查看当前显式身份与登记状态；身份不从环境变量读取 |
| `yotta-memory iam <id> [--name <显示名>] [--user <用户名>] [--relationship <关系>] [--force]` | 登记本智能体唯一身份并自动落自我档案（`agents.json`，ID 必须唯一；可选扩展显示名 / 用户 / 关系）|
| `yotta-memory token new --agent <id> [--force]` / `token list` / `token revoke --agent <id>` | 为智能体生成 / 列出 / 吊销访问 token（登记于记忆库 `.server/tokens.json`；同 ID 已被其它来源占用需 `--force` 覆盖，防不同智能体合流）|
| `yotta-memory serve [--host 0.0.0.0] [--port 8787] [--no-auth] [--stdio]` | 启动 MCP 记忆引擎（streamable HTTP 局域网 / --stdio 本地零进程模式；Bearer token + X-Agent-Id + X-Agent-Key 鉴权）|
| `yotta-memory lan enable [--onstart] / disable / status` | 开机自启管理（Windows：计划任务 S4U 主体后台静默、不弹窗口；默认登录自启、`--onstart` 开机即启（无登录会话也可启动，注册需管理员），非管理员自动降级用户级 Startup 静默自启；Linux：systemd 用户单元，不可用时自动降级用户 crontab @reboot）。v0.24.1 生成每用户 `serve-profile.json`；`lan status` 检查路径漂移并提示缺少 `--profile` 的旧任务 |
| `yotta-memory serve --profile <文件>` | 读取每用户服务 profile，固定记忆库 / 运行时 / 配置目录；路径缺失、非法或 Windows 用户不匹配时在监听端口前 fail-closed |
| `yotta-memory maintain [--dry-run] [--apply] [--purge] [--threshold N] [--age N] [--dedup] [--dedup --apply] [--merge A,B]` / `maintain --capacity [--json]` | 记忆自组织：归档 / 遗忘候选 / 置信度查重 / 自动合并高置信组；默认 dry-run；`--dedup` 与归档互斥。`--capacity` 只读报告容量水位、LRU / LFU 淘汰候选与晋升建议（冷却期与常青条目豁免）|
| `yotta-memory consolidate [--propose] [--min-age N] [--min-idle N] [--max-utility N] [--min-group N] [--period N] [--type T] [--model <cmd>] [--apply [--yes]] [--undo <batch>] [--batches]` | 周期摘要压缩：同主题旧记忆 → 带溯源摘要 + 原文归档；默认等价 `--propose`（结构化报告，不写盘）；`--apply` 需确认（非交互必须 `--yes`）；`--undo <batch>` 回滚批次；`--batches` 查批次 |
| `yotta-memory feedback <文件|主题> --useful|--useless [--reason <原因>] [--undo]` | 使用反馈（useful/useless 调整 weight / confidence / feedback_net；`--undo` 回滚最近一次）|
| `yotta-memory distill [--owner <id>] [--subject <主题>] [--model <cmd>] [--out <路径>]` | 心理日志蒸馏（统计摘要 / 主题画像 / 知识地图；可选本地模型，仅 CLI）|
| `yotta-memory explain <文件|主题>` | 查看单条记忆效用分项与归档 / 遗忘 / BOUND 豁免状态 |
| `yotta-memory bench [--evalset <文件>] [--k N] [--seed N] [--bootstrap N] [--ablate] [--gate <指标>=<数值>] [--timing] [--year <yyyy>] [--json] [--out <文件>]` | 可复算检索基准评测（v0.17.0）：默认按库内条目确定性抽样，或用 `--evalset` 指定评测集 v1；输出 Recall@k / MRR / nDCG@k / HitRate + bootstrap 95% 置信区间、库指纹与评测集指纹，默认不含墙钟时间；`--ablate` 对比关键词 / 语义 × 融合 / 纯分；`--gate` 不达标 exit 1；`--timing` 附带 p50 / p95 后不再逐字节可复算。全程只读：不重建索引、不写访问计数、不调用外部 embedding 插件 |
| `yotta-memory scan [--path <目录>] [--gate <安全级别>] [--quarantine --yes] [--restore] [--id <批次>] [--json]` | 记忆库安全扫描（v0.17.0）：七类 = 恶意指令 / Prompt 注入 / 凭证泄漏 / 数据外泄 / 护栏绕过 / 行为操纵 / 权限提升；五级 + `file:line` 证据与规则出处；默认只报告、零网络零依赖；`--gate` 命中该级别及以上 exit 1；`--quarantine` 需 `--yes` 或交互确认，先把原文件逐字节备份到 `.memory-scan/quarantine/` 再替换命中行；`--restore` 还原；凭证片段打码不回显 |

类型：`FACT`（事实，公共共享）/ `PREF`（偏好）/ `BOUND`（边界）/ `COMMIT`（承诺）。

示例：
```bash
yotta-memory init
yotta-memory remember PREF 用户 偏好短回复，不要用表情
yotta-memory recall 偏好
yotta-memory profile
yotta-memory context --limit 10
yotta-memory recall --type FACT --limit 10
```

环境变量：
- `YOTTA_MEMORY_HOME`：覆盖用户级记忆库目录（默认 `~/.yottamemory/`）。
- `YOTTA_MEMORY_AGENT_HOME` / `YOTTA_MEMORY_AGENT_KEY_FILE`：`key status` / `key claim` 的显式 AI 宿主目录 / key 文件覆盖项；命令行 `--to` / `--agent-key-file` 优先级更高。

身份环境变量（`YOTTA_AGENT_ID` / `AGENT_ID` / `YOTTA_MEMORY_AGENT_KEY` / `YOTTA_MEMORY_TRUST_ENV_AGENT`）已不支持：CLI 会忽略，HTTP / stdio MCP 启动时会直接拒绝，避免旧宿主配置静默沿用旧身份。

## 智能体接入后怎么用

把技能装进智能体后，SKILL.md 会自动教会智能体：开工 `recall` 恢复上下文 → 重要信息 `remember` 落盘 → 收工归档。也可在对话中直接说「记住 XXX」「上次说到哪了」。

## 局域网多机共享（便携记忆盘模式）

记忆库可以装在任何主机或硬盘上（= 记忆引擎），供局域网内其它主机上的智能体远程接入：

- **本机直连**：CLI 直接读写，无需 token；
- **远程接入**：引擎主机运行 `yotta-memory serve` 常驻（或 `lan enable` 注册开机自启），远程智能体通过 MCP 以 `url + token + agent_key` 连接；同机 / 共享文件系统用 `key claim` 领取，跨机不共享文件系统时由用户安全传输宿主 key 文件。
- **本地零进程**：本机 MCP 客户端可用 `serve --stdio --agent-id <id> --agent-key-file <path>` 按需拉起 CLI（无常驻进程）。

```json
{
  "mcpServers": {
    "yotta-memory": {
      "command": "node",
      "args": [
        "<runtimeRoot>/current/bin/yotta-memory.js",
        "serve", "--stdio", "--tools", "core",
        "--agent-id", "<本智能体ID>",
        "--agent-key-file", "<AI_HOME>/.yotta-memory-agent-key"
      ]
    }
  }
}
```

### 引擎侧（记忆所在主机）

1. 初始化或接入记忆库（见 CLI 用法）。
2. 安装或刷新稳定运行时入口：
   ```bash
   yotta-memory runtime install --from-current
   yotta-memory runtime status
   yotta-memory doctor --runtime
   ```
   > `lan enable` 与备份调度会自动做同样的 runtime 准备，只登记 `<runtimeRoot>/current/bin/yotta-memory.js`。
3. 为需要访问的每个智能体生成独立 token：
   ```bash
   yotta-memory token new --agent <智能体ID>     # 打印一次，如 ytm_...（同 ID 已被其它来源占用需加 --force）
   yotta-memory token list                        # 查看已登记智能体
   yotta-memory token revoke --agent <智能体ID>   # 吊销
   ```
   > 新生成的 token 即时生效，无需重启服务。
4. 启动服务（默认监听 0.0.0.0:8787，Bearer token + X-Agent-Id + X-Agent-Key 鉴权）——临时运行或注册开机自启二选一：
   ```bash
   yotta-memory serve                          # 临时前台运行
   yotta-memory lan enable                     # 注册开机自启（Windows：计划任务/用户级 Startup；Linux：systemd 用户单元/用户 crontab）
   yotta-memory lan status                     # 查看自启状态
   ```
   > `lan enable` 注册 S4U 后台静默计划任务（不弹窗口）；`--onstart` 改为开机即启、无登录会话也可启动（注册需管理员）；非管理员时 `lan enable` 自动改用用户级 Startup 静默自启（无需管理员）；`lan disable` 移除自启。

> 首次监听 0.0.0.0 时，Windows / 系统防火墙可能询问是否放行，需允许放行，否则局域网内其它主机无法访问；`--no-auth` 会关闭鉴权，仅限可信内网使用。

### 客户端侧（远程智能体）

在智能体 MCP 配置中登记连接前，先确认该 AI 已领取 agent_key：

```bash
yotta-memory key status <智能体ID>
yotta-memory key claim <智能体ID>
```

如果引擎与 AI 不在同一文件系统，`key claim` 不能在远端直接读取 pending，需要用户用密码管理器或安全文件传输把 key 放到目标宿主目录。然后再登记连接（`url` + 三个请求头）：

```json
{
  "mcpServers": {
    "yotta-memory": {
      "url": "http://<引擎主机IP>:8787/mcp",
      "headers": {
        "Authorization": "Bearer <TOKEN>",
        "X-Agent-Id": "<本智能体ID>",
        "X-Agent-Key": "<本智能体宿主 key 文件中的 agent_key>"
      }
    }
  }
}
```

连接后可通过 MCP tools（remember / recall / search / context / doctor / forget / archive / reindex / export / import / agent_info）读写记忆与确认身份；管理动作（init / config / token / lan / serve）不进 MCP，token 管理不远程暴露；MCP export/import 路径限记忆库内、distill 不支持 `--model`，MCP 也不接受远端传入 embedding 命令——embedding 插件只能由引擎主机本地 `config set embedding_cmd` 配置。`X-Agent-Id` 必须与 token 登记的智能体一致；加密私密读写还必须携带匹配的 `X-Agent-Key`。读取分区规则与 CLI 相同（FACT 公共可读，PREF / BOUND / COMMIT 私密隔离）。

### 位置持久化

CLI 会持久记住记忆库位置（`~/.yottamemory/config.json`），同一主机上的智能体此后开工 `recall` 自动使用正确位置，无需每次指定：

```bash
yotta-memory config set memory_home <记忆库目录>
yotta-memory config get
```

位置解析优先级：`YOTTA_MEMORY_HOME`（临时覆盖）> `config.json#memory_home`（持久）> 默认 `~/.yottamemory`。把记忆库放在硬盘上、插到任意主机后执行一次 `config set memory_home`（或用 `yotta-memory init --dir <目录>` 一步初始化到指定位置），即可在该主机恢复全部记忆。

## 开发与校验

本项目内运行：`python tools/validate-skill.py yotta-memory`。

## 许可证

MIT © YottaMeta —— 详见 [LICENSE](./LICENSE)。
