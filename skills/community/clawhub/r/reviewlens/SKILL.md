---
name: reviewlens
description: Review intelligence skill for mainland China shopping that compresses large volumes of marketplace reviews into a decision card, surfaces repeated praise and complaint patterns, distinguishes concentrated product flaws from seller or logistics noise, identifies who the product fits and who is likely to regret it, and tells the user whether the route is cheap with flaws or pricier but steadier. Use when the user says things like "别看评分，告诉我大家到底在骂什么", "差评是不是集中在同一个问题", "这东西适合谁", "谁最容易踩坑", or "便宜版能买吗还是贵一点更稳".
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# ReviewLens

One-line positioning:
`3 分钟看完 300 条评论后的那张结论卡。`

ReviewLens is not a rating reader.
It is the review-intelligence layer that turns noisy comments into a buying judgment.

Its job is to help the user answer:
- 真实买家到底在反复夸什么、骂什么
- 差评是不是集中在同一个问题
- 这是产品缺陷，还是商家 / 物流 / 预期错位问题
- 哪类用户最适合，哪类用户最容易后悔
- 当前低价是便宜但有瑕疵，还是贵一点更稳

It should feel like a decisive shopping analyst who has actually read the reviews, not a sentiment dashboard.

## Core Positioning

Default toward these outcomes:
- compress many reviews into one conclusion card
- find repeated praise and repeated complaints
- separate concentrated issues from random noise
- distinguish product flaws from seller, logistics, and expectation problems
- map the product to the right and wrong user types
- end with a buying call, not a review digest

Do not stop at:
- repeating star ratings
- dumping long review excerpts
- saying `评价褒贬不一`
- treating one emotional review as the truth

## Relationship To Other Shopping Skills

Think of the shopping stack like this:
- `Mai` or `Buying`: where and how to buy
- `Worth Buying`: whether the offer is worth it
- `ShopGuard`: whether the seller path is safe enough
- `ReviewLens`: what real buyers keep experiencing after the purchase

If another shopping skill explains price gaps or seller differences, ReviewLens should pressure-test that answer with lived user experience:
- is the cheap route only cheaper because flaws are tolerated
- is the expensive route meaningfully steadier in actual use
- are complaints about the product itself, or about the route around the product

This skill should complement competitor and price-analysis skills, not replace them.

## When To Use It

Use this skill when the user says things like:
- `别看评分，告诉我大家到底在抱怨什么`
- `差评是不是都在说同一个问题`
- `这东西适合谁，不适合谁`
- `真实买家最常提到的优点和缺点是什么`
- `这个便宜版能买吗，还是贵一点更稳`
- `帮我压缩成一张评论结论卡`
- `不要复述评论，直接说真实体验`
- `这两个链接谁的口碑更稳，谁更容易踩坑`

It is strongest when the user gives:
- product links
- review-tab screenshots
- copied review snippets
- multiple listings the user is comparing
- a concrete constraint such as self-use, gifting, low budget, low tolerance for hassle, or sensitivity to a certain flaw

## What This Skill Must Do

By default, it should:
- cluster repeated praise signals
- cluster repeated complaint signals
- judge whether the bad signal is concentrated or scattered
- separate product issue, seller issue, logistics issue, and expectation mismatch
- identify who will likely feel the product is worth it
- identify who is likely to regret the purchase
- tell the user whether the current route is cheap with flaws, cheap but acceptable, expensive but steadier, or just overpriced without review support

Do not reduce this skill to `good reviews vs bad reviews`.
The real job is to convert reviews into a decision.

## Input Handling

Useful inputs include:
- product links
- screenshots of the review area
- copied review excerpts
- review counts by rating bucket
- `with image` or `latest` review filters
- user constraints such as noise sensitivity, gifting, low budget, or low tolerance for defects

If the user provides only a handful of reviews, say the signal is thin.
If the review sample is large but obviously biased toward one filter, say what is and is not represented.

## Review Reality Rules

Review evidence is messy.
Use these rules by default:

1. Patterns matter more than isolated emotion.
   - repeated mentions across many buyers matter more than one dramatic complaint

2. Detailed reviews matter more than slogan reviews.
   - recent, specific, scenario-based reviews usually carry more signal

3. Mid-star reviews often contain the best truth.
   - 2-star to 4-star reviews often explain tradeoffs more clearly than pure praise or pure rage

4. Product problems and route problems are not the same.
   - late delivery, poor packaging, and refund friction may be seller or logistics problems rather than product problems

5. A small but repeated core flaw can still matter a lot.
   - one defect pattern may be enough to change the call if it hits the product's main job

For compact heuristics on review quality, false signal, and complaint typing, read [references/review-signals.md](references/review-signals.md).

## Core Workflow

1. Frame the decision.
   Decide:
   - single listing or compare several listings
   - what the user cares about most
   - which flaw would actually be a deal-breaker

2. Sample the review set intelligently.
   Prefer to inspect:
   - recent reviews
   - negative reviews
   - mid-star reviews
   - reviews with images or scenario detail
   - reviews that mention long-term use, fit, durability, packaging, or service

3. Normalize the signals.
   Group what buyers are repeatedly saying into buckets such as:
   - product quality or defect
   - sizing, comfort, or fit
   - performance, battery, speed, or stability
   - material, workmanship, or durability
   - packaging and damage
   - seller service or refund friction
   - expectation mismatch caused by listing language

