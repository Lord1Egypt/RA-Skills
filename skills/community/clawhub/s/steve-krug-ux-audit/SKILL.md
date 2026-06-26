---
name: steve-krug-ux-audit
description: "Perform a UX audit on any website or web app using Steve Krug's proven methodology. Provide a URL or local path and get a structured usability review grounded in Krug's core principles, laws, and heuristics. Identifies issues from most critical to quick wins."
author: Chris Couriard
version: 1.0.0
license: MIT
tags: [ux, usability, audit, design, web, accessibility, steve-krug]
---

# Steve Krug UX Audit

## Methodology Attribution

This skill applies **Steve Krug's UX audit methodology** — a proven approach to evaluating web usability and user-centered design. All core laws, heuristics, and frameworks referenced herein are drawn from Krug's established methodology.

## Overview

Perform a practical usability audit of a website or web app using the principles from Steve Krug's *Don't Make Me Think, Revisited* (3rd Edition, 2014).

This skill evaluates real pages — via browser snapshots, screenshots, or provided URLs — against Krug's core laws, heuristics, and conventions. The output is an actionable audit report, not abstract theory.

## When to Use

- When provided with a URL or local dev path to review
- When evaluating a page design, wireframe, or prototype for usability
- When doing a pre-launch usability check
- When reviewing competitor sites for UX comparison

## How to Run the Audit

### Step 1: Capture the Page

Use the browser tool to navigate to the URL/path and take a snapshot + screenshot.
If multiple pages are specified, capture each one.
At minimum, always audit:
- The Home page
- One key task flow (e.g. signup, purchase, search → result)

### Step 2: The Trunk Test (Chapter 6)

Imagine being dropped on this page blindfolded. Can you answer these instantly?

| Question | What to Look For |
|----------|-----------------|
| **What site is this?** | Site ID/logo — top-left, distinctive, recognizable at any size |
| **What page am I on?** | Page name — prominent, in the right place, matches what you clicked |
| **What are the major sections?** | Primary navigation — visible, consistent, well-labeled |
| **What are my options at this level?** | Local/secondary navigation — clear subsections |
| **Where am I in the scheme of things?** | "You are here" indicators — highlighted nav items, breadcrumbs |
| **How can I search?** | Search box — visible, uses standard pattern (box + button + "Search") |

**Scoring:** For each question, rate as ✅ Clear, ⚠️ Unclear, or ❌ Missing/Broken.

### Step 3: Krug's Three Laws

#### First Law: "Don't make me think!" (Chapter 1)

Scan the page for **question marks** — anything that makes users pause and wonder:

- **Unclear names:** Cute, clever, marketing-speak, or jargon labels instead of obvious ones
- **Ambiguous clickability:** Links/buttons that don't look clickable, or non-links that do
- **Confusing choices:** Options that require thought to distinguish (e.g. "RFPs" vs "Fixed-Price")
- **Unnecessary mental chatter:** Form fields, labels, or flows that make users ask "What do they mean by...?"

**Standard:** The page should be **self-evident** (no thought required) or at minimum **self-explanatory** (a tiny amount of thought). If neither, it fails this law.

#### Second Law: "It doesn't matter how many times I have to click, as long as each click is a mindless, unambiguous choice." (Chapter 4)

Check all navigation paths and choices:

