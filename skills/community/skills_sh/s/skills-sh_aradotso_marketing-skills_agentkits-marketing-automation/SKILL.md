---
name: agentkits-marketing-automation
description: Enterprise AI marketing automation toolkit with 18 agents, 93 commands, and 28 skills for campaign planning, content creation, SEO, CRO, and growth workflows
triggers:
  - "help me with marketing automation"
  - "create a marketing campaign"
  - "optimize landing page conversion"
  - "generate SEO content"
  - "set up email sequences"
  - "plan product launch"
  - "improve conversion rate"
  - "create marketing copy"
---

# AgentKits Marketing Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Enterprise-grade AI marketing automation for Claude Code, Cursor, GitHub Copilot, and any AI assistant supporting agents & skills. Production-ready marketing agents, skills, commands, and workflows built for SaaS founders, marketers, and growth teams.

## What This Project Does

AgentKits Marketing is a comprehensive marketing automation toolkit containing:

- **18 Specialized Agents**: Attraction specialist, lead qualifier, email wizard, conversion optimizer, SEO specialist, etc.
- **93 Slash Commands**: Organized by category (campaign, content, SEO, CRO, growth)
- **28 Marketing Skills**: Psychology frameworks, copywriting, programmatic SEO, pricing strategy, etc.
- **Core Workflows**: Campaign lifecycle, sales pipeline, CRM automation

It transforms your AI coding assistant into a marketing expert that can plan campaigns, generate content, optimize conversions, and execute growth strategies.

## Installation

### Method 1: npx (Recommended)

Install everything (agents, skills, commands):

```bash
npx @aitytech/agentkits-marketing install
```

Platform-specific installation:

```bash
# Claude Code
npx @aitytech/agentkits-marketing install --platform claude

# Cursor IDE
npx @aitytech/agentkits-marketing install --platform cursor

# Windsurf
npx @aitytech/agentkits-marketing install --platform windsurf

# Cline
npx @aitytech/agentkits-marketing install --platform cline

# GitHub Copilot
npx @aitytech/agentkits-marketing install --platform copilot

# All platforms
npx @aitytech/agentkits-marketing install --platform all
```

### Method 2: Claude Code Plugin Marketplace

```bash
# Add marketplace
/plugin marketplace add aitytech/agentkits-marketing

# Install full suite
/plugin install agentkits-marketing@agentkits-marketing

# Or install components separately
/plugin install agentkits-marketing-skills@agentkits-marketing
/plugin install agentkits-marketing-agents@agentkits-marketing
/plugin install agentkits-marketing-commands@agentkits-marketing
```

### Method 3: Clone and Use

```bash
git clone https://github.com/aitytech/agentkits-marketing.git
cd agentkits-marketing
claude
```

### Method 4: Manual Installation

```bash
# Clone repository
git clone https://github.com/aitytech/agentkits-marketing.git

# Copy agents
cp agentkits-marketing/.claude/agents/*.md ~/.claude/agents/

# Copy commands
cp -r agentkits-marketing/.claude/commands/* ~/.claude/commands/

# Copy skills
cp -r agentkits-marketing/.claude/skills/* ~/.claude/skills/

# Copy workflows
cp -r agentkits-marketing/.claude/workflows/* ~/.claude/workflows/
```

## CLI Commands

```bash
# Show help
npx @aitytech/agentkits-marketing --help

# List supported IDEs
npx @aitytech/agentkits-marketing list-ides

# List available modules
npx @aitytech/agentkits-marketing list-modules

# Update existing installation
npx @aitytech/agentkits-marketing update
```

## Project Structure

```
agentkits-marketing/
├── .claude-plugin/
│   ├── plugin.json           # Plugin metadata
│   └── marketplace.json      # Marketplace catalog
├── .claude/
│   ├── agents/               # 18 marketing agents
│   ├── commands/             # 93 slash commands
│   ├── skills/               # 28 marketing skills
│   └── workflows/            # Core workflows
├── training/                 # Interactive lessons (multilingual)
└── docs/                     # Documentation
```

## Key Commands by Category

### Campaign Management

