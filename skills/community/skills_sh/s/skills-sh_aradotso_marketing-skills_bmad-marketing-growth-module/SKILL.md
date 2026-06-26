---
name: bmad-marketing-growth-module
description: AI-powered marketing team module for BMAD Framework with 14 specialized agents and 6 workflows for complete SaaS growth
triggers:
  - set up marketing automation for my SaaS
  - create a social media campaign across multiple platforms
  - plan and execute a product launch strategy
  - generate SEO-optimized content with AI agents
  - build a content marketing pipeline
  - audit my growth metrics and marketing performance
  - coordinate marketing activities with AI orchestration
  - deploy specialized marketing agents for different channels
---

# BMAD Marketing Growth Module

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

## Overview

The BMAD Marketing Growth Module provides a complete AI-powered marketing team with 14 specialized agents organized in a 3-tier hierarchy and 6 coordinated workflows. Built on the BMAD Framework, it handles everything from high-level marketing strategy to platform-specific social media execution for SaaS companies.

**Key capabilities:**
- Marketing orchestration with delegation patterns
- Multi-platform social media automation (Twitter, LinkedIn, Reddit, YouTube, Discord, Instagram, TikTok, Pinterest)
- SEO strategy and content optimization
- Product launch coordination
- Growth analytics and KPI tracking
- Content pipeline automation with memory-enabled agents

## Installation

### Prerequisites

The BMAD Framework Core must be installed in your project. This module extends BMAD's agent system.

### Quick Install (BMAD Installer)

```bash
bmad install marketing-growth
```

### Manual Installation

1. Clone or download the module:

```bash
cd your-project
mkdir -p _bmad
cd _bmad
git clone https://github.com/MatthiasMRC/bmad-marketing-growth.git marketing-growth
```

2. Copy memory files:

```bash
cp -r marketing-growth/_memory/* _bmad/_memory/
```

3. Verify structure:

```
your-project/
├── _bmad/
│   ├── marketing-growth/
│   │   ├── module.yaml
│   │   ├── config.yaml
│   │   ├── agents/
│   │   ├── workflows/
│   │   └── _memory/
│   └── _memory/
│       ├── marketing-orchestrator/
│       ├── content-architect/
│       └── ... (agent sidecars)
```

## Configuration

Edit `_bmad/marketing-growth/config.yaml`:

```yaml
# User Configuration
user_name: "Your Name"
communication_language: "English"  # English, French, Spanish
company_name: "Your SaaS Company"
company_url: "https://yoursaas.com"
primary_channel: "twitter"  # twitter, linkedin, youtube, instagram, tiktok
target_audience: "B2B SaaS founders"

# Module Settings
module_code: "marketing-growth"
version: "1.0.0"

# Agent Behavior
auto_delegation: true  # Allow agents to delegate automatically
require_confirmation: false  # Set to true for manual approval of delegations
verbose_logging: true  # Enable detailed workflow logs
```

## Agent Architecture

### Tier 1: Orchestrator

**Max Growth** (`/marketing-growth:marketing-orchestrator` or `/max-growth`)
- Coordinates all marketing activities
- Delegates to specialized agents
- Manages workflows and strategy

### Tier 2: Department Leads

- **Milo Page** (`/milo-page`) - Content Architect
- **Quinn Crawler** (`/quinn-crawler`) - SEO Strategist
- **Nova Reach** (`/nova-reach`) - Social Media Strategist
- **Luna Blast** (`/luna-blast`) - Launch Coordinator
- **Pixel Metrics** (`/pixel-metrics`) - Growth Analyst

### Tier 3: Platform Specialists

- **Vex Thread** (`/vex-thread`) - Twitter/X
- **Karma Ken** (`/karma-ken`) - Reddit
- **Ivy Pro** (`/ivy-pro`) - LinkedIn
- **Yuri Views** (`/yuri-views`) - YouTube
- **Disco Dave** (`/disco-dave`) - Discord
- **Indy Grid** (`/indy-grid`) - Instagram
- **Tikko Viral** (`/tikko-viral`) - TikTok
- **Penny Pin** (`/penny-pin`) - Pinterest

## Core Workflows

### Marketing Strategy (MS)

Comprehensive strategy development and coordination.

```
/max-growth

# Select: [MS] Marketing Strategy
```

This workflow:
1. Analyzes your SaaS and market
2. Develops multi-channel strategy
3. Coordinates content, SEO, and social plans
4. Creates execution timeline
5. Delegates to relevant specialists

