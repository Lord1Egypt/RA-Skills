# Block Content Analysis & Stage Classification

This file defines how to analyze block content and assign psychology phases.

## Part 1: Block Content Analysis

For each block, determine its marketing module category and summarize its content.

### Module Categories by Page Type

#### Sales LP / Ad LP (10 categories)
1. **First View (FV)**: Top of page — main catchphrase, hero image, initial CTA
2. **Pain Points**: User problems/worries to build empathy
3. **Benefits/USP**: Specific selling points, features, "Point 1, 2, 3" structures
4. **Proof/Authority**: Rankings, media coverage, expert endorsements, awards
5. **Voice of Customer (VOC)**: User reviews, testimonials, star ratings
6. **Product Intro**: Basic product specs, ingredients, visual presentation
7. **Q&A / Trust**: FAQ, company info, refund policies
8. **Usage Process**: Step-by-step guide on how to use
9. **Offer/CTA**: Price presentation, discount, urgency, Call-To-Action
10. **Other**: Content not fitting above

#### PDP (10 categories)
1. **Buy Box**: Product title, price, variants, primary "Add to Cart"
2. **Product Gallery**: Product images, video, 360-view
3. **Key Benefits**: Main selling points, feature highlights
4. **Specifications**: Technical specs, dimensions, materials
5. **Social Proof**: Reviews, ratings, UGC
6. **Cross-sell**: Recommendations, "also bought", bundles
7. **Shipping/Returns**: Delivery info, return policy
8. **Guarantees**: Warranty, satisfaction guarantee
9. **CTA (secondary)**: Additional purchase CTAs lower on page
10. **Other**: Content not fitting above

#### Homepage (9 categories)
1. **Hero/FV**: Main banner, value proposition
2. **Navigation Hub**: Category links, menu highlights
3. **New Arrivals/Featured**: Product highlights, seasonal picks
4. **Brand Story**: About us, mission, differentiators
5. **Trust Signals**: Awards, media, partner logos
6. **Blog/Content**: Articles, tips, educational content
7. **Newsletter/CTA**: Email signup, app download
8. **Social Proof**: Reviews, testimonials aggregate
9. **Other**: Content not fitting above

#### Article LP (8 categories)
1. **Headline/Hook**: Title, subtitle, reading hook
2. **Problem Awareness**: Issue introduction, pain description
3. **Cause Analysis**: Why the problem exists
4. **Discovery/Story**: Narrative, case study, personal story
5. **Solution Introduction**: Product/service as answer (soft)
6. **Social Proof**: Expert quotes, user stories, data
7. **Transition CTA**: "Learn more", "Try now" — soft action
8. **Other**: Content not fitting above

#### Campaign / Promotion (9 categories)
1. **Key Visual**: Theme banner, discount headline
2. **Rules/Timeline**: Eligibility, time window, terms
3. **Coupons**: Discount codes, deal tiers
4. **Hero Products**: Featured deals, top picks
5. **Category Floors**: Product grids by category
6. **Urgency Cues**: Countdown timers, stock alerts
7. **Primary CTA**: Main conversion action
8. **FAQ/Support**: Questions, contact
9. **Other**: Content not fitting above

#### Other Content (8 categories)
1. **Header/Relevance Signal**: Page title, intro, breadcrumb
2. **Core Content Section**: Main body (article, job desc, FAQ answers, pricing table)
3. **Supporting Evidence**: Data, examples, case studies
4. **Visual/Media**: Images, videos, infographics
5. **Trust/Credibility**: Author info, certifications, awards
6. **Secondary Content**: Related articles, sidebar
7. **Action CTA**: Apply, contact, download, register
8. **Other**: Content not fitting above

#### Other Function (6 categories)
1. **Task Header**: Page title, instructions
2. **Primary Form/Action**: Login form, signup form, checkout form, search
3. **Help/Guidance**: Field hints, tooltips, help links
4. **Feedback/Confirmation**: Success/error messages, validation
5. **Post-task Navigation**: Next step links, redirect
6. **Other**: Content not fitting above

