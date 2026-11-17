#!/usr/bin/env python3
"""
图检索（Graph RAG）基础框架
===========================
从文档中提取实体和关系，构建知识图谱，支持图遍历检索。

使用方法：
    from graph_rag import GraphRAG

    gra = GraphRAG()
    gra.build_from_text("北京是中国的首都，故宫位于北京。")
    results = gra.query("故宫在哪里")

零依赖：不依赖外部 NLP 模型，使用规则模式实体提取。
支持 LLM 增强：传入 llm_client 后可使用 LLM 进行实体识别。
"""
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class Entity:
    """知识图谱实体"""
    id: str
    label: str
    type: str  # Person, Organization, Location, Concept, etc.
    mentions: int = 0
    aliases: Set[str] = field(default_factory=set)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type,
            "mentions": self.mentions,
            "aliases": list(self.aliases),
        }


@dataclass
class Relation:
    """知识图谱关系"""
    id: str
    source: str  # entity id
    target: str  # entity id
    relation_type: str
    confidence: float = 1.0
    evidence: str = ""

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "relation_type": self.relation_type,
            "confidence": self.confidence,
            "evidence": self.evidence,
        }


@dataclass
class GraphQueryResult:
    """图检索结果"""
    query: str
    matched_entities: List[Entity]
    related_entities: List[Entity]
    relations: List[Relation]
    answer: str
    confidence: float

    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "matched_entities": [e.to_dict() for e in self.matched_entities],
            "related_entities": [e.to_dict() for e in self.related_entities],
            "relations": [r.to_dict() for r in self.relations],
            "answer": self.answer,
            "confidence": self.confidence,
        }


class EntityExtractor:
    """
    实体提取器：从文本中提取实体。

    规则模式：基于中文/英文常见实体模式匹配。
    LLM 模式：传入 llm_client 后使用 LLM 识别实体。
    """

    # 规则模式：常见实体模式（注意：使用 (word1|word2|...) 而非 [chars]）
    _PATTERNS = {
        "Location": re.compile(r'(?:北京|上海|广州|深圳|杭州|南京|成都|武汉|西安|重庆'
            r'|东京|纽约|伦敦|巴黎|首尔|柏林'
            r'|中国|美国|日本|英国|法国|德国|意大利|西班牙|韩国|印度'
            r'|故宫|长城|天安门|西湖|颐和园)'),
        "Organization": re.compile(r'(?:谷歌|百度|阿里巴巴|腾讯|字节跳动|华为|苹果|微软|IBM|Meta|OpenAI)'),
        "Person": re.compile(r'(?:马云|马化腾|雷军|比尔盖茨|马斯克|乔布斯)'),
        "Concept": re.compile(r'(?:RAG|BERT|GPT|LLM|NLP|AI|机器学习|深度学习|人工智能'
            r'|信息检索|知识图谱|神经网络|向量空间|注意力机制)'),
    }

    def __init__(self, llm_client=None, config: Dict = None):
        self.llm = llm_client
        self.config = config or {}
        self._entity_counter = 0

    def extract(self, text: str) -> List[Entity]:
        """从文本中提取实体"""
        if self.llm:
            return self._llm_extract(text)

        return self._rule_extract(text)

    def _rule_extract(self, text: str) -> List[Entity]:
        """规则模式实体提取"""
        entities = []
        seen = set()

        for entity_type, pattern in self._PATTERNS.items():
            matches = pattern.findall(text)
            for match in matches:
                match = match.strip()
                if match and match not in seen:
                    self._entity_counter += 1
                    entity_id = f"entity_{self._entity_counter}"
                    entity = Entity(
                        id=entity_id,
                        label=match,
                        type=entity_type,
                        mentions=1,
                    )
                    entities.append(entity)
                    seen.add(match)

        # 通用实体：匹配2-4字中文词（非空格结尾的通用词）
        general_matches = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        for match in general_matches:
            if match not in seen and len(match) >= 2:
                # 避免提取过于通用的虚词
                if any(c in match for c in "的是在了有不与和或则"):
                    continue
                if re.match(r'^[\u4e00-\u9fff]{2,4}$', match):
                    self._entity_counter += 1
                    entity_id = f"entity_{self._entity_counter}"
                    entity = Entity(
                        id=entity_id,
                        label=match,
                        type="General",
                        mentions=1,
                    )
                    entities.append(entity)
                    seen.add(match)

        return entities

    def _llm_extract(self, text: str) -> List[Entity]:
        """LLM 模式实体提取"""
        # 使用 LLM 识别实体（需要外部模型支持）
        prompt = f"""
从以下文本中提取实体和关系，返回 JSON 格式：
{{
    \"entities\": [
        {{\"label\": \"实体名\", \"type\": \"Person|Organization|Location|Concept\"}},
        ...
    ],
    \"relations\": [
        {{\"source\": \"源实体\", \"target\": \"目标实体\", \"type\": \"关系类型\"}},
        ...
    ]
}}

文本：{text}
"""
        try:
            if hasattr(self.llm, 'invoke'):
                response = self.llm.invoke(prompt)
            else:
                response = self.llm(prompt)

            import json
            # 提取 JSON
            json_match = re.search(r'\{[\s\S]*\}', str(response))
            if json_match:
                data = json.loads(json_match.group())
                entities = []
                for ent in data.get('entities', []):
                    self._entity_counter += 1
                    entities.append(Entity(
                        id=f"entity_{self._entity_counter}",
                        label=ent.get('label', ''),
                        type=ent.get('type', 'Concept'),
                    ))
                return entities
        except Exception as e:
            logger.warning(f"LLM 实体提取失败: {e}")

        # Fallback to rule-based
        return self._rule_extract(text)


