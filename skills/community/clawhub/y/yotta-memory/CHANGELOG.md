# Changelog

## v0.24.3 (2026-11-14)

- **CI 精度回归**：将命中打点后的 mtime 断言收紧到 Node 原生精度边界内（纳秒偏差 < 5µs）并保留可见毫秒不变；避免 Linux 上 `utimesSync` 的亚微秒浮点误差把正确行为误判为失败。

## v0.24.2 (2026-11-14)

- **跨平台修复**：Windows profile 绝对路径（如 `C:\Users\...\serve-profile.json`）在 Linux CI / 非 Windows 环境生成任务 XML 时不再被 `path.resolve()` 误拼成仓库内相对路径；新增 host-independent profile 路径解析并保留 XML 回归。

## v0.24.1 (2026-11-14)

- **自启服务 profile**：`lan enable` 在目标用户上下文解析并写入 `serve-profile.json`（memoryHome / runtimeHome / configDir / host / port / userId），Windows 任务 XML、Startup 兜底、systemd unit 与 crontab 均显式引用该 profile，不再依赖 S4U 启动环境的 `os.homedir()`。
- **serve fail-closed**：新增 `serve --profile <文件>`；启动时校验 profile schema、绝对路径、memoryHome / runtimeHome 是否存在、userId 是否匹配，并原子覆盖进程环境。缺文件、空库、错误用户或非法路径均拒绝启动并给出中文提示。
- **状态与迁移**：`lan status` 显示 profile 的 memoryHome / runtimeHome，与当前配置比较漂移；旧任务缺少 `--profile` 时提示重新执行 `lan enable`。重新执行 `lan enable` 即可迁移旧任务。
- **验证**：新增 Windows task / Startup / Linux unit / crontab profile 回归，以及 `serve --profile` 的路径固化、缺库、错用户、CLI 缺文件用例；全量测试覆盖正常与失败路径。

## v0.24.0 (2026-11-11)

- **备份可靠性**：`backup status` 改为按 manifest `created` 解析时间排序，超过当前时间 15 分钟的备份标记 `future_timestamp` 并排除；manifest 缺失 / 不完整 / created 无效不参与健康判定；新增 `latest_valid` / `config_last_success` / `effective_last_success` / `source` / `anomalies`，`ensure-daily` 与默认备份体检复用同一选择逻辑。
- **索引诊断**：新增 `yotta-memory index --stats [--json]`，只读输出当前存储体积、逻辑体积、tokens / statement / subject / tags / usage 字段占比、token / 拼音 token 统计和 v5 gzip 年份分片预估。
- **索引 v5**：按逻辑体积 > 4 MB 或条目数 > 5000 触发 `index-<year>.json.gz`；兼容平铺 v4、分片 v4 与 v5 gzip；`--year` 只读命中的 gzip 分片；命中回写只重压对应分片；损坏 gzip fail-closed；备份白名单支持 `.json.gz`；`doctor` 新增 `index_logical_bytes` / `index_shards` / `index_format`。
- **日级布局**：新写入改为 `facts/<yyyy>/<mm>/<dd>/` 与 `private/<owner>/<type>/<yyyy>/<mm>/<dd>/`，旧布局继续可读。
- **布局迁移**：新增 `layout plan` / `layout apply --from-plan <文件> --yes` / `layout rollback --batch <id> --yes`；计划含旧 / 新路径、内容哈希与冲突；apply 写 journal，任一步失败逆序恢复；路径穿越与重复执行 fail-closed；加密 owner 无 key 时跳过。
- **类型压力**：`doctor --json` 的 `checks.scale.type_pressure` 输出 `total` / `stale_180d` / `archive_candidates` / `growth_30d` / `stale_ratio` / `growth_ratio_30d` / `pressure_level`；按计划保留 7 天观察窗，暂不删除旧 `type_max` 兼容告警。
- **扫描例外**：新增 `security/scan-policy.json` 精确例外，只接受规则 + 文件 + 整行 SHA-256 + 原因 + `review_by`；通配、路径穿越、无效哈希 fail-closed；内容变化或过期自动恢复命中；`--no-policy` 全量复核；`scan --policy-candidates --out <文件>` 只生成候选，不自动写策略。
- **验证**：真实库副本公开索引 19,638,987 B → 3,221,545 B（16.4%），bench 指标前后一致；隔离副本 `facts/2026/10` 874 文件迁移后单目录最大 874 → 466，rollback 恢复；40 条扫描候选生成但未启用。

## v0.23.3 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

## v0.23.2 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.23.1 (2026-10-25)

- **ClawHub 英文门面（无引擎变更）**：发布副本改为英文优先的双语 `summary` / `description`（英文在前、中文关键词保留在后）并补英文 tags，上线后 ClawHub 技能卡摘要由纯中文变为英文优先；构建与校验由独立发布副本流程覆盖，中文检索优化字段只增不减。
- **README 使用案例**：英文 / 中文 README 首屏新增「使用案例」三条（跨会话恢复上下文 / 决策当场落盘 / 收工留锚点 + 压缩审计）。
- 兼容性：命令、参数、输出与记忆库格式全部不变；本次仅展示层文案与发布元数据。

## v0.23.0 (2026-10-20)
- **上下文包 COMMIT 段保留策略（根治上下文包无预算膨胀）**：开工上下文包第 6 段默认只展示最近 20 条 COMMIT，`weight ≥ 1.5` 或带 `pinned` / `evergreen` 标签的条目不受上限影响、始终展示；其余折叠为一行提示（不删除，`recall --type COMMIT` 仍可检索）。新配置键 `context_commits_limit`（0 = 全部展示，回旧行为）；BOUND 段保持全量（底线保证不变）。
- **归档门槛与效用地板对齐（根治「库只长不瘦」）**：`maintain_archived_utility` 默认 0.35 → **0.55**（记忆默认 `confidence=1.0`，效用分地板约 0.42~0.47，旧门槛永远打不到）；按分类型半衰形成退役阶梯：COMMIT 约 6 个月 / PREF 约 13 个月 / FACT 约 17 个月（无再访问时，且需超 180 天龄；BOUND / immutable / pinned / evergreen 豁免不变）。`context` 的「归档提醒」升级为可执行：显示超龄条数与已达门槛条数，并给出 `maintain` 预览 / `--apply` 命令。
- **规模体检补强（防复发）**：新增「超长 statement（> 2000 字）」与「单类型堆积」两项指标（info / warn 两档，新配置键 `scale_info_long_statements` / `scale_warn_long_statements` / `scale_info_type_count` / `scale_warn_type_count`），随 `doctor` / `context` 可靠性提醒展示。
- **用法引导**：`remember` 写超长 COMMIT（> 1200 字）时提示精简与常显标签；SKILL / USER_GUIDE 补充收工锚点与保留策略说明。
- **候选修订（WorkBuddy 首轮验收缺陷修复）**：① COMMIT 段排序修复——此前按 `updated`（仅到「日」）排序，同日条目平局后退化为索引插入序，取到的是最旧 N 条（刚写入的承诺反而被折叠）；现按 `created` 倒序 + 同日按文件名序号倒序（写入先后），折叠提示范围同步校正。② `reindex` / 静默校准修复——未加密库的私密条目此前被 owner-key 门槛整段跳过，索引损坏后「重建」反而清空、库对 AI 永久不可检索；现以磁盘为准全量重建（未加密库私密条目与公共条目同存主索引），加密库无授权 key 时输出明确跳过提示与可执行路径。
- 兼容性：显式设置过 `maintain_archived_utility` / `context_commits_limit` 的用户不受默认值变化影响；`context_commits_limit 0` 可恢复「全部展示」旧行为。

## v0.22.9 (2026-10-11)

- **管理台「高级 / CLI」完整帮助：配置键块与 config 命令相邻化（UX-M-01）**：此前 39 键「配置键（config set）」块统一追加在所有命令分组之后，与「加密与安全」组末尾的 `config` 命令之间隔着整个「平台与服务」组，阅读流断裂；现在键表紧随 `config` 命令（同组相邻），找不到 config 命令时仍回退到末尾（`keysPlaced` 兜底）。
- 回归门禁：`test/view-cli-help.test.js` 断言放置逻辑标记；`tools/check_memory_view.js` 在 1440 / 390 两档断言「`#cliConfigKeys` 必须是 config 命令 `<details>` 的相邻兄弟节点」。

## v0.22.8 (2026-10-10)

- **管理台「记忆」列表两处展示修复**：① 顶部类型 chips（全部 / FACT / PREF / BOUND / COMMIT）计数跟随当前智能体 / 搜索筛选，不再固定显示全库口径（概览页四类分布保持全局口径）；② 列表排序与时间语义修复：命中打点（search / use 信号写回）改为保留文件原时间戳，旧条目被搜到不再顶到「最新」；卡片与详情显示「创建（frontmatter created，文件 btime 兜底）+ 更新（文件 mtime 到秒）」双时间。
- 修复（WorkBuddy 验收 D1）：打点恢复 mtime 的精度从毫秒提升到 BigInt 纳秒——毫秒对齐值逐 tick 精确还原；带亚毫秒余数的值误差收敛到 Node 公开 API 上限（~µs 级；原实现会把亚毫秒抹成毫秒，实测 −495,100ns → −700ns）。
- **`backup drill` 凭证入口补齐**：帮助新增 `--password` / `--recovery-key` / `--password-stdin`；无凭证时复用统一凭证入口（交互输入 / `--password-stdin` / `YOTTA_MEMORY_PASS` 环境变量），非交互且无凭证时给出明确提示。
- **修复：`backup drill` 对年 / 月分层私密条目静默跳过校验**（v0.17+ 分层写入布局回归：旧实现只扫平铺一层 `prefs/*.md.enc`，纯分层库找不到私密文件、直接跳过解密校验）→ 递归查找任意层级 `*.md.enc`，分层库同样走完整私密解密校验。
- 测试：新增 search / use 打点 mtime 稳定性回归 2 项、管理台 counts 跟随筛选 1 项、drill needPassword / 分层探测 / CLI 三入口 3 项。

## v0.22.7 (2026-10-09)

