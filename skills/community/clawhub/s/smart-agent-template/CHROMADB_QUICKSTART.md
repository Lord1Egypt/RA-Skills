# ChromaDB 快速实施指南

> 5 分钟快速启用 ChromaDB 语义搜索

---

## 步骤 1：安装 ChromaDB

```bash
pip install chromadb
```

---

## 步骤 2：下载实施代码

将以下代码保存为 `integrations/chroma_memory.py`：

```python
"""ChromaDB 记忆后端"""
import os
from typing import List, Dict
import chromadb
from chromadb.config import Settings

class ChromaMemoryBackend:
    def __init__(self, storage_dir: str = "./data/chroma"):
        os.makedirs(storage_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=storage_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(name="memory")
    
    def add(self, user_id: str, text: str, metadata: Dict = None):
        doc_id = f"{user_id}_{len(self.collection.get()['ids'])}"
        self.collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[{"user_id": user_id, **(metadata or {})}]
        )
    
    def search(self, user_id: str, query: str, limit: int = 5) -> List[str]:
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where={"user_id": user_id}
        )
        return results['documents'][0] if results['documents'] else []
    
    def get_all(self, user_id: str) -> str:
        results = self.collection.get(where={"user_id": user_id})
        return "\n\n".join(results['documents']) if results['documents'] else ""
```

---

## 步骤 3：修改 memory_manager.py

在 `integrations/memory_manager.py` 开头添加：

```python
# 检测 ChromaDB
try:
    from chroma_memory import ChromaMemoryBackend
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
```

修改 `__init__` 方法：

```python
def __init__(self, storage_dir: str, ai_client=None, ai_model: str = None, 
             openclaw_workspace: str = None, use_chroma: bool = False):
    self.storage_dir = storage_dir
    self.ai_client = ai_client
    self.ai_model = ai_model
    self.openclaw_workspace = openclaw_workspace
    
    # 优先级：ChromaDB > OpenClaw > 本地文件
    if use_chroma and CHROMA_AVAILABLE:
        self.backend = ChromaMemoryBackend(storage_dir + "/chroma")
        self.use_chroma = True
        print("✅ 使用 ChromaDB 语义搜索")
    elif _detect_openclaw():
        self.use_openclaw = True
        self.use_chroma = False
        print("✅ 使用 OpenClaw memory_search")
    else:
        self.use_openclaw = False
        self.use_chroma = False
        print("📁 使用本地文件 + AI 压缩")
    
    os.makedirs(storage_dir, exist_ok=True)
```

修改 `load_memory` 方法：

```python
def load_memory(self, user_id: str, query: str = None) -> str:
    # ChromaDB 语义搜索
    if self.use_chroma and query:
        results = self.backend.search(user_id, query, limit=5)
        if results:
            return "【语义搜索结果】\n" + "\n\n".join(results)
    
    # OpenClaw 语义搜索
    if self.use_openclaw and query:
        result = _openclaw_memory_search(query, self.openclaw_workspace)
        if result:
            return f"【语义搜索结果】\n{result}\n\n【完整记忆】\n{self._load_memory_file(user_id)}"
    
    # 本地文件
    return self._load_memory_file(user_id)
```

---

## 步骤 4：启用 ChromaDB

在 `integrations/telegram/bot.py` 中：

```python
# 创建消息处理器（启用 ChromaDB）
handlers = MessageHandlers(
    ai_adapter, 
    storage_dir="./data/memory",
    use_chroma=True  # 启用 ChromaDB
)
```

---

## 步骤 5：测试

```bash
cd integrations/telegram
python bot.py
```

**启动日志：**
```
✅ 使用 ChromaDB 语义搜索
✅ ChromaDB 初始化成功：./data/memory/chroma
```

---

## 验证

发送消息测试：

1. "我叫张三，我是 iOS 开发"
2. "我擅长 Swift 和 Objective-C"
3. "你知道我擅长什么编程语言吗？"

Bot 应该通过语义搜索找到相关记忆。

---

## 回滚

如果不想用 ChromaDB，只需：

```python
handlers = MessageHandlers(
    ai_adapter, 
    storage_dir="./data/memory",
    use_chroma=False  # 禁用 ChromaDB
)
```

---

## 完整代码

完整实施代码见：`CHROMADB_INTEGRATION.md`

---

**预计耗时：** 5 分钟  
**难度：** ⭐⭐☆☆☆
