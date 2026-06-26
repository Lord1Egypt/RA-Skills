# Qwen-Omni API Notes

官方文档：

- https://help.aliyun.com/zh/model-studio/qwen-omni
- https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api
- https://help.aliyun.com/zh/model-studio/stream

## 当前 skill 使用方式

- 接口：`POST /chat/completions`
- Base URL（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 鉴权：`Authorization: Bearer $DASHSCOPE_API_KEY`
- 输出：强制流式
- 会话历史：由本地脚本管理，服务端仍然是标准 `messages` 多轮输入
- 凭证来源：优先读取环境变量，也支持本地 `config.json`

## 配置与覆盖规则

- 模型选择：`CLI --model > DASHSCOPE_MODEL > selectionPolicy=auto > config.defaultModel > config.model > 内置默认`
- Base URL：`DASHSCOPE_BASE_URL > config.baseUrl > 内置默认`
- 音色选择：`CLI --voice > DASHSCOPE_VOICE > config.voiceByModelFamily[模型家族] > config.voice > 内置默认`
- API Key：`DASHSCOPE_API_KEY > config.apiKey`
- `selectionPolicy=fixed|auto`
  - `fixed`：按默认模型走，不自动切换
  - `auto`：音频/视频理解优先 `qwen3.5-omni-plus`，文本/图片理解与语音输出优先 `qwen3.5-omni-flash`
- `config.modelCandidates` 用于维护候选模型列表；`selectionPolicy=auto` 时会优先在候选列表里选模型
- `config.voiceByModelFamily` 用于给不同模型家族配置不同默认音色
- `--dry-run` 不要求 API Key，但仍会校验本地文件、打印价格提醒和脱敏后的请求体预览

## 当前支持的模型选择

- 默认模型：`qwen3.5-omni-flash`
- 可显式切换到：
  - `qwen3.5-omni-plus`
  - `qwen3.5-omni-plus-2026-03-15`
  - `qwen3.5-omni-flash`
  - `qwen3.5-omni-flash-2026-03-15`
  - `qwen3-omni-flash`
  - `qwen3-omni-flash-2025-12-01`
  - `qwen3-omni-flash-2025-09-15`
  - `qwen-omni-turbo`
  - `qwen-omni-turbo-latest`
  - `qwen-omni-turbo-2025-03-26`
  - `qwen-omni-turbo-2025-01-19`
- 当前 skill 支持受约束的自动选型；是否自动切换模型由 `selectionPolicy` 决定
- 推荐在 `config.json` 中使用 `selectionPolicy` 管理自动选型开关，用 `defaultModel` 管理兜底默认模型，用 `modelCandidates` 管理候选列表
- 价格取舍基于你提供的中国内地价格表：
  - `qwen3.5-omni-flash`：成本更低，适合默认文本/图片理解与语音输出
  - `qwen3.5-omni-plus`：长音频、长视频与复杂跨模态理解更稳
  - `qwen-omni-turbo`：保留显式兼容，不再作为默认自动选型目标
- 当前脚本的自动选型默认在 `qwen3.5-omni-flash` 和 `qwen3.5-omni-plus` 间切换；旧模型作为显式兼容项保留

## 当前支持的音色选择

- `--with-audio` 时，脚本会按模型家族校验 `voice`
- 可用 `--list-voices --model <model>` 查看当前模型家族支持的音色
- `qwen3.5-omni` 当前内置全部 55 个官方音色，默认音色为 `Tina(甜甜 Tina)`
- 常用示例：`Tina`、`Serena`、`Ethan`、`Katerina`、`Jennifer`、`Ryan`、`Sunny`、`Dylan`、`Rocky`、`Chloe`
- `qwen-omni-turbo` 当前内置音色：
  - `Cherry(辛悦)`、`Serena(苏瑶)`、`Ethan(晨煦)`、`Chelsie(千雪)`