### Output per Block

```json
{
  "block_id": 12345,
  "module_category": "string",
  "content_summary": "concise description of text and visual",
  "key_selling_points": ["point1", "point2"],
  "marketing_intent": "psychological goal of this block"
}
```

---

## Part 2: Block Stage Classification (4-Phase Psychology Model)

Map each block to one of 4 user psychology phases. The phase names vary by page type.

### Phase Names by Page Type and Language

#### ad_lp
| Phase | CHINESE | JAPANESE | ENGLISH |
|-------|---------|----------|---------|
| 1 | 承接用户第一直觉 | 第一印象を受け止める | Capture first impression |
| 2 | 与用户产生共鸣 | 共感を生む | Build resonance |
| 3 | 给予用户购买理由 | 購入理由を与える | Provide purchase reasons |
| 4 | 消除用户顾虑 | 不安を解消する | Reduce concerns |

#### sales_lp
| Phase | CHINESE | JAPANESE | ENGLISH |
|-------|---------|----------|---------|
| 1 | 聚焦活动价值 | キャンペーン価値に集中する | Focus on campaign value |
| 2 | 说明参与规则 | 参加ルールを説明する | Explain participation rules |
| 3 | 分类高效选品 | カテゴリで素早く商品を選べるようにする | Enable quick selection by category |
| 4 | 冲刺完成下单 | 注文完了まで後押しする | Push to order completion |

#### pdp
| Phase | CHINESE | JAPANESE | ENGLISH |
|-------|---------|----------|---------|
| 1 | 对齐购买要素 | 購入判断要素を揃える | Align purchase decision factors |
| 2 | 解释产品价值 | 商品価値を伝える | Explain product value |
| 3 | 验证信任证据 | 信頼の根拠を示す | Provide proof and trust signals |
| 4 | 促成交易动作 | 購入行動を後押しする | Drive purchase action |

#### homepage
| Phase | CHINESE | JAPANESE | ENGLISH |
|-------|---------|----------|---------|
| 1 | 定位品牌与人群 | ブランドとターゲットを明確にする | Clarify brand and audience |
| 2 | 分发下一步路径 | 次の導線へ誘導する | Guide the next step |
| 3 | 强化可信与理由 | 信頼と理由を強化する | Strengthen trust and reasons |
| 4 | 承接可持续关系 | 継続関係につなげる | Build ongoing relationships |

#### article_lp
| Phase | CHINESE | JAPANESE | ENGLISH |
|-------|---------|----------|---------|
| 1 | 建立阅读信任 | 読み進める信頼をつくる | Build reading trust |
| 2 | 放大问题共鸣 | 課題への共感を強める | Amplify problem resonance |
| 3 | 闭环方案说服 | 解決策で納得させる | Persuade with a complete solution |
| 4 | 降低行动门槛 | 行動のハードルを下げる | Lower the action barrier |

#### other_content
| Phase | CHINESE | JAPANESE | ENGLISH |
|-------|---------|----------|---------|
| 1 | 判断相关性 | 関連性を判断する | Assess relevance |
| 2 | 深入探索内容 | コンテンツを深く探索する | Explore content in depth |
| 3 | 评估与确认 | 評価と確認 | Evaluate and confirm |
| 4 | 目标动作 | 目標行動 | Target action |

#### other_function
| Phase | CHINESE | JAPANESE | ENGLISH |
|-------|---------|----------|---------|
| 1 | 识别操作入口 | 操作入口を特定する | Identify entry point |
| 2 | 执行核心操作 | コアタスクを実行する | Execute core task |
| 3 | 反馈与确认 | フィードバックと確認 | Feedback and confirmation |
| 4 | 后续引导 | 次のステップへ誘導 | Guide to next step |

### Phase Assignment Criteria

#### Ad LP Phases (detailed)

**Phase 1 — Capture first impression**
- User state: Quick scan, "is this for me?"
- Typical blocks: FV, Hero, first 1-2 blocks
- Checklist: Result orientation? Zero-thinking simplicity? Quick entry for high-intent users?
- Ad-specific: Strong visual impact, result showcase ("from A to B"), number-backed promises

