# Semantic Search 项目配置清单

**查看时间**: 2026-03-04  
**配置来源**: `utils/config.py` (Nacos 配置中心)

---

## 📋 完整配置

### 1. 数据库配置 (FlightSQL)

```python
"flight_db": {
    "host": "192.168.0.221",
    "port": 33460,
    "user": "admin",
    "password": "password",
    "insecure": True
}
```

---

### 2. LLM 配置

**主模型**:
```python
"llm": {
    "model": "qwen3_30b",
    "api_key": "EMPTY",
    "base_url": "http://192.168.0.14:8867/v1"
}
```

**多模型配置**:
```python
"model_info": [
    {
        "model_name": "DeepSeek-R1-Distill-Qwen-32B",
        "model_show_name": "Deepseek-32B",
        "base_url": "http://192.168.0.153:11358/v1",
        "api_key": "EMPTY",
        "think_model": 1
    },
    {
        "model_name": "qwen2.5-14",
        "model_show_name": "Qwen2.5-14B",
        "base_url": "http://192.168.0.153:9666/v1",
        "api_key": "EMPTY",
        "think_model": 2
    },
    {
        "model_name": "Qwen3-14B",
        "model_show_name": "Qwen3-14B",
        "base_url": "http://192.168.0.155:9555/v1",
        "api_key": "EMPTY",
        "think_model": 3
    }
]
```

---

### 3. Embedding 配置

```python
"embedding": {
    "model": "bge-m3",
    "api_key": "empty",
    "base_url": "http://192.168.0.153:9998/v1",
    "dimensions": 1024
}
```

---

### 4. Rerank 配置

**BGE Reranker**:
```python
"rerank": {
    "model": "bge-reranker-v2-m3",
    "url": "http://192.168.0.153:12313/v1/rerank"
}
```

**Qwen Reranker**:
```python
"qwen_rerank": {
    "model": "Qwen3-Reranker-0.6B",
    "url": "http://192.168.0.17:8002/v1/rerank"
}
```

---

### 5. 向量数据库表配置

**结构化表**:
```python
"struct_table": "struct_table",
"struct_table_embed_field": ["file_name", "fields_abstract", "resource_abstract"],

"sub_struct_table": "sub_struct_table",
"sub_struct_table_embed_field": ["field_desc"],
```

**文本表**:
```python
"text_table": "text_table",
"text_table_embed_field": ["summary", "chunk", "question1", "question2", "question3"],

"sub_text_table": "sub_text_table",
"sub_text_table_embed_field": ["file_name", "resource_abstract"],
```

**历史表**:
```python
"history_table": ["struct_1128"]
```

---

### 6. Nacos 配置中心

```python
"NACOS_CONFIG": {
    "server_addresses": "nacos.nacos.svc.cluster.local:8848",
    "namespace": "datacenter",
    "username": "bjsh",
    "password": "pwd123",
},
"DATA_ID": "semantic_search",
"GROUP": "DEFAULT_GROUP"
```

---

### 7. 其他服务配置

**QA 生成**:
```python
"qa_generate_api": "http://192.168.0.221/generate-questions",
"qa_time_out": 3600,
```

**知识库**:
```python
"kb_url": "http://192.168.0.221/ksh/v1/table_label/result/send_back?file_id=",
"kg_info": "http://192.168.0.221/ami/gdb/get_file_tags/",
```

**RocketMQ**:
```python
"rocketmq": {
    "name_server": "192.168.0.221:9876",
    "topic": "data_latitude_longitude_data_context",
    "group_id": "refresh_summary_group",
    "postgres": {
        "host": "192.168.0.215",
        "user": "postgres",
        "dbname": "data_latitude_longitude",
        "password": "bjsh",
        "port": "24410",
        "sslmode": "disable",
        "application_name": "data_latitude_longitude"
    }
}
```

---

### 8. 模型版本配置

```python
"recall_model_version": {
    "yingji": {
        "model_name": "指挥调度专用模型",
        "version": "v1.0.0",
        "description": "使用 qwen3+bge-m3+rerank 模型"
    },
    "guotu": {
        "model_name": "国土变更调查专用模型",
        "version": "v1.0.0",
        "description": "使用 qwen3+bge-m3+rerank 模型"
    },
    "shenpi": {
        "model_name": "单独选址专用模型",
        "version": "v1.0.0",
        "description": "使用 qwen3+bge-m3+rerank 模型"
    },
    "general": {
        "model_name": "通用模型",
        "version": "v1.0.0",
        "description": "使用 qwen3+bge-m3+rerank 模型"
    }
}
```

---

## 🎯 Skill 使用的核心配置

Semantic Search Skill 主要使用以下配置：

| 配置项 | 用途 | 值 |
|--------|------|-----|
| `flight_db` | 向量数据库连接 | 192.168.0.221:33460 |
| `llm` | 主 LLM 模型 | qwen3_30b |
| `embedding` | 向量化模型 | bge-m3 (1024 维) |
| `rerank` | 重排序模型 | bge-reranker-v2-m3 |
| `text_table` | 文本向量表 | text_table |
| `struct_table` | 结构化向量表 | struct_table |

---

## 📝 配置加载方式

**优先级**:
1. Nacos 配置中心 (优先)
2. 本地 fallback 配置 (Nacos 失败时)

**加载代码**:
```python
try:
    CONFIG = get_nacos_config()
    logger.info(f"Nacos 配置获取成功")
except Exception as e:
    CONFIG = { ... }  # 本地 fallback 配置
    logger.warning(f"Nacos 配置获取失败，使用本地配置")
```

---

## 🔍 配置验证

运行以下命令验证配置：

```bash
cd D:\clawd\semantic_search
python -c "from utils.config import CONFIG; print(CONFIG.keys())"
```

---

*更新时间：2026-03-04*
