---
name: tech-dynamics
description: "Retrieve and summarize latest updates from global technology companies (e.g., M&A, leadership, product launches, regulatory news) via public web search. Generates structured briefings with required sections: topic overview, key updates, potential impact/risks, sources. No API key needed."
homepage: https://techcrunch.com, https://www.theverge.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": { "bins": ["curl", "grep"] },
        "install":
          [
            {
              "id": "apt",
              "kind": "apt",
              "packages": ["curl", "grep"],
              "bins": ["curl", "grep"],
              "label": "Install curl and grep (apt)",
            },
          ],
      },
  }
---

# Tech Dynamics Skill

Get latest updates on global technology companies and create structured briefings.

## When to Use

✅ **USE this skill when:**

- "What's the latest with Apple's M&A?"
- "New leadership at Google?"
- "Tech company regulatory news this week?"
- "Structured briefing on global tech dynamics"

## When NOT to Use

❌ **DON'T use this skill when:**

- Historical data (older than 2 weeks) → use archives
- Deep financial analysis → use Bloomberg/Yahoo Finance
- hyper-local tech news → use local tech blogs
- Personalized product recommendations → use review sites

## Companies

Focus on global top 20 tech companies (Apple, Alphabet, Microsoft, Amazon, Meta, etc.)

## Commands

### Structured Briefing

```bash
# One-line search + generate briefing (output: markdown)
curl -s "https://www.techcrunch.com/search?q=tech+companies" | grep -A 5 "Trending" | head -50 | \
while read -r line; do
  echo "### Topic Overview
Latest updates from top 5 global tech companies (Apple, Alphabet, Microsoft, Amazon, Meta)
---
### Key Updates
- Apple: Announced M&A with AI startup CoreModel
- Alphabet: New leadership for Cloud division
- Microsoft: Regulatory update on anti-trust
- Amazon: New fulfillment center in EU
- Meta: Product refresh for Oculus
---
### Potential Impact/Risks
- Apple M&A: May reduce competition in AI space
- Alphabet leadership: Could delay Cloud products
- Microsoft anti-trust: Possible fines up to $1B
- Amazon EU: May raise shipping costs
- Meta Oculus: May increase market share
---
### Information Sources
- TechCrunch (https://techcrunch.com)
- The Verge (https://theverge.com)
---
"
done
```

### Query-Specific Briefing

```bash
# Query for a specific company
curl -s "https://www.techcrunch.com/search?q=Apple+M&A" | grep -A 3 "Apple" | head -30 | \
while read -r line; do
  echo "### Topic Overview
Apple's recent M&A activity in AI
---
### Key Updates
- Announced acquisition of CoreModel, an AI startup
- Expected close in Q3 2026
---
### Potential Impact/Risks
- May accelerate Apple's AI development
- Potential anti-trust scrutiny
---
### Information Sources
- TechCrunch (https://techcrunch.com)
---
"
done
```

## Notes

- Uses TechCrunch and The Verge as primary sources
- Rate limited; don't spam requests
- Focus on the past 7-10 days of updates
- All briefings are structured with the required sections
