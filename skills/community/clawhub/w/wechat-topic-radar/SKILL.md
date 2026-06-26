# Skill: 公众号爆款选题雷达

---

version: "1.0.0"
name: "wechat-topic-radar"
display_name: "公众号爆款选题雷达"
description: |
  全网热点聚合分析工具，智能发现公众号爆款选题。
  采集知乎、微博、小红书、公众号等多平台热点，
  通过综合热度算法识别高潜力选题，
  提供切入角度建议、竞品分析和内容差异化方案。
author: "liujian"
tags: ["内容创作", "公众号", "热点分析", "选题工具", "数据分析"]

---

## 功能特性

### 🔥 多平台热点采集 (20+平台)
- **国内热点**: 百度热搜、微博热搜、知乎热榜、今日头条、抖音热搜、B站热搜/日榜
- **技术社区**: 掘金、CSDN、GitHub、V2EX、HackerNews
- **新闻资讯**: 网易新闻、少数派、爱范儿
- **自动故障转移**: 多源备份，确保数据稳定采集

### 🌡️ 综合热度算法
基于5大维度评估选题价值：
- **平台热度** (20%)：原始热度数据
- **互动热度** (25%)：点赞/评论/分享数据
- **趋势热度** (20%)：新鲜度和增长趋势
- **内容质量** (15%)：标题质量和完整性
- **爆款潜力** (20%)：情绪价值和传播潜力

### 🎯 智能选题建议
- **切入角度推荐**：5种角度类型（情感共鸣/实用干货/观点评论/数据洞察/故事叙事）
- **标题优化建议**：基于爆款标题公式生成
- **文章结构规划**：提供完整的内容大纲
- **情绪定位分析**：匹配目标读者情绪

### 📊 竞品分析
- **相似话题识别**：发现同主题竞品内容
- **角度分布分析**：避免同质化竞争
- **差异化策略**：提供独特的切入建议

### 📈 可视化报告
- **HTML交互报告**：美观的可视化分析
- **热度趋势图表**：TOP10热度排行、雷达图分析
- **关键词云图**：热点词汇提取
- **JSON数据导出**：便于二次分析

---

## 使用方法

### 完整扫描
```bash
# 执行完整的热点扫描和分析
python scripts/radar_main.py scan

# 指定平台和数量
python scripts/radar_main.py scan -p zhihu weibo -l 30
```

### 快速扫描
```bash
# 快速获取热点概览
python scripts/radar_main.py quick

# 按关键词筛选
python scripts/radar_main.py quick -k 职场
```

### 单选题分析
```bash
# 分析单个选题
python scripts/radar_main.py analyze "为什么年轻人都不结婚了？"
```

### 多选题对比
```bash
# 对比多个选题
python scripts/radar_main.py compare "标题1" "标题2" "标题3"
```

### Python API调用
```python
from scripts.radar_main import WechatTopicRadar

# 初始化雷达
radar = WechatTopicRadar('config/config.yaml')

# 执行完整扫描
result = radar.scan()

# 获取TOP10热门选题
top_topics = result['scores'][:10]
for score in top_topics:
    print(f"{score.topic.title} - 热度: {score.total_score}")

# 快速扫描
quick_result = radar.quick_scan(keyword="职场")

# 分析单个选题
analysis = radar.analyze_topic("你的选题标题")
print(analysis.angles[0]['suggested_title'])
```

---

## 输出示例

