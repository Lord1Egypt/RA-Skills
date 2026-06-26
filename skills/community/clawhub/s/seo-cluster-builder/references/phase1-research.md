# Phase 1 — Research & Competition Analysis

Run this phase before designing any cluster. Never skip.

---

## Step 1.1 — Fetch the client's site

```
web_fetch: https://[client-domain]/
web_search: site:[client-domain]
```

Identify:
- What platform (WordPress, Shopify, custom)?
- What blog/URL structure does it use? (`/blog/slug`, `/slug/`, `/tin-tuc/slug`?)
- What clusters or informational content already exists?
- Which existing articles could be redirected or bridged into the new cluster?

**Flag for audit box:**
- Articles with overlapping topic → cannibalization risk
- Old thin articles → redirect candidate
- Related articles → bridge link candidate

---

## Step 1.2 — Identify top competitors for the target keyword

```
web_search: [target keyword] (Vietnamese)
web_search: [target keyword] site:[competitor1]
```

For each top-3 result, note:
| Metric | What to check |
|---|---|
| Domain type | Brand? Platform? Blog? |
| Content depth | Word count estimate, H2 count |
| Schema | Does it have FAQPage/HowTo in SERP? |
| Gap | What angle do they NOT cover? |

**DA proxy heuristic** (no tool access):
- National news site / major e-commerce platform → DA 60+ → avoid head term
- Niche blog / small shop → DA 20–40 → possible to compete directly
- No result or thin results → blue ocean → go for it

---

## Step 1.3 — Determine the winning angle

Use this decision tree:

```
Head term competitor DA 60+?
├── YES → Find a specific angle:
│         - Product-specific: "X for [product]" (pinata.vn → "trò chơi tiệc")
│         - Long-tail: "[topic] cho bé trai/gái/[age]"
│         - Local: "[topic] tại [city]"
│         - Theme: "[topic] chủ đề [character]"
└── NO  → Can go for head term directly
          BUT: still check for cannibalization on own site
```

**The pinata.vn examples:**
- "tổ chức tiệc sinh nhật" → DA 60+ (Huggies, PasGo) → pivot to "trò chơi tiệc sinh nhật" (low competition, high conversion)
- "pinata sinh nhật" → low competition → go direct
- "pinata là gì" → medium competition (glowstore.vn) → go direct, win with depth

---

## Step 1.4 — Map keyword groups

From the angle, expand to keyword groups. Each group = 1 cluster article.

**4 intent groups to cover:**

```
INFORMATIONAL  → "X là gì", "lịch sử X", "nguồn gốc X"
HOW-TO         → "cách làm X", "cách chơi X", "cách tổ chức X"
COMMERCIAL     → "mua X ở đâu", "giá X bao nhiêu", "X loại nào tốt"
THEME/LONG-TAIL → "X cho bé trai", "X chủ đề khủng long", "X tại Hà Nội"
```

For each group, identify:
1. Primary keyword (highest intent)
2. 2–3 secondary keywords (variations, long-tails)
3. Whether to make it 1 article or combine into pillar

**Combine into pillar if:** all keywords have the same search intent AND the pillar would answer all of them adequately.

**Make separate articles if:** intent differs OR depth required per topic exceeds ~800 words.

---

## Step 1.5 — Pre-flight checklist

Before moving to Phase 2:

```
☐ Client site platform identified
☐ Existing articles scanned for cannibalization
☐ Top 3 competitors fetched and analyzed
☐ Winning angle selected (not head-on DA60+ competition)
☐ 6–8 keyword groups mapped
☐ Redirect/bridge candidates noted for audit box
```

**Output of Phase 1:**
→ Angle + pillar topic
→ List of 6–8 article titles + primary keywords
→ List of pre-existing articles to redirect/bridge
