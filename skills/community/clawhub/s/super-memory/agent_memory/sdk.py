"""Agent Memory SDK — Minimal 5-method API for instant integration.

Usage:
    from agent_memory import Memory

    mem = Memory()                       # Zero config
    mem.remember("Python is great")      # Remember a memory
    results = mem.recall("python")       # Recall memories
    mem.update(id, "new content")        # Update a memory
    mem.forget(id)                       # Forget a memory
    mem.status()                         # Health check

That's it. 5 methods. Zero learning curve.
For advanced features, access the underlying engine: mem.engine
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class Memory:
    """Agent Memory — 智能记忆系统

    3个核心方法，3秒学会：
        mem.remember("内容")   # 记住 → 返回 SaveResult
        mem.recall("查询")     # 回忆 → 返回 SearchResult
        mem.forget(memory_id)  # 忘记 → 返回 DeleteResult

    兼容别名：save() = remember(), search() = recall(), delete() = forget()

    更多方法：
        mem.update(id, content)    # 更新记忆
        mem.revert(id, version)    # 回滚版本
        mem.bookmark(id)           # 收藏记忆
        mem.bookmarks()            # 查看收藏
        mem.echo()                 # 主动推荐
        mem.status()               # 系统状态
        mem.milestones()           # 查看成就
        mem.share_card()           # 分享卡片
        mem.close()                # 释放资源

    Advanced:
        mem.engine  — Access the full AgentMemory engine for advanced features
        mem.store   — Access the MemoryStore for direct DB operations

    Examples:
        # Basic usage
        from agent_memory import Memory
        mem = Memory()

        mid = mem.remember("Meeting at 3pm with Alice")
        results = mem.recall("meeting Alice")
        mem.update(mid, "Meeting at 4pm with Alice")
        mem.forget(mid)

        # With metadata
        mid = mem.remember("Deployed v2.1", tags=["deploy", "v2.1"], importance="high")

        # Multi-tenant
        mem = Memory(tenant_id="team_alpha")

        # Remote server
        mem = Memory(server="http://localhost:8000", api_key="<YOUR_API_KEY>")
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        agent_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        server: Optional[str] = None,
        api_key: Optional[str] = None,
        profile: Optional[str] = None,
        recall_config: Optional[dict] = None,
        ingest_config: Optional[dict] = None,
        store_config: Optional[dict] = None,
        **kwargs,
    ):
        """Initialize memory module.

        Args:
            db_path: Database file path. Default: ~/.agent_memory/default.db
            agent_id: Agent identifier. Default: "default"
            tenant_id: Tenant identifier for multi-tenant isolation
            server: Remote API server URL (e.g., "http://localhost:8000")
            api_key: API key for remote server authentication
            profile: Preset configuration ("personal", "chatbot", "knowledge", "enterprise")
            recall_config: Override recall engine parameters
            ingest_config: Override ingest engine parameters
            store_config: Override store parameters
            **kwargs: Additional options passed to AgentMemory
        """
        self._tenant_id = tenant_id
        self._server = server
        self._api_key = api_key
        self._profile = profile or "personal"

        if server:
            # Remote mode — use HTTP client
            from agent_memory.sdk_client import MemoryClient
            self._client = MemoryClient(server, api_key=api_key, tenant_id=tenant_id)
            self._engine = None
        else:
            # Apply profile
            from agent_memory.profiles import merge_profile
            config = merge_profile(self._profile, {
                **({"recall": recall_config} if recall_config else {}),
                **({"ingest": ingest_config} if ingest_config else {}),
                **({"store": store_config} if store_config else {}),
            })

            # Pass profile config to AgentMemory
            engine_kwargs = dict(kwargs)
            if config.get("recall"):
                engine_kwargs["recall_config"] = config["recall"]
            if config.get("ingest"):
                engine_kwargs["ingest_config"] = config["ingest"]
            if config.get("store"):
                engine_kwargs["store_config"] = config["store"]

            # Local mode — use embedded engine
            from agent_memory.memory_system import AgentMemory
            self._engine = AgentMemory(
                db_path=db_path,
                agent_id=agent_id,
                **engine_kwargs,
            )
            self._client = None

    @property
    def engine(self):
        """Access the full AgentMemory engine (local mode only)."""
        if self._engine is None:
            raise RuntimeError("远程模式下引擎不可用，请使用 MemoryClient 方法。")
        return self._engine

    @property
    def store(self):
        """Access the MemoryStore directly (local mode only)."""
        return self.engine.store

    def save(self, content: str, **kwargs) -> 'SaveResult':
        """Save a memory. Returns SaveResult with memory_id, status, message, and tip.

        Args:
            content: The content to remember
            **kwargs: Optional metadata:
                importance: "high" / "normal" / "low" / "ephemeral"
                topics: List of topics
                nature: Nature code (e.g., "note", "fact")
                force: Skip filter, force write (default False)

        Returns:
            SaveResult with memory_id, accepted, status, message, and tip

        Examples:
            result = mem.save("Deployed v2.1")
            if result:
                print(result.memory_id)
            result = mem.save("Critical alert", importance="high")
        """
        from agent_memory.result_types import SaveResult

        # Empty content check
        if not content or not content.strip():
            return SaveResult(
                memory_id="",
                accepted=False,
                status="empty",
                message="内容为空",
                tip="请确保内容至少包含 1 个非空白字符。",
            )

        if self._client:
            mid = self._client.save(content, **kwargs)
            if mid:
                return SaveResult(memory_id=mid, accepted=True, status="stored", message="记忆已保存")
            return SaveResult(accepted=False, status="error", message="远程保存失败")

        result = self._engine.remember(content, **kwargs)

        if isinstance(result, dict):
            written = result.get("written", result.get("accepted", False))
            memory_id = result.get("memory_id", "")
            status = result.get("status", "stored" if written else "filtered")
            reason = result.get("reason", "")
            quality_score = result.get("quality_score")
            quality_level = result.get("quality_level")

            # Generate tip based on status
            tip = self._generate_save_tip(status, reason, quality_level, content)
            message = self._generate_save_message(status, reason)

            # Check for milestone achievement
            milestone = None
            if written:
                milestone = self._check_milestone()

            return SaveResult(
                memory_id=memory_id if written else "",
                accepted=written,
                status=status,
                message=message,
                tip=tip,
                quality_score=quality_score,
                quality_level=quality_level,
                milestone=milestone,
            )

        if isinstance(result, str):
            return SaveResult(memory_id=result, accepted=True, status="stored", message="记忆已保存")

        return SaveResult(accepted=False, status="error", message="意外的结果类型")

    def recall(self, query: str, limit: int = 10, **kwargs) -> 'SearchResult':
        """Recall memories. Returns SearchResult with items, suggestions, and explore.

        This is the primary method for searching memories. Also available as search() for compatibility.

        Each result dict contains:
            memory_id: Unique identifier
            content: Memory content text
            score: Relevance score (0.0-1.0)
            importance: Importance level
            created_at: Creation timestamp

        Args:
            query: Search query text
            limit: Maximum results to return (default 10)
            **kwargs: Optional filters:
                importance: Filter by importance level
                topic: Filter by topic
                keyword: Keyword search

        Returns:
            SearchResult with items, suggestions, explore, and tip

        Examples:
            result = mem.recall("deploy")
            if result:
                for r in result:
                    print(f"[{r['memory_id']}] {r['content']}")
        """
        from agent_memory.result_types import SearchResult

        if self._client:
            items = self._client.search(query, limit=limit, **kwargs)
            suggestions = [] if items else ["Try broader keywords", "Check spelling"]
            return SearchResult(items=items, total=len(items), suggestions=suggestions)

        result = self._engine.recall(query=query, limit=limit, **kwargs)

        items = []
        suggestions = []
        explore = []
        tip = ""
        degraded = []

        if isinstance(result, dict):
            primary = result.get("primary", result.get("results", []))
            suggestions = result.get("suggestions", [])
            degraded = result.get("_warnings", [])

            # Check degradation warnings from engine
            if not degraded and hasattr(self._engine, 'get_degradation_warnings'):
                warnings = self._engine.get_degradation_warnings()
                if warnings:
                    degraded = warnings

            if isinstance(primary, list):
                for r in primary:
                    if isinstance(r, dict):
                        items.append({
                            "memory_id": r.get("memory_id", ""),
                            "content": r.get("content", ""),
                            "score": r.get("_rrf_score", r.get("score", 0.0)),
                            "importance": r.get("importance", "normal"),
                            "created_at": r.get("time_ts", ""),
                            "tags": r.get("tags", []),
                            "topic": r.get("topic", ""),
                        })

            # Generate explore recommendations for empty results
            if not items:
                explore = self._get_explore_recommendations(limit=3)
                if not suggestions:
                    suggestions = [
                        "试试更宽泛或不同的关键词",
                        "确认信息是否已经存入",
                        "用 echo() 浏览你的记忆",
                    ]
                tip = "没找到相关记忆 — 试试下面的建议，或浏览你的记忆"
            elif len(items) <= 3:
                tip = "Few results found. Try related keywords for more."

        if isinstance(result, list):
            for r in result:
                if isinstance(r, dict) and "_degraded" not in r:
                    items.append(r)
            items = items[:limit]

        return SearchResult(
            items=items[:limit],
            total=len(items),
            suggestions=suggestions,
            explore=explore,
            tip=tip,
            degraded=degraded,
        )

    # Backward-compatible alias
    def search(self, query: str, limit: int = 10, **kwargs) -> 'SearchResult':
        """Alias for recall(). Prefer recall() for brand consistency."""
        return self.recall(query, limit=limit, **kwargs)

    def update(self, memory_id: str, content: str, **kwargs) -> bool:
        """Update a memory's content. Returns True if successful.

        Args:
            memory_id: The memory to update
            content: New content
            **kwargs: Optional metadata to update:
                importance: New importance level
                topics: New topic list

        Returns:
            True if updated, False if not found

        Examples:
            mem.update("mem_abc123", "Updated content")
            mem.update("mem_abc123", "New info", importance="high")
        """
        if self._client:
            return self._client.update(memory_id, content, **kwargs)

        try:
            result = self._engine.store.update_memory(memory_id, content, **kwargs)
            if isinstance(result, dict):
                return result.get("updated", False) or result.get("success", False) or "error" not in result
            return True
        except Exception as e:
            logger.debug("Update failed: %s", e)
            return False

    def forget(self, memory_id: str, permanent: bool = False) -> 'DeleteResult':
        """Forget a memory. Returns DeleteResult with status details.

        This is the primary method for deleting memories. Also available as delete() for compatibility.

        Args:
            memory_id: The memory to delete
            permanent: If True, permanently delete (cannot be restored)
                       If False (default), soft delete (can be restored)

        Returns:
            DeleteResult with deleted, status, message, and restorable

        Examples:
            result = mem.forget("mem_abc123")           # Soft delete (restorable)
            result = mem.forget("mem_abc123", permanent=True)  # Permanent delete
        """
        from agent_memory.result_types import DeleteResult

        if self._client:
            ok = self._client.delete(memory_id, permanent=permanent)
            return DeleteResult(
                memory_id=memory_id,
                deleted=ok,
                status="permanent" if permanent and ok else ("deleted" if ok else "not_found"),
                message="记忆已忘记（30天内可恢复）" if ok and not permanent else ("记忆已永久删除" if ok else "找不到这条记忆 — 它可能已被删除"),
                restorable=not permanent if ok else False,
            )

        try:
            result = self._engine.store.delete_memory(memory_id, permanent=permanent)
            if isinstance(result, dict):
                deleted = result.get("deleted", False)
                reason = result.get("reason", "")
                is_soft = result.get("soft_delete", not permanent)

                if not deleted and "not exist" in reason.lower():
                    return DeleteResult(
                        memory_id=memory_id, deleted=False, status="not_found",
                        message="找不到这条记忆 — 它可能已被删除", restorable=False,
                    )
                if not deleted and "already" in reason.lower():
                    return DeleteResult(
                        memory_id=memory_id, deleted=False, status="already_deleted",
                        message="记忆已被删除", restorable=True,
                    )

                return DeleteResult(
                    memory_id=memory_id, deleted=deleted,
                    status="permanent" if permanent else "deleted",
                    message="记忆已永久删除" if permanent else "记忆已忘记（30天内可恢复）",
                    restorable=is_soft and not permanent,
                )
            return DeleteResult(memory_id=memory_id, deleted=True, status="deleted", message="记忆已忘记（30天内可恢复）", restorable=not permanent)
        except Exception as e:
            return DeleteResult(memory_id=memory_id, deleted=False, status="error", message=str(e), restorable=False)

    # Backward-compatible alias
    def delete(self, memory_id: str, permanent: bool = False) -> 'DeleteResult':
        """Alias for forget(). Prefer forget() for brand consistency."""
        return self.forget(memory_id, permanent=permanent)

    def status(self) -> dict:
        """Check memory system health. Returns status dict.

        Returns:
            {
                "healthy": bool,
                "status": "healthy" / "degraded" / "unhealthy",
                "total_memories": int,
                "components": {...},
                "stats": {...},
            }
        """
        if self._client:
            return self._client.status()

        return self._engine.health_check()

    def echo(self, context: str = "", limit: int = 3) -> list:
        """Get proactive memory recommendations — "Hey, remember when..."

        Unlike search(), echo() doesn't need a specific query. It proactively
        suggests memories based on time, context, and activity patterns.

        Args:
            context: Optional current context for association-based recommendations
            limit: Maximum recommendations (default 3)

        Returns:
            List of {"memory_id", "content", "reason", "relevance"}

        Examples:
            # What should I be reminded of?
            echoes = mem.echo()
            for e in echoes:
                print(f"📖 {e['reason']}: {e['content']}")

            # Context-aware recommendations
            echoes = mem.echo(context="deploying new version")
        """
        if self._client:
            return self._client.echo(context=context, limit=limit)

        try:
            from agent_memory.echo import MemoryEcho
            echo_engine = MemoryEcho(self._engine.store, self._engine.recall_engine)
            return echo_engine.echo(context=context, limit=limit)
        except Exception as e:
            logger.debug("Echo failed: %s", e)
            return []

    def revert(self, memory_id: str, version: int) -> bool:
        """Revert a memory to a specific version. Returns True if successful.

        Args:
            memory_id: The memory to revert
            version: Version number to revert to (1-based)

        Returns:
            True if reverted successfully, False otherwise
        """
        if self._client:
            return self._client.update(memory_id, "")  # Remote doesn't support revert yet

        try:
            result = self._engine.store.revert_to_version(memory_id, version)
            return result.get("reverted", False)
        except Exception as e:
            logger.debug("Revert failed: %s", e)
            return False

    def bookmark(self, memory_id: str) -> bool:
        """Bookmark a memory for quick access.

        Args:
            memory_id: The memory to bookmark

        Returns:
            True if bookmarked, False if not found
        """
        if self._client:
            return self._client.bookmark(memory_id)
        try:
            result = self._engine.store.bookmark(memory_id)
            if result.get("bookmarked", False):
                logger.info("⭐ 已收藏！用 bookmarks() 快速查看所有收藏")
            return result.get("bookmarked", False)
        except Exception:
            return False

    def unbookmark(self, memory_id: str) -> bool:
        """Remove bookmark from a memory.

        Args:
            memory_id: The memory to unbookmark

        Returns:
            True if unbookmarked
        """
        if self._client:
            return self._client.unbookmark(memory_id)
        try:
            self._engine.store.unbookmark(memory_id)
            return True
        except Exception:
            return False

    def bookmarks(self, limit: int = 50) -> list:
        """Get all bookmarked memories.

        Args:
            limit: Maximum number of bookmarks to return (default 50)

        Returns:
            List of bookmarked memory dicts
        """
        if self._client:
            return self._client.bookmarks(limit=limit)
        try:
            return self._engine.store.get_bookmarks(limit=limit)
        except Exception:
            return []

    def close(self):
        """Close the memory system and release resources."""
        if self._engine:
            self._engine.close()

    def _get_explore_recommendations(self, limit=3):
        """Get popular/recent memories as explore recommendations."""
        recommendations = []

        try:
            # 1. "On this day" — memories from 7/30/365 days ago
            import time as _time
            now = _time.time()
            for days_ago in [7, 30, 365]:
                target_ts = now - (days_ago * 86400)
                day_start = target_ts - (target_ts % 86400)
                day_end = day_start + 86400

                rows = self._engine.store.query(
                    time_from=int(day_start),
                    time_to=int(day_end),
                    limit=1,
                )
                if rows:
                    r = rows[0]
                    label = f"{days_ago}天前的今天" if days_ago < 365 else "去年的今天"
                    recommendations.append({
                        "memory_id": r.get("memory_id", ""),
                        "content": (r.get("content") or "")[:80],
                        "reason": label,
                    })
                    if len(recommendations) >= limit:
                        break
        except Exception:
            pass

        # 2. Fallback: most recent memories
        if len(recommendations) < limit:
            try:
                recent = self._engine.store.query(limit=limit - len(recommendations))
                for r in recent:
                    if r.get("content"):
                        recommendations.append({
                            "memory_id": r.get("memory_id", ""),
                            "content": (r.get("content") or "")[:80],
                            "reason": "最近存储",
                        })
            except Exception:
                pass

        return recommendations[:limit]

    def _generate_save_tip(self, status: str = "", reason: str = "", quality_level: str = None, content: str = "") -> str:
        """Generate a contextual tip after save operations."""
        if status == "filtered":
            return "内容可能与已有记忆太相似，或未通过质量检查。"
        if status == "duplicate":
            return "类似记忆已存在，如需修改请使用 update()。"
        if status == "cooldown":
            return "同一主题写入太快，请稍等几秒。"
        if status == "circuit_open":
            return "系统暂时不可用，请稍后重试。"
        if quality_level == "trivial":
            return "内容信息量较少，添加更多细节可以让未来的搜索更精准。"
        if quality_level == "low":
            return "内容较简短，补充更多上下文可以提升检索效果。"
        if status == "stored" and content and len(content.strip()) < 20:
            return "添加更多上下文信息，有助于未来搜索时找到这条记忆。"

        # Milestone-based tips
        if status == "stored":
            try:
                count = self._engine.store.count()
                if count == 1:
                    return "好的开始！继续添加记忆，搜索效果会越来越好。"
                if count == 10:
                    return "已存储10条记忆！试试用 recall 搜索看看效果。"
                if count == 100:
                    return "100条记忆！你的知识库正在壮大。"
            except Exception:
                pass

        return ""

    def _generate_save_message(self, status: str, reason: str = "") -> str:
        """Generate human-readable message for save result."""
        messages = {
            "stored": "记忆已存储",
            "filtered": f"记忆被过滤：{reason}" if reason else "记忆被过滤",
            "duplicate": "类似记忆已存在",
            "cooldown": "写入太快，请稍慢",
            "circuit_open": "系统暂时不可用",
            "error": f"错误：{reason}" if reason else "未知错误",
        }
        return messages.get(status, reason or status)

    def _check_milestone(self):
        """Check if any achievement milestone was unlocked."""
        try:
            if not self._engine:
                return None

            # Try to use the achievement system
            achievements = getattr(self._engine, '_achievements', None)
            if achievements is None:
                # Try to get from growth module
                try:
                    from agent_memory.growth.achievements import AchievementSystem
                    achievements = AchievementSystem(self._engine.store)
                except (ImportError, Exception):
                    return None

            if achievements is None:
                return None

            stats = achievements.compute_stats()
            result = achievements.check_achievements(stats)
            if result and result:
                new = result[0]  # First new achievement
                return {
                    "name": new.get("name", "Achievement Unlocked"),
                    "icon": new.get("icon", "🏆"),
                    "message": new.get("description", "You unlocked a new achievement!"),
                }
            return None
        except Exception:
            return None

    def milestones(self) -> list:
        """View all achievement milestones (unlocked and locked)."""
        if self._client:
            return self._client.milestones()

        try:
            from agent_memory.growth.achievements import AchievementSystem
            achievements = AchievementSystem(self._engine.store)
            all_achievements = achievements.get_achievements()

            result = []
            for a in all_achievements:
                result.append({
                    "name": a.get("name", ""),
                    "icon": a.get("icon", "🔒"),
                    "description": a.get("description", ""),
                    "unlocked": a.get("unlocked", False),
                })
            return result
        except Exception:
            return []

    def share_card(self, card_type: str = "stats") -> str:
        """Generate a shareable HTML card.

        Args:
            card_type: "stats" for statistics card, "recall" for search results card

        Returns:
            HTML string of the share card
        """
        if self._client:
            return self._client.share_card(card_type=card_type)

        try:
            from agent_memory.growth.share_card import ShareCardGenerator
            generator = ShareCardGenerator(self._engine.store)

            if card_type == "stats":
                return generator.generate_stat_card()
            else:
                return generator.render_to_html({"type": card_type})
        except ImportError:
            return "<p>Share card feature requires growth module</p>"
        except Exception as e:
            return f"<p>Could not generate share card: {e}</p>"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __repr__(self):
        mode = "remote" if self._client else "local"
        if self._engine:
            try:
                count = self._engine.store.count()
            except Exception:
                count = "?"
            return f"Memory(mode={mode}, memories={count})"
        return f"Memory(mode={mode}, server={self._server})"
