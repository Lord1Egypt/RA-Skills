# DeepSeek V4-Flash API 集成方案

## 一、方案概述

本文档设计义乌小商品AI智能贸易系统的DeepSeek V4-Flash集成方案，追赶OKKI的AI能力，目标实现商品匹配、报价生成、客服对话等核心AI功能。

### 1.1 技术架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     DeepSeek API 集成架构                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│   │  Agent SDK  │───→│ Router      │───→│ Cache Layer │        │
│   │  (Python)   │    │ 智能路由     │    │ Redis缓存   │        │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘        │
│          │                  │                   │               │
│          ▼                  ▼                   ▼               │
│   ┌──────────────────────────────────────────────────────┐     │
│   │              DeepSeek API Gateway                     │     │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐              │     │
│   │  │Streaming │ │  Batch   │ │  Retry   │              │     │
│   │  │ Handler  │ │ Handler  │ │ Handler  │              │     │
│   │  └──────────┘ └──────────┘ └──────────┘              │     │
│   └──────────────────────────┬───────────────────────────┘     │
│                              │                                  │
│                              ▼                                  │
│   ┌──────────────────────────────────────────────────────┐     │
│   │           DeepSeek V4-Flash API                       │     │
│   │  https://api.deepseek.com/v1/chat/completions        │     │
│   └──────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 核心性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 流式响应首Token延迟 | < 500ms | P95 |
| 完整响应时间 | < 3s | P95 |
| API可用性 | ≥ 99.5% | 月度统计 |
| Token成本 | < ¥0.01/千Token | 优化后 |

---

## 二、API调用最佳实践

### 2.1 客户端封装

```python
# deepseek_client.py
import asyncio
import hashlib
import json
from typing import AsyncIterator, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class APIMode(Enum):
    STREAMING = "streaming"    # 流式响应
    BATCH = "batch"            # 批量处理
    SYNC = "sync"              # 同步调用

@dataclass
class DeepSeekConfig:
    api_key: str
    base_url: str = "https://api.deepseek.com/v1"
    model: str = "deepseek-chat"
    max_tokens: int = 2048
    temperature: float = 0.7
    timeout: int = 30
    max_retries: int = 3

class DeepSeekClient:
    """DeepSeek API 封装客户端"""
    
    def __init__(self, config: DeepSeekConfig, cache_client=None):
        self.config = config
        self.cache = cache_client  # Redis客户端
        self._session = None
    
    async def chat(
        self,
        messages: list[dict],
        mode: APIMode = APIMode.SYNC,
        **kwargs
    ) -> str | AsyncIterator[str]:
        """统一聊天接口"""
        
        # 1. 检查缓存
        cache_key = self._generate_cache_key(messages)
        if cached := await self._get_cached(cache_key):
            return cached
        
        # 2. 路由选择
        if mode == APIMode.STREAMING:
            return await self._stream_chat(messages, cache_key, **kwargs)
        elif mode == APIMode.BATCH:
            return await self._batch_chat(messages, **kwargs)
        else:
            return await self._sync_chat(messages, cache_key, **kwargs)
    
    async def _sync_chat(
        self,
        messages: list[dict],
        cache_key: str,
        **kwargs
    ) -> str:
        """同步调用"""
        import httpx
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            **kwargs
        }
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await self._request_with_retry(
                client, "POST", 
                f"{self.config.base_url}/chat/completions",
                json=payload
            )
            
            result = response.json()["choices"][0]["message"]["content"]
            
            # 缓存结果
            await self._cache_result(cache_key, result)
            
            return result
    
    async def _stream_chat(
        self,
        messages: list[dict],
        cache_key: str,
        **kwargs
    ) -> AsyncIterator[str]:
        """流式调用"""
        import httpx
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "temperature": kwargs.get("temperature", self.config.temperature),
            "stream": True,
            **kwargs
        }
        
        full_content = []
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            async with client.stream(
                "POST",
                f"{self.config.base_url}/chat/completions",
                json=payload
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        if data.get("choices"):
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                full_content.append(content)
                                yield content
        
        # 缓存完整结果
        await self._cache_result(cache_key, "".join(full_content))
    
    async def _batch_chat(
        self,
        messages_list: list[list[dict]],
        **kwargs
    ) -> list[str]:
        """批量调用 - 使用Promise池并发"""
        
        tasks = [
            self._sync_chat(messages, None, **kwargs)
            for messages in messages_list
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _request_with_retry(
        self,
        client,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        """带重试的请求"""
        import httpx
        
        for attempt in range(self.config.max_retries):
            try:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
                if attempt == self.config.max_retries - 1:
                    raise
                # 指数退避
                await asyncio.sleep(2 ** attempt)
        
        raise Exception("Max retries exceeded")
    
    def _generate_cache_key(self, messages: list[dict]) -> str:
        """生成缓存键"""
        content = json.dumps(messages, sort_keys=True)
        return f"deepseek:cache:{hashlib.md5(content.encode()).hexdigest()}"
    
    async def _get_cached(self, key: str) -> Optional[str]:
        if not self.cache:
            return None
        return await self.cache.get(key)
    
    async def _cache_result(self, key: str, result: str, ttl: int = 3600):
        if self.cache and key:
            await self.cache.setex(key, ttl, result)
```

