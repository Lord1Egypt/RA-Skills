---
name: marketing-os-starter
description: Set up and run an AI marketing team with 4 specialized agents, battle-tested frameworks, and persistent memory for campaign execution
triggers:
  - "set up marketing os"
  - "create ai marketing team"
  - "configure marketing agents"
  - "run marketing campaign with agents"
  - "deploy marketing os starter"
  - "initialize marketing automation system"
  - "build marketing agent pipeline"
  - "launch ai marketing workflow"
---

# Marketing OS Starter

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## What It Does

Marketing OS Starter is a complete AI marketing team built for Claude Code. It includes 4 specialized agents (Orchestrator, Researcher, Strategist, Copywriter), 5 marketing skills, and battle-tested frameworks that turn research into creative briefs into finished copy — all with persistent memory that compounds across sessions.

The system runs on structured agent handoffs (JSON schemas), enforces brand voice automatically, and applies proven frameworks like the 6 Hook Formulas and BOFU Domination to every piece of output.

## Installation

```bash
# Clone the repository
git clone https://github.com/ericosiu/marketing-os-starter.git my-marketing-os
cd my-marketing-os
```

The project structure:
```
marketing-os-starter/
├── CLAUDE.md                    # Main context file - your agency priorities
├── .claude/
│   ├── agents/marketing-os/     # 4 specialist agents
│   │   ├── orchestrator.md
│   │   ├── researcher.md
│   │   ├── strategist.md
│   │   └── copywriter.md
│   ├── skills/                  # 5 marketing skills
│   │   ├── research.md
│   │   ├── campaign-brief.md
│   │   ├── copywriting.md
│   │   ├── social-content.md
│   │   └── email-sequence.md
│   └── rules/                   # Intent routing
│       └── proactive-marketing.md
├── brands/                      # Agency + client brand files
│   └── your-agency/
│       ├── BRAND.md
│       ├── voice.md
│       └── clients/
├── memory/                      # Persistent memory
│   └── marketing-os/
│       ├── brand-voice.md
│       ├── campaign-history.md
│       ├── marketing-wisdom.md
│       └── working.md
├── schemas/                     # JSON contracts for handoffs
│   ├── audience-profile.json
│   ├── creative-brief.json
│   └── copy-deliverable.json
└── examples/                    # Sample outputs
```

## Initial Configuration

### 1. Configure CLAUDE.md

This is the brain of your system. Claude reads it at the start of every session.

```markdown
# Your Agency Context

**Agency**: [Your Agency Name]
**Primary Service**: [What you do]

## Priorities (Next 12 Months)

1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Standards

**Minimum ROI Bar**: [X]x ROAS or [Y]% conversion lift
**Never Accept**: "Awareness" campaigns without revenue tracking

## Client Portfolio

- **[Client Name]**: [Brief description]
- **[Client Name]**: [Brief description]
```

### 2. Set Up Your Agency Brand

Edit `brands/your-agency/BRAND.md`:

```markdown
# [Your Agency Name]

## Overview
[2-3 sentence value proposition]

## What We Do
- [Service 1]
- [Service 2]
- [Service 3]

## Public Client Examples
- [Client success story 1]
- [Client success story 2]
```

Edit `brands/your-agency/voice.md`:

```markdown
# Voice Guidelines

## Tone
- Direct and data-driven
- No jargon or corporate speak
- Numbers over adjectives

## Always Use
- Specific metrics (e.g., "3.4x ROI" not "great results")
- Active voice
- Short sentences

## Never Use
- leverage, synergize, value-add, paradigm
- "excited to announce"
- Corporate platitudes

## Examples That Nail Our Voice

### Good
"We cut their CAC from $847 to $312 in 6 weeks. Here's the breakdown."

### Bad
"We're excited to share that our innovative approach helped drive meaningful results."
```

### 3. Add Your First Client

Copy the example client template:

```bash
cp -r brands/your-agency/clients/example-client brands/your-agency/clients/acme-corp
```

Edit `brands/your-agency/clients/acme-corp/BRAND.md`:

```markdown
# Acme Corp

## Company Overview
- **Industry**: [SaaS/E-commerce/etc]
- **Target Market**: [B2B/B2C, company size, role]
- **Product**: [What they sell]

## Voice
[How this specific client speaks - may differ from agency voice]

## Past Campaigns
None yet.
```

## Key Commands and Workflows

### Running a Complete Campaign Pipeline

Start Claude Code and describe your need naturally:

```
"I need to promote Acme Corp's new analytics feature to marketing directors at B2B SaaS companies. Budget $5K, 45-day timeline."
```

