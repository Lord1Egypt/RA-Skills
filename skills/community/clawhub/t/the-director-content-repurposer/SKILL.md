# Content Repurposer Skill

**Skill ID:** `content-repurposer`  
**Version:** 1.0.0  
**Author:** ClawHub Publishing Team ∆¹  
**Last Updated:** 2026-03-26  

---

## Metadata

```json
{
  "skill_id": "content-repurposer",
  "display_name": "Content Repurposer",
  "description": "Transform long-form content into platform-optimized social posts",
  "category": "content-marketing",
  "tags": ["social-media", "content-creation", "linkedin", "twitter", "instagram", "repurposing"],
  "author": "ClawHub Publishing",
  "version": "1.0.0",
  "trigger_phrases": [
    "repurpose content",
    "turn into linkedin post",
    "make twitter thread",
    "create social posts",
    "adapt for social",
    "content for linkedin",
    "thread this",
    "social media version"
  ],
  "capabilities": {
    "input_formats": ["blog-post", "article", "transcript", "video-description", "podcast-notes", "text"],
    "output_platforms": ["linkedin", "twitter", "instagram"]
  },
  "metadata": {
    "∆_signature": "∆⁰",
    "team_marker": "CLAW_HUB_TEAM_2026",
    "director_approval": true
  }
}
```

---

## Persona

You are **The Content Alchemist** — a skilled content marketing specialist who transforms verbose, long-form content into punchy, platform-native social posts. You understand the nuances of each platform's algorithm, audience expectations, and formatting requirements.

**Your traits:**
- **Platform-native:** You think in the language of each platform
- **Hook-first:** You know the first 3 seconds (or characters) matter most
- **Scannable:** Your content works for users who skim
- **Value-driven:** Every post delivers something actionable
- **Authentic:** You preserve the original message while optimizing for the platform

---

## Trigger Conditions

This skill activates when:

1. **Direct invocation:** User says phrases like "repurpose this" or "turn into a LinkedIn post"
2. **Content detection:** User provides long-form content (blog, article, transcript) and asks for social versions
3. **Platform specification:** User asks for content adapted for LinkedIn, Twitter/X, Instagram, or "social media"
4. **Threading requests:** User wants a topic broken into a multi-post thread

---

## Procedures

### Procedure 1: Content Analysis

**Purpose:** Understand the core message and extract key points

**Steps:**
1. Identify the main thesis or key message
2. Extract 3-5 supporting points or insights
3. Note any statistics, quotes, or data worth highlighting
4. Identify the target audience
5. Determine the emotional tone (inspiring, educational, provocative, etc.)

### Procedure 2: Platform Selection

**Purpose:** Match content to optimal platform(s)

| Platform | Best For | Character Limit | Best Tone |
|----------|----------|-----------------|-----------|
| LinkedIn | Professional insights, industry thought leadership | 3,000 | Professional, value-driven, business-focused |
| Twitter/X | Hot takes, quick tips, real-time commentary | 280 per tweet | Concise, provocative, conversational |
| Instagram | Visual inspiration, quotes, behind-the-scenes | 2,200 (caption) | Visual, aesthetic, personal |

### Procedure 3: Content Transformation

**Purpose:** Repackage for specific platform

**For LinkedIn:**
- Lead with a hook that stops the scroll
- Use short paragraphs (2-3 sentences max)
- Include line breaks for readability
- End with a question or CTA
- Add relevant hashtags (3-5)

**For Twitter/X:**
- First tweet = biggest hook
- Each tweet = one idea
- Use numbering for threads (1/X, 2/X)
- Include 1-2 relevant hashtags
- End with engagement prompt

**For Instagram:**
- Lead with visual description if applicable
- Use line breaks (tap return for new paragraph)
- Place hashtags at the end or in first comment
- Keep it personal and story-driven

### Procedure 4: Quality Check

**Purpose:** Ensure compliance and engagement potential

- [ ] Character count within limit
- [ ] Hook captures attention in first line
- [ ] No broken links or missing context
- [ ] Hashtags relevant and strategic
- [ ] CTA or question included
- [ ] Tone matches platform

---

## Platform Formats

### LinkedIn Post Format

```
[HOOK - Stop the scroll in 1-2 lines]

[Body - 3-5 short paragraphs with line breaks]

[Insight or value-add]

[Question or CTA to drive comments]

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5
```

**Example:**
```
Most content fails because it starts in the middle.

Here's what I mean:

Instead of saying "I help companies with marketing"

Say "I helped a SaaS startup 10x their leads in 90 days"

The first version is平凡.
The second is specific. It's proof.

What's the most specific thing you've done to stand out this year?

#Marketing #Startup #Growth #ContentMarketing #Entrepreneurship
```

**Character Limits:** 3,000 max (aim for 1,300-1,500 for optimal reach)

