---
name: video-viral-pipeline
description: 把一条外语长视频一键做成中文字幕成片，并自动切成多条"独立成爆款"的 9:16 竖屏短片（带钩子标题+gpt-image 封面），可选一键发布到微信视频号 / 抖音 / 小红书 / 公众号四个平台。当用户说"翻译视频并切片""做爆款切片""视频号一条龙""发抖音小红书""把这个 YouTube 链接做成短视频矩阵"时使用。
---

# video-viral-pipeline 外语视频 → 爆款竖屏切片 → 视频号一条龙

`{baseDir}` = 本 SKILL.md 所在目录，执行脚本时替换为绝对路径。

## 能做什么

输入一个视频链接（YouTube / 本地文件）→ 输出：
1. **中英双语字幕成片**（整片）
2. **N 条 9:16 竖屏爆款短片**：每条是一个自包含的爆点，顶部烧中文钩子大标题，背景模糊填充
3. **每条独立封面图** + 把封面作为 1.5s **封面帧**拼到片头
4. （可选）**自动发布到微信视频号**，（可选）公众号深度文排版+推草稿

## 前置依赖（首次）

跑 `bash {baseDir}/scripts/setup.sh` 安装。核心要求：
- `yt-dlp`（下载）
- **`ffmpeg-full`**（必须带 libass/freetype；macOS 上 Homebrew 常规 `ffmpeg` 是精简版烧不了字幕，要 `brew install ffmpeg-full`，脚本会自动探测 `/usr/local/opt/ffmpeg-full/bin/ffmpeg`）
- **faster-whisper** 装在独立 `python3.12` venv（`~/.vvp-whisper`；Python 3.14 无 wheel）。转写脚本若当前 `python3` 没引擎需 re-exec 到该 venv。
- 翻译/选片/文案由**调用方 Claude** 完成（本 skill 是编排 + 确定性媒体脚本）。
- （可选）视频号发布：`social-auto-upload`（patchright 浏览器自动化，需手机扫码登录）。

## 完整流程

### 步骤 0 · 确认意图与参数
- 拿到链接/路径。**超长视频（>30 min）先问清范围**：整片 / 前 N 分钟 / 指定区间。在 CPU 上转写约 2x 实时，2 小时视频转写就要约 1 小时，要提醒用户。
- 字幕类型若用户没明说，问：中文 / 中英双语。

### 步骤 1 · 下载
```bash
yt-dlp --cookies-from-browser chrome -f "bv*[height<=1080]+ba/b[height<=1080]" \
  --merge-output-format mp4 -o "<tmp>/源.%(ext)s" "<URL>"
```
- YouTube 报"Sign in to confirm you're not a bot"→ 加 `--cookies-from-browser chrome`。
- 只要片段时可用 `--download-sections "*0-180"`；整片就别用。
- yt-dlp 偶尔不自动合并音视频流 → 用 ffmpeg-full 手动 `-map 0:v:0 -map 1:a:0 -c copy` 合并。

### 步骤 2 · 提取音频 + Whisper 转写
```bash
ffmpeg-full -i 源.mp4 -vn -acodec libmp3lame -q:a 2 源.mp3
<whisper-venv>/bin/python transcribe_srt.py 源.mp3 --output 源.srt --engine faster --language en
```
得到带精确时间戳的英文 SRT。

### 步骤 3 · 翻译润色（双语 SRT）
- 逐条翻成**中文在上、英文在下**，时间戳一对一，不合并不拆分。
- 中文行**去标点**（口语、停顿用空格）、专有名词保留英文、中英之间加空格。
- 长视频（数千条）**分块并行**：切成 ~8 块，并行 agent 各译一块，再合并、校验编号连续、补漏译、规范时间戳（小时位补零）。

### 步骤 4 · 烧字幕成片
- 双语先转 ASS（中文大/英文小，约 1.7 倍反差），再 `ass=` 滤镜烧录；**音频强制 `-c:a aac`**（别 copy，Opus 在部分平台传不了）。
- 烧完**抽 ≥2 帧验证**：中文非方块、双语反差清晰、不遮挡。

### 步骤 5 · 选爆款片段（关键，靠 agent 判断）
从整片 SRT 里挑 N 个**能独立成爆款**的片段。判据：
1. **3 秒内有钩子**（炸裂的一句 / 强反差）
2. **自包含**：零前文也看懂
3. **有情绪或反认知爆点**：脆弱坦白 / 惊人数字 / 狂言 / 催泪 / 干货
4. **30–90 秒**，结尾落在金句上
覆盖不同传播人群（故事/干货/催泪/狂言/反差各来一条）。
> 长视频建议**派并行 agent**：每个 agent 给一个主题+大致时间窗，读 SRT 返回**精确起止时间码 + ≤15 字中文钩子标题**。

把结果写成 `clips.json`（见 `{baseDir}/examples/clips.example.json`）：每条含 `start/end/hook/cover_title/cover_frac/name`。

