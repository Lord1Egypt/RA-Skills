# Agent协作协议设计

## 一、协议概述

本文档定义义乌小商品AI智能贸易系统中多Agent之间的通信协议，确保信息流转不丢失、协作高效可靠。

### 1.1 协作架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      Agent协作协议架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────────────────────────────────────────────┐     │
│   │              Orchestrator (协调器)                     │     │
│   │   任务分发 → 状态跟踪 → 结果聚合 → 异常处理            │     │
│   └──────────────────────┬───────────────────────────────┘     │
│                          │                                       │
│         ┌────────────────┼────────────────┐                    │
│         │                │                │                    │
│         ▼                ▼                ▼                    │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│   │ Product  │    │   Sales  │    │  Service │              │
│   │  Agent   │◄──►│  Agent   │◄──►│  Agent   │              │
│   │  商品代理 │    │  销售代理 │    │  客服代理 │              │
│   └──────────┘    └──────────┘    └──────────┘              │
│          │                │                │                    │
│          └────────────────┼────────────────┘                    │
│                           │                                      │
│                           ▼                                      │
│   ┌──────────────────────────────────────────────────────┐     │
│   │              Hermes Memory (三层记忆)                   │     │
│   └──────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 协议设计原则

| 原则 | 说明 |
|------|------|
| **松耦合** | Agent通过消息通信，不直接依赖 |
| **可追踪** | 每个消息有唯一ID，全链路可追溯 |
| **幂等性** | 重复消息不影响最终结果 |
| **超时控制** | 消息处理有明确超时时间 |
| **错误隔离** | 单个Agent失败不影响全局 |

---

## 二、消息格式标准

