# Proactivity Guide for Remotion Animator

When to proactively suggest creating an animation/video, and how to pitch it without being annoying.

## Decision Flow

```
User shares content
        │
        ▼
Is it one of these formats?
├── Transcript / dialogue / interview
├── Stats / metrics / numbers
├── Product/feature announcement
├── Step-by-step guide
├── Weekly/monthly report
├── Social post request
└── Presentation / deck
        │
        ├─ YES → Ask once: "Want me to animate this?"
        │         If yes → scaffold template + customize
        │         If no/ignore → drop it
        │
        └─ NO → Stay quiet
```

## Match Content to Template

| Content Type | Best Template | Customize |
|--------------|--------------|-----------|
| Interview / podcast transcript | `conversation` | Speaker names, colors, alignment |
| Customer discovery notes | `conversation` | Label speakers (INTERVIEWER / CUSTOMER) |
| Growth metrics / KPIs | `data-kinetic` | Replace metrics array, adjust colors |
| Feature launch | `intro` | Logo placeholder → text/emoji, tagline |
| Tutorial / how-to | `explainer` | Steps array, titles, details |
| Weekly wrap-up | `data-kinetic` or custom | 3-5 key numbers from the week |
| Social clip / reel | `intro` (vertical) | 1080×1920, punchy text |
| Pitch deck | Custom composition | Per-slide compositions with stagger |

## Pitch Templates

Use these as starting points. Keep them tight.

**Transcript → Conversation video**
> "This reads like a dialogue. Want me to turn it into a conversation video with speaker labels and a dark background? Takes ~2 min."

**Metrics → Data kinetic**
> "These numbers would hit harder as an animated clip. I can build a 5-8s count-up video. Want it?"

**Launch → Intro**
> "Want a quick logo-reveal intro for the announcement? 5s, render-ready."

**Tutorial → Explainer**
> "This step-by-step flow would work great as an animated explainer. I can scaffold it in 30s."

**Weekly report → Recap**
> "Want a 10s animated recap of the week? I pull the top 3 numbers and render it."

**Generic fallback**
> "Want me to animate this into a short video?"

## Anti-Patterns (Don't Do This)

❌ "I'm going to make a video for you" — never auto-generate without asking
❌ Re-offering after a "no" on the same content
❌ Suggesting video for text that is clearly meant to stay text (code, config, email draft)
❌ Overwhelming with options: "I can do 5 different templates!" — pick the best one, offer one

## Recurring Proactivity

Set up cron jobs for recurring video creation:

| Trigger | Action | Template |
|---------|--------|----------|
| Friday 5 PM | Generate weekly metrics recap | `data-kinetic` |
| End of sprint | Sprint summary video | `explainer` |
| Monthly revenue close | Revenue/milestone video | `data-kinetic` |
| Monthly all-hands prep | Automated intro slide | `intro` |

Mark recurring offers so you don't re-ask if the user consistently declines.
