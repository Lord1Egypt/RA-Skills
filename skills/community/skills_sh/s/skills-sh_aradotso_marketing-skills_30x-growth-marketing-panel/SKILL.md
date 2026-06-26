---
name: 30x-growth-marketing-panel
description: AI Growth Marketing Expert Panel with 11 world-class experts distilled from 4,000+ YouTube videos for Claude Code
triggers:
  - "ask the marketing panel"
  - "get marketing advice from experts"
  - "how should I price this offer"
  - "what would Alex Hormozi say about"
  - "ask the growth marketing experts"
  - "get SEO strategy from Neil Patel"
  - "marketing roundtable discussion"
  - "consult the marketing panel"
---

# 30x Growth Marketing Panel

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

An AI-powered expert panel of 11 world-class marketing experts distilled from 4,000+ YouTube videos. Get answers from the right expert(s) in their voice, using their actual frameworks.

## What It Does

The 30x Growth Marketing Panel uses a dual-layer architecture to provide authentic expert advice:

- **Layer 1 (Brain)**: NotebookLM retrieval from 4,000+ indexed YouTube videos
- **Layer 2 (Soul)**: Persona Protocol with expert personality, frameworks, and anti-patterns
- **Semantic routing**: Automatically matches your question to the right expert(s)
- **Anti-hallucination**: Retrieve-first protocol ensures responses are grounded in actual expert content

## Installation

```bash
npx skills add norahe0304-art/30x-growth-marketing-panel
```

Works with Claude Code, Cursor, Codex, and 45+ AI coding agents.

## The Expert Panel

| Expert | Domain | Best For |
|--------|--------|----------|
| **Alex Hormozi** | Offer creation, pricing, sales, scaling | SaaS pricing, value propositions, sales frameworks |
| **Greg Isenberg** | AI startups, community growth, vibe marketing | Community-led growth, AI product positioning |
| **Neil Patel** | SEO, paid ads, CRO, social media | Traffic generation, conversion optimization |
| **Nathan Gotch** | AI SEO, Search Everywhere Optimization | AI-powered SEO strategies, ranking tactics |
| **Authority Hacker** | AI content at scale, affiliate marketing | Content automation, affiliate revenue |
| **Sabrina Ramonov** | AI agents, automation workflows, MCP | Marketing automation, AI agent implementation |
| **Liam Ottley** | AI automation agency, client acquisition | Agency model, service packaging |
| **Julia McCoy** | AI writing, content strategy, brand building | Content creation, brand voice |
| **Ryan Doser** | AI marketing tools, practical implementation | Tool stack, workflow optimization |
| **Growth Tribe** | Growth hacking, experimentation, AARRR | Experimentation frameworks, funnel optimization |
| **Dan Koe** | One-person business, writing, personal brand | Solopreneur strategy, personal branding |

## Usage Patterns

### Single Expert Consultation

Ask focused questions to get advice from the most relevant expert:

```bash
# Pricing question → routes to Alex Hormozi
"How should I price my B2B SaaS product?"

# SEO question → routes to Neil Patel or Nathan Gotch
"What's the best AI SEO strategy for 2026?"

# Content question → routes to Julia McCoy
"How do I build a consistent content voice?"
```

### Named Expert Request

Explicitly request a specific expert:

```bash
"Ask Alex Hormozi about my offer: [describe your offer]"

"What would Neil Patel say about this landing page conversion issue?"

"Get Greg Isenberg's take on community-led growth for an AI tool"
```

### Multi-Expert Roundtable

Broad strategic questions trigger multiple experts:

```bash
"How should I go to market with a new AI marketing tool?"
# Returns perspectives from Greg Isenberg, Neil Patel, Ryan Doser

"What's the best growth strategy for a bootstrapped SaaS?"
# Returns perspectives from Alex Hormozi, Dan Koe, Growth Tribe
```

## Expert Knowledge Base Structure

Each expert has two components:

### 1. NotebookLM Brain (Raw Retrieval)

```bash
# 200-300 YouTube videos per expert
# Indexed in NotebookLM Pro (300 sources/notebook)
# Zero information loss from original content
```

### 2. Persona Protocol (Personality)

Located in `expert_kb.md` for each expert:

```markdown
## Role
Who the expert is, their background, core expertise

## Thinking Models
Frameworks they use (e.g., Hormozi's Value Equation, AARRR funnel)

## Tone & Communication
How they speak, teaching style, personality markers

## Anti-Patterns
What they avoid, common mistakes they call out

## Retrieval Logic
How to search their NotebookLM notebook effectively
```

