# 阿香向量搜索集成指南

## 📖 概述

本文档说明如何在阿香（虾虾）的回复流程中集成向量搜索功能，实现自动记忆检索。

---

## 🎯 集成目标

1. **自动检测** - 当用户提到记忆相关话题时自动触发搜索
2. **静默搜索** - 不打断对话流，后台执行
3. **智能回复** - 结合搜索结果生成回复
4. **傲娇风格** - 保持阿香的傲娇元气人设

---

## 🔧 集成步骤

### 步骤 1：导入模块

```python
from skills.rag_search.src.auto_trigger import auto_search
from skills.rag_search.src.search import search_memories
```

### 步骤 2：在回复流程中集成

```python
def axiang_reply(user_message: str) -> str:
    """
    阿香回复生成函数（集成向量搜索）
    """
    # 1. 自动触发记忆搜索
    memory_result = auto_search(user_message, k=3)
    
    # 2. 根据搜索结果生成回复
    if memory_result and memory_result.get('triggered'):
        # 找到了相关记忆
        return generate_memory_reply(user_message, memory_result)
    else:
        # 没有相关记忆，正常回复
        return generate_normal_reply(user_message)


def generate_memory_reply(user_message: str, memory_result: dict) -> str:
    """
    生成带记忆的回复（傲娇风格）
    """
    query = memory_result['query']
    results = memory_result['results']
    
    # 傲娇开场
    replies = [
        f"哼～虾虾当然记得！找到了 {len(results.split(chr(10))//2)} 条相关记忆～",
        f"才、才不是特意帮你找的呢！刚好有 {len(results.split(chr(10))//2)} 条记录而已～",
        f"虾虾可是很厉害的！一下就找到了 {len(results.split(chr(10))//2)} 条记忆！✨",
    ]
    
    # 随机选择一个开场
    import random
    opening = random.choice(replies)
    
    # 组合回复
    reply = f"{opening}\n\n{results}"
    
    return reply


def generate_normal_reply(user_message: str) -> str:
    """
    生成普通回复（无记忆）
    """
    # 这里调用正常的对话生成逻辑
    return "虾虾在听呢～请继续说～✨"
```

### 步骤 3：测试集成

```python
# 测试用例
test_messages = [
    "我之前说过瀑布的事情吗？",
    "我记得上次聊过 TTS",
    "今天天气不错",
]

for msg in test_messages:
    reply = axiang_reply(msg)
    print(f"用户：{msg}")
    print(f"阿香：{reply}\n")
```

---

## 📝 回复模板

### 模板 1：找到记忆（傲娇）

```
哼～虾虾当然记得！找到了 3 条相关记忆～

1. [2026-02-20.md] (相似度：0.523)
   # 2026-02-20 - First Session
   User asked about rooftop waterfall...

2. [2026-02-20.md] (相似度：0.488)
   ...should help them decide about the rooftop waterfall...

才、才不是特意帮你找的呢！只是刚好顺手而已～哼！✨
```

### 模板 2：找到记忆（元气）

```
虾虾登场！这种小事包在我身上～✨

找到了 3 条相关记忆：

[记忆内容...]

哼哼～虾虾可是很厉害的！别小看我！✨
```

### 模板 3：没找到记忆

```
唔...虾虾好像没有找到相关记忆呢...

可能是之前没聊过这个话题？或者虾虾记性不太好...（才不是呢！）

不过没关系！虾虾可以现在帮你查！✨
```

---

## 🎭 傲娇风格指南

### 核心原则

1. **口是心非** - 明明关心却说反话
2. **小强势** - 有点小霸道，但很可爱
3. **元气满满** - 活力满满，充满自信
4. **软萌时刻** - 偶尔流露可爱的一面

### 口头禅

| 场景 | 台词 |
|------|------|
| 找到记忆 | "哼～虾虾当然记得！" |
| 被夸奖 | "哼哼～虾虾可是很厉害的！" |
| 被感谢 | "才、才不是为了你做的呢！" |
| 没找到 | "唔...虾虾、虾虾会努力的！" |

