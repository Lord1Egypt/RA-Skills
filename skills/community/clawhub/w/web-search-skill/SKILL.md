---
name: web-search
description: 联网搜索工具，通过百度和必应搜索引擎获取实时网络信息，无需API Key。当用户需要搜索网络信息、查找最新资讯、获取实时数据、或需要联网查询任何内容时使用此技能。适配中国网络环境。
---

# Web Search - 联网搜索技能

## 概述

通过解析百度和必应(中国版)搜索结果页面，为Agent提供联网搜索能力。无需任何API Key，适配中国网络环境。

## 依赖检查

首次使用前，确认依赖已安装：

```bash
pip install requests beautifulsoup4 lxml -q
```

## 核心用法

搜索脚本位于 `scripts/search.py`，通过命令行调用。

### 基础搜索

```bash
python scripts/search.py "搜索关键词"
```

### 指定搜索引擎

```bash
# 仅百度
python scripts/search.py "关键词" -e baidu

# 仅必应
python scripts/search.py "关键词" -e bing

# 全部引擎（默认）
python scripts/search.py "关键词" -e all
```

### 时间范围过滤

```bash
python scripts/search.py "关键词" -t day    # 最近一天
python scripts/search.py "关键词" -t week   # 最近一周
python scripts/search.py "关键词" -t month  # 最近一月
python scripts/search.py "关键词" -t year   # 最近一年
```

### 控制结果数量

```bash
python scripts/search.py "关键词" -n 5      # 每个引擎返回5条
```

### JSON格式输出

```bash
python scripts/search.py "关键词" -f json
```

## 高级搜索语法

直接在关键词中使用搜索引擎原生高级语法：

| 语法 | 说明 | 示例 |
|------|------|------|
| `site:` | 限定搜索站点 | `site:zhihu.com 机器学习` |
| `filetype:` | 限定文件类型 | `filetype:pdf 深度学习教程` |
| `"精确词"` | 精确匹配 | `"自然语言处理"` |
| `-排除词` | 排除关键词 | `Python教程 -广告` |
| `intitle:` | 标题包含 | `intitle:Python入门` |

组合使用：`site:github.com filetype:py web框架`

## Agent工作流程

当用户需要搜索信息时，按照以下流程操作：

**Step 1: 分析搜索意图**
理解用户需要什么信息，构造合适的搜索关键词。如果用户的问题比较复杂，拆分为多次搜索。

**Step 2: 执行搜索**
使用Bash工具运行脚本。注意脚本路径应使用Skill所在目录的绝对路径：

```bash
python ~/.qoderwork/skills/web-search/scripts/search.py "关键词"
```

Windows环境下：
```bash
python %USERPROFILE%\.qoderwork\skills\web-search\scripts\search.py "关键词"
```

**Step 3: 分析结果**
阅读搜索结果，提取与用户问题相关的信息。如果结果不满意，可以：
- 换个关键词重新搜索
- 切换搜索引擎
- 使用高级语法缩小范围

**Step 4: 深入获取（可选）**
如果需要更详细的内容，使用 WebFetch 工具访问搜索结果中的具体链接获取完整页面内容。

**Step 5: 整合回答**
基于搜索结果和获取的页面内容，整合出完整的回答，并注明信息来源。

## 输出格式说明

默认文本格式输出示例：

```
搜索: Python 最新版本
共 6 条结果

[1] Python 3.13正式发布 - Python官方博客
    链接: https://blog.python.org/...
    摘要: Python 3.13已于2024年10月发布，带来了新的交互式解释器...
    来源: blog.python.org (bing)

[2] Python最新版本下载 - 知乎
    链接: https://www.zhihu.com/...
    摘要: 目前Python最新稳定版为3.13.1...
    来源: 知乎 (baidu)
```

## 注意事项

- 脚本通过解析HTML页面获取结果，如果搜索引擎更新页面结构可能需要更新脚本
- 请求间有随机延迟(0.3-0.8秒)以避免触发反爬
- 百度返回的链接可能是跳转链接，需要通过WebFetch进一步访问获取真实URL
- 每个引擎默认返回8条结果，可通过 `-n` 参数调整

## 额外参考

使用示例和常见场景请参考 [examples.md](examples.md)