- **管理台 / 官网「配置键」补全人话说明**：高级 / CLI 页的 39 个配置键不再只显示「键名 + 命令」，每个键改为「键名 + 它是做什么的 + 默认值 / 取值 / 什么时候改」，与命令选项同一排版；键说明为单一真源（`CONFIG_KEY_HELP`），管理台 `/api/help` 与官网 `/product/` 同步渲染。
- 新增配置键说明覆盖回归：每个 `CONFIG_VALUE_KEYS` 键必须有非空 `what` / `when` 说明，且不允许出现孤儿说明（说明里存在但键列表没有）。

## v0.22.6 (2026-10-09)

- **并发写入加固**：索引更新改为跨进程互斥（`.index.lock`，mkdir 原子语义 + 陈旧锁自动回收）+ 原子落盘（临时文件 + rename）；序号分配 / 记忆落盘 / 索引更新同处一个临界区，多智能体（多宿主、多 MCP 进程）同时写入更稳。
- **索引一致性维护**：以记忆文件为唯一真源，读取路径与用户平台在后台做轻量一致性校准（自动对齐，无需用户操作；不修改任何记忆文件）。
- **管理台搜索增强**：搜索支持按编号（文件名）与归属智能体查找（原支持标题 / 内容 / 标签）。
- **管理台 CLI 页补全配置键**：高级 / CLI 页新增 39 个配置键速查（`config set` 单一真源，含 `memory_home` / `backup_*` / `maintain_*` / `consolidate_*` / `scale_*` 等），可直接搜索与复制。
- **doctor**：新增索引一致性检查（条数 = 文件数）。
- **安装器洁净度**：顶层跳过并清理 `*.tgz` 与 `test-fixtures/`（与 npm 包白名单一致），安装副本不再携带源码侧残留。
- 新增 `test/index-consistency.test.js` 5 项（一致性检测与校准、幂等、6 进程并发 120 条零丢失、跨进程锁互斥、显示与实际对账 + 编号 / 归属搜索）。
- 新增 `test/password-stdin-bom.test.js`（Windows PowerShell 管道 BOM）与 `test/installer-hygiene.test.js`（薄片洁净度 + 残留清理）。

## v0.22.5 (2026-10-07)

- **修复 Electron 宿主（YottaCode shim）下开机自启拉起 GUI 而非服务**：宿主运行时为 Electron 时（`process.versions.electron`；`process.execPath` 指向 Electron 可执行文件），此前生成的任务 / 兜底 / 定时配置不带 `ELECTRON_RUN_AS_NODE=1`，开机拉起的是桌面程序本体、8787 无监听（新机首例实测）。现在自动检测并统一注入：Windows 主任务与每日备份任务（cmd /c + `set "ELECTRON_RUN_AS_NODE=1"`）、Windows Startup 兜底 .cmd（set 前缀）、Linux systemd 单元 / crontab @reboot / 备份定时器（`Environment=` / 行内前缀）、macOS 备份 LaunchAgent（EnvironmentVariables）。
- `lan status` 新增告警：任务或 Startup 兜底命令指向 Electron 可执行文件且缺少 `ELECTRON_RUN_AS_NODE` 时，提示重新 `lan enable` 修复。
- 非 Electron 宿主行为不变（纯 Node 下生成的命令与旧版一致）。
- `test/lan-windows-autostart.test.js` 新增 8 项（Electron / 非 Electron 双态：任务 XML / 兜底 cmd / 备份任务 / Linux 单元与 crontab / macOS plist / status 告警两例）；全量 `npm test` 352/352。

## v0.22.4 (2026-10-07)

- **修复 Windows `lan enable` 开机自启三缺陷（实测复现）**：此前计划任务用 schtasks 默认交互式主体——① 在登录会话运行会弹控制台窗口；② `--onstart` 开机触发时无登录会话，任务起不来且不补跑（实测 LastTaskResult 267011）；③ schtasks 默认带电池限制与 72 小时执行时限。本版改为 **S4U 主体 + 任务 XML 注册**（零依赖）：后台静默运行不弹窗口，开机 / 登录触发均可用；默认去掉电池限制与 72h 时限（`ExecutionTimeLimit=PT0S` 不限时）；`--onstart` 在 Windows 真正生效（BootTrigger）。任务注册成功时自动清理旧 Startup 兜底文件，避免双份自启。
- `lan status` 增加显示「登录模式」并对旧交互式任务给出重新 `lan enable` 的修复提示；非管理员执行 `lan disable` 无法移除管理员注册的任务时，明确提示改用管理员终端。
- 非管理员路径行为不变：schtasks 失败（含 Access denied）自动降级用户级 Startup 静默自启（VBS 自愈保留）。
- 新增 `test/lan-windows-autostart.test.js`（11 项：任务 XML 结构 / S4U / 无电池与时限 / XML 转义 / XML 注册 / 旧兜底清理 / 权限与非权限失败降级 / status 登录模式与旧任务告警 / disable 双通道）。

## v0.22.3 (2026-10-05)

- **安装器 junction 守卫**：`bin/install.js` 对目标基目录 / 技能目录为符号链接（含 Windows junction）时 fail-closed 拒绝（退出码 4，与 `install.sh` 同口径）——不再写穿 Hub 链接指向的真源，也不再误删 Hub 侧 `bin/` runtimePayload。统一安装器以分技能灰度补丁落地（模板与其余技能输出不变）。

## v0.22.2 (2026-10-05)

- **修复（分发载荷缺口）**：`@yottameta/yotta-memory-plugin@0.22.1` 包内载荷落后技能源（`errText` 0/17、`bodyMirrorsStatement` 0/2）——0.22.1 的 D2/D3 修复未随插件分发。本版为维护性同步升版：引擎行为与 0.22.1 一致，插件载荷重新从技能源构建并对齐（逐字节校验）。

## v0.22.1 (2026-10-03)

- 管理台「高级 / CLI」页速查层升级为**全量**：覆盖 `HELP_MODEL` 全部 33 命令 / 31 子命令（64 项），分组对齐引擎帮助的 4 组（核心记忆 / 身份与画像 / 加密与安全 / 平台与服务）；每条 = 引用命令 + 可复制示例 + 危险标记 + 注意事项，说明文案仍从 `HELP_MODEL` 取（单一真源）。
- 覆盖度双向门禁：`test/view-cli-help.test.js` 断言每个命令 / 子命令至少一条速查、速查引用真实存在；`tools/export_cli_help.js --check` 在仓库级复跑同一口径。
- 完整帮助（175 选项行）与只读 `POST /api/help` 不变；页面仍只展示与复制，不执行命令。
- **管理台归属修正**：编辑 FACT（公共记忆）时可直接改归属（仅元数据 + 审计 + 可撤销，ID 校验）；PREF / BOUND / COMMIT（私密）归属置灰，提示删除重写或等待后续「归属迁移」功能。
- **写操作身份回显（防串号）**：`remember` / `forget` 输出 `[身份] agent_id: …；来源: …`；检测到宿主身份环境 `YOTTA_MEMORY_AGENT_HOME` 时追加 `[注意]` 警告；`SKILL.md` 增加「身份自检」流程（显式身份 + 回显核对 + 异常停写）。
- **修复（WorkBuddy 验收 D1）**：编辑记忆的「撤销」此前必然失败（`viewUpdateCore` 就地改写 + `viewRestoreCore` 拒绝覆盖已存在目标）；现在 `.trash/view-history/` 的编辑历史撤销允许安全覆盖，并先把当前版本留作重做快照；回收区直恢复仍 fail-closed。
- **修复（D2）**：失败提示不再把布尔 `error` 当文案（统一 `errText`，覆盖 7 处 toast + 重设口令 1 处）；失败时显示服务端 `text`。
- **修复（D3）**：编辑常规条目时同步 markdown 正文（仅当旧正文与旧 statement 完全一致；`distill` 类长文保留原 body）。

## v0.22.0 (2026-10-03)

- 记忆管理台新增「高级 / CLI」页：左侧菜单入口 + 高频命令分组速查（备份恢复 / 维护瘦身 / 检索上下文 / 扫描安全 / 导入导出 / 身份权限 / 运行时与局域网），每条 = 人话说明 + 可复制示例 + 危险操作标记；「完整命令与参数」按需加载，直接渲染引擎帮助模型（`HELP_MODEL` 单一真源，随安装版本自动更新）。
- 页面只展示与复制，不执行任何命令；新增只读 `POST /api/help`（需先解锁），不引入命令执行面。
- 新增 `test/view-cli-help.test.js`（4 项：未解锁 401 / 帮助模型与速查一致性 / 页面结构与复制入口 / 无执行端点）；全量 `npm test` 327/327。

## v0.21.1 (2026-10-02)

- 管理台「新建 / 编辑记忆」的归属 AI 选择改为平铺选择列表：一次显示全部已登记 AI（带已授权 / 未授权标记），并保留自定义 ID 输入；修复原生 datalist 弹层一次只显示约 4 项、容易被误认为 AI 缺失的问题。
- 修复记忆详情抽屉的遮罩层级：此前遮罩盖在抽屉之上，点「编辑 / 删除」会被遮罩拦截（抽屉被关掉、看起来像没做功能）；现在抽屉在上、遮罩在下。
- 记忆列表 / 最近更新 / 详情的时间显示精确到秒（文件创建与最近写入时间，由 view API 附带，不改变 frontmatter 日期格式）。

## v0.21.0 (2026-10-02)

- 记忆管理台（view）M1：本地 Web 管理台支持真读写——新建 / 编辑 / 删除（回收区 + 撤销）/ 藏（归档，可放回）/ 权限矩阵（授权 / 吊销 + agent_key 一次性展示）；概览统计与健康只读；设置页（重设口令 / 恢复钥匙 / 导出）。
- 安全与可靠性：沿用 127.0.0.1 + 主口令会话 + host / origin 校验 + CSP；写路径全部复用引擎核心（删除进回收区、编辑前保留原字节历史、归档可放回）；不新增远程能力，保持零依赖内核。
- 修复：保留式重写（view 编辑 / 读打点 / 去重等路径）会给 `tags` 逐层叠加转义反斜杠的问题；内联数组现在可正确解析，历史污染条目会在下一次重写时自动修复为规范格式。
- 新增 `test/view-m1.test.js`（7 项，含 tags 稳定性 / 历史转义修复回归）；全量 `npm test` 322/322。