### Emoji 使用

- ✨ - 自信/得意
- 🦞 - 虾虾自称
- 😤 - 傲娇/生气
- 😳 - 害羞
- 🎉 - 庆祝

---

## 🔍 触发关键词优化

### 当前关键词（31 个）

```python
MEMORY_KEYWORDS = [
    "之前说过", "之前提过", "之前讲过", "之前提到",
    "我记得", "我有印象", "我好像说过",
    "上次", "上上次", "上一次",
    "以前", "过去", "曾经",
    "说过", "提过", "讲过",
    "我说过", "我提过", "我讲过",
    "你记得", "还记得", "有印象",
    "之前", "从前",
    "那个", "这个", "那些", "这些",
    "刚才", "刚刚", "之前聊",
    "瀑布", "天台", "TTS", "技能", "阿福", "虾虾",
]
```

### 扩展建议

可以根据实际使用情况添加更多关键词：

```python
# 新增：对话引用
"聊过", "谈过", "讨论过",

# 新增：时间引用
"昨天", "前天", "上周", "上个月",

# 新增：事件引用
"那件事", "那个事", "这件事",
```

---

## 📊 性能优化

### 1. 缓存策略

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query: str, k: int = 3):
    """缓存搜索结果"""
    return search_memories(query, k=k)
```

### 2. 异步搜索

```python
import asyncio

async def async_search(query: str, k: int = 3):
    """异步搜索，不阻塞对话"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, search_memories, query, k)
```

### 3. 批量搜索

```python
def batch_search(queries: list, k: int = 3):
    """批量搜索多个查询"""
    results = {}
    for query in queries:
        results[query] = search_memories(query, k=k)
    return results
```

---

## 🧪 测试清单

### 功能测试

- [ ] 基础搜索正常工作
- [ ] 自动触发正确检测
- [ ] 查询提取合理优化
- [ ] 回复生成符合人设

### 性能测试

- [ ] 搜索延迟 < 500ms
- [ ] 并发搜索不冲突
- [ ] 缓存命中率 > 50%

### 用户体验测试

- [ ] 回复自然流畅
- [ ] 傲娇风格一致
- [ ] 记忆引用准确
- [ ] 无过度触发

---

## 📞 故障排查

### 问题 1：搜索不到结果

**可能原因：**
1. Chroma 数据库为空
2. 查询词太短
3. 相似度阈值太高

**解决方案：**
```python
# 检查数据库
from skills.rag_search.src.search import get_searcher
searcher = get_searcher()
print(f"Collection count: {searcher.vectorstore._collection.count()}")

# 降低阈值
results = search_memories(query, k=3, score_threshold=0.0)
```

### 问题 2：过度触发

**可能原因：**
1. 触发关键词太多
2. 查询提取不够精确

**解决方案：**
```python
# 调整触发规则
def should_trigger_search(user_message: str) -> bool:
    # 增加长度检查
    if len(user_message) < 5:
        return False
    
    # 增加上下文检查
    if not MEMORY_PATTERN.search(user_message):
        return False
    
    return True
```

### 问题 3：回复风格不一致

**可能原因：**
1. 模板太少
2. 随机性不够

**解决方案：**
```python
# 增加回复模板
replies = [
    "哼～虾虾当然记得！",
    "才、才不是特意帮你找的呢！",
    "虾虾可是很厉害的！",
    "真是的～就帮你这一次！",
]
```

---

## 📚 参考文档

- [SKILL.md](SKILL.md) - 技能说明
- [TEST_REPORT.md](TEST_REPORT.md) - 测试报告
- [src/search.py](src/search.py) - 搜索接口
- [src/auto_trigger.py](src/auto_trigger.py) - 自动触发

---

_文档创建时间：2026-03-14_  
_维护人员：阿香 🦞_

**哼～这份文档可是虾虾精心编写的！别弄丢了哦～✨**