### 2.2 流式响应处理

```python
# streaming_handler.py
import asyncio
import json
from typing import AsyncIterator

class StreamingResponseHandler:
    """流式响应处理器"""
    
    def __init__(self):
        self.buffer_size = 10  # 缓冲Token数
    
    async def process_stream(
        self,
        stream: AsyncIterator[str],
        on_token: callable = None
    ) -> str:
        """
        处理流式响应
        - 实时yield token
        - 累积完整内容
        - 可选回调
        """
        full_content = []
        
        async for token in stream:
            # 实时回调
            if on_token:
                await on_token(token)
            
            full_content.append(token)
            yield token
        
        return "".join(full_content)
    
    def format_sse(self, content: str, event: str = "message") -> str:
        """格式化SSE响应"""
        return f"event: {event}\ndata: {json.dumps({'content': content})}\n\n"
```

### 2.3 批量处理策略

```python
# batch_processor.py
import asyncio
from typing import List, Callable, Awaitable
from dataclasses import dataclass
import time

@dataclass
class BatchJob:
    job_id: str
    messages: List[dict]
    callback: Callable = None
    priority: int = 0

class BatchProcessor:
    """批量任务处理器"""
    
    def __init__(self, client, max_concurrent: int = 10, batch_size: int = 50):
        self.client = client
        self.max_concurrent = max_concurrent
        self.batch_size = batch_size
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.results = {}
        self._running = False
    
    async def start(self):
        """启动批量处理器"""
        self._running = True
        asyncio.create_task(self._process_loop())
    
    async def submit(self, job: BatchJob):
        """提交批量任务"""
        await self.queue.put((job.priority, time.time(), job))
    
    async def _process_loop(self):
        """处理循环"""
        while self._running:
            batch = []
            
            # 收集批量任务
            while len(batch) < self.batch_size and not self.queue.empty():
                try:
                    _, _, job = await asyncio.wait_for(
                        self.queue.get(), 
                        timeout=1.0
                    )
                    batch.append(job)
                except asyncio.TimeoutError:
                    break
            
            if batch:
                await self._execute_batch(batch)
    
    async def _execute_batch(self, jobs: List[BatchJob]):
        """执行批量任务"""
        tasks = [
            self.client.chat(job.messages, mode=APIMode.SYNC)
            for job in jobs
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for job, result in zip(jobs, results):
            self.results[job.job_id] = result
            if job.callback:
                await job.callback(result)
```

---

## 三、Prompt模板设计

