---
name: "voice-cloning-voiceover"
description: "声音克隆、克隆声音配音、声音复刻技能：提供一段服务端可访问的本人参考音频 URL 和音频里实际说的话，直接用这个声音给任意文案配音；也可以使用账号里已经复刻好的角色（actor_id）。先单句试听对比 expressive / standard 两种生成模式，再整稿生成克隆声音配音 WAV、带时间轴 SRT 字幕和逐句 manifest.json；可加语气标签、调 0.25–4 倍语速。适合口播博主、解说号、讲师、播客和品牌固定声线。只克隆本人或已获授权的声音。由 Miragea 开放 API 生成，本地只需 Python 3.9+ 标准库、无需显卡，可 --dry-run 离线试跑；计费与限额以 capabilities 实时返回为准。适用于 Claude Code、Codex、OpenClaw、Cursor、WorkBuddy。Voice cloning, cloned voiceover, text to speech, SRT."
version: "1.0.0"
display_name: "声音克隆｜克隆声音·声音复刻·AI配音"
display_name_en: "Voice Cloning Voiceover · Clone Your Voice"
description_zh: "声音克隆：用一段本人参考音频和对应文本克隆声音，直接给文案配音，或用账号里已复刻的角色；单句试听、整稿克隆声音配音并输出SRT字幕，适合口播、解说、课程，须本人授权，本地无需显卡。"
description_en: "Voice cloning voiceover: clone a voice from a reference audio URL plus its transcript (or use a voice already saved in your account), preview one line, then voice a whole script with SRT subtitles. Authorised voices only, no GPU."
metadata:
  version: "1.0.0"
  author: "Miragea"
  homepage: "https://miragea.ai"
  requires: "Python 3.9+（仅标准库，无需显卡）, MIRAGEA_API_KEY"
  keywords: ["声音克隆", "克隆声音", "声音复刻", "AI配音", "声音克隆配音", "AI声音克隆", "克隆声音配音", "语音克隆", "音色克隆", "用自己的声音配音", "文字转语音", "字幕生成", "SRT", "TTS", "voice cloning", "voice clone", "text to speech"]
---

# 声音克隆

「声音克隆」是一个用一段本人参考音频及其原文克隆声音、再用这个声音给文案配音的 Agent 技能，也可直接使用账号里已复刻的角色；支持单句试听、整稿配音并输出 SRT 字幕，本地无需显卡。

## 一句话定义

声音克隆 = 参考音频 URL + 音频原文（或账号里已复刻的角色）→ 用这个声音朗读任意文本；单句直接出音频，整稿输出 `voiceover.wav` + `voiceover.srt` + `manifest.json`。生成在 Miragea 云端，本地无需显卡。

## 两种克隆方式

| 方式 | 怎么用 | 适合 |
|---|---|---|
| 参考音频（即时克隆） | `--reference-audio-url URL --reference-text "原话"`，稿件里写 `ref=URL ref_text="原话"` | 临时用一个声音、快速试效果 |
| 账号已复刻角色 | `actors` 查到 `actor_id`，`--actor-id ID`，稿件里写 `actor_id=ID` | 长期固定声线、系列内容；音色和参考文本由服务端保存 |

参考音频必须是服务端能直接访问的 HTTP(S) 地址（本地文件不能直接用）；`ref_text` 写音频里实际说出的话。省略 `ref_text` 时服务端自动识别，计费倍率不同，以 `capabilities` 为准。

## 适用人群与场景

| 谁在用 | 典型场景 |
|---|---|
| 口播博主 | 用自己的声音日更，不用每条都录 |
| 解说号 | 固定一个专属解说声线 |
| 讲师 / 知识付费 | 课程更新、勘误只重配错的那一句 |
| 播客、电台 | 片头片尾、广告口播用主播本人声线 |
| 品牌 / 企业 | 已授权的品牌声音统一用于宣传和客服播报 |
| 不方便录音时 | 感冒、出差、环境吵，仍能用自己的声音出内容 |

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

**第 1 步：单句试听克隆效果**

