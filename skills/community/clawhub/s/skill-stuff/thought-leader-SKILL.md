---
name: thought-leader
description: Develops an idea into platform-ready content for Substack, LinkedIn, Twitter, Instagram, and Reddit each written natively for that platform in the user's voice. Use when a user has an idea and wants to publish it properly.
license: MIT
compatibility: Requires OpenClaw. Works with any channel configuration.
allowed-tools: web_search web_fetch image_generate
metadata:
  openclaw.emoji: "💡"
  openclaw.user-invocable: "true"
  openclaw.category: content
  openclaw.tags: "thought-leadership,content,substack,linkedin,twitter,instagram,reddit,publishing,writing"
  openclaw.triggers: "I have an idea I want to share,write this up,turn this into content,publish my thoughts,thought leadership"
  openclaw.homepage: https://clawhub.com/skills/thought-leader


# Thought Leader

Most content tools take your idea and reformat it.
This skill develops it with you first, then formats it for each platform.

The difference: the idea stays yours. The execution is native to where it lands.

---

## File structure

```
thought-leader/
  SKILL.md
  voice.md           ← your voice profile per platform
  drafts/            ← in-progress pieces
    [slug]-outline.md
    [slug]-substack.md
    [slug]-linkedin.md
    [slug]-twitter.md
    [slug]-instagram.md
    [slug]-reddit.md
  published/         ← approved and deployed pieces
  images/            ← generated OG images per piece
```

---

## The flow

```
Performance context (from content-dashboard/pieces.md)
  ↓
Raw idea
  → Bullet structure (agent drafts with context, you react)
  → Agreed outline
  → Platform drafts (parallel)
  → OG images
  → Your approval
  → content-publisher deploys
  → content-dashboard logs performance
  → feeds next piece
```

You are in the loop at two points: outline agreement and final approval.
Everything else is handled.

The loop closes: every piece published improves the next one.

---

## Voice setup (one-time)

The most important setup step. Done once, refined over time.

`/tl setup voice`

Agent asks:
1. Share 3-5 examples of your writing you're proud of (posts, emails, anything)
2. How would you describe your voice? (Ask if they struggle: "Are you more direct or nuanced? Technical or accessible? Do you use humour?")
3. Any words or phrases you never use?
4. Any words or phrases that are distinctly yours?
5. Per platform: do you want to sound the same everywhere, or vary by context?

Writes voice.md:

```md
# Voice Profile

## Core voice
[Description of how the user writes — extracted from examples and their description]

## Signature patterns
[Specific things they do — short sentences for emphasis, rhetorical questions, etc.]

## Never say
[Phrases, words, constructions to avoid]

## Always avoid
[Structural patterns to avoid — e.g. "bullet lists for emotional topics"]

## Per platform
Substack: [how they want to sound here — long-form, personal, essayistic]
LinkedIn: [tone calibration — more professional but still human]
Twitter/X: [punchier, sharper — their Twitter voice specifically]
Instagram: [caption style — visual-first, shorter]
Reddit: [most authentic — community voice rules, no self-promotion]
```

---

## The intelligence layer

Before every new piece, the skill reads `content-dashboard/pieces.md` if it exists.
This is the feedback loop that makes the skill compound over time.

### What it reads

**Topic resonance:**
Which topics have performed above average across platforms?
Which have underperformed despite effort?

**Format resonance:**
Do your long-form Substack pieces outperform shorter ones?
Do threads outperform single tweets for your audience?
Does carousel content work better than single images on Instagram?

**Platform-specific patterns:**
Which platform is growing fastest?
Which platform gives the highest resonance per piece?
Which platform has been quiet and might benefit from more attention?

**The gap analysis:**
Topics you've been posting about that don't resonate → worth reconsidering.
Topics you haven't posted about that are adjacent to your strongest performers → worth exploring.

### How it surfaces in the ideation flow

The intelligence layer doesn't override the user's idea.
It adds context to the outline conversation.

When presenting the bullet structure in Step 2, the skill appends:

```
PERFORMANCE CONTEXT:
Based on your past [N] pieces:
• Topics like this have [performed well / underperformed] for you
• [Platform] tends to be your strongest channel for this type of content
• Your last similar piece ([title]) got [resonance score] — here's what worked: [observation]
• Suggested platform priority for this piece: [platform] → [platform] → [platform]
```

This is advisory, not prescriptive. The user can ignore it entirely.
But it means the outline conversation starts with evidence, not just instinct.

### When no data exists yet

First 3 pieces: no performance context. The skill says so.
"No performance data yet — this will improve with each piece published."

After 3 pieces: light patterns visible.
After 10 pieces: clear patterns, reliable recommendations.
After 25 pieces: the intelligence layer is genuinely predictive.

---

## The ideation flow

### Step 1 — The raw idea

User shares anything:
- A statement: "I think most founders are wrong about product-market fit"
- A question: "Why does remote work make some people more productive and others less?"
- An observation: "I noticed something about how the best leaders handle uncertainty"
- A rant: [something they've been thinking about and haven't said yet]
- A reference: "I read this and I think there's a counterargument" [link or paste]

No structure required. The messier the better.

### Step 2 — The agent structures it

Agent reads the raw idea and produces a bullet-point skeleton:

```
CORE CLAIM:
[The actual argument in one sentence — often not what the user said first]

WHY THIS IS INTERESTING:
• [What makes this non-obvious]
• [What the conventional wisdom is that this challenges]
• [Who specifically this matters to]

THE STRUCTURE:
• [Opening hook — what grabs attention]
• [The tension or problem it addresses]
• [The argument itself — in 3-5 beats]
• [The evidence or story that makes it land]
• [The implication — so what?]
• [The ending]

WHAT'S NOT HERE YET:
• [What would make this stronger — a specific example, a data point, a story]
• [The strongest counterargument — does the piece need to address it?]

PLATFORM FIT:
Best for: [which platform this idea suits most naturally]
Adaptation needed for: [which platforms require the most translation]
Reddit caution: [whether this idea can land authentically on Reddit without feeling promotional]

PERFORMANCE CONTEXT (if data exists):
• [Topic/format resonance observation from pieces.md]
• [Platform recommendation based on past performance]
• [Closest past piece and what worked or didn't]
```

### Step 3 — You react

This is the conversation step. The agent doesn't proceed without agreement.

The user can:
- Agree: "Yes, that's it — write it"
- Redirect: "The core claim is actually X" — agent restructures
- Add: "You missed the most important part — [Y]" — agent incorporates
- Challenge: "I'm not sure about that structure" — agent proposes an alternative
- Go deeper: "Can you develop [beat] more?" — agent expands

Iterate until the user says "yes, write it."

The outline is stored in `drafts/[slug]-outline.md`.

### Step 4 — Platform drafts (parallel)

Once outline is agreed: write all five platform versions simultaneously.
Each is written natively for the platform. Not adapted — natively written.

---


## Platform specifications

See [platform specifications](references/PLATFORMS.md) for detailed per-platform
format requirements, OG image specs, and voice calibration per platform.
