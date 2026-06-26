# 微信公众号写作技能 - 技术架构详解

## 📋 项目概述

这是一个完整的微信公众号文章写作与发布系统，支持从话题输入到草稿推送的全流程自动化。

**核心能力：**
- 两种写作模式（自动/指定主题）
- 五套精美排版主题
- 智能主题推荐
- 内容验证与搜索
- 封面自动生成
- 一键推送草稿

---

## 🏗️ 技术架构

### 1. 核心模块

```
┌─────────────────────────────────────────────────────────────┐
│                    微信公众号写作技能                          │
├─────────────────────────────────────────────────────────────┤
│  用户界面层                                                    │
│  ├── write_article.py      # 主入口，两种写作模式              │
│  ├── push_draft.py         # 推送草稿到公众号                  │
│  └── generate_cover.py     # 封面生成工具                      │
├─────────────────────────────────────────────────────────────┤
│  业务逻辑层                                                    │
│  ├── outline_generator.py  # 大纲生成器                       │
│  ├── html_writer.py        # HTML写作器                       │
│  ├── content_validator.py  # 内容验证器                       │
│  └── markdown_to_wechat_html.py  # 主题系统                   │
├─────────────────────────────────────────────────────────────┤
│  基础设施层                                                    │
│  ├── 微信公众号 API (access_token, draft)                     │
│  ├── 封面图片上传接口                                          │
│  └── 文件存储系统                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 依赖的开源项目

### 1. **微信公众号 API**
- **来源：** 微信官方
- **功能：** 获取 access_token、上传封面图片、创建草稿
- **接口：**
  - `GET /cgi-bin/token` - 获取访问令牌
  - `POST /cgi-bin/media/uploadimg` - 上传封面图片
  - `POST /draft/add` - 创建图文草稿

### 2. **html2canvas** (封面生成)
- **版本：** 1.4.1
- **来源：** https://html2canvas.hertzen.com/
- **功能：** 将 HTML/CSS 渲染为 Canvas，再导出为 PNG
- **用途：** 生成 900×383 的公众号封面图
- **特点：**
  - 纯前端实现，无需后端
  - 支持 CSS3 渐变、阴影等效果
  - 2x 高清导出

### 3. **FileSaver.js** (文件下载)
- **版本：** 2.0.5
- **来源：** https://github.com/eligrey/FileSaver.js
- **功能：** 浏览器端文件保存
- **用途：** 自动下载生成的封面图片

### 4. **Python 标准库**
- `urllib.request` - HTTP 请求
- `json` - JSON 数据处理
- `re` - 正则表达式
- `os` / `pathlib` - 文件系统操作
- `argparse` - 命令行参数解析

---

## 🎨 五套排版主题

### 主题设计哲学

| 主题 | 配色方案 | 适用场景 | 设计特点 |
|------|----------|----------|----------|
| **极简商务** | 蓝黑 #1a1a2e + #0984e3 | 商业、职场、管理 | 专业稳重，底部边框 |
| **温暖文艺** | 米金 #8b6914 + #fdf8f0 | 生活、情感、读书 | 柔和温馨，居中标题 |
| **科技现代** | 深色 #0d1117 + #58a6ff | 技术、编程、数码 | GitHub 风格，代码高亮 |
| **活泼清新** | 多彩 #ff6b6b + #4ecdc4 | 美食、旅行、生活方式 | 年轻活力，大圆角 |
| **杂志高级** | 黑白 #1a1a1a + #c0a080 | 时尚、艺术、深度阅读 | 精致留白，设计感强 |

### 主题实现方式

采用 **CSS-in-Python** 架构：

```python
THEME_PRESETS = {
    'minimal_business': {
        'name': '极简商务',
        'colors': {
            'primary': '#1a1a2e',
            'accent': '#0984e3',
            'background': '#ffffff',
            'text': '#2c3e50'
        },
        'typography': {
            'h1': {'font-size': '20px', 'border-bottom': '2px solid #1a1a2e'},
            'h2': {'border-left': '3px solid #0984e3'},
            'blockquote': {'border-left': '3px solid #0984e3'}
        }
    }
    # ... 其他主题
}
```

---

## 🔄 完整工作流程

### 模式一：自动写作

```
用户输入话题
    ↓
[1] 分析话题类型（关键词匹配）
    ↓
[2] 生成搜索查询（内容验证器）
    ↓
