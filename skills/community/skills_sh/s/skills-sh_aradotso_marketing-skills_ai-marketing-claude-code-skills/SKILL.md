---
name: ai-marketing-claude-code-skills
description: Install and use marketing framework skills for Claude Code and other AI coding agents
triggers:
  - "install marketing skills for Claude Code"
  - "how do I use AI marketing skills"
  - "add marketing frameworks to my agent"
  - "setup Claude Code skills for marketing"
  - "what marketing skills are available"
  - "help me with Claude Code marketing skills"
  - "configure AI agent marketing expertise"
  - "install positioning skills"
---

# AI Marketing Claude Code Skills

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This project provides pre-packaged marketing expertise as "skills" that AI coding agents (Claude Code, OpenClaw, Cursor, etc.) can load and execute. Instead of prompting from scratch, these skills give your agent structured frameworks for positioning, content strategy, LinkedIn authority, homepage audits, and more.

## What This Project Does

AI Marketing Skills turn marketing frameworks into executable instructions for AI agents. Each skill contains:

- **Triggers**: Natural language phrases that activate the skill
- **Framework**: Step-by-step methodology from marketing experts
- **Output format**: Structured deliverables (audits, strategies, content)
- **Execution modes**: Quick, standard, or deep analysis levels

The project includes 23 free skills and 10 premium skills covering strategy, content, research, conversion, and productivity.

## Installation

### Quick Install (Auto-detect Platform)

```bash
git clone https://github.com/BrianRWagner/ai-marketing-claude-code-skills.git
cd ai-marketing-claude-code-skills
bash scripts/install.sh
```

The installer auto-detects Claude Code, OpenClaw, Cursor, and Windsurf and installs to the correct location.

### Manual Install for Claude Code

```bash
# Clone the repository
git clone https://github.com/BrianRWagner/ai-marketing-claude-code-skills.git

# Create Claude Code skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy all skills
cp -r ai-marketing-claude-code-skills/* ~/.claude/skills/
```

### Install for OpenClaw

```bash
mkdir -p ~/.openclaw/skills
cp -r ai-marketing-claude-code-skills/* ~/.openclaw/skills/
```

OpenClaw uses `SKILL-OC.md` files (token-efficient versions) when available, falling back to `SKILL.md` if not present.

### Install for Cursor

```bash
# From project root
bash scripts/convert.sh --platform=cursor --output-dir=./.cursor/rules
```

This converts `SKILL.md` files to `.mdc` format with proper frontmatter for Cursor.

### Install for Windsurf

```bash
bash scripts/convert.sh --platform=windsurf --output-dir=./.windsurf/rules
```

### Install Flags

```bash
# Install to all detected platforms
bash scripts/install.sh --all

# Install to specific platform only
bash scripts/install.sh --platform=cursor

# Include premium skills (if you've purchased them)
bash scripts/install.sh --include-pro

# Preview without actually installing
bash scripts/install.sh --dry-run
```

## Available Skills Reference

### List All Skills

```bash
cd ai-marketing-claude-code-skills
bash scripts/list-skills.sh
```

Output shows:
- Skill name
- Category
- File location
- Free vs Premium status

### Key Free Skills

**Strategy & Positioning:**
- `positioning-basics` - Core positioning framework (who, what, why different)
- `ai-discoverability-audit` - How your brand appears in AI search (ChatGPT, Perplexity, Claude)
- `marketing-principles` - Apply timeless principles from Drucker, Ogilvy, Godin, etc.

**Content & Authority:**
- `linkedin-authority-builder` - Build LinkedIn thought leadership system
- `content-idea-generator` - Generate content ideas based on ICP and positioning
- `voice-extractor` - Extract and document authentic writing voice from samples
- `de-ai-ify` - Remove AI jargon, restore human voice
- `social-card-gen` - Generate platform-specific social posts (Twitter, LinkedIn, Reddit)

