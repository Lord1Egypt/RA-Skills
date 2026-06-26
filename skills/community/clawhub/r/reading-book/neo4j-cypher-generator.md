# 🗄️ Neo4j Cypher生成技能 (Neo4j Cypher Generator Skill)

> **创建日期**: 2026-03-22
> **版本**: 1.0
> **用途**: 将概念列表转换为分批次的Neo4j Cypher语句
> **标签**: #Neo4j #Cypher #知识图谱 #批次化

---

## 🎯 核心职责

接收结构化的概念和关系数据，生成批次化的Cypher语句，确保每批次的语句数量可控，避免参数过长导致的执行失败。

---

## 📋 操作流程

### Step 1: 接收概念数据

**输入格式**:
```json
{
  "book_title": "书名",
  "chapter": 1,
  "concepts": [
    {
      "name": "概念名称",
      "category": "书籍/类别/子类别",
      "chapter": 1,
      "description": "清晰描述",
      "formula": "公式/标准 (可选)",
      "importance": "5star",
      "author_quote": "作者观点 (可选)"
    }
  ],
  "relationships": [
    {
      "from": "概念1",
      "to": "概念2",
      "type": "INCLUDES",
      "description": "描述"
    }
  ]
}
```

---

### Step 2: 构建批次化Cypher语句

**⚠️ 关键规则：批次化处理**

为避免PowerShell参数过长报错，必须分批次生成Cypher：

| 批次类型 | 语句数量 | 说明 |
|---------|---------|------|
| **索引批次** | 1-2条 | 单独创建索引 |
| **概念批次** | 3-5条 | 每批创建3-5个概念节点 |
| **关系批次** | 2-3条 | 每批创建2-3个关系 |

**批次构建逻辑**:
```python
def build_batches(concepts, relationships):
    """
    构建批次化Cypher语句
    """
    batches = []
    batch_id = 1

    # Batch 1: 创建索引（单独）
    batches.append({
        "batch_id": batch_id,
        "type": "index",
        "cypher": "CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)",
        "statement": f'{{"statements": [{{"statement": "CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)"}}]}}'
    })
    batch_id += 1

    # Batches: 创建概念（每批3-5个）
    concept_batches = [concepts[i:i+4] for i in range(0, len(concepts), 4)]
    for batch_concepts in concept_batches:
        cypher_statements = []
        for concept in batch_concepts:
            # 构建概念CREATE语句
            props = f"name: '{concept['name']}', category: '{concept['category']}', chapter: {concept['chapter']}"
            if concept.get('description'):
                props += f", description: '{escape_single_quote(concept['description'])}'"
            if concept.get('formula'):
                props += f", formula: '{escape_single_quote(concept['formula'])}'"
            if concept.get('importance'):
                props += f", importance: '{concept['importance']}'"
            if concept.get('author_quote'):
                props += f", author_quote: '{escape_single_quote(concept['author_quote'])}'"

            cypher_statements.append(f"CREATE (:Concept {{{props}}})")

        cypher = "; ".join(cypher_statements)
        batches.append({
            "batch_id": batch_id,
            "type": "concepts",
            "count": len(batch_concepts),
            "cypher": cypher,
            "statement": f'{{"statements": [{{"statement": "{cypher}"}}]}}'
        })
        batch_id += 1

    # Batches: 创建关系（每批2-3个）
    relationship_batches = [relationships[i:i+2] for i in range(0, len(relationships), 2)]
    for batch_rels in relationship_batches:
        cypher_statements = []
        for rel in batch_rels:
            cypher_statements.append(
                f"MATCH (a:Concept {{name: '{rel['from']}'}}), (b:Concept {{name: '{rel['to']}'}}) "
                f"CREATE (a)-[:{rel['type']}]->(b)"
            )

        cypher = "; ".join(cypher_statements)
        batches.append({
            "batch_id": batch_id,
            "type": "relationships",
            "count": len(batch_rels),
            "cypher": cypher,
            "statement": f'{{"statements": [{{"statement": "{cypher}"}}]}}'
        })
        batch_id += 1

    return batches
```