The Orchestrator will automatically:
1. Invoke **Researcher** → produces `audience-profile.json`
2. Invoke **Strategist** → produces `creative-brief.json`
3. Invoke **Copywriter** → produces finished copy

### Manual Skill Invocation

You can also call skills directly:

```
/research
Target audience: Marketing directors at B2B SaaS companies (50-500 employees)
Focus: Pain points around marketing attribution
```

```
/campaign-brief
Audience: [reference research output]
Goal: 30 demo requests
Timeline: 45 days
Budget: $5K
```

```
/copywriting
Brief: [reference brief output]
Deliverables: 5 LinkedIn posts, 1 landing page hero
```

```
/social-content
Topic: Marketing attribution mistakes
Platform: LinkedIn
Quantity: 5 posts
Target: Marketing directors
```

```
/email-sequence
Type: Nurture sequence
Segment: Ghost users (signed up, 0 actions)
Length: 5 emails over 2 weeks
Goal: First dashboard connection
```

## Agent Handoff Pattern

Agents communicate through structured JSON. Example flow:

**Researcher Output** (`memory/marketing-os/campaigns/acme-q2/audience-profile.json`):
```json
{
  "target_audience": {
    "role": "Marketing Director",
    "company_size": "50-500 employees",
    "industry": "B2B SaaS"
  },
  "pain_points": [
    {
      "pain": "Attribution reporting takes 2-3 days to compile",
      "evidence": "14 Reddit posts in r/marketing, 23 G2 reviews",
      "quote": "I spend more time building reports than reading them"
    }
  ],
  "voice_of_customer": {
    "actual_phrases": [
      "I spend more time building reports than reading them",
      "My CEO thinks marketing is a cost center because I can't prove otherwise"
    ]
  }
}
```

**Strategist Reads** the audience profile and outputs (`creative-brief.json`):
```json
{
  "campaign_name": "Acme Attribution Fix",
  "core_message": "Stop spending 2 days building reports. See real-time attribution in 15 minutes.",
  "proof_points": [
    "14 Reddit posts confirm this pain point",
    "Average time saved: 2.3 days per month"
  ],
  "growth_playbook": "Playbook 6: Marketing Mistakes Content",
  "hook_formula": "Harsh Reality",
  "deliverables": {
    "landing_page_hero": 1,
    "linkedin_posts": 5,
    "email_sequence": 3
  }
}
```

**Copywriter Reads** the brief and produces final copy with the selected hook formula applied.

## Working with Memory Files

### Campaign History

After each campaign, the Strategist logs results to `memory/marketing-os/campaign-history.md`:

```markdown
## Campaign: Acme Attribution Fix
- **Date**: 2026-05-15
- **Channel**: LinkedIn + Landing Page
- **Result**: 47 demo requests, 12 closed deals
- **What Worked**: "Harsh Reality" hook + specific time-saved stat
- **What Didn't**: Generic "learn more" CTA underperformed vs "See your attribution now"
```

This memory prevents repeating failed approaches and reinforces what works.

### Brand Voice Evolution

As you approve copy, add winning examples to `memory/marketing-os/brand-voice.md`:

```markdown
## Approved Headlines (2026-05)

### Hook: Harsh Reality
"Harsh reality: your marketing attribution is lying to you."
- **Campaign**: Acme Q2
- **Performance**: 8.2% CTR (2.3x average)

### Hook: Contrarian Challenge
"Everyone says 'just pick an attribution model.' That's surface-level thinking."
- **Campaign**: Acme Q2
- **Performance**: 6.7% CTR
```

After 5-10 campaigns, the Copywriter matches your voice without explicit direction.

### Task Queue

`memory/marketing-os/working.md` tracks the current pipeline:

```markdown
# Current Tasks

## In Progress
- [ ] Acme Q2 Campaign - waiting for client approval on headlines
- [ ] Research for DataPulse competitive analysis

## Blocked
- [ ] Email sequence for Acme - need segment data from client

## Completed This Week
- [x] Landing page copy for Acme Attribution Fix
- [x] 5 LinkedIn posts for Acme Q2
```

You can resume exactly where you left off in any session.

## Real Usage Examples

### Example 1: Full Campaign from Scratch

