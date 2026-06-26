# TRTC AI 智能客服 - 配置参数完全指南

## 目录

1. [配置文件结构](#配置文件结构)
2. [部署区域](#部署区域)
3. [腾讯云 API 密钥](#腾讯云-api-密钥)
4. [TRTC 应用凭据](#trtc-应用凭据)
5. [LLM 配置](#llm-配置)
6. [欢迎语](#欢迎语)
7. [数字人配置](#数字人配置)
8. [关键词与告别语](#关键词与告别语)
9. [转人工关键词与提示语](#转人工关键词与提示语)
10. [TTS 音色映射表](#tts-音色映射表)
11. [STT 引擎映射表](#stt-引擎映射表)
12. [固定默认参数](#固定默认参数)
13. [UI 可调参数](#ui-可调参数)
14. [Region 切换机制](#region-切换机制)

---

## 配置文件结构

配置使用 YAML 格式，通过 `envyaml` 库加载（支持环境变量替换）。

```yaml
# env.yaml 完整模板
Deployment:
  Region: intl

CloudAPI:
  SECRET_ID: your-secret-id
  SECRET_KEY: your-secret-key

TRTC:
  SDKAPPID: 0
  SECRET: your-trtc-secret

LLMConfig:
  LLMType: openai
  Model: your-model-name
  APIKey: your-api-key
  APIUrl: your-llm-api-url
  Timeout: 5.0
  History: 20
  Temperature: 0.3
  SystemPrompt: |
    你是一名专业的客服助手...
  SystemPromptYue: |
    你係一名專業嘅客服助手...
  SystemPromptEn: |
    You are a professional customer service assistant...

WelcomeMessage:
  zh: 您好，我是AI客服小助手...
  yue: 您好，我係AI客服小助手...
  en: "Hello! I'm your AI assistant..."

AvatarConfig:
  AvatarType: tencent
  Appkey: ""
  AccessToken: ""
  VirtualmanProjectId: ""

EndKeywords:
  zh: [拜拜, 再见, 挂了, ...]
  yue: [拜拜, 再見, 收線啦, ...]
  en: [bye, goodbye, see you, ...]

FarewellMessage:
  zh: 感谢您的咨询，再见！
  yue: 多謝您嘅諮詢，再見！
  en: Thank you for your inquiry. Goodbye!

TransferKeywords:
  zh: [转人工, 人工客服, 找人工, ...]
  yue: [轉人工, 人工客服, 搵人工, ...]
  en: [transfer, human agent, real person, ...]

TransferMessage:
  zh: 好的，正在为您转接人工客服，请稍候...
  yue: 好嘅，正在為您轉接人工客服，請稍候...
  en: Sure, transferring you to a human agent, please wait...
```

---

## 部署区域

```yaml
Deployment:
  Region: intl   # intl / cn
```

| 值 | 说明 | TRTC Endpoint | TRTC Region |
|----|------|---------------|-------------|
| `intl` | 国际站账号（默认） | `trtc.intl.tencentcloudapi.com` | `ap-singapore` |
| `cn` | 中国大陆账号 | `trtc.tencentcloudapi.com` | `ap-guangzhou` |

Region 决定了 TRTC OpenAPI 的请求域名和地域参数。

---

## 腾讯云 API 密钥

```yaml
CloudAPI:
  SECRET_ID: your-secret-id
  SECRET_KEY: your-secret-key
```

用于 TRTC OpenAPI 的 TC3-HMAC-SHA256 签名。在腾讯云控制台获取（[国际站](https://console.intl.cloud.tencent.com/cam/capi) | [中国站](https://console.cloud.tencent.com/cam/capi)）。

**安全提醒**：这是主账号密钥，生产环境建议使用子账号并限制权限。

---

## TRTC 应用凭据

```yaml
TRTC:
  SDKAPPID: 0
  SECRET: your-trtc-secret
```

- `SDKAPPID`：TRTC 应用 ID，在 TRTC 控制台创建（[国际站](https://console.trtc.io/app) | [中国站](https://console.cloud.tencent.com/trtc/app)）
- `SECRET`：用于生成 UserSig 的密钥

---

## LLM 配置

```yaml
LLMConfig:
  LLMType: openai             # LLM 协议类型（目前仅支持 openai）
  Model: your-model-name      # 模型名称
  APIKey: your-api-key        # LLM API Key
  APIUrl: your-llm-api-url    # LLM API 端点（兼容 OpenAI /v1/chat/completions 协议）
  Timeout: 5.0                # 超时时间（秒）
  History: 20                 # 上下文轮数
  Temperature: 0.3            # 温度参数（越低越确定）
  SystemPrompt: |             # 中文系统提示词
    你是一名专业的客服助手...
  SystemPromptYue: |          # 粤语系统提示词（可选，默认用中文）
    你係一名專業嘅客服助手...
  SystemPromptEn: |           # 英文系统提示词（可选，默认用中文）
    You are a professional customer service assistant...
```

**重要**：LLM 由 TRTC 云端 AI Bot 调用，不是本项目后端调用。配置会通过 `StartAIConversation` API 传递给 TRTC 服务端。

> ⚠️ **数据隐私提示**：您的 LLM 配置（包括 APIKey、APIUrl、SystemPrompt）以及用户对话内容将通过 TRTC 云端服务转发给 LLM 提供商。请确保：
> 1. 了解所选 LLM 提供商的数据处理政策
> 2. 不要在 SystemPrompt 中包含敏感的业务数据
> 3. 在生产环境中评估是否需要数据脱敏措施

### 支持的 LLM 提供商

任何兼容 OpenAI 协议的 LLM 均可使用，详见官方 LLM 配置指南（[国际站](https://trtc.io/document/68338?product=conversationalai) | [中国站](https://cloud.tencent.com/document/product/647/115413)）：

**推荐：TokenHub（腾讯云统一 LLM 网关，开箱即用）**

| 配置项 | 国际站 (intl) | 中国站 (cn) |
|--------|-------------|------------|
| LLMType | `openai` | `openai` |
| APIUrl | `https://tokenhub-intl.tencentcloudmaas.com/v1/chat/completions` | `https://tokenhub.tencentmaas.com/v1/chat/completions` |
| Model | `deepseek-v4-flash`（推荐） | `deepseek-v4-flash`（推荐） |
| APIKey | [国际站 TokenHub 控制台](https://console.intl.cloud.tencent.com/tokenhub) 获取 | [中国站 TokenHub 控制台](https://console.cloud.tencent.com/tokenhub) 获取 |

也支持其他兼容 OpenAI 协议的 LLM：
- OpenAI / Azure OpenAI
- DeepSeek
- 通义千问
- 其他支持 `/v1/chat/completions` 的服务

### SystemPrompt 编写建议

1. 明确角色定位和服务范围
2. 限制回复长度（语音场景建议 3 句以内）
3. 要求纯文本输出（不使用 Markdown、括号注释等）
4. 说明何时建议转人工
5. 如有订单等结构化信息，说明如何使用

---

## 欢迎语

```yaml
WelcomeMessage:
  zh: 您好，欢迎来到云尚商城！我是AI客服小助手...
  yue: 您好，歡迎嚟到雲尚商城！我係AI客服小助手...
  en: "Welcome to CloudShop Mall! I'm your AI assistant..."
```

AI Bot 进入房间后自动播报的第一条消息。

---

## 数字人配置

```yaml
AvatarConfig:
  AvatarType: tencent                    # 数字人类型
  Appkey: ""                             # 数字人 Appkey
  AccessToken: ""                        # 数字人 Access Token
  VirtualmanProjectId: ""                # 数字人项目 ID
```

**启用条件**：`Appkey`、`AccessToken`、`VirtualmanProjectId` 三项全部非空。

**降级机制**：任一为空 → 自动降级为纯语音模式。UI 上"数字人"选项会变为灰色不可选。

启用数字人后：
- `TTSConfig.TTSType` 自动设为 `dummy`（TTS 由数字人引擎处理）
- 前端会显示数字人视频流

---

## 关键词与告别语

```yaml
EndKeywords:
  zh: [拜拜, 再见, 先挂了, 先这样, 就这样吧, 没事了, 挂了, 不需要了, 不用了]
  yue: [拜拜, 再見, 收線啦, 咁先啦, 唔使啦, 冇事啦, 掛啦]
  en: [bye, goodbye, see you, that's all, thanks bye, gotta go, i'm done]

FarewellMessage:
  zh: 感谢您光临云尚商城，祝您购物愉快，再见！
  yue: 多謝您光臨雲尚商城，祝您購物愉快，再見！
  en: Thank you for visiting CloudShop Mall. Happy shopping and goodbye!
```

**匹配机制**：前端实时检测用户 ASR 文本，命中关键词后触发 `FarewellAndStop`。

**词边界匹配**：
- 英文：`\b关键词\b`（标准词边界）
- 中文：`(^|[^\u4e00-\u9fa5A-Za-z0-9])关键词(?=[^\u4e00-\u9fa5A-Za-z0-9]|$)`

这样"再见面"不会误触发"再见"，"我没事了"不会误触发"没事了"。

---

## 转人工关键词与提示语

```yaml
TransferKeywords:
  zh: [转人工, 人工客服, 找人工, 转接人工, 真人客服, 找真人]
  yue: [轉人工, 人工客服, 搵人工, 轉接人工, 真人客服]
  en: [transfer, human agent, real person, talk to a person, speak to someone]

TransferMessage:
  zh: 好的，正在为您转接人工客服，请稍候...
  yue: 好嘅，正在為您轉接人工客服，請稍候...
  en: Sure, transferring you to a human agent, please wait...
```

命中转人工关键词后：
1. 调用 `TransferAndStop` 播报转接提示语
2. 前端显示模拟排队进度
3. 排队"失败"后恢复 AI 对话（MVP 中为模拟，生产环境对接真实呼叫中心）

---

## TTS 音色映射表

| 语言 | 性别 | VoiceId | 描述 |
|------|------|---------|------|
| zh（中文） | female | `female-kefu-xiaoyue` | 客服小悦 |
| zh（中文） | male | `male-kefu-xiaoxu` | 客服小徐 |
| yue（粤语） | female | `v-female-k3P8sL0Q` | 粤语女声 |
| yue（粤语） | male | `v-male-L4s7PqZ9` | 粤语男声 |
| en（英文） | female | `v-female-Z3x9LmQ2` | 理性女讲解 |
| en（英文） | male | `v-male-Q6p8ZxL3` | 阳光男演讲 |

TTS 引擎：`flow` 类型 + `flow_01_turbo` 模型（延迟最低）。

> 如需自定义 TTS 音色（更换声线、调整语速语调等），请参考官方 TTS 音色配置指南（[国际站](https://trtc.io/document/79682?product=conversationalai) | [中国站](https://cloud.tencent.com/document/product/647/115414)）。

---

## STT 引擎映射表

| 语言 | STTConfig.Language | 说明 |
|------|-------------------|------|
| zh（中文） | `zh` | 中文识别 |
| yue（粤语） | `zh-TW` | 粤语识别 |
| en（英文） | `en` | 英文识别 |

后端根据前端传入的 `lang` 参数自动选择 STT 引擎。

---

## 固定默认参数

这些参数在后端代码中硬编码，用户无需配置：

| 参数 | 值 | 理由 |
|------|------|------|
| `TurnDetection.SemanticEagerness` | `auto` | 平衡响应速度与耐心 |
| `FilterOneWord` | `false` | 保留"嗯""好"等应答词 |
| `WelcomeMessagePriority` | `0` | 欢迎语可被打断 |
| `MaxIdleTime` | `60s` | 客服标准空闲超时 |
| `SubtitleMode` | `1` | 句子级同步下发（非逐字） |
| `FilterBracketsContent` | `1`(zh) / `2`(en) | 过滤 LLM 输出的舞台说明 |
| `LLMConfig.Streaming` | `true` | 流式输出，首字延迟最优 |

---

## UI 可调参数

用户可通过前端 UI 调整：

| 参数 | 控件 | 取值 | 默认 | 含义 |
|------|------|------|------|------|
| 语言 | 顶部栏切换 | zh/yue/en | 跟随浏览器 | 联动 STT/TTS/Prompt/UI 文案 |
| 对话模式 | Pill 切换 | voice/avatar | voice | 需 AvatarConfig 三项全填 |
| 客服角色 | 头像卡片 | female/male | female | 影响 TTS VoiceId |
| 断句模式 | Pill 切换 | 3(语义)/0(VAD) | 3 | 语义断句用 LLM 判断 |
| 打断模式 | Pill 切换 | 0(智能)/1(手动) | 0 | 智能=自动检测打断 |
| VAD 时长 | 滑块 | 240-2000ms | 600ms | 越小响应越快 |
| 远场人声抑制 | 滑块 | 0-5 | 3 | 越高抑制越强 |
| 打断时长 | 滑块 | 240-2000ms | 600ms | 仅智能打断模式 |

---

## Region 切换机制

`config_loader.py` 中的实现：

```python
REGION_PROFILES = {
    "cn": {
        "trtc_endpoint": "trtc.tencentcloudapi.com",
        "trtc_region": "ap-guangzhou",
    },
    "intl": {
        "trtc_endpoint": "trtc.intl.tencentcloudapi.com",
        "trtc_region": "ap-singapore",
    },
}
```

配置加载时根据 `Deployment.Region` 自动选择对应的 endpoint 和 region。未知 region 值会回退到 `intl`。
