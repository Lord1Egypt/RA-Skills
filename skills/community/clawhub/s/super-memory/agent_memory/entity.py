"""
entity.py — Phase 2.2: 实体消解引擎

从记忆内容中提取实体（人名/组织/地点/概念），
通过精确匹配 → 别名匹配 → 模糊匹配实现实体消解，
并维护实体-记忆关联和实体间关系图。
"""

from __future__ import annotations

import json
import logging
import re
import time
import uuid
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

# ── 规则式实体提取模式 ──────────────────────────────────

# 中文人名模式：2-4 字常见姓氏 + 名
_ZH_SURNAME = (
    "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜"
    "戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐"
    "费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄"
    "和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁"
    "杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍"
    "虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程"
    "嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗"
    "山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶"
    "郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴郁胥能苍双闻莘党翟谭贡"
    "劳逄姬申扶堵冉宰郦雍却璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充"
    "慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东欧殳"
    "沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾母沙乜养鞠须丰巢关蒯相"
    "查后荆红游竺权逯盖益桓公"
)

_PERSON_PATTERNS = [
    # 中文名：姓 + 1-2 字名，前后有上下文标记
    re.compile(rf"(?<=\s|，|、|和|与|叫|是|跟|找|给|对|问|请|让|帮|被|把|替|向|跟|跟|的)([{_ZH_SURNAME}][\u4e00-\u9fff]{{1,2}})(?=\s|，|。|、|说|做|去|来|在|的|了|和|与|给|把|被)"),
    # "小X"/"老X"/"X哥"/"X姐"/"X总"/"X经理" 等昵称
    re.compile(r"(?:小|老|阿)([\u4e00-\u9fff]{1,2})(?=\s|，|。|、|说|做|去|来|在|的|了)"),
    re.compile(r"([\u4e00-\u9fff]{1,2})(?:哥|姐|总|经理|老师|老板|主任)(?=\s|，|。|、|说|做|去|来|在|的|了)"),
    # 英文名
    re.compile(r"\b([A-Z][a-z]{1,15}(?:\s[A-Z][a-z]{1,15})?)\b"),
]

_ORG_PATTERNS = [
    re.compile(r"([\u4e00-\u9fff]{2,10}(?:公司|团队|部门|组织|集团|机构|实验室|工作室|中心))"),
    re.compile(r"([\u4e00-\u9fff]{2,6}(?:Team|Lab|Group|Inc|Corp|Ltd))", re.IGNORECASE),
]

_LOCATION_PATTERNS = [
    re.compile(r"(深圳|北京|上海|广州|杭州|成都|武汉|南京|西安|重庆|苏州|长沙|厦门|青岛|大连|东莞|佛山|合肥|郑州|天津|济南|福州|昆明|贵阳|兰州|太原|沈阳|哈尔滨|长春|石家庄|呼和浩特|乌鲁木齐|拉萨|银川|西宁|南宁|海口|三亚|珠海|无锡|常州|徐州|温州|宁波|绍兴|嘉兴|泉州|漳州|烟台|潍坊|洛阳|襄阳|宜昌|株洲|湘潭|衡阳|岳阳|常德|遵义|绵阳|德阳|宜宾|曲靖|大理|丽江|桂林|柳州|北海|芜湖|蚌埠|淮南|马鞍山|淮北|铜陵|安庆|黄山|滁州|阜阳|宿州|六安|亳州|池州|宣城)"),
    re.compile(r"([\u4e00-\u9fff]{2,6}(?:市|省|区|县|镇|街道|路|街|巷|弄|号))"),
]

# 关系提取模式 (subject → predicate → object)
_RELATION_PATTERNS = [
    re.compile(r"([\u4e00-\u9fff]{2,6})(?:是|为|属于|在|去了|来了|加入了|离开了|负责|管理|领导|创建|成立了)([\u4e00-\u9fff]{2,10})"),
    re.compile(r"([\u4e00-\u9fff]{2,6})(?:的|之)(?:老板|经理|领导|同事|朋友|老师|学生|上级|下属|搭档|伙伴)(?:是|为)?(?:([\u4e00-\u9fff]{2,6}))?"),
]

