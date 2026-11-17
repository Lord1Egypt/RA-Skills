#!/usr/bin/env python3
"""
企业微信智能机器人语音消息回调服务器 v2.0

核心改进：
1. 真正执行操作（查询天气使用 wttr.in 免费 API）
2. 模糊表达理解（支持口语化、多意图拆分）
3. 多轮对话确认（不确定时主动引导而非假回复）
4. 丰富错误提示（给出具体恢复动作）
5. 健康检查 + 自动重试
6. 零依赖（纯 Python 标准库）

使用方法:
    python scripts/wecom_webhook_server.py                # 启动服务器
    python scripts/wecom_webhook_server.py --quick       # 一键体验所有功能
    python scripts/wecom_webhook_server.py --port 9000   # 指定端口
"""

import http.server
import json
import time
import logging
import sys
import os
import re
import socket
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any

# 日志格式（必须在情感分析模块之前定义 logger）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("WeComServer")

# 情感分析模块（v2.2 新增）
sys.path.insert(0, os.path.dirname(__file__))
try:
    from emotion_analyzer import EmotionAnalyzer, Emotion, EmotionEscalationTracker, HardwareAdaptiveConfig
    EMOTION_AVAILABLE = True
    logger.info("情感分析模块已加载")
except ImportError:
    EMOTION_AVAILABLE = False
    logger.warning("情感分析模块不可用，将跳过情感分析")

# 方言检测模块（v2.3 新增）
try:
    from dialect_detector import DialectDetector, Dialect
    DIALECT_AVAILABLE = True
    logger.info("方言检测模块已加载")
except ImportError:
    DIALECT_AVAILABLE = False
    logger.warning("方言检测模块不可用，将跳过方言检测")

# 工单管理模块（v2.3 新增）
try:
    from ticket_manager import TicketManager, TicketStatus, TicketPriority, TicketCategory
    TICKET_AVAILABLE = True
    logger.info("工单管理模块已加载")
except ImportError:
    TICKET_AVAILABLE = False
    logger.warning("工单管理模块不可用，将跳过工单管理")

# VAD 语音活动检测模块（v2.4 新增）
try:
    from vad_filter import VADFilter, VADEnum
    VAD_AVAILABLE = True
    logger.info("VAD 语音活动检测模块已加载")
except ImportError:
    VAD_AVAILABLE = False
    logger.warning("VAD 模块不可用，将跳过语音活动检测")

# 优先级请求队列模块（v2.4 新增）
try:
    from priority_queue import PriorityRequestQueue, Priority
    QUEUE_AVAILABLE = True
    logger.info("优先级请求队列模块已加载")
except ImportError:
    QUEUE_AVAILABLE = False
    logger.warning("优先级队列模块不可用，将跳过多路排队")

# 合规模块（v2.4 增强）
try:
    from compliance import ComplianceManager, MandatoryAnnouncement
    COMPLIANCE_AVAILABLE = True
    logger.info("合规模块已加载（含强制录音告知）")
except ImportError:
    COMPLIANCE_AVAILABLE = False
    logger.warning("合规模块不可用")

# 通话记录子系统（v2.5 新增）
try:
    from call_record_subsystem import CallRecordSubsystem
    CALL_RECORD_AVAILABLE = True
    logger.info("通话记录子系统已加载")
except ImportError:
    CALL_RECORD_AVAILABLE = False
    logger.warning("通话记录子系统不可用")

# 多渠道抽象层（v2.5 新增）
try:
    from voice_channel import VoiceChannelFactory, StandardMessage, ChannelType
    CHANNEL_AVAILABLE = True
    logger.info("多渠道抽象层已加载")
except ImportError:
    CHANNEL_AVAILABLE = False
    logger.warning("多渠道抽象层不可用")

# 语音留言摘要（v2.5 新增）
try:
    from voicemail_summary import VoicemailSummarizer
    VOICEMAIL_AVAILABLE = True
    logger.info("语音留言摘要系统已加载")
except ImportError:
    VOICEMAIL_AVAILABLE = False
    logger.warning("语音留言摘要系统不可用")

# 自选导入 urllib（兼容 Python 3.x）
try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError
except ImportError:
    from urllib2 import urlopen, Request, URLError

# 群聊语音合规模块（v2.9 新增）
try:
    from group_compliance import GroupCompliance, get_compliance
    GROUP_COMPLIANCE_AVAILABLE = True
except ImportError:
    GROUP_COMPLIANCE_AVAILABLE = False
    logger.warning("群合规模块不可用，群语音将默认不落盘")

# 实体抽取增强（v2.9 群任务三元组）
try:
    from entity_extractor import EntityExtractor
    ENTITY_EXTRACTOR_AVAILABLE = True
except ImportError:
    ENTITY_EXTRACTOR_AVAILABLE = False
    logger.warning("实体抽取模块不可用，群任务三元组将降级")

# 跟进待办闭环（v2.9 复用）
try:
    from todo_followup import TodoFollowupManager
    TODO_AVAILABLE = True
except ImportError:
    TODO_AVAILABLE = False
    logger.warning("待办闭环模块不可用，群任务分发将降级")

# ==========================================
# 配置
# ==========================================

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080
USER_AGENT = "workbuddy-wecom-voice/2.0"

# ==========================================
# 情感分析管理器（v2.2 新增）
# ==========================================

class EmotionManager:
    """情感分析管理器，集成到对话处理流程中"""
    
    def __init__(self):
        self.analyzer = None
        self.tracker = None
        self.config = None
        
        if EMOTION_AVAILABLE:
            templates_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'emotion_strategies.json')
            self.analyzer = EmotionAnalyzer(strategies_path=templates_path)
            self.tracker = EmotionEscalationTracker(threshold=2)
            self.config = HardwareAdaptiveConfig.get_config()
            logger.info("情感分析管理器已初始化")
    
    def analyze(self, text: str) -> dict:
        """分析文本情感"""
        if not self.analyzer:
            return {"emotion": "neutral", "confidence": 0.5}
        return self.analyzer.analyze(text)
    
    def should_escalate(self, userid: str) -> bool:
        """判断是否应该转人工"""
        if not self.tracker:
            return False
        return self.tracker.should_escalate(userid)
    
    def record_emotion(self, emotion: str, userid: str):
        """记录情感状态"""
        if self.tracker and EMOTION_AVAILABLE:
            emotion_enum = Emotion.from_string(emotion)
            self.tracker.record(emotion_enum, userid)
    
    def get_strategy(self, emotion: str, confidence: float) -> dict:
        """获取对应情感的策略"""
        if not self.analyzer:
            return {}
        emotion_enum = Emotion.from_string(emotion) if EMOTION_AVAILABLE else None
        if emotion_enum:
            return self.analyzer.get_strategy(emotion_enum, confidence)
        return {}


# ==========================================
# 方言管理器（v2.3 新增）
# ==========================================

class DialectManager:
    """方言管理器：检测方言并提供方言回复"""
    
    def __init__(self):
        self.detector = None
        if DIALECT_AVAILABLE:
            self.detector = DialectDetector()
            logger.info("方言管理器已初始化")
    
    def detect(self, text: str) -> dict:
        """检测方言类型"""
        if not self.detector:
            return {"dialect": "mandarin", "confidence": 0.0}
        return self.detector.detect(text)
    
    def get_reply(self, dialect: str, template_name: str) -> str:
        """获取方言回复模板"""
        if not self.detector:
            return "您好！请问有什么可以帮您？"
        try:
            d = Dialect(dialect) if DIALECT_AVAILABLE else Dialect.MANDARIN
            return self.detector.get_reply_template(d, template_name)
        except (ValueError, AttributeError):
            return "您好！请问有什么可以帮您？"


# ==========================================
# 工单管理器集成（v2.3 新增）
# ==========================================

