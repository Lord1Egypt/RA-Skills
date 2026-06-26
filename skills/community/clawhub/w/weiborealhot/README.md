# 微博热搜技能 - Weibo Hot Search Skill 📱

## 🎯 功能概述

这是一个通过浏览器自动化技术实时抓取微博热搜的 Python 技能。支持四大分类（实时、生活、文娱、社会），可灵活配置运行模式，适用于舆情监控、热点追踪等场景。

---

## 📦 文件结构

```
weibo-hot-search/
├── SKILL.md              # 技能文档（OpenClaw 格式）
├── scripts/
│   └── weibo_hot_search.py  # Python 核心脚本
└── README.md             # 本说明文档
```

---

## 🚀 快速开始

### 方法一：通过 OpenClaw WebSearch（推荐）

在 OpenClaw 中使用 web-search 技能，系统会自动识别并调用对应功能。

**示例查询：**
- `weibo hot search life category` - 获取生活类热搜
- `weibo hot search real-time` - 获取实时热搜

### 方法二：直接运行 Python 脚本

```bash
# 安装依赖（首次使用）
pip install selenium webdriver-manager

# 获取生活类热搜
python scripts/weibo_hot_search.py --category life

# 获取实时热搜（JSON 格式输出）
python scripts/weibo_hot_search.py --category 实时 --json

# 指定自定义 URL
python scripts/weibo_hot_search.py --url https://s.weibo.com/top/summary?cate=entrank

# 显示浏览器界面（便于调试）
python scripts/weibo_hot_search.py --no-headless
```

---

## 📋 参数说明

### 命令行参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--category` | 指定热搜分类 | - | `life`, `realtimehot`, `entrank`, `socialevent` |
| `--url` | 直接指定 URL | - | `https://s.weibo.com/top/summary?cate=life` |
| `--headless` | 无头模式 | `True` | `-` |
| `--no-headless` | 显示浏览器界面 | - | `-` |
| `--json` | JSON 格式输出 | text | `-` |
| `--help` | 显示帮助信息 | - | `-` |

### 支持的热搜分类

| 中文名称 | 英文代码 | URL 参数 | 说明 |
|---------|---------|---------|------|
| 实时 | realtimehot | realtimehot | 当前最热门话题 |
| 生活 | life | life | 生活方式、民生热点 |
| 文娱 | entrank | entrank | 娱乐新闻、明星八卦 |
| 社会 | socialevent | socialevent | 社会事件、公共议题 |

---

## 💡 使用场景

### 1. 舆情监控系统
```python
import requests
from scripts.weibo_hot_search import get_weibo_hot_search

def monitor_social_sentiment():
    """监控社会类热搜，分析舆情走向"""
    result = get_weibo_hot_search("https://s.weibo.com/top/summary?cate=socialevent")
    
    if result['code'] == 200:
        hot_topics = [item for item in result['data'] if '争议' in item['title']]
        print(f"发现争议话题：{hot_topics}")

# 定时调用（如每小时一次）
while True:
    monitor_social_sentiment()
```

### 2. 娱乐资讯平台
```python
def get_entertainment_trends():
    """获取文娱类热搜，用于内容推荐"""
    url = "https://s.weibo.com/top/summary?cate=entrank"
    result = get_weibo_hot_search(url)
    
    # 提取影视相关话题
    movies = [item for item in result['data'] if '电影' in item['title'] or '剧' in item['title']]
    return movies[:10]  # 取前 10 条

# 调用示例
entertainment_trends = get_entertainment_trends()
for trend in entertainment_trends:
    print(f"🎬 {trend['title']} (热度：{trend['hot']})")
```

### 3. 生活趋势分析
```python
def analyze_lifestyle_topics():
    """分析生活方式类热门话题"""
    result = get_weibo_hot_search("https://s.weibo.com/top/summary?cate=life")
    
    # 统计各类目出现频率
    categories = {}
    for item in result['data']:
        if '健康' in item['title']:
            categories['health'] += 1
        elif '美食' in item['title']:
            categories['food'] += 1
            
    print("生活趋势分析:", categories)
```

