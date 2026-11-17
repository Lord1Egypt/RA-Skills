---
name: yt2podcast
description: 把 YouTube 视频变成中文音频播客：NotebookLM Audio Overview 生成、ffmpeg 转码，再上传小宇宙（上传即进入平台审核，通过后自动上线；可用 --hold-upload 在上传前停下）；完成后回推一条结果通知。用户从微信/聊天里发来 YouTube 链接时使用。
metadata:
  openclaw:
    requires:
      bins: ["opencli", "ffmpeg", "ffprobe"]
---

# yt2podcast：YouTube → 中文播客 → 小宇宙

把一个 YouTube 视频用 NotebookLM 的 Audio Overview 做成中文对谈播客，
再上传到小宇宙（默认**草稿**，不公开发布）。

## 能力与风险声明（Capabilities & Safety）

ClawHub 的自动扫描会检查"行为是否超出描述"。本 skill 的行为范围如下，全部为明示能力，没有隐藏动作：

**会执行的外部命令**
- `opencli youtube video`（只读，取标题/时长）
- `opencli notebooklm create / add-source / source-guide / open / download-audio`（建本、加源、生成并下载音频）
- `opencli xiaoyuzhou upload`（上传节目）
- `ffmpeg` / `ffprobe`（转码与取时长）
- `openclaw system event`（跑完唤醒发起会话，发一条中文通知）

**网络访问**：YouTube（元数据）、notebook.google.com（生成）、lh3.googleusercontent.com（下载音频，可能需要代理）、xiaoyuzhoufm.com（上传）。

**文件写入**：只写 `${YT2PODCAST_ROOT}`（默认 `~/.openclaw/workspace/yt2podcast`）下的 `jobs/`。不读不写用户其它目录，不上传任何本地文件到第三方（唯一上传目标是小宇宙，内容是本次生成的音频）。

**公开发布能力（重要）**：默认 `--draft`，只存草稿。公开发布需要**双重显式授权**：
`--publish` 且环境变量 `YT2PODCAST_ALLOW_PUBLISH=1`，缺一个就直接报错拒绝
（`PUBLISH_NOT_ALLOWED`）。公开发布不可撤销，只有在用户明确要求时才可用。

**进程生命周期**：本 skill 不自行 detach 进程——worker 由调用方（agent 的宿主、
用户终端、或宿主托管的后台任务）启动，随宿主结束而结束；不安装 systemd/cron/开机项。

**通知行为**：任务结束（成功或失败）会主动唤醒发起会话并推送一条中文消息，这是用户预期内的结果回执，不是营销推送。

**无遥测**：本 skill 不含任何统计、上报、埋点。

## 依赖（缺一样都跑不通）

| 依赖 | 用途 | 检查 |
| --- | --- | --- |
| `opencli` | adapter 运行时 | `opencli --version` |
| **本 skill 自带的 3 个 adapter** | `notebooklm download-audio`、`xiaoyuzhou upload`、`xiaoyuzhou upload-status` —— **opencli 官方基线里没有，必须装** | `bash {baseDir}/scripts/install-adapters.sh --check` |
| `ffmpeg` / `ffprobe` | 转码 m4a、取时长 | `ffmpeg -version` |
| Chrome 登录态（persistent session） | notebook.google.com + podcaster.xiaoyuzhoufm.com | 出错会报 `NEED_LOGIN` |
| Google 可达的网络 | 音频文件在 `lh3.googleusercontent.com`，国内直连会失败 | 见"网络代理" |
| `openclaw` CLI | worker 跑完后唤醒会话 | `openclaw --version` |

**小宇宙节目 id 必须自己提供**（`--podcast` 或环境变量 `YT2PODCAST_PODCAST_ID`），代码和 adapter 里都没有默认值。

**adapter 必须单独安装**（这是最容易漏的一步）：

```bash
bash {baseDir}/scripts/install-adapters.sh --check     # 先看缺什么
bash {baseDir}/scripts/install-adapters.sh --install   # 装到 ~/.opencli/clis/（会备份旧文件）
```

