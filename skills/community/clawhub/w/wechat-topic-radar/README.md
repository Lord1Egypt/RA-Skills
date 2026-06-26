# 🔥 公众号爆款选题雷达

> 全网热点聚合分析工具，智能发现公众号爆款选题

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 功能特性

### 📡 多平台热点采集
- **知乎热榜** - 实时抓取知乎热门话题
- **微博热搜** - 监控微博热搜榜单  
- **小红书热门** - 采集小红书热门笔记
- **公众号爆文** - 追踪公众号10万+文章

### 🌡️ 综合热度算法
基于5大维度科学评估选题价值：

| 维度 | 权重 | 说明 |
|:---|:---:|:---|
| 平台热度 | 20% | 原始热度数据 |
| 互动热度 | 25% | 点赞/评论/分享数据 |
| 趋势热度 | 20% | 新鲜度和增长趋势 |
| 内容质量 | 15% | 标题质量和完整性 |
| 爆款潜力 | 20% | 情绪价值和传播潜力 |

### 🎯 智能选题建议
- ✅ **5种切入角度**：情感共鸣 / 实用干货 / 观点评论 / 数据洞察 / 故事叙事
- ✅ **标题优化**：基于爆款标题公式生成建议
- ✅ **文章结构**：提供完整的内容大纲规划
- ✅ **情绪定位**：匹配目标读者情绪

### 📊 竞品分析
- 🔍 相似话题识别
- 📈 角度分布分析
- 💡 差异化策略建议

### 📈 可视化报告
- 📄 美观的HTML交互报告
- 📊 热度趋势图表（TOP10排行、雷达图）
- ☁️ 关键词云图
- 📤 JSON数据导出

---

## 🚀 快速开始

### 安装依赖

```bash
# 克隆项目
cd wechat-topic-radar

# 安装依赖
pip install -r requirements.txt
```

### 使用方法

#### 1. 完整扫描（推荐）
```bash
python scripts/radar_main.py scan
```

#### 2. 快速扫描
```bash
python scripts/radar_main.py quick
```

#### 3. 分析单个选题
```bash
python scripts/radar_main.py analyze "为什么年轻人都不结婚了？"
```

#### 4. 对比多个选题
```bash
python scripts/radar_main.py compare "标题1" "标题2" "标题3"
```

---

## 📖 使用示例

### 完整扫描输出

```bash
$ python scripts/radar_main.py scan

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
   3. [小红书] 职场新人必看的10个建议... (热度: 87.1)
   4. [知乎] 揭秘大厂裁员背后的真相... (热度: 85.6)
   5. [微博] 这届年轻人的消费观变了... (热度: 84.2)

📁 输出文件:
   • ./data/reports/topic_radar_report_20240115_093015.html
   • ./data/topic_data_20240115_093015.json
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

# 分析单个选题
analysis = radar.analyze_topic("为什么年轻人都不结婚了？")
print(f"推荐标题: {analysis.angles[0]['suggested_title']}")
print(f"切入角度: {analysis.angles[0]['type']}")
print(f"文章结构: {' → '.join(analysis.angles[0]['structure'])}")
```

---

## 📊 报告预览

生成的HTML报告包含：

### 1. 数据概览
- 采集热点数、覆盖平台数
- 平均热度分、关键词数量

### 2. 可视化图表
- **TOP10热度排行** - 横向条形图
- **平台分布** - 环形图
- **热度维度雷达图** - 多维度对比
- **关键词云图** - 热门词汇

### 3. 选题推荐
- 🔥 **当下最热** - 立即跟进
- 💎 **高潜力** - 提前布局
- 💡 **被低估** - 差异化机会

### 4. 深度分析
- 切入角度建议
- 竞品分析
- 差异化策略
- 内容规划

---

## ⚙️ 配置说明

编辑 `config/config.yaml` 自定义配置：

```yaml
# 扫描平台
data_collection:
  platforms:
    - zhihu
    - weibo
    - xiaohongshu
    - wechat
  limit_per_platform: 50

# 热度算法权重
heat_algorithm:
  min_heat_score: 50
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

## 📁 项目结构

```
wechat-topic-radar/
├── SKILL.md                    # Skill定义文件
├── README.md                   # 项目说明
├── requirements.txt            # Python依赖
├── clawhub.json               # ClawHub配置
├── LICENSE                    # 许可证
├── config/
│   └── config.yaml            # 配置文件
├── scripts/
│   ├── radar_main.py          # 主控模块 ⭐入口
│   ├── enhanced_collector.py  # 增强版数据采集 (20+平台)
│   ├── heat_algorithm.py      # 热度算法
│   ├── topic_analyzer.py      # 选题分析
│   └── report_generator.py    # 报告生成
├── data/                      # 数据存储
│   └── reports/              # 报告输出
└── assets/                    # 静态资源
```

---

## 🛠️ 技术栈

- **Python 3.8+** - 核心语言
- **requests** - 网络数据采集
- **jieba** - 中文分词和关键词提取
- **numpy** - 数值计算
- **plotly** - 交互式可视化
- **pyyaml** - 配置管理

---

## 📝 数据来源

| 平台 | 数据类型 | 更新频率 |
|:---|:---|:---|
| 知乎 | 热榜话题 | 实时 |
| 微博 | 热搜榜单 | 实时 |
| 小红书 | 热门搜索 | 实时 |
| 公众号 | 热门文章 | 定时采集 |

---

## ⚠️ 注意事项

1. **数据准确性**：网络数据采集可能存在延迟或波动
2. **合规使用**：请遵守各平台的数据使用规范
3. **热点时效**：热点内容具有时效性，建议及时跟进
4. **人工判断**：算法建议仅供参考，最终选题需结合人工判断

---

## 🗺️ 更新计划

- [ ] 接入更多数据源（抖音、B站等）
- [ ] AI智能标题生成
- [ ] 历史热点趋势分析
- [ ] 个性化推荐算法
- [ ] 定时自动推送报告

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👤 作者

- **作者**: liujian
- **邮箱**: sxzxlj@163.com
- **版本**: 1.0.0

---

## 💬 反馈与支持

如有问题或建议，欢迎通过以下方式联系：
- 📧 邮箱: sxzxlj@163.com
- 💬 Issue: 提交GitHub Issue

如果这个项目对你有帮助，请给个 ⭐ Star！
