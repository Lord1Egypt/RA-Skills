---
name: web-researcher
description: "Use this skill for deep research, fact-checking, or finding the latest technical news."
---

# Web Researcher Skill

## When to use
- Use when the user asks for "the latest," "news," or "research" on a topic.
- Use when you need to verify a fact that isn't in your local training data.

## Research Protocol
1. **Multi-Query Search**: Don't just search once. Run 2-3 targeted searches (e.g., "OpenClaw 2026.3.2 features" AND "OpenClaw 2026.3.2 bugs").
2. **Deep Dive**: Use `web_fetch` on at least the top 2 most relevant URLs to get the full text. Snippets are not enough for deep research.
3. **Synthesis**: Summarize the findings by grouping them into "Key Facts," "Timeline," and "Contradictions" (if any).
4. **Cite Sources**: Always list the URLs you actually read at the end of your report.

## Output Format
- Start with a 🪐 **Jupiter Research Brief** header.
- Use bullet points for readability.
- Highlight any "Breaking News" or "Critical Alerts" in bold.