### 3.1 商品匹配Prompt

```python
# prompts/product_matching.py

PRODUCT_MATCHING_SYSTEM = """你是一位专业的义乌小商品贸易专家。

## 你的角色
你是"商品猎手"，帮助采购商快速找到最具性价比的商品和最可靠的供应商。

## 专业背景
- 精通义乌小商品分类体系（文胸类、箱包类、玩具类、钟表类等20大类）
- 熟悉各类商品的MOQ、价格区间、质检标准
- 了解跨境贸易术语和物流方案

## 输出要求
必须以JSON格式输出，包含以下字段：
- matched_products: 匹配的商品列表
- match_reasons: 匹配原因说明
- supplier_notes: 供应商注意事项
- price_estimates: 价格估算
- confidence: 匹配置信度(0-1)

## 注意事项
1. 价格信息24小时内有效，需标注
2. 不确定信息需标注置信度
3. 优先推荐有出口经验的供应商"""

PRODUCT_MATCHING_USER_TEMPLATE = """
## 采购需求
商品描述: {query}
采购数量: {quantity} {unit}
目标价格: {price_range}
产地偏好: {location_preference}

## 可选筛选条件
{optional_filters}

## 历史采购记录（用于个性化）
{user_history}

请根据以上需求，匹配最合适的商品和供应商。
"""

def generate_product_matching_prompt(
    query: str,
    quantity: int = None,
    unit: str = "件",
    price_range: str = None,
    location_preference: str = None,
    optional_filters: dict = None,
    user_history: list = None
) -> tuple[str, list[dict]]:
    """生成商品匹配Prompt"""
    
    system = PRODUCT_MATCHING_SYSTEM
    
    user = PRODUCT_MATCHING_USER_TEMPLATE.format(
        query=query,
        quantity=quantity or "未指定",
        unit=unit,
        price_range=price_range or "面议",
        location_preference=location_preference or "无",
        optional_filters=_format_filters(optional_filters),
        user_history=_format_history(user_history)
    )
    
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]
    
    return system, messages

def _format_filters(filters: dict) -> str:
    if not filters:
        return "无"
    
    lines = []
    for key, value in filters.items():
        lines.append(f"- {key}: {value}")
    return "\n".join(lines)

def _format_history(history: list) -> str:
    if not history:
        return "无历史采购记录"
    
    items = [f"- {h['product']} (采购于{h['date']})" for h in history[-5:]]
    return "\n".join(items)
```

### 3.2 报价生成Prompt

```python
# prompts/quote_generation.py

QUOTE_GENERATION_SYSTEM = """你是一位专业的义乌外贸报价专员。

## 你的职责
根据商品信息和客户需求，生成专业、准确的多语言报价单。

## 报价单标准格式
```
报价单号: QUOTE-{date}-{sequence}
有效期: {validity_period}
币种: {currency}

商品明细:
| SKU | 商品名 | 规格 | 单价 | 数量 | 小计 |
|-----|-------|------|------|------|------|

价格条款: {price_term} (FOB/CIF/EXW等)
付款方式: {payment_terms}
交货周期: {lead_time}
包装方式: {packing}