## Anti-Hallucination Protocol

The panel follows strict retrieval rules:

1. **Retrieve first**: Must search NotebookLM before generating responses
2. **Dual verification**: Cross-reference retrieval with KB persona
3. **Explicit marking**: Extrapolations from core principles marked with ⚠️
4. **Never fabricate**: If an expert hasn't covered a topic, say so

Example output structure:

```markdown
**Alex Hormozi's Perspective:**

[Retrieved content from NotebookLM]

Framework: Value Equation
- Dream Outcome: [specific to your question]
- Perceived Likelihood: [specific analysis]
- Time Delay: [specific analysis]  
- Effort & Sacrifice: [specific analysis]

⚠️ *Extrapolating from core principles:* [only if needed]
```

## Distilling Your Own Expert

Use the `distill_anyone.md` prompt template:

```bash
# 1. Copy the prompt from distill_anyone.md
# 2. Change 3 variables:
#    - Expert name
#    - YouTube channel/playlist URL
#    - Domain expertise
# 3. Run in Claude Code

# The pipeline automatically:
# - Collects YouTube URLs with yt-dlp
# - Creates NotebookLM notebook
# - Bulk adds videos with notebooklm-py
# - Generates Persona Protocol KB
# - Creates semantic routing rules
```

### Variables to Configure

```bash
EXPERT_NAME="Your Expert"
YOUTUBE_SOURCE="https://youtube.com/@channel or playlist URL"
DOMAIN="their core expertise area"
```

## Key Commands

### Query the Panel

```bash
# General query (auto-routes)
"[Your marketing question]"

# Named expert
"Ask [Expert Name] about [topic]"

# Multi-expert
"Get a roundtable on [strategic question]"
```

### Inspect Expert Knowledge

```bash
# List all experts and domains
"Show me the expert panel"

# View expert frameworks
"What frameworks does Alex Hormozi use?"

# Check NotebookLM coverage
"How many videos are indexed for Neil Patel?"
```

## Configuration

### Language Support

Responses automatically match your query language. Framework names stay in English:

```bash
# Query in Spanish → Response in Spanish
"¿Cómo debería fijar el precio de mi SaaS?"

# Query in French → Response in French  
"Quelle est la meilleure stratégie SEO?"
```

### Retrieval Depth

Adjust how many NotebookLM sources to search:

```bash
# Default: 5-10 most relevant sources
# Deep research: 20-30 sources (slower, more comprehensive)
# Quick answer: 3-5 sources (faster, still accurate)
```

## Real Code Examples

### Example 1: Pricing Strategy (Alex Hormozi)

**Query:**
```
"How should I price my B2B SaaS with a $10k LTV and 6-month sales cycle?"
```

**Expected Response:**
```markdown
**Alex Hormozi's Pricing Framework:**

[Retrieved from NotebookLM: Hormozi's pricing videos]

**Value Equation Analysis:**
1. Dream Outcome: Enterprise efficiency gain (high)
2. Perceived Likelihood: 6-month cycle = trust-building needed
3. Time Delay: 6 months is long → charge more upfront
4. Effort & Sacrifice: Implementation complexity matters

**Pricing Recommendation:**
- Annual contract: $5,000-$7,500/year
- Upfront discount: 20% off for annual vs monthly
- Reduce time delay perception: 30-day quick wins
- Stack value: Implementation support included

**Hormozi's Principle:** "Charge for the dream outcome, not your cost"
```

### Example 2: SEO Strategy (Neil Patel + Nathan Gotch)

**Query:**
```
"What's the best AI SEO strategy for a new marketing tool in 2026?"
```

**Expected Response:**
```markdown
**Neil Patel's Take:**
[Retrieved content about AI content + E-E-A-T]

- Focus on helpful content, not just keywords
- Build topical authority clusters
- Optimize for Google's AI Overviews

**Nathan Gotch's SEO Approach:**
[Retrieved content about Search Everywhere Optimization]

- SEO = Search Everywhere Optimization now
- Target YouTube, LinkedIn, Reddit, not just Google
- Use AI to create platform-specific content variants

**Combined Strategy:**
1. Build content cluster on "AI marketing automation"
2. Create YouTube tutorials (ranks in Google + YouTube)
3. Repurpose to LinkedIn thought leadership
4. Use Reddit for community validation signals
```

### Example 3: Community-Led Growth (Greg Isenberg)

