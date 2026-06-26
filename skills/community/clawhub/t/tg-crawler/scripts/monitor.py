"""
消息监控模块 - Telethon 实时监听 + 消息采集核心
"""
import os
import re
import asyncio
import logging
import random
from datetime import datetime

from telethon import TelegramClient, events
from telethon.errors import (
    FloodWaitError,
    ChannelPrivateError,
    InviteHashExpiredError,
    UserAlreadyParticipantError,
)
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

from config_loader import TargetsConfig, get_target_identifiers
from keyword_filter import KeywordFilter
from deduplicator import Deduplicator
from database import Database

logger = logging.getLogger(__name__)


class Monitor:
    """TG 消息监控器"""

    def __init__(
        self,
        client: TelegramClient,
        targets: TargetsConfig,
        db: Database,
        media_dir: str = "data/media",
    ):
        self.client = client
        self.targets = targets
        self.db = db
        self.media_dir = media_dir
        self.dedup = Deduplicator(cache_size=50000)
        self.keyword_filter = KeywordFilter(
            keywords=targets.global_keywords,
            rules=targets.keyword_rules,
        )
        self._running = False
        self._stats = {
            "messages_received": 0,
            "messages_matched": 0,
            "messages_saved": 0,
            "media_downloaded": 0,
            "errors": 0,
            "start_time": None,
        }

    # ------------------------------------------------------------------
    # 公开 API
    # ------------------------------------------------------------------

    async def start(self):
        """启动监控"""
        logger.info("=" * 60)
        logger.info(f"TG 爬虫启动")
        logger.info(f"目标数量: {len(self.targets.targets)}")
        logger.info(f"关键词: {self.targets.global_keywords}")
        logger.info(f"匹配模式: {self.targets.keyword_rules.logic_mode} (match: {self.targets.keyword_rules.match_mode})")
        logger.info("=" * 60)

        self._running = True
        self._stats["start_time"] = datetime.now().isoformat()

        # 1. 加入目标频道/群组
        await self._join_targets()

        # 2. 注册消息事件处理器
        target_ids = get_target_identifiers(self.targets)
        @self.client.on(events.NewMessage(chats=target_ids))
        async def handler(event: events.NewMessage.Event):
            await self._on_new_message(event)

        logger.info(f"已注册消息监听，等待新消息...")
        logger.info(f"监听目标: {len(target_ids)} 个")

        # 3. 保持运行
        while self._running:
            await asyncio.sleep(10)

    async def stop(self):
        """停止监控"""
        self._running = False
        logger.info("监控已停止")
        logger.info(f"统计: {self._stats}")

    def get_stats(self) -> dict:
        """获取运行统计"""
        return {
            **self._stats,
            "dedup": self.dedup.stats(),
        }

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    async def _join_targets(self):
        """加入所有目标频道/群组"""
        channels = []
        groups = []

        for t in self.targets.targets:
            if t.type == "channel":
                channels.append(t)
            elif t.type == "group":
                groups.append(t)

        # 加入公开频道（无限制，直接加入）
        logger.info(f"加入 {len(channels)} 个公开频道...")
        for i, ch in enumerate(channels):
            try:
                entity = await self.client.get_entity(ch.identifier)
                logger.info(f"  [{i+1}/{len(channels)}] ✅ {ch.identifier}")
                # 记录到 channel_progress（标记为已加入，供 backfill 断点续传参考）
                await self.db.set_progress(
                    chat_identifier=ch.identifier,
                    chat_title=getattr(entity, 'title', ch.note),
                    status='joined',
                )
            except FloodWaitError as e:
                wait = e.seconds + 5
                logger.warning(f"  [{i+1}/{len(channels)}] ⏳ Flood wait {wait}s, 等待中...")
                await asyncio.sleep(wait)
                try:
                    entity = await self.client.get_entity(ch.identifier)
                    logger.info(f"  [{i+1}/{len(channels)}] ✅ {ch.identifier}")
                    await self.db.set_progress(
                        chat_identifier=ch.identifier,
                        chat_title=getattr(entity, 'title', ch.note),
                        status='joined',
                    )
                except Exception as e2:
                    logger.error(f"  [{i+1}/{len(channels)}] ❌ {ch.identifier}: {e2}")
            except ChannelPrivateError:
                logger.warning(f"  [{i+1}/{len(channels)}] 🔒 {ch.identifier} (私有/不存在)")
            except Exception as e:
                logger.error(f"  [{i+1}/{len(channels)}] ❌ {ch.identifier}: {e}")
            # 频率控制
            await asyncio.sleep(random.uniform(2, 4))

        # 加入私密群组（通过邀请链接，需谨慎）
        for grp in groups:
            if not grp.invite_link:
                logger.warning(f"  ⚠️ {grp.identifier} 缺少邀请链接，跳过")
                continue
            try:
                # 提取 invite hash
                await self._join_private_group(grp.invite_link)
                logger.info(f"  ✅ 私密群组: {grp.id}")
                await self.db.set_progress(
                    chat_identifier=grp.invite_link,
                    chat_title=grp.note or grp.id,
                    status='joined',
                )
            except UserAlreadyParticipantError:
                logger.info(f"  ✅ 私密群组: {grp.id} (已加入)")
            except InviteHashExpiredError:
                logger.error(f"  ❌ 私密群组: {grp.id} (邀请链接已过期)")
            except FloodWaitError as e:
                logger.warning(f"  ⏳ 私密群组 Flood wait {e.seconds}s")
                await asyncio.sleep(e.seconds + 5)
            except Exception as e:
                logger.error(f"  ❌ 私密群组: {grp.id}: {e}")
            await asyncio.sleep(random.uniform(5, 10))

    async def _join_private_group(self, invite_link: str):
        """通过邀请链接加入私密群组"""
        # 从链接中提取 hash
        # 格式: https://t.me/+XXXXXX 或 https://t.me/joinchat/XXXXXX
        match = re.search(r'(?:joinchat/|\+)([\w-]+)', invite_link)
        if match:
            hash_value = match.group(1)
            await self.client(ImportChatInviteRequest(hash_value))
        else:
            raise ValueError(f"无法解析邀请链接: {invite_link}")

    async def _on_new_message(self, event: events.NewMessage.Event):
        """新消息事件处理"""
        self._stats["messages_received"] += 1

        try:
            message = event.message
            chat = await event.get_chat()

            chat_id = chat.id
            msg_id = message.id

            # 第一层去重：内存缓存
            if self.dedup.exists(chat_id, msg_id):
                return

            # 第二层去重：数据库
            if await self.db.message_exists(chat_id, msg_id):
                self.dedup.add(chat_id, msg_id)
                return

            # 关键词过滤
            text = message.text or message.message or ""
            matched, hit_keywords = self.keyword_filter.match(text)

            if not matched:
                return

            self._stats["messages_matched"] += 1

            # 获取发送者信息
            sender_id = None
            sender_username = None
            sender_name = None
            if message.sender_id:
                sender_id = message.sender_id
                try:
                    sender = await message.get_sender()
                    if sender:
                        sender_username = getattr(sender, 'username', None)
                        sender_name = (
                            getattr(sender, 'first_name', '')
                            + (' ' + getattr(sender, 'last_name', '') if getattr(sender, 'last_name', None) else '')
                        ).strip() or None
                except Exception:
                    pass

            # 媒体处理
            media_type = None
            media_path = None
            if message.media:
                media_type = self._get_media_type(message.media)
                if media_type:
                    media_path = await self._download_media(message, chat_id, msg_id)

            # 写入数据库
            saved = await self.db.save_message(
                msg_id=msg_id,
                chat_id=chat_id,
                chat_title=getattr(chat, 'title', None),
                chat_username=getattr(chat, 'username', None),
                sender_id=sender_id,
                sender_username=sender_username,
                sender_name=sender_name,
                text=text[:10000] if text else None,  # 限制文本长度
                media_type=media_type,
                media_path=media_path,
                msg_date=message.date.isoformat() if message.date else None,
                matched_keywords=hit_keywords,
            )

            if saved:
                self._stats["messages_saved"] += 1
                # media_files 记录已在 save_message 同一事务中写入
                logger.info(
                    f"💾 [{chat.title or chat.username}] {hit_keywords} | "
                    f"{text[:80].replace(chr(10), ' ')}..."
                )
            else:
                self.dedup.add(chat_id, msg_id)

        except FloodWaitError as e:
            logger.warning(f"⏳ Flood wait {e.seconds}s")
            await asyncio.sleep(e.seconds + random.uniform(1, 3))
        except Exception as e:
            self._stats["errors"] += 1
            logger.error(f"处理消息异常: {type(e).__name__}: {e}")

    async def _download_media(self, message, chat_id: int, msg_id: int) -> str | None:
        """下载消息中的媒体文件"""
        try:
            date_str = message.date.strftime("%Y-%m-%d") if message.date else "unknown"
            dir_path = os.path.join(self.media_dir, str(chat_id), date_str)
            os.makedirs(dir_path, exist_ok=True)

            ext = self._get_media_extension(message.media)
            file_path = os.path.join(dir_path, f"{msg_id}{ext}")

            await message.download_media(file=file_path)
            self._stats["media_downloaded"] += 1
            logger.debug(f"📎 媒体已下载: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"媒体下载失败: {e}")
            return None

    @staticmethod
    def _get_media_type(media) -> str | None:
        """判断媒体类型"""
        if isinstance(media, MessageMediaPhoto):
            return "photo"
        elif isinstance(media, MessageMediaDocument):
            doc = media.document
            if doc:
                mime = doc.mime_type or ""
                if "video" in mime:
                    return "video"
                elif "audio" in mime:
                    return "audio"
                elif "image" in mime or "gif" in mime:
                    return "image"
                else:
                    return "document"
            return "document"
        return None

    @staticmethod
    def _get_media_extension(media) -> str:
        """根据媒体类型返回文件扩展名"""
        if isinstance(media, MessageMediaPhoto):
            return ".jpg"
        elif isinstance(media, MessageMediaDocument):
            doc = media.document
            if doc:
                mime = doc.mime_type or ""
                # 尝试从原始文件名获取扩展名
                for attr in doc.attributes:
                    if hasattr(attr, 'file_name') and attr.file_name:
                        _, ext = os.path.splitext(attr.file_name)
                        return ext if ext else ".bin"
                # 从 MIME 推断
                ext_map = {
                    "video/mp4": ".mp4", "video/quicktime": ".mov",
                    "audio/mpeg": ".mp3", "audio/ogg": ".ogg",
                    "image/gif": ".gif", "image/png": ".png",
                    "image/webp": ".webp",
                }
                return ext_map.get(mime.split(";")[0], ".bin")
        return ".bin"
