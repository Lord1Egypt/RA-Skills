# Semantic Search Skill 配置指南

## 📋 必需配置

### 1. 数据库连接 (必需)

**FlightSQL 数据库配置**:

```python
# 方式 1: 环境变量
export FLIGHT_DB_HOST="localhost"
export FLIGHT_DB_PORT="31337"
export FLIGHT_DB_USER="admin"
export FLIGHT_DB_PASSWORD="your_password"
export FLIGHT_DB_INSECURE="true"
```

```yaml
# 方式 2: config.yaml 配置文件
flight_db:
  host: localhost
  port: 31337
  user: admin
  password: your_password
  insecure: true
```

```python
# 方式 3: 代码中直接配置
skill = SemanticSearchSkill(config={
    "flight_db": {
        "host": "localhost",
        "port": 31337,
        "user": "admin",
        "password": "your_password",
        "insecure": True
    }
})
```

---

### 2. LLM 配置 (必需)

**用于意图识别、SQL 生成、查询增强**:

```python
# 方式 1: 环境变量
export LLM_PROVIDER="qwen"  # 或 deepseek, openai
export LLM_MODEL="qwen-max"
export LLM_API_KEY="sk-xxx"
```

```yaml
# 方式 2: config.yaml
llm:
  provider: qwen  # qwen | deepseek | openai
  model: qwen-max
  api_key: sk-xxx
  base_url: https://dashscope.aliyuncs.com/compatible-mode/v1  # 可选
```

---

### 3. Embedding 配置 (必需)

**用于向量化查询和文档**:

```yaml
# config.yaml
embedding:
  model: BGE-M3  # 或 text-embedding-3-small
  dimension: 1024  # BGE-M3 是 1024 维
  api_key: sk-xxx  # 如果使用 API
```

**注意**: 项目中使用的是本地 BGE-M3 模型，需要安装：
```bash
pip install FlagEmbedding
```

---

### 4. Rerank 配置 (可选)

**用于结果重排序，提升精度**:

```yaml
# config.yaml
rerank:
  model: BGE-Reranker
  api_key: sk-xxx  # 如果需要
```

---

### 5. Nacos 配置 (可选，如果项目使用)

**动态配置管理**:

```yaml
# config.yaml
nacos:
  server_addr: localhost:8848
  namespace: your_namespace
  username: nacos
  password: nacos
```

---

## 🔧 完整配置示例

### config.yaml (推荐)

```yaml
# 数据库配置
flight_db:
  host: localhost
  port: 31337
  user: admin
  password: your_password
  insecure: true

# LLM 配置
llm:
  provider: qwen
  model: qwen-max
  api_key: sk-xxx

# Embedding 配置
embedding:
  model: BGE-M3
  dimension: 1024

# Rerank 配置 (可选)
rerank:
  model: BGE-Reranker

# 日志配置
logging:
  level: INFO  # DEBUG | INFO | WARNING | ERROR
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## 📝 使用方式

### 1. 加载配置文件

```python
from src import SemanticSearchSkill
import yaml

# 读取配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 创建 skill 实例
skill = SemanticSearchSkill(config=config)

# 调用
result = await skill.invoke("table_search", {
    "query": "查找用户表",
    "limit": 10
})
```

### 2. 使用环境变量

```python
import os
from src import SemanticSearchSkill

# 环境变量会自动被读取
skill = SemanticSearchSkill()

result = await skill.invoke("field_search", {
    "query": "查找时间字段",
    "resource_id": 1
})
```

### 3. 混合配置

```python
skill = SemanticSearchSkill(config={
    "flight_db": {
        "host": os.getenv("FLIGHT_DB_HOST"),
        "port": int(os.getenv("FLIGHT_DB_PORT")),
        "user": os.getenv("FLIGHT_DB_USER"),
        "password": os.getenv("FLIGHT_DB_PASSWORD"),
    },
    "llm": {
        "provider": "qwen",
        "api_key": os.getenv("QWEN_API_KEY")
    }
})
```

---

## 🚀 快速开始

### 最小配置 (仅测试)

```yaml
# config.minimal.yaml
flight_db:
  host: localhost
  port: 31337
  user: admin
  password: test

llm:
  provider: qwen
  model: qwen-turbo  # 使用最便宜的模型
  api_key: sk-xxx
```

### 生产配置

```yaml
# config.production.yaml
flight_db:
  host: your-production-db.com
  port: 31337
  user: prod_user
  password: secure_password
  insecure: false

llm:
  provider: qwen
  model: qwen-max  # 使用最强模型
  api_key: sk-xxx
  
embedding:
  model: BGE-M3
  dimension: 1024

rerank:
  model: BGE-Reranker
  top_k: 10

logging:
  level: INFO
```

---

## ⚠️ 注意事项

1. **数据库连接**: 必须确保 FlightSQL 服务可访问
2. **API Key**: 妥善保管，不要提交到 Git
3. **模型选择**: 
   - 测试：qwen-turbo (便宜)
   - 生产：qwen-max (准确)
4. **向量维度**: 必须与数据库中的一致 (BGE-M3 是 1024 维)
5. **超时设置**: 建议设置合理的超时时间 (默认 60 秒)

---

## 🔍 配置验证

运行以下命令验证配置：

```bash
python -c "
import yaml
from src import SemanticSearchSkill

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

skill = SemanticSearchSkill(config=config)
print('✅ 配置加载成功！')
"
```

---

## 📞 获取配置信息

如果你使用的是现有项目，配置可能在：

1. **项目配置文件**: `utils/config.py`
2. **环境变量**: `.env` 文件
3. **Nacos 配置中心**: 如果项目使用了 Nacos
4. **Docker 环境变量**: 如果是 Docker 部署

从这些文件中可以找到数据库连接、LLM API Key 等配置信息。

---

*创建时间：2026-03-04*
