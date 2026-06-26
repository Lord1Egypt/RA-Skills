---
name: showstart
description: 秀动演出查询与管理工具。用于查询秀动平台上的演出信息，包括演出详情、城市搜索、分类搜索、风格搜索、艺人搜索、附近演出等功能。当用户需要查找演出信息、了解演出详情、按城市/分类/风格搜索演出、或查找附近演出时使用此技能。
---

# Showstart Skill

秀动演出查询与管理工具，支持多种方式搜索和查询演出信息。

## 功能概述

- 查询演出详情
- 关键字搜索演出
- 按城市搜索（支持模糊匹配）
- 按分类搜索（音乐节、演唱会等）
- 按风格搜索（摇滚、流行、民谣等）
- 艺人/场地名搜索
- 附近演出查询（基于经纬度）

## 使用方法

### 1. 查询演出详情

获取指定演出的详细信息：

```python
from scripts.showstart_api import get_activity

activity = get_activity(135591)
```

### 2. 搜索演出

#### 关键字搜索
```python
from scripts.showstart_api import search_keyword

results = search_keyword("周云蓬")
```

#### 城市搜索
```python
from scripts.showstart_api import search_city

# 搜索北京的演出
results = search_city("北京")

# 搜索北京的音乐节
results = search_city("北京", category="音乐节")

# 搜索北京的摇滚演出
results = search_city("北京", style="摇滚")
```

#### 分类搜索
```python
from scripts.showstart_api import search_category

# 搜索音乐节
results = search_category("音乐节")

# 搜索上海的音乐节
results = search_category("音乐节", city="上海")
```

#### 风格搜索
```python
from scripts.showstart_api import search_style

# 搜索摇滚演出
results = search_style("摇滚")

# 搜索北京的民谣演出
results = search_style("民谣", city="北京")
```

#### 艺人/场地搜索
```python
from scripts.showstart_api import search_name

results = search_name("周云蓬")
```

#### 附近演出
```python
from scripts.showstart_api import search_nearby

# 搜索附近的演出（经纬度）
results = search_nearby(116.3956, 39.9299)
```

### 3. 使用命令行工具

```bash
# 查询演出详情
python scripts/showstart_api.py activity 135591

# 关键字搜索
python scripts/showstart_api.py keyword 周云蓬

# 城市搜索
python scripts/showstart_api.py city 北京

# 分类搜索
python scripts/showstart_api.py category 音乐节

# 风格搜索
python scripts/showstart_api.py style 摇滚

# 艺人/场地搜索
python scripts/showstart_api.py name 周云蓬

# 附近演出
python scripts/showstart_api.py nearby 116.3956 39.9299
```

## API 限制

- **频率限制**: 1秒最多1次请求，10分钟最多60次请求
- **缓存**: 搜索结果缓存1小时
- **分页**: 默认每页100条，最大100条

## 错误处理

| 错误码 | 说明 |
| ------ | ------ |
| 100001 | 资源不存在 |
| 100002 | 缺少必要参数 |
| 100003 | 频率限制超限 |

## 参考资料

详细API文档请参见：[references/api_docs.md](references/api_docs.md)