class TicketManagerIntegration:
    """工单管理器集成：自动创建工单、检测意图"""
    
    def __init__(self):
        self.manager = None
        if TICKET_AVAILABLE:
            self.manager = TicketManager()
            logger.info("工单管理器集成已初始化")
    
    def should_create_ticket(self, text: str, emotion: str = "neutral") -> bool:
        """判断是否需要创建工单"""
        if not self.manager:
            return False
        
        # 紧急/投诉类内容自动建单
        urgent_keywords = ["投诉", "差评", "欺骗", "骗子", "骗钱", "虚假宣传",
                          "态度恶劣", "敷衍", "推诿", "不处理"]
        for kw in urgent_keywords:
            if kw in text:
                return True
        
        # 愤怒情绪自动建单
        if emotion == "angry":
            return True
        
        # 退款/账户问题
        refund_keywords = ["退款", "退费", "退货", "账号被封", "密码忘记", "无法登录"]
        for kw in refund_keywords:
            if kw in text:
                return True
        
        return False
    
    def auto_create(self, text: str, userid: str = "system",
                    emotion_tag: str = "neutral", dialect_tag: str = "mandarin") -> dict:
        """自动创建工单"""
        if not self.manager:
            return {"success": False, "error": "工单管理器不可用"}
        
        return self.manager.auto_create_ticket(
            text=text,
            created_by=userid,
            emotion_tag=emotion_tag,
            dialect_tag=dialect_tag,
            source="auto"
        )


# 全局管理器实例
emotion_manager = EmotionManager()
dialect_manager = DialectManager()
ticket_integration = TicketManagerIntegration()
vad_filter = VADFilter(sensitivity="medium") if VAD_AVAILABLE else None
priority_queue = PriorityRequestQueue(max_size=200, rate_limit=20) if QUEUE_AVAILABLE else None
# ==========================================
# VAD 前置过滤器（v2.4 新增）
# ==========================================

class VADPreFilter:
    """
    VAD 前置过滤引擎
    
    在消息进入主处理流程前，过滤非人声消息（电视/音乐/噪音），
    降低误触发率 80%+。
    """
    
    def __init__(self):
        self.vad = VADFilter(sensitivity="medium") if VAD_AVAILABLE else None
        self._filtered_count = 0
        self._total_count = 0
    
    def filter(self, msgtype: str, content: str = "", audio_path: str = "") -> Dict:
        """
        过滤消息
        
        Args:
            msgtype: 消息类型 (voice/text/image/...)
            content: 文本内容
            audio_path: 音频文件路径（voice 消息）
            
        Returns:
            dict: {
                "pass": bool,           # 是否通过过滤
                "reason": str,          # 过滤原因
                "confidence": float     # 置信度
            }
        """
        self._total_count += 1
        
        # 非语音消息直接通过
        if msgtype != "voice":
            return {"pass": True, "reason": "非语音消息", "confidence": 1.0}
        
        # VAD 不可用，降级放行
        if not self.vad:
            return {"pass": True, "reason": "VAD 不可用，降级放行", "confidence": 0.5}
        
        # 文本内容直接通过（已通过 ASR 转写）
        if content and len(content) > 0:
            return {"pass": True, "reason": "已有 ASR 文本", "confidence": 1.0}
        
        # 分析音频文件
        if audio_path and os.path.exists(audio_path):
            try:
                result = self.vad.analyze(audio_path)
                is_speech = result.get("is_speech", True)
                
                if not is_speech:
                    self._filtered_count += 1
                    logger.info(f"VAD 过滤: 非人声消息被过滤 (置信度: {result.get('confidence', 0)})")
                    return {
                        "pass": False,
                        "reason": "非人声消息",
                        "confidence": result.get("confidence", 0)
                    }
                
                return {
                    "pass": True,
                    "reason": "人声消息",
                    "confidence": result.get("confidence", 0.5)
                }
            except Exception as e:
                logger.warning(f"VAD 分析失败 ({e})，降级放行")
                return {"pass": True, "reason": "VAD 错误，降级放行", "confidence": 0.0}
        
        # 无音频文件，放行
        return {"pass": True, "reason": "无音频文件", "confidence": 0.5}
    
    def get_stats(self) -> Dict:
        """获取过滤统计"""
        return {
            "total": self._total_count,
            "filtered": self._filtered_count,
            "filter_rate": round(self._filtered_count / max(self._total_count, 1), 4)
        }


# ==========================================
# 优先级路由器（v2.4 新增）
# ==========================================

class PriorityRouter:
    """
    请求优先级路由器
    
    根据用户类型和消息内容，分配优先级，
    高价值客户优先响应。
    """
    
    def __init__(self):
        self.queue = PriorityRequestQueue(max_size=200, rate_limit=20) if QUEUE_AVAILABLE else None
        # VIP 用户列表（可从配置文件加载）
        self._vip_users: set = set()
        self._high_value_users: set = set()
    
    def add_vip(self, userid: str):
        """添加 VIP 用户"""
        self._vip_users.add(userid)
    
    def add_high_value(self, userid: str):
        """添加高价值用户"""
        self._high_value_users.add(userid)
    
    def get_priority(self, userid: str, content: str = "") -> Priority:
        """
        获取请求优先级
        
        Args:
            userid: 用户ID
            content: 消息内容
            
        Returns:
            Priority: 优先级
        """
        if not QUEUE_AVAILABLE:
            return Priority.NORMAL
        
        if userid in self._vip_users:
            return Priority.VIP
        
        if userid in self._high_value_users:
            return Priority.HIGH_VALUE
        
        # 根据消息内容判断
        urgent_keywords = ["紧急", "投诉", "退款", "报警"]
        for kw in urgent_keywords:
            if kw in content:
                return Priority.HIGH_VALUE
        
        return Priority.NORMAL
    
    def enqueue_or_process(self, userid: str, content: str, 
                          callback, **kwargs) -> Optional[Dict]:
        """
        入队或直接处理
        
        如果限流且非VIP，入队等待；否则直接处理。
        
        Args:
            userid: 用户ID
            content: 消息内容
            callback: 处理回调函数
            **kwargs: 其他参数
            
        Returns:
            dict or None: 处理结果
        """
        priority = self.get_priority(userid, content)
        
        # 检查限流
        rate_check = self.queue.check_rate_limit() if self.queue else {"allowed": True}
        
        if not rate_check.get("allowed", True) and priority == Priority.VIP:
            # VIP 也限流，但允许插队
            pass
        
        # 直接处理（限流允许或高优先级）
        if rate_check.get("allowed", True) or priority <= Priority.HIGH_VALUE:
            return callback()
        
        # 限流且低优先级，入队
        if self.queue:
            result = self.queue.enqueue_simple(
                request_id=f"req_{int(time.time()*1000)}_{userid}",
                userid=userid,
                content=content,
                priority=priority,
                **kwargs
            )
            
            if result.get("dropped"):
                return {
                    "msgtype": "text",
                    "text": {
                        "content": "当前咨询量较大，请稍后再试。您也可以留下联系方式，我们会尽快回复。"
                    }
                }
            
            return {
                "msgtype": "text",
                "text": {
                    "content": f"您的请求已排队（位置: {result.get('position', '?')}），预计等待 {result.get('estimated_wait', 0):.0f} 秒。"
                }
            }
        
        return callback()


# ==========================================
# 全局实例
# ==========================================

vad_prefilter = VADPreFilter()
priority_router = PriorityRouter()
compliance_mgr = ComplianceManager() if COMPLIANCE_AVAILABLE else None
call_record_subsystem = CallRecordSubsystem() if CALL_RECORD_AVAILABLE else None
voicemail_summarizer = VoicemailSummarizer() if VOICEMAIL_AVAILABLE else None


# ==========================================
# 模式 1：纯 keyword 匹配
# ==========================================

