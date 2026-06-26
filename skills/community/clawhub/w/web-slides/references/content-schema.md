# Content Schema

## Goal

给 `generate-slide-html.mjs` 提供结构化输入，避免每次都从零拼文案。

## Usage

传入：

- `--content path/to/deck.json`

也可以先用 markdown 提纲转换：

- `node scripts/markdown-to-content.mjs --input examples/investor-pitch.md --output examples/investor-pitch.json --scene investor-pitch --mobile`

内容文件应为 JSON，推荐结构：

```json
{
  "title": "Investor Pitch",
  "subtitle": "AI-native workflow platform",
  "scene": "investor-pitch",
  "density": "medium",
  "mobile": true,
  "slides": [
    {
      "layout": "cover",
      "eyebrow": "Series A",
      "title": "Building the AI Operating Layer",
      "subtitle": "From fragmented agents to one production system"
    },
    {
      "layout": "agenda",
      "title": "Today",
      "points": ["Problem", "Product", "Traction", "Roadmap"]
    },
    {
      "layout": "insight",
      "title": "Teams lose time across disconnected AI workflows",
      "points": [
        "Prompts, files, and approvals live in separate tools",
        "Operations lack visibility and governance",
        "Teams cannot scale agent workflows reliably"
      ],
      "stat": "63%",
      "statLabel": "time wasted in coordination"
    }
  ]
}
```

## Supported Layout Fields

### `cover`

- `eyebrow`
- `title`
- `subtitle`

### `agenda`

- `title`
- `points[]`

### `section-break`

- `title`
- `subtitle`

### `insight`

- `title`
- `points[]`
- `stat`
- `statLabel`

### `two-column`

- `title`
- `leftTitle`
- `leftPoints[]`
- `rightTitle`
- `rightPoints[]`

### `metrics`

- `title`
- `metrics[]`
  - `value`
  - `label`

### `chart-focus`

- `title`
- `chartBars[]`
  - `label`
  - `value`
- `conclusion`

### `timeline`

- `title`
- `steps[]`

### `comparison`

- `title`
- `leftTitle`
- `leftPoints[]`
- `rightTitle`
- `rightPoints[]`

### `quote`

- `title`
- `subtitle`

### `closing`

- `title`
- `subtitle`

## Recommendation

如果用户先给的是长讲稿，先整理成这个 JSON 结构，再交给生成器脚本。这样更稳、更省 token，也更容易保证页面质量。
