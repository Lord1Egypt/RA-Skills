---
name: video-en2zh-dub
description: 把英文视频变成中文配音视频，也支持生成中英双音轨。当用户提出"把这个视频翻译成中文/中文化/视频汉化"、"给视频配中文音/中文解说"、"提取字幕并翻译"、"英文视频转中文"、"给视频加一条中文音轨"等需求时使用。执行四步流水线，whisper 转写英文字幕、大模型翻译为中文字幕、edge-tts 合成中文配音、ffmpeg 音画合并，产出中文配音版 mp4。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [ffmpeg, ffprobe]
    install:
      - kind: uv
        package: openai-whisper edge-tts pysrt pydub
---

# 英文视频中文化流水线

把英文原声视频变成中文配音视频：**语音识别 → 字幕翻译 → 语音合成 → 音画合并**。

前三步和第四步的封装命令都由 `scripts/` 下的脚本完成，**只有"字幕英译汉"需要你（大模型）亲自做**。不要用自己写的临时代码片段去替代这些脚本。

## 何时使用

- 用户给出英文视频，想要中文讲解/中文配音版本
- 需要提取视频字幕并翻译成中文
- 需要为本视频重新配音，**替换掉**原音 → 步骤 4 用基础命令
- 需要**新增一条中文音轨、与英文原声并存可切换** → 步骤 4 改用双音轨命令
- 想要中文配音为主、同时保留低音量英文原声做背景 → 步骤 4 用混音变体

**先确认用户要的是"替换"还是"并存"**，这一句话决定步骤 4 用哪条命令。**前三步在任何情况下都完全一样。**

**不适用**：只要一份中文字幕文件却不需要配音（只跑步骤 1+2）；源视频本身没有语音。

## 目录与产物

假设工作目录是 `<WD>`（源视频所在地），skill 安装目录为 `<SKILL>`。

| 路径 | 角色 |
| --- | --- |
| `<WD>/input.mp4` | 源视频（用户提供） |
| `<SKILL>/scripts/transcribe.py` | 步骤 1：whisper 转写 → 英文字幕 |
| `<WD>/input.srt` | 步骤 1 产物：英文字幕（**步骤 2 的输入**） |
| `<WD>/output.srt` | 步骤 2 产物：中文字幕（**由你翻译生成**） |
| `<SKILL>/scripts/synthesize.py` | 步骤 3：edge-tts 配音 → `output.mp3` |
| `<WD>/output.mp3` | 步骤 3 产物：中文配音音轨 |
| `<WD>/output.mp4` | **最终产物**：中文配音视频 |
| `<SKILL>/scripts/check_env.py` | 环境自检（只依赖标准库） |
| `<SKILL>/references/pitfalls.md` | 踩坑笔记，步骤报错时查阅 |
| `<SKILL>/references/sync-tuning.md` | 音画同步优化，用户追求节奏贴合时查阅 |

## 硬性约束（执行前必读）

1. **所有流水线命令都在 `<WD>` 下执行**，产物都落在当前目录。两个主脚本都支持 `-i/-o` 参数，但**默认就用 `input.mp4` / `output.srt` / `output.mp3`**，通常不必显式传。
2. **路径一律加英文双引号**。工作目录可能含空格。
3. **解释器要选对**。机器上往往有多个 Python，依赖装在哪个里面并不显然。用第 0 步的自检确认；若 `check_env.py` 报 MISS 但依赖其实装过，说明选错了解释器，换一个再试。**不要在每个 Python 里都重装一遍依赖。**
4. **每条命令在独立 shell 中执行**，变量赋值不会带到下一条，不要指望先 `$PY=xxx` 再复用。
5. **步骤 1 和步骤 3 必须后台运行**，不要用短超时的前台命令。全链路从几分钟到一小时不等，取决于视频长度，开始前先告诉用户预计耗时。
6. **步骤 3 很可能以 failed 收尾却是"假失败"**：脚本会在打印完成功信息后才清理临时目录，某些环境下批量删除会被安全策略拦截并终止进程，而**产物早已写盘**。务必先核验 `output.mp3` 时长，正常就继续，**切勿盲目重跑**（一次要几十分钟）。
7. **确认 ffmpeg 的调用方式**。若自检提示 ffmpeg"仅在当前目录"，则所有 ffmpeg 命令都要写成 `./ffmpeg`（Git Bash / Linux / macOS）或 `.\ffmpeg.exe`（PowerShell / CMD），否则会找不到它。这只是权宜之计，**把它所在目录加入 PATH 才是正解**——否则换目录运行就会失效。