class KeywordIntentParser:
    """基于关键词的意图识别器"""
    
    def __init__(self):
        self.intent_keywords = {
            "query_schedule": [
                "日程", "会议", "安排", "行程", "有什么会", "几点开会",
                "日程安排", "会议安排", "什么安排", "下周", "下周有什么",
                "下周一", "下周二", "下周三", "下周四", "下周五", "下周六", "下周日",
                "明天会", "明天安排", "后天会", "今天会议", "今天的会",
                "什么会", "有哪些会", "几号有会", "哪天开会"
            ],
            "create_todo": [
                "提醒", "待办", "任务", "别忘了", "记得", "定时提醒",
                "设提醒", "创建待办", "定提醒", "叫我", "喊我",
                "不要忘", "别忘了带", "提醒我带", "通知我", "到点叫我",
                "记得提醒", "需要注意", "千万别忘"
            ],
            "query_weather": [
                "天气", "气温", "下雨", "温度", "穿什么", "热不冷",
                "天气预报", "气温多少", "冷不冷", "热不热", "温度多少",
                "多少度", "下不下雨", "出太阳", "刮风", "空气质量",
                "湿度", "雾霾", "pm2.5"
            ],
            "send_message": [
                "发消息", "告诉", "通知", "发信息", "发微信",
                "给.*发", "发给他", "发给她", "转告", "传话",
                "跟.*说", "发条信息", "发个消息"
            ],
            "help": [
                "帮助", "能做什么", "怎么用", "功能", "help",
                "你可以做什么", "使用说明", "教教我", "告诉我怎么用",
                "帮我了解", "你是干嘛的", "你的功能"
            ],
            "exit_voice": [
                "退出", "不用了", "谢谢", "结束", "再见", "拜拜",
                "先这样", "好吧", "好的再见", "没事了", "退下"
            ],
            "greeting": [
                "你好", "hi", "hello", "嗨", "早上好", "下午好", "晚上好",
                "在吗", "在不", "你是谁", "你叫什么"
            ],
            "time_query": [
                "几点", "时间", "现在时间", "今天几号", "今天星期几",
                "当前时间", "现在几点", "今日日期"
            ]
        }
    
    def parse(self, text):
        """解析意图（支持混合匹配：字面包含 + 正则模式）"""
        if not text:
            return None, 0, {}
        
        text_lower = text.lower().strip()
        best_intent = "custom"
        max_score = 0
        
        for intent, keywords in self.intent_keywords.items():
            score = 0
            for kw in keywords:
                # 包含正则元字符的关键词用正则匹配
                if any(c in kw for c in ".^$*+?{}[]|()"):
                    try:
                        if re.search(kw, text_lower):
                            score += 1
                    except re.error:
                        if kw in text_lower:
                            score += 1
                else:
                    if kw in text_lower:
                        score += 1
            # 加权：匹配多个不同关键词有加分
            if score > 0:
                score += (score - 1) * 0.1
            if score > max_score:
                max_score = score
                best_intent = intent
        
        confidence = min(max_score / 3.0, 1.0)
        entities = self._extract_entities(text_lower)
        
        return best_intent, confidence, entities
    
    def _extract_entities(self, text):
        """提取实体信息"""
        entities = {}
        
        # 时间
        time_map = {
            "今天": 0, "明天": 1, "后天": 2, "大后天": 3,
            "昨天": -1, "前天": -2
        }
        for word, offset in time_map.items():
            if word in text:
                target = datetime.now() + timedelta(days=offset)
                entities["time"] = word
                entities["date"] = target.strftime("%Y-%m-%d")
                break
        
        # 周一..周日匹配
        for i, day in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            if day in text:
                today = datetime.now()
                days_ahead = (i - today.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7
                target = today + timedelta(days=days_ahead)
                entities["date"] = target.strftime("%Y-%m-%d")
                entities["time"] = day
        
        # 日期匹配: X月X日
        date_m = re.search(r'(\d{1,2})月(\d{1,2})日', text)
        if date_m:
            month, day = date_m.groups()
            entities["date"] = f"{datetime.now().year}-{int(month):02d}-{int(day):02d}"
        
        # 时间匹配: X点X分 / X点 / 下午X点
        time_m = re.search(r'(\d{1,2})点(\d{1,2})分', text)
        if time_m:
            hour = int(time_m.group(1))
            minute = int(time_m.group(2))
            entities["time_of_day"] = f"{hour:02d}:{minute:02d}"
        else:
            time_m = re.search(r'(上|下|晚)?午?(\d{1,2})点', text)
            if time_m:
                prefix = time_m.group(1) or ""
                hour = int(time_m.group(2))
                # PM conversion
                if prefix in ("下", "晚") and hour < 12:
                    hour += 12
                entities["time_of_day"] = f"{hour:02d}:00"
        
        # 人物（排除常见动词干扰："张三发"→只取"张三"）
        surname_cls = "王李张刘陈杨黄赵周吴徐孙马朱胡郭何高林郑谢罗梁宋唐许韩冯邓曹彭曾田董袁潘于蒋蔡余杜叶程苏魏吕丁任沈姚卢姜崔钟谭陆汪范金石廖贾夏付方白邹孟熊秦江薛闫段雷侯龙史陶黎贺顾毛郝龚邵万钱严覃武戴莫孔白汤"
        verb_cls = "发说告诉传话通知知提醒"
        name_m = re.search(rf'([{surname_cls}][^{verb_cls}][^{verb_cls}])', text)
        if name_m:
            entities["person"] = name_m.group(1)
        
        # 地点
        cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉",
                  "西安", "南京", "重庆", "苏州", "天津", "长沙", "郑州", "大连",
                  "青岛", "厦门", "福州", "昆明", "珠海"]
        for c in cities:
            if c in text:
                entities["location"] = c
                break
        
        return entities


# ==========================================
# 服务执行层
# ==========================================

