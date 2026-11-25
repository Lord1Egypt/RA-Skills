# Visual Design Tools Workflow

Use this reference when the user wants the resume to look impressive, polished, Canva-ready, Figma-ready, portfolio-style, or better than a plain DOCX.

## Recommendation

Use a dual-output strategy:

- `ats-resume.docx`: application file for job portals and applicant tracking systems.
- `designed-resume.html` plus optional `designed-resume.pdf`: visual resume for recruiters, referrals, networking, and portfolio review.

Do not force the rich visual design into DOCX. DOCX is useful for editability, but HTML/PDF/Figma are better for exact layout, spacing, typography, color, visual hierarchy, and profile-photo treatment.

## Tool Selection

| User Goal | Best Tool Path | Output |
| --- | --- | --- |
| Submit through job portal | DOCX text-first template | `ats-resume.docx` |
| Share with recruiter or referral | HTML rendered to PDF | `designed-resume.html`, `designed-resume.pdf` |
| Fine-tune a visual layout | Figma MCP when user provides or approves a Figma file | Figma design plus exported PDF/PNG |
| Use Canva templates | Manual/import handoff unless user explicitly approves upload | `visual-tool-handoff.md`, sanitized copy blocks, HTML/PDF |
| Preserve exact design locally | Browser-rendered HTML/PDF | HTML, PDF, PNG screenshot |
| Need editable Word file | Designed DOCX companion with clear caveats | `designed-resume.docx` |

## Visual Template Selection

Before building an impressive visual artifact, read `visual-template-profiles.md` and create `visual-template-selector.md`.

Record:

- Selected profile: Modern Technical, Executive Compact, Open Source Builder, Enterprise Platform, or AI Automation.
- Target audience: recruiter, referral, hiring manager, portfolio, or internal review.
- Why the selected profile fits the user's target role, years of experience, evidence, and disclosure limits.
- Profile picture status: omitted, user-provided local path, or approved for this artifact.
- Third-party upload status: not needed, needs user approval, or user approved.

Do not make the visual selector a blocker for normal resume generation. It is a decision record for visual outputs.

## HTML/PDF First Workflow

1. Build `professional-resume.md` from verified evidence.
2. Select a visual profile and create `visual-template-selector.md`.
3. Build `designed-resume.html` from the same sanitized content.
4. Use browser tooling when available to render desktop and print views.
5. Export or print to `designed-resume.pdf` when requested.
6. Create `visual-design-review.md` with viewport, print, spacing, clipping, and page-break checks.

The HTML design should:

- Use a strong first-page hierarchy: name, target role, role-fit summary, key skills, and strongest impact.
- Keep visual structure clean: restrained accent color, generous spacing, readable type, and clear sections.
- Avoid decorative clutter that reduces scanability.
- Use profile photo only when user provides and approves it.
- Keep private content local unless the user explicitly approves third-party upload.

## Figma Workflow

Use Figma when the user wants a high-quality design artifact or wants to edit visually after generation.

Requirements:

- The Figma plugin must be available.
- The user must provide or approve a target Figma file.
- Before writing to Figma, load the Figma use guidance and follow the Figma MCP workflow.
- Search the design system first when a file has existing components, variables, or styles.

Figma output should contain:

- A Letter or A4 resume frame.
- A recruiter-facing visual frame.
- Optional profile-photo placeholder or approved image.
- Clearly named text layers for easy editing.
- A note that `ats-resume.docx` remains the submission file for job portals.

## Canva Workflow

Canva is useful for manual polish and visual templates, but do not upload private resume content or profile pictures automatically.

When the user asks for Canva:

- Produce `designed-resume.html` and `designed-resume.pdf` locally first.
- Create `visual-tool-handoff.md` with sanitized copy blocks and section ordering.
- Ask before any third-party upload.
- If the user manually imports into Canva, recommend using the designed PDF/PNG as visual reference and pasting sanitized text blocks.
- Keep `ats-resume.docx` for applications.

## DOCX Caveat

If the user says the DOCX does not look as good as HTML, acknowledge that this is expected. DOCX supports polished typography and spacing, but it is weaker for exact visual composition. The skill should offer a visual-first output instead of over-styling the ATS DOCX.

## QA Checklist

Create `visual-design-review.md` and check:

- Desktop view is polished and readable.
- Print/PDF page breaks are acceptable.
- Text does not overlap or clip.
- Skills, dates, and company names remain readable.
- The first viewport or first page sells role fit quickly.
- The design remains professional, not decorative at the cost of clarity.
- Third-party upload status is explicit: not uploaded, manually imported, or user-approved upload.
- The selected visual profile is documented in `visual-template-selector.md`.