**Query:**
```
"How do I build community around my AI productivity tool?"
```

**Expected Response:**
```markdown
**Greg Isenberg's Community Framework:**

[Retrieved from NotebookLM: Community-building videos]

**Phase 1: Vibe Check (Month 1-2)**
- Find where your ideal users already hang out
- Join conversations, don't pitch
- Identify the "energy" — what gets them excited?

**Phase 2: Minimum Viable Community (Month 3)**
- Discord or Slack, not Facebook
- 1 channel: #wins (social proof flywheel)
- You post first 20 wins yourself if needed

**Phase 3: Community-Led Product**
- Ship features the community requests
- Give power users early access
- Make them feel like co-creators

**Greg's Key Insight:** "Community isn't a channel, it's a moat"
```

## Common Patterns

### Pattern 1: Multi-Stage Funnel Question

```bash
# Question spans multiple domains
"I need help with my SaaS go-to-market: offer, SEO, and community"

# Response includes:
# - Alex Hormozi: Offer positioning
# - Neil Patel: SEO strategy  
# - Greg Isenberg: Community layer
```

### Pattern 2: Framework Deep-Dive

```bash
# Request specific framework
"Explain Alex Hormozi's Value Equation for my use case"

# Response:
# - Retrieves original explanation from NotebookLM
# - Maps framework to your specific scenario
# - Includes anti-patterns from KB
```

### Pattern 3: Comparative Analysis

```bash
# Compare expert approaches
"How would Dan Koe vs Alex Hormozi approach pricing a course?"

# Response:
# - Dan Koe: Personal brand, premium positioning, audience relationship
# - Alex Hormozi: Value equation, enterprise pricing, sales frameworks
# - Synthesis: When to use each approach
```

## Troubleshooting

### Issue: Generic or Vague Response

**Problem:** Response doesn't sound like the expert

**Solution:**
- Check if question is in expert's domain
- Request named expert explicitly
- Ask for specific framework by name

```bash
# Instead of: "How do I market?"
# Try: "Ask Alex Hormozi: How should I position my offer using the Value Equation?"
```

### Issue: No Retrieval Evidence

**Problem:** Response lacks [Retrieved from NotebookLM] markers

**Solution:**
- Expert may not have covered this topic
- Reframe question to match expert's known content areas
- Check expert domain table above

### Issue: Multi-Expert Overload

**Problem:** Too many perspectives for a simple question

**Solution:**
- Ask for single expert
- Rephrase as focused question

```bash
# Instead of: "How do I grow?"
# Try: "What's Neil Patel's SEO strategy for [specific use case]?"
```

### Issue: Outdated Framework

**Problem:** Expert's content is from 2023-2024

**Solution:**
- Ask for principles, not tactics
- Request ⚠️ extrapolation for 2026 context

```bash
"What would Neil Patel's SEO principles be for 2026, given AI Overviews?"
```

## Advanced Usage

### Combine with Your Context

```bash
# Provide your specific situation
"Here's my SaaS: [details]. Ask Alex Hormozi how to price it."

# Attach data
"My conversion rate is 2%. Ask Neil Patel to audit my funnel."
```

### Sequential Expert Consultation

```bash
# Step 1: Offer with Hormozi
"Alex Hormozi: Review my offer"

# Step 2: Traffic with Neil Patel  
"Neil Patel: Now how do I drive traffic to this offer?"

# Step 3: Community with Greg Isenberg
"Greg Isenberg: Should I add a community layer?"
```

### Export Expert Advice

```bash
# Generate structured output
"Create a marketing strategy doc consulting:
- Alex Hormozi for offer
- Neil Patel for SEO
- Greg Isenberg for community"

# Output: Markdown doc with all expert perspectives organized
```

## Tools Used Internally

The panel is built with:

- **yt-dlp**: YouTube URL batch collection
- **notebooklm-py**: Programmatic NotebookLM access
- **NotebookLM Pro**: 300 sources/notebook indexing
- **Claude Code Skills**: Persona Protocol + dual-layer fusion

You don't need to install these separately — they're embedded in the skill.

## Best Practices

1. **Be specific**: "How do I price?" → "How do I price a B2B SaaS at $10k ACV?"
2. **Name the expert**: When you know who you want
3. **Provide context**: Share your industry, stage, constraints
4. **Request frameworks**: Ask for specific models by name
5. **Iterate**: Start with one expert, then consult others

## License

MIT — Free to use, modify, and distribute.
