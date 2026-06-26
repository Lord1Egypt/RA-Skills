#!/usr/bin/env python3
"""
TG 爬虫 - 主入口
========================
基于 Telethon 的 Telegram 频道/群组消息监控爬虫。

用法:
    # 实时监控模式（默认）
    python main.py

    # 历史消息回溯模式
    python main.py --backfill --backfill-limit 500

    # 指定配置路径
    python main.py --targets ../data/targets.yaml --env .env

环境变量 (.env):
    TG_API_ID     - Telegram API ID (从 my.telegram.org 获取)
    TG_API_HASH   - Telegram API Hash
    TG_PHONE      - 账号手机号 (+86xxx)
    PROXY_HOST    - SOCKS5 代理地址（可选）
    PROXY_PORT    - SOCKS5 代理端口（可选）
"""
import os
import sys
import asyncio
import logging
import argparse
import signal
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChannelPrivateError

from config_loader import load_targets, get_target_identifiers
from database import Database
from monitor import Monitor


# ------------------------------------------------------------------
# 日志配置
# ------------------------------------------------------------------

def setup_logging(level: str = "INFO"):
    """配置日志格式"""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # 降低第三方库日志级别
    logging.getLogger("telethon").setLevel(logging.WARNING)


# ------------------------------------------------------------------
# 环境检测
# ------------------------------------------------------------------