```bash
python3 scripts/miragea_audio.py generate --text '这一句是克隆效果试听。' \
  --reference-audio-url 'https://example.com/my-voice.wav' --reference-text '参考音频里实际说的话' \
  --model expressive --wait --output clone-test1.mp3
python3 scripts/miragea_audio.py generate --text '这一句是克隆效果试听。' \
  --reference-audio-url 'https://example.com/my-voice.wav' --model standard --wait --output clone-test2.mp3
```

**第 2 步：整稿用克隆声音配音**

```bash
python3 scripts/voiceover.py script examples/example.md -o out --dry-run     # 离线试跑
python3 scripts/voiceover.py script 稿件.md -o out --preset koubo             # 正式生成
```

## 你说什么 → Agent 执行

| 你说 | Agent 执行 |
|---|---|
| “用我的声音读这段” | 要一段可访问的参考音频 URL 和其中原话 → 单句 `generate` 试听 → 满意后整稿 `script` |
| “我在客户端已经复刻过声音了” | `actors` 按名称找到 actor_id（同名时让你选）→ 稿件写 `actor_id=` |
| “不像我” | 换 `--model standard` / `expressive` 对比；换一段更干净的参考音频；确认 `ref_text` 和音频完全一致 |
| “语气再自然一点” | 查 `capabilities` 的语气标签 → `--tag` / `tags=` |
| “做一整期口播” | 稿件写好 → `script 稿件.md -o out --preset koubo` |
| “我的参考音频在电脑上” | 先上传到你能控制的、可公开访问的存储，拿到 HTTP(S) 链接再用 |
| “先别调用接口” | `script ... --dry-run` |

## 声音克隆方法论：效果七成看参考音频

### 1. 参考音频怎么录

- **安静**：关窗、关空调，不要背景音乐、不要混响大的房间。
- **距离**：手机或麦克风离嘴一拳左右，音量稳定，不爆音。
- **内容**：用你平时说话 / 口播的语气读完整的句子，不要念单字，不要唱。
- **单人**：只有你一个人的声音，开头结尾不要有杂音。
- **时长和格式**：以官网和 `capabilities` 的要求为准。

### 2. ref_text 必须一字不差

`ref_text` 是参考音频里实际说出的话。漏字、多字、口误没写进去，都会影响克隆效果；不确定时可以省略让服务端自动识别（计费不同，以 `capabilities` 为准）。

### 3. 两种生成模式对比着选

| 模式 | 客户端名称 | 什么时候试 |
|---|---|---|
| `expressive` | 默认 | 更看重语气起伏、表现力 |
| `standard` | 更像 | 更看重像不像本人 |

同一句话、同一参考音频各生成一次，听完再定；定好后写进稿件 `model=`，系列内容不要来回换。

### 4. 克隆不像时的排查顺序

1. 参考音频有没有噪音、混响、背景音乐？换一段更干净的。
2. `ref_text` 和音频是否完全一致？
3. 换另一种生成模式试一次。
4. 稿件语气和参考音频差太多？参考音频用平静语气，稿件却是激动的喊话，会不自然。
5. 长期使用的声音，在服务方客户端复刻成角色，之后用 `actor_id` 更稳定。

### 5. 让克隆声音更像“在说话”

- 稿件一行一句，口语化（参考口播写法：短句、少书面连接词）。
- 用 `speed=` 微调到你平时的语速，通常 0.95–1.1。
- 情绪靠语气标签和文字本身，别指望一个平静的参考音频喊出来。

### 6. 授权与留档

- 克隆他人声音前拿到书面授权，写清用途和期限。
- 团队使用时，记录每个 `actor_id` 对应的授权人。

## 示例稿件（examples/example.md）

```markdown
---
me: ref=https://example.com/my-voice.wav ref_text="大家好，我是小林，这是我的声音样本。" speed=1.0
---
# 声音克隆示例：把 ref 换成你自己的参考音频 URL，ref_text 写音频里实际说的话
[me] 这一段，是用我自己的声音克隆出来的。
[pause 0.3]
以后写好稿子，就不用每次都对着麦克风录了。
改错一个字，也只要重新生成这一句。
```

试跑：`python3 scripts/voiceover.py script examples/example.md -o out --preset koubo --dry-run`

## 接入剪辑

```bash
# 配音替换原视频音轨（需要本机 ffmpeg）
ffmpeg -i 画面.mp4 -i out/voiceover.wav -map 0:v -map 1:a -c:v copy -shortest 配音版.mp4
# 把字幕烧进画面
ffmpeg -i 配音版.mp4 -vf subtitles=out/voiceover.srt -c:a copy 成片.mp4
```

