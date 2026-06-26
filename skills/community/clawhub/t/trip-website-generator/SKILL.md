---
name: "trip-website-generator"
description: "Generates iOS26 liquid glass style multi-page travel websites from travel plans. Invoke when user wants to create a travel website, trip planner page, or provides detailed travel itinerary."
---

# Trip Website Generator

This skill generates a beautiful iOS26 liquid glass style multi-page travel website from a detailed travel plan.

## When to Invoke

Invoke this skill when:
- User wants to create a travel website or trip planner page
- User provides a detailed travel itinerary and wants it visualized
- User asks to generate a trip planning tool
- User mentions "旅行网站", "行程页面", "travel website", "trip planner"

## Templates

This skill includes template files in the `templates/` directory:

| File | Description |
|------|-------------|
| `templates/styles.css` | Complete CSS design system (copy directly) |
| `templates/app.js` | Shared JavaScript functionality (copy directly) |
| `templates/index.html` | Itinerary page template |
| `templates/prepare.html` | Preparation checklist template |
| `templates/notes.html` | Notes page template |
| `templates/budget.html` | Budget page template |

When generating a new travel website:
1. **Create a dedicated output directory** named by date and destination (e.g., `guangzhou-shenzhen-20260429/`, `xian-20260715/`, `beijing-20260801/`)
2. **Copy `templates/styles.css` and `templates/app.js` directly to the output directory - DO NOT modify these files in any way, copy them exactly as-is**
3. Generate HTML files by replacing template variables with actual content
4. All HTML files should reference these two files

**IMPORTANT:**
- The styles.css and app.js files must be copied verbatim without any changes. Do not read, modify, or regenerate these files - just copy them directly from templates/.
- All website files (index.html, prepare.html, notes.html, budget.html, styles.css, app.js) must be generated in a separate directory, NOT in the root directory.

## Template Variables

Templates use `{{VARIABLE_NAME}}` syntax for placeholders. Repeatable sections are marked with HTML comments like `<!-- SECTION_START -->` and `<!-- SECTION_END -->`.

### Common Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{TRIP_TITLE}}` | Trip title | 广州深圳亲子游 |
| `{{TRAVELERS}}` | Number of travelers | 一大一小 |
| `{{DURATION}}` | Trip duration | 6天5夜 |

### index.html (Itinerary Page)

**Header Section:**
- `{{TRIP_TITLE}}` - Trip title
- `{{TRAVELERS}}` - Number of travelers
- `{{START_DATE}}` - Start date (e.g., 2026.04.29)
- `{{END_DATE}}` - End date (e.g., 05.04)
- `{{DURATION}}` - Duration (e.g., 6天5夜)
- `{{TAG_1}}`, `{{TAG_2}}`, `{{TAG_3}}` - Feature tags

**Day Section (between `<!-- DAY_START -->` and `<!-- DAY_END -->`):**
- `{{ANIMATION_DELAY}}` - Animation delay (e.g., 0s, 0.05s, 0.1s...)
- `{{GRADIENT}}` - Gradient color class (purple, pink, orange, blue, green, red)
- `{{DAY_NUMBER}}` - Day number (D1, D2, D3...)
- `{{DAY_TITLE}}` - Day title
- `{{DATE}}` - Date (e.g., 4月29日 周二)
- `{{SUBTITLE}}` - Subtitle (e.g., D2431次)
- `{{HOTEL}}` - Hotel name

**Timeline Item (between `<!-- TIMELINE_START -->` and `<!-- TIMELINE_END -->`):**
- `{{HIGHLIGHT_CLASS}}` - Add " highlight" for highlighted items, empty string otherwise
- `{{TIME}}` - Time (e.g., 08:16)
- `{{ACTIVITY}}` - Activity name
- `{{DETAIL}}` - Detail description

**Guide Section (between `<!-- GUIDE_START -->` and `<!-- GUIDE_END -->`):**
- `{{GUIDE_TITLE}}` - Guide section title
- `{{GUIDE_ITEM}}` - Guide item content (repeat between `<!-- GUIDE_ITEMS_START -->` and `<!-- GUIDE_ITEMS_END -->`)
- `{{TIP}}` - Tip text (between `<!-- TIP_START -->` and `<!-- TIP_END -->`)