**Research & Intelligence:**
- `last30days` - Research any topic across Reddit, X, web (last 30 days)
- `reddit-insights` - Semantic search and analysis of Reddit content
- `youtube-summarizer` - Fetch transcripts and generate structured summaries
- `linkedin-profile-optimizer` - Audit and rewrite LinkedIn profile for visibility

**Conversion & Sales:**
- `homepage-audit` - Quick conversion audit for landing pages
- `cold-outreach-sequence` - Build personalized LinkedIn/email sequences
- `case-study-builder` - Turn client wins into formatted case studies
- `testimonial-collector` - Systematically gather testimonials

**Productivity:**
- `plan-my-day` - Energy-optimized daily planning (circadian + GTD)
- `newsletter-creation-curation` - Industry-adaptive B2B newsletter creation
- `go-mode` - Deep work execution mode

## Using Skills with Claude Code

Once installed, Claude Code automatically detects and uses skills based on your conversation.

### Trigger Skills Naturally

```
You: "Help me with positioning for my SaaS product"
→ Activates positioning-basics skill

You: "How do I show up in ChatGPT search?"
→ Activates ai-discoverability-audit skill

You: "What should I post on LinkedIn this week?"
→ Activates content-idea-generator skill
```

### Specify Execution Mode

All v3.1+ skills support three execution modes:

```
You: "Quick positioning help for my startup"
→ Quick mode: Fast answers, minimal questions

You: "Standard positioning audit"
→ Standard mode: Balanced depth

You: "Deep positioning analysis for enterprise rebrand"
→ Deep mode: Comprehensive audit, all phases
```

### Direct Skill Invocation

```
You: "Use the homepage-audit skill on https://example.com"

You: "Run linkedin-authority-builder in deep mode"

You: "Apply marketing-principles to this decision: [paste context]"
```

## Skill File Structure

Each skill directory contains:

```
skill-name/
├── SKILL.md          # Full Claude Code version (verbose, all phases)
├── SKILL-OC.md       # OpenClaw version (token-efficient, ~200 lines)
├── README.md         # Human-readable documentation
└── examples/         # Optional usage examples
```

### Anatomy of a SKILL.md File

```markdown
---
name: skill-name
description: One-line description of what the skill does
triggers:
  - "natural phrase 1"
  - "natural phrase 2"
  - "natural phrase 3"
---

# Skill Name

## Context
[When to use this skill]

## Execution Modes
- **Quick**: Fast answers, 2-3 questions
- **Standard**: Balanced depth, 5-7 questions
- **Deep**: Comprehensive, all phases

## Framework
[Step-by-step methodology]

## Output Format
[Structured deliverable format]

## Examples
[Real usage examples]
```

## Configuration

### Environment Variables

Skills that use external APIs require environment variables:

```bash
# For skills that search Reddit
export REDDIT_API_KEY="your_reddit_api_key"

# For skills that use web search
export SERP_API_KEY="your_serp_api_key"

# For YouTube transcript fetching
# No API key needed - uses public endpoints
```

Add to `~/.bashrc`, `~/.zshrc`, or use a `.env` file:

```bash
# .env file in project root
REDDIT_API_KEY=your_reddit_api_key
SERP_API_KEY=your_serp_api_key
```

### Platform-Specific Paths

| Platform | Default Skills Location |
|----------|------------------------|
| Claude Code | `~/.claude/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| Cursor | `.cursor/rules/` (project-level) |
| Windsurf | `.windsurf/rules/` (project-level) |
| Generic | `./ai-marketing-skills/` |

## Common Patterns

### Pattern 1: Strategic Decision Making

```
You: "Should I focus on LinkedIn or Twitter for B2B SaaS?"

Claude (using marketing-principles):
→ Applies first principles from Drucker, Godin
→ Evaluates based on your ICP
→ Provides framework-backed recommendation
```

### Pattern 2: Content Creation Workflow

```
You: "I need to build LinkedIn presence"

Step 1: Use linkedin-authority-builder
→ Get positioning, content pillars, posting rhythm

Step 2: Use content-idea-generator
→ Generate 30 days of content ideas