## 第 0 步：环境自检

```bash
cd "<WD>"
"<PY>" "<SKILL>/scripts/check_env.py"
```

四项 Python 依赖、`audioop`、ffmpeg 与 ffprobe 全部 OK 才继续。缺什么它会给出对应的安装命令。

**`ffprobe` 是必需的**，不是可选项——pydub 解码 mp3 依赖它，有些 ffmpeg 包只带 `ffmpeg.exe`。

首次使用需安装依赖，分两步：

```bash
# 1. 先装 CPU 版 torch：直接装 whisper 时可能拉到数 GB 的 CUDA 包
"<PY>" -m pip install torch --index-url https://download.pytorch.org/whl/cpu

# 2. 再装其余依赖
"<PY>" -m pip install -U openai-whisper edge-tts pysrt pydub
```

若自检仍报缺失两项，按它的提示补装（**Python 3.13+ 必装第一个**）：

```bash
"<PY>" -m pip install audioop-lts   # Python 3.13 起标准库移除了 audioop，pydub 依赖它
"<PY>" -m pip install msvc-runtime  # Windows 缺 VC++ 运行库会让 torch/whisper 导入崩溃
```

首次转写会下载 Whisper 模型（`base` 约 140MB）到 `~/.cache/whisper`。

## 步骤 1：语音转写（生成英文字幕）

```bash
cd "<WD>"
"<PY>" "<SKILL>/scripts/transcribe.py"
```

- 默认 Whisper `base`、CPU 推理。**后台运行**。
- 预期输出 `input.srt`，末行打印 `完成：写出 N 条字幕 -> input.srt`。
- 常用参数：`-i 视频 -o 字幕 -m small`（更准但更慢，长视频或专业内容可用）、`-l en`、`--device cuda`（有 N 卡时快一个量级，脚本会 fp16）。
- 若 `input.srt` 已存在且用户没说要重做，**跳过本步**。

记录字幕条数与末条结束时间，步骤 2 必须与之完全一致。

## 步骤 2：字幕英译汉（这一步由你完成）

读取 `input.srt`，翻译全部文本行，**其余字节原样保留**，写出 `output.srt`（UTF-8 无 BOM，尾随换行）。

### SRT 结构规则

```
{序号}
{开始} --> {结束}
{文本}

```

- **序号**：保持原有 1、2、3…，不重排、不补号
- **时间轴行**：连空格一起照抄，一个字符都不许改
- **空行**：两条之间的分隔必须保留，文件末尾保留最后一个空行
- **只有文本行被翻译**；一条内可含多行，译文行数可不同，但**不要引入空行**（空行会被解析成新字幕）

### 翻译质量要求

- 口语化中文，适合朗读，不要翻译腔、不要书面语长句
- 专有名词、品牌、人名、代码、命令、URL 保持原样不译
- **中文朗读约 4–5 字/秒，而时间轴不能动**，所以一条 N 毫秒的字幕槽最多容 `N / 1000 × 4.5` 个字。把这条当硬约束，长句要精简提炼，**宁短勿长**
- 保留必要标点；不要添加原文没有的引号、感叹号
- 纯音效字幕（`[MUSIC]`、`[Applause]`）译作 `[音乐]`、`[掌声]`，不要整条删掉
- 被 whisper 断碎的短句，译文要补成完整中文表达，但贴合所在时间片
- **专名要回正**：ASR 常把人名地名听错（实测把 Susie Wiles 听成 "Suzy Walsh"、把 "the President-elect" 听成 "Electromp"）。遇到可疑拼写按常识还原，不要照字面直译

### 执行方式

