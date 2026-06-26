---
name: read-it-later
description: Save and retrieve "read it later" content - links, articles, notes, and ideas for future reference. Use when the user wants to (1) save a link, URL, article, or note to read later, (2) retrieve previously saved content, (3) list or search their saved read-later items, or (4) organize their reading list. Works with a markdown-based storage system. Trigger keywords include "read it later", "RIL", "稍后阅读", "保存链接", "阅读列表", "我的待读".
---

# Read It Later

帮助用户保存和调取稍后阅读的内容。

## 核心功能

### 1. 保存内容

当用户想要保存内容时：

1. 读取 `read-it-later.md` 文件（如果不存在则创建）
2. 将新内容按格式追加到文件中

**存储格式：**
```markdown
## [类别标签] 标题/摘要

- **来源**: URL 或来源说明
- **添加时间**: YYYY-MM-DD HH:mm
- **状态**: 未读 / 已读 / 归档

内容摘要或用户备注...

---
```

**支持的输入类型：**
- URL/链接
- 文章标题 + 链接
- 纯文本笔记/想法
- 图片/文件（保存路径或描述）

### 2. 调取内容

当用户想要查看已保存的内容时：

1. 读取 `read-it-later.md`
2. 根据用户需求筛选：
   - 按状态筛选（未读/已读/全部）
   - 按标签筛选
   - 按日期范围筛选
   - 关键词搜索

### 3. 更新状态

支持标记内容状态：
- `未读` → `已读`
- 移动到 `归档`

## 文件位置

默认存储位置：`~/read-it-later.md`

如果工作区中有 `read-it-later.md`，优先使用工作区内的文件。

## 使用示例

**保存：**
- "帮我保存这个链接 https://example.com/article"
- "记一下：稍后看这篇关于AI的文章"
- "read it later: 设计系统最佳实践"

**调取：**
- "我保存的链接有哪些？"
- "显示我的稍后阅读列表"
- "找出关于[标签]的内容"
- "标记这篇文章为已读"

## 工作流程

### 保存内容

1. 确定文件路径（工作区或用户目录）
2. 读取现有内容
3. 解析用户输入，提取：
   - URL（如果有）
   - 标题/描述
   - 标签（用户指定或自动推断）
4. **如果是 URL：自动抓取内容并打标签**
   - 使用 kimi_fetch 获取网页内容
   - 分析内容主题
   - 自动选择最匹配的标签（从预定义标签中选择）
   - 提取或生成标题
5. 按格式追加新条目
6. 保存文件
7. 确认保存成功，显示自动识别的标签

### 自动标签规则

预定义标签：
- `#ai` - 人工智能、机器学习、大模型相关内容
- `#yc-combinator` - YC、创业、融资相关内容
- `#podcast` - 播客、音频内容
- `#技术` - 编程、开发、工具
- `#设计` - UI/UX、视觉设计
- `#产品` - 产品管理、运营、增长
- `#商业` - 商业分析、行业趋势
- `#待分类` - 无法确定分类时

**自动打标逻辑：**
- 抓取 URL 内容后，分析主题
- 选择 1-2 个最相关的标签
- 如果内容涉及多个领域，选择最主要的
- 无法确定时使用 `#待分类`

### 调取内容

1. 确定文件路径
2. 读取文件内容
3. 根据筛选条件解析条目
4. 格式化输出给用户

### 更新状态

1. 读取文件
2. 定位目标条目
3. 修改状态字段
4. 保存文件
