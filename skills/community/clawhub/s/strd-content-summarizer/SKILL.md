---
name: content-summarizer
description: Fetch any URL and produce a structured content summary with extractive summarization, AI enhancement prompts, and structured output templates. Extracts clean text from HTML, identifies key sentences, generates metadata, and provides ready-to-use prompts for AI summarization. Perfect for content repurposing, research pipelines, and newsletter workflows.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl", "python3"] },
        "install": [],
      },
  }
---

# Content Summarizer

Transform any URL or raw text into structured, actionable content summaries using extractive summarization + AI enhancement prompts.

## What This Skill Does

1. **Fetches** any URL and extracts clean text (removes HTML, nav, scripts, ads)
2. **Extracts** key sentences algorithmically (extractive summarization — no API needed)
3. **Generates** metadata (title, word count, reading time)
4. **Outputs** a structured markdown template + AI enhancement prompt ready for any LLM

The AI enhancement prompt makes the extracted content easy to summarize with MiniMax, GPT-4o, or Claude.

## Quick Start

```bash
# Summarize a URL (outputs to terminal + /tmp/summaries/)
./scripts/url-to-summary.sh https://example.com/article

# Summarize text directly (from argument or pipe)
./scripts/summarize.sh "Your article text here..."
cat article.txt | ./scripts/summarize.sh

# Custom model for AI prompt
./scripts/url-to-summary.sh https://example.com --model openai
```

## Scripts

### url-to-summary.sh — Full Summary from URL

```bash
./scripts/url-to-summary.sh <url> [--model minimax|openai|anthropic]
```

Fetches URL, extracts clean text, produces:
- Extracted key sentences (extractive summarization)
- Structured markdown template (summary, tweet hook, key takeaways)
- **AI enhancement prompt** — copy-paste into any LLM for full summarization
- Metadata (title, word count, reading time)

Output saved to `/tmp/summaries/summary-TIMESTAMP.md`

### summarize.sh — Summarize Text Directly

```bash
./scripts/summarize.sh "Your text..."
cat file.txt | ./scripts/summarize.sh
```

Same output as url-to-summary.sh but for raw text input.

## Output Format

```
# Content Summary

**Source:** [url]
**Title:** [extracted or unknown]
**Stats:** ~1,200 words | ~6 min read

## Key Sentences (Extractive Summary)
[Top 15-20 most meaningful sentences from the text]

## Structured Summary Template
[TODO fields for: what, why, key points]

## Tweet Hook
[TODO: Compelling one-liner]

## Key Takeaways
1. [TODO]
2. [TODO]
3. [TODO]

## AI Enhancement Prompt
[Ready-to-use prompt with extracted text embedded]
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OUTPUT_DIR` | `/tmp/summaries` | Where to save summary files |
| `MODEL` | `minimax` | AI model for enhancement prompt |

## Use Cases

- **Content repurposing**: Fetch articles, extract key points, feed into content pipeline
- **Research pipeline**: Batch summarize 20 URLs, collect key points, synthesize insights
- **Newsletter workflow**: Fetch sources, generate structured summaries, assemble newsletter
- **Quick reading**: Extract key sentences from long articles for rapid triage

## Notes

- Uses extractive summarization (algorithmically selects important sentences) — no API key needed
- AI enhancement prompt is the value-add: paste into MiniMax/GPT/Claude for full abstractive summary
- HTML extraction removes scripts, styles, nav, footer, ads — focuses on article body
- Limited to 15,000 characters of extracted text to keep context manageable

## Output Format

```markdown
## Summary

[2-3 paragraph summary of the content]

## Tweet Hook
> [One compelling, shareable sentence that captures the essence]

## Key Takeaways
1. [First key point]
2. [Second key point]
3. [Third key point]

---
*Source: [URL] | ~X min read | ~Y words*
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SUMMARIZER_MODEL` | No | auto | LLM model for summarization (or let the agent auto-select) |
| `MAX_TOKENS` | No | `500` | Max tokens in summary output |

## Usage Examples

```bash
# Summarize a blog post
./scripts/url-to-summary.sh https://yourcompetitor.com/blog/industry-trends

# Process a research paper
./scripts/summarize.sh "$(curl -sL https://arxiv.org/pdf/2301.00001.pdf | head -c 10000)"

# Quick key points for a meeting
./scripts/key-points.sh https://news.ycombinator.com/item?id=12345678

# Use with OpenClaw: feed the output directly into your workflow
SUMMARY=$(./scripts/url-to-summary.sh https://example.com/article)
echo "$SUMMARY" | ./scripts/key-points.sh
```

## Tips

- For better results, provide clean article URLs (avoid paywalls and heavy JS pages)
- Use `MAX_TOKENS=1000` for longer, more detailed summaries
- Chain with other skills: competitor-tracker alerts → content-summarizer → social posting
- The tweet hook is designed to be engaging, not just a truncated sentence
- Key points should be actionable insights, not just topic labels

## Dependencies

- `curl` — for fetching URLs
- OpenClaw agent with web_fetch tool for content extraction (used internally by the agent)
