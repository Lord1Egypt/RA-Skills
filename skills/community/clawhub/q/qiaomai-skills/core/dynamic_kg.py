"""
荞麦饼 Skills - 动态知识图谱 (DynamicKG)
知识拓扑结构优化
"""

import json
import time
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict
import heapq


@dataclass
class Entity:
    """知识实体"""
    id: str
    name: str
    type: str  # 人、组织、概念、事件、文档
    attributes: Dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    importance: float = 0.5  # 0-1
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Relation:
    """实体关系"""
    id: str
    source: str  # 源实体ID
    target: str  # 目标实体ID
    type: str    # 关系类型
    weight: float = 1.0  # 关系权重
    attributes: Dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class KnowledgePath:
    """知识路径"""
    entities: List[str]
    relations: List[str]
    total_weight: float
    length: int


class DynamicKnowledgeGraph:
    """动态知识图谱"""
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relations: Dict[str, Relation] = {}
        self.adjacency: Dict[str, List[str]] = defaultdict(list)  # 邻接表
        self.entity_index: Dict[str, Set[str]] = defaultdict(set)  # 类型索引
        self.relation_index: Dict[str, Set[str]] = defaultdict(set)  # 关系类型索引
        self.version = 0
    
    def add_entity(self, name: str, entity_type: str, 
                   attributes: Dict = None, importance: float = 0.5) -> str:
        """添加实体"""
        entity_id = f"ent_{name}_{entity_type}_{int(time.time())}"
        
        entity = Entity(
            id=entity_id,
            name=name,
            type=entity_type,
            attributes=attributes or {},
            importance=importance
        )
        
        self.entities[entity_id] = entity
        self.entity_index[entity_type].add(entity_id)
        self.version += 1
        
        return entity_id
    
    def add_relation(self, source_id: str, target_id: str, 
                     relation_type: str, weight: float = 1.0,
                     attributes: Dict = None) -> str:
        """添加关系"""
        if source_id not in self.entities or target_id not in self.entities:
            raise ValueError("实体不存在")
        
        relation_id = f"rel_{source_id}_{target_id}_{relation_type}"
        
        relation = Relation(
            id=relation_id,
            source=source_id,
            target=target_id,
            type=relation_type,
            weight=weight,
            attributes=attributes or {}
        )
        
        self.relations[relation_id] = relation
        self.adjacency[source_id].append(relation_id)
        self.relation_index[relation_type].add(relation_id)
        self.version += 1
        
        return relation_id
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """获取实体"""
        return self.entities.get(entity_id)
    
    def get_relation(self, relation_id: str) -> Optional[Relation]:
        """获取关系"""
        return self.relations.get(relation_id)
    
    def find_entity_by_name(self, name: str) -> List[Entity]:
        """按名称查找实体"""
        return [
            e for e in self.entities.values()
            if name.lower() in e.name.lower()
        ]
    
    def find_entities_by_type(self, entity_type: str) -> List[Entity]:
        """按类型查找实体"""
        entity_ids = self.entity_index.get(entity_type, set())
        return [self.entities[eid] for eid in entity_ids if eid in self.entities]
    
    def get_neighbors(self, entity_id: str, relation_type: str = None) -> List[Tuple[Entity, Relation]]:
        """获取邻居实体"""
        if entity_id not in self.entities:
            return []
        
        neighbors = []
        for rel_id in self.adjacency.get(entity_id, []):
            relation = self.relations.get(rel_id)
            if relation:
                if relation_type and relation.type != relation_type:
                    continue
                
                target = self.entities.get(relation.target)
                if target:
                    neighbors.append((target, relation))
        
        # 按权重排序
        neighbors.sort(key=lambda x: x[1].weight, reverse=True)
        return neighbors
    
    def find_path(self, source_id: str, target_id: str, 
                  max_depth: int = 5) -> Optional[KnowledgePath]:
        """查找实体间的路径（BFS）"""
        if source_id not in self.entities or target_id not in self.entities:
            return None
        
        # Dijkstra 算法
        distances = {source_id: 0}
        previous = {source_id: None}
        pq = [(0, source_id)]
        visited = set()
        
        while pq:
            current_dist, current_id = heapq.heappop(pq)
            
            if current_id in visited:
                continue
            visited.add(current_id)
            
            if current_id == target_id:
                # 重构路径
                path_entities = []
                path_relations = []
                node = target_id
                
                while node is not None:
                    path_entities.append(node)
                    prev = previous[node]
                    if prev:
                        # 找到关系
                        for rel_id in self.adjacency.get(prev, []):
                            rel = self.relations.get(rel_id)
                            if rel and rel.target == node:
                                path_relations.append(rel_id)
                                break
                    node = prev
                
                path_entities.reverse()
                path_relations.reverse()
                
                return KnowledgePath(
                    entities=path_entities,
                    relations=path_relations,
                    total_weight=current_dist,
                    length=len(path_relations)
                )
            
            # 探索邻居
            for rel_id in self.adjacency.get(current_id, []):
                relation = self.relations.get(rel_id)
                if relation:
                    neighbor_id = relation.target
                    weight = 1.0 / relation.weight  # 转换为距离
                    distance = current_dist + weight
                    
                    if neighbor_id not in distances or distance < distances[neighbor_id]:
                        distances[neighbor_id] = distance
                        previous[neighbor_id] = current_id
                        heapq.heappush(pq, (distance, neighbor_id))
        
        return None
    
    def find_communities(self, min_size: int = 3) -> List[List[str]]:
        """发现社区（简单连通分量）"""
        visited = set()
        communities = []
        
        def dfs(node, community):
            visited.add(node)
            community.append(node)
            
            for rel_id in self.adjacency.get(node, []):
                relation = self.relations.get(rel_id)
                if relation and relation.target not in visited:
                    dfs(relation.target, community)
        
        for entity_id in self.entities:
            if entity_id not in visited:
                community = []
                dfs(entity_id, community)
                if len(community) >= min_size:
                    communities.append(community)
        
        return communities
    
    def calculate_centrality(self, entity_id: str) -> float:
        """计算实体中心性（度中心性）"""
        if entity_id not in self.entities:
            return 0.0
        
        out_degree = len(self.adjacency.get(entity_id, []))
        in_degree = sum(
            1 for rel in self.relations.values()
            if rel.target == entity_id
        )
        
        max_degree = max(len(self.entities) - 1, 1)
        return (out_degree + in_degree) / (2 * max_degree)
    
    def infer_relation(self, entity1_id: str, entity2_id: str) -> Optional[str]:
        """推断实体间关系"""
        # 查找共同邻居
        neighbors1 = set()
        neighbors2 = set()
        
        for rel_id in self.adjacency.get(entity1_id, []):
            rel = self.relations.get(rel_id)
            if rel:
                neighbors1.add(rel.target)
        
        for rel_id in self.adjacency.get(entity2_id, []):
            rel = self.relations.get(rel_id)
            if rel:
                neighbors2.add(rel.target)
        
        common = neighbors1 & neighbors2
        
        if common:
            return f"共同关联: {len(common)} 个实体"
        
        # 查找路径
        path = self.find_path(entity1_id, entity2_id, max_depth=2)
        if path:
            return f"间接关联（距离 {path.length}）"
        
        return None
    
    def evolve(self, new_entities: List[Entity], new_relations: List[Relation]):
        """图谱演化（增量更新）"""
        # 添加新实体
        for entity in new_entities:
            if entity.id not in self.entities:
                self.entities[entity.id] = entity
                self.entity_index[entity.type].add(entity.id)
        
        # 添加新关系
        for relation in new_relations:
            if relation.id not in self.relations:
                self.relations[relation.id] = relation
                self.adjacency[relation.source].append(relation.id)
                self.relation_index[relation.type].add(relation.id)
        
        # 更新版本
        self.version += 1
        
        # 清理过期数据
        self._cleanup()
    
    def _cleanup(self):
        """清理过期数据"""
        current_time = time.time()
        expired_relations = []
        
        for rel_id, relation in self.relations.items():
            # 检查关系时效性（例如30天）
            if current_time - relation.timestamp > 30 * 24 * 3600:
                # 检查是否仍被频繁访问
                # 简化：保留权重高的关系
                if relation.weight < 0.3:
                    expired_relations.append(rel_id)
        
        # 移除过期关系
        for rel_id in expired_relations:
            relation = self.relations.pop(rel_id, None)
            if relation:
                self.adjacency[relation.source].remove(rel_id)
                self.relation_index[relation.type].discard(rel_id)
    
    def export_graph(self) -> Dict:
        """导出图谱"""
        return {
            "version": self.version,
            "entities": [e.to_dict() for e in self.entities.values()],
            "relations": [r.to_dict() for r in self.relations.values()],
            "stats": self.get_stats()
        }
    
    def import_graph(self, data: Dict):
        """导入图谱"""
        # 导入实体
        for entity_data in data.get("entities", []):
            entity = Entity(**entity_data)
            self.entities[entity.id] = entity
            self.entity_index[entity.type].add(entity.id)
        
        # 导入关系
        for relation_data in data.get("relations", []):
            relation = Relation(**relation_data)
            self.relations[relation.id] = relation
            self.adjacency[relation.source].append(relation.id)
            self.relation_index[relation.type].add(relation.id)
        
        self.version = data.get("version", 0)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        entity_types = {t: len(ids) for t, ids in self.entity_index.items()}
        relation_types = {t: len(ids) for t, ids in self.relation_index.items()}
        
        return {
            "entity_count": len(self.entities),
            "relation_count": len(self.relations),
            "entity_types": entity_types,
            "relation_types": relation_types,
            "version": self.version,
            "density": len(self.relations) / max(len(self.entities) * (len(self.entities) - 1), 1)
        }
    
    def visualize_data(self) -> Dict:
        """生成可视化数据"""
        nodes = []
        edges = []
        
        for entity in self.entities.values():
            nodes.append({
                "id": entity.id,
                "label": entity.name,
                "type": entity.type,
                "importance": entity.importance,
                "centrality": self.calculate_centrality(entity.id)
            })
        
        for relation in self.relations.values():
            edges.append({
                "source": relation.source,
                "target": relation.target,
                "label": relation.type,
                "weight": relation.weight
            })
        
        return {"nodes": nodes, "edges": edges}