### 2.1 JSON Schema定义

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AgentMessage",
  "description": "Agent间通信消息格式",
  "type": "object",
  "required": ["message_id", "timestamp", "sender", "receiver", "action", "payload"],
  "properties": {
    "message_id": {
      "type": "string",
      "pattern": "^[a-zA-Z0-9_-]{8,32}$",
      "description": "全局唯一消息ID，格式: {type}_{timestamp}_{uuid}"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "消息创建时间，ISO8601格式"
    },
    "correlation_id": {
      "type": "string",
      "description": "关联ID，用于追踪请求-响应关系"
    },
    "sender": {
      "type": "object",
      "required": ["agent_id", "agent_type"],
      "properties": {
        "agent_id": {"type": "string"},
        "agent_type": {"type": "string", "enum": ["orchestrator", "product", "sales", "service", "supplier"]},
        "skill_name": {"type": "string"},
        "instance_id": {"type": "string"}
      }
    },
    "receiver": {
      "type": "object",
      "required": ["agent_id", "agent_type"],
      "properties": {
        "agent_id": {"type": "string"},
        "agent_type": {"type": "string"},
        "skill_name": {"type": "string"}
      }
    },
    "action": {
      "type": "string",
      "enum": [
        "request",      // 请求执行
        "response",     // 响应结果
        "event",        // 事件通知
        "callback",     // 回调通知
        "error",        // 错误通知
        "timeout",      // 超时通知
        "cancel"        // 取消请求
      ]
    },
    "mode": {
      "type": "string",
      "enum": ["sync", "async", "callback"],
      "default": "sync",
      "description": "通信模式"
    },
    "priority": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5,
      "default": 3,
      "description": "优先级 1=最高 5=最低"
    },
    "payload": {
      "type": "object",
      "description": "消息内容",
      "properties": {
        "task": {"type": "string", "description": "任务类型"},
        "data": {"type": "object", "description": "业务数据"},
        "context": {"type": "object", "description": "上下文信息"},
        "options": {"type": "object", "description": "执行选项"},
        "metadata": {"type": "object", "description": "元数据"}
      },
      "required": ["task"]
    },
    "timeout": {
      "type": "integer",
      "minimum": 1000,
      "maximum": 300000,
      "default": 30000,
      "description": "超时时间(毫秒)"
    },
    "retry": {
      "type": "object",
      "properties": {
        "enabled": {"type": "boolean"},
        "max_attempts": {"type": "integer", "default": 3},
        "backoff": {"type": "string", "enum": ["linear", "exponential"], "default": "exponential"}
      }
    },
    "trace": {
      "type": "object",
      "properties": {
        "trace_id": {"type": "string"},
        "span_id": {"type": "string"},
        "parent_span_id": {"type": "string"}
      }
    }
  }
}
```

### 2.2 消息类型示例

#### 2.2.1 请求消息

```json
{
  "message_id": "req_1705123456789_a1b2c3d4",
  "timestamp": "2024-01-13T10:30:56.789Z",
  "correlation_id": "conv_1705123456000_001",
  "sender": {
    "agent_id": "orchestrator_001",
    "agent_type": "orchestrator",
    "instance_id": "orchestrator-v1"
  },
  "receiver": {
    "agent_id": "product_agent_001",
    "agent_type": "product",
    "skill_name": "product-matching"
  },
  "action": "request",
  "mode": "sync",
  "priority": 2,
  "payload": {
    "task": "product_matching",
    "data": {
      "query": "指尖陀螺 儿童玩具",
      "filters": {
        "category": "玩具类",
        "price_range": "1-5元",
        "moq": 100
      }
    },
    "context": {
      "user_id": "user_12345",
      "session_id": "sess_abc123",
      "language": "zh-CN"
    },
    "options": {
      "limit": 10,
      "include_supplier": true
    }
  },
  "timeout": 30000,
  "retry": {
    "enabled": true,
    "max_attempts": 3,
    "backoff": "exponential"
  },
  "trace": {
    "trace_id": "trace_xyz789",
    "span_id": "span_001",
    "parent_span_id": null
  }
}
```

#### 2.2.2 响应消息

```json
{
  "message_id": "resp_1705123456790_e5f6g7h8",
  "timestamp": "2024-01-13T10:30:57.890Z",
  "correlation_id": "req_1705123456789_a1b2c3d4",
  "sender": {
    "agent_id": "product_agent_001",
    "agent_type": "product"
  },
  "receiver": {
    "agent_id": "orchestrator_001",
    "agent_type": "orchestrator"
  },
  "action": "response",
  "mode": "sync",
  "payload": {
    "success": true,
    "task": "product_matching",
    "data": {
      "matched_products": [
        {
          "id": "prod_001",
          "name": "义乌指尖陀螺 三叶款",
          "price": "2.5",
          "moq": 100,
          "supplier": {
            "id": "sup_001",
            "name": "义乌玩具工厂"
          }
        }
      ],
      "total_count": 15,
      "search_time_ms": 120
    },
    "metadata": {
      "confidence": 0.85,
      "cache_hit": false
    }
  }
}
```

#### 2.2.3 错误消息

```json
{
  "message_id": "err_1705123456791_i9j0k1l2",
  "timestamp": "2024-01-13T10:30:58.001Z",
  "correlation_id": "req_1705123456789_a1b2c3d4",
  "sender": {
    "agent_id": "product_agent_001",
    "agent_type": "product"
  },
  "receiver": {
    "agent_id": "orchestrator_001",
    "agent_type": "orchestrator"
  },
  "action": "error",
  "payload": {
    "error": {
      "code": "PRODUCT_NOT_FOUND",
      "message": "未找到匹配的商品",
      "details": {
        "query": "不存在的商品XYZ",
        "suggestions": ["尝试模糊搜索", "浏览热门商品"]
      }
    },
    "retryable": true
  }
}
```

---

## 三、Agent间调用协议

### 3.1 调用模式

```python
# agent_protocol.py
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Any, Callable
import asyncio

class CallMode(Enum):
    SYNC = "sync"       # 同步调用，等待结果
    ASYNC = "async"     # 异步调用，不等待结果
    CALLBACK = "callback" # 回调模式，结果通过回调返回

