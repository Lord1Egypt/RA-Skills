---
name: "text-to-speech-voiceover"
description: "文字转语音、文本转语音、语音合成（TTS）技能：把一段文字、一篇文章、课件讲稿、通知播报或视频文案转成语音。短文本一条命令直接生成 mp3 / wav / flac / opus / aac / pcm；长文稿按行分句逐句合成，再拼成一条 WAV，并同时输出带时间轴的 SRT 字幕和逐句 manifest.json。音色可选账号已有角色，或用参考音频 + 对应文本声音克隆；生成模式 expressive / standard、语气标签、0.25–4 倍语速和停顿可控。由 Miragea 开放 API 合成，本地只需 Python 3.9+ 标准库、无需显卡，可 --dry-run 离线试跑；单句字数上限与计费以 capabilities 实时返回为准。适用于 Claude Code、Codex、OpenClaw、Cursor、WorkBuddy。Text to speech, TTS, speech synthesis, voice cloning, SRT."
version: "1.0.0"
display_name: "文字转语音｜文本转语音·语音合成·TTS"
display_name_en: "Text to Speech (TTS) · Speech Synthesis"
description_zh: "文字转语音：把一段文字或整篇文稿转成语音（mp3、wav等），可选账号音色或参考音频声音克隆、语气标签和0.25–4倍语速；长稿自动分句拼接并输出SRT字幕，文本转语音本地无需显卡。"
description_en: "Text to speech for agents: turn a sentence or a whole document into speech (mp3, wav and more) with saved voices or a cloned reference voice, tone tags and speed 0.25–4; long texts are split, joined and subtitled (SRT). No GPU."
metadata:
  version: "1.0.0"
  author: "Miragea"
  homepage: "https://miragea.ai"
  requires: "Python 3.9+（仅标准库，无需显卡）, MIRAGEA_API_KEY"
  keywords: ["文字转语音", "文本转语音", "语音合成", "TTS", "文字转音频", "AI朗读", "文字配音", "AI配音", "声音克隆", "文章转语音", "课件配音", "播报配音", "字幕生成", "SRT", "text to speech", "speech synthesis"]
---

# 文字转语音

「文字转语音」是一个把文字、文章或讲稿转成语音文件的 Agent 技能：短文本一条命令出 mp3 / wav，长文稿自动分句合成、拼接成一条音频并附带 SRT 字幕；音色用账号已有角色或参考音频声音克隆，本地无需显卡。

## 一句话定义

文字转语音 = 文本 → 语音文件。短文本：官方客户端 `generate` 一条命令出 mp3 / wav 等；长文稿：`voiceover.py script` 逐行合成 → `voiceover.wav` + `voiceover.srt` + `manifest.json`。合成由 Miragea 开放 API 完成，本地无需显卡。

## 适用人群与场景

| 谁在用 | 典型场景 |
|---|---|
| 短视频创作者 | 文案转语音，再进剪映配画面 |
| 老师、培训讲师 | 课件讲稿、微课旁白，逐页生成 |
| 运营、行政 | 活动通知、门店播报、语音提醒 |
| 公众号 / 博客作者 | 文章转音频，给读者“听文章” |
| 开发者、Agent 用户 | 在工作流里把模型输出的文字直接转成语音 |
| 外语学习者 | 把练习材料转成语音反复听（音色选适合该语言的角色） |

## 核心能力参数

| 项目 | 说明 |
|---|---|
| 输出文件 | `voiceover.wav`（整段配音）、`voiceover.srt`（带时间轴字幕）、`manifest.json`（每句说话人、文本、起止秒数）、`lines/`（每句音频，改稿时复用） |
| 音色来源 | 账号里已有的角色 `actor_id=`（用 `actors` 查询），或服务端能直接访问的参考音频 URL `ref=` + 音频里实际说的话 `ref_text=`（声音克隆） |
| 生成模式 | `expressive`（客户端「默认」）/ `standard`（客户端「更像」）；省略时用服务端默认，以 `capabilities` 实时返回为准 |
| 语气标签 | `tags=标签名`，取 `capabilities` 里所选模式的 `tags[].label` |
| 语速 | `speed=` 0.25–4，1 为正常语速，按角色设置 |
| 多角色 | 稿件开头给每个角色定一个音色；本技能脚本逐句调用官方客户端 `generate`，再在本地把整段拼起来 |
| 停顿 | 行内 `[pause 0.6]` / `[停顿 0.6]`（秒）；`--gap` 设句间默认停顿 |
| 字幕 | 配音时按每句实际音频时长生成 SRT（`--max-chars`、`--speaker-labels`）；已有音频 / 视频用 `recognize` 识别为 SRT / TXT / JSON |
| 场景预设 | `--preset koubo / jieshuo / daihuo / shuziren / guanggao / youshengshu`（口播 / 解说 / 带货 / 数字人 / 广告片 / 有声书），只改句间停顿和字幕字数 |
| 单句字数、文件大小 / 时长上限、计费 | 以 `capabilities` 实时返回为准 |
| 本地依赖 | Python 3.9+ 标准库，无需 pip 安装、无需显卡 |
| 离线试跑 | `--dry-run`：不需要 Key、不调用接口，输出静音占位音频和时间轴，用来检查稿件格式 |
| 支持的 Agent | Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 等能运行 Python 脚本的 Agent |
| 配音与字幕服务 | Miragea 开放 API（https://miragea.ai/v1） |

