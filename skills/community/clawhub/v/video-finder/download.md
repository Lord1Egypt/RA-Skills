---
name: video_finder_download
description: "下载影片：Layer1 目录确定、Layer2 下载调度、Layer3 进度监控（状态机+cron）、Layer4 清理。触发：下载、下片、下回来、download、yt-dlp"
---

# download — 影片下载与进度跟踪

四层架构：Directory Resolution → Download Dispatch → Progress Monitor → Cleanup。

## 前置条件

- **称呼约定**：`{{{user}}}` 为占位符
- `yt-dlp` 安装在宿主机
- **依赖**：`video_finder_proxy`（代理判断）
- **状态文件**：`./tracking/downloads.json`（首次自动从 `tracking/downloads.example.json` 复制）

---

## Layer 1: Directory Resolution（目录确定）

纯函数式：输入 preferences.json + 用户回答 → 输出绝对路径。

```
resolve_dir():
  
  # 1. 偏好中已存 → 直接用
  dir = preferences.download_dir
  if dir 非空 && [ -d "$dir" ]:
    return dir

  # 2. 非首次下载 → 自动沿用上次目录，不询问
  last_dir = tracking/downloads.json 最后一条 completed 的 output_dir
            ?? history.md 最后一条记录的目录
  if last_dir && [ -d "$last_dir" ]:
    return last_dir

  # 3. 首次下载 → 询问用户
  dir = ask("{{{user}}}，下到哪个目录呀？")
  if dir 有效:
    return dir

  # 4. 用户未指定 → 自动探测
  for d in [~/Downloads, ~/downloads, /downloads, /data/downloads, ./workspace]:
    if [ -d "$d" ]: return d

  return "./workspace"
```

**规则**：
- 非首次下载**不问**，直接取 `tracking/downloads.json` 中最近一次成功的目录
- 用户指定新目录 → 仅本次有效，不覆盖 `preferences.download_dir`
- 探测到多个目录 → 让用户选
- **确定目录后立即检查空间**：`df -BG --output=avail "{dir}" | tail -1`，若剩余 < 1GB → 警告用户
## Layer 2: Download Dispatch（下载调度）

### 2.1 URL 校验

构建命令前，先校验 URL：

```
if url NOT match /^https?:\/\/.+/ :
  告知用户 "链接格式不对，换个试试"
  abort

if url 含 `'` :             ← 单引号会逃逸出 yt-dlp '{url}' 的引号包裹
  告知用户 "链接包含不安全字符"
  abort

if url 含 `; | $ \` ( ) { } < >` :    ← shell 元字符（& 不在此列，单引号内安全）
  告知用户 "链接包含不安全字符"
  abort
