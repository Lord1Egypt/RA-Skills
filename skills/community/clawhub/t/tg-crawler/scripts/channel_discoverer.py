"""
频道发现模块 - 多渠道发现 TG 频道/群组
=======================================
支持三种发现策略:
  1. TG 官方 SearchRequest API - 全局搜索关键词相关的频道/群组
  2. 搜索 Bot (xbso1/jisou) - 调用搜索 bot 获取消息级引用中的频道链接
  3. 结果去重 & 过滤

用法:
    from channel_discoverer import ChannelDiscoverer
    discoverer = ChannelDiscoverer(client)
    channels = await discoverer.discover(['无尽冬日', 'Whiteout Survival'])
"""
import asyncio
import logging
import re
from dataclasses import dataclass, field
from typing import Optional

from telethon import TelegramClient
from telethon.tl.functions.contacts import SearchRequest
from telethon.errors import FloodWaitError, ChatWriteForbiddenError
from telethon.tl.types import Channel, Chat

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredChannel:
    """发现的频道/群组"""
    username: str           # 如 "wujindongri6"
    title: str              # 如 "无尽冬日最新国际服17代总群"
    chat_type: str          # "group" / "channel" / "bot"
    member_count: Optional[int] = None  # 成员数（SearchRequest 可返回）
    source: str = ""        # 发现来源: "tg_search" / "xbso1" / "jisou"
    invite_link: Optional[str] = None   # 如果有邀请链接
    confidence: float = 1.0  # 置信度 (0-1)，TG API 结果置信度最高