class KnowledgeQueryEngine:
    """知识查询引擎"""
    
    def __init__(self, kg: DynamicKnowledgeGraph):
        self.kg = kg
    
    def query(self, query_str: str) -> Dict:
        """自然语言查询"""
        # 简单解析查询
        # 实际应使用 NLP 解析
        
        results = {
            "entities": [],
            "relations": [],
            "paths": [],
            "suggestions": []
        }
        
        # 查找实体
        entities = self.kg.find_entity_by_name(query_str)
        results["entities"] = [e.to_dict() for e in entities[:10]]
        
        # 查找关系
        for entity in entities[:3]:
            neighbors = self.kg.get_neighbors(entity.id)
            for neighbor, relation in neighbors[:5]:
                results["relations"].append({
                    "source": entity.name,
                    "target": neighbor.name,
                    "type": relation.type,
                    "weight": relation.weight
                })
        
        return results
    
    def recommend_related(self, entity_id: str, top_k: int = 5) -> List[Entity]:
        """推荐相关实体"""
        if entity_id not in self.kg.entities:
            return []
        
        # 基于共同邻居推荐
        entity = self.kg.entities[entity_id]
        neighbors = self.kg.get_neighbors(entity_id)
        
        # 收集邻居的邻居
        candidates = defaultdict(float)
        
        for neighbor, rel1 in neighbors:
            for neighbor2, rel2 in self.kg.get_neighbors(neighbor.id):
                if neighbor2.id != entity_id:
                    # 共同邻居越多，推荐度越高
                    candidates[neighbor2.id] += rel1.weight * rel2.weight
        
        # 排序并返回
        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        
        return [
            self.kg.entities[eid]
            for eid, _ in sorted_candidates[:top_k]
            if eid in self.kg.entities
        ]


