# 简历生成模板参考

## 空模板（可复制修改）

```json
{
  "id": "cm9[随机字符]",
  "name": "姓名 - 职位",
  "slug": "name-position",
  "picture": {
    "hidden": true,
    "url": "",
    "size": 80,
    "rotation": 0,
    "aspectRatio": 1,
    "borderRadius": 0,
    "borderColor": "rgba(0, 0, 0, 0.5)",
    "borderWidth": 0,
    "shadowColor": "rgba(0, 0, 0, 0.5)",
    "shadowWidth": 0
  },
  "basics": {
    "name": "",
    "headline": "",
    "email": "",
    "phone": "",
    "location": "",
    "website": { "url": "", "label": "" },
    "customFields": []
  },
  "summary": {
    "title": "个人简介",
    "columns": 1,
    "hidden": false,
    "content": "<p></p>"
  },
  "sections": {
    "profiles": { "title": "社交链接", "columns": 1, "hidden": true, "items": [] },
    "experience": {
      "title": "工作经历",
      "columns": 1,
      "hidden": false,
      "items": []
    },
    "education": {
      "title": "教育背景",
      "columns": 1,
      "hidden": false,
      "items": []
    },
    "projects": {
      "title": "项目经历",
      "columns": 1,
      "hidden": false,
      "items": []
    },
    "skills": {
      "title": "技能",
      "columns": 1,
      "hidden": false,
      "items": []
    },
    "languages": {
      "title": "语言",
      "columns": 1,
      "hidden": false,
      "items": []
    },
    "certifications": {
      "title": "证书",
      "columns": 1,
      "hidden": false,
      "items": []
    },
    "interests": { "title": "兴趣爱好", "columns": 1, "hidden": true, "items": [] },
    "awards": { "title": "获奖", "columns": 1, "hidden": true, "items": [] },
    "publications": { "title": "出版物", "columns": 1, "hidden": true, "items": [] },
    "volunteer": { "title": "志愿经历", "columns": 1, "hidden": true, "items": [] },
    "references": { "title": "推荐人", "columns": 1, "hidden": true, "items": [] }
  },
  "customSections": [],
  "metadata": {
    "template": "azurill",
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
        "fontFamily": "Noto Sans SC",
        "fontWeights": ["400", "500"],
        "fontSize": 10,
        "lineHeight": 1.5
      },
      "heading": {
        "fontFamily": "Noto Sans SC",
        "fontWeights": ["600"],
        "fontSize": 14,
        "lineHeight": 1.5
      }
    },
    "notes": ""
  },
  "createdAt": "[当前时间 ISO]",
  "updatedAt": "[当前时间 ISO]"
}
```

---

## 主题配色参考

| 模板 | Primary Color |
|------|---------------|
| azurill | rgba(16, 185, 129, 1) — 绿色 |
| pikachu | rgba(250, 204, 21, 1) — 黄色 |
| gengar | rgba(139, 92, 246, 1) — 紫色 |
| onyx | rgba(255, 255, 255, 1) — 白色 |
| bronzor | rgba(180, 83, 9, 1) — 棕色 |
| chikorita | rgba(34, 197, 94, 1) — 亮绿 |

---

## 字体推荐

| 字体 | 风格 |
|------|------|
| Noto Sans SC | 中文默认，清晰易读 |
| IBM Plex Serif | 商务专业感 |
| Inter | 现代简约 |
| Source Han Sans CN | 思源黑体 |

---

## HTML 描述格式

工作经历描述示例：

```html
<ul>
  <li>主导 XX 项目，服务 XX 用户</li>
  <li>优化性能，提升 XX%</li>
  <li>带领 X 人团队完成交付</li>
</ul>
```

项目描述示例：

```html
<p>基于 XX 技术，实现 XX 功能。GitHub XX Stars。</p>
```
