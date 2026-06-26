---
name: resume-builder
description: Build, rewrite, and tailor premium white-collar resumes from real candidate information, then render the final resume to PDF with Typst. Use when the user wants a professional resume or CV, resume rewrite, JD-targeted resume optimization, or a Typst-generated PDF resume.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - typst
    homepage: https://github.com/hilaraklesantosw-art/skills
---

# Resume Builder

Use this skill when the user wants a premium, professional white-collar resume.

This skill is for:

- building a resume from raw experience notes
- rewriting an existing resume
- tailoring a resume to a target job description
- generating a polished PDF resume with Typst

It supports white-collar roles such as:

- software engineering, data, AI, QA, DevOps
- product and project management
- operations, growth, and e-commerce
- marketing, branding, and campaign roles
- sales, presales, and customer success
- HR, recruiting, finance, and administration

## Outcome

The task is only complete when the final resume has been rendered to PDF with Typst.

Produce:

- a structured resume draft
- a Typst source file
- a final PDF resume

If PDF compilation fails, do not present the task as complete.

## Workflow

### 1. Determine the resume task

Identify whether the user needs:

- a new resume from scratch
- a rewrite of an existing resume
- a JD-targeted resume
- a formatting refresh with PDF output

### 2. Extract only real candidate facts

Build a structured candidate profile from the provided material:

- name and contact details
- target role
- summary highlights
- work experience
- project experience
- education
- skills, tools, certifications, languages, links

Do not invent missing facts.

If key information is missing, ask for it or generate a conservative version that makes the gaps obvious.

### 3. Rewrite for white-collar hiring standards

Apply the writing rules from [role-writing-guidelines.md](./references/role-writing-guidelines.md).

Prioritize:

- business impact over task lists
- strong verbs over weak phrasing
- clear ownership and scope
- concrete outcomes when provided
- concise, executive-grade tone

Avoid:

- empty buzzwords
- student-style filler
- unsupported metrics
- generic claims like "good communication skills"

### 4. Tailor to the target job when a JD is provided

Read the JD and align the resume by:

- prioritizing the most relevant experience first
- reflecting the user's real match to the role
- emphasizing keywords that are already supported by the candidate's background

Do not insert technologies, industries, achievements, or responsibilities the user did not provide.

### 5. Structure the resume before rendering

Use the schema in [resume-schema.md](./references/resume-schema.md).

Default section order:

1. Header
2. Professional Summary
3. Core Skills
4. Experience
5. Selected Projects
6. Education
7. Certifications, Languages, or Links when relevant

Keep the result compact and premium. Default target length is one page for early to mid-career profiles and at most two pages for senior profiles.

### 6. Render with Typst and compile to PDF

Use the bundled renderer:

```bash
python3 scripts/render_resume.py --input candidate.json --output-dir out
```

The renderer will:

- normalize the input data
- generate `resume.typ`
- compile `resume.pdf` with `typst`

Success requires `resume.pdf` to exist.

## Output Rules

- Return a concise summary of what was generated.
- State the output file paths clearly.
- If the PDF was compiled successfully, say so explicitly.
- If compilation failed, report the error and stop short of claiming completion.

## Style Rules

Default visual style is premium executive:

- restrained, expensive-looking, high-trust layout
- no cheap template effects
- no progress bars, stars, or decorative charts
- strong hierarchy, controlled spacing, and readable density

The final resume should look credible for senior white-collar hiring, not like an auto-generated template.

## Scope Boundaries

This skill is for factual resume generation and professional PDF rendering.

It is not for:

- fabricating experience
- inventing metrics or promotions
- guaranteeing interviews or ATS outcomes
- creating overly decorative portfolio layouts
