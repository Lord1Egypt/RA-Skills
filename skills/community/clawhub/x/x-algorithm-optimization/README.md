# X For You Algorithm Optimization Skill

**Premium skill for BlockframeLabs agents** to optimize X (Twitter) content strategy based on the xai-org/x-algorithm architecture.

## Overview

This skill distills the technical details of X's For You feed algorithm into actionable content strategy. It covers the Grok-based transformer model, candidate isolation, multi-action prediction, scoring weights, filters, and author diversity mechanisms.

## What's Inside

```
x-algorithm-optimization/
├── SKILL.md                  # Main skill documentation (17KB)
├── QUICK_REFERENCE.md        # One-page summary and cheat sheet
├── REFERENCES.md             # Technical source references and file analysis
├── AGENT_USAGE.md            # How other agents should query and use this skill
├── README.md                 # This file
└── scripts/
    └── evaluate_post.py      # Interactive post evaluator tool
```

## Key Knowledge Areas

- **Algorithm Architecture**: Two-stage retrieval → ranking with candidate isolation
- **Engagement Types**: 17+ discrete actions + continuous dwell time
- **Scoring Mechanics**: Weighted sum + author diversity adjustment
- **Content Optimization**: How to trigger high-value engagements (reply, quote, video view, dwell)
- **Negative Signals**: What causes blocks, mutes, reports, and "not interested"
- **Filters**: Pre and post-selection quality gates
- **Cadence**: Author diversity decay and optimal posting frequency
- **Video Strategy**: Native upload, vertical format, hook requirements
- **Testing Framework**: Scientific A/B testing methodology

## Who Should Use This

- **Luna (Senior SMM)**: Creating posts, threads, campaigns for BlockframeLabs
- **Daniel (Web Engineer)**: If generating social content for product updates
- **Rex (Chief Orchestrator)**: Understanding distribution mechanics
- **Michael (Researcher)**: If aggregating social performance data
- **Any agent** that needs to understand X's ranking system for content creation

## Quick Start

1. **Read SKILL.md** for comprehensive understanding
2. **Reference QUICK_REFERENCE.md** for day-to-day content decisions
3. **Use evaluate_post.py** to score drafts:

```bash
python3 scripts/evaluate_post.py "Your post text" --has-media
```

4. **Query the skill** when facing specific challenges:
   - "How do I increase replies?"
   - "Why is my reach dropping?"
   - "Should I post a thread or single tweet?"

## Example: Evaluating a Post

```bash
$ python3 scripts/evaluate_post.py "How I gained 10k followers in 30 days 🧵👇" --has-media

═══════════════════════════════════════════════════
  X ALGORITHM POST EVALUATION
═══════════════════════════════════════════════════

Overall Score: 33/100

STRENGTHS:
  ✓ Contains curiosity-driving words
  ✓ Media (images) increase photo expand potential
  ✓ Controversial angle encourages replies and quotes
  ✓ Emojis increase visual appeal and emotional connection

WEAKNESSES:
  ✗ No clear call-to-action
  ✗ Risk of negative signals if tone is aggressive
  ✗ Missing clear value proposition

RECOMMENDATIONS:
  • Add a subtle CTA: 'Reply with your thoughts' or 'RT if you agree'
  • Ensure controversial content is respectful, not hostile
  • Make the value explicit: what the audience gains

ESTIMATED ENGAGEMENT POTENTIAL:
  reply             3/10  ███
  photo_expand      3/10  ███
  quote             2/10  ██
  dwell             2/10  ██
  favorite          1/10  █
```

## Algorithm Insights at a Glance

| Aspect | Key Finding | Content Implication |
|--------|-------------|---------------------|
| Candidate isolation | Scores independent, not relative | Quality always matters, no "competition" effects |
| Multi-action prediction | Predicts 17+ engagement types | Optimize for high-value actions (reply, quote, retweet) |
| Negative weights | Blocks/mutes/reports penalize | Avoid spammy, misleading, or offensive content |
| Author diversity | Decay factor on consecutive posts | Space posts: 2-4 hours minimum |
| Video weight | VQV applies if duration > 2s | Upload native, ensure >2s, hook in first 3 seconds |
| Freshness | Age filter removes old posts | Timeliness = higher reach |
| Hash embeddings | Semantic understanding | Write naturally, don't keyword-stuff |
| No hand-engineered features | Pure ML | The algorithm understands context, not just hashtags |
| User history relevance | Based on past engagements | Consistency in niche builds better embeddings over time |

## The Scoring Pipeline

```
User + History (128 positions)
         │
         ▼
┌─────────────────────┐
│  Grok Transformer   │  ← Candidate isolation mask
└─────────────────────┘
         │
         ▼
[Candidate 1] ──→ Unembedding → Logits → Softmax → Probabilities
[Candidate 2] ──→ Unembedding → Logits → Softmax → Probabilities
  ...
         │
         ▼
Weighted sum of P(action) × weight
         │
         ▼
Author diversity multiplier (decay)
         │
         ▼
Final score → sort → top K → post-selection filters → feed
```

## When to Consult This Skill

- Drafting posts that need to hit strategic goals
- Diagnosing underperforming content
- Planning content calendar and cadence
- Deciding between formats (video vs. image vs. text)
- Setting posting frequency
- Crafting hooks and CTAs
- Understanding why certain posts do well/badly
- Training new team members on X best practices

## Important Caveats

⚠ **Exact weights unknown**: The proprietary weight values (FAVORITE_WEIGHT, REPLY_WEIGHT, etc.) are not public. Our scoring heuristic in `evaluate_post.py` uses inferred priorities based on engagement type importance.

⚠ **Thresholds not disclosed**: Age filter duration, video minimum duration, diversity decay factor, and negative offset are tuned internally. Our default values are educated guesses.

⚠ **Algorithm evolves**: X continuously updates the model. These principles are current as of March 2026 based on the public x-algorithm repository.

⚠ **Audience variation**: Your specific audience may respond differently than the global average. Always validate with your own analytics.

## Further Reading

See `REFERENCES.md` for a detailed breakdown of source files and technical analysis.

## Author & Context

- **Created**: March 2026
- **Analyst**: Luna (Senior Social Media Manager)
- **Source**: xai-org/x-algorithm public repository reverse-engineering
- **Purpose**: Enable BlockframeLabs agents to create X content optimized for the For You feed algorithm
- **Goal**: Support $50k+ revenue by EOY 2026 through effective social distribution

## License

This skill documents publicly available technical information from the x-algorithm repository. The original code is licensed under Apache 2.0 by X.AI Corp. This documentation is provided for educational and strategic purposes within BlockframeLabs.
