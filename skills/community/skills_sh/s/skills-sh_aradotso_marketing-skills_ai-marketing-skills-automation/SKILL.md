---
name: ai-marketing-skills-automation
description: Open-source AI marketing automation skills for growth experiments, sales pipeline, content ops, outbound, SEO, and finance automation
triggers:
  - "run a marketing experiment"
  - "automate sales pipeline from website visitors"
  - "score content quality with expert panel"
  - "generate cold outbound emails"
  - "analyze SEO opportunities"
  - "audit financial costs"
  - "extract insights from sales calls"
  - "optimize conversion rates"
---

# AI Marketing Skills Automation

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This project provides **battle-tested marketing automation workflows** — not prompts, but complete Python scripts with scoring algorithms, expert panels, and automation pipelines. Built for Claude Code and other AI coding agents to execute real marketing operations.

## What It Does

AI Marketing Skills gives you 15+ categories of marketing automation:

- **Growth Engine**: Autonomous experiments with statistical testing
- **Sales Pipeline**: Website visitor → qualified pipeline automation
- **Content Ops**: Quality scoring and production workflows
- **Outbound Engine**: ICP definition to cold emails
- **SEO Ops**: Content gap analysis and keyword research
- **Finance Ops**: AI CFO for cost analysis
- **Revenue Intelligence**: Sales call insights and attribution
- **Conversion Ops**: CRO audits and lead magnet generation
- **Podcast Ops**: Episode → multi-platform content
- **Sales Playbook**: Value-based pricing frameworks
- **Autoresearch**: Evolutionary content optimization
- **Deck Generator**: AI slide deck creation
- **YT Competitive Analysis**: YouTube outlier detection
- **X Long-Form**: Human-sounding X/Twitter posts

## Installation

```bash
# Clone the repository
git clone https://github.com/ericosiu/ai-marketing-skills.git
cd ai-marketing-skills

# Navigate to a specific skill category
cd growth-engine  # or sales-pipeline, content-ops, etc.

# Install dependencies for that category
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

## Configuration

Each category uses a `.env` file for API keys and configuration:

```bash
# Common environment variables across skills
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here

# Growth Engine specific
GOOGLE_ANALYTICS_KEY=your_ga_key
LINKEDIN_API_KEY=your_linkedin_key

# Sales Pipeline specific
RB2B_API_KEY=your_rb2b_key
INSTANTLY_API_KEY=your_instantly_key
APOLLO_API_KEY=your_apollo_key

# SEO Ops specific
GOOGLE_SEARCH_CONSOLE_CREDENTIALS=path/to/credentials.json

# Revenue Intelligence specific
GONG_API_KEY=your_gong_key
SALESFORCE_API_KEY=your_salesforce_key
```

## Growth Engine

Run autonomous marketing experiments with statistical rigor.

### Experiment Engine

```python
from experiment_engine import ExperimentEngine

# Initialize the engine
engine = ExperimentEngine(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    data_source="google_analytics"
)

# Create an experiment
experiment = engine.create_experiment(
    hypothesis="Thread posts get 2x engagement vs single posts",
    variable="format",
    variants=["thread", "single"],
    metric="impressions",
    duration_days=14,
    traffic_split=0.5
)

# Run the experiment
results = engine.run_experiment(experiment.id)

# Get statistical significance
analysis = engine.analyze_results(
    experiment.id,
    confidence_level=0.95,
    test_method="mann_whitney"
)

print(f"Winner: {analysis['winner']}")
print(f"P-value: {analysis['p_value']}")
print(f"Confidence: {analysis['confidence_interval']}")
```

### Pacing Alerts

```python
from pacing_alert import PacingMonitor

monitor = PacingMonitor(
    budget_monthly=10000,
    platform="linkedin"
)

# Check daily pacing
alert = monitor.check_pacing(
    spend_to_date=3500,
    days_elapsed=8,
    days_in_month=30
)

if alert['status'] == 'overpacing':
    print(f"Alert: Overpacing by {alert['variance_percent']}%")
    print(f"Recommended daily spend: ${alert['recommended_daily']}")
```

### CLI Usage

```bash
# Create experiment
python experiment-engine.py create \
  --hypothesis "Carousel posts outperform static images" \
  --variable post_type \
  --variants '["carousel", "static"]' \
  --metric engagement_rate \
  --duration 14

# Check pacing
python pacing-alert.py check \
  --budget 10000 \
  --spend 3500 \
  --days-elapsed 8

# Generate weekly scorecard
python autogrowth-weekly-scorecard.py generate \
  --start-date 2026-05-01 \
  --end-date 2026-05-07
