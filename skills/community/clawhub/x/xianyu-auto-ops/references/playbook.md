# Xianyu Auto Ops Playbook v3

## 1. Best trigger examples

Use this skill for requests like:

- 帮我写一个闲鱼商品文案，中英文双语
- 把这段产品介绍改成闲鱼更容易成交的版本
- 给我 10 个闲鱼标题
- 为这个二手商品做一套自动运营 SOP
- 给我批量整理 20 个 SKU 的闲鱼文案
- 按数码/家居/服饰分别给我模板
- 帮我写闲鱼私聊自动回复话术
- 给这个商品配一张广告海报提示词
- 帮我把 CSV 里的商品批量转成闲鱼文案
- 帮我卖 AI 安装/培训/自动化服务
- Write a Xianyu listing package for this product
- Turn these product specs into an Idle Fish sales post

## 2. Information to collect

Ask for or infer:

- product name / category
- brand
- condition
- age / usage frequency
- flaws
- accessories included
- shipping / pickup method
- target city
- desired price
- urgency to sell

If 20-30% of inputs are missing, continue with assumptions instead of blocking.

## 3. Category templates

### Digital / 数码
Focus on:
- model and specs
- battery / repair / warranty state
- accessories included
- authenticity and trust cues
- suitable buyer scenario

### Home / 家居
Focus on:
- dimensions
- material / style
- visible wear
- pickup / delivery burden
- where it fits in a home

### Fashion / 服饰
Focus on:
- size and fit
- material
- seasonality
- visible flaws
- styling scenario

### Virtual / 虚拟产品或服务
Focus on:
- what exactly is delivered
- how delivery happens
- whether support is included
- account / usage boundaries
- trust and compliance wording

### Training / Side-hustle / AI services
Focus on:
- target buyer
- what result they get
- delivery format
- onboarding speed
- difference from generic competitors
- trust and support boundary

For this category, also read `ai-services-template.md`.

## 4. CSV / spreadsheet batch flow

If the user provides a CSV file, normalize it first with:

```bash
python3 scripts/batch_csv_to_brief.py ./products.csv
```

Then use the JSON output as compact batch input.

Supported columns:
- sku / 编号
- name / 商品名 / 名称
- category / 类目 / 分类
- brand / 品牌
- condition / 成色 / 状态
- price_target / 价格 / 目标价
- flaws / 瑕疵
- accessories / 配件
- city / 城市
- delivery / 发货 / 交付
- notes / 备注

## 5. Title patterns

### Chinese title patterns
1. `品牌名 + 商品名 + 成色说明 + 适合谁`
2. `低价转 + 商品名 + 功能亮点 + 自提/包邮`
3. `闲置出 + 商品名 + 配件齐全 + 性价比高`
4. `适合新手/家用/学生党 + 商品名 + 省钱点`

### English title patterns
1. `Brand + item + condition + use case`
2. `Affordable + item + key benefit`
3. `Well-kept + item + bundle included`

## 6. Description formula

### Chinese
Use this order:
1. 开头一句说明是什么
2. 为什么出 / 为什么值得买
3. 成色与瑕疵说明
4. 配件、发货、自提信息
5. 友好成交收口

### English
Compress into:
1. item summary
2. condition
3. delivery / bundle
4. action line

## 7. Reply template bank

### 还在吗
在的，商品还在，方便的话我可以把细节图/使用情况再发你看。  
Still available. I can also share more detail photos if you want.

### 最低多少
这个价格已经按成色和配件压过一轮了，真心想要的话可以小刀，但不适合砍太狠。  
The current price is already fairly adjusted. Small negotiation is okay if you're serious.

### 有瑕疵吗
有，已经在描述里写明了，主要是___，不影响正常使用。我也可以补近照给你确认。  
Yes, the flaw is disclosed clearly. It mainly is ___ and does not affect normal use. I can send close-up photos.

### 包邮吗
看地区，近一点可以包，偏远地区可能需要补一点运费。  
Depends on location. Nearby shipping may be included; remote areas may need extra shipping.

### 安全交易
建议直接走平台流程更稳妥，信息和发货也都更清楚。  
Using the platform flow is safer for both sides and keeps shipping/details clearer.

### 成交推进
如果你这边确定要，我可以今天帮你保留/安排发出。  
If you want it, I can reserve it for you and arrange shipping today.

## 8. Poster / image prompt formulas

### Platform-safe cover prompt
`clean marketplace product cover, realistic product-centered composition, neutral or lightly branded background, clear lighting, no clutter, trustworthy second-hand sale style, high click-through visual hierarchy`

### Promotional poster prompt
`premium resale marketplace hero image, product-centered layout, strong contrast, clean typography-safe negative space, realistic details, modern ecommerce ad feel, high clarity, platform-friendly composition`

### 16:9 article cover add-on
Append:
`16:9 horizontal composition, strong headline-safe empty space, cover-image friendly, no watermark, no messy text`

## 9. Batch mode

When the user gives multiple products:
- keep each item compact
- one title set + one short description + one price idea + one reply note per SKU
- avoid writing long essays for every item
- group by category if helpful

Recommended compact structure:
- SKU:
- Category:
- CN title options:
- Short CN description:
- EN summary:
- Price idea:
- Reply note:
- Image direction:

## 10. v3 additions

This version adds:
- CSV / spreadsheet normalization script
- stronger batch workflow
- dedicated AI service / training / installation template
- clearer virtual goods and service boundary guidance