### Content Pipeline (CP)

Automated content creation from brief to publication.

```
/milo-page

# Select: [CP] Content Pipeline
```

Stages:
1. Content brief definition
2. Research and outline
3. First draft writing
4. SEO optimization (delegates to Quinn)
5. Social distribution (delegates to Nova)
6. Publication and promotion

### Social Campaign (SC)

Multi-platform social media campaign execution.

```
/nova-reach

# Select: [SC] Social Campaign
```

Nova delegates to platform specialists:
- Twitter threads via Vex Thread
- LinkedIn posts via Ivy Pro
- Reddit marketing via Karma Ken
- Video content via Yuri Views
- Community engagement via Disco Dave

### Launch Sequence (LS)

J-14 to post-launch coordination.

```
/luna-blast

# Select: [LS] Launch Sequence
```

Timeline:
- **J-14**: Pre-launch buzz, teaser content
- **J-7**: Countdown, early access
- **J-Day**: Launch execution across all channels
- **J+7**: Post-launch momentum, feedback collection

### Growth Audit (GA)

Comprehensive KPI analysis and recommendations.

```
/pixel-metrics

# Select: [GA] Growth Audit
```

Analyzes:
- Traffic sources and trends
- Conversion funnels
- Social media performance
- Content effectiveness
- SEO rankings
- Provides actionable recommendations

### SEO Sprint (SS)

Quick-win SEO optimization.

```
/quinn-crawler

# Select: [SS] SEO Sprint
```

Process:
1. Technical SEO audit
2. Keyword gap analysis
3. Content optimization opportunities
4. Quick wins implementation
5. Monitoring setup

## Usage Patterns

### Starting a New Campaign

```
# 1. Initialize with orchestrator
/max-growth

# User input
I'm launching a new feature next month. I need a complete marketing campaign.

# Max Growth will:
# - Analyze the feature
# - Delegate to Luna Blast for launch planning
# - Delegate to Milo Page for content
# - Delegate to Nova Reach for social distribution
# - Coordinate timeline
```

### Platform-Specific Content

```
# Direct access to specialist
/vex-thread

# User input
Create a 10-tweet thread about our new AI features, make it viral

# Vex Thread will:
# - Research your AI features
# - Create hook-driven thread
# - Add viral elements (curiosity gaps, stats, stories)
# - Format for Twitter
# - Suggest posting times
```

### Content SEO Optimization

```
# Start with content agent
/milo-page

# User input
I wrote this blog post about API security, can you optimize it for SEO?

# Milo will:
# - Review the content
# - Delegate to Quinn Crawler for SEO analysis
# - Receive keyword recommendations
# - Optimize content structure
# - Add internal linking suggestions
```

### Cross-Platform Launch

```
/luna-blast

# Select: [LS] Launch Sequence

# Luna coordinates:
# - Email campaign (via content team)
# - Social media blitz (via Nova Reach)
#   - Twitter threads (Vex)
#   - LinkedIn posts (Ivy)
#   - Reddit AMAs (Karma Ken)
#   - YouTube demo (Yuri)
# - Blog posts (Milo)
# - SEO optimization (Quinn)
# - Analytics tracking (Pixel)
```

## Agent Memory System

Each agent has a sidecar memory system in `_bmad/_memory/{agent-name}/`:

```
_memory/
├── marketing-orchestrator/
│   ├── memory.md          # Previous strategies, learnings
│   ├── context.md         # Current company context
│   └── instructions.md    # Custom instructions
├── content-architect/
│   ├── memory.md          # Content themes, successful formats
│   └── context.md         # Brand voice, content calendar
└── twitter-ghostwriter/
    ├── memory.md          # Viral patterns, engagement data
    └── context.md         # Twitter strategy, posting schedule
```

### Updating Agent Memory

Agents automatically update their memories after tasks. You can also manually update:

```bash
# Edit memory file
vim _bmad/_memory/marketing-orchestrator/context.md
```

Example context update:

```markdown
# Company Context

## Product
- SaaS: AI-powered project management
- Target: B2B teams 10-100 people
- USP: 10x faster task automation

## Current Priorities
- Q2 2024: Focus on enterprise features
- Key launch: AI assistant (April 15)
- Growth goal: 1000 → 5000 MRR

## Brand Voice
- Professional but friendly
- Data-driven claims
- Founder story emphasis

## Channels Priority
1. Twitter (primary)
2. LinkedIn (secondary)
3. Product Hunt (launches)
```