原因：opencli 官方只提供 `notebooklm generate-audio` 和 `xiaoyuzhou history/download` 之类的基础命令，
**没有** `download-audio`（生成+轮询+下载+转码一体）、`upload`（小宇宙主播后台上传）、
`upload-status`（查单集状态）。这三个是本 skill 的配套 adapter，放在 `adapters/` 目录里一起分发。
不装的话 worker 会在 `generating` / `uploading` 阶段报 `ADAPTER_MISSING` 或命令不存在。

## 目录约定

| 东西 | 路径 |
| --- | --- |
| skill 根目录 | `{baseDir}`（本 SKILL.md 所在目录） |
| 运行数据根目录 | `${YT2PODCAST_ROOT:-$HOME/.openclaw/workspace/yt2podcast}` |
| job 文件 | `<root>/jobs/<video_id>.json` |
| job 目录 | `<root>/jobs/<video_id>/`（worker.log / audio.wav / cover.jpg / episode.m4a / notify.json） |

## 第 0 步：环境自检（首次使用、换机器、报 NEED_LOGIN 时先跑）

```bash
bash {baseDir}/scripts/setup.sh           # 首次使用:装 adapter + 自检(一条命令)
bash {baseDir}/scripts/doctor.sh          # 只自检,不改动系统
bash {baseDir}/scripts/doctor.sh --json   # 机读
```

> 为什么不能"装好就自动生效":skill 安装只解压文件,平台**不允许** skill 在安装时执行代码
> (这是安全设计,本 skill 也不该偷偷改你的系统)。所以这里用 **fail-closed** 兜底:
> `new-job.sh` 在写 job 之前会毫秒级检查依赖,缺东西就**直接拒绝**并打印唯一修复命令
> `bash {baseDir}/scripts/setup.sh`;`worker.py` 开跑前还会再查一次(防止绕过入口)。
> 也就是说,配置没做时不会"跑到一半才失败",而是在第一步就被拦住并告诉你怎么修。

会逐项检查并给出**具体修复命令**：
- 命令行依赖：`opencli` / `ffmpeg` / `ffprobe` / `python3` / `openclaw`
- adapter：opencli 是否装了，以及**本 skill 自带的 3 个 adapter 文件**是否就位（缺了直接给 `install-adapters.sh --install`）
- 登录态：NotebookLM（`notebooklm whoami`）、小宇宙主播后台（用历史单集的状态查询探活）
- 配置：`YT2PODCAST_PODCAST_ID` 有没有设
- 网络：`lh3.googleusercontent.com` 是否可达（自动探测系统代理）
- 数据目录是否可写

退出码：`0` 全绿、`1` 有阻塞项、`2` 只有警告。
前置条件不满足时**先别建 job**——不然会白跑一趟、浪费 NotebookLM 生成配额。

## 第一步：收到链接时

1. 从消息里挑出 YouTube 链接（`youtu.be/`、`watch?v=`、`/shorts/`、`/live/` 都行；`?si=` 之类的追踪参数由脚本自动去掉）。
2. 读标题和时长（只读，不耗配额）：

   ```bash
   opencli youtube video "<url>" -f json      # data 是 [{field,value}]，取 title / duration
   ```

3. 建 job（只落文件，不启动）：

   ```bash
   bash {baseDir}/scripts/new-job.sh "<url>" \
     --podcast "<小宇宙节目id>" \
     --title "<中文播客名>" \
     --description "<一句话中文简介>" \
     --session-key "<当前会话 key>"
   ```

   - 本脚本**只建 job 文件，从不启动 worker**（不会 fork、不会 nohup、不会 setsid）。
   - `"existing": true` → 这个视频已在跑，别重复起，直接回执。
   - `stage: failed` → 先按"排障"处理，重跑加 `--retry`。
   - **默认一条龙**：生成完直接上传（用户期望的默认行为）。
     想在上传前停下等确认，加 `--hold-upload`；想连平台"发布"接口一起调再加 `--publish`（需 `YT2PODCAST_ALLOW_PUBLISH=1`）。

