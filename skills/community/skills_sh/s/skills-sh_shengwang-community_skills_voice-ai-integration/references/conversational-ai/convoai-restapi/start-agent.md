---
title: "创建对话式智能体"
description: "创建一个对话式智能体(Conversational AI agent)实例，并加入一个 RTC 频道。"
---

# 创建对话式智能体

`POST /v2/projects/{appid}/join`

创建一个对话式智能体(Conversational AI agent)实例，并加入一个 RTC 频道。

## 鉴权

任选其一：
- RTC Token：`Authorization: agora token="{RTC_TOKEN}"`
- Basic Auth：`Authorization: Basic base64("{SHENGWANG_CUSTOMER_KEY}:{SHENGWANG_CUSTOMER_SECRET}")`

## 参数

| 名称 | 位置 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- | --- |
| `appid` | path | string | 是 | - | 你的项目使用的 [App ID](http://doc.shengwang.cn/doc/convoai/restful/get-started/enable-service#%E8%8E%B7%E5%8F%96-app-id)。 |

## 请求体

Content-Type: `application/json`

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `name` | string | 是 | - | 智能体唯一标识，相同标识不可重复创建。 |
| `properties` | object | 是 | - | 智能体详细配置。 |
| &nbsp;&nbsp;`properties.channel` | string | 是 | - | 智能体加入的 RTC 频道名。 |
| &nbsp;&nbsp;`properties.token` | string | 否 | - | 加入 RTC 频道使用的 Token，即用于鉴权的动态密钥（Token）。如果你的项目已启用 App 证书，则务必在该字段中传入你项目的动态密钥。详见[使用 Token 鉴权](https://doc.shengwang.cn/doc/rtc/android/basic-features/token-authentication)。 |
| &nbsp;&nbsp;`properties.agent_rtc_uid` | string | 是 | - | 智能体在 RTC 频道内的用户 ID。填 `"0"` 时表示随机分配，但 Token 需要相应修改。 |
| &nbsp;&nbsp;`properties.remote_rtc_uids` | string[] | 是 | - | 智能体在 RTC 频道中订阅的用户 ID 列表，只有订阅的用户才能与智能体互动。目前只支持订阅一个用户 ID。 |
| &nbsp;&nbsp;`properties.agent_rtm_uid` | string | 否 | - | &gt; 该字段已废弃，请参考 [FAQ](https://doc.shengwang.cn/faq/integration-issues/generate-token) 生成同时具备 RTC 和 RTM 权限的 Token，之后改用 `token` 字段。  智能体在 RTM 频道内的用户 ID。仅在 `advanced_features.enable_rtm` 为 `true` 时生效。 |
| &nbsp;&nbsp;`properties.enable_string_uid` | boolean | 否 | `false` | 是否启用 String UID： - `true`：智能体和订阅用户 ID 均使用 String UID。 - `false`：（默认）智能体和订阅用户 ID 均使用 Int UID。 &gt; 同一频道内，Int 型和 String 型的用户 ID 不可混用。更多使用 String UID 的相关信息请参考[如何使用 String 型用户 ID](https://doc.shengwang.cn/faq/integration-issues/string-uid)。 |
| &nbsp;&nbsp;`properties.idle_timeout` | integer | 否 | `30` | RTC 频道的最大空闲时间 (s)。检测到 `remote_rtc_uids` 中指定的用户全部离开频道后的时间视为频道空闲时间，超过设定的最大值时，频道的智能体将自动停止并退出频道。如果填写为 `0`，则直到手动退出，智能体才会停止。 |
| &nbsp;&nbsp;`properties.silence_timeout` | integer | 否 | `0` | &gt; 该字段已废弃，请改用 `parameters.silence_config`。  智能体最大静默时间 (s)，取值范围为 [0,60]。智能体创建成功，且用户加入频道后，智能体不处于倾听、思考或说话状态的持续时间称为智能体静默时间。静默时间达到设定值后，智能体将播报 `llm.silence_message` 中填写的静默提示消息，之后重新计算静默时间。 - 设置为 `0`（默认值）：表示不启用该功能。 - 设置为 (0,60] 时，必需同时设置 `llm.silence_message` 才能正常播报静默提示消息，否则设置无效。 |
| &nbsp;&nbsp;`properties.advanced_features` | object | 否 | - | 高级功能配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.advanced_features.enable_aivad` | boolean | 否 | `false` | &gt; 该字段已废弃，请改用 `turn_detection.config.end_of_speech.mode.semantic` 实现。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.advanced_features.enable_rtm` | boolean | 否 | `false` | 是否启用实时消息 RTM 服务。启用后智能体会自动登录 RTM 并订阅 `channel` 中指定的频道，可结合 RTM 提供的能力实现一些进阶功能，例如[传递自定义信息](https://doc.shengwang.cn/doc/convoai/restful/user-guides/custom-data)。  &gt; 启用 RTM 服务前需要确保 Token 同时具备 RTC 和 RTM 权限。智能体加入 RTM 频道会复用 `token` 字段配置的 Token。你可以参考 [FAQ](https://doc.shengwang.cn/faq/integration-issues/generate-token) 了解如何生成同时具备 RTC 和 RTM 权限的 Token。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.advanced_features.enable_sal` | boolean | 否 | `false` | 是否启用选择性注意力锁定（Selective Attention Locking, SAL）功能。启用后，在 `sal` 字段中完成相关设置，智能体即可识别用户的声纹特征，有效区分不同说话者，屏蔽 95% 的环境人声、噪声。 &gt; 该功能目前处于 Beta 阶段。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.advanced_features.enable_tools` | boolean | 否 | `false` | 是否启用工具调用功能。启用后，智能体可以调用 MCP 服务器提供的工具，实现更复杂的业务逻辑。 |
| &nbsp;&nbsp;`properties.asr` | object | 否 | - | 自动语音识别 (ASR) 配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.asr.language` | string | 否 | `"zh-CN"` | 用户与智能体互动时使用的语言： - `zh-CN`：中文（支持中英文混合） - `en-US`：英语 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.asr.vendor` | string | 否 | - | ASR 服务供应商，可选以下值： - `fengming`：（默认）声网凤鸣 ASR。 - `tencent`：腾讯 ASR。 - `microsoft`：微软 ASR。 - `xfyun`：讯飞云传统语音转写识别服务。 - `xfyun_bigmodel`：讯飞云语音识别大模型服务。 - `xfyun_dialect`：讯飞云方言自由说识别服务。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.asr.params` | oneOf | 否 | - | ASR 配置参数。不同 ASR 供应商下该参数结构不同。 &gt; 各供应商示例代码中未提及的参数，声网对话式 AI 引擎不保证完全支持。 |
| &nbsp;&nbsp;`properties.tts` | object | 是 | - | 文本转语音 (TTS) 模块配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.tts.vendor` | string | 是 | - | TTS 供应商，支持传入以下值： - `minimax`：Minimax TTS - `tencent`：腾讯 TTS - `bytedance`：火山引擎 TTS - `microsoft`：微软 Azure TTS - `cosyvoice`：阿里云 CosyVoice TTS - `bytedance_duplex`：火山引擎双向流式 TTS - `stepfun`：阶跃星辰 TTS |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.tts.skip_patterns` | integer[] | 否 | `[]` | 过滤模式配置，用于控制是否跳过 LLM 返回文本中括号内的内容，避免智能体播报不必要的结构性提示信息如语气、动作描述等。默认值为 `[]`，即不过滤任何内容。可选值如下，传入即启用该功能：  - `1`：跳过中文圆括号（ ）中的内容 - `2`：跳过中文方括号【 】中的内容 - `3`：跳过英文圆括号 ( ) 中的内容 - `4`：跳过英文方括号 [ ] 中的内容 - `5`：跳过英文花括号 \{ } 中的内容  &gt; - 当输入文本中存在嵌套括号，且多种括号类型都被配置为跳过时，智能体只处理最外层括号，即系统将从文本的起始位置开始匹配，一旦找到第一个符合跳过规则的最外层括号对，该括号对及其包含的所有内容（包括任何嵌套的其他类型括号）都将被整体跳过。 &gt; - 无论是否打开[实时字幕](https://doc.shengwang.cn/doc/convoai/restful/user-guides/realtime-sub)，智能体短期记忆都会包含被过滤的内容，即 LLM 生成的完整文本。 &gt; - 开启[实时字幕](https://doc.shengwang.cn/doc/convoai/restful/user-guides/realtime-sub)时，实时字幕在 TTS 播报时不会包含被过滤的内容，等这句话播报完毕后，字幕会把这些内容添加回来。 &gt; - 火山引擎双向流式 TTS 暂不支持该功能。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.tts.params` | oneOf | 是 | - | TTS 配置参数。不同 TTS 供应商下该参数结构不同。 &gt; 各供应商示例代码中未提及的参数，声网对话式 AI 引擎不保证完全支持。 |
| &nbsp;&nbsp;`properties.llm` | object | 是 | - | 大语言模型 (LLM) 配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.url` | string | 是 | - | LLM 回调地址，要求与 OpenAI 协议兼容。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.api_key` | string | 否 | - | LLM 校验 api key。默认为空，生产环境中务必启用 api key。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.system_messages` | object[] | 否 | - | 一组每次调用 LLM 时被附加在最前的预定义信息，用于控制 LLM 输出。可以是角色设定、提示词和回答样例等。要求与 OpenAI 协议兼容。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.params` | object | 否 | - | 在消息体内传输的 LLM 附加信息，例如使用的模型、最大 Token 数限制等。不同的 LLM 供应商支持的配置不同，请参考对应文档按需填入。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.max_history` | integer | 否 | `32` | LLM 中缓存的短期记忆条目数。取值范围为 `[1,1024]`。短期记忆包括用户和智能体对话消息、工具调用信息和时间戳。智能体和用户会单独记录短期记忆条目。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.input_modalities` | string[] | 否 | - | LLM 的输入模态，支持： - `["text"]`：（默认）仅文字。 - `["text", "image"]`：文字加图片，要求所选 LLM 支持视觉模态输入。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.output_modalities` | string[] | 否 | - | LLM 的输出模态，支持： - `["text"]`：（默认）仅文字。输出的文字会经过 TTS 模块转换成语音后发布至 RTC 频道。 - `["audio"]`：仅语音。语音会直接发布至 RTC 频道。 - `["text", "audio"]`：文字加语音。你可以自行编写逻辑，按需处理 LLM 的输出。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.greeting_message` | string | 否 | - | 智能体问候语。如果填写，则在频道内没有订阅用户列表 (`remote_rtc_uids`) 中的用户时，智能体会自动向首位加入频道的订阅用户发送问候语。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.greeting_configs` | object | 否 | - | 智能体问候语播报配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.greeting_configs.mode` | string | 否 | - | 智能体问候语播报模式，支持以下选项： - `"single_every"`：（默认）每次有用户加入空频道时，智能体都播报一次问候语。 - `"single_first"`：仅首位用户加入空频道时，智能体播报一次问候语。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.failure_message` | string | 否 | - | 智能体处理失败提示语。如果填写，则在 LLM 调用错误时会通过 TTS 模块返回。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.silence_message` | string | 否 | - | &gt; 该字段已废弃，请改用 `parameters.silence_config`。  静默提示消息。默认为空字符串。智能体创建成功，且用户加入频道后，智能体不处于倾听、思考或说话状态的持续时间称为智能体静默时间。静默时间达到 `silence_timeout` 中设定的值后，智能体将播报静默提示消息。`silence_timeout` 设置为 `0` 时，该参数无效。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.vendor` | string | 否 | - | LLM 供应商，支持以下两种设置： - 商业大模型供应商，支持以下值：   - `aliyun`：阿里云   - `bytedance`：字节跳动   - `deepseek`：深度求索   - `tencent`：腾讯    设置后，将保证最大兼容性，避免因携带了 LLM 不支持的信息导致请求失败。 - 自定义 LLM，即设为 `"custom"`。设置后智能体调用 custom LLM 时，除了 `role` 和 `content` 外，将额外携带以下信息：   - `turn_id`：唯一的对话轮次标识符。`turn_id` 从 0 开始递增，用户和智能体的一轮对话对应一个 `turn_id`。   - `timestamp`：请求时间戳，精度为毫秒。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.mcp_servers` | object[] | 否 | - | MCP (Model Context Protocol) 服务器配置列表。通过配置 MCP 服务器，智能体可以调用外部服务提供的工具，实现更复杂的业务逻辑。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.mcp_servers[].name` | string | 是 | - | MCP 服务器的唯一标识。长度不超过 48 字符，支持以下字符： - 所有小写英文字母：a 到 z - 所有大写英文字母：A 到 Z - 所有数字字符：0 到 9 - "." 和 "-" |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.mcp_servers[].endpoint` | string | 是 | - | MCP 服务器的端点地址，智能体将通过该地址与 MCP 服务器通信。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.mcp_servers[].transport` | string | 否 | - | 传输协议类型，支持传入以下值： - `"streamable_http"`：流式 HTTP 协议 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.mcp_servers[].headers` | object | 否 | - | 请求 MCP 服务器时携带的 HTTP 头部信息，例如认证信息。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.mcp_servers[].allowed_tools` | string[] | 否 | - | 允许智能体调用的工具列表。只有在此列表中的工具才能被智能体使用。 &gt; `allowed_tools` 字段生效规则: &gt; - 不填写 `allowed_tools` 字段：所有工具都生效 &gt; - 填写 `allowed_tools` 字段： &gt;    - 填写为 `[]`：所有工具不生效 &gt;    - 填写为 `["*"]`：所有工具生效 &gt;    - 填写为 `["aa", "bb", "cc"]`：`aa`、`bb`、`cc` 生效 &gt;    - 填写为 `["aa", "bb", "*"]`：所有工具生效 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.mcp_servers[].timeout_ms` | integer | 否 | `10000` | MCP 服务器请求超时时间，单位为毫秒。请求超时后，智能体将不会等待 MCP 服务器响应，而是继续执行后续逻辑。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.llm.template_variables` | object | 否 | - | 动态参数配置，用于在智能体的 `system_messages`、`greeting_message`、`failure_message` 和 `parameters.silence_config.content` 文本中插入变量。键值对形式，键为变量名，值为变量值。  **使用方式**:在 Prompt 文本中使用 `{{variable_name}}` 格式引用变量，系统会自动将其替换为 `template_variables` 中定义的对应值。 &gt; 注意：变量名和变量值不支持引用其他变量。例如自定义变量 `"farewell": "期待下次再见，{{name}}"`，其中的 `{{name}}` 不会被解析。 |
| &nbsp;&nbsp;`properties.avatar` | object | 否 | - | 数字人 (Avatar) 配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.avatar.enable` | boolean | 否 | - | 是否为智能体启用数字人功能： - `true`：启用。启用后需配置 `vendor` 和 `params` 字段。 - `false`：（默认）不启用。  &gt; 开启数字人功能将产生 RTC 视频通话费用，详见 [RTC 计费说明](https://doc.shengwang.cn/doc/rtc/android/billing/billing-strategy)。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.avatar.vendor` | string | 否 | - | 数字人供应商，支持传入以下值： - `sensetime`：商汤数字人 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.avatar.params` | oneOf | 否 | - | 数字人配置参数。不同数字人供应商下该参数结构不同。 &gt; 各供应商示例代码中未提及的参数，声网对话式 AI 引擎不保证完全支持。 |
| &nbsp;&nbsp;`properties.turn_detection` | object | 否 | - | 对话轮次检测设置，用于控制语音活动检测和对话轮次判定逻辑。   该配置支持多种检测模式组合：  - **Start of Speech (SoS)**：支持 VAD、关键词、禁用三种模式。  - **End of Speech (EoS)**：支持 VAD 和语义两种模式。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.turn_detection.mode` | `default` | 否 | `"default"` | 对话轮次检测模式，当前支持以下值： - `"default"`：（默认）默认模式，使用标准的对话轮次检测配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.turn_detection.config` | object | 否 | - | 对话轮次检测详细配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.turn_detection.config.speech_threshold` | number(float) | 否 | `0.5` | 语音识别灵敏度，取值范围为 (0.0, 1.0)。决定音频信号中何种程度的声音被视为"语音活动"。较低的值会使智能体更容易检测到语音，较高的值则可能忽略微弱声音。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.turn_detection.config.start_of_speech` | object | 否 | - | 对话开始 (Start of Speech, SoS) 检测配置，用于判定用户何时开始说话。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.turn_detection.config.end_of_speech` | object | 否 | - | 对话结束 (End of Speech, EoS) 检测配置，用于判定用户何时结束说话。 |
| &nbsp;&nbsp;`properties.sal` | object | 否 | - | 选择性注意力锁定（Selective Attention Locking, SAL）配置。 &gt; 该功能目前处于 Beta 阶段。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.sal.sal_mode` | string | 否 | `"locking"` | 选择性注意力锁定模式，支持以下选项： - `"locking"`：（默认）主讲人锁定模式。智能体锁定主讲人，屏蔽 95% 的环境人声、噪声。该模式可通过两种方式启用：   - 无感识别：用户在对话初期大声、清晰地说话，智能体即可自动将用户识别为主讲人。   - 预注册：创建智能体时，通过 `sample_urls` 字段预注册一名主讲人的声纹 URL，智能体将根据预注册的声纹 URL 锁定主讲人。 - `"recognition"`：声纹识别模式。你可以通过 `sample_urls` 字段预注册声纹 URL，目前仅支持单声纹注册。智能体将识别不同的说话人并抑制其他背景人声和环境噪音。识别到的说话人身份会通过 `metadata` 字段里的 `vpids` 字段标识并发送给 LLM，你需要将 `llm.vendor` 设置为 `"custom"`，并参考[自定义大模型](https://doc.shengwang.cn/doc/convoai/restful/user-guides/custom-llm)了解如何让 LLM 处理说话人信息。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.sal.sample_urls` | object | 否 | - | 注册声纹 URL，为键值对形式，键为注册的声纹名称，值为对应说话者的声纹 URL 下载地址。 &gt; - 传入的声纹名称不可设置为 `"unknown"`，这是一个保留关键字，用于标识未知说话人。 &gt; - 对于注册的声纹，需满足以下条件： &gt;   - 数量: 每个任务请求的注册声纹URL数量，目前仅支持单声纹，数量为 1 个。 &gt;   - 大小: 单个声纹文件不得超过 2 MB。 &gt;   - 时长：时长为 10 到 15 秒, 其中有效音频不小于 8 秒（不能有太多静音段）。 &gt;   - 格式: 必须为 16k 采样率、16bit 位深、单声道的 PCM 音频文件，文件名后缀必须为 `.pcm`。 |
| &nbsp;&nbsp;`properties.labels` | object | 否 | - | 自定义标签，键值对形式，键为标签名，值为标签值。用于让智能体携带自定义业务信息。  这些自定义信息会与智能体绑定，并在对话式 AI 引擎所有类型消息通知回调的 `payload` 字段中返回，可用于实现自定义业务逻辑，例如标记活动 ID、客户分组、业务场景等。 |
| &nbsp;&nbsp;`properties.rtc` | object | 否 | - | RTC 媒体内容加密配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.rtc.encryption_key` | string | 否 | - | 字符串类型的加密密钥，长度不受限制。声网建议使用 32 字节的密钥。 &gt; 如果未设置加密密钥或将其设置为空，则无法使用内置加密。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.rtc.encryption_salt` | string | 否 | - | 用于加密的盐值，Base64 编码的字符串，解码后长度为 32 字节。 &gt; 该参数仅在 `encryption_mode` 设为 `7`（AES_128_GCM2）或 `8`（AES_256_GCM2）时生效。在此情况下，请确保该参数不为空。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.rtc.encryption_mode` | integer | 否 | - | 内置加密模式，支持以下值： - `1`: AES_128_XTS - 128 位 AES 加密，XTS 模式。 - `2`: AES_128_ECB - 128 位 AES 加密，ECB 模式。 - `3`: AES_256_XTS - 256 位 AES 加密，XTS 模式。 - `4`: SM4_128_ECB - 128 位 SM4 加密，ECB 模式。 - `5`: AES_128_GCM - 128 位 AES 加密，GCM 模式。 - `6`: AES_256_GCM - 256 位 AES 加密，GCM 模式。 - `7`: AES_128_GCM2 - 128 位 AES 加密，GCM 模式。该模式需设置 salt（`encryption_salt`）。 - `8`: AES_256_GCM2 - 256 位 AES 加密，GCM 模式。该模式需设置 salt（`encryption_salt`）。  &gt; 声网建议使用 `7`（AES_128_GCM2）或 `8`（AES_256_GCM2）模式，这两种模式支持使用加密盐以提升安全性。 |
| &nbsp;&nbsp;`properties.filler_words` | object | 否 | - | 垫词功能 (Beta) 配置，用于在 LLM 响应等待时播报垫词，缓解用户等待焦虑，提升对话流畅度。  垫词播报遵循以下规则： - **播报顺序**：当多个垫词或 LLM 响应等待播报时，按照文本到达的先后顺序进行播报。 - **打断控制**：继承全局配置中的打断模式设置 (`turn_detection.config`)。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.filler_words.enable` | boolean | 否 | `false` | 是否启用垫词功能： - `true`：启用。 - `false`：（默认）不启用。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.filler_words.trigger` | object | 否 | - | 垫词触发配置，定义何时触发垫词播报。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.filler_words.trigger.mode` | string | 否 | - | 垫词触发模式，支持以下值： - `"fixed_time"`：固定时间触发。当 LLM 响应等待时间超过设定阈值时触发垫词播报。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.filler_words.trigger.{mode}_config` | oneOf | 否 | - | 垫词触发配置参数。不同触发模式下该参数名称和结构不同。 &gt; - 传入的配置类型需要和 `mode` 相匹配。例如 `mode` 为 `"fixed_time"` 时，需传入 `fixed_time_config` 对应的配置。 &gt; - 不可同时传入多个模式配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.filler_words.content` | object | 否 | - | 垫词内容配置，定义垫词的来源和选择规则。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.filler_words.content.mode` | string | 否 | - | 垫词内容模式，支持以下值： - `"static"`：静态垫词。使用预定义的垫词列表。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.filler_words.content.{mode}_config` | oneOf | 否 | - | 垫词内容配置参数。不同内容模式下该参数名称和结构不同。 &gt; - 传入的配置类型需要和 `mode` 相匹配。例如 `mode` 为 `"static"` 时，需传入 `static_config` 对应的配置。 &gt; - 不可同时传入多个模式配置。 |
| &nbsp;&nbsp;`properties.parameters` | object | 否 | - | 智能体参数配置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.silence_config` | object | 否 | - | 智能体静默设置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.silence_config.timeout_ms` | integer | 否 | - | 智能体最大静默时间 (ms)，取值范围为 [0,60000]。智能体创建成功，且用户加入频道后，智能体不处于倾听、思考或说话状态的持续时间称为智能体静默时间。静默时间达到设定值后，智能体将播报静默提示消息。该功能可用于在用户不活跃时让智能体提醒用户。 - 设置为 `0`（默认值）：表示不启用该功能。 - 设置为 `(0,60000]` 时，必需同时设置 `content` 才能正常播报静默提示，否则设置无效。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.silence_config.action` | string | 否 | - | 静默时间达到设定值后，智能体采取的行为，可设为以下值： - `"speak"`：（默认）使用 TTS 模块播报静默提示内容 (`content`)。 - `"think"`：将静默提示内容 (`content`) 追加在上下文的最后，并传递给 LLM。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.silence_config.content` | string | 否 | - | 静默提示消息的内容。设置的内容会根据 `action` 中的设置以不同的方式使用。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.farewell_config` | object | 否 | - | 智能体优雅挂断设置。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.farewell_config.graceful_enabled` | boolean | 否 | `false` | 是否启用优雅退出（Graceful Leave）功能： - `true`：启用。开启后，调用 [POST 停止对话式智能体](https://doc.shengwang.cn/doc/convoai/restful/convoai/operations/stop-agent)接口，让智能体退出频道时，会确保智能体处于静默状态（`IDLE`）后再离开频道。 - `false`：（默认）不启用。 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.farewell_config.graceful_timeout_seconds` | integer | 否 | `30` | 优雅退出超时时间 (s)，表示在退出频道前等待智能体进入静默状态（`IDLE`）的最长时间，超出该时间后，即便智能体不处于静默状态，也会立即退出频道。该字段仅在 `graceful_enabled` 为 `true` 时生效，取值范围为 [0,120]。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.data_channel` | string | 否 | - | 智能体数据传输通道，可选以下值： - `rtm`：使用 RTM 传输。该配置仅在 `advanced_features.enable_rtm` 为 `true` 时生效。  - `datastream`：（默认）使用 RTC 的 [`DataStream`](https://doc.shengwang.cn/api-ref/rtc/android/API/toc_datastream#callback_irtcengineeventhandler_onstreammessage) 传输。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.enable_metrics` | boolean | 否 | `false` | 是否接收智能体性能数据： - `true`：接收。 - `false`：（默认）不接收。  该配置仅在 `advanced_features.enable_rtm` 为 `true` 时生效。你可以参考[监听智能体事件](https://doc.shengwang.cn/doc/convoai/restful/user-guides/listen-agent-events)了解如何使用客户端组件接收智能体性能数据，或参考[接收 Webhook 事件](https://doc.shengwang.cn/doc/convoai/restful/webhook/enable-ncs)了解如何使用 Webhook 接收智能体性能数据。 |
| &nbsp;&nbsp;&nbsp;&nbsp;`properties.parameters.enable_error_message` | boolean | 否 | `false` | 是否接收智能体错误事件： - `true`：接收。 - `false`：（默认）不接收。  该配置仅在 `advanced_features.enable_rtm` 为 `true` 时生效。你可以参考[监听智能体事件](https://doc.shengwang.cn/doc/convoai/restful/user-guides/listen-agent-events)了解如何使用客户端组件接收智能体错误事件。 |

### 请求示例

<details>
<summary>Defalut</summary>

```json
{
  "name": "unique_name",
  "properties": {
    "channel": "channel_name",
    "token": "token",
    "agent_rtc_uid": "0",
    "remote_rtc_uids": [
      "123"
    ],
    "enable_string_uid": false,
    "idle_timeout": 120,
    "advanced_features": {
      "enable_aivad": true
    },
    "llm": {
      "url": "https://api.minimax.chat/v2/text/chatcompletion_v2",
      "api_key": "xxx",
      "system_messages": [
        {
          "role": "system",
          "content": "You are a helpful chatbot."
        }
      ],
      "greeting_message": "您好，有什么可以帮您？",
      "failure_message": "抱歉，我无法回答这个问题。",
      "max_history": 32,
      "params": {
        "model": "abab6.5s-chat",
        "max_token": 1024,
        "userName": "Tomas"
      }
    },
    "asr": {
      "language": "zh-CN",
      "vendor": "fengming"
    },
    "tts": {
      "vendor": "minimax",
      "skip_patterns": [
        1
      ],
      "params": {
        "group_id": "xxxx",
        "key": "xxxx",
        "model": "speech-01-turbo",
        "voice_setting": {
          "voice_id": "female-shaonv",
          "speed": 1,
          "vol": 1,
          "pitch": 0,
          "emotion": "happy"
        },
        "audio_setting": {
          "sample_rate": 16000
        }
      }
    }
  }
}
```
</details>

<details>
<summary>使用 String uid</summary>

```json
{
  "name": "unique_name",
  "properties": {
    "channel": "channel_name",
    "token": "token",
    "agent_rtc_uid": "friday",
    "remote_rtc_uids": [
      "*"
    ],
    "enable_string_uid": true,
    "idle_timeout": 120,
    "advanced_features": {
      "enable_aivad": true
    },
    "llm": {
      "url": "https://api.minimax.chat/v1/text/chatcompletion_v2",
      "api_key": "xxx",
      "system_messages": [
        {
          "role": "system",
          "content": "You are a helpful chatbot."
        }
      ],
      "greeting_message": "您好，有什么可以帮您？",
      "failure_message": "抱歉，我无法回答这个问题。",
      "max_history": 32,
      "params": {
        "model": "abab6.5s-chat",
        "max_tokens": 1024,
        "userName": "Tomas"
      }
    },
    "asr": {
      "language": "zh-CN",
      "vendor": "fengming"
    },
    "tts": {
      "vendor": "tencent",
      "skip_patterns": [
        1,
        3
      ],
      "params": {
        "group_id": "xxx",
        "key": "xxx",
        "model": "speech-01-turbo",
        "voice_setting": {
          "voice_id": "female-shaonv",
          "speed": 1,
          "vol": 1,
          "pitch": 0,
          "emotion": "happy"
        },
        "audio_setting": {
          "sample_rate": 16000
        }
      }
    }
  }
}
```
</details>

<details>
<summary>完整配置示例</summary>

```json
{
  "name": "full_config_agent",
  "properties": {
    "channel": "full_channel_name",
    "token": "full_token_value",
    "agent_rtc_uid": "12345",
    "remote_rtc_uids": [
      "67890"
    ],
    "enable_string_uid": false,
    "idle_timeout": 180,
    "silence_timeout": 30,
    "advanced_features": {
      "enable_aivad": true,
      "enable_rtm": true,
      "enable_sal": true
    },
    "asr": {
      "language": "zh-CN",
      "vendor": "microsoft",
      "params": {
        "key": "your_microsoft_key",
        "region": "chinaeast2",
        "language": "zh-CN",
        "phrase_list": [
          "agora",
          "fengming"
        ]
      }
    },
    "tts": {
      "vendor": "microsoft",
      "skip_patterns": [
        1,
        2
      ],
      "params": {
        "key": "your_microsoft_key",
        "region": "chinaeast2",
        "voice_name": "zh-CN-YunxiNeural",
        "speed": 1,
        "volume": 70,
        "sample_rate": 24000
      }
    },
    "llm": {
      "url": "https://api.openai.com/v1/chat/completions",
      "api_key": "your_openai_api_key",
      "system_messages": [
        {
          "role": "system",
          "content": "You are a professional AI assistant. User name is {{user_name}}."
        }
      ],
      "greeting_message": "您好{{user_name}}，我是您的智能助手，有什么可以帮您？",
      "greeting_configs": {
        "mode": "single_every"
      },
      "failure_message": "抱歉，系统出现问题，请稍后再试。",
      "max_history": 64,
      "input_modalities": [
        "text",
        "image"
      ],
      "output_modalities": [
        "text"
      ],
      "vendor": "custom",
      "params": {
        "model": "gpt-4o",
        "temperature": 0.8,
        "max_tokens": 2048,
        "stream": true
      },
      "template_variables": {
        "user_name": "张三",
        "company_name": "声网科技"
      }
    },
    "avatar": {
      "enable": true,
      "vendor": "sensetime",
      "params": {
        "agora_token": "avatar_token",
        "agora_uid": "99999",
        "appId": "sensetime_app_id",
        "app_key": "sensetime_app_key",
        "sceneList": [
          {
            "digital_role": {
              "face_feature_id": "face_feature_id_001",
              "position": {
                "x": 0,
                "y": 0
              },
              "url": "https://example.com/avatar_model.zip"
            }
          }
        ]
      }
    },
    "turn_detection": {
      "mode": "default",
      "config": {
        "speech_threshold": 0.5,
        "start_of_speech": {
          "mode": "vad",
          "vad_config": {
            "interrupt_duration_ms": 160,
            "speaking_interrupt_duration_ms": 320,
            "prefix_padding_ms": 800
          }
        },
        "end_of_speech": {
          "mode": "semantic",
          "semantic_config": {
            "silence_duration_ms": 320,
            "max_wait_ms": 3000
          }
        }
      }
    },
    "sal": {
      "sal_mode": "locking",
      "sample_urls": {
        "speaker1": "https://example.com/voiceprint1.pcm"
      }
    },
    "labels": {
      "campaign_id": "spring_2025",
      "customer_group": "vip",
      "region": "east_china"
    },
    "rtc": {
      "encryption_key": "your_32_byte_encryption_key_here",
      "encryption_salt": "TsP4fLLyxxxxxxxxxroLA9oE=",
      "encryption_mode": 8
    },
    "filler_words": {
      "enable": true,
      "trigger": {
        "mode": "fixed_time",
        "config": {
          "response_wait_ms": 1500
        }
      },
      "content": {
        "mode": "static",
        "config": {
          "phrases": [
            "请稍等。",
            "好的。",
            "嗯嗯。"
          ],
          "selection_rule": "shuffle"
        }
      }
    },
    "parameters": {
      "silence_config": {
        "timeout_ms": 15000,
        "action": "think",
        "content": "用户长时间未响应，请主动询问是否需要继续服务。"
      },
      "farewell_config": {
        "graceful_enabled": true,
        "graceful_timeout_seconds": 60
      },
      "data_channel": "rtm",
      "enable_metrics": true,
      "enable_error_message": true
    }
  }
}
```
</details>

<details>
<summary>接入 MCP</summary>

```json
{
  "name": "unique_name",
  "properties": {
    "channel": "channel_name",
    "token": "token",
    "agent_rtc_uid": "0",
    "remote_rtc_uids": [
      "*"
    ],
    "idle_timeout": 120,
    "advanced_features": {
      "enable_aivad": true
    },
    "llm": {
      "url": "https://api.minimax.chat/v2/text/chatcompletion_v2",
      "api_key": "xxx",
      "system_messages": [
        {
          "role": "system",
          "content": "You are a helpful assistant. User name is {{user_name}}, and their account ID is {{account_id}}."
        }
      ],
      "greeting_message": "您好 {{user_name}}，有什么可以帮您？",
      "failure_message": "抱歉 {{user_name}}，我无法回答这个问题。请稍后再试。",
      "max_history": 32,
      "params": {
        "model": "abab6.5s-chat",
        "max_token": 1024
      },
      "template_variables": {
        "user_name": "张三",
        "account_id": "ACC123456",
        "silent_prompt": "用户长时间未响应，请询问是否需要继续服务。"
      },
      "mcp_servers": [
        {
          "name": "mcpserver",
          "endpoint": "https://registry.run.mcp.com.ai/mcp",
          "transport": "streamable_http",
          "headers": {
            "Authentication": "Basic xxxx"
          },
          "allowed_tools": [
            "getV01Servers"
          ]
        }
      ]
    },
    "asr": {
      "language": "zh-CN",
      "vendor": "fengming"
    },
    "tts": {
      "vendor": "minimax",
      "skip_patterns": [
        1
      ],
      "params": {
        "group_id": "xxxx",
        "key": "xxxx",
        "model": "speech-01-turbo",
        "voice_setting": {
          "voice_id": "female-shaonv",
          "speed": 1,
          "vol": 1,
          "pitch": 0,
          "emotion": "happy"
        },
        "audio_setting": {
          "sample_rate": 16000
        }
      }
    },
    "parameters": {
      "silence_config": {
        "timeout_ms": 10000,
        "action": "think",
        "content": "{{silent_prompt}}"
      }
    }
  }
}
```
</details>

## 响应

### 200

- 若返回的状态码为 `200` 则表示请求成功。响应包体中包含本次请求的结果。
- 若返回的状态码不为 `200` 则表示请求失败。响应包体中包含错误的类别和描述，你可以参考[响应状态码](https://doc.shengwang.cn/doc/convoai/restful/api/response-code)了解可能的原因。

| 字段 | 类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `agent_id` | string | 否 | - | 对话式智能体 ID，即智能体唯一标识。 |
| `create_ts` | integer | 否 | - | 智能体创建时间戳。 |
| `status` | string | 否 | - | 智能体运行状态： - `IDLE` (0)：空闲状态的智能体。 - `STARTING` (1)：正在启动的智能体。 - `RUNNING` (2)：正在运行的智能体。 - `STOPPING` (3)：正在停止的智能体。 - `STOPPED` (4)：已完成退出的智能体。 - `RECOVERING` (5)：正在恢复的智能体。 - `FAILED` (6)：执行失败的智能体。 |

**响应示例**

**Example 1**

```json
{
  "agent_id": "1NT29X10YHxxxxxWJOXLYHNYB",
  "create_ts": 1737111452,
  "status": "RUNNING"
}
```

## 服务器

- `https://api.agora.io/cn/api/conversational-ai-agent`