---

### Step 3: 生成标准输出

**输出格式**:
```json
{
  "book_title": "Security Analysis",
  "chapter": 1,
  "batches": [
    {
      "batch_id": 1,
      "type": "index",
      "cypher": "CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)",
      "statement": "{\"statements\": [{\"statement\": \"CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)\"}]}"
    },
    {
      "batch_id": 2,
      "type": "concepts",
      "count": 3,
      "cypher": "CREATE (:Concept {name: 'Intrinsic Value', category: 'Security Analysis/Core Concepts', chapter: 1, description: '由资产、收益、股息等事实确定的内在价值', importance: '5star', author_quote: 'The intrinsic value of a business is determined by its assets, earnings, dividends and definite future prospects.'}); CREATE (:Concept {name: 'Security Analysis', category: 'Security Analysis/Core Concepts', chapter: 1, description: '对证券的价值分析过程', importance: '5star'}); CREATE (:Concept {name: 'Margin of Safety', category: 'Security Analysis/Core Concepts', chapter: 1, description: '价格与内在价值之间的安全边际', importance: '5star'})",
      "statement": "{\"statements\": [{\"statement\": \"CREATE (:Concept {name: 'Intrinsic Value', category: 'Security Analysis/Core Concepts', chapter: 1, description: '由资产、收益、股息等事实确定的内在价值', importance: '5star', author_quote: 'The intrinsic value of a business is determined by its assets, earnings, dividends and definite future prospects.'}); CREATE (:Concept {name: 'Security Analysis', category: 'Security Analysis/Core Concepts', chapter: 1, description: '对证券的价值分析过程', importance: '5star'}); CREATE (:Concept {name: 'Margin of Safety', category: 'Security Analysis/Core Concepts', chapter: 1, description: '价格与内在价值之间的安全边际', importance: '5star'})\"}]}"
    },
    {
      "batch_id": 3,
      "type": "concepts",
      "count": 2,
      "cypher": "CREATE (:Concept {name: 'Market Price', category: 'Security Analysis/Market', chapter: 1, description: '证券的市场交易价格', importance: '4star'}); CREATE (:Concept {name: 'Book Value', category: 'Security Analysis/Valuation', chapter: 1, description: '基于资产的账面价值', importance: '4star'})",
      "statement": "{\"statements\": [{\"statement\": \"CREATE (:Concept {name: 'Market Price', category: 'Security Analysis/Market', chapter: 1, description: '证券的市场交易价格', importance: '4star'}); CREATE (:Concept {name: 'Book Value', category: 'Security Analysis/Valuation', chapter: 1, description: '基于资产的账面价值', importance: '4star'})\"}]}"
    },
    {
      "batch_id": 4,
      "type": "relationships",
      "count": 2,
      "cypher": "MATCH (a:Concept {name: 'Security Analysis'}), (b:Concept {name: 'Intrinsic Value'}) CREATE (a)-[:DEFINES]->(b); MATCH (a:Concept {name: 'Security Analysis'}), (b:Concept {name: 'Margin of Safety'}) CREATE (a)-[:REQUIRES]->(b)",
      "statement": "{\"statements\": [{\"statement\": \"MATCH (a:Concept {name: 'Security Analysis'}), (b:Concept {name: 'Intrinsic Value'}) CREATE (a)-[:DEFINES]->(b); MATCH (a:Concept {name: 'Security Analysis'}), (b:Concept {name: 'Margin of Safety'}) CREATE (a)-[:REQUIRES]->(b)\"}]}"
    },
    {
      "batch_id": 5,
      "type": "relationships",
      "count": 1,
      "cypher": "MATCH (a:Concept {name: 'Intrinsic Value'}), (b:Concept {name: 'Book Value'}) CREATE (a)-[:RELATED_TO]->(b)",
      "statement": "{\"statements\": [{\"statement\": \"MATCH (a:Concept {name: 'Intrinsic Value'}), (b:Concept {name: 'Book Value'}) CREATE (a)-[:RELATED_TO]->(b)\"}]}"
    }
  ],
  "total_batches": 5,
  "total_concepts": 5,
  "total_relationships": 3
}
```