Step 3: Use voice-extractor (on your existing content)
→ Document your authentic voice

Step 4: Use social-card-gen
→ Generate platform-specific variants
```

### Pattern 3: Research + Execution

```
You: "Research AI agent trends and create a LinkedIn post"

Step 1: Use last30days
→ Research "AI agents" across Reddit, X, web (last 30 days)
→ Get trends, sentiment, key themes

Step 2: Use content-idea-generator
→ Turn insights into post angles

Step 3: Use de-ai-ify
→ Remove AI jargon from final draft
```

### Pattern 4: Audit + Optimize

```
You: "Audit my homepage and LinkedIn profile"

Step 1: Use homepage-audit
→ Get conversion feedback on landing page

Step 2: Use linkedin-profile-optimizer
→ Rewrite headline, about section
→ AI visibility checklist

Step 3: Use ai-discoverability-audit
→ Check how you appear in ChatGPT, Perplexity, Claude
```

## Converting Skills for Other Platforms

### Convert to Cursor Rules

```bash
bash scripts/convert.sh --platform=cursor --output-dir=./.cursor/rules
```

Creates `.mdc` files with frontmatter:

```markdown
---
rule: skill-name
description: Skill description
triggers:
  - trigger phrase 1
  - trigger phrase 2
---

[SKILL.md content converted]
```

### Convert to Windsurf Rules

```bash
bash scripts/convert.sh --platform=windsurf --output-dir=./.windsurf/rules
```

Creates `.md` files with Windsurf-compatible frontmatter.

### Convert All Platforms at Once

```bash
bash scripts/convert.sh --all
```

Outputs to `./converted/cursor/`, `./converted/windsurf/`, etc.

## Adding Custom Skills

### Create a New Skill

```bash
# Create skill directory
mkdir -p ~/.claude/skills/my-custom-skill

# Create SKILL.md
cat > ~/.claude/skills/my-custom-skill/SKILL.md << 'EOF'
---
name: my-custom-skill
description: What this skill does
triggers:
  - "trigger phrase 1"
  - "trigger phrase 2"
  - "trigger phrase 3"
---

# My Custom Skill

## Context
When to use this skill

## Framework
Step-by-step methodology

## Output Format
What the skill delivers

## Examples
Real usage examples
EOF
```

### Skill Development Best Practices

1. **Clear triggers**: Use natural language phrases users would actually say
2. **Execution modes**: Support quick/standard/deep for flexibility
3. **Structured output**: Define clear deliverable format
4. **Real examples**: Include actual usage examples, not placeholders
5. **Self-contained**: Skills should work without external dependencies when possible

## Troubleshooting

### Skills Not Loading

**Claude Code:**
```bash
# Verify installation path
ls -la ~/.claude/skills/

# Check permissions
chmod -R 755 ~/.claude/skills/