@dataclass
class AgentRequest:
    """Agent请求"""
    message_id: str
    sender: str
    receiver: str
    skill_name: str
    payload: dict
    mode: CallMode = CallMode.SYNC
    priority: int = 3
    timeout_ms: int = 30000
    correlation_id: Optional[str] = None
    
@dataclass 
class AgentResponse:
    """Agent响应"""
    message_id: str
    correlation_id: str
    success: bool
    data: Optional[dict] = None
    error: Optional[dict] = None
    metadata: dict = field(default_factory=dict)

class AgentProtocol:
    """Agent通信协议"""
    
    def __init__(self, message_queue, memory_client):
        self.queue = message_queue
        self.memory = memory_client
        self.handlers = {}
        self.pending_requests = {}
    
    def register_handler(self, skill_name: str, handler: Callable):
        """注册技能处理器"""
        self.handlers[skill_name] = handler
    
    async def send_request(self, request: AgentRequest) -> AgentResponse:
        """发送请求并等待响应"""
        
        # 1. 构建消息
        message = self._build_message(request)
        
        # 2. 存储到记忆系统
        await self._store_message(message)
        
        # 3. 根据模式处理
        if request.mode == CallMode.SYNC:
            return await self._sync_call(request, message)
        elif request.mode == CallMode.ASYNC:
            asyncio.create_task(self._async_call(request, message))
            return AgentResponse(
                message_id=message["message_id"],
                correlation_id=request.message_id,
                success=True,
                metadata={"status": "queued"}
            )
        elif request.mode == CallMode.CALLBACK:
            return await self._callback_call(request, message)
    
    async def _sync_call(
        self, 
        request: AgentRequest, 
        message: dict
    ) -> AgentResponse:
        """同步调用"""
        
        try:
            # 发送到消息队列
            await self.queue.publish(
                f"agent.{request.receiver}",
                message
            )
            
            # 等待响应
            response = await asyncio.wait_for(
                self._wait_for_response(request.message_id),
                timeout=request.timeout_ms / 1000
            )
            
            return response
            
        except asyncio.TimeoutError:
            return AgentResponse(
                message_id=self._generate_id("err"),
                correlation_id=request.message_id,
                success=False,
                error={
                    "code": "TIMEOUT",
                    "message": f"请求超时 ({request.timeout_ms}ms)"
                }
            )
    
    async def _async_call(
        self, 
        request: AgentRequest, 
        message: dict
    ):
        """异步调用"""
        try:
            await self.queue.publish(
                f"agent.{request.receiver}",
                message
            )
        except Exception as e:
            await self._notify_error(request, str(e))
    
    async def _callback_call(
        self, 
        request: AgentRequest, 
        message: dict
    ) -> AgentResponse:
        """回调模式"""
        
        # 添加回调地址
        message["callback"] = {
            "queue": f"callback.{request.sender}",
            "correlation_id": request.message_id
        }
        
        await self.queue.publish(
            f"agent.{request.receiver}",
            message
        )
        
        return AgentResponse(
            message_id=message["message_id"],
            correlation_id=request.message_id,
            success=True,
            metadata={"status": "waiting_callback"}
        )
    
    async def _wait_for_response(self, correlation_id: str) -> AgentResponse:
        """等待响应"""
        future = asyncio.Future()
        self.pending_requests[correlation_id] = future
        
        try:
            return await future
        finally:
            self.pending_requests.pop(correlation_id, None)
    
    def _build_message(self, request: AgentRequest) -> dict:
        """构建消息"""
        import time
        import uuid
        
        return {
            "message_id": f"msg_{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.utcnow().isoformat(),
            "correlation_id": request.message_id,
            "sender": {"agent_id": request.sender},
            "receiver": {"agent_id": request.receiver, "skill_name": request.skill_name},
            "action": "request",
            "mode": request.mode.value,
            "priority": request.priority,
            "payload": request.payload,
            "timeout": request.timeout_ms
        }
    
    async def _store_message(self, message: dict):
        """存储消息到记忆系统"""
        await self.memory.append(
            "conversation_history",
            message
        )
    
    async def handle_response(self, response: AgentResponse):
        """处理响应消息"""
        future = self.pending_requests.get(response.correlation_id)
        if future and not future.done():
            future.set_result(response)