## v0.20.1 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.20.0 (2026-09-30)

上下文分页 P2.5：先修 `memory.hook` 的 PREF 驱逐空转，再新增 `context.paging` 预算调用点。

- 修复 `memory.hook` 对画像段落驱逐空转：hook / paging 决策实际生效时，画像段落按实时可读条目渲染并套用同一套过滤；自我接入档案不进候选、不可驱逐；无 provider 时仍读 `profile.md`，基线输出逐字节不变。
- 修复 `profile` 只读单层目录：`private/<owner>/{prefs,bounds,commits}/YYYY/MM/` 里的分层条目现在也会进入静态画像；`context` 的实时画像路径不受影响。
- 新增 `context.paging`：仅在用户显式传 `--budget` 时调用；`memory.hook` 先过滤，`context.paging` 再排序 / 分页。`drop` 始终安全应用；`order` 仅在 `complete:true` 且候选未超过 500 时应用；候选集外文件只记 note、不进入输出。
- `context --json` 新增 `paging` 块（`status` / `provider_id` / `applied` / `dropped` / `ordered` / `truncated` / `budget` / `used` / `note`）；文本仅在 `context.paging` 实际被声明或触发时增加状态行；审计沿用 `provider-audit.jsonl`，不含记忆正文。
- provider 子进程透传 `YOTTA_LICENSE_HOME` / `YOTTA_LICENSE_KEYS_DIR` / `YOTTA_LICENSE_BASE_URL` / `YOTTA_LICENSE_SERVER_ID`，与路线 B 授权隔离环境一致。
- 协议文档升级 v1.1，新增 `context.paging` 请求 / 响应 / 回落说明。

## v0.19.0 (2026-09-28)
- 新增扩展提供方（provider）装载点：`context` 可选调用本地 provider（capability `memory.hook`），在权限过滤后的候选集内驱逐条目；BOUND / COMMIT 与身份画像不可驱逐，预算 / 去重 / 宽限仍由引擎掌控。
- 未配置 / 未授权 / 超时 / 非法输出一律 fail-open 回普通记忆；`provider.json` 非法只记状态、不阻断。
- `context --json` 输出结构化 JSON（`schema` / `hook` / `text`）；此前该参数回落为文本。
- 扩展调用只写本地审计元数据（`provider-audit.jsonl`：capability / 状态 / 耗时 / 字节数），不含 payload 正文。

## v0.18.1 (2026-09-27)

第二波 P2：蒸馏溯源链 + 分类型提取 / 相对日期绝对化 + 巩固标记 / 重复踩坑 → 规则晋升建议 / 权威顺序与写入纪律（文档）。

**蒸馏溯源链与分类型提取（A8）**

- `distill` 新增分类型提取清单：事件 / 教训 / 待办 / 成长 / 规则边界 / 其他；每条提取项带 `[溯源: 文件#L<a>-L<b>]`，要素缺失显式写「未记录」。
- 新增质量指标（只报本次实测，不承诺压缩倍数 / 语义保真）：实测压缩比 / 条目覆盖率 / 溯源覆盖率 / 要素提取率。
- 新增跳过与边界清单：空文件、BOM、非 UTF-8、无 frontmatter、单行超长截断。
- 修复：`distill --json` 现在真正输出结构化报告（此前帮助已声明但只打印文本）；帮助补 `--owner` / `--out`。

**日期绝对化与巩固标记（A9）**

- `consolidate` 摘要正文按条目 `created`（缺则 `updated`）把「昨天 / 上周 / 本月 / 今年」等写成绝对日期（如 `昨天（2026-01-09）`）；「最近 / 前几天 / 刚才」等模糊词不归一；无基准日期则跳过。
- 归档副本追加一行 `<!-- yotta-memory: consolidated to … -->` 巩固标记；`--undo` 剥离标记并还原原始内容；标记失败不阻断批次，报告与审计记录 `markers_written` / `marker_errors`。
- `consolidate --json` 报告新增 `date_normalized` / `markers_written` / `marker_errors`，propose 报告带每组 `date_normalized_preview`。

**规则晋升建议（A10）**

- 新增 `maintain --rules`（默认维护报告附带非空结果）：同组 ≥ `maintain_rule_min_hits`（默认 3）时输出组键 / 时间跨度 / 代表条目 / `remember BOUND` 建议命令；只读，不自动写规则、不改权重。
- 分组键优先级：`pattern-key:` 标签 → 元习 `yotta-learn: <area>` + `[<category>]` → 领域标签 → subject 指纹；跨 owner 私密条目 fail-closed。
- MCP `maintain` 新增只读入参 `rules`。
- 元习联动：元忆不读 `.learnings/`、不调元习命令；分工与 pattern-key 对齐口径写入 SKILL / USER_GUIDE。

**权威顺序与写入纪律（A12 / A13，文档）**

- SKILL「记忆守则」新增 §10：冲突权威顺序 6 层、内嵌指令不可信、写入纪律三条；USER_GUIDE / protocol / FAQ 同步。
- 边界：不新增 scan 检测规则（YTM-PIJ 系列已覆盖注入检测）。

## v0.18.0 (2026-09-26)

第二波 P1：命中打点与容量水位 / consolidate 提案闸门 / 规模分级 / 上下文压缩审计。

**命中打点与容量水位（A3）**

- `recall` / `explain` / `feedback --useful` / `context` 记录本地命中元数据：`hit_days`（按天计数，默认保留 90 天，窗口可配）与 `hit_queries`（`sha256(query)` 前 8 位指纹计数，默认最多 12 槽，不保存查询原文）；字段随记忆文件一起加密 / 备份 / 导出。
- 开关：`config set usage_enabled false` 全局关闭；`recall` / `explain` / `context` 支持 `--no-usage` 单次关闭。只读命令（`bench` / `doctor` / `scan` / `baseline` / `export` / `context --audit`）不写打点；跨 owner 私密条目不写（fail-closed）。
- 新 `maintain --capacity [--json]`：只读报告水位（条目 / 记忆文件字节 / 索引字节 / 单目录最大文件数 / 冷启动）、30 / 90 天活跃度、LRU 与 LFU 淘汰候选、晋升建议（90 天命中 ≥ 3 且不同查询 ≥ 3，只打印建议命令）。淘汰候选排除冷却期（默认 30 天）与常青条目（immutable / BOUND / `evergreen` / `pinned`）。
- `archive` 尊重冷却期与 `evergreen` / `pinned` 标签；`--force` 显式关闭这两项豁免（immutable 与 BOUND 始终豁免）。
- 修复：加密库私密条目命中后，owner 加密索引在同一次调用内同步，不再滞等到 `reindex`。

**consolidate 授权闸门（A5）**

- `consolidate` 默认等价 `--propose`：输出结构化候选报告（候选统计 / 分组 / 摘要预览 / 归档目标 / 保留期 / 回滚命令），`--json` 供自动化读取；不写盘。
- `--apply` 新增确认门：交互式需输入「X 组 / Y 条」确认串；非交互必须显式 `--yes`，否则拒绝退出（exit 2）。破坏性闸门（doctor + 独立备份 + 事务快照）与 `--undo <batch>` 回滚不变。
- 首次启用时显示一次数据生命周期说明（保留期 + 检查 / 纠正 / 导出 / 停用 / 删除），按 `.archive` 审计记录判定，不新建标记文件；AI 不得代替用户执行 `--apply`。

**规模与健康度分级（A6）**

- `doctor` 规模体检新增四个 `scale_info_*` 阈值键与 `metrics[]` 逐项 `ok | info | warning`；文本增加健康度行（正常 / 提示 / 告警 + 最高项）。
- `doctor.ok` 语义不变（只看 critical）：info / warning 都不锁定破坏性写入；`maintain --capacity` 复用同一套阈值与分级。

**context --audit（A7）**

- `context --audit [--from <文件|->] [--json] [--gate N]`：把被压缩掉的内容（宿主摘要或丢弃段落）喂进来，逐条核对是否已落盘；输出已落盘 / 未落盘 / 无法判定与 `remember` 建议命令；`--gate N` 在未落盘条数超过门槛时 exit 1。
- 无 `--from` 时审计当前上下文包的 dropped 清单（duplicate / budget_exceeded），给出仍可召回的 `recall` 命令。全程只读：不复制输入、不自动补写、不写打点；只匹配当前身份可读条目。

**MCP 只读 / 预演面**

- MCP 工具面同步本批能力，但只补「只读 + 预演」子集：`archive` 新增 `dryRun`（只预览、零写入）；`maintain` 新增 `capacity`（只读容量水位报告）；`context` 新增 `audit` + `auditText` + `gate`（内联文本审计，**不接受文件路径**，也不读 stdin —— stdio MCP 的 fd 0 是协议流）；新增 `consolidate` 工具，只出 propose 报告。
- 破坏性覆盖留在本机 CLI，MCP fail-closed：`archive --force` 不入 MCP（透传会被忽略）；`consolidate` 的 `--apply` / `--undo` / `--batches` 在 MCP 侧显式拒绝并提示改走 CLI（A5 闸门口径：AI 不得代替用户执行 `--apply`）。
- 这样 MCP-first 宿主（只接 MCP 的客户端）也能用上容量水位 / 压缩审计 / 归档预演与压缩候选报告，同时不放开常青豁免与确认闸门。

**修正（2026-09-26 验收回执）**

- `archive --dry-run` 此前被静默吞掉（帮助声明「只预览归档结果」，`archiveCore` 却整段没读 `opts.dryRun`，照常移文件 + 建整库快照 + 写审计）。现在补齐预演分支：只打印将归档清单（文件 / 类型 / 天龄 / 效用 / subject）与跳过统计，**不动文件、不建事务快照、不写审计、不改索引**，输出以「预览（未改动）」开头；CLI 与 MCP（`dryRun`）共用同一条路径。
- 顺带收口同批两处：`archive` 在没有候选时不再创建整库事务快照（无写入就不建快照）；`archive` 支持 `--json` 输出结构化报告（`mode / candidates / archived / skipped`，此前 `--json` 也被静默吞掉）；`archive` 被破坏性闸门拒绝时明确 exit 2。
- `context --audit` 的 `remember` 建议命令 subject 改为在非标点边界截断（此前硬截 20 字符会切在「（」中间）。