```bash
# Plan campaign
/campaign:plan "Q1 Product Launch"

# Create campaign brief
/campaign:brief "Feature announcement campaign"

# Analyze campaign performance
/campaign:analyze "campaign-data.csv"

# Generate OKRs
/campaign:okrs "Q1 marketing goals"
```

### Content Creation

```bash
# Generate blog post
/content:blog "AI marketing automation" "target keyword"

# Create landing page
/content:landing "new feature" "target audience"

# Write email sequence
/content:email "product launch" "trial users"

# Good vs bad copy
/content:good "Blog post about SaaS pricing"

# Edit and polish
/content:editing "draft content here"
```

### SEO Optimization

```bash
# Keyword research
/seo:keywords "ai marketing automation"

# Optimize content
/seo:optimize "content.md" "target keyword"

# SEO audit
/seo:audit "website-url.com"

# Programmatic SEO strategy
/seo:programmatic "SaaS alternatives pages"

# Schema markup
/seo:schema "product page"
```

### Conversion Rate Optimization (CRO)

```bash
# Landing page optimization
/cro:page "homepage conversion audit"

# Form optimization
/cro:form "lead capture form"

# Popup/modal optimization
/cro:popup "exit intent design"

# Signup flow optimization
/cro:signup "registration flow"

# Onboarding optimization
/cro:onboarding "user activation flow"

# Paywall/upgrade optimization
/cro:paywall "freemium conversion"

# A/B test setup
/test:ab-setup "headline variations"
```

### Growth Strategies

```bash
# Marketing ideas
/marketing:ideas "SaaS product description"

# Marketing psychology
/marketing:psychology "pricing objections"

# Launch strategy
/growth:launch "Product Hunt launch plan"

# Referral program
/growth:referral "viral loop design"

# Free tool strategy
/growth:free-tool "engineering as marketing"

# Pricing strategy
/pricing:strategy "tier structure and packaging"
```

### Research & Competitive Analysis

```bash
# Market research
/research:market "SaaS productivity tools"

# Competitor deep dive
/competitor:deep "competitor-url.com"

# Alternatives page
/competitor:alternatives "your-product vs competitor"
```

## Core Marketing Skills

### Marketing Psychology (70+ Mental Models)

```bash
# Access psychology frameworks
/marketing:psychology "pricing objections"

# Example triggers:
# - Anchoring and price perception
# - Loss aversion in CTAs
# - Social proof implementation
# - Scarcity and urgency tactics
# - Authority building
```

