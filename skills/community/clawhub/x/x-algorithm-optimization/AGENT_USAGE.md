# Agent Usage Guide

## How to Use This Skill

This skill is designed to be consulted by any agent when dealing with X (Twitter) content strategy. You don't "run" it directly; you **query it** for insights.

## When to Invoke

Whenever you need to:
- Create or optimize X posts for a client
- Diagnose why a post underperformed
- Plan content calendar and cadence
- Advise on X growth strategy
- Answer questions about the X algorithm
- A/B test content hypotheses
- Understand engagement mechanics

## How to Query

The skill is a knowledge base. Read `SKILL.md` to access the information. You can use `memory_search` to find relevant sections by topic.

### Example Queries

```
Query: "How do I get more replies on X?"
→ Reference: "Content Strategy: Key Insights" section: "Trigger REPLIES" strategies.
→ Reference: "Hook Formula" section for templates.
→ Reference: "Engagement Value" table showing replies are high-value.

Query: "Why is my reach dropping after posting many videos?"
→ Reference: "Author Diversity" section: multiple posts attenuate reach.
→ Reference: "Video Optimization": ensure native upload, >2s, vertical, hook.
→ Reference: Check for negative signals in videos that might trigger filters.

Query: "Should I post this as a thread or single tweet?"
→ Reference: "Threads" in format optimization: good for dwell time, replies, but serialize content.
→ Compare: Single tweet = quick consumption, potentially higher share rate.
→ Decision depends on content length and desired engagement type.

Query: "What time should I post?"
→ Reference: No absolute answer in skill; recommend testing. "When your audience is active."
→ Suggest: Check analytics, test different windows, use consistent timing for pattern.

Query: "Do hashtags help the algorithm?"
→ Reference: TL;DR: "Probably minimal direct impact on ML scoring. Use for discoverability/grouping."
→ Strategy: Hashtags may increase categorical clarity for retrieval matching if used consistently.
```

## Query by Section

- **Overview**: For algorithm summary
- **Engagement Types**: For understanding what actions the model predicts
- **Scoring Mechanics**: For how scores are computed
- **Filters**: For quality gates to avoid
- **Content Strategy**: For actionable advice
- **Testing Framework**: For scientific validation
- **Quick Reference**: For one-page summary

## Integration Pattern

When a user asks about X content, you should:

1. **Read SKILL.md** to retrieve relevant section(s)
2. **Synthesize** the knowledge with user's specific context
3. **Provide actionable advice** with reasoning
4. **Cite sources** within the skill (e.g., "According to the X Algorithm Optimization skill's section on Author Diversity...")

## Prompt Template (optional)

When responding to X strategy questions, consider this structure:

```
[Context of user's situation]
Based on the X For You algorithm:

[Key insight from skill]
[Specific recommendation]
[Expected outcome]

Supporting detail: [additional nuance]

Optional: Question to refine, e.g., "What's your current posting frequency?"
```

## Example Consultation

User: "I want my posts to get more reach. What should I change?"

Agent (using skill):

```
I consulted the X Algorithm Optimization skill. Key points:

1. Reach is driven by the For You feed. Posts are scored by a Grok transformer that predicts engagement probabilities.

2. High-value engagements are: replies, quotes, retweets, video views, dwell time. Focus on triggering these rather than just likes.

3. Author diversity matters: if you post multiple times in a short window (less than 2-4 hours), your later posts get attenuated even if they're great. Space your top content.

4. Dwell time is crucial: medium-length posts (200-500 characters) with dense value encourage reading time, which is a strong signal.

5. Video get special weight but must be native (uploaded to X), vertical format, and first 3 seconds must hook. Also video duration > 2s to qualify for VQV weight.

Immediate actions:
- Ensure your next 3 posts are spaced at least 3 hours apart
- Make the hook in the first line provocative or curiosity-driven
- If using video, upload directly, not via YouTube link
- End posts with a question to encourage replies

Would you like specific advice on your last few posts? I can analyze them.
```

## Maintaining the Skill

If you update the skill:
1. Update `SKILL.md` with new insights
2. Update `QUICK_REFERENCE.md` if tips change
3. Update `REFERENCES.md` if new source material added
4. Consider publishing to ClawHub for other agents to install

## Advanced: Querying the Learning

The skill's knowledge came from reverse-engineering the public x-algorithm repository. If you have access to:
- Internal X data/weights (unlikely)
- Your own analytics (impressions, engagement breakdown)
- A/B test results

You can refine the inferences. For instance, if you find that likes actually correlate best with reach in your niche, adjust your weighting mentally.

## Limitations

The skill makes inferences about:
- Relative importance of engagement types (weights NOT public)
- Exact thresholds (age, video duration, diversity decay)
- Whether secondary actions like "share via DM" matter as much as retweet

Treat these as educated guesses based on ML best practices and what actions are modeled. Validate with your own data.

## Troubleshooting

If skill consultation seems off:
- Check if you're referencing the right section (some topics appear in multiple places)
- Consider your specific audience may behave differently than the global average
- The algorithm may have been updated since this skill was written (X continuously iterates)
- You may have hit edge cases not covered (ask for clarification)

## Feedback

If you discover new insights about the X algorithm that should be added to this skill, update the SKILL.md and share with the team.
