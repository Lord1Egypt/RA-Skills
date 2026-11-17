---
name: tailor-resume
description: Tailor and polish an existing resume in Google Docs for a particular job without inventing qualifications, experience, metrics, or outcomes. Use when the user provides an editable Google Docs resume link plus either direct recruiter feedback for the hiring role or a direct link to the role description, and wants the document updated to improve relevance, clarity, keyword alignment, or emphasis while remaining strictly truthful.
---

# Tailor Resume

Tailor an existing resume to a specific role by sharpening truthful material already supported by the resume or explicitly confirmed by the user. Favor honest specificity over bravado and surface unsupported gaps instead of disguising them.

## Required inputs

Require both:

1. An editable Google Docs link to the resume to update.
2. One source of role-specific direction:
   - direct recruiter feedback from a recruiter hiring for the position, or
   - a direct link to the role description.

Do not begin tailoring when either required input is missing. Ask only for the missing input. Do not substitute a generic job title, search result, inferred job description, or unrelated posting.

If a role-description link is inaccessible, ask the user for a working direct link. Do not reconstruct the posting from search snippets. If recruiter feedback is ambiguous, ask a focused question before making an edit that depends on the ambiguity.

## Truthfulness boundary

Treat the existing resume and the user's explicit factual confirmations as the only sources of candidate facts. Treat recruiter feedback and the role description as targeting guidance, not evidence that the candidate possesses a qualification.

Never:

- invent or inflate job titles, dates, employers, education, certifications, skills, responsibilities, scope, metrics, outcomes, or seniority;
- convert a team result into an individual claim without support;
- add a required or preferred qualification merely because the role mentions it;
- imply hands-on experience from adjacent knowledge;
- fabricate numbers to make a bullet appear stronger;
- conceal a material mismatch through vague or misleading language.

When a desirable claim is plausible but unsupported, ask the user to confirm it. If the user cannot confirm it, omit it and identify the gap plainly. Preserve reasonable qualifiers such as “supported,” “contributed,” or “familiar with” when stronger ownership is not established.

## Workflow

### 1. Read the role direction

Open the supplied role-description link or analyze the recruiter feedback. Extract:

- core responsibilities;
- required and preferred qualifications;
- recurring skills, terminology, and domain language;
- seniority and ownership signals;
- priorities explicitly emphasized by the recruiter.

Keep requirements separate from preferences. Do not overfit to generic company language.

### 2. Inspect the Google Doc

Use the connected Google Docs or Google Drive capability to read the supplied resume. Confirm that the link identifies a Google Doc and that write access is available before editing. Preserve the document's overall visual system, section hierarchy, dates, links, and factual content unless a targeted change is justified.

If the document cannot be opened or edited, stop and ask the user to correct access. Do not create a replacement document unless the user explicitly requests one.

### 3. Build an evidence map

For each important role priority, classify the resume evidence as:

- **Supported:** directly established by the resume or user confirmation.
- **Adjacent:** related experience exists, but the exact qualification is not established.
- **Unsupported:** no evidence exists.

Use supported evidence freely but accurately. Reframe adjacent evidence without equating it to the requested qualification. Never add unsupported claims.

### 4. Tailor the resume

Prioritize high-value, evidence-backed edits:

- strengthen the summary around demonstrated fit;
- reorder existing skills or bullets to foreground relevant experience;
- rewrite bullets for clarity, active voice, concise ownership, and role-relevant outcomes;
- use accurate terminology from the role when it describes the candidate's actual experience;
- remove repetition, filler, empty adjectives, and unsupported self-assessment;
- retain concrete metrics already present, but never create or extrapolate metrics;
- keep language natural and readable rather than mechanically repeating keywords.

Do not optimize for keyword matching at the expense of truth, nuance, or human readability. Avoid hollow descriptors such as “world-class,” “visionary,” or “expert” unless the underlying record clearly supports the term and it improves the document.

Use comments or ask for confirmation when a potentially valuable improvement requires a new fact. Do not insert placeholders or speculative language into the finished resume without the user's permission.

### 5. Verify and report

Re-read the edited document and verify:

- every factual claim remains supported;
- dates, employers, titles, links, and credentials are unchanged unless explicitly corrected;
- recruiter priorities or major role requirements are reflected where honest evidence exists;
- no keyword was introduced in a way that overstates proficiency;
- formatting and section structure remain coherent;
- the resume is concise, internally consistent, and free of obvious grammar errors.

Report:

- the sections materially changed;
- the role priorities emphasized;
- any important qualifications left unclaimed because evidence was missing;
- any factual questions that could support a later revision.

Do not claim the candidate is a perfect match or guarantee interview or hiring outcomes.
