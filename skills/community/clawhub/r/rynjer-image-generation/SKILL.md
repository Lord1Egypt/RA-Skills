---
name: rynjer-image-generation
version: 0.3.0
summary: Agent-first marketing image generation — templates for landing/ad/blog/ecommerce, smart size recommendations, prompt rewrite, cost estimate, and fast execution.
---

# Agent-first Marketing Image Generation

**不是大而全创作平台，而是面向 Agent 和工作流的短路径出图工具。**

---

## Why install this

Use this skill when you need a **usable marketing image fast**, with a low-friction path from:

**rough request → prompt rewrite → cost estimate → image**

This skill is built for:
- landing page hero images
- blog and article covers
- ad creative variations
- ecommerce product visuals
- any agent workflow that needs quick, predictable image outputs

### What makes this different

| Others | Rynjer |
|--------|--------|
| Creative playground, explore options | Execute task, get usable result |
| Manual prompt engineering | Auto rewrite from rough input |
| Generate first, cost unknown | Cost estimate before execution |
| Project-based studio workflow | Short path API for agents |
| Guess platform specs | Smart size recommendations built-in |

---

## Quick Start — Use a Template

Fastest way to get started with optimized defaults:

```javascript
// Generate a landing page hero image
await rynjer.generate_image({
  goal: "SaaS product homepage",
  prompt: "AI-powered analytics dashboard, modern tech style",
  use_case: "landing",
  template: "landing",  // Auto-applies 16:9, 2K, landing-optimized style
  quality_mode: "balanced",
  count: 1
});
```

**Available templates:**
- `landing` — Landing page hero (16:9, 2K)
- `ad` — Social media ads (1:1, 1K)
- `blog` — Blog/article covers (16:9, 1K)
- `ecommerce` — Product images (1:1, 2K)

---

## Start here — 4 steps to your first image

1. **rewrite_image_prompt** — describe your goal, get a better prompt
2. **estimate_image_cost** — see cost before spending credits
3. **generate_image** — execute with your approved prompt and budget
4. **poll_image_result** — wait for completion and get the result

---

## What it does

### Rewrite image prompts
Turn rough requests into optimized prompts for business and marketing use.

**Input:**
- `goal` — what you need the image for
- `raw_prompt` — your rough description
- `use_case` — landing page, blog cover, ad creative, etc.
- `template` (optional) — apply template defaults
- `tone` (optional) — brand voice or mood
- `audience` (optional) — target audience

**Output:** ready-to-generate prompt optimized for your use case.

### Estimate image cost
Know the cost before you commit. Essential for budget-aware agent workflows.

**Input:**
- `use_case`
- `count` — how many images
- `resolution` — 1K, 2K, 4K
- `aspect_ratio` — 16:9, 1:1, 9:16, etc.
- `quality_mode` — fast, balanced, high
- `template` (optional) — auto-apply template defaults
- `platform` (optional) — get platform-optimized recommendations

**Output:** estimated credits required.

### Smart size recommendations
Get platform-optimized size settings without guesswork.

```javascript
// Get Instagram post recommendations
await rynjer.recommend_image_size({
  platform: "instagram_post"
});
// Returns: { aspect_ratio: "1:1", resolution: "1K", size_px: "1080x1080" }
```

**Supported platforms:**
- `instagram_post` — 1:1, 1080x1080
- `instagram_story` — 9:16, 1080x1920
- `facebook_ad` — 1.91:1, 1200x628
- `twitter_card` — 1.91:1, 1200x628
- `linkedin_ad` — 1.91:1, 1200x627
- `blog_cover` — 1.91:1, 1200x630
- `youtube_thumbnail` — 16:9, 1280x720
- `app_store` — 16:9, 1920x1080

### Generate images
Execute generation with your approved prompt and budget.

**Input:**
- `prompt` — rewritten or custom
- `use_case`
- `template` (optional) — apply template defaults
- `platform` (optional) — use platform-optimized settings
- `aspect_ratio`
- `resolution`
- `quality_mode`
- `count`
- `auto_poll` (optional)

**Output:** generation request submitted.

### Poll image results
Check status and download completed images.

**Input:**
- `request_id`

**Output:** image URLs or download ready.

---

## Templates — One-line setup

Templates automatically configure optimal settings for common use cases:

| Template | Aspect Ratio | Resolution | Best For |
|----------|--------------|------------|----------|
| `landing` | 16:9 | 2K | Homepage hero, product showcases |
| `ad` | 1:1 | 1K | Social media ads, quick tests |
| `blog` | 16:9 | 1K | Article covers, content marketing |
| `ecommerce` | 1:1 | 2K | Product images, white backgrounds |

**Usage:**
```javascript
// Use template
generate_image({ template: "ecommerce", ... })

// Use template + override specific settings
generate_image({ 
  template: "ad", 
  aspect_ratio: "16:9",  // Override template default
  ... 
})
```

---

## Best for

| Use Case | Why it works |
|----------|--------------|
| **Landing page hero** | Fast iteration on homepage visuals |
| **Blog/article cover** | Consistent cover images at scale |
| **Ad creative variations** | Test multiple concepts cheaply |
| **Ecommerce visuals** | Product images, lifestyle shots |
| **Social posts** | Quick turnaround for content calendars |

---

## Good fit

Use this skill when:
- You need **usable images fast**, not artistic exploration
- You want **cost predictability** before generation
- You're building an **agent workflow** that needs image generation
- You want to **skip manual model selection** and prompt tuning
- You're producing **marketing assets** (landing, blog, ads, ecommerce)
- You want **smart defaults** without guessing platform specs

---

## Not a good fit

This v1 is **intentionally not** designed for:
- video generation
- music/audio generation
- complex multi-step creative pipelines
- large-scale brand asset management systems
- creator studio workflows with collaboration features

**For those, consider full creative platforms instead.**

---

## Reality check

This is:
- soft launch
- early-access
- image-only v1

The core flow (rewrite → estimate → generate → poll) is live and verified. Templates and smart recommendations are ready for use. It works for real tasks, but the clearest path is still the recommended workflow above.

---

## Pricing

- **Free:** prompt rewrite, routing help, cost estimate, size recommendations
- **Paid:** image generation via Rynjer credits or API access

---

## Positioning

Rynjer is **not** a generic creative playground or full studio platform.

It is a **business-facing image generation entry point** focused on:
- low-friction execution
- predictable cost
- smart defaults (templates + platform recommendations)
- default routing over manual model-picking
- repeatable, workflow-ready use

**If you need a full creative studio with video, storyboards, and collaboration — this isn't it.**
**If you need fast, cost-transparent image generation for marketing tasks — this is.**