备注: {notes}
```

## 定价规则
1. 阶梯报价: 数量越多，单价越低
2. 包含项: 商品价格、基础包装、国内运费
3. 不含项: 国际运费、海关税费、保险费

## 语言支持
- 中文
- 英文
- 西班牙语
- 阿拉伯语"""

QUOTE_GENERATION_USER_TEMPLATE = """
## 客户信息
客户名称: {customer_name}
国家/地区: {country}
采购语言: {language}
客户等级: {customer_tier} (VIP/普通/新客户)

## 商品信息
商品列表:
{product_list}

## 交易条件
目标价格: {target_price}
目标数量: {target_quantity}
价格条款: {price_term}
付款方式: {payment_terms}
交货期限: {delivery_date}

## 历史报价（如有）
{historical_quotes}

请生成专业报价单，包含FOB/CIF双价格选项。
"""

def generate_quote_prompt(
    customer_name: str,
    country: str,
    products: list[dict],
    language: str = "zh",
    customer_tier: str = "普通",
    **kwargs
) -> tuple[str, list[dict]]:
    """生成报价Prompt"""
    
    system = QUOTE_GENERATION_SYSTEM
    
    product_lines = []
    for i, p in enumerate(products, 1):
        product_lines.append(
            f"{i}. {p['name']} | SKU: {p.get('sku', 'N/A')} | "
            f"MOQ: {p.get('moq', 1)} | 单价区间: {p.get('price_range', '询价')}"
        )
    
    user = QUOTE_GENERATION_USER_TEMPLATE.format(
        customer_name=customer_name,
        country=country,
        language=language,
        customer_tier=customer_tier,
        product_list="\n".join(product_lines),
        target_price=kwargs.get("target_price", "待定"),
        target_quantity=kwargs.get("target_quantity", "待定"),
        price_term=kwargs.get("price_term", "FOB Ningbo"),
        payment_terms=kwargs.get("payment_terms", "T/T 30% deposit"),
        delivery_date=kwargs.get("delivery_date", "待确认"),
        historical_quotes=kwargs.get("historical_quotes", "新客户首单")
    )
    
    return system, [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]
```

### 3.3 客服对话Prompt

```python
# prompts/customer_service.py

CUSTOMER_SERVICE_SYSTEM = """你是一位专业的义乌外贸客服专员。

## 你的角色
你是"问题解决专家"，通过智能识别客户意图、快速响应FAQ和妥善处理投诉，维护客户满意度。

## 专业背景
- 精通义乌小商品出口流程和常见问题
- 熟悉跨境电商平台卖家的痛点
- 掌握多语言客服沟通技巧
- 了解客户情绪管理和投诉处理技巧

## 意图分类
1. 售前咨询 - 产品信息、价格、MOQ
2. 订单查询 - 物流、发货状态
3. 售后服务 - 退换货、质量问题
4. 技术支持 - 使用指导、参数说明
5. 投诉建议 - 反馈意见
6. 闲聊 - 非业务问题
7. 转接人工 - 需要专人处理
8. 未知意图 - 需要澄清

## 回复策略
- 情绪激动客户: 先安抚，共情表达
- 投诉客户: 承认问题，提出解决方案
- 咨询客户: 专业解答，适度推荐
- 模糊意图: 多选项引导澄清

## 行为准则
1. 同理心优先：理解客户情绪
2. 快速响应：30秒内首次响应
3. 精准解答：提供准确信息
4. 透明沟通：如需等待，说明原因
5. 闭环管理：每个问题跟踪到底

## 输出格式
必须以JSON格式输出：
{
  "intent": "意图类型",
  "confidence": 0.95,
  "response": "回复内容",
  "action_required": "reply/escalate/transfer",
  "emotion": "neutral/angry/satisfied/anxious",
  "follow_up": ["跟进事项"]
}"""

def generate_service_prompt(
    message: str,
    conversation_history: list = None,
    customer_info: dict = None,
    current_product: str = None
) -> list[dict]:
    """生成客服对话Prompt"""
    
    system = CUSTOMER_SERVICE_SYSTEM
    
    # 构建上下文
    history_context = ""
    if conversation_history:
        history_lines = []
        for h in conversation_history[-5:]:
            role = "客户" if h["role"] == "user" else "客服"
            history_lines.append(f"{role}: {h['content'][:100]}")
        history_context = "## 对话历史\n" + "\n".join(history_lines) + "\n\n"
    
    customer_context = ""
    if customer_info:
        customer_context = f"""## 客户信息
客户ID: {customer_info.get('id', 'N/A')}
客户等级: {customer_info.get('tier', '普通')}
历史订单: {customer_info.get('order_count', 0)}单
客诉记录: {customer_info.get('complaint_count', 0)}次
"""
    
    product_context = ""
    if current_product:
        product_context = f"## 当前咨询商品\n{current_product}\n\n"
    
    user = f"""{history_context}{customer_context}{product_context}## 当前消息
{message}

请分析客户意图并生成回复。"""

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]
```

