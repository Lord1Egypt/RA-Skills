"""
查询引擎 - 整合关键词提取 + 索引查询 + 关系追溯
提供统一的查询接口
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Set, Optional, Tuple
from collections import defaultdict

from retrieval.keyword_extractor import KeywordExtractor
from retrieval.index_manager import IndexManager
from storage.knowledge_store import KnowledgeStore


class QueryEngine:
    """知识查询引擎"""

    def __init__(self, skill_dir: str = None):
        """
        Args:
            skill_dir: domain-kit 技能根目录
        """
        if skill_dir is None:
            skill_dir = str(Path(__file__).parent.parent)
        self.skill_dir = Path(skill_dir)
        storage_path = str(self.skill_dir / "storage")
        schema_path = str(self.skill_dir / "schema")

        self.store = KnowledgeStore(storage_path)
        self.index = IndexManager(storage_path)
        self.keyword_extractor = KeywordExtractor(schema_path)

    def query(self, input_text: str, top_k: int = 10,
              entity_type_filter: str = None,
              tag_filter: List[str] = None) -> List[Dict[str, Any]]:
        """
        统一查询接口。

        Args:
            input_text: 用户输入文本
            top_k: 返回最大结果数
            entity_type_filter: 实体类型过滤
            tag_filter: 额外标签过滤

        Returns:
            排序后的实体列表，包含关系信息
        """
        # 1. 关键词提取
        keywords = self.keyword_extractor.extract(input_text)

        # 2. 候选 ID 收集
        candidate_ids = set()

        # 通过关键词查询
        keyword_ids = self.index.query_by_keywords(keywords)
        candidate_ids.update(keyword_ids)

        # 通过标签查询
        all_tags = list(set(keywords.get('models', []) + keywords.get('scenarios', [])))
        if tag_filter:
            all_tags.extend(tag_filter)
        if all_tags:
            tag_ids = self.index.query_by_tags(all_tags)
            candidate_ids.update(tag_ids)

        # 通过实体类型过滤
        if entity_type_filter:
            type_ids = self.index.query_by_entity_type(entity_type_filter)
            candidate_ids = candidate_ids.intersection(type_ids) if candidate_ids else type_ids

        # 如果关键词没匹配到但有型号词，用型号做兜底
        if not candidate_ids and keywords.get('models'):
            candidate_ids = self.index.query_by_tags(keywords['models'])

        # 3. 获取实体详情
        results = []
        for eid in candidate_ids:
            entity = self.store.get_entity(eid)
            if entity:
                # 添加关系信息
                relations = self._get_2hop_relations(eid)
                entity['_relations'] = relations
                entity['_keywords'] = keywords
                results.append(entity)

        # 4. 排序：按 confidence 降序
        results.sort(
            key=lambda x: x.get('provenance', {}).get('confidence', 0),
            reverse=True
        )

        # 5. 截断
        return results[:top_k]

    def _get_2hop_relations(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        获取 2-hop 关系邻居。
        1-hop: 直接关联的实体
        2-hop: 关联实体的关联实体
        """
        relations_1hop = self.index.get_all_relations(entity_id)
        result = []
        seen_ids = {entity_id}

        # 1-hop
        for rel in relations_1hop:
            neighbor_id = rel['to'] if rel['direction'] == 'forward' else rel['from']
            if neighbor_id in seen_ids:
                continue
            seen_ids.add(neighbor_id)

            neighbor_entity = self.store.get_entity(neighbor_id)
            result.append({
                "hop": 1,
                "relation": rel,
                "neighbor_entity": neighbor_entity
            })

            # 2-hop
            neighbor_relations = self.index.get_all_relations(neighbor_id)
            for nrel in neighbor_relations:
                nn_id = nrel['to'] if nrel['direction'] == 'forward' else nrel['from']
                if nn_id in seen_ids:
                    continue
                seen_ids.add(nn_id)

                nn_entity = self.store.get_entity(nn_id)
                result.append({
                    "hop": 2,
                    "relation": nrel,
                    "neighbor_entity": nn_entity
                })

        return result

    def query_by_type(self, entity_type: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """按实体类型查询"""
        ids = self.index.query_by_entity_type(entity_type)
        results = []
        for eid in ids:
            entity = self.store.get_entity(eid)
            if entity:
                results.append(entity)
        results.sort(
            key=lambda x: x.get('provenance', {}).get('confidence', 0),
            reverse=True
        )
        return results[:top_k]

    def query_by_tag(self, tag: str, top_k: int = 20) -> List[Dict[str, Any]]:
        """按标签查询"""
        ids = self.index.query_by_tags([tag])
        results = []
        for eid in ids:
            entity = self.store.get_entity(eid)
            if entity:
                results.append(entity)
        results.sort(
            key=lambda x: x.get('provenance', {}).get('confidence', 0),
            reverse=True
        )
        return results[:top_k]


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    engine = QueryEngine(str(Path(__file__).parent.parent))

    test_queries = [
        "AM600 输送带控制",
        "堆垛机调度规则",
        "视觉检测缺陷",
        "PLC 编程模板"
    ]

    for q in test_queries:
        results = engine.query(q)
        print(f"查询: {q}")
        print(f"  命中 {len(results)} 条:")
        for r in results:
            print(f"    [{r['entity_type']}] conf={r.get('provenance',{}).get('confidence',0)}")
            if r.get('_relations'):
                print(f"      关系: {len(r['_relations'])} 条")
        print()