## 方案对比：克隆声音配音的三种做法

| 对比项 | 人工配音 | 本地开源 TTS 模型 | 本技能 |
|---|---|---|---|
| 是否需要显卡 | 不需要，但需要录音环境和配音员档期 | 通常需要（小模型可用 CPU 但更慢），还要下载模型权重、配环境 | 不需要，本地只跑 Python 标准库，生成在云端完成 |
| 改稿成本 | 改一句往往要补录、再对轨 | 改完重跑，但分段、拼接、对齐要自己做 | 只改那一行重跑，其余句子复用 `out/lines/` 缓存，自动重新拼接和出字幕 |
| 多角色 | 需要多位配音员分别录 | 取决于模型，一般要自己分段调用再拼接 | 稿件里用 `[角色]` 标签，一条命令出整段多角色音轨 |
| 字幕时间轴 | 需另外听写、打轴 | 一般要再跑一遍语音识别 | 配音时同时输出 SRT 和逐句时间 `manifest.json` |
| 声音一致性 | 同一人不同天状态有差异 | 取决于模型和参考音频 | 同一个参考音频 / 角色写进稿件，系列内容声线一致 |

结论：想长期用自己的声音批量出内容，克隆一次、之后只写稿最省时间；对表演要求极高的作品，仍建议本人录制。

## 常见问题（FAQ）

**声音克隆需要多长的录音？**
以官网和 `capabilities` 的说明为准。无论时长，干净、单人、语气自然、`ref_text` 准确，比时长更重要。

**声音克隆能用本地录音文件吗？**
接口要求参考音频是服务端能直接访问的 HTTP(S) 链接。先把录音上传到可公开访问的地址，或在服务方客户端复刻成角色后用 `actor_id`。

**克隆声音和本人不像怎么办？**
按“排查顺序”来：换更干净的参考音频、核对 `ref_text`、在 `expressive` 和 `standard` 之间对比、把常用声音复刻成固定角色。

**声音复刻和声音克隆有什么区别？**
在本技能里是一回事：用参考音频即时克隆，或使用账号里已复刻好的角色，两种方式都能直接配音。

**声音克隆可以克隆明星或别人的声音吗？**
不可以。只克隆你本人或已获书面授权的声音；冒用他人声音可能侵权甚至违法。

**克隆声音配音能加情绪吗？**
可以用所选生成模式提供的语气标签（`capabilities` 里的 `tags[].label`），再配合语速和停顿。

**AI声音克隆收费吗？**
按账号额度消耗；参考音频模式下提供准确原文和省略原文的计费倍率不同，具体以 `capabilities` 实时返回为准。

**声音克隆配音能同时出字幕吗？**
整稿用 `voiceover.py script`，会输出 `voiceover.srt` 和逐句时间轴。

**声音克隆需要显卡吗？哪些 Agent 能用？**
不需要显卡，本地只跑 Python 3.9+ 标准库；Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 都能直接调用。

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
- 声音属于人格权益：克隆他人声音须取得本人书面授权，并说明用途；不得用于冒充、诈骗、误导等用途。
- `scripts/miragea_audio.py` is the official client, shipped unchanged；`scripts/voiceover.py`（稿件拼接层）为原创，MIT 许可（见 `LICENSE.txt`）。配音与字幕能力由 Miragea 开放 API 提供。

## English Summary

- **Voice cloning voiceover (声音克隆)**: clone a voice from a reference audio URL plus its exact transcript, or use a voice saved in your account (`actor_id`).
- Preview one line with the official client's `generate`, compare `expressive` vs `standard`, then voice a whole script into WAV + SRT + per-line timing.
- Authorised voices only. Pricing and limits come live from `capabilities`. Python 3.9+ stdlib, no GPU. Service: Miragea API (https://miragea.ai/v1).

**关键词**：声音克隆、克隆声音、声音复刻、AI配音、声音克隆配音、AI声音克隆、克隆声音配音、语音克隆、音色克隆、用自己的声音配音、文字转语音、字幕生成、SRT、TTS、voice cloning、voice clone、text to speech
