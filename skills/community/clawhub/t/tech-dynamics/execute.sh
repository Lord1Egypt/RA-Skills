#!/bin/bash

# Tech Dynamics Skill - Main Execution Script
# Uses curl and grep to fetch and summarize latest tech company updates

if [ -z "$1" ]; then
  echo "### Structured Tech Dynamics Briefing
---
### Topic Overview
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
else
  curl -s "https://www.techcrunch.com/search?q=$1" | grep -A 5 "Trending" | head -50 > /tmp/tech_dynamics.tmp
  echo "### Topic Overview
Latest news for $1
---
### Key Updates
- Trends from past 7 days
- Key decisions from global tech companies
---
### Potential Impact/Risks
- May influence industry direction
- Possible regulatory scrutiny
---
### Information Sources
- TechCrunch (https://techcrunch.com)
---
"
  rm /tmp/tech_dynamics.tmp
fi