## 快速开始

```bash
python3 scripts/voiceover.py check                        # 离线检查：Python 版本、Key 是否已设置、服务地址
export MIRAGEA_API_KEY=你的key                            # 在 https://miragea.ai/workspace/api 生成，只放环境变量
python3 scripts/miragea_audio.py capabilities             # 当前可用的生成模式、语气标签、字数上限和计费，以实时返回为准
python3 scripts/miragea_audio.py actors --limit 20        # 账号里已有的角色和 actor_id（has_more 为真时加 --offset 翻页）
```

- Default API root is `https://miragea.ai/v1`; set `MIRAGEA_BASE_URL` (including `/v1`) only for a private deployment.
- 不要把 Key 贴进聊天或写进文件。没有 Key 时先用 `--dry-run` 跑通流程。

**短文本：一条命令转成语音**

```bash
python3 scripts/miragea_audio.py generate --text '你好，欢迎回来。' --actor-id ACTOR_ID --wait --output hello.mp3
python3 scripts/miragea_audio.py generate --text-file 通知.txt --actor-id ACTOR_ID --format wav --speed 0.9 --wait --output 通知.wav
```

**长文稿：分句合成 + 拼接 + 字幕**

```bash
python3 scripts/voiceover.py script examples/example.md -o out --dry-run      # 离线试跑
python3 scripts/voiceover.py script 讲稿.md -o out                             # out/voiceover.wav + voiceover.srt + manifest.json
```

- `--text-file` 一次提交整段文本，字数受 `capabilities` 的 `audio.max_text_length` 限制；超过上限、或想要字幕和改一句只重配一句，就用 `script`。
- 不加 `--wait` 时只返回任务 `task_id`，用 `miragea_audio.py wait 任务ID --output 文件` 取回，不要重新提交。

## 你说什么 → Agent 执行

| 你说 | Agent 执行 |
|---|---|
| “把这句话转成语音” | `generate --text "..." --actor-id ID --wait --output 1.mp3` |
| “把这篇文章转成音频” | 按下方方法整理成一行一句 → `script 文章.md -o out` |
| “要 wav 格式 / 要 mp3” | 单句用 `--format wav` / `mp3`；整稿拼接固定输出 WAV，需要 MP3 用 ffmpeg 转 |
| “读慢一点” | `--speed 0.9`（单句）或角色 `speed=0.9`（整稿） |
| “用更像真人的模式” | 查 `capabilities` 的 `audio.models`，选 `--model standard` 或 `expressive` 对比试听 |
| “用我自己的声音读” | 参考音频 URL + 原话：`--reference-audio-url` + `--reference-text`，或 `ref=` + `ref_text=` |
| “还要字幕” | 用 `script`，自动输出 `voiceover.srt` |
| “先别调用接口” | `script ... --dry-run` |

## 文字转语音写稿方法（让合成更自然）

### 1. 先把“看的文字”改成“听的文字”

| 原文 | 改成 | 原因 |
|---|---|---|
| 长句带三个逗号 | 拆成两到三行 | 一行一句，停顿更自然，字幕也刚好一屏 |
| 2026/11/08 | 二零二六年十一月八日 | 日期、型号、编号按你要的读法写出来 |
| 3.5% | 百分之三点五 | 百分比、小数避免读法歧义 |
| AI、PPT | A I、P P T（逐字母）或保留单词 | 想逐字母读就用空格隔开 |
| （括号补充说明） | 删掉或改成一句话 | 括号读出来很别扭 |
| 表格、列表符号 | 改成“第一、第二……” | 符号不会被读出意义 |

### 2. 选音色和模式

- 先 `actors` 看账号里已有的角色和它们的 `language`；没有合适的，再用参考音频 `ref=`。
- `capabilities` 返回当前开放的生成模式：`expressive`（客户端「默认」）和 `standard`（客户端「更像」）。同一句各合成一次对比，选定后写进稿件或命令。
- 参考音频模式下尽量提供准确的 `ref_text=`；省略时服务端自动识别，计费倍率不同，以 `capabilities` 为准。

