---
name: xianyu-auto-ops
description: Bilingual Xianyu (闲鱼) listing and lightweight operations workflow for second-hand goods, side-hustle products, and marketplace distribution. Use when the user wants to create, optimize, or batch-produce Xianyu listing assets such as titles, selling points, product descriptions, image prompts, reply scripts, pricing angles, posting checklists, or simple operating SOPs in Chinese and English. Also use when the user asks to turn product info or CSV-like SKU data into publish-ready marketplace materials, wants category-specific Xianyu templates, needs buyer chat replies, or wants a reusable batch-oriented Xianyu sales process for physical goods, digital products, or AI services.
---

# Xianyu Auto Ops

Use this skill to turn rough product information into a repeatable **Xianyu / Idle Fish operating package**.

Default output language: **bilingual Chinese + English**.  
Default business goal: **faster listing, clearer positioning, better inquiry conversion**.

## Core workflow

Follow this sequence unless the user asks for only one part.

1. **Clarify the offer**
   - Identify product type, condition, target buyer, price band, and delivery method.
   - If key details are missing, make lightweight assumptions and label them clearly.

2. **Choose the operating mode**
   - **Single listing mode**: one product, one polished package.
   - **Batch listing mode**: multiple SKUs, concise per-item outputs.
   - **Reply mode**: buyer inquiry handling, objection answers, negotiation copy.
   - **Optimization mode**: improve an existing listing.
   - **Poster mode**: generate ad-style image prompts for listing cover or off-platform promo.

3. **Pick a category template**
   Use the closest category framing:
   - **Digital / 数码**: specs, condition, accessories, battery, warranty, authenticity cues.
   - **Home / 家居**: size, cleanliness, usage marks, pickup logistics, scene fit.
   - **Fashion / 服饰**: size, fabric, season, flaws, try-on expectation.
   - **Virtual / 虚拟产品或服务**: delivery scope, usage rights, support boundaries, trust language.
   - **Training / Side-hustle / AI services**: results, delivery format, onboarding, trust signals, support boundaries. Read `references/ai-services-template.md` when the product is training, installation, deployment, consulting, or AI service resale.

4. **Produce the listing package**
   Return, in this order when relevant:
   - Chinese title ×3
   - English title ×1
   - Core selling points / 卖点摘要
   - Chinese listing description
   - English summary description
   - Suggested tags / keywords
   - Suggested price anchor and negotiation room
   - Cover image prompt(s)
   - Buyer reply scripts
   - Posting checklist

5. **Keep it platform-native**
   - Prefer short, direct, benefit-led copy.
   - Avoid exaggerated claims that sound fake or risky.
   - Make the listing feel like a real seller wrote it, not a brand brochure.

## Batch listing mode

When the user gives multiple items, default to a compact table-like structure using bullets, not markdown tables on chat surfaces.

For each SKU, include:
- SKU / item name
- Chinese title ×2
- One short Chinese description
- One short English summary
- Suggested listed price / expected close price
- One key reply note
- One image direction

If the user provides a CSV or spreadsheet, use `scripts/batch_csv_to_brief.py <file>` to normalize the rows first, then use the JSON output as batch input.

Expected columns can include:
`sku, name, category, brand, condition, price_target, flaws, accessories, city, delivery, notes`

Chinese headers like `商品名 / 类目 / 成色 / 价格 / 瑕疵 / 配件 / 城市 / 发货 / 备注` are also supported.

Do not ask the user to perfect the data before starting. Fill gaps with assumptions and mark them.

## Output rules

### Titles

Write titles that are:
- easy to scan
- keyword-rich without obvious stuffing
- benefit-forward
- believable for Xianyu

Prefer this rough formula:

`[brand/category] + [core item] + [condition / key value] + [buyer use case / bonus point]`

### Descriptions

For each Chinese description, keep this structure:

1. What it is
2. Why selling / product background
3. Condition / usage / delivery details
4. Why worth buying
5. Call to action

For English, provide a shorter mirror summary rather than a full literal translation unless the user asks for full bilingual parity.

### Pricing

When suggesting price, provide three layers when possible:
- **Listed price** / 挂价
- **Expected成交价** / expected closing price
- **最低可谈区间** / lowest negotiable band

Base suggestions on:
- condition
- urgency to sell
- scarcity / uniqueness
- bundled extras
- local delivery convenience

### Buyer reply scripts

When generating reply scripts, include short ready-to-send messages for:
- “还在吗？” / “Is this still available?”
- “最低多少？” / “What’s your lowest price?”
- “有瑕疵吗？” / “Any flaws?”
- “包邮吗？” / “Is shipping included?”
- “怎么交易更稳妥？” / “How do we trade safely?”
- closing push / 成交推进

Keep replies short and human.

### Poster prompts

When the user asks for ad visuals, output two prompt layers:
- **Platform-safe cover prompt**: more realistic, cleaner, product-led.
- **Promotional poster prompt**: more visual tension, more marketing feel, more negative space for title text.

Prefer **16:9** for article covers and **1:1 / 4:5** for feed-like visuals unless the user says otherwise.

## Recommended response format

Use this template unless the user asks for a different one.

### 1. 商品定位 / Positioning
- Chinese:
- English:

### 2. 标题建议 / Title Options
- CN-1:
- CN-2:
- CN-3:
- EN-1:

### 3. 卖点提炼 / Selling Points
- 

### 4. 商品文案 / Listing Copy
**中文版本**

**English version**

### 5. 配图建议 / Image Plan
- Cover idea:
- Detail shots:
- Platform-safe AI image prompt:
- Promotional poster prompt:

### 6. 价格建议 / Pricing Strategy
- Listed price:
- Expected close price:
- Lowest negotiable range:

### 7. 私聊回复模板 / Chat Reply Scripts
- 在的 / Available:
- 最低价 / Lowest price:
- 瑕疵说明 / Flaw disclosure:
- 安全交易 / Safe trade:
- 成交推进 / Closing push:

### 8. 发布清单 / Posting Checklist
- [ ] photos ready
- [ ] condition disclosed
- [ ] delivery method stated
- [ ] keywords included
- [ ] price strategy set
- [ ] reply script ready

## Bilingual handling

When the user asks for bilingual output, do not translate mechanically.

- Chinese should sound like a native Xianyu seller.
- English should sound like a concise marketplace assistant summary.
- If the target buyers are Chinese users only, keep English shorter.

## Safety and quality guardrails

- Do not fabricate certifications, warranties, invoices, or brand authorization.
- Do not hide material defects if the user explicitly mentions them.
- Do not promise impossible delivery times.
- Flag risky categories, compliance-sensitive products, or obvious fraud patterns.
- For virtual goods or services, clearly describe what is and is not delivered.

## References

Read `references/playbook.md` when the user needs stronger title formulas, batch handling, category-specific patterns, buyer reply banks, or poster prompt templates.
