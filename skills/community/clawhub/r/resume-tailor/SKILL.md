---
name: resume-tailor
description: |
  Customize resumes and generate cover letters based on a specific job description (JD). 
  Use this skill whenever the user wants to tailor their resume to a job posting, adapt their CV for a specific role, 
  highlight relevant skills for a position, write a personalized cover letter, or asks anything related to job applications, 
  job hunting materials, or making their resume more competitive for a specific company or role.
  Triggers: "tailor my resume", "customize CV", "write a cover letter", "optimize resume for JD", 
  "make my resume match this job", "apply for job", "job application materials", "rewrite resume for role".
version: 1.0.0
metadata:
  openclaw:
    emoji: "📄"
---

# Resume Tailor

Transform a generic resume into a targeted, compelling job application package — tailored resume + cover letter — matched to a specific job description.

## When This Skill Activates

Use this skill when the user provides:
- A resume (text, file, or paste) + a job description/posting
- A request to write a cover letter for a specific role
- A request to optimize/tailor their resume for a job

If the user hasn't provided both resume and JD yet, ask for them before proceeding.

---

## Workflow

### Step 1: Gather Inputs

Collect (or request) the following:
1. **Resume** – full text or uploaded file (.docx, .pdf, .txt)
2. **Job Description** – full JD text, URL, or paste
3. **Target Role/Company** – confirm if not obvious from JD
4. **Optional extras** – user's preferred tone (formal/casual), language (EN/ZH), or specific aspects to emphasize

If any of these are missing, ask the user before continuing.

---

### Step 2: Analyze the JD

Parse the JD for:
- **Required skills** – hard skills, tools, technologies, certifications
- **Preferred skills** – nice-to-haves the user can highlight if they have them
- **Key responsibilities** – what the role actually does day-to-day
- **Culture signals** – tone of JD, company values, keywords that suggest what they value
- **Red flags to address** – experience gaps, unusual requirements

Create a mental "keyword map" from these. You will use this to rewrite the resume.

---

### Step 3: Tailor the Resume

Rewrite/restructure the resume with these rules:

#### Core Principles
- **Mirror the JD's language**: use the exact keywords and phrasing from the JD where the user has relevant experience. ATS systems match keywords literally.
- **Lead with relevance**: reorder bullet points so the most relevant accomplishments appear first.
- **Quantify everything possible**: transform vague bullets into impact statements with metrics.
- **Cut irrelevant content**: if something doesn't support this specific application, trim it or remove it.
- **Never fabricate**: only use skills/experience the user actually has. If a required skill is missing, note it but don't invent it.

#### Section-by-section guidance

**Summary/Objective**
- Rewrite to mention the target role, company (if desired), and top 2-3 qualifications that match the JD.
- Keep it to 2-4 sentences.

**Work Experience**
- For each role, keep only bullets relevant to the JD.
- Start bullets with strong action verbs that echo JD language.
- Add quantified outcomes wherever possible (%, $, time saved, team size, etc.)
- If the user has experience that's tangential but transferable, frame it using the JD's vocabulary.

**Skills Section**
- Reorder to put JD-matched skills first.
- Add any skills from the JD that the user has but didn't list.
- Remove skills that are completely irrelevant.

**Education / Certifications**
- Highlight relevant coursework, projects, or certifications that match JD requirements.

---

### Step 4: Write the Cover Letter

Structure:

```
[Opening paragraph]
Hook: mention the role + one strong reason you're excited / a specific thing about the company.
Tie your background to their mission/product briefly.

[Body paragraph 1: "Why me"]
Highlight 2-3 specific accomplishments that directly address their top requirements.
Use metrics. Reference the JD explicitly ("Your posting mentions X — here's my experience with X").

[Body paragraph 2: "Why them" (optional but powerful)]
Show you've done research. Reference a product, initiative, recent news, or company value.
Explain why this role at this company, not just any company.

[Closing paragraph]
Express enthusiasm. State your next step (happy to discuss, available for an interview).
Thank them for their time.
```

**Tone guidelines**:
- Default: professional but personable, not robotic
- Tech startups: more casual, show personality
- Finance/law/enterprise: more formal
- Follow user preferences if specified

**Length**: 3-4 paragraphs, max 400 words. Hiring managers skim.

---

### Step 5: Output Format

Present results clearly in this order:

1. **Gap Analysis** (brief) — list JD requirements the user's resume currently doesn't address well, and how you handled each
2. **Tailored Resume** — full rewritten resume in clean markdown or the user's preferred format
3. **Cover Letter** — complete, ready-to-send letter
4. **Quick tips** (optional) — 2-3 specific things the user should be prepared to discuss in an interview based on the JD

---

## Output Quality Checklist

Before presenting output, verify:
- [ ] JD keywords appear naturally throughout resume (not keyword-stuffed)
- [ ] Each resume bullet starts with an action verb
- [ ] At least 60% of experience bullets have quantifiable outcomes
- [ ] Cover letter mentions company by name and a specific role/detail
- [ ] No fabricated skills or experiences
- [ ] Cover letter is under 400 words
- [ ] Tone is consistent throughout

---

## Edge Cases

**User has significant skill gaps**: Be honest. Note which requirements they don't meet, suggest how to frame adjacent skills, and recommend whether to apply or upskill first.

**JD is vague**: Ask the user for more context about the company/team. If not available, make reasonable inferences and note your assumptions.

**Multiple JDs**: If the user wants to apply to many roles, create a "master resume" with all bullets, then a targeted subset for each role. Document which sections to activate per role type.

**No resume provided, starting from scratch**: Ask the user for their work history, skills, and education. Build a resume from scratch following modern standards, then tailor it.

**Non-English job applications**: Adapt language, phrasing norms, and CV format to the target country's conventions. See `references/regional-cv-formats.md` for country-specific guidance.

---

## Reference Files

- `references/ats-keywords.md` — Tips on ATS optimization and keyword matching
- `references/regional-cv-formats.md` — Country/region-specific resume conventions (EU, Asia, UK, etc.)
- `references/cover-letter-examples.md` — Example cover letters for different industries
