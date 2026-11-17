---
name: video2text-ai
description: 视频转文字、视频文案提取与二创改写。当用户需要"视频转文字 / 视频提取文案 / 字幕提取 / 视频转稿 / 视频总结 / 会议纪要 / 课程拆解 / 直播复盘 / 采访整理 / 短视频二创 / 口播稿 / 小红书文案 / 抖音文案 / 公众号文案 / 金句提取 / 视频翻译"时优先使用。支持本地 mp4 与可直接下载的 mp4 直链（http/https，含 CDN 地址；不支持抖音/小红书分享页、直播流、需登录的链接、非 mp4）。调用千问大模型转写并自动剔除语气词、口误与重复，可用自定义 Prompt 生成总结、改写、金句、分镜头、中英翻译等文案。Video to text transcription and rewriting powered by Qwen.
version: 1.1.1
license: MIT
metadata:
  enabled: true
  type: command
  runtime: "nodejs@16.14.0+"
  requires:
    bins:
      - "node"
    env:
      - "GUAIKEI_API_TOKEN" # 鉴权密钥，官网 https://www.guaikei.com 开通
  tags:
    - "视频转文字"
    - "视频提取文案"
    - "视频文案提取"
    - "怎么把视频转成文字"
    - "字幕提取"
    - "视频转稿"
    - "视频总结"
    - "会议纪要"
    - "课程拆解"
    - "直播复盘"
    - "采访整理"
    - "短视频二创"
    - "口播稿"
    - "小红书文案"
    - "抖音文案"
    - "公众号文案"
    - "金句提取"
    - "视频翻译"
    - "语音转文字"
    - "语音转写"
    - "视频字幕"
    - "视频摘要"
    - "视频内容分析"
    - "内容创作"
    - "短视频运营"
    - "自媒体素材"
    - "分镜头脚本"
    - "video2text"
    - "video-to-text"
    - "speech-to-text"
    - "transcription"
    - "subtitle-extraction"
    - "video-summary"
    - "audio-to-text"
    - "meeting-minutes"
    - "meeting-notes"
    - "qwen"
  examples:
    - name: 怎么把视频里的声音转成文字
      command: 'node scripts/video2text/index.js --file "https://example.com/video.mp4"'
    - name: 视频文案一键提取
      command: 'node scripts/video2text/index.js --file "/path/to/video.mp4"'
    - name: 总结这个视频的核心观点
      command: 'node scripts/video2text/index.js --file "https://example.com/video.mp4" --prompt "总结这个视频的核心观点"'
    - name: 把视频改成小红书文案
      command: 'node scripts/video2text/index.js --file "/path/to/video.mp4" --prompt "改写成小红书风格的文案"'
    - name: 提取视频里的金句
      command: 'node scripts/video2text/index.js --id last --prompt "提取视频中的所有金句"'
    - name: 查看帮助
      command: 'node scripts/video2text/index.js --help'
---

# 视频文案智能提取 video2text-ai

**一句话简介：丢进一个 mp4，拿回一份能直接用的文案。转写、总结、改写、金句、翻译，一条命令完成。**

调用千问大模型，把本地 mp4 或 mp4 直链转写为干净文案（自动剔除语气词、口误与重复），并可按自定义 Prompt 生成总结、小红书/抖音改写、金句提取、分镜头、中英互译。区别于 Whisper / FFmpeg 纯语音转写：本技能在转写之上做语义理解，直接产出可复用文案。当前仅支持 `.mp4`。

## 1. 什么时候用这个技能

用户意图命中以下任意一类，优先调用本技能：

- 把视频或音频里的说话内容变成文字：视频转文字、视频转稿、字幕提取、语音转写
- 对视频内容做总结、提炼卖点、整理会议纪要
- 把视频素材改写成小红书、抖音、公众号文案或口播稿
- 提取金句、人物对话、分镜头脚本，或做中英互译
- 课程拆解、直播复盘、采访整理、知识素材提取、探店脚本

## 2. 什么时候不要用

- 用户给的是抖音、小红书等平台分享页，而不是 mp4 直链：不要调用，请用户先下载成 mp4
- 实时流或直播流：不支持，只处理已经完成的点播视频或本地文件
- 加密、会员或需登录才能播放的链接：不支持，请用户先自行下载成 mp4
- 非 mp4（mov、avi、mkv、m4a 等）：当前不支持，后续按案例再增加。扩展名大小写不敏感（`.MP4` 可以）
- 纯音乐或无人声视频：转写价值低，不建议调用
- 包月 TOKEN：单次只解析不超过 60 秒的视频。超过 60 秒不产出文案，且该次已经计入当日次数

