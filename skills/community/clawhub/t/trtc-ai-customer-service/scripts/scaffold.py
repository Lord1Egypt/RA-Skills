#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRTC AI 电商客服 - 项目脚手架生成器

生成一个完整的基于腾讯云 TRTC ConversationAI 的电商客服 Web 应用后端骨架，
内置订单查询、退换货处理、商品咨询、物流追踪、优惠活动等电商客服场景。
默认支持中文/英文/粤语三语。

用法：
    python scaffold.py <输出目录> [--name <商城名称>] [--name-en <英文名>]

示例：
    python scaffold.py ./my-ecommerce-service
    python scaffold.py ./my-ecommerce-service --name "星辰商城" --name-en "StarMall"
"""
import os
import sys
import argparse
import textwrap


def generate_env_yaml(mall_name: str, mall_name_en: str) -> str:
    return textwrap.dedent(f"""\
# =====================================================================
# {mall_name} AI 电商客服 - 配置文件
# 使用方法：cp env.example.yaml env.yaml，然后填入真实密钥
# ⚠️ 切勿将填入真实密钥的 env.yaml 提交到代码仓库！
# =====================================================================

# 部署区域：intl = 国际站账号；cn = 中国大陆账号
Deployment:
  Region: intl   # intl / cn

# 腾讯云主账号 API 密钥（用于 TRTC OpenAPI 签名）
CloudAPI:
  SECRET_ID: your-secret-id
  SECRET_KEY: your-secret-key

# TRTC 应用凭据
TRTC:
  SDKAPPID: 0
  SECRET: your-trtc-secret

# LLM 配置（实时对话用，由 TRTC 服务端调用）
LLMConfig:
  LLMType: openai
  Model: your-model-name
  APIKey: your-llm-api-key
  APIUrl: your-llm-api-url
  Timeout: 5.0
  History: 20
  Temperature: 0.3
  SystemPrompt: |
    你是一名专业的电商客服助手，服务于"{mall_name}"。
    你的职责包括：查询订单状态、处理退换货、解答商品问题、物流查询、优惠活动咨询。
    请遵循以下原则：
    1. 回答简洁明了，每次回复控制在 3 句话以内
    2. 语气亲切自然，像朋友一样聊天
    3. 如果用户提供了订单信息，结合订单内容回答
    4. 如果问题超出你的处理范围，建议用户转接人工客服
    始终仅输出纯文本，不使用任何格式化符号、Markdown 或括号注释。
  SystemPromptYue: |
    你係「{mall_name}」嘅專業電商客服助手。
    你嘅職責包括：查詢訂單狀態、處理退換貨、解答商品問題、物流查詢、優惠活動諮詢。
    請遵循以下原則：
    1. 回答簡潔明瞭，每次回覆控制喺 3 句話以內
    2. 語氣親切自然，好似朋友咁傾偈
    3. 如果用戶提供咗訂單資訊，結合訂單內容回答
    4. 如果問題超出你嘅處理範圍，建議用戶轉接人工客服
    始終僅輸出純文本，唔好使用任何格式化符號、Markdown 或括號註釋。請用粵語（繁體中文）回覆。
  SystemPromptEn: |
    You are a professional e-commerce customer service assistant for "{mall_name_en}".
    Your responsibilities include: order status inquiries, returns and exchanges, product questions, shipping tracking, and promotions.
    Please follow these principles:
    1. Keep responses concise, within 3 sentences per reply
    2. Use a warm and natural tone, like chatting with a friend
    3. If the user provides order information, incorporate it into your response
    4. If the question is beyond your scope, suggest transferring to a human agent
    Always output plain text only, no formatting symbols, Markdown, or bracket annotations.

# 欢迎语（AI 入房后首条消息）
WelcomeMessage:
  zh: 您好，欢迎来到{mall_name}！我是AI客服小助手，可以帮您查询订单、处理退换货、了解优惠活动，请问有什么可以帮您？
  yue: 您好，歡迎嚟到{mall_name}！我係AI客服小助手，可以幫您查詢訂單、處理退換貨、了解優惠活動，請問有咩可以幫到您？
  en: "Welcome to {mall_name_en}! I'm your AI assistant. I can help with orders, returns, shipping, and promotions. How can I help you?"

# 数字人配置（可选）
# 三项全部填写 -> 启用数字人模式，TTSConfig 自动设为 dummy
# 任一为空      -> 降级为纯语音（本 MVP 默认推荐）
AvatarConfig:
  AvatarType: tencent
  Appkey: ""
  AccessToken: ""
  VirtualmanProjectId: ""

# 关键词触发结束（用户原话匹配命中即触发告别语并自动结束）
# 匹配规则：中文用"两侧非中文字母数字"边界，英文用 \\b 词边界
EndKeywords:
  zh:
    - 拜拜
    - 再见
    - 先挂了
    - 先这样
    - 就这样吧
    - 没事了
    - 我有事
    - 挂了
    - 不需要了
    - 不用了
  yue:
    - 拜拜
    - 再見
    - 收線啦
    - 咁先啦
    - 唔使啦
    - 冇事啦
    - 掛啦
  en:
    - bye
    - goodbye
    - see you
    - that's all
    - thanks bye
    - gotta go
    - i'm done

