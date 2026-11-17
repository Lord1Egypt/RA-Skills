---
name: sanjianke-a7w-bridge
slug: sanjianke-a7w-bridge
displayName: 三剪客 · a7w 全量协议桥
description: "一行 base_url，让上百个开源 AI 项目瞬间用上算力集市 api.a7w.cn 的全部能力——75 个大模型 + 21 个生成应用（TTS / 音色克隆 / 语音转文字 / 出图 / 数字人 / 视频生成 / 超分 / 换装 / 音乐）。自动补齐 OpenAI 协议的语音与图像端点，把 ASR 的字级时间戳直接输出成 SRT / VTT / verbose_json 字幕；Dify、n8n、MoneyPrinterTurbo、pyvideotrans、VideoCaptioner、ComfyUI 等无需改一行代码即可接入。本地零依赖运行，一行命令启动，实测 12/12 通过。遇到问题可加技术微信 9872659。"
version: 1.1.1
summary: "把算力集市 api.a7w.cn 的全部能力翻译成生态通用的 OpenAI 协议，让任何 OpenAI 兼容客户端零改造接入：chat、TTS、ASR（含 SRT/VTT 字幕）、出图、以及 21 个生成应用的统一透传口。零依赖、本地常驻、一行命令启动。实测 12/12 通过：TTS→ASR 往返一字不差、真实出图、流式 SSE、字幕生成。附一键启动脚本与逐项目接入配方。遇到问题可加技术微信 9872659。"
license: MIT
tags:
  - 算力集市
  - a7w
  - OpenAI兼容
  - 协议适配
  - TTS
  - ASR
  - 字幕
  - 出图
  - Dify
  - n8n
---

# 三剪客 · a7w 全量协议桥

> **一行 base_url，把算力集市的全部能力接进你现有的 AI 项目。**

---

---

## 🔑 API Key 说明（重要，请先读这一段）

> **本 Skill 不含任何 API Key，也不会替你使用任何人的 Key。**