# 便捷函数
def create_kg() -> DynamicKnowledgeGraph:
    """创建知识图谱"""
    return DynamicKnowledgeGraph()


def quick_query(kg: DynamicKnowledgeGraph, query: str) -> Dict:
    """快速查询"""
    engine = KnowledgeQueryEngine(kg)
    return engine.query(query)


if __name__ == "__main__":
    # 测试
    kg = DynamicKnowledgeGraph()
    
    # 添加实体
    ent1 = kg.add_entity("人工智能", "概念", {"定义": "模拟人类智能的技术"}, 0.9)
    ent2 = kg.add_entity("机器学习", "概念", {"定义": "AI的一个分支"}, 0.8)
    ent3 = kg.add_entity("深度学习", "概念", {"定义": "ML的一个分支"}, 0.8)
    ent4 = kg.add_entity("OpenAI", "组织", {"类型": "公司"}, 0.7)
    
    # 添加关系
    kg.add_relation(ent1, ent2, "包含", 0.9)
    kg.add_relation(ent2, ent3, "包含", 0.9)
    kg.add_relation(ent4, ent1, "研究", 0.8)
    kg.add_relation(ent4, ent3, "应用", 0.7)
    
    # 查询
    print("知识图谱统计:")
    print(kg.get_stats())
    
    print("\n查找路径（人工智能 -> 深度学习）:")
    path = kg.find_path(ent1, ent3)
    if path:
        print(f"路径长度: {path.length}")
        print(f"总权重: {path.total_weight:.2f}")
    
    print("\n邻居查询（人工智能）:")
    neighbors = kg.get_neighbors(ent1)
    for neighbor, relation in neighbors:
        print(f"  -> {neighbor.name} ({relation.type})")
    
    print("\n可视化数据:")
    viz_data = kg.visualize_data()
    print(f"节点数: {len(viz_data['nodes'])}")
    print(f"边数: {len(viz_data['edges'])}")
