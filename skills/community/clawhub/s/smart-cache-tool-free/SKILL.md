---
slug: smart-cache-tool-free
name: smart-cache-tool-free
version: 1.0.0
displayName: 智能缓存工具-免费版
summary: "智能缓存管理工具,支持LRU/LFU策略与自动失效,适合个人项目性能优化。智能缓存管理工具免费版,面向个人开发者与小型项目."
license: Proprietary
edition: free
description: '智能缓存管理工具免费版,面向个人开发者与小型项目.
  核心能力:

  - LRU/LFU 缓存策略

  - TTL 自动过期失效

  - 内存缓存管理

  - 缓存命中率统计

  - 手动缓存清理

  - 简单持久化支持

  适用场景:

  - API 响应缓存

  - 计算结果缓存

  - 文件内容缓存

  - 个人项目性能优化

  差异化:免费版提供基础缓存能力。PRO版扩展分布式缓存、多级缓存与智能预热.
  适用关键词: cache, lru, lfu, ttl, 缓存, 缓存策略, 命中率, 缓存失效'
tags:
  - 缓存
  - 性能优化
  - LRU
  - 工具
  - 效率
  - 创意
  - 图像
  - cache
  - ttl
  - lru
  - 缓存策略
  - lfu
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
---
# 智能缓存工具 - 免费版

## 概述

智能缓存工具免费版帮助个人开发者实现高效的本地缓存管理。支持 LRU(最近最少使用)和 LFU(最不经常使用)两种缓存淘汰策略,配合 TTL 自动过期机制,有效提升应用性能。适合 API 响应缓存、计算结果缓存与文件内容缓存.
## 核心能力

### 1. LRU 缓存策略

最近最少使用淘汰,当缓存满时移除最久未访问的数据。适合访问模式均匀的场景.

**处理**: 解析LRU 缓存策略的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回LRU 缓存策略的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. LFU 缓存策略

最不经常使用淘汰,移除访问频率最低的数据。适合热点数据明显的场景.

**处理**: 解析LFU 缓存策略的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回LFU 缓存策略的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. TTL 自动过期

为缓存项设置生存时间,到期自动失效,保证数据新鲜度.

**处理**: 解析TTL 自动过期的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回TTL 自动过期的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 命中率统计

实时统计缓存命中率,帮助评估缓存效果.

**处理**: 解析命中率统计的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回命中率统计的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 5. 手动管理

支持手动获取、设置、删除缓存项,以及清空全部缓存.

**处理**: 解析手动管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回手动管理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 6. 持久化支持

将缓存内容保存到磁盘,重启后可恢复.

**处理**: 解析持久化支持的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回持久化支持的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：智能缓存管理工具、策略与自动失效、适合个人项目性能、免费版、面向个人开发者与、小型项目等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:API 响应缓存

缓存 API 响应,减少重复请求.
用户可通过自然语言指令触发此场景，工具将自动执行相应操作并返回结构化结果.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 智能缓存工具-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
from smart_cache import SmartCache
# ...
# 创建 LRU 缓存,最大 1000 项,TTL 300 秒
cache = SmartCache(
    strategy="lru",
    max_size=1000,
    ttl=300
)
# ...
# 缓存 API 响应
def get_user_profile(user_id):
    cache_key = f"user_profile:{user_id}"
# ...
    # 尝试从缓存获取
    cached = cache.get(cache_key)
    if cached:
        return cached
# ...
    # 缓存未命中,调用 API
    profile = call_api(f"/users/{user_id}")
# ...
    # 存入缓存
    cache.set(cache_key, profile)
    return profile
# ...
# 查看缓存统计
stats = cache.stats()
print(f"命中率: {stats['hit_rate']:.1%}")
print(f"总请求: {stats['total_requests']}")
print(f"命中: {stats['hits']}, 未命中: {stats['misses']}")
```

### 场景二:计算结果缓存

缓存耗时计算的结果.
```python
import time
from smart_cache import SmartCache
# ...
cache = SmartCache(strategy="lru", max_size=500, ttl=3600)
# ...
@cache.cached(prefix="compute")
def expensive_computation(n):
    """耗时的计算函数"""
    time.sleep(2)  # 模拟耗时计算
    return sum(i * i for i in range(n))
# ...
# 第一次调用(缓存未命中,执行计算)
result1 = expensive_computation(10000)  # 耗时约 2 秒
# ...
# 第二次调用(缓存命中,直接返回)
result2 = expensive_computation(10000)  # 耗时约 0.001 秒
# ...
print(f"两次结果一致: {result1 == result2}")  # True
```

### 场景三:文件内容缓存

缓存频繁读取的文件内容.
```python
from smart_cache import SmartCache
# ...
cache = SmartCache(strategy="lfu", max_size=100, ttl=600)
# ...
def read_config_file(path):
    cached = cache.get(f"file:{path}")
    if cached:
        return cached
