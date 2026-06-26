---
name: real-estate-listing-writer
description: Turn raw property details into an MLS-ready listing description plus matching Instagram, Facebook, short-form video, and email-blast variants. Use whenever the user pastes property specs (address, beds/baths, sqft, features) or asks for "write a listing", "make a listing description", "draft MLS copy", "turn this into a listing", "social posts for my new listing", or similar. Optimized for US real estate agents and brokerages.
version: 1.0.0
license: MIT
tags:
  - real-estate
  - marketing
  - copywriting
  - listings
  - mls
  - social-media
metadata:
  openclaw:
    requires:
      env: []
      bins: []
---

# Real Estate Listing Writer

Turn a handful of property details into a complete marketing package: one MLS-ready description plus matching social and email variants, all Fair-Housing-compliant and on-brand.

## When to use this skill

Trigger this skill when the user:
- Pastes raw property details (address, beds/baths, square footage, year built, features) and asks for listing copy
- Says "write a listing for...", "make an MLS description", "turn this into listing copy", "draft marketing for this property"
- Shares a spec sheet, datasheet, or bullet list of property features and wants polished marketing copy
- Asks for social posts, email blasts, or "just listed" announcements for a specific property

Do NOT trigger this skill for:
- Comparable-sales reports (CMA) — that's a separate skill
- Lead replies or buyer follow-ups — separate skills
- Commercial property analysis — out of scope

## Step 1 — Collect inputs

Before writing anything, confirm you have the items below. If any are missing, ask for them in a single grouped message (don't drip-feed one question at a time).

Required:
1. Property address (street, city, state)
2. Beds and baths (full + half)
3. Interior square footage
4. Property type (single-family, condo, townhome, multi-family, land)
5. Key features — a bullet list of anything notable: upgrades, finishes, views, location perks, recent renovations, lot size, schools, HOA notes
6. Agent name and brokerage (for sign-off in the email variant)

Optional (use if provided, don't ask twice):
7. Asking price
8. Year built
9. Target tone — pick one: warm-professional (default), luxury, investor-focused, first-time-buyer-friendly, fast-sale-urgency
10. Preferred CTA contact (phone, email, showing link)

## Step 2 — Generate all four deliverables

Produce every deliverable in a single response, clearly labeled with H2 headers. Never skip a deliverable.

### MLS Listing Description (primary)
- Length: 150–220 words
- Opens with a strong hook that names the neighborhood OR a standout feature — never generic ("Welcome home!" is banned)
- Middle walks through interior highlights (kitchen, primary suite, living spaces), then exterior/location
- Closes with a clear call to action ("Schedule your private tour today")
- Active verbs, short sentences, specific nouns (granite counters, not "nice counters")
- No superlatives unsupported by the inputs

### Instagram Caption
- ~100 words
- 2–3 emojis maximum, placed for rhythm not decoration
- Opens with a hook line
- CTA: "DM me for a private showing" or "Link in bio to tour"
- 8 relevant hashtags at the end, mixing broad (#realestate), city-specific (#austinrealestate), and niche (#midcenturymodern)
- **Tone changes voice and sentence rhythm, not just adjectives:** warm-professional = conversational, occasional wit, natural pacing; luxury = precise, understated, no slang or contractions; investor-focused = data-forward, minimal flourish; first-time-buyer-friendly = encouraging, jargon-free, shorter sentences; fast-sale-urgency = punchy, imperative verbs, tight rhythm. Match the agent's brand — quirky asides belong only in warm-professional.

### Facebook / Long-Form Social Post
- ~150 words
- More narrative, first-person from the agent's voice
- Tell a mini-story: what makes this home special, who it's perfect for (without naming protected classes)
- CTA: ask for a comment or click

### Email Blast
- Subject line: ≤ 60 characters, curiosity or specificity (avoid all-caps, avoid "!!")
- Preheader: ≤ 100 characters, complements subject, doesn't repeat it
- Body: ~120 words, first-person from the agent, one clear CTA with a placeholder link `[SHOWING_LINK]`
- Sign-off with agent name and brokerage

## Step 3 — Fair Housing compliance (non-negotiable)

Never include or imply:
- Any reference to race, color, religion, national origin, sex, familial status, or disability
- Phrases like "perfect for families," "safe neighborhood," "Christian community," "walking distance to [school]" (school references require extreme care — stick to district names, never walkability claims)
- Adjectives that imply exclusion ("exclusive," "private" are OK; "restricted," "traditional families" are not)

If a feature in the input describes residents rather than the property (e.g., "great for young professionals"), reframe to describe the property itself ("close to downtown nightlife and transit").

## Step 4 — Style guardrails

- Never invent features not present in the inputs. If the inputs don't mention a pool, don't write about a pool.
- Match the requested tone exactly. Luxury ≠ flowery; it means specific, confident, understated.
- Avoid clichés: "must see," "one of a kind," "won't last long," "move-in ready" (unless literally stated), "charming"
- Prefer em-dashes over semicolons; prefer periods over both

## Step 5 — Offer follow-ups

After delivering the package, ask once:
- "Want a shorter/punchier version of any of these?"
- "Want a matching 'Just Listed' flyer headline set?"
- "Want me to retune for a different tone?"

Do not auto-regenerate unless asked.

## Example run

**User input:**
> 4521 Mesa Dr, Austin TX. 3bd/2ba, 1,850 sqft, built 1962, mid-century modern, just renovated. Features: new kitchen with quartz + Bosch appliances, original terrazzo floors restored, floor-to-ceiling windows, xeriscaped yard, detached studio, walking distance to Mueller Lake Park area. Asking $785k. Agent: Dani Lopez, Claw Realty. Tone: warm-professional.

**Skill output (abbreviated):**

*MLS:* "Set behind xeriscaped landscaping on a quiet Mesa Drive lot, this 1962 mid-century modern has been brought into its second life. The renovated kitchen pairs quartz countertops with Bosch appliances, while restored original terrazzo floors run through the main living spaces. Floor-to-ceiling windows pull daylight across the great room and frame the landscaped yard. Three bedrooms, two full baths, and 1,850 sqft of thoughtful interior space are complemented by a detached studio — home office, guest suite, or creative room. Walkable to Mueller-area shops, restaurants, and green space. Schedule your private tour today."

*Instagram:* "✨ Just listed at 4521 Mesa Dr. A 1962 mid-century, reborn..." (continues)

*Facebook:* (continues)

*Email:* Subject: "4521 Mesa Dr — mid-century, quietly reimagined"
