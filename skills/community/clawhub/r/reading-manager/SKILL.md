---
name: reading-manager
description: "Personal reading management system for tracking books, articles, reading progress, notes, and generating reading reports. Use when: (1) recording books and articles to read, (2) tracking reading progr"
version: "1.0.0"
---

# Reading Manager - 阅读管家

个人阅读管理系统，帮助记录书籍、跟踪阅读进度、管理笔记并生成阅读报告。

## 功能特性

### 1. 书籍/文章管理
- 支持 ISBN、URL、手动输入录入书籍
- 自动获取书籍元数据（Google Books API / 豆瓣 API）
- 文章链接收藏与管理
- 多类型支持：书籍、文章、论文、文档

### 2. 阅读进度跟踪
- 页码进度记录
- 百分比进度计算
- 阅读时长统计
- 阅读速度分析

### 3. 阅读笔记
- 高亮记录
- 批注管理
- 标签分类
- Markdown 导出

### 4. 阅读清单
- 想读 (Want to Read)
- 在读 (Currently Reading)
- 已读 (Finished)
- 自定义书单

### 5. 阅读报告
- 月度/年度阅读统计
- 阅读趋势分析
- 书籍类型分布
- 阅读时长报告

### 6. 阅读目标
- 年度阅读目标设定
- 每日/每周阅读提醒
- 目标完成进度追踪

## 安装

```bash
cd ~/.openclaw/workspace/skills/reading-manager
pip install -e .
```

## 使用方法

### 书籍管理

```bash
# 添加书籍（通过 ISBN）
reading book add --isbn 9787115428028

# 添加书籍（手动输入）
reading book add --title "深入理解计算机系统" --author "Randal E. Bryant" --pages 800

# 通过 URL 添加文章
reading book add --url https://example.com/article --type article

# 列出所有书籍
reading book list

# 查看书籍详情
reading book show 1

# 更新书籍信息
reading book update 1 --status reading --rating 5

# 删除书籍
reading book delete 1
```

### 阅读进度

```bash
# 更新阅读进度
reading progress update 1 --page 150
reading progress update 1 --percent 25

# 查看阅读进度
reading progress show 1

# 阅读时长记录
reading progress time 1 --minutes 45

# 阅读历史
reading progress history 1
```

### 阅读笔记

```bash
# 添加笔记
reading note add 1 --content "这是一个重要的概念" --page 120 --tags "important,concept"

# 添加高亮
reading note highlight 1 --content "关键段落" --page 120 --color yellow

# 列出笔记
reading note list 1

# 按标签搜索笔记
reading note search --tag important

# 导出笔记为 Markdown
reading note export 1 --output notes.md
```

### 阅读清单

```bash
# 查看想读列表
reading list want

# 查看在读列表
reading list reading

# 查看已读列表
reading list finished

# 移动书籍到不同列表
reading list move 1 --to finished

# 创建自定义书单
reading list create "技术书单" --description "编程技术相关书籍"
reading list add-book "技术书单" 1
```

### 阅读报告

```bash
# 生成月度报告
reading report monthly 2024-01

# 生成年度报告
reading report yearly 2024

# 阅读统计概览
reading report stats

# 阅读趋势
reading report trend --days 30
```

### 阅读目标

```bash
# 设置年度目标
reading goal set-yearly 50

# 设置月度目标
reading goal set-monthly 4

# 查看目标进度
reading goal status

# 查看历史目标完成情况
reading goal history
```

### 搜索与发现

```bash
# 搜索书籍（在线）
reading search "计算机系统" --source douban
reading search "Clean Code" --source google

# 本地搜索
reading search-local "计算机"

# 按作者搜索
reading search --author "刘瑜"
```

## 数据存储

数据库位置：`~/.config/reading-manager/reading.db`

```bash
# 查看数据库路径
reading data path

# 导出数据
reading data export --format json --output backup.json

# 导入数据
reading data import backup.json
```

## 技术栈

- Python 3.8+
- SQLite 数据存储
- Click (CLI 框架)
- Rich (终端美化)
- requests (API 调用)

## 数据模型

### 书籍表 (books)
```python
{
    id: int
    title: str              # 书名
    subtitle: str           # 副标题
    authors: str            # 作者（JSON 数组）
    isbn10: str
    isbn13: str
    publisher: str          # 出版社
    published_date: str     # 出版日期
    page_count: int         # 总页数
    description: str        # 简介
    cover_url: str          # 封面图片 URL
    categories: str         # 分类（JSON 数组）
    source_type: str        # 来源：book, article, paper
    source_url: str         # 来源 URL
    status: str             # 状态：want, reading, finished
    rating: int             # 评分 1-5
    started_at: str         # 开始阅读时间
    finished_at: str        # 完成时间
    created_at: str
    updated_at: str
}
```

### 阅读进度表 (reading_progress)
```python
{
    id: int
    book_id: int
    current_page: int       # 当前页
    total_pages: int        # 总页数
    percent: float          # 百分比
    minutes_read: int       # 阅读时长（分钟）
    recorded_at: str
    notes: str
}
```

### 笔记表 (notes)
```python
{
    id: int
    book_id: int
    content: str            # 笔记内容
    page: int               # 页码
    note_type: str          # 类型：note, highlight
    highlight_color: str    # 高亮颜色
    tags: str               # 标签（JSON 数组）
    created_at: str
}
```

### 书单表 (lists)
```python
{
    id: int
    name: str               # 书单名称
    description: str        # 描述
    book_ids: str           # 书籍 ID 列表（JSON）
    created_at: str
}
```

### 阅读目标表 (goals)
```python
{
    id: int
    year: int               # 年份
    month: int              # 月份（可选，年度目标为 null）
    target_count: int       # 目标数量
    completed_count: int    # 已完成数量
    created_at: str
}
```