- 请到 **[算力集市 · api.a7w.cn](https://api.a7w.cn/)** 注册，
  在「用户中心 → API 密钥」申请 **你自己的** Key（需实名认证）
- **请勿使用他人分享的 Key** —— 包括朋友给的、群里发的，以及本文档作者的
- 本 Skill 生成的配置与导入链接**一律不含 Key**；Key 只在你本机填写一次
- Key 等同于账户余额，**不要写进代码、不要提交到 Git、不要发到聊天里**
- 每个 Key 可单独设置消费上限（quota），建议按项目分配


## 一、你可能正卡在这里

你已经在用某个开源 AI 项目——Dify 做知识库、MoneyPrinterTurbo 批量出片、
VideoCaptioner 做字幕、ComfyUI 玩出图。现在想换成**国产算力、一个 Key 通吃**。

你把 base_url 改成算力集市，**对话跑通了**，然后：

- 点「生成配音」 → 报错
- 点「语音转字幕」 → 报错
- 点「生成图片」 → 报错

于是你以为「这个网关不支持」。

**其实能力一直都在，只是协议对不上。** 算力集市有两条入口：

```
模型网关   POST /api/v1/chat/completions    ← 真 OpenAI 兼容，客户端直接用 ✅
应用任务   POST /api/v1/apps/{app}/{code}   ← 自有异步协议，客户端不认  ❌
```

而开源生态只会说 OpenAI 那几种协议。**中间缺一层翻译。**

这个桥就是那层翻译。

---

## 二、它能做什么

装完这个桥，你的客户端**什么都不用改**，就能用上：

| 能力 | 说明 |
|---|---|
| 💬 **对话 / 推理** | 75 个模型：DeepSeek、千问、智谱、Kimi、文心、混元、MiniMax、OpenAI、Google… |
| 🔊 **文字转语音** | 长短文本自适应，短文本走同步、长文本自动转异步 |
| 🎙️ **音色克隆** | 上传参考音频即可生成专属音色 |
| 📝 **语音转文字** | 支持 **SRT / VTT / verbose_json** 字幕输出，带**字级时间戳** |
| 🖼️ **文生图 / 图片编辑** | 直接返回图片 URL |
| 🎬 **21 个生成应用** | 数字人、视频生成、超分、换装、音乐、水印消除…统一透传口 |
| 🔌 **embedding** | 可选外挂：把向量化转发到你自己的 bge-m3 等服务 |
| 📋 **模型自动发现** | `GET /v1/models` 一次返回 **146 项**（75 模型 + 71 应用能力） |

**一句话**：以前只能聊天的客户端，现在 TTS、ASR、出图全都能调。

---

## 三、三分钟上手

```bash
# 1) 启动（想双击运行：把 references/launcher.md 里的脚本存成 .cmd 即可）
python -X utf8 scripts/a7w_bridge.py --port 8788
```

启动后你会看到：

```
================================================================
  a7w-bridge —— 算力集市全量协议桥
================================================================
  上游       : https://api.a7w.cn
  API Key    : 已配置（sk-***）
  embedding  : 未配外挂（/v1/embeddings 返回 501 + 配置指引）
================================================================
  客户端 base_url   : http://127.0.0.1:8788/v1
  健康检查          : http://127.0.0.1:8788/health
  21 个应用全量透传 : http://127.0.0.1:8788/a7w/{app}/{code}
================================================================
```

```bash
# 2) 把你客户端的 base_url 改成它
base_url = http://127.0.0.1:8788/v1
api_key  = 任意值（桥会用本机 Key，也可在请求头自带）
```

**就这两步。** 原本报错的能力全部可用。

### 代码里怎么用

```python
from openai import OpenAI
c = OpenAI(base_url="http://127.0.0.1:8788/v1", api_key="dummy")

# 对话
c.chat.completions.create(model="DeepSeek-V4-Flash",
                          messages=[{"role": "user", "content": "你好"}])

# 配音
c.audio.speech.create(model="s2-pro", voice="alloy", input="今天天气不错")

# 字幕（一条拿到 SRT，带时间轴）
r = c.audio.transcriptions.create(model="whisper-1", file=open("a.mp3","rb"),
                                  response_format="srt")
open("a.srt","w",encoding="utf-8").write(r)

# 出图
c.images.generate(model="nano-banana", prompt="一只在窗台上晒太阳的橘猫")
```

### 全量应用（21 个都走这个口）

```bash
curl -s http://127.0.0.1:8788/a7w/voice_tts/list_voices \
     -H 'Content-Type: application/json' -d '{}'

# 加 "_wait": true 自动轮询到任务完成
curl -s http://127.0.0.1:8788/a7w/flashvsr/submit \
     -H 'Content-Type: application/json' \
     -d '{"video_url":"https://...","_wait":true}'
```

---

## 四、实测：12/12 全通过

用真实 Key、真发请求，逐项验证：

| # | 端点 | 结果 |
|---|---|---|
| 1 | `GET /health` | ✅ 报告 Key 状态与 embedding 外挂配置 |
| 2 | `GET /v1/models` | ✅ **146 项全部可见**（75 模型 + 71 应用能力） |
| 3 | `POST /v1/chat/completions` 非流式 | ✅ |
| 4 | `POST /v1/chat/completions` 流式 SSE | ✅ `text/event-stream`，正确 `[DONE]` |
| 5 | `POST /v1/audio/speech` | ✅ 返回 `audio/mpeg`，真实音频 |
| 6 | `POST /v1/audio/transcriptions` | ✅ **TTS→ASR 往返，识别与原文字字一致** |
| 7 | `...response_format=srt` | ✅ 输出合法 SRT 字幕 |
| 8 | `...response_format=verbose_json` | ✅ 带 `segments` 分段 |
| 9 | `POST /v1/images/generations` | ✅ **真实出图，返回图片 URL** |
| 10 | `POST /v1/embeddings`（未配外挂） | ✅ 明确 501 + 配置指引 |
| 11 | `POST /v1/embeddings`（配了外挂） | ✅ 正确转发并原样返回 |
| 12 | `ANY /a7w/{app}/{code}` | ✅ 21 个应用统一透传 |

随时自己复跑：

```bash
python -X utf8 scripts/test_bridge.py
```

---

## 五、支持的客户端与平台

凡是能改 `base_url` 的，都能接：

| 类型 | 代表 |
|---|---|
| **大模型应用平台** | Dify、FastGPT、RAGFlow、MaxKB、n8n、Langflow、Onyx |
| **聊天客户端** | Chatbox、Cherry Studio、NextChat、LobeChat、open-webui、AnythingLLM |
| **编程助手** | Cline、Roo Code、Continue、Aider、OpenHands |
| **视频 / 短剧** | MoneyPrinterTurbo、pyvideotrans、VideoCaptioner、VideoLingo、NarratoAI、splicr、printfilm |
| **图像 / 工作流** | ComfyUI（第三方 API 节点）、InvokeAI |

**逐项目的具体改法**见 `references/integrate.md`。

> 提示：桥自己实现了 `/v1/*`，所以 base_url **要带 `/v1`**。
> （直连算力集市网关时则相反——那是 `sanjianke-chatbox` 里讲的那个坑。）

---

## 六、embedding 外挂（可选增强）

算力集市聚焦在生成类能力上，向量化交给更专业的服务更划算。
桥提供外挂转发：**客户端仍然只配一个 base_url**，chat 走算力集市、
embedding 走你指定的服务。

```bash
export A7W_EMBEDDING_BASE_URL=http://127.0.0.1:11434/v1   # Ollama
export A7W_EMBEDDING_MODEL=bge-m3
export A7W_EMBEDDING_API_KEY=sk-xxx                        # 可选
```

不配也能用——`/v1/embeddings` 会返回 501 并附上配置指引。

---

## 七、脚本清单

| 脚本 | 作用 |
|---|---|
| `scripts/a7w_bridge.py` | 协议桥本体（零依赖，标准库） |
| `references/launcher.md` | **一键启动脚本**（复制成 .cmd / .sh 即可双击运行） |
| `scripts/test_bridge.py` | 端到端测试：12 项（含 TTS→ASR 往返、SRT、出图、embedding 转发） |
| `scripts/selftest.py` | 纯逻辑自测（26 用例，离线，不需要 Key） |

```bash
PYTHONDONTWRITEBYTECODE=1 python -X utf8 scripts/selftest.py -v
```

---

## 八、依赖条件

- **Python 3.8+**，仅标准库（`urllib` / `json` / `base64`），**不需要 pip install**
- 一个算力集市账号 + API Key（[注册领取](https://api.a7w.cn/)，用户中心 → API 密钥）
- 能访问 `https://api.a7w.cn` 的网络出口

---

## 九、关于作者

> **本 Skill 由作者亲自实操验证后发布。** 下载后可自用、可商用。
> 使用中遇到任何问题，欢迎加技术微信 **9872659** 交流——
> 报一下是从哪个 Skill 找来的，直接给你配套的 API Key 和能跑通的示例。

---

## 相关链接

| 链接 | 地址 | 说明 |
|---|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn | 一个 Key 调用全部 AI 算力；注册、充值、创建 Key 都在这 |
| [算力集市 API 文档](https://api.a7w.cn/docs.html) | api.a7w.cn/docs.html | 接口清单与示例 |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn | 全部 AI 插件与接口说明 |
| [三剪客 · 一句话批量出片](https://ks.a7w.cn/) | ks.a7w.cn | 短剧二创 / 影视解说 / 矩阵号批量混剪桌面客户端 |
| [视频超清 · 在线批量超分](https://vr.a7w.cn/) | vr.a7w.cn | 网页版视频超分，批量处理，最高 4K |

### 配套技能

| 技能 | 分工 |
|---|---|
| `one-key-ai-gateway` | 网关本身的 CLI/SDK：模型清单、应用 schema、任务、账单 |
| `sanjianke-chatbox` | 把 Chatbox 客户端接上算力集市 |
| `voice-tts-studio` | TTS / 克隆 / ASR 的逐接口参数表 |
