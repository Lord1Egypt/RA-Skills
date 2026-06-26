# 向量检索技术实现

## 一、方案概述

本文档设计义乌小商品AI智能贸易系统的向量检索完整技术方案，支持商品匹配、相似商品推荐、语义搜索等核心功能。

### 1.1 技术架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    向量检索技术架构                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│   │  商品数据源   │───→│ 数据处理管道  │───→│ 向量生成服务 │   │
│   │义乌购/1688等 │    │ ETL + 清洗    │    │ 多模态Embedding│   │
│   └──────────────┘    └──────────────┘    └──────┬───────┘   │
│                                                    │             │
│                                                    ▼             │
│   ┌──────────────────────────────────────────────────────┐    │
│   │                    向量数据库                           │    │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐             │    │
│   │  │ Product │  │ Supplier│  │  Query  │             │    │
│   │  │  Index  │  │  Index  │  │  Index  │             │    │
│   │  └─────────┘  └─────────┘  └─────────┘             │    │
│   └──────────────────────────┬───────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│   ┌──────────────────────────────────────────────────────┐    │
│   │                  检索服务层                            │    │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │    │
│   │  │ 混合检索 │ │  重排服务 │ │  缓存层  │            │    │
│   │  └──────────┘ └──────────┘ └──────────┘            │    │
│   └──────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│   ┌──────────────────────────────────────────────────────┐    │
│   │                   Agent 集成层                        │    │
│   └──────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 核心指标目标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 向量检索延迟 | < 50ms | P99，百万级数据 |
| 召回率@10 | ≥ 95% | Top-10召回准确率 |
| 索引构建速度 | 10000条/秒 | 增量索引 |
| 支持数据规模 | 1000万向量 | 水平扩展 |
| 内存占用 | < 64GB | 100万向量 |

---

## 二、向量数据库选型

### 2.1 主流方案对比

| 维度 | Milvus 2.4 | Qdrant | Pinecone | Weaviate |
|------|-----------|--------|----------|----------|
| **开源** | ✅ | ✅ | ❌ | ✅ |
| **部署方式** | K8s/裸机 | Docker/K8s | 云托管 | K8s/Docker |
| **向量维度** | ≤32768 | ≤4096 | 无限制 | ≤65535 |
| **过滤支持** | 强 | 强 | 强 | 强 |
| **HNSW** | ✅ | ✅ | ✅ | ✅ |
| **GPU加速** | ✅ | ❌ | ✅ | ❌ |
| **多租户** | ✅ | ✅ | ✅ | ✅ |
| **社区活跃度** | 高 | 高 | 中 | 中 |
| **文档完善度** | 好 | 好 | 非常好 | 好 |
| **运维复杂度** | 中 | 低 | 无 | 中 |

### 2.2 推荐方案

**推荐选择：Qdrant + Milvus 混合架构**

```
┌─────────────────────────────────────────────────────────────────┐
│                    混合向量数据库架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    Qdrant (主库)                        │  │
│   │   用于: 商品向量检索、实时查询                            │  │
│   │   优势: 轻量、高性能、易运维                             │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              │ 定期同步                           │
│                              ▼                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    Milvus (备份/离线)                   │  │
│   │   用于: 离线分析、模型训练、全量备份                     │  │
│   │   优势: GPU加速、大规模数据处理                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 选型理由

1. **Qdrant 优先**：
   - 单节点部署简单，适合初期MVP
   - 性能优秀，召回率高
   - 过滤查询优化好
   - Rust实现，资源占用低

2. **Milvus 备选**：
   - 支持GPU加速批量处理
   - 适合离线训练场景
   - 企业级特性完善

---

## 三、商品向量生成方案

### 3.1 多模态向量策略

```python
# multimodal_embedding.py
from dataclasses import dataclass
from typing import Optional, List
import asyncio

@dataclass
class EmbeddingConfig:
    """Embedding配置"""
    # 文本向量
    text_model: str = "text-embedding-3-small"
    text_dimension: int = 1536
    
    # 图片向量
    image_model: str = "clip-vit-b/32"
    image_dimension: int = 512
    
    # 最终融合向量维度
    final_dimension: int = 1024

