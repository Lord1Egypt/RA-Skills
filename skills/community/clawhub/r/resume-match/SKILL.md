---
name: resume-match
slug: resume-match
description: "Match resume against a job description. Quantified scoring and prioritized improvement tips."
---

# Resume Match

Use this skill when the user wants to compare their resume(s) against a specific job description and get a quantified match score, gap analysis, and tailored rewrite suggestions.

## Good triggers

- "Check if my resume fits this job posting."
- "Score my resume against this JD."
- "What's missing from my resume for this role?"
- "Optimize my resume for this job application."
- "A/B test two versions of my resume against the same JD."

## Workflow

1. **Extract resume structure.** Parse the resume input into:
   - Education (degrees, institutions, graduation year)
   - Work experience (companies, titles, dates, key achievements)
   - Skills (technical and soft, explicitly listed or embedded)
   - Projects or publications (if any)
   - Certifications / languages / awards

2. **Extract JD requirements.** Parse the job description into:
   - **Must-have** — explicit requirements ("5+ years Python", "Bachelor's required")
   - **Nice-to-have** — preferred qualifications ("experience with Kubernetes is a plus")
   - **Soft skills** — inferred or stated ("team player", "strong communication")
   - **Hidden signals** — industry keywords, hard-to-find experience the JD emphasizes

3. **Compute match score (0-100).** Break down by dimension:
   - Technical skills match (weighted by must-have vs nice-to-have)
   - Experience level match
   - Education/certification match
   - Soft skills evidence
   - Overall keyword density in resume vs JD

4. **Gap analysis.** For each JD requirement the resume does not satisfy:
   - Label GAP, PARTIAL, or MATCH
   - Suggest: upskill, rephrase, or add hidden experience
   - Estimate impact on scoring if fixed

5. **2×2 skills matrix.** Plot:
   |                         | JD Requires       | JD Doesn't Require |
   |-------------------------|-------------------|--------------------|
   | Resume Has              | Strength zone     | Overqualified zone |
   | Resume Missing          | Gap zone          | Irrelevant zone    |

6. **Prioritize changes.** P0 → P1 → P2:
   - P0: Must-fix gaps blocking interview (missing JD critical skill)
   - P1: Strengthen weak areas (rephrase to match JD language)
   - P2: Nice-to-have additions (low effort, moderate impact)

7. **Resume rewrite.** For each section, rewrite the resume to match JD language without fabricating facts:
   - Replace generic verbs with JD-aligned action words
   - Reorder bullet points to surface most relevant achievements first
   - Add missing keywords naturally (if true)
   - Adjust summary/objective to mirror JD tone

8. **Keyword density check.** Extract top 20 TF-IDF keywords from JD and count occurrences in original vs optimized resume. Flag density < 30% of JD frequency.

9. **Deliver match report.** Structured output:
   - Overall score and dimension breakdown
   - Gap analysis table
   - 2×2 matrix
   - Prioritized change list
   - Original vs optimized resume (side by side)
   - Keyword density comparison

## Sample prompt

```
resume-match match --resume resume.pdf --jd "https://example.com/job/123"
```