- `qwen3-omni-flash` 当前内置音色：
  - `Cherry(辛悦)`、`Ethan(晨煦)`、`Nofish(不吃鱼)`、`Jennifer(詹妮弗)`、`Ryan(甜茶)`
  - `Katerina(卡捷琳娜)`、`Elias(墨讲师)`、`Jada(上海-阿珍)`、`Dylan(北京-晓东)`、`Sunny(四川-晴儿)`
  - `Li(南京-老李)`、`Marcus(陕西-秦川)`、`Roy(闽南-阿杰)`、`Peter(天津-李彼得)`、`Rocky(粤语-阿强)`、`Kiki(粤语-阿清)`、`Eric(四川-程川)`
- 如果配置或 CLI 指定了当前模型不支持的音色，脚本会直接报错，并给出可选列表

## 内容类型

- 文本：`{ "type": "text", "text": "..." }`
- 图片：`{ "type": "image_url", "image_url": { "url": "..." } }`
- 音频：`{ "type": "input_audio", "input_audio": { "data": "...", "format": "mp3" } }`
- 视频文件：`{ "type": "video_url", "video_url": { "url": "...", "fps": 2.0 } }`
- 图片列表形式视频：`{ "type": "video", "video": ["url1", "url2"] }`

本地文件应转换成 Base64 Data URL。

## 约束

- Qwen-Omni 只支持流式调用
- 一条 `user` 消息只允许文本加一种模态
- `Qwen3.5-Omni` 的图片列表视频要求 4 到 512 帧
- `qwen3-omni-flash` 的图片列表视频要求 2 到 128 帧
- 文本加音频输出时，要传 `modalities: ["text", "audio"]`
- `qwen3.5-omni-plus` 和 `qwen3.5-omni-flash` 不支持思考模式
- `qwen3-omni-flash` 开启思考模式时，不支持音频输出

## 当前脚本的多轮策略

- 会话文件保存在 `sessions/<session-id>.json`
- `auto` 模式下，新图片/音频/视频输入默认视为新话题
- `continue` 模式下，脚本会带上最近几轮原始历史
- 更早历史不会原样无限累加，而是压缩成一段系统摘要
- `fresh` 模式下，脚本重置当前活动上下文，避免旧话题污染新问题

## 会话调用规则

- 默认推荐单轮调用；只有确实需要延续上下文时才传 `--session`
- 未指定 `--session` 时，不能使用 `--mode=continue`
- `--reset-session` 会在当前请求前重置活动上下文
- `--mode=fresh` 只重置当前活动话题，不会删除整个 session 文件
- `--dry-run` 不会写入、更新或删除 session 文件；所有会话变更仅做预览

## 推荐的 Agent 调用方式

- 看图、听音频、看视频这类一次性理解任务，默认不带 session
- 默认模型选择优先依赖 `config.selectionPolicy`、`config.defaultModel` 和 `config.modelCandidates`
- 默认音色优先依赖 `config.voiceByModelFamily`
- 明显追问时，复用同一个 `--session` 并使用 `--mode=continue`
- 用户给了新模态输入且没有说“基于刚才”时，优先 `--mode=fresh`
- 需要语音输出时，传 `--with-audio`，并确保 `--enable-thinking=false`
- 不确定音色时，先运行 `--list-voices --model <model>` 再决定 `--voice`
- 正式请求前先运行 `--dry-run`，确认模型来源、模态类型、会话模式、价格提醒和请求体预览

## 当前脚本的价格提醒

- 基于你提供的中国内地价格表内置单价提醒
- 调用前显示当前输入/输出模式对应的单价；`Qwen3.5-Omni` 会按单次请求输入 Token 阶梯显示区间价
- 若 `usage` 中包含足够的 token 明细，调用后追加 best-effort 费用估算
- 费用估算依赖服务端返回的统计字段，字段不完整时只显示单价提醒

## 最小请求体

```json
{
  "model": "qwen3.5-omni-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "这段音频讲了什么？" },
        {
          "type": "input_audio",
          "input_audio": {
            "data": "data:audio/mp3;base64,...",
            "format": "mp3"
          }
        }
      ]
    }
  ],
  "stream": true,
  "stream_options": {
    "include_usage": true
  }
}
```