class MultimodalEmbedder:
    """多模态向量生成器"""
    
    def __init__(self, config: EmbeddingConfig, deepseek_client):
        self.config = config
        self.deepseek = deepseek_client
        self._text_cache = {}
        self._image_cache = {}
    
    async def embed_product(self, product: dict) -> List[float]:
        """生成商品向量"""
        
        # 1. 文本向量
        text_vector = await self._embed_text(product)
        
        # 2. 图片向量（如果有）
        image_vector = await self._embed_image(product.get("images", []))
        
        # 3. 融合向量
        fused_vector = self._fuse_vectors(text_vector, image_vector)
        
        return fused_vector
    
    async def _embed_text(self, product: dict) -> List[float]:
        """文本向量生成"""
        
        # 构建文本描述
        text_parts = [
            product.get("name", ""),
            product.get("description", ""),
            product.get("category", ""),
            f"价格: {product.get('price', '未知')}",
            f"MOQ: {product.get('moq', '未知')}",
            product.get("features", "")
        ]
        
        text = " | ".join(filter(None, text_parts))
        
        # 检查缓存
        cache_key = hash(text)
        if cache_key in self._text_cache:
            return self._text_cache[cache_key]
        
        # 调用DeepSeek API生成向量
        vector = await self._call_embedding_api(text)
        
        # 缓存
        self._text_cache[cache_key] = vector
        
        return vector
    
    async def _embed_image(self, images: List[str]) -> List[float]:
        """图片向量生成"""
        if not images:
            return [0.0] * self.config.image_dimension
        
        # 取第一张图片
        image_url = images[0]
        
        # 检查缓存
        if image_url in self._image_cache:
            return self._image_cache[image_url]
        
        # 调用图片Embedding API
        vector = await self._call_image_api(image_url)
        
        self._image_cache[image_url] = vector
        
        return vector
    
    def _fuse_vectors(
        self,
        text_vector: List[float],
        image_vector: List[float]
    ) -> List[float]:
        """融合向量 - 加权拼接"""
        
        # 文本权重0.7，图片权重0.3
        text_weight = 0.7
        image_weight = 0.3
        
        # 归一化
        text_norm = self._normalize(text_vector) * text_weight
        
        # 图片向量归一化并padding到相同维度
        image_norm = self._normalize(image_vector) * image_weight
        if len(image_norm) < len(text_norm):
            image_norm = list(image_norm) + [0.0] * (len(text_norm) - len(image_norm))
        
        # 加权求和
        fused = [t + i for t, i in zip(text_norm, image_norm)]
        
        # 最终归一化
        return self._normalize(fused)
    
    def _normalize(self, vector: List[float]) -> List[float]:
        """L2归一化"""
        import math
        
        norm = math.sqrt(sum(x*x for x in vector))
        if norm == 0:
            return vector
        
        return [x / norm for x in vector]
```

### 3.2 商品特征提取

```python
# product_feature_extractor.py
from typing import List, Dict, Any
import re