**测试**

- 新增 `test/usage-hits.test.js` / `test/capacity-report.test.js` / `test/consolidate-propose.test.js` / `test/doctor-scale-levels.test.js` / `test/context-audit.test.js` / `test/archive-preview.test.js` / `test/mcp-v018-readonly-surface.test.js`；`npm test` 275 / 275 通过，帮助快照同步重算（`5bde7ffa…`）。

## v0.17.4 (2026-09-26)

新增 `rename`：给单条记忆改名，用来消除「平铺 / 分层同序号」冲突。

- 用法：`yotta-memory rename <记忆 id> <新文件名> [--dry-run] [--reason <原因>] [--unsafe]`；新文件名需形如 `YYYY-MM-DD-NNNN.md`。
- 身份键 = 类型 + owner + 文件名：目标名会**跨平铺 / 分层**检查同身份占用，占用即拒绝；目标文件已存在也拒绝覆盖（fail-closed）。
- 写入闸门复用 `destructiveGuardCore`（doctor + 独立备份 + 事务快照）；改名后重建索引并写 `action: rename` 审计（含目标路径与原因）。
- 权限：走 `checkOwnerWritable`，其它 owner 的私密记忆默认拒绝，需 `--unsafe` 显式授权。
- `--dry-run` 只预览、零写入。命令仅 CLI 提供（写操作不进 MCP 工具面，工具数不变）。
- 回归：新增 `test/rename.test.js` 5 项（冲突消除 + 跨布局占用拒绝 + 非法名 / 已存在拒绝 + owner 门 + dry-run 零写入）。

## v0.17.3 (2026-09-26)

帮助可读性微调：顶层 `--help` 的每个选项去掉逐项重复的「做什么：」前缀，直接写说明正文；
「什么时候用：」与「注意：」保留不变。仅影响帮助文案输出，命令行为、参数与退出码零变化。

## v0.17.2 (2026-09-25)

安全修复：私密维护的 owner 门（explain fail-closed / archive / maintain 跨 owner 跳过）。

- 背景：`explain` 对其它 owner 的私密条目照样输出 subject + statement（只加一句「仅元数据」注释）；`archive` / `maintain` 遍历全部 owner，任何身份都能归档 / 遗忘别人的私密记忆（ClawHub T05 High）。
- 修复：`explain` 命中跨 owner 时直接拒绝（不回显正文）；`archive` / `maintain` 逐条走 `checkOwnerWritable`，跨 owner（含未声明身份）私密条目一律跳过并在输出里说明数量与补救方式；CLI 与 MCP 两条路径都传入调用方身份。
- 边界：公共明文 FACT 不受影响；加密库里无对应密钥的条目本就不可解，本次把明文库与写路径补齐。
- 安装器加固：拒绝对符号链接目标写入、不做整目录删除。
- 回归：新增 `test/owner-gate.test.js` 5 项，`npm test` 232/232 通过。

**view 删除身份的错误提示修复**

- `view` 的 AI 列表点击「删除」后，如果确认 ID 输入错误，前端现在会立即提示「ID 不匹配，请输入完整 agent ID：<id>」；用户取消仍保持静默，不会误触删除。
- 回归：`test/identity-remove.test.js` 新增 1 项，确认错误 ID 有可见提示；后端 400 校验与破坏性闸门保持不变。

## v0.17.1 (2026-09-25)

## v0.17.0 (2026-09-25)

**帮助改造（A）**

- 顶层 `--help` 重排为四段（核心记忆 / 身份与画像 / 加密与安全 / 平台与服务），逐条列出命令、子命令路径与全部选项；每个选项给出「做什么 / 什么时候用 / 注意」三段中文说明，风险选项（`--no-encrypt` / `--unsafe` / `--apply` / `--force` / `--purge` / `--allow-same-volume`）必须带「注意」。
- 帮助文案收敛到单一真源 `HELP_MODEL`（`usage()` 只做渲染），解析器侧 `CLI_FLAG_OPTS` / `CLI_VALUE_OPTS` 上移为模块级名单；新增 `test/help-coverage.test.js` 四件护栏（命令 / 子命令覆盖、帮助 ↔ 解析器双向一致、风险项必须带注意、`main()` 布尔字面量必须登记）+ 渲染快照，禁止两处手写文案漂移。

**规模三项（B1 写入分层 + B2 规模体检）**

- 记忆文件新写入按年/月分层：公共 `facts/<yyyy>/<mm>/`，私密 `private/<owner>/<type>/<yyyy>/<mm>/`。读取与索引递归兼容新旧两种布局，v0.16 及更早的平铺文件保持原位、不自动迁移。
- 去重与序号跨布局统一：序号在「类型目录 + owner」内全局唯一（平铺与分层不重复编号）；写入去重只扫当前年/月、同年平铺文件与类型根，避免大库每次写入全量遍历（跨月重复由既有的 `maintain --dedup` 与 `consolidate` 处理）。
- 归档保留分层：`archive` / `maintain --apply --purge` / `consolidate` 移入 `.archive/` 时按原年/月路径落位，不同月份的同名文件不再互相覆盖；旧平铺文件仍落到归档根。
- 明文库转加密（`migrate`）递归处理年/月子目录，不再漏掉分层私密文件。
- 平铺 / 分层同序号：条目身份 = 类型 + owner + 文件名（`YYYY-MM-DD-NNNN.md`），与存放位置无关；公共 FACT 的 owner 取自 frontmatter，不同 owner 的同序号文件不误报。内容摘要相同 → 只索引一次；内容不同 → 两份都保留可读，`doctor` 新增 `checks.layout` 与路径告警；新写入永不复用已占用的序号。加密条目在当前密钥不可用时按「待核」处理，不静默丢弃任何一份。
- `doctor` 新增规模体检：记忆条数 / 单目录最大文件数 / 索引总体积 / 索引冷启动耗时（多次取中位数）；阈值走 `config set scale_warn_entries` / `scale_warn_files_per_dir` / `scale_warn_index_bytes` / `scale_warn_cold_start_ms`，超阈值进 `checks.scale.warnings` 并计入 doctor warning，只读、不锁定破坏性写入。
- 回归：`test/scale-layout.test.js` 8 项（新写入分层 / 跨布局序号 / 新旧混读 / 导出导入往返 / 私密归属 / 归档路径 / doctor 规模正常与告警）。
- 升级提示：升到 0.17.0 后请用 **0.17.0 引擎**执行一次 `yotta-memory reindex`。0.16.7 及更早引擎不识别年/月分层目录，旧引擎重建索引会漏掉分层条目；本批去重只影响索引与告警，不自动删除、不移动、不覆盖磁盘文件。

**索引按需加载 + 基准评测（B3 + A1）**

- 索引按年份懒加载：新增 `loadIndexFor(root, { years })`；命中分片 manifest（`index-<year>.json`）时只读取指定年份的分片文件，`recall --year <yyyy>` / `context --year <yyyy>` 走该路径（可重复传多次），不传年份维持全量读取、既有行为零变化。命中后的访问计数回写（`touchIndex`）同样只碰命中年份的分片，其它年份分片逐字节不变。平铺索引（未达 5000 条分片阈值）无法少读文件，按条目年份过滤；`--year` 只接受四位年份，非法值给中文提示并 exit 2。
- 新增 `bench` 可复算基准评测：默认按库内条目做确定性抽样（固定种子，最多 20 条查询）生成基线评测集，也可用 `--evalset <文件>` 指定评测集 v1（`{ "version": 1, "queries": [ { "query": "...", "expect": ["<记忆 id>"] } ] }`，记忆 id 可写相对路径或文件名）。
- 指标 = `Recall@k` / `MRR` / `nDCG@k` / `HitRate` + 固定种子 bootstrap 95% 置信区间；报告写明库指纹（条数 + 索引 SHA-256 + 评测集 SHA-256）与参数，默认不含墙钟时间——同库 + 同评测集 + 同参数必须同输出。`--ablate` 给关键词 / 语义 × 融合（0.65 语义 + 0.35 效用）/ 纯分四组消融；`--gate <指标>=<数值>` 供 CI（不达标 exit 1，指标可选 `recall` / `mrr` / `ndcg` / `hit`）；`--timing` 显式附带检索耗时 p50 / p95（带上后报告标记为不可逐字节复算）。
- `bench` 全程只读：索引缺失或版本过旧时提示先 `reindex`（不代建索引）、不写访问计数、不调用外部 embedding 插件；评测集非法（版本 / 空 query / 空 expect / 非法 JSON / 文件不存在）分别给中文修复建议并 exit 2；对当前身份不可读的记忆计入 `corpus.denied` 并跳过。
- 检索打分与排序抽成共享原语 `scoreCandidates` / `rankHits`，`recall` 与 `bench` 走同一套逻辑，避免「评测口径」与真实检索漂移；recall 自身行为逐字节不变。
- 帮助与回归：`--help` 新增 `bench` 命令与 `--year` / `--evalset` / `--k` / `--seed` / `--bootstrap` / `--ablate` / `--gate` / `--timing` 逐项中文说明；新增 `test/index-lazy-year.test.js` 5 项（分片读取集合 / 无年份全量一致 / 平铺过滤 / recallCore 年份 / CLI `--year` 与非法年份）+ `test/bench.test.js` 8 项（指标手算 / 复算与只读 / 索引指纹 / 门禁 / 消融 / 评测集与索引校验 / `--out` / 文本与 `--timing`）；全量 `npm test` 196/196 PASS（0.16.7 基线 171）。

**恢复探针 + 记忆库安全扫描（A2 + A4）**

