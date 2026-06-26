# 📱 Weibo Hot Search (微博热搜) - 微博热搜实时获取技能

## 功能描述
通过浏览器自动化技术，实时抓取微博平台各分类下的热门搜索词条。支持实时、生活、文娱、社会四大分类。

## 🌐 支持的分类

- **实时** - 当前最热门的实时热搜话题
- **生活** - 生活方式、民生相关热点
- **文娱** - 娱乐新闻、明星八卦等文化内容
- **社会** - 社会事件、公共议题讨论

## 🔧 使用方法

### 方法一：通过 OpenClaw web_search 工具（推荐）

```python
from openclaw import WebSearch

# 获取微博生活类热搜
search = WebSearch()
result = search.query("weibo hot search life category")
print(result)
```

系统会自动识别关键词并调用对应的 URL：
- "实时" → https://s.weibo.com/top/summary?cate=realtimehot
- "生活" → https://s.weibo.com/top/summary?cate=life
- "文娱" → https://s.weibo.com/top/summary?cate=entrank
- "社会" → https://s.weibo.com/top/summary?cate=socialevent

### 方法二：直接调用 Python 脚本

```python
from weibo_hot_search import get_weibo_hot_search

# 获取生活类热搜
result = get_weibo_hot_search("https://s.weibo.com/top/summary?cate=life")
print(result)
```

## 💡 使用场景示例

1. **实时热点追踪** - 了解当前微博最热门的话题
2. **社会舆情监控** - 分析社会类热搜，把握公共舆论走向
3. **娱乐趋势洞察** - 关注文娱板块，了解明星动态和影视资讯
4. **生活话题挖掘** - 发现民生相关的高关注度事件

## 📋 返回数据格式

```json
{
  "code": 200,
  "message": "成功",
  "data": [
    {
      "title": "热搜词条名称",
      "hot": "12345678"
    },
    ...
  ]
}
```

## ⚙️ 技术参数

- **浏览器**: Microsoft Edge（可配置为 Chrome）
- **模式支持**: 
  - 无头模式 (headless) - 适合服务器环境
  - 有界面模式 - 便于调试和可视化
- **超时时间**: 10 秒
- **数据量**: 每次获取约 20-30 条热搜词条

## 🚀 API 调用示例

```python
import json

# 完整使用流程
if __name__ == "__main__":
    url = "https://s.weibo.com/top/summary?cate=life"  # 生活分类
    
    result = get_weibo_hot_search(url, headless=True)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 🎯 优势特点

1. **多分类支持** - 一次性获取四类热搜数据
2. **灵活配置** - 可开关无头模式，适应不同运行环境
3. **稳定高效** - 使用 WebDriverWait 确保页面加载完成
4. **容错性强** - 完善的异常处理和超时机制
5. **JSON 输出** - 标准化格式，便于程序处理

## ⚠️ 注意事项

1. **网络依赖** - 需要能够访问微博网站的网络环境
2. **反爬虫检测** - 建议定期更换浏览器指纹或使用代理
3. **页面结构变化** - 如微博改版，需及时调整选择器
4. **使用频率** - 避免短时间内高频调用，防止 IP 被封

## 📦 部署说明

技能文件位于：`C:\Users\Administrator\.openclaw\workspace\skills\web-hot-search\`

包含文件：
- `SKILL.md` - 技能文档（本文档）
- `scripts/weibo_hot_search.py` - 核心 Python 脚本
- `README.md` - 使用说明

---

**版本**: v1.0  
**更新日期**: 2026-03-27  
**维护者**: Kimi (金米) 📈
