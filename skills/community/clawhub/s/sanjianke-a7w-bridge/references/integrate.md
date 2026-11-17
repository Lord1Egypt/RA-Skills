# 逐项目接入配方

> 前提：桥已启动（`python -X utf8 scripts/a7w_bridge.py --port 8788`）。
> 下面每个项目的「桥之前」都是实测/调研确认过的状态。

---

## 一、通用改法

几乎所有项目都长这样：

```bash
# 桥之前
OPENAI_BASE_URL=https://api.openai.com/v1

# 桥之后
OPENAI_BASE_URL=http://127.0.0.1:8788/v1
OPENAI_API_KEY=dummy        # 桥会用本机 ~/.a7w/config.json 的 Key
```

**注意**：桥自己实现了 `/v1/*`，所以 base_url **必须带 `/v1`**。
（这与 `sanjianke-chatbox` 里那个坑刚好相反——那里是直连网关，不能带 `/v1`。）

---

## 二、字幕 / 翻译配音类（收益最大）

### pyvideotrans

| 环节 | 桥之前 | 桥之后 |
|---|---|---|
| 文案（LLM） | ✅ 本就通 | 不变 |
| **TTS** | ❌ 打 `/audio/speech` → 404 | ✅ 通 |
| **ASR** | ❌ 打 `/audio/transcriptions` → 404 | ✅ 通 |

三个环节全通，**改一个 base_url 即可**。这是本桥收益最大的单个项目。

```bash
OPENAI_BASE_URL=http://127.0.0.1:8788/v1
```

### SmartSub（MIT，最适合先验证）

设置里选「OpenAI 兼容」，端点填 `http://127.0.0.1:8788/v1`。
它的字幕+配音一体化正好覆盖 TTS 与 ASR 两条线。

### VideoCaptioner 卡卡字幕助手

LLM 部分本就是 A 级；桥之后 ASR 也能换：

```
LLM 服务 → OpenAI（兼容模式）
API Base URL = http://127.0.0.1:8788/v1
转写服务   → OpenAI Whisper 兼容
```

**直接要字幕**：

```python
r = client.audio.transcriptions.create(
        model="whisper-1", file=open("ep01.mp3", "rb"),
        response_format="srt")          # 桥内部走词级时间戳再合并
open("ep01.srt", "w", encoding="utf-8").write(r)
```

### VideoLingo / SoniTranslate / haoone-app

同理：把转写与配音的端点指向桥。

---

## 三、短剧 / 自动成片类

| 项目 | 文案 | TTS | ASR | 改法 |
|---|---|---|---|---|
| MoneyPrinterTurbo | ✅ | ✅ | — | `openai_base_url` → 桥 |
| NarratoAI | ✅ | ✅（纯 URL 字段） | ✅ | `text_openai_base_url` + 转写端点 |
| splicr 叙影 | ✅ | ✅ | — | 独立 TTS Base URL → 桥 |
| printfilm | ✅ | ✅ | — | `MODEL_AUDIO` 走桥 |
| ArcReel | ✅ | ✅（自定义供应商） | 未核实 | 「TTS 调用端点」填桥 |
| xiakeman-ai-short-drama | ✅ | ✅ | — | `TTS_BASE_URL_ALLOWLIST` 加桥地址 |

> ⚠️ **许可提醒**：`ArcReel` 是 AGPL-3.0+附加条款、`JJYB_AI 智剪` 明确禁止商用、
> `pyvideotrans` 是 GPL+non-commercial 标注。接入前先确认。

---

## 四、平台类（Dify / n8n / Coze）

这些平台原生支持「自定义 OpenAI 兼容模型」，改完就能用 chat + audio：

| 平台 | 改法 |
|---|---|
| **Dify** | 模型供应商加 `OpenAI-API-compatible`，Base URL 填 `http://127.0.0.1:8788/v1` |
| **n8n** | OpenAI 凭据 Base URL 填桥（记得关 `Use Responses API`） |
| **FastGPT / MaxKB / RAGFlow** | 自定义模型端点填桥 |

> ⚠️ Dify 的 OpenAI-API-compatible 插件对 **embedding/rerank/STT/TTS 类型**会自己再拼一次 `/v1`。
> 桥的路径已经带 `/v1`，遇到双拼就把 Base URL 填成 `http://127.0.0.1:8788`（不带 `/v1`）。

---

## 五、异步应用（视频 / 数字人 / 超分 / 换装）

**OpenAI 没有对应的通用协议**，所以只能走桥的透传口：

```bash
# 提交 + 自动轮询（_wait: true）
curl -s http://127.0.0.1:8788/a7w/flashvsr/submit \
  -H 'Content-Type: application/json' \
  -d '{"video_url":"https://...","_wait":true}'

# 只提交，自己轮询
curl -s http://127.0.0.1:8788/a7w/voice_tts/list_voices -H 'Content-Type: application/json' -d '{}'
curl -s http://127.0.0.1:8788/a7w/tasks/<task_id>
```

**21 个应用统一是这个入口**，不用记各自的路径。
参数名先用 `one-key-ai-gateway` 的 `schema <app>` 查：

```bash
python -X utf8 ../one-key-ai-gateway/scripts/client.py schema nano_banana
```

---

## 六、ComfyUI

ComfyUI 的第三方节点（`ComfyUI-UniAPI`、`comfyui-byokey` 等）打的是
`{base_url}/v1/images/generations` —— **桥正好实现了这个端点**。

节点里填：

```
base_url = http://127.0.0.1:8788
api_key  = dummy
```

> ⚠️ 但**当前网关侧的 `nano_banana` 不可用**（返回 UNKNOWN），
> 所以这条路要等平台修好才能真正出图。桥这侧的代码已经就绪。

---

## 七、验证你的接入

```bash
# 桥自身 11 项端到端
python -X utf8 scripts/test_bridge.py

# 只验客户端要用的那个端点
curl -s http://127.0.0.1:8788/v1/models | head -c 200
```

跑完对照 `sanjianke-chatbox` 的排错手册——两边的 401/402/429 处理逻辑是一样的。