- 新增恢复 / 迁移基线探针：`doctor --baseline [--against <库路径>] [--template <文件>]`，`backup drill <id> --probe [--against <库路径>]`。六类固定探针 = ① 身份（`agents.json` / `iam` 在位）② 近期（最近条目可召回）③ 仅源库独有（`--against` 差集条目必须已在目标库）④ CJK（中文条目可召回）⑤ 操作规则（`BOUND` 类可读）⑥ owner 范围（各 owner 计数 + 无法读取文件清单）；任何一项失败都会列出缺失清单并以非零状态退出（`doctor` exit 2、`drill` 判失败）。探针内容由确定性抽样或用户模板生成，**不硬编码任何具体记忆**。
- 探针全程只读：直接读记忆文件（不依赖可能过期的索引）、不重建索引、不写访问计数、不调用外部 embedding。`doctor --baseline` 的探针结果进 `checks.baseline`（`probes` / `counts` / `unreadable` / `ok`），不带 `--baseline` 时 `doctor` 既有语义与输出不变；`backup drill` 不带 `--probe` 时行为与旧版一致（成功返回新增 `probes: null`）。
- 探针模板 v1（`--template <文件>`）只加严判定、不放宽：`{ "version": 1, "expect_owners": [], "expect_min_entries": 0, "expect_types": { "BOUND": 1 }, "queries": [ { "id": "...", "query": "...", "expect": ["<记忆 id>"] } ] }`；模板文件不存在 / 非法 JSON / 版本不支持 / 类型或条数非法都给出中文修复建议并 exit 2。
- 条目身份键与布局无关（`类型/owner/文件名`），旧平铺 `facts/x.md` 与新年/月分层指向同一条记忆时不会误报「缺失」，因此 `--against` 可直接用于旧库 → 新库的迁移验收。
- 新增 `scan` 记忆库安全扫描：`yotta-memory scan [--path <目录>] [--gate <安全级别>] [--quarantine --yes] [--restore] [--id <批次>] [--json]`。七类检测 = 恶意指令 / Prompt 注入 / 凭证泄漏 / 数据外泄 / 护栏绕过 / 行为操纵 / 权限提升；五级 `safe → low → medium → high → critical`；每条命中给 `file:line` 证据与规则出处。
- 扫描默认**只报告**：不改写任何文件、不自动隔离、不自动删除、零网络零依赖。`--gate` 命中该级别及以上 exit 1（`--gate safe` 表示任何命中都不允许），非法级别 exit 2；`--path` 可指向另一个记忆库或导出目录（递归扫 `.md` / `.md.enc`，跳过 `.git` / `node_modules` / 隔离目录）。`.md.enc` 后缀但内容其实是明文的文件（历史恢复残留）不会被当成密文跳过，按文本扫描并计入 `summary.mislabelled`；每条命中除 `file:line` 外给出命中片段前后各 40 字符与命中原文（凭证类打码），长行也能一眼看到命中在哪。
- `scan --quarantine` 需要显式确认（`--yes` 或交互 `y/N`；非交互环境未确认时 exit 2 且不改文件）：先把原文件逐字节备份到 `.memory-scan/quarantine/<批次>/` 并写 `manifest.json`，再把命中行替换为 `[已隔离: <规则> <类别>]`；`scan --restore [--id <批次>]` 还原最近（或指定）批次，批次已还原则拒绝重复还原。加密条目（`.md.enc`）在无授权密钥时不扫描，只计入 `summary.encrypted`。`scan` 是库主人的维护命令，会读整库文件（含其它 owner 的私密目录）：智能体不应用它查看其它智能体的私密内容，跨 owner 扫描前先取得用户授权。
- 凭证类命中的片段一律打码（`[已打码]`），报告与 JSON 都不会回显密钥原文；规则词表不另起一套：每条规则的 `ref` 指向家族规则表的原始规则 id（`PIJ-xxx@yotta-verify` / `github@yotta-secret` / `DEX-001@yotta-security-audit` / `CMD-*@yotta-guardian`），`test/memory-scan.test.js` 在源码仓库内逐条回查这些规则 id 在对应技能里是否仍存在（发布产物内自动跳过该用例）。分工口径：元钥扫源码仓库、元信扫技能包、元忆扫记忆库。
- 帮助与回归：`--help` 新增 `doctor --baseline` / `--against` / `--template`、`backup drill --probe` 与 `scan` 的逐项中文说明（风险项 `--quarantine` / `--restore` / `--yes` 均带「注意」）；新增 `test/baseline-probe.test.js` 7 项（六类探针 / 身份缺失变红 / 差集缺失清单 / 模板期望 / 模板校验 / 只读 / `drill --probe`）+ `test/memory-scan.test.js` 9 项（七类命中 / 证据行号与出处 / 凭据打码 / 门禁 / 加密跳过与 `--path` / 只读 / 隔离与还原 / 规则出处回查）；全量 `npm test` 212/212 PASS（0.16.7 基线 171 + S2–S5 新增 41）。

**彻底删除 AI 身份与私密记忆（identity remove）**

- 新增 `yotta-memory identity remove <id> [--dry-run] [--yes] [--keep-memories] [--keep-identity]`，并在用户查看平台 `view` 的 AI 列表里加「删除」按钮：某个 AI 不再使用时，一次把它清干净——① `agents.json` 身份登记 ② `keys/<id>.key.enc`（owner 密钥与恢复侧文件）③ `keys/bindings/<id>.key.agent` 授权绑定 ④ `keys/pending/<id>.key` 待领取 key ⑤ `keys/cache/<id>.key` 明文缓存 ⑥ `private/<id>/` 整个目录（私密记忆 + owner 索引 + profile / distill）⑦ `.server/tokens.json` 里的 token ⑧ `grants.json` 里的授权引用 ⑨ 重建索引并写审计。**公共明文 FACT 不删**（共享事实），其它 owner 零影响。
- 语义：**真删**（不可恢复）。删掉 owner 密钥后，该 owner 现存密文在密码学上也不可再解；需要保留记忆时用 `--keep-memories`（只注销身份与授权），需要保留登记时用 `--keep-identity`（只清私密记忆与授权）。`--dry-run` 先列清单且只读。
- 权限边界：**只能由用户本人执行**。加密库要求提供主口令（能解开任一 owner key 或恢复材料）或 `--recovery-key`；明文库没有可校验的用户凭据，要求显式 `--agent user`；`view` 里已用主口令解锁的会话视为用户本人。AI 用自身身份调用一律拒绝——AI 不得删除自己或别的 AI 的身份。
- 破坏性闸门：走既有 `doctor` + 独立备份 + 事务快照口径（未配置独立备份目录、或 doctor 严重项时直接拒绝），执行前写 `transaction_start`、执行后写 `identity_remove` 审计（含快照 id、授权方式、删除清单）。CLI 交互需输入完整 id 确认，或显式 `--yes`；`view` 侧要求确认串等于完整 agent ID。
- 回归：新增 `test/identity-remove.test.js` 9 项（九步清单真删 / 公共明文与其它 owner 零变化 / `--dry-run` 只读 / 拒绝 AI 身份 / 加密库口令校验 / 明文库用户身份与备份闸门 / 幂等 / 两个保留开关 / view 端点确认串与闸门）；全量 `npm test` 221/221 PASS。
- 回归：新增 `test/layout-collision.test.js` 5 项（相同摘要去重 / 冲突双保留与路径告警 / 不同日期不误报 / 不同 owner 不误报 / 加密待核不丢弃）；全量 `npm test` 226/226 PASS。

## v0.16.7 (2026-09-23)

**迁移口令安全 + view 根指纹复用校验**

- 明文库迁移文档与 CLI `--help` 不再给出可复制的中文占位符管道命令；推荐交互式输入，非 ASCII 口令明确禁止使用 Windows 管道，自动化改用 `YOTTA_MEMORY_PASS` + ASCII 口令。
- `migrate` 后 `view` 报「口令错误」时，文档给出用恢复钥匙 `reset-password` 的安全恢复路径。
- `view /api/status` 新增 memory-home `rootId`；`view` 复用已在运行的服务前必须校验根指纹，跨 memory_home 或旧版无指纹服务会拒绝复用并提示关闭进程或换端口。
- 新增回归：`test/view-root-guard.test.js`（同库复用、跨库拒绝、旧版无指纹拒绝）+ `test/migration-guidance.test.js`（文档安全命令与 CLI help 检查）。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / CHANGELOG / 引擎 VERSION = 0.16.7。

## v0.16.6 (2026-09-23)

**插件 MCP 身份启动器（Agent Plugin 开箱可用）**

- 新增 `bin/plugin-mcp.js`：宿主只替换 `${PLUGIN_ROOT}`、不替换 `${AGENT_ID}` / `${AGENT_KEY_FILE}` 时，按「宿主替换值 → 环境变量 → `PLUGIN_DATA/identity.json` → 未授权可执行指引」解析身份。
- 未装配身份时不再把字面量占位符传给引擎：以未授权模式启动（公共 FACT 可读、私密 fail-closed），并输出含 `key claim` 与 `identity.json` 的可执行指引。
- `key claim <id> --plugin-data <PLUGIN_DATA>`：一条命令同时写入插件 key 与 `identity.json`；与 `--to` / `--agent-key-file` 互斥校验。
- 插件 `mcp.json` 入口由 `yotta-memory.js` 改为 `plugin-mcp.js`；宿主替换占位符的旧路径继续有效。
- 回归：`test/plugin-mcp-launcher.test.js`（身份优先级 / 无身份指引）+ `test/plugin-claim-binding.test.js`（claim → 插件身份 → 私密读取端到端）；全量 `npm test` 167/167 PASS。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / CHANGELOG / 引擎 VERSION = 0.16.6。

## v0.16.5 (2026-09-22)

**doctor --json 稳定契约补齐**

- `doctor --json` 顶层新增 `schemaVersion: 1`、`encryption: boolean`、`migration_required: [{ agent, reason }]`。
- 保留 `checks`、`warnings`、`identity`、`text` 等既有字段；旧消费方无需改动。
- `migrationRequiredInfo()` 同步返回逐 owner 的 `entries`，供 CLI JSON 与宿主契约共用。
- 回归覆盖明文库空迁移数组、加密库未绑定 owner 迁移条目及 warning 兼容。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / CHANGELOG / 引擎 VERSION = 0.16.5。

## v0.16.4 (2026-09-22)

**agent-key 缺文件提示范围修复**