---

## 四、成本优化策略

### 4.1 缓存策略

```python
# cache_strategy.py

class CacheStrategy:
    """缓存策略"""
    
    # 缓存TTL配置（秒）
    TTL_CONFIG = {
        "product_matching": 1800,      # 30分钟
        "quote_generation": 3600,      # 1小时
        "customer_service": 600,       # 10分钟
        "intent_classification": 300,  # 5分钟
    }
    
    # 缓存键前缀
    PREFIX_CONFIG = {
        "product_matching": "pm:",
        "quote_generation": "qt:",
        "customer_service": "cs:",
        "intent_classification": "ic:",
    }
    
    @classmethod
    def get_cache_key(cls, task_type: str, **params) -> str:
        """生成缓存键"""
        import hashlib
        import json
        
        prefix = cls.PREFIX_CONFIG.get(task_type, "default:")
        content = json.dumps(params, sort_keys=True, ensure_ascii=False)
        hash_val = hashlib.md5(content.encode()).hexdigest()[:12]
        
        return f"{prefix}{hash_val}"
    
    @classmethod
    def get_ttl(cls, task_type: str) -> int:
        """获取TTL"""
        return cls.TTL_CONFIG.get(task_type, 600)
```

### 4.2 降级策略

```python
# degradation_strategy.py
from enum import Enum
from typing import Optional
import asyncio

class DegradationLevel(Enum):
    FULL = "full"           # 完全正常
    REDUCED = "reduced"     # 降级模式
    FALLBACK = "fallback"   # 兜底方案
    OFFLINE = "offline"     # 离线模式

class DegradationManager:
    """降级管理器"""
    
    def __init__(self):
        self.current_level = DegradationLevel.FULL
        self.error_count = 0
        self.error_threshold = 10
        self.window_size = 60  # 60秒窗口
    
    async def check_and_degrade(self, error: Exception) -> DegradationLevel:
        """检查是否需要降级"""
        self.error_count += 1
        
        if self.error_count >= self.error_threshold:
            self.current_level = DegradationLevel.REDUCED
            await self._trigger_degradation()
        
        return self.current_level
    
    def get_fallback_response(self, task_type: str, **params) -> dict:
        """获取兜底响应"""
        
        fallbacks = {
            "product_matching": {
                "matched_products": [],
                "message": "当前搜索繁忙，请稍后重试或使用关键词搜索",
                "hot_products": self._get_hot_products()
            },
            "quote_generation": {
                "quote": None,
                "message": "报价生成中，请稍后查看或联系客服",
                "estimated_price_range": "待确认"
            },
            "customer_service": {
                "response": "抱歉，当前服务繁忙，请稍后重试或留言",
                "queue_position": "未知",
                "wait_time": "约5-10分钟"
            }
        }
        
        return fallbacks.get(task_type, {"message": "服务暂时不可用"})
    
    def _get_hot_products(self) -> list:
        """获取热门商品兜底"""
        return [
            {"id": "hot_001", "name": "义乌爆款指尖陀螺", "price": "¥2.5"},
            {"id": "hot_002", "name": "网红同款解压玩具", "price": "¥3.8"},
            {"id": "hot_003", "name": "亚马逊爆款钥匙扣", "price": "¥1.5"}
        ]
    
    async def _trigger_degradation(self):
        """触发降级"""
        # 发送告警
        # 记录日志
        # 切换降级策略
        pass
```

### 4.3 智能路由