- 条数 ≤ 60：一次 Write 写出完整 `output.srt`
- 条数 > 60：**分批**，每批 30–50 条，先 Write 头部，再用 Edit 在末尾追加，避免单次输出过长丢条
- 禁止 sed/正则批量替换，禁止只处理前 N 条就收工

### 自检（必须做）

```bash
cd "<WD>"
"<PY>" -c "
import pysrt
a=pysrt.open('input.srt',encoding='utf-8'); b=pysrt.open('output.srt',encoding='utf-8')
print('英文条数:',len(a),' 中文条数:',len(b))
bad=[i+1 for i,(x,y) in enumerate(zip(a,b)) if str(x.start)!=str(y.start) or str(x.end)!=str(y.end)]
print('时间轴不一致:', bad if bad else '无')
empty=[i+1 for i,y in enumerate(b) if not y.text.strip()]
print('空译文:', empty if empty else '无')
"
```

条数相等、时间轴一致、无空译文，**任一项不合格必须修正后才能进步骤 3**。

## 步骤 3：TTS 配音（生成 output.mp3）

```bash
cd "<WD>"
"<PY>" "<SKILL>/scripts/synthesize.py"
```

- 逐条用 `zh-CN-XiaoxiaoNeural` 合成，按原时间轴落位，导出 `output.mp3`（192kbps）。
- **后台运行**。耗时 ≈ 条数 × (sleep + 合成时间)，默认 `--sleep 1.5`，166 条约 6 分钟。
- 常用参数：`--rate "+15%"`（语速加快，缓解溢出）、`--report`（输出每条溢出统计）、`--sleep 10`（被限流时改保守）、`--limit 20`（先试跑 20 条验证链路）、`--keep-temp`。
- 单条失败会以指数退避重试 3 次，仍失败才跳过；跑完看「语音片段数」，差距过大说明被限流，告知用户稍后重跑。
- 产物时长 = 末条字幕结束 + 500ms，**可能短于视频**，导致片尾无声，见步骤 4 变体。

**核验（无论任务报成功还是 failed 都要做）**：

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1 output.mp3
```

时长接近「末条字幕结束 + 0.5 秒」即为成功，直接进入步骤 4。残留的 `temp_audio/` 交给用户决定是否清理，**不要擅自批量删除**。

## 步骤 4：音画合成（生成 output.mp4）

**替换原音**（丢弃英文原音轨）：

```bash
cd "<WD>"
ffmpeg -y -i input.mp4 -i output.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
```

- `-y` 不能省：**没有它，第二次运行会卡在等待「是否覆盖」的输入上**。
- `-c:v copy` 不重编码视频，十几秒完成。
- `-map` 决定保留哪些流，未选中的轨道会被丢弃。

### 可选变体

**双音轨并存**（保留英文原声，另加一条中文轨，播放器中可切换）——**务必打语言标记**，否则两条轨都叫"音轨 1 / 音轨 2"，用户分不清：

```bash
ffmpeg -y -i input.mp4 -i output.mp3 \
  -map 0:v:0 -map 0:a:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 128k \
  -metadata:s:a:0 language=eng -metadata:s:a:0 title="English" \
  -metadata:s:a:1 language=zho -metadata:s:a:1 title="中文配音" \
  output_dual.mp4
```

**若用户要中文配音版，还应把中文轨设为默认轨**（追加两个 `-disposition` 参数）。不做这一步，播放器默认仍播英文原声，用户很可能误以为配音没生效：

```bash
ffmpeg -y -i input.mp4 -i output.mp3 \
  -map 0:v:0 -map 0:a:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 128k \
  -metadata:s:a:0 language=eng -metadata:s:a:0 title="English" \
  -metadata:s:a:1 language=zho -metadata:s:a:1 title="中文配音" \
  -disposition:a:0 0 -disposition:a:1 default \
  output_dual.mp4