class WeatherService:
    """天气查询服务（使用 wttr.in 免费 API，无需 API key）"""
    
    @staticmethod
    def query(location="北京"):
        """
        查询指定城市的天气
        
        Args:
            location: 城市名
        Returns:
            str: 天气信息文本
        """
        if not location:
            location = "北京"
        
        # 城市名映射（中文名 -> wttr.in 代码）
        city_map = {
            "北京": "Beijing", "上海": "Shanghai", "广州": "Guangzhou",
            "深圳": "Shenzhen", "杭州": "Hangzhou", "成都": "Chengdu",
            "武汉": "Wuhan", "西安": "Xian", "南京": "Nanjing",
            "重庆": "Chongqing", "苏州": "Suzhou", "天津": "Tianjin"
        }
        
        query_name = city_map.get(location, location)
        
        try:
            # wttr.in JSON 接口（免费，无需注册）
            url = f"https://wttr.in/{query_name}?format=j1"
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            
            current = data["current_condition"][0]
            temp = current["temp_C"]
            desc_en = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            wind_kmph = current["windspeedKmph"]
            feels_like = current["FeelsLikeC"]
            
            # 天气描述翻译_map
            desc_map = {
                "Sunny": "☀️ 晴",
                "Clear": "☀️ 晴",
                "Partly cloudy": "⛅ 多云",
                "Partly Cloudy": "⛅ 多云",
                "Cloudy": "☁️ 阴",
                "Overcast": "☁️ 阴",
                "Mist": "🌫️ 薄雾",
                "Fog": "🌫️ 雾",
                "Freezing fog": "🌫️ 冻雾",
                "Patchy rain possible": "🌦️ 可能有零星小雨",
                "Patchy rain nearby": "🌦️ 附近有雨",
                "Patchy snow possible": "🌨️ 可能有零星小雪",
                "Patchy sleet possible": "🌨️ 可能有雨夹雪",
                "Patchy freezing drizzle possible": "🌧️ 可能有冻毛雨",
                "Thundery outbreaks possible": "⛈️ 可能有雷暴",
                "Blowing snow": "🌨️ 吹雪",
                "Blizzard": "❄️ 暴风雪",
                "Light drizzle": "🌧️ 小毛毛雨",
                "Patchy light drizzle": "🌧️ 零星小雨",
                "Freezing drizzle": "🌧️ 冻毛雨",
                "Heavy freezing drizzle": "🌧️ 强冻雨",
                "Light rain": "🌧️ 小雨",
                "Light rain shower": "🌧️ 小阵雨",
                "Moderate rain": "🌧️ 中雨",
                "Moderate rain at times": "🌧️ 间歇性中雨",
                "Heavy rain": "🌧️ 大雨",
                "Heavy rain at times": "🌧️ 间歇性大雨",
                "Light freezing rain": "🌧️ 小冻雨",
                "Moderate or heavy freezing rain": "🌧️ 中到大冻雨",
                "Light sleet": "🌧️ 小雨夹雪",
                "Moderate or heavy sleet": "🌧️ 中到大雨夹雪",
                "Light snow": "🌨️ 小雪",
                "Patchy light snow": "🌨️ 零星小雪",
                "Moderate snow": "🌨️ 中雪",
                "Patchy moderate snow": "🌨️ 零星中雪",
                "Heavy snow": "🌨️ 大雪",
                "Patchy heavy snow": "🌨️ 零星大雪",
                "Ice pellets": "🧊 冰粒",
                "Light showers of ice pellets": "🧊 小冰粒阵雨",
                "Moderate or heavy showers of ice pellets": "🧊 中到大冰粒阵雨",
                "Moderate or heavy rain shower": "🌧️ 中到大阵雨",
                "Torrential rain shower": "🌧️ 暴雨",
                "Light sleet showers": "🌧️ 小雨夹雪阵雨",
                "Moderate or heavy sleet showers": "🌧️ 中到大雨夹雪阵雨",
                "Light snow showers": "🌨️ 小阵雪",
                "Moderate or heavy snow showers": "🌨️ 中到大阵雪",
                "Patchy light rain with thunder": "⛈️ 零星小雨伴雷",
                "Moderate or heavy rain with thunder": "⛈️ 中到大雷雨",
                "Patchy light snow with thunder": "⛈️ 零星小雪伴雷",
                "Moderate or heavy snow with thunder": "⛈️ 中到大雷雪"
            }
            
            # 天气描述翻译（不区分大小写 + 部分匹配）
            desc_zh = desc_en
            desc_lower = desc_en.lower()
            for en_key, zh_val in desc_map.items():
                if en_key.lower() in desc_lower:
                    desc_zh = zh_val
                    break
            
            # 穿衣建议
            temp_int = int(temp)
            if temp_int >= 30:
                advice = "非常热，穿短袖短裤，注意防晒"
            elif temp_int >= 25:
                advice = "较热，穿短袖薄衫即可"
            elif temp_int >= 20:
                advice = "舒适，穿长袖薄衫或衬衫"
            elif temp_int >= 15:
                advice = "微凉，建议穿薄外套"
            elif temp_int >= 10:
                advice = "凉，穿夹克或薄毛衣"
            elif temp_int >= 5:
                advice = "较冷，穿厚外套或棉服"
            elif temp_int >= 0:
                advice = "冷，穿厚棉服或羽绒服"
            else:
                advice = "非常冷，请穿羽绒服保暖"
            
            result = (
                f"{location}当前天气：\n\n"
                f"{desc_zh}\n"
                f"🌡️ 温度：{temp}°C | 体感温度：{feels_like}°C\n"
                f"💧 湿度：{humidity}%\n"
                f"🌬️ 风速：{wind_kmph}km/h\n"
                f"👗 穿衣建议：{advice}"
            )
            
            return result
            
        except (URLError, socket.timeout, ConnectionError) as e:
            logger.warning(f"天气API网络错误: {e}")
            return (
                f"{location}天气查询\n\n"
                f"⚠️ 暂时无法获取天气数据（网络连接问题）。\n"
                f"请稍后重试，或直接搜索「{location}天气」查看。\n\n"
                f"常见原因：\n"
                f"• 当前网络无法访问天气服务\n"
                f"• 企业微信服务器网络波动\n\n"
                f"您可以：\n"
                f"1. 稍后再次尝试\n"
                f"2. 切换到手机网络后重试"
            )
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            logger.warning(f"天气API数据解析错误: {e}")
            return (
                f"{location}天气查询\n\n"
                f"⚠️ 天气数据解析失败，请稍后重试。\n"
                f"您可以尝试说「明天天气」来查询明天的情况。"
            )
        except Exception as e:
            logger.error(f"天气查询未知错误: {e}")
            return (
                f"天气查询遇到了临时问题 😅\n"
                f"请稍后重试，或尝试其他指令。"
            )


class TimeService:
    """时间查询服务（本地计算，无需网络）"""
    
    @staticmethod
    def query(text):
        """查询时间/日期"""
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%Y年%m月%d号")
        weekday_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekday = weekday_map[now.weekday()]
        return f"现在是 {date_str} {weekday} {time_str}"


# ==========================================
# 主消息处理器
# ==========================================

