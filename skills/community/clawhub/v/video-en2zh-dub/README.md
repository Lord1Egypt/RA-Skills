# video-en2zh-dub

把英文视频变成中文配音视频。三大件：**Whisper**（语音识别）→ **大模型**（字幕翻译）→ **edge-tts**（语音合成）→ **ffmpeg**（音画封装）。

全部离线/免费组件，不需要任何 API key。

## 快速开始

```bash
# 1. 安装 Python 依赖（分两步，避免 torch 拉到数 GB 的 CUDA 包）
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# Python 3.13+ 还需补装（标准库已移除 audioop，pydub 依赖它）
pip install audioop-lts

# 2. 确认环境（依赖 + ffmpeg + ffprobe）
python scripts/check_env.py

# 3. 把英文视频放到工作目录，命名 input.mp4，然后：
python scripts/transcribe.py    # input.mp4 -> input.srt（英文字幕）
#    ↓  由你的 AI 助手把 input.srt 翻译成 output.srt
python scripts/synthesize.py    # output.srt -> output.mp3（中文配音）
ffmpeg -y -i input.mp4 -i output.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
```

作为 Agent skill 使用时，由 Agent 自动编排上述流程，**你只需要提供视频**。

## 实测数据

一条 9 分 29 秒 / 1280x720 的英文访谈：

| 环节 | 耗时 | 产物 |
| --- | --- | --- |
| whisper `base`（CPU）转写 | 57 秒（宿主机 6 核）；另一次受限环境约 2 分钟 | 166 条英文字幕 |
| 大模型翻译 | — | 166 条中文字幕，三项自检零偏差 |
| edge-tts 配音 | 约 6 分钟（默认 sleep 1.5） | output.mp3，569.7 秒 |
| ffmpeg 合成 | 5.35 秒 | output_dual.mp4，49MB |

> 早期版本每条间固定 `sleep(10)`，同样 166 条要 34 分钟。改成 1.5 秒 + 失败退避重试后降到约 6 分钟。

成片音视频时长差 0.21 秒。

溢出数据（同一视频两次独立运行）：中位 0.95 / 溢出 42 条，与中位 1.01 / 溢出 57 条（后者加了 `--rate "+10%"`）。
**这两组数字不能直接比较**，因为两次译文不同；共同点是溢出几乎全部集中在 1–2 秒短碎片——
优化方式需对症，详见 `references/sync-tuning.md`。

## 四种输出模式

| 模式 | 适用场景 | 命令要点 |
| --- | --- | --- |
| 替换原音 | 纯中文配音 | `-map 0:v:0 -map 1:a:0` |
| 双音轨并存 | 中英可切换 | 两条 audio 都 map，打 `-metadata:s:a:N language=` |
| 双音轨 + 中文默认 | 打开就播中文 | 再加 `-disposition:a:0 0 -disposition:a:1 default` |
| 混音 | 中文为主 + 英文背景音 | `amix` + `volume=0.25` |

双音轨务必打语言标记，否则播放器里只会显示"音轨 1 / 音轨 2"。

**做中文配音版时记得把中文轨设为默认轨**：不加 `-disposition` 的话，播放器默认仍播英文原声，
很容易让人误以为配音没生效。

## 目录结构

```
video-en2zh-dub/
├── SKILL.md                      # Agent 读取的指令（含 frontmatter）
├── README.md                     # 本文件
├── LICENSE                       # MIT-0（ClawHub 要求）
├── requirements.txt
├── .clawhubignore
├── scripts/
│   ├── check_env.py              # 环境自检，仅依赖标准库
│   ├── transcribe.py             # 步骤 1：Whisper 转写
│   └── synthesize.py             # 步骤 3：edge-tts 配音
└── references/
    ├── pitfalls.md               # 踩坑笔记
    └── sync-tuning.md            # 音画同步优化
```

## 价值在哪里

两个脚本本身不难写。真正难的是 **`references/pitfalls.md`** 里那些东西——它们只有在完整跑通过几百条字幕后才会暴露：清理临时目录导致的"假失败"、`SSLKEYLOGFILE` 把"已安装"伪装成"未安装"、后台任务 stdout 缓冲让进度看起来像卡死、Whisper 把 Susie Wiles 听成 "Suzy Walsh"、配音时长溢出字幕时槽。

每个人自己踩一遍要花掉好几个小时。

## 已知局限

- **音画同步是 TTS 方案的固有短板**。中文朗读时长常超出字幕时槽，实测 25% 条目溢出，且集中在 1–2 秒短碎片。缓解办法见 `references/sync-tuning.md`，但无法彻底消除
- **短碎片（1–2 秒）天然难配**。英文碎片译成中文后往往需要完整短句才通顺，而 1.2 秒只装得下 5 个字左右无法彻底消除
- **edge-tts 依赖微软在线服务**，离线不可用，且可能被限流。脚本内置指数退避重试，可通过 `--sleep` 调节节奏
- **CPU 推理下 Whisper 较慢**。`base` 处理 10 分钟视频约 1 分钟，换 `small`/`medium` 精度更高但耗时成倍增长

## 发布到 ClawHub

```bash
npm i -g clawhub
clawhub login
clawhub skill publish ./video-en2zh-dub \
  --slug video-en2zh-dub \
  --name "Video English to Chinese Dub" \
  --categories creative,automation \
  --topics "whisper,tts,ffmpeg,subtitle,video-dubbing"
```

发布前请确认：

1. `LICENSE` 中的 `YOUR_NAME` 已替换为你的名字
2. 本 skill 会以 **MIT-0** 授权发布，且该许可证不可覆盖——等同于放弃著作权保护
3. 包内不含 `input.mp4` / `ffmpeg.exe` 等大文件（见 `.clawhubignore`）
4. 已在另一台机器上验证过 `check_env.py` 能跑通

> 首次发布的版本在安全扫描完成前，可能暂不出现在公开安装列表。
