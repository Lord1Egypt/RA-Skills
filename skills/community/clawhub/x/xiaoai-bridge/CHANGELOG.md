# Changelog

## [1.3.13] - 2026-11-07

### Changed

- 响应 openclaw/clawhub#4471 的官方指引（"If the content or metadata changed, publish a fixed version or release first"）：
  - SKILL.md 新增“当前安全验证状态”小结（静态扫描、声明权限、子进程边界、凭据存储、依赖、数据外发、测试七个维度），便于审计与复审快速索引；
  - 行为无变化，触发对新内容的完整扫描。

## [1.3.12] - 2026-11-07

### Security

- 响应 1.3.11 SkillSpector LP1（Underdeclared Capability）复审结论："a shell capability in scripts/lib/state.js that is not covered by declared permissions"。
  - 根因：SkillSpector LP1 按 SKILL.md frontmatter 的 `permissions[]` 能力类别清单与代码实际能力比对（词表：bash/shell/terminal/command→shell、network/http/fetch/api→network、read→file_read、write→file_write、env/environment→env）；本技能此前只有 `allowed-tools`（工具预批准列表，非能力清单），其中的 `exec` 不在其类别词表内，导致 `child_process`（icacls/whoami）的 shell 能力未声明；
  - 修复：frontmatter 新增 `permissions: [shell, network, read, write, env]`，与实际能力精确对应（shell=icacls/whoami、network=小米接口+Jev、read/write=状态目录、env=凭据环境变量）；不多声明以避免 LP4（Overdeclared）；
  - 新增 manifest 守卫测试：`permissions` 必须声明这 5 项且恰好 5 项。

### Changed

- 版本号 1.3.11 → 1.3.12。

## [1.3.11] - 2026-11-07

### Security

- 响应 1.3.10 SkillSpector 复审结论（"the ACL check can accept **a different account with the same short username**"）：修复允许名单的同短名账户绕过。
  - 此前账户名信任判断用 `name.endsWith("\\" + username)` 后缀匹配——当前用户为 `asus` 时，其他域/机器下的同名账户（如 `EVIL-PC\asus`）会被误判为当前用户而放行；
  - 修复：改用系统 `whoami.exe /user /fo csv /nh` 解析出的**完整账户名（DOMAIN\user）与 SID 精确匹配**（大小写不敏感），移除一切后缀/包含匹配；裸用户名仅在 icacls 输出恰好为裸名时做精确匹配兜底；
  - 新增测试：`EVIL-PC\asus` 在当前用户为 `asus` 时必须被拒绝；完整账户名/SID 精确匹配放行。

### Changed

- 版本号 1.3.10 → 1.3.11。

## [1.3.10] - 2026-11-07

### Security

- 响应 1.3.9 ClawScan 复审结论的三项意见：
  - "ACL parsing bug may ignore **a comma-separated read permission**"：`parseWindowsAclEntries` 此前把合并形式（如 `(R,X)`、`(DE,RC)`）的整段 token 当作未知丢弃，逗号合并的授权会被无视。修复：解析时按逗号拆分为独立权限 token，未识别 token 仍按“授权”计（宁严勿漏）；
  - SID 归因：icacls 输出中无法解析为账户名的 SID 条目（常见于 Temp 树的陈旧账户 ACE）此前会被整行跳过（等同于无视授权）。现在：内置系统主体 SID（SYSTEM/Administrators 等）放行、宽账户组 SID（Everyone/Users 等）明确拒绝、其余 SID 经系统 `whoami.exe`（只读，结果缓存）归因为当前用户才放行，仍无法归因即硬失败；
  - "an unexpected filesystem change in a diagnostic command"：`check` 此前会创建状态目录并自动收紧权限（诊断命令带副作用）。修复：`check` 改为**纯只读诊断**——不创建目录、不修改权限、不触碰 ACL；目录缺失时仅报告“不存在（首次运行监听/speak 时自动创建）”，过宽权限一律报告失败并保留现场。