# 编辑距离模糊匹配阈值
_FUZZY_THRESHOLD = 0.75


def _levenshtein_ratio(s1: str, s2: str) -> float:
    """计算两个字符串的相似度（0~1），基于 SequenceMatcher"""
    if not s1 or not s2:
        return 0.0
    return SequenceMatcher(None, s1, s2).ratio()


class EntityResolver:
    """实体消解引擎：提取、消解、注册、关联实体"""

    # 别名倒排索引：alias_name → entity_id，惰性构建
    _ALIAS_INDEX_MAX = 10000          # 别名索引最大条目数
    _FUZZY_CACHE_MAX = 1000           # 模糊匹配缓存最大条目数

    def __init__(self, store=None, llm_fn: callable = None):
        self.store = store
        self._llm_fn = llm_fn
        self._alias_index: dict[str, str] = {}       # alias → entity_id
        self._alias_index_built: bool = False
        self._fuzzy_cache: dict[str, str | None] = {} # "name|entity_type" → entity_id or None

    # ── 实体提取 ────────────────────────────────────────

    def extract_entities(self, content: str) -> list[dict]:
        """
        从内容中提取实体。

        优先使用 LLM 提取，失败时回退到规则式。
        返回: [{"name": str, "type": str, "role": str}, ...]
        """
        if not content or not content.strip():
            return []

        # 优先尝试 LLM 提取
        if self._llm_fn is not None:
            try:
                llm_result = self._extract_entities_llm(content)
                if llm_result:
                    return llm_result
            except Exception as e:
                logger.debug("entity: LLM extract failed, fallback to rules: %s", e)

        return self._extract_entities_rules(content)

    def _extract_entities_llm(self, content: str) -> list[dict] | None:
        """使用 LLM 做实体提取，返回实体列表或 None"""
        prompt = (
            "从以下文本中提取实体，包括人名、地名、组织名、技术名、产品名等。\n"
            "返回 JSON 数组，每个元素包含 name 和 type 字段。\n"
            "type 可选值: person, location, org, tech, product, other。\n"
            "仅返回 JSON 数组，不要包含其他文字。\n\n"
            f"文本：{content}\n\n"
            '示例输出：[{"name": "张三", "type": "person"}, {"name": "北京", "type": "location"}]'
        )

        response = self._llm_fn(prompt)
        if not response:
            return None

        # 尝试从响应中解析 JSON
        text = response.strip() if isinstance(response, str) else str(response)

        # 提取 JSON 数组部分（兼容 LLM 可能返回的额外文字）
        start = text.find("[")
        end = text.rfind("]")
        if start == -1 or end == -1 or end <= start:
            return None

        json_str = text[start:end + 1]
        items = json.loads(json_str)

        if not isinstance(items, list):
            return None

        entities = []
        seen_names = set()
        valid_types = {"person", "location", "org", "tech", "product", "other"}
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name", "")
            etype = item.get("type", "other")
            if not name or not isinstance(name, str):
                continue
            name = name.strip()
            if not name or name in seen_names:
                continue
            if etype not in valid_types:
                etype = "other"
            seen_names.add(name)
            entities.append({"name": name, "type": etype, "role": "mentioned"})

        return entities if entities else None

    def _extract_entities_rules(self, content: str) -> list[dict]:
        """规则式实体提取（原有逻辑）"""
        entities = []
        seen_names = set()

        # 1. 提取人名
        for pattern in _PERSON_PATTERNS:
            for match in pattern.finditer(content):
                name = match.group(1).strip()
                if name and len(name) >= 2 and name not in seen_names and name not in (
                    "什么", "怎么", "为什么", "如何", "哪里", "这个", "那个",
                    "可以", "没有", "不是", "已经", "应该", "需要", "知道",
                    "觉得", "认为", "希望", "可能", "关于", "通过", "使用",
                    "公司", "团队", "部门", "组织", "集团", "机构", "项目",
                    "The", "This", "That", "What", "How", "Why", "When",
                    "There", "Here", "They", "Their", "Which", "Where",
                ):
                    seen_names.add(name)
                    entities.append({"name": name, "type": "person", "role": "mentioned"})

        # 2. 提取组织
        for pattern in _ORG_PATTERNS:
            for match in pattern.finditer(content):
                name = match.group(1).strip()
                if name and name not in seen_names:
                    seen_names.add(name)
                    entities.append({"name": name, "type": "org", "role": "mentioned"})

        # 3. 提取地点
        for pattern in _LOCATION_PATTERNS:
            for match in pattern.finditer(content):
                name = match.group(1).strip()
                if name and name not in seen_names:
                    seen_names.add(name)
                    entities.append({"name": name, "type": "location", "role": "mentioned"})

        # 4. 尝试提取关系三元组 (subject, predicate, object)
        for pattern in _RELATION_PATTERNS:
            for match in pattern.finditer(content):
                groups = match.groups()
                subj_name = groups[0].strip() if groups[0] else None
                obj_name = groups[-1].strip() if groups[-1] else None
                if subj_name and subj_name not in seen_names:
                    seen_names.add(subj_name)
                    entities.append({"name": subj_name, "type": "person", "role": "subject"})
                if obj_name and obj_name not in seen_names:
                    seen_names.add(obj_name)
                    entities.append({"name": obj_name, "type": "person", "role": "object"})

        return entities

    # ── 别名倒排索引 ────────────────────────────────────

    def _build_alias_index(self):
        """构建别名倒排索引（惰性，首次 resolve_entity 时调用）"""
        if not self.store:
            return
        self._alias_index.clear()
        try:
            rows = self.store.conn.execute(
                "SELECT entity_id, aliases FROM entities"
            ).fetchall()
            for r in rows:
                try:
                    aliases = json.loads(r["aliases"]) if r["aliases"] else []
                except (json.JSONDecodeError, TypeError):
                    aliases = []
                for alias in aliases:
                    if alias and len(self._alias_index) < self._ALIAS_INDEX_MAX:
                        self._alias_index[alias] = r["entity_id"]
            self._alias_index_built = True
        except Exception as e:
            logger.warning("entity: build_alias_index: %s", e)

    def _invalidate_alias_index(self):
        """标记别名索引失效，下次 resolve_entity 时重建"""
        self._alias_index_built = False
        self._alias_index.clear()

    # ── 实体消解 ────────────────────────────────────────

    def resolve_entity(self, name: str, entity_type: str = None) -> str | None:
        """
        实体消解：将名称映射到已有实体 ID。

        匹配策略：
        1. 精确匹配 canonical_name（带 entity_type 过滤）
        2. 匹配 aliases（使用倒排索引，O(1)）
        3. 模糊匹配（带 entity_type 过滤 + 缓存）

        返回: entity_id 或 None
        """
        if not self.store or not name:
            return None

        conn = self.store.conn

        # 1. 精确匹配 canonical_name（优先带 entity_type 过滤）
        if entity_type:
            row = conn.execute(
                "SELECT entity_id FROM entities WHERE canonical_name = ? AND entity_type = ?",
                (name, entity_type),
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT entity_id FROM entities WHERE canonical_name = ?",
                (name,),
            ).fetchone()
        if row:
            return row["entity_id"]

        # 2. 匹配 aliases（使用倒排索引，O(1)）
        if not self._alias_index_built:
            self._build_alias_index()
        entity_id = self._alias_index.get(name)
        if entity_id:
            return entity_id

        # 3. 模糊匹配（带缓存）
        cache_key = f"{name}|{entity_type or ''}"
        if cache_key in self._fuzzy_cache:
            return self._fuzzy_cache[cache_key]

        # 3a. 包含关系：name 是 canonical_name 的子串，或反过来
        if entity_type:
            rows = conn.execute(
                "SELECT entity_id, canonical_name FROM entities WHERE entity_type = ?",
                (entity_type,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT entity_id, canonical_name FROM entities",
            ).fetchall()

        for r in rows:
            canonical = r["canonical_name"]
            if (name in canonical or canonical in name) and len(min(name, canonical, key=len)) >= 2:
                self._fuzzy_cache[cache_key] = r["entity_id"]
                self._trim_fuzzy_cache()
                return r["entity_id"]

        # 3b. 编辑距离模糊匹配（同类型优先，rows 已在 3a 中按 entity_type 过滤）
        best_id = None
        best_score = 0.0
        for r in rows:
            score = _levenshtein_ratio(name, r["canonical_name"])
            if score > best_score:
                best_score = score
                best_id = r["entity_id"]

        if best_score >= _FUZZY_THRESHOLD:
            self._fuzzy_cache[cache_key] = best_id
            self._trim_fuzzy_cache()
            return best_id

        # 缓存未命中结果，避免重复计算
        self._fuzzy_cache[cache_key] = None
        self._trim_fuzzy_cache()
        return None

    def _trim_fuzzy_cache(self):
        """模糊匹配缓存超限时淘汰旧条目"""
        if len(self._fuzzy_cache) > self._FUZZY_CACHE_MAX:
            # 简单策略：删除最早的一半
            keys_to_remove = list(self._fuzzy_cache.keys())[: len(self._fuzzy_cache) // 2]
            for k in keys_to_remove:
                del self._fuzzy_cache[k]

    # ── 实体注册 ────────────────────────────────────────

    def register_entity(self, name: str, entity_type: str, aliases: list = None) -> str:
        """
        注册新实体，返回 entity_id。

        如果同名实体已存在，更新 last_seen 和 mention_count。
        """
        if not self.store:
            return ""

        now = time.time()
        conn = self.store.conn

        # 先尝试消解
        existing_id = self.resolve_entity(name, entity_type)
        if existing_id:
            # 更新已有实体的统计
            try:
                conn.execute(
                    "UPDATE entities SET last_seen = ?, mention_count = mention_count + 1 WHERE entity_id = ?",
                    (now, existing_id),
                )
                conn.commit()
            except Exception as e:
                logger.warning("entity: update existing: %s", e)
            return existing_id

        # 新建实体
        entity_id = f"ent_{uuid.uuid4().hex[:16]}"
        aliases_json = json.dumps(aliases or [], ensure_ascii=False)

        try:
            conn.execute(
                """INSERT INTO entities
                   (entity_id, canonical_name, entity_type, aliases, first_seen, last_seen, mention_count)
                   VALUES (?, ?, ?, ?, ?, ?, 1)""",
                (entity_id, name, entity_type, aliases_json, now, now),
            )
            conn.commit()
            # 新实体加入后，模糊缓存可能失效（新实体可能成为更好的匹配）
            self._fuzzy_cache.clear()
            # 增量更新别名索引
            if self._alias_index_built and aliases:
                for alias in aliases:
                    if alias:
                        self._alias_index[alias] = entity_id
        except Exception as e:
            logger.warning("entity: register: %s", e)
            return ""

        return entity_id

    # ── 别名管理 ────────────────────────────────────────

    def add_alias(self, entity_id: str, alias: str):
        """为实体添加别名"""
        if not self.store or not entity_id or not alias:
            return

        conn = self.store.conn
        try:
            row = conn.execute(
                "SELECT aliases FROM entities WHERE entity_id = ?",
                (entity_id,),
            ).fetchone()
            if not row:
                return

            aliases = json.loads(row["aliases"]) if row["aliases"] else []
            if alias not in aliases:
                aliases.append(alias)
                conn.execute(
                    "UPDATE entities SET aliases = ? WHERE entity_id = ?",
                    (json.dumps(aliases, ensure_ascii=False), entity_id),
                )
                conn.commit()
                # 增量更新别名索引（避免全量重建）
                if self._alias_index_built:
                    self._alias_index[alias] = entity_id
        except Exception as e:
            logger.warning("entity: add_alias: %s", e)

    # ── 记忆-实体关联 ──────────────────────────────────

    def link_memory_entities(self, memory_id: str, entities: list[dict]):
        """
        关联记忆与实体。

        entities: [{"name": str, "type": str, "role": str}, ...]
        对每个实体：先消解，消解失败则注册新实体，然后建立关联。
        如果提取到已知实体的别名，自动合并。
        """
        if not self.store or not memory_id or not entities:
            return

        conn = self.store.conn
        for ent in entities:
            name = ent.get("name", "")
            etype = ent.get("type", "other")
            role = ent.get("role", "mentioned")

            if not name:
                continue

            # 尝试消解
            entity_id = self.resolve_entity(name, etype)

            if entity_id:
                # 已有实体：检查是否需要添加别名
                row = conn.execute(
                    "SELECT canonical_name FROM entities WHERE entity_id = ?",
                    (entity_id,),
                ).fetchone()
                if row and row["canonical_name"] != name:
                    # 名称与 canonical_name 不同，自动添加为别名
                    self.add_alias(entity_id, name)
                # 更新统计
                try:
                    conn.execute(
                        "UPDATE entities SET last_seen = ?, mention_count = mention_count + 1 WHERE entity_id = ?",
                        (time.time(), entity_id),
                    )
                except Exception as e:
                    logger.warning("entity: update stats: %s", e)
            else:
                # 注册新实体
                entity_id = self.register_entity(name, etype)

            if not entity_id:
                continue

            # 建立记忆-实体关联
            try:
                conn.execute(
                    """INSERT OR IGNORE INTO memory_entities (memory_id, entity_id, role)
                       VALUES (?, ?, ?)""",
                    (memory_id, entity_id, role),
                )
            except Exception as e:
                logger.warning("entity: link_memory: %s", e)

        try:
            conn.commit()
        except Exception as e:
            logger.warning("entity: commit link: %s", e)

    # ── 实体相关记忆 ────────────────────────────────────

    def get_entity_memories(self, entity_id: str, limit: int = 20) -> list[dict]:
        """获取实体的所有相关记忆"""
        if not self.store or not entity_id:
            return []

        try:
            rows = self.store.conn.execute(
                """SELECT m.*, me.role as entity_role
                   FROM memories m
                   JOIN memory_entities me ON m.memory_id = me.memory_id
                   WHERE me.entity_id = ?
                   ORDER BY m.time_ts DESC
                   LIMIT ?""",
                (entity_id, limit),
            ).fetchall()

            results = []
            for row in rows:
                mem = dict(row)
                results.append(mem)
            return results
        except Exception as e:
            logger.warning("entity: get_memories: %s", e)
            return []

    # ── 实体关系图 ──────────────────────────────────────

    def get_entity_graph(self, entity_id: str, depth: int = 2) -> dict:
        """
        获取实体的关系图。

        从指定实体出发，沿 relations 表遍历 depth 层，
        返回节点和边的集合。

        返回: {"nodes": [...], "edges": [...], "center": entity_id}
        """
        if not self.store or not entity_id:
            return {"nodes": [], "edges": [], "center": entity_id}

        nodes = {}
        edges = []
        visited = set()
        frontier = [entity_id]

        # 获取起始实体
        row = self.store.conn.execute(
            "SELECT entity_id, canonical_name, entity_type FROM entities WHERE entity_id = ?",
            (entity_id,),
        ).fetchone()
        if row:
            nodes[row["entity_id"]] = {
                "entity_id": row["entity_id"],
                "canonical_name": row["canonical_name"],
                "entity_type": row["entity_type"],
            }

        for _ in range(depth):
            next_frontier = []
            if not frontier:
                break

            for placeholders, chunk_ids in _chunked_entity_ids(frontier):
                # 查找以 frontier 为 subject 的关系
                fwd_rows = self.store.conn.execute(
                    f"""SELECT r.*, e.canonical_name as obj_name, e.entity_type as obj_type
                        FROM relations r
                        JOIN entities e ON r.object_entity_id = e.entity_id
                        WHERE r.subject_entity_id IN ({placeholders})""",
                    chunk_ids,
                ).fetchall()

                # 查找以 frontier 为 object 的关系
                bwd_rows = self.store.conn.execute(
                    f"""SELECT r.*, e.canonical_name as subj_name, e.entity_type as subj_type
                        FROM relations r
                        JOIN entities e ON r.subject_entity_id = e.entity_id
                        WHERE r.object_entity_id IN ({placeholders})""",
                    chunk_ids,
                ).fetchall()

                for r in fwd_rows:
                    obj_id = r["object_entity_id"]
                    if obj_id not in nodes:
                        nodes[obj_id] = {
                            "entity_id": obj_id,
                            "canonical_name": r["obj_name"],
                            "entity_type": r["obj_type"],
                        }
                    edges.append({
                        "source": r["subject_entity_id"],
                        "predicate": r["predicate"],
                        "target": obj_id,
                        "confidence": r["confidence"],
                    })
                    if obj_id not in visited:
                        next_frontier.append(obj_id)

                for r in bwd_rows:
                    subj_id = r["subject_entity_id"]
                    if subj_id not in nodes:
                        nodes[subj_id] = {
                            "entity_id": subj_id,
                            "canonical_name": r["subj_name"],
                            "entity_type": r["subj_type"],
                        }
                    edges.append({
                        "source": subj_id,
                        "predicate": r["predicate"],
                        "target": r["object_entity_id"],
                        "confidence": r["confidence"],
                    })
                    if subj_id not in visited:
                        next_frontier.append(subj_id)

            visited.update(frontier)
            frontier = next_frontier

        return {
            "nodes": list(nodes.values()),
            "edges": edges,
            "center": entity_id,
        }

    # ── 关系注册 ────────────────────────────────────────

    def add_relation(
        self,
        subject_entity_id: str,
        predicate: str,
        object_entity_id: str,
        source_memory_id: str = None,
        confidence: float = 1.0,
    ) -> str:
        """注册实体间关系，返回 relation_id"""
        if not self.store:
            return ""

        relation_id = f"rel_{uuid.uuid4().hex[:16]}"
        try:
            self.store.conn.execute(
                """INSERT INTO relations
                   (relation_id, subject_entity_id, predicate, object_entity_id,
                    source_memory_id, confidence)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (relation_id, subject_entity_id, predicate, object_entity_id, source_memory_id, confidence),
            )
            self.store.conn.commit()
            return relation_id
        except Exception as e:
            logger.warning("entity: add_relation: %s", e)
            return ""

    # ── 从查询中提取实体名 ──────────────────────────────

    def extract_entity_names_from_query(self, query: str) -> list[str]:
        """
        从查询文本中提取可能的实体名称，用于扩展检索。

        返回: [entity_name, ...]
        """
        if not query:
            return []

        names = []
        for pattern in _PERSON_PATTERNS:
            for match in pattern.finditer(query):
                name = match.group(1).strip()
                if name and len(name) >= 2:
                    names.append(name)

        for pattern in _ORG_PATTERNS:
            for match in pattern.finditer(query):
                name = match.group(1).strip()
                if name:
                    names.append(name)

        for pattern in _LOCATION_PATTERNS:
            for match in pattern.finditer(query):
                name = match.group(1).strip()
                if name:
                    names.append(name)

        return list(dict.fromkeys(names))  # 去重保序

    # ── 通过实体名获取关联的 memory_id ──────────────────

    def get_memory_ids_by_entity_names(self, names: list[str], limit: int = 50) -> list[str]:
        """
        根据实体名称列表，查找关联的 memory_id 集合。

        用于检索管道的实体扩展。
        """
        if not self.store or not names:
            return []

        entity_ids = set()
        for name in names:
            eid = self.resolve_entity(name)
            if eid:
                entity_ids.add(eid)

        if not entity_ids:
            return []

        try:
            memory_ids = []
            eid_list = list(entity_ids)
            for placeholders, chunk_ids in _chunked_entity_ids(eid_list):
                rows = self.store.conn.execute(
                    f"SELECT DISTINCT memory_id FROM memory_entities WHERE entity_id IN ({placeholders}) LIMIT ?",
                    chunk_ids + [limit],
                ).fetchall()
                memory_ids.extend(r["memory_id"] for r in rows)
            return memory_ids[:limit]
        except Exception as e:
            logger.warning("entity: get_memory_ids: %s", e)
            return []


def _chunked_entity_ids(ids: list, chunk_size: int = 999):
    """分片占位符生成（与 store._chunked_placeholders 兼容）"""
    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i + chunk_size]
        yield ",".join("?" * len(chunk)), chunk