```

### 3.2 消息队列配置

```python
# mq_config.py

class MessageQueueConfig:
    """消息队列配置"""
    
    # 队列定义
    QUEUES = {
        "orchestrator": {
            "durable": True,
            "max_length": 10000,
            "message_ttl": 300000  # 5分钟
        },
        "agent.product": {
            "durable": True,
            "max_length": 5000,
            "message_ttl": 60000,  # 1分钟
            "prefetch_count": 10
        },
        "agent.sales": {
            "durable": True,
            "max_length": 5000,
            "message_ttl": 120000,  # 2分钟
            "prefetch_count": 5
        },
        "agent.service": {
            "durable": True,
            "max_length": 10000,
            "message_ttl": 30000,  # 30秒
            "prefetch_count": 20
        },
        "callback.*": {
            "durable": True,
            "max_length": 5000,
            "message_ttl": 60000
        }
    }
    
    # 交换机定义
    EXCHANGES = {
        "agent.direct": {
            "type": "direct",
            "bindings": ["agent.product", "agent.sales", "agent.service"]
        },
        "agent.topic": {
            "type": "topic",
            "bindings": ["agent.#", "callback.#"]
        },
        "agent.fanout": {
            "type": "fanout",
            "bindings": ["orchestrator"]
        }
    }
    
    # 死信队列
    DEAD_LETTER = {
        "exchange": "dlx",
        "queue": "dlq.agent",
        "routing_key": "dead_letter"
    }
```

---

## 四、状态机设计

### 4.1 任务生命周期状态机

```
┌─────────────────────────────────────────────────────────────────┐
│                      任务生命周期状态机                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐                                                 │
│   │ CREATED  │                                                 │
│   │   创建   │                                                 │
│   └────┬─────┘                                                 │
│        │                                                       │
│        ▼                                                       │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐              │
│   │ PENDING  │────►│ RUNNING  │────►│COMPLETED│              │
│   │   等待   │     │   执行   │     │   完成   │              │
│   └──────────┘     └────┬─────┘     └──────────┘              │
│        │                │                     ▲                 │
│        │                │ timeout             │                 │
│        │                ▼                     │                 │
│        │           ┌──────────┐                │                 │
│        │           │WAITING_  │                │                 │
│        │           │CALLBACK  │───────┐        │                 │
│        │           │  等待回调 │       │        │                 │
│        │           └──────────┘       │        │                 │
│        │                              │        │                 │
│        ▼                              │        │                 │
│   ┌──────────┐     ┌──────────┐       │        │                 │
│   │ CANCELLED│◄────│ CANCEL_ │◄──────┘        │                 │
│   │  已取消  │     │ PENDING │                │                 │
│   └──────────┘     └──────────┘                │                 │
│                                                │                 │
│   ┌──────────┐     ┌──────────┐                │                 │
│   │  FAILED  │◄────│ ERROR    │────────────────┘                 │
│   │   失败   │     │   错误   │    (重试耗尽或不可重试)            │
│   └──────────┘     └──────────┘                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 状态机实现

