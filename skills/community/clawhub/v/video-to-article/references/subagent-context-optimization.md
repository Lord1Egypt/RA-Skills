# Subagent Context Optimization

## Observed comparison

| Context Style | Approx. Input Tokens | Typical Subagent Tool Use |
|------|------|------|
| "Screenshots are in the folder, format is..." | ~214K | many file-search validation calls |
| Explicit "do not verify" plus slug table | ~22K | mostly read and write only |
| Slug table plus restricted toolset | ~16K | mostly read and write only |

Core finding: telling subagents not to verify files can cut input token usage by roughly 90 percent.

## Recommended template

```python
context = f"""
Write the course note in English.

Input: {path}/section{N}.txt

All screenshots are already prepared. Do not verify files.
Reference them directly as:
  ![[../../../assets/{course}/{slug}-{label}.jpg]]

Slug table:
- Section Overview -> section-overview (no screenshots)
- XXXX -> xxxx-slug (3 images: overview, detail, result)

Density: overview and recap lessons get no screenshots. Other lessons get 3 screenshots each.

Output: {vault}/sources/{course}/section-{N}-{slug}.md
"""
```

## Six practical rules

1. Hardcode the slug table instead of asking the subagent to compute it
2. Explicitly say "do not verify files"
3. List lessons with no screenshots separately
4. Restrict tools when possible so the subagent does not waste time searching
5. Pass preprocessed plain text, not raw subtitle files
6. Reserve `index.md` updates for the main agent

## Anti-patterns

```python
# Bad: asking the subagent to discover screenshot files
context = "Screenshots are in assets/, named like {video-name}-{index}.jpg"

# Bad: asking the subagent to decide screenshot density on its own
context = "Choose screenshot density as needed"

# Bad: giving unrestricted tools when simple file IO is enough
```
