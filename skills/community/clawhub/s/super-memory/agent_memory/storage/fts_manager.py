from __future__ import annotations

import logging
import re
import threading

logger = logging.getLogger(__name__)

# jieba 分词器（懒加载，线程安全）
_jieba = None
_jieba_initialized = False
_jieba_lock = threading.Lock()


def _get_jieba():
    """懒加载 jieba 分词器（double-check locking）"""
    global _jieba, _jieba_initialized
    if _jieba_initialized:
        return _jieba
    with _jieba_lock:
        if _jieba_initialized:
            return _jieba
        _jieba_initialized = True
        try:
            import jieba
            _jieba = jieba
            logger.info("jieba 中文分词器已加载")
        except ImportError:
            logger.info("jieba 未安装，中文分词不可用。安装: pip install jieba")
    return _jieba


def _tokenize_chinese(text: str) -> str:
    """对文本做中文分词，返回空格分隔的分词结果。

    jieba 可用时：中文部分分词，非中文部分保留原样
    jieba 不可用时：返回原文
    """
    jieba = _get_jieba()
    if not jieba or not text:
        return text

    # 分离中文和非中文部分
    parts = re.split(r'([\u4e00-\u9fff\u3400-\u4dbf]+)', text)
    result = []
    for i, part in enumerate(parts):
        if re.match(r'[\u4e00-\u9fff\u3400-\u4dbf]+', part):
            # 中文部分：jieba 分词
            words = list(jieba.cut(part))
            result.extend(words)
        else:
            # 非中文部分：按空格分词
            tokens = part.strip().split()
            result.extend(tokens)

    return " ".join(result)


