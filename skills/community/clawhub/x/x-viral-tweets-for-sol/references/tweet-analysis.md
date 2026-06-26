# Tweet Analysis Reference

Use this when analyzing a tweet, auditing engagement, or scoring generated variants before output.

## Classification taxonomy

Every CT tweet fits into one or more of these categories. When analyzing, label the dominant category and any secondary modes.

| Category | Marker | Example shape |
|---|---|---|
| **educational** | teaches something concrete | "How [X] actually works under the hood..." |
| **alpha/leak** | non-public or pre-consensus info | "watching wallet 0x... accumulate [thing] for 3 weeks" |
| **meme** | image or text purely for laughs / culture | format-based, punchline-based |
| **builder** | "I shipped" / "we built" | "just deployed [thing] on mainnet" |
| **ecosystem update** | factual news re: project/protocol | partnership, launch, roadmap |
| **hot take** | spicy opinion meant to divide | "[popular thing] is overrated" |
| **engagement bait** | structured to maximize replies/QRTs | "name 1 thing", "wrong answers only", polls |
| **storytelling** | personal narrative, founder arc | "3 months ago I was..." |
| **motivation / grindset** | identity & aspirational | "you will make it. keep building." |
| **market commentary** | price / flows / sentiment | "alts about to leak" |
| **propaganda** | ecosystem tribalism | "ETH is a museum, sol is the city" |
| **reply guy gold** | clever short reply to a big account | one-liner that QRTs a giant |

A tweet that fits one cleanly tends to perform better than one straddling three.

## Tweet Quality Score (TQS) — detailed

Sum to 0–100. Score every variant before shipping multiple.

### Hook strength — 0–25
The first 7 words decide whether the scroll stops.

- 25: stop-scroll guaranteed (pattern interrupt, numeric specificity, named enemy, contrarian declaration, mystery)
- 15: solid (clear stakes, sharp claim)
- 5: generic ("just thinking about", "today I learned")
- 0: dead on arrival ("Hello everyone!")

Stop-scroll patterns:
- numeric: "spent $4,200 on..."
- named target: "vitalik is wrong about..."
- contrarian: "you don't need a token to..."
- mystery: "the real reason [thing] failed wasn't..."
- stakes: "I almost rage-quit crypto last night."

### Compression — 0–15
Info-per-character. Each word should pay rent. Adjectives almost always evict themselves.

Test: can you delete 3 words without losing meaning? If yes, deduct.

### Cultural fit — 0–15
Does this sound like a person who lives on CT, or a brand?

- Tone match (lowercase, terse, no marketing voice)
- Slang used correctly (don't force, don't over-explain)
- No outsider tells ("the Solana blockchain")

### Repostability — 0–15
Will someone screenshot this? QRT it with "this"?

Markers of high repostability:
- self-contained (no thread needed to understand)
- screenshot-shaped (≤240 char, no truncation)
- carries a single clean claim
- works without the author's context

### Originality — 0–10
Has this been said 1000 times this week? Is the angle the user's, or borrowed?

- 10: only this account could have said it
- 5: known idea, fresh framing
- 0: copy-paste of a viral post from yesterday

### Emotional charge — 0–10
Does it produce a body reaction? Curiosity, anger, awe, FOMO, validation, schadenfreude, humor.

Flat tweets ≤ 3. Tweets that make someone feel something ≥ 7.

### Authority signal — 0–10
Does the post imply the author has earned the right to make this claim? Earned authority > stated authority.

- "I've shipped 4 anchor programs to mainnet" → earned
- "as an expert in DeFi" → stated, dock points

## Engagement audit framework

When auditing an account or a batch of recent posts:

1. **Read 20 most recent posts.** Don't trust memory.
2. **Tag each** with category + TQS.
3. **Plot the distribution.** What % is each category?
4. **Find the dead zones.** Categories at 0% that should be there (e.g., zero builder posts for a founder).
5. **Find the saturation.** Categories at >40% (e.g., 60% market commentary = looks like a trader account, not a founder).
6. **Hook audit.** What % of first-7-words actually stop scroll? Target ≥ 60%.
7. **Reply ratio.** What % are replies vs originals? Target 40–60% replies for growth phase.
8. **Time-of-day distribution.** Are posts hitting active CT windows (see growth-playbook)?
9. **Prescription.** Output: 3 specific fixes for the next 7 days, each with a concrete example post.

## Common pathologies & fixes

| Pathology | Symptom | Fix |
|---|---|---|
| **Brand voice creep** | "Excited to share...", "Thrilled to announce..." | Replace with declarative or numeric opener |
| **Hashtag boomer** | #Solana #Crypto tail | Strip all hashtags |
| **Emoji vomit** | 🚀🔥💎 strings | One purposeful emoji max, usually zero |
| **Thread addiction** | Everything is 1/9 | Compress to single tweets; reserve threads for actual arcs |
| **Soft hot takes** | "Maybe X is kinda overrated?" | Drop the hedges. Take the position fully. |
| **Reply-guy-only mode** | All replies, no originals | Inject 2–3 original posts/day to build IP |
| **Founder-as-shill** | Every post is the product | 70/20/10 — culture/insight/product |

## Quick rubric for in-line scoring

When dropping a quick score next to a generated variant:

```
[tweet text]
TQS ~62 · hook 18/25 · cultural fit 12/15 · repostable
```

Don't over-decorate. Single line.
