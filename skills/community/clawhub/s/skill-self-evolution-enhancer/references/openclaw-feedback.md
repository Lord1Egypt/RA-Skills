# OpenClaw Active Feedback Integration

When a skill is enhanced with self-evolution, the agent must **tell the user** when experience was used and what improvement resulted. Add these snippets to SOUL.md or AGENTS.md in the OpenClaw workspace (or to the enhanced skill's EVOLUTION.md) so OpenClaw proactively surfaces evolution feedback.

## SOUL.md Snippet (Behavioral Guidelines)

```markdown
## Self-Evolution Feedback

When using experience from `.learnings/` (LEARNINGS.md, ERRORS.md):

1. **During task**: Optionally mention when a learning was applied: "本次参考了经验 [LRN-xxx]: ..."
2. **After task**: Summarize when relevant: which learnings were used, what evolution result, what improvement
3. **Decide contextually**: Per-use mention vs end-of-task summary — choose based on task length and user need

Do not leave the user in the dark. If evolution was used, surface it at an appropriate moment.
```

## AGENTS.md Snippet (Workflow)

```markdown
## Self-Evolution Workflow

Before using an enhanced skill:
1. Load relevant entries from `.learnings/LEARNINGS.md` (filter by area/tags)
2. Apply learnings during the task
3. After completing the task, evaluate: did we use any learnings?
   - If yes: Tell the user (per-use or summary, decide based on context)
   - Include: which entries, what improvement
```

## EVOLUTION.md Integration

When generating EVOLUTION.md for an enhanced skill, include a section:

```markdown
## OpenClaw Feedback

When this skill uses experience from .learnings/:
- Mention to user: which learning was used, what improvement
- Let OpenClaw decide: per-use mention vs end-of-task summary
- Example: "本次改写了口播稿，参考了 [LRN-xxx]（科普场景应避免过于书面），相比之前更口语化。"
```

## Hook Reminder (Optional)

For domain-specific activation, the activator script can remind:

```bash
# In scripts/activator.sh for the enhanced skill
cat << 'EOF'
<self-evolution-reminder>
After this task, if you used any entries from .learnings/:
- Tell the user which learnings were applied
- Summarize the evolution result and improvement
</self-evolution-reminder>
EOF
```