class ProductFeatureExtractor:
    """商品特征提取器"""
    
    # 商品属性正则
    PATTERNS = {
        "color": r"(红色|蓝色|绿色|黑色|白色|粉色|黄色|紫色|金色|银色|多色)",
        "material": r"(塑料|金属|木质|布料|玻璃|陶瓷|硅胶|不锈钢|铝合金)",
        "size": r"(\d+)(cm|mm|inch|寸|尺)",
        "weight": r"(\d+\.?\d*)(g|kg|斤|磅)",
        "age_range": r"(\d+)[-~](\d+)岁",
        "certification": r"(CE|FCC|ROHS|UL|CCC|ISO)"
    }
    
    def extract_features(self, product: dict) -> dict:
        """提取商品特征"""
        
        features = {
            "category_id": product.get("category_id"),
            "price_level": self._extract_price_level(product.get("price")),
            "moq_level": self._extract_moq_level(product.get("moq")),
            "attributes": self._extract_attributes(product),
            "keywords": self._extract_keywords(product),
            "hot_indicators": self._detect_hot_indicators(product)
        }
        
        return features
    
    def _extract_price_level(self, price: str) -> str:
        """提取价格区间"""
        try:
            p = float(re.sub(r"[^\d.]", "", str(price)))
            if p < 1:
                return "超低价"
            elif p < 5:
                return "低价"
            elif p < 20:
                return "中价"
            elif p < 50:
                return "中高"
            else:
                return "高价"
        except:
            return "未知"
    
    def _extract_moq_level(self, moq: Any) -> str:
        """提取MOQ级别"""
        try:
            m = int(moq)
            if m <= 10:
                return "小批量"
            elif m <= 100:
                return "中批量"
            elif m <= 1000:
                return "大批量"
            else:
                return "超大规模"
        except:
            return "未知"
    
    def _extract_attributes(self, product: dict) -> dict:
        """提取属性"""
        combined_text = f"{product.get('name', '')} {product.get('description', '')}"
        
        attrs = {}
        for attr_name, pattern in self.PATTERNS.items():
            match = re.search(pattern, combined_text)
            if match:
                attrs[attr_name] = match.group(0)
        
        return attrs
    
    def _extract_keywords(self, product: dict) -> List[str]:
        """提取关键词"""
        # 使用jieba分词
        import jieba
        
        text = f"{product.get('name', '')} {product.get('category', '')}"
        
        # 停用词
        stopwords = {"的", "了", "和", "是", "在", "有", "个", "我", "你", "他"}
        
        words = jieba.cut(text)
        keywords = [w for w in words if len(w) > 1 and w not in stopwords]
        
        return keywords[:10]
    
    def _detect_hot_indicators(self, product: dict) -> List[str]:
        """检测爆款指标"""
        indicators = []
        
        # 热销标签
        if product.get("hot_tag"):
            indicators.append("hot")
        
        # 新品标签
        if product.get("is_new"):
            indicators.append("new")
        
        # 促销标签
        if product.get("has_discount"):
            indicators.append("discount")
        
        # 好评率高
        if product.get("rating", 0) >= 4.5:
            indicators.append("high_rating")
        
        return indicators
```

---

## 四、索引策略

### 4.1 HNSW参数调优

```python
# hnsw_config.py
from dataclasses import dataclass

@dataclass
class HNSWConfig:
    """HNSW索引配置"""
    
    # 基础参数
    m: int = 16           # 每个节点的最大连接数
    ef_construction: int = 200  # 构建时动态列表大小
    
    # 查询参数
    ef_search: int = 100  # 查询时动态列表大小
    
    # 其他
    num_threads: int = -1  # -1表示使用CPU核数
    normalize: bool = True
    
    @classmethod
    def for_large_dataset(cls) -> 'HNSWConfig':
        """大规模数据集配置"""
        return cls(
            m=32,
            ef_construction=400,
            ef_search=200
        )
    
    @classmethod
    def for_small_dataset(cls) -> 'HNSWConfig':
        """小规模数据集配置"""
        return cls(
            m=16,
            ef_construction=100,
            ef_search=50
        )
    
    @classmethod
    def for_realtime(cls) -> 'HNSWConfig':
        """实时性优先配置"""
        return cls(
            m=12,
            ef_construction=100,
            ef_search=50
        )

