#!/usr/bin/env python3
"""
QQ 官方机器人 - WebSocket 连接示例
完整功能实现，可直接运行
"""
import asyncio
import json
import websockets
import requests
import aiohttp
from datetime import datetime
from pathlib import Path

# ========== 配置 ==========
APP_ID = "你的AppID"           # 替换为你的 AppID
APP_SECRET = "你的AppSecret"   # 替换为你的 AppSecret

# API 地址
TOKEN_URL = "https://bots.qq.com/app/getAppAccessToken"
GATEWAY_URL = "https://api.sgroup.qq.com/gateway"
API_BASE = "https://api.sgroup.qq.com"

# 订阅的事件意图 (INTENTS)
# 参考: https://bot.q.qq.com/wiki/develop/api/gateway/intents.html
# GUILDS (1 << 0) - 基础权限
# GUILD_MEMBERS (1 << 1) - 成员变更
# GUILD_MESSAGES (1 << 9) - 频道消息
# DIRECT_MESSAGE (1 << 12) - 私信
# GROUP_AND_C2C_EVENT (1 << 25) - 群和 C2C 事件
# AT_MESSAGES (1 << 30) - @消息
# 注意: C2C_MESSAGE_CREATE 包含在 GROUP_AND_C2C_EVENT (1<<25) 中
INTENTS = (1 << 0) | (1 << 25) | (1 << 30)