class FTSManager:
    def __init__(self, conn_provider):
        self._get_conn = conn_provider
        self._has_fts = False

    @property
    def has_fts(self) -> bool:
        return self._has_fts

    @has_fts.setter
    def has_fts(self, value: bool):
        self._has_fts = value

    def init_fts(self):
        # 尝试 trigram tokenizer（对中文支持好），不可用则回退 unicode61
        for tokenizer in ("trigram", "unicode61"):
            try:
                self._get_conn().execute(f"""
                    CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                        memory_id UNINDEXED,
                        content,
                        tokenize='{tokenizer}'
                    )
                """)
                count = self._get_conn().execute("SELECT COUNT(*) FROM memories_fts").fetchone()[0]
                mem_count = self._get_conn().execute("SELECT COUNT(*) FROM memories WHERE deleted=0").fetchone()[0]
                if count < mem_count:
                    logger.info(f"FTS 同步: {mem_count - count} 条记忆")
                    self._get_conn().execute("DELETE FROM memories_fts")
                    # v12: 中文内容做 jieba 分词后再写入 FTS，提升 unicode61 下的中文匹配率
                    self._sync_memories_to_fts()
                self._get_conn().commit()
                self._has_fts = True
                logger.info(f"FTS5 初始化成功 (tokenizer={tokenizer})")
                return
            except Exception as e:
                logger.warning(f"FTS5 tokenizer '{tokenizer}' 不可用: {e}")
                # 清理失败的表
                try:
                    self._get_conn().execute("DROP TABLE IF EXISTS memories_fts")
                except Exception:
                    pass
                continue
        self._has_fts = False

    def rebuild_fts(self) -> dict:
        self._get_conn().execute("DROP TABLE IF EXISTS memories_fts")
        self._get_conn().commit()

        for tokenizer in ("trigram", "unicode61"):
            try:
                self._get_conn().execute(f"""
                    CREATE VIRTUAL TABLE memories_fts USING fts5(
                        memory_id UNINDEXED,
                        content,
                        tokenize='{tokenizer}'
                    )
                """)

                # v12: 中文内容做 jieba 分词后再写入 FTS
                self._sync_memories_to_fts()
                self._get_conn().commit()

                count = self._get_conn().execute("SELECT COUNT(*) FROM memories_fts").fetchone()[0]
                self._has_fts = True
                logger.info(f"FTS 索引重建完成: {count} 条 (tokenizer={tokenizer})")
                return {"rebuilt": True, "count": count, "error": None}
            except Exception as e:
                logger.warning(f"FTS rebuild tokenizer '{tokenizer}' 失败: {e}")
                try:
                    self._get_conn().execute("DROP TABLE IF EXISTS memories_fts")
                except Exception:
                    pass
                continue

        self._has_fts = False
        return {"rebuilt": False, "count": 0, "error": "no available tokenizer"}

    def query_fts(self, keyword: str, limit: int) -> list[dict]:
        try:
            # v12: 中文查询做 jieba 分词
            tokenized_keyword = _tokenize_chinese(keyword)
            if tokenized_keyword != keyword:
                logger.debug(f"FTS 中文分词: '{keyword}' -> '{tokenized_keyword}'")

            search_keyword = tokenized_keyword if len(tokenized_keyword.strip()) >= 3 else keyword

            if len(search_keyword.strip()) < 3:
                rows = self._get_conn().execute(
                    "SELECT * FROM memories WHERE deleted=0 AND content LIKE ? ORDER BY time_ts DESC LIMIT ?",
                    (f"%{keyword}%", limit),
                ).fetchall()
                return [dict(r) for r in rows]

            safe_keyword = search_keyword.replace('"', '""')
            safe_keyword = re.sub(r'\b(NOT|AND|OR|NEAR)\b', ' ', safe_keyword, flags=re.IGNORECASE)
            safe_keyword = safe_keyword.replace('+', ' ').replace('-', ' ')
            words = [w.strip() for w in safe_keyword.split() if len(w.strip()) >= 1]
            if not words:
                words = [safe_keyword]

            match_expr = " OR ".join(f'"{w}"*' for w in words)
            rows = self._get_conn().execute(
                """SELECT m.* FROM memories m
                   JOIN memories_fts fts ON m.memory_id = fts.memory_id
                   WHERE m.deleted=0 AND memories_fts MATCH ?
                   ORDER BY rank
                   LIMIT ?""",
                (match_expr, limit),
            ).fetchall()

            if not rows and self.is_cjk_query(keyword):
                logger.debug(f"FTS 返回 0 结果，CJK LIKE 回退: {keyword}")
                rows = self.like_fallback_cjk(keyword, limit)

            return [dict(r) for r in rows]
        except Exception as e:
            logger.warning(f"FTS 查询异常，触发自动重建: {e}")
            try:
                self.rebuild_fts()
            except Exception as e:
                logger.warning("store: %s", e)
            return self.like_fallback_cjk(keyword, limit)

    def like_fallback_cjk(self, keyword: str, limit: int) -> list[dict]:
        try:
            # 先用完整 keyword 做 LIKE
            rows = self._get_conn().execute(
                "SELECT * FROM memories WHERE deleted=0 AND content LIKE ? ORDER BY time_ts DESC LIMIT ?",
                (f"%{keyword}%", limit),
            ).fetchall()
            if rows:
                return [dict(r) for r in rows]

            # 对空格分隔的多词，逐词 LIKE 并取并集
            words = [w.strip() for w in keyword.split() if len(w.strip()) >= 1]
            if len(words) > 1:
                like_parts = []
                params = []
                for w in words:
                    like_parts.append("content LIKE ?")
                    params.append(f"%{w}%")
                rows = self._get_conn().execute(
                    f"SELECT * FROM memories WHERE deleted=0 AND ({' OR '.join(like_parts)}) ORDER BY time_ts DESC LIMIT ?",
                    params + [limit],
                ).fetchall()
                if rows:
                    return [dict(r) for r in rows]

            # CJK bigram 回退
            cjk_chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]+', keyword)
            if not cjk_chars:
                return []
            like_parts = []
            for segment in cjk_chars:
                for i in range(len(segment) - 1):
                    bigram = segment[i:i+2]
                    if bigram not in like_parts:
                        like_parts.append(bigram)

            if not like_parts:
                return []

            _MAX_LIKE_PARTS = 10
            if len(like_parts) > _MAX_LIKE_PARTS:
                logger.warning(
                    "CJK LIKE bigram 截断: %d -> %d (keyword=%r)",
                    len(like_parts), _MAX_LIKE_PARTS, keyword,
                )
                like_parts = like_parts[:_MAX_LIKE_PARTS]

            conditions = " OR ".join(["content LIKE ?"] * len(like_parts))
            params = [f"%{bg}%" for bg in like_parts]
            rows = self._get_conn().execute(
                f"SELECT * FROM memories WHERE deleted=0 AND ({conditions}) ORDER BY time_ts DESC LIMIT ?",
                params + [limit],
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            logger.debug("store: CJK LIKE fallback: %s", e)
            return []

    @staticmethod
    def is_cjk_query(text: str) -> bool:
        return bool(re.search(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))

    def _sync_memories_to_fts(self):
        """将 memories 表数据同步到 FTS，中文内容做 jieba 分词。

        分词后的内容写入 FTS 索引，使得 unicode61 tokenizer 也能
        通过空格分词正确匹配中文。
        """
        rows = self._get_conn().execute(
            "SELECT memory_id, content FROM memories WHERE deleted=0"
        ).fetchall()

        for row in rows:
            mid = row["memory_id"] if isinstance(row, dict) else row[0]
            content = row["content"] if isinstance(row, dict) else row[1]
            # 对中文内容做分词
            tokenized = _tokenize_chinese(content)
            self._get_conn().execute(
                "INSERT INTO memories_fts(memory_id, content) VALUES (?, ?)",
                (mid, tokenized),
            )
