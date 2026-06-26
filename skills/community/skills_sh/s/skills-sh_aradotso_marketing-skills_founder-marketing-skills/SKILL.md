---
name: founder-marketing-skills
description: Open-source marketing skills for founders using Claude agents - keyword research, growth strategy, social search audit, and competitor analysis
triggers:
  - install marketing skills for my startup
  - run social search audit
  - generate growth strategy for my business
  - research keywords for TikTok and Instagram
  - audit my competitors' marketing
  - help me with founder marketing
  - set up ScaleBrick marketing skills
  - analyze if social search works for my niche
---

# Founder Marketing Skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

Open-source marketing skills for founders who do their own marketing. Provides 4 AI-powered skills for keyword research, growth strategy, social search audit, and competitor intelligence. Works with Claude Code, Codex, Cursor, and any agent that reads `SKILL.md` files.

## What This Project Does

ScaleBrick's Founder Marketing Skills is a collection of structured marketing methodologies packaged as `SKILL.md` files that AI agents can execute. Each skill follows a specific framework to analyze your business and produce actionable marketing insights:

- **Social Search Audit**: Evaluates if TikTok/Instagram search is viable for your business
- **Growth Strategy**: Generates comprehensive marketing strategy with keywords and content pillars
- **Keyword Research**: Finds high-intent keywords people search on social platforms
- **Competitor Audit**: Analyzes competitors' SEO, content, and social media presence

Core insight: 40% of Gen Z uses TikTok and Instagram as search engines. These skills help you capture that high-intent traffic.

## Installation

Install all 4 skills into your agent's skills directory:

```bash
npx skills add ScaleBrick/founder-marketing-skills
```

This installs the skills into your agent's skills directory (typically `~/.skills/` or your agent's configured path). No API keys or account required.

### Manual Installation

If you prefer manual installation:

```bash
# Clone the repository
git clone https://github.com/ScaleBrick/founder-marketing-skills.git

# Copy skills to your agent's skills directory
cp founder-marketing-skills/*.md ~/.skills/
```

## Key Commands

Each skill is invoked with a specific command:

| Command | Skill | Purpose |
|---------|-------|---------|
| `/audit` | Social Search Audit | Evaluate social search viability for your niche |
| `/strategy` | Growth Strategy | Generate full marketing strategy |
| `/keywords` | Keyword Research | Find high-intent keywords |
| `/competitors` | Competitor Audit | Audit competitors' marketing |

## Usage Patterns

### Running a Social Search Audit

```
/audit

Business: Cal AI
Description: AI-powered calorie tracking app
Website: https://cal.ai
Target Audience: Health-conscious Gen Z users who want effortless calorie tracking
```

**Expected output:**
- Niche competition analysis
- Search demand evaluation
- Content type fit assessment
- 10 starter keywords with intent categories
- Conversion potential ratings
- Direct TikTok/Instagram search URLs for verification

### Generating a Growth Strategy

```
/strategy

Business: AIFlyer
Description: AI-powered flyer design tool
Target Audience: Small business owners, event organizers, and marketers who need quick professional designs
Website: https://aiflyer.com
```

**Expected output:**
- Core marketing themes (3-5)
- Content pillars mapped to business value
- Brand voice guidelines
- 20+ categorized keywords with intent types
- Posting plan and frequency recommendations
- Channel-specific tactics

### Keyword Research

```
/keywords

Business: AI healthcare app for diabetes management
Niche: Healthcare tech, diabetes monitoring
Target Audience: Type 2 diabetics aged 30-55 seeking easier tracking
```

**Expected output:**
- Educational keywords (how-to, explainer content)
- Problem-aware keywords (pain point searches)
- Tool comparison keywords (competitor alternatives)
- Intent ratings (high/medium/low conversion potential)
- Search volume indicators
- Content format recommendations

### Competitor Audit

```
/competitors

Business: Project management tool for remote teams
Competitors: Asana, Monday.com, ClickUp, Notion, Trello
Website: https://yourapp.com
```

**Expected output:**
- SEO analysis (keyword gaps, ranking opportunities)
- Content strategy breakdown
- Social media presence audit
- Positioning gaps no one is claiming
- 5 specific actionable moves for this week
- Quick wins vs. long-term plays

## Information Required

For best results, provide:

**Minimum:**
- Business name
- Brief description (1-2 sentences)
- Target audience

**Recommended:**
- Website URL
- Specific competitors (for competitor audit)
- Current marketing efforts (if any)
- Known pain points or challenges

**Example complete request:**

```
/audit

Business: Calmly
Description: AI-powered meditation app that personalizes sessions based on stress levels and biometric data
Website: https://calmly.app
Target Audience: Busy professionals aged 28-45 experiencing burnout who want science-backed stress relief
Current situation: Just launched, 500 beta users, no marketing team
Competitors: Headspace, Calm, Insight Timer
```

## Understanding the Output

### Intent Categories

Skills categorize keywords by search intent:

- **Educational**: "how to track calories", "what is macro counting" (Top of funnel)
- **Problem-aware**: "can't lose weight tracking calories", "calorie tracking not working" (Middle funnel)
- **Tool comparison**: "MyFitnessPal vs Lose It", "best calorie tracker app" (Bottom funnel)
- **Direct**: "Cal AI review", "Cal AI app download" (Bottom funnel)

### Conversion Potential Ratings