class QQOfficialBot:
    """QQ 官方机器人"""
    
    def __init__(self):
        self.token = None
        self.ws = None
        self.session_id = None
        self.seq = 0
        self.heartbeat_interval = 41250  # 心跳间隔（毫秒）
        self.heartbeat_task = None
    
    def get_access_token(self):
        """获取 Access Token"""
        payload = {
            "appId": APP_ID,
            "clientSecret": APP_SECRET
        }
        try:
            response = requests.post(TOKEN_URL, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                expires_in = data.get("expires_in", 0)
                print(f"✅ Access Token 获取成功")
                print(f"   有效期: {expires_in} 秒")
                return self.token
            else:
                print(f"❌ 获取 Token 失败: {response.status_code}")
                print(f"   响应: {response.text}")
                # 检查是否是 IP 白名单错误
                if "11298" in response.text:
                    print("\n⚠️ 错误 11298: IP 不在白名单")
                    print("   请访问 https://bot.q.qq.com/console/ 更新 IP 白名单")
                return None
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None
    
    async def connect(self):
        """建立 WebSocket 连接"""
        # 1. 获取 WebSocket 地址
        headers = {"Authorization": f"QQBot {self.token}"}
        try:
            response = requests.get(GATEWAY_URL, headers=headers)
            if response.status_code != 200:
                print(f"❌ 获取 Gateway 失败: {response.text}")
                return False
            
            gateway = response.json().get("url")
            print(f"📡 Gateway 地址: {gateway}")
        except Exception as e:
            print(f"❌ 获取 Gateway 异常: {e}")
            return False
        
        # 2. 连接 WebSocket
        try:
            self.ws = await websockets.connect(gateway)
            print("✅ WebSocket 连接成功")
            
            # 3. 处理消息循环
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    await self.handle_message(data)
                except json.JSONDecodeError:
                    print(f"⚠️ 收到非 JSON 消息: {message}")
                except Exception as e:
                    print(f"❌ 处理消息异常: {e}")
                    
        except websockets.exceptions.ConnectionClosed as e:
            print(f"⚠️ WebSocket 连接关闭: {e}")
            return False
        except Exception as e:
            print(f"❌ WebSocket 异常: {e}")
            return False
        
        return True
    
    async def handle_message(self, data):
        """处理 WebSocket 消息"""
        op = data.get("op")
        
        # OP Code 说明:
        # 0 = Dispatch (服务端主动推送)
        # 10 = Hello (连接成功后发送)
        # 11 = Heartbeat ACK (心跳确认)
        
        if op == 10:  # Hello
            interval = data.get("d", {}).get("heartbeat_interval", 41250)
            self.heartbeat_interval = interval
            print(f"💓 心跳间隔: {interval}ms")
            
            # 启动心跳
            self.heartbeat_task = asyncio.create_task(self.heartbeat_loop())
            
            # 发送鉴权
            await self.identify()
        
        elif op == 11:  # Heartbeat ACK
            print("💓 心跳确认")
        
        elif op == 0:  # Dispatch
            self.seq = data.get("s", 0)
            event_type = data.get("t")
            payload = data.get("d", {})
            
            await self.handle_event(event_type, payload)
    
    async def handle_event(self, event_type, payload):
        """处理业务事件"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 打印所有收到的事件（用于调试）
        print(f"[{timestamp}] 📨 收到事件: {event_type}")
        
        if event_type == "READY":
            # 鉴权成功
            self.session_id = payload.get("session_id")
            user = payload.get("user", {})
            print(f"\n{'='*50}")
            print(f"✅ 鉴权成功!")
            print(f"   Session ID: {self.session_id}")
            print(f"   Bot 名称: {user.get('username')}")
            print(f"   Bot ID: {user.get('id')}")
            print(f"{'='*50}\n")
        
        elif event_type == "RESUMED":
            # 会话恢复成功
            print(f"✅ 会话恢复成功")
        
        elif event_type == "AT_MESSAGE_CREATE":
            # 收到 @ 消息
            await self.handle_at_message(payload)
        
        elif event_type == "C2C_MESSAGE_CREATE":
            # 收到私聊消息
            await self.handle_c2c_message(payload)
        
        elif event_type == "GROUP_AT_MESSAGE_CREATE":
            # 收到群 @ 消息
            await self.handle_group_at_message(payload)
        
        elif event_type == "MESSAGE_CREATE":
            # 收到普通消息（需要特定权限）
            print(f"[{timestamp}] 收到消息: {payload.get('content', '')}")
        
        elif event_type == "GUILD_MEMBER_ADD":
            # 新成员加入频道
            member = payload.get("user", {})
            print(f"[{timestamp}] 新成员加入: {member.get('username')}")
        
        else:
            print(f"[{timestamp}] 未处理事件: {event_type}")
    
    async def handle_at_message(self, message):
        """处理 @ 消息"""
        content = message.get("content", "").strip()
        author = message.get("author", {})
        channel_id = message.get("channel_id")
        guild_id = message.get("guild_id")
        msg_id = message.get("id")
        
        # 去除 @ 标记
        # QQ 官方消息格式: <@!123456789> 实际内容
        import re
        content = re.sub(r'<@!\d+>', '', content).strip()
        
        print(f"\n📩 [{datetime.now().strftime('%H:%M:%S')}] 收到 @ 消息")
        print(f"   来自: {author.get('username')} ({author.get('id')})")
        print(f"   频道: {guild_id}")
        print(f"   内容: {content}")
        
        # 处理命令或回复
        reply_content = self.generate_reply(content, author)
        
        # 发送回复
        await self.send_reply(channel_id, msg_id, reply_content)
    
    def generate_reply(self, content, author):
        """生成回复内容"""
        username = author.get('username', '用户')
        
        # 简单命令处理
        if content.lower() in ['help', '帮助', '菜单']:
            return f"""@{username} 
🤖 可用命令:
/help - 显示帮助
/hello - 打招呼
/time - 查看时间
/ping - 测试延迟
直接输入文字可与 AI 对话"""
        
        elif content.lower() in ['hello', 'hi', '你好']:
            return f"@{username} 你好! 👋 有什么可以帮你的吗?"
        
        elif content.lower() in ['time', '时间']:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"@{username} 当前时间: {now}"
        
        elif content.lower() == 'ping':
            return f"@{username} Pong! 🏓"
        
        else:
            # 调用 OpenClaw AI 处理
            return self.call_openclaw_ai(content, username, author.get('id', 'unknown'))
    
    def call_openclaw_ai(self, message, username, user_id):
        """调用 OpenClaw AI 处理消息"""
        import uuid
        import time
        request_id = str(uuid.uuid4())[:8]
        
        # 写入请求文件
        request_file = Path.home() / ".openclaw" / "workspace" / "qq_queue" / f"ai_request_{request_id}.json"
        response_file = Path.home() / ".openclaw" / "workspace" / "qq_queue" / f"ai_response_{request_id}.txt"
        
        request_data = {
            "request_id": request_id,
            "user_id": user_id,
            "username": username,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        # 确保目录存在
        request_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(request_file, "w", encoding="utf-8") as f:
            json.dump(request_data, f, ensure_ascii=False, indent=2)
        
        print(f"🤖 AI 请求已发送: {request_file.name}")
        print(f"⏳ 等待 OpenClaw AI 回复...")
        
        # 等待 OpenClaw 回复（最多 30 秒）
        for i in range(30):
            if response_file.exists():
                with open(response_file, "r", encoding="utf-8") as f:
                    reply = f.read()
                # 清理文件
                try:
                    response_file.unlink()
                    request_file.unlink()
                except:
                    pass
                print(f"✅ 收到 AI 回复: {reply[:50]}...")
                return f"@{username}\n{reply}"
            time.sleep(1)
        
        # 超时，清理文件
        try:
            if request_file.exists():
                request_file.unlink()
        except:
            pass
        return f"@{username} 抱歉，AI 响应超时，请稍后再试"
    
    async def send_reply(self, channel_id, msg_id, content):
        """发送回复消息"""
        url = f"{API_BASE}/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"QQBot {self.token}",
            "Content-Type": "application/json"
        }
        
        # 使用 msg_id 引用回复
        payload = {
            "content": content,
            "msg_id": msg_id  # 引用原消息
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        print(f"✅ 回复发送成功")
                    else:
                        error_text = await resp.text()
                        print(f"❌ 发送失败 ({resp.status}): {error_text}")
        except Exception as e:
            print(f"❌ 发送异常: {e}")
    
    async def handle_c2c_message(self, message):
        """处理私聊消息"""
        content = message.get("content", "").strip()
        author = message.get("author", {})
        user_id = author.get("id")
        msg_id = message.get("id")
        
        print(f"\n📩 [{datetime.now().strftime('%H:%M:%S')}] 收到私聊消息")
        print(f"   来自: {author.get('username')} ({user_id})")
        print(f"   内容: {content}")
        
        # 生成回复
        reply_content = self.generate_reply(content, author)
        
        # 发送私聊回复
        await self.send_private_reply(user_id, msg_id, reply_content)
    
    async def handle_group_at_message(self, message):
        """处理群 @ 消息"""
        content = message.get("content", "").strip()
        author = message.get("author", {})
        group_id = message.get("group_id")
        msg_id = message.get("id")
        
        # 去除 @ 标记
        import re
        content = re.sub(r'<@!\d+>', '', content).strip()
        
        print(f"\n📩 [{datetime.now().strftime('%H:%M:%S')}] 收到群 @ 消息")
        print(f"   来自: {author.get('username')} ({author.get('id')})")
        print(f"   群号: {group_id}")
        print(f"   内容: {content}")
        
        # 生成回复
        reply_content = self.generate_reply(content, author)
        
        # 发送群回复
        await self.send_group_reply(group_id, msg_id, reply_content)
    
    async def send_private_reply(self, user_id, msg_id, content):
        """发送私聊回复"""
        url = f"{API_BASE}/v2/users/{user_id}/messages"
        headers = {
            "Authorization": f"QQBot {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "content": content,
            "msg_id": msg_id
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        print(f"✅ 私聊回复发送成功")
                    else:
                        error_text = await resp.text()
                        print(f"❌ 私聊回复发送失败 ({resp.status}): {error_text}")
        except Exception as e:
            print(f"❌ 私聊回复发送异常: {e}")
    
    async def send_group_reply(self, group_id, msg_id, content):
        """发送群回复"""
        url = f"{API_BASE}/v2/groups/{group_id}/messages"
        headers = {
            "Authorization": f"QQBot {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "content": content,
            "msg_id": msg_id
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        print(f"✅ 群回复发送成功")
                    else:
                        error_text = await resp.text()
                        print(f"❌ 群回复发送失败 ({resp.status}): {error_text}")
        except Exception as e:
            print(f"❌ 群回复发送异常: {e}")
    
    async def identify(self):
        """发送鉴权消息"""
        payload = {
            "op": 2,  # Identify
            "d": {
                "token": f"QQBot {self.token}",
                "intents": INTENTS,
                "shard": [0, 1],  # [当前分片, 总分片数]
                "properties": {
                    "$os": "windows",
                    "$browser": "openclaw-bot",
                    "$device": "openclaw-bot"
                }
            }
        }
        await self.ws.send(json.dumps(payload))
        print("🔑 鉴权消息已发送...")
    
    async def heartbeat_loop(self):
        """心跳循环"""
        while True:
            await asyncio.sleep(self.heartbeat_interval / 1000)
            
            if not self.ws or self.ws.state.name != 'OPEN':
                break
            
            payload = {
                "op": 1,  # Heartbeat
                "d": self.seq if self.seq > 0 else None
            }
            try:
                await self.ws.send(json.dumps(payload))
            except Exception as e:
                print(f"⚠️ 心跳发送失败: {e}")
                break
    
    async def run(self):
        """运行机器人"""
        print("🤖 QQ 官方机器人启动中...")
        print(f"   App ID: {APP_ID}")
        print(f"   订阅事件: AT_MESSAGE_CREATE, C2C_MESSAGE_CREATE, GROUP_AT_MESSAGE_CREATE")
        print()
        
        # 获取 Token
        if not self.get_access_token():
            print("❌ 启动失败: 无法获取 Access Token")
            return
        
        # 连接 WebSocket
        while True:
            success = await self.connect()
            if not success:
                print("⚠️ 5 秒后重连...")
                await asyncio.sleep(5)
            else:
                # 连接断开，尝试重连
                print("⚠️ 连接断开，尝试重连...")
                await asyncio.sleep(5)

# ========== 运行 ==========
if __name__ == "__main__":
    # 检查配置
    if APP_ID == "你的AppID" or APP_SECRET == "你的AppSecret":
        print("❌ 请先编辑脚本，填入你的 AppID 和 AppSecret")
        exit(1)
    
    bot = QQOfficialBot()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n👋 机器人已停止")
    except Exception as e:
        print(f"❌ 运行异常: {e}")
