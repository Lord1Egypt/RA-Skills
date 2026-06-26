---
name: youtube-analysis
description: Analyze YouTube videos with summary and deep-dive analysis. Use when a user provides a YouTube URL and wants both a summary and analytical insights about the content, implications, quality, and intersections with other topics.
---

# YouTube Analysis

Use the main chat model for the final summary and analysis.

Goal: extract the transcript first when possible, then use the main model for judgment, synthesis, and deeper analysis. Do not rely on a cheap/local summarizer as the default final narrator.

## Workflow

### Step 1: Extract transcript first when possible

Prefer transcript extraction as the first step:

```bash
summarize "URL" --youtube web --video-mode transcript --extract --format md
```

When invoking it via `exec`, give it a long timeout and generous `yieldMs` so slow extraction is not killed early.

Treat the extracted transcript as source material, not as verified truth. YouTube captions may contain transcription errors, especially for names, numbers, and charged claims.

### Step 2: Assess transcript quality

Check whether the extracted transcript is usable.

Common signs of source-caption problems:
- misheard names or places
- broken grammar or repeated filler
- obvious word substitutions
- malformed numbers or dates
- signs that only auto-captions are available

If transcript quality is poor, keep confidence lower and say so.

### Step 3: Use the main chat model for summary and analysis

After extraction, do the real work in-chat using the main model:
- summarize clearly for the user
- identify main claims or arguments
- analyze implications and significance
- assess credibility, bias, and missing context
- separate speaker claims from established facts when needed
- connect the video to related topics or current context

This keeps the main model focused on synthesis and judgment while grounding it in extracted source material.

### Step 4: Fallbacks

Use this order:
1. Try `--youtube web --extract`
2. If needed, compare with `--youtube yt-dlp` or `--youtube no-auto`
3. If no usable transcript is available, use direct summarization as a lower-confidence fallback
4. Clearly label lower-confidence output when the transcript is missing or noisy

## Analysis method

For each major point:
1. What does this mean? — implication or significance
2. How does it connect? — intersections with other topics
3. Quality assessment — credibility, biases, missing context
4. Actionable takeaway — what to do with this information

## Output format

Present as two sections:

**Summary**
- concise overview of the video content
- grounded in the transcript when available

**Analysis**
- key insights
- implications
- connections to other topics
- credibility / quality notes
- counterpoints or gaps

## Operating principle

Transcript first, analysis second.

Use extracted transcript as the preferred source material whenever possible.
Use the main model for interpretation and synthesis.
Do not overclaim certainty when captions are noisy or source quality is weak.

## Notes

- Prefer `--youtube web --extract` as the default first pass
- Be explicit when confidence is reduced because only noisy auto-captions were available
- If the video is long, summarize from extracted transcript chunks rather than relying on unsupported memory of the whole transcript
- Include intersections with other videos or ongoing topics the user cares about when relevant
- If the user wants to swap models manually for transcript cleanup or summarization, treat that as an optional override rather than the default skill path
