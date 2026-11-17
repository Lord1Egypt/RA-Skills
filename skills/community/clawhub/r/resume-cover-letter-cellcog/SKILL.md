---
name: resume-cover-letter-cellcog
description: "AI resume and cover letter generation powered by CellCog. ATS-optimized resumes, CVs, cover letters, LinkedIn profiles, career documents — PDF or DOCX. Research-first approach that analyzes target roles before writing."
metadata:
  openclaw:
    emoji: "📝"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Resume & Cover Letter - AI Resume Builder Powered by CellCog

**7 seconds.** That's how long the average recruiter spends on your resume. CellCog makes every second count.

#1 on DeepResearch Bench (October 2026) — CellCog researches your target role, understands what hiring managers look for, optimizes for ATS systems, and generates beautifully designed resumes — PDF for polished presentation or DOCX when ATS systems require Word format. Not another template filler — a research-first resume engine.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
print(result["message"])
```


---

## What You Can Create

### Resumes & CVs

Build resumes that pass ATS filters and impress humans:

- **Modern Resumes**: "Create a modern, ATS-friendly resume for a senior product manager"
- **Career Change Resumes**: "Build a resume that positions my finance background for a tech PM role"
- **Academic CVs**: "Create a detailed academic CV for a postdoc in computational biology"
- **Executive Resumes**: "Design an executive resume for a VP of Engineering with 15 years experience"
- **Entry-Level Resumes**: "Build a compelling resume for a recent CS graduate with internship experience"

**Example prompt:**
> "Create an ATS-optimized resume for:
> 
> Name: Sarah Chen
> Target Role: Senior Product Manager at a B2B SaaS company
> 
> Experience:
> - Stripe (2021-present): Led payments platform, grew merchant revenue 40%
> - Slack (2018-2021): Launched 3 enterprise features, drove $12M ARR
> - Microsoft (2016-2018): Associate PM on Azure DevOps
> 
> Education: Stanford MBA, UC Berkeley CS
> Skills: Product strategy, data analysis, cross-functional leadership, SQL, A/B testing
> 
> Clean, modern design with blue accents. Highlight metrics and impact."

### Cover Letters

Compelling cover letters that complement your resume:

- **Role-Specific**: "Write a cover letter for the Senior PM position at Notion"
- **Career Change**: "Write a cover letter explaining my transition from consulting to product"
- **Internal Transfer**: "Draft an internal transfer letter for moving from engineering to product"

**Example prompt:**
> "Write a compelling cover letter for:
> 
> Applicant: Sarah Chen (use the resume we just created)
> Target: Senior Product Manager at Notion
> 
> Key angles:
> - My experience building collaboration tools at Slack is directly relevant
> - I'm passionate about Notion's mission of making tools that feel like your own
> - Highlight the payments platform growth at Stripe as evidence of scaling ability
> 
> Tone: Professional but authentic, not corporate-speak."

### LinkedIn Optimization

Optimize your professional presence:

- **Profile Rewrite**: "Rewrite my LinkedIn headline and summary to attract recruiters for ML engineering roles"
- **About Section**: "Create a compelling LinkedIn About section based on my resume"
- **Experience Bullets**: "Transform my resume bullets into LinkedIn-style achievement descriptions"

### Portfolio Documents

Showcase your work:

- **Case Studies**: "Create a product management case study document from my Stripe experience"
- **Design Portfolios**: "Build a portfolio PDF showcasing my top 5 UX projects"
- **Writing Samples**: "Format my blog posts into a professional writing portfolio"

---

## Why CellCog for Resumes?

| Generic Resume Builders | CellCog Resume Cog |
|------------------------|-------------------|
| Pick a template, fill in blanks | Researches your target role first |
| Same advice for everyone | Tailored to specific companies and industries |
| Basic ATS keyword stuffing | Deep understanding of what ATS systems scan for |
| Template designs | State-of-the-art PDF generation, custom every time |
| Text only | Can include charts, visual elements, custom layouts |

---

## Choosing Mode & Tier

| Scenario | Recommended |
|----------|-------------|
| Resumes and cover letters | `chat_mode="agent"` (defaults to the `"core"` tier) |
| Career strategy with multiple role-specific variants | `chat_mode="agent", chat_tier="max"` |

**The core tier is the default and handles most resume work well**, balanced speed and depth. **Upgrade to `chat_tier="max"`** when quality disappoints or the work is genuinely complex: just re-run the same prompt with `chat_tier="max"`.

Agent Team (`chat_mode="team"`) is reserved for deep research — don't use it for resume work.

---

## Tips for Better Resumes

1. **Provide real details**: Don't say "I worked on projects" — give specific metrics, tools, and outcomes. CellCog can't invent your achievements.

2. **Name the target role**: "Resume for a PM" is vague. "Resume targeting Senior PM roles at B2B SaaS companies in fintech" gives CellCog direction.

3. **Include metrics**: Revenue numbers, user counts, percentage improvements — quantifiable results make resumes stand out.

4. **Specify design preferences**: "Modern and minimal", "traditional corporate", "creative with color" — or let CellCog choose based on your industry.

5. **Choose your format**: PDF is the default for polished, presentation-ready resumes. Request DOCX when you need to edit or when ATS systems require Word format.

---

## If CellCog is not installed

**Claude Code, Cursor, Codex + 70 more agents:** `npx skills add cellcog/skills --skill cellcog`
**OpenClaw:** `openclaw skills install @cellcog/cellcog`
**CellCog plugin users:** run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool)
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
