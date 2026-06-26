---
name: weekly-menu
description: |
  Generate a weekly meal plan with images, recipes, and shopping lists.
  Searches Xiaohongshu (小红书) for trending seasonal recipes, creates a
  beautifully formatted Feishu document with photos, source links, headings
  (for table of contents navigation), and checkboxes, and stores it in the
  receipts folder. Default: 20 dishes across 6 categories.
  Use when: user asks for meal planning, weekly menu, "出菜单", "这周吃什么",
  "推荐菜", "下周菜单", or any food/cooking planning request.
---

# Weekly Menu Skill

Generate a weekly meal recommendation document with images and Xiaohongshu source links,
stored as a Feishu doc in the receipts folder.

## Prerequisites

- **agent-reach** skill installed (Xiaohongshu channel configured)
- **Feishu** channel configured with permissions: `docx:document`, `docx:document:create`, `drive:drive`
- User profile at `meals/profile.yaml` (see `references/profile-template.yaml`)

## Workflow

### 1. Load User Profile

Read `meals/profile.yaml` for:
- `location` — determines seasonal ingredients
- `household.portions` — serving size
- `cooking.equipment` — available appliances (air fryer, pressure cooker, etc.)
- `cooking.timeAvailable` — quick/moderate/slow
- `cooking.spiceTolerance` — none/mild/medium-hot/hot
- `preferences.cuisinesFavourite` — preferred cuisines
- `preferences.explorationLevel` — conservative/adventurous
- `schedule.cookingDays` — how many days per week

If profile doesn't exist, ask user the basics and create one from `references/profile-template.yaml`.

### 2. Search for Recipe Inspiration

Use agent-reach Xiaohongshu search to find trending recipes:

```
mcporter call 'xiaohongshu.search_feeds(keyword: "<search_term>")'
```

Search strategy (3-5 searches):
- Current season + location + "时令菜"
- Equipment-specific: "空气炸锅 家常菜", "高压锅 菜谱"
- Cuisine preference: "川菜 家常", "苏菜 做法"
- General: "一周菜谱 简单好吃"

Pick the top results by likes/collects. Aim for **20 candidate dishes** across 6 categories:
- 🌿 春季时令 (seasonal)
- 🔥 空气炸锅 (air fryer)
- 🍲 高压锅硬菜 (pressure cooker)
- 🌶️ 下饭菜 (rice killers)
- 🏠 经典家常 (classic home cooking)
- 🍳 快手 & 主食 (quick meals & staples)

### 3. Compose the Menu

Organize 20 dishes into 6 themed sections based on equipment, cuisine, and cooking method:
- Balance variety: don't repeat proteins or methods within a section
- Each dish needs: number (①-⑳), name, one-line description, cooking time, equipment used

### 4. Download Dish Images

Download a representative image for each dish (from Unsplash or similar free sources — Xiaohongshu CDN blocks direct downloads):

```bash
curl -sL --connect-timeout 10 --max-time 20 -o ./tmp/dishes/01-name.jpg "<url>"
```

Store in `workspace/tmp/dishes/`. Verify each file is a valid JPEG/PNG (not empty or HTML error).

### 5. Create Feishu Document

Read `references/feishu-doc-recipe.md` for the full Feishu API procedure.

**Summary:**
1. Create doc with title `🍽️ YYYY-MM-DD 推荐菜单` (Monday's date) in receipts folder
2. Grant user `full_access` permission
3. Insert blocks in ≤50-block batches. For each dish, create these blocks in order:
   - **heading3** (block_type 5) — dish name, enables table of contents navigation
   - **todo/checkbox** (block_type 17, `done: false`) — same dish name, for user to check off
   - **text** (block_type 2) — description + cooking time
   - **empty image** (block_type 27) — placeholder, filled later
   - **text with link** — "📌 小红书菜谱" linking to XHS post
4. After all text blocks inserted, fill images: upload to drive → patch with `replace_image`
5. Sections separated by divider (block_type 22) + heading2 (block_type 4)

**Key constraints:**
- Max 50 blocks per insert call — split 20 dishes into 4 batches (~25 blocks each)
- Max 3 edits/second per document — use `time.sleep(0.4)` between API calls
- Image blocks must be created empty (`{"block_type": 27, "image": {}}`) then filled via patch
- Insert batches bottom-to-top when adding blocks to avoid index shifting

### 6. Share Result

Send the document link to the user in chat. Format:

```
🍽️ 本周菜单已出炉！20 道菜已备好

👉 <document_url>

打开文档，从目录浏览所有菜，勾选你想做的～
```

### 7. Update History

Append the week's menu to `meals/history.yaml` for future reference and to avoid repeats.

## Config

| Key | Location | Description |
|-----|----------|-------------|
| User profile | `meals/profile.yaml` | Taste preferences and constraints |
| Receipts folder | Feishu drive | Token stored in MEMORY.md |
| Meal history | `meals/history.yaml` | Past menus to avoid repeats |

## File References

- `references/profile-template.yaml` — blank user profile template
- `references/feishu-doc-recipe.md` — step-by-step Feishu document creation API guide
