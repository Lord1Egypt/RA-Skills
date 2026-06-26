---
name: resume-jd-match
description: >
  AI-powered JD-matched resume generator with native Chinese and English support.
  Collects structured user profile (work history, projects, skills, education),
  parses target job descriptions, performs explicit match analysis before generating,
  then outputs print-optimized HTML resume + auto-export PDF.
  Core strengths: (1) JD→resume full pipeline with transparency, (2) Chinese resume
  native support, (3) persistent profile reuse across multiple JDs.
  Use when: tailoring resume for a job posting, creating resume from scratch,
  optimizing for ATS, building Chinese/English resume, "make me a resume",
  "customize resume for this job", "简历定制", "针对岗位优化简历".
security: >
  PDF export uses local headless browser (Edge/Chrome) via scripts/export-pdf.ps1.
  No network requests, no credential access, no file system writes outside workspace/resumes/.
---

# Resume JD Match — JD 定制简历生成器

Generate polished, JD-matched HTML resume + PDF. Two-phase workflow: collect profile → match JD → generate.

## Phase 1: Profile Collection

On first run (no `resume-profile.md` exists), collect user info. Ask one section at a time, confirm before next. Save to `resume-profile.md`.

**Confirm preferences first:**
1. **Accent color** — hex/name, default `#6b4c9a`
2. **Language** — 中文 or English
3. **Target region** — mainland China (include birth date) or overseas (exclude)

### Sections (structured data per section)
1. Personal — name, phone, email, birth date, location, LinkedIn
2. Education — school, degree, major, date, honors
3. Work Experience — per role: company, title, dates, 3-6 bullets (quantify!)
4. Side Projects — per project: name, type, status, role, features/metrics, tech stack
5. Skills — domain + technical tools + languages, grouped
6. Certificates & Awards

On subsequent runs: load profile, ask "Anything to update?"

## Phase 2: JD Match & Generate

### 2.1 Collect JD
Accept pasted text, file, or URL. Parse and confirm with user before proceeding:
- Job title, company, core requirements (3-5), preferred qualifications

### 2.2 Match Analysis (show user, wait for confirmation)
```
🎯 Target: [Title] @ [Company]
📊 Match: [High/Medium/Low]
✅ Strong matches: ...
⚠️ Gaps: ...
📝 Strategy: Emphasize / Reframe / Downplay
```

### 2.3 Generate HTML Resume

Single self-contained HTML with inline CSS. See [references/html-template-guide.md](references/html-template-guide.md).

**Content rules:**
- 3 core advantages in top highlight grid → mapped to top JD priorities
- Work experience ordered by JD relevance
- Mirror JD keywords naturally, don't stuff
- Every bullet quantified where possible
- Skills section prioritizes JD-required skills (use tag-highlight class)
- 1-2 pages A4 max

### 2.4 Export PDF

```powershell
powershell -File scripts/export-pdf.ps1 -HtmlPath "$htmlPath" -OutputPath "$pdfPath"
```

If export fails: tell user to open HTML in browser → Ctrl+P.

### 2.5 Deliver

Save to `resumes/`: `[Name]-[Title].html` + `[Name]-[Title].pdf`

Pre-send checklist:
- Contact info correct
- Dates accurate
- No typos in company/project names
- Achievements not overstated
- PDF formatting correct

## File Structure
```
workspace/
├── resume-profile.md
├── resumes/
└── skills/resume-tailor/
    ├── SKILL.md
    ├── scripts/export-pdf.ps1
    └── references/html-template-guide.md
```