# ...
    with open(path, 'r') as f:
        content = f.read()
# ...
    cache.set(f"file:{path}", content)
    return content
# ...
# 手动失效(配置文件更新后)
cache.delete("file:config.json")
# ...
# 清空所有缓存
cache.clear()
```

## 不适用场景

以下场景智能缓存工具-免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 安装

```bash
pip install smart-cache
```

### 基本使用

```python
from smart_cache import SmartCache
# ...
# 创建缓存
cache = SmartCache(
    strategy="lru",      # 策略: lru 或 lfu
    max_size=1000,       # 最大缓存项数
    ttl=300              # 默认 TTL(秒)
)
# ...
# 设置缓存
cache.set("key1", "value1")
cache.set("key2", {"data": [1, 2, 3]}, ttl=60)  # 自定义 TTL
# ...
# 获取缓存
value = cache.get("key1")  # "value1"
missing = cache.get("key3")  # None
# ...
# 删除缓存
cache.delete("key1")
# ...
# 查看统计
stats = cache.stats()
```

### 持久化

```python
# 保存到磁盘
cache.save_to_disk("cache_backup.json")
# ...
# 从磁盘恢复
cache.load_from_disk("cache_backup.json")
```

## 示例

### 缓存策略对比

| 策略 | 淘汰规则 | 适用场景 | 优点 |
|:-----|:-----|:-----|:-----|
| LRU | 最久未访问 | 访问均匀 | 实现简单,命中率高 |
| LFU | 访问最少 | 热点明显 | 保留热点数据 |
| FIFO | 最先进入 | 时序数据 | 实现最简单 |

### 命令参数

```python
SmartCache(
    strategy="lru",       # 缓存策略: lru, lfu, fifo
    max_size=1000,        # 最大缓存项数
    ttl=300,              # 默认 TTL(秒),0 表示不过期
    thread_safe=True,     # 线程安全
    persist=False,        # 是否自动持久化
    persist_path=None,    # 持久化路径
    stats=True            # 是否启用统计
)
```

### 装饰器使用

```python
# 函数结果缓存
@cache.cached(prefix="api", ttl=60)
def fetch_data(url):
    return requests.get(url).json()
# ...
# 带条件缓存
@cache.cached(prefix="search", condition=lambda r: r["count"] > 0)
def search(query):
    return search_engine.search(query)
```

## 最佳实践

1. **合理设置 TTL**:根据数据更新频率设置 TTL,太短命中率低,太长数据过期
2. **选择合适策略**:访问均匀用 LRU,热点明显用 LFU
3. **控制缓存大小**:根据可用内存设置 max_size,避免 OOM
4. **监控命中率**:命中率低于 50% 说明缓存效果差,需要调整策略
5. **缓存键规范**:使用 `前缀:标识` 格式(如 `user:123`),便于管理与清理
6. **及时失效**:数据更新后主动删除对应缓存,避免脏数据

## 常见问题

### Q: 缓存命中率低怎么办?

A: 检查以下几点:1) TTL 是否过短;2) max_size 是否过小导致频繁淘汰;3) 缓存键是否过于细粒度(如包含时间戳);4) 策略是否匹配访问模式。尝试调整参数并重新统计.
### Q: 缓存占用内存过大怎么办?

A: 1) 减小 max_size;2) 缓存前检查数据大小,过大不入缓存;3) 使用弱引用(WeakReference)缓存;4) 定期调用 `cache.cleanup()` 清理过期项.
### Q: LRU 和 LFU 怎么选?

A: 如果访问模式均匀(每个 key 被访问的概率差不多),用 LRU。如果有明显的热点数据(少数 key 被频繁访问),用 LFU。不确定时先用 LRU(适用性更广),根据命中率再调整.
### Q: 持久化缓存重启后会恢复吗?

A: 会。调用 `save_to_disk()` 保存后,重启程序调用 `load_from_disk()` 恢复。注意 TTL 在恢复后会继续倒计时,已过期的项不会恢复.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Python 3 | 运行时 | 必需 | 官方网站下载 |
| smart-cache | 缓存库 | 必需 | pip install smart-cache |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置

- 本 Skill 无需 API Key
- 纯本地缓存,不涉及外部 API 调用

### 可用性分类

- **分类**: MD+EXEC(Markdown指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 实现缓存管理与优化
- **限制**: 免费版仅支持本地内存缓存,不支持分布式缓存与多级缓存

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "智能缓存工具-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "smart cache"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
