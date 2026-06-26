# Xiaohongshu Recommended Templates

Use `list_templates({ platform: "xiaohongshu" })` to browse all available templates. Below are curated recommendations by note type.

## By Note Type

### 种草笔记 (Product Recommendation)
- Search: `list_templates({ platform: "xiaohongshu", q: "product showcase" })`
- Typical variables: `title`, `subtitle`, `product_image`, `bg_color`, `price`
- Style: Magazine or Clean Minimal
- Key element: Product image prominence + clear title

### 测评笔记 (Review)
- Search: `list_templates({ platform: "xiaohongshu", q: "review comparison" })`
- Typical variables: `title`, `product_name`, `rating`, `product_image`
- Style: Clean Minimal or Impact Contrast
- Key element: Rating/score visualization + honest tone

### 教程笔记 (Tutorial)
- Search: `list_templates({ platform: "xiaohongshu", q: "tutorial steps" })`
- Typical variables: `title`, `step_count`, `category_icon`, `bg_color`
- Style: Handwritten Feel or Clean Minimal
- Key element: Step number prominence + clear value promise

### 合集笔记 (Collection/Roundup)
- Search: `list_templates({ platform: "xiaohongshu", q: "collection roundup" })`
- Typical variables: `title`, `item_count`, `images[]`, `bg_color`
- Style: Magazine or Clean Minimal
- Key element: Grid of items + number emphasis

### 对比笔记 (Comparison)
- Search: `list_templates({ platform: "xiaohongshu", q: "comparison before after" })`
- Typical variables: `title`, `left_label`, `right_label`, `left_image`, `right_image`
- Style: Impact Contrast
- Key element: Clear visual split + labels

### 日常分享 (Daily/Lifestyle)
- Search: `list_templates({ platform: "xiaohongshu", q: "lifestyle daily" })`
- Typical variables: `title`, `subtitle`, `main_image`, `accent_color`
- Style: Warm Lifestyle or Handwritten Feel
- Key element: Personal warmth + approachable layout

## Prompt Examples by Category

When no suitable template exists, use AI generation with these prompt patterns:

### 美妆
```
generate_image({
  prompt: "小红书种草封面，粉色柔和色调，标题'油皮亲妈粉底液测评'，副标题'持妆12小时实测'，中央留出圆形产品展示区，杂志风排版，现代无衬线字体",
  platform: "xiaohongshu",
  locale: "zh"
})
```

### 美食
```
generate_image({
  prompt: "小红书教程封面，暖棕色大地色调，标题'5分钟搞定减脂早餐'，手绘风装饰元素，底部三格分步骤预览区域，温暖生活风格",
  platform: "xiaohongshu",
  locale: "zh"
})
```

### 旅行
```
generate_image({
  prompt: "小红书旅行攻略封面，天蓝色和沙色配色，标题'大理7天穷游攻略'，副标题'人均2000全搞定'，顶部大标题+底部景点缩略图网格，干净利落风格",
  platform: "xiaohongshu",
  locale: "zh"
})
```

### 数码
```
generate_image({
  prompt: "小红书测评封面，深蓝灰色科技感，标题'M4 MacBook Pro 真实使用一个月'，左侧产品渲染图区域，右侧评分和关键词标签，极简风格，无衬线粗体字",
  platform: "xiaohongshu",
  locale: "zh"
})
```