class ChannelDiscoverer:
    """多渠道频道发现器"""

    # 内置的搜索 Bot 列表（已知可用且有效的）
    SEARCH_BOTS = [
        {
            "username": "xbso1",
            "name": "新币搜 (xbso1)",
            "priority": 1,  # 最先调用，覆盖最广
        },
        {
            "username": "jisou",
            "name": "极搜 (jisou)",
            "priority": 2,  # 互补覆盖
        },
    ]

    def __init__(self, client: TelegramClient):
        self.client = client

    # ------------------------------------------------------------------
    # 公开 API
    # ------------------------------------------------------------------

    async def discover(self, keywords: list[str]) -> list[DiscoveredChannel]:
        """
        多路发现频道/群组

        流程:
          1. TG SearchRequest API 搜索 → 获取主题群组（置信度高）
          2. 搜索 Bot 调用 → 获取消息级引用中的频道（覆盖面广）
          3. 去重合并
          4. 按置信度排序

        Args:
            keywords: 搜索关键词列表，如 ['无尽冬日', 'Whiteout Survival']

        Returns:
            去重后的频道列表
        """
        all_channels: dict[str, DiscoveredChannel] = {}  # key=username (去重)

        # 策略1: TG 官方 SearchRequest
        logger.info("🔄 策略1: TG 官方 SearchRequest 搜索...")
        for kw in keywords:
            try:
                channels = await self._discover_via_tg_search(kw)
                for ch in channels:
                    key = ch.username.lower() if ch.username else ch.title.lower()
                    if key and key not in all_channels:
                        all_channels[key] = ch
                logger.info(f"  ✅ SearchRequest('{kw}') → {len(channels)} 个")
            except FloodWaitError as e:
                logger.warning(f"  ⏳ Flood wait {e.seconds}s for '{kw}'")
                await asyncio.sleep(e.seconds + 2)
            except Exception as e:
                logger.error(f"  ❌ SearchRequest('{kw}'): {type(e).__name__}: {e}")
            await asyncio.sleep(1.5)  # 关键词间间隔

        # 策略2: 搜索 Bot 调用
        logger.info("🔄 策略2: 搜索 Bot 调用...")
        for bot in sorted(self.SEARCH_BOTS, key=lambda b: b["priority"]):
            try:
                channels = await self._discover_via_search_bot(
                    bot["username"], keywords
                )
                new_count = 0
                for ch in channels:
                    key = ch.username.lower() if ch.username else ch.title.lower()
                    if key and key not in all_channels and key not in ('xbso1', 'jisou', 'xbso2', 'jisou2'):
                        all_channels[key] = ch
                        new_count += 1
                logger.info(f"  ✅ {bot['name']} → {len(channels)} 个引用 (新增 {new_count})")
            except FloodWaitError as e:
                logger.warning(f"  ⏳ {bot['name']} Flood wait {e.seconds}s")
                await asyncio.sleep(e.seconds + 5)
            except ChatWriteForbiddenError:
                logger.warning(f"  ⚠️ {bot['name']} 禁止私聊，跳过")
            except Exception as e:
                logger.error(f"  ❌ {bot['name']}: {type(e).__name__}: {e}")
            await asyncio.sleep(3)  # bot 间间隔

        # 排序：置信度降序
        result = sorted(all_channels.values(), key=lambda c: -c.confidence)

        logger.info(f"🎯 频道发现完成: 共 {len(result)} 个唯一频道")
        for ch in result:
            members = f" ({ch.member_count}人)" if ch.member_count else ""
            logger.info(f"    [{ch.chat_type}] {ch.title} @{ch.username}{members} 来源: {ch.source}")

        return result

    async def discover_only_tg_api(self, keywords: list[str]) -> list[DiscoveredChannel]:
        """
        仅使用 TG 官方 SearchRequest 发现频道（轻量模式）
        """
        all_channels: dict[str, DiscoveredChannel] = {}
        for kw in keywords:
            try:
                channels = await self._discover_via_tg_search(kw)
                for ch in channels:
                    key = ch.username.lower() if ch.username else ch.title.lower()
                    if key and key not in all_channels:
                        all_channels[key] = ch
            except Exception as e:
                logger.warning(f"SearchRequest('{kw}'): {type(e).__name__}")
            await asyncio.sleep(1.5)
        return sorted(all_channels.values(), key=lambda c: -c.confidence)

    async def discover_only_bots(self, keywords: list[str]) -> list[DiscoveredChannel]:
        """
        仅通过搜索 Bot 发现频道
        """
        all_channels: dict[str, DiscoveredChannel] = {}
        for bot in sorted(self.SEARCH_BOTS, key=lambda b: b["priority"]):
            try:
                channels = await self._discover_via_search_bot(bot["username"], keywords)
                for ch in channels:
                    key = ch.username.lower() if ch.username else ch.title.lower()
                    if key and key not in all_channels:
                        all_channels[key] = ch
            except Exception as e:
                logger.warning(f"{bot['name']}: {type(e).__name__}")
            await asyncio.sleep(3)
        return sorted(all_channels.values(), key=lambda c: -c.confidence)

    # ------------------------------------------------------------------
    # 策略实现
    # ------------------------------------------------------------------

    async def _discover_via_tg_search(self, keyword: str) -> list[DiscoveredChannel]:
        """
        策略1: TG 官方 contacts.SearchRequest
        返回的是真实的频道/群组实体，有成员数、类型等完整元信息
        """
        result = await self.client(SearchRequest(q=keyword, limit=30))
        channels = []

        for chat in result.chats:
            title = getattr(chat, 'title', '') or getattr(chat, 'first_name', '') or ''
            username = getattr(chat, 'username', '') or ''
            is_bot = getattr(chat, 'bot', False)
            is_broadcast = getattr(chat, 'broadcast', False)  # 频道
            is_megagroup = getattr(chat, 'megagroup', False)   # 超级群组
            member_count = getattr(chat, 'participants_count', None)

            # 跳过 bot
            if is_bot:
                continue

            chat_type = "channel" if is_broadcast else ("group" if is_megagroup else "unknown")

            # 构建邀请链接（私密群组需要）
            invite_link = None
            if not username and hasattr(chat, 'id'):
                invite_link = f"https://t.me/c/{chat.id}/1"  # 仅作标记，不一定能加入

            channels.append(DiscoveredChannel(
                username=username,
                title=title,
                chat_type=chat_type,
                member_count=member_count,
                source="tg_search",
                invite_link=invite_link,
                confidence=0.95,  # TG API 高置信度
            ))

        return channels

    async def _discover_via_search_bot(
        self, bot_username: str, keywords: list[str]
    ) -> list[DiscoveredChannel]:
        """
        策略2: 调用搜索 Bot
        向 bot 发送关键词 → 解析返回的 t.me 链接 → 提取频道
        """
        channels = []
        seen_links = set()

        for kw in keywords:
            try:
                # 发送关键词
                await self.client.send_message(bot_username, kw)
                # 等待 bot 处理并回复
                await asyncio.sleep(3)

                # 获取 bot 最近的消息（含搜索结果）
                replies = await self.client.get_messages(bot_username, limit=5)

                for msg in replies:
                    text = msg.text or ""
                    # 跳过自己发的关键词回显
                    if text.strip() == kw:
                        continue

                    # 提取 t.me/xxx 链接
                    raw_links = re.findall(r't\.me/([a-zA-Z0-9_+]+)', text)
                    for link in raw_links:
                        if link in seen_links or link.startswith('+'):
                            continue
                        seen_links.add(link)

                        ch = self._parse_channel_from_link(link, bot_username)
                        if ch:
                            channels.append(ch)
            except Exception as e:
                logger.debug(f"Bot {bot_username} kw='{kw}': {type(e).__name__}")
                continue

            # Bot 调用间短暂间隔
            await asyncio.sleep(1)

        return channels

    def _parse_channel_from_link(
        self, link: str, source_bot: str
    ) -> Optional[DiscoveredChannel]:
        """
        从 t.me 链接片段还原频道信息
        link 格式:
          - username: "shouyou126"  (频道/群组)
          - msg_ref: "yxqzy/244"    (频道 + 消息ID)
          - invite: "+ABC123..."    (邀请链接)
        """
        # 去除片段后的空格/标点（rstrip 参数是字符集合）
        link = link.strip().rstrip(')】.')

        # 私密群组邀请链接
        if link.startswith('+'):
            return DiscoveredChannel(
                username="",
                title=f"私密群组 ({link[:12]}...)",
                chat_type="group",
                source=source_bot,
                invite_link=f"https://t.me/{link}",
                confidence=0.3,  # 低置信度（可能无法加入）
            )

        # 消息引用: "yxqzy/244" → 取频道部分
        if '/' in link:
            parts = link.split('/')
            username = parts[0]
            if username.startswith('+'):
                return DiscoveredChannel(
                    username="",
                    title=f"私密群组 ({username[:12]}...)",
                    chat_type="group",
                    source=source_bot,
                    invite_link=f"https://t.me/{username}",
                    confidence=0.3,
                )
            # 非 invite 的消息引用场景，继续用 username 走下去
        else:
            username = link

        # 过滤搜索 bot 自身的引用
        if username.lower() in ('xbso1', 'xbso2', 'jisou', 'jisou2', 'jisou1bot'):
            return None

        # 过滤明显是 user 的短链接
        if len(username) <= 3 and not username.startswith('+'):
            return None

        return DiscoveredChannel(
            username=username,
            title=username,  # 标题稍后通过 get_entity 获取
            chat_type="unknown",  # 稍后确认
            source=source_bot,
            confidence=0.6,  # Bot 搜索结果置信度中等
        )