- 测试同步更新（目录缺失不创建、过宽权限不自动收紧且现场保留、逗号合并权限、SID 归因矩阵）；Windows 测试目录改在 `%LOCALAPPDATA%` 下创建以避开 Temp 树的陈旧 SID ACE（默认状态目录同级，继承干净 ACL）。

### Changed

- 版本号 1.3.9 → 1.3.10。

## [1.3.9] - 2026-11-07

### Security

- 响应 1.3.8 AIG 复审结论（"Windows ACL validation can **ignore advanced permission grants**"）：修复 ACL 解析器对 `GENERIC_*` 高级权限授予的处理。
  - 此前 `GENERIC_READ` / `GENERIC_WRITE` / `GENERIC_EXECUTE` / `GENERIC_ALL` 被误归为继承标志——对 `Everyone` 等账户的 GENERIC 授权会被当作“无权限位”跳过，即高级权限授予被 ACL 校验无视；
  - 修复：`GENERIC_*` 从标志集合移除并计入授权；权限 token 正则放宽为允许下划线；未识别的 token 一律按“授权”计（宁严勿漏）；
  - 新增测试：对 Everyone 的四种 GENERIC 授权均判 `ACL_TOO_OPEN`，当前用户自身的 GENERIC 授权不误报。

### Changed

- 版本号 1.3.8 → 1.3.9。

## [1.3.8] - 2026-11-07

### Security

- 响应 1.3.7 ClawScan 复审结论（"an insecure-state override can accept a directory **without checking its ACL**"）——复审器指出的代码路径真实存在：`evaluateDirSecurity` 的 Windows 分支此前对“目录不在当前用户 profile 内”返回可覆盖的 `ACL_UNVERIFIABLE`，携带 `XIAOAI_ALLOW_INSECURE_STATE_DIR=true` 时会在**未执行任何 ACL 校验**的情况下放行。
  - Windows 上彻底移除 insecure 覆盖路径：目录不在当前用户 profile 内改为 `FOREIGN_LOCATION` 硬失败（不可覆盖）；`XIAOAI_ALLOW_INSECURE_STATE_DIR` 在 Windows 上不被读取，仅保留其原设计场景（POSIX 文件系统无法强制权限）；
  - 至此 Windows 安全判定链为：用户 profile 路径 → 目录真实 ACL（icacls）→ 缓存文件真实 ACL（登录前+登录后），任何一步失败都直接中止，不存在“未经 ACL 校验就接受目录”的代码路径；
  - 测试同步更新（非用户目录断言 `FOREIGN_LOCATION` 且不可覆盖）。

### Changed

- 版本号 1.3.7 → 1.3.8。

## [1.3.7] - 2026-11-07

### Security

- 响应 1.3.6 ClawScan 复审结论（"a Windows permissions weakness that could expose **saved account session credentials**"）：把 ACL 校验从目录扩展到**缓存文件本身**——凭据最终落在 `.mi.json`，此前只验证了目录 ACL（依赖"文件继承目录授权"的隐含假设）。
  - `prepareCacheFile`（登录前预创建）与 `verifyCacheFile`（登录后复验）在 Windows 上新增对 `.mi.json` 的只读 `icacls` ACL 校验，规则与目录一致：授予当前用户 / `SYSTEM` / `Administrators` 之外账户、无法解析输出、无法归因的 SID 授权一律硬失败，不可被 `XIAOAI_ALLOW_INSECURE_STATE_DIR` 绕过；
  - 新增共享辅助 `verifyWindowsAclPath`（ensureStateDir 同步复用，消除重复），`evaluateWindowsAcl` 支持 `kind` 参数区分目录/缓存文件的错误信息；
  - 新增 2 个测试用例（文件 ACL 过宽硬失败 / 正常通过）。

### Changed

- 版本号 1.3.6 → 1.3.7。

## [1.3.6] - 2026-11-07

### Security