4. **启动 worker —— 必须用后台托管，不要用 nohup**：

   用 exec 工具以 `background: true` + `timeoutSeconds: 0` 运行：

   ```bash
   python3 {baseDir}/scripts/worker.py <video_id>
   ```

   - `timeoutSeconds: 0` 必须给：否则长视频（生成+下载可能 30 分钟以上）会被 exec 的默认超时砍断。
   - 这个后台服务**不会**因为 agent 回合结束而中断，但**会**随 Gateway 重启/更新/退出而终止
     （OpenClaw 文档明确：background 不保证跨宿主重启存活）。中断不可怕——job 文件记着
     `notebook_id` / `source_id` / `stages_done`，重启后用 `worker.py <video_id>` 从断点续跑，
     不会重复消耗 NotebookLM 生成配额。

   > ⚠️ 关键坑：OpenClaw 的 exec 在回合结束时会 kill 整个进程组（日志里能看到
   > `treeOwnership: process-group`）。普通 `nohup ... &` 起的 worker 会被立刻杀掉，
   > job 永远停在第一个阶段，而且**不会**有失败通知。所以必须用宿主的 background 托管能力，
   > 不要自己 detach。

5. **秒回执**（一条消息，然后结束本回合）：

   ```
   ✅ 已收到《<中文播客名>》，原视频 <时长>，正在生成音频并上传小宇宙，
   大约 10–20 分钟（上传后进入平台审核，通过即自动上线）。完成后我把链接发你。
   ```

   不要 sleep、不要轮询 job 文件；worker 结束时自己唤醒。

## 第二步：收到唤醒时

worker 结束时执行 `openclaw system event --text "yt2podcast {...}" --mode now` 唤醒原会话。
最稳的做法是先读 `jobs/<video_id>/notify.json`（同一个 JSON 的落盘版）。

### 情况 A：只在 `--hold-upload` 模式下出现——生成完、等你确认上传（`needs_confirmation: true`）

```
🎧 音频已就绪，等你确认
名称：<中文播客名>
时长：<duration_text>　大小：<size_text>
本地文件：<final_file>
确认上传吗？上传后小宇宙会进入平台审核，**审核通过即自动上线**，无法撤回。
```

用户确认后，用后台托管（`background: true` + `timeoutSeconds: 0`）跑：

```bash
python3 {baseDir}/scripts/worker.py <video_id> --upload
```

然后等下一次通知（那一轮才是最终结果）。用户说"不用了"就什么都不做，job 停在 `awaiting_upload`。

### 情况 B：默认一条龙，上传完成（`stage: done`）

```
✅ 播客已生成
名称：<中文播客名>
简介：<一两句中文简介>
时长：<duration_text>
大小：<size_text>
状态：<平台口径：草稿 / 审核中 / 已发布>
链接：<episode_url>
```

- 名称/简介要**二次润色**：读 `source_summary`（NotebookLM 的中文摘要）后用自己的话写，
  不要照抄 Markdown 标记（`**`）。
- **状态必须用平台回查值**，不要凭 `draft` 标志下结论。payload 里三个字段：
  - `episode_status`：`draft` / `reviewing` / `published`
  - `review_status`：`PENDING` / `APPROVED` / `REJECTED`
  - `episode_published`：布尔
- **小宇宙的"草稿"语义要小心**：托管单集的 `draft` 只是后端状态 `INITIALIZED`，
  后台界面显示为「单集审核中」；审核通过后平台可能**自动上线**，不需要再点发布。
  所以对用户要说"已上传，平台状态：审核中（通过后会自动出现在节目里）"，
  只有在 `episode_status=published` 时才说"已发布"。
- 想确认后续状态：`opencli xiaoyuzhou upload-status <episode_id> --podcast <id> --site-session persistent --keep-tab true`。

### 失败

```
❌ 播客生成失败
视频：<原视频标题>
原因：<error.message>
建议：<error.suggestion>
```

