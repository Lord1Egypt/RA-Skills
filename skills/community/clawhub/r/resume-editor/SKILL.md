---
name: resume-builder
description: 'Build, edit, and format professional resumes with PDF import, styled HTML/PDF export, and multi-language support. Use this skill whenever a user mentions resumes, CVs, or curriculum vitae — whether they want to create one from scratch, import and edit an existing PDF resume, add or update sections (education, experience, projects, skills), export to a styled HTML or PDF document, generate multi-language versions, or apply professional formatting. Also triggers for requests like "help me update my CV", "format my resume", "translate my resume to Chinese", or "I need a professional-looking resume".'
---

# Resume Builder

## Overview

Build professional resumes with AI-assisted content management, supporting PDF import/export, HTML styling, and multi-language output.

**Canonical resume schema**: See `references/resume-schema.json` and `references/data-structure.md`
**Troubleshooting**: See `references/troubleshooting.md`
**Customization (themes, languages)**: See `references/customization.md`

## Dependencies

- **HTML generation**: Python 3 (no extra deps)
- **PDF import**: `pip install pymupdf`
- **PDF export** (either one; Playwright preferred for faithful CSS rendering): `pip install playwright && playwright install chromium` OR `pip install pdfkit && brew install wkhtmltopdf`

## Work File Convention

Save resume JSON to `resume.json` in the current working directory unless the user specifies another path. When importing from PDF, save the extracted JSON alongside the source file.

Always keep the working file in the canonical schema used by the renderer. If imported data is rough or partially parsed, normalize it before presenting edits or exporting.

## Workflow

### 1. Initial Import (if user provides existing PDF)

The `scripts/extract_from_pdf.py` script does basic text extraction, but it produces rough output. For best results, use your AI capabilities to read and understand the PDF content directly, then structure it into the resume JSON schema yourself. The script is available as a fallback:

```bash
python3 "$SKILL_DIR/scripts/extract_from_pdf.py" input.pdf output.json
```

After extraction (by any method), do not export immediately. First:

1. Normalize the data into the canonical schema.
2. Identify obvious gaps, duplicated bullets, or fields that landed as rough text.
3. Present the structured data to the user for review and ask what should be corrected or expanded.

### 2. Content Management

When adding or editing sections, gather complete information through natural conversation. The key areas to ask about:

**For Education:** institution, degree, period, location, GPA (if applicable), honors.
**For Work Experience:** company, position, period, location, responsibilities, quantifiable achievements.
**For Projects:** name, role, period, technologies, description, key achievements.

Keep asking follow-up questions if responses are brief or unclear. The goal is a complete, well-structured entry — not a minimal one.

#### Portrait photo (optional, ask before adding)

Built-in themes hide `personal.photo` by default — most regions (US, UK, Canada, Australia, much of the EU) expect resumes **without** a photo and may discard photo-bearing resumes for legal reasons (anti-discrimination). Do **not** add a photo unprompted.

Ask about a photo only when the context suggests one is expected, for example:
- Job markets where photos are conventional: mainland China, Hong Kong, Taiwan, Japan, South Korea, much of Southeast Asia, Middle East, Latin America
- Academic / research CVs in some fields, performing-arts applications, certain consulting or sales roles
- The user explicitly says the resume is for a market or role where photos are expected

When in doubt, ask once: *"Do you want a portrait on this resume? Some markets expect one, others penalize it."*

If the user wants a photo:
1. Require them to provide the image themselves. Accept a **file path**, **http(s) URL**, or **data: base64 URI**. Do not invent, fetch, or generate an image.
2. Store the value in `personal.photo`. Relative paths resolve against the HTML output location, so the user should keep the photo next to the generated HTML (or use an absolute path / URL / data URI).
3. Photo rendering is **opt-in per theme**. Built-in themes don't display it; scaffold a custom theme with `scripts/create_theme.py` and enable it:
   ```css
   .resume-photo {
       display: block;
       width: 96px; height: 96px;
       object-fit: cover;
       border-radius: 50%;   /* or 4px for a square headshot */
   }
   ```
4. Warn the user before they ship a photo resume to a market that penalizes it.

When the user requests meaningful edits, especially after import, prefer an edit-review-export flow:

1. Update `resume.json`.
2. Generate an editable HTML preview when the user will likely want to iterate visually.
3. Review the resulting content for clarity, grammar, consistency, and scannability before final export.

When the user dislikes the built-in look and wants a more personalized visual style:

1. Identify the closest built-in theme (`modern`, `classic`, `minimal`, `creative`).
2. Scaffold a reusable custom theme from that base:
   ```bash
   python3 "$SKILL_DIR/scripts/create_theme.py" custom-theme-name --base modern
   ```
3. Tune `user-themes/custom-theme-name/style.css` based on the user's feedback.
4. If layout structure must change, also adjust `user-themes/custom-theme-name/template.html`.
5. Reuse that custom theme in future exports with `--theme custom-theme-name`.

Prefer this path over editing built-in assets directly. It preserves the stock themes and gives the user a reusable personal template.

