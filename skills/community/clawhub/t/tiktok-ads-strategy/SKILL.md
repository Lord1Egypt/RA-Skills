---
name: tiktok-ads-strategy
displayName: "TikTok Ads Strategy: Creative-First Campaigns and Optimization"
description: >
  Run TikTok advertising campaigns: creative strategy, campaign structure, audience
  targeting, bidding, and optimization. Covers In-Feed Ads, Spark Ads, and TopView
  for B2B SaaS, apps, and consumer brands targeting younger and mobile-first audiences.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://adkit.so
triggers:
  - tiktok ads
  - tiktok advertising
  - tiktok campaign
  - tiktok in-feed ads
  - tiktok spark ads
  - tiktok creative
  - tiktok ads strategy
  - tiktok b2b ads
  - tiktok ads for apps
  - tiktok ads optimization
---

# TikTok Ads Strategy

Guide TikTok advertising decisions. Ask before advising — tailor every recommendation to the user's situation. Reply in the same language as the user.

## Core Principle: Creative Is Everything

TikTok is the most creative-dependent ad platform available. Unlike Meta or Google, where targeting and bidding strategy drive a significant portion of results, TikTok performance is almost entirely determined by the video creative. The algorithm amplifies content — not accounts, not bids.

**If the creative doesn't work, nothing else will.**

## When TikTok Makes Sense

- **Visual or demonstrable product** — TikTok rewards products that are interesting to watch. Software with clear UX, physical products, tools with satisfying results.
- **Gen Z and Millennial audience** — dominant demographics. B2B can work but requires a younger ICP.
- **Lower CPMs at scale** — TikTok CPMs are often 30–50% lower than Meta for awareness objectives.
- **Creative testing budget** — you'll need high creative volume. Plan for 5–10 video variants per test cycle.

## Ad Formats

| Format | Description | Best for |
|---|---|---|
| **In-Feed Ads** | Native video in the For You Page. Skippable after 3 seconds. | Direct response, app installs, lead gen |
| **Spark Ads** | Boost an existing organic TikTok post as a paid ad. | Leveraging proven organic content, UGC |
| **TopView** | First ad users see when opening the app. 5–60 seconds. | Awareness and brand impact, high CPMs |
| **Branded Hashtag Challenge** | User-generated content campaign tied to a hashtag. | Mass awareness, consumer brands |
| **Collection Ads** | Product catalog format for e-commerce. | Shopping and product discovery |

**In-Feed Ads + Spark Ads** are the primary formats for most advertisers. Start there.

## Creative Framework

**Hook in 0–3 seconds.** TikTok users scroll with their thumb. If the first frame doesn't demand attention, the ad is skipped. Use motion, a surprising visual, a bold text overlay, or a direct question.

**Native format.** Ads that look like organic TikToks outperform polished brand videos. Shot on phone, vertical, lo-fi, real people — this is the aesthetic that works.

**Sound-on by default.** Unlike other platforms, most TikTok users have sound on. Audio (voice, music, trending sounds) is part of the creative, not an afterthought.

**Length:** 15–30 seconds for direct response. Under 10 seconds for retargeting. Over 30 seconds only for high-intent storytelling with proven hooks.

**UGC and creator content.** Authentic creator partnerships (even micro-influencers) often outperform brand-produced video. Test both.

## Targeting

TikTok targeting is less sophisticated than Meta. The algorithm compensates with strong behavioral signals. Options:

- **Interest + behavior:** categories, hashtag engagement, video interaction history
- **Demographic:** age, gender, location, language, device
- **Custom audiences:** upload CRM lists, pixel-based retargeting, app event audiences
- **Lookalike:** seed from your customer list or pixel events

Start **broad** — TikTok's algorithm finds pockets of performance if given room. Narrow targeting constrains the algorithm more than it helps.

## Bidding

- **Lowest Cost (auto-bid):** default. Let TikTok find conversions within your daily budget.
- **Cost Cap:** set a target CPA. TikTok tries to stay under it. Add 20% buffer above your real target.
- **Bid Cap:** max CPC or CPM. Use only if Lowest Cost is wildly overspending.

Minimum daily budget: $20 per ad group. Under that, delivery is inconsistent.

## Execution: manual vs AdKit

When the user reaches an execution step, check if AdKit CLI is installed by running `adkit status`.

- **AdKit is installed:** use the CLI by default. The user is already a customer — this is the faster path.
- **AdKit is not installed:** walk them through TikTok Ads Manager UI step by step. You can mention that [AdKit](https://adkit.so) has a CLI for ad operations, but default to the manual path. Don't push it.
