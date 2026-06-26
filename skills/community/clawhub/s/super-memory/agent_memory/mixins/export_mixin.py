from __future__ import annotations

import json
import logging
import os
import time
import uuid

logger = logging.getLogger(__name__)

# Import size limits
MAX_IMPORT_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_IMPORT_RECORDS = 100_000  # Max records per import


class ExportMixin:
    def export_json(
        self,
        output_path: str,
        tenant_id: str | None = None,
        batch_size: int = 1000,
        offset: int = 0,
        limit: int | None = None,
    ) -> dict:
        """
        全量导出为 JSON（含所有维度），支持租户隔离和分批流式导出。

        流式写入：每批查询结果直接写入文件，避免一次性加载所有记忆到内存导致 OOM。

        参数:
            output_path: 导出文件路径
            tenant_id: 租户 ID（为 None 时导出全部，指定时仅导出该租户数据）
            batch_size: 每批查询的记录数（避免一次性加载过多数据）
            offset: 起始偏移量（用于分页导出）
            limit: 最大导出条数（None 表示不限制，导出全部）
        """
        total_exported = 0
        current_offset = offset

        # 获取总记录数（用于元数据）
        total_count = self._count_memories(tenant_id)

        try:
            version = __version__
        except NameError:
            version = "0.0.0"

        with open(output_path, "w", encoding="utf-8") as f:
            # Write JSON header
            f.write('{\n')
            f.write(f'  "version": {json.dumps(version)},\n')
            f.write(f'  "exported_at": {json.dumps(time.strftime("%Y-%m-%dT%H:%M:%S"))},\n')
            f.write(f'  "tenant_id": {json.dumps(tenant_id)},\n')
            f.write(f'  "total_count": {total_count},\n')
            f.write(f'  "offset": {offset},\n')
            f.write('  "memories": [\n')

            first = True
            while True:
                batch_limit = min(batch_size, limit - total_exported) if limit else batch_size
                if batch_limit <= 0:
                    break

                if tenant_id:
                    memories = self._query_by_tenant(tenant_id, batch_limit, current_offset)
                else:
                    memories = self.store.query(
                        limit=batch_limit,
                        offset=current_offset,
                    )

                if not memories:
                    break

                for mem in memories:
                    record = {
                        "memory_id": mem["memory_id"],
                        "time_id": mem.get("time_id", ""),
                        "time_ts": mem.get("time_ts", 0),
                        "person_id": mem.get("person_id", ""),
                        "nature_id": mem.get("nature_id", ""),
                        "content": mem.get("content", ""),
                        "content_hash": mem.get("content_hash", ""),
                        "importance": mem.get("importance", "medium"),
                        "topics": mem.get("topics", []),
                        "tools": mem.get("tools", []),
                        "knowledge": mem.get("knowledge", []),
                        "is_aggregated": bool(mem.get("is_aggregated", 0)),
                        "source_count": mem.get("source_count", 1),
                    }
                    if not first:
                        f.write(",\n")
                    first = False
                    json.dump(record, f, ensure_ascii=False, default=str)
                    total_exported += 1

                current_offset += len(memories)

                # 如果本批数据少于请求数量，说明已经没有更多数据
                if len(memories) < batch_limit:
                    break

            f.write('\n  ]\n}\n')

        return {
            "exported": total_exported,
            "total_count": total_count,
            "file": output_path,
            "tenant_id": tenant_id,
        }

    def export_csv(
        self,
        output_path: str,
        tenant_id: str | None = None,
        batch_size: int = 1000,
        offset: int = 0,
        limit: int | None = None,
    ) -> dict:
        """
        导出为 CSV（扁平化，方便 Excel/数据分析工具），支持租户隔离和分批导出。

        参数:
            output_path: 导出文件路径
            tenant_id: 租户 ID（为 None 时导出全部，指定时仅导出该租户数据）
            batch_size: 每批查询的记录数
            offset: 起始偏移量
            limit: 最大导出条数（None 表示不限制）
        """
        import csv

        total_exported = 0
        current_offset = offset
        first_batch = True

        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)

            while True:
                batch_limit = min(batch_size, limit - total_exported) if limit else batch_size
                if batch_limit <= 0:
                    break

                if tenant_id:
                    memories = self._query_by_tenant(tenant_id, batch_limit, current_offset)
                else:
                    memories = self.store.query(
                        limit=batch_limit,
                        offset=current_offset,
                    )

                if not memories:
                    break

                if first_batch:
                    writer.writerow([
                        "memory_id", "time_id", "time_ts", "person_id", "nature_id",
                        "content", "importance", "topics", "is_aggregated",
                    ])
                    first_batch = False

                for mem in memories:
                    topics = mem.get("topics", [])
                    topic_str = ";".join(
                        t.get("code", "") if isinstance(t, dict) else t for t in topics
                    )
                    writer.writerow([
                        mem["memory_id"],
                        mem.get("time_id", ""),
                        mem.get("time_ts", 0),
                        mem.get("person_id", ""),
                        mem.get("nature_id", ""),
                        mem.get("content", "")[:500],  # CSV 截断
                        mem.get("importance", "medium"),
                        topic_str,
                        bool(mem.get("is_aggregated", 0)),
                    ])

                total_exported += len(memories)
                current_offset += len(memories)

                if len(memories) < batch_limit:
                    break

        total_count = self._count_memories(tenant_id)

        return {
            "exported": total_exported,
            "total_count": total_count,
            "file": output_path,
            "tenant_id": tenant_id,
        }

    def import_json(
        self,
        file_path: str,
        tenant_id: str | None = None,
        merge_strategy: str = "skip",
    ) -> dict:
        """
        从 JSON 文件导入记忆数据（含文件大小和记录数限制）。

        参数:
            file_path: 导入文件路径
            tenant_id: 导入到的目标租户 ID（None 表示使用导出时的租户或默认）
            merge_strategy: 冲突合并策略
                - 'skip': 跳过已存在的记录（按 memory_id 判断）
                - 'overwrite': 覆盖已存在的记录
                - 'rename': 为冲突记录生成新的 memory_id

        返回: {"total": int, "imported": int, "skipped": int, "errors": list}
        """
        # 文件存在性检查
        if not os.path.exists(file_path):
            return {"total": 0, "imported": 0, "skipped": 0, "errors": [f"文件不存在: {file_path}"]}

        # 文件大小检查
        file_size = os.path.getsize(file_path)
        if file_size > MAX_IMPORT_FILE_SIZE:
            return {
                "total": 0,
                "imported": 0,
                "skipped": 0,
                "errors": [f"文件过大（{file_size / 1024 / 1024:.1f}MB），最大允许 {MAX_IMPORT_FILE_SIZE / 1024 / 1024:.0f}MB"],
            }

        # 加载并验证 JSON
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return {"total": 0, "imported": 0, "skipped": 0, "errors": [f"JSON 格式错误: {e}"]}
        except Exception as e:
            return {"total": 0, "imported": 0, "skipped": 0, "errors": [f"文件读取失败: {e}"]}

        # 提取 memories 列表
        if isinstance(data, dict):
            memories = data.get("memories", [])
        elif isinstance(data, list):
            memories = data
        else:
            return {"total": 0, "imported": 0, "skipped": 0, "errors": ["文件内容必须是 JSON 对象或数组"]}

        # 记录数检查
        if len(memories) > MAX_IMPORT_RECORDS:
            return {
                "total": 0,
                "imported": 0,
                "skipped": 0,
                "errors": [f"记录数过多（{len(memories)}），最大允许 {MAX_IMPORT_RECORDS}"],
            }

        # 验证 memories 为 list
        if not isinstance(memories, list):
            return {"total": 0, "imported": 0, "skipped": 0, "errors": ["数据格式错误: memories 应为 list"]}

        if merge_strategy not in ("skip", "overwrite", "rename"):
            return {"total": 0, "imported": 0, "skipped": 0, "errors": [f"无效的合并策略: {merge_strategy}"]}

        total = len(memories)
        imported = 0
        skipped = 0
        errors = []

        for i, mem in enumerate(memories):
            try:
                # 验证必要字段
                if not isinstance(mem, dict):
                    errors.append(f"记录 {i}: 不是 dict 类型，跳过")
                    continue

                memory_id = mem.get("memory_id", "")
                if not memory_id:
                    errors.append(f"记录 {i}: 缺少 memory_id，跳过")
                    continue

                content = mem.get("content", "")
                if not content:
                    errors.append(f"记录 {i}: 缺少 content，跳过")
                    continue

                # 检查是否已存在
                existing = self.store.get_memory(memory_id)

                if existing:
                    if merge_strategy == "skip":
                        skipped += 1
                        continue
                    elif merge_strategy == "rename":
                        memory_id = f"{memory_id}_import_{uuid.uuid4().hex[:8]}"
                    # overwrite: 使用 INSERT OR REPLACE（SQLite 原子操作，避免 delete+insert 间隙丢数据）
                    # skip 和 rename 走下面的 INSERT OR IGNORE / 正常插入

                # 构建导入参数
                import time as _time
                time_ts = mem.get("time_ts", int(_time.time()))
                content_hash = mem.get("content_hash", "")
                if not content_hash:
                    import hashlib
                    content_hash = hashlib.sha256(content.encode()).hexdigest()

                # 处理 topics
                topics = mem.get("topics", [])
                if isinstance(topics, list):
                    topic_codes = [
                        t.get("code", t) if isinstance(t, dict) else t
                        for t in topics
                        if t
                    ]
                else:
                    topic_codes = []

                # 处理 tools
                tools = mem.get("tools", [])
                if not isinstance(tools, list):
                    tools = []

                # 处理 knowledge
                knowledge = mem.get("knowledge", [])
                if not isinstance(knowledge, list):
                    knowledge = []

                # 生成 time_id
                time_id = mem.get("time_id", "")
                if not time_id:
                    time_id = f"d{time_ts}"

                self.store.insert_memory(
                    memory_id=memory_id,
                    time_id=time_id,
                    time_ts=time_ts,
                    person_id=mem.get("person_id", ""),
                    nature_id=mem.get("nature_id", ""),
                    content=content,
                    content_hash=content_hash,
                    topics=topic_codes,
                    tools=tools,
                    knowledge_types=knowledge,
                    importance=mem.get("importance", "medium"),
                    is_aggregated=mem.get("is_aggregated", False),
                    source_count=mem.get("source_count", 1),
                    upsert=(merge_strategy == "overwrite"),
                )
                imported += 1

            except Exception as e:
                errors.append(f"记录 {i} ({memory_id if memory_id else 'unknown'}): {e}")
                logger.warning("import_json: 记录 %d 导入失败: %s", i, e)

        return {
            "total": total,
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
        }

    def _count_memories(self, tenant_id: str | None = None) -> int:
        """获取记忆总数（支持租户过滤）。"""
        try:
            conn = self.store.conn
            if tenant_id:
                # 检查是否有 tenant_id 列
                try:
                    cols = {
                        row["name"]
                        for row in conn.execute("PRAGMA table_info(memories)").fetchall()
                    }
                    if "tenant_id" in cols:
                        row = conn.execute(
                            "SELECT COUNT(*) FROM memories WHERE tenant_id = ? AND deleted=0",
                            (tenant_id,),
                        ).fetchone()
                        return row[0] if row else 0
                except Exception:
                    pass
            # 无租户过滤或无 tenant_id 列，返回总数
            return self.store.count()
        except Exception:
            return 0

    def _query_by_tenant(self, tenant_id: str, limit: int, offset: int) -> list[dict]:
        """按租户 ID 查询记忆（直接 SQL，因为 store.query() 暂不支持 tenant_id）。"""
        try:
            conn = self.store.conn
            # 检查是否有 tenant_id 列
            cols = {
                row["name"]
                for row in conn.execute("PRAGMA table_info(memories)").fetchall()
            }
            if "tenant_id" not in cols:
                logger.warning("tenant_id column not found in memories table, returning all")
                return self.store.query(limit=limit, offset=offset)

            rows = conn.execute(
                "SELECT * FROM memories WHERE tenant_id = ? AND deleted=0 ORDER BY time_ts DESC LIMIT ? OFFSET ?",
                (tenant_id, limit, offset),
            ).fetchall()

            memory_ids = [row["memory_id"] for row in rows]
            topics_map = self.store._batch_get_topics(memory_ids)
            tools_map = self.store._batch_get_tools(memory_ids)
            knowledge_map = self.store._batch_get_knowledge(memory_ids)

            results = []
            for row in rows:
                mem = dict(row)
                mid = mem["memory_id"]
                mem["topics"] = topics_map.get(mid, [])
                mem["tools"] = tools_map.get(mid, [])
                mem["knowledge"] = knowledge_map.get(mid, [])
                results.append(mem)
            return results
        except Exception as e:
            logger.warning("_query_by_tenant failed: %s", e)
            return self.store.query(limit=limit, offset=offset)

    def auto_backup(self, backup_dir: str = None, keep_days: int = 7) -> dict:
        """
        自动备份数据库 + 向量库。

        保留最近 keep_days 天的备份，超期自动清理。
        """
        import os
        import glob
        from datetime import datetime, timedelta

        backup_dir = backup_dir or os.path.join(self._project_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)

        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_backup = os.path.join(backup_dir, f"memory_{now_str}.db")

        # 备份 SQLite
        self.store.backup(db_backup)

        # 备份质量统计
        q_path = os.path.join(self._project_dir, "quality_stats.json")
        if os.path.exists(q_path):
            import shutil
            shutil.copy2(q_path, os.path.join(backup_dir, f"quality_{now_str}.json"))

        # 清理过期备份
        cutoff = datetime.now() - timedelta(days=keep_days)
        cleaned = 0
        for pattern in ["memory_*.db", "quality_*.json"]:
            for f in glob.glob(os.path.join(backup_dir, pattern)):
                try:
                    # 从文件名提取时间
                    basename = os.path.basename(f)
                    parts = basename.split("_")
                    if len(parts) >= 2:
                        date_str = parts[1].split(".")[0]
                        file_date = datetime.strptime(date_str, "%Y%m%d")
                        if file_date < cutoff:
                            os.unlink(f)
                            cleaned += 1
                except Exception as e:
                    logger.warning("memory_system: %s", e)

        return {
            "db_backup": db_backup,
            "cleaned_old": cleaned,
            "backup_dir": backup_dir,
        }
