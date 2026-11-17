# 腾讯视频（v.qq.com）流媒体 —— 逆向笔记

> 实测日期：2026-09-25
> 实测样本：`v.qq.com/x/cover/<cid>/<vid>.html` 形式的免费长视频（约 20 分钟）
> 成果：720P（1280×720）/ 19 分 38 秒 / H.264 + AAC
> 结论：**yt-dlp 原生支持，无需登录，无需浏览器拦截**——本平台是全流程最快的

---

## 1. 链接形态与入口

```
https://v.qq.com/x/cover/<cid>/<vid>.html?callTime=<毫秒时间戳>
```

- `<vid>`（如 `i3290k6avdi`）是**单集标识**，`<cid>` 是专辑/剧集标识。
- `callTime` 等查询参数**与取流无关**，可原样保留，也可删掉。
- 有些站内跳转参数会让 yt-dlp 报 `Unsupported URL`，此时去掉查询串只留 `.../<vid>.html` 即可。

短链/分享链（`m.v.qq.com`、`vv.video.qq.com` 等）先归一化成上面的 `cover` 直链再交给 yt-dlp。

---

## 2. ⛔ 首要结论：yt-dlp 可用，不要上浏览器重流程

腾讯是**唯一不需要 `browser_ctl.mjs` 拦截**的平台之一：

| 手段 | 结果 |
|---|---|
| `yt-dlp -F "<cover 直链>"` | ✅ 正常列出档位 |
| `yt-dlp -f "shd-0" ...` | ✅ 直接下完并自动合流 |

本平台**不要**走「优酷式」的 seek 采集 → probe → 并发 Range → 手工合并六阶段流程，
那套是给「取流接口被风控、必须靠浏览器签名」的站点（优酷、爱奇艺）准备的。
腾讯照搬那套只会白折腾，直接用 yt-dlp 一条命令即可。

---

## 3. 档位与登录态（与优酷/B站不同！）

未登录实测档位：

| format-id | 分辨率 | 标注 |
|---|---|---|
| `hd-0` ~ `hd-3` | 864×486 | 480P |
| `shd-0` ~ `shd-3` | 1280×720 | 720P |

**关键实测：带 cookie 与不带 cookie，档位列表完全一致**（都只到 720P）。

- 说明该片为**免费内容，未登录即给到免费最高档 720P**，登录不改变结果。
- 与优酷（480/720/1080 三档，不登录只能低画质）、B 站（1080P 需 SESSDATA）**行为不同**。
- ⚠️ 因此腾讯**不要**一上来就按「登录态影响画质」去打断用户；先 `-F` 看一眼档位，
  拿到的档位若已满足需求就直接下。付费/VIP 内容才会受限，届时再走手动介入协议。

> 待补：若遇到 VIP 专享片源（`-F` 只到 480P 且页面弹会员），需登录后再实测档位变化，
> 并把结论补进本节。

---

## 4. ⚠️ 最大的坑：默认下载得到 HEVC(H.265)，用户端「只有声音没有画面」

### 现象

yt-dlp 下载成功、`ffprobe` 一切正常（有视频轨、有音频轨、时长正确），
但用户在本地播放器打开**只有声音、画面全黑**。

### 根因

腾讯的 `shd-*` / `hd-*` 档位**实际是 H.265（HEVC）编码**，
yt-dlp 用 `-c copy` 无损封装成 MP4，`codec_tag_string=hev1`：

```
codec_name=hevc    codec_tag_string=hev1    profile=Main
```

而许多播放器（尤其 Windows 自带「电影和电视」、部分老版 PotPlayer/VLC、
微信/QQ 内置播放器、部分电视盒子与投屏器）**不含 HEVC 解码器，或不解 `hev1` 这个 tag**，
遇到 HEVC 视频轨直接跳过渲染 → 只剩 AAC 音轨能放 → 「只有声音没有画面」。

> 注意：`ffmpeg`/`ffplay` 能正常解码，因为它自带 hevc 解码器（`VFS..D hevc`）。
> **所以「我们这边验过了能播」不等于「用户那边能播」**——这是本坑最阴的地方。

### 判据（下载完必查）

```bash
ffprobe -v error -show_entries stream=codec_name,codec_tag_string -of default=noprint_wrappers=1 out.mp4
```

- 输出 `codec_name=hevc` / `hev1` → **必须转码**，否则大概率用户端黑屏。
- 输出 `codec_name=h264` / `avc1` → 可直接交付。

### 解法：转码成 H.264（`avc1`）

```bash
# 首选：能拿到带 libx264 的 ffmpeg 时（压缩率好，20 分钟片约 100 MB）
ffmpeg -i in.mp4 -c:v libx264 -preset medium -crf 21 \
       -profile:v high -level 4.1 -pix_fmt yuv420p \
       -c:a copy -movflags +faststart -y out.mp4
```

- `-c:a copy`：音轨原样保留，不重复损失。
- `-pix_fmt yuv420p`：兼容性必需。
- `-movflags +faststart`：moov 前置，适合边下边播/投屏。
- 转码耗时约为片长的 1/7（实测 19.6 分钟片约 2 分 50 秒，6.8× 速度）。

### ⚠️ 本机 ffmpeg 缺 libx264 的应对

本环境 `/usr/local/bin/ffmpeg` 编译时带了 `--disable-libx264`，
**没有 `libx264` 编码器**。它只提供 `libopenh264`（备用方案），但压缩率差很多：