- 主入口不再对 `--agent-key-file` 不存在无条件输出全局 `stderr` 警告；`migrate`、`doctor`、`config` 等公共 / 维护命令保持安静。
- 未授权提示下沉到真实私密访问边界：私密读写仍 fail-closed，并明确给出缺失文件、`view` / `key bind`、`key status` / `key claim` 的可操作步骤。
- `whoami --json`、`doctor --json`、`config get --json` 新增 `identity.mode` / `identity.agentKeyStatus` / `identity.source` / `identity.keyFile` / `identity.action`，默认人类输出不加全局警告。
- 回归覆盖公共命令安静、私密命令 fail-closed、JSON 身份状态三组行为；全量 `npm test` 158/158 PASS。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / CHANGELOG / 引擎 VERSION = 0.16.4。

## v0.16.3 (2026-09-22)

**迁移最短路径与授权引导修复**

- `migrate` 成功输出不再只提示 `key bind`：现在明确输出“授权二选一（等价）”——推荐 `yotta-memory view` 页面授权，高级 CLI 方式为 `yotta-memory key bind <id>`，随后 AI 统一执行 `key status` → `key claim`。
- `SKILL.md`、`USER_GUIDE.md`、`references/faq.md`、中英 README 统一加入明文库第一次转加密命令（v0.16.7 已废弃原中文占位符管道写法）；后续补充交互终端 / PowerShell / cmd / 管道等口令传递方式和一个统一报错对照。
- 修正迁移后的索引顺序：必须 **授权 → `key claim` → 带 `--agent-key-file` 执行 `reindex` → `recall` 验证**；`migrate` 在没有 agent_key 时无法建立每 owner 加密索引。MCP 自检同时要求配置带 `--agent-key-file`。
- `--help` 的 `migrate` 行同步给出首次迁移命令与两条等价授权路径。
- 新增 `test/migration-guidance.test.js`，锁定迁移命令、`view` / `key bind` 等价关系和 CLI 帮助口径。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / CHANGELOG / 引擎 VERSION = 0.16.3。

## v0.16.2 (2026-09-21)

**首启修复：空加密库可解锁、非 TTY 可自举、缺 key 降级未授权**

- 修复空加密库 `view` 授权死锁：`/api/unlock` 在无 owner key 时用恢复钥匙校验主口令，空库可进入授权平台；无 owner 时页面提示先执行 `yotta-memory iam <id>`。
- 非 TTY 环境不再静默「已取消」：`init --encrypt` / `migrate` / `reset-password` / `key bind` 给出可操作错误；新增 `--password-stdin`（管道读口令，不进 argv）。
- `--agent-key-file` 指向不存在的文件时降级为未授权模式：公共 FACT 可读，私密操作 fail-closed 并提示 `key bind`；文件存在但为空 / 不可读仍报错。
- 空加密库 `iam` 先登记身份、不因自我档案写失败而退出；授权后带 `--agent-key-file` 重新执行 `iam --force` 写入加密档案。
- `migrate` 支持空明文库直接启用加密（创建 salt + recovery，不创建 owner key），迁移后提示 `key bind`。
- 新增 `--recovery-key-out <文件>`：恢复钥匙写文件（`init` / `migrate`），不在 stdout 打印完整钥匙，适配 GUI 宿主 stdout 不可捕获场景。
- `init --attach` / `init --no-encrypt` 明确输出当前模式（明文 / 加密）与下一步。
- `isExistingStore` 不再把 `agents.json` 单独视为现有库；`key list` 合并 `keys/*.key.enc`，显示仅有钥、尚未写记忆的 owner。
- `doctor` 对全新空库的缺失 index / agents 降为 info（不再误报）；只有私密数据、没有公共 FACT 的库不再误报公共索引缺失；输出 agent home 发现规则与 `YOTTA_MEMORY_AGENT_HOME` 提示。
- `view` 启动前做端口健康检查：已在运行则复用并打印 URL；端口被占用给明确错误；`server.on('error')` 不再抛未处理异常。
- 明文库 `view` 提示改写 stdout，GUI 宿主可感知。
- 新增 `test/firstboot-0.16.2.test.js`（15 项首启回归）；全量 `npm test` 148/148 PASS。
- 版本对齐：package.json / SKILL.md frontmatter / skill-manifest.json / CHANGELOG / 引擎 VERSION = 0.16.2。

## v0.16.1 (2026-09-19)

维护性重发（无功能变更）：

- 发布包清理：平台分发副本不再包含误打包的历史 tarball（构建脚本已排除 `*.tgz` 等压缩包并新增归档校验）。
- 检索文案更新：分发副本的 summary / description 使用连写关键词（AI记忆系统 / 长期记忆 / 永久记忆 / 记忆引擎），并为该成果增加构建守卫。

## v0.16.0 (2026-09-18, M1 身份模型候选)

**身份模型：请求边界即身份边界**

- HTTP / 远程 MCP 身份只从请求头读取：`Authorization: Bearer <token>` + `X-Agent-Id` + `X-Agent-Key`；鉴权模式下缺少任一身份头直接返回 401，不再进入工具调用。
- stdio MCP 身份只从显式启动参数读取：`serve --stdio --agent-id <id> --agent-key-file <path>`；不再读取 `YOTTA_AGENT_ID` / `YOTTA_MEMORY_AGENT_KEY` / `YOTTA_MEMORY_TRUST_ENV_AGENT`，并拒绝把裸 key 放进 `--agent-key` 命令行。
- 删除身份环境变量解析；启动 HTTP / stdio MCP 时检测到旧身份 env 会以 `[YTM_IDENTITY_ENV_REMOVED]` 明确拒绝，并给出请求头 / 显式参数迁移指引，不静默降级。
- 增加 per-call identity context，HTTP 与 stdio 的并发调用不再共享可变的进程级身份；新增三 agent 并发私密上下文隔离回归。
- CLI 仍是 `--agent <id>` + `--agent-key` / `--agent-key-file`；`--agent-id` 与 `--agent` 同时出现且不一致时拒绝启动。
- **运行时稳定入口（M2）**：新增 `runtime list` / `runtime install <tarball|版本> [--from-current] [--force]` / `runtime use <版本> [--restart]` / `runtime rollback [--restart]` / `runtime status`；`runtime.json` 记录 current / previous / 安装时间 / tree hash，`<runtimeRoot>/current` 作为 stable launcher。
- `lan enable` 与备份调度先准备 runtime current，只登记 `<runtimeRoot>/current/bin/yotta-memory.js`；`runtime use --restart` 尝试重启受管 server，失败时把 current 切回旧版本。
- **运行时诊断与握手（M3）**：新增 `doctor --runtime [--json] [--mcp-config <文件>] [--skill-dir <目录>]`，检查 CLI / current / runtime.json / MCP 配置 / 运行中 server / 技能副本 / 身份模式漂移，并为每项漂移输出实际版本、期望版本、修复命令和是否阻断。
- MCP `initialize` 与 `server/discover` 的 `serverInfo` 新增 `runtimePath` / `identityMode` / `toolProfile`，宿主可直接读取实际执行的运行时路径、身份模式和工具分组。
- 本条目为 0.16.0 的 M1-M3 候选；完成后才进入发布闸门。

## v0.15.0 (2026-09-17)

**MCP 工具分组：降低常驻工具面**

- `serve` 新增 `--tools core|full`：`core` 暴露 `context / recall / search / remember`，`full` 保留现有 16 个工具；未指定时默认 `full`，保持向后兼容。
- `tools/list` 按当前分组返回；`tools/call` 调非当前分组工具时返回可执行提示，要求切换到 `--tools full`。
- OpenCode 集成默认使用 `core`，需要在智能体运行中减少工具常驻税；完整维护能力仍可按需启动 `full`。
- 新增 `test/mcp-tool-profiles.test.js`，覆盖 core 列表、legacy / modern 分组一致性与越组调用提示。
- 存储格式、AES-256-GCM、owner 隔离、agent_key 与权限判定不变。

## v0.14.0 (2026-09-17)

**上下文编排：让 AI 越用越懂用户；合并 O2 CLI 诊断修复**

- `context` 新增「长期理解摘要」段：优先加载 `consolidate` 生成的周期摘要（`source=consolidate` / tags `consolidate` + `summary`），只注入 subject + statement，原文细节继续用 `recall` 下钻。
- `context` 新增「近期走廊」段：按 `updated / created` 倒序取样，不受 utility 排序影响，让最近发生的事稳定进入开工上下文。
- 原有近期记忆改为「近期高价值记忆（补位）」：保留 importance + utility 融合排序，并与摘要、focus、走廊按文件去重；摘要、身份、铁律、画像、边界、承诺与会话闭环契约不受 `--budget` 截断。
- `context` 末尾新增「本会话闭环契约」：开工加载、进行中信号即 `remember --verify`、收工前复盘并检查 COMMIT / 会话小结是否落盘。
- SKILL / protocol / USER_GUIDE / README 中英同步说明摘要优先、近期走廊、会话闭环与 `--budget` 语义。
- 合并 O2 `0.13.3` CLI 诊断候选：非受信 ambient `YOTTA_AGENT_ID` 不再参与身份冲突判定，显式 `--agent` 优先；只有 `YOTTA_MEMORY_TRUST_ENV_AGENT=1` 时才接受环境身份。
- `key status` / `key claim` 统一 AI_HOME 解析：显式 `--to` / `--agent-key-file` > `YOTTA_MEMORY_AGENT_HOME` / `YOTTA_MEMORY_AGENT_KEY_FILE` > 宿主默认（Codex `$CODEX_HOME` 或 `~/.codex`；OpenCode `$XDG_CONFIG_HOME/opencode`；通用 `~/.<agent_id>`）> 文件名 `.yotta-memory-agent-key`；`key status` 输出 `checked` 与实际发现规则。
- 顶层 usage 明确 `remember <type> <subject> <statement>` 与 `recall [关键词]`；`--query`、remember `--type` 等位置参数误用给出专门提示。
- 新增 `test/context-cognition.test.js` 与 `test/cli-diagnostics.test.js`；合并后全量 `npm test` 108/108 PASS。
- 不新增存储格式、不改变 AES-256-GCM、owner 隔离、agent_key 与权限判定；`consolidate` / `profile` / `distill` 语义保持兼容。

## v0.13.2 (2026-09-16)

**安全修复：调用者认证 + agent_key 绑定**

