# Semantic Search Skill - 使用示例

## 示例 1: 表格检索

```python
import asyncio
from src import SemanticSearchSkill

async def example_table_search():
    skill = SemanticSearchSkill()
    
    result = await skill.invoke("table_search", {
        "query": "查找包含用户信息的表",
        "resource_ids": [1, 2, 3],
        "limit": 10,
        "enable_query_enhancement": True,
        "enable_keywords": True
    })
    
    print(f"Code: {result['code']}")
    print(f"Message: {result['msg']}")
    print(f"Tables: {result['data']}")

# 运行
asyncio.run(example_table_search())
```

## 示例 2: 字段检索

```python
async def example_field_search():
    skill = SemanticSearchSkill()
    
    result = await skill.invoke("field_search", {
        "query": "查找用户的创建时间字段",
        "resource_id": 1,
        "limit": 5
    })
    
    print(f"Fields: {result['data']}")

asyncio.run(example_field_search())
```

## 示例 3: Text-to-SQL 数据生成

```python
async def example_data_gen():
    skill = SemanticSearchSkill()
    
    result = await skill.invoke("data_gen", {
        "query": "查询最近注册的用户数量",
        "resource_id": 1,
        "max_attempts": 2,
        "confidence_threshold": 0.8
    })
    
    print(f"Result: {result['data']['result']}")
    print(f"SQL: {result['data']['sql']}")

asyncio.run(example_data_gen())
```

## 示例 4: 文件检索

```python
async def example_file_search():
    skill = SemanticSearchSkill()
    
    result = await skill.invoke("file_search", {
        "query": "查找用户手册文档",
        "search_type": "text",
        "limit": 10
    })
    
    print(f"Files: {result['data']}")

asyncio.run(example_file_search())
```

## 示例 5: 在 OpenClaw 中使用

```python
# 在 OpenClaw agent 中调用
from openclaw import skill

# 表格检索
tables = await skill.invoke("semantic-search", {
    "action": "table_search",
    "query": "查找销售相关的表",
    "limit": 5
})

# 字段检索
fields = await skill.invoke("semantic-search", {
    "action": "field_search",
    "query": "查找订单日期字段",
    "resource_id": tables['data'][0]['resource_id']
})

# 数据生成
data = await skill.invoke("semantic-search", {
    "action": "data_gen",
    "query": "查询上个月的订单总数",
    "resource_id": tables['data'][0]['resource_id']
})

print(f"订单总数：{data['data']['result']}")
```

## 示例 6: 批量调用

```python
import asyncio
from src import SemanticSearchSkill

async def batch_search():
    skill = SemanticSearchSkill()
    
    # 并发执行多个查询
    tasks = [
        skill.invoke("table_search", {"query": "用户表", "limit": 5}),
        skill.invoke("table_search", {"query": "订单表", "limit": 5}),
        skill.invoke("table_search", {"query": "产品表", "limit": 5}),
    ]
    
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results):
        print(f"查询 {i+1}: {len(result['data'])} 个结果")

asyncio.run(batch_search())
```

## 配置示例

### 方式 1: 环境变量

```bash
export FLIGHT_DB_HOST="localhost"
export FLIGHT_DB_PORT="31337"
export FLIGHT_DB_USER="admin"
export FLIGHT_DB_PASSWORD="your_password"
```

### 方式 2: 配置文件

创建 `config.yaml`:

```yaml
flight_db:
  host: localhost
  port: 31337
  user: admin
  password: your_password
  insecure: true

llm:
  provider: qwen
  model: qwen-max
  api_key: your_api_key

embedding:
  model: BGE-M3
  dimension: 1024
```

### 方式 3: 代码配置

```python
skill = SemanticSearchSkill(config={
    "flight_db": {
        "host": "localhost",
        "port": 31337,
        "user": "admin",
        "password": "password"
    },
    "llm": {
        "provider": "qwen",
        "model": "qwen-max"
    }
})
```

---

*更多示例请参考 SKILL.md 和测试文件*