### prepare.html (Preparation Page)

**Category Section (between `<!-- CATEGORY_START -->` and `<!-- CATEGORY_END -->`):**
- `{{ANIMATION_DELAY}}` - Animation delay
- `{{CATEGORY_NAME}}` - Category name (e.g., 证件, 衣物, 防晒驱蚊)

**Checklist Item (between `<!-- CHECKLIST_ITEM_START -->` and `<!-- CHECKLIST_ITEM_END -->`):**
- `{{ITEM_ID}}` - Unique item ID for localStorage
- `{{ITEM_TEXT}}` - Item text

**Progress Card:**
- `{{TOTAL_ITEMS}}` - Total number of checklist items

### notes.html (Notes Page)

**Note Category (between `<!-- NOTE_CATEGORY_START -->` and `<!-- NOTE_CATEGORY_END -->`):**
- `{{ANIMATION_DELAY}}` - Animation delay
- `{{ICON_COLOR}}` - Icon color class (red, orange, blue, green)
- `{{{ICON_SVG}}}` - SVG icon (use triple braces for HTML)
- `{{CATEGORY_TITLE}}` - Category title
- `{{CATEGORY_DESC}}` - Category description

**Note Item (between `<!-- NOTE_ITEM_START -->` and `<!-- NOTE_ITEM_END -->`):**
- `{{ITEM_ICON}}` - Emoji icon
- `{{ITEM_TITLE}}` - Item title
- `{{ITEM_CONTENT}}` - Item content

### budget.html (Budget Page)

**Total Card:**
- `{{TOTAL_BUDGET}}` - Total budget (e.g., ¥7,250 - 8,800)

**Budget Section (between `<!-- BUDGET_SECTION_START -->` and `<!-- BUDGET_SECTION_END -->`):**
- `{{ANIMATION_DELAY}}` - Animation delay
- `{{SECTION_ICON}}` - Emoji icon
- `{{SECTION_TITLE}}` - Section title

**Budget Item (between `<!-- BUDGET_ITEM_START -->` and `<!-- BUDGET_ITEM_END -->`):**
- `{{ITEM_NAME}}` - Item name
- `{{ITEM_PRICE}}` - Price
- `{{ITEM_NOTE}}` - Note (between `<!-- ITEM_NOTE_START -->` and `<!-- ITEM_NOTE_END -->`)
- `{{ITEM_INCLUDED}}` - Included text (between `<!-- ITEM_INCLUDED_START -->` and `<!-- ITEM_INCLUDED_END -->`)

**Tip Card:**
- `{{TIP}}` - Tip text

## Gradients for Day Numbers

| Day | Gradient Class | Colors |
|-----|----------------|--------|
| D1 | `gradient-purple` | #667eea → #764ba2 |
| D2 | `gradient-pink` | #f093fb → #f5576c |
| D3 | `gradient-orange` | #fa709a → #fee140 |
| D4 | `gradient-blue` | #4facfe → #00f2fe |
| D5 | `gradient-green` | #43e97b → #38f9d7 |
| D6 | `gradient-red` | #f5576c → #f093fb |

## SVG Icons for Notes Page

```html
<!-- Clock icon (red) -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <circle cx="12" cy="12" r="10"/>
  <path d="M12 6v6l4 2"/>
</svg>

<!-- Sun icon (orange) -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707"/>
  <circle cx="12" cy="12" r="4"/>
</svg>

<!-- Lightning icon (blue) -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
</svg>

<!-- Smile icon (green) -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
  <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
  <line x1="9" y1="9" x2="9.01" y2="9"/>
  <line x1="15" y1="9" x2="15.01" y2="9"/>
</svg>
```

## Important Notes

1. Always use Chinese for content unless user specifies otherwise
2. Include practical tips in guide sections
3. Make sure all internal links work correctly
4. Ensure tabbar highlights the current page
5. Test checklist functionality with localStorage
6. Verify responsive design on mobile viewports
7. Include dark mode support via prefers-color-scheme
8. Animation delays should increment by 0.05s for each card
