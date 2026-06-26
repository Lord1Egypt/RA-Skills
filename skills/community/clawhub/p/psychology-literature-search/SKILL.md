# 心理学文献检索助手

通过免费学术 API 快速检索心理学相关文献，支持中英文检索、表格导出、多种引用格式，帮助研究者高效查找论文、生成参考文献。

## 功能介绍

整合多个免费学术数据库，提供一站式文献检索服务。无需 API key，无需付费订阅，输入关键词即可获取相关论文及完整元数据，并可一键导出为表格或生成多种格式引用。

## 支持的数据源

| 数据源 | 特点 | 适用场景 |
|--------|------|----------|
| **Semantic Scholar** | 覆盖广、含摘要 | 综合检索、看摘要 |
| **OpenAlex** | 开放获取信息全 | 找可下载论文 |
| **CrossRef** | DOI 元数据权威 | 核对引用信息 |
| **中文文献** | OpenAlex 中文期刊 | 检索中文研究 |

> ⚠️ **关于中文文献**：知网(CNKI)、万方没有公开免费 API 且禁止爬取。本工具通过 OpenAlex 收录的中文期刊文献（带 DOI）进行合规检索。

## 主要功能

### 🔍 多源关键词检索
- 支持中英文关键词
- 可按年份过滤（只看近期文献）
- 按被引次数排序，优先展示高影响力论文

### 🇨🇳 中文文献检索
- 专门的中文文献检索通道
- 通过语言过滤定位中文研究

### 📊 批量导出表格
- 一键导出为 CSV（可用 Excel 打开）
- 自动处理中文编码，不乱码
- 包含标题、作者、年份、期刊、被引、DOI、链接

### 📝 多种引用格式
- **APA** - 心理学/社科常用
- **GB/T 7714** - 中国国家标准
- **MLA** - 人文学科
- **Chicago** - 芝加哥格式
- 可批量导出参考文献列表

## 使用方法

### 基础检索
```python
from literature_search import LiteratureSearch

# 初始化（填邮箱可获得更快响应，可选）
searcher = LiteratureSearch(email="your_email@example.com")

# 英文检索
papers = searcher.search(
    query="social cognition attention",
    source="semantic_scholar",
    limit=10,
    year_from=2020
)
```

### 中文文献检索
```python
# 检索中文文献
cn_papers = searcher.search(
    query="社会认知 注意",
    source="chinese",
    limit=10
)
```

### 导出为表格
```python
# 导出检索结果为 CSV 表格
searcher.export_to_csv(papers, filename="文献列表.csv")
```

### 生成引用
```python
# 单条引用 - 支持多种格式
print(searcher.format_citation(papers[0], style="apa"))      # APA
print(searcher.format_citation(papers[0], style="gbt7714"))  # 国标
print(searcher.format_citation(papers[0], style="mla"))      # MLA
print(searcher.format_citation(papers[0], style="chicago"))  # Chicago

# 批量导出参考文献列表
searcher.export_citations(papers, style="gbt7714", filename="参考文献.txt")
```

## 引用格式示例

同一篇文献的不同格式输出：

```
APA:     Zhang Wei, Li Ming, & Wang Fang (2023). The role of gaze cueing
         in social attention. Journal of Experimental Psychology.
         https://doi.org/10.1234/example.2023

国标:     Zhang Wei, Li Ming, Wang Fang. The role of gaze cueing in social
         attention[J]. Journal of Experimental Psychology, 2023.

MLA:     Zhang Wei, et al. "The role of gaze cueing in social attention."
         Journal of Experimental Psychology, 2023.

Chicago: Zhang Wei, Li Ming, and Wang Fang. "The role of gaze cueing in
         social attention." Journal of Experimental Psychology (2023).
```

## 应用场景

- **文献综述**：快速收集某主题核心论文，导出表格整理
- **追踪前沿**：用年份过滤查看最新研究
- **找经典文献**：按被引次数定位领域高引论文
- **中文研究**：检索国内学者的相关工作
- **写论文**：一键生成符合期刊要求的参考文献格式

## 检索关键词建议

心理学常用检索词：
- 社会认知：`social cognition`, `theory of mind`, `face perception`
- 注意与知觉：`attention`, `gaze cueing`, `visual perception`
- 记忆：`implicit memory`, `working memory`, `priming`
- 情绪：`emotion regulation`, `affective processing`

> 💡 提示：英文关键词在国际数据库中检索效果最佳；中文检索请用 `source="chinese"`。

## 系统要求

- Python 3.8 或更高版本
- 无需额外依赖（仅使用 Python 标准库）
- 需要网络连接

## 注意事项

- 所有 API 均免费且无需注册
- 提供邮箱可加入 OpenAlex/CrossRef 的"礼貌池"，响应更快更稳定
- 请合理控制请求频率，避免对公共 API 造成压力
- 知网/万方等商业数据库需通过官方授权途径访问

## 关于本工具

为心理学及行为科学研究人员设计，旨在降低文献检索门槛，提高研究与写作效率。

**作者**: @zhan599
**所属机构**: 华南师范大学 应用心理学系
**用途**: 学术文献检索、引用管理、研究辅助