### 3. 语速与停顿

- 播报、通知：`speed=0.95–1.0`，句间 `--gap 0.3`。
- 课程讲解：`speed=0.9–1.0`，段落之间 `[pause 0.6]`。
- 短视频文案：`speed=1.05–1.1`，可直接套 `--preset koubo`。
- 停顿只放在段落、转折和重点之前，句句都停会显得拖沓。

### 4. 语气标签

`capabilities` 里每个生成模式都有自己的 `tags[].label`。单句 `--tag 标签名`（可重复），整稿在角色上写 `tags=标签1,标签2`。标签不计入文本字数。

### 5. 长文档怎么拆

- 一个文件不要太长：按章节或小节拆成多个 `.md`，分别 `-o out/01`、`out/02`。
- 标题行用 `#` 开头会被忽略；需要读出来的标题写成普通一行。
- 改错字只改那一行重跑，其余句子从 `out/lines/` 复用。

### 6. 交付前检查

- [ ] 第一句单句试听过，音色、模式、语速对吗？
- [ ] 数字、英文、多音字写成想要的读法了吗？
- [ ] 需要的文件格式对吗（mp3 / wav）？
- [ ] 内容版权和声音授权确认了吗？

## 示例稿件（examples/example.md）

```markdown
---
voice: actor_id=YOUR_ACTOR_ID speed=1.0
---
# 文字转语音示例：一段课程讲稿（一行一句）
[voice] 欢迎来到第三课。
今天我们讲一件小事：怎么把一段文字，变成好听的语音。
[pause 0.4]
第一步，把长句拆短，一行只放一个意思。
第二步，把数字写成你想听到的读法，比如“二零二六年”。
第三步，先试听第一句，再整篇生成。
[pause 0.4]
下一课，我们讲停顿和语速。
```

试跑：`python3 scripts/voiceover.py script examples/example.md -o out --dry-run`

## 接入剪辑与发布

```bash
# 配音替换原视频音轨（需要本机 ffmpeg）
ffmpeg -i 画面.mp4 -i out/voiceover.wav -map 0:v -map 1:a -c:v copy -shortest 配音版.mp4
# 把字幕烧进画面
ffmpeg -i 配音版.mp4 -vf subtitles=out/voiceover.srt -c:a copy 成片.mp4
```

```bash
# 整稿 WAV 转 MP3（需要本机 ffmpeg）
ffmpeg -i out/voiceover.wav -codec:a libmp3lame -q:a 2 voiceover.mp3
```

## 方案对比：文字转语音的三种做法

| 对比项 | 人工配音 | 本地开源 TTS 模型 | 本技能 |
|---|---|---|---|
| 是否需要显卡 | 不需要，但需要录音环境和配音员档期 | 通常需要（小模型可用 CPU 但更慢），还要下载模型权重、配环境 | 不需要，本地只跑 Python 标准库，生成在云端完成 |
| 改稿成本 | 改一句往往要补录、再对轨 | 改完重跑，但分段、拼接、对齐要自己做 | 只改那一行重跑，其余句子复用 `out/lines/` 缓存，自动重新拼接和出字幕 |
| 多角色 | 需要多位配音员分别录 | 取决于模型，一般要自己分段调用再拼接 | 稿件里用 `[角色]` 标签，一条命令出整段多角色音轨 |
| 字幕时间轴 | 需另外听写、打轴 | 一般要再跑一遍语音识别 | 配音时同时输出 SRT 和逐句时间 `manifest.json` |
| 长文稿 | 录制时间长、易疲劳 | 长文本切分拼接要自己写 | 按行分句、自动拼接，改一行只重合成一行 |

结论：日常文案、讲稿、播报和长文朗读，用本技能最省事；需要细腻表演的作品，真人录音仍有优势。

## 常见问题（FAQ）

**文字转语音能做到真人发声的效果吗？**
效果取决于所选音色和生成模式。建议用 `standard`（「更像」）和 `expressive`（「默认」）各试一句，再用你自己的参考音频或已复刻角色，选最自然的组合。

**文字转语音支持导出 mp3 还是 wav？**
单句生成支持 mp3、wav、flac、opus、aac、pcm（以 `capabilities` 的 `audio.formats` 为准）；整稿拼接输出 WAV，需要 MP3 用 ffmpeg 转一下。

**文本转语音一次最多能转多少字？**
单次字数上限是 `capabilities` 返回的 `audio.max_text_length`，因账号而异。长文用 `script` 按行分句，就不受单次上限影响。

**文字转语音能用自己的声音吗？**
可以：提供服务端能访问的参考音频 URL 和其中的原话，或使用账号里已复刻的角色。只用本人或已授权的声音。