## Delegation Patterns

Agents follow a hierarchical delegation model:

```
Max Growth (orchestrator)
    ↓ delegates strategy execution
Milo Page (content)
    ↓ delegates SEO optimization
Quinn Crawler (SEO)
    ↓ returns optimized keywords
Milo Page (content)
    ↓ delegates distribution
Nova Reach (social)
    ↓ delegates platform-specific
Vex Thread + Ivy Pro + Karma Ken (platforms)
```

### Automatic Delegation

With `auto_delegation: true`:

```
/max-growth

# User: "Create and distribute a blog post about our new API"

# Automatic flow:
# Max Growth → Milo Page (content creation)
# Milo Page → Quinn Crawler (SEO optimization)
# Milo Page → Nova Reach (distribution strategy)
# Nova Reach → Vex Thread (Twitter thread)
# Nova Reach → Ivy Pro (LinkedIn post)
# Pixel Metrics ← Tracking setup
```

### Manual Delegation

With `require_confirmation: true`:

```
# Agent will ask before delegating:
"I recommend delegating SEO optimization to Quinn Crawler. Proceed? [Y/n]"
```

## Platform-Specific Examples

### Twitter Strategy (Vex Thread)

```
/vex-thread

# Input
Create a week of tweets for our product launch

# Output format
🧵 THREAD STRUCTURE

Hook Tweet:
"Most SaaS founders waste 20+ hours/week on [problem].

Here's how we cut that to 2 hours with AI automation 👇"

Tweet 2: Problem amplification
Tweet 3: Failed solutions
Tweet 4: The insight/turning point
Tweet 5: Our solution intro
Tweet 6: How it works
Tweet 7: Results/proof
Tweet 8: CTA

---

📅 DAILY TWEETS (Day 1-7)

Day 1: Hook thread
Day 2: Customer testimonial
Day 3: Behind-the-scenes
Day 4: Feature highlight
Day 5: Founder story
Day 6: Launch countdown
Day 7: LAUNCH announcement
```

### LinkedIn B2B (Ivy Pro)

```
/ivy-pro

# Input
Write a thought leadership post about AI in project management

# Output format
📝 LINKEDIN POST

Hook: Personal story or contrarian take
Body: Framework or insights (3-5 points)
Visual: Suggested carousel topics
CTA: Comment prompt

Suggested carousel:
- Slide 1: Title + hook
- Slides 2-4: Main framework
- Slide 5: CTA + profile

Hashtags: #ProjectManagement #AIProductivity #SaaS
```

### Reddit Growth (Karma Ken)

```
/karma-ken

# Input
Promote our tool in project management subreddits without being salesy

# Strategy output
🎯 SUBREDDIT TARGETS

r/projectmanagement (500K members)
- Karma requirement: 100+
- Strategy: Help posts, case studies
- Best time: Tuesday-Thursday 9am EST

r/SaaS (200K members)
- Strategy: "Show HN" style posts
- Approach: Problem-solution storytelling

SAMPLE POSTS:

Title: "I built a tool that automates PM busy work (here's what I learned)"
Content: [Story format, tool mention in comments only]

Title: "What's the biggest time-waster in your PM workflow?"
Content: [Survey post, collect insights, offer solution in comments]
```

## Troubleshooting

### Agent Not Found

```bash
# Check module installation
ls _bmad/marketing-growth/agents/

# Verify BMAD core is installed
bmad version

# Re-run installer
bmad install marketing-growth --force
```

### Delegation Failures

If agents aren't delegating properly:

1. Check `config.yaml`:
```yaml
auto_delegation: true
```

2. Verify agent memory files exist:
```bash
ls _bmad/_memory/*/memory.md
```

3. Check workflow files:
```bash
ls _bmad/marketing-growth/workflows/
```

### Memory Not Persisting

Ensure agent has write permissions:

```bash
chmod -R 755 _bmad/_memory/
```

Check memory file format:

```markdown
# Memory: Marketing Orchestrator

## Completed Strategies
- [2024-01-15] Product launch for Feature X
  - Result: 500 signups
  - Learning: Twitter + Product Hunt combo works best

## Active Campaigns
- Q1 Content Sprint (ongoing)
```

### Custom Agent Instructions

Add custom behavior to `_bmad/_memory/{agent}/instructions.md`:

```markdown
# Custom Instructions

## Content Architect (Milo)

### Brand Guidelines
- Always include data/stats
- Use "we" not "I"
- Keep paragraphs under 3 lines
- Add TL;DR to long posts

### Content Rules
- No hype words (revolutionary, game-changing)
- Focus on specific outcomes
- Include customer quotes when possible
```

## Advanced Patterns

### Multi-Stage Campaign

```
# Stage 1: Strategy
/max-growth
[MS] Marketing Strategy → Define Q2 campaign

# Stage 2: Content Creation
/milo-page
[CP] Content Pipeline → Create supporting content

# Stage 3: SEO Optimization
/quinn-crawler
[SS] SEO Sprint → Optimize all content

# Stage 4: Launch
/luna-blast
[LS] Launch Sequence → Execute launch

# Stage 5: Analytics
/pixel-metrics
[GA] Growth Audit → Measure results
```

### Custom Workflow Creation

Create new workflows in `_bmad/marketing-growth/workflows/custom-workflow/`:

```markdown
# Custom Workflow: Webinar Promotion

## Trigger: [WP]

## Lead Agent: Luna Blast

## Steps:
1. Luna: Create webinar promotion plan
2. Delegate to Milo: Landing page copy
3. Delegate to Quinn: SEO for registration page
4. Delegate to Nova: Social media promotion
   - Vex: Twitter thread + daily reminders
   - Ivy: LinkedIn event + posts
   - Yuri: Promo video
5. Delegate to Pixel: Tracking setup

## Timeline: J-21 to webinar day
```

## Integration Examples

### With External Tools

```javascript
// Example: Export Max Growth strategy to Notion
// (This would be implemented in your codebase)

const { execSync } = require('child_process');
const fs = require('fs');

// Run Max Growth workflow
const strategy = execSync('/max-growth --workflow=MS --export-json').toString();

// Parse and send to Notion
const strategyData = JSON.parse(strategy);
await notion.pages.create({
  parent: { database_id: process.env.NOTION_DB_ID },
  properties: {
    Title: { title: [{ text: { content: strategyData.title } }] },
    Status: { select: { name: 'In Progress' } },
    Channel: { multi_select: strategyData.channels.map(c => ({ name: c })) }
  }
});
```

### With Calendar Systems

```python
# Example: Schedule social posts from Nova Reach
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def schedule_social_posts(posts_json):
    """Schedule posts from Nova Reach campaign to Google Calendar"""
    
    credentials = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_SERVICE_ACCOUNT_FILE']
    )
    
    service = build('calendar', 'v3', credentials=credentials)
    calendar_id = os.environ['MARKETING_CALENDAR_ID']
    
    for post in posts_json['scheduled_posts']:
        event = {
            'summary': f"{post['platform']}: {post['title']}",
            'description': post['content'],
            'start': {'dateTime': post['scheduled_time']},
            'end': {'dateTime': post['scheduled_time']},
            'reminders': {'useDefault': False, 'overrides': [
                {'method': 'popup', 'minutes': 30}
            ]}
        }
        service.events().insert(calendarId=calendar_id, body=event).execute()
```

## Environment Variables

The module respects these environment variables:

```bash
# Configuration override
export BMAD_MG_CONFIG_PATH="/custom/path/config.yaml"

# Language override
export BMAD_MG_LANGUAGE="Spanish"

# Logging
export BMAD_MG_VERBOSE="true"

# API Keys for integrations (if needed)
export TWITTER_API_KEY="your-key"
export LINKEDIN_ACCESS_TOKEN="your-token"
export GOOGLE_ANALYTICS_ID="GA-XXXXXX"
```

## Best Practices

1. **Start with Max Growth** for complex campaigns - let orchestration handle delegation
2. **Use specialist agents directly** for single-platform tasks
3. **Update agent memories** after successful campaigns to improve future suggestions
4. **Set realistic timelines** in config - agents will plan accordingly
5. **Review delegation chains** in verbose mode to optimize workflows
6. **Customize instructions** per agent for brand-specific behavior
7. **Use workflows** for repeatable processes, direct agents for one-off tasks

## Resources

- GitHub: https://github.com/MatthiasMRC/bmad-marketing-growth
- Author Twitter: [@matthias_mrc](https://x.com/matthias_mrc)
- BMAD Framework: https://bmad.ai (hypothetical - adjust if real URL exists)
- Support: https://buymeacoffee.com/matthiasmrc