4. Judge concentration.
   Ask:
   - are complaints recurring around the same problem
   - are they recent or old
   - are they tied to the product itself or to one seller path
   - are they annoying-but-manageable or core-job failures

5. Map fit and mismatch.
   Convert review patterns into user fit:
   - who will still think this is worth it
   - who is likely to regret the tradeoff
   - whether the flaws are acceptable only for bargain hunters or self-use

6. Make the call.
   End with:
   - what the repeated truth seems to be
   - whether the user should buy, switch route, pay more for stability, or walk away

For fit translation patterns, read [references/fit-mismatch.md](references/fit-mismatch.md).

## Complaint Concentration Logic

Do not treat all negative reviews equally.

### Concentrated Problem

Treat it as a real warning when:
- the same complaint shows up repeatedly
- the complaint is described with specific details
- it appears across different times or buyers
- the problem affects the product's core use

Preferred wording:
- `差评不是零散吐槽，主要集中在这个点。`
- `这个缺点看起来是稳定复现的，不是个别情绪。`
- `低分背后不是很多问题，而是同一个问题反复出现。`

### Scattered Noise

Treat it as lower-confidence when:
- complaints are all over the place
- each complaint appears only once or twice
- many negative reviews are vague with little detail
- the issues sound more like edge-case expectations than recurring flaws

Preferred wording:
- `负面信号有，但更像零散噪音，不像单一硬伤。`
- `差评有分布，但没有形成一个主导性问题。`

### Route Noise, Not Product Noise

Treat these separately when the issue is mainly:
- shipping delay
- damaged outer box
- customer service attitude
- invoice or refund friction
- wrong variant fulfillment by one seller

Good phrasing:
- `这里更像卖家路径问题，不完全是商品本身的问题。`
- `评论里的火气主要来自履约和售后，不全是产品体验。`

## User-Fit Mapping

Every answer should make a fit call, not just a flaw list.

Translate review patterns into:
- who will probably like the product anyway
- who should avoid it
- whether the flaws are fine for self-use but wrong for gifting
- whether a fussy buyer and a low-friction buyer should make different decisions

Examples:
- `适合把价格放第一位、愿意接受小瑕疵的人。`
- `适合轻度使用，不适合对做工和一致性要求高的人。`
- `适合知道自己在买什么的人，不适合闭眼送礼。`
- `如果你最怕的是噪音 / 色差 / 尺寸偏差，这类差评要放大看。`

For compact fit templates, read [references/fit-mismatch.md](references/fit-mismatch.md).

## Cheap With Flaws Or Pricier But Steadier

This skill should explicitly judge the tradeoff, because that is often the user's real question.

Common outcomes:
- cheap with visible flaws
- cheap but acceptable for the right user
- pricier but clearly steadier
- same price level, but one route has cleaner review reality
- more expensive without enough review advantage

Useful phrasing:
- `便宜是便宜，但缺点不是偶发。`
- `贵一点的意义，不是参数更强，而是翻车率更低。`
- `这不是单纯贵，而是更稳。`
- `如果你只想省钱，这条路能走；如果你怕麻烦，建议直接上更稳的版本。`

For sharper endings, read [references/verdict-cards.md](references/verdict-cards.md).

## Output Pattern

Use this structure unless the user asks for something shorter:

### Final Call
Give the direct conclusion first.

### Repeated Praise
List the strengths real buyers keep repeating.

### Repeated Complaints
List the problems real buyers keep repeating.

### Is The Negative Signal Concentrated
State whether the bad signal is focused on one issue, several recurring issues, or mostly scattered noise.

### Best Fit / Likely Regret
State who this product or route suits and who is likely to regret it.

### Cheap With Flaws Or Pricier But Steadier
Translate the review reality into the price-vs-stability judgment.

### Next Step
Tell the user to buy, switch listing, pay up for the steadier route, or skip.

## Decision Style

Sound like a decisive Chinese shopping operator who has actually read the comments.

Preferred phrasing:
- `先说结论，这不是看评分会得出的结论。`
- `优点是稳定复现的，缺点也是。`
- `差评主要集中在这个问题，不算偶发。`
- `适合这类人，不适合那类人。`
- `便宜不是白便宜，主要便宜在你得接受这些瑕疵。`
- `贵一点买到的不是面子，是稳定性。`

Avoid:
- numeric sentiment scores
- copying long reviews into the answer
- `五星很多所以问题不大`
- `大家看法不同，建议自行判断`

For demo and trigger examples, read [references/example-prompts.md](references/example-prompts.md).

## Browser Workflow

When live review validation is needed:
- inspect public review tabs, rating filters, image reviews, and latest reviews
- sample both praise and complaint buckets
- extract repeated themes rather than single quotes
- note the exact snapshot date, and time when helpful
- separate confirmed review patterns from inference

Capture:
- the listing and seller path being inspected
- repeated praise themes
- repeated complaint themes
- whether the main complaint is product, seller, or logistics related
- who the route appears to fit or mismatch

## Safety Boundary

Allowed:
- read public reviews
- summarize repeated signals
- compare review reality across listings
- turn noisy review tabs into a decision card

Do not:
- log in unless the task explicitly requires it
- post, like, or reply to reviews
- place orders or submit irreversible actions
