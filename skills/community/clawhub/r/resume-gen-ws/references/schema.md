---
title: Reactive Resume Schema v2.0
description: 简历 JSON 生成器完整规范，将任意简历数据转换为 Reactive Resume 标准 JSON 格式
tags: [skill, resume, reactive-resume, schema]
created: 2026-04-11
source: https://rxresu.me
version: 2.0.0
---

# 简历 JSON 生成器 (完整版) 🎯

> 将任意简历数据转换为 Reactive Resume 完整标准 JSON 格式，包含所有必需字段。

---

## 顶层必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 简历唯一标识符（UUID格式） |
| `name` | string | 简历显示名称（封面标题） |
| `slug` | string | URL友好标识（小写，用-连接） |
| `picture` | object | 头像配置 |
| `basics` | object | 基本信息 |
| `summary` | object | 个人简介 |
| `sections` | object | 各版块内容 |
| `customSections` | array | 自定义版块 |
| `metadata` | object | 样式元数据 |
| `createdAt` | string | 创建时间（ISO格式） |
| `updatedAt` | string | 更新时间（ISO格式） |

---

## 完整字段详解

### picture 头像配置

```json
"picture": {
  "hidden": false,
  "url": "",
  "size": 80,
  "rotation": 0,
  "aspectRatio": 1,
  "borderRadius": 0,
  "borderColor": "rgba(0, 0, 0, 0.5)",
  "borderWidth": 0,
  "shadowColor": "rgba(0, 0, 0, 0.5)",
  "shadowWidth": 0
}
```

### basics 基本信息

```json
"basics": {
  "name": "string - 姓名",
  "headline": "string - 职位/头衔",
  "email": "string - 邮箱",
  "phone": "string - 电话",
  "location": "string - 地址",
  "website": { "url": "string", "label": "string" },
  "customFields": []
}
```

### summary 个人简介

```json
"summary": {
  "title": "个人简介",
  "columns": 1,
  "hidden": false,
  "content": "string - HTML格式内容"
}
```

### sections 各版块

```json
"sections": {
  "profiles": { "title": "社交链接", "columns": 1, "hidden": true, "items": [] },
  "experience": { "title": "工作经历", "columns": 1, "hidden": false, "items": [...] },
  "education": { "title": "教育背景", "columns": 1, "hidden": false, "items": [...] },
  "projects": { "title": "项目经验", "columns": 1, "hidden": false, "items": [...] },
  "skills": { "title": "技能", "columns": 1, "hidden": false, "items": [...] },
  "languages": { "title": "语言", "columns": 1, "hidden": false, "items": [...] },
  "certifications": { "title": "证书", "columns": 1, "hidden": false, "items": [...] },
  "interests": { "title": "兴趣爱好", "columns": 1, "hidden": true, "items": [] },
  "awards": { "title": "获奖", "columns": 1, "hidden": true, "items": [] },
  "publications": { "title": "出版物", "columns": 1, "hidden": true, "items": [] },
  "volunteer": { "title": "志愿经历", "columns": 1, "hidden": true, "items": [] },
  "references": { "title": "推荐人", "columns": 1, "hidden": true, "items": [] }
}
```

#### experience 工作经历 item

```json
{
  "id": "uuid",
  "hidden": false,
  "company": "string - 公司名",
  "position": "string - 职位",
  "location": "string - 地点",
  "period": "string - 时间段",
  "website": { "url": "", "label": "" },
  "description": "string - HTML格式描述",
  "roles": []
}
```

#### education 教育背景 item

```json
{
  "id": "uuid",
  "hidden": false,
  "school": "string - 学校名",
  "degree": "string - 学位",
  "area": "string - 专业",
  "grade": "string - 成绩",
  "location": "string - 地点",
  "period": "string - 时间段",
  "website": { "url": "", "label": "" },
  "description": "string"
}
```

#### projects 项目经验 item

```json
{
  "id": "uuid",
  "hidden": false,
  "name": "string - 项目名",
  "period": "string - 时间",
  "website": { "url": "", "label": "" },
  "description": "string - HTML格式"
}
```

#### skills 技能 item

```json
{
  "id": "uuid",
  "hidden": false,
  "icon": "",
  "name": "string - 技能名",
  "proficiency": "string - 熟练度描述",
  "level": "number 0-5",
  "keywords": ["string array"]
}
```

#### languages 语言 item

```json
{
  "id": "uuid",
  "hidden": false,
  "language": "string - 语言名",
  "fluency": "string - 流利度",
  "level": "number 0-5"
}
```

#### certifications 证书 item

```json
{
  "id": "uuid",
  "hidden": false,
  "title": "string - 证书名",
  "issuer": "string - 颁发机构",
  "date": "string - 日期",
  "website": { "url": "", "label": "" },
  "description": "string"
}
```

### metadata 样式配置

```json
"metadata": {
  "template": "azurill | onyx | pikachu | gengar | bronzor | chikorita",
  "layout": {
    "sidebarWidth": 35,
    "pages": [
      {
        "fullWidth": false,
        "main": ["summary", "experience", "education", "projects"],
        "sidebar": ["skills", "certifications", "languages"]
      }
    ]
  },
  "css": { "enabled": false, "value": "" },
  "page": {
    "gapX": 4,
    "gapY": 6,
    "marginX": 14,
    "marginY": 12,
    "format": "a4",
    "locale": "zh-CN",
    "hideIcons": false
  },
  "design": {
    "colors": {
      "primary": "rgba(16, 185, 129, 1)",
      "text": "rgba(0, 0, 0, 1)",
      "background": "rgba(255, 255, 255, 1)"
    },
    "level": { "icon": "star", "type": "circle" }
  },
  "typography": {
    "body": {
      "fontFamily": "IBM Plex Serif",
      "fontWeights": ["400", "500"],
      "fontSize": 10,
      "lineHeight": 1.5
    },
    "heading": {
      "fontFamily": "IBM Plex Serif",
      "fontWeights": ["600"],
      "fontSize": 14,
      "lineHeight": 1.5
    }
  },
  "notes": ""
}
```

---

## 模板列表

| 模板名 | 风格描述 |
|--------|----------|
| `azurill` | 简约现代，适合技术人员 |
| `onyx` | 专业商务，适合传统行业 |
| `pikachu` | 活泼创意，适合设计师 |
| `gengar` | 深色主题，个性鲜明 |
| `bronzor` | 经典稳重，适合高管 |
| `chikorita` | 清新自然，适合应届生 |

---

## 使用步骤

1. 复制上面的 example 内容
2. 修改 `id`/`name`/`slug` 为你的信息
3. 填充 `basics`/`sections` 等数据
4. 保存为 `.json` 文件
5. 在 W简历 中选择 `Reactive Resume (JSON)` 导入

### ⚠️ 重要提示

> 必须包含 `id`/`name`/`slug`/`createdAt`/`updatedAt` 顶层字段，否则封面显示错误。

---

## 常见问题排查

| 问题 | 原因 |
|------|------|
| 封面显示随机名字 | 缺少 `name` 和 `slug` 顶层字段 |
| 导入报错 | 字段名与 schema 不一致 |
| sections 报错 | `sections` 是对象不是数组，每个 section 必须有 `title`/`columns`/`hidden`/`items` |

---

## 相关资源

| 资源 | 链接 |
|------|------|
| Reactive Resume 官网 | https://rxresu.me |
| Reactive Resume Schema | https://rxresu.me/schema.json |
| Kelly Skill 位置 | `~/.openclaw/workspace-kelly/skills/resume-builder/` |

---

_最后更新：2026-04-11_
