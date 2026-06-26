---
name: xiaohongshu
description: "Create high-performing Xiaohongshu (Little Red Book / RED) cover images and content graphics. Use when the user mentions: '小红书', 'xiaohongshu', 'RED', '种草', '笔记封面', '小红书图片', '小红书卡片', or wants to create content for the Xiaohongshu platform. Combines platform algorithm knowledge, visual design best practices, and Rendshot image generation."
---

# Xiaohongshu Content Image Generator

Create cover images and content graphics optimized for Xiaohongshu's recommendation algorithm and visual aesthetic standards.

## Workflow

When a user wants to create Xiaohongshu content images:

### Step 1: Understand the Business Context

Ask (if not provided):
- What product/service/topic? (e.g., coffee, skincare, travel)
- What type of note? (种草/测评/教程/合集/日常分享)
- Target audience? (defaults based on category, see [references/algorithm.md](references/algorithm.md))

### Step 2: Apply Algorithm-Aware Design Decisions

Read [references/algorithm.md](references/algorithm.md) for:
- Title formula selection (数字型/疑问型/对比型/紧迫型)
- Cover design patterns that drive click-through
- Content type matching to audience expectations
- Avoid patterns that trigger suppression (敏感词, 过度营销)

### Step 3: Apply Visual Style

Read [references/design-style.md](references/design-style.md) for:
- Style selection based on category (杂志风/手写感/干净利落/对比冲击)
- Color palette by category
- Typography and layout rules
- The 3-second rule for cover stopping power

### Step 4: Generate with Rendshot

**Option A — Use existing template:**
```
list_templates({ platform: "xiaohongshu", q: "<category keyword>" })
get_template({ template_id: "tpl_xxx" })
generate_image({
  template_id: "tpl_xxx",
  variables: { title: "...", ... }
})
```

**Option B — AI generate from prompt:**
```
generate_image({
  prompt: "<detailed design prompt based on Steps 1-3>",
  platform: "xiaohongshu",   // 1080x1440
  locale: "zh"
})
```

The prompt should encode your design decisions:
```
generate_image({
  prompt: "手工皂种草笔记封面，温暖大地色调，中央大标题'三步入门冷制皂'，副标题'新手也能做出专柜级手工皂'，底部产品摆拍留白区域，杂志风排版，衬线标题字体",
  platform: "xiaohongshu",
  locale: "zh"
})
```

**Option C — Wide format:**
```
generate_image({
  prompt: "...",
  platform: "xiaohongshu_wide",  // 1080x810
  locale: "zh"
})
```

### Step 5: Save Good Results

```
create_template({
  name: "手工皂种草封面",
  html: "<returned html>",
  variables: [...],
  platform: "xiaohongshu",
  category: "lifestyle",
  tags: ["handmade", "soap", "tutorial"]
})
```

## Quick Reference

| Dimension | Standard | Wide |
|-----------|----------|------|
| Platform | `xiaohongshu` | `xiaohongshu_wide` |
| Size | 1080x1440 (3:4) | 1080x810 (4:3) |
| Use case | 种草/测评/教程 | 合集/对比/攻略 |

## Design Prompt Construction

When building prompts for Rendshot AI, always include:

1. **Note type**: 种草/测评/教程/合集/日常
2. **Color direction**: Based on category (see design-style.md)
3. **Title text**: Use algorithm-optimized formula (see algorithm.md)
4. **Layout style**: 杂志风/手写感/干净利落/对比冲击
5. **Key visual element**: Product photo area, illustration, or pattern
6. **Typography hint**: Font style preference

## References

- [Algorithm and content strategy](references/algorithm.md) — recommendation mechanics, title formulas, audience targeting
- [Visual design guide](references/design-style.md) — style categories, color palettes, typography, layout rules
- [Recommended templates](references/templates.md) — curated templates by note type