```python
# smart_router.py
from dataclasses import dataclass
from typing import Literal

@dataclass
class RouteConfig:
    """路由配置"""
    task_type: str
    model: str
    max_tokens: int
    temperature: float
    cache_enabled: bool
    fallback_models: list[str]

class SmartRouter:
    """智能路由 - 根据任务类型选择最优模型"""
    
    ROUTE_TABLE = {
        "product_matching": RouteConfig(
            task_type="product_matching",
            model="deepseek-chat",
            max_tokens=2048,
            temperature=0.3,  # 低温度保证准确性
            cache_enabled=True,
            fallback_models=["deepseek-coder"]
        ),
        "quote_generation": RouteConfig(
            task_type="quote_generation",
            model="deepseek-chat",
            max_tokens=1536,
            temperature=0.2,  # 低温度保证格式准确
            cache_enabled=True,
            fallback_models=[]
        ),
        "customer_service": RouteConfig(
            task_type="customer_service",
            model="deepseek-chat",
            max_tokens=1024,
            temperature=0.7,  # 适中温度保证自然
            cache_enabled=True,
            fallback_models=[]
        ),
        "content_generation": RouteConfig(
            task_type="content_generation",
            model="deepseek-chat",
            max_tokens=2048,
            temperature=0.8,  # 高温度保证多样性
            cache_enabled=False,
            fallback_models=[]
        )
    }
    
    @classmethod
    def get_route(cls, task_type: str) -> RouteConfig:
        """获取路由配置"""
        return cls.ROUTE_TABLE.get(task_type, cls.ROUTE_TABLE["customer_service"])
    
    @classmethod
    async def route_and_execute(
        cls,
        task_type: str,
        messages: list[dict],
        client
    ) -> str:
        """路由并执行"""
        route = cls.get_route(task_type)
        
        try:
            result = await client.chat(
                messages,
                mode=APIMode.SYNC if route.cache_enabled else APIMode.STREAMING,
                max_tokens=route.max_tokens,
                temperature=route.temperature
            )
            return result
        except Exception as e:
            if route.fallback_models:
                for fallback in route.fallback_models:
                    try:
                        result = await client.chat(
                            messages,
                            model=fallback,
                            max_tokens=route.max_tokens,
                            temperature=route.temperature
                        )
                        return result
                    except:
                        continue
            
            raise
```

---

## 五、与Agent技能集成

### 5.1 集成架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent技能集成架构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐                                             │
│   │ Agent SKILL │ ← Skill定义（YAML + Markdown）                │
│   └──────┬──────┘                                             │
│          │                                                    │
│          ▼                                                    │
│   ┌─────────────┐    ┌─────────────┐                         │
│   │ Skill Loader│───→│ Skill Router│                         │
│   │  技能加载器  │    │  技能路由    │                         │
│   └──────┬──────┘    └──────┬──────┘                         │
│          │                  │                                  │
│          ▼                  ▼                                  │
│   ┌─────────────────────────────────────────────────────┐    │
│   │              DeepSeek Integration Layer              │    │
│   │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │    │
│   │  │ Prompt  │ │ Cache   │ │ Retry   │ │ Monitor │    │    │
│   │  │ Manager │ │ Manager │ │ Manager │ │ Manager │    │    │
│   │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │    │
│   └─────────────────────────────────────────────────────┘    │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────┐    │
│   │                 DeepSeek API                         │    │
│   └─────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Skill集成示例