```

### 2.2 构建命令

```
yt-dlp \
  [--proxy http://user:***@host:port]   ← 来自 proxy.md 判断
  -f "bestvideo[height<=?{quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<=?{quality}]"
  -o "{dir}/%(title)s.%(ext)s"
  --newline
  --downloader aria2-next
  --downloader-args "aria2-next:-x 16 -s 16 -k 1M"
  --socket-timeout 30
  "{url}"
```

- `{quality}` 从 `preferences.quality_min` 提取数字（1080p → 1080，4K → 2160）
- `/best[height<=?{quality}]` 作为 fallback：单流站点（无独立音视频轨）自动降级
- `--socket-timeout 30` 防止网络卡死时无限挂起
- 代理参数仅在 `proxy.md` 判断需要时加入

### 2.3 启动 + 写跟踪

```bash
exec background=true
  command="cd {dir} && yt-dlp '{url}' ... > /tmp/ytdlp-{ts}-{rand}.log 2>&1"
```

同时写入 `tracking/downloads.json`：

```json
{
  "active": [{
    "id": "{ts}-{rand}",
    "pid": <PID>,
    "logfile": "/tmp/ytdlp-{ts}-{rand}.log",
    "url": "<URL>",
    "title": "<标题>",
    "output_dir": "<目录>",
    "total_size_bytes": null,
    "started_at": "<ISO时间>",
    "state": "downloading",
    "last_progress": { "percent": 0, "speed": null, "eta": null },
    "last_check_at": null
  }]
}
```

- `total_size_bytes` 首次检测到 `~X.XMiB` 时回填，用于 ETA 计算
- `pid` 配合 `/proc/{pid}/cmdline` 做双重校验防 PID 回收

### 2.4 多下载并发

`downloads.json` 的 `active` 是数组 — 天然支持多个同时下载。每次新增 push 一条，Layer 3 遍历全部。

---

## Layer 3: Progress Monitor（进度监控状态机）

每个下载独立跑状态机：

```
                    ┌──────────────────┐
                    │   DOWNLOADING     │
                    │   cron 定时检测    │
                    └───────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
         有进度更新     30s无变化       进程死亡
              │             │             │
              ▼             ▼             ▼
         重算间隔      间隔翻倍重试    日志有100%?
         设新cron      仍卡→通知     ┌──Y──┘└──N──┐
                         │           ▼           ▼
                         │       COMPLETED     FAILED
                         │
                         └─────── 保持 DOWNLOADING
```

### 3.1 定时器管理

> **并发安全**：读写 `downloads.json` 时先用 `cp downloads.json downloads.json.tmp` 创建副本，操作副本后再 `mv` 覆盖。两个 cron 可能同时触发，`mv` 是原子操作，避免 JSON 写一半被另一个 cron 读到。

两个 cron 协同：

| cron | 类型 | 间隔 | 职责 |
|------|------|------|------|
| **动态** | `at` 一次性 | 根据 ETA 计算（10s~120s） | 检测进度，决定状态转换 |
| **心跳** | `every` 120s | 固定 2 分钟 | 向用户汇报进度（兜底） |

**动态间隔计算**：

```
剩余大小 = total_size × (100% - percent)
速度 = 当前下载速度
eta = 剩余大小 / 速度
interval = clamp(eta / 4, 10s, 120s)
```

| 预估剩余 | < 1min | 1-5min | 5-30min | > 30min |
|---------|--------|--------|---------|---------|
| 检查间隔 | 10s | 30s | 60s | 120s |

### 3.2 检测触发时

```
cron 触发 systemEvent "video-finder download progress check"
  │
  ├─ 读取 tracking/downloads.json（先 cp 到临时文件再读，防并发写损坏）
  │
  └─ 遍历 active 中 state=downloading 的条目:
      │
      ├─ tail -5 {logfile}                          # 读最新日志
      ├─ grep -q "yt-dlp" /proc/{pid}/cmdline       # 防 PID 回收：确认该 PID 仍是 yt-dlp
      ├─ stat -c %Y {logfile}                       # 日志文件最近修改时间
      │
      └─ 判断:
          │
          ├─ 日志有 [download] 100% 或输出文件 .part 消失
          │   → state = "completed", 通知用户, 走 Layer 4
          │
          ├─ /proc/{pid}/cmdline 不含 yt-dlp（PID 已被回收）
          │   → state = "failed", 原因 = "进程异常退出（PID 已回收）"
          │
          ├─ 启动超过 max_timeout（默认 2 小时）
          │   → state = "failed", 原因 = "下载超时（> 2 小时）"
          │
          ├─ 进程活着 && 有新进度
          │   → 解析 [download] X.X% of ~Y.YMiB at Z.ZMiB/s ETA HH:MM
          │   → 若 total_size_bytes 为空 → 回填 total_size_bytes = Y.Y 转 bytes
          │   → 更新 last_progress, 计算新间隔, 设新动态 cron
          │
          ├─ 进程活着 && last_progress 30s 未变
          │   → 间隔翻倍重试一次, 仍卡 → 通知用户"可能卡住了"
          │
          └─ /proc/{pid}/cmdline 不可读 && logfile 超过 120s 未更新
              → state = "failed", 原因 = "进程消失且无完成标记"

全部 active 清空 → 移除心跳 cron
```

### 3.3 汇报策略

| 触发 | 向用户汇报？ | 内容 |
|------|:----------:|------|
| 动态 cron 检测到进度 | ❌ 静默 | — |
| 动态 cron 检测到完成 | ✅ | 文件名、路径、大小 |
| 动态 cron 检测到失败 | ✅ | 失败原因 |
| 心跳 cron | ✅ | 当前进度 %、速度、ETA |
| 心跳 cron 发现全部完成 | ✅ | 汇总 + 移除自身 |

---

## Layer 4: Cleanup（清理）

下载完成或失败后执行：

```
1. 从 downloads.json active 移除 → 移到 completed（成功）/ failed（失败）
2. rm -f {logfile}
3. rm -f {output_dir}/*.part {output_dir}/*.part-Frag* {output_dir}/*.ytdl
4. 取消该下载的动态 cron
5. 若 active 全部清空 → 取消心跳 cron
```

---

## 状态文件完整 schema

`tracking/downloads.json`：

```json
{
  "active": [{
    "id": "1718123456-a3b9f2",
    "pid": 12345,
    "logfile": "/tmp/ytdlp-1718123456-a3b9f2.log",
    "url": "https://...",
    "title": "Passionate sex of real amateur couple",
    "output_dir": "~/Downloads/movies",
    "total_size_bytes": 488636416,
    "max_timeout": 7200,
    "started_at": "2026-07-06T14:30:00+08:00",
    "state": "downloading",
    "last_progress": { "percent": 45.3, "speed": "12.5MiB/s", "eta": "02:30" },
    "last_check_at": "2026-07-06T14:32:30+08:00"
  }],
  "completed": [...],
  "failed": [...]
}
```

| 字段 | 说明 |
|------|------|
| `total_size_bytes` | 首次检测到文件总大小时回填，用于 ETA 计算 |
| `max_timeout` | 最大允许下载时间（秒），默认 7200（2 小时），超时判定失败 |

## 其他站点

尝试 yt-dlp 通用格式；不支持的站点 → 告知用户。