```python
# task_state_machine.py
from enum import Enum
from typing import Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

class TaskState(Enum):
    CREATED = "created"
    PENDING = "pending"
    RUNNING = "running"
    WAITING_CALLBACK = "waiting_callback"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    CANCEL_PENDING = "cancel_pending"

class TaskEvent(Enum):
    START = "start"
    PROGRESS = "progress"
    COMPLETE = "complete"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCEL = "cancel"
    RETRY = "retry"
    CALLBACK_RECEIVED = "callback_received"

@dataclass
class TaskContext:
    """任务上下文"""
    task_id: str
    state: TaskState = TaskState.CREATED
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    result: Optional[dict] = None
    error: Optional[dict] = None
    retry_count: int = 0
    progress: float = 0.0
    metadata: dict = field(default_factory=dict)

class TaskStateMachine:
    """任务状态机"""
    
    # 状态转换规则
    TRANSITIONS = {
        TaskState.CREATED: [TaskState.PENDING, TaskState.CANCELLED],
        TaskState.PENDING: [TaskState.RUNNING, TaskState.CANCEL_PENDING],
        TaskState.RUNNING: [
            TaskState.WAITING_CALLBACK,
            TaskState.COMPLETED,
            TaskState.FAILED,
            TaskState.CANCEL_PENDING
        ],
        TaskState.WAITING_CALLBACK: [
            TaskState.COMPLETED,
            TaskState.FAILED,
            TaskState.CANCEL_PENDING
        ],
        TaskState.COMPLETED: [],
        TaskState.FAILED: [TaskState.PENDING],  # 可重试
        TaskState.CANCELLED: [],
        TaskState.CANCEL_PENDING: [TaskState.CANCELLED, TaskState.RUNNING],
    }
    
    def __init__(self, task_context: TaskContext):
        self.context = task_context
        self.listeners: list[Callable] = []
        self._lock = asyncio.Lock()
    
    def can_transition(self, target_state: TaskState) -> bool:
        """检查是否可以转换"""
        current = self.context.state
        return target_state in self.TRANSITIONS.get(current, [])
    
    async def transition(
        self, 
        target_state: TaskState, 
        event: TaskEvent,
        data: dict = None
    ) -> bool:
        """执行状态转换"""
        async with self._lock:
            if not self.can_transition(target_state):
                return False
            
            old_state = self.context.state
            self.context.state = target_state
            self.context.updated_at = datetime.utcnow()
            
            if data:
                self.context.metadata.update(data)
            
            # 触发监听器
            for listener in self.listeners:
                await listener(old_state, target_state, event, self.context)
            
            return True
    
    def add_listener(self, listener: Callable):
        """添加状态变化监听器"""
        self.listeners.append(listener)
    
    async def start(self) -> bool:
        """开始任务"""
        return await self.transition(TaskState.PENDING, TaskEvent.START)
    
    async def run(self) -> bool:
        """运行任务"""
        return await self.transition(TaskState.RUNNING, TaskEvent.START)
    
    async def complete(self, result: dict) -> bool:
        """完成任务"""
        self.context.result = result
        return await self.transition(TaskState.COMPLETED, TaskEvent.COMPLETE)
    
    async def fail(self, error: dict, retryable: bool = True) -> bool:
        """任务失败"""
        self.context.error = error
        if retryable and self.context.retry_count < 3:
            self.context.retry_count += 1
            return await self.transition(TaskState.PENDING, TaskEvent.RETRY, {"retry": True})
        return await self.transition(TaskState.FAILED, TaskEvent.ERROR)
    
    async def cancel(self) -> bool:
        """取消任务"""
        if self.context.state == TaskState.RUNNING:
            success = await self.transition(TaskState.CANCEL_PENDING, TaskEvent.CANCEL)
        else:
            success = await self.transition(TaskState.CANCELLED, TaskEvent.CANCEL)
        return success
    
    async def wait_callback(self) -> bool:
        """等待回调"""
        return await self.transition(
            TaskState.WAITING_CALLBACK, 
            TaskEvent.PROGRESS,
            {"progress": 0.9}
        )
    
    async def receive_callback(self, data: dict) -> bool:
        """接收回调"""
        self.context.result = data
        return await self.transition(TaskState.COMPLETED, TaskEvent.CALLBACK_RECEIVED)
```

### 4.3 任务管理器