class RelationExtractor:
    """
    关系提取器：从文本中识别实体之间的关系。

    规则模式：基于预定义的关系模板匹配。
    """

    # 关系模式：(正则, 关系类型) — 使用 (?:...) 非捕获组
    _RELATION_PATTERNS = [
        (re.compile(r'([\u4e00-\u9fff\w]+)位于([\u4e00-\u9fff\w]+)'), 'located_in'),
        (re.compile(r'([\u4e00-\u9fff\w]+)是([\u4e00-\u9fff\w]+)(?:的首都|的首部)'), 'is_capital_of'),
        (re.compile(r'([\u4e00-\u9fff\w]+)属于([\u4e00-\u9fff\w]+)'), 'belongs_to'),
        (re.compile(r'([\u4e00-\u9fff\w]+)是([\u4e00-\u9fff\w]+)(?:发明|创始人|开发者)'), 'invented_by'),
        (re.compile(r'([\u4e00-\u9fff\w]+)由([\u4e00-\u9fff\w]+)(?:发明|创建|开发|设计)'), 'created_by'),
        (re.compile(r'([\u4e00-\u9fff\w]+)用于([\u4e00-\u9fff\w]+)'), 'used_for'),
        (re.compile(r'([\u4e00-\u9fff\w]+)包含([\u4e00-\u9fff\w]+)'), 'contains'),
    ]

    def __init__(self, config: Dict = None):
        self.config = config or {}

    def extract(self, text: str, entities: List[Entity]) -> List[Relation]:
        """从文本中提取关系"""
        relations = []
        rel_counter = 0
        entity_labels = {e.label: e.id for e in entities}

        for pattern, rel_type in self._RELATION_PATTERNS:
            matches = pattern.findall(text)
            for source, target in matches:
                source = source.strip()
                target = target.strip()
                if source in entity_labels and target in entity_labels:
                    rel_counter += 1
                    relations.append(Relation(
                        id=f"relation_{rel_counter}",
                        source=entity_labels[source],
                        target=entity_labels[target],
                        relation_type=rel_type,
                        confidence=0.8,
                        evidence=f"{source} {rel_type} {target}",
                    ))

        return relations


class KnowledgeGraph:
    """知识图谱：存储实体和关系，支持遍历查询"""

    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []
        self.adjacency: Dict[str, List[Tuple[str, str]]] = defaultdict(list)

    def add_entity(self, entity: Entity):
        """添加实体"""
        if entity.id not in self.entities:
            self.entities[entity.id] = entity
        else:
            self.entities[entity.id].mentions += 1

    def add_relation(self, relation: Relation):
        """添加关系"""
        self.relations.append(relation)
        self.adjacency[relation.source].append((relation.target, relation.relation_type))
        self.adjacency[relation.target].append((relation.source, f"reverse_{relation.relation_type}"))

    def get_neighbors(self, entity_id: str, depth: int = 1) -> List[Entity]:
        """获取邻居实体"""
        neighbors = set()
        queue = [(entity_id, 0)]

        while queue:
            current, d = queue.pop(0)
            if d >= depth:
                continue
            for neighbor_id, _ in self.adjacency.get(current, []):
                if neighbor_id not in neighbors and neighbor_id in self.entities:
                    neighbors.add(neighbor_id)
                    queue.append((neighbor_id, d + 1))

        return [self.entities[nid] for nid in neighbors]

    def find_entity_by_label(self, label: str) -> Optional[Entity]:
        """根据标签查找实体"""
        label_lower = label.lower()
        for entity in self.entities.values():
            if label_lower in entity.label.lower() or label_lower in [a.lower() for a in entity.aliases]:
                return entity
        return None

    def to_dict(self) -> Dict:
        """序列化为字典"""
        return {
            "entities": {eid: e.to_dict() for eid, e in self.entities.items()},
            "relations": [r.to_dict() for r in self.relations],
        }


