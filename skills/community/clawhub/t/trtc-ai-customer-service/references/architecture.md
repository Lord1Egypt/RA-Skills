# TRTC AI 智能客服 - 架构设计参考

## 目录

1. [系统架构](#系统架构)
2. [项目结构](#项目结构)
3. [后端实现详解](#后端实现详解)
4. [认证流程](#认证流程)
5. [核心设计模式](#核心设计模式)
6. [依赖清单](#依赖清单)
7. [启动与部署](#启动与部署)

---

## 系统架构

### 三平面模型

```
┌─────────────────────────────────────────────────┐
│              浏览器 (TRTC Web SDK v5)              │
│                                                   │
│   音频流 (WebRTC)   自定义消息 (字幕/状态/文字)       │
└───────────┬─────────────────┬─────────────────────┘
            │                 │
            ▼                 ▼
┌───────────────────────────────────────────────────┐
│                  TRTC Room (云端)                   │
│                                                     │
│   ASR ──► LLM ──► TTS ──► 推回房间                  │
│                                                     │
│              TRTC AI Bot (云端实例)                   │
└───────────┬─────────────────────────────────────────┘
            │ OpenAPI (TC3-HMAC-SHA256)
            ▼
┌───────────────────────────────────────────────────┐
│   Flask 后端 (app.py)                               │
│   - UserSig 签发                                    │
│   - TRTC OpenAPI 中转                               │
│   - 零 LLM 调用                                     │
└─────────────────────────────────────────────────────┘
```

关键洞察：**后端完全不调用 LLM**。LLM 推理由 TRTC 云端 AI Bot 内部完成。后端只做两件事：
1. 签发 UserSig（用于 TRTC 房间鉴权）
2. 中转 TRTC OpenAPI 请求（启动/停止/控制 AI 对话）

### 消息类型

| type | 方向 | 内容 |
|------|------|------|
| `10000` | 云→端 | 字幕（用户 ASR 结果 + AI 回复文本） |
| `10001` | 云→端 | AI 状态（聆听/思考/说话/打断/结束） |
| `20000` | 端→云 | 文字输入（跳过 ASR 直送 LLM） |
| `20001` | 端→云 | 手动打断 |

---

## 项目结构

```
project/
├── app.py                        # Flask 主入口（~296 行，5 个 Action 处理器）
├── config_loader.py              # 配置加载器（Region/TTS/STT 映射）
├── trtc_signer.py                # UserSig 三套签发封装
├── TLSSigAPIv2.py                # 腾讯云官方 TRTC HMAC 鉴权库（不修改）
├── env.example.yaml              # 配置模板
├── env.yaml                      # 实际配置（.gitignore 排除）
├── requirements.txt              # 4 个 Python 依赖
├── start.sh / start.bat          # 一键启动脚本
├── templates/
│   └── customer_service.html     # 主页面（配置侧边栏 + 聊天区 + 评分弹窗）
├── static/
│   ├── app.js                    # 前端核心交互逻辑
│   ├── i18n.js                   # 国际化字典（zh/yue/en）
│   └── avatars/                  # 客服头像
└── docs/
    └── PARAMS.md                 # 参数配置详解
```

---

## 后端实现详解

### 初始化

```python
# 加载配置
config = AppConfig("env.yaml")
signer = TRTCSigner(config.sdkappid, config.trtc_secret)

# 初始化 TRTC OpenAPI 客户端
_cred = credential.Credential(config.secret_id, config.secret_key)
_http = HttpProfile()
_http.endpoint = config.trtc_endpoint  # 按 Region 自动切换
_client_profile = ClientProfile()
_client_profile.httpProfile = _http
trtc_api = trtc_client.TrtcClient(_cred, config.trtc_region, _client_profile)
```

### 路由设计

仅 2 个路由，极简：
- `GET /` → 渲染主页面
- `POST /action` → 统一 API 调度，通过 `Action` 请求头区分

### Action 处理器详解

#### handle_join(data)

签发三套 UserSig 并下发配置：

```python
def handle_join(data):
    user_id = data.get("userid")
    sigs = signer.sign_trio(user_id)     # 用户 + 机器人 + 数字人
    avatar_enabled = config.is_avatar_enabled()
    return {
        "sdkappid": sigs["sdkappid"],
        "userid": sigs["user_id"],
        "usersig": sigs["user_sig"],
        "robot_userid": sigs["robot_user_id"],
        "robot_usersig": sigs["robot_user_sig"],
        "avatar_userid": sigs["avatar_user_id"] if avatar_enabled else "",
        "avatar_usersig": sigs["avatar_user_sig"] if avatar_enabled else "",
        "avatar_available": avatar_enabled,
        "end_keywords": config.all_end_keywords(),        # 三语结束关键词
        "farewell_message": {...},                         # 三语告别语
        "transfer_keywords": config.all_transfer_keywords(),  # 三语转人工关键词
        "transfer_message": {...},                         # 三语转接提示
    }
```

#### handle_start_ai_conversation(body)

组装 5 大配置块并调用 TRTC OpenAPI：

```python
def handle_start_ai_conversation(body):
    lang = body["AgentConfig"]["Lang"]          # zh/yue/en
    use_avatar = body.get("UseAvatar", False)

    # 1. AgentConfig：机器人身份 + 对话参数
    agent_cfg = {
        "UserId": body["AgentConfig"]["UserId"],
        "UserSig": body["AgentConfig"]["UserSig"],
        "TargetUserId": body["AgentConfig"]["TargetUserId"],
        "MaxIdleTime": 60,
        "WelcomeMessage": config.welcome_message(lang),
        "TurnDetectionMode": 3,                 # 语义断句
        "TurnDetection": {"SemanticEagerness": "auto"},
        "SubtitleMode": 1,                      # 句子级字幕
        "InterruptMode": interrupt_mode,         # 0=智能/1=手动
        "InterruptSpeechDuration": interrupt_speech_duration,
    }

    # 2. STTConfig：语音识别
    stt_cfg = {
        "Language": get_stt_language(lang),      # zh / zh-TW / en
        "VadLevel": vad_level,
        "VadSilenceTime": vad_silence_time,
    }

    # 3. LLMConfig：从 env.yaml 读取
    llm_cfg = config.llm_config(lang)            # 按语言切换 SystemPrompt

    # 4. TTSConfig
    if use_avatar:
        tts_cfg = {"TTSType": "dummy"}           # 数字人模式：TTS 由数字人引擎处理
    else:
        tts_cfg = {
            "TTSType": "flow",
            "Model": "flow_01_turbo",
            "VoiceId": get_voice_id(lang, gender),  # 6 种组合
        }

    # 5. AvatarConfig（可选）
    if use_avatar:
        params["AvatarConfig"] = json.dumps({...})

    # 调用 TRTC OpenAPI
    req = models.StartAIConversationRequest()
    req.from_json_string(json.dumps(params))
    resp = trtc_api.StartAIConversation(req)
    return json.loads(resp.to_json_string())     # 包含 TaskId
```

#### handle_farewell_and_stop(body)

一站式结束的核心实现：

```python
def handle_farewell_and_stop(body):
    params = {
        "TaskId": task_id,
        "Command": "ServerPushText",
        "ServerPushText": {
            "Text": farewell_text,           # 告别语
            "Interrupt": True,               # 打断当前播报
            "StopAfterPlay": True,           # TTS 播完后自动停止任务
            "AddHistory": True,
            "Priority": 0,
        },
    }
    req = models.ControlAIConversationRequest()
    req.from_json_string(json.dumps(params))
    resp = trtc_api.ControlAIConversation(req)
```

`StopAfterPlay=True` 的优势：
- 不需要前端估算 TTS 播报时长
- 不需要 setTimeout 轮询
- 服务端确保播报完整后才停止任务

#### handle_transfer_and_stop(body)

与 FarewellAndStop 结构相同，只是文本换成转接提示语。

### 错误处理

```python
class ErrorCode(enum.Enum):
    InvalidParameter = "InvalidParameter"

def err(code: ErrorCode, msg: str):
    return {"Response": {"Error": {"Code": code.name, "Message": msg}}}
```

所有异常统一返回腾讯云 API 风格的错误结构。`TaskNotExist` 错误被静默处理（幂等设计）。

---

## 认证流程

### UserSig 签发

```python
class TRTCSigner:
    def sign_trio(self, user_id):
        # 一次签发 3 套 UserSig：
        # - user_id           → 真人用户
        # - {user_id}_robot   → AI 机器人
        # - {user_id}_avatar  → 数字人
        robot_id = f"{user_id}_robot"
        avatar_id = f"{user_id}_avatar"
        return {
            "user_sig": self.sign(user_id),
            "robot_user_sig": self.sign(robot_id),
            "avatar_user_sig": self.sign(avatar_id),
        }
```

底层使用 `TLSSigAPIv2`（HMAC-SHA256 + zlib 压缩 + Base64URL 编码），这是腾讯云官方库，无需修改。

### 认证流程

1. 前端调用 `join` → 后端用 TRTC SECRET 签发 UserSig
2. UserSig 随响应返回前端 → 前端用于 TRTC SDK 鉴权进房
3. 同时签发机器人的 UserSig → 传递给 `StartAIConversation` API
4. TRTC SECRET 和 CloudAPI 密钥永远不暴露给前端

---

## 核心设计模式

### 1. ServerPushText + StopAfterPlay

这是最重要的设计模式。通过一次 `ControlAIConversation` 调用实现"播报告别语后自动结束"：

```
前端: FarewellAndStop(TaskId, Lang)
  → 后端: ControlAIConversation(ServerPushText + StopAfterPlay=true)
    → TRTC 云端: 打断当前播报 → TTS 播报告别语 → 自动 StopAIConversation
      → 机器人退房
        → 前端: onRobotLeave → 用户退房 → 显示评分
```

### 2. 语音/文字双模混合

同一个对话中可以无缝切换：
- **语音模式**：麦克风 → TRTC 音频流 → 云端 ASR → LLM
- **文字模式**：输入框 → `sendCustomMessage(type: 20000)` → 直接 LLM（跳过 ASR）

### 3. 配置驱动的多语言

一份配置文件 (`env.yaml`) 驱动全链路国际化：
- `LLMConfig.SystemPrompt` / `SystemPromptYue` / `SystemPromptEn`
- `WelcomeMessage.zh/yue/en`
- `EndKeywords.zh/yue/en`
- `FarewellMessage.zh/yue/en`
- `TransferKeywords.zh/yue/en`
- `TransferMessage.zh/yue/en`

后端根据前端传入的 `lang` 参数自动切换。

### 4. 数字人可选降级

```python
def is_avatar_enabled(self):
    avatar = self.env.get("AvatarConfig")
    return bool(avatar.get("Appkey")) and bool(avatar.get("AccessToken")) \
        and bool(avatar.get("VirtualmanProjectId"))
```

三项全填 → 启用数字人，TTSConfig 设为 `dummy`（由数字人引擎处理 TTS）
任一为空 → 降级为纯语音 + `flow` TTS

---

## 依赖清单

```
Flask==3.0.3                     # Web 框架
envyaml==1.10.211231             # YAML 配置加载（支持环境变量）
loguru==0.7.3                    # 结构化日志
tencentcloud-sdk-python==3.1.93  # 腾讯云 OpenAPI SDK（含 TRTC 模块）
```

极简：仅 4 个直接依赖。

---

## 启动与部署

### 开发环境

```bash
# 一键启动（推荐）
./start.sh

# 手动启动
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

`start.sh` 自动完成：
1. 检测 Python >= 3.8
2. 首次从 `env.example.yaml` 生成 `env.yaml` 并暂停提示填密钥
3. 创建 venv 虚拟环境
4. 检测并安装依赖（清华镜像优先）
5. 端口冲突检测
6. 启动 Flask 服务（端口 8080）

### 生产部署建议

| 项目 | 开发 | 生产 |
|------|------|------|
| 服务器 | Flask 内置 | Gunicorn + Nginx |
| 协议 | HTTP | HTTPS（必须，WebRTC 要求） |
| 鉴权 | 无 | `/action` 添加 Token/Session 鉴权 |
| 日志 | loguru 文件 | 接入 ELK / 腾讯云 CLS |
| 配置 | env.yaml | 环境变量或密钥管理服务 |