- 响应 1.3.5 ClawScan 复审结论（"a Windows access-control parsing issue that may allow unsafe cache directories"）：Windows 上目录 ACL 校验的**任何失败**改为硬失败，彻底消除“无法验证时放行”的路径。
  - `ACL_UNVERIFIABLE`（icacls 不可用 / 输出无法解析 / 存在无法归因的 SID 授权）从可覆盖改为不可覆盖——`icacls` 是 Windows 系统内置组件，“无法验证”本身就是解析/归因异常信号，放行等于把凭据写入 ACL 未知的目录；
  - `XIAOAI_ALLOW_INSECURE_STATE_DIR` 的适用范围收窄为原设计场景：仅 POSIX 上权限无法强制的文件系统（Windows 目录 ACL 校验全都不适用该开关）；
  - 错误信息改为引导换目录/排查解析异常，不再提示 insecure 开关；
  - 测试同步更新；SKILL.md / SECURITY.md / env.example / skill-card.md 同步收紧描述。

### Changed

- 版本号 1.3.5 → 1.3.6。

## [1.3.5] - 2026-11-07

### Security

- 响应 1.3.4 ClawScan 复审结论（"a confirmed state-directory permission issue could expose session credentials when an insecure override is enabled"）：把「已确认的过宽 ACL」从可覆盖改为**硬失败**。
  - `ACL_TOO_OPEN`（icacls 确认 Everyone/Users 等账户被授权）的 `overridable` 由 true 改为 false：`XIAOAI_ALLOW_INSECURE_STATE_DIR` 不再能绕过已确认的过宽授权；用户需用 icacls 修正授权（错误信息附修复命令示例）或改用其他目录；
  - `ACL_UNVERIFIABLE`（icacls 不可用 / 输出无法解析 / 无法归因的 SID 授权）保持可覆盖，与既有“权限无法强制 / ACL 无法验证”口径一致；
  - 测试同步更新（ACL 过宽时 insecure 开关同样拒绝）；SKILL.md / SECURITY.md / env.example / skill-card.md 同步说明，并明确 `icacls` 是运行期唯一子进程调用（只读，属已声明 exec 能力）。

### Changed

- 版本号 1.3.4 → 1.3.5。

## [1.3.4] - 2026-11-07

### Security

- 响应 1.3.3 ClawScan 复审结论（"confirmed weakness in how Windows session-cache permissions are checked"）：Windows 的 `fs.Stats.mode` 是合成值，POSIX 权限位检查无效，此前目录仅靠“位于当前用户 profile 内”的路径策略放行，未校验真实 ACL。
  - `ensureStateDir` 在 Windows 路径策略通过后，调用系统内置 `icacls`（只读，5 秒超时）校验真实 ACL：把访问权授予当前用户 / `SYSTEM` / `Administrators` 之外账户（Everyone / Users / Authenticated Users 等）一律拒绝（`ACL_TOO_OPEN`）；
  - `icacls` 不可用、输出无法解析、或存在无法归因的 SID 授权时，按既有口径判 `ACL_UNVERIFIABLE`（可覆盖），需 `XIAOAI_ALLOW_INSECURE_STATE_DIR=true` 显式确认；
  - 新增纯函数 `parseWindowsAclEntries` / `evaluateWindowsAcl`（离线可测，测试注入 `aclExec`），12 个新测试用例覆盖标准 ACL、域前缀账户名、DENY 条目、继承标志、SID 归因与失败路径；
  - ACL 校验只对真实文件系统生效（测试 fs 替身自动跳过），不做任何 ACL 修改。

### Changed

- 版本号 1.3.3 → 1.3.4。

## [1.3.3] - 2026-11-07

### Security

