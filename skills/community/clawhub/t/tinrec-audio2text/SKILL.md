---
name: tinrec-audio2text
description: 将音频转文字，并提供 AI 总结、录音要点与发言人区分。 音频转文字：云端转写，支持多格式（mp3/wav/m4a 等）。 AI 总结：自动生成摘要与纪要。 录音要点：章节、待办、推荐等结构化要点。 发言人区分：转写结果带发言人标识，便于会议/对话场景。
---
## 使用说明
使用tinrec的云端API进行便捷的音频转文字，区分发言人并快速总结音频内容和生成摘要

## 使用流程
1. 先获取api-keys，获取地址[https://tinrec.com/api-keys](https://tinrec.com/api-keys)，注册账号后即可免费获取 Key
1.1. claw需要将用户发送的key保存至api-keys文件后使用cli模式进行调用，调用时通过 `--api-keys-file` 指定该文件，每位用户注册后可免费领取1小时转写额度，开通Pro后解锁转写限制


在技能目录下使用 Python CLI，一次完成上传、转写、轮询并输出结果：

```bash
cd script
# 使用目录下的 api-keys 文件
python audio2text_cli.py /path/to/audio.mp3 --api-keys-file ./api-keys
```

- `--api-keys-file`：API Key 文件路径（默认当前目录 `api-keys`），文件内第一行非空非注释即为 Key。
- `--api-key`：直接传入 Key，优先于文件和环境变量。
- `--base-url`：API 地址，默认 `https://api.tinrec.com/api`。
- `--json`：仅输出 JSON（含转写、总结、要点、发言人），便于 AI 解析。
- `--no-wait`：只提交不轮询，返回任务 id。
- `--poll-interval` / `--timeout`：轮询间隔与总超时。

输出包含：`summary`（AI 总结）、`chapters`/`todos`（要点）、`transcripts`（转写正文）、`speaker_data`（发言人信息）。  
**状态说明**：接口有两个状态——**转写状态**（`transcript_status`）与**任务状态**（`task_status`）。转写完成后才有正文；任务状态完成后才会有总结、要点、发言人等信息，CLI 会轮询到两者均完成后再输出。

## 使用场景

在以下场景下应调用本技能（传入用户提供的**本地音频文件路径**及可选的 `--api-keys-file`）：

- **用户发来/提到一段本地录音文件**，希望转成文字、要全文或摘要时。
- **用户明确要求「把这段音频转成文字」「听写/转写这段录音」**，且能访问到本地文件路径时。
- **用户需要会议/访谈纪要**：要总结、要点、待办或「谁说了什么」的发言人区分时。
- **用户提供录音并希望得到结构化结果**：如章节、待办列表、推荐后续动作等，且文件在本地可读时。
- **用户说「用 Tinrec / 用你们的转写」** 或指定要用该服务处理本地音频时。

不适用：仅提供在线链接/URL 而无法下载为本地文件时，需先下载再调用；无本地文件路径或用户未提供音频文件时不调用。