### 控制台输出
```
============================================================
🔥 公众号爆款选题雷达 - 开始扫描
============================================================
📱 扫描平台: zhihu, weibo, xiaohongshu, wechat
📊 每平台采集: 50 条
⏰ 开始时间: 2024-01-15 09:30:00
------------------------------------------------------------

📡 Step 1: 多平台数据采集...
   ✅ 共采集 156 条热点数据

🌡️  Step 2: 综合热度计算...
   ✅ 计算完成，89 条达到热度阈值

📈 Step 3: 热点趋势分析...
   ✅ 提取 45 个关键词
   ✅ 识别 23 个上升话题

🔍 Step 4: 选题深度分析...
   ✅ 完成 10 个选题深度分析

📄 Step 5: 生成分析报告...
   ✅ HTML报告: ./data/reports/topic_radar_report_20240115_093015.html
   ✅ JSON数据: ./data/topic_data_20240115_093015.json

============================================================
✨ 扫描完成!
============================================================
🏆 TOP 5 热门选题:
   1. [知乎] 2024年最赚钱的10个行业... (热度: 92.5)
   2. [微博] 为什么年轻人都不结婚了？... (热度: 89.3)
   ...
```

### 分析报告内容
- 📊 **数据概览**：采集统计、平台分布
- 📈 **可视化图表**：热度排行、雷达图、关键词图
- ⭐ **精选推荐**：当下最热/高潜力/被低估选题
- 🔍 **深度分析**：TOP5选题的切入角度、差异化建议

---

## 配置说明

配置文件位置：`config/config.yaml`

```yaml
# 扫描平台配置
data_collection:
  platforms:
    - zhihu
    - weibo
    - xiaohongshu
    - wechat
  limit_per_platform: 50

# 热度算法权重
heat_algorithm:
  weights:
    platform: 0.20
    interaction: 0.25
    trend: 0.20
    quality: 0.15
    potential: 0.20

# 报告配置
report:
  output_dir: ./data/reports
```

---

## 项目结构

```
wechat-topic-radar/
├── SKILL.md                    # Skill定义文件
├── README.md                   # 项目说明
├── requirements.txt            # Python依赖
├── config/
│   └── config.yaml            # 配置文件
├── scripts/
│   ├── radar_main.py          # 主控模块
│   ├── data_collector.py      # 数据采集
│   ├── heat_algorithm.py      # 热度算法
│   ├── topic_analyzer.py      # 选题分析
│   └── report_generator.py    # 报告生成
├── data/                      # 数据存储
│   └── reports/              # 报告输出
└── assets/                    # 静态资源
```

---

## 技术栈

- **Python 3.8+**
- **requests**：网络数据采集
- **jieba**：中文分词和关键词提取
- **numpy**：数值计算
- **plotly**：交互式可视化
- **pyyaml**：配置管理

---

## 数据来源

| 平台 | 类型 | 数据源 |
|:---|:---|:---|
| 百度热搜 | 综合热点 | 小尘API |
| 微博热搜 | 社交媒体 | 小尘API |
| 知乎热榜 | 问答社区 | 小尘API |
| 今日头条 | 新闻资讯 | 小尘API |
| 抖音热搜 | 短视频 | 小尘API |
| B站热搜/日榜 | 视频社区 | 小尘API |
| 掘金 | 技术社区 | 小尘API |
| CSDN | 技术社区 | 小尘API |
| GitHub | 开源社区 | 小尘API |
| 网易新闻 | 新闻资讯 | 小尘API |
| 少数派 | 科技媒体 | 小尘API |
| 爱范儿 | 科技媒体 | 小尘API |
| V2EX | 技术社区 | 官方API |
| HackerNews | 技术社区 | 官方API |

---

## 注意事项

1. **数据准确性**：网络数据采集可能存在延迟或波动
2. **合规使用**：请遵守各平台的数据使用规范
3. **热点时效**：热点内容具有时效性，建议及时跟进
4. **人工判断**：算法建议仅供参考，最终选题需结合人工判断

---

## 更新计划

- [x] 接入更多数据源（抖音、B站、今日头条等）
- [ ] AI智能标题生成
- [ ] 历史热点趋势分析
- [ ] 个性化推荐算法
- [ ] 定时自动推送报告

---

## 联系作者

- 作者: liujian
- 邮箱: sxzxlj@163.com
- 版本: 1.0.0