```

## Sales Pipeline

Turn anonymous website visitors into qualified pipeline.

### RB2B Router

```python
from rb2b_instantly_router import RB2BRouter

router = RB2BRouter(
    rb2b_key=os.getenv("RB2B_API_KEY"),
    instantly_key=os.getenv("INSTANTLY_API_KEY")
)

# Fetch website visitors from RB2B
visitors = router.fetch_visitors(
    lookback_hours=24,
    min_intent_score=7
)

# Route to Instantly campaigns
for visitor in visitors:
    # Score and enrich
    enriched = router.enrich_visitor(visitor)
    
    # Route based on criteria
    if enriched['seniority'] in ['C-Level', 'VP', 'Director']:
        router.add_to_campaign(
            email=enriched['email'],
            campaign_id="high-intent-vp",
            personalization={
                'company': enriched['company'],
                'trigger': enriched['page_visited']
            }
        )
```

### Deal Resurrector

```python
from deal_resurrector import DealResurrector

resurrector = DealResurrector(
    crm_api_key=os.getenv("SALESFORCE_API_KEY")
)

# Find stale deals with departed champions
stale_deals = resurrector.find_stale_deals(
    days_inactive=90,
    min_deal_value=10000
)

# Track champions to new companies
for deal in stale_deals:
    champion_moves = resurrector.track_champion(
        champion_email=deal['primary_contact'],
        linkedin_api_key=os.getenv("LINKEDIN_API_KEY")
    )
    
    if champion_moves['new_company']:
        resurrector.create_new_opportunity(
            company=champion_moves['new_company'],
            contact=champion_moves['new_email'],
            context=deal['previous_context']
        )
```

### ICP Learner

```python
from icp_learning_analyzer import ICPLearner

learner = ICPLearner()

# Analyze win/loss patterns
deals = learner.fetch_closed_deals(months_back=12)
patterns = learner.analyze_patterns(deals)

# Update ICP definition
new_icp = learner.update_icp(
    current_icp="""
    Company size: 50-500 employees
    Industry: SaaS, E-commerce
    Tech stack: React, Python
    """,
    win_loss_data=patterns
)

print(new_icp)
```

## Content Ops

Ship content that scores 90+ every time.

### Expert Panel

```python
from expert_panel import ExpertPanel