- 私密操作不再把 owner ID 当身份：`whoami` / `context` / `profile` / `remember` / `recall` 需要显式 `--agent <id>` 或受信任的 MCP 环境身份。
- 新增 `agent_key` capability：`key bind <id>` 生成并只展示一次 agent_key；owner key 由 `keys/bindings/<id>.key.agent` 使用 agent_key 包裹。
- 删除对 `keys/cache/<id>.key` 明文 owner key 缓存的加载路径；legacy cache 只提示，不参与解密。
- MCP 必须同时配置 `YOTTA_AGENT_ID` + `YOTTA_MEMORY_AGENT_KEY` + `YOTTA_MEMORY_TRUST_ENV_AGENT=1`；普通 shell 的 `YOTTA_AGENT_ID` 默认不可信。
- 新增身份冲突、无 agent_key、错误 agent_key、冒充他人 ID、legacy cache 不加载等对抗性回归。
- `key list` 与失败的私密操作输出 `[YTM_MIGRATION_REQUIRED]`：列出仍有私密数据且未绑定的 agent 与原因，供 AI 主动引导用户完成绑定迁移；`doctor` 同步给出提醒。仅存在 legacy cache、没有可迁移私密数据的 owner 单独提示，不进入迁移清单；授权决策仍由用户逐个确认。
- 修复明文库 `migrate` 在身份解析处的崩溃，迁移后明确提示逐 agent `key bind`（不再写明文授权缓存）。
- `view` 平台授权会一次性弹出并展示 `agent_key`，页面可复制保存；已有 binding 时返回 409 并提示先吊销，防止误换 key 打断在用的智能体。授权 / 吊销入口新增 owner ID 路径穿越校验。
- `view` / `key bind` 授权后新增临时待领取文件 `keys/pending/<id>.key`；新增 `key status <id> --to <AI_HOME>` 与 `key claim <id> --to <AI_HOME>`，AI 可将 key 原子写入 `<AI_HOME>/.yotta-memory-agent-key`，回读校验后删除 pending。pending 不入 backup / export，避免备份包夹带明文 key。
- `key revoke` 现在同时删除 binding 与 pending；私密读取不再跨操作缓存 owner key，长驻 MCP 进程在吊销后继续使用旧 key 会立即校验失败，必须由用户重新授权生成新 key。
- 授权写入改为事务式：binding 写入后若 pending 交接文件写入失败，会回滚刚写入的 binding，避免产生“已绑定但用户拿不到 key”的孤儿授权。
- 修复 MCP stdio 私密读写未使用宿主注入的 `YOTTA_MEMORY_AGENT_KEY` 的缺陷；远程 MCP 新增 `X-Agent-Key` 请求头，token 只负责连接鉴权，加密私密读写仍必须持有匹配的 agent_key。
- `key bind` / `key revoke` / `token new` / `token revoke` / MCP `callTool` 统一拒绝非法 agent ID，阻止 `..` 或路径分隔符在密钥、token 与记忆路径入口被利用。
- MCP `import` 在写入前校验私密条目 `owner`，拒绝路径穿越；`view` 平台校验 Host / Origin，并对页面与 API 响应关闭缓存、补安全响应头，阻止 DNS rebinding / 跨站请求面。
- `key bind` 与 `view` 授权在 owner key 文件缺失时会先从 `keys/<owner>.key.recovery` 恢复原 key；原 key 与恢复文件都不可用且仍有密文时拒绝新建，避免旧数据被静默变成不可解密。
- 恢复演练不再读取 legacy `keys/cache/*.key` 明文缓存；解密必须提供恢复钥匙或主口令。
- 迁移边界：重新授权由用户在 `yotta-memory view` 平台逐个完成，AI 只转达 `[YTM_MIGRATION_REQUIRED]` 与操作步骤，不代替用户执行 `migrate` / `key bind`；`view` 授权确认框同步说明该操作属于用户侧。
- 查看平台 HTML 移出内嵌字符串，改存 `assets/view.html`。
- 发布前必须通过 security review；现有加密库需执行一次 `key bind` 迁移，明文库需先迁移加密。

## v0.13.1 (2026-09-13)

- 清理发布文档与测试夹具中的本机专属盘符 / 路径示例，统一改为 `~/.yottamemory` 或占位路径。
- 修复 `forget --unsafe` 未透传到核心的缺陷，并补 CLI 回归测试；显式授权清理其它 owner 私密条目时行为与帮助文案一致。
- 发布前新增机器专属路径硬编码扫描闸门后，此类问题不允许再进入发布件。

## v0.13.0 (2026-09-13)

**P0-4.6 元忆 after_milestone 试点**：

- 新增 `skill-manifest.json`，声明 `after_milestone` / `remember_commit` / `fallback: explicit-unverified`。
- 里程碑记忆必须有真实 `file_path` 证据才允许标记 verified；缺证据或写入失败时输出 `explicit-unverified` + 一次纠偏。
- 元阁适配器回归覆盖成功与降级两条路径。

## v0.12.2 (2026-09-12)

**可靠性收口：开工 doctor + 破坏性操作前事务快照**

- 修正 `init --force` 的过期拒绝文案：明确已有记忆库的强制重建必须由完整备份与显式确认保护，当前版本不提供覆盖初始化路径。
- 新增 `yotta-memory doctor [--json]`：只读检查记忆库根目录、加密库密钥文件、公共索引、`agents.json` 与最近备份；严重异常返回非零退出码，并锁定破坏性写入。
- 新增 MCP `doctor` 工具；`context` 的开工可靠性提醒改为直接使用 doctor 结果，critical 时明确提示“破坏性写入已锁定”。
- `maintain --apply`（含 `--dedup --apply`）、`consolidate --apply`、`merge`、`archive` 与 `--purge` 在写入前自动创建新的整库事务快照；未配置独立备份目录、doctor critical 或快照失败时拒绝写入，原记忆保持不变。
- `--allow-same-volume` 仍只用于 `backup create` 的显式临时备份，不会绕过破坏性写入门；不存在 CLI 级跳过快照开关。
- 每次事务快照写入 `.archive/audit-<日期>.jsonl`（transaction / operation / snapshot 记录）；`forget` 继续只进 `.trash/`，不重复做整库快照。
- 新增 `test/reliability-doctor.test.js` 与 `test/reliability-destructive-guard.test.js`；既有 consolidate / maintain 回归补齐临时快照目录。

## v0.12.1 (2026-09-12)

安装与更新文档修复（无功能变更）：

- 明确区分两个 bin：`yotta-memory` 是引擎 CLI，`yotta-memory-install` 是技能安装器；`npx -y @yottameta/yotta-memory` 只临时运行引擎，不安装技能。
- README 中英版、USER_GUIDE、SKILL、FAQ 补全安装 / 更新命令：更新技能统一使用 `npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <name>`（或 `--dir <技能目录>`）；全局安装后可运行 `yotta-memory-install`。
- 修正 `bin/install.js` 头部注释中的错误示例，并新增 `test/docs-install-update.test.js` 防止两个 bin 的文档再次漂移。

## v0.12.0 (2026-09-12)

**可靠性基线（误删事故整改）**：

- `init` 对已有记忆库默认拒绝覆盖；新增 `--attach` 接入现有库；`--force` 也不能覆盖已有记忆库，防止初始化再次清空记忆。
- `forget` 不再物理删除，改为移动到 `.trash/<timestamp>/<原相对路径>`，并写 `audit-<date>.jsonl` 审计记录。
- 新增 `backup create / list / doctor / restore <id> --to <目录>`：备份 `facts/`、`private/`、`keys/`（排除 `keys/cache/` 授权缓存）、`agents.json`、`index.json`、`.archive/`，生成 SHA-256 清单；默认拒绝同卷备份；`restore` 默认只恢复到新目录，不覆盖正在使用的记忆库。
- 新增每日自动备份闭环：`backup volumes` 只枚举当前机器实际存在、可写、与记忆库异卷的路径；用户确认一次位置后 `backup setup` 默认启用每日备份（默认 03:30），Windows Task Scheduler / Linux systemd user timer（cron 降级）/ macOS LaunchAgent 负责无人值守，`serve` 启动与每 6 小时用幂等 `backup ensure-daily` 补跑。
- `context` 增加可靠性提醒：未配置、超过 36 小时或失败时提示；用户明确选择手动备份后不重复打扰。
- 新增 `backup drill`：恢复到隔离副本，校验 manifest、重建索引并解密一条测试私密；默认使用本机 owner 授权缓存，裸恢复可显式传恢复钥匙。
- 新增 `test/reliability-init.test.js`、`test/reliability-forget.test.js`、`test/reliability-backup.test.js`、`reliability-backup-volumes/setup/daily/schedule/context/drill`；`npm test` 覆盖既有与新增可靠性测试。

## v0.11.0 (2026-09-06)

**MCP 协议对齐最新版 2026-07-28（无状态时代）**：yotta-memory MCP（stdio + serve streamable HTTP）升级 dual-era——modern 直连（server/discover 免握手、逐请求 _meta 版本声明、resultType、-32022 版本错误、HTTP header 校验 HeaderMismatch -32020）服务新客户端；legacy（initialize 握手，protocolVersion 2025-11-25）兼容旧客户端，旧形状响应零惊扰；HTTP+SSE GET 保留为 deprecated 兼容入口。SKILL 标注「基于 MCP 最新协议 2026-07-28（向后兼容 2025-11-25 及更早握手）」。新增 test/mcp-dualera.test.js（26/26：A 层 + HTTP 层），存量测试全绿。

## v0.10.1 (2026-09-05)

发布件修复：SKILL.md frontmatter `description` 曾以 ASCII 双引号开头但未闭合
（v0.10.0 引入），严格 YAML 解析器会报 MISSING_CHAR，导致技能在 ClawHub/OpenClaw 等
平台注册被跳过。已改为无引号裸标量（内容不变）；validate-skill 新增 frontmatter 引号
闭合检查（防再犯）。版本 0.10.0 → 0.10.1。

## v0.10.0 (2026-09-02)

压缩遗忘（S1）——consolidate 周期摘要 + 近重复自动合并 + 分类型衰减 + 批次回滚。

