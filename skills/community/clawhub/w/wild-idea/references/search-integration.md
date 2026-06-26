# 方法B搜索集成

## 搜索优先级

1. **Tavily API**（推荐，绕过所有浏览器反爬）
   脚本路径：`~/.hermes/skills/openclaw-imports/openclaw-tavily-search/scripts/tavily_search.py`
   API key 自动从 `~/.openclaw/.env` 加载。

2. **浏览器备选**（如 Tavily 不可用）
   - DuckDuckGo HTML 版：`browser_navigate("https://html.duckduckgo.com/html/?q=关键词")`
   - Bing：`browser_navigate("https://www.bing.com/search?q=关键词")`

3. **全部失败** → 跳过方法B，标注🚫
   **禁止在搜索失败时用自己的知识推断领域。搜不到就跳过，不猜。**

## 实测用例

| 组合词 | 搜索方式 | 命中 | 提取领域 |
|--------|---------|------|---------|
| 香冻 | Tavily | 食品科学论文 | 食品加工 |
| 矿外 | Tavily | 智慧矿山系统论文 | 工业互联网 |
| 相与 | Tavily | 晋商信任体系 | 传统商业 |
| 铁论 | Tavily | 盐铁论（西汉古籍） | 中国古代政治经济史 |
| 讲选 | Tavily | 艾思奇讲稿选 | 马克思主义哲学教育 |
| 须作 | Tavily | 须佐能乎（火影忍者） | 动漫文化 |
| 除流 | Tavily | GitHub Actions工作流 | CI/CD |