### 步骤 6 · 渲染竖屏切片
```bash
python3 {baseDir}/scripts/render_clips.py --config clips.json
```
→ `<output_dir>/<name>.mp4`：9:16、模糊填充、顶部钩子大标题、保留双语字幕。

### 步骤 7 · 封面 + 封面帧
```bash
python3 {baseDir}/scripts/render_covers.py  --config clips.json   # 出封面图到 封面/
python3 {baseDir}/scripts/prepend_covers.py --config clips.json   # 把封面拼成 1.5s 片头
```
- 封面取**干净无字幕源帧**（`clean_video`），`cover_frac` 控制取帧点——确保取到主角正脸（切到他人镜头就调 frac）。
- **封面标题是爆款命门**：用反差/悬念/数字/提问，≤2 行。务必和用户确认或给选项。**文案要把产品名+独门能力顶在最前，别稀释成泛泛"AI神器"。**

#### 步骤 7b（强烈推荐）· 用 gpt-image 出真正的爆款封面
ffmpeg 封面只能做到约 85%；真正头部的封面用 **AI 生图**。本 skill 内置 `scripts/gen_covers_ai.py`（gpt-image-2，经 Ofox 中转，中文渲染准确）：
```bash
unset http_proxy https_proxy all_proxy   # ⚠️ 必须直连，走代理大图会 SSL EOF
OFOX_API_KEY=... python3 {baseDir}/scripts/gen_covers_ai.py --config covers.json
```
- 两种已验证有效的赛道风格：`"style":"cyber"`（深色霓虹+发光终端+光带分割，点击力最强）/ `"soft"`（奶油薄荷圆角卡片+扁平图标，小红书原生）。
- `covers.json` 每条配 `eyebrow/title/highlight/subtitle/terminal`，见 `examples/covers.example.json`。
- 出 1024×1536（2:3），脚本自动在 `3x4/` 生成 3:4 版（黑底补边不裁字）适配小红书。
- **拆解小红书爆款**：3:4、色调统一、明确主体+留白、0.5 秒传递情绪、标题=数字/提问/痛点。

### 步骤 8（可选）· 发布到四个平台
视频号/抖音/小红书都经 `social-auto-upload`（浏览器自动化，无官方 API）。每个平台**首次各需扫码登录一次**（`examples/get_<平台>_cookie.py` 生成二维码 png → 对应 App 扫；二维码几分钟失效，准备好再生成）。**一律先发 1 条试水，确认无异常再小批量。**

| 平台 | 脚本 | 稳定度 / 要点 |
|---|---|---|
| **视频号** | `scripts/publish_shipinhao.py` | 最稳。**用「直接发表」**（`is_draft=False`）；草稿路径选择器在新版助手下超时。`publish.json` 每条 `title/short_title(6-16字)/tags/thumbnail`。 |
| **抖音** | `scripts/publish_douyin.py` | 可用，自动加封面/原创声明。登录扫码偶尔磨叽。`item` 有 `thumbnail` 则用作竖封面。 |
| **小红书** | `scripts/publish_xiaohongshu.py` | **风控最严**。标题≤20字；**小批量+大间隔(≥90s)+先试1条**；会自动勾原创声明（搬运慎用）；偶发 `Locator timeout` 多为限流信号，**一出现就停**。 |

```bash
cd <social-auto-upload>
PYTHONPATH=. .venv/bin/python {baseDir}/scripts/publish_douyin.py --config publish.json --idx 1
```
`publish.json` 每条配 `file/title/tags/desc/thumbnail`（thumbnail 指向 gpt-image 封面，建议小红书用 3:4）。

**公众号**（图文，非视频）：用 `xiaohu-wechat-format` 技能排版深度文 + 2.35:1 封面 + `publish.py` 推**草稿**（需 app_id/secret + IP 白名单 + **已认证服务号/订阅号**；个人未认证号无接口权限）。

## ⚠️ 注意事项 / 风险
- **视频号/抖音/小红书均无官方发布 API**，发布是浏览器自动化、属灰色地带、**有账号被限流/封禁风险**；翻译搬运他人视频还涉及版权。**风控严格度：小红书 > 抖音 > 视频号**。务必**先试 1 条、小批量、错峰**，账号风险自负。
- **gpt-image 封面必须直连**：`unset http_proxy https_proxy all_proxy` 后再调 Ofox；走本地代理大图常 SSL EOF / Connection refused（脚本已加重试）。模型名是 `gpt-image-2`（gpt-image-1 在 Ofox 上 404）。
- ffmpeg 必须带 libass，否则 `ass=`/`subtitles=` 滤镜报错。
- CPU 转写慢；GPU（Apple Silicon 用 mlx-whisper）会快很多。
- 国内网络下 HuggingFace 模型下载不稳，建议 curl 续传预下模型到 `~/.cache/xh-models/`。
- 自检：每个产物（成片/切片/封面）都抽帧或核对，别只靠脚本退出码。

## 配置文件
- `clips.json` — 切片+封面配置，结构见 `examples/clips.example.json`
- `publish.json` — 视频号发布配置，结构见 `examples/publish.example.json`
