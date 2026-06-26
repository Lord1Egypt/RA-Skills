#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 用户关系图谱
从会话中提取实体和关系，构建用户知识图谱

用法:
    from user_model import UserModel
    model = UserModel()
    model.extract_entities(session_text)  # 提取实体
    model.build_graph()                   # 构建图谱
    model.update_model()                  # 增量更新
    model.query_model("项目X")            # 按话题查询

触发时机: 每次会话结束时增量提取
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
GRAPH_DB = MEMORY_DIR / ".user_graph.json"
GRAPH_STATS = MEMORY_DIR / ".user_graph_stats.json"


# ============== 实体关系图谱 ==============

class UserModel:
    """用户关系图谱"""

    # 实体类型定义
    ENTITY_TYPES = {
        "user": {"keywords": ["用户", "客户", "联系人", "我"], "weight": 2.0},
        "project": {"keywords": ["项目", "project", "系统", "产品"], "weight": 1.8},
        "technology": {"keywords": ["技术", "框架", "库", "语言", "工具"], "weight": 1.5},
        "person": {"keywords": ["人名", "开发者", "工程师", "经理"], "weight": 1.3},
        "concept": {"keywords": ["概念", "理论", "方法", "方案", "架构"], "weight": 1.0},
        "preference": {"keywords": ["喜欢", "偏好", "习惯", "倾向"], "weight": 1.2},
    }

    # 关系类型定义
    RELATION_TYPES = [
        "works_on",      # 用户从事某项目
        "uses",          # 使用某技术
        "manages",       # 管理某项目
        "interested_in", # 对某概念感兴趣
        "has_preference", # 有某偏好
        "related_to",    # 与某实体相关
        "collaborates_with", # 与某人合作
    ]

    def __init__(self):
        self.graph = self._load_graph()
        self.stats = self._load_stats()

    # ============== 持久化 ==============

    def _load_graph(self) -> Dict:
        """加载图谱"""
        if GRAPH_DB.exists():
            try:
                return json.loads(GRAPH_DB.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "entities": {},      # {entity_id: {type, name, mentions, last_seen, properties}}
            "relations": [],      # [{source, target, type, weight, last_seen}]
            "version": 1
        }

    def _save_graph(self):
        """保存图谱"""
        try:
            GRAPH_DB.write_text(
                json.dumps(self.graph, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"[UserModel] 保存图谱失败: {e}")

    def _load_stats(self) -> Dict:
        """加载统计"""
        if GRAPH_STATS.exists():
            try:
                return json.loads(GRAPH_STATS.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "total_entities": 0,
            "total_relations": 0,
            "last_update": None,
            "entity_types": {},
            "top_entities": []
        }

    def _save_stats(self):
        """保存统计"""
        # 更新统计
        self.stats["total_entities"] = len(self.graph["entities"])
        self.stats["total_relations"] = len(self.graph["relations"])
        self.stats["last_update"] = datetime.now().isoformat()

        # 实体类型统计
        type_counts = defaultdict(int)
        for entity in self.graph["entities"].values():
            type_counts[entity.get("type", "unknown")] += 1
        self.stats["entity_types"] = dict(type_counts)

        # Top 实体（按 mentions 排序）
        top = sorted(
            self.graph["entities"].items(),
            key=lambda x: x[1].get("mentions", 0),
            reverse=True
        )[:10]
        self.stats["top_entities"] = [
            {"id": k, "name": v.get("name", ""), "mentions": v.get("mentions", 0)}
            for k, v in top
        ]

        try:
            GRAPH_STATS.write_text(
                json.dumps(self.stats, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception:
            pass

    # ============== 实体提取 ==============

    def extract_entities(self, text: str) -> List[Dict]:
        """从文本中提取实体

        Returns:
            实体列表 [{type, name, properties}]
        """
        entities = []

        # 1. 项目实体
        project_patterns = [
            r'(?:项目|project|系统|产品)[:：]\s*["\']?([^"\'\n]+?)["\']?(?:\n|$)',
            r'(?:做|开发|负责|参与)["\']?\s*([^"\'\n]{2,20}?)(?:项目|系统)',
            r'`([^`]+?项目[^`]*)`',  # 代码中的项目引用
        ]
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                name = m.strip()
                if len(name) >= 2:
                    entities.append({
                        "type": "project",
                        "name": name[:50],
                        "properties": {"source": "project_pattern"}
                    })

        # 2. 技术实体
        tech_patterns = [
            r'\b(Python|JavaScript|TypeScript|Java|Go|Rust|C\+\+|React|Vue|Angular|Flask|FastAPI|Django|Next\.js|LangGraph|RAG|OpenAI|Claude|MiniMax|Git|Docker|Kubernetes)\b',
            r'(?:使用|采用|基于)[:：]\s*([A-Za-z][A-Za-z0-9.]+)',
            r'(?:技术|框架|库)[:：]\s*["\']?([^"\'\n]+?)["\']?',
        ]
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                name = m.strip()
                if len(name) >= 2:
                    entities.append({
                        "type": "technology",
                        "name": name[:30],
                        "properties": {"source": "tech_pattern"}
                    })

        # 3. 人物实体
        person_patterns = [
            r'(?:开发者|工程师|经理|负责人|产品经理|设计师)[:：]\s*["\']?([A-Za-z\u4e00-\u9fa5]{2,10})["\']?',
            r'@([A-Za-z\u4e00-\u9fa5]{2,10})',
            r'([A-Z][a-z]+)\s+(?:说|认为|表示|指出)',
        ]
        for pattern in person_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                name = m.strip()
                if len(name) >= 2:
                    entities.append({
                        "type": "person",
                        "name": name[:20],
                        "properties": {"source": "person_pattern"}
                    })

        # 4. 概念实体
        concept_patterns = [
            r'(?:架构|设计|方案|方法|理论|概念)[:：]\s*["\']?([^"\'\n]{3,30}?)["\']?',
            r'(?:微服务|RESTful|GraphQL|CI/CD|DevOps|敏捷|Kanban)',
        ]
        for pattern in concept_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                name = m.strip()
                if len(name) >= 2:
                    entities.append({
                        "type": "concept",
                        "name": name[:50],
                        "properties": {"source": "concept_pattern"}
                    })

        # 5. 偏好实体
        preference_patterns = [
            r'(?:喜欢|偏好|倾向|习惯)[:：]\s*["\']?([^"\'\n]{2,30}?)["\']?',
            r'(?:不|讨厌|不喜欢)[:：]\s*["\']?([^"\'\n]{2,30}?)["\']?',
        ]
        for pattern in preference_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                name = m.strip()
                if len(name) >= 2:
                    entities.append({
                        "type": "preference",
                        "name": name[:50],
                        "properties": {"source": "preference_pattern"}
                    })

        # 去重
        seen = set()
        unique = []
        for e in entities:
            key = (e["type"], e["name"].lower())
            if key not in seen:
                seen.add(key)
                unique.append(e)

        return unique

    def extract_relations(self, text: str, entities: List[Dict]) -> List[Dict]:
        """从文本中提取实体间关系

        Args:
            text: 原始文本
            entities: 已提取的实体列表

        Returns:
            关系列表 [{source, target, type, weight}]
        """
        relations = []
        entity_names = [e["name"] for e in entities]

        # 提取 co-occurrence 关系（同一上下文中出现的实体）
        sentences = text.split('.')
        for sentence in sentences:
            mentioned = []
            for e in entities:
                if e["name"] in sentence:
                    mentioned.append(e)

            # 同一句中提到的实体建立关系
            for i, e1 in enumerate(mentioned):
                for e2 in mentioned[i+1:]:
                    # 判断关系类型
                    rel_type = self._infer_relation(sentence, e1, e2)
                    if rel_type:
                        relations.append({
                            "source": e1["name"],
                            "target": e2["name"],
                            "type": rel_type,
                            "weight": 1.0
                        })

        # 基于动词的关系提取
        verb_patterns = [
            (r'(\w+)\s+(?:使用|采用)\s+(\w+)', "uses"),
            (r'(\w+)\s+(?:开发|构建|实现)\s+(\w+)', "works_on"),
            (r'(\w+)\s+(?:对|关注)\s+(\w+)', "interested_in"),
            (r'(\w+)\s+(?:和|与)\s+(\w+)\s+(?:合作|一起)', "collaborates_with"),
        ]
        for pattern, rel_type in verb_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                if len(m) >= 2:
                    relations.append({
                        "source": m[0].strip(),
                        "target": m[1].strip(),
                        "type": rel_type,
                        "weight": 1.5  # 明确的关系权重更高
                    })

        # 去重
        seen = set()
        unique = []
        for r in relations:
            key = (r["source"].lower(), r["target"].lower(), r["type"])
            if key not in seen:
                seen.add(key)
                unique.append(r)

        return unique

    def _infer_relation(self, context: str, e1: Dict, e2: Dict) -> Optional[str]:
        """推断两个实体之间的关系类型"""
        ctx_lower = context.lower()

        # 基于上下文的关键词判断
        if any(kw in ctx_lower for kw in ["使用", "采用", "基于", "技术栈"]):
            return "uses"
        if any(kw in ctx_lower for kw in ["开发", "做", "参与", "负责"]):
            return "works_on"
        if any(kw in ctx_lower for kw in ["喜欢", "偏好", "感兴趣"]):
            return "interested_in"
        if any(kw in ctx_lower for kw in ["和", "与", "合作", "一起"]):
            return "collaborates_with"
        if any(kw in ctx_lower for kw in ["关于", "涉及", "相关"]):
            return "related_to"

        return "related_to"  # 默认

    # ============== 图谱构建 ==============

    def build_graph(self, texts: List[str] = None):
        """构建图谱

        Args:
            texts: 文本列表（可选，默认从 memory 读取）
        """
        if texts is None:
            texts = self._load_all_texts()

        # 增量更新
        self.update_model(texts)

    def _load_all_texts(self) -> List[str]:
        """从 memory 目录加载所有文本"""
        texts = []

        # 从 daily 加载
        daily_dir = MEMORY_DIR / "daily"
        if daily_dir.exists():
            for f in daily_dir.glob("*.md"):
                if not f.name.startswith('.'):
                    try:
                        texts.append(f.read_text(encoding="utf-8"))
                    except Exception:
                        pass

        return texts

    def update_model(self, texts: List[str] = None):
        """增量更新图谱

        Args:
            texts: 文本列表
        """
        if texts is None:
            texts = self._load_all_texts()

        all_entities = []
        all_relations = []

        for text in texts:
            entities = self.extract_entities(text)
            relations = self.extract_relations(text, entities)
            all_entities.extend(entities)
            all_relations.extend(relations)

        # 更新实体
        self._update_entities(all_entities)

        # 更新关系
        self._update_relations(all_relations)

        # 统计
        self._save_graph()
        self._save_stats()

    def _update_entities(self, new_entities: List[Dict]):
        """更新实体集合"""
        now = datetime.now().isoformat()

        for e in new_entities:
            # 生成实体 ID
            entity_id = self._generate_entity_id(e["name"])

            if entity_id in self.graph["entities"]:
                # 更新已有实体
                self.graph["entities"][entity_id]["mentions"] += 1
                self.graph["entities"][entity_id]["last_seen"] = now
            else:
                # 新增实体
                self.graph["entities"][entity_id] = {
                    "type": e["type"],
                    "name": e["name"],
                    "mentions": 1,
                    "first_seen": now,
                    "last_seen": now,
                    "properties": e.get("properties", {})
                }

    def _update_relations(self, new_relations: List[Dict]):
        """更新关系集合"""
        now = datetime.now().isoformat()

        # 现有关系索引
        existing = {}
        for i, r in enumerate(self.graph["relations"]):
            key = (r["source"].lower(), r["target"].lower(), r["type"])
            existing[key] = i

        for r in new_relations:
            key = (r["source"].lower(), r["target"].lower(), r["type"])

            if key in existing:
                # 更新权重
                idx = existing[key]
                self.graph["relations"][idx]["weight"] += r["weight"]
                self.graph["relations"][idx]["last_seen"] = now
            else:
                # 新增关系
                self.graph["relations"].append({
                    "source": r["source"],
                    "target": r["target"],
                    "type": r["type"],
                    "weight": r["weight"],
                    "first_seen": now,
                    "last_seen": now
                })
                existing[key] = len(self.graph["relations"]) - 1

    def _generate_entity_id(self, name: str) -> str:
        """生成实体 ID"""
        # 使用前30个字符 + 哈希
        import hashlib
        short_name = name.lower()[:30]
        h = hashlib.md5(short_name.encode()).hexdigest()[:6]
        return f"{short_name.replace(' ', '_')}_{h}"

    # ============== 图谱查询 ==============

    def query_model(self, topic: str, max_results: int = 10) -> Dict:
        """按话题查询相关用户特征

        Args:
            topic: 查询话题
            max_results: 最大结果数

        Returns:
            查询结果 {
                "entities": [...],  # 相关实体
                "relations": [...],  # 相关关系
                "profile": {...}      # 用户画像摘要
            }
        """
        topic_lower = topic.lower()

        # 1. 找相关实体
        relevant_entities = []
        for entity_id, entity in self.graph["entities"].items():
            name_lower = entity["name"].lower()
            # 关键词匹配
            if topic_lower in name_lower:
                relevant_entities.append(entity)
            # 实体类型权重
            elif entity["type"] in ["project", "technology"] and any(
                kw in name_lower for kw in topic_lower.split()
            ):
                relevant_entities.append(entity)

        # 按 mentions 和类型权重排序
        type_weights = {k: v["weight"] for k, v in self.ENTITY_TYPES.items()}
        relevant_entities.sort(
            key=lambda e: e["mentions"] * type_weights.get(e["type"], 1.0),
            reverse=True
        )

        # 2. 找相关关系
        relevant_relations = []
        topic_words = set(topic_lower.split())
        for r in self.graph["relations"]:
            if (topic_lower in r["source"].lower() or
                topic_lower in r["target"].lower() or
                topic_words & {r["source"].lower(), r["target"].lower()}):
                relevant_relations.append(r)

        # 3. 构建用户画像摘要
        profile = self._build_profile_summary(relevant_entities, relevant_relations)

        return {
            "topic": topic,
            "entities": relevant_entities[:max_results],
            "relations": relevant_relations[:max_results],
            "profile": profile
        }

    def _build_profile_summary(self, entities: List[Dict], relations: List[Dict]) -> Dict:
        """构建用户画像摘要"""
        profile = {
            "total_entities": len(entities),
            "entity_types": defaultdict(int),
            "top_technologies": [],
            "top_projects": [],
            "preferences": [],
            "key_contacts": []
        }

        for e in entities:
            etype = e["type"]
            profile["entity_types"][etype] += 1

            if etype == "technology" and e["mentions"] >= 2:
                profile["top_technologies"].append(e["name"])
            elif etype == "project" and e["mentions"] >= 2:
                profile["top_projects"].append(e["name"])
            elif etype == "preference":
                profile["preferences"].append(e["name"])
            elif etype == "person" and e["mentions"] >= 2:
                profile["key_contacts"].append(e["name"])

        # 限制数量
        profile["top_technologies"] = profile["top_technologies"][:5]
        profile["top_projects"] = profile["top_projects"][:5]
        profile["preferences"] = profile["preferences"][:5]
        profile["key_contacts"] = profile["key_contacts"][:5]

        return dict(profile)

    def get_entity_graph(self, entity_name: str, depth: int = 1) -> Dict:
        """获取某个实体的局部图谱

        Args:
            entity_name: 实体名称
            depth: 深度（1=直接邻居，2=邻居的邻居）

        Returns:
            {center, nodes: [], edges: []}
        """
        result = {
            "center": entity_name,
            "nodes": [],
            "edges": []
        }
        seen_nodes = {entity_name}

        # BFS 查找关系
        current_level = [entity_name]
        for d in range(depth):
            next_level = []
            for name in current_level:
                for r in self.graph["relations"]:
                    neighbor = None
                    if r["source"].lower() == name.lower():
                        neighbor = r["target"]
                    elif r["target"].lower() == name.lower():
                        neighbor = r["source"]

                    if neighbor and neighbor not in seen_nodes:
                        seen_nodes.add(neighbor)
                        next_level.append(neighbor)

                        # 查找实体信息
                        entity_info = self._find_entity_by_name(neighbor)
                        if entity_info:
                            result["nodes"].append(entity_info)

                        # 添加边
                        result["edges"].append({
                            "source": r["source"],
                            "target": r["target"],
                            "type": r["type"],
                            "weight": r["weight"]
                        })

            current_level = next_level

        return result

    def _find_entity_by_name(self, name: str) -> Optional[Dict]:
        """根据名称查找实体"""
        name_lower = name.lower()
        for entity in self.graph["entities"].values():
            if entity["name"].lower() == name_lower:
                return entity
        return None

    # ============== 工具方法 ==============

    def get_stats(self) -> Dict:
        """获取图谱统计"""
        return self.stats

    def format_query_result(self, result: Dict) -> str:
        """格式化查询结果"""
        parts = [f"\n## 用户图谱查询: {result['topic']}\n"]

        profile = result.get("profile", {})
        if profile:
            parts.append("### 用户画像\n")

            types = profile.get("entity_types", {})
            if types:
                parts.append(f"- 实体分布: {dict(types)}\n")

            tech = profile.get("top_technologies", [])
            if tech:
                parts.append(f"- 技术栈: {', '.join(tech)}\n")

            projects = profile.get("top_projects", [])
            if projects:
                parts.append(f"- 相关项目: {', '.join(projects)}\n")

            prefs = profile.get("preferences", [])
            if prefs:
                parts.append(f"- 偏好: {', '.join(prefs)}\n")

            contacts = profile.get("key_contacts", [])
            if contacts:
                parts.append(f"- 联系人: {', '.join(contacts)}\n")

        entities = result.get("entities", [])
        if entities:
            parts.append("\n### 相关实体\n")
            for e in entities[:5]:
                parts.append(f"- [{e['type']}] {e['name']} (提及: {e['mentions']})\n")

        relations = result.get("relations", [])
        if relations:
            parts.append("\n### 相关关系\n")
            for r in relations[:5]:
                parts.append(f"- {r['source']} --[{r['type']}]--> {r['target']}\n")

        return ''.join(parts)

    def vacuum(self):
        """清理低频实体和关系"""
        MIN_MENTIONS = 2
        MIN_WEIGHT = 1.5

        # 清理实体
        to_remove = []
        for entity_id, entity in self.graph["entities"].items():
            if entity.get("mentions", 0) < MIN_MENTIONS:
                to_remove.append(entity_id)

        for entity_id in to_remove:
            del self.graph["entities"][entity_id]

        # 清理关系
        self.graph["relations"] = [
            r for r in self.graph["relations"]
            if r.get("weight", 0) >= MIN_WEIGHT
        ]

        self._save_graph()
        self._save_stats()
        print(f"[UserModel] 清理完成: 移除 {len(to_remove)} 低频实体")


# ============== 与 profile_miner 集成 ==============

class ProfileMinerIntegration:
    """与 profile_miner 的集成接口"""

    def __init__(self):
        self.miner = None
        # UserModel 在同一个文件，直接引用（类已定义）
        self.model = None  # 延迟初始化

    def _get_miner(self):
        """延迟加载 profile_miner"""
        if self.miner is None:
            from profile_miner import ProfileMiner
            self.miner = ProfileMiner()
        return self.miner

    def process_session(self, text: str) -> Dict:
        """处理会话：提取偏好 + 更新图谱

        Args:
            text: 会话文本

        Returns:
            {preferences: {...}, graph: {...}}
        """
        # 1. 提取偏好（profile_miner）
        miner = self._get_miner()
        pref_results = miner.process(text)

        # 2. 提取实体（user_model）
        entities = self.model.extract_entities(text)
        relations = self.model.extract_relations(text, entities)

        # 3. 更新图谱
        self.model._update_entities(entities)
        self.model._update_relations(relations)
        self.model._save_graph()
        self.model._save_stats()

        return {
            "preferences": pref_results,
            "entities_found": len(entities),
            "relations_found": len(relations),
            "graph_stats": self.model.get_stats()
        }


# ============== 主程序 ==============

def main():
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw 用户关系图谱")
    parser.add_argument("--query", "-q", help="查询话题")
    parser.add_argument("--build", "-b", action="store_true", help="构建图谱")
    parser.add_argument("--update", "-u", action="store_true", help="增量更新")
    parser.add_argument("--stats", "-s", action="store_true", help="图谱统计")
    parser.add_argument("--vacuum", action="store_true", help="清理低频")
    parser.add_argument("--entity", "-e", help="获取实体局部图谱")
    parser.add_argument("--depth", "-d", type=int, default=1, help="图谱深度")
    args = parser.parse_args()

    model = UserModel()

    if args.build:
        print("[UserModel] 正在构建图谱...")
        model.build_graph()
        print(f"[OK] 完成: {len(model.graph['entities'])} 实体, {len(model.graph['relations'])} 关系")
        return

    if args.update:
        print("[UserModel] 正在更新图谱...")
        model.update_model()
        print(f"[OK] 更新完成")
        return

    if args.vacuum:
        print("[UserModel] 正在清理...")
        model.vacuum()
        return

    if args.stats:
        stats = model.get_stats()
        print("## 用户图谱统计\n")
        print(f"  实体总数: {stats.get('total_entities', 0)}")
        print(f"  关系总数: {stats.get('total_relations', 0)}")
        print(f"  最后更新: {stats.get('last_update', 'N/A')}")
        print(f"\n  实体类型分布:")
        for t, c in stats.get('entity_types', {}).items():
            print(f"    - {t}: {c}")
        print(f"\n  Top 实体:")
        for e in stats.get('top_entities', [])[:5]:
            print(f"    - {e['name']} (提及: {e['mentions']})")
        return

    if args.entity:
        graph = model.get_entity_graph(args.entity, depth=args.depth)
        print(f"\n## {args.entity} 的局部图谱\n")
        print(f"节点: {len(graph['nodes'])}")
        print(f"边: {len(graph['edges'])}\n")
        for n in graph['nodes']:
            print(f"- [{n['type']}] {n['name']}")
        for e in graph['edges']:
            print(f"  {e['source']} --[{e['type']}]--> {e['target']}")
        return

    if args.query:
        result = model.query_model(args.query)
        print(model.format_query_result(result))
        return

    parser.print_help()


if __name__ == "__main__":
    main()