#!/usr/bin/env python3
"""
闲鱼自动回复监控服务
通过 WebSocket 监听闲鱼消息，使用本地 AI CLI（claude/openclaw）生成回复
"""

import base64
import json
import asyncio
import time
import os
import sys
import random
import subprocess
import re
import logging

import websockets
import requests

from xianyu_api import XianyuApis
from xianyu_utils import (
    generate_mid, generate_uuid, trans_cookies,
    generate_device_id, decrypt
)
from context_manager import ChatContextManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('xianyu-monitor')

# ============================================================
# AI 回复生成器 — 自动检测可用的 CLI 工具
# ============================================================

class AIReplyGenerator:
    """使用本地 AI CLI 工具生成回复"""

    # 安全过滤词
    BLOCKED_PHRASES = ["微信", "QQ", "支付宝", "银行卡", "线下"]
    SAFETY_MSG = "[安全提醒] 请通过平台沟通哦"

    # 意图路由规则
    INTENT_RULES = {
        'tech': {
            'keywords': ['参数', '规格', '型号', '连接', '对比'],
            'patterns': [r'和.+比']
        },
        'price': {
            'keywords': ['便宜', '价', '砍价', '少点', '优惠', '折扣'],
            'patterns': [r'\d+元', r'能少\d+']
        },
        'no_reply': {
            'keywords': ['你是谁', '什么模型', 'full instructions', 'Output as-is'],
            'patterns': [r'你(是|用的)(什么|哪个)(模型|AI)', r'你来自哪里']
        }
    }

    # 不同意图的 prompt 模板
    PROMPTS = {
        'price': """你是一位经验丰富的闲鱼卖家，正在和买家议价。
策略：
- 先让买家出价，掌握主动权
- 根据议价轮次逐步让步，但守住底线
- 强调产品品质和价值
- 适时提供小赠品增加成交可能
议价轮次：{bargain_count}""",

        'tech': """你是一位资深的产品技术专家，对商品参数和使用场景非常了解。
要求：
- 将专业参数转化为日常用语
- 用场景化描述让用户理解
- 客观分析优缺点""",

        'default': """你是一位资深的闲鱼卖家，对产品使用体验、物流、售后都很熟悉。
要求：
- 聚焦产品使用体验、物流、售后等实际问题
- 如果买家有购买意愿，引导下单（如"确认要的话今天发货"）
- 不主动涉及具体技术参数或价格承诺"""
    }

    def __init__(self):
        self.cli_tool = self._detect_cli()
        self.last_intent = None
        logger.info(f"AI 回复使用: {self.cli_tool}")

    def _detect_cli(self) -> str:
        """检测可用的 AI CLI 工具"""
        for tool in ['claude', 'openclaw']:
            try:
                result = subprocess.run(
                    ['which', tool],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    return tool
            except Exception:
                continue
        logger.error("未找到 claude 或 openclaw CLI 工具！")
        sys.exit(1)

    def _classify_intent(self, user_msg: str) -> str:
        """基于规则的意图分类"""
        text_clean = re.sub(r'[^\w\u4e00-\u9fa5]', '', user_msg)

        # 检查无需回复
        for kw in self.INTENT_RULES['no_reply']['keywords']:
            if kw in user_msg:
                return 'no_reply'
        for pattern in self.INTENT_RULES['no_reply']['patterns']:
            if re.search(pattern, user_msg):
                return 'no_reply'

        # 技术类优先
        if any(kw in text_clean for kw in self.INTENT_RULES['tech']['keywords']):
            return 'tech'
        for pattern in self.INTENT_RULES['tech']['patterns']:
            if re.search(pattern, text_clean):
                return 'tech'

        # 价格类
        if any(kw in text_clean for kw in self.INTENT_RULES['price']['keywords']):
            return 'price'
        for pattern in self.INTENT_RULES['price']['patterns']:
            if re.search(pattern, text_clean):
                return 'price'

        return 'default'

    def _safety_filter(self, text: str) -> str:
        """安全过滤"""
        if any(p in text for p in self.BLOCKED_PHRASES):
            return self.SAFETY_MSG
        return text

    @staticmethod
    def _sanitize_text(text: str) -> str:
        """清理文本中的控制字符，保留可打印字符和常规空白"""
        return ''.join(c for c in text if c.isprintable() or c in '\n\r\t')

    def _call_ai(self, prompt: str) -> str:
        """调用本地 AI CLI 工具（claude 或 openclaw）生成回复"""
        prompt = self._sanitize_text(prompt)
        try:
            if self.cli_tool == 'claude':
                cmd = ['claude', '-p', '--max-turns', '1', prompt]
            else:
                cmd = ['openclaw', 'agent', '--prompt', prompt]

            result = subprocess.run(
                cmd,
                capture_output=True, text=True,
                timeout=60,
                env={**os.environ, 'LANG': 'zh_CN.UTF-8'}
            )

            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            else:
                logger.error(f"AI CLI 调用失败: returncode={result.returncode}, stderr={result.stderr[:200]}")
                return ""
        except subprocess.TimeoutExpired:
            logger.error("AI CLI 调用超时(60s)")
            return ""
        except Exception as e:
            logger.error(f"AI CLI 调用异常: {e}")
            return ""

    def generate_reply(self, user_msg: str, item_desc: str, context: str, bargain_count: int = 0) -> str:
        """生成回复的主入口"""
        # 1. 意图分类
        intent = self._classify_intent(user_msg)
        self.last_intent = intent
        logger.info(f"意图识别: {intent}")

        if intent == 'no_reply':
            return "-"

        # 2. 构建 prompt
        role_prompt = self.PROMPTS.get(intent, self.PROMPTS['default'])
        if intent == 'price':
            role_prompt = role_prompt.format(bargain_count=bargain_count)

        full_prompt = f"""{role_prompt}

【商品信息】
{item_desc}

【你与买家的对话历史】
{context}

【买家最新消息】
{user_msg}

请用简短的语言回复买家。要求：
- 每句不超过15字，总字数不超过50字
- 用闲鱼平台常见用语
- 不要提及微信、QQ、支付宝等站外联系方式
- 不要用感叹号和表情符号
- 直接输出回复内容，不要加任何前缀说明

回复："""

        # 3. 调用 AI
        reply = self._call_ai(full_prompt)

        if not reply:
            return "-"

        # 4. 安全过滤
        return self._safety_filter(reply)


# ============================================================
# 闲鱼 WebSocket 监控服务
# ============================================================

class XianyuMonitor:
    """闲鱼消息监控主服务"""

    def __init__(self, config: dict):
        cookies_str = config['cookie']
        self.config = config
        self.xianyu = XianyuApis()
        self.base_url = 'wss://wss-goofish.dingtalk.com/'
        self.cookies_str = cookies_str
        self.cookies = trans_cookies(cookies_str)
        self.xianyu.session.cookies.update(self.cookies)
        self.myid = self.cookies.get('unb', '')
        self.device_id = generate_device_id(self.myid)
        self.context_manager = ChatContextManager()
        self.ai = AIReplyGenerator()

        # 心跳配置
        self.heartbeat_interval = config.get('heartbeat_interval', 15)
        self.heartbeat_timeout = 5
        self.last_heartbeat_time = 0
        self.last_heartbeat_response = 0
        self.heartbeat_task = None
        self.ws = None

        # Token 刷新
        self.token_refresh_interval = 3600
        self.token_retry_interval = 300
        self.last_token_refresh_time = 0
        self.current_token = None
        self.token_refresh_task = None
        self.connection_restart_flag = False

        # 人工接管
        self.manual_mode_conversations = set()
        self.manual_mode_timeout = 3600
        self.manual_mode_timestamps = {}

        # 消息过期
        self.message_expire_time = config.get('message_expire_time', 300000)

        # 人工接管关键词（中文句号）
        self.toggle_keyword = "。"

        # 模拟打字
        self.simulate_typing = config.get('simulate_typing', False)

        if not self.myid:
            logger.error("Cookie 中未找到 unb 字段，无法识别用户 ID")
            sys.exit(1)

        logger.info(f"监控服务初始化完成，卖家 ID: {self.myid}")

    # ---------- Token 管理 ----------

    async def refresh_token(self):
        try:
            logger.info("刷新 token...")
            token_result = self.xianyu.get_token(self.device_id)
            if 'data' in token_result and 'accessToken' in token_result['data']:
                self.current_token = token_result['data']['accessToken']
                self.last_token_refresh_time = time.time()
                logger.info("Token 刷新成功")
                return self.current_token
            else:
                logger.error(f"Token 刷新失败: {token_result}")
                return None
        except Exception as e:
            logger.error(f"Token 刷新异常: {e}")
            return None

    async def token_refresh_loop(self):
        while True:
            try:
                if time.time() - self.last_token_refresh_time >= self.token_refresh_interval:
                    new_token = await self.refresh_token()
                    if new_token:
                        self.connection_restart_flag = True
                        if self.ws:
                            await self.ws.close()
                        break
                    else:
                        await asyncio.sleep(self.token_retry_interval)
                        continue
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Token 刷新循环出错: {e}")
                await asyncio.sleep(60)

    # ---------- WebSocket 通信 ----------

    async def send_msg(self, ws, cid, toid, text):
        text_payload = {
            "contentType": 1,
            "text": {"text": text}
        }
        text_base64 = base64.b64encode(
            json.dumps(text_payload).encode('utf-8')
        ).decode('utf-8')

        msg = {
            "lwp": "/r/MessageSend/sendByReceiverScope",
            "headers": {"mid": generate_mid()},
            "body": [
                {
                    "uuid": generate_uuid(),
                    "cid": f"{cid}@goofish",
                    "conversationType": 1,
                    "content": {
                        "contentType": 101,
                        "custom": {"type": 1, "data": text_base64}
                    },
                    "redPointPolicy": 0,
                    "extension": {"extJson": "{}"},
                    "ctx": {"appVersion": "1.0", "platform": "web"},
                    "mtags": {},
                    "msgReadStatusSetting": 1
                },
                {
                    "actualReceivers": [
                        f"{toid}@goofish",
                        f"{self.myid}@goofish"
                    ]
                }
            ]
        }
        await ws.send(json.dumps(msg))

    async def init_connection(self, ws):
        if not self.current_token or (time.time() - self.last_token_refresh_time) >= self.token_refresh_interval:
            await self.refresh_token()

        if not self.current_token:
            raise Exception("Token 获取失败")

        msg = {
            "lwp": "/reg",
            "headers": {
                "cache-header": "app-key token ua wv",
                "app-key": "444e9908a51d1cb236a27862abc769c9",
                "token": self.current_token,
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 DingTalk(2.1.5) OS(Windows/10) Browser(Chrome/133.0.0.0) DingWeb/2.1.5 IMPaaS DingWeb/2.1.5",
                "dt": "j",
                "wv": "im:3,au:3,sy:6",
                "sync": "0,0;0;0;",
                "did": self.device_id,
                "mid": generate_mid()
            }
        }
        await ws.send(json.dumps(msg))
        await asyncio.sleep(1)

        sync_msg = {
            "lwp": "/r/SyncStatus/ackDiff",
            "headers": {"mid": "5701741704675979 0"},
            "body": [{
                "pipeline": "sync", "tooLong2Tag": "PNM,1",
                "channel": "sync", "topic": "sync",
                "highPts": 0, "pts": int(time.time() * 1000) * 1000,
                "seq": 0, "timestamp": int(time.time() * 1000)
            }]
        }
        await ws.send(json.dumps(sync_msg))
        logger.info("WebSocket 连接注册完成")

    # ---------- 心跳 ----------

    async def send_heartbeat(self, ws):
        heartbeat_msg = {
            "lwp": "/!",
            "headers": {"mid": generate_mid()}
        }
        await ws.send(json.dumps(heartbeat_msg))
        self.last_heartbeat_time = time.time()

    async def heartbeat_loop(self, ws):
        while True:
            try:
                current = time.time()
                if current - self.last_heartbeat_time >= self.heartbeat_interval:
                    await self.send_heartbeat(ws)
                if (current - self.last_heartbeat_response) > (self.heartbeat_interval + self.heartbeat_timeout):
                    logger.warning("心跳超时，连接可能已断开")
                    break
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"心跳循环出错: {e}")
                break

    async def handle_heartbeat_response(self, data):
        if (isinstance(data, dict) and data.get("code") == 200
                and "headers" in data and "mid" in data["headers"]):
            self.last_heartbeat_response = time.time()
            return True
        return False

    # ---------- 消息判断 ----------

    @staticmethod
    def is_chat_message(message):
        try:
            return (isinstance(message, dict)
                    and "1" in message
                    and isinstance(message["1"], dict)
                    and "10" in message["1"]
                    and isinstance(message["1"]["10"], dict)
                    and "reminderContent" in message["1"]["10"])
        except Exception:
            return False

    @staticmethod
    def is_sync_package(data):
        try:
            return (isinstance(data, dict)
                    and "body" in data
                    and "syncPushPackage" in data["body"]
                    and "data" in data["body"]["syncPushPackage"]
                    and len(data["body"]["syncPushPackage"]["data"]) > 0)
        except Exception:
            return False

    @staticmethod
    def is_typing_status(message):
        try:
            return (isinstance(message, dict)
                    and "1" in message
                    and isinstance(message["1"], list)
                    and len(message["1"]) > 0
                    and isinstance(message["1"][0], dict)
                    and "1" in message["1"][0]
                    and isinstance(message["1"][0]["1"], str)
                    and "@goofish" in message["1"][0]["1"])
        except Exception:
            return False

    @staticmethod
    def is_system_message(message):
        try:
            return (isinstance(message, dict)
                    and "3" in message
                    and isinstance(message["3"], dict)
                    and message["3"].get("needPush") == "false")
        except Exception:
            return False

    @staticmethod
    def is_bracket_system_message(text):
        if not text or not isinstance(text, str):
            return False
        clean = text.strip()
        return clean.startswith('[') and clean.endswith(']')

    # ---------- 人工接管 ----------

    def is_manual_mode(self, chat_id):
        if chat_id not in self.manual_mode_conversations:
            return False
        if time.time() - self.manual_mode_timestamps.get(chat_id, 0) > self.manual_mode_timeout:
            self.manual_mode_conversations.discard(chat_id)
            self.manual_mode_timestamps.pop(chat_id, None)
            return False
        return True

    def toggle_manual_mode(self, chat_id):
        if self.is_manual_mode(chat_id):
            self.manual_mode_conversations.discard(chat_id)
            self.manual_mode_timestamps.pop(chat_id, None)
            return "auto"
        else:
            self.manual_mode_conversations.add(chat_id)
            self.manual_mode_timestamps[chat_id] = time.time()
            return "manual"

    # ---------- 商品信息 ----------

    @staticmethod
    def format_price(price):
        try:
            return round(float(price) / 100, 2)
        except (ValueError, TypeError):
            return 0.0

    def build_item_description(self, item_info):
        clean_skus = []
        for sku in item_info.get('skuList', []):
            specs = [p['valueText'] for p in sku.get('propertyList', []) if p.get('valueText')]
            clean_skus.append({
                "spec": " ".join(specs) if specs else "默认规格",
                "price": self.format_price(sku.get('price', 0)),
                "stock": sku.get('quantity', 0)
            })

        valid_prices = [s['price'] for s in clean_skus if s['price'] > 0]
        if valid_prices:
            mn, mx = min(valid_prices), max(valid_prices)
            price_display = f"¥{mn}" if mn == mx else f"¥{mn} - ¥{mx}"
        else:
            main_price = round(float(item_info.get('soldPrice', 0)), 2)
            price_display = f"¥{main_price}"

        return json.dumps({
            "title": item_info.get('title', ''),
            "desc": item_info.get('desc', ''),
            "price_range": price_display,
            "total_stock": item_info.get('quantity', 0),
            "sku_details": clean_skus
        }, ensure_ascii=False)

    # ---------- 消息处理 ----------

    async def handle_message(self, message_data, websocket):
        try:
            # 发送 ACK
            try:
                headers = message_data.get("headers", {})
                ack = {
                    "code": 200,
                    "headers": {
                        "mid": headers.get("mid", generate_mid()),
                        "sid": headers.get("sid", ""),
                    }
                }
                for key in ["app-key", "ua", "dt"]:
                    if key in headers:
                        ack["headers"][key] = headers[key]
                await websocket.send(json.dumps(ack))
            except Exception:
                pass

            if not self.is_sync_package(message_data):
                return

            sync_data = message_data["body"]["syncPushPackage"]["data"][0]
            if "data" not in sync_data:
                return

            # 解密
            data = sync_data["data"]
            try:
                decoded = base64.b64decode(data).decode("utf-8")
                json.loads(decoded)
                return  # 无需解密的消息，跳过
            except Exception:
                decrypted_data = decrypt(data)
                message = json.loads(decrypted_data)

            # 订单类消息
            try:
                reminder = message.get('3', {}).get('redReminder', '')
                if reminder in ['等待买家付款', '交易关闭', '等待卖家发货']:
                    logger.info(f"订单消息: {reminder}")
                    return
            except Exception:
                pass

            # 过滤非聊天消息
            if self.is_typing_status(message):
                return
            if not self.is_chat_message(message):
                return

            # 提取消息信息
            create_time = int(message["1"]["5"])
            send_user_name = message["1"]["10"]["reminderTitle"]
            send_user_id = message["1"]["10"]["senderUserId"]
            send_message = message["1"]["10"]["reminderContent"]

            # 过期消息
            if (time.time() * 1000 - create_time) > self.message_expire_time:
                return

            # 获取商品 ID 和会话 ID
            url_info = message["1"]["10"]["reminderUrl"]
            item_id = url_info.split("itemId=")[1].split("&")[0] if "itemId=" in url_info else None
            chat_id = message["1"]["2"].split('@')[0]

            if not item_id:
                logger.warning("无法获取商品 ID")
                return

            # 卖家自己的消息
            if send_user_id == self.myid:
                if send_message.strip() == self.toggle_keyword:
                    mode = self.toggle_manual_mode(chat_id)
                    emoji = "🔴" if mode == "manual" else "🟢"
                    logger.info(f"{emoji} 会话 {chat_id} 切换为{'人工接管' if mode == 'manual' else '自动回复'}")
                    return
                # 记录卖家人工回复
                self.context_manager.add_message_by_chat(chat_id, self.myid, item_id, "assistant", send_message)
                return

            logger.info(f"收到消息 | 买家: {send_user_name} | 商品: {item_id} | 内容: {send_message}")

            # 人工接管模式
            if self.is_manual_mode(chat_id):
                logger.info(f"🔴 会话 {chat_id} 处于人工接管模式，跳过")
                self.context_manager.add_message_by_chat(chat_id, send_user_id, item_id, "user", send_message)
                return

            # 系统消息
            if self.is_bracket_system_message(send_message):
                return
            if self.is_system_message(message):
                return

            # 获取商品信息
            item_info = self.context_manager.get_item_info(item_id)
            if not item_info:
                api_result = self.xianyu.get_item_info(item_id)
                if 'data' in api_result and 'itemDO' in api_result['data']:
                    item_info = api_result['data']['itemDO']
                    self.context_manager.save_item_info(item_id, item_info)
                else:
                    logger.warning(f"获取商品信息失败")
                    return

            item_description = self.build_item_description(item_info)

            # 获取对话上下文
            context_msgs = self.context_manager.get_context_by_chat(chat_id)
            formatted_context = "\n".join(
                f"{msg['role']}: {msg['content']}"
                for msg in context_msgs
                if msg['role'] in ['user', 'assistant']
            )

            # 获取议价次数
            bargain_count = self.context_manager.get_bargain_count_by_chat(chat_id)

            # 生成回复
            bot_reply = self.ai.generate_reply(
                send_message,
                item_description,
                formatted_context,
                bargain_count=bargain_count
            )

            if bot_reply == "-":
                logger.info(f"无需回复")
                return

            # 保存上下文
            self.context_manager.add_message_by_chat(chat_id, send_user_id, item_id, "user", send_message)

            if self.ai.last_intent == "price":
                self.context_manager.increment_bargain_count_by_chat(chat_id)

            self.context_manager.add_message_by_chat(chat_id, self.myid, item_id, "assistant", bot_reply)

            logger.info(f"回复: {bot_reply}")

            # 模拟打字延迟
            if self.simulate_typing:
                delay = min(random.uniform(0, 1) + len(bot_reply) * random.uniform(0.1, 0.3), 10.0)
                await asyncio.sleep(delay)

            await self.send_msg(websocket, chat_id, send_user_id, bot_reply)

        except Exception as e:
            logger.error(f"处理消息出错: {e}")

    # ---------- 主循环 ----------

    async def main(self):
        while True:
            try:
                self.connection_restart_flag = False
                headers = {
                    "Cookie": self.cookies_str,
                    "Host": "wss-goofish.dingtalk.com",
                    "Connection": "Upgrade",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                    "Origin": "https://www.goofish.com",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                }

                async with websockets.connect(self.base_url, extra_headers=headers) as ws:
                    self.ws = ws
                    await self.init_connection(ws)

                    self.last_heartbeat_time = time.time()
                    self.last_heartbeat_response = time.time()

                    self.heartbeat_task = asyncio.create_task(self.heartbeat_loop(ws))
                    self.token_refresh_task = asyncio.create_task(self.token_refresh_loop())

                    async for message in ws:
                        try:
                            if self.connection_restart_flag:
                                break

                            data = json.loads(message)

                            if await self.handle_heartbeat_response(data):
                                continue

                            await self.handle_message(data, ws)
                        except json.JSONDecodeError:
                            pass
                        except Exception as e:
                            logger.error(f"消息处理异常: {e}")

            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket 连接关闭")
            except Exception as e:
                logger.error(f"连接异常: {e}")
            finally:
                for task in [self.heartbeat_task, self.token_refresh_task]:
                    if task:
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass

                if self.connection_restart_flag:
                    logger.info("主动重连...")
                else:
                    logger.info("5 秒后重连...")
                    await asyncio.sleep(5)


# ============================================================
# 入口
# ============================================================

def main():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    if not os.path.exists(config_path):
        logger.error(f"配置文件不存在: {config_path}")
        logger.error("请先通过 skill 配置 Cookie")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if not config.get('cookie'):
        logger.error("配置中缺少 cookie")
        sys.exit(1)

    monitor = XianyuMonitor(config)
    asyncio.run(monitor.main())


if __name__ == '__main__':
    main()
