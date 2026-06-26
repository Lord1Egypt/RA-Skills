---
name: research-tools
description: 科研工具包 - 包含文献搜索、数据分析、代码开发等科研常用工具
metadata:
  {
    "openclaw":
      {
        "emoji": "🔬",
        "requires": { "anyBins": ["python", "node", "git"] },
      },
  }
---

# 科研工具包 (Research Tools)

专为科研工作者设计的工具集合，支持文献搜索、数据分析、代码开发等功能。

## 核心功能

### 📚 文献搜索与获取
- 学术搜索引擎集成
- 文献摘要提取
- 全文内容分析

### 📊 数据分析
- 数据可视化
- 统计分析
- 机器学习建模

### 💻 代码开发
- 科研代码编写
- 数据处理脚本
- 模型训练代码

## 使用方法

### 文献搜索
```bash
# 搜索特定主题的文献
web_search query:"your research topic" count:10 freshness:"month"

# 获取文献全文
web_fetch url:"https://arxiv.org/abs/your-paper"
```

### 数据分析
```bash
# 使用 Python 进行数据分析
exec command:"python -c 'import pandas as pd; import matplotlib.pyplot as plt; # your analysis code'"
```

### 代码开发
```bash
# 创建科研项目
sessions_spawn runtime:"acp" task:"Create a research project structure for [your topic]"
```

## 科研工作流

1. **文献调研** - 搜索相关文献
2. **内容分析** - 总结文献要点
3. **方法复现** - 实现文献中的方法
4. **实验设计** - 设计新的实验方案
5. **结果分析** - 分析实验结果

## 支持的研究领域

- 计算机科学
- 人工智能
- 生物医学
- 物理化学
- 工程科学
- 社会科学