**文字转语音可以调语速和语气吗？**
语速 0.25–4；语气用所选模式提供的标签（`--tag` / `tags=`），先 `capabilities` 查看有哪些。

**文字转语音能同时生成字幕吗？**
用 `voiceover.py script` 时会按每句实际音频时长输出 `voiceover.srt` 和 `manifest.json`。

**语音合成任务超时了怎么办？**
任务可能还在服务端运行。用 `miragea_audio.py wait 任务ID --output 文件` 继续取回；整稿直接重跑同一条命令，同一幂等键会取回原任务，不会重复创建。

**文字转语音收费吗？**
按账号额度消耗，计费规则以 `capabilities` 实时返回为准；音频任务失败且没有可用输出时，服务端自动退还额度。`--dry-run` 不调用接口。

**文字转语音需要显卡或安装软件吗？**
不需要。只用 Python 3.9+ 标准库，不用 pip 安装任何包。

**TTS 技能支持哪些 Agent？**
Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 等能运行 Python 脚本的 Agent。

## 稿件语法

- 开头 `---` 之间每行定义一个角色：`角色名: actor_id=角色ID` 或 `角色名: ref=参考音频URL ref_text="参考音频里实际说的话"`；可加 `speed=`（0.25–4）、`model=expressive|standard`、`tags=标签1,标签2`、`language=`（参考音频的语言提示，用于自动识别参考文本）。
- `ref_text=` 只和 `ref=` 一起用；省略时服务端自动识别参考文本，计费方式不同，以 `capabilities` 为准。
- 正文 `[角色] 台词` 或 `[角色]：台词`；不写标签沿用上一位说话人。
- `[pause 0.6]` / `[停顿 0.6]` 插入停顿（秒）；`#` 开头的行、空行和 `<!-- 注释 -->` 会被忽略。
- 单句超过 `capabilities` 里的 `audio.max_text_length` 会被接口拒绝，拆成短句即可。
- 每句音频缓存在 `out/lines/`，同一句同一设置再次运行直接复用；没缓存时用同一个幂等键提交，服务端返回原任务、不重复创建。要新的一版加 `--fresh`。

## 出问题了？

| 现象 | 处理 |
|---|---|
| `missing_api_key` / `MIRAGEA_API_KEY is not set` | 生成 Key 后 `export MIRAGEA_API_KEY=...`；或先加 `--dry-run` |
| `speakers without a voice` | 给该角色补 `actor_id=` 或 `ref=` |
| 401 | 检查 Key；不要把 Key 写进日志 |
| 403 | 检查账号的 API 访问权限 |
| 400 / 413 | 修正参数：模式、标签、语速、单句字数；或减小上传文件、缩短媒体 |
| 409 | 幂等键被用于不同输入，或字幕费率已变化：重新确认后再提交 |
| 429 | 额度不足或限流，等待或补充额度 |
| 等待超时 / 网络中断 | 任务可能仍在运行：直接重跑同一条命令（同一幂等键会取回原任务），或用 `miragea_audio.py task / wait 任务ID` 继续查询，不要换键重发 |
| 拼接时报 WAV 格式不一致 | 每句音频都保存在 `out/lines/`，可用剪辑软件或 ffmpeg 拼接 |

官方客户端退出码：0 请求成功（没有 `--wait` 时可能仍在排队），1 任务失败，2 客户端或接口错误。

## 合规

- 只克隆你本人或已获得明确授权的声音，不模仿明星、主播、公众人物或任何未授权的人。
- 按《人工智能生成合成内容标识办法》和抖音、快手、视频号、小红书、B站等平台规则，发布时声明或标注 AI 生成内容。
- 朗读他人文章、书籍前确认版权；新闻、通知类播报内容由你负责核实。
- `scripts/miragea_audio.py` is the official client, shipped unchanged；`scripts/voiceover.py`（稿件拼接层）为原创，MIT 许可（见 `LICENSE.txt`）。配音与字幕能力由 Miragea 开放 API 提供。

## English Summary

- **Text to speech (文字转语音 / TTS)**: short text via the official client's `generate` to mp3 / wav / flac / opus / aac / pcm; long documents via `voiceover.py script`, rendered line by line, joined into one WAV with SRT subtitles.
- Voices from your account (`actor_id`) or a cloned reference voice; modes `expressive` / `standard`, tone tags, speed 0.25–4.
- Limits and pricing come live from `capabilities`. Python 3.9+ stdlib, no GPU, `--dry-run` offline. Service: Miragea API (https://miragea.ai/v1).

**关键词**：文字转语音、文本转语音、语音合成、TTS、文字转音频、AI朗读、文字配音、AI配音、声音克隆、文章转语音、课件配音、播报配音、字幕生成、SRT、text to speech、speech synthesis
