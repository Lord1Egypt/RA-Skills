# 财经热点新闻爬取与话题归纳系统
###技术支持：微信名quant\_village\_dog | QQ:13620658 | 邮件：13620658@qq.com
###技术社区：QQ群：1057968391

---
name: stock-hot-news
description: >
   财经热点新闻爬取与话题归纳系统。
  Use when: 用户需要获取实时财经新闻或快讯，财经热点新闻，焦点话题。
  NOT for: 普通新闻，天气预报，娱乐新闻，花边新闻
---

# 技能标题

## When to Run
- 触发条件1：用户说“财经新闻”
- 触发条件2：用户说“财经热点”
- 触发条件3：用户说“财经快讯”
- 触发条件4：用户说“财经焦点”
- 触发条件5：用户说“财经快报”

## Workflow
```bash
cd skills/stock-hot-news
python main.py --module3-mode playwright
```

## Output Format
定义输出的格式


## 系统概述

这是一个完整的财经热点新闻爬取、话题归纳和实时快讯采集系统。系统分为四个核心模块，可以独立运行或通过主调度程序集成使用。

**当前版本特点**：
- ✅ **3个主力财经网站**：财联社、金融界、证券时报网（稳定爬取）
- ✅ **混合评分系统**：本地规则(55分) + 大模型评估(45分)
- ✅ **专业HTML报告**：可视化设计，自动打开浏览器
- ✅ **实时快讯采集**：华尔街见闻重要快讯（Playwright模式）
- ⏳ **未来扩展**：更多财经网站适配器正在开发中

**注意**：配置文件中的其他6个财经网站（新浪财经、华尔街见闻、和讯网、21世纪经济报道、第一财经、财新网）当前版本暂未实现完整适配器，已禁用。未来版本将逐步添加支持。

## 文件结构

### 1. 主程序和工作流
- **`main.py`** - 主调度程序，集成Module 1-4的完整工作流
- **`run_main.bat`** - Windows批处理启动菜单

### 2. Module 1：主力网站热点新闻爬取
- **`module1_main_sites.py`** - 主力财经网站热点新闻爬取模块（财联社、金融界、证券时报网）
- **`website_adapters_final.py`** - 网站适配器支持模块
- **`cls_hot_news.py`** - 财联社热点新闻抓取器
- **`jrj_hot_news.py`** - 金融界热点新闻抓取器  
- **`stcn_hot_news.py`** - 证券时报网热点新闻抓取器

### 3. Module 2：热点新闻话题归纳与评分
- **`module2_summarize_filtered.py`** - 过滤版话题归纳模块
  - 过滤掉标题小于5字的无关内容
  - 过滤与财经、政治、国际形势、科技无关的内容
  - 结合summarize和关键词过滤
  - 支持话题评分和深度分析
- **`rate_news_new.py`** - 新闻评分模块（混合本地+大模型评分）
- **`summarize_utils.py`** - 摘要生成工具函数

### 4. Module 3：华尔街见闻快讯采集
- **`module3_news_flash.py`** - 华尔街见闻重要快讯采集模块
  - 支持Playwright模式（带浏览器）
  - 自动过滤财经相关重要快讯
  - 输出JSON和文本格式

### 5. Module 4：综合报告生成
- **`module4_report_generator.py`** - 财经热点新闻综合报告生成器
  - 整合三个模块数据：热点话题TOP5 + 深度分析TOP3 + 快讯TOP10
  - 生成文本版和HTML版报告（专业视觉设计）
  - 包含自动打开浏览器和清理旧数据功能

### 6. 辅助工具
- **`scrapling_util.py`** - 网络爬取工具函数
- **`url_config.json`** - 系统配置文件（已精简优化）

### 7. 文档文件
- **`README.md`** - 主说明文档（本文档）
- **`DEEP_ANALYSIS_ENHANCEMENT.md`** - 深度分析模块增强说明
- **`JRJ_HOT_NEWS_README.md`** - 金融界热点新闻抓取器使用说明
- **`STCN_HOT_NEWS_README.md`** - 证券时报网热点新闻抓取器使用说明
- **`技术支持.jpg`** - 使用和技术支持说明

## 核心功能

### 1. 完整工作流（main.py）
```
输入 → Module 1爬取 → 文章数据 → Module 2归纳 → 热点话题 → Module 3快讯 → Module 4报告 → 输出
```

### 2. Module 1功能
- 爬取多个主力财经网站（证券时报、金融界、财联社等）
- 使用scrapling进行隐身访问
- 48小时时间过滤
- 保存为JSON格式