# Qdrant HNSW配置
QDRANT_HNSW_CONFIG = {
    "m": 16,
    "ef_construct": 200,
    "full_scan_threshold": 10000,  # 小于1万条时用全表扫描
    "max_indexing_threads": 0,     # 0表示自动
    "on_disk": False,
    "payload_m": 16
}
```

### 4.2 索引创建

```python
# index_manager.py
import asyncio
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class VectorIndexManager:
    """向量索引管理器"""
    
    def __init__(self, client: QdrantClient):
        self.client = client
    
    async def create_product_index(self, collection_name: str = "products"):
        """创建商品索引"""
        
        # 检查是否已存在
        collections = self.client.get_collections().collections
        if collection_name in [c.name for c in collections]:
            return
        
        # 创建集合
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1024,  # 向量维度
                distance=Distance.COSINE  # 余弦距离
            ),
            hnsw_config=QDRANT_HNSW_CONFIG,
            optimizers_config={
                "default_segment_number": 2,
                "indexing_threshold": 20000
            }
        )
        
        # 创建payload索引（用于过滤）
        self.client.create_payload_index(
            collection_name=collection_name,
            field_name="category_id",
            field_schema="keyword"
        )
        
        self.client.create_payload_index(
            collection_name=collection_name,
            field_name="price_level",
            field_schema="keyword"
        )
        
        self.client.create_payload_index(
            collection_name=collection_name,
            field_name="has_stock",
            field_schema="bool"
        )
    
    async def insert_products(self, products: List[dict]):
        """批量插入商品"""
        
        points = []
        for i, product in enumerate(products):
            point = PointStruct(
                id=product["id"],
                vector=product["embedding"],
                payload={
                    "product_id": product["id"],
                    "name": product["name"],
                    "category_id": product["category_id"],
                    "price": product["price"],
                    "price_level": product.get("price_level", "未知"),
                    "moq": product.get("moq", 1),
                    "supplier_id": product.get("supplier_id"),
                    "has_stock": product.get("has_stock", True),
                    "rating": product.get("rating", 0),
                    "hot_indicators": product.get("hot_indicators", [])
                }
            )
            points.append(point)
        
        # 批量上传
        self.client.upsert(
            collection_name="products",
            points=points
        )
    
    async def delete_product(self, product_id: str):
        """删除商品"""
        self.client.delete(
            collection_name="products",
            points_selector=[product_id]
        )
    
    async def update_product(self, product_id: str, updates: dict):
        """更新商品信息"""
        self.client.set_payload(
            collection_name="products",
            payload=updates,
            points=[product_id]
        )
```

### 4.3 查询服务

```python
# search_service.py
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class SearchRequest:
    """搜索请求"""
    query_vector: Optional[List[float]] = None
    query_text: Optional[str] = None
    filters: Dict[str, Any] = None
    limit: int = 10
    offset: int = 0
    with_payload: bool = True
    with_vectors: bool = False

@dataclass
class SearchResult:
    """搜索结果"""
    id: str
    score: float
    payload: dict

class VectorSearchService:
    """向量搜索服务"""
    
    def __init__(
        self,
        index_manager: VectorIndexManager,
        embedder: MultimodalEmbedder,
        cache_client = None
    ):
        self.index_manager = index_manager
        self.embedder = embedder
        self.cache = cache_client
    
    async def search(
        self,
        request: SearchRequest
    ) -> List[SearchResult]:
        """混合搜索"""
        
        # 1. 如果有文本查询，生成向量
        if request.query_text:
            if self.cache:
                cache_key = f"query:{hash(request.query_text)}"
                cached = await self.cache.get(cache_key)
                if cached:
                    query_vector = cached
                else:
                    query_vector = await self.embedder._embed_text(
                        {"name": request.query_text, "description": request.query_text}
                    )
                    await self.cache.setex(cache_key, 3600, query_vector)
            else:
                query_vector = await self.embedder._embed_text(
                    {"name": request.query_text, "description": request.query_text}
                )
        else:
            query_vector = request.query_vector
        
        # 2. 构建过滤条件
        filter_condition = self._build_filter(request.filters)
        
        # 3. 执行搜索
        results = self.index_manager.client.search(
            collection_name="products",
            query_vector=query_vector,
            query_filter=filter_condition,
            limit=request.limit,
            offset=request.offset,
            with_payload=request.with_payload,
            with_vectors=request.with_vectors
        )
        
        # 4. 格式化结果
        return [
            SearchResult(
                id=r.id,
                score=r.score,
                payload=r.payload
            )
            for r in results
        ]
    
    async def search_with_rerank(
        self,
        request: SearchRequest,
        rerank_model = None
    ) -> List[SearchResult]:
        """带重排的搜索"""
        
        # 1. 初步召回
        initial_results = await self.search(request)
        
        if len(initial_results) < request.limit:
            return initial_results
        
        # 2. 准备重排数据
        if rerank_model:
            # 调用重排模型
            reranked = await rerank_model.rerank(
                query=request.query_text,
                documents=initial_results
            )
            return reranked
        
        return initial_results
    
    def _build_filter(self, filters: Dict[str, Any]) -> dict:
        """构建过滤条件"""
        if not filters:
            return None
        
        conditions = []
        
        if "category_id" in filters:
            conditions.append({
                "key": "category_id",
                "match": {"value": filters["category_id"]}
            })
        
        if "price_range" in filters:
            min_price, max_price = filters["price_range"]
            conditions.append({
                "key": "price",
                "range": {
                    "gte": min_price,
                    "lte": max_price
                }
            })
        
        if "has_stock" in filters:
            conditions.append({
                "key": "has_stock",
                "match": {"value": filters["has_stock"]}
            })
        
        if "hot_only" in filters and filters["hot_only"]:
            conditions.append({
                "key": "hot_indicators",
                "match_any": {"any": ["hot", "high_rating"]}
            })
        
        if len(conditions) == 1:
            return conditions[0]
        elif len(conditions) > 1:
            return {
                "must": conditions
            }
        
        return None