- **新增 `consolidate`（周期摘要压缩）**：把超龄（默认 ≥180 天）+ 长期闲置（默认 ≥90 天）+ 低效用（默认 ≤0.6）的同主题旧记忆聚类成**带溯源**的周期摘要并留在活跃区，原文整体移入 `.archive/`。默认 dry-run；`--apply` 执行；`--undo <batch>` 一键回滚（幂等拒绝重复）；`--batches` 只读查批次审计。immutable / BOUND 豁免；活跃 / 高效用记忆不动；参数可调（--min-age / --min-idle / --max-utility / --min-group / --period / --type）；`--model <cmd>` 可选本地模型提炼（仅 CLI，协议同 distill）。
- **近重复自动合并（maintain --dedup 增强）**：重复组带置信度分档（≥0.85 高置信 / 0.65–0.85 建议手动 / 其余忽略）；`maintain --dedup --apply` 自动合并同归属高置信组（写批次审计可回滚）。**`--dedup` 与归档/遗忘互斥**：`--dedup [--apply]` 只查重 / 自动合并，不执行归档。
- **分类型衰减曲线**：效用分「时效」从全类型同一线性（365 天归零）改为**指数半衰** `0.5^(d/半衰)`——FACT 慢（默认 730 天）/ PREF 中（默认 365 天）/ COMMIT 任务类快（默认 90 天）/ BOUND 不衰减；半衰可用 `config set maintain_decay_halflife_<TYPE> <天>` 调整。
- **BOUND 归档豁免口径收口**：BOUND 永不归档 / 遗忘（行为对齐文档「immutable / BOUND 豁免」；此前代码只豁免遗忘）。
- **`.archive/` 路径带 owner**：公共 `.archive/facts/`；私密 `.archive/private/<owner>/<type>/`（archive / maintain / merge / consolidate 统一，修复跨 owner 同名撞名隐患；既有存量不迁移）。
- **`config set/get` 支持 maintain_* / consolidate_* 键**（此前文档写了但 CLI 写端只支持 3 个键）。
- **审计升级**：consolidate / 自动合并写批次审计（batch manifest + before/after 影像）；`consolidate --batches` 可查、`--undo <batch>` 可回滚；`--purge` 硬删除维持不可回滚。
- **安全边界不变**：consolidate / undo / batches 属管理动作**不进 MCP**；maintain / archive 维持既有 MCP 暴露；自动合并全程受 owner 写权限约束，跨智能体只预览不执行。
- 测试：新增 `test/consolidate.test.js`（30 断言：dry-run / 公共与私密压缩 / immutable·BOUND 豁免 / 活跃与高效用保护 / min-group / undo 幂等 / 自动合并置信度 / 跨 owner 预览 / 归档互斥 / 衰减单元）+ `test/security-boundary.test.js` 扩至 9 断言（MCP 不暴露 consolidate / undo / batches）；兼容回归 recall-context 4 断言全绿。
- 版本对齐：package.json / SKILL.md frontmatter / CHANGELOG / 引擎 VERSION / 插件 package.json = 0.10.0。

## v0.9.2 (2026-09-02)

发布日期修正。

- 修复 v0.9.1 SKILL.md 正文「最后更新」误写为 2026-09-03（实际发布日为 2026-09-02）的问题；校验工具同步新增「未来日期」拦截。
- 无功能变更。

## v0.9.1 (2026-09-02)

文档版本一致性修复。

- 修复 SKILL.md 正文头部版本行（v0.8.5 / 2026-08-29 残留未随 0.9.0 更新）；正文行改为 0.9.1 / 2026-09-03。
- 版本对齐范围从「四件」扩为「五件」：package.json / SKILL.md frontmatter / SKILL.md 正文版本行 / CHANGELOG / CLI VERSION。
- 无功能变更。

## v0.9.0 (2026-09-01)

召回质量与上下文选择升级。

- **两阶段召回**：词法候选 + 可选本地 embedding 插件候选，统一按语义分与效用分融合排序。
- **可选 embedding 插件**：`--embedding <command>` 或 `config set embedding_cmd <command>`；本地子进程、`stdin/stdout` JSON 协议、超时默认 3000ms、失败自动降级为词法召回。
- **任务感知上下文**：`context --focus <关键词>` 新增任务相关记忆段，按身份 / 边界 / 承诺 / 画像 / 任务记忆 / 近期记忆优先级组装。
- **选择解释**：`context --explain` 输出 included / dropped 与原因；`recall --explain` 继续显示命中理由并补充 embedding 分。
- **MCP 同步**：`recall` / `search` 新增 `embedding` / `embeddingTimeout` / `explain` 参数；新增 `context` 工具。
- **版本四件对齐**：package.json / SKILL.md / CHANGELOG.md / 引擎 VERSION = 0.9.0。

## v0.8.7 (2026-09-01)

评测反馈优化（文档 + 错误提示，功能不变）。

- 新增 `references/faq.md`：10 条常见问题 / 避坑（类型选错、私密区加密、多智能体权限、记忆找不到、忘记主口令、局域网连接、MCP 加载、记忆库位置、跨会话恢复、备份迁移）。
- 错误提示友好化：顶层错误附「修复建议」人话（检查 memory_home、主口令与恢复钥匙等）。
- README 中英：新增「命令输出样例」（init / remember / recall / context 屏幕输出示意）+「常见问题 FAQ 速查」。
- SKILL.md：新增「常见问题 FAQ（速查）」小节，指向 references/faq.md。
- 版本四件对齐 0.8.7（package.json / SKILL.md / CHANGELOG / 引擎 VERSION）。

## v0.8.5 (2026-08-29)

安全修复（安全扫描发现高危，修复后三源同步升版）：

- **MCP 命令执行入口封死**：MCP `distill` 不再接受 `--model`（`callTool` 在工具边界直接拒绝），远端智能体无法再借 MCP 在引擎主机执行任意命令。
- **MCP 任意路径读写封死**：MCP `export` / `import` 的 `out` / `src` 必须落在记忆库根内（新增 `resolveWithinRoot` 校验，防 `..` 穿越），库外路径直接拒绝，与「远程只能读写记忆」承诺对齐。
- **CLI 参数解析修复**：`--model` / `--subject` / `--reason` / `--merge` 此前被 valueOpts 消费但未写入 opts，导致 `distill --model` / `--subject` 实际不生效；本版补齐映射，CLI `distill --model` 现已真正走 `runDistillModel` 安全路径（`shell:false` + 允许清单）。
- **CLI distill 去 shell 注入**：`distill --model` 改走 `runDistillModel` —— `spawnSync(argv[0], argv.slice(1), { shell:false, windowsHide:true })` + `splitCommandArgv` 拆分 argv，彻底移除 shell 注入面；新增 `distillModelAllowlist`（环境变量 `YOTTA_DISTILL_MODELS` 或 `config.distill_models`，未配置时放行本地 CLI，但已无 shell 注入；MCP 层已直接禁 `--model`，不达此处）。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 文档边界说明 = 0.8.5。
- 新增回归测试：`test/security-boundary.test.js`（MCP 禁 --model / export-import 限库内 / 合法操作仍可用，6 项断言）。
## v0.8.4 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-memory --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-memory.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.8.4。
- 修复：SKILL.md / USER_GUIDE.md 安装命令改 `--agent <name>` 合规形式（`npx -y --package @yottameta/yotta-memory yotta-memory-install --agent <name>`），移除 `-g` 与 `npx skills` 推荐。
- 无功能变更（仅文档与版本同步）。

## v0.8.3 (2026-08-28)

中英双语 README 对齐（确定「英文门面 + 中文全档」）：

- **README.md 改为英文**：作为 GitHub / npm / ClawHub 首页的英文门面（翻译 + 精简，覆盖定位 / 核心价值 / 四类型 / 权限隔离 / 身份 / 语义检索 / 生命周期 / 对比 / 安装（CLI+技能双装）/ 升级 / CLI 用法 / 局域网共享 / 开发校验全流程）。
- **新增 README.zh-CN.md**：原中文完整主文档整体平移，顶部加语言切换链接。
- **新增 NOTICE + .npmignore + CHANGELOG.md**：对齐 YottaMeta 技能家族标准（品牌声明 + npm 打包排除 + 更新日志）。
- **package.json**：description 改英文；files 加 README.zh-CN.md / NOTICE / CHANGELOG.md；版本 0.8.2 → 0.8.3。
- 版本四处对齐：package.json / SKILL frontmatter / 引擎 VERSION / 文档。
- 边界（B 方案）：references / USER_GUIDE / 测试注释不翻译；SKILL 触发描述保持中文。

## 历史版本

- **v0.8.2 (2026-08-27)**：发布元数据修复——ClawHub 重发带 `--name 元忆 yotta-memory`，修复展示名缺失中文；无功能变更。
- **v0.8.1 (2026-08-27)**：view 用户查看平台服务端分页 + recall 候选预过滤 + 公共 index.json 超 5000 条按年份分片。
- **v0.8.0 (2026-08-27)**：自我学习/自我进化/自我提升——语义检索（同义词/拼音/字段加权/模糊）+ 效用分融合排序 + feedback 反馈闭环 + maintain 规则层自组织 + distill 心理日志蒸馏 + explain；索引 version 3 旧库自动重建。
- **v0.7.0 (2026-08-27)**：私密区机制级加密（AES-256-GCM 信封加密 + 口令派生主密钥 + 恢复钥匙 + 每 owner 加密索引）+ view 用户查看平台 + migrate + reset-password + key 授权 + context 收工纪律。
- **v0.6.5**：recall/context 根位置去重。
- **v0.6.4**：lan enable Linux 开机自启（systemd 用户单元 / 用户 crontab @reboot 降级）。
- **v0.6.3**：开机自启 VBS 自愈（内联启动命令，根治 80070002）。
- **v0.6.2**：remember --verify 写后回读确定性判定。
- **v0.6.1**：context --budget 字符预算 + 多智能体接入铁律 + remember --source/--weight + 近期记忆排序融合。
- **v0.6.0**：灵魂盘核心——profile 用户画像 + context 开工上下文包 + iam 扩展 + remember --verify + SKILL 记忆守则。
- **v0.5.4**：lan enable 非管理员自动降级用户级 Startup 静默自启。
- **v0.5.3**：CLI 选项可前置。
- **v0.5.2**：schtasks /tr 引号写法修复。