### 3. Module 2功能（过滤版）
- **智能过滤**：
  - 过滤标题小于5字的无关内容
  - 过滤与财经、政治、国际形势、科技无关的内容
  - 使用财经关键词库进行内容过滤
  - 移除广告、推广等非新闻内容
- **话题分组**：基于关键词的精确分组
- **AI话题归纳**：使用summarize技能生成专业总结
- **话题评分**：基于文章数量、来源多样性、总结质量等
- **生成前N名热点话题**：默认top5，支持自定义

### 4. Module 3功能
- 从华尔街见闻重要快讯页面采集实时快讯
- 支持单次抓取和滚动抓取（模拟用户浏览）
- 自动过滤财经相关重要快讯
- 关键词过滤（财经、重要事件等）
- 去重和时间排序处理
- 输出JSON和文本格式

### 5. Module 4功能
- **数据整合**：整合Module 1、2、3的输出数据
- **头条新闻TOP5**：显示热度最高的5篇新闻
- **深度分析TOP3**：显示评分最高的3个话题的深度分析
- **快讯TOP10**：显示最重要的10条实时快讯
- **智能评分**：自动计算热度和重要性评分
- **投资建议**：基于话题分析生成投资建议
- **多格式输出**：生成文本版和HTML版报告
- **可视化展示**：HTML报告包含卡片式布局和交互效果



## 使用方法

### 1. 运行完整系统（推荐）
```bash
# 使用批处理启动菜单
run_main.bat

# 或使用Python直接运行
python main.py --module3-mode playwright
```

### 2. 只运行Module 1（新闻爬取）
```bash
python module1_main_sites.py
```

### 3. 只运行Module 2（话题归纳与评分）
```bash
python module2_summarize_filtered.py
```

### 4. 只运行Module 3（华尔街见闻快讯）
```bash
# 当前只支持Playwright模式（带浏览器）
python module3_news_flash.py
```

### 5. 只运行Module 4（综合报告生成）
```bash
python module4_report_generator.py
```

### 6. 测试单个网站爬虫
```bash
# 测试财联社爬虫
python cls_hot_news.py

# 测试金融界爬虫
python jrj_hot_news.py

# 测试证券时报网爬虫
python stcn_hot_news.py
```

## 输出目录结构

```
D:/SelfData/clawtemp/
├── title_news_crawl/
│   ├── temp/                    # Module 1输出
│   ├── summarized/              # Module 2输出
│   └── article_summaries/       # 文章摘要结果
├── wallstreetcn_news/           # Module 3输出目录
├── reports/
│   ├── final/                   # Module 4输出目录（综合报告）
│   └── main/                    # main.py执行报告
└── logs/                        # 日志文件
```

## 配置要求

1. **Python环境**：Python 3.7+
2. **依赖包**：
   - `scrapling`：网页抓取
   - 其他标准库：json, pathlib, datetime等
3. **API密钥**：需要设置DeepSeek API密钥
   ```python
   os.environ['OPENAI_API_KEY'] = 'your-api-key'
   os.environ['OPENAI_BASE_URL'] = 'https://api.deepseek.com'
   ```

## 注意事项

1. **scrapling使用**：系统使用scrapling命令行方式获取网页内容
2. **summarize命令**：需要正确配置summarize命令路径
3. **网络访问**：需要能够访问目标财经网站
4. **频率控制**：避免过于频繁的请求，以免被网站屏蔽

## 版本历史

- **V1**：基础爬取功能
- **V2**：增加话题归纳
- **V3**：完整工作流 + 话题评分 + 文章摘要
- **当前版本**：修复版，解决参数传递和报告生成问题

## 故障排除

### 常见问题：
1. **scrapling不可用**：检查scrapling是否安装，使用命令行测试
2. **summarize命令找不到**：检查summarize命令路径
3. **API密钥错误**：检查环境变量设置
4. **编码问题**：Windows系统可能需要处理GBK编码

### 调试方法：
1. 运行测试脚本检查工具可用性
2. 查看日志文件了解详细错误信息
3. 逐步运行各个模块定位问题

## 扩展开发

### 添加新网站适配器：
1. 在`website_adapters_final.py`中添加新的适配器类
2. 实现`fetch_hot_news()`方法
3. 在`module1_main_sites.py`中注册新适配器

### 修改话题关键词：
1. 编辑`module2_summarize_filtered.py`中的`finance_keywords`和`filter_keywords`列表
2. 添加或修改财经关键词和过滤关键词

### 调整评分算法：
1. 修改`rate_news_new.py`中的评分逻辑
2. 调整信源权重、时间新鲜度等评分参数

---

**最后更新**：2026-03-28  
**维护者**：OpenClaw Assistant  
**状态**：生产就绪 ✅