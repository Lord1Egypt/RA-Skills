# ChromaDB 集成指南（可选方案）

> 为需要强大语义搜索能力的用户提供 ChromaDB 集成方案

**适用场景：** 记忆量 > 5000 条，需要精准语义搜索

---

## 一、为什么选择 ChromaDB？

### 优势

- ✅ **语义搜索强大**：向量相似度，比关键词匹配准确
- ✅ **本地部署**：无需外部服务，数据安全
- ✅ **开源免费**：Apache 2.0 许可证
- ✅ **社区活跃**：14.5k+ Star，持续更新

### 劣势

- ❌ **依赖重**：~150 MB 核心 + ~500 MB 模型
- ❌ **启动慢**：首次加载模型需要 3 秒
- ❌ **内存占用**：至少需要 512 MB 内存

### 适用场景

✅ 记忆量大（> 5000 条）  
✅ 需要精准语义搜索  
✅ 服务器部署（资源充足）  
✅ 多用户场景（并发查询）

---

## 二、安装 ChromaDB

### 2.1 基础安装

```bash
pip install chromadb
```

### 2.2 完整安装（含本地 Embedding）

```bash
pip install chromadb sentence-transformers
```

### 2.3 验证安装

```python
import chromadb
print(chromadb.__version__)
```

---

## 三、实施步骤

### 3.1 创建 ChromaMemoryBackend

在 `integrations/` 目录下创建 `chroma_memory.py`：

```python
"""
ChromaDB 记忆后端（可选）
需要安装：pip install chromadb
"""

import os
from typing import List, Dict
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


class ChromaMemoryBackend:
    """ChromaDB 记忆后端"""
    
    def __init__(self, storage_dir: str = "./data/chroma"):
        if not CHROMADB_AVAILABLE:
            raise ImportError("请先安装 chromadb: pip install chromadb")
        
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # 初始化 ChromaDB 客户端
        self.client = chromadb.PersistentClient(
            path=storage_dir,
            settings=Settings(
                anonymized_telemetry=False,  # 关闭遥测
                allow_reset=True
            )
        )
        
        # 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name="memory",
            metadata={"description": "User memory storage"}
        )
        
        print(f"✅ ChromaDB 初始化成功：{storage_dir}")
    
    def add(self, user_id: str, text: str, metadata: Dict = None):
        """添加记忆"""
        doc_id = f"{user_id}_{len(self.collection.get()['ids'])}"
        
        self.collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[{
                "user_id": user_id,
                **(metadata or {})
            }]
        )
    
    def search(self, user_id: str, query: str, limit: int = 5) -> List[str]:
        """语义搜索"""
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where={"user_id": user_id}
        )
        
        if results and results['documents']:
            return results['documents'][0]
        return []
    
    def get_all(self, user_id: str) -> str:
        """获取所有记忆"""
        results = self.collection.get(
            where={"user_id": user_id}
        )
        
        if results and results['documents']:
            return "\n\n".join(results['documents'])
        return ""
    
    def clear(self, user_id: str):
        """清空用户记忆"""
        results = self.collection.get(
            where={"user_id": user_id}
        )
        
        if results and results['ids']:
            self.collection.delete(ids=results['ids'])
```

### 3.2 修改 memory_manager.py

在 `integrations/memory_manager.py` 中添加 ChromaDB 支持：

```python
# 在文件开头添加
try:
    from chroma_memory import ChromaMemoryBackend
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

# 修改 MemoryManager.__init__
def __init__(self, storage_dir: str, ai_client=None, ai_model: str = None, 
             openclaw_workspace: str = None, use_chroma: bool = False):
    """
    storage_dir: 存储目录
    ai_client: AI 客户端（用于压缩摘要）
    ai_model: AI 模型名称
    openclaw_workspace: OpenClaw workspace 路径（可选）
    use_chroma: 是否使用 ChromaDB（可选）
    """
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

# 修改 load_memory 方法
def load_memory(self, user_id: str, query: str = None) -> str:
    """加载长期记忆（支持 ChromaDB）"""
    if self.use_chroma and query:
        # 使用 ChromaDB 语义搜索
        search_results = self.backend.search(user_id, query, limit=5)
        if search_results:
            return f"【语义搜索结果】\n" + "\n\n".join(search_results)
    
    # 降级到 OpenClaw 或本地文件
    if self.use_openclaw and query:
        search_result = _openclaw_memory_search(query, self.openclaw_workspace)
        if search_result:
            return f"【语义搜索结果】\n{search_result}\n\n【完整记忆】\n{self._load_memory_file(user_id)}"
    
    return self._load_memory_file(user_id)
```

### 3.3 修改 bot.py

在 `integrations/telegram/bot.py` 中启用 ChromaDB：

```python
# 创建消息处理器（可选启用 ChromaDB）
handlers = MessageHandlers(
    ai_adapter, 
    storage_dir="./data/memory",
    use_chroma=True  # 启用 ChromaDB
)
```

---

## 四、配置选项

### 4.1 环境变量