---

## 🔧 关键语法规范

### 1. 引号转义规则

**必须使用单引号**:
```cypher
✅ 正确: CREATE (:Concept {name: 'Intrinsic Value'})
❌ 错误: CREATE (:Concept {name: "Intrinsic Value"})
```

**JSON中的转义**:
```json
{
  "statement": "{\"statements\": [{\"statement\": \"CREATE (:Concept {name: 'Intrinsic Value'})\"}]}"
}
```

### 2. 属性值转义

```python
def escape_single_quote(text):
    """转义单引号"""
    return text.replace("'", "\\'")
```

### 3. MATCH-CREATE模式

创建关系必须先MATCH节点:
```cypher
✅ 正确: MATCH (a:Concept {name: 'A'}), (b:Concept {name: 'B'}) CREATE (a)-[:REL]->(b)
❌ 错误: CREATE (:Concept {name: 'A'})-[:REL]->(:Concept {name: 'B'})
```

---

## 📊 批次统计表格

**生成批次概览**:
```markdown
| 批次ID | 类型 | 数量 | Cypher预览 |
|--------|------|------|-----------|
| Batch 1 | 索引 | 2 | CREATE INDEX ... |
| Batch 2 | 概念 | 3 | CREATE (:Concept {name: 'Intrinsic Value'... |
| Batch 3 | 概念 | 2 | CREATE (:Concept {name: 'Market Price'... |
| Batch 4 | 关系 | 2 | MATCH (a:Concept... CREATE (a)-[:DEFINES]->(b) |
| Batch 5 | 关系 | 1 | MATCH (a:Concept... CREATE (a)-[:RELATED_TO]->(b) |

**总计**: 5批次, 5概念, 3关系
```

---

## ✅ 质量检查清单

### 语法检查
- [ ] 所有属性值使用单引号
- [ ] JSON中的statement字段正确转义
- [ ] 每批语句数量符合规范（概念3-5个，关系2-3个）
- [ ] 索引批次单独创建

### 逻辑检查
- [ ] 概念category格式正确：`书名/类别/子类别`
- [ ] chapter字段与输入一致
- [ ] importance字段值为5star/4star/3star
- [ ] 关系类型使用大写（INCLUDES, REQUIRES等）
- [ ] 关系创建使用MATCH-CREATE模式

### 完整性检查
- [ ] 所有概念都已包含
- [ ] 所有关系都已包含
- [ ] batch_id连续无重复
- [ ] total_batches、total_concepts、total_relationships准确

---

## 🎓 使用示例

**输入**:
```json
{
  "book_title": "Security Analysis",
  "chapter": 1,
  "concepts": [
    {
      "name": "Intrinsic Value",
      "category": "Security Analysis/Core Concepts",
      "chapter": 1,
      "description": "由资产、收益、股息等事实确定的内在价值",
      "importance": "5star"
    }
  ],
  "relationships": [
    {
      "from": "Security Analysis",
      "to": "Intrinsic Value",
      "type": "DEFINES",
      "description": "Security analysis defines intrinsic value"
    }
  ]
}
```