```
User: "Build a campaign to get 30 demo requests for Acme's new attribution feature. Target marketing directors at B2B SaaS companies, budget $5K, 45 days."

Orchestrator: Detecting new campaign request. Invoking full pipeline.

[Researcher produces audience-profile.json with 87 data points]

Strategist: Reading audience profile... Core pain point identified: "2-3 days per month wasted on attribution reports."

[Strategist produces creative-brief.json selecting Growth Playbook #6 and Harsh Reality hook]

Copywriter: Reading creative brief... Applying Harsh Reality hook formula.

[Copywriter produces 5 LinkedIn posts, 1 landing page hero, 3-email sequence]

Orchestrator: Campaign deliverables ready. Files saved to memory/marketing-os/campaigns/acme-q2/.
```

### Example 2: Research Only

```
User: "Who should we target for a marketing attribution tool?"

[Orchestrator detects research intent, invokes Researcher]

Researcher: Conducting BOFU-first research...
- Analyzing search intent for "best marketing attribution tool"
- Scraping G2 reviews for voice-of-customer quotes
- Cross-referencing Reddit r/marketing pain points

[Produces audience-profile.json with job titles, pain points, actual quotes]
```

### Example 3: Writing with Existing Brief

```
User: "Write 5 LinkedIn posts using the Acme Q2 brief."

[Orchestrator detects copywriting intent with existing brief, invokes Copywriter]

Copywriter: Reading brief at memory/marketing-os/campaigns/acme-q2/creative-brief.json...
- Hook formula: Harsh Reality
- Proof point: "2.3 days saved per month"
- Voice check: Loading brands/your-agency/clients/acme-corp/voice.md

[Produces 5 posts, each with different hook formula variation]
```

## Configuration Reference

### Agent Roles

| Agent | File | Primary Function |
|-------|------|------------------|
| Orchestrator | `.claude/agents/marketing-os/orchestrator.md` | Routes requests, tracks pipeline, never writes copy |
| Researcher | `.claude/agents/marketing-os/researcher.md` | Produces audience profiles, competitive analysis (BOFU-first) |
| Strategist | `.claude/agents/marketing-os/strategist.md` | Creates campaign briefs, matches growth playbooks |
| Copywriter | `.claude/agents/marketing-os/copywriter.md` | Writes finished copy using hook formulas |

### Skill Triggers

The proactive routing system in `.claude/rules/proactive-marketing.md` auto-detects:

- **Research triggers**: "who's our audience", "competitive landscape", "pain points"
- **Brief triggers**: "plan a campaign", "what should we say", "strategy"
- **Copy triggers**: "write copy", "landing page", "headline"
- **Social triggers**: "LinkedIn post", "tweet", "social content"
- **Email triggers**: "drip campaign", "welcome sequence", "nurture"

### Framework Reference

All frameworks live in `memory/marketing-os/marketing-wisdom.md`:

**6 Hook Formulas**:
1. Observation + Stat: "I analyzed 500 landing pages. 89% make the same mistake."
2. Contrarian Challenge: "Everyone says X. That's surface-level thinking."
3. Harsh Reality: "Harsh reality: your approach is costing you $X."
4. Personal Limitation: "I used to believe X. Then I ran the numbers."
5. Social Proof: "I sat in on 12 board meetings. Same scene every time."
6. Simple Declarative: "Your attribution is broken. Here's why."

**7 Growth Playbooks** (abbreviated):
- Playbook 1: Free Tool Flywheel
- Playbook 2: LLM Citation Strategy
- Playbook 3: Vertical Domination
- Playbook 6: Marketing Mistakes Content (3-5x engagement)
- Playbook 7: Data Network Effects

## Common Patterns

### Pattern: Multi-Client Agency Setup

```bash
brands/
├── your-agency/
│   ├── BRAND.md          # Your agency brand
│   ├── voice.md          # Your agency voice
│   └── clients/
│       ├── acme-corp/
│       │   ├── BRAND.md
│       │   └── voice.md  # May differ from agency voice
│       ├── techstart/
│       │   ├── BRAND.md
│       │   └── voice.md
│       └── dataflow/
│           ├── BRAND.md
│           └── voice.md
```

When starting a campaign, specify the client:

```
"Build a campaign for Acme Corp's new feature..."
```

The Orchestrator will load `brands/your-agency/clients/acme-corp/` context automatically.

### Pattern: Testing with Example Brand

The repo includes a complete fictional agency:

```bash
brands/example-agency/
├── BRAND.md              # GrowthLab (fictional agency)
├── voice.md
└── clients/
    └── datapulse/        # DataPulse (fictional SaaS client)
        ├── BRAND.md
        └── voice.md
```

Test the full pipeline before setting up your own brand:

```
"Build a campaign for DataPulse targeting marketing directors at mid-market SaaS companies."
```