**Phase 2 — Build resonance**
- User state: "Do you understand my problem?"
- Typical blocks: Pain points, scenarios, Before/After
- Checklist: Concrete pain specificity? Clear contrast? Identity match? Emotion-to-CTA bridge?
- Ad-specific: Multi-layered pain (surface → deep anxiety), scene-based language, 3-5 parallel pain points

**Phase 3 — Provide purchase reasons**
- User state: "Is the product reliable/effective?"
- Typical blocks: USP, benefits, authority, reviews, usage method, product intro
- Checklist: Uniqueness explanation? Doubt elimination? Evidence logic?
- Ad-specific: Dense proof elements, multiple evidence types stacked

**Phase 4 — Reduce concerns**
- User state: "Is the price worth it? Any risks?"
- Typical blocks: Pricing, guarantees, FAQ, final CTA
- Checklist: Value-price clarity? Risk elimination? Urgency?
- Ad-specific: Strong urgency triggers, risk reversal, countdown/scarcity

#### Homepage Phases (detailed)

Homepage phases are fundamentally different from LP phases — they focus on navigation and brand
building rather than a purchase decision funnel.

**Phase 1 — Clarify brand and audience (ブランドとターゲットを明確にする)**
- Typical blocks: Hero Banner, main navigation, brand tagline, first 1-2 blocks
- Key question: Can users understand "who you are and who you serve" within 3 seconds?

**Phase 2 — Guide the next step (次の導線へ誘導する)**
- Typical blocks: Category navigation, product curation (New Arrivals, Best Sellers), feature
  showcases, product/service highlights, collection links
- Key question: Can users find something interesting and know where to go next?
- NOTE: Product/feature introductions belong HERE, not Phase 3

**Phase 3 — Strengthen trust and reasons (信頼と理由を強化する)**
- Typical blocks: Customer logos, testimonials/reviews, "As Seen On" media, brand story,
  Instagram feed, awards, sustainability claims
- Key question: Does users trust this brand enough to take action?
- NOTE: Social proof (client logos, testimonials) belongs HERE, not Phase 2. The distinction is:
  Phase 2 = "what you offer" (products/features), Phase 3 = "why to trust you" (evidence/proof)

**Phase 4 — Build ongoing relationships (継続関係につなげる)**
- Typical blocks: Newsletter signup, CTA, blog/content links, membership, footer, contact
- Key question: Does the page give users a clear next action before they leave?

#### Assignment Heuristic: Ad LP / Sales LP (when content is limited)

| Signal | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|---------|---------|---------|---------|
| Position | First 1-2 blocks | Early-middle | Middle | Late |
| block_name | FV, Hero, Header, Main Visual | Pain, Problem, Concern, Before/After | Feature, Benefit, Proof, Review, USP, Product | Price, CTA, FAQ, Guarantee, Footer, Q&A |
| module_category | First View | Pain Points | Benefits, Proof, VOC, Product Intro, Usage | Offer/CTA, Q&A/Trust |

#### Assignment Heuristic: Homepage (when content is limited)

| Signal | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|--------|---------|---------|---------|---------|
| Position | First 1-2 blocks | Early-to-middle | Middle-to-late | Late / footer |
| block_name | Hero, Banner, Navigation, Main Visual | Product, Feature, Service, Category, Collection, All-in, Solution | Customer, Testimonial, Review, Voice, Brand Story, Trust, Logo, Media | CTA, Subscribe, Newsletter, Resource, Footer, Contact, Blog |
| module_category | Hero Banner, Category Navigation | Product Curation, Feature Showcase | Social Proof, Brand Story, VOC | Newsletter, Lead Gen, Footer, Content/Blog |

**Critical distinction for Homepage**: Client logos, customer testimonials, and "trusted by X
companies" blocks are Phase 3 (trust), NOT Phase 2 (exploration). Product feature descriptions
are Phase 2 (what we offer), NOT Phase 3 (why trust us).