```

---

## 五、实时更新机制

### 5.1 数据同步架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    实时数据同步架构                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│   │  数据源      │───→│  CDC Change  │───→│   Kafka      │   │
│   │ MySQL/MongoDB│    │  DataStream  │    │   Topics     │   │
│   └──────────────┘    └──────────────┘    └──────┬───────┘   │
│                                                   │             │
│         ┌────────────────────────────────────────┘             │
│         │                                                       │
│         ▼                                                       │
│   ┌──────────────────────────────────────────────────────┐    │
│   │              Flink 实时处理                            │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │    │
│   │  │ Debezium │→ │ Transform│→ │ Vectorize │           │    │
│   │  │  解析    │  │ 数据转换 │  │ 向量化   │           │    │
│   │  └──────────┘  └──────────┘  └──────┬───┘           │    │
│   └─────────────────────────────────────┼───────────────┘    │
│                                        │                      │
│                                        ▼                      │
│   ┌──────────────────────────────────────────────────────┐    │
│   │              Qdrant 实时写入                          │    │
│   │  upsert / delete / update                            │    │
│   └──────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 增量索引实现

```python
# incremental_indexer.py
import asyncio
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class IndexEvent:
    """索引事件"""
    event_type: str  # insert, update, delete
    product_id: str
    data: Dict[str, Any]
    timestamp: datetime
    sequence: int

class IncrementalIndexer:
    """增量索引器"""
    
    def __init__(
        self,
        index_manager: VectorIndexManager,
        embedder: MultimodalEmbedder,
        kafka_consumer = None
    ):
        self.index_manager = index_manager
        self.embedder = embedder
        self.kafka = kafka_consumer
        self.redis = None  # 用于顺序保证
        self._running = False
    
    async def start(self):
        """启动增量索引"""
        self._running = True
        
        if self.kafka:
            asyncio.create_task(self._consume_from_kafka())
        else:
            asyncio.create_task(self._poll_database())
    
    async def stop(self):
        """停止增量索引"""
        self._running = False
    
    async def _consume_from_kafka(self):
        """从Kafka消费事件"""
        async for message in self.kafka:
            try:
                event = IndexEvent(**json.loads(message.value))
                await self._process_event(event)
            except Exception as e:
                # 记录错误，继续处理
                await self._handle_error(event, e)
    
    async def _poll_database(self):
        """轮询数据库变更"""
        last_sequence = 0
        
        while self._running:
            try:
                # 从数据库获取增量数据
                events = await self._fetch_incremental_events(last_sequence)
                
                for event in events:
                    await self._process_event(event)
                    last_sequence = event.sequence
                
                await asyncio.sleep(1)  # 避免过度轮询
                
            except Exception as e:
                await self._handle_error(None, e)
                await asyncio.sleep(5)
    
    async def _process_event(self, event: IndexEvent):
        """处理索引事件"""
        
        if event.event_type == "insert":
            await self._handle_insert(event)
        elif event.event_type == "update":
            await self._handle_update(event)
        elif event.event_type == "delete":
            await self._handle_delete(event)
    
    async def _handle_insert(self, event: IndexEvent):
        """处理新增"""
        # 生成向量
        product = event.data
        product["embedding"] = await self.embedder.embed_product(product)
        
        # 插入索引
        await self.index_manager.insert_products([product])
        
        # 记录成功
        await self._record_success(event)
    
    async def _handle_update(self, event: IndexEvent):
        """处理更新"""
        # 只更新payload，向量不变
        product = event.data
        
        updates = {
            "name": product.get("name"),
            "price": product.get("price"),
            "has_stock": product.get("has_stock", True),
            "rating": product.get("rating"),
            "hot_indicators": product.get("hot_indicators", [])
        }
        
        # 移除None值
        updates = {k: v for k, v in updates.items() if v is not None}
        
        await self.index_manager.update_product(event.product_id, updates)
        await self._record_success(event)
    
    async def _handle_delete(self, event: IndexEvent):
        """处理删除"""
        await self.index_manager.delete_product(event.product_id)
        await self._record_success(event)
    
    async def _record_success(self, event: IndexEvent):
        """记录成功处理"""
        # 可以记录到Redis用于监控
        pass
    
    async def _handle_error(self, event: IndexEvent, error: Exception):
        """错误处理"""
        # 记录错误日志
        # 发送告警
        # 重试或放入死信队列
        pass
    
    async def _fetch_incremental_events(
        self,
        last_sequence: int
    ) -> List[IndexEvent]:
        """获取增量事件（伪代码）"""
        # 实现数据库轮询逻辑
        pass
