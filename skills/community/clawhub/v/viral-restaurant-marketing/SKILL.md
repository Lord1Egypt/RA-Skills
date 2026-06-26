---
name: viral-restaurant-marketing
version: 1.0.0
description: >
  Use this skill when a restaurant owner or marketer needs help with:
  viral TikTok/Instagram content strategy, content calendar generation,
  hook writing, Google Reviews growth, or website conversion optimization.
  Built on real results: millions of views achieved for restaurant clients.
  Triggers on keywords like "restaurant marketing", "TikTok restaurant",
  "viral food content", "restaurant social media", "meer klanten restaurant",
  "restaurant Instagram", "restaurant TikTok", "Google Reviews restaurant".
author: Momo (Ayman's AI Partner)
category: marketing
tags:
  - restaurant
  - tiktok
  - instagram
  - viral
  - social-media
  - content-marketing
  - google-reviews
  - website-conversion
scripts:
  - scripts/generate-content-calendar.js
  - scripts/restaurant-hooks.js
references:
  - references/viral-formulas.md
  - references/pricing.md
---

# 🍽️ Viral Restaurant Marketing Skill

> Built on real results: millions of organic views for restaurant clients in Belgium & Netherlands.
> This skill packages battle-tested strategies into an executable workflow.

---

## When To Use This Skill

Activate this skill when the user:
- Owns or manages a restaurant and wants more customers
- Needs a TikTok/Instagram content strategy
- Wants to generate viral hooks for food content
- Needs a weekly content calendar
- Wants to boost Google Reviews
- Needs website conversion improvements
- Asks about restaurant marketing in general

---

## Workflow Overview

```
Step 1 → Niche Analysis       (understand the restaurant)
Step 2 → Content Calendar     (3-5 posts/week plan)
Step 3 → Hook Generation      (viral-first content ideas)
Step 4 → Platform Strategy    (TikTok vs Instagram approach)
Step 5 → Google Reviews       (reputation snowball system)
Step 6 → Website Conversion   (turn visitors into bookings)
Step 7 → Scheduling & Analytics (Postiz integration + tracking)
```

---

## Step 1: Restaurant Niche Analysis

**Run first. Always. No generic content — everything is niche-specific.**

Ask the user (or extract from context):
1. **Restaurant type**: kebab / sushi / pizza / burger / fine dining / bistro / vegan / Asian fusion / etc.
2. **Location**: city + neighborhood (affects local hashtags and Google strategy)
3. **Unique factor**: what makes them different? (family recipe, secret sauce, open kitchen, etc.)
4. **Current following**: 0-500 / 500-5K / 5K-50K / 50K+
5. **Content capacity**: can they film daily, 3x/week, or only weekends?
6. **Target audience**: families, students, young professionals, foodies, date-night crowd

**Use the niche to determine the content angle:**

| Restaurant Type | Winning Content Angle |
|---|---|
| Kebab / Fast Food | Speed + size + value ("you won't believe how big this is") |
| Sushi / Japanese | Aesthetics + craft + ASMR cutting sounds |
| Pizza | Cheese pulls, dough tossing, oven reveal |
| Burger | Stack builds, sauce drip, cross-section reveal |
| Fine Dining | Plating process, chef's hands, behind the curtain |
| Vegan / Healthy | Transformation (this is 100% plant-based?!) |
| Family/Traiteur | Nostalgia, grandmother's recipe, emotional storytelling |
| Bakery / Patisserie | Satisfying processes: croissant layers, glaze pours |

---

## Step 2: Content Calendar Generator

**Run the script to generate a full week plan:**

```bash
node skills/viral-restaurant-marketing/scripts/generate-content-calendar.js \
  --type "pizza" \
  --location "Leuven" \
  --frequency 4 \
  --output weekly
```

Or call the function directly in agent context:

```javascript
const { generateCalendar } = require('./scripts/generate-content-calendar.js');
const calendar = generateCalendar({
  restaurantType: 'pizza',
  location: 'Leuven',
  postsPerWeek: 4,
  platforms: ['tiktok', 'instagram']
});
console.log(calendar);
```

**Manual Calendar Template (if not using script):**

| Day | Format | Hook Type | Platform | CTA |
|---|---|---|---|---|
| Monday | Behind the scenes | Curiosity ("you never see this at restaurants") | TikTok + Reels | Comment your order |
| Wednesday | Product showcase | Sensory ("the sound of this pizza") | TikTok | Tag someone you'd bring |
| Friday | Staff/Chef story | Emotional ("he's been making this for 20 years") | Reels | Save for your next date |
| Saturday | Before/After | Transformation ("raw → ready in 90 seconds") | TikTok | Share if you want this |

**Content Frequency Guidelines:**
- **0-1K followers**: Post 5x/week minimum. Volume beats quality at this stage.
- **1K-10K followers**: 4x/week. Mix hooks with proof (reviews, reactions).
- **10K-50K followers**: 3x/week. Quality over quantity. Repurpose best performers.
- **50K+ followers**: 2-3x/week. One hero video/week + 2 supporting.

---

## Step 3: Viral Hook Generation

**Run the hook generator:**

```bash
node skills/viral-restaurant-marketing/scripts/restaurant-hooks.js \
  --type "sushi" \
  --hook-style "curiosity" \
  --count 10
```

**The 7 Hook Formulas That Work For Restaurants:**

### Formula 1: The Forbidden Reveal
> "What [restaurant type] doesn't want you to know about [their product]"
- Example: "What sushi restaurants don't want you to know about their salmon"
- Works because: triggers curiosity + slightly controversial

### Formula 2: The Size/Value Shock
> "I paid €[price] and got THIS much [food]"
- Example: "I paid €12 and got THIS much pizza 🍕"
- Works because: relatability + value validation

### Formula 3: The Process Hypnosis
> (No text needed — just the sound + visual of: dough stretching, cheese melting, knife cutting)
- Works because: ASMR effect, watch time stays high, algorithm loves it

### Formula 4: The Transformation
> "Raw → [finished dish] in [time] — watch till the end"
- Example: "Raw tuna → €35 sashimi plate in 45 seconds"
- Works because: completion bait + satisfying payoff

### Formula 5: The Emotional Story
> "He's been making this dish for [X] years. Here's why he never changed the recipe."
- Works because: human connection, shares, saves

### Formula 6: The Challenge/Comparison
> "We tried every [dish] in [city]. This one won."
- Example: "We tried every kebab in Leuven. This one is on another level."
- Works because: local pride + shareability + FOMO

### Formula 7: The Reaction
> Film real customer reactions (first bite, surprise at portion size, etc.)
- Works because: social proof + authentic emotion = trust

---

## Step 4: Platform Strategy

### TikTok Strategy

**Algorithm rules for restaurants:**
1. First 2 seconds must have motion OR text hook on screen
2. Use trending audio (check TikTok Creative Center weekly)
3. Caption should ask a question to drive comments
4. Post between 17:00-20:00 local time (dinner decision window)
5. Reply to every comment in first 30 minutes (boosts distribution)

**TikTok Slideshow Templates:**
- Slides 1-3: Hook + build up (problem/curiosity)
- Slides 4-6: The reveal / process / story
- Slide 7-8: Social proof (reviews, reactions)
- Slide 9: CTA ("Where are you ordering from tonight? 👇")

**Best performing restaurant formats on TikTok:**
1. POV: You work at [restaurant] for a day
2. Day in the life of our chef
3. What €20 gets you at [restaurant] vs [expensive competitor]
4. Rating our own dishes honestly
5. Customer's first reaction to [signature dish]

### Instagram Reels Strategy

**Key differences from TikTok:**
- Slightly more polished/aesthetic than TikTok
- Stories convert better to bookings (use "Reserve" sticker)
- Hashtag research matters more than TikTok
- Carousel posts (product menus, story behind dish) perform well

**Instagram Hashtag Strategy:**
- 5 hyper-local: `#leuven #leuvenrestaurant #leuveneten #uitloven #levensgenotensleuven`
- 5 niche: `#pizzalover #pizzabelgium #artisanpizza #woodfiredpizza #napolipizza`
- 5 broad food: `#foodie #foodporn #instafood #foodlovers #belgianfood`
- Total: 15 hashtags (sweet spot — not spammy, still reach)

**Instagram Stories for Conversion:**
1. Poll: "Wil jij dat we [dish] toevoegen?" (engagement)
2. Countdown to new menu / event
3. Behind the scenes during prep (10-15 sec clips)
4. Swipe-up / link sticker to menu/reservation

---

## Step 5: Google Reviews Boost Strategy

**The Snowball System — from 10 to 200+ reviews in 3 months:**

### Phase 1: Foundation (Week 1-2)
1. Claim and fully optimize Google Business Profile:
   - 20+ photos (interior, food, team, menu)
   - Complete hours, menu link, website
   - Add products/services
   - Enable messaging
2. Ask your top 10 regulars personally (WhatsApp/in person) for a review
3. Target: 10-15 reviews to start (social proof baseline)

### Phase 2: Systems (Week 3-4)
1. Create a QR code linking directly to your Google review page
   - Place on: table cards, receipts, packaging, menu
   - Script for staff: "If you enjoyed your meal, a Google review helps us a lot 🙏"
2. WhatsApp broadcast to existing contacts (if you have a group)
3. Add review link to Instagram bio and Stories

### Phase 3: Snowball (Month 2-3)
1. Reply to EVERY review (Google rewards this with visibility)
2. Run a monthly "Win a free meal" contest — entry = Google review
3. Feature 5-star reviews in TikTok/Reels content ("Our customers said...")
4. Each new video brings new visitors → more reviews → higher Maps ranking

**Review Response Templates:**
- Positive: "Dankjewel [naam]! 😊 We kijken ernaar uit je snel terug te zien. [Handtekening Chef]"
- Negative: "Bedankt voor je feedback [naam]. We nemen dit serieus en doen ons best dit te verbeteren. Stuur ons een DM zodat we het kunnen rechtzetten."

---

## Step 6: Website Conversion Optimization

**The Restaurant Website must do ONE job: turn visitors into customers NOW.**

### Critical Conversion Elements:

**1. Hero Section (above the fold)**
- High-quality food photo (NOT stock photo — real dishes)
- Clear value prop: "De beste [cuisine] van [stad]"
- TWO CTAs: "📋 Bekijk menu" + "📅 Reserveer nu"
- No more than 3 seconds to understand what you offer

**2. Menu Page**
- Mobile-first (80%+ of traffic is mobile)
- Photos for every dish or at least per category
- Prices visible (hiding prices = trust killer)
- "Meest besteld" / "Chef's keuze" labels
- Direct link to order (Deliveroo / own system / WhatsApp)

**3. Social Proof Section**
- Google Reviews widget (embed top 5 reviews)
- Instagram feed embed (shows life at restaurant)
- "X tevreden klanten" counter
- Press mentions / awards if available

**4. Booking Flow**
- Embedded reservation form (not a phone number alone)
- Options: online booking widget OR WhatsApp button (Belgian market loves WhatsApp)
- Show available times directly
- Confirm via WhatsApp/email immediately

**5. Local SEO on Website**
- Title tag: "[Naam restaurant] - [cuisine] in [stad] | Reserveer online"
- Every page has location keywords naturally in text
- Schema markup: Restaurant type, address, hours, menu
- Google Maps embed on contact page

**6. Speed & Mobile**
- Page load < 3 seconds (use Lovable hosting or Vercel)
- Images compressed (< 200KB each)
- No autoplay video on mobile
- Tap targets min 44px (easy to tap buttons)

---

## Step 7: Scheduling & Analytics with Postiz

### Postiz Setup (Scheduling)

Postiz is the recommended scheduling tool for this workflow.

**Setup steps:**
1. Connect TikTok, Instagram accounts to Postiz
2. Set up content pipeline: Draft → Review → Scheduled → Posted
3. Create recurring time slots: Mon/Wed/Fri/Sat at optimal times
4. Use Postiz calendar view to see full week at a glance

**Optimal posting times (Belgium/Netherlands):**
- TikTok: 17:30, 19:00, 21:00
- Instagram Reels: 11:00, 17:00, 20:00
- Instagram Stories: 08:00, 13:00, 21:00

**Postiz API Integration (if automating):**
```javascript
// Post via Postiz API
const response = await fetch('https://api.postiz.com/v1/posts', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.POSTIZ_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    content: hookText,
    scheduledAt: scheduledTime,
    platforms: ['tiktok', 'instagram'],
    mediaUrls: [videoUrl]
  })
});
```

### Analytics Tracking

**Weekly metrics to track (every Sunday):**

| Metric | Tool | Target |
|---|---|---|
| Video views | TikTok/Instagram analytics | Week-over-week growth |
| Follower growth | Platform analytics | +50-200/week |
| Profile visits | Instagram Insights | Conversion to website |
| Website visits | Google Analytics | From social traffic |
| Reservations | Booking system | Tied to content peaks |
| Google Reviews | Google Business | +2-5/week |
| Top performing video | Platform analytics | Repurpose & iterate |

**The Iteration Loop:**
1. Every Sunday: pull top 3 performing videos
2. Ask: what format? what hook? what time posted?
3. Make 2-3 more videos with the same formula
4. Test ONE new format per week
5. Kill what doesn't work after 2 videos. Double down on what does.

---

## Quick Start Checklist

For a new restaurant client, complete in this order:

- [ ] Fill in niche analysis (Step 1)
- [ ] Run `generate-content-calendar.js` for first 2 weeks
- [ ] Run `restaurant-hooks.js` to get 20 hook options
- [ ] Film 5 videos before posting any (content buffer)
- [ ] Optimize Google Business Profile
- [ ] Add QR review code to table/receipt
- [ ] Audit website with conversion checklist
- [ ] Connect Postiz and schedule first week
- [ ] Set tracking dashboard (weekly Sunday ritual)

---

## Pro Tips (From Real Client Experience)

1. **Post the ugly truth**: the busiest kitchen, the mess, the rush — people love authenticity
2. **Film during the prep**: morning prep is gold — no customers, clean angles, real process
3. **Let the chef talk**: 10 seconds of the chef saying why he loves this dish = magic
4. **Don't chase trends blindly**: trending audio helps but a great hook with wrong audio still wins
5. **1 viral video changes everything**: keep posting until you hit it, then capitalize immediately
6. **Reply to comments fast**: TikTok pushes posts that get early engagement
7. **Cross-post everything**: TikTok → Instagram Reels → YouTube Shorts — same video, 3x the reach
8. **Consistency beats perfection**: 3 "good enough" videos/week beats 1 perfect video/month

---

## Integration Notes

- **Lovable**: use for restaurant website builds (Chef's preferred tool)
- **Claude Code**: for adding chatbot / AI reservation assistant to website
- **Upload-Post skill**: for when content is approved and ready to post
- **Google Sheets skill**: for tracking leads and content performance
- **Postiz**: primary scheduling tool (connect via POSTIZ_API_KEY)

---

*Skill version 1.0.0 — Built by Momo for Ayman's AI Agency*
*Based on real results: millions of views, 3-5 satisfied restaurant clients in Belgium*