[3] 生成文章大纲（大纲生成器）
    ├── 选择文章类型模板
    ├── 分配各章节字数
    └── 提取关键点
    ↓
[4] 自动写作内容（AI生成）
    ├── 引言部分
    ├── 背景介绍
    ├── 核心内容
    ├── 实践案例
    └── 总结展望
    ↓
[5] 转换为 HTML（HTML写作器）
    ├── 应用主题样式
    ├── 添加背景色块
    └── 添加页脚
    ↓
[6] 内容验证（内容验证器）
    ├── 识别事实性陈述
    ├── 生成搜索查询
    └── 标记需核实内容
    ↓
[7] 保存文件
    ├── HTML 文件
    └── JSON 大纲
    ↓
[8] 推送草稿（可选）
    ├── 上传封面
    ├── 创建草稿
    └── 返回 Media ID
```

### 模式二：指定主题写作

```
用户输入话题 + 要求
    ↓
[1] 确认写作需求
    ↓
[2] 生成大纲（可交互修改）
    ↓
[3] 分段写作（每段可确认）
    ├── 第1部分：引言
    ├── 第2部分：背景
    ├── ...
    └── 第N部分：总结
    ↓
[4-8] 同自动模式
```

---

## 🧠 核心算法

### 1. 话题类型分析

```python
def analyze_topic(self, topic: str) -> Tuple[str, float]:
    """
    基于关键词匹配分析话题类型
    
    类型优先级：
    1. 技术文章 - AI、编程、代码、算法
    2. 商业分析 - 商业、职场、管理、战略
    3. 生活随笔 - 生活、情感、读书、故事
    4. 教程指南 - 教程、指南、步骤、如何
    5. 产品评测 - 评测、测评、体验、开箱
    """
    keywords = {
        'tech': ['技术', '编程', '代码', '开发', 'AI', '算法'],
        'business': ['商业', '职场', '管理', '战略', '分析'],
        'life': ['生活', '情感', '读书', '故事', '随笔'],
        'tutorial': ['教程', '指南', '步骤', '如何', '怎么'],
        'review': ['评测', '测评', '体验', '开箱', '推荐']
    }
    # 计算匹配度，返回最佳类型
```

### 2. 大纲生成算法

```python
def generate_outline(self, topic: str, word_count: int, 
                     article_type: str) -> Dict:
    """
    基于模板生成结构化大纲
    
    技术文章模板：
    - 引言(10%) → 背景(15%) → 核心内容(40%) → 实践案例(20%) → 总结展望(15%)
    
    商业分析模板：
    - 现象描述(10%) → 背景分析(20%) → 深度解读(35%) → 案例支撑(20%) → 趋势判断(15%)
    
    生活随笔模板：
    - 开篇引入(10%) → 个人经历(25%) → 深入探讨(35%) → 实用建议(20%) → 结语感悟(10%)
    """
    template = self.TEMPLATES[article_type]
    sections = []
    for section in template['sections']:
        section_words = int(word_count * section['ratio'])
        sections.append({
            'title': section['title'],
            'word_count': section_words,
            'key_points': self._generate_key_points(topic, section['title'])
        })
```

### 3. 智能主题推荐

```python
def recommend_theme(self, topic: str) -> Tuple[str, float]:
    """
    基于关键词匹配推荐最佳主题
    
    匹配规则：
    - 商业关键词 → minimal_business
    - 生活关键词 → warm_artistic
    - 技术关键词 → tech_modern
    - 美食/旅行 → fresh_lively
    - 时尚/艺术 → magazine_premium
    
    返回：(主题名, 置信度)
    """
    scores = {}
    for theme, keywords in THEME_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in topic)
        scores[theme] = score / len(keywords)
    
    best_theme = max(scores, key=scores.get)
    confidence = scores[best_theme]
    
    if confidence < 0.1:
        return 'minimal_business', 0.0  # 默认主题
    return best_theme, confidence
```

### 4. 内容验证算法

```python
def identify_facts(self, content: str) -> List[str]:
    """
    识别内容中需要验证的事实性陈述
    
    识别模式：
    - 数字+单位："100万用户"、"50%增长"
    - 时间点："2024年"、"去年"
    - 专有名词：公司名、产品名
    - 比较级："第一"、"最大"、"领先"
    """
    patterns = [
        r'\d+[万亿]?\s*[元美元户次]',
        r'\d{4}\s*年',
        r'第[一二三四五]|第一|最大|领先'
    ]
    facts = []
    for pattern in patterns:
        matches = re.findall(pattern, content)
        facts.extend(matches)
    return facts