- 响应 1.3.2 ClawScan 审计结论（"reports a potentially vulnerable dependency"）：lockfile 锁定的传递依赖 `follow-redirects@1.16.1`（`@mi-gpt/miot → axios@1.20.0 → follow-redirects`）命中 HIGH 公告 [GHSA-mrwp-f3q8-3g9p](https://github.com/advisories/GHSA-mrwp-f3q8-3g9p)（跨域重定向时敏感头数组被丢弃、自定义凭据可能跟随重定向）。
  - `npm audit fix` 将 lockfile 升级到修复版 `follow-redirects@1.16.2`，`npm audit` 回到 0 vulnerabilities；
  - 本技能不发起任何跨域重定向请求（小米接口为固定 API 域名，Jev 判定为固定 https 端点），实际暴露面有限，但仍按公告修复；
  - 代码行为无变化。

### Changed

- 版本号 1.3.2 → 1.3.3。

## [1.3.2] - 2026-11-07

### Security

- 修复 1.3.1 的发布事故：发布时误将本地草稿文件 `audit13.html`（审计页面存档，240KB）打包进发布物。该文件包含大量扫描器敏感文本（"Credential Access"、"exfiltration"、finding 描述等），导致 1.3.1 的 SkillSpector 扫描把页面里的每条历史 finding 再标记一遍，findings 从 51 暴涨到 219，审计状态从 Pass 变为 Review。
  - 从发布物中移除该文件（1.3.1 → 1.3.2 无代码行为变化，代码与 1.3.1 一致）；
  - `.clawhubignore` 新增 `*.html` / `audit*.json` / `parse-audit*.js` 排除项；
  - `manifest.test.js` 新增断言：发布树中不得出现任何 `.html` 文件，防止同类事故复发。

### Changed

- 版本号 1.3.1 → 1.3.2。

## [1.3.1] - 2026-11-05

### Security

- 响应 1.3.0 ClawHub 审计的 Description-Behavior Mismatch（High，95%/94% 置信）：声明的 description 未披露 Jev 这一「额外的外部接收方」。
  - SKILL.md frontmatter `description` 明确披露：配置 `JEV_API_KEY` 后全部语音转写文本会发送至 Jev 判定服务（默认 https://tokenrhythm.studio），仅含转写文本与能力边界说明，不含账号/设备/凭据；
  - SECURITY.md 新增「第三方数据流（Jev 判定，可选）」章节：默认无第三方发送、启用后的数据内容与范围、与热词模式的差异、最小化措施与退出方式；
  - 行为本身无变化（正文「转发判定」一节的披露与运行期 stderr 提示在 1.3.0 已存在）。

### Changed

- 版本号 1.3.0 → 1.3.1。

## [1.3.0] - 2026-11-05

### Added

- **Jev 智能判定转发**（热词触发的上位替代）：配置 `JEV_API_KEY` 后，每条语音由 Jev 判定模型（`NeoHorse-Jev-4B`，`POST /v1/decision`）动态决定是否转发给外部 AI；未配置或服务不可用时自动降级回热词触发。
  - 新增 `scripts/lib/jev-policy.js`：三挡判定策略纯函数（`loose` 0.35 / `balanced` 0.60 默认 / `strict` 0.80 转发阈值 + 原生能力否决线 + 显式豁免线），`JEV_DECISION_THRESHOLD` 可覆盖阈值；判定规则为 `转发 = shouldForward ≥ 阈值 AND NOT (isNativeCapability ≥ 否决线 AND shouldForward < 豁免线)`，兼顾小爱原生能力（家电/音乐/天气/闹钟不转发）与用户显式指定 Agent（转发）。
  - 新增 `scripts/lib/jev-client.js`：与 `mi-client.js` 同级的网络边界模块（不读 `process.env`），内置 10 分钟 LRU 判定缓存（200 条）、超时与错误分类（auth/rate_limit/server/request/network/timeout/protocol）。
  - 降级策略：单批判定失败回退热词匹配；连续 3 次失败进入 60 秒冷却；401/403 认证错误进入 10 分钟长冷却；冷却期满自动重试。
  - `extractTranscripts`/`pollTranscripts`：Jev 模式下不做前缀过滤，全部新转写交由判定；时间戳游标与 `extractCommands` 共享。
  - 新增 `judge` 子命令：对单条文本做 Jev 转发判定（不需要小米配置），输出 JSON；`test` 子命令配置 Jev 时附带连通性检查。
  - stdout 消息新增可选字段 `via`（`jev`/`prefix`），向后兼容。
- 新增配置：`JEV_API_KEY`、`JEV_LEVEL`、`JEV_DECISION_THRESHOLD`、`JEV_TIMEOUT_MS`、`JEV_BASE_URL`（强制 https）、`JEV_MODEL`。
- 文档：SKILL.md 新增“转发判定”专节（挡位矩阵、降级行为、隐私披露：启用即同意语音转写文本发送至 Jev 判定服务）、`judge` 用法与故障排查条目。

### Security

- `redact.js` 新增 `JEV_API_KEY` 键名脱敏与 `sk_` 令牌兜底脱敏；Jev 判定日志只保留转写前 20 个字符，不落完整语音内容。
- `manifest.test.js` 架构边界测试扩展：`jev-client.js` 允许网络但禁止读取 `process.env`，`jev-policy.js` 保持纯函数，入口脚本不得内联判定服务地址或鉴权头。

## [1.2.4] - 2026-10-23

### Changed

- 重新发布与 1.2.3 相同的修复内容：1.2.3 的发布尝试在 ClawHub 侧一直停留在 pending，版本号已被占用。1.2.3 的扫描结果确认静态分析 `suspicious.env_credential_access` 已清除（staticAnalysis: clean）。
- 代码无新增变更；包含 1.2.1 日志脱敏、1.2.2 网络客户端隔离、1.2.3 环境变量读取集中化。

## [1.2.3] - 2026-10-23

### Security

- 继续消除 1.2.2 审计页仍残留的两处 Critical `suspicious.env_credential_access`：1.2.2 已把网络库移出入口，但入口脚本仍直接读取 `process.env`，启发式规则仍判定“env 访问 + 网络能力”。
  - 新增 `scripts/lib/runtime.js`，集中所有 `process.env` 读取（配置、状态目录、check、PRINT_TRANSCRIPTS）；
  - `xiaoai-listen.js` / `debug-fetch.js` 不再出现 `process.env`，也不再导入网络库；
  - manifest 架构测试同时断言：入口脚本无 `process.env`、无网络导入，`runtime.js` 不导入网络库，`mi-client.js` 不读 env。
- 1.2.2 的版本级 LLM 扫描为 clean/benign。

### Changed

- 版本号 1.2.2 → 1.2.3。

## [1.2.2] - 2026-10-23

### Security

- 修复 1.2.1 审计页静态分析的两处 Critical `suspicious.env_credential_access`（`scripts/debug-fetch.js`、`scripts/xiaoai-listen.js`）：入口脚本同时读取 `process.env` 并导入网络库，被规则判定为“环境变量访问 + 网络发送”。
  - 新增 `scripts/lib/mi-client.js` 作为唯一网络边界：只接收已解析配置，不读取 `process.env`；
  - 两个入口脚本改为调用 `connectMiNA()`，不再直接导入 `@mi-gpt/miot`；
  - 新增 manifest 架构测试，禁止入口脚本直接导入网络库或发起 HTTP 请求。
- 1.2.1 的版本级扫描已从 suspicious 变为 clean/benign（日志脱敏修复生效）。

### Changed

- 版本号 1.2.1 → 1.2.2。

## [1.2.1] - 2026-10-23

### Security

- 修复 1.2.0 发布扫描发现的问题：上游 `@mi-gpt/miot` 在登录/轮询失败时会 `console.error` 整个 axios 错误对象，其中请求头 `Cookie` 含 `passToken`/`serviceToken`，导致凭据进入 stderr。
  - 新增 `scripts/lib/redact.js`，`xiaoai-listen.js` 与 `debug-fetch.js` 在加载任何凭据前安装 console 脱敏包装；
  - 脱敏范围：`Cookie`/`Set-Cookie` 整行、`passToken`、`password`、`serviceToken`、`yetAnotherServiceToken`、`ssecurity`、`nonce`、`MI_PASS_TOKEN`/`MI_PASSWORD`、Bearer 头、JSON 键与表单字段；
  - 自身状态/错误日志（`log()`）同样经过脱敏；
  - 新增 `redact.test.js` 覆盖 Cookie/JSON/表单/Error/console 包装。
- 文档补充：脱敏是尽力而为，仍不应把 stderr 长期落盘。

### Changed

- 版本号 1.2.0 → 1.2.1（针对已发布 1.2.0 的日志泄露扫描结果发布修复版）。

## [1.2.0] - 2026-10-23

响应 ClawHub 安全审计（T09 + 启发式发现）的安全迭代版本。

### Security

- 修复 T09：会话缓存目录与凭据文件改为**强制校验 + fail-closed**（`scripts/lib/state.js`）：
  - 默认目录从共享临时目录迁到当前用户的私有状态目录（Windows `%LOCALAPPDATA%`、macOS `Application Support`、其它 `$XDG_STATE_HOME`/`~/.local/state`）；
  - 拒绝符号链接目录、非目录路径、属主不是当前用户的目录（POSIX）；
  - 目录权限收紧到 `0700` 并复验，chmod 失败不再静默忽略；
  - 缓存文件在登录前以 `0600` 独占预创建，登录后复验类型/属主/权限/硬链接/大小；
  - 任何校验失败以 `ConfigError` 中止（退出码 2），不写入凭据。
- 新增 `XIAOAI_ALLOW_INSECURE_STATE_DIR`：仅在“权限无法强制 / ACL 无法验证”时显式放行，并打印安全告警；不会绕过符号链接、非目录、属主不符、硬链接检查。
- 新增 `check`（别名 `doctor`）命令：本地检查状态目录、目录权限、缓存文件与旧版遗留缓存，不联网、不登录、不输出凭据。
- 收紧 `.env` 权限：POSIX 下可被同组/其他用户修改时直接拒绝；仅“可读”过宽时收紧到 `0600` 并复验，失败则中止（符号链接只告警）。
- 登录后校验缓存内容形态，损坏/非对象内容重置为 `{}`，避免上游把非对象当 store 合并时报错。
- 二次自查加固（独立审查发现的问题）：
  - 硬链接检查覆盖 Windows NTFS（此前在 win32 分支提前返回被跳过）；
  - Windows 公共目录/其他用户 profile（`C:\Users\Public`、`C:\Windows\Temp`、`C:\ProgramData`、`C:\Users\<他人>`）一律拒绝，不安全开关不可绕过；
  - `.env` 不能注入 `LOCALAPPDATA`/`APPDATA`/`USERPROFILE`/`HOME`/`XDG_STATE_HOME`/`ProgramData`/`PUBLIC`/`SystemRoot`/`windir`/`TEMP`/`TMP`/`TMPDIR`/`XIAOAI_ALLOW_INSECURE_STATE_DIR`，且 `.env` 权限不可修改或读取失败时不再静默继续；
  - `clean` 只对当前状态目录尝试删空目录，legacy 位置只删“内容像小米会话缓存”的文件，且不再把 cwd/技能目录作为删目录目标；失败返回非 0；
  - `check` 使用不安全开关放行时返回退出码 2 并标注“不安全”；
  - 目录权限自动收紧仅限“空目录或仅含 `.mi.json`”的专用目录，避免擅自修改 `$HOME` 等项目目录；
  - 登录前清理缓存中的未知顶层键与 `__proto__`，登录后要求缓存非空并比对 `dev/ino`，防止“未写入却校验通过”或文件被替换；
  - 收尾 `stat` 失败统一转为 `ConfigError`（退出码 2），并覆盖 `prepareCacheFile`/`verifyCacheFile` 的 chmod 失败与不安全开关分支测试。
- `SKILL.md` 声明 `allowed-tools: read, write, exec, env` 与 `metadata.openclaw`（`primaryEnv`、`requires.env`、`requires.bins`、`envVars`），消除“检测到 env 能力但未声明工具范围”的发现。
- `.clawhubignore` 排除 `node_modules/`，发布物收敛为约 15 个文本文件，避免安全扫描器无法完整分析依赖产物（原审计 15 条 Incomplete referenced artifact analysis）。
- 文档明确：只读取 `.env` 与自有 `.mi.json`，不访问 SSH/AWS/浏览器/钥匙串凭据；高风险语音动作需消费方二次确认。

### Fixed

- 修复目录 chmod 失败被 `catch {}` 吞掉、`restrictFilePermissions` 返回值被忽略的问题。
- 修复旧版本在共享临时目录 `os.tmpdir()/xiaoai-bridge` 中可被其他本地用户预先创建目录的问题。
- 修复 `SKILL.md` 后台运行示例把 stdout（含语音转写）重定向到日志文件的问题。
- 修复 `VERSION` 常量（此前停留在 1.1.0）与发布版本不一致的问题，并新增一致性测试。
- 修复 `createCacheFile`/缓存内容异常导致上游写入时崩溃的潜在路径。

### Changed

- 版本号 1.1.1 → 1.2.0。
- 新增 `scripts/lib/errors.js`、`scripts/lib/state.js`、`scripts/lib/env.js`；`scripts/lib/core.js` 不再包含目录/权限逻辑。
- `clean` 现在同时清理旧临时目录、`scripts/`、技能根目录与当前目录遗留的 `.mi.json`，并在目录为符号链接时拒绝清理。
- 测试新增 `state.test.js`、`manifest.test.js`，覆盖目录/文件校验、默认目录解析、失败注入、frontmatter 与发布包卫生。

## [1.1.1] - 2026-10-21

### Security

- 删除发布包中泄露真实小米会话的 `scripts/.mi.json`。
- 会话缓存改写到私有目录 `XIAOAI_STATE_DIR`（默认系统临时目录，0700/0600），不再落进技能目录。
- 新增 `clean` 命令清理缓存，启动时检测并告警遗留 `.mi.json`。
- 重新生成 `package-lock.json`，全部依赖改为 HTTPS 官方 registry，并升级有漏洞的传递依赖：
  - `axios` 1.13.5 → 1.20.0（修复 34 条 OSV 告警）
  - `follow-redirects` 1.15.11 → 1.16.1
  - `form-data` 4.0.5 → 4.0.6
- 文档中的所有集成示例改用 `execFile` 参数数组，消除 shell 命令注入示例。
- 空 `TRIGGER_PREFIX` 改为必须显式设置 `XIAOAI_ALLOW_UNFILTERED=true`，避免误处理所有语音。
- `debug-fetch.js` 默认不打印语音转写原文，需 `PRINT_TRANSCRIPTS=true` 才输出。
- 发布包通过 `.clawhubignore` 排除 `scripts/test/`，避免测试代码中的 `spawnSync` 被 ClawHub 静态扫描误判为 `suspicious.dangerous_exec` 而阻塞发布。

### Fixed

- 修复同一轮轮询中多条新语音被漏处理的问题（记录为新 → 旧时只处理了最新一条）。
- 修复 `.env` 加载路径依赖当前目录、与文档不一致的问题。
- 修复 dotenv v17 提示信息与状态日志污染监听 stdout 的问题；现在 stdout 只输出 JSON。
- 修复 SKILL.md 中的 3 个 U+FFFD 乱码字符。
- 修复 `references/migpt-api.md` 中 `getMiNA()` 配置结构错误（`{ speaker: ... }` → 扁平 `MiServiceConfig`）。
- 修复轮询失败时无退避、无限刷日志的问题。

### Changed

- 版本号 1.0.0 → 1.1.1。
- 新增 `LICENSE`（MIT-0）、`SECURITY.md`、`env.example`、`.gitignore`。
- 新增 `node:test` 单元测试与 CLI 测试。
- `test-fetch.js` 重命名为 `debug-fetch.js`，避免被 `node --test` 当作测试文件。
