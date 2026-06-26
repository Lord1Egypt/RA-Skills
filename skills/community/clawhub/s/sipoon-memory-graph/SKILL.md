---
name: memory-graph
description: 基于 SQLite 的实体关系图谱存储，提供 add_entity / add_relation / query / traverse / get_path 等原子操作，供 skill-compounding 沉淀时调用。
version: 0.2.0
owner: local-workspace-agent
tags: [memory, graph, sqlite, knowledge]
---

# Memory Graph（知识图谱记忆）

基于 SQLite 实现 Phase 3 图数据库存储和查询，存储位置 `knowledge/graph.db`。

## 核心 API（graph_store.py）

```python
from skills.memory-graph.graph_store import add_entity, add_relation, query, traverse, get_path, stats

# 添加实体（type: 项目/技术/决策/日期/人物/技能/工具）
add_entity(type_="skill", name="brainstorming", meta={"trigger": "复杂任务规划", "confidence": 0.9})
add_entity(type_="project", name="JD Reader DRM", meta={"goal": "EPUB解密逆向"})

# 添加关系（weight: 0-1，rel: 因果/包含/依赖/触发/使用/产生）
add_relation(source="brainstorming#skill", rel="used_for", target="JD Reader DRM#project", weight=0.8)

# 搜索实体
query("brainstorming")           # name 模糊匹配
query("brainstorming", type_="skill")  # type_ 精确过滤

# 图遍历
traverse(start="brainstorming#skill", rel="used_for", direction="out")
# → [{source, rel, target, target_name, target_type, weight}]

# 找路径
get_path(from_="用户", to="JD Reader DRM", max_depth=3)

# 统计
stats()
# → {nodes, edges, by_type, by_rel, db_path}
```

## 数据模型

```
nodes (id=16字符SHA256, type_, name, meta=JSON, updated_at)
    id = SHA256("type:name") 取前16位（保证同一 type:name 不重复）
    type_ ∈ {项目, 技术, 决策, 日期, 人物, 技能, 工具}
    meta 存扩展属性（置信度、来源、标签等）

edges (id=16字符SHA256, source, rel, target, weight, meta, updated_at)
    id = SHA256("source|rel|target") 取前16位（保证唯一）
    rel ∈ {因果, 包含, 依赖, 触发, 使用, 产生, 导致, 用于, 继承}
    source/target 支持 entity_id（16字符）或 name#type 格式
```

## 与 skill-compounding 的配合

skill-compounding 沉淀时调用示例：

```python
from skills.memory-graph.graph_store import add_entity, add_relation

def on_skill_compounding(compounding_result: dict):
    """skill-compounding 触发时的实体关系沉淀"""
    skill_name = compounding_result["skill_name"]
    trigger = compounding_result.get("trigger", "")
    decisions = compounding_result.get("decisions", [])
    projects = compounding_result.get("projects", [])

    # 1. 提取实体
    skill_id = add_entity("skill", skill_name, {"trigger": trigger})
    for p in projects:
        add_entity("project", p)
    for d in decisions:
        add_entity("decision", d, {"source": "skill-compounding"})

    # 2. 建立关系
    for p in projects:
        add_relation(f"{skill_name}#skill", "用于", f"{p}#project")
    for d in decisions:
        add_relation(f"{skill_name}#skill", "导致", f"{d}#decision")
    if trigger:
        add_relation(trigger, "触发", f"{skill_name}#skill")
```

## 查询能力

| 查询 | 方法 | 说明 |
|------|------|------|
| "用户最近在做什么项目？" | traverse(user, "参与", "out") | 用户参与的项目 |
| "brainstorming 用于哪些场景？" | traverse("brainstorming#skill", "用于", "out") | 所有应用场景 |
| "决策X的影响链是什么？" | get_path("决策X", "用户", max_depth=4) | 最短因果路径 |
| "某项目用了哪些技术？" | traverse(project, "使用", "out") | 技术栈 |
| "哪些技能受某项目影响？" | traverse(project, "触发", "in") | 受影响技能 |

## 状态

| 阶段 | 状态 | 说明 |
|------|------|------|
| Phase 1：实体提取 | ✅ 规范已定义 | 正则提取，需 skill-compounding 触发 |
| Phase 2：关系推理 | ✅ 规范已定义 | 规则推断，需 skill-compounding 触发 |
| Phase 3：图数据库 | ✅ **已实现** | SQLite，graph_store.py 提供全套 API |

---

## 触发命令

"开启知识图谱"、"记忆关系图"、"实体关系检索"