```

### 5.3 批量重建索引

```python
# index_rebuilder.py
import asyncio
from datetime import datetime

class IndexRebuilder:
    """索引重建器"""
    
    def __init__(
        self,
        index_manager: VectorIndexManager,
        embedder: MultimodalEmbedder,
        source_db
    ):
        self.index_manager = index_manager
        self.embedder = embedder
        self.source_db = source_db
    
    async def rebuild_full_index(
        self,
        batch_size: int = 1000,
        collection_name: str = "products"
    ):
        """全量重建索引"""
        
        print(f"开始全量重建索引: {datetime.now()}")
        
        # 1. 创建临时集合
        temp_collection = f"{collection_name}_temp_{int(time.time())}"
        await self.index_manager.create_product_index(temp_collection)
        
        # 2. 分批处理
        total_count = 0
        batch_num = 0
        
        async for batch in self._fetch_all_products(batch_size):
            batch_num += 1
            
            # 向量化
            embedded_batch = []
            for product in batch:
                try:
                    product["embedding"] = await self.embedder.embed_product(product)
                    embedded_batch.append(product)
                except Exception as e:
                    print(f"向量化失败: {product['id']}, {e}")
            
            # 插入临时集合
            await self._insert_to_collection(temp_collection, embedded_batch)
            
            total_count += len(embedded_batch)
            print(f"已完成: {total_count} 条")
            
            # 批次间暂停，避免压力过大
            await asyncio.sleep(0.1)
        
        # 3. 原子切换
        await self._atomic_swap(collection_name, temp_collection)
        
        print(f"全量重建完成: {total_count} 条, 耗时: {elapsed}s")
    
    async def _fetch_all_products(self, batch_size: int):
        """分批获取所有商品"""
        offset = 0
        
        while True:
            batch = await self.source_db.fetch_products(
                limit=batch_size,
                offset=offset
            )
            
            if not batch:
                break
            
            yield batch
            offset += batch_size
    
    async def _atomic_swap(
        self,
        old_collection: str,
        new_collection: str
    ):
        """原子切换集合"""
        # 删除旧集合
        self.index_manager.client.delete_collection(old_collection)
        
        # 重命名新集合
        self.index_manager.client.recreate_collection(
            old_collection,
            from_snapshot=new_collection
        )
```

---

## 六、成本估算

### 6.1 基础设施成本

| 资源 | 配置 | 月费用(¥) | 说明 |
|------|------|----------|------|
| Qdrant服务器 | 8核16G | 800 | 单节点 |
| 嵌入模型API | DeepSeek | 500 | 约500万Token/月 |
| Redis缓存 | 2GB | 60 | 查询缓存 |
| 对象存储 | 100GB | 30 | 图片存储 |
| **合计** | | **1,390** | |

### 6.2 性能与成本平衡

| 策略 | 性能影响 | 成本节省 |
|------|---------|---------|
| 查询缓存命中率>70% | 延迟-30% | 50% API费用 |
| 增量更新替代全量 | 实时性+ | 80% 计算资源 |
| 按需向量化 | 无 | 60% API费用 |