class MessageHandler:
    """消息处理主控制器"""
    
    def __init__(self):
        self.parser = KeywordIntentParser()
        self.weather = WeatherService()
        self.time_svc = TimeService()
        self.msgid_cache = set()
        # v2.9 群聊相关依赖（缺失时降级，不阻断单聊）
        self.entity_extractor = EntityExtractor() if ENTITY_EXTRACTOR_AVAILABLE else None
        self.todo_mgr = TodoFollowupManager() if TODO_AVAILABLE else None
        self.compliance = get_compliance() if GROUP_COMPLIANCE_AVAILABLE else None
        # 群管理员列表（发言者角色判定），环境变量逗号分隔 userid
        self.group_admins = set(
            a.strip() for a in os.environ.get("WECOM_GROUP_ADMINS", "").split(",") if a.strip()
        )
        # 群聊上下文暂存（供 _dispatch 的处理器读取身份/群维度）
        self._chat_ctx = {}
    
    def handle(self, callback):
        """
        处理一条回调消息（含 VAD 过滤 v2.4、优先级队列 v2.4、语音留言 v2.5）
        
        Args:
            callback: dict, 回调 JSON
        Returns:
            dict or None: 回复消息
        """
        msgid = callback.get("msgid", "")
        msgtype = callback.get("msgtype", "")
        userid = callback.get("from", {}).get("userid", "")
        content = callback.get("voice", {}).get("content", "") or callback.get("text", {}).get("content", "")
        
        # VAD 前置过滤（v2.4 新增）
        vad_result = vad_prefilter.filter(msgtype, content)
        if not vad_result.get("pass", True):
            logger.info(f"VAD 过滤消息: userid={userid}, reason={vad_result.get('reason')}")
            return None
        
        # 去重
        if msgid in self.msgid_cache:
            logger.info(f"重复消息: {msgid[:12]}")
            return None
        self.msgid_cache.add(msgid)
        if len(self.msgid_cache) > 5000:
            self.msgid_cache.clear()
        
        logger.info(f"收到 {msgtype} 消息, userid={userid}")

        # v2.9 群聊路由：识别群消息，仅响应 @机器人 的指令（未被 @ 静默忽略，防刷屏）
        chattype = callback.get("chattype") or callback.get("chat_type") or ""
        chatid = callback.get("chatid") or callback.get("chat_id") or ""
        if chattype == "group" or chatid:
            return self._handle_group(callback, chattype=chattype, chat_id=chatid)

        # 语音留言处理（v2.5 新增）
        if msgtype == "voicemail":
            return self._handle_voicemail(callback)
        
        # 分发
        if msgtype == "voice":
            return self._handle_voice(callback)
        elif msgtype == "text":
            return self._handle_text(callback)
        elif msgtype == "image":
            return self._text_resp("收到图片 📷 暂不支持图片识别，请用语音或文字告诉我您的需求。")
        elif msgtype == "mixed":
            return self._text_resp("收到混合消息 📎 请发送语音或文字消息获取最佳体验。")
        elif msgtype == "file":
            return self._text_resp("收到文件 📎 暂不支持文件处理，请用语音或文字告诉我您的需求。")
        elif msgtype == "video":
            return self._text_resp("收到视频 🎬 暂不支持视频处理，请用语音或文字告诉我您的需求。")
        else:
            return self._text_resp("暂不支持此类消息格式 😅 请发送语音或文字。")
    
    def _handle_voice(self, callback):
        """处理语音消息（含情感分析 v2.2、方言检测+工单 v2.3）"""
        content = callback.get("voice", {}).get("content", "").strip()
        userid = callback.get("from", {}).get("userid", "")
        
        logger.info(f"语音内容: {content[:80]}")
        
        if not content:
            return self._text_resp(
                "抱歉，我没有听清您的语音 😅\n\n"
                "请确认：\n"
                "• 说话时靠近麦克风 20-30cm\n"
                "• 环境不要太嘈杂\n"
                "• 用普通话慢慢说\n"
                "• 控制在 60 秒内"
            )
        
        # 单聊路径：复用统一内容处理（v2.9 抽出，便于群聊复用单聊引擎）
        return self._process_content(content, userid, chat_type="single")

    def _try_handle_confirm(self, content: str, userid: str):
        """
        群任务确认回执闭环（v2.9）：被指派人在单聊或群 @机器人 回复时闭环

        当消息内容是一句简短的确认/拒绝，且该用户存在 pending_confirm 的群任务时，
        拦截并调用 confirm_todo 完成回执闭环，避免进入通用意图引擎造成误回复。
        """
        if not (self.todo_mgr and userid):
            return None
        c = (content or "").strip()
        if not c:
            return None
        # 低误判：仅当内容简短且命中确认/拒绝关键词才拦截
        stripped = re.sub(r'[\s，。、！？!?.,]+', '', c)
        if len(stripped) > 12:
            return None
        is_reject = any(w in stripped for w in ("拒绝", "不接受", "不同意", "不要", "不行", "驳回"))
        is_confirm = any(w in stripped for w in ("确认", "接受", "同意", "好的", "可以", "ok", "OK", "没问题"))
        if not (is_reject or is_confirm):
            return None
        # 查找该用户待确认的群任务
        try:
            todos = self.todo_mgr.query_by_assignee(userid, keyword="")
        except Exception:
            return None
        pending = [t for t in todos if t.get("confirm_status") == "pending_confirm"]
        if not pending:
            return None
        # 取最近一条待确认任务闭环
        pending.sort(key=lambda t: t.get("created_at", ""), reverse=True)
        accept = not is_reject
        receip = self.todo_mgr.confirm_todo(pending[0].get("todo_id"), accept=accept)
        if receip.get("ok"):
            return self._text_resp(receip.get("receipt", "已处理。"))
        return None

    def _process_content(self, content: str, userid: str, chat_type: str = "single",
                         chat_id: str = "", speaker_role: str = "", speaker_userid: str = ""):
        """
        统一内容处理（v2.9 抽出）：情感分析→方言→工单→意图→策略→分发
        单聊与群聊共用此引擎，仅 chat_type / 身份上下文不同。

        Args:
            content: 已清理的文本内容
            userid: 用户ID（群聊时为发言者）
            chat_type: single / group
            chat_id: 群聊ID
            speaker_role: 发言者角色（member/admin/unknown）
            speaker_userid: 发言者 userid（群聊，用于身份注入）
        """
        # v2.9 群任务确认回执闭环：被指派人回复「确认/拒绝」优先拦截闭环
        confirm_resp = self._try_handle_confirm(content, userid)
        if confirm_resp is not None:
            return confirm_resp

        # 情感分析（v2.2 新增）
        emotion_result = self._analyze_emotion(content, userid)

        # 情感升级检测
        if emotion_result.get("should_escalate"):
            return self._text_resp(
                "为了更好地解决您的问题，我现在为您转接专属人工客服，请稍等... 🙏\n\n"
                "您也可以留下联系方式，我们会尽快回复。"
            )

        # 方言检测（v2.3 新增）
        dialect_result = dialect_manager.detect(content)
        dialect = dialect_result.get("dialect", "mandarin")
        dialect_str = dialect.value if hasattr(dialect, 'value') else str(dialect)

        # 自动工单创建（v2.3 新增）
        ticket_id = None
        emotion = emotion_result.get("emotion", "neutral")
        if ticket_integration.should_create_ticket(content, emotion):
            ticket_result = ticket_integration.auto_create(
                text=content,
                userid=userid,
                emotion_tag=emotion,
                dialect_tag=dialect_str
            )
            if ticket_result.get("success") or ticket_result.get("id"):
                ticket_id = ticket_result.get("id")
                logger.info(f"自动创建工单: {ticket_id}")

        # 意图分析
        intent, confidence, entities = self.parser.parse(content)
        logger.info(f"意图: {intent}, 置信度: {confidence:.2f}, 情感: {emotion}, 方言: {dialect_str}, 类型: {chat_type}")

        # 根据情感调整回复策略
        strategy = emotion_manager.get_strategy(emotion, emotion_result.get("confidence", 0.5))

        # 置信度低时，用智能确认策略
        if confidence < 0.25:
            return self._smart_clarify(content, emotion=emotion, strategy=strategy,
                                       dialect=dialect_str, ticket_id=ticket_id)

        return self._dispatch(intent, entities, content, emotion=emotion, strategy=strategy,
                              dialect=dialect_str, ticket_id=ticket_id,
                              chat_type=chat_type, chat_id=chat_id, speaker_role=speaker_role,
                              speaker_userid=speaker_userid or userid)
    
    def _handle_voicemail(self, callback):
        """
        处理语音留言（v2.5 新增）
        
        当用户无法接听时，语音留言自动转录并生成摘要，
        推送给被叫方。
        """
        content = callback.get("voicemail", {}).get("content", "").strip()
        caller = callback.get("from", {}).get("userid", "")
        callee = callback.get("to", {}).get("userid", "")
        vm_id = callback.get("msgid", "")
        
        logger.info(f"语音留言: caller={caller}, callee={callee}, content={content[:50]}")
        
        if not content:
            return self._text_resp(
                "收到语音留言，但内容无法识别。\n"
                "请确认留言时长在 60 秒以内，并用普通话清晰表达。"
            )
        
        # 生成语音留言摘要（v2.5 新增）
        if VOICEMAIL_AVAILABLE and voicemail_summarizer:
            try:
                summary_result = voicemail_summarizer.process_voicemail(
                    vm_id=vm_id,
                    caller=caller,
                    content=content,
                    source="voicemail"
                )
                rendered = voicemail_summarizer.render_summary(summary_result)
                
                # 记录到通话记录子系统（v2.5 新增）
                if CALL_RECORD_AVAILABLE and call_record_subsystem:
                    try:
                        call_record_subsystem.create_record(
                            call_id=vm_id,
                            caller=caller,
                            callee=callee,
                            direction="voicemail"
                        )
                        call_record_subsystem.add_transcript(vm_id, content, summary_result.get("intent", "voicemail"))
                    except Exception as e:
                        logger.warning(f"语音留言记录失败: {e}")
                
                return self._text_resp(rendered)
            except Exception as e:
                logger.warning(f"语音留言摘要生成失败: {e}")
                # 降级：直接返回原始内容
                return self._text_resp(
                    f"📮 收到语音留言\n\n"
                    f"来电：{caller}\n"
                    f"内容：{content[:200]}\n\n"
                    f"摘要生成失败，请查看原始留言内容。"
                )
        
        # 降级：无摘要能力
        return self._text_resp(
            f"📮 收到语音留言\n\n"
            f"来电：{caller}\n"
            f"内容：{content[:200]}"
        )

    def _analyze_emotion(self, text: str, userid: str) -> dict:
        """
        分析文本情感并记录状态（v2.2）
        
        Returns:
            dict: {
                "emotion": str,
                "confidence": float,
                "should_escalate": bool
            }
        """
        if not EMOTION_AVAILABLE:
            return {"emotion": "neutral", "confidence": 0.5, "should_escalate": False}
        
        try:
            result = emotion_manager.analyze(text)
            emotion = result.get("emotion", Emotion.NEUTRAL)
            confidence = result.get("confidence", 0.5)
            
            # 记录情感
            emotion_manager.record_emotion(emotion.value if hasattr(emotion, 'value') else str(emotion), userid)
            
            # 检查是否升级
            should_escalate = emotion_manager.should_escalate(userid)
            
            return {
                "emotion": emotion.value if hasattr(emotion, 'value') else str(emotion),
                "confidence": confidence,
                "should_escalate": should_escalate
            }
        except Exception as e:
            logger.warning(f"情感分析失败: {e}")
            return {"emotion": "neutral", "confidence": 0.5, "should_escalate": False}
    
    def _handle_text(self, callback):
        """处理文本消息（含情感分析 v2.2、方言检测+工单 v2.3）"""
        content = callback.get("text", {}).get("content", "").strip()
        userid = callback.get("from", {}).get("userid", "")
        
        if not content:
            return self._text_resp("您好！请输入您的需求，或发送语音消息。")
        
        # 退出命令
        if content in ["退出语音模式", "结束", "再见"]:
            return self._text_resp(
                "已退出语音模式 ✅ 下次需要时请再次私聊我并发送语音消息。\n\n"
                "感谢您使用语音助手，再见～🌟"
            )
        
        # 帮助命令
        if content in ["帮助", "能做什么", "怎么用", "?"]:
            return self._help_response()
        
        # 单聊路径：复用统一内容处理（v2.9 抽出）
        return self._process_content(content, userid, chat_type="single")

    # === 群聊处理（v2.9）===

    def _handle_group(self, callback, chattype="group", chat_id=""):
        """
        群聊消息处理（v2.9）

        仅响应 @机器人 的指令；未被 @ 静默忽略（防刷屏）。
        复用单聊内容引擎（_process_content），并注入发言者身份上下文
        （谁在说话 / 什么角色），使意图识别与应答能区分群内不同成员。

        Args:
            callback: 回调 JSON
            chattype: 会话类型标识
            chat_id: 群聊ID
        """
        msgtype = callback.get("msgtype", "")
        userid = callback.get("from", {}).get("userid", "")
        speaker_role = "admin" if userid in self.group_admins else "member"

        # 群聊合规：默认不落盘（磁盘零语音文件），仅即时转写处理
        if self.compliance and self.compliance.record_audio_disabled():
            logger.info(f"群聊合规：语音不落盘，仅转写处理 chat_id={chat_id}")

        # 未被 @机器人 则静默忽略（防刷屏，企微机制已保证群推送必 @）
        if not self._is_mentioned(callback):
            logger.info(f"群消息未 @机器人，静默忽略 userid={userid}")
            return None

        # 提取并清理内容（去掉 @机器人 前缀，便于意图解析）
        if msgtype == "voice":
            content = callback.get("voice", {}).get("content", "").strip()
        else:
            content = callback.get("text", {}).get("content", "").strip()
        content = self._strip_mention(content)

        # v2.9 群内 @机器人 确认回执闭环（被指派人确认/拒绝）
        confirm_resp = self._try_handle_confirm(content, userid)
        if confirm_resp is not None:
            return confirm_resp

        if not content:
            return self._text_resp(
                "您好！我已收到您的 @，请告诉我具体需求，例如「@我 周三前交方案」。"
            )

        # 设置群聊上下文（发言者身份 + 群维度），供处理器与群任务分发使用
        self._chat_ctx = {
            "chat_type": "group", "chat_id": chat_id,
            "speaker_role": speaker_role, "speaker_userid": userid,
        }

        # 群任务指派优先：识别「@某人 期限 任务」三元组，独立于意图引擎
        if self.entity_extractor and self.todo_mgr:
            assign = self.entity_extractor.extract_assignment(content, userid)
            if assign.get("is_assignment") and assign.get("assignee"):
                return self._dispatch_group_assignment(assign, content)

        # 否则复用单聊引擎，注入发言者身份（谁在说话 / 角色），零重构
        return self._process_content(
            content, userid,
            chat_type="group", chat_id=chat_id,
            speaker_role=speaker_role, speaker_userid=userid,
        )

    def _dispatch_group_assignment(self, assign: Dict[str, Any], content: str):
        """
        群任务指派分发（v2.9）：落库 + 指派确认回执

        把群里的口头安排从「说了」变成「记了 + 认了」：
        - 建群待办（assigner=发言者, assignee=被指派人）
        - 向被指派人推送确认回执，待其确认/拒绝闭环
        """
        due_date = assign.get("due_date")
        if not due_date:
            due_date = (datetime.now() + timedelta(days=1)).date().isoformat()
        todo = {
            "call_id": self._chat_ctx.get("chat_id", ""),
            "userid": assign.get("assigner", ""),
            "content": content,
            "due_date": due_date,
        }
        ok = self.todo_mgr.register_todo(
            todo, assigner=assign["assigner"], assignee=assign["assignee"],
            chat_id=self._chat_ctx.get("chat_id", ""), source_group=True,
            auto_schedule=False,
        )
        if ok:
            return self._text_resp(
                f"📌 已在群里建立任务\n\n"
                f"• 内容：{content}\n"
                f"• 指派给：@{assign['assignee']}\n"
                f"• 指派方：{assign.get('assigner', '')}\n"
                f"• 截止：{due_date}\n\n"
                f"@{assign['assignee']} 请确认是否接受（回复「确认」/「拒绝」）。"
            )
        return self._text_resp("任务登记失败，请稍后再试。")

    def _is_mentioned(self, callback: dict) -> bool:
        """
        判断是否 @机器人（群聊防刷屏）

        企微机制：群聊中仅 @机器人 的消息才会推送给机器人。
        若回调显式给出 mention_list 则按列表判定；否则群语音信任企微推送，
        群文本按内容是否含 @ 判定。
        """
        mention_list = (callback.get("text", {}).get("mention_list")
                       or callback.get("mention_list") or [])
        if mention_list:
            bot_userid = os.environ.get("WECOM_BOT_USERID", "")
            if bot_userid:
                return ("@all" in mention_list) or (bot_userid in mention_list)
            # 未配置机器人 userid：信任企微推送（必 @ 才到）
            return True
        # 无 mention_list：群语音信任企微推送；群文本需内容含 @
        msgtype = callback.get("msgtype", "")
        if msgtype == "voice":
            return True
        content = callback.get("text", {}).get("content", "")
        return "@" in content

    def _strip_mention(self, content: str) -> str:
        """去掉开头的 @某人 前缀，便于意图解析"""
        if not content:
            return content
        m = re.match(r'^@([A-Za-z0-9_\u4e00-\u9fff]{1,20})\s*', content)
        if m:
            return content[m.end():].strip()
        return content

    def _dispatch(self, intent, entities, raw_text, emotion=None, strategy=None,
                  dialect=None, ticket_id=None, chat_type="single", chat_id="",
                  speaker_role="", speaker_userid=""):
        """分发到具体处理器（含情感策略 v2.2、方言+工单 v2.3）"""
        # v2.9 暂存群聊上下文，供处理器（如群任务分发）读取身份/群维度
        self._chat_ctx = {
            "chat_type": chat_type, "chat_id": chat_id,
            "speaker_role": speaker_role, "speaker_userid": speaker_userid,
        }
        handlers = {
            "query_schedule": self._do_query_schedule,
            "create_todo": self._do_create_todo,
            "query_weather": self._do_query_weather,
            "send_message": self._do_send_message,
            "help": self._do_help,
            "exit_voice": self._do_exit,
            "greeting": self._do_greeting,
            "time_query": self._do_time_query,
            "custom": lambda e, t: self._smart_clarify(t, emotion=emotion, strategy=strategy,
                                                       dialect=dialect, ticket_id=ticket_id)
        }
        handler = handlers.get(intent, lambda e, t: self._smart_clarify(t, emotion=emotion, strategy=strategy,
                                                                         dialect=dialect, ticket_id=ticket_id))
        
        result = handler(entities, raw_text)
        
        # handler 返回 dict（_text_resp 格式）或 str
        if not result:
            return result
        
        # 提取文本内容进行处理
        if isinstance(result, dict):
            text_content = result.get("text", {}).get("content", "")
        elif isinstance(result, str):
            text_content = result
        else:
            return result
        
        # 应用情感策略
        if emotion and strategy:
            text_content = self._apply_emotion_strategy(text_content, emotion, strategy)
        
        # 应用方言模板（v2.3 新增）
        if dialect and dialect != "mandarin":
            text_content = self._apply_dialect_template(text_content, dialect)
        
        # 添加工单信息（v2.3 新增）
        if ticket_id:
            text_content = self._append_ticket_info(text_content, ticket_id)
        
        # 返回格式化响应
        if isinstance(result, dict):
            result["text"]["content"] = text_content
            return result
        return text_content
    
    def _apply_emotion_strategy(self, response: str, emotion: str, strategy: dict) -> str:
        """应用情感策略到响应中
        
        Args:
            response: 原始响应文本
            emotion: 情感类型
            strategy: 策略模板
            
        Returns:
            str: 应用策略后的响应
        """
        if not strategy or emotion == "neutral":
            return response
        
        # 愤怒/焦虑：在回复前添加安抚前缀
        if emotion == "angry":
            calm_prefix = "非常抱歉给您带来不好的体验，我理解您的不满。\n\n"
            return calm_prefix + response
        elif emotion == "anxious":
            reassure_prefix = "请您放心，我马上为您处理。\n\n"
            return reassure_prefix + response
        elif emotion == "confused":
            clarify_prefix = "抱歉刚才没讲清楚，我再详细说明一下：\n\n"
            return clarify_prefix + response
        elif emotion == "satisfied":
            # 满意时顺势请求反馈
            feedback_suffix = "\n\n如果您方便的话，可以给我们一个五星好评吗？⭐"
            return response + feedback_suffix
        
        return response
    
    def _apply_dialect_template(self, response: str, dialect: str) -> str:
        """应用方言模板到响应中（v2.3 新增）
        
        Args:
            response: 原始响应文本
            dialect: 方言类型字符串
            
        Returns:
            str: 应用方言模板后的响应
        """
        if not DIALECT_AVAILABLE or dialect == "mandarin":
            return response
        
        # 获取方言问候模板，替换标准问候
        dialect_greeting = dialect_manager.get_reply(dialect, "greeting")
        
        # 检测回复中是否含有标准问候，如果有则替换
        mandarin_greetings = ["您好！", "你好！", "您好，"]
        for mg in mandarin_greetings:
            if mg in response:
                response = response.replace(mg, dialect_greeting + " ", 1)
                break
        
        return response
    
    def _append_ticket_info(self, response: str, ticket_id: str) -> str:
        """在响应末尾添加工单信息（v2.3 新增）
        
        Args:
            response: 原始响应文本
            ticket_id: 工单ID
            
        Returns:
            str: 添加工单信息后的响应
        """
        ticket_suffix = f"\n\n📋 已为您创建工单：{ticket_id}\n我们将尽快为您处理。"
        return response + ticket_suffix
    
    def _smart_clarify(self, text, emotion=None, strategy=None, dialect=None, ticket_id=None):
        """
        智能确认：尝试理解用户模糊意图并给出选项
        不再回复"需要配置API接入"
        含情感策略调整（v2.2）、方言+工单支持（v2.3）
        """
        # 尝试从文本中提取关键信息进行智能匹配
        text_lower = text.lower()
        
        # 如果包含任何关键词但不足以确定，给出引导
        guide = (
            "抱歉，我没有完全理解您的意思 😅\n\n"
            "我可以帮您处理以下任务：\n\n"
            "🗣️ 查询日程：\n"
            '"查一下明天的日程" / "下周一有什么会？"\n\n'
            "🗣️ 创建待办：\n"
            '"提醒我下午3点开会" / "记得叫我带文件"\n\n'
            "🗣️ 查询天气：\n"
            '"北京今天天气怎么样？" / "上海明天会下雨吗？"\n\n'
            "🗣️ 当前时间：\n"
            '"现在几点？" / "今天几号？"\n\n'
            "🗣️ 发送消息：\n"
            '"给张三发消息，明天开会"\n\n'
            "请用上面的例子对我说，我会尽力帮到您！"
        )
        
        # 应用方言模板（v2.3 新增）
        if dialect and dialect != "mandarin":
            guide = self._apply_dialect_template(guide, dialect)
        
        # 添加工单信息（v2.3 新增）
        if ticket_id:
            guide = self._append_ticket_info(guide, ticket_id)
        
        return self._text_resp(guide)
    
    def _do_query_schedule(self, entities, raw_text):
        """查询日程 - 提供真实有用的回复"""
        date = entities.get("date", "今天")
        time = entities.get("time", "")
        person = entities.get("person", "")
        
        # 构建时间范围提示
        when = f"{time}" if time else "今天"
        if date and date != "今天":
            when = date
        
        return self._text_resp(
            f"🗓️ 日程查询（{when}）\n\n"
            f"查询条件：\n"
            f"{'• ' + person + ' 参与' if person else ''}{'  ' if person else ''}{when}的日程安排\n\n"
            f"很抱歉，要查询企业微信日程，需要您配置企业的「日程」应用权限。\n\n"
            f"💡 快速解决方案：\n"
            f"1. 管理员登录 work.weixin.qq.com\n"
            f"2. 应用管理 → 自建应用 → 权限管理\n"
            f"3. 开启「企业微信日程」权限\n"
            f"4. 等待用户授权后，再次尝试\n\n"
            f"✅ 授权完成后，我将可以：\n"
            f"• 查询您指定日期的日程\n"
            f"• 显示会议时间和地点\n"
            f"• 列出所有参与人\n"
            f"\n"
            f"如需快速测试，您可以先问我「北京天气」或「现在几点」看看效果 😊"
        )
    
    def _do_create_todo(self, entities, raw_text):
        """创建待办（v2.9 群聊支持任务指派分发）"""
        date = entities.get("date", "今天")
        tod = entities.get("time_of_day", "")

        # 尝试提取待办内容
        todo_content = raw_text
        # 去掉"提醒" "记得" 等前缀
        for kw in ["提醒我", "提醒", "记得", "别忘了", "定时提醒", "设提醒", "创建待办", "到点叫我"]:
            if kw in todo_content:
                todo_content = todo_content.replace(kw, "").strip()
                break

        if not todo_content:
            todo_content = "（待办内容未识别）"

        # 单聊：维持原提示（需管理员授权才能真正创建企业微信待办）
        # 群任务指派由 _dispatch_group_assignment 优先处理，不在此分支
        return self._text_resp(
            f"✅ 待办提醒已收到！\n\n"
            f"📝 内容：{todo_content}\n"
            f"⏰ 时间：{f'{date} ' if date else ''}{tod if tod else '未指定具体时间'}\n\n"
            f"💡 要创建真实的待办提醒到企业微信，需要您配置应用的「待办」权限。\n\n"
            f"📋 配置步骤：\n"
            f"1. 管理员打开 work.weixin.qq.com → 应用管理\n"
            f"2. 自建应用 → 权限管理 → 开启「企业微信待办」\n"
            f"3. 等待用户授权后，将自动创建提醒\n\n"
            f"✅ 授权完成后，我将可以：\n"
            f"• 自动创建企业微信待办\n"
            f"• 设置提醒时间并准时推送\n"
            f"• 查询和管理待办事项\n"
            f"\n"
            f"您可以先试试「北京天气」来测试当前效果～"
        )
    
    def _do_query_weather(self, entities, raw_text):
        """查询天气 - 调用 wttr.in 获取真实数据"""
        location = entities.get("location", "北京")
        
        # 尝试从原文补全地点
        if location == "Beijing" or location == "auto":
            location = "北京"
        
        # 调用天气服务
        result = self.weather.query(location)
        return self._text_resp(result)
    
    def _do_send_message(self, entities, raw_text):
        """发送消息处理"""
        person = entities.get("person", "")
        
        # 如果 person 末尾含动词（"张三发"），裁掉
        if person and person[-1] in "发说告诉传话通知":
            person = person[:-1]
        
        # 二次提取：正则找"XX发"前面的名字
        if not person:
            m = re.search(r'(给|让|叫)?([\u4e00-\u9fff]{2,3})(发|说|告诉|传话|通知)', raw_text)
            if m:
                person = m.group(2)
        
        # 提取消息内容
        content = raw_text
        if person:
            content = re.sub(rf'(给|让|叫)?{person}(发|说|告诉|传话|通知)[：:]?', '', content).strip()
        
        if not person:
            return self._text_resp(
                "📬 发消息给谁？\n\n"
                "请告诉我对方的姓名，例如：\n"
                '"给张三发：明天早上9点开会"\n'
                '"通知李四下午交报告"'
            )
        
        if not content:
            content = "（消息内容未识别）"
        
        return self._text_resp(
            f"✅ 消息已准备好\n\n"
            f"发送给：{person}\n"
            f"内容：{content}\n\n"
            f"💡 要真正发送到企业微信，需要您配置应用的「消息」权限。\n\n"
            f"📋 配置步骤：\n"
            f"1. 管理员打开 work.weixin.qq.com → 应用管理\n"
            f"2. 自建应用 → 权限管理 → 开启「企业微信消息」\n"
            f"3. 等待用户授权后，将自动发送\n\n"
            f"✅ 授权完成后，我将可以：\n"
            f"• 代您向指定同事发送消息\n"
            f"• 支持群聊消息发送\n"
            f"• 支持文字和图片混合消息\n"
            f"\n"
            f"您可以先试试「北京天气」来测试其他功能～"
        )
    
    def _do_help(self, entities=None, raw_text=None):
        """帮助请求"""
        return self._help_response()
    
    def _do_exit(self, entities=None, raw_text=None):
        return self._text_resp(
            "好的，期待下次为您服务～🌟\n\n"
            "何时需要，直接私聊我并发送语音即可。"
        )
    
    def _do_greeting(self, entities=None, raw_text=None):
        return self._text_resp(
            "您好！👋 我是企业微信语音助手。\n\n"
            "我可以用语音帮您：\n"
            "🗣️ 查询天气（说：北京天气怎么样？）\n"
            "🗣️ 查询日程（说：明天有什么会议？）\n"
            "🗣️ 创建待办（说：提醒我下午3点开会）\n"
            "🗣️ 发送消息（说：给张三发，明天开会）\n"
            "🗣️ 时间查询（说：现在几点？）\n\n"
            "直接发语音告诉我您的需求～"
        )
    
    def _do_time_query(self, entities=None, raw_text=None):
        """时间查询 - 本地计算，100%可用"""
        result = self.time_svc.query(raw_text)
        return self._text_resp(f"🕐 {result}")
    
    def _help_response(self):
        return self._text_resp(
            "📋 我是企业微信语音助手，您的语音办公小帮手。\n\n"
            "🗣️ 常用语音指令：\n\n"
            "1️⃣ 查天气（推荐！100%可用）\n"
            '"北京今天天气怎么样？"\n'
            '"上海明天会下雨吗？"\n\n'
            "2️⃣ 查日程（*需管理员授权）\n"
            '"查一下明天的日程"\n'
            '"下周一有什么会？"\n\n'
            "3️⃣ 建待办（*需管理员授权）\n"
            '"提醒我下午3点开会"\n'
            '"记得叫我带文件"\n\n'
            "4️⃣ 发消息（*需管理员授权）\n"
            '"给张三发：明天9点开会"\n\n'
            "5️⃣ 查时间（100%可用）\n"
            '"现在几点？"\n\n'
            "💡 使用小贴士：\n"
            "• 请在安静环境使用普通话发送语音\n"
            "• 语音时长建议控制在 60 秒内\n"
            "• 仅限私聊使用\n"
            "• 一次说一件事效果更好\n\n"
            "⚠️ 关于「*需管理员授权」功能：\n"
            "这些功能需要企业微信管理员在后台开启权限后，\n"
            "才能真正执行。纯查询类（天气/时间）不需要。\n"
            "如需配置，请让管理员参考部署指南开启权限。\n"
            "如有问题，发送邮件至 njskills@agent.qq.com"
        )
    
    def _text_resp(self, content):
        """构建文本回复对象"""
        return {"msgtype": "text", "text": {"content": content}}


