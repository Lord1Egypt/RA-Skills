# DOCX Template Workflow

Use this reference when the user asks for DOCX, Word, Google Docs-targeted, PDF-export, Canva-ready, Figma-ready, or visually polished resume output.

## Template Strategy

Create two resume surfaces when the user wants an impressive template:

- `ats-resume.docx`: the primary application file. It should be polished, single-column, text-first, and safe for applicant tracking systems.
- `designed-resume.docx`: the recruiter/referral version. It may use stronger visual hierarchy, accent color, compact skill groupings, and optional profile-picture treatment when explicitly approved.

Keep `professional-resume.md` as the content source of truth. Do not let the visual template introduce unsupported claims, hidden keyword stuffing, internal names, or unapproved profile photos.

If the user says the HTML resume looks better than the DOCX, treat that as expected. Keep DOCX as the ATS/application surface, then switch the impressive version to HTML/PDF/Figma/Canva handoff using `visual-design-tools-workflow.md`. Do not keep adding DOCX complexity until the ATS file becomes fragile.

## Recommended Template Options

Use one of these local template profiles:

| Profile | Best For | Visual Treatment | ATS Risk |
| --- | --- | --- | --- |
| `ats-safe` | Online applications and job portals | Single column, standard headings, clean typography, no photo, no tables used for layout | Low |
| `modern-technical` | Senior engineers, staff/principal engineers, platform/cloud/data roles | Strong header, restrained blue accent, compact technical skills, impact-first sections | Medium |
| `executive-compact` | Engineering managers, directors, senior leaders | Compact leadership summary, muted accent, selected impact blocks, board-ready spacing | Medium |

Default to `ats-safe` for job applications. Add `modern-technical` or `executive-compact` only as a designed companion file.

## Tooling

When available, use the Documents plugin workflow for DOCX creation and verification:

1. Resolve workspace document dependencies.
2. Build DOCX using `scripts/build_resume_docx.py` or the Documents plugin's DOCX tooling.
3. Render the DOCX to PNG pages with the Documents skill renderer.
4. Visually inspect each rendered page for clipping, overlap, awkward page breaks, tiny text, excessive whitespace, and formatting drift.
5. Iterate until the DOCX is clean.
6. Create `docx-render-review.md` summarizing template profile, pages rendered, issues found, fixes made, and remaining limitations.

If rendering fails because LibreOffice is missing, deliver the DOCX only after structural checks and clearly state that visual render QA could not be completed.

## DOCX Design Rules

For `ats-safe`:

- Use a single-column layout.
- Use standard section headings: Summary, Technical Skills, Professional Experience, Selected Projects, Open Source, Education, Certifications.
- Do not include profile photos, icons, text boxes, sidebars, multi-column layouts, or important content in headers/footers.
- Keep skills as plain text grouped by category.
- Use common fonts such as Aptos, Calibri, Arial, or Helvetica.
- Use 10.5-11 pt body text and readable margins.

For `modern-technical` and `executive-compact`:

- Use stronger typography and spacing before adding decoration.
- Use one restrained accent color and muted dividers.
- Keep important content in normal document flow, not text boxes.
- Use compact skill groupings only when they remain readable after render.
- Use tables only for genuine comparable data or controlled visual grouping in the designed companion version.
- Include profile pictures only in the designed version and only with user approval.
- Keep page count strategy from `resume-scorecard.md`.

## External Design Tools

Canva, Figma, Word templates, and Google Docs templates can be useful for manual polish, but they are not the default generation path because private resume content and profile pictures should not be uploaded automatically. If the user explicitly wants one of these tools:

- Produce sanitized `professional-resume.md`, `ats-resume.docx`, `designed-resume.html`, and preferably `designed-resume.pdf` first.
- Ask before uploading or pasting private content into a third-party service.
- Use the designed HTML/PDF as the visual reference. Use `designed-resume.docx` only when Word editability matters.
- Keep `ats-resume.docx` as the application file even if a visual Canva/Figma version is created.

## Quality Gate

Before final delivery, confirm:

- The ATS-safe file is not the visually busy version.
- The designed file looks intentional, not plain default Word styling.
- No important content is hidden in headers, footers, images, or text boxes.
- The first page sells role fit quickly: target role, seniority, core technologies, and strongest impact.
- The template does not force tiny fonts or cramped spacing to hit an arbitrary one-page target.
- Rendered pages show no overlap, clipping, broken bullets, cramped tables, or awkward large gaps.