在 `.env` 文件中添加：

```bash
# ChromaDB 配置（可选）
USE_CHROMA=true
CHROMA_STORAGE_DIR=./data/chroma
```

### 4.2 代码配置

```python
# 方式1：直接启用
handlers = MessageHandlers(ai_adapter, use_chroma=True)

# 方式2：通过环境变量
import os
use_chroma = os.getenv("USE_CHROMA", "false").lower() == "true"
handlers = MessageHandlers(ai_adapter, use_chroma=use_chroma)
```

---

## 五、性能优化

### 5.1 选择 Embedding 模型

```python
# 默认模型（英文）
collection = client.get_or_create_collection(name="memory")

# 中文模型（推荐）
from chromadb.utils import embedding_functions
chinese_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="shibing624/text2vec-base-chinese"
)
collection = client.get_or_create_collection(
    name="memory",
    embedding_function=chinese_ef
)
```

### 5.2 批量插入

```python
# 批量添加记忆（更快）
self.collection.add(
    documents=[text1, text2, text3],
    ids=[id1, id2, id3],
    metadatas=[meta1, meta2, meta3]
)
```

### 5.3 定期清理

```python
# 清理旧记忆（保留最近 1000 条）
results = self.collection.get()
if len(results['ids']) > 1000:
    old_ids = results['ids'][:-1000]
    self.collection.delete(ids=old_ids)
```

---

## 六、测试验证

### 6.1 单元测试

```python
def test_chroma_memory():
    backend = ChromaMemoryBackend("./test_data")
    
    # 添加记忆
    backend.add("user1", "我喜欢吃苹果")
    backend.add("user1", "我喜欢打篮球")
    backend.add("user1", "我是 iOS 开发工程师")
    
    # 语义搜索
    results = backend.search("user1", "你喜欢什么水果？")
    assert "苹果" in results[0]
    
    results = backend.search("user1", "你的职业是什么？")
    assert "iOS" in results[0]
    
    print("✅ ChromaDB 测试通过")

if __name__ == "__main__":
    test_chroma_memory()
```

### 6.2 性能测试

```python
import time

backend = ChromaMemoryBackend()

# 插入 1000 条记忆
start = time.time()
for i in range(1000):
    backend.add("user1", f"记忆 {i}")
print(f"插入 1000 条耗时：{time.time() - start:.2f} 秒")

# 查询性能
start = time.time()
results = backend.search("user1", "记忆 500")
print(f"查询耗时：{(time.time() - start) * 1000:.2f} 毫秒")
```

---

## 七、故障排查

### 7.1 导入错误

```
ImportError: No module named 'chromadb'
```

**解决：** `pip install chromadb`

### 7.2 模型下载慢

```
Downloading model...
```

**解决：** 使用国内镜像

```bash
export HF_ENDPOINT=https://hf-mirror.com
pip install sentence-transformers
```

### 7.3 内存不足

```
MemoryError: Unable to allocate array
```

**解决：** 使用更小的模型或增加内存

```python
# 使用更小的模型
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"  # 更小的模型
)
```

---

## 八、迁移指南

### 8.1 从本地文件迁移到 ChromaDB

```python
def migrate_to_chroma():
    # 读取旧记忆
    with open("./data/memory/user1_memory.md", "r") as f:
        old_memory = f.read()
    
    # 分段（按段落）
    paragraphs = old_memory.split("\n\n")
    
    # 导入到 ChromaDB
    backend = ChromaMemoryBackend()
    for i, para in enumerate(paragraphs):
        if para.strip():
            backend.add("user1", para, {"source": "migration", "index": i})
    
    print(f"✅ 迁移完成：{len(paragraphs)} 条记忆")
```

### 8.2 从 ChromaDB 导出到文件

```python
def export_from_chroma():
    backend = ChromaMemoryBackend()
    all_memory = backend.get_all("user1")
    
    with open("./data/memory/user1_memory_export.md", "w") as f:
        f.write(all_memory)
    
    print("✅ 导出完成")
```

---

## 九、常见问题

### Q1: ChromaDB 和 OpenClaw memory_search 有什么区别？

A: 
- **ChromaDB**：独立向量数据库，功能更强大，但依赖重
- **OpenClaw**：OpenClaw 内置工具，轻量，但需要安装 OpenClaw

### Q2: 可以同时使用 ChromaDB 和 OpenClaw 吗？

A: 可以，优先级：ChromaDB > OpenClaw > 本地文件

### Q3: ChromaDB 数据存储在哪里？

A: `./data/chroma/` 目录（可配置）

### Q4: 如何备份 ChromaDB 数据？

A: 直接复制 `./data/chroma/` 目录

---

## 十、参考资源

- **ChromaDB 官网**：https://www.trychroma.com/
- **GitHub**：https://github.com/chroma-core/chroma
- **文档**：https://docs.trychroma.com/
- **中文模型**：https://huggingface.co/shibing624/text2vec-base-chinese

---

**版本：** v1.0  
**更新日期：** 2026-03-29  
**作者：** 组长