```python
# task_manager.py

class TaskManager:
    """任务管理器"""
    
    def __init__(self, state_machine_factory, memory_client):
        self.state_machines: dict[str, TaskStateMachine] = {}
        self.factory = state_machine_factory
        self.memory = memory_client
    
    async def create_task(
        self,
        task_id: str,
        initial_state: TaskState = TaskState.CREATED
    ) -> TaskContext:
        """创建任务"""
        context = TaskContext(
            task_id=task_id,
            state=initial_state
        )
        
        sm = self.factory(context)
        sm.add_listener(self._on_state_change)
        
        self.state_machines[task_id] = sm
        await self._persist_context(context)
        
        return context
    
    async def get_task(self, task_id: str) -> Optional[TaskContext]:
        """获取任务"""
        sm = self.state_machines.get(task_id)
        if sm:
            return sm.context
        
        # 从持久化存储加载
        return await self._load_context(task_id)
    
    async def _on_state_change(
        self,
        old_state: TaskState,
        new_state: TaskState,
        event: TaskEvent,
        context: TaskContext
    ):
        """状态变化回调"""
        # 记录到记忆系统
        await self.memory.append("task_history", {
            "task_id": context.task_id,
            "old_state": old_state.value,
            "new_state": new_state.value,
            "event": event.value,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # 触发后续处理
        if new_state == TaskState.FAILED:
            await self._handle_failure(context)
        elif new_state == TaskState.COMPLETED:
            await self._handle_completion(context)
    
    async def _persist_context(self, context: TaskContext):
        """持久化上下文"""
        await self.memory.set(
            f"task:{context.task_id}",
            asdict(context)
        )
    
    async def _load_context(self, task_id: str) -> Optional[TaskContext]:
        """加载上下文"""
        data = await self.memory.get(f"task:{task_id}")
        if data:
            return TaskContext(**data)
        return None
```

---

## 五、错误处理与重试机制

### 5.1 错误分类

```python
# error_types.py
from enum import Enum

class ErrorCode(Enum):
    # 系统级错误
    SYSTEM_ERROR = ("E1000", True, "系统内部错误")
    SERVICE_UNAVAILABLE = ("E1001", True, "服务不可用")
    TIMEOUT = ("E1002", True, "请求超时")
    
    # Agent级错误
    AGENT_NOT_FOUND = ("E2001", False, "Agent不存在")
    AGENT_BUSY = ("E2002", True, "Agent忙")
    SKILL_NOT_FOUND = ("E2003", False, "技能不存在")
    
    # 业务级错误
    PRODUCT_NOT_FOUND = ("E3001", False, "商品未找到")
    QUOTE_EXPIRED = ("E3002", False, "报价已过期")
    CUSTOMER_NOT_FOUND = ("E3003", False, "客户不存在")
    INSUFFICIENT_STOCK = ("E3004", False, "库存不足")
    
    # 消息级错误
    INVALID_MESSAGE = ("E4001", False, "无效消息格式")
    PAYLOAD_TOO_LARGE = ("E4002", False, "消息负载过大")
    
    def __init__(self, code: str, retryable: bool, message: str):
        self.code = code
        self.retryable = retryable
        self.default_message = message

@dataclass
class AgentError:
    """Agent错误"""
    code: str
    message: str
    details: dict = field(default_factory=dict)
    retryable: bool = False
    retry_after: int = 0  # 秒
```

### 5.2 重试策略

```python
# retry_strategy.py
from dataclasses import dataclass
from typing import Callable, TypeVar
import asyncio
import random

@dataclass
class RetryConfig:
    """重试配置"""
    max_attempts: int = 3
    initial_delay_ms: int = 100
    max_delay_ms: int = 10000
    backoff_multiplier: float = 2.0
    jitter: bool = True
    retryable_errors: set = None  # 可重试的错误码

class RetryStrategy:
    """重试策略"""
    
    def __init__(self, config: RetryConfig):
        self.config = config
    
    async def execute(self, func: Callable, *args, **kwargs):
        """执行带重试的函数"""
        last_error = None
        
        for attempt in range(self.config.max_attempts):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_error = e
                
                if not self._is_retryable(e):
                    raise
                
                if attempt < self.config.max_attempts - 1:
                    delay = self._calculate_delay(attempt)
                    await asyncio.sleep(delay)
        
        raise last_error
    
    def _is_retryable(self, error: Exception) -> bool:
        """判断是否可重试"""
        if isinstance(error, AgentError):
            return error.retryable
        
        # 默认可重试的网络错误
        return isinstance(error, (TimeoutError, ConnectionError))
    
    def _calculate_delay(self, attempt: int) -> float:
        """计算延迟"""
        delay = self.config.initial_delay_ms * (
            self.config.backoff_multiplier ** attempt
        )
        delay = min(delay, self.config.max_delay_ms)
        
        if self.config.jitter:
            delay = delay * (0.5 + random.random())
        
        return delay / 1000
```

