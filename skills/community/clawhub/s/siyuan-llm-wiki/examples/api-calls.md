# 思源 API 调用示例

## 基础配置

```bash
SIYUAN_API="http://127.0.0.1:6806"  # 如使用自定义端口请修改
TOKEN="你的API Token"
NOTEBOOK="你的笔记本ID"
```

## 1. 系统检查

### 获取版本
```bash
curl -X POST "$SIYUAN_API/api/system/version" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**响应：**
```json
{
  "code": 0,
  "msg": "",
  "data": "3.1.28"
}
```

## 2. 笔记本操作

### 列出所有笔记本
```bash
curl -X POST "$SIYUAN_API/api/notebook/lsNotebooks" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**响应：**
```json
{
  "code": 0,
  "msg": "",
  "data": {
    "notebooks": [
      {
        "id": "20240430120000-abc123",
        "name": "LLM-Wiki",
        "icon": "1f4d6",
        "sort": 0,
        "closed": false
      }
    ]
  }
}
```

### 获取文档树
```bash
curl -X POST "$SIYUAN_API/api/filetree/listDocTree" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notebook": "'"$NOTEBOOK"'",
    "path": "/"
  }'
```

## 3. 文档操作

### 用 Markdown 创建文档
```bash
curl -X POST "$SIYUAN_API/api/filetree/createDocWithMd" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notebook": "'"$NOTEBOOK"'",
    "path": "/sources/karpathy-llm-wiki-gist",
    "markdown": "# Karpathy LLM Wiki Gist\n\n## 元信息\n- **类型**: article\n- **来源**: https://gist.github.com/karpathy/...\n- **作者**: [[Andrej-Karpathy]]\n- **日期**: 2026-04\n- **标签**: #source #llm #knowledge-management\n\n## TL;DR\nKarpathy 提出了一种用 LLM 维护个人知识库的新模式...\n\n## 核心要点\n1. 把 LLM 当知识工程师，不是搜索引擎\n2. 维护结构化的 Markdown 知识库\n3. 知识库会复利增长\n\n## 相关链接\n- [[LLM-Wiki模式]]"
  }'
```

**响应：**
```json
{
  "code": 0,
  "msg": "",
  "data": "20240430124500-xyz789"
}
```
`data` 字段就是新创建文档的 ID。

### 追加块到文档
```bash
curl -X POST "$SIYUAN_API/api/block/appendBlock" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "parentID": "20240430124500-xyz789",
    "dataType": "markdown",
    "data": "## 新增章节\n\n这是追加的内容，包含 [[双向链接]]。"
  }'
```

### 更新块内容
```bash
curl -X POST "$SIYUAN_API/api/block/updateBlock" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "20240430124501-aaa111",
    "dataType": "markdown",
    "data": "更新后的块内容"
  }'
```

### 获取块 Kramdown 源码
```bash
curl -X POST "$SIYUAN_API/api/block/getBlockKramdown" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "20240430124500-xyz789"
  }'
```

## 4. 查询

### SQL 查询：查找知识库中所有段落
```bash
curl -X POST "$SIYUAN_API/api/query/sql" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stmt": "SELECT id, content, path, updated FROM blocks WHERE path LIKE '\''/LLM-Wiki/%'\'' AND type = '\''p'\'' ORDER BY updated DESC LIMIT 20"
  }'
```

### SQL 查询：搜索包含关键词的文档
```bash
curl -X POST "$SIYUAN_API/api/query/sql" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stmt": "SELECT id, content, path FROM blocks WHERE (content LIKE '\''%RAG%'\'' OR content LIKE '\''%检索增强%') AND path LIKE '\''/LLM-Wiki/%'\'' LIMIT 30"
  }'
```

### SQL 查询：查找某个文档下的所有子块
```bash
curl -X POST "$SIYUAN_API/api/query/sql" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stmt": "SELECT id, content, type FROM blocks WHERE path = '\''/LLM-Wiki/sources/karpathy-llm-wiki-gist.sy'\'' ORDER BY created"
  }'
```

### SQL 查询：查找引用关系
```bash
curl -X POST "$SIYUAN_API/api/query/sql" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stmt": "SELECT * FROM refs WHERE defBlockPath LIKE '\''/LLM-Wiki/entities/%'\'' LIMIT 20"
  }'
```

### 搜索文档
```bash
curl -X POST "$SIYUAN_API/api/filetree/searchDocs" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "k": "Karpathy",
    "flashcard": false
  }'
```

## 5. 属性操作

### 设置块属性
```bash
curl -X POST "$SIYUAN_API/api/attr/setBlockAttrs" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "20240430124500-xyz789",
    "attrs": {
      "custom-importance": "high",
      "custom-status": "reviewed",
      "custom-domain": "ai"
    }
  }'
```

### 获取块属性
```bash
curl -X POST "$SIYUAN_API/api/attr/getBlockAttrs" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "20240430124500-xyz789"
  }'
```

### SQL 按属性筛选
```bash
curl -X POST "$SIYUAN_API/api/query/sql" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stmt": "SELECT a.block_id, b.content, a.value FROM attributes AS a JOIN blocks AS b ON a.block_id = b.id WHERE a.name = 'custom-importance' AND a.value = 'high'"
  }'
```

## 6. 实用查询组合

### 查找知识库中最近 7 天更新的文档
```sql
SELECT DISTINCT path, updated 
FROM blocks 
WHERE path LIKE '/LLM-Wiki/%' 
  AND type = 'd' 
  AND updated > strftime('%Y%m%d%H%M%S', 'now', '-7 days')
ORDER BY updated DESC;
```

### 统计各类型文档数量
```sql
SELECT 
  CASE 
    WHEN path LIKE '/LLM-Wiki/sources/%' THEN 'sources'
    WHEN path LIKE '/LLM-Wiki/entities/%' THEN 'entities'
    WHEN path LIKE '/LLM-Wiki/concepts/%' THEN 'concepts'
    WHEN path LIKE '/LLM-Wiki/syntheses/%' THEN 'syntheses'
    ELSE 'other'
  END as doc_type,
  COUNT(*) as count
FROM blocks 
WHERE path LIKE '/LLM-Wiki/%' AND type = 'd'
GROUP BY doc_type;
```

### 查找没有被引用的文档（孤立页面）
```sql
SELECT b.path, b.content 
FROM blocks b 
WHERE b.path LIKE '/LLM-Wiki/%' 
  AND b.type = 'd'
  AND b.id NOT IN (
    SELECT DISTINCT defBlockID 
    FROM refs 
    WHERE defBlockPath LIKE '/LLM-Wiki/%'
  );
```