### Pattern: Voice Evolution Loop

1. **Generate copy** with current voice guidelines
2. **Review and edit** to match your actual voice
3. **Log approved examples** to `memory/marketing-os/brand-voice.md`
4. **Repeat** — the Copywriter learns from approved examples

After 5-10 campaigns, the voice matching becomes automatic.

## Troubleshooting

### Issue: Generic output despite brand voice file

**Problem**: Copy doesn't match your voice, sounds generic.

**Solution**: 
1. Check `brands/your-agency/voice.md` has specific examples (not just rules)
2. Add 2-3 "Good vs Bad" examples showing your voice clearly
3. Add winning headlines to `memory/marketing-os/brand-voice.md`

```markdown
## Examples That Nail Our Voice

### Good
"We cut their CAC from $847 to $312 in 6 weeks. Here's the breakdown."

### Bad
"We're excited to share that our innovative approach helped drive meaningful results."
```

### Issue: Agent doesn't invoke the right skill

**Problem**: You ask for research but get copy instead.

**Solution**: The proactive routing in `.claude/rules/proactive-marketing.md` may need more trigger phrases. Add your common phrasing:

```markdown
## Research Triggers
- "who should we target"
- "what do they care about"
- "audience analysis"
- [ADD YOUR PHRASE HERE]
```

Or invoke skills manually: `/research` instead of relying on auto-detection.

### Issue: Handoff breaks between agents

**Problem**: Strategist can't find Researcher output.

**Solution**: 
1. Check that Researcher saved output to `memory/marketing-os/campaigns/[campaign-name]/`
2. Verify JSON schema matches `schemas/audience-profile.json`
3. Manually reference the file:

```
"Create a brief using the research at memory/marketing-os/campaigns/acme-q2/audience-profile.json"
```

### Issue: Campaign history not influencing new campaigns

**Problem**: Strategist repeats a failed approach.

**Solution**: Ensure `memory/marketing-os/campaign-history.md` has clear "What Worked / What Didn't" sections:

```markdown
## Campaign: Acme Q1 Email Sequence
- **What Didn't Work**: Generic "Learn more" CTA → 1.2% CTR
- **Lesson**: Use specific action CTAs ("See your dashboard now" → 4.8% CTR)
```

The Strategist reads this file before creating new briefs.

### Issue: Memory files getting too large

**Problem**: `campaign-history.md` or `brand-voice.md` becomes unwieldy after 50+ campaigns.

**Solution**: Archive old campaigns quarterly:

```bash
# Create archive
mkdir -p memory/marketing-os/archive/2026-q1

# Move old campaign data
mv memory/marketing-os/campaigns/acme-q1 memory/marketing-os/archive/2026-q1/

# Keep only last 10 campaigns in campaign-history.md
# Move older entries to archive/campaign-history-2026-q1.md
```

## Advanced: Adding Custom Skills

To add a new skill (e.g., `/paid-ads`):

1. Create `.claude/skills/paid-ads.md`
2. Define the skill structure:

```markdown
---
name: paid-ads
description: Generate paid advertising strategy and ad copy
triggers:
  - "create paid ads"
  - "facebook ads"
  - "google ads campaign"
---

# Paid Ads Strategy

## What This Skill Does
[Description]

## Inputs Required
- Campaign brief (from Strategist)
- Budget and timeline
- Target platform (Meta, Google, LinkedIn)

## Outputs
- Platform-specific ad copy
- Targeting recommendations
- Budget allocation

## Process
[Step-by-step]
```

3. Add trigger phrases to `.claude/rules/proactive-marketing.md`
4. Create a schema if needed: `schemas/paid-ads-plan.json`

The Orchestrator will automatically detect and route requests.

## Integration with MCP Servers

To connect live data sources:

**Google Analytics (GA4)**:
```bash
# Install GA4 MCP server (example - adjust to actual implementation)
npm install -g @mcp/google-analytics

# Add to Claude configuration
# Reference in CLAUDE.md: "GA4 data available via MCP"
```

Then in research:
```
"Pull last 30 days of campaign data from GA4 for Acme Corp."
```

**HubSpot CRM**:
```bash
# Install HubSpot MCP server
npm install -g @mcp/hubspot

# Reference contact segments in research
"Get email engagement data for Ghost Users segment from HubSpot."
```

The Researcher and Strategist can query live data instead of relying solely on manual input.

---

**Start using Marketing OS**: Open Claude Code in your `marketing-os-starter` directory and describe your first campaign. The system handles the rest.