### 5.3 断路器模式

```python
# circuit_breaker.py
from enum import Enum
from datetime import datetime, timedelta
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"      # 正常
    OPEN = "open"          # 熔断
    HALF_OPEN = "half_open"  # 半开

class CircuitBreaker:
    """断路器"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
    
    async def call(self, func: Callable, *args, **kwargs):
        """带断路器的调用"""
        
        if self.state == CircuitState.OPEN:
            if self._should_try_reset():
                self._transition_to_half_open()
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_try_reset(self) -> bool:
        """检查是否应该尝试重置"""
        if not self.last_failure_time:
            return True
        
        elapsed = (datetime.utcnow() - self.last_failure_time).seconds
        return elapsed >= self.recovery_timeout
    
    def _transition_to_half_open(self):
        """转换到半开状态"""
        self.state = CircuitState.HALF_OPEN
        self.half_open_calls = 0
    
    def _on_success(self):
        """成功处理"""
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                self._transition_to_closed()
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        """失败处理"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self._transition_to_open()
    
    def _transition_to_open(self):
        """转换到打开状态"""
        self.state = CircuitState.OPEN
    
    def _transition_to_closed(self):
        """转换到关闭状态"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
```

---

## 六、完整协作流程示例

### 6.1 流程：Product Agent → Sales Agent → Service Agent

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    多Agent协作完整流程                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  用户: "我想找一批儿童玩具，要求性价比高"                                   │
│                                                                         │
│  ┌──────────────┐                                                       │
│  │ Orchestrator │                                                       │
│  └──────┬───────┘                                                       │
│         │ 创建任务 T_001                                                │
│         ▼                                                               │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Product Agent (商品匹配)                        │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │   │
│  │  │ CREATED │→│ PENDING │→│ RUNNING │→│COMPLETED│            │   │
│  │  └─────────┘  └─────────┘  └────┬────┘  └─────────┘            │   │
│  │                                   │                               │   │
│  │                                   ▼                               │   │
│  │                          返回: 20款匹配商品                          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    │ 提取TOP 5商品                       │
│                                    ▼                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Sales Agent (销售报价)                          │   │
│  │  收到商品列表 + 客户信息                                            │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                          │   │
│  │  │CREATED │→│ PENDING │→│ RUNNING │→ ...                       │   │
│  │  └─────────┘  └─────────┘  └─────────┘                          │   │
│  │                                                                    │   │
│  │  生成报价单 → 发送WhatsApp消息                                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    │ 客户回复 "价格太高"                  │
│                                    ▼                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Service Agent (客服处理)                        │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                          │   │
│  │  │CREATED │→│ PENDING │→│ RUNNING │→ ...                       │   │
│  │  └─────────┘  └─────────┘  └─────────┘                          │   │
│  │                                                                    │   │
│  │  识别意图: 讨价还价                                                 │   │
│  │  调用 Product Agent 获取成本价建议                                  │   │
│  │  回复客户: 可协商至 ¥2.3/件                                         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                         完成/归档                                  │   │
│  │  记录完整对话 → 更新客户画像 → 写入记忆系统                         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 代码实现