- **High**: Strong purchase/signup intent, ready to convert
- **Medium**: Interested but researching, needs nurturing
- **Low**: Early awareness stage, educational content

### Content Type Recommendations

Based on niche analysis:
- **Problem-first**: Lead with pain points (converts 54% better in health/productivity niches)
- **Educational**: How-to content (works for technical/learning niches)
- **Aspirational**: Lifestyle/transformation content (fitness, personal finance)

## Integration with Your Workflow

### With Claude Code

Skills are automatically available after installation:

```
User: Help me audit if social search works for my SaaS tool
Claude: I'll run the Social Search Audit skill for you. Please provide...
```

### With Cursor

Skills appear in the skills menu or can be invoked via chat:

```
@skills run social-search-audit for [business description]
```

### With Codex/Custom Agents

Skills are read from the skills directory. Agents parse the SKILL.md format:

```yaml
---
name: social-search-audit
triggers:
  - audit my social search potential
  - check if TikTok search works for me
---
```

## Real Results Framework

The skills are based on proven results:

```
YC-backed AI healthcare app:
  - 353K views in 47 days
  - 5,300 page visits
  - $0 ad spend

AIFlyer:
  - 0 to 15,000 signups in 3 months
  - Ranks alongside Canva in TikTok LLM responses
  - All organic traffic
```

**The method:**
1. Find demand (what people actually search)
2. Categorize intent (educational vs. problem-aware vs. comparison)
3. Match content type (different formats convert differently)
4. Focus ruthlessly (80/20 rule - kill what doesn't work)
5. Close the loop (track signups, not just views)

## Common Patterns

### Pattern 1: Full Funnel Setup

```
1. Run /audit to validate the channel
2. Run /strategy to get core themes and keywords
3. Run /competitors to find gaps
4. Run /keywords for specific content ideas
```

### Pattern 2: Quick Validation

```
Run /audit with your business idea to see if social search is viable before building
```

### Pattern 3: Competitive Intelligence

```
Run /competitors quarterly to track positioning shifts and new opportunities
```

### Pattern 4: Content Planning

```
/keywords → filter by high conversion potential → map to content calendar
```

## Troubleshooting

### Skills Not Found

**Issue**: Agent can't find the skills after installation

**Solution**:
```bash
# Check skills directory location
echo $SKILLS_DIR

# Verify installation
ls ~/.skills/

# Reinstall if needed
npx skills add ScaleBrick/founder-marketing-skills --force
```

### Generic Output

**Issue**: Skills produce generic advice instead of specific insights

**Solution**: Provide more context:
- Add website URL for the agent to analyze
- List specific competitors
- Describe your unique value proposition
- Mention current metrics or situation

### No Search URLs

**Issue**: Audit doesn't include verification URLs

**Solution**: The agent may need explicit instruction:
```
Run the social search audit and include direct TikTok search URLs for each keyword
```

### Skills Not Triggering

**Issue**: Natural language doesn't trigger skills

**Solution**: Use explicit commands:
- `/audit` instead of "help me audit"
- `/strategy` instead of "I need a strategy"

## Advanced Usage

### Combining Skills

Chain skills for comprehensive analysis:

```
1. /audit [validates channel]
2. If viable → /strategy [gets full plan]
3. /competitors [finds gaps]
4. /keywords [gets specific content ideas]
```

### Iterative Refinement

```
First pass:
/keywords for "AI productivity tools"

Refine:
/keywords for "AI productivity tools for remote teams" with focus on Slack/Notion integration pain points
```

### Niche Drilling

```
Broad: /audit for "fitness app"
Specific: /audit for "kettlebell workout app for women over 40"

The specific version produces 10x more actionable insights.
```

## Project Structure

```
founder-marketing-skills/
├── social-search-audit.md    # /audit skill
├── growth-strategy.md         # /strategy skill
├── keyword-research.md        # /keywords skill
├── competitor-audit.md        # /competitors skill
├── README.md                  # Documentation
└── docs/
    └── images/                # Example outputs
```

Each skill is a standalone `SKILL.md` file with:
- YAML frontmatter (name, description, triggers)
- Structured methodology
- Analysis framework
- Output format specifications

## Configuration

No configuration files needed. Skills work out of the box.

Optional environment variables for enhanced functionality:

```bash
# If you want to customize skills directory
export SKILLS_DIR=~/my-custom-skills

# For agents that support skill namespacing
export SKILL_NAMESPACE=marketing
```

## Contributing New Skills

Skills are just structured markdown files. To add a new skill:

1. Create `your-skill-name.md` with YAML frontmatter:

```yaml
---
name: your-skill-name
description: One-line description
triggers:
  - trigger phrase 1
  - trigger phrase 2
---
```

2. Add methodology in markdown
3. Include output format specification
4. Test with Claude Code or your agent
5. Submit PR to the repository

## License

MIT License - free forever, modify as needed.

## Resources

- Repository: https://github.com/ScaleBrick/founder-marketing-skills
- Homepage: https://scalebrick.com
- Issues: https://github.com/ScaleBrick/founder-marketing-skills/issues

## Full-Service Alternative

For execution beyond strategy, ScaleBrick offers Morgan - an AI VP of Marketing that runs the complete growth loop: keyword research, content production, publishing, attribution tracking, and weekly optimization.

Not required to use these skills - they work standalone.