# 告别语（结束时由服务端推送，StopAfterPlay 自动结束任务）
FarewellMessage:
  zh: 感谢您光临{mall_name}，祝您购物愉快，再见！
  yue: 多謝您光臨{mall_name}，祝您購物愉快，再見！
  en: Thank you for visiting {mall_name_en}. Happy shopping and goodbye!

# 转人工关键词（用户原话匹配命中即触发转人工流程）
TransferKeywords:
  zh:
    - 转人工
    - 人工客服
    - 找人工
    - 转接人工
    - 真人客服
    - 找真人
  yue:
    - 轉人工
    - 人工客服
    - 搵人工
    - 轉接人工
    - 真人客服
  en:
    - transfer
    - human agent
    - real person
    - talk to a person
    - speak to someone

# 转人工提示语
TransferMessage:
  zh: 好的，正在为您转接人工客服，请稍候...
  yue: 好嘅，正在為您轉接人工客服，請稍候...
  en: Sure, transferring you to a human agent, please wait...
""")


def generate_requirements() -> str:
    return textwrap.dedent("""\
Flask==3.0.3
envyaml==1.10.211231
loguru==0.7.3
tencentcloud-sdk-python==3.1.93
""")


def generate_gitignore() -> str:
    return textwrap.dedent("""\
env.yaml
venv/
certs/
__pycache__/
*.pyc
server.log*
.DS_Store
""")


def generate_app_py(mall_name: str) -> str:
    return textwrap.dedent(f'''\
# -*- coding: utf-8 -*-
"""
{mall_name} AI 电商客服 - Flask 后端
路由:
  GET  /                    - 主对话页面
  POST /action  join                  - 申请 UserSig + 下发关键词/告别语/数字人开关
  POST /action  StartAIConversation   - 启动 AI 对话任务
  POST /action  StopAIConversation    - 停止任务（兜底）
  POST /action  FarewellAndStop       - 推送告别语 + StopAfterPlay 一站式结束
  POST /action  TransferAndStop       - 播报转接提示语 + StopAfterPlay 一站式结束
