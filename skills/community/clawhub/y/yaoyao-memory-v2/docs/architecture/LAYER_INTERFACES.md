# yaoyao-memory - 层间接口规范

> **版本**: V1.0.0  
> **定义**: 记忆系统内部的标准接口与数据格式

---

## 接口总览

```
┌─────────┐   Memory_Input    ┌─────────┐   Memory_Output   ┌─────────┐
│  调用方  │ ───────────────► │   L2    │ ───────────────► │  上层   │
│ (Agent) │                   │ memory  │                   │(编排层) │
└─────────┘                   └─────────┘                   └─────────┘
```

---

## Memory_Input: 记忆输入

```json
{
  "schema": "Memory_Input_v1",
  "timestamp": "2026-04-10T10:35:00+08:00",
  "request": {
    "type": "search|retrieve|store|update|delete",
    "query": "用户查询文本",
    "limit": 5,
    "filters": {
      "type": ["info", "decision"],
      "importance": ["High", "Critical"],
      "date_from": "2026-04-01",
      "date_to": "2026-04-10"
    },
    "options": {
      "use_cache": true,
      "use_vector": true,
      "use_fts": true,
      "explain": false
    }
  },
  "context": {
    "session_id": "session_xxx",
    "user_id": "user_xxx",
    "channel": "feishu",
    "token_budget": 4000
  }
}
```

---

## Memory_Output: 记忆输出

```json
{
  "schema": "Memory_Output_v1",
  "timestamp": "2026-04-10T10:35:01+08:00",
  "status": "success|partial|error",
  "results": {
    "items": [
      {
        "id": "mem_xxx",
        "type": "info|decision|error|learning|preference",
        "importance": "Normal|High|Critical|Low",
        "title": "记忆标题",
        "content": "记忆内容摘要...",
        "source": "memory/2026-04-10.md",
        "relevance_score": 0.95,
        "updated_at": "2026-04-10T08:30:00+08:00"
      }
    ],
    "total_found": 42,
    "total_returned": 5,
    "search_method": "vector|fts|hybrid",
    "latency_ms": 12
  },
  "metadata": {
    "token_used": 1850,
    "cache_hit": true,
    "vector_db_status": "ok",
    "chroma_status": "ok"
  },
  "errors": []
}
```

---

## Cache_Entry: 缓存条目

```json
{
  "schema": "Cache_Entry_v1",
  "key": "hash_of_query",
  "ttl_seconds": 3600,
  "created_at": "2026-04-10T10:35:00+08:00",
  "expires_at": "2026-04-10T11:35:00+08:00",
  "data": {
    "results": [...],
    "token_used": 1200
  },
  "stats": {
    "hit_count": 5,
    "last_hit": "2026-04-10T10:40:00+08:00"
  }
}
```

---

## Governance_Input: 治理层输入

```json
{
  "schema": "Governance_Input_v1",
  "timestamp": "2026-04-10T10:35:01+08:00",
  "operation": "read|write|delete",
  "target": {
    "type": "memory|config|cache",
    "id": "mem_xxx"
  },
  "risk_level": "low|medium|high|critical",
  "audit": {
    "operator": "user_xxx",
    "session_id": "session_xxx",
    "ip": "xxx.xxx.xxx.xxx"
  }
}
```

---

## Governance_Output: 治理层输出

```json
{
  "schema": "Governance_Output_v1",
  "timestamp": "2026-04-10T10:35:02+08:00",
  "decision": "allow|deny|review|rollback",
  "reason": "决策原因",
  "actions_taken": ["audit_logged", "backup_created"],
  "warnings": [],
  "rollback_available": true
}
```

---

## Token_Budget: Token预算

```json
{
  "schema": "Token_Budget_v1",
  "total_budget": 4000,
  "allocated": {
    "identity_context": 500,
    "memory_retrieval": 2000,
    "search_results": 1000,
    "governance_overhead": 300,
    "reserved": 200
  },
  "used": {
    "current": 1850,
    "peak": 2100,
    "limit": 4000
  },
  "status": "ok|warning|critical"
}
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| V1.0.0 | 2026-04-10 | 初始接口定义 |
