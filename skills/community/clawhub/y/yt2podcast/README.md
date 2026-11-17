# yt2podcast

把 YouTube 视频变成**中文对谈播客**，自动上传到[小宇宙](https://www.xiaoyuzhoufm.com/)（默认草稿）。
给 AI agent 用的 OpenClaw skill：一条链接进去，十几分钟后一条中文播客草稿出来。

```
YouTube 链接
   │  new-job.sh  (建 job 文件)
   ▼
background worker (python3, 不依赖 LLM)
   ├─ sourcing    NotebookLM: 建 notebook → 加 YouTube 源 → 读中文摘要
   ├─ generating  Audio Overview 生成 + 下载音频（自动走代理）
   ├─ postprocess ffmpeg 转 128k m4a + 内嵌封面/元数据
   └─ uploading   opencli xiaoyuzhou upload --draft
   ▼
openclaw system event 唤醒会话 → agent 发中文通知（含链接）
```

## 特性

- **一条命令一条龙**：取源、生成、转码、上传、通知全自动，agent 只负责"识别链接 + 回执 + 结果播报"。
- **不烧配额的重试**：job 文件记录 `notebook_id` / `source_id` / `stages_done`，失败后 `--rerun` 从断点续跑，不重建 notebook、不重复生成音频。
- **一条龙上传**：生成完直接上传，默认不需要人工确认。**小宇宙没有可用的"草稿箱"**——
  上传即进入平台审核，**审核通过后自动上线**（实测：全程未点发布按钮，第一集仍变成
  `published/APPROVED`）。所以别拿 draft 当保护：要拦截就加 `--hold-upload`（上传前停下等确认）；
  要显式调平台发布接口再加 `--publish`（需 `YT2PODCAST_ALLOW_PUBLISH=1`）。
- **国内网络友好**：自动读 macOS 系统代理（`scutil --proxy`）并注入 `NODE_USE_ENV_PROXY`，解决 `lh3.googleusercontent.com` 直连超时。
- **URL 归一化**：`youtu.be/xxx?si=...` 这类带追踪参数的短链会先转成 `watch?v=<id>` 再喂 NotebookLM。
- **串行安全**：文件锁 `jobs/.worker.lock`，一次只跑一个 job。
- **可离线自检**：`--dry-run` 只跑状态机，不调外部命令。

## 依赖

| 依赖 | 说明 |
| --- | --- |
| [OpenClaw](https://docs.openclaw.ai) | agent 运行环境（提供 exec / system event / skills） |
| [opencli](https://www.npmjs.com/package/@jackwener/opencli) | adapter 运行时（adapter 由本项目自带，见下） |
| **本项目自带 3 个 adapter**（`adapters/`） | `notebooklm download-audio`、`xiaoyuzhou upload`、`xiaoyuzhou upload-status` —— opencli 基线没有，必须安装 |
| `ffmpeg` / `ffprobe` | 转码 m4a、读时长 |
| Chrome 登录态 | notebook.google.com 与 podcaster.xiaoyuzhoufm.com 都要登录（persistent session） |
| 可访问 Google 的网络 | 音频文件在 `lh3.googleusercontent.com` |

## 安装

```bash
git clone https://github.com/<owner>/yt2podcast ~/.openclaw/workspace/coding/yt2podcast
ln -sfn ~/.openclaw/workspace/coding/yt2podcast ~/.openclaw/skills/yt2podcast
openclaw skills list      # 出现 yt2podcast 即安装成功
```

**先装 adapter**（这是最容易漏的一步，opencli 官方没有这三个命令）：

```bash
bash scripts/install-adapters.sh --install   # 复制到 ~/.opencli/clis/，自动备份旧文件
opencli adapter status                       # 应看到 notebooklm / xiaoyuzhou 的 override
```

**首次配置一条命令**（装 adapter + 环境自检）：

```bash
bash scripts/setup.sh
```

之后如果只想复检：`bash scripts/doctor.sh`（逐项 ✅/❌，退出码 1 = 有阻塞项）。

> skill 安装不会执行任何代码（平台安全设计），所以首次要手动跑一次 setup。
> 忘跑也不会白跑任务：`new-job.sh` 会在建 job 前就拦住并只给这一条修复命令。

设置你的小宇宙节目 id（代码里没有默认值）：

```bash
export YT2PODCAST_PODCAST_ID="<podcast id>"
```

## 使用

### 让 agent 用（推荐）

在聊天里直接发 YouTube 链接即可。agent 会读 `SKILL.md` 的流程：
取元数据 → `new-job.sh --no-start` 建 job → 用后台托管跑 `worker.py` → 秒回执 → 完成后播报。

### 手工跑

```bash
# 建 job（不启动）
bash scripts/new-job.sh "https://youtu.be/<id>" \
  --podcast "<podcast id>" \
  --title "中文播客名" \
  --description "一句话简介"

# 跑流水线（在生产里请放到后台托管，别用 nohup，见"已知坑"）
python3 scripts/worker.py <video_id>

# 失败后断点重跑（复用 notebook，不重复消耗生成配额）
python3 scripts/worker.py <video_id> --rerun

# 只补发通知
python3 scripts/worker.py <video_id> --notify-only

# 卡住自愈:找出"没在跑也没结束"的 job(Gateway/机器重启后必用),可一键续跑
python3 scripts/resume-stalled.py            # 只检查,退出码 10 = 有待处理
python3 scripts/resume-stalled.py --resume   # 按落盘产物续跑,不重复消耗配额

# 离线自检状态机
python3 scripts/worker.py <video_id> --dry-run
```

## 配置（环境变量）

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `YT2PODCAST_ROOT` | `~/.openclaw/workspace/yt2podcast` | job 数据根目录 |
| `YT2PODCAST_PODCAST_ID` | 空（必填） | 小宇宙节目 id，或被 `--podcast` 覆盖 |
| `YT2PODCAST_PROXY` | 空（读系统代理） | 访问 Google 的 HTTP 代理 |
| `YT2PODCAST_FFMPEG` / `YT2PODCAST_FFPROBE` | `which` 结果 | 自定义 ffmpeg 路径 |
| `YT2PODCAST_TIMEOUT_*` | 见 worker.py | 各阶段超时（秒），排障时可调小 |

## 安全说明

执行的外部命令、网络访问、文件写入范围、发布授权门槛、进程生命周期（**不自行 detach、不装
cron/systemd**）与"无遥测"承诺，都写在 [SECURITY.md](./SECURITY.md)。

## 已知坑（都已修，留档避免回归）

1. **worker 启动即被杀**：OpenClaw 的 exec 在回合结束时会 kill 整个进程组（`treeOwnership: process-group`），`nohup ... &` 不顶用，job 会永远停在第一阶段且**没有任何通知**。
   → 用 exec 的 `background: true` 托管；`new-job.sh` 的内部启动也加了 setsid 兜底。
2. **AddSources RPC 静默失败**：`youtu.be/xxx?si=...` 带追踪参数会让 NotebookLM 加源返回 no source id。
   → `canonical_youtube_url()` 统一成 `https://www.youtube.com/watch?v=<id>`。
3. **下载音频 `fetch failed`**：音频在 `lh3.googleusercontent.com`，国内直连超时；opencli 用 Node fetch，不读 macOS 系统代理。
   → `system_proxy()` + `child_env()` 注入 `HTTP(S)_PROXY` 和 `NODE_USE_ENV_PROXY=1`。

## 实测数据

源视频 2 小时 14 分（Cheeky Pint，Zuckerberg 访谈）：

> 运行方式：worker 必须由宿主的后台托管能力启动（OpenClaw 用 exec `background: true` +
> `timeoutSeconds: 0`）。它不会随 agent 回合结束而死，但会随 Gateway 重启/退出而终止；
> 中断后 `worker.py <video_id>` 可从断点续跑，不重复消耗生成配额。

| 阶段 | 耗时 |
| --- | --- |
| sourcing（建本 + 加源 + 摘要） | 约 25 秒 |
| generating（生成 + 下载 194MB wav） | 约 8 分钟（代理慢时下载约 25 KB/s） |
| postprocess（转 128k m4a，17.8 MB） | 14 秒 |
| uploading（小宇宙草稿） | 18 秒 |
| **成片** | 19 分 15 秒 / 17.8 MB |

## 目录结构

```
yt2podcast/
├── SKILL.md            # agent 读的流程说明（核心）
├── scripts/
│   ├── new-job.sh        # 只建 job 文件（不启动 worker）
│   ├── worker.py         # 五阶段流水线（不依赖 LLM）
│   ├── resume-stalled.py # 卡住自愈：发现 + 断点续跑
│   ├── doctor.sh         # 环境自检（依赖/adapter/登录/网络）
│   └── install-adapters.sh  # 安装自带 adapter 到 ~/.opencli/clis/
├── adapters/           # 自带 opencli adapter（opencli 基线没有这三个命令）
├── CHANGELOG.md
└── LICENSE
```

## 发布到 ClawHub

这是一个 **skill**（流程说明 + 脚本），不是 plugin（不注册工具/渠道）。

```bash
npm i -g clawhub
clawhub login
clawhub skill publish ./yt2podcast --version 0.1.0
```

## License

MIT
