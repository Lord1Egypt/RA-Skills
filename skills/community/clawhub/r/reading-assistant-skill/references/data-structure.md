# 数据结构定义

本文档定义了读书辅助工具使用的所有数据结构。

## 目录

- [书籍档案结构](#书籍档案结构)
- [摘录数据结构](#摘录数据结构)
- [当前在读信息](#当前在读信息)
- [完整示例](#完整示例)

## 书籍档案结构

每本书的档案存储在独立的 JSON 文件中，路径为 `./reading-notes/books/{书名}.json`。

### 数据模型

```json
{
  "book_info": {
    "title": "string (必需) - 书名",
    "author": "string (可选) - 作者",
    "status": "string (必需) - 阅读状态：reading | completed | archived",
    "created_at": "string (必需) - 创建日期，格式：YYYY-MM-DD",
    "tags": "array (可选) - 书籍级别的标签",
    "cover": "string (可选) - 封面图片URL或路径",
    "isbn": "string (可选) - ISBN编号",
    "publisher": "string (可选) - 出版社",
    "total_pages": "number (可选) - 总页数"
  },
  "excerpts": [
    {
      "id": "string (必需) - 摘录唯一标识",
      "content": "string (必需) - 摘录原文内容",
      "chapter": "string (可选) - 章节信息",
      "tags": "array (可选) - 关键词标签",
      "deep_meaning": "string (可选) - 深层含义分析",
      "application": "string (可选) - 应用建议",
      "created_at": "string (必需) - 创建时间，格式：YYYY-MM-DD HH:MM:SS",
      "source": "string (可选) - 来源：wechat | kindle | manual",
      "page": "number (可选) - 页码",
      "location": "string (可选) - 位置信息（Kindle）",
      "note": "string (可选) - 用户添加的笔记"
    }
  ]
}
```

### 字段说明

#### book_info 对象

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| title | string | 是 | 书名，作为文件名的一部分 |
| author | string | 否 | 作者姓名 |
| status | string | 是 | 阅读状态：reading（在读）、completed（已完成）、archived（已归档） |
| created_at | string | 是 | 创建日期，格式：YYYY-MM-DD |
| tags | array | 否 | 书籍级别的标签，如 ["心理学", "认知科学"] |
| cover | string | 否 | 封面图片URL或本地路径 |
| isbn | string | 否 | ISBN编号 |
| publisher | string | 否 | 出版社名称 |
| total_pages | number | 否 | 总页数 |

#### excerpts 数组元素

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| id | string | 是 | 摘录唯一标识，格式：exc_YYYYMMDDHHMMSS_序号 |
| content | string | 是 | 摘录原文内容 |
| chapter | string | 否 | 章节信息，如"第1章"、"Chapter 1" |
| tags | array | 否 | 关键词标签，如 ["系统1", "认知偏差"] |
| deep_meaning | string | 否 | 深层含义分析，由智能体生成 |
| application | string | 否 | 应用建议，由智能体生成 |
| created_at | string | 是 | 创建时间，格式：YYYY-MM-DD HH:MM:SS |
| source | string | 否 | 来源：wechat（微信读书）、kindle、manual（手动输入） |
| page | number | 否 | 页码 |
| location | string | 否 | 位置信息（Kindle特有） |
| note | string | 否 | 用户添加的个人笔记 |

## 当前在读信息

`current.json` 文件记录当前正在阅读的书籍，方便快速切换。

### 数据模型

```json
{
  "current_book": "string - 当前在读的书名",
  "updated_at": "string - 更新时间，格式：YYYY-MM-DD HH:MM:SS"
}
```

### 示例

```json
{
  "current_book": "思考，快与慢",
  "updated_at": "2024-01-15 10:30:00"
}
```

## 完整示例

### 书籍档案示例

```json
{
  "book_info": {
    "title": "思考，快与慢",
    "author": "丹尼尔·卡尼曼",
    "status": "reading",
    "created_at": "2024-01-01",
    "tags": ["心理学", "认知科学", "决策"],
    "isbn": "978-7-5086-3355-0",
    "publisher": "中信出版社",
    "total_pages": 418
  },
  "excerpts": [
    {
      "id": "exc_20240101100000_0",
      "content": "系统1的运行是无意识且快速的，完全处于自主控制状态，几乎不费脑力。系统2将注意力转移到需要费脑力的大脑活动上来。",
      "chapter": "第1章 一张愤怒的脸和一道乘法题",
      "tags": ["系统1", "系统2", "双系统理论"],
      "deep_meaning": "作者揭示了人类思维的二元结构。系统1负责快速直觉判断，系统2负责慢速理性分析。两者相互配合，但系统2往往懒惰，容易让系统1主导决策。",
      "application": "在重要决策时，刻意激活系统2进行慢思考。可以问自己：我是否过于依赖直觉？有没有足够的证据支持这个判断？",
      "created_at": "2024-01-01 10:00:00",
      "source": "manual",
      "page": 15
    },
    {
      "id": "exc_20240102110000_1",
      "content": "锚定效应：人们在进行判断时，容易受第一印象或第一信息的支配。",
      "chapter": "第11章 锚定效应",
      "tags": ["认知偏差", "锚定效应", "决策陷阱"],
      "deep_meaning": "锚定效应是一种强大的认知偏差。即使我们知道锚点无关，仍然会受其影响。这说明理性思考是多么困难。",
      "application": "在谈判、购物、估值等场景中，警惕锚定效应的影响。主动寻找多个参考点，避免被单一信息主导。",
      "created_at": "2024-01-02 11:00:00",
      "source": "wechat"
    }
  ]
}
```

## 数据验证规则

### 书籍名称

- 不能包含特殊字符：`\ / : * ? " < > |`
- 长度限制：1-100 字符
- 建议格式：中文书名直接使用，英文书名使用原名

### 摘录 ID

- 格式：`exc_YYYYMMDDHHMMSS_序号`
- YYYYMMDDHHMMSS：创建时间戳
- 序号：当日摘录的序号，从 0 开始

### 时间格式

- 日期：`YYYY-MM-DD`（如 2024-01-01）
- 时间：`YYYY-MM-DD HH:MM:SS`（如 2024-01-01 10:00:00）

### 状态值

- `reading`：在读
- `completed`：已完成
- `archived`：已归档

### 来源值

- `wechat`：微信读书
- `kindle`：Kindle 设备或应用
- `manual`：手动输入
- `imported`：批量导入（未指定来源）

## 数据迁移

如果需要从其他笔记工具迁移数据，请：

1. 按照本数据结构创建 JSON 文件
2. 确保 `id` 字段唯一
3. 确保 `created_at` 格式正确
4. 将文件放入 `./reading-notes/books/` 目录

## 注意事项

1. **唯一性**：每条摘录的 `id` 必须唯一，避免重复
2. **时间格式**：严格遵守时间格式，便于统计和排序
3. **标签规范**：标签应简洁明确，避免同义词（如"认知偏差"和"认知偏误"应统一）
4. **编码格式**：所有文件使用 UTF-8 编码
5. **备份**：定期备份 `reading-notes/` 目录