`error.suggestion` 已按错误类型给好，直接用，别自己编。常见：

| error.code | 含义 | 处理 |
| --- | --- | --- |
| `NEED_LOGIN` | NotebookLM / 小宇宙掉登录 | 先跑 `scripts/doctor.sh` 看是哪一侧掉了，登录后 `--rerun` |
| `QUOTA_EXHAUSTED` | NotebookLM 每日生成配额用完 | 等第二天 |
| `ADAPTER_MISSING` | opencli adapter 没装 | 先装 adapter |
| `COMMAND_EXEC` + `fetch failed` | 下载音频时 Google 存储不可达 | 配代理后重跑（见下） |
| `SOURCE_PROCESS_TIMEOUT` | 源抽取超时 | 确认视频可访问后重跑 |
| `PODCAST_ID_MISSING` | 没给小宇宙节目 id | `--podcast` 或 `YT2PODCAST_PODCAST_ID` |
| `FFMPEG_FAILED` | 转码失败，已降级用 wav 上传 | 想听 m4a 就重跑一次 |

失败后**不要盲目自动重试**（白耗配额）；按下面的「自主修复策略」判断哪些能自己修。

## 自主修复策略（agent 能自己修到什么程度）

失败载荷里有 `repair` 字段时，按 `repair.safe` 决策：

- **`repair.safe: true`** → 直接执行 `repair.cmd`，然后按 `repair.then` 指定的动作重试一次。
  典型："缺 adapter" → 跑 `scripts/setup.sh` → 重新执行同一条 `new-job.sh`。
- **`repair.safe: false`**，或没有 `repair` → **停下来告诉用户**，附上 `suggestion`
  和需要用户做的决定（凭据、节目 id、是否公开发布等）。

### 允许自动执行（幂等，只动本机 skill / opencli 目录，不装全局包、不登录账号）

- `bash {baseDir}/scripts/setup.sh`（装自带 adapter + 自检）
- `bash {baseDir}/scripts/install-adapters.sh --install`（仅补 adapter）
- `python3 {baseDir}/scripts/resume-stalled.py --resume`（卡住续跑）
- `bash {baseDir}/scripts/doctor.sh`（诊断，只读）
- `python3 {baseDir}/scripts/worker.py <job_id>`（按 suggestion 续跑，非配额类错误）

### 必须交回用户（禁止代劳）

- 安装全局包：`npm i -g …`、`brew install …`
- 登录 / 扫码 / 提供密码（`NEED_LOGIN`）
- 猜或编造小宇宙节目 id（`PODCAST_ID_MISSING`）
- 公开发布：`--publish` / `YT2PODCAST_ALLOW_PUBLISH=1`（`PUBLISH_NOT_ALLOWED`）
- 改用户的代理/VPN 配置（网络问题只给配置建议，不动手）
- 可能消耗生成配额的重跑（`QUOTA_EXHAUSTED`）

### 重试纪律

- 每次失败最多「自动修复 + 重试」**一轮**；同一个 job 连续两次同类错误就停手，报给用户。
- 修完必须在结果消息里用一句话说明**你修了什么**（例如"发现缺 adapter，已自动安装后重跑"），不要静默。

## 网络代理（国内必看）

NotebookLM 的音频挂在 `lh3.googleusercontent.com`，直连会 `fetch failed`。
opencli 内部用 Node 的 `fetch`，**不读 macOS 系统代理**，所以 worker 会自动：

1. 读 `scutil --proxy`（或环境变量 `YT2PODCAST_PROXY` / `HTTPS_PROXY`）拿代理地址；
2. 给所有 opencli 子进程注入 `HTTP(S)_PROXY` + `NODE_USE_ENV_PROXY=1`。

启动时日志会打印一行 `代理: http://127.0.0.1:xxxx` 或 `代理: 未检测到(直连)`，先看这行。

## 排障

**查状态**