```python
# collaboration_example.py

class TradeCollaboration:
    """贸易协作流程"""
    
    def __init__(self, protocol: AgentProtocol, memory):
        self.protocol = protocol
        self.memory = memory
    
    async def handle_product_search(
        self,
        user_id: str,
        query: str,
        filters: dict = None
    ) -> dict:
        """处理商品搜索请求"""
        
        # 1. 创建任务
        task_id = f"task_{uuid.uuid4().hex[:12]}"
        
        # 2. 调用 Product Agent
        product_request = AgentRequest(
            message_id=f"req_{task_id}_1",
            sender="orchestrator",
            receiver="product_agent",
            skill_name="product-matching",
            payload={
                "task": "product_matching",
                "data": {
                    "query": query,
                    "filters": filters or {}
                },
                "context": {"user_id": user_id}
            },
            timeout_ms=30000
        )
        
        product_response = await self.protocol.send_request(product_request)
        
        if not product_response.success:
            return {
                "success": False,
                "error": product_response.error
            }
        
        # 3. 提取TOP商品
        products = product_response.data.get("matched_products", [])[:5]
        
        # 4. 获取客户信息
        customer_info = await self._get_customer_info(user_id)
        
        # 5. 调用 Sales Agent 生成报价
        quote_request = AgentRequest(
            message_id=f"req_{task_id}_2",
            sender="orchestrator",
            receiver="sales_agent",
            skill_name="quote-generation",
            payload={
                "task": "quote_generation",
                "data": {
                    "products": products,
                    "customer": customer_info
                }
            },
            mode=CallMode.SYNC,
            timeout_ms=20000
        )
        
        quote_response = await self.protocol.send_request(quote_request)
        
        # 6. 发送WhatsApp通知
        if quote_response.success:
            await self._send_whatsapp_notification(
                customer_info,
                quote_response.data
            )
        
        return {
            "success": True,
            "products": products,
            "quote": quote_response.data if quote_response.success else None,
            "task_id": task_id
        }
    
    async def handle_customer_feedback(
        self,
        user_id: str,
        message: str,
        conversation_id: str
    ) -> dict:
        """处理客户反馈"""
        
        # 1. 获取上下文
        context = await self._load_context(conversation_id)
        
        # 2. 调用 Service Agent 分类意图
        intent_request = AgentRequest(
            message_id=f"req_{uuid.uuid4().hex[:8]}_intent",
            sender="orchestrator",
            receiver="service_agent",
            skill_name="intent-classification",
            payload={
                "task": "intent_classification",
                "data": {
                    "message": message,
                    "history": context.get("history", [])
                }
            },
            timeout_ms=10000
        )
        
        intent_response = await self.protocol.send_request(intent_request)
        
        intent = intent_response.data.get("intent", "unknown")
        confidence = intent_response.data.get("confidence", 0)
        
        # 3. 根据意图路由
        if intent == "negotiation" and confidence > 0.8:
            # 讨价还价 - 重新询价
            return await self._handle_negotiation(context, message)
        elif intent == "complaint":
            # 投诉 - 升级处理
            return await self._handle_complaint(context, message)
        else:
            # 普通咨询 - FAQ处理
            return await self._handle_faq(message)
    
    async def _handle_negotiation(
        self,
        context: dict,
        message: str
    ) -> dict:
        """处理议价"""
        
        # 咨询 Product Agent 获取成本价
        cost_request = AgentRequest(
            message_id=f"req_{uuid.uuid4().hex[:8]}_cost",
            sender="orchestrator",
            receiver="product_agent",
            skill_name="price-analysis",
            payload={
                "task": "price_analysis",
                "data": {
                    "product_ids": [p["id"] for p in context.get("products", [])]
                }
            },
            timeout_ms=15000
        )
        
        cost_response = await self.protocol.send_request(cost_request)
        
        # 计算可接受的价格范围
        min_prices = cost_response.data.get("min_prices", {})
        
        return {
            "success": True,
            "action": "negotiation",
            "suggested_prices": min_prices,
            "message": "已计算可协商价格范围"
        }
```

---

## 七、性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 消息端到端延迟 | < 500ms | P95 |
| 消息投递成功率 | ≥ 99.9% | 含重试 |
| Agent响应时间 | < 3s | P95 |
| 并发处理能力 | 1000 QPS | 单Agent |
| 任务状态追踪 | 100% | 全链路可追溯 |