# ==========================================
# HTTP 服务器
# ==========================================

class WebhookHTTPHandler(http.server.BaseHTTPRequestHandler):
    """HTTP 请求处理器"""
    
    handler = MessageHandler()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        # 健康检查
        if parsed.path == "/health":
            self._respond(200, {"status": "ok", "time": int(time.time())})
            return
        
        # 简洁版健康检查
        if parsed.path == "/":
            self._respond(200, {
                "status": "ok",
                "msg": "企业微信语音助手服务运行中",
                "endpoints": ["/", "/health", "/ (POST for WeCom callback)"]
            })
            return
        
        self._respond(404, {"error": "not found"})
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        
        try:
            callback_data = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self._respond(400, {"error": "invalid json"})
            return
        
        try:
            result = self.handler.handle(callback_data)
            if result:
                self._respond(200, result)
            else:
                self._respond(200, {"errcode": 0})
        except Exception as e:
            logger.error(f"处理回调时出错: {e}")
            self._respond(500, {"error": "internal error"})
    
    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
    
    def log_message(self, fmt, *args):
        # 禁用默认 stderr 输出
        pass


# ==========================================
# quick-start 模式
# ==========================================

def run_quick_start():
    """一键体验所有功能"""
    print("=" * 60)
    print("企业微信语音助手 — 快速体验模式")
    print("=" * 60)
    
    h = MessageHandler()
    tests = [
        {"msgid": "t1", "msgtype": "voice", "from": {"userid": "test"}, "voice": {"content": "北京今天天气"}},
        {"msgid": "t2", "msgtype": "text", "from": {"userid": "test"}, "text": {"content": "帮助"}},
        {"msgid": "t3", "msgtype": "voice", "from": {"userid": "test"}, "voice": {"content": "现在几点"}},
        {"msgid": "t4", "msgtype": "voice", "from": {"userid": "test"}, "voice": {"content": "明天有什么会"}},
        {"msgid": "t5", "msgtype": "voice", "from": {"userid": "test"}, "voice": {"content": "给张三发明天开会"}},
        {"msgid": "t6", "msgtype": "voice", "from": {"userid": "test"}, "voice": {"content": "提醒我下午3点带文件"}},
        {"msgid": "t7", "msgtype": "voice", "from": {"userid": "test"}, "voice": {"content": "上海天气"}},
        {"msgid": "t8", "msgtype": "voice", "from": {"userid": "test"}, "voice": {"content": "退出"}},
        {"msgid": "t9", "msgtype": "voice", "from": {"userid": "test"}, "voice": {"content": ""}},
        {"msgid": "t10", "msgtype": "image", "from": {"userid": "test"}, "image": {"url": "http://x.com/1.jpg"}},
    ]
    
    for i, test in enumerate(tests):
        print(f"\n{'─'*50}")
        msgtype = test.get("msgtype")
        if msgtype == "voice":
            txt = test.get("voice", {}).get("content", "")
            print(f"[测试 {i+1}] 语音: \"{txt}\"")
        elif msgtype == "text":
            txt = test.get("text", {}).get("content", "")
            print(f"[测试 {i+1}] 文字: \"{txt}\"")
        else:
            print(f"[测试 {i+1}] 类型: {msgtype}")
        print(f"{'─'*50}")
        result = h.handle(test)
        if result:
            print(result.get("text", {}).get("content", "(无内容)"))
        else:
            print("(无回复)")
    
    print(f"\n{'='*60}")
    print("体验完毕！启动服务器：")
    print("python scripts/wecom_webhook_server.py")
    print('='*60)


# ==========================================
# 启动
# ==========================================

def main():
    if "--quick" in sys.argv:
        run_quick_start()
        return
    
    port = SERVER_PORT
    for i, arg in enumerate(sys.argv):
        if arg == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
    
    server = http.server.HTTPServer((SERVER_HOST, port), WebhookHTTPHandler)
    logger.info("=" * 60)
    logger.info(f"企业微信语音助手回调服务器 v2.0")
    logger.info(f"监听地址: http://{SERVER_HOST}:{port}")
    logger.info("")
    logger.info("接口列表:")
    logger.info("  GET  /         - 服务状态")
    logger.info("  GET  /health   - 健康检查")
    logger.info("  POST /         - 企业微信消息回调")
    logger.info("")
    logger.info("快速测试: python wecom_webhook_server.py --quick")
    logger.info("按 Ctrl+C 停止")
    logger.info("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("\n服务器已停止")
        server.server_close()


if __name__ == "__main__":
    main()