panel = ExpertPanel(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Load expert personas
panel.load_experts([
    'experts/seo_expert.json',
    'experts/conversion_expert.json',
    'experts/content_strategist.json'
])

# Score content
content = """
Your blog post content here...
"""

scores = panel.score_content(
    content=content,
    rubric='scoring-rubrics/blog_post.json',
    min_score=90
)

# Recursive improvement
while scores['average'] < 90:
    feedback = panel.get_improvement_suggestions(scores)
    content = panel.improve_content(content, feedback)
    scores = panel.score_content(content, 'scoring-rubrics/blog_post.json')

print(f"Final score: {scores['average']}")
print(f"Expert breakdown: {scores['by_expert']}")
```

### Quality Gate

```bash
# CLI quality gate
python quality-gate.py check \
  --file blog-post.md \
  --rubric scoring-rubrics/blog_post.json \
  --min-score 90 \
  --experts seo conversion content-strategy
```

## Outbound Engine

ICP to inbox automation.

### Cold Outbound Optimizer

```python
from cold_outbound_optimizer import OutboundEngine

engine = OutboundEngine(
    apollo_key=os.getenv("APOLLO_API_KEY"),
    instantly_key=os.getenv("INSTANTLY_API_KEY")
)

# Define ICP
icp = {
    'titles': ['VP Marketing', 'CMO', 'Head of Growth'],
    'company_size': [50, 500],
    'industries': ['SaaS', 'E-commerce'],
    'technologies': ['HubSpot', 'Salesforce']
}

# Build lead list
leads = engine.build_lead_list(
    icp=icp,
    limit=1000,
    exclude_domains=['competitor1.com', 'competitor2.com']
)

# Generate personalized emails
for lead in leads:
    email = engine.generate_email(
        lead=lead,
        template='references/cold_email_template.md',
        personalization_depth='high'
    )
    
    engine.add_to_sequence(
        email=lead['email'],
        campaign='q2-outbound',
        message=email
    )
```

## SEO Ops

Find keywords your competitors missed.

### Content Attack Brief

```python
from content_attack_brief import SEOBrief

brief = SEOBrief(
    gsc_credentials=os.getenv("GOOGLE_SEARCH_CONSOLE_CREDENTIALS")
)

# Analyze content gaps
gaps = brief.find_content_gaps(
    target_domain='yoursite.com',
    competitor_domains=['competitor1.com', 'competitor2.com'],
    topic='marketing automation'
)

# Generate brief
content_brief = brief.generate_brief(
    keyword=gaps[0]['keyword'],
    search_intent=gaps[0]['intent'],
    top_ranking_urls=gaps[0]['serp_results']
)

print(content_brief)
```

### GSC Optimizer

```bash
# CLI GSC optimization
python gsc_client.py analyze \
  --domain yoursite.com \
  --lookback-days 90 \
  --min-impressions 1000 \
  --position-range 11-20
```

## Finance Ops

AI CFO for cost analysis.

### CFO Briefing

```python
from cfo_briefing import FinanceAnalyzer

analyzer = FinanceAnalyzer()

# Upload financial data
analyzer.load_data(
    expenses='data/expenses_q1.csv',
    revenue='data/revenue_q1.csv'
)

# Generate CFO briefing
briefing = analyzer.generate_briefing(
    focus_areas=['hidden_costs', 'vendor_optimization', 'budget_variance']
)

# Get cost-saving recommendations
recommendations = analyzer.find_savings_opportunities(
    min_impact=5000  # Minimum $5k annual savings
)

print(briefing)
for rec in recommendations:
    print(f"{rec['category']}: Save ${rec['annual_savings']:,.0f}")
```

## Revenue Intelligence

Sales call insights and attribution.

### Gong Insight Pipeline

```python
from gong_insight_pipeline import GongAnalyzer

analyzer = GongAnalyzer(
    gong_api_key=os.getenv("GONG_API_KEY")
)

# Fetch recent calls
calls = analyzer.fetch_calls(
    date_range='last_7_days',
    min_duration_minutes=20
)

# Extract insights
for call in calls:
    insights = analyzer.extract_insights(call['id'])
    
    # Key patterns
    print(f"Objections: {insights['objections']}")
    print(f"Competitor mentions: {insights['competitors']}")
    print(f"Next steps: {insights['next_steps']}")
    
    # Update CRM
    analyzer.sync_to_crm(
        call_id=call['id'],
        insights=insights,
        crm='salesforce'
    )
```

## Troubleshooting

### API Rate Limits

```python
# All scripts include retry logic with exponential backoff
from utils import retry_with_backoff

@retry_with_backoff(max_retries=5, base_delay=2)
def api_call():
    return client.make_request()
```

### PII Sanitization

```bash
# Scan for sensitive data before commits
python3 security/sanitizer.py --scan --dir . --recursive

# Install pre-commit hook
cp security/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Dependencies Issues

```bash
# Each category has isolated dependencies
cd growth-engine
pip install --upgrade -r requirements.txt

# If conflicts, use virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Data Privacy

All scripts sanitize PII by default:

```python
from security.sanitizer import sanitize_output

# Automatically removes emails, phone numbers, API keys
safe_data = sanitize_output(raw_data)
```

## Common Patterns

### Chain Multiple Skills

```python
# Example: SEO → Content → Quality Gate → Publish
from content_attack_brief import SEOBrief
from expert_panel import ExpertPanel

# 1. Get SEO brief
brief = SEOBrief().generate_brief(keyword='ai marketing automation')

# 2. Generate content
content = generate_from_brief(brief)  # Your content generation

# 3. Score with expert panel
panel = ExpertPanel()
scores = panel.score_content(content, min_score=90)

# 4. Publish if passed
if scores['average'] >= 90:
    publish_to_cms(content)
```

### Telemetry (Opt-In)

```bash
# View local usage stats
python3 telemetry/telemetry_report.py

# Check for updates
python3 telemetry/version_check.py

# Opt out of remote telemetry (local logging still works)
export AI_MARKETING_SKILLS_TELEMETRY=false
```

## Project Structure

```
ai-marketing-skills/
├── growth-engine/          # Experiments, pacing, scorecards
├── sales-pipeline/         # RB2B, deal resurrector, ICP learner
├── content-ops/            # Expert panel, quality gates
├── outbound-engine/        # Cold email automation
├── seo-ops/                # Content gaps, GSC analysis
├── finance-ops/            # CFO briefings, cost analysis
├── revenue-intelligence/   # Gong insights, attribution
├── conversion-ops/         # CRO audits, lead magnets
├── podcast-ops/            # Episode → content pipeline
├── sales-playbook/         # Value pricing frameworks
├── autoresearch/           # Evolutionary content optimization
├── deck-generator/         # AI slide decks
├── yt-competitive-analysis/ # YouTube outlier detection
└── x-longform-post/        # Human-sounding X posts
```

Each category contains:
- `SKILL.md` — Category-specific skill documentation
- `scripts/` — Python automation scripts
- `requirements.txt` — Dependencies
- `.env.example` — Configuration template
- `README.md` — Category guide