# Restart Claude Code
```

**OpenClaw:**
```bash
# Check if SKILL-OC.md exists (preferred) or SKILL.md (fallback)
ls -la ~/.openclaw/skills/*/SKILL*.md

# Verify OpenClaw config
cat ~/.openclaw/config.json
```

### Skill Not Triggering

1. Use exact trigger phrases from the skill's frontmatter
2. Try direct invocation: "Use the [skill-name] skill"
3. Specify mode: "Quick [skill-name]" or "Deep [skill-name]"

### API-Dependent Skills Failing

```bash
# Check environment variables
echo $REDDIT_API_KEY
echo $SERP_API_KEY

# Reload environment
source ~/.bashrc  # or ~/.zshrc

# Test API access
curl -H "Authorization: Bearer $REDDIT_API_KEY" https://oauth.reddit.com/api/v1/me
```

### Conversion Script Issues

```bash
# Make script executable
chmod +x scripts/convert.sh
chmod +x scripts/install.sh
chmod +x scripts/list-skills.sh

# Run with verbose output
bash -x scripts/install.sh

# Check script dependencies
which jq  # Required for some conversions
```

### Platform Detection Fails

```bash
# Manually specify platform
bash scripts/install.sh --platform=cursor

# Check if platform directories exist
ls -la ~/.claude/
ls -la ~/.openclaw/
ls -la ./.cursor/
```

## Premium Skills

Premium skills include structured reasoning phases, self-critique loops, and advanced frameworks.

Available on Gumroad: https://brianrwagner.gumroad.com

| Skill | Price | What It Does |
|-------|-------|-------------|
| AI Marketing Bundle | $49 | All 7 premium skills |
| AI Discoverability Audit v2 | $19 | Deep audit of AI search presence |
| Founder Intelligence | $15 | Competitive founder/company research |
| Competitor Intel Brief | $12 | Structured competitor analysis |
| Morning Brief System | $14 | Personalized daily intelligence brief |
| Brand Voice Extractor | $9 | Extract brand voice from content samples |
| AI Employee Onboarding | $9 | Onboard AI agents to your business |
| Brand Positioning Audit | $9 | Deep positioning framework audit |

After purchase, extract to `pro/` directory and use `--include-pro` flag:

```bash
# Unzip purchased skills
unzip ai-marketing-pro-skills.zip -d ./pro/

# Install with premium skills
bash scripts/install.sh --include-pro
```

## Real-World Examples

### Example 1: Launch Positioning

```
You: "I'm launching a new AI tool for marketers. Help me with positioning."

Claude (using positioning-basics in standard mode):
1. Who is this for? (ICP definition)
2. What do you do? (Core offering)
3. Why are you different? (Unique positioning)
4. What's the category? (Market context)
5. What's the promise? (Value proposition)

→ Delivers: Structured positioning framework document
```

### Example 2: LinkedIn Content System

```
You: "Build me a LinkedIn content system for SaaS founders"

Claude (using linkedin-authority-builder):
→ Positioning audit
→ 3-5 content pillars
→ Content formats (frameworks, stories, hot takes)
→ Posting rhythm (3-5x/week)
→ 30-day content calendar

Then use content-idea-generator:
→ 30 specific post ideas across pillars

Then use voice-extractor (on your existing writing):
→ Voice guide for AI-assisted writing
```

### Example 3: Competitive Research

```
You: "Research what people are saying about Notion vs ClickUp in the last 30 days"

Claude (using last30days):
→ Searches Reddit, X, web
→ Aggregates sentiment and themes
→ Identifies switching triggers
→ Highlights feature gaps

Then use competitor-intel-brief (premium):
→ Structured competitive analysis
→ Feature comparison matrix
→ Positioning gaps
→ Opportunity areas
```

## Contributing

To contribute new skills or improvements:

1. Fork the repository
2. Create a new skill directory following the structure
3. Include both `SKILL.md` (full) and `SKILL-OC.md` (condensed)
4. Add `README.md` for human readers
5. Submit pull request

See existing skills for examples.

## Project Structure

```
ai-marketing-claude-code-skills/
├── scripts/
│   ├── install.sh          # Auto-install to detected platforms
│   ├── convert.sh          # Convert to platform formats
│   └── list-skills.sh      # List all available skills
├── positioning-basics/
│   ├── SKILL.md           # Claude Code version
│   ├── SKILL-OC.md        # OpenClaw version
│   └── README.md          # Documentation
├── ai-discoverability-audit/
│   ├── SKILL.md
│   ├── SKILL-OC.md
│   └── README.md
├── [23 free skills total]
├── pro/                    # Premium skills (not included)
│   ├── founder-intelligence/
│   ├── competitor-intel-brief/
│   └── [10 premium skills]
└── README.md              # This file
```

## License

MIT License - Free skills are open source. Premium skills are licensed per purchase.

## Additional Resources

- **Documentation**: https://www.brianrwagner.com/
- **Twitter**: [@BrianRWagner](https://twitter.com/BrianRWagner)
- **LinkedIn**: [Brian Wagner](https://linkedin.com/in/brianrwagner)
- **Premium Skills**: https://brianrwagner.gumroad.com
- **Agent Skills Standard**: https://agentskills.ai
