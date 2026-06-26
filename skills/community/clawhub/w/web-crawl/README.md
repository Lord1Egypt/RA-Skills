# 🕷️ Web Crawl Skill - 深度研究增强工具

## 已实现功能

✅ **多模式内容提取**
- `text` - 纯文本提取
- `markdown` - 完整 Markdown 转换（保留格式）
- `links` - 链接提取
- `structured` - JSON 结构化数据
- `full` - 综合提取

✅ **智能内容识别**
- 自动识别 `main`, `article`, `content` 等主要内容区域
- 自动清理脚本、样式、广告等元素

✅ **完整 HTML → Markdown 转换**
- 标题、段落、链接、图片、列表、表格
- 代码块、引用、分隔线

✅ **并行抓取**
- 同时抓取多个 URL
- 可配置并发数

## 使用方式

### 方法 1: 直接调用 Python 函数

```python
from skills.web-crawl.web_crawl import crawl_url, parallel_crawl

# 抓取单个页面
result = crawl_url(
    url="https://example.com",
    mode="markdown",
    max_length=10000
)
print(result)

# 并行抓取多个页面
result = parallel_crawl(
    urls=["https://site1.com", "https://site2.com"],
    mode="markdown",
    max_length=8000
)
print(result)
```

### 方法 2: 命令行

```bash
cd ~/.openclaw/workspace-main/skills/web-crawl

# 抓取单个 URL
python3 web_crawl.py https://example.com markdown 5000

# 可用模式: text, markdown, links, structured, full
```

### 方法 3: 作为 Agent 工具使用

在对话中，当你需要深度研究时，我会自动使用此工具：

**你**: "研究一下 OpenManus-Max"

**我**:
1. 使用 `web_search` 搜索相关来源
2. 使用 `parallel_crawl` 抓取前 5 个结果
3. 分析、整合、输出研究报告

## 深度研究工作流

```
用户提问
    ↓
[web_search] 搜索多个相关查询
    ↓
[parallel_crawl] 并行抓取 Top URLs
    ↓
[分析] 提取关键信息、对比、整合
    ↓
[输出] 结构化研究报告 + 来源引用
```

## 与 web_fetch 的对比

| 功能 | web_fetch (旧) | web_crawl (新) |
|------|----------------|----------------|
| 提取模式 | 2种 (text/markdown) | 5种 |
| CSS 选择器 | ❌ | ✅ |
| 智能正文识别 | 基础 | 高级 |
| 链接提取 | ❌ | ✅ |
| 结构化数据 | ❌ | JSON 输出 |
| 并行抓取 | ❌ | ✅ |
| 表格转换 | ⚠️ | ✅ 完整支持 |

## 示例输出

### Markdown 模式

```markdown
# Page Title

## Section Heading

This is **bold** and *italic* text.

- List item 1
- List item 2

[Link text](https://example.com)

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
```

### Structured 模式

```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "description": "Meta description",
  "headings": [
    {"level": "h1", "text": "Main Title"},
    {"level": "h2", "text": "Section"}
  ],
  "main_text": "Content preview...",
  "links_count": 42,
  "images_count": 5
}
```

## 安装依赖

```bash
pip3 install requests beautifulsoup4
```

## 文件结构

```
skills/web-crawl/
├── SKILL.md          # Skill 定义文件
├── web_crawl.py      # 核心爬虫实现
├── research.py       # 深度研究工具
├── EXAMPLES.md       # 使用示例
└── README.md         # 本文档
```

---

**现在你可以要求我进行深度研究了！** 🚀