def check_dependencies():
    """检查依赖是否安装"""
    missing = []
    for pkg in ["telethon", "yaml", "aiosqlite", "dotenv"]:
        try:
            __import__("dotenv" if pkg == "dotenv" else pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        print(f"   请运行: pip install -r requirements.txt")
        sys.exit(1)


# ------------------------------------------------------------------
# 主逻辑
# ------------------------------------------------------------------

async def run_monitor(
    client: TelegramClient,
    targets_path: str,
    db_path: str,
    media_dir: str,
):
    """运行实时监控模式"""
    db = Database(db_path)
    await db.init()

    try:
        targets = load_targets(targets_path)
        monitor = Monitor(
            client=client,
            targets=targets,
            db=db,
            media_dir=media_dir,
        )
        await monitor.start()
    finally:
        await db.close()


async def run_export(
    db_path: str,
    output: str,
    format: str = "csv",
    since: str | None = None,
    until: str | None = None,
    chats: list[str] | None = None,
) -> int:
    """导出数据库消息到文件"""
    db = Database(db_path)
    await db.init()
    try:
        count = await db.export_messages(
            output_path=output,
            format=format,
            since=since,
            until=until,
            chat_usernames=chats,
        )
        return count
    finally:
        await db.close()


async def run_backfill(
    client: TelegramClient,
    targets_path: str,
    db_path: str,
    media_dir: str,
    limit: int = 500,
    keywords: list[str] | None = None,
    resume: bool = True,
    fetch_sender: bool = False,
    sender_batch_size: int = 15,
    sender_batch_delay: float = 3.0,
):
    """运行历史消息回溯模式"""
    from keyword_filter import KeywordFilter

    db = Database(db_path)
    await db.init()

    try:
        targets = load_targets(targets_path)
        filter_keywords = keywords if keywords else targets.global_keywords
        keyword_filter = KeywordFilter(
            keywords=filter_keywords,
            rules=targets.keyword_rules,
        )

        total_saved = 0
        identifiers = get_target_identifiers(targets)

        total_saved = await _backfill_channels(
            client, keyword_filter, identifiers, limit, db,
            resume=resume,
            fetch_sender=fetch_sender,
            sender_batch_size=sender_batch_size,
            sender_batch_delay=sender_batch_delay,
        )

        logging.info(f"回溯完成，共保存 {total_saved} 条消息")
    finally:
        await db.close()


async def _backfill_channels(
    client: TelegramClient,
    keyword_filter,
    identifiers: list[str],
    limit: int,
    db: "Database",
    resume: bool = True,
    title_filter_keywords: list[str] | None = None,
    new_identifiers: set[str] | None = None,
    fetch_sender: bool = False,
    sender_batch_size: int = 15,
    sender_batch_delay: float = 3.0,
) -> int:
    """回溯指定频道列表，返回保存的消息数。
    
    Args:
        resume: 是否启用断点续传（跳过已完成频道）
        title_filter_keywords: 新频道 title 二次过滤关键词，应用 discover 的生态词，而非 backfill 品牌词
        new_identifiers: 新发现频道的 identifier 集合（不在集合中的频道不参与二次过滤）
        fetch_sender: 是否获取发送者信息（默认 False，避免 Flood Wait）
        sender_batch_size: 每批获取发送者数量
        sender_batch_delay: 批次间延迟秒数
    """
    from sender_cache import SenderCache

    total_saved = 0
    cache = SenderCache(client) if fetch_sender else None

    # 断点续传：跳过已完成/已跳过/已私有化的频道，但重试 rate_limited/partial
    if resume:
        done = await db.get_all_progress()
        retry_statuses = {'rate_limited', 'partial'}
        pending = [
            ident for ident in identifiers
            if ident not in done or done[ident].get('status') in retry_statuses
        ]
        retried = sum(1 for ident in pending if ident in done and done[ident].get('status') in retry_statuses)
        skipped = len(identifiers) - len(pending)
        if skipped > 0:
            logging.info(f"🔄 断点续传: {len(pending)} 个待回溯, {skipped} 个已跳过")
        if retried > 0:
            logging.info(f"   🔄 其中 {retried} 个为之前限速/部分完成的，重新回溯")
        identifiers = pending

    for identifier in identifiers:
        logging.info(f"回溯: {identifier} (limit={limit})")

        # get_entity 重试包装器：短 FloodWait 自动重试
        entity = None
        get_entity_error = None
        for g_retry in range(2):
            try:
                entity = await client.get_entity(identifier)
                break
            except FloodWaitError as e:
                get_entity_error = e
                if e.seconds < 60 and g_retry == 0:
                    logging.info(f"  ⏳ {identifier} get_entity FloodWait {e.seconds}s, 等待后重试...")
                    await asyncio.sleep(e.seconds + 2)
                else:
                    break
            except ChannelPrivateError as e:
                get_entity_error = e
                break
            except Exception as e:
                get_entity_error = e
                break

        if entity is None:
            if isinstance(get_entity_error, FloodWaitError):
                logging.warning(f"  ⏳ {identifier} 被限速 {get_entity_error.seconds}s (>60s 或重试失败), 标记 rate_limited")
                if resume:
                    await db.set_progress(chat_identifier=identifier, status='rate_limited')
            elif isinstance(get_entity_error, ChannelPrivateError):
                logging.warning(f"  🔒 {identifier} 频道已私有化，跳过")
                if resume:
                    await db.set_progress(chat_identifier=identifier, status='private')
            else:
                logging.error(f"  回溯 {identifier} 失败: {get_entity_error}")
                if resume:
                    await db.set_progress(chat_identifier=identifier, status='failed')
            continue

        # 搜索 Bot 结果二次过滤：对新发现频道，用 title 做相关性检查
        # 利用 get_entity 获取的 title，避免对无关频道做 iter_messages（节省 API 配额）
        if title_filter_keywords and new_identifiers and identifier in new_identifiers:
            entity_title = getattr(entity, 'title', '') or ''
            if entity_title:
                title_lower = entity_title.lower()
                matched_title = any(kw.lower() in title_lower for kw in title_filter_keywords)
                if not matched_title:
                    logging.info(f"  ⏭️ 跳过 (title 不匹配): {entity_title}")
                    if resume:
                        await db.set_progress(
                            chat_identifier=identifier,
                            chat_title=entity_title,
                            status='skipped',
                        )
                    continue
                logging.info(f"  ✅ title 命中: {entity_title}")

        try:
            async for msg in client.iter_messages(
                entity,
                limit=limit,
                wait_time=2,
            ):
                text = msg.text or msg.message or ""
                matched, hit_keywords = keyword_filter.match(text)
                if not matched:
                    continue

                media_type = None
                media_path = None
                if msg.media:
                    media_type = Monitor._get_media_type(msg.media)

                # 获取发送者信息（优先缓存，避免 Flood Wait）
                sender_id = msg.sender_id
                sender_username, sender_name = None, None
                if sender_id and cache:
                    sender_username, sender_name = cache.get(sender_id)
                    if sender_username is None and sender_name is None:
                        # 缓存未命中，标记为待获取（延迟批量补充）
                        cache.mark_pending(sender_id)

                saved = await db.save_message(
                    msg_id=msg.id,
                    chat_id=entity.id,
                    chat_title=getattr(entity, 'title', None),
                    chat_username=getattr(entity, 'username', None),
                    sender_id=sender_id,
                    sender_username=sender_username,
                    sender_name=sender_name,
                    text=text[:10000] if text else None,
                    media_type=media_type,
                    media_path=media_path,
                    msg_date=msg.date.isoformat() if msg.date else None,
                    matched_keywords=hit_keywords,
                )
                if saved:
                    total_saved += 1
                    # media_files 记录已在 save_message 同一事务中写入
                    logging.info(f"  💾 [{entity.title or identifier}] {hit_keywords}")

                await asyncio.sleep(1.5)
        except FloodWaitError as e:
            logging.warning(f"  ⏳ 回溯 {identifier} Flood Wait {e.seconds}s, 已保存 {total_saved} 条")
            await asyncio.sleep(e.seconds + 5)
            # 标记部分完成，下次 --resume 继续
            if resume:
                await db.set_progress(
                    chat_identifier=identifier,
                    chat_title=getattr(entity, 'title', None),
                    status='partial',
                )
            continue

        # 频道回溯完成后，批量补充发送者信息
        if cache and cache.has_pending():
            pending = cache.pending_count()
            logging.info(f"  🔄 补充发送者信息: {pending} 个待获取 (batch={sender_batch_size}, delay={sender_batch_delay}s)")
            try:
                await cache.fetch_all_pending(
                    batch_size=sender_batch_size,
                    batch_delay=sender_batch_delay,
                )
                # 更新数据库中的 sender 信息
                await db.update_senders_batch(cache)
            except Exception as e:
                logging.warning(f"  ⚠️ 补充发送者信息失败: {e}")

        # 回溯完成，记录进度（即使 0 命中也标记为 done，避免重复回溯）
        if resume:
            await db.set_progress(
                chat_identifier=identifier,
                chat_title=getattr(entity, 'title', None),
                status='done',
            )
    return total_saved


async def run_discover(
    client: TelegramClient,
    targets_path: str,
    keywords: list[str],
    disable_bots: bool = False,
):
    """运行频道发现模式（仅发现，不回溯不监控）"""
    from channel_discoverer import ChannelDiscoverer

    discoverer = ChannelDiscoverer(client)

    if disable_bots:
        channels = await discoverer.discover_only_tg_api(keywords)
    else:
        channels = await discoverer.discover(keywords)

    # 追加到 targets.yaml
    added = 0
    if channels:
        new_targets = []
        for ch in channels:
            if ch.username and ch.username not in ('xbso1', 'jisou', 'xbso2', 'jisou2'):
                new_targets.append({
                    "identifier": ch.username,
                    "title": ch.title,
                    "type": ch.chat_type if ch.chat_type != "unknown" else "channel",
                    "note": f"自动发现: {ch.source} | {ch.title}",
                    "invite_link": ch.invite_link,
                })

        from config_loader import add_targets
        # 自动分类模式：根据频道内容写入对应行业文件
        n = add_targets("auto", new_targets)
        logging.info(f"✅ 已将 {n} 个新频道按行业分类追加到对应 targets 文件")
        added = n

    logging.info(f"发现完成: {len(channels)} 个频道, 新增 {added} 个")
    return channels


async def run_hybrid(
    client: TelegramClient,
    targets_path: str,
    db_path: str,
    media_dir: str,
    keywords: list[str],
    backfill_keywords: list[str] | None = None,
    limit: int = 500,
    disable_bots: bool = False,
    backfill_filter: bool = True,
    resume: bool = True,
    skip_discover: bool = False,
    fetch_sender: bool = False,
    sender_batch_size: int = 15,
    sender_batch_delay: float = 3.0,
):
    """
    混合模式：先发现 → 加入频道 → 回溯 → 导出

    流程:
      1. 从 targets.yaml 加载已有目标
      2. 通过 TG API + 搜索 Bot 发现新频道
      3. 将新发现频道追加到 targets.yaml
      4. 对所有目标频道（已有+新发现）执行回溯
      5. 汇总结果
    """
    from channel_discoverer import ChannelDiscoverer
    from keyword_filter import KeywordFilter
    from config_loader import add_targets, load_targets, get_target_identifiers

    logger = logging.getLogger(__name__)

    # --- 阶段1: 加载已有目标 ---
    targets = load_targets(targets_path)
    existing_count = len(targets.targets)
    logger.info(f"📋 已有目标: {existing_count} 个频道/群组")

    # --- 阶段2: 发现新频道 ---
    if skip_discover:
        logger.info(f"\n{'='*60}")
        logger.info(f"⏭️ 阶段1: 频道发现 (已跳过 --skip-discover)")
        logger.info(f"{'='*60}")
        discovered = []
    else:
        logger.info(f"\n{'='*60}")
        logger.info(f"🔄 阶段1: 频道发现 (关键词: {keywords})")
        logger.info(f"{'='*60}")

        discoverer = ChannelDiscoverer(client)
        if disable_bots:
            discovered = await discoverer.discover_only_tg_api(keywords)
        else:
            discovered = await discoverer.discover(keywords)

    # 追加到 targets.yaml
    new_targets = []
    for ch in discovered:
        if ch.username and ch.username not in ('xbso1', 'jisou', 'xbso2', 'jisou2'):
            new_targets.append({
                "identifier": ch.username,
                "title": ch.title,
                "type": ch.chat_type if ch.chat_type != "unknown" else "channel",
                "note": f"自动发现: {ch.source} | {ch.title}",
                "invite_link": ch.invite_link,
            })

    if new_targets:
        added = add_targets("auto", new_targets)
        logger.info(f"✅ 新增 {added} 个频道（已按行业分类写入）")
    else:
        logger.info("无新频道可追加")

    # 重新加载（含新追加的）
    try:
        targets = load_targets(targets_path)
    except Exception as e:
        logger.error(f"❌ 重新加载 targets 失败: {e}")
        logger.error(f"   discover 结果已写入文件，但 backfill 无法继续。")
        logger.error(f"   请手动修复 targets 文件后使用 --skip-discover 重试。")
        return {
            "discovered": len(discovered),
            "total_targets": 0,
            "total_messages": 0,
            "by_chat": [],
            "error": f"load_targets failed: {e}",
        }

    # --- 阶段2.5: 过滤新增频道，只回溯与关键词相关的 ---
    # 已有频道（targets 中原有的）全部回溯，不受过滤影响
    # 新发现频道：title/username 与 backfill_keywords 或 keywords 做相关性匹配
    # 不匹配的跳过回溯（但仍已存入 targets.yaml 供未来使用）
    # --no-backfill-filter 可禁用此行为
    # ⚠️ 相关性过滤用 discover 关键词（生态词），不是 backfill 品牌词
    # 例如 discover 搜「优惠券」→ 发现的频道 title 应与「优惠券」相关，而非 backfill 的「伊利」
    relevance_filter_kw = keywords or targets.global_keywords
    new_identifiers = set()           # 所有新发现频道的 identifier
    relevant_identifiers = set()      # 相关的新频道 identifier
    if new_targets and backfill_filter:
        for ch in discovered:
            if ch.username and ch.username not in ('xbso1', 'jisou', 'xbso2', 'jisou2'):
                new_identifiers.add(ch.username)
                search_text = f"{ch.title} {ch.username}".lower()
                if any(kw.lower() in search_text for kw in relevance_filter_kw):
                    relevant_identifiers.add(ch.username)

        new_total = len(new_targets)
        new_skipped = new_total - len(relevant_identifiers)
        if new_skipped > 0:
            skipped_examples = [nt['identifier'] for nt in new_targets if nt['identifier'] not in relevant_identifiers][:5]
            logger.info(f"🔍 新发现频道相关性过滤: {len(relevant_identifiers)}/{new_total} 相关, {new_skipped} 跳过")
            logger.info(f"   跳过示例: {skipped_examples}")

    # --- 阶段3: 回溯 ---
    logger.info(f"\n{'='*60}")
    logger.info(f"🔄 阶段2: 消息回溯 (单频道 limit={limit})")
    logger.info(f"{'='*60}")

    db = Database(db_path)
    await db.init()

    try:
        # hybrid 模式下，关键词优先使用 --keywords 输入的（如果是发现+回溯同一主题）
        # 回溯关键词优先级: --backfill-keywords > --keywords > global_keywords
        filter_keywords = backfill_keywords or keywords or targets.global_keywords
        logger.info(f"回溯过滤关键词: {filter_keywords}")

        keyword_filter = KeywordFilter(
            keywords=filter_keywords,
            rules=targets.keyword_rules,
        )
        all_identifiers = get_target_identifiers(targets)

        # 过滤新发现频道：已有频道全部保留，新发现频道只保留相关的
        if new_identifiers:
            identifiers = [
                ident for ident in all_identifiers
                if ident not in new_identifiers  # 已有频道，保留
                or ident in relevant_identifiers  # 新发现且相关，保留
            ]
            skipped = len(all_identifiers) - len(identifiers)
            if skipped > 0:
                logger.info(f"回溯目标: {len(identifiers)}/{len(all_identifiers)} 个 (跳过 {skipped} 个不相关的新频道)")
        else:
            identifiers = all_identifiers
            logger.info(f"共 {len(identifiers)} 个目标")

        # title 二次过滤应用 discover 关键词（生态词），而非 backfill 品牌词
        # 例如 discover 搜「优惠券」→ 用「优惠券」过滤频道 title，而非 backfill 的「伊利」
        title_filter_kw = keywords if (new_identifiers and backfill_filter) else None
        total_saved = await _backfill_channels(
            client, keyword_filter, identifiers, limit, db, resume=resume,
            title_filter_keywords=title_filter_kw,
            new_identifiers=new_identifiers if (new_identifiers and backfill_filter) else None,
            fetch_sender=fetch_sender,
            sender_batch_size=sender_batch_size,
            sender_batch_delay=sender_batch_delay,
        )

        # --- 阶段4: 汇总 ---
        stats = await db.get_stats()
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ 混合模式完成")
        logger.info(f"{'='*60}")
        logger.info(f"  发现频道数: {len(discovered)}")
        logger.info(f"  总目标数: {len(identifiers)} (新增 {len(identifiers)-existing_count})")
        logger.info(f"  回溯命中: {stats.get('total_messages', 0)} 条消息")

        # 按频道统计
        by_chat = stats.get('by_chat', [])
        if by_chat:
            logger.info(f"  命中频道:")
            for row in by_chat[:10]:
                name = row['title'] or row['username'] or 'unknown'
                logger.info(f"    {name}: {row['count']} 条")

        return {
            "discovered": len(discovered),
            "total_targets": len(identifiers),
            "total_messages": stats.get('total_messages', 0),
            "by_chat": by_chat,
        }
    finally:
        await db.close()


# ------------------------------------------------------------------
# 数据保留策略
# ------------------------------------------------------------------

async def run_retention_cleanup(
    db_path: str,
    media_dir: str,
    retention_days: int,
    do_vacuum: bool = True,
    existing_db: "Database | None" = None,
):
    """
    统一的数据保留清理入口：
      1. 清理过期消息 (messages)
      2. 清理关联的媒体文件 (文件系统 + media_files 表)
      3. 清理过期的断点续传记录 (channel_progress)
      4. 可选 VACUUM 回收空间

    Args:
        existing_db: 可选，传入已有的 Database 实例复用（避免重复打开冲突）
    """
    if retention_days <= 0:
        logging.info("数据保留: 未设保留天数，跳过清理")
        return

    # 复用已有实例或创建新实例
    db = existing_db
    own_db = False
    if db is None:
        db = Database(db_path)
        await db.init()
        own_db = True
    try:
        # 1. 获取清理前的数据库状态
        size_before = await db.get_db_size()
        counts_before = await db.get_table_counts()
        logging.info(f"数据保留: 清理 >{retention_days} 天的数据 (当前消息 {counts_before.get('messages', 0)} 条, "
                     f"DB 大小 {size_before/1024/1024:.1f}MB)")

        # 2. 清理过期消息，获取关联媒体路径
        deleted_msgs, media_paths = await db.retain_messages(retention_days)

        # 3. 清理关联的媒体文件
        deleted_files = 0
        if media_paths:
            import os as _os
            for path in media_paths:
                try:
                    if path and _os.path.exists(path):
                        _os.remove(path)
                        deleted_files += 1
                    # 清理空文件夹
                    parent = _os.path.dirname(path)
                    if _os.path.isdir(parent) and not _os.listdir(parent):
                        _os.rmdir(parent)
                        grandparent = _os.path.dirname(parent)
                        if _os.path.isdir(grandparent) and not _os.listdir(grandparent):
                            _os.rmdir(grandparent)
                except OSError as e:
                    logging.debug(f"清理媒体文件失败: {path}: {e}")
            logging.info(f"🧹 媒体文件: 清理 {deleted_files} 个文件")

        # 4. 清理过期断点续传记录
        await db.retain_channel_progress(retention_days)

        # 5. VACUUM
        if do_vacuum and deleted_msgs > 0:
            await db.vacuum()
            size_after = await db.get_db_size()
            saved = size_before - size_after
            if saved > 0:
                logging.info(f"🧹 空间回收: {saved/1024/1024:.1f}MB (DB {size_after/1024/1024:.1f}MB)")

        counts_after = await db.get_table_counts()
        logging.info(f"数据保留完成: 消息 {counts_after.get('messages', 0)} 条 "
                     f"(删 {deleted_msgs} 条)")
    finally:
        if own_db:
            await db.close()


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="TG 爬虫 - Telegram 频道/群组消息监控",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
模式:
  python main.py                                      # 实时监控 (默认)
  python main.py --backfill --backfill-limit 500      # 回溯历史消息
  python main.py --mode discover --keywords "无尽冬日" # 频道发现
  python main.py --mode hybrid --keywords "无尽冬日"   # 发现+回溯 (推荐)

示例:
  python main.py --mode hybrid --keywords "无尽冬日,Whiteout Survival"
  python main.py --mode discover --keywords "无尽冬日" --no-bots
  python main.py --targets custom.yaml --env .env
  python main.py --export results.csv --since 2026-06-01 --format csv
  python main.py --export results.md --chats jdbroo,xbcia --format markdown
        """,
    )
    parser.add_argument(
        "--targets", default="../config/targets.yaml",
        help="目标配置文件路径 或 行业 profile (gaming/retail/all)。逗号分隔可组合多个，如 gaming,retail"
    )
    parser.add_argument(
        "--env", default="../config/.env",
        help="环境变量文件路径 (默认: ../config/.env)"
    )
    parser.add_argument(
        "--db", default="../data/crawler.db",
        help="数据库路径 (默认: ../data/crawler.db)"
    )
    parser.add_argument(
        "--media-dir", default="../data/media",
        help="媒体文件目录 (默认: ../data/media)"
    )
    parser.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="日志级别 (默认: INFO)"
    )
    parser.add_argument(
        "--backfill", action="store_true",
        help="[兼容模式] 历史消息回溯模式（非实时监听）。新项目建议用 --mode hybrid"
    )
    parser.add_argument(
        "--backfill-limit", type=int, default=500,
        help="单频道回溯消息数 (默认: 500)"
    )
    parser.add_argument(
        "--session", default="tg_crawler",
        help="Telethon session 名称 (默认: tg_crawler)"
    )
    parser.add_argument(
        "--account", type=int, default=1, choices=[1, 2, 3],
        help="TG 账号编号 (1/2/3，默认: 1)。对应 .env 中的 TG1_* / TG2_* / TG3_* 凭证组"
    )
    parser.add_argument(
        "--failover", type=int, default=0, metavar="N",
        help="启用账号自动 failover：当前账号失败时依次尝试后续 N 个账号 (如 --failover 2 表示失败后尝试 +1,+2)"
    )
    parser.add_argument(
        "--code", default=None,
        help="验证码（首次登录或 session 过期时使用）"
    )
    parser.add_argument(
        "--code-file", default=None,
        help="从文件读取验证码（适用于非交互环境）"
    )
    parser.add_argument(
        "--password", default=None,
        help="2FA 密码（如果账号开启了二次验证）"
    )
    # --- 新增: 模式 & 关键词 ---
    parser.add_argument(
        "--mode", default="monitor",
        choices=["monitor", "backfill", "discover", "hybrid"],
        help="运行模式 (默认: monitor) - discover=仅发现频道, hybrid=发现+回溯"
    )
    parser.add_argument(
        "--keywords", default=None,
        help="搜索关键词，逗号分隔 (用于 discover/hybrid 模式)，如 '无尽冬日,Whiteout Survival'"
    )
    parser.add_argument(
        "--backfill-keywords", default=None,
        help="回溯阶段专属关键词，逗号分隔。不传时回退到 --keywords。适用场景：discover 搜生态词(优惠券) + backfill 搜品牌名(伊利)"
    )
    parser.add_argument(
        "--no-backfill-filter", action="store_true",
        help="禁用新发现频道的相关性过滤（默认启用：新频道 title 与关键词不匹配则跳过回溯）"
    )
    parser.add_argument(
        "--no-resume", action="store_true",
        help="禁用断点续传（默认启用：已完成回溯的频道会被跳过，Flood Wait 中断后重跑不重复）"
    )
    parser.add_argument(
        "--no-bots", action="store_true",
        help="禁用搜索 Bot，仅使用 TG 官方 API (用于 discover/hybrid 模式)"
    )
    parser.add_argument(
        "--skip-discover", action="store_true",
        help="hybrid 模式下跳过频道发现阶段，仅对已有频道回溯（节省 API 配额）"
    )
    parser.add_argument(
        "--fetch-sender", action="store_true",
        help="获取发送者信息（用户名/显示名称）。启用后会增加少量 API 调用，已通过缓存+批量延迟防 Flood Wait"
    )
    parser.add_argument(
        "--sender-batch-size", type=int, default=15,
        help="每批获取发送者数量 (默认: 15)"
    )
    parser.add_argument(
        "--sender-batch-delay", type=float, default=3.0,
        help="发送者信息批次间延迟秒数 (默认: 3.0)"
    )
    parser.add_argument(
        "--export", default=None, metavar="FILE",
        help="导出数据库消息到文件（跳过采集流程），如 'results.csv'"
    )
    parser.add_argument(
        "--export-format", default="csv", choices=["csv", "json", "markdown"],
        help="导出格式: csv/json/markdown (默认: csv)"
    )
    parser.add_argument(
        "--since", default=None,
        help="导出起始日期 YYYY-MM-DD"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="试运行模式：不连接 TG，仅打印将执行的操作和参数"
    )
    parser.add_argument(
        "--retention-days", type=int, default=90, metavar="DAYS",
        help="数据保留天数: 自动清理超过 N 天的消息、媒体文件和断点记录 (默认: 90, 设 0 禁用)"
    )
    parser.add_argument(
        "--no-vacuum", action="store_true",
        help="禁用自动 VACUUM 空间回收（默认：清理后自动 VACUUM）"
    )
    parser.add_argument(
        "--purge-after-export", action="store_true",
        help="导出完成后清理数据库和媒体文件（⚠️ 危险操作，确认后执行）"
    )
    parser.add_argument(
        "--until", default=None,
        help="导出截止日期 YYYY-MM-DD"
    )
    parser.add_argument(
        "--chats", default=None,
        help="限定频道，逗号分隔的 username 列表"
    )
    parser.add_argument(
        "--discover-only", action="store_true",
        help="[兼容] 同 --mode discover"
    )

    args = parser.parse_args()

    # 加载 .env
    env_path = Path(args.env)
    if env_path.exists():
        load_dotenv(env_path)
    else:
        logging.warning(f".env 文件不存在: {args.env}，将使用系统环境变量")

    # 解析账号编号（支持 --account 1 或 --account 2）
    account = getattr(args, 'account', 1) or 1
    failover = getattr(args, 'failover', 0) or 0
    if account not in (1, 2, 3):
        print(f"❌ 不支持的账号编号: {account}，仅支持 1、2 或 3")
        sys.exit(1)
    if failover < 0:
        failover = 0

    setup_logging(args.log_level)
    check_dependencies()

    def _build_client(acct: int) -> tuple[TelegramClient, str | None]:
        """构建指定账号的 Telethon 客户端和 2FA 密码。返回 (client, password)"""
        nonlocal args
        prefix = f"TG{acct}_"

        # 账号 1 支持向后兼容
        api_id = os.getenv(f"{prefix}API_ID")
        api_hash = os.getenv(f"{prefix}API_HASH")
        phone = os.getenv(f"{prefix}PHONE")
        pwd_env = os.getenv(f"{prefix}PASSWORD")
        if acct == 1:
            api_id = api_id or os.getenv("TG_API_ID")
            api_hash = api_hash or os.getenv("TG_API_HASH")
            phone = phone or os.getenv("TG_PHONE")
            pwd_env = pwd_env or os.getenv("TG_PASSWORD")

        if not api_id or not api_hash or not phone:
            return None, None

        session_name = f"{args.session}_acc{acct}" if acct > 1 else args.session
        # 2FA 密码：命令行 > 环境变量（空字符串视为未设置）
        tg_password = args.password or pwd_env or None

        # 代理
        proxy = None
        proxy_host = os.getenv(f"{prefix}PROXY_HOST") or os.getenv("PROXY_HOST")
        proxy_port = os.getenv(f"{prefix}PROXY_PORT") or os.getenv("PROXY_PORT")
        proxy_user = os.getenv(f"{prefix}PROXY_USER") or os.getenv("PROXY_USER")
        proxy_pass = os.getenv(f"{prefix}PROXY_PASS") or os.getenv("PROXY_PASS")
        if proxy_host and proxy_port:
            if proxy_user and proxy_pass:
                proxy = ("socks5", proxy_host, int(proxy_port), True, proxy_user, proxy_pass)
                logging.info(f"使用 SOCKS5 代理 (账号 {acct}, 认证): {proxy_host}:{proxy_port}")
            else:
                proxy = ("socks5", proxy_host, int(proxy_port))
                logging.info(f"使用 SOCKS5 代理 (账号 {acct}): {proxy_host}:{proxy_port}")
        elif os.getenv(f"{prefix}PROXY_HOST") or os.getenv("PROXY_HOST"):
            logging.warning(f"代理配置不完整 (账号 {acct})，跳过代理")

        client = TelegramClient(session_name, int(api_id), api_hash, proxy=proxy)
        return client, tg_password

    async def _try_connect(acct: int, is_failover: bool = False) -> TelegramClient | None:
        """尝试连接并登录指定账号，成功返回 client，失败返回 None
        
        Args:
            acct: 账号编号 1/2/3
            is_failover: 是否来自 failover 链（切换账号），用于控制验证码和行为
        """
        result = _build_client(acct)
        if result[0] is None:
            logging.warning(f"账号 {acct} 凭证缺失，跳过")
            return None

        client, tg_password = result
        try:
            def read_code():
                # 🔒 安全规则：failover 绝不用主账号的验证码
                # 验证码与 phone_code_hash 绑定，换账号必须换 code
                if is_failover:
                    # check dedicated code file: code_acc{acct}.txt
                    import os as _os
                    dedicated = f"code_acc{acct}.txt"
                    if _os.path.exists(dedicated):
                        with open(dedicated) as f:
                            return f.read().strip()
                    # Only allow --code for failover if explicitly set (rare)
                    if args.code:
                        return args.code
                    raise RuntimeError(
                        f"⛔ failover 到账号 {acct} 但无专属验证码文件 code_acc{acct}.txt。"
                        f"主账号的验证码对其他账号无效，已终止 failover 避免污染备用账号。"
                    )
                # 正常模式（主账号）
                if args.code:
                    return args.code
                if args.code_file:
                    try:
                        with open(args.code_file, 'r') as f:
                            return f.read().strip()
                    except Exception as e:
                        logging.error(f"读取验证码文件失败: {e}")
                        raise
                try:
                    return input('Please enter the code you received: ')
                except EOFError:
                    logging.warning("非交互环境无法输入验证码，请使用 --code 或 --code-file")
                    raise RuntimeError("验证码输入不可用") from None

            kwargs = {"phone": _build_phone(acct), "code_callback": read_code}
            if tg_password:
                kwargs["password"] = tg_password
            await client.start(**kwargs)
            me = await client.get_me()
            logging.info(f"✅ 已登录: {me.first_name} (@{me.username}) [ID: {me.id}]")
            return client
        except FloodWaitError as e:
            logging.warning(f"账号 {acct} Flood Wait {e.seconds}s")
            try:
                await client.disconnect()
            except Exception:
                pass
            return None
        except Exception as e:
            # 区分可恢复 vs 不可恢复错误
            err_name = type(e).__name__
            err_msg = str(e)
            unrecoverable = any(kw in err_name or kw in err_msg for kw in (
                'PasswordHashInvalid', 'password', '2fa', 'two-step',
                'AccessTokenInvalid', 'AuthKey', 'API_ID', 'api_id',
            ))
            if unrecoverable:
                logging.error(f"⛔ 账号 {acct} 不可恢复错误: {err_name}: {err_msg[:100]}")
            else:
                logging.warning(f"账号 {acct} 连接失败: {err_name}: {err_msg[:100]}")
            try:
                await client.disconnect()
            except Exception:
                pass
            return None

    def _build_phone(acct: int) -> str:
        """从环境变量读取指定账号的 phone"""
        prefix = f"TG{acct}_"
        phone = os.getenv(f"{prefix}PHONE")
        if acct == 1:
            phone = phone or os.getenv("TG_PHONE")
        return phone or ""

    # 主连接：支持 failover
    original_phone = _build_phone(account)
    client = None  # 供 finally 清理用，非局部变量

    async def run():
        nonlocal account, client

        # --- dry-run 模式：不连接 TG，打印计划后直接退出 ---
        if args.dry_run:
            mode = args.mode
            if args.backfill:
                mode = "backfill"
            if args.discover_only:
                mode = "discover"

            keywords = [kw.strip() for kw in args.keywords.split(',') if kw.strip()] if args.keywords else []
            backfill_keywords = None
            if args.backfill_keywords:
                backfill_keywords = [kw.strip() for kw in args.backfill_keywords.split(',') if kw.strip()]

            print("\n" + "=" * 60)
            print(f"🔍 DRY-RUN: {mode.upper()} 模式")
            print("=" * 60)
            print(f"  账号: TG{account}")
            if failover:
                print(f"  Failover: 失败后尝试 +1 ~ +{failover}")
            print(f"  行业: {args.targets}")

            if mode in ("discover", "hybrid"):
                if args.skip_discover:
                    print(f"  Discover: ⏭️ 跳过 (--skip-discover)")
                else:
                    print(f"  Discover 关键词: {keywords}")
                    print(f"  搜索 Bot: {'禁用' if args.no_bots else '启用 (xbso1, jisou)'}")
                    print(f"  预计发现: 每关键词 10-50 个频道")

            if mode in ("backfill", "hybrid"):
                bf_kw = backfill_keywords or keywords
                print(f"  Backfill 关键词: {bf_kw}")
                print(f"  单频道回溯: {args.backfill_limit} 条")
                print(f"  断点续传: {'禁用' if args.no_resume else '启用'}")
                if not args.no_backfill_filter:
                    print(f"  新频道过滤: 启用 (title 与 discover 关键词匹配才回溯)")
                if args.fetch_sender:
                    print(f"  发送者信息: ✅ 启用 (批量 {args.sender_batch_size}/批, 延迟 {args.sender_batch_delay}s)")
                else:
                    print(f"  发送者信息: ❌ 未启用 (加 --fetch-sender 开启)")

            if args.retention_days > 0:
                print(f"  数据保留: {args.retention_days} 天")
                print(f"  VACUUM: {'启用' if not args.no_vacuum else '禁用'}")
            else:
                print(f"  数据保留: 不清理 (--retention-days 0)")

            if mode == "hybrid":
                print(f"  流程: discover → 追加 channels → backfill → 汇总")
            elif mode == "monitor":
                print(f"  流程: 7×24 监听 targets.yaml 中新消息")

            print(f"  目标文件: {args.targets}")
            print(f"  数据库: {args.db}")
            print("=" * 60 + "\n")

            from config_loader import load_targets
            try:
                targets = load_targets(args.targets)
                print(f"📋 当前已有频道: {len(targets.targets)} 个")
                by_type = {}
                for t in targets.targets:
                    by_type[t.type] = by_type.get(t.type, 0) + 1
                for tp, cnt in by_type.items():
                    print(f"   {tp}: {cnt} 个")
            except Exception:
                pass

            print(f"\n💡 去掉 --dry-run 即可正式执行。\n")
            return

        # --- 正常模式：连接 TG ---
        client = await _try_connect(account, is_failover=False)
        used_account = account

        if client is None:
            # 自动 failover：仅 FloodWait 或网络临时故障才尝试备用
            if failover > 0:
                logging.info(f"🔄 账号 {account} 不可用，启用 failover (最多 {failover} 个备用)")
            for offset in range(1, failover + 1):
                candidate = account + offset
                if candidate > 3:
                    break
                logging.info(f"🔄 尝试备用账号 {candidate}...")
                client = await _try_connect(candidate, is_failover=True)
                if client:
                    used_account = candidate
                    args.account = candidate
                    break

        if client is None:
            print(f"❌ 所有账号均不可用（主账号 {account} + {failover} 个备用）")
            sys.exit(1)

        if used_account != account:
            logging.info(f"⚠️ 已切换到账号 {used_account} (原账号 {account} 不可用)")
            account = used_account

        # 解析模式
        mode = args.mode
        # 兼容旧的 --backfill 和 --discover-only 标志
        if args.backfill:
            mode = "backfill"
        if args.discover_only:
            mode = "discover"

        # --export 模式：不连接 TG，直接导出数据库
        if args.export:
            chats_list = None
            if args.chats:
                chats_list = [c.strip() for c in args.chats.split(',') if c.strip()]
            count = await run_export(
                db_path=args.db,
                output=args.export,
                format=args.export_format,
                since=args.since,
                until=args.until,
                chats=chats_list,
            )
            print(f"✅ 导出完成: {count} 条消息 → {args.export}")

            # --purge-after-export: 导出后清理所有数据
            if args.purge_after_export:
                confirm = input("⚠️ 即将清空数据库和所有媒体文件，确认？(输入 yes 继续): ")
                if confirm.strip().lower() == "yes":
                    db = Database(args.db)
                    await db.init()
                    try:
                        counts = await db.get_table_counts()
                        logging.warning(f"清理前: messages={counts.get('messages', 0)}, "
                                        f"media_files={counts.get('media_files', 0)}, "
                                        f"progress={counts.get('channel_progress', 0)}")
                        await db.conn.execute("DELETE FROM messages")
                        await db.conn.execute("DELETE FROM channel_progress")
                        await db.conn.execute("DELETE FROM media_files")
                        await db.conn.commit()
                        logging.info("✅ 数据库已清空")
                        # 全表 DELETE 后 VACUUM 回收磁盘空间
                        await db.vacuum()
                    finally:
                        await db.close()
                    # 清理 media_dir
                    import shutil, os as _os2
                    media_dir_path = args.media_dir
                    if _os2.path.isdir(media_dir_path):
                        for item in _os2.listdir(media_dir_path):
                            item_path = _os2.path.join(media_dir_path, item)
                            try:
                                if _os2.path.isdir(item_path):
                                    shutil.rmtree(item_path)
                                else:
                                    _os2.remove(item_path)
                            except OSError as e:
                                logging.warning(f"清理媒体失败: {item_path}: {e}")
                        logging.info("✅ 媒体文件已清空")
                    print("✅ 数据库和媒体文件已全部清空")
                else:
                    print("已取消清理操作")
            return

        # 解析关键词
        keywords = None
        if args.keywords:
            keywords = [kw.strip() for kw in args.keywords.split(',') if kw.strip()]

        # 解析回溯专属关键词（不传时回退到 --keywords）
        backfill_keywords = None
        if args.backfill_keywords:
            backfill_keywords = [kw.strip() for kw in args.backfill_keywords.split(',') if kw.strip()]

        if mode == "discover":
            # 仅频道发现
            if not keywords:
                logging.error("discover 模式需要 --keywords 参数")
                return
            await run_discover(
                client=client,
                targets_path=args.targets,
                keywords=keywords,
                disable_bots=args.no_bots,
            )

        elif mode == "hybrid":
            # 发现 + 回溯
            if not keywords:
                logging.error("hybrid 模式需要 --keywords 参数")
                return
            await run_hybrid(
                client=client,
                targets_path=args.targets,
                db_path=args.db,
                media_dir=args.media_dir,
                keywords=keywords,
                backfill_keywords=backfill_keywords or keywords,
                limit=args.backfill_limit,
                disable_bots=args.no_bots,
                backfill_filter=not args.no_backfill_filter,
                resume=not args.no_resume,
                skip_discover=args.skip_discover,
                fetch_sender=args.fetch_sender,
                sender_batch_size=args.sender_batch_size,
                sender_batch_delay=args.sender_batch_delay,
            )

        elif mode == "backfill":
            # 纯回溯（使用已有 targets.yaml）
            await run_backfill(
                client=client,
                targets_path=args.targets,
                db_path=args.db,
                media_dir=args.media_dir,
                limit=args.backfill_limit,
                keywords=backfill_keywords or keywords,
                resume=not args.no_resume,
                fetch_sender=args.fetch_sender,
                sender_batch_size=args.sender_batch_size,
                sender_batch_delay=args.sender_batch_delay,
            )

        else:
            # monitor 模式
            await run_monitor(
                client=client,
                targets_path=args.targets,
                db_path=args.db,
                media_dir=args.media_dir,
            )

    # 优雅退出
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def shutdown():
        logging.info("收到退出信号，正在关闭...")
        for task in asyncio.all_tasks(loop):
            task.cancel()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, shutdown)
        except NotImplementedError:
            # Windows 不支持 add_signal_handler
            signal.signal(sig, lambda s, f: shutdown())

    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        logging.info("用户中断")
    except asyncio.CancelledError:
        pass
    finally:
        # 先断开 TG 连接，取消后台 Telethon 任务
        if client is not None:
            try:
                loop.run_until_complete(client.disconnect())
            except Exception:
                pass

        # 数据保留清理（所有模式执行完毕后触发，dry-run 跳过）
        if not args.dry_run:
            try:
                loop.run_until_complete(run_retention_cleanup(
                    db_path=args.db,
                    media_dir=args.media_dir,
                    retention_days=args.retention_days,
                    do_vacuum=not args.no_vacuum,
                ))
            except Exception as e:
                logging.warning(f"数据保留清理失败: {e}")

        loop.close()
        logging.info("爬虫已停止")


if __name__ == "__main__":
    main()
