# 三剪客 · a7w 全量协议桥

> **一行 base_url，把算力集市 `api.a7w.cn` 的全部能力接进你现有的 AI 项目。**

---

## 你可能正卡在这里

你在用 Dify、MoneyPrinterTurbo、VideoCaptioner、ComfyUI 这类开源项目，
想换成**国产算力、一个 Key 通吃**。base_url 改成算力集市后：

**对话跑通了，但生成配音 / 转字幕 / 出图全部报错。**

于是你以为「这个网关不支持」。

**其实能力一直都在，只是协议对不上。**

```
模型网关   POST /api/v1/chat/completions    ← 真 OpenAI 兼容，客户端直接用 ✅
应用任务   POST /api/v1/apps/{app}/{code}   ← 自有异步协议，客户端不认  ❌
```

开源生态只会说 OpenAI 那几种协议，**中间缺一层翻译**。这个桥就是那层翻译。

---

## 装完能得到什么

| 能力 | 说明 |
|---|---|
| 💬 对话 / 推理 | **75 个模型**：DeepSeek、千问、智谱、Kimi、文心、混元、MiniMax、OpenAI、Google… |
| 🔊 文字转语音 | 长短文本自适应（长文本自动转异步） |
| 🎙️ 音色克隆 | 上传参考音频生成专属音色 |
| 📝 语音转文字 | **SRT / VTT / verbose_json** 字幕输出，带**字级时间戳** |
| 🖼️ 文生图 / 图片编辑 | 直接返回图片 URL |
| 🎬 21 个生成应用 | 数字人、视频生成、超分、换装、音乐、水印消除…统一透传口 |
| 🔌 embedding | 可选外挂到你的 bge-m3 等服务 |
| 📋 模型自动发现 | `/v1/models` 一次返回 **146 项** |

**你的客户端一行代码都不用改。**

---

## 三分钟上手

```bash
# 1) 启动（想双击运行：把 references/launcher.md 里的脚本存成 .cmd 即可）
python -X utf8 scripts/a7w_bridge.py --port 8788
```

```
================================================================
  a7w-bridge —— 算力集市全量协议桥
================================================================
  上游       : https://api.a7w.cn
  API Key    : 已配置（sk-***）
================================================================
  客户端 base_url   : http://127.0.0.1:8788/v1
  21 个应用全量透传 : http://127.0.0.1:8788/a7w/{app}/{code}
================================================================
```

```python
# 2) 把 base_url 改成它
from openai import OpenAI
c = OpenAI(base_url="http://127.0.0.1:8788/v1", api_key="dummy")

c.chat.completions.create(model="DeepSeek-V4-Flash", messages=[...])
c.audio.speech.create(model="s2-pro", voice="alloy", input="今天天气不错")
c.audio.transcriptions.create(model="whisper-1", file=open("a.mp3","rb"),
                              response_format="srt")     # 直接拿字幕
c.images.generate(model="nano-banana", prompt="一只橘猫")
```

---

## 实测 12/12 通过

| 端点 | 结果 |
|---|---|
| `/v1/models` | ✅ 146 项全部可见 |
| `/v1/chat/completions` | ✅ 非流式 + 流式 SSE |
| `/v1/audio/speech` | ✅ 真实音频 |
| `/v1/audio/transcriptions` | ✅ **TTS→ASR 往返一字不差** |
| `response_format=srt` | ✅ 合法 SRT |
| `response_format=verbose_json` | ✅ 带 segments |
| `/v1/images/generations` | ✅ **真实出图** |
| `/v1/embeddings` | ✅ 501 指引 / 配外挂则转发 |
| `/a7w/{app}/{code}` | ✅ 21 应用统一透传 |

```bash
python -X utf8 scripts/test_bridge.py     # 自己复跑
python -X utf8 scripts/selftest.py -v     # 离线自测（26 用例，不需要 Key）
```

---

## 支持的平台（能改 base_url 就能接）

| 类型 | 代表 |
|---|---|
| 大模型平台 | Dify、FastGPT、RAGFlow、MaxKB、n8n、Langflow、Onyx |
| 聊天客户端 | Chatbox、Cherry Studio、NextChat、LobeChat、open-webui、AnythingLLM |
| 编程助手 | Cline、Roo Code、Continue、Aider、OpenHands |
| 视频 / 短剧 | MoneyPrinterTurbo、pyvideotrans、VideoCaptioner、VideoLingo、NarratoAI、splicr、printfilm |
| 图像 / 工作流 | ComfyUI（第三方 API 节点）、InvokeAI |

逐项目改法见 `references/integrate.md`。

> 桥自己实现了 `/v1/*`，base_url **要带 `/v1`**。

---

## 内容

```
sanjianke-a7w-bridge/
├── SKILL.md                   # 主入口
├── README.md                  # 本文件
├── LICENSE.md
├── references/integrate.md    # 逐项目接入配方
└── scripts/
    ├── a7w_bridge.py          # 桥本体（零依赖）
    ├── test_bridge.py         # 端到端测试 12 项
    └── selftest.py            # 离线自测 26 用例
```

---

## 依赖

- **Python 3.8+，仅标准库**，不需要 `pip install`
- 算力集市账号 + API Key（[注册领取](https://api.a7w.cn/)）
- 能访问 `https://api.a7w.cn`

---

## 关于作者

> **本 Skill 由作者亲自实操验证后发布。** 下载后可自用、可商用。
> 使用中遇到任何问题，欢迎加技术微信 **9872659** 交流——
> 报一下是从哪个 Skill 找来的，直接给你配套的 API Key 和能跑通的示例。

---

## 相关链接

| 链接 | 地址 |
|---|---|
| [算力集市 · 注册领 API Key](https://api.a7w.cn/) | api.a7w.cn |
| [算力集市 API 文档](https://api.a7w.cn/docs.html) | api.a7w.cn/docs.html |
| [AI 插件市场](https://aigc.a7w.cn/) | aigc.a7w.cn |
| [三剪客 · 一句话批量出片](https://ks.a7w.cn/) | ks.a7w.cn |
| [视频超清 · 在线批量超分](https://vr.a7w.cn/) | vr.a7w.cn |