"""
import json
import enum
import traceback

import loguru
from flask import Flask, request, render_template

from tencentcloud.trtc.v20190722 import trtc_client, models
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from config_loader import AppConfig, get_voice_id, get_stt_language
from trtc_signer import TRTCSigner


# ============ 初始化 ============
config = AppConfig("env.yaml")
signer = TRTCSigner(config.sdkappid, config.trtc_secret)

_cred = credential.Credential(config.secret_id, config.secret_key)
_http = HttpProfile()
_http.endpoint = config.trtc_endpoint
_client_profile = ClientProfile()
_client_profile.httpProfile = _http
trtc_api = trtc_client.TrtcClient(_cred, config.trtc_region, _client_profile)


app = Flask(__name__, static_folder="static")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3600


class ErrorCode(enum.Enum):
    InvalidParameter = "InvalidParameter"


def err(code: ErrorCode, msg: str):
    return {{"Response": {{"Error": {{"Code": code.name, "Message": msg}}}}}}


ACTION_LIST = {{
    "join",
    "StartAIConversation",
    "StopAIConversation",
    "UpdateAIConversation",
    "FarewellAndStop",
    "TransferAndStop",
}}


# ============ Action 处理 ============

def handle_join(data: dict) -> dict:
    user_id = data.get("userid")
    if not user_id:
        raise ValueError("userid is required")
    sigs = signer.sign_trio(user_id)
    avatar_enabled = config.is_avatar_enabled()

    return {{
        "sdkappid": sigs["sdkappid"],
        "userid": sigs["user_id"],
        "usersig": sigs["user_sig"],
        "robot_userid": sigs["robot_user_id"],
        "robot_usersig": sigs["robot_user_sig"],
        "avatar_userid": sigs["avatar_user_id"] if avatar_enabled else "",
        "avatar_usersig": sigs["avatar_user_sig"] if avatar_enabled else "",
        "avatar_available": avatar_enabled,
        "end_keywords": config.all_end_keywords(),
        "farewell_message": {{
            "zh": config.farewell_message("zh"),
            "yue": config.farewell_message("yue"),
            "en": config.farewell_message("en"),
        }},
        "transfer_keywords": config.all_transfer_keywords(),
        "transfer_message": {{
            "zh": config.transfer_message("zh"),
            "yue": config.transfer_message("yue"),
            "en": config.transfer_message("en"),
        }},
    }}


def handle_start_ai_conversation(body: dict) -> dict:
    lang = body.get("AgentConfig", {{}}).get("Lang", "zh")
    use_avatar = bool(body.get("UseAvatar", False)) and config.is_avatar_enabled()

    user_cfg = body.get("UserConfig", {{}}) or {{}}
    interrupt_mode = int(user_cfg.get("InterruptMode", 0))
    interrupt_speech_duration = int(user_cfg.get("InterruptSpeechDuration", 600))
    vad_level = int(user_cfg.get("VadLevel", 3))
    vad_silence_time = int(user_cfg.get("VadSilenceTime", 600))
    stt_language = get_stt_language(lang)
    gender = user_cfg.get("Gender", "female")
    if gender not in ("female", "male"):
        gender = "female"

    welcome = config.welcome_message(lang)

    agent_cfg = {{
        "UserId": body["AgentConfig"]["UserId"],
        "UserSig": body["AgentConfig"]["UserSig"],
        "TargetUserId": body["AgentConfig"]["TargetUserId"],
        "MaxIdleTime": 60,
        "WelcomeMessage": welcome,
        "WelcomeMessagePriority": 0,
        "TurnDetectionMode": 3,
        "TurnDetection": {{"SemanticEagerness": "auto"}},
        "FilterOneWord": False,
        "FilterBracketsContent": 2 if lang == "en" else 1,
        "SubtitleMode": 1,
        "InterruptMode": interrupt_mode,
        "InterruptSpeechDuration": interrupt_speech_duration,
    }}

    stt_cfg = {{
        "Language": stt_language,
        "VadLevel": vad_level,
        "VadSilenceTime": vad_silence_time,
    }}

    llm_cfg = config.llm_config(lang)

    if use_avatar:
        tts_cfg = {{"TTSType": "dummy"}}
    else:
        tts_cfg = {{
            "TTSType": "flow",
            "Model": "flow_01_turbo",
            "VoiceId": get_voice_id(lang, gender),
            "Language": lang if lang in ("zh", "yue", "en") else "zh",
            "Speed": 1.0,
            "Volume": 1.0,
            "Pitch": 0,
        }}

    params = {{
        "SdkAppId": config.sdkappid,
        "RoomId": str(body["RoomId"]),
        "RoomIdType": 0,
        "AgentConfig": agent_cfg,
        "STTConfig": stt_cfg,
        "LLMConfig": json.dumps(llm_cfg, ensure_ascii=False),
        "TTSConfig": json.dumps(tts_cfg, ensure_ascii=False),
    }}

    if use_avatar:
        avatar = config.avatar_config()
        params["AvatarConfig"] = json.dumps({{
            **avatar,
            "AvatarUserID": body["AvatarConfig"]["AvatarUserID"],
            "DriverType": 1,
            "AvatarUserSig": body["AvatarConfig"]["AvatarUserSig"],
        }}, ensure_ascii=False)

    loguru.logger.info(
        f"StartAIConversation: lang={{lang}}, gender={{gender}}, avatar={{use_avatar}}, "
        f"interrupt={{interrupt_mode}}/{{interrupt_speech_duration}}ms, "
        f"vad={{vad_level}}/{{vad_silence_time}}ms, stt={{stt_language}}"
    )

    req = models.StartAIConversationRequest()
    req.from_json_string(json.dumps(params, ensure_ascii=False))
    resp = trtc_api.StartAIConversation(req)
    result = json.loads(resp.to_json_string())
    loguru.logger.info(f"StartAIConversation ok: TaskId={{result.get('TaskId')}}")
    return result


def handle_stop_ai_conversation(body: dict) -> dict:
    task_id = body["TaskId"]
    req = models.StopAIConversationRequest()
    req.from_json_string(json.dumps({{"TaskId": task_id}}))
    try:
        resp = trtc_api.StopAIConversation(req)
        return json.loads(resp.to_json_string())
    except Exception as e:
        if "TaskNotExist" in str(e):
            return {{"RequestId": "N/A", "message": "Task already stopped"}}
        raise


def handle_update_ai_conversation(body: dict) -> dict:
    """对话中动态更新 AI 配置（语言切换 / 侧边栏配置调整）"""
    task_id = body["TaskId"]
    lang = body.get("Lang", "zh")
    gender = body.get("Gender", "female")

    params = {{"TaskId": task_id}}

    # 语言切换 → 更新 TTSConfig + LLMConfig + WelcomeMessage
    if "Lang" in body:
        tts_cfg = {{
            "TTSType": "flow",
            "Model": "flow_01_turbo",
            "VoiceId": get_voice_id(lang, gender),
            "Language": lang if lang in ("zh", "yue", "en") else "zh",
            "Speed": 1.0,
            "Volume": 1.0,
            "Pitch": 0,
        }}
        llm_cfg = config.llm_config(lang)
        params["TTSConfig"] = json.dumps(tts_cfg, ensure_ascii=False)
        params["LLMConfig"] = json.dumps(llm_cfg, ensure_ascii=False)

        # 同步切换 WelcomeMessage（下次重新进房时使用新语言欢迎语）
        if body.get("UpdateWelcome"):
            params["WelcomeMessage"] = config.welcome_message(lang)

    # 侧边栏配置调整 → 更新 InterruptMode / InterruptSpeechDuration
    if "InterruptMode" in body:
        params["InterruptMode"] = int(body["InterruptMode"])
    if "InterruptSpeechDuration" in body:
        params["InterruptSpeechDuration"] = int(body["InterruptSpeechDuration"])

    loguru.logger.info(
        f"UpdateAIConversation: TaskId={{task_id}}, "
        f"keys={{[k for k in params.keys() if k != 'TaskId']}}"
    )

    req = models.UpdateAIConversationRequest()
    req.from_json_string(json.dumps(params, ensure_ascii=False))
    try:
        resp = trtc_api.UpdateAIConversation(req)
        result = json.loads(resp.to_json_string())
        loguru.logger.info(f"UpdateAIConversation ok: TaskId={{task_id}}")
        return result
    except Exception as e:
        if "TaskNotExist" in str(e):
            return {{"RequestId": "N/A", "message": "Task already ended"}}
        raise


def handle_farewell_and_stop(body: dict) -> dict:
    """推送告别语 + StopAfterPlay=true 一站式结束"""
    task_id = body["TaskId"]
    lang = body.get("Lang", "zh")
    farewell_text = body.get("FarewellText") or config.farewell_message(lang)

    params = {{
        "TaskId": task_id,
        "Command": "ServerPushText",
        "ServerPushText": {{
            "Text": farewell_text,
            "Interrupt": True,
            "StopAfterPlay": True,
            "AddHistory": True,
            "Priority": 0,
        }},
    }}
    req = models.ControlAIConversationRequest()
    req.from_json_string(json.dumps(params, ensure_ascii=False))
    try:
        resp = trtc_api.ControlAIConversation(req)
        result = json.loads(resp.to_json_string())
        result["FarewellText"] = farewell_text
        loguru.logger.info(f"FarewellAndStop ok: TaskId={{task_id}}")
        return result
    except Exception as e:
        if "TaskNotExist" in str(e):
            return {{"RequestId": "N/A", "message": "Task already ended",
                    "FarewellText": farewell_text}}
        raise


def handle_transfer_and_stop(body: dict) -> dict:
    """播报转接提示语 + StopAfterPlay=true，播报完自动结束 AI 任务"""
    task_id = body["TaskId"]
    lang = body.get("Lang", "zh")
    transfer_text = body.get("TransferText") or config.transfer_message(lang)

    params = {{
        "TaskId": task_id,
        "Command": "ServerPushText",
        "ServerPushText": {{
            "Text": transfer_text,
            "Interrupt": True,
            "StopAfterPlay": True,
            "AddHistory": True,
            "Priority": 0,
        }},
    }}
    req = models.ControlAIConversationRequest()
    req.from_json_string(json.dumps(params, ensure_ascii=False))
    try:
        resp = trtc_api.ControlAIConversation(req)
        result = json.loads(resp.to_json_string())
        result["TransferText"] = transfer_text
        loguru.logger.info(f"TransferAndStop ok: TaskId={{task_id}}")
        return result
    except Exception as e:
        if "TaskNotExist" in str(e):
            return {{"RequestId": "N/A", "message": "Task already ended",
                    "TransferText": transfer_text}}
        raise


# ============ 路由 ============

@app.route("/")
def index():
    return render_template("customer_service.html")


@app.post("/action")
def actions():
    action = request.headers.get("Action", "")
    if action not in ACTION_LIST:
        return err(ErrorCode.InvalidParameter, f"action {{action!r}} invalid")

    body = request.json or {{}}
    try:
        if action == "join":
            return handle_join(body)
        if action == "StartAIConversation":
            return handle_start_ai_conversation(body)
        if action == "StopAIConversation":
            return handle_stop_ai_conversation(body)
        if action == "UpdateAIConversation":
            return handle_update_ai_conversation(body)
        if action == "FarewellAndStop":
            return handle_farewell_and_stop(body)
        if action == "TransferAndStop":
            return handle_transfer_and_stop(body)
    except Exception as e:
        loguru.logger.error(f"action {{action}} failed: {{traceback.format_exc()}}")
        return err(ErrorCode.InvalidParameter, str(e))


if __name__ == "__main__":
    loguru.logger.add("server.log", rotation="50 MB", retention=3)
    PORT = 8080
    use_https = "--https" in __import__("sys").argv
    if use_https:
        import ssl
        import os
        cert = os.path.join(os.path.dirname(__file__), "certs", "cert.pem")
        key = os.path.join(os.path.dirname(__file__), "certs", "key.pem")
        if not os.path.exists(cert) or not os.path.exists(key):
            loguru.logger.error("HTTPS cert not found. Run: ./start.sh --https")
            raise SystemExit(1)
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        loguru.logger.info(f"Starting {mall_name} AI Customer Service on https://0.0.0.0:{{PORT}}")
        app.run("0.0.0.0", PORT, debug=False, ssl_context=ctx)
    else:
        loguru.logger.info(f"Starting {mall_name} AI Customer Service on http://0.0.0.0:{{PORT}}")
        app.run("0.0.0.0", PORT, debug=False)
''')


def generate_config_loader() -> str:
    return textwrap.dedent('''\
# -*- coding: utf-8 -*-
"""
配置加载器
- 根据 Deployment.Region 切换 TRTC OpenAPI Endpoint 和地域
- 提供 TTS VoiceId 的"语言 + 性别"映射
- 关键词与告别语统一访问入口
"""
from typing import Dict, List, Optional
from envyaml import EnvYAML
import loguru


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

# TTS VoiceId: (lang, gender) -> VoiceId
TTS_VOICE_MAP = {
    ("zh", "female"): "female-kefu-xiaoyue",
    ("zh", "male"): "male-kefu-xiaoxu",
    ("yue", "female"): "v-female-k3P8sL0Q",
    ("yue", "male"): "v-male-L4s7PqZ9",
    ("en", "female"): "v-female-Z3x9LmQ2",
    ("en", "male"): "v-male-Q6p8ZxL3",
}

# STT Language: lang -> STTConfig.Language
STT_LANG_MAP = {
    "zh": "zh",
    "yue": "zh-TW",
    "en": "en",
}


def get_voice_id(lang: str, gender: str) -> str:
    key = (lang if lang in ("zh", "yue", "en") else "zh",
           gender if gender in ("female", "male") else "female")
    return TTS_VOICE_MAP[key]


def get_stt_language(lang: str) -> str:
    return STT_LANG_MAP.get(lang, "zh")


class AppConfig:
    def __init__(self, env_path: str = "env.yaml"):
        self.env = EnvYAML(env_path)
        region = self.env.get("Deployment.Region", "intl")
        if region not in REGION_PROFILES:
            loguru.logger.warning(f"Unknown region '{region}', falling back to 'intl'")
            region = "intl"
        self.region = region
        self.profile = REGION_PROFILES[region]
        loguru.logger.info(
            f"AppConfig: region={region}, "
            f"trtc={self.profile['trtc_endpoint']} ({self.profile['trtc_region']})"
        )

    @property
    def secret_id(self) -> str:
        return self.env["CloudAPI.SECRET_ID"]

    @property
    def secret_key(self) -> str:
        return self.env["CloudAPI.SECRET_KEY"]

    @property
    def sdkappid(self) -> int:
        return int(self.env["TRTC.SDKAPPID"])

    @property
    def trtc_secret(self) -> str:
        return self.env["TRTC.SECRET"]

    @property
    def trtc_endpoint(self) -> str:
        return self.profile["trtc_endpoint"]

    @property
    def trtc_region(self) -> str:
        return self.profile["trtc_region"]

    def llm_config(self, lang: str = "zh") -> dict:
        cfg = dict(self.env["LLMConfig"])
        prompt_zh = cfg.get("SystemPrompt", "")
        prompt_yue = cfg.get("SystemPromptYue", prompt_zh)
        prompt_en = cfg.get("SystemPromptEn", prompt_zh)
        if lang == "en":
            cfg["SystemPrompt"] = prompt_en
        elif lang == "yue":
            cfg["SystemPrompt"] = prompt_yue
        else:
            cfg["SystemPrompt"] = prompt_zh
        cfg.pop("SystemPromptYue", None)
        cfg.pop("SystemPromptEn", None)
        cfg["Streaming"] = True
        cfg["Temperature"] = float(cfg.get("Temperature", 0.3))
        cfg["History"] = int(cfg.get("History", 20))
        return cfg

    def welcome_message(self, lang: str) -> str:
        defaults = {
            "zh": "您好，我是 AI 客服小助手，请问有什么可以帮您？",
            "yue": "您好，我係 AI 客服小助手，請問有咩可以幫到您？",
            "en": "Hello! I'm your AI customer service assistant. How can I help you today?",
        }
        return self.env.get(f"WelcomeMessage.{lang}", defaults.get(lang, defaults["zh"]))

    def is_avatar_enabled(self) -> bool:
        avatar = self.env.get("AvatarConfig")
        if not isinstance(avatar, dict):
            return False
        return bool(avatar.get("Appkey")) and bool(avatar.get("AccessToken")) \\
            and bool(avatar.get("VirtualmanProjectId"))

    def avatar_config(self) -> Optional[dict]:
        if not self.is_avatar_enabled():
            return None
        return {
            "AvatarType": self.env.get("AvatarConfig.AvatarType", "tencent"),
            "Appkey": self.env["AvatarConfig.Appkey"],
            "AccessToken": self.env["AvatarConfig.AccessToken"],
            "VirtualmanProjectId": self.env["AvatarConfig.VirtualmanProjectId"],
        }

    def all_end_keywords(self) -> Dict[str, List[str]]:
        return {
            "zh": list(self.env.get("EndKeywords.zh", []) or []),
            "yue": list(self.env.get("EndKeywords.yue", []) or []),
            "en": list(self.env.get("EndKeywords.en", []) or []),
        }

    def farewell_message(self, lang: str) -> str:
        defaults = {
            "zh": "感谢您的咨询，祝您购物愉快，再见！",
            "yue": "多謝您嘅諮詢，祝您購物愉快，再見！",
            "en": "Thank you for your inquiry. Happy shopping and goodbye!",
        }
        return self.env.get(f"FarewellMessage.{lang}", defaults.get(lang, defaults["zh"]))

    def all_transfer_keywords(self) -> Dict[str, List[str]]:
        return {
            "zh": list(self.env.get("TransferKeywords.zh", []) or []),
            "yue": list(self.env.get("TransferKeywords.yue", []) or []),
            "en": list(self.env.get("TransferKeywords.en", []) or []),
        }

    def transfer_message(self, lang: str) -> str:
        defaults = {
            "zh": "好的，正在为您转接人工客服，请稍候...",
            "yue": "好嘅，正在為您轉接人工客服，請稍候...",
            "en": "Sure, transferring you to a human agent, please wait...",
        }
        return self.env.get(f"TransferMessage.{lang}", defaults.get(lang, defaults["zh"]))
''')


def generate_trtc_signer() -> str:
    return textwrap.dedent('''\
# -*- coding: utf-8 -*-
"""
TRTC UserSig 签名工具
封装 TLSSigAPIv2，提供"用户/机器人/数字人"三套签名生成
"""
import TLSSigAPIv2


class TRTCSigner:
    def __init__(self, sdkappid: int, secret: str):
        self.sdkappid = sdkappid
        self.api = TLSSigAPIv2.TLSSigAPIv2(sdkappid, secret)

    def sign(self, user_id: str, expire: int = 86400) -> str:
        """生成 UserSig，默认 24 小时有效"""
        if not user_id or len(user_id) > 32:
            raise ValueError(f"Invalid userId: {user_id!r}")
        return self.api.genUserSig(user_id, expire)

    def sign_trio(self, user_id: str, expire: int = 86400) -> dict:
        """
        一次性签发 用户/机器人/数字人 三套 UserSig
        - 真人:    user_id
        - 机器人:  {user_id}_robot
        - 数字人:  {user_id}_avatar
        """
        robot_id = f"{user_id}_robot"
        avatar_id = f"{user_id}_avatar"
        return {
            "sdkappid": self.sdkappid,
            "user_id": user_id,
            "user_sig": self.sign(user_id, expire),
            "robot_user_id": robot_id,
            "robot_user_sig": self.sign(robot_id, expire),
            "avatar_user_id": avatar_id,
            "avatar_user_sig": self.sign(avatar_id, expire),
        }
''')


def generate_readme(mall_name: str) -> str:
    return textwrap.dedent(f"""\
