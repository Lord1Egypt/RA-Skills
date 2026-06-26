---
name: marketing-orchestrator-skill
description: AI-powered marketing orchestrator with six specialist routes, client memory, and self-improving revision loop for freelance marketers
triggers:
  - "set up marketing orchestrator for Claude"
  - "route marketing tasks to specialists"
  - "create client profiles for marketing"
  - "run marketing campaign workflow"
  - "deploy marketing skill to GitHub"
  - "improve marketing skill with revision log"
  - "repurpose content across platforms"
  - "generate ad copy with character limits"
---

# Marketing Orchestrator Skill

> Skill by [ara.so](https://ara.so) — Marketing Skills collection

## What This Project Does

The Marketing Orchestrator is a Claude skill that routes marketing requests to six specialist sub-skills: Brand Strategy & ICP, Ad Copy & Paid Media, Content Creation, Repurpose, Campaign Mode, and GitHub Deploy. It includes:

- **Automatic routing** based on user intent
- **Client memory** that persists across sessions
- **Self-evaluation** of outputs before delivery
- **Revision loop** that improves the skill over time from logged usage patterns

## Installation

This is a Claude AI skill designed for [Claude.ai](https://claude.ai) with Skills feature enabled.

1. Clone the repository:
```bash
git clone https://github.com/bryanengel72/marketing-orchestrator.git
cd marketing-orchestrator
```

2. Install via Claude Skills interface by uploading the project folder

3. Verify installation by checking for these files:
```
marketing-orchestrator/
├── SKILL.md                          # Main orchestrator
├── references/
│   ├── revision-log.md               # Session tracking
│   └── client-profiles/              # Client data
└── sub-skills/                       # Six specialist routes
    ├── brand-strategy-icp/SKILL.md
    ├── ad-copy-paid-media/SKILL.md
    ├── content-creation/SKILL.md
    ├── repurpose/SKILL.md
    ├── campaign-mode/SKILL.md
    └── github-deploy/SKILL.md
```

## Project Structure

### Core Components

**SKILL.md** (Main Orchestrator)
- Handles intake and routing
- Manages client profile lookup/creation
- Performs self-evaluation before delivery
- Tracks revision loop (every 3rd session)

**Sub-Skills** (Six Specialists)
Each sub-skill has its own `SKILL.md` with specialist instructions:
- `brand-strategy-icp/` — ICP profiles, positioning, brand voice
- `ad-copy-paid-media/` — Platform ads with character limits
- `content-creation/` — Blogs, social posts, email sequences
- `repurpose/` — Multi-platform content adaptation
- `campaign-mode/` — Full campaign architecture
- `github-deploy/` — Git setup for non-developers

**References**
- `references/revision-log.md` — Session log for improvement tracking
- `references/client-profiles/` — Persistent client context

## How to Use

### Starting a Session

The orchestrator automatically handles routing. User says:

```
"I need Google Ads copy for a new SaaS product"
```

Orchestrator:
1. Checks for existing client profile in `references/client-profiles/{client-name}.md`
2. If new, asks intake questions (company name, industry, target audience, etc.)
3. Routes to `ad-copy-paid-media` sub-skill
4. Sub-skill generates output
5. Self-evaluates against rubric (audience fit, clarity, voice, format, goal alignment)
6. Logs session to `references/revision-log.md`
7. Delivers final output with quality check signal

### Client Profile Format

Client profiles are saved as:
```
references/client-profiles/acme-corp.md
```

Example profile structure:
```markdown
# Acme Corp

**Industry:** B2B SaaS
**Target Audience:** Mid-market operations managers
**Brand Voice:** Professional, data-driven, empathetic
**Key Pain Points:** Manual workflows, data silos
**Unique Value Prop:** All-in-one automation without IT dependency

## Past Projects
- 2026-04-15: Google Ads campaign (5 ad variants)
- 2026-05-02: Blog post series (productivity tips)

## Notes
- Avoid technical jargon
- Emphasize ROI and time savings
```

### Revision Loop

Every third session, the orchestrator prompts:
```
"📊 Revision reminder: It's been 3 sessions. Would you like me to analyze 
the revision log and suggest an improvement?"
```

If user accepts:
1. Reads `references/revision-log.md`
2. Identifies most frequent pattern (e.g., "intake questions too long")
3. Proposes specific fix
4. Updates relevant sub-skill after approval
5. Logs change with version bump

### Revision Log Format

```markdown
# Revision Log

## Version 1.2.0 (2026-05-17)
- Reduced brand-strategy intake from 8 to 5 questions
- Added auto-skip for returning clients with profiles
- Source: Sessions #12, #14, #16 flagged intake length

## Session #16 (2026-05-17)
**Route:** brand-strategy-icp
**Client:** New (TechFlow Inc)
**Quality Check:** ✅ Passed all rubric categories
**Flag:** Intake took 4 back-and-forth exchanges

## Session #15 (2026-05-14)
**Route:** ad-copy-paid-media
**Client:** Returning (Acme Corp)
**Quality Check:** ✅ Passed all rubric categories
**Note:** Profile auto-loaded, no redundant questions
```

## Key Workflows

### 1. Brand Strategy with Document Export

User request:
```
"Create an ICP profile and positioning doc for my coaching business"
```

Sub-skill output includes:
- Structured ICP with demographics, psychographics, pain points
- Positioning framework (category, audience, problem, solution, differentiation)
- Brand voice guide with tone attributes and examples
- **Downloadable Word doc** with formatted sections

The sub-skill automatically structures content for `.docx` export via Claude's artifact system.

### 2. Ad Copy with Platform Constraints

User request:
```
"Write Meta Ads for a webinar registration campaign"
```

Output includes:
```markdown
## Ad Variant A
**Primary Text (125 chars):** Join 500+ marketers mastering AI workflows. 
Free webinar May 30. Save your seat →

**Headline (40 chars):** Master AI Marketing in 60 Minutes

**Description (30 chars):** Live Q&A included. No replay.

---

**Character Counts:**
- Primary: 125/125 ✅
- Headline: 32/40 ✅
- Description: 29/30 ✅
```

Platform limits are enforced during generation.

### 3. Multi-Platform Repurposing

User provides source content (e.g., blog post) and target platforms:
```
"Repurpose this blog post for LinkedIn, Twitter, and Instagram"
```

Sub-skill generates:
- **LinkedIn:** Professional narrative (1200-1500 chars), hashtags, engagement hook
- **Twitter:** Thread format (280 chars/tweet), optimized for retweets
- **Instagram:** Visual-first caption, story-friendly formatting

Each is **rewritten natively** for platform, not truncated.

### 4. Full Campaign Mode

User request:
```
"Plan a product launch campaign for a new app feature"
```

Campaign Mode sub-skill:
1. Defines campaign architecture (awareness → consideration → conversion)
2. Lists all deliverables in funnel sequence
3. Creates each asset with connecting narrative thread
4. Generates launch checklist with dates and owners

Example output structure:
```markdown
# Campaign Architecture

**Goal:** 500 beta signups in 2 weeks
**Funnel:** Teaser posts → Feature explainer → Signup CTA

## Deliverables (in sequence)
1. Teaser email (1 week before)
2. LinkedIn announcement post (launch day)
3. Demo video script (launch day)
4. Retargeting ad copy (days 3-7)
5. Follow-up email (1 week after)

[Full copy for each deliverable follows]

## Launch Checklist
- [ ] Load email into ESP (Day -1)
- [ ] Schedule LinkedIn post (Day 0, 9am)
- [ ] Activate retargeting ads (Day 3)
```

### 5. GitHub Deploy for Non-Developers

User request:
```
"Help me set up GitHub for my marketing files"
```

Sub-skill provides:
```bash
# Step 1: Create GitHub account at github.com

# Step 2: Install Git
# macOS:
brew install git

# Windows:
# Download from git-scm.com

# Step 3: Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Step 4: Create repository on GitHub (via web UI)
# Repository name: marketing-files
# Visibility: Private

# Step 5: Initialize local folder
cd ~/Documents/marketing-files
git init
git remote add origin https://github.com/YOUR_USERNAME/marketing-files.git

# Step 6: First commit
git add .
git commit -m "Initial commit"
git push -u origin main

# Daily workflow:
git add .
git commit -m "Updated campaign docs"
git push
```

Includes troubleshooting for common errors (authentication, branch naming, merge conflicts).

## Self-Evaluation Rubric

Before delivering output, the orchestrator evaluates against:

1. **Audience Fit:** Does this match the client's target audience profile?
2. **Clarity:** Is the language clear and jargon-appropriate?
3. **Voice Consistency:** Does it match the client's brand voice?
4. **Platform Format:** Does it meet platform-specific requirements (char limits, structure)?
5. **Goal Alignment:** Does it directly support the stated objective?

Outputs are silently revised if any category fails. Final delivery includes:
```
✅ Quality check: Passed all rubric categories
```

## Configuration

### Custom Sub-Skill

To add a new specialist route:

1. Create folder: `sub-skills/new-specialist/`
2. Add `SKILL.md` with specialist instructions:
```markdown
# New Specialist Sub-Skill

## Scope
Handles [specific marketing task category]

## Intake Questions
- Question 1
- Question 2

## Output Format
[Structured template]

## Self-Evaluation Focus
[Task-specific quality criteria]
```

3. Update main `SKILL.md` routing logic to include new route trigger phrases

### Environment Variables

For API integrations (not included in base skill):
```bash
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
```

## Troubleshooting

### Client Profile Not Loading

**Symptom:** Orchestrator asks intake questions for returning client

**Fix:**
1. Check filename matches client name (kebab-case): `acme-corp.md`
2. Verify file location: `references/client-profiles/acme-corp.md`
3. Confirm markdown syntax is valid

### Revision Log Not Tracking

**Symptom:** No entries appear in `references/revision-log.md`

**Fix:**
1. Ensure file exists at `references/revision-log.md`
2. Check file permissions (must be writable)
3. Verify orchestrator is logging at end of each session

### Sub-Skill Not Routing

**Symptom:** Wrong specialist handles request

**Fix:**
1. Check user request includes clear trigger words (e.g., "ad copy", "campaign", "repurpose")
2. Review routing logic in main `SKILL.md`
3. If ambiguous, orchestrator should ask clarifying question before routing

## Common Patterns

### Pattern: Resume Previous Session

User returns with:
```
"Continue working on the Acme Corp campaign from last week"
```

Orchestrator:
1. Loads `references/client-profiles/acme-corp.md`
2. Reads "Past Projects" section for context
3. Confirms campaign details with user
4. Routes to appropriate sub-skill

### Pattern: Batch Content Request

User:
```
"Create 5 LinkedIn posts about remote work productivity"
```

Orchestrator routes to `content-creation`, which:
1. Generates all 5 posts in single session
2. Ensures variety in hooks and formats
3. Numbers each post for easy reference
4. Offers to add to content calendar

### Pattern: Quick Edit

User:
```
"Make that last ad copy more concise"
```

Orchestrator:
1. Retrieves previous output from session context
2. Applies edit instruction
3. Re-runs self-evaluation
4. Delivers revised version with quality check

## Advanced Usage

### Chaining Multiple Routes

User:
```
"Create a brand voice guide, then write 3 ads using that voice"
```

Orchestrator:
1. Routes to `brand-strategy-icp` first
2. Saves output to client profile under "Brand Voice" section
3. Routes to `ad-copy-paid-media` with voice guide context
4. Generates ads conforming to established voice

### Export Formats

For document-heavy routes (Brand Strategy, Campaign Mode):
- Orchestrator structures output for Claude's artifact system
- User can download as `.docx`, `.md`, or `.pdf`
- Formatting includes headers, bullet lists, tables

## Testing the Skill

### Test 1: New Client Intake
```
User: "I need a blog post about AI in healthcare"
Expected: Intake questions → content-creation route → quality check
```

### Test 2: Returning Client
```
User: "Create another ad set for Acme Corp"
Expected: Auto-load profile → ad-copy route → no redundant questions
```

### Test 3: Revision Loop
```
After 3rd session, expected: "📊 Revision reminder..." prompt
User: "Yes, analyze the log"
Expected: Pattern analysis → proposed fix → update confirmation
```

## License

MIT License — Free to use, adapt, and extend.