def generate_search_queries(self, topic: str, article_type: str) -> List[str]:
    """
    为话题生成搜索查询
    
    生成策略：
    1. 基础查询：话题本身
    2. 时效查询：话题 + 最新/2024/2025
    3. 类型查询：话题 + 技术趋势/市场分析
    """
    queries = [topic]
    queries.append(f"{topic} 最新")
    queries.append(f"{topic} 2024 2025")
    
    type_keywords = {
        'tech': '技术趋势',
        'business': '市场分析',
        'life': '生活感悟',
        'tutorial': '教程指南',
        'review': '评测体验'
    }
    queries.append(f"{topic} {type_keywords.get(article_type, '')}")
    
    return queries[:5]
```

---

## 📱 移动端排版优化

### 核心原则

1. **避免 margin 叠加**
   ```css
   /* 错误：上下边距会叠加 */
   p { margin: 20px 0; }
   
   /* 正确：只设底部边距 */
   p { margin: 0 0 16px 0; }
   ```

2. **紧凑间距**
   - 段间距：16px
   - 标题边距：24px/20px
   - 引用块内边距：12-16px

3. **字体大小**
   - 正文：15-16px
   - H1：19-22px
   - H2：16-18px
   - 引用：14-15px
   - 代码：13px

4. **背景色块**
   - 使用 `section` 包裹整篇文章
   - 渐变背景增加视觉层次
   - 内容区使用半透明白色背景

---

## 🚀 使用方法

### 1. 自动写作

```bash
# 快速生成文章
python3 scripts/write_article.py "人工智能发展趋势"

# 指定字数
python3 scripts/write_article.py "人工智能发展趋势" --words 2000
```

### 2. 指定主题写作

```bash
# 精细控制
python3 scripts/write_article.py "咖啡文化" --mode guided --style life --words 1500
```

### 3. 推送草稿

```bash
# 自动推荐主题
python3 scripts/push_draft.py --file _drafts/文章.html --title "文章标题"

# 指定主题
python3 scripts/push_draft.py --file _drafts/文章.html --title "文章标题" --theme warm_artistic

# 查看所有主题
python3 scripts/push_draft.py --list-themes
```

### 4. 生成封面

```bash
# 生成5个主题封面
python3 generate_covers.py

# 用浏览器打开下载
open cover_minimal.html
```

---

## 📁 文件结构

```
mp-wechat/
├── scripts/
│   ├── write_article.py           # 主写作流程
│   ├── outline_generator.py       # 大纲生成器
│   ├── html_writer.py             # HTML写作器
│   ├── content_validator.py       # 内容验证器
│   ├── markdown_to_wechat_html.py # 主题系统
│   ├── push_draft.py              # 推送草稿
│   └── update_draft.py            # 更新草稿
├── _drafts/                       # 草稿目录
│   ├── theme-demo-*.html          # 主题演示
│   └── *.json                     # 大纲文件
├── images/
│   └── cover.jpg                  # 默认封面
├── cover_*.html                   # 封面生成器
├── generate_covers.py             # 批量生成封面
├── THEMES_GUIDE.md                # 主题使用指南
├── WORKFLOW_DESIGN.md             # 工作流设计文档
└── SKILL_OVERVIEW.md              # 本文件
```

---

## 🔮 未来扩展

### 计划功能

1. **AI 写作集成**
   - 接入 Claude/GPT API 实现真正的自动写作
   - 流式输出，实时生成内容

2. **图片搜索与插入**
   - 根据内容自动搜索配图
   - 支持 Unsplash/Pexels 等图库

3. **数据分析**
   - 阅读量、点赞数统计
   - 最佳发布时间推荐

4. **多平台支持**
   - 知乎、今日头条同步
   - 一键多平台发布

5. **协作功能**
   - 多人编辑
   - 评论批注
   - 版本历史

---

## 📝 技术栈总结

| 层级 | 技术 | 用途 |
|------|------|------|
| 前端 | HTML5 + CSS3 | 封面生成、样式渲染 |
| 前端 | html2canvas 1.4.1 | Canvas 转 PNG |
| 后端 | Python 3.8+ | 业务逻辑 |
| API | 微信公众号 API | 草稿推送 |
| 存储 | 本地文件系统 | 文章存储 |
| 部署 | 命令行工具 | 本地运行 |

---

**Made with 🐾 by 小爪**

*小爪制作，需要审核*
