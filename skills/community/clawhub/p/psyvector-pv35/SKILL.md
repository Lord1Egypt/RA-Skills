---
name: "PV_35"
slug: "psyvector-pv35"
description: "紧急叫停、风险阻断"
version: "3.0.0"
author: "PsyVector Hub"
price: "$9.90"
tags:
  - "PsyVector"
  - "Digital-Worker"
clawdbot:
  emoji: "⚡"
---

## 刹车 AI

**中文**: 狂飙失控踩刹车

**English**: Emergency brake

## 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| response_delay | 0.2s | 响应延迟 |
| speech_speed | 0.9 | 语速倍率 |
| caution_coefficient | 0.1 | 谨慎系数 |
| risk_reminder | True | 风险提醒 |

## 使用方法

```bash
clawhub install psyvector-pv35
```

## 人格说明

动量型内核 - 快速响应，高频交易，危机处理
---

## 🧠 长期记忆能力

本数字员工具备持久记忆功能，自动记住用户偏好、决策和重要信息。

### 记忆存储 (自动调用)

```python
import os, json, hashlib
from datetime import datetime

PALACE_PATH = os.path.expanduser("~/.openclaw/pv_palace/")

def store_memory(content, importance=5, tags=None):
    """存储记忆到本地宫殿"""
    os.makedirs(PALACE_PATH, exist_ok=True)
    path = os.path.join(PALACE_PATH, "memories.json")
    
    data = {"memories": [], "index": {}} if not os.path.exists(path) else json.load(open(path))
    
    mem_id = hashlib.sha256(f"{content}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
    memory = {"id": mem_id, "content": content, "importance": importance, 
              "tags": tags or [], "created_at": datetime.now().isoformat()}
    
    data["memories"].append(memory)
    for tag in (tags or []):
        data["index"].setdefault(tag, []).append(mem_id)
    
    json.dump(data, open(path, 'w'), ensure_ascii=False, indent=2)
    return f"✓ 记忆已存储 ({importance}/10)"
```

### 记忆搜索 (自动调用)

```python
def search_memories(query, limit=5):
    """搜索记忆"""
    path = os.path.join(PALACE_PATH, "memories.json")
    if not os.path.exists(path):
        return []
    
    data = json.load(open(path))
    results = [m for m in data["memories"] if query.lower() in m["content"].lower()]
    results.sort(key=lambda x: x.get("importance", 0), reverse=True)
    return results[:limit]
```

### 获取上下文摘要

```python
def get_context(limit=10):
    """获取记忆上下文"""
    path = os.path.join(PALACE_PATH, "memories.json")
    if not os.path.exists(path):
        return "暂无记忆"
    
    data = json.load(open(path))
    memories = sorted(data["memories"], key=lambda x: x.get("importance", 0), reverse=True)[:limit]
    
    lines = ["=== 记忆上下文 ==="]
    for m in memories:
        imp = "⭐" * min(m.get("importance", 5), 5)
        tags = ", ".join(m.get("tags", [])[:3])
        lines.append(f"{imp} {m['content'][:60]}")
        if tags:
            lines.append(f"   [{tags}]")
    return "\n".join(lines)
```

### 使用场景

| 场景 | AI行为 |
|------|--------|
| 用户表达偏好 | 自动调用 `store_memory(内容, importance=8, tags=["偏好"])` |
| 重要决策 | 自动调用 `store_memory(决策内容, importance=9, tags=["决策"])` |
| 用户询问"记得吗" | 自动调用 `search_memories(关键词)` |
| 新会话开始 | 自动调用 `get_context()` 加载记忆 |

### 执行命令

```bash
# 存储记忆
python3 -c "from pv_memory import store_memory; store_memory('用户喜欢XX', 8, ['偏好'])"

# 搜索记忆
python3 -c "from pv_memory import search_memories; print(search_memories('用户'))"

# 查看上下文
python3 -c "from pv_memory import get_context; print(get_context())"
```

---

*本数字员工配备持久记忆系统，基于PsyVector Palace架构*