---

## 🛠️ 技术实现细节

### 浏览器配置
- **默认**: Microsoft Edge（Windows）/ Chrome（跨平台）
- **无头模式**: `True`（适合服务器部署）
- **反检测措施**: 
  - Disable AutomationControlled features
  - Add excludeSwitches configuration

### 数据获取流程
1. 初始化浏览器实例
2. 访问指定热搜 URL
3. 等待页面加载完成（最长 10 秒）
4. 提取标题和热度值
5. 返回结构化 JSON 数据

### 容错机制
- **超时处理**: 10 秒自动终止并返回友好错误信息
- **网络异常**: 识别连接失败，提供针对性提示
- **元素未找到**: 尝试备用选择器，最后返回空结果而非崩溃

---

## ⚙️ OpenClaw 集成方式

### 作为 web-search 技能使用

在 OpenClaw 中调用时，系统会自动解析查询并匹配对应功能：

```python
from openclaw import WebSearch

search = WebSearch()

# 用户输入："我想看看生活类的微博热搜"
result = search.query("weibo hot search life category")

# 系统识别关键词 "life", "category" → 自动调用 dict['生活'] URL
print(result)
```

### Skill Metadata (SKILL.md)

技能文档已配置，包含：
- 功能描述
- 使用示例
- API 规范
- 部署说明

OpenClaw 会自动读取 `SKILL.md` 并匹配相关查询。

---

## 📊 返回数据格式

### JSON 输出（标准格式）

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "title": "热搜词条名称",
      "hot": "12345678"
    },
    ...
  ]
}
```

### 人类可读格式输出

```
============================================================
微博热搜 - 生活分类
============================================================
1. 春节假期旅游热度创新高 [热度:987654]
2. 健康饮食新趋势 [热度:876543]
3. 智能家居产品推荐 [热度:765432]
...
============================================================
```

---

## 🎯 性能指标

| 项目 | 数值/说明 |
|------|----------|
| **响应时间** | 8-15 秒（含浏览器启动） |
| **数据量** | 每次约 20-30 条热搜词条 |
| **并发能力** | 单进程，建议串行调用 |
| **内存占用** | ~150MB (Chrome/Edge) |

---

## ⚠️ 注意事项

### 使用限制

1. **网络环境**: 必须能访问微博网站（中国大陆）
2. **IP 频率**: 避免短时间高频调用，防止 IP 被封
3. **反爬机制**: 
   - 建议定期更换 User-Agent
   - 考虑使用代理服务器
   - 控制请求间隔（建议 >60 秒）

### 代码维护

1. **页面结构变化**: 微博改版后需调整选择器
2. **依赖更新**: Selenium API 升级可能影响代码
3. **浏览器版本**: 定期更新 Edge/Chrome 保持兼容

---

## 🔄 常见问题 (FAQ)

**Q: 如何获取所有分类的热搜？**  
A: 分别调用四次，或使用循环脚本批量获取。

**Q: 为什么返回空数据？**  
A: 
- 检查网络连接
- 确认 URL 正确性
- 查看浏览器控制台是否有错误信息

**Q: 能否指定某条热搜的排名位置？**  
A: 当前版本不支持，可修改代码添加 `limit` 参数。

**Q: 如何保存结果到文件？**  
A: 使用 JSON 输出模式并重定向：
```bash
python scripts/weibo_hot_search.py --category life --json > hotsearch.json
```

---

## 📞 技术支持

- **作者**: Kimi (金米) 📈
- **版本**: v1.0
- **更新时间**: 2026-03-27
- **依赖**: Python 3.7+ + Selenium + webdriver-manager

如有问题，请查看：
- [微博热搜官网](https://s.weibo.com/top/summary)
- [Selenium 文档](https://www.selenium.dev/documentation/)

---

**最后提醒**: 本脚本仅供学习和研究使用，请勿用于恶意爬取或商业用途。📈
