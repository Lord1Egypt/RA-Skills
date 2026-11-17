# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与语义化版本。

## [0.2.4] - 2026-11-08

### Changed
- 内置 adapter 与上游 PR (#2792) 对齐：内部传输字段更名，避免与命令输出列重名
  （`httpStatus` / `responseBody` / `pageUrl` / `errorCode` / `loginFormVisible` / `artifact*` 系列），
  修掉上游 `silent-column-drop` 与 `silent-sentinel` 两个门禁告警；行为不变。
- `download-audio` 的 `columns` 补上实际返回的 `content_type`、`converted_to_wav`。

## [0.2.3] - 2026-11-08

### Added
- `doctor.sh` 的 adapter 检查升级为**内容比对**（`cmp`）：文件存在但内容与仓库版本不一致时报
  `⚠️ 与仓库版本不一致` 并给出 `install-adapters.sh --install` 同步命令，避免 `git pull` 后
  `~/.opencli/clis/` 里留着旧副本却无人察觉。

## [0.2.2] - 2026-11-08

### Docs
- `SKILL.md` 的 description 与现状对齐：上传即进入平台审核、通过后自动上线（`--hold-upload` 可在上传前停下），
  不再声称"默认只存草稿"。

## [0.2.1] - 2026-11-08

### Changed
- **默认恢复一条龙上传**：生成到 m4a 后直接上传，不再默认停等确认（用户确认这是期望行为）。
  需要拦截时用新参数 `--hold-upload`（停下等 `worker.py <id> --upload`）；`--auto-upload` 保留为兼容别名。

### Docs
- 明确写清"小宇宙没有可用草稿箱"：上传即进入平台审核，通过后自动上线；
  `draft` 标志只是后端 `INITIALIZED`（后台显示"单集审核中"），不能当作未发布凭证。

## [0.2.0] - 2026-11-08

### Changed
- **默认流程改为两段式（重大行为变更）**：worker 生成到 `episode.m4a` 后停下，
  `stage=awaiting_upload` 并发一条"音频已就绪、等确认"的通知；用户确认后跑
  `worker.py <job_id> --upload` 才真正上传。原因：小宇宙托管单集没有真正的草稿箱——
  上传即进入平台审核，**审核通过后自动上线**（实测：全程未点发布按钮，第一集仍变成
  `published/APPROVED`），上传是不可撤回的对外动作，必须由人拍板。
- 新增 `new-job.sh --auto-upload`：显式选择"生成完直接上传"的一条龙模式。
- 通知载荷新增 `needs_confirmation` 与 `final_file`，方便在确认阶段把本地音频交给用户试听。
- `resume-stalled.py` 把 `awaiting_upload` 视为"等人工确认"，不会自动续跑。

## [0.1.9] - 2026-11-08

### Fixed
- **"草稿"表述误导**：小宇宙托管单集的 `draft` 只是后端状态 `INITIALIZED`（后台显示
  「单集审核中」），审核通过后平台可能自动上线。此前通知一律写"草稿、确认后我再发布"，
  与实际不符。现在上传后会用 `xiaoyuzhou upload-status` **回查平台真实状态**，
  记入 `episode_status` / `review_status` / `episode_published` 并随通知下发，
  文档要求按平台口径播报。

## [0.1.8] - 2026-11-08

### Added
- **错误载荷新增 `repair` 字段**：`{"safe": bool, "cmd": "...", "then": "...", "note": "..."}`。
  `new-job.sh` 的入口阻断与 `worker.py` 的 `StageError` 都会带上，agent 可据此自主修复。
- 新增「自主修复策略」章节：白名单（setup / install-adapters / resume-stalled / doctor /
  非配额类重跑，safe=true 可直接执行）与黑名单（装全局包、登录、猜节目 id、公开发布、改代理、
  配额外重生成），以及"每次失败最多自动修一轮、必须说明修了什么"的重试纪律。

## [0.1.7] - 2026-11-08

### Added
- `scripts/setup.sh`：首次配置一条命令（装自带 adapter + 环境自检），解决"装完不知道还要做什么"。
- **fail-closed 前置检查**：`new-job.sh` 在写 job 前毫秒级校验命令/adapter/节目 id，
  缺任何一项**直接拒绝建 job** 并只输出一条修复命令；`worker.py` 开跑前再校验一次
  （`ADAPTER_MISSING` / `MISSING_BINARY`，带具体修复命令）。

### Why
skill 安装时平台不允许执行代码，因此无法"自动注册 adapter"。改用"入口阻断 + 明确修复命令"
保证用户和 agent 一定会在正确的位置发现它，而不是跑到 generating/uploading 才失败。

## [0.1.6] - 2026-11-07

### Added
- **自带 3 个 opencli adapter**（`adapters/`）：`notebooklm download-audio`、
  `xiaoyuzhou upload`、`xiaoyuzhou upload-status`。这三条命令 opencli 官方基线里没有，
  之前只有作者本机装了 → 别的用户装完 skill 必然卡在 generating / uploading。
  现在随包分发 + `scripts/install-adapters.sh` 一条命令安装（自动备份旧文件、支持 --check/--restore）。
- `doctor.sh` 增加 adapter 文件就位检查，缺了直接给出安装命令。

### Changed
- adapter 里的 `DEFAULT_PODCAST_ID` 硬编码移除，改由 `--podcast` 或 `YT2PODCAST_PODCAST_ID` 提供，
  缺失时报错（避免把作者的节目 id 写进公开代码）。
- `SKILL.md` 依赖表区分"opencli 本体"与"本项目自带的 adapter"，并说明不装的后果。

## [0.1.5] - 2026-11-07

### Added
- `scripts/doctor.sh`：环境自检。检查命令行依赖、opencli adapter（notebooklm / xiaoyuzhou）、
  NotebookLM 登录态、小宇宙主播后台登录态（借历史单集状态探活）、节目 id、Google 存储可达性
  （自动探测系统代理）、数据目录可写性。每项都附带**具体修复命令**，退出码 0/1/2 区分
  全绿 / 有阻塞 / 仅警告。`--json` 供 agent 读取。

### Changed
- `SKILL.md` 增加"第 0 步：环境自检"，明确前置条件不满足时不要建 job（避免白耗配额）；
  `NEED_LOGIN` 的处理指向 doctor。

## [0.1.4] - 2026-11-07

### Added
- `resume-stalled.py --quiet`：无卡住 job 时零输出，适合放进心跳/定时任务，不产生噪音与多余 token。
- `docs/automation.md`：卡住自愈的三种接法（心跳巡检 / `openclaw cron` / 手动），
  并说明为什么 skill 不自行安装定时任务、不改用户的 `HEARTBEAT.md`。

## [0.1.3] - 2026-11-07

### Added
- `scripts/resume-stalled.py`：卡住自愈。找出"没在跑也没结束"的 job（无存活 worker 进程且
  `updated_at` 超阈值），按落盘产物推断续跑起点（m4a→uploading / wav→postprocess /
  有 source_id→generating / 否则 sourcing），改好 `stage`+`stages_done` 后可一键续跑。
  解决 Gateway 重启、Mac 重启、宿主回收导致 worker 中途消失、job 静默停摆的问题；
  续跑复用已有产物与 notebook，不重复消耗生成配额。

### Changed
- 文档明确 worker 生命周期：用 exec `background: true` + `timeoutSeconds: 0` 启动，
  不随回合结束而死，但会随 Gateway 重启而终止 → 用卡住自愈补齐。

## [0.1.2] - 2026-11-07

### Changed
- **公开发布改为双重显式授权**：`--publish` 且 `YT2PODCAST_ALLOW_PUBLISH=1`，缺一即报
  `PUBLISH_NOT_ALLOWED`。回应安全扫描"public publishing can occur without explicit authorization"。
- **不再自行 detach 进程**：`new-job.sh` 只写 job 文件并打印下一步命令，移除了 setsid/nohup 启动路径。
  回应"a worker can outlive the host's process cleanup"。
- 新增 `SECURITY.md`，逐项说明执行命令、网络、写入范围、发布授权、进程生命周期、无遥测。

## [0.1.1] - 2026-11-07

### Changed
- `SKILL.md` 增加「能力与风险声明」：明示会执行的外部命令、网络访问、文件写入范围、
  **公开发布能力**（`--publish` 不可撤销、仅限用户明确要求）与完成通知行为。
- frontmatter description 明确"默认草稿、可显式公开发布、完成后回推通知"，
  与代码实际能力对齐（ClawHub 安全扫描此前判为 suspicious 的原因）。

## [0.1.0] - 2026-11-07

首个可发布版本。基于一次真实端到端实测（2 小时 14 分的 YouTube 访谈 → 19 分 15 秒中文播客）。

### Added
- 五阶段流水线 `pending → sourcing → generating → postprocess → uploading → done`，断点续跑。
- `new-job.sh`：建 job 文件（幂等，同一视频不会重复起），可选启动 worker。
- `worker.py`：不依赖 LLM 的流水线执行器，失败唤醒 + `notify.json` 落盘。
- `--rerun` / `--notify-only` / `--dry-run` 三种运维模式。
- 自动代理探测（`scutil --proxy`）与 `NODE_USE_ENV_PROXY` 注入，解决 Google 存储下载超时。
- YouTube URL 归一化，剥离 `?si=` 等追踪参数。

### Fixed
- worker 在 agent 回合结束时被连同进程组一起杀掉，job 永久卡在 sourcing 且无通知。
- 带追踪参数的短链导致 NotebookLM `AddSources` 返回 no source id。
- `lh3.googleusercontent.com` 直连超时导致的 `Downloading the NotebookLM audio failed: fetch failed`。
- 代码中硬编码的小宇宙节目 id 与节目名，改为必填配置；缺失时明确报 `PODCAST_ID_MISSING`。
- frontmatter 依赖声明由 `anyBins`（任一存在即可）改为 `bins`（全部必需）。