**输出**:
```json
{
  "book_title": "Security Analysis",
  "chapter": 1,
  "batches": [
    {
      "batch_id": 1,
      "type": "index",
      "cypher": "CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)",
      "statement": "{\"statements\": [{\"statement\": \"CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)\"}]}"
    },
    {
      "batch_id": 2,
      "type": "concepts",
      "count": 1,
      "cypher": "CREATE (:Concept {name: 'Intrinsic Value', category: 'Security Analysis/Core Concepts', chapter: 1, description: '由资产、收益、股息等事实确定的内在价值', importance: '5star'})",
      "statement": "{\"statements\": [{\"statement\": \"CREATE (:Concept {name: 'Intrinsic Value', category: 'Security Analysis/Core Concepts', chapter: 1, description: '由资产、收益、股息等事实确定的内在价值', importance: '5star'})\"}]}"
    },
    {
      "batch_id": 3,
      "type": "relationships",
      "count": 1,
      "cypher": "MATCH (a:Concept {name: 'Security Analysis'}), (b:Concept {name: 'Intrinsic Value'}) CREATE (a)-[:DEFINES]->(b)",
      "statement": "{\"statements\": [{\"statement\": \"MATCH (a:Concept {name: 'Security Analysis'}), (b:Concept {name: 'Intrinsic Value'}) CREATE (a)-[:DEFINES]->(b)\"}]}"
    }
  ],
  "total_batches": 3,
  "total_concepts": 1,
  "total_relationships": 1
}
```

---

## 🔄 与其他模块的接口

**上游模块**:
- `note-generator`: 接收concepts和relationships

**下游模块**:
- `neo4j-importer`: 接收batches列表进行导入
- `book-learning-coordinator`: 接收批次统计信息

---

## ⚠️ 常见错误及修复

| 错误 | 原因 | 修复方案 |
|------|------|---------|
| 参数过长 | 单批概念超过5个 | 拆分为多个批次 |
| 语法错误 | 双引号未转义 | 全部改为单引号 |
| 关系创建失败 | 节点不存在 | 确保概念批次先执行 |
| 索引冲突 | 索引已存在 | 使用IF NOT EXISTS |

---

## 🛠️ OpenClaw 脚本配置

**脚本文件**: `neo4j-cypher-generator-script.py`
**脚本类型**: Python
**调用方式**: 外部工具
**依赖**: 需要先执行 note-generator-script.py 获取概念数据

### 执行命令
```bash
python neo4j-cypher-generator-script.py --concepts_data <JSON数据>
```

### 输入参数
```json
{
  "book_title": "Security Analysis",
  "chapter": 1,
  "concepts": [
    {
      "name": "Intrinsic Value",
      "category": "Security Analysis/Core Concepts",
      "chapter": 1,
      "description": "由资产、收益、股息等事实确定的内在价值",
      "importance": "5star"
    }
  ],
  "relationships": [
    {
      "from": "Security Analysis",
      "to": "Intrinsic Value",
      "type": "DEFINES",
      "description": "Security analysis defines intrinsic value"
    }
  ]
}
```

### 输出格式
```json
{
  "success": true,
  "book_title": "Security Analysis",
  "chapter": 1,
  "batches": [
    {
      "batch_id": 1,
      "type": "index",
      "cypher": "CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)",
      "statement": "{\"statements\": [{\"statement\": \"CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)\"}]}"
    },
    {
      "batch_id": 2,
      "type": "concepts",
      "count": 1,
      "cypher": "CREATE (:Concept {name: 'Intrinsic Value', category: 'Security Analysis/Core Concepts', chapter: 1, description: '由资产、收益、股息等事实确定的内在价值', importance: '5star'})",
      "statement": "{\"statements\": [{\"statement\": \"CREATE (:Concept {name: 'Intrinsic Value', category: 'Security Analysis/Core Concepts', chapter: 1, description: '由资产、收益、股息等事实确定的内在价值', importance: '5star'})\"}]}"
    }
  ],
  "total_batches": 2,
  "total_concepts": 1,
  "total_relationships": 1
}
```

### OpenClaw 调用逻辑
1. 接收概念和关系数据（来自 note-generator）
2. 构建批次化Cypher语句（索引、概念、关系分批）
3. 验证语法正确性
4. 生成批次统计
5. 返回批次列表供 neo4j-importer 使用

### 错误处理
- 概念数据为空 → 提示需要先提取概念
- 批次生成失败 → 返回错误详情
- 语法验证失败 → 列出具体问题

---

_Neo4j Cypher Generator v1.0 · 2026-03-22_ 🗄️