class GraphRAG:
    """
    图检索增强生成（Graph RAG）

    将文档转换为知识图谱，支持：
    1. 实体提取：从文本中识别命名实体
    2. 关系构建：识别实体之间的关系
    3. 图遍历检索：根据查询找到相关实体和关系
    4. 答案生成：基于图谱信息生成答案
    """

    def __init__(self, llm_client=None, config: Dict = None):
        self.config = config or {}
        self.llm = llm_client

        self.entity_extractor = EntityExtractor(llm_client=llm_client, config=config)
        self.relation_extractor = RelationExtractor(config=config)
        self.graph = KnowledgeGraph()

    def build_from_text(self, text: str, source: str = "default") -> Dict:
        """
        从文本构建知识图谱

        Args:
            text: 输入文本
            source: 文档来源标识

        Returns:
            {entities: [...], relations: [...], graph_stats: {...}}
        """
        entities = self.entity_extractor.extract(text)
        relations = self.relation_extractor.extract(text, entities)

        for entity in entities:
            self.graph.add_entity(entity)
        for relation in relations:
            self.graph.add_relation(relation)

        return {
            "entities": [e.to_dict() for e in entities],
            "relations": [r.to_dict() for r in relations],
            "graph_stats": {
                "total_entities": len(self.graph.entities),
                "total_relations": len(self.graph.relations),
                "source": source,
            },
        }

    def build_from_texts(self, texts: List[str], sources: List[str] = None) -> Dict:
        """从多个文本构建图谱"""
        results = []
        for i, text in enumerate(texts):
            src = sources[i] if sources and i < len(sources) else f"doc_{i}"
            result = self.build_from_text(text, source=src)
            results.append(result)

        return {
            "results": results,
            "total_entities": len(self.graph.entities),
            "total_relations": len(self.graph.relations),
        }

    def query(self, query_text: str, top_k: int = 5, depth: int = 2) -> GraphQueryResult:
        """
        基于图遍历进行检索

        Args:
            query_text: 查询文本
            top_k: 返回结果数量
            depth: 图遍历深度

        Returns:
            GraphQueryResult
        """
        # 1. 在查询中提取实体
        query_entities = self.entity_extractor.extract(query_text)

        # 2. 在图中匹配查询实体
        matched = []
        for qe in query_entities:
            entity = self.graph.find_entity_by_label(qe.label)
            if entity and entity not in matched:
                matched.append(entity)

        # 3. 图遍历：获取相关实体
        related = set()
        matched_relations = []
        for entity in matched:
            neighbors = self.graph.get_neighbors(entity.id, depth=depth)
            for n in neighbors:
                if n.id not in related:
                    related.add(n.id)
                    # 收集关系
                    for r in self.graph.relations:
                        if r.source == entity.id or r.target == entity.id:
                            if r not in matched_relations:
                                matched_relations.append(r)

        related_entities = [self.graph.entities[nid] for nid in related if nid in self.graph.entities]

        # 4. 生成答案
        answer = self._generate_answer(query_text, matched, related_entities, matched_relations)

        confidence = self._calculate_confidence(matched, related_entities, query_text)

        return GraphQueryResult(
            query=query_text,
            matched_entities=matched[:top_k],
            related_entities=related_entities[:top_k],
            relations=matched_relations[:top_k],
            answer=answer,
            confidence=confidence,
        )

    def _generate_answer(self, query: str, matched: List[Entity],
                         related: List[Entity], relations: List[Relation]) -> str:
        """基于图谱生成答案"""
        if not matched and not related:
            return "未在知识图谱中找到相关信息。"

        # 构建答案摘要
        parts = []
        if matched:
            matched_labels = [e.label for e in matched[:3]]
            parts.append(f"相关实体: {', '.join(matched_labels)}")

        if relations:
            rel_summaries = []
            for r in relations[:3]:
                src_label = self.graph.entities.get(r.source, Entity(r.source, r.source, "Unknown")).label
                tgt_label = self.graph.entities.get(r.target, Entity(r.target, r.target, "Unknown")).label
                rel_summaries.append(f"{src_label} --[{r.relation_type}]--> {tgt_label}")
            if rel_summaries:
                parts.append(f"关系: {'; '.join(rel_summaries)}")

        if related:
            related_labels = [e.label for e in related[:5]]
            if len(related_labels) > 0:
                parts.append(f"关联实体: {', '.join(related_labels)}")

        return " | ".join(parts) if parts else "未在知识图谱中找到相关信息。"

    def _calculate_confidence(self, matched: List[Entity], related: List[Entity],
                              query: str) -> float:
        """计算答案置信度"""
        if not matched and not related:
            return 0.0

        # 有匹配实体时基础置信度
        base = 0.3
        if matched:
            base += 0.3 * min(len(matched), 3) / 3.0
        if related:
            base += 0.2 * min(len(related), 5) / 5.0

        # 查询文本与实体标签的重叠
        query_lower = query.lower()
        overlap = 0
        for e in matched:
            if e.label.lower() in query_lower:
                overlap += 1
        if overlap > 0:
            base += 0.2 * min(overlap / max(len(matched), 1), 1.0)

        return min(1.0, base)

    def export_graph(self, output_path: str = None) -> Dict:
        """导出知识图谱"""
        graph_data = self.graph.to_dict()
        if output_path:
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, ensure_ascii=False, indent=2)
            logger.info(f"知识图谱已导出: {output_path}")
        return graph_data

    def get_graph_stats(self) -> Dict:
        """获取图谱统计信息"""
        return {
            "total_entities": len(self.graph.entities),
            "total_relations": len(self.graph.relations),
            "entity_types": {},
            "relation_types": {},
        }