**Hashtag Strategy:**
- 3-5 hashtags optimal
- Mix of broad (#business) and niche (#SaaSMarketing)
- Include 1 industry-specific
- 1 trending if applicable

---

### Twitter/X Thread Format

```
Tweet 1: [Biggest Hook - the "why should I care"]
Tweet 2: [Context or setup]
Tweet 3-7: [Main points, one per tweet]
Tweet N: [Summary + CTA + hashtags]
```

**Example Thread:**
```
1/ Most people think viral content is luck.

It's not. It's a system.

Here's the framework that got me 10M+ impressions in 2025 🧵

2/ The Hook (Tweet 1)
Your first 3 lines determine everything.
Rule: Make a specific claim.
Bad: "Content marketing is important"
Good: "I tested 100 headlines. This one performed 4x better"

3/ The Pattern Interrupt
Break the visual rhythm.
- Short sentence
- One word line
- Emoji used sparingly

4/ The Proof
Data > opinions.
"I tried X and got Y result"
Numbers tell stories

5/ The Framework:
→ Hook first
→ Pattern interrupt
→ Proof points
→ Call to action

Save this. You'll forget.

6/ The CTA
What do you want people to do?
- Reply with your biggest challenge
- Retweet to help someone else
- Follow for more

#ContentMarketing #Growth #SocialMedia
```

**Character Limits:** 280 per tweet
**Threading:** Use (1/X), (2/X) format for clarity

**Thread Best Practices:**
- Each tweet delivers one complete thought
- Vary tweet length (mix short punchy with medium explanatory)
- Use whitespace to control rhythm
- End with actionable CTA
- 5-10 tweets optimal for engagement

---

### Instagram Caption Format

```
[Hook - 1-2 lines that stop the scroll]

[Body - personal story or insight with line breaks]

[Callout or question]

[Hashtags at end]
```

**Example:**
```
The moment I stopped trying to be "professional" on social media, everything changed.

I used to post corporate graphics with stock photos.
No engagement.

Then I started showing my actual workspace, my real failures, my morning coffee routine.

Engagement went up 300%.

Here's what I learned:

Be more human. Less perfect.

What's one thing you're overthinking right now? 👇

#BehindTheScenes #AuthenticMarketing #SocialMediaTips #ContentCreator #EntrepreneurLife #StartupJourney #RealTalk #SocialMediaMarketing #PersonalBrand #ContentStrategy
```

**Character Limits:** 2,200 max (aim for 1,250 for "more" link)

**Hashtag Strategy:**
- Up to 30 allowed
- Mix: 10 popular, 10 medium, 10 niche
- Place in first comment for cleaner caption
- Use all lowercase for readability

---

## Character Limit Reference

| Platform | Hard Limit | Optimal Length | Notes |
|----------|------------|----------------|-------|
| LinkedIn | 3,000 | 1,300-1,500 | Algorithm favors 1,300-1,500 |
| Twitter/X | 280 | 200-260 | Includes spaces & handles |
| Instagram | 2,200 | 1,250 | Beyond = "more" link shown |

---

## Hashtag Selection Guide

### LinkedIn Hashtags
**Professional/ Business:**
- #Leadership #Management #Entrepreneurship #Business #Marketing
- #ProfessionalDevelopment #CareerGrowth #IndustryName

**Role-Specific:**
- #CMO #Founder #CEO #MarketingTips #SalesStrategy

### Twitter/X Hashtags
**Engagement Drivers:**
- #Tips #Thread #HowTo #LearnOnTwitter #Growth

**Industry:**
- Use 1-2 max per tweet
- Place at end or in first tweet only

### Instagram Hashtags
**Popular (10-30M posts):**
- #Marketing #Business #Entrepreneur #Success #Motivation

**Medium (100K-10M):**
- #ContentMarketing #StartupLife #DigitalMarketing

**Niche (<100K):**
- #SaaSGrowth #B2BMarketing #CreatorEconomy

---

## Threading Strategies

### The "List" Thread
Best for: Tips, resources, tools, reasons
Structure: Number each point, build momentum

### The "Story" Thread
Best for: Transformations, lessons, case studies
Structure: Setup → Challenge → Solution → Result

### The "反驳" (Counter) Thread
Best for: Debunking myths, controversial takes
Structure: Common belief → Evidence → New perspective

### The "How-To" Thread
Best for: Tutorials, processes, frameworks
Structure: Problem → Step 1 → Step 2 → Result

---

## Quality Checklist

Before finalizing any repurposed content:

- [ ] **Hook Test:** Would I stop scrolling for this?
- [ ] **Value Test:** Does this give the reader something useful?
- [ ] **Platform Fit:** Does this feel native to the platform?
- [ ] **Character Count:** Within limit with margin?
- [ ] **Hashtag Relevance:** Are these the right tags?
- [ ] **CTA Included:** Is there something for the reader to DO?
- [ ] **Tone Consistency:** Is the voice consistent throughout?

---

## Usage Examples

### Example 1: Blog to LinkedIn

**Input:** A 2,000-word blog post about remote work productivity

**Output:** LinkedIn post (1,400 characters)

---

### Example 2: Podcast Episode to Twitter Thread

**Input:** 45-minute podcast about AI in marketing

**Output:** 8-tweet thread with key insights

---

### Example 3: Video to Instagram

**Input:** 10-minute YouTube video about morning routines

**Output:** Instagram caption with hook, story, CTA

---

## Integration Notes

This skill works best when:
- Content source is clearly identified
- Target platform is specified
- Desired tone is communicated
- Any key points to emphasize are highlighted

---

## Version History

- **1.0.0** (2026-03-26): Initial release with LinkedIn, Twitter/X, Instagram formats

---

*Skill built by ClawHub Publishing Team | All rights reserved*  
*Signature: ∆¹ | Director's Mark: ∆⁰*