```bash
cat <root>/jobs/<video_id>.json                # stage / error / episode_url
tail -n 50 <root>/jobs/<video_id>/worker.log   # 详细日志（含每条 opencli 命令）
ls -la <root>/jobs/<video_id>/                 # audio.wav / cover.jpg / episode.m4a
```

stage：`pending → sourcing → generating → postprocess → uploading → done / failed`

**重跑失败 job**（复用 notebook，不重复建本、不重复消耗生成配额）

```bash
python3 {baseDir}/scripts/worker.py <video_id> --rerun
```

**只补通知**（结果已就绪，只是没发出去）

```bash
python3 {baseDir}/scripts/worker.py <video_id> --notify-only
```

**断点续跑**：如果 `audio.wav` / `episode.m4a` 已经拿到，可以手工把 job 的
`stages_done` 补上已完成阶段、`stage` 改成下一阶段，再直接 `python3 worker.py <video_id>`。

**卡住判断**：`stage` 不是 done/failed 且 `updated_at` 超过 20 分钟 → 看 worker.log 最后一行再决定是否重跑。

**卡住自愈（Gateway 重启/宿主被回收后必用）**

worker 活在宿主的生命周期里，Gateway 重启、Mac 重启、宿主被回收都会让它中途消失，
job 就停在某个 stage 且不会再有通知。job 文件是幂等断点，所以只需"发现 + 重新调用"：

```bash
python3 {baseDir}/scripts/resume-stalled.py                 # 只检查，输出 JSON（退出码 10 = 有卡住的）
python3 {baseDir}/scripts/resume-stalled.py --max-age 20    # 自定义判定阈值（分钟）
python3 {baseDir}/scripts/resume-stalled.py --resume        # 就地续跑（前台顺序执行）
python3 {baseDir}/scripts/resume-stalled.py --resume --dry-run   # 只演练不落盘
```

判定逻辑：没有存活的 `worker.py <job_id>` 进程 + `updated_at` 超过阈值 → 卡住。
续跑起点按落盘产物推断（产物即真相）：
`episode.m4a` 在 → `uploading`；`audio.wav` 在 → `postprocess`；有 `source_id` → `generating`；否则 `sourcing`。
这样已生成/已下载的产物不会重做，**不会重复消耗 NotebookLM 配额**。

巡检建议（心跳/定时任务里）：

```bash
python3 {baseDir}/scripts/resume-stalled.py --quiet    # 退出码 10 = 有待续跑;没情况零输出
```

发现卡住的 job 时，用宿主后台托管方式启动 `worker.py <job_id>`（脚本已把 `stage` / `stages_done` 改好，
直接跑就是从断点继续），或直接 `--resume`。续跑成功/失败都会照常发通知。

**怎么接自动化由用户决定**：心跳巡检 / cron / 手动，三种接法与命令见
[docs/automation.md](docs/automation.md)。本 skill **不会**自己往系统里装 cron/systemd/launchd，
也不会改用户的 `HEARTBEAT.md`——那是用户自己的配置。

**干扰排查**：`--dry-run` 只跑状态机不调外部命令，可用来验证 job/状态流转。

## 边界

- worker 不依赖 LLM：标题/简介的中文提炼由被唤醒的 agent 用 `source_summary` 二次润色。
- **串行执行**：一个 `jobs/.worker.lock`（flock），抢不到就退出，不要并发重试。
- **草稿优先**：小宇宙公开发布不可撤销，默认永远是草稿。
- **配额**：一次真实生成就消耗一次 NotebookLM 每日额度，不要为了"试一下"反复起 job。
- `adapters/` 不归本 skill 管，本 skill 只调用 `opencli` 命令。

## 安装

```bash
git clone <repo> ~/.openclaw/workspace/coding/yt2podcast
ln -sfn ~/.openclaw/workspace/coding/yt2podcast ~/.openclaw/skills/yt2podcast
openclaw skills list        # 看到 yt2podcast 即装好
export YT2PODCAST_PODCAST_ID="<你的小宇宙节目id>"
```

改完 SKILL.md 需要 `/new` 或 `openclaw gateway restart` 才能让 agent 读到新版本。
