# 🪞 Soul Question

**Ask the questions you can't ask yourself.**

You can't see your own blind spots. You can't challenge assumptions you don't know you're making. But after reading enough of your context, AI can — because it knows everything you know without being trapped in your thinking patterns.

Soul Question reads your conversations, meeting notes, journals, or any text you throw at it, and finds the cracks: contradictions you didn't notice, assumptions you never tested, values you preach but don't practice. Then it turns those cracks into 1-3 questions that might change how you think.

Not a coach. Not a summarizer. Just the questions you didn't know you needed to face.

## Quick start

```bash
openclaw install @plaud/soul-question
```

Then paste any text and say **"soul question"**.

## What it catches

| Signal | What it looks like |
|--------|-------------------|
| **Value-behavior gap** | You say you value X, but your decisions say Y |
| **Untested assumption** | Everyone accepts a premise nobody ever verified |
| **Frame lock** | You've been using one lens so long you forgot others exist |
| **Contradiction** | You said A on Monday and not-A on Thursday |
| **Avoidance** | Something important keeps coming up but never gets discussed |
| **Meta-question** | You're optimizing *how* without ever asking *why* |

## Examples

**Input**: Slack thread where a founder talks about "moving fast" but has delayed shipping 3 features waiting for "perfect" designs.

**Output**:
```
🪞 Soul Question

When you say "move fast", do you mean the team should move fast,
or that you want to feel like things are moving fast? Because your
last 3 shipping decisions optimized for polish over speed.
↳ Based on: feature delay discussions in #product (March 3, 7, 12)
```

---

**Input**: Personal journal entries from the past month.

**Output**:
```
🪞 Soul Question

You've written about "needing more time to think" in 6 out of 9 entries,
but you also signed up for 3 new commitments this month. Is "not enough
time to think" actually your problem, or is filling your schedule how
you avoid the thinking?
↳ Based on: journal entries March 2, 8, 11, 14 + new commitments log
```

## What makes it different

Most "reflection" tools ask generic questions — "What went well? What would you change?" Soul Question doesn't work from templates. It reads **your** material, finds **your** specific cracks, and asks questions **only you** need to answer.

Every question must pass four gates:
1. **Grounded** — based on your specific words and actions, not generic
2. **Structural** — points to a crack in your thinking framework, not a knowledge gap
3. **Novel** — you genuinely never thought about it that way
4. **Transformative** — answering it could change how you think, not just what you know

If it can't find a question that passes all four, it tells you honestly instead of forcing something shallow.

## Works with anything

Paste chat logs, meeting transcripts, journal entries, strategy docs, book annotations, email threads — any text in any language. Output matches your input language automatically.

## Privacy

- **Zero data transmission** — all processing happens locally through your Claude instance
- **Zero storage** — nothing is written to disk; output appears and that's it
- **Zero external calls** — no web searches, no API calls, no telemetry

## License

MIT
