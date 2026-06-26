# Web Search 使用示例

## 场景1: 查找最新新闻

用户: "最近有什么AI方面的重大新闻？"

```bash
python scripts/search.py "AI 人工智能 最新新闻 2026" -t week -n 10
```

## 场景2: 技术问题搜索

用户: "Python asyncio怎么用？"

```bash
python scripts/search.py "Python asyncio 教程 用法" -e all
```

如果需要更专业的内容，缩小范围：

```bash
python scripts/search.py "site:docs.python.org asyncio tutorial" -e bing
```

## 场景3: 限定站点搜索

用户: "在知乎上找一下关于大模型微调的讨论"

```bash
python scripts/search.py "site:zhihu.com 大模型微调 LoRA" -e baidu
```

## 场景4: 查找文档/论文

用户: "找一些关于RAG技术的PDF论文"

```bash
python scripts/search.py "filetype:pdf RAG retrieval augmented generation" -e bing
```

## 场景5: 组合高级语法

用户: "在GitHub上找Python写的web爬虫项目，不要教程"

```bash
python scripts/search.py "site:github.com Python web爬虫 crawler -教程 -博客" -e all
```

## 场景6: JSON格式获取结果供程序处理

```bash
python scripts/search.py "深度学习框架对比" -f json -n 5
```

输出可以被后续脚本直接解析处理。

## 场景7: 多轮搜索深入调研

第一步：宽泛搜索了解大方向

```bash
python scripts/search.py "2026年编程语言趋势" -t year
```

第二步：根据结果深入某个方向

```bash
python scripts/search.py "Rust 2026 生态系统 发展" -t month
```

第三步：用WebFetch获取某篇具体文章的完整内容

```
WebFetch(url="https://example.com/article", prompt="总结这篇文章的核心观点")
```

## 场景8: 排除干扰结果

用户: "搜一下Python装饰器，不要那些入门级的"

```bash
python scripts/search.py "Python装饰器 高级用法 -入门 -初学者 -基础" -e all
```