```

`-disposition:a:0 0` 是取消英文轨的默认标记，`-disposition:a:1 default` 把默认交给中文轨。实测生效（eng 轨 `default=0`、zho 轨 `default=1`）。

验轨（应见 1 条 video + 2 条 audio，语言分别为 eng / zho）：

```bash
ffprobe -v error -show_entries stream=index,codec_type:stream_tags=language,title -of csv=p=0 output_dual.mp4
```

> MP4 容器会把 `title` 映射为 `name` 字段，ffprobe 输出里看到 `name=` 属正常，播放器读取的正是它。

**配音短于视频时补静音**（`apad` 垫到与视频等长，`-shortest` 在视频结束时收尾，**两者必须同时给**，否则 apad 会无限填充）：

```bash
ffmpeg -y -i input.mp4 -i output.mp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -af apad -shortest output.mp4
```

**保留原声做背景音**（中英混音）：

```bash
ffmpeg -y -i input.mp4 -i output.mp3 \
  -filter_complex "[0:a]volume=0.25[a0];[1:a]volume=1[a1];[a0][a1]amix=inputs=2:duration=longest[out]" \
  -map 0:v:0 -map "[out]" -c:v copy -c:a aac output.mp4
```

完成后向用户报告视频时长、中文字幕条数、配音片段数、产物路径，并调用 present_files 展示 `output.mp4`。

## 收尾

核对 `output.mp4` 的音视频时长是否接近：

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1 output.mp4
```

差值在 1 秒内属正常。若配音明显短于视频（画面还有内容却已无声），用上面的 apad 变体重做步骤 4。

## 故障排查

遇到具体报错先看 `references/pitfalls.md`。高频问题速查：

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `ModuleNotFoundError` | 选错 Python 解释器 | 换一个 Python 重跑 `check_env.py` 确认 |
| `ModuleNotFoundError: No module named 'audioop'` | Python 3.13+ 已将该模块移出标准库 | `pip install audioop-lts`（pydub 依赖它） |
| torch / whisper 导入崩溃，`OSError: [WinError 126] ... c10.dll` | Windows 缺 VC++ 运行库 | `pip install msvc-runtime`（**无需管理员权限**，比装 vc_redist 更可行） |
| ffmpeg 明明在目录里却报"找不到命令" | 未加入 PATH，且当前不在该目录 | 用 `./ffmpeg` 调用，或把该目录加入 PATH |
| `FileNotFoundError: [WinError 2]`（pydub/whisper 报） | ffmpeg 不在 PATH | 安装 ffmpeg 并加入 PATH |
| pydub 解码 mp3 失败，但 ffmpeg 明明能用 | 缺 `ffprobe.exe` | 补一个 ffprobe 放到 PATH，与 ffmpeg 同目录 |
| `pip install` 卡在下载几百 MB 甚至数 GB | torch 拉到了 CUDA 包 | 改装 CPU 版：`pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| `PermissionError` 且路径含 `sslkey.log` | 环境变量 `SSLKEYLOGFILE` 指向无写入权限路径 | 命令前 `unset SSLKEYLOGFILE`，或从系统环境变量里删除它 |
| `pip list` 看得到包却 `No module named` | 同上，SSL 报错伪装成"没装" | 同上；**不要靠重装解决** |
| 步骤 1 后 `input.srt` 为空 | 视频无音轨或语音过小 | `ffmpeg -i input.mp4` 确认音频流，或换大模型 |
| 步骤 3 报找不到 `output.srt` | 漏了步骤 2 | 先完成翻译并通过自检 |
| 步骤 3 大量「失败，跳过」 | edge-tts 限流/断网 | 加 `--sleep 10` 重跑，或稍后再试 |
| 步骤 4 卡住不动 | 缺 `-y` | 中断后加 `-y` 重跑 |
| 步骤 3 报 failed 但打印了「完成!」 | 清理临时目录被拦截 | **假失败**：核验 mp3 时长，正常就继续 |
| 成片后半段没声音 | mp3 短于视频 | 用 apad 变体或混音变体 |

## 禁止事项

- 不要用自己写的临时 Python 代码替代这三个脚本
- 不要让步骤 1、3 跑在短超时的前台命令里
- 不要在字幕自检未通过时进入下一步
- 不要擅自批量删除 `temp_audio/`（数百个文件，易触发保护）
- 不要在核验 mp3 之前就断言步骤 3 失败