Key frameworks included:
- Cognitive biases (anchoring, loss aversion, social proof)
- Persuasion principles (Cialdini's 6 principles)
- Decision-making heuristics
- Emotional triggers
- Objection handling

### Marketing Ideas (140+ SaaS Strategies)

```bash
# Get strategic ideas
/marketing:ideas "B2B SaaS product for project management"

# Returns categorized strategies:
# - Content marketing
# - SEO tactics
# - Growth hacking
# - Partnerships
# - Community building
# - Product-led growth
```

### Copywriting

```bash
# High-converting copy
/content:good "Feature description for AI chatbot"

# Copy editing
/content:editing "existing draft to polish"
```

Frameworks included:
- PAS (Problem-Agitate-Solution)
- AIDA (Attention-Interest-Desire-Action)
- FAB (Features-Advantages-Benefits)
- 4 Ps (Picture-Promise-Proof-Push)

### Programmatic SEO

```bash
# Strategy planning
/seo:programmatic "alternatives pages for CRM tools"

# Template generation
# Creates scalable page templates for:
# - Alternatives pages
# - Comparison pages
# - Location-based pages
# - Category pages
```

Workflow:
1. Identify template opportunity
2. Define data sources
3. Create page templates
4. Set up automation
5. Implement internal linking

### Email Sequences

```bash
/content:email "trial onboarding sequence"

# Sequence types:
# - Welcome/onboarding
# - Trial nurture
# - Re-engagement
# - Upsell/cross-sell
# - Abandoned cart
# - Post-purchase
```

## Working with Agents

### Activate Specific Agents

```python
# In your prompt or command context
"@attraction-specialist help me generate leads"
"@conversion-optimizer audit this landing page"
"@email-wizard create a welcome sequence"
"@seo-specialist optimize this blog post"
```

### Core Agents and Their Roles

**Attraction Specialist**
- Lead generation strategies
- SEO optimization
- Landing page creation
- Top-of-funnel content

**Lead Qualifier**
- Lead scoring frameworks
- Segmentation strategies
- Qualification criteria
- Nurture path assignment

**Email Wizard**
- Email sequence creation
- Automation workflows
- Copy optimization
- A/B testing strategies

**Conversion Optimizer**
- Landing page CRO
- Form optimization
- A/B test design
- Funnel analysis

**SEO Specialist**
- Keyword research
- On-page optimization
- Technical SEO
- Content strategy

**Sales Enabler**
- Sales collateral creation
- Battlecards
- Case studies
- ROI calculators

## Common Usage Patterns

### Pattern 1: Full Campaign Launch

```bash
# 1. Research phase
/research:market "target market description"
/competitor:deep "main-competitor.com"

# 2. Strategy phase
/campaign:plan "Q2 Product Launch"
/marketing:ideas "product description"

# 3. Content creation
/content:landing "feature description" "target audience"
/content:email "launch announcement" "existing users"
/content:blog "feature deep dive" "primary keyword"

# 4. Optimization
/cro:page "landing page audit"
/seo:optimize "blog-post.md" "target keyword"

# 5. Testing
/test:ab-setup "headline variations"
```

### Pattern 2: Landing Page Optimization

```bash
# 1. Initial audit
/cro:page "existing landing page URL or content"

# 2. Copy improvement
/content:good "value proposition for [product]"

# 3. Form optimization
/cro:form "lead capture form design"

# 4. SEO optimization
/seo:optimize "landing-page.html" "target keyword"

# 5. A/B test setup
/test:ab-setup "CTA variations"
```

### Pattern 3: Content Marketing Workflow

```bash
# 1. Keyword research
/seo:keywords "topic area"

# 2. Content creation
/content:blog "topic" "primary keyword"

# 3. Optimization
/seo:optimize "draft.md" "keyword"

# 4. Schema markup
/seo:schema "article"

# 5. Internal linking strategy
# (Review output for linking opportunities)
```

### Pattern 4: Email Automation Setup

```bash
# 1. Sequence planning
/content:email "trial onboarding" "free trial users"

# 2. Copy refinement
/content:editing "email draft"

# 3. A/B test variants
/test:ab-setup "subject line variations"

# 4. Review with agent
"@email-wizard review this email sequence for deliverability"
```

## Configuration

### Environment Variables

No API keys required for core functionality. If integrating with external services:

```bash
# Example for analytics integration
export ANALYTICS_API_KEY=your_key_here
export CRM_API_KEY=your_key_here
export EMAIL_SERVICE_KEY=your_key_here
```

### Plugin Configuration

For Claude Code plugin users, configuration is in `.claude-plugin/plugin.json`:

```json
{
  "name": "agentkits-marketing",
  "version": "1.0.0",
  "description": "Enterprise AI marketing automation",
  "components": {
    "agents": ".claude/agents/**/*.md",
    "commands": ".claude/commands/**/*.md",
    "skills": ".claude/skills/**/*.md",
    "workflows": ".claude/workflows/**/*.md"
  }
}
```

### Customizing Agents

Edit agent files directly to adjust behavior:

```bash
# Edit agent configuration
~/.claude/agents/attraction-specialist.md
```

Modify:
- System prompts
- Response templates
- Decision frameworks
- Output formats

## Real-World Examples

### Example 1: Product Launch Campaign

```bash
# Step 1: Market research
/research:market "AI-powered project management tools for remote teams"

# Step 2: Competitive analysis
/competitor:deep "asana.com"
/competitor:deep "monday.com"

# Step 3: Campaign planning
/campaign:plan "Q2 Product Launch - AI Assistant Feature"

# Step 4: Create landing page
/content:landing "AI assistant that automates project updates" "project managers at tech companies"

# Step 5: Email sequence
/content:email "AI feature launch announcement" "existing customers"

# Step 6: Blog content
/content:blog "How AI is transforming project management" "ai project management"

# Step 7: Optimize
/cro:page "[paste landing page content]"
/seo:optimize "blog-draft.md" "ai project management"

# Step 8: Set up tests
/test:ab-setup "Headline: 'AI-Powered Updates' vs 'Never Write Status Reports Again'"
```

### Example 2: Conversion Rate Optimization Audit

```bash
# Homepage audit
/cro:page "
[Paste homepage HTML or describe current layout]
Product: SaaS analytics platform
Audience: Marketing managers
Goal: Free trial signups
"

# Signup flow optimization
/cro:signup "
Current flow:
1. Email input
2. Password creation
3. Company details (10 fields)
4. Team invitation
5. Billing info
Problem: 80% drop-off at step 3
"

# Form optimization
/cro:form "
Lead capture form fields:
- First name
- Last name
- Email
- Phone
- Company
- Company size
- Role
- Budget
Goal: Increase submissions
"

# A/B test design
/test:ab-setup "
Element: CTA button
Variant A: 'Start Free Trial'
Variant B: 'Get Started Free'
Variant C: 'Try It Free'
Goal: Click-through rate
"
```

### Example 3: SEO Content Strategy

```bash
# Keyword research
/seo:keywords "marketing automation for small businesses"

# Create pillar content
/content:blog "Complete guide to marketing automation" "marketing automation"

# Optimize
/seo:optimize "pillar-content.md" "marketing automation"

# Programmatic SEO for alternatives
/seo:programmatic "alternatives pages for marketing automation tools"

# Schema markup
/seo:schema "article"

# Create supporting content cluster
/content:blog "Email automation best practices" "email automation"
/content:blog "CRM automation workflows" "crm automation"
/content:blog "Social media automation tools" "social media automation"
```

### Example 4: Growth Strategy Brainstorm

```bash
# Get strategic ideas
/marketing:ideas "
Product: AI writing assistant for content marketers
Stage: Series A, $2M ARR
Team: 15 people
Goal: 10x ARR in 18 months
"

# Psychological frameworks
/marketing:psychology "
Objection: 'AI writing sounds robotic'
Context: B2B content marketers
Goal: Address quality concerns
"

# Launch strategy
/growth:launch "
Launching: Chrome extension version
Audience: Existing users + new prospects
Timeline: 4 weeks
"

# Referral program
/growth:referral "
Product: Monthly subscription ($49/mo)
Users: 5,000 active
Goal: Viral coefficient > 1
"

# Free tool strategy
/growth:free-tool "
Expertise: AI content optimization
Audience: Content marketers, SEO specialists
Goal: Lead generation
"
```

## Advanced Workflows

### Multi-Agent Collaboration

```python
# Campaign review workflow using multiple agents
"""
1. @attraction-specialist - Generate landing page
2. @copywriter - Refine messaging
3. @conversion-optimizer - CRO audit
4. @seo-specialist - SEO optimization
5. @brand-voice-guardian - Brand consistency check
"""

# Example orchestration
"@attraction-specialist create landing page for [product]"
# Review output
"@copywriter improve the value proposition section"
# Review output
"@conversion-optimizer audit for conversion issues"
# Review output
"@seo-specialist optimize for keyword [keyword]"
# Review output
"@brand-voice-guardian ensure this matches our brand voice"
```

### Campaign Workflow Automation

```bash
# Use primary workflow
# File: .claude/workflows/primary-workflow.md

# Workflow stages:
# 1. Research & Strategy
/research:market "target market"
/campaign:plan "campaign name"

# 2. Content Creation
/content:landing "product" "audience"
/content:email "message" "segment"

# 3. Optimization
/cro:page "landing page"
/seo:optimize "content" "keyword"

# 4. Launch & Monitor
/campaign:okrs "campaign goals"
/test:ab-setup "test variations"
```

## Troubleshooting

### Commands Not Working

```bash
# Verify installation
npx @aitytech/agentkits-marketing list-modules

# Reinstall
npx @aitytech/agentkits-marketing update

# Check platform-specific paths
# Claude Code: ~/.claude/
# Cursor: ~/.cursor/
# Windsurf: ~/.windsurf/
```

### Agents Not Responding

```bash
# Ensure agents are properly installed
ls ~/.claude/agents/

# Activate explicitly with @mention
"@attraction-specialist help with lead generation"

# Check agent file syntax (should be valid Markdown)
```

### Skills Not Available

```bash
# Verify skills directory
ls ~/.claude/skills/

# Reinstall skills only
/plugin install agentkits-marketing-skills@agentkits-marketing

# Or via npx
npx @aitytech/agentkits-marketing install --components skills
```

### Plugin Marketplace Issues

```bash
# Remove and re-add marketplace
/plugin marketplace remove aitytech/agentkits-marketing
/plugin marketplace add aitytech/agentkits-marketing

# Restart Claude Code
# Then reinstall
/plugin install agentkits-marketing@agentkits-marketing
```

### Output Quality Issues

**Problem**: Generic or low-quality responses

**Solutions**:
- Provide more context in prompts
- Use specific commands instead of general requests
- Activate relevant agents explicitly
- Reference specific skills or frameworks
- Provide examples of desired output

**Example**:
```bash
# Instead of:
"Write a landing page"

# Use:
/content:landing "
Product: AI email assistant
Audience: Busy executives
Key benefit: Save 10 hours/week on email
Objections: Privacy concerns, learning curve
CTA: Start 14-day trial
"
```

### Performance Optimization

**For large campaigns**:
- Break into smaller tasks
- Use specific commands for each phase
- Save intermediate outputs
- Chain commands sequentially

**For faster responses**:
- Use targeted skills instead of general agents
- Provide structured input formats
- Reference previous outputs by context

## Best Practices

1. **Start with Research**: Always begin campaigns with `/research:market` and `/competitor:deep`

2. **Layer Skills**: Combine multiple skills for comprehensive output (e.g., copywriting + psychology + CRO)

3. **Iterate with Agents**: Use reviewer agents (@brand-voice-guardian, @conversion-optimizer) to refine output

4. **Document Context**: Save campaign briefs, audience profiles, and brand guidelines for consistent results

5. **Test Everything**: Use `/test:ab-setup` for any significant changes

6. **Follow Workflows**: Use built-in workflows for complex multi-step processes

7. **Customize Agents**: Edit agent files to match your brand voice and standards

8. **Version Control**: Track changes to marketing content in Git for rollback capability

## Integration Examples

### With CRM Systems

```python
# Example: Export campaign data
# After using /campaign:plan, export to your CRM

import os
import requests

CRM_API_KEY = os.getenv('CRM_API_KEY')

def create_campaign_in_crm(campaign_data):
    """Push campaign plan to CRM"""
    headers = {'Authorization': f'Bearer {CRM_API_KEY}'}
    response = requests.post(
        'https://your-crm.com/api/campaigns',
        json=campaign_data,
        headers=headers
    )
    return response.json()
```

### With Email Service Providers

```python
# Example: Push email sequence to ESP
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

def create_email_sequence(emails):
    """Upload email sequence to SendGrid"""
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    
    for email in emails:
        message = Mail(
            from_email='marketing@yourcompany.com',
            to_emails=email['segment'],
            subject=email['subject'],
            html_content=email['body']
        )
        response = sg.send(message)
```

### With Analytics Platforms

```python
# Example: Track campaign performance
import os
import requests

ANALYTICS_API_KEY = os.getenv('ANALYTICS_API_KEY')

def track_campaign_metrics(campaign_id, metrics):
    """Send campaign metrics to analytics platform"""
    headers = {'Authorization': f'Bearer {ANALYTICS_API_KEY}'}
    response = requests.post(
        f'https://analytics.com/api/campaigns/{campaign_id}/metrics',
        json=metrics,
        headers=headers
    )
    return response.json()
```

## Resources

- **Documentation**: https://www.agentkits.net/docs
- **Website**: https://www.agentkits.net/marketing
- **Repository**: https://github.com/aitytech/agentkits-marketing
- **Issues**: https://github.com/aitytech/agentkits-marketing/issues
- **Training**: 23 interactive lessons in 11 languages (see `/training` directory)

## License

MIT License - See repository for full details