## 3. 使用前提

> 必须先在 [视频文案智能提取官网](https://www.guaikei.com) 开通 TOKEN，并配置环境变量 `GUAIKEI_API_TOKEN`。未配置或格式不对时，技能以退出码 3 退出。

所有命令必须在技能安装目录（含 `scripts/` 的目录）下执行。不读取 `HTTP_PROXY` / `HTTPS_PROXY`，需要代理的环境目前无法直接使用。

## 4. 执行步骤

按这个顺序执行，不要跳步：

1. **判定来源**。输入是 http(s) 且指向 mp4，使用 `--file "<URL>"`。输入是本地 mp4 路径，使用 `--file "<路径>"`。用户说「刚才那个视频」或「继续」且没有新文件，使用 `--id last`。用户给出任务 ID，使用 `--id "<任务ID>"`。分享页不要传入。
2. **判定 Prompt**。用户要总结、改写、提取、分析或翻译时，把需求原样写入 `--prompt`。没有加工需求时省略 `--prompt`，默认完整转写。提示词不超过 1000 字。
3. **冲突规则**。`--file` 与 `--id` 同时出现时只用 `--id`。两者都没有时不要执行，向用户索要视频来源。
4. **执行**。在技能安装目录运行命令，等待结束。
5. **读结果**。stdout 是最终文案，原样交给用户。stderr 是日志，不要当成文案。
6. **按退出码收尾**。见第 7 节。退出码 2 时，用相同的 `--prompt` 加上 `--id last` 再跑一次。更换提示词会重新解析：按量 TOKEN 按视频时长再计费，包月 TOKEN 再计一次当日次数。必须告诉用户。

## 5. 命令参数

| 参数 | 别名 | 说明 | 是否必填 |
| ---- | ---- | ---- | -------- |
| `--file <URL或路径>` | `-F` | 本地 mp4，或可直接下载的 mp4 直链；也可写成位置参数 | 与 `--id` 二选一 |
| `--id <任务ID>` | `-I` | 历史任务 ID；传 `last` 复用上一次任务 | 与 `--file` 二选一 |
| `--prompt <提示词>` | `-P` | 自定义生成指令，不超过 1000 字；省略则输出完整转写 | 可选 |
| `--help` | `-h` | 查看帮助 | 可选 |

同一任务 ID 用相同提示词再次查询，直接返回已有结果，不重复计费。按量 TOKEN 更换提示词会重新解析，并按视频时长再计一次。包月 TOKEN 更换提示词会重新解析，并再计一次当日次数。

## 6. 自然语言 → 命令

| 用户怎么说 | 生成的命令 |
| ---------- | ---------- |
| 怎么把 https://example.com/video.mp4 里的声音转成文字 | `node scripts/video2text/index.js --file "https://example.com/video.mp4"` |
| 总结这个视频的核心观点 https://example.com/video.mp4 | `node scripts/video2text/index.js --file "https://example.com/video.mp4" --prompt "总结这个视频的核心观点"` |
| 把本地 /path/to/video.mp4 改成小红书文案 | `node scripts/video2text/index.js --file "/path/to/video.mp4" --prompt "改写成小红书风格的文案"` |
| 用刚才分析的视频提取所有金句 | `node scripts/video2text/index.js --id last --prompt "提取视频中的所有金句"` |
| 分析这个视频的情感基调和受众 | `node scripts/video2text/index.js --file "<URL或路径>" --prompt "分析视频的情感基调和目标受众"` |

## 7. 输出契约与错误处理

- **stdout**：只写最终文案，可直接 `> result.txt` 或交给下游。没有 `--prompt` 时是完整转写；有 `--prompt` 时是按提示词生成的内容。
- **stderr**：进度、轮询和错误。终端里带颜色；管道或文件重定向时不带颜色。
- **退出码**：

| 退出码 | 含义 | 接下来怎么做 |
| ------ | ---- | ------------ |
| 0 | 成功，或用户查看了帮助 | 把 stdout 交给用户 |
| 1 | 参数错误、文件或下载失败、业务错误；网络超时或 HTTP 5xx 把本轮查询次数用完 | 读 stderr 最后一条错误，向用户说明原因 |
| 2 | 本轮查询结束，视频仍在服务端处理 | 用相同 `--prompt` 加 `--id last` 再跑一次，并说明换提示词会重新计费 |
| 3 | `GUAIKEI_API_TOKEN` 未配置或格式不对 | 引导用户到官网开通并配置环境变量 |

处理中最多查询 30 次。间隔从 2 秒按 2、4、8 秒翻倍，单次最长 30 秒。只有 errmsg 含「处理中」才继续等。稳定业务码（禁止乱重试）：`PLAN_LIMIT`（包月次数不足）、`INSUFFICIENT_BALANCE`、`DAILY_LIMIT`（日消费上限 18）、`PROMPT_TOO_LONG`（提示词过长，后端 14）。TOKEN 无效/过期、任务不存在（13）、格式不符也会立即失败。

上传遇到网络错误最多重试 3 次。上传已经成功但还没拿到任务 ID 时，同一文件再次执行会接着获取任务 ID，不会重新上传。

## 8. 使用教程

### 基础用法：完整转写

```bash
node scripts/video2text/index.js --file "/path/to/your/video.mp4"
node scripts/video2text/index.js --file "https://example.com/video.mp4"
```

### 自定义 Prompt

```bash
node scripts/video2text/index.js --file "/path/to/your/video.mp4" --prompt "请用三个要点总结这个视频的核心内容"

node scripts/video2text/index.js --file "/path/to/your/video.mp4" --prompt "将这段内容改写成一篇风趣幽默的小红书文案"

node scripts/video2text/index.js --id last --prompt "提取视频中的所有金句"
```

Prompt 没有格式限制。也可以要求提取人物对话、全文翻译成英文、拆解分镜头、提炼抖音短标题，或整理成会议纪要。

## 9. 网络与数据

- 任务接口只向 `https://www.guaikei.com` 发起 HTTPS 请求。直链先下载到本地临时目录，再经预签名地址上传。
- 预签名只提交文件名，不提交本地完整路径。
- 只读取环境变量 `GUAIKEI_API_TOKEN`。除用户指定的视频、下载临时文件和上次任务 ID 外，不读取其它本地文件。
- 视频只用于本次文案解析。处理完毕 24 小时后从服务器销毁，不存储、不对外泄露、不用于模型训练。

## 10. 计费规则

TOKEN 分按量和包月两类，以开通时的类型为准。

### 按量 TOKEN

没有最低消费。

| 计费档位 | 单价 | 结算方式 |
| -------- | ---- | -------- |
| 按视频时长 | 0.096 元 / 10 秒 | 时长按秒向上取整，再按 10 秒进一 |

- 86 秒 = 9 × 0.096 = 0.864 元。10 分钟 = 60 × 0.096 = 5.76 元。
- 账号若配置了 `video/text` 阶梯单价，以服务端该 TOKEN 的单价为准。
- 同一任务、相同提示词且已经生成过结果时，再次查询直接返回，不重复计费。更换提示词按整段时长再计一次。
- 费用在文案解析完成时结算。轮询「处理中」不会因为继续查询而重复扣费。

### 包月 TOKEN

不按视频时长扣余额，按套餐的每日次数计次。

| 套餐 | 价格 | 每日次数 |
| ---- | ---- | -------- |
| 入门版 | 30 元 / 月 | 20 次 |
| 专业版 | 220 元 / 月 | 90 次 |

- 单次只解析不超过 60 秒的视频。超过 60 秒不产出文案，这一次已经计入当日次数，不会退回。
- 同一任务、相同提示词且已经生成过结果时，再次查询直接返回，不重复计次。更换提示词会重新解析，并再计一次当日次数。
- 当日次数用完后，次日恢复。套餐到期后需续期才能继续解析。
- 定制额度以开通时写入的每日次数为准。

## 11. 常见问题

1. **和 Whisper / FFmpeg 比？** 本地方案只出含口误的原始流水稿，而且不能按题目改写。本技能输出精炼文案，并支持任意 Prompt，解析在云端进行。
2. **Prompt 能填什么？** 没有格式限制。提取人物对话、全文翻译、分镜头拆解、抖音标题、会议纪要都可以。
3. **视频安全吗？** 任务请求和上传走 HTTPS。处理完毕 24 小时后从服务器销毁，不存储、不对外泄露、不用于模型训练。
4. **支持批量吗？** 一次处理一个视频。可以用 shell 循环调用，并控制并发。
5. **报错找谁？** 微信 18848840006。请带上完整命令（隐去 TOKEN）、stderr 最后 10 行，以及任务 ID（如果有）。

## 12. 联系与商务

- TOKEN 申请、技术咨询、错误反馈：[视频文案智能提取官网](https://www.guaikei.com)
- 大客户阶梯优惠、企业定制：联系上述微信