**Important separation principle:**
- **Work Experience** should stay high-level: job responsibilities at a business level, scope (team size, industry sectors), leadership and business impact.
- **Projects** should go deep on technical specifics: technologies, architecture, quantified achievements with metrics.

This separation makes the resume scannable for HR while providing depth for engineering interviews.

### 3. Export

1. Confirm format (HTML or PDF), theme, and language with the user.
2. Use the unified export script:
   ```bash
   python3 "$SKILL_DIR/scripts/export_resume.py" --format html --theme modern --lang en resume.json output.html
   ```
3. For PDF export, use:
   ```bash
   python3 "$SKILL_DIR/scripts/export_resume.py" --format pdf --theme modern --lang en resume.json output.pdf
   ```

The PDF flow always renders a clean HTML intermediary first, then converts it to PDF. Do not use editable HTML as the final PDF source.

**Available themes:** `modern`, `classic`, `minimal`, `creative`
**Custom themes:** Any folder under `user-themes/<name>/` with a `style.css`, or a direct path to a custom theme directory
**Available languages:** `en`, `zh`, `ja`, `fr`, `de`, `es`

> **`--lang` only switches UI labels** (section titles like "Work Experience", the edit-mode toolbar strings, and the `html lang` attribute). It does not translate resume body content. When a user asks to "translate my resume to X", translate the JSON content yourself first, then export with `--lang X` so labels and content stay consistent.

### 4. Interactive Edit Mode (Edit-Review-Export)

For collaborative refinement with the user, generate an editable HTML that includes inline editing capabilities:

```bash
python3 "$SKILL_DIR/scripts/export_resume.py" --format html --theme modern --lang en --editable resume.json output.html
```

**Workflow:**

1. Generate the editable HTML and tell the user to open it in a browser.
2. Guide the user explicitly:
   - Hover near the top-right corner to reveal the pencil button.
   - Click it to enter edit mode.
   - Edit text directly, add/remove bullet items where controls appear.
   - In body fields (summary, descriptions, achievement/responsibility list items, project achievements, honors), the user can select text and apply **B** / *I* / U / color from the toolbar. Title and short fields stay plain by design.
   - When finished, click **Save** in the toolbar — this writes the edited resume back to `resume.json` on disk through a local sync server that the export step starts automatically.
3. Once the user tells you they clicked Save, **re-read `resume.json` yourself** to pick up the changes. Do not ask the user to paste JSON.
4. **Final review**: Check the updated content for grammar, spelling, consistency, formatting, and section separation quality. Suggest corrections if needed.
5. Apply any corrections to `resume.json`.
6. Generate the final, non-editable version for export (HTML or PDF) using the standard export command without `--editable`.

**Rich-text markup.** Body fields support a small Markdown subset for emphasis. Both the agent (when authoring JSON) and the user (via the toolbar) use the same syntax, so they round-trip:

| Syntax | Effect |
|---|---|
| `**text**` | bold |
| `*text*` | italic |
| `_text_` | underline |
| `==text\|#rrggbb==` or `==text\|namedcolor==` | colored run |

Example: `"Achieved **30%** growth with *custom* analytics."`. The renderer applies a strict whitelist — invalid color specs are left as literal text, and HTML/script tags are escaped. Title-like fields (`name`, `company`, `position`, `degree`, `institution`, `project-name`, `role`, `category-title`, `period`, `location`, `gpa`, `technologies`, skill items) render plain to keep layouts clean.

**Notes:**
- Edit UI is hidden during print/PDF export, so the visual output is unaffected.
- The toolbar labels are localized with the selected output language.
- The local sync server binds to 127.0.0.1 only, validates the target path against the resume JSON it was started with, and requires a bearer token. Its PID/port are written next to the output HTML as `<output>.sync.json` for explicit cleanup.
- If `--no-sync` is passed (or the server failed to start), the **Save** button is disabled and the user falls back to **Copy JSON**; in that case ask them to paste.
- If you have Playwright access, you can evaluate `JSON.stringify(window.extractToJson ? extractToJson() : 'N/A')` to read edits programmatically without Save.

## Content Best Practices

- **Quantify achievements**: Include numbers and metrics (e.g., "Improved efficiency by 30%")
- **Action verbs**: Use strong action verbs (e.g., "Led", "Architected", "Built")
- **Consistency**: Maintain consistent formatting and tense across entries
- **Proofread**: Review for typos and grammatical errors before export

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/extract_from_pdf.py` | Extract text from PDF resumes (fallback — prefer AI-based parsing) |
| `scripts/generate_html.py` | Generate styled HTML from resume JSON |
| `scripts/generate_pdf.py` | Convert HTML resume to PDF |
| `scripts/export_resume.py` | Unified entrypoint for HTML/PDF export |
| `scripts/create_theme.py` | Scaffold a reusable custom theme |
| `scripts/validate_resume.py` | Validate a resume JSON against the canonical schema |
| `scripts/_edit_sync_server.py` | Local-only HTTP server (background) that the editable toolbar POSTs edits to — writes them back to `resume.json`. Started automatically by `generate_html.py` when `--editable` is set and `--no-sync` is not. Not invoked directly. |