- Are choices **mindless** (obvious what you'll get) or do they require thought?
- Is the **scent of information** strong? (Do links clearly indicate their target?)
- When choices are hard, is there **just-in-time guidance** (brief, timely, unavoidable)?

#### Third Law: "Get rid of half the words on each page, then get rid of half of what's left." (Chapter 5)

Evaluate text content:

- **Happy talk:** Introductory/welcome text that says nothing useful ("Welcome to our amazing...")
- **Instructions nobody reads:** Long instruction blocks instead of self-explanatory design
- **Needless words:** Paragraphs that could be cut in half without losing meaning
- **Wall of words:** Long unbroken paragraphs instead of short ones
- **Missing bullet lists:** Series of items in paragraph form that should be bulleted

### Step 4: Billboard Design (Chapter 3)

Users scan, they don't read. Evaluate the page as a billboard going by at 60 mph:

| Principle | Check |
|-----------|-------|
| **Conventions** | Does it follow standard web conventions for layout, navigation, and element appearance? |
| **Visual hierarchy** | Are important things more prominent? Are related things grouped? Is nesting clear? |
| **Clearly defined areas** | Can you play "$25,000 Pyramid" — point at areas and say what they are? |
| **Obvious clickability** | Can you instantly tell what's clickable and what's not? |
| **Noise level** | Is there shouting (everything competing)? Disorganization (no grid)? Clutter (too much stuff)? |
| **Scannable text** | Plenty of headings? Short paragraphs? Bullet lists? Key terms bolded? |
| **Heading hierarchy** | Obvious visual distinction between heading levels? Headings closer to their section than the previous one? |

### Step 5: Navigation Design (Chapter 6)

#### Persistent Navigation
- Present on every page (except forms)?
- Contains: Site ID, Sections, Utilities, Search?
- Consistent location and appearance throughout?

#### Page Names
- Every page has one?
- Prominent and in the right place (framing the content)?
- Matches what user clicked to get there?

#### "You Are Here" Indicators
- Current location highlighted in navigation?
- Stands out enough? (Multiple visual distinctions — not too subtle)

#### Breadcrumbs (if applicable)
- At the top of the page?
- Uses ">" between levels?
- Last item is bold and not a link?

#### Tabs (if used)
- Active tab visually connects with content below?
- Different color/shade from inactive tabs?

### Step 6: Home Page (Chapter 7)

The Big Bang Theory of Web Design — first impressions are critical:

#### The Four Questions (must answer at a glance)
1. **What is this?** — Is the site's purpose immediately clear?
2. **What can I do here?** — Are available actions/content obvious?
3. **What do they have here?** — Is the offering visible?
4. **Why should I be here and not somewhere else?** — Is differentiation clear?

#### Key Elements
- **Tagline:** Clear, informative, 6-8 words, conveys differentiation? (Not a vague motto)
- **Welcome blurb:** Terse, prominent description of the site?
- **"Learn more" option:** Video or explainer for complex propositions?
- **Entry points:** Clear "where to start" for search, browse, and key tasks?
- **Promotional balance:** Are promos overwhelming the core purpose (tragedy of the commons)?

#### The Fifth Question
- **Where do I start?** — Is it obvious where to begin for search, browse, sign in, or the primary task?

### Step 7: How Users Actually Behave (Chapter 2)

Evaluate the page against the three facts of web use:

1. **We don't read, we scan.** Does the page support scanning? Or does it assume careful reading?
2. **We don't make optimal choices, we satisfice.** Will the first reasonable-looking option lead users right? Or will satisficing lead them astray?
3. **We don't figure out how things work, we muddle through.** Can someone muddle through successfully? Or will wrong mental models cause real problems?

### Step 8: Mobile & Responsive (Chapter 10)

If reviewing mobile or responsive versions:

- **Prioritization:** Are the most-needed features close at hand? Everything else reachable?
- **Affordances visible:** Are tap targets obvious? (No hidden gestures, no reliance on hover)
- **Flat design tradeoffs:** Has visual flattening removed useful affordances?
- **Performance:** Any signs of bloat that would hurt mobile load times?
- **Zooming allowed?** Can users zoom if they need to?
- **Deep links work?** Do shared links go to the right page, not the home page?
- **Full site option?** Is there a way to access the desktop version?

### Step 9: Usability as Common Courtesy (Chapter 11)

#### Goodwill Drains (things that deplete trust)
- [ ] Hiding information users want (pricing, support phone, shipping costs)
- [ ] Punishing users for "wrong" formatting (phone numbers, credit cards)
- [ ] Asking for unnecessary personal information
- [ ] Faux sincerity / "shucking and jiving"
- [ ] Sizzle blocking the path (marketing photos in the way of content)
- [ ] Amateurish appearance

#### Goodwill Builders (things that increase trust)
- [ ] Main user tasks are obvious and easy
- [ ] Upfront about costs, limitations, shipping
- [ ] Saves user steps wherever possible
- [ ] Effort clearly put into quality
- [ ] FAQs are real, current, and candid
- [ ] Graceful error recovery
- [ ] Apologizes when inconveniencing users

### Step 10: Accessibility Quick Check (Chapter 12)

Krug's "low-hanging fruit" accessibility checks:

- [ ] **Text contrast:** Sufficient contrast between text and background? No small, low-contrast type?
- [ ] **Form labels:** Labels outside form fields (not floating inside)?
- [ ] **Text resizing:** Does the page respond to browser text size changes?
- [ ] **Headings:** Using semantic heading hierarchy (h1 → h2 → h3)?
- [ ] **Link distinction:** Visited vs unvisited links visually different?
- [ ] **Keyboard navigation:** Can all content be accessed via keyboard?

## Output Format

Structure the audit report as:

```markdown
# Krug UX Audit: [Site Name]
**URL:** [url]
**Date:** [date]
**Pages reviewed:** [list]

## Executive Summary
[2-3 sentence overall assessment]
[Overall grade: A/B/C/D/F with brief justification]

## Trunk Test Results
[Table with ✅/⚠️/❌ for each question]

## Krug's Laws Assessment
### Law 1: Don't Make Me Think
[Findings with specific examples]

### Law 2: Mindless Choices
[Findings with specific examples]

### Law 3: Omit Needless Words
[Findings with specific examples]

## Billboard Design
[Findings organized by principle]

## Navigation
[Findings organized by element]

## Home Page
[Four Questions assessment + element review]

## Mobile/Responsive
[If applicable]

## Courtesy & Goodwill
[Drains and builders identified]

## Accessibility
[Quick check results]

## Top 5 Issues (Prioritized)
1. [Most critical — what to fix first]
2. ...
3. ...
4. ...
5. ...

## Quick Wins
[Things that can be fixed in under an hour]

## Recommendations
[Specific, actionable changes ordered by impact]
```

## Key Quotes to Ground the Audit

Use these Krug principles as anchoring references throughout:

- *"If you can't make something self-evident, you at least need to make it self-explanatory."*
- *"The most important thing you can do is understand the basic principle of eliminating question marks."*
- *"If your audience is going to act like you're designing billboards, then design great billboards."*
- *"Clarity trumps consistency."*
- *"We don't read pages. We scan them."*
- *"We don't make optimal choices. We satisfice."*
- *"We don't figure out how things work. We muddle through."*
- *"The reservoir of goodwill is not bottomless."*
- *"People won't use your Web site if they can't find their way around it."*
- *"FOCUS RUTHLESSLY ON FIXING THE MOST SERIOUS PROBLEMS FIRST."*

## Important Notes

- **Be specific.** Every finding must reference a concrete element on the page, not abstract theory.
- **Include screenshots/refs.** When using browser snapshots, reference specific elements by their ref IDs.
- **Prioritize ruthlessly.** Krug's mantra: fix the most serious problems first. Don't drown the report in minor issues.
- **No jargon without explanation.** Krug wrote for everyone, not just UX professionals. Keep the audit readable.
- **Suggest, don't just criticize.** Every problem should come with a practical fix suggestion.
- **Grade on real impact.** A beautiful site with confusing navigation is worse than an ugly site that's easy to use.
