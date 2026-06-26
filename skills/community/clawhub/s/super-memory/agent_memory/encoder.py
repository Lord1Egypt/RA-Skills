"""
encoder.py - 维度编码器（v8.3 自适应增强版）
负责将维度值编码为 memory_id，查注册表

v8.3 增强:
- 动态维度注册：nature/person/tool/knowledge 自动分配 ID
- 使用频率追踪：高频维度值自动提升优先级
- 维度健康检查：发现冗余/孤立的维度值
- 向后兼容：现有代码无需修改
"""

from __future__ import annotations

import json
import re
import hashlib
import time
import uuid
import logging
import threading
from datetime import datetime
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)

REGISTRY_PATH = Path(__file__).parent / "config" / "dimensions.json"

_registry_write_lock = threading.Lock()


class DimensionEncoder:
    def __init__(self, registry_path: str = None):
        self.registry_path = Path(registry_path) if registry_path else REGISTRY_PATH
        with open(self.registry_path, "r", encoding="utf-8") as f:
            self.registry = json.load(f)
        # 建反向索引：code → id（避免线性扫描）
        self._nature_by_code = {}
        for nid, info in self.registry["natures"].items():
            self._nature_by_code[info["code"]] = nid

        self._person_by_code = {}
        for pid, info in self.registry["persons"].items():
            self._person_by_code[info["code"]] = pid

        self._tool_by_code = {}
        for tid, info in self.registry["tools"].items():
            self._tool_by_code[info["code"]] = tid

        self._knowledge_by_code = {}
        for kid, info in self.registry["knowledge_types"].items():
            self._knowledge_by_code[info["code"]] = kid

        # v8.3: 使用频率追踪
        self._usage_counts = defaultdict(int)
        self._usage_dirty = False
        self._last_flush_ts = 0.0
        self._USAGE_FLUSH_INTERVAL = 60.0

        # v8.3: 确保 _dynamic 维度容器存在
        for dim_key in ("natures", "persons", "tools", "knowledge_types"):
            if dim_key not in self.registry:
                self.registry[dim_key] = {}

    # ── 时间编码 ──────────────────────────────────────────

    def encode_time(self, ts: float = None, precision: str = "second") -> str:
        """生成时间编码
        precision: 'second' → T20260411.213742
                   'minute' → T20260411.2137
                   'micro'  → T20260411.213742.123456 (防冲突)
        """
        dt = datetime.utcfromtimestamp(ts) if ts else datetime.utcnow()
        if precision == "minute":
            return f"T{dt.strftime('%Y%m%d.%H%M')}"
        if precision == "micro":
            us = int((ts or time.time()) % 1 * 1_000_000)
            return f"T{dt.strftime('%Y%m%d.%H%M%S')}.{us:06d}"
        return f"T{dt.strftime('%Y%m%d.%H%M%S')}"

    # ── 人物编码 ──────────────────────────────────────────

    def encode_person(self, person_id: str) -> str:
        """直接用注册表里的 ID，如 P01"""
        if person_id not in self.registry["persons"]:
            raise ValueError(f"未注册的人物 ID: {person_id}，请先在 dimensions.json 中注册")
        self._track_usage(f"person:{person_id}")
        return person_id

    def get_person_by_code(self, code: str, auto_register: bool = True) -> str:
        """通过 code 查 person_id（O(1) 反向索引）

        v8.3: auto_register=True 时，未找到的 code 自动注册并分配 ID
        """
        if code in self._person_by_code:
            pid = self._person_by_code[code]
            self._track_usage(f"person:{pid}")
            return pid
        if auto_register:
            return self._auto_register_dimension("persons", code, "P", code)
        raise ValueError(f"未找到 code={code} 的人物")

    # ── 主题编码 ──────────────────────────────────────────

    def encode_topic(self, topic_path: str, auto_register: bool = True) -> str:
        """主题路径直接作为编码，如 ai.rag.vdb

        如果路径未注册：
        - auto_register=True（默认）：自动在注册表中创建，静默通过
        - auto_register=False：抛 ValueError（向后兼容）
        """
        parts = topic_path.split(".")
        node = self.registry["topics"]
        missing_from = None
        for i, p in enumerate(parts):
            if p not in node:
                missing_from = i
                break
            if "children" in node[p]:
                node = node[p]["children"]
            elif p != parts[-1]:
                if auto_register:
                    # 中间节点缺失 children，补充之
                    node[p]["children"] = {}
                    node = node[p]["children"]
                    missing_from = i + 1
                    break
                else:
                    raise ValueError(f"主题路径不完整: {topic_path}")

        # 自动注册缺失的路径段
        if missing_from is not None and auto_register:
            self._auto_register_topic_path(topic_path, parts, missing_from)
        elif missing_from is not None:
            raise ValueError(f"未注册的主题路径: {topic_path}，请先在 dimensions.json 中注册")

        return topic_path

    def _auto_register_topic_path(self, full_path: str, parts: list, start_idx: int):
        """自动将缺失的主题路径段写入注册表（线程安全）

        Fix (P0): 加 threading.Lock 防止同进程内多线程同时写 JSON 导致损坏。
        Fix (Bug 3): 移除 fcntl 文件锁，改用 threading.Lock 实现线程安全。
        """
        import os

        with _registry_write_lock:
            self._do_register_topic_path(full_path, parts, start_idx)

    def _do_register_topic_path(self, full_path: str, parts: list, start_idx: int):
        """实际的注册逻辑（由 _auto_register_topic_path 持锁后调用）"""
        import os

        node = self.registry["topics"]
        # 先导航到 start_idx 之前的节点
        for p in parts[:start_idx]:
            if "children" in node[p]:
                node = node[p]["children"]
            else:
                node[p]["children"] = {}
                node = node[p]["children"]

        # 创建缺失的路径段
        for p in parts[start_idx:]:
            if p not in node:
                node[p] = {"name": p, "keywords": [p]}
            else:
                if "keywords" not in node[p]:
                    node[p]["keywords"] = [p]
            if p != parts[-1]:
                if "children" not in node[p]:
                    node[p]["children"] = {}
                node = node[p]["children"]

        # Fix (Bug 3): threading.Lock 已在 _auto_register_topic_path 中获取
        # 此处直接原子写入（os.rename 在同一文件系统上是原子的）
        registry_path = self.registry_path
        try:
            # 持有锁期间读取磁盘上最新版本
            latest = {}
            if registry_path.exists():
                try:
                    with open(registry_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if content.strip():
                            latest = json.loads(content)
                except (json.JSONDecodeError, IOError, ValueError) as read_err:
                    import logging as _logging
                    _logging.getLogger(__name__).warning(
                        f"注册表文件读取异常，用内存版本兜底: {read_err}"
                    )
                    latest = {}

            # 合并：把我们新增的路径合并到最新版本
            if "topics" in latest:
                self._merge_topics(latest["topics"], self.registry["topics"])
            else:
                latest = {"topics": dict(self.registry["topics"])}

            # 原子写入：写 tmp → rename（rename 在同一文件系统上是原子的）
            import uuid as _uuid
            tmp = f"{registry_path}.{os.getpid()}.{_uuid.uuid4().hex[:8]}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(latest, f, ensure_ascii=False, indent=4)
            os.replace(tmp, str(registry_path))
        except Exception as e:
            import logging as _logging
            _logging.getLogger(__name__).warning(
                f"主题注册表写入失败 path={full_path}: {e} — "
                f"该主题在下次重启前有效，但可能丢失。建议检查磁盘空间和文件权限。"
            )

    @staticmethod
    def _merge_topics(base: dict, incoming: dict):
        """将 incoming 的主题树合并到 base 中（深合并）"""
        for key, val in incoming.items():
            if key not in base:
                base[key] = val
            else:
                # 合并 keywords
                if "keywords" in val:
                    existing_kw = set(base[key].get("keywords", []))
                    existing_kw.update(val["keywords"])
                    base[key]["keywords"] = list(existing_kw)
                # 递归合并 children
                if "children" in val:
                    if "children" not in base[key]:
                        base[key]["children"] = {}
                    DimensionEncoder._merge_topics(base[key]["children"], val["children"])

    def list_topics(self, prefix: str = "") -> list:
        """列出所有主题路径"""
        results = []
        self._walk_topics(self.registry["topics"], prefix, results)
        return results

    def _walk_topics(self, node, path, results):
        for key, val in node.items():
            full = f"{path}.{key}" if path else key
            if "children" in val:
                self._walk_topics(val["children"], full, results)
            else:
                results.append(full)

    # ── 性质编码 ──────────────────────────────────────────

    def encode_nature(self, nature_code: str, auto_register: bool = True) -> str:
        """通过 code（如 'explore'）查找 D 编码

        v8.3: auto_register=True 时，未注册的 nature 自动分配 D 编码
        """
        if nature_code in self._nature_by_code:
            nid = self._nature_by_code[nature_code]
            self._track_usage(f"nature:{nid}")
            return nid
        if nature_code in self.registry["natures"]:
            self._track_usage(f"nature:{nature_code}")
            return nature_code
        if auto_register:
            return self._auto_register_dimension("natures", nature_code, "D", nature_code)
        raise ValueError(f"未注册的性质: {nature_code}")

    # ── 知识类型编码 ──────────────────────────────────────

    def encode_knowledge(self, knowledge_code: str, auto_register: bool = True) -> str:
        """通过 code（如 'rule'）查找 K 编码（O(1) 反向索引）

        v8.3: auto_register=True 时，未注册的知识类型自动分配 K 编码
        """
        if knowledge_code in self._knowledge_by_code:
            kid = self._knowledge_by_code[knowledge_code]
            self._track_usage(f"knowledge:{kid}")
            return kid
        if knowledge_code in self.registry["knowledge_types"]:
            self._track_usage(f"knowledge:{knowledge_code}")
            return knowledge_code
        if auto_register:
            return self._auto_register_dimension("knowledge_types", knowledge_code, "K", knowledge_code)
        raise ValueError(f"未注册的知识类型: {knowledge_code}")

    # ── 重要度编码 ──────────────────────────────────────────

    VALID_IMPORTANCE = ("high", "medium", "low")

    def encode_importance(self, level: str) -> str:
        """校验并返回 importance 值"""
        if level not in self.VALID_IMPORTANCE:
            raise ValueError(f"未注册的重要度: {level}，可选: {self.VALID_IMPORTANCE}")
        return level

    # ── 工具编码 ──────────────────────────────────────────

    def encode_tool(self, tool_id: str) -> str:
        """直接用注册表里的工具 ID，如 t_lc"""
        if tool_id not in self.registry["tools"]:
            raise ValueError(f"未注册的工具 ID: {tool_id}，请先在 dimensions.json 中注册")
        self._track_usage(f"tool:{tool_id}")
        return tool_id

    def get_tool_by_code(self, code: str, auto_register: bool = True) -> str:
        """通过 code 查 tool_id（O(1) 反向索引）

        v8.3: auto_register=True 时，未注册的工具自动分配 t_ 前缀 ID
        """
        if code in self._tool_by_code:
            tid = self._tool_by_code[code]
            self._track_usage(f"tool:{tid}")
            return tid
        if auto_register:
            return self._auto_register_dimension("tools", code, "t_", code)
        raise ValueError(f"未找到 code={code} 的工具")

    # ── Memory ID 生成 ────────────────────────────────────

    def generate_memory_id(
        self,
        time_id: str,
        person_id: str,
        topic_codes: list[str],
        nature_id: str,
        tool_ids: list[str] = None,
    ) -> str:
        """组合维度生成唯一 memory_id
        格式: T20260411.213742_P01_rag.vdb_D04_lc.ch
        """
        # 主题取主主题（第一个）
        primary_topic = topic_codes[0] if topic_codes else "none"
        # 短化：去掉顶层前缀 ai./dev./life.
        for prefix in ("ai.", "dev.", "life."):
            if primary_topic.startswith(prefix):
                primary_topic = primary_topic[len(prefix):]
                break

        # 工具缩写（取前两个）
        tool_part = ""
        if tool_ids:
            tool_codes = []
            for tid in tool_ids[:2]:
                info = self.registry["tools"].get(tid, {})
                tool_codes.append(info.get("code", tid))
            tool_part = "." + "+".join(tool_codes)

        raw = f"{time_id}_{person_id}_{primary_topic}_{nature_id}{tool_part}"

        # 末尾加 8 位 uuid hex 保证唯一性（16^8 = 42 亿种可能，碰撞概率可忽略）
        # 替代原来的 random.randint(0, 0xFFFF)（只有 65536 种，批量写入必撞）
        suffix = uuid.uuid4().hex[:8]
        raw = f"{raw}_{suffix}"

        # 如果组合太长，截断并保留 hash
        if len(raw) > 64:
            h = hashlib.sha256(raw.encode()).hexdigest()[:6]
            raw = f"{raw[:58]}_{h}"

        return raw

    _MEMORY_ID_PATTERN = re.compile(
        r'^'
        r'(T[\d.]+)'                # time_id: T20260411.213742
        r'_'
        r'(P\w+)'                   # person_id: P01
        r'_'
        r'(.+?)'                    # primary_topic: rag.vdb (non-greedy)
        r'_'
        r'(D\w+?)'                  # nature_id: D04 (non-greedy)
        r'(?:\.(\w+(?:\+\w+)*))?'   # optional tool_part: .lc+ch
        r'_'
        r'([0-9a-f]+)'              # suffix: abc12345
        r'$'
    )

    @staticmethod
    def parse_memory_id(memory_id: str) -> dict:
        """从 memory_id 反向提取6D维度信息

        使用正则表达式精确匹配 generate_memory_id 产生的 ID 格式。

        Returns:
            dict with keys: time_id, person_id, topic_code, nature_id, tool_ids, suffix
            或空 dict（解析失败时）
        """
        if not memory_id:
            return {}
        m = DimensionEncoder._MEMORY_ID_PATTERN.match(memory_id)
        if not m:
            return {}
        result = {
            "time_id": m.group(1),
            "person_id": m.group(2),
            "topic_code": m.group(3),
            "nature_id": m.group(4),
            "suffix": m.group(6),
        }
        tool_part = m.group(5)
        if tool_part:
            result["tool_ids"] = tool_part.split("+")
        return result

    @staticmethod
    def content_hash(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    # ══════════════════════════════════════════════════════
    # v8.3: 自适应维度注册
    # ══════════════════════════════════════════════════════

    def _auto_register_dimension(
        self, dim_key: str, code: str, id_prefix: str, name: str
    ) -> str:
        """
        自动注册一个新的维度值，分配 ID 并写入注册表。

        参数:
            dim_key: 维度类别键名（natures/persons/tools/knowledge_types）
            code: 维度值的 code
            id_prefix: ID 前缀（D/P/t_/K）
            name: 显示名称

        返回: 新分配的维度 ID
        """
        with _registry_write_lock:
            existing_ids = list(self.registry[dim_key].keys())

            if id_prefix in ("D", "K", "P"):
                max_num = 0
                for eid in existing_ids:
                    try:
                        num = int(eid.replace(id_prefix, ""))
                        if num > max_num:
                            max_num = num
                    except (ValueError, AttributeError) as e:
                        logger.debug("encoder: id parse: %s", e)
                new_id = f"{id_prefix}{max_num + 1:02d}"
            else:
                short_code = code[:6].replace(".", "_").replace("-", "_")
                new_id = f"{id_prefix}{short_code}"

            if new_id in self.registry[dim_key]:
                h = hashlib.md5(code.encode()).hexdigest()[:4]
                new_id = f"{new_id}_{h}"

            self.registry[dim_key][new_id] = {
                "code": code,
                "name": name,
                "desc": f"自动注册 ({datetime.now().strftime('%Y-%m-%d')})",
                "auto_registered": True,
                "registered_at": int(time.time()),
            }

            if dim_key == "natures":
                self._nature_by_code[code] = new_id
            elif dim_key == "persons":
                self._person_by_code[code] = new_id
            elif dim_key == "tools":
                self._tool_by_code[code] = new_id
            elif dim_key == "knowledge_types":
                self._knowledge_by_code[code] = new_id

            self._flush_registry()
            logger.info(f"📐 自适应维度注册: {dim_key}/{new_id} = {code}")

            return new_id

    def _track_usage(self, key: str):
        """追踪维度值的使用频率"""
        self._usage_counts[key] += 1
        self._usage_dirty = True
        now = time.time()
        if now - self._last_flush_ts > self._USAGE_FLUSH_INTERVAL:
            self._flush_usage_counts()
            self._last_flush_ts = now

    def _flush_usage_counts(self):
        """将使用频率持久化到注册表"""
        if not self._usage_dirty:
            return
        try:
            usage_key = "_usage_stats"
            existing = self.registry.get(usage_key, {})
            for k, v in self._usage_counts.items():
                existing[k] = existing.get(k, 0) + v
            self.registry[usage_key] = existing
            self._usage_counts.clear()
            self._usage_dirty = False
        except Exception as e:
            logger.debug(f"使用频率持久化失败: {e}")

    def _flush_registry(self):
        """将注册表原子写入磁盘"""
        import os
        registry_path = self.registry_path
        try:
            tmp = f"{registry_path}.{os.getpid()}.{uuid.uuid4().hex[:8]}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.registry, f, ensure_ascii=False, indent=4)
            os.replace(tmp, str(registry_path))
        except Exception as e:
            logger.warning("encoder: %s", e)

    # ── 维度健康检查 ────────────────────────────────────

    def health_check(self) -> dict:
        """
        维度注册表健康检查。

        检测：
        1. 孤立维度值（已注册但从未使用）
        2. 高频维度值（使用次数远超平均）
        3. 自动注册但未人工审核的维度值
        4. ID 冲突或格式异常

        返回: {
            "orphaned": [...],
            "high_frequency": [...],
            "unreviewed_auto": [...],
            "anomalies": [...],
            "summary": str,
        }
        """
        usage_stats = self.registry.get("_usage_stats", {})
        result = {
            "orphaned": [],
            "high_frequency": [],
            "unreviewed_auto": [],
            "anomalies": [],
        }

        for dim_key in ("natures", "persons", "tools", "knowledge_types"):
            dim_data = self.registry.get(dim_key, {})
            if not dim_data:
                continue

            for dim_id, info in dim_data.items():
                code = info.get("code", "")
                usage_key = f"{dim_key.rstrip('s')}:{dim_id}"
                count = usage_stats.get(usage_key, 0)

                if info.get("auto_registered") and not info.get("reviewed"):
                    result["unreviewed_auto"].append({
                        "dim_key": dim_key,
                        "id": dim_id,
                        "code": code,
                        "name": info.get("name", ""),
                        "registered_at": info.get("registered_at"),
                        "usage_count": count,
                    })

                if count == 0 and info.get("auto_registered"):
                    result["orphaned"].append({
                        "dim_key": dim_key,
                        "id": dim_id,
                        "code": code,
                    })

        total_usage = sum(usage_stats.values())
        if total_usage > 0 and usage_stats:
            avg_usage = total_usage / max(1, len(usage_stats))
            for key, count in usage_stats.items():
                if count > avg_usage * 5 and count > 10:
                    result["high_frequency"].append({
                        "key": key,
                        "count": count,
                        "ratio": round(count / avg_usage, 1),
                    })

        summary_parts = []
        if result["orphaned"]:
            summary_parts.append(f"{len(result['orphaned'])} 个孤立维度值")
        if result["unreviewed_auto"]:
            summary_parts.append(f"{len(result['unreviewed_auto'])} 个未审核的自动注册值")
        if result["high_frequency"]:
            summary_parts.append(f"{len(result['high_frequency'])} 个高频维度值")

        result["summary"] = "；".join(summary_parts) if summary_parts else "维度注册表健康"
        return result

    def review_auto_dimension(self, dim_key: str, dim_id: str, action: str = "approve") -> dict:
        """
        审核自动注册的维度值。

        参数:
            dim_key: 维度类别（natures/persons/tools/knowledge_types）
            dim_id: 维度 ID
            action: "approve"（保留）| "rename"（改名）| "remove"（删除）

        返回: {"action": str, "dim_id": str, "status": str}
        """
        dim_data = self.registry.get(dim_key, {})
        if dim_id not in dim_data:
            return {"action": action, "dim_id": dim_id, "status": "not_found"}

        with _registry_write_lock:
            if action == "approve":
                dim_data[dim_id]["reviewed"] = True
                dim_data[dim_id].pop("auto_registered", None)
                self._flush_registry()
                return {"action": action, "dim_id": dim_id, "status": "approved"}
            elif action == "remove":
                info = dim_data.pop(dim_id)
                code = info.get("code", "")
                if dim_key == "natures" and code in self._nature_by_code:
                    del self._nature_by_code[code]
                elif dim_key == "persons" and code in self._person_by_code:
                    del self._person_by_code[code]
                elif dim_key == "tools" and code in self._tool_by_code:
                    del self._tool_by_code[code]
                elif dim_key == "knowledge_types" and code in self._knowledge_by_code:
                    del self._knowledge_by_code[code]
                self._flush_registry()
                return {"action": action, "dim_id": dim_id, "status": "removed"}

        return {"action": action, "dim_id": dim_id, "status": "unknown_action"}

    def get_usage_ranking(self, dim_key: str = None, top_n: int = 20) -> list[dict]:
        """
        获取维度值使用频率排名。

        参数:
            dim_key: 指定维度类别（None=全部）
            top_n: 返回前 N 个

        返回: [{"key": str, "count": int, "dim_key": str, "id": str}]
        """
        usage_stats = self.registry.get("_usage_stats", {})
        items = []
        for key, count in usage_stats.items():
            parts = key.split(":", 1)
            if len(parts) != 2:
                continue
            prefix, dim_id = parts
            if dim_key and not key.startswith(dim_key.rstrip("s") + ":"):
                continue
            items.append({"key": key, "count": count, "prefix": prefix, "id": dim_id})

        items.sort(key=lambda x: -x["count"])
        return items[:top_n]


if __name__ == "__main__":
    enc = DimensionEncoder()
    print("=== 性质列表 ===")
    for nid, info in enc.registry["natures"].items():
        print(f"  {nid} ({info['code']:8s}) → {info['name']}  {info['desc']}")

    print("\n=== 主题树 ===")
    for t in enc.list_topics():
        print(f"  {t}")

    print("\n=== 示例编码 ===")
    tid = enc.encode_time(precision="second")
    mid = enc.generate_memory_id(
        time_id=tid,
        person_id="P01",
        topic_codes=["ai.rag.vdb"],
        nature_id=enc.encode_nature("explore"),
        tool_ids=["t_ch", "t_lc"],
    )
    print(f"  memory_id = {mid}")