| 编码器 | 20 分钟片成品体积 | 说明 |
|---|---|---|
| `libx264`（首选） | 约 98 MB | High profile，推荐 |
| `libopenh264`（备用） | 约 269 MB | 仅 Constrained Baseline，体积约 2.7 倍 |

`libopenh264` 用法（体积可接受时也可用）：

```bash
ffmpeg -i in.mp4 -c:v libopenh264 -b:v 2500k -maxrate 3000k -bufsize 6000k \
       -c:a copy -movflags +faststart -y out.mp4
```

**拿到 libx264 的两条路（本机已验证第 1 条可用）**：

```bash
# 1) imageio-ffmpeg 自带的完整静态 ffmpeg（含 libx264）
python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
#   → .../site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
# 用它替代系统 ffmpeg 执行上面的转码命令即可。

# 2) 系统装了 libx264 动态库时，装带 x264 的 ffmpeg
ldconfig -p | grep x264          # 本机已有 libx264.so.164
sudo apt-get install -y ffmpeg   # 或用 johnvansickle 静态构建
```

脚本化建议：转码前先探测可用编码器，
`ffmpeg -encoders | grep libx264` 有则用 x264，无则回退 `libopenh264`。

> 若用户明确接受 HEVC（自己播放器能放、或要投屏到支持 HEVC 的设备），
> 则跳过转码直接交付原文件，省时省体积。

---

## 5. 标准命令（腾讯专用，最简）

```bash
# 1) 看档位（务必先看，确认最高档是否够用、是否需登录）
yt-dlp -F "https://v.qq.com/x/cover/<cid>/<vid>.html"

# 2) 下载 720P（shd-0；480P 用 hd-0）
yt-dlp -f "shd-0" --merge-output-format mp4 -o "out.mp4" \
       "https://v.qq.com/x/cover/<cid>/<vid>.html"

# 3) 必查编码，hevc 就转码
ffprobe -v error -show_entries stream=codec_name,codec_tag_string \
        -of default=noprint_wrappers=1 out.mp4
# 若 hevc/hev1 → 执行第 4 节的转码命令

# 4) 全片解码体检（0 行输出 = 无错误）
ffmpeg -v error -i out.mp4 -f null -
```

下载特征：HLS 分片约 99 个，实测约 2.15 MB/s，20 分钟片约 18 秒下完。

---

## 6. 校验清单

- [ ] `yt-dlp -F` 确认拿到的是本次可得的最高档
- [ ] **`codec_name` 是 `h264` 且 `codec_tag_string` 是 `avc1`**（关键！hevc 必须转码）
- [ ] 有音轨（`aac`）、时长正确
- [ ] `ffmpeg -v error -i out.mp4 -f null -` 输出 0 行
- [ ] 抽首/中/尾三帧看画面连贯、结尾正常收束
- [ ] 交用户播放验收

---

## 7. 何时需要人工介入

| 情况 | 处理 |
|---|---|
| `-F` 档位已满足需求（免费内容常见） | **全自动，不打扰用户** |
| `-F` 最高只有 480P 且页面弹会员 | 付费片源，走手动介入协议；按项目首选项**建议用户用「本地任务」模式新建会话**登录 |
| 页面弹验证码 / 滑动验证 | 立即停止自动化，交给用户 |

---

## 8. 与其它平台对比

| 维度 | 优酷 | 爱奇艺 | B站 | **腾讯视频** |
|---|---|---|---|---|
| 下载方式 | 浏览器拦截 + 并发 Range | 浏览器抓签名 URL | yt-dlp + cookie | **yt-dlp 直接下** |
| 取流接口是否风控 | 是（需 seek 采集） | 是（接口全 403/405） | 412（缺 cookie） | **否** |
| 未登录可得最高 | 低画质 | 720P（免费内容） | 480P | **720P（免费内容）** |
| 登录是否影响画质 | 是 | 免费内容否 | 是（1080P 需登录） | **免费内容否**（VIP 片待测） |
| 编码 | MP4 分片（H.264） | MPEG-TS（H.264） | DASH（H.264/AV1） | **HEVC(H.265) → 需转码** |
| 主要坑 | 分片号十六进制、漏片 | 接口风控、签名 CDN | 412 风控、短信登录被 Geetest 拦 | **HEVC 导致用户端只有声音没画面** |

---

## 9. 踩坑速查

| 坑 | 现象 | 解法 |
|---|---|---|
| **HEVC 坑（本平台头号坑）** | 我们这边能播，用户端只有声音没画面 | 交付前必查 `codec_name`，hevc → `libx264` 转码成 `avc1`（第 4 节） |
| 系统 ffmpeg 无 libx264 | `Codec 'libx264' is not recognized` | 用 `imageio_ffmpeg.get_ffmpeg_exe()` 那个静态 ffmpeg；或装带 x264 的构建 |
| libopenh264 体积大 | 20 分钟片 269 MB | 仅作备用；有条件就用 libx264（约 98 MB） |
| 误上浏览器重流程 | 白折腾、白等 | 腾讯 yt-dlp 原生支持，直接用，不要 seek 采集 |
| 一上来就要求登录 | 白白打断用户 | 先 `-F` 看档位；免费内容未登录即 720P，登录不改变结果 |
| `Unsupported URL` | 带某些查询参数时解析失败 | 去掉查询串，只留 `.../<vid>.html` |