```python
# skill_integration.py

class SkillDeepSeekBridge:
    """Skill与DeepSeek桥接器"""
    
    def __init__(self, deepseek_client: DeepSeekClient):
        self.client = deepseek_client
        self.prompt_generators = {
            "product_matching": generate_product_matching_prompt,
            "quote_generation": generate_quote_prompt,
            "customer_service": generate_service_prompt,
        }
    
    async def execute_skill(
        self,
        skill_name: str,
        context: dict
    ) -> dict:
        """执行Skill并返回结果"""
        
        # 1. 加载Skill定义
        skill_def = self._load_skill(skill_name)
        
        # 2. 生成Prompt
        prompt_gen = self.prompt_generators.get(skill_name)
        if not prompt_gen:
            raise ValueError(f"Unknown skill: {skill_name}")
        
        _, messages = prompt_gen(**context)
        
        # 3. 调用DeepSeek
        response = await self.client.chat(messages)
        
        # 4. 解析响应
        result = self._parse_skill_response(skill_name, response)
        
        # 5. 后处理
        result = self._post_process(skill_name, result, skill_def)
        
        return result
    
    def _load_skill(self, skill_name: str) -> dict:
        """加载Skill定义"""
        # 从文件系统或数据库加载SKILL.md
        return {
            "name": skill_name,
            "output_format": "json",
            "required_fields": []
        }
    
    def _parse_skill_response(self, skill_name: str, response: str) -> dict:
        """解析Skill响应"""
        import json
        import re
        
        # 提取JSON
        json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        return {"raw_response": response}
    
    def _post_process(self, skill_name: str, result: dict, skill_def: dict) -> dict:
        """后处理"""
        result["skill"] = skill_name
        result["success"] = True
        return result
```

---

## 六、监控与告警

### 6.1 监控指标

```python
# monitoring.py

@dataclass
class APIMetrics:
    """API监控指标"""
    
    # 延迟指标
    first_token_latency_ms: float = 0
    full_response_latency_ms: float = 0
    
    # 流量指标
    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    
    # 质量指标
    error_count: int = 0
    retry_count: int = 0
    timeout_count: int = 0
    
    # 成本指标
    total_tokens: int = 0
    total_cost: float = 0

class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self.metrics = defaultdict(APIMetrics)
        self.start_time = time.time()
    
    def record_request(
        self,
        task_type: str,
        latency_ms: float,
        tokens: int,
        cached: bool = False,
        error: bool = False
    ):
        """记录请求"""
        m = self.metrics[task_type]
        m.total_requests += 1
        m.full_response_latency_ms = max(m.full_response_latency_ms, latency_ms)
        m.total_tokens += tokens
        m.total_cost += tokens * 0.0001  # DeepSeek费率
        
        if cached:
            m.cache_hits += 1
        else:
            m.cache_misses += 1
        
        if error:
            m.error_count += 1
    
    def get_summary(self) -> dict:
        """获取指标摘要"""
        total = APIMetrics()
        for m in self.metrics.values():
            total.total_requests += m.total_requests
            total.cache_hits += m.cache_hits
            total.error_count += m.error_count
            total.total_tokens += m.total_tokens
            total.total_cost += m.total_cost
        
        return {
            "total_requests": total.total_requests,
            "cache_hit_rate": total.cache_hits / max(total.total_requests, 1),
            "error_rate": total.error_count / max(total.total_requests, 1),
            "total_tokens": total.total_tokens,
            "estimated_cost": total.total_cost,
            "uptime_seconds": time.time() - self.start_time
        }
```

---

## 七、成本估算

### 7.1 月度成本测算

| 成本项 | 配置 | 单价 | 用量 | 月费用(¥) |
|-------|-----|------|------|----------|
| DeepSeek API | V4-Flash | ¥0.001/千Token | 500万Token | 5,000 |
| Redis缓存 | 2GB | ¥0.5/GB/天 | 60天 | 60 |
| 监控日志 | ELK | ¥500/月 | 1套 | 500 |
| **合计** | | | | **5,560** |

### 7.2 优化后成本

| 优化策略 | 预期节省 | 说明 |
|---------|---------|------|
| 缓存命中率>60% | 40% | 重复查询缓存 |
| 批量处理 | 20% | 合并请求 |
| 模型降级 | 15% | 简单任务用小模型 |
| **总计节省** | **~50%** | |

**优化后月成本**：约 ¥2,780