# {mall_name} AI 电商客服

基于腾讯云 TRTC ConversationAI 构建的 **AI 电商客服系统**。
支持语音/文字双模对话、订单查询、退换货处理、商品咨询、物流追踪等电商场景。

## 快速开始

```bash
# macOS / Linux
./start.sh

# Windows
start.bat
```

### 首次运行

1. 运行 `./start.sh`，会自动生成 `env.yaml`
2. 编辑 `env.yaml` 填入密钥：
   - `CloudAPI.SECRET_ID / SECRET_KEY`：腾讯云主账号
   - `TRTC.SDKAPPID / SECRET`：TRTC 应用凭据
   - `LLMConfig.APIKey`：LLM API Key（[配置指南](https://trtc.io/document/68338?product=conversationalai)）
3. 再次运行 `./start.sh` 即启动
4. 浏览器访问 **http://localhost:8080**

## 核心特性

- 🎤 **语音对话** —— TRTC 房间内用户↔AI Bot 实时语音
- ⌨️ **文字输入** —— 不便说话时切换键盘，跳过 ASR 直送 LLM
- 💬 **IM 气泡风格 UI** —— 上下滚动消息流
- 🌐 **中文/粤语/英文三语** —— UI / STT / TTS / SystemPrompt 全套国际化
- 📦 **订单面板** —— 模拟电商订单卡片，可发送给 AI 进行查询
- 🤖 **数字人可选** —— 配置即启用，否则降级为纯语音
- 🛑 **关键词触发结束** —— 用户说"拜拜""bye"即触发告别语自动结束
- 🔁 **转人工** —— 用户说"转人工"即触发转接流程
- ⭐ **服务评分** —— 4 维度手动评分

## 架构

```
浏览器 (TRTC Web SDK v5)
     ↕ 音频 (WebRTC) + 自定义消息 (字幕/状态/文字/订单)
TRTC Room → ASR → LLM → TTS
     ↕ OpenAPI
Flask 后端 —— UserSig 签发 + OpenAPI 中转（零 LLM 调用）
```

## License

MIT
""")


def generate_start_sh(mall_name: str) -> str:
    return textwrap.dedent(f"""\
#!/usr/bin/env bash
# {mall_name} AI 电商客服 - 一键启动脚本
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="venv"
VENV_PY="$VENV_DIR/bin/python"
REQ_FILE="requirements.txt"
ENV_FILE="env.yaml"
ENV_EXAMPLE="env.example.yaml"

# 1. 检测 Python
find_python() {{
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null; then
            local ver
            ver=$("$cmd" -c "import sys; print(f'{{sys.version_info.major}}.{{sys.version_info.minor}}')" 2>/dev/null)
            local major=${{ver%%.*}}
            local minor=${{ver##*.}}
            if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    echo "ERROR: Python >= 3.8 not found" >&2
    exit 1
}}

SYS_PY=$(find_python)
echo "Using Python: $SYS_PY ($($SYS_PY --version))"

# 2. env.yaml
if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_EXAMPLE" ]; then
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        echo "已生成 $ENV_FILE，请填入真实密钥后重新运行"
        exit 0
    else
        echo "ERROR: $ENV_EXAMPLE not found" >&2
        exit 1
    fi
fi

# 3. venv
if [ "$1" = "--rebuild" ] && [ -d "$VENV_DIR" ]; then
    echo "Rebuilding venv..."
    rm -rf "$VENV_DIR"
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv..."
    "$SYS_PY" -m venv "$VENV_DIR"
fi

# 4. Dependencies (default: PyPI, fallback: Tsinghua mirror)
if ! "$VENV_PY" -c "import flask, envyaml, loguru, tencentcloud" 2>/dev/null; then
    echo "Installing dependencies..."
    "$VENV_PY" -m pip install -r "$REQ_FILE" --quiet --timeout 30 || {{
        echo "PyPI failed, retrying with Tsinghua mirror..."
        "$VENV_PY" -m pip install -r "$REQ_FILE" -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet --timeout 15
    }}
fi

# 5. Auto-detect public IP & HTTPS
PUBLIC_IP=$(curl -s --max-time 3 https://ifconfig.me 2>/dev/null | tr -d '[:space:]' || true)
USE_HTTPS=0
for arg in "$@"; do [ "$arg" = "--https" ] && USE_HTTPS=1; done
if [ "$USE_HTTPS" -eq 0 ] && echo "$PUBLIC_IP" | grep -qE '^[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+$' && [ "$PUBLIC_IP" != "127.0.0.1" ]; then
    echo "Public IP detected: $PUBLIC_IP, auto-enabling HTTPS"
    USE_HTTPS=1
fi

CERT_DIR="certs"
if [ "$USE_HTTPS" -eq 1 ]; then
    if [ ! -f "$CERT_DIR/cert.pem" ]; then
        if command -v openssl >/dev/null 2>&1; then
            echo "Generating self-signed certificate..."
            mkdir -p "$CERT_DIR"
            openssl req -x509 -newkey rsa:2048 -nodes \\
                -keyout "$CERT_DIR/key.pem" -out "$CERT_DIR/cert.pem" \\
                -days 365 -subj "/CN=localhost" 2>/dev/null
            echo "⚠️  Self-signed cert: browser will show security warning on first visit"
        else
            echo "⚠️  openssl not found, falling back to HTTP"
            USE_HTTPS=0
        fi
    fi
fi

PROTO="http"; [ "$USE_HTTPS" -eq 1 ] && PROTO="https"
if [ -n "$PUBLIC_IP" ] && [ "$PUBLIC_IP" != "127.0.0.1" ]; then
    echo "🚀 Starting {mall_name} AI Customer Service"
    echo "   Public: $PROTO://$PUBLIC_IP:8080"
    echo "   Local:  $PROTO://localhost:8080"
else
    echo "🚀 Starting {mall_name} AI Customer Service on $PROTO://localhost:8080"
fi

if [ "$USE_HTTPS" -eq 1 ]; then
    exec "$VENV_PY" app.py --https
else
    exec "$VENV_PY" app.py
fi
""")


def main():
    parser = argparse.ArgumentParser(
        description="TRTC AI 电商客服项目脚手架生成器",
        epilog="示例: python scaffold.py ./my-shop --name 星辰商城",
    )
    parser.add_argument("output_dir", help="输出目录路径")
    parser.add_argument("--name", default="云尚商城", help="商城名称（默认: 云尚商城）")
    parser.add_argument("--name-en", default=None, dest="name_en",
                        help="English store name (default: auto-derived from --name, e.g. 'CloudShop Mall')")
    args = parser.parse_args()

    # Derive English name: use --name-en if provided, otherwise use --name as-is
    # (for CJK names, default to "CloudShop Mall")
    if args.name_en is None:
        # If name contains CJK characters, use default English name
        import re
        if re.search(r'[\u4e00-\u9fff]', args.name):
            args.name_en = "CloudShop Mall"
        else:
            args.name_en = args.name

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 创建目录结构
    for d in ["static", "static/avatars", "templates", "docs"]:
        os.makedirs(os.path.join(output_dir, d), exist_ok=True)

    # 生成后端代码文件
    files = {
        "env.example.yaml": generate_env_yaml(args.name, args.name_en),
        "requirements.txt": generate_requirements(),
        ".gitignore": generate_gitignore(),
        "app.py": generate_app_py(args.name),
        "config_loader.py": generate_config_loader(),
        "trtc_signer.py": generate_trtc_signer(),
        "README.md": generate_readme(args.name),
        "start.sh": generate_start_sh(args.name),
    }

    for filename, content in files.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        if filename == "start.sh":
            os.chmod(filepath, 0o755)

    # 从 assets/ 目录复制前端文件和 TLSSigAPIv2.py
    import shutil
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(os.path.dirname(script_dir), "assets")

    copied_assets = []
    if os.path.isdir(assets_dir):
        # 复制 TLSSigAPIv2.py
        src = os.path.join(assets_dir, "TLSSigAPIv2.py")
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(output_dir, "TLSSigAPIv2.py"))
            copied_assets.append("TLSSigAPIv2.py")

        # 复制 start.sh（带交互式引导的完整版，覆盖简化版）
        src = os.path.join(assets_dir, "start.sh")
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(output_dir, "start.sh"))
            os.chmod(os.path.join(output_dir, "start.sh"), 0o755)

        # 复制 start.bat（Windows 版）
        src = os.path.join(assets_dir, "start.bat")
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(output_dir, "start.bat"))
            copied_assets.append("start.bat")

        # 复制 templates/
        src = os.path.join(assets_dir, "templates", "customer_service.html")
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(output_dir, "templates", "customer_service.html"))
            copied_assets.append("templates/customer_service.html")

        # 复制 static/app.js, static/i18n.js
        for js_file in ["app.js", "i18n.js"]:
            src = os.path.join(assets_dir, "static", js_file)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(output_dir, "static", js_file))
                copied_assets.append(f"static/{js_file}")

        # 复制 static/mock-orders.json（可自定义订单数据）
        src = os.path.join(assets_dir, "static", "mock-orders.json")
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(output_dir, "static", "mock-orders.json"))
            copied_assets.append("static/mock-orders.json")

        # 复制 static/avatars/
        avatars_src = os.path.join(assets_dir, "static", "avatars")
        if os.path.isdir(avatars_src):
            for img in os.listdir(avatars_src):
                if img.endswith(".png"):
                    shutil.copy2(
                        os.path.join(avatars_src, img),
                        os.path.join(output_dir, "static", "avatars", img),
                    )
            copied_assets.append("static/avatars/*.png")

        # ---- 品牌名全链路替换 ----
        # 如果用户指定了自定义商城名（非默认），替换前端文件中的品牌名
        default_mall = "云尚商城"
        default_mall_en = "CloudShop Mall"
        if args.name != default_mall or args.name_en != default_mall_en:
            replace_targets = [
                os.path.join(output_dir, "templates", "customer_service.html"),
                os.path.join(output_dir, "static", "i18n.js"),
            ]
            for fpath in replace_targets:
                if os.path.exists(fpath):
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read()
                    if args.name != default_mall:
                        content = content.replace(default_mall, args.name)
                    if args.name_en != default_mall_en:
                        content = content.replace(default_mall_en, args.name_en)
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(content)
    else:
        print(f"\n⚠️  assets/ 目录未找到 ({assets_dir})，前端文件未复制。")
        print(f"   请手动从 trtc-ai-customer-service-demo 项目复制前端文件。")

    # 输出结果
    print(f"\n✅ 电商客服项目已生成到: {output_dir}")
    print(f"\n📁 完整项目结构:")
    print(f"   {output_dir}/")
    all_files = sorted(files.keys())
    all_files += sorted(copied_assets)
    for f in all_files:
        print(f"   ├── {f}")

    if copied_assets:
        print(f"\n🎉 项目已包含全部文件（后端 + 前端 + 头像 + 鉴权库），开箱即用！")
        print(f"\n📦 可自定义:")
        print(f"   • static/mock-orders.json  → 修改商品和订单数据（改 JSON 即可，无需动代码）")
        print(f"   • env.yaml 中 SystemPrompt → 调整 AI 客服的角色和话术")
        print(f"\n🚀 启动步骤:")
        print(f"   1. 运行 ./start.sh → 首次会引导你逐步填入密钥")
        print(f"   2. 浏览器访问 http://localhost:8080")
    else:
        print(f"\n🚀 下一步:")
        print(f"   1. 复制 TLSSigAPIv2.py 到项目根目录")
        print(f"   2. 复制前端文件（templates/ + static/）")
        print(f"   3. 运行 ./start.sh 生成 env.yaml 并填入密钥")


if __name__ == "__main__":
    main()
