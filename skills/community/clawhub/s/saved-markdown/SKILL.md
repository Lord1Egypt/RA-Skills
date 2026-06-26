---
name: saved-markdown
description: |
  Publish content to saved.md and return a public shareable URL. Use when the
  user wants to publish, host, or share a Markdown, HTML, or JSX page via
  saved.md, including requests like "publish to saved.md", "post this to
  saved.md", "make this shareable", "host this page", or "give me a public
  link". Also use when the user asks for a saved.md scaffold or structured
  template-driven starting point. Do not use for private local-only drafts or
  ordinary markdown editing with no publishing or saved.md intent.
---

# saved-markdown

Publish immutable, anonymous pages to https://saved.md. Pages can be Markdown (with chart widgets), HTML (sanitized static pages with CSS), or JSX (sandboxed interactive React).

---

## Core principle

Frontmatter decides **when** to use this skill.  
Everything below defines **how** to execute once triggered.

---

## Workflow modes

After triggering, pick the mode that best matches user intent. If unclear, default to **one-shot** and mention that other modes exist.

| Mode | When | What happens |
|---|---|---|
| **One-shot** | Quick reports, logs, exports | Generate → publish → return URL |
| **Interactive** | Resumes, landing pages, anything user-facing | Generate → show draft → user edits → publish |
| **Local-only** | User explicitly wants no publishing | Save `.md` / `.html` / `.jsx`, no API call |
| **Enhance** | Existing markdown needs charts or polish | Read → enhance → publish new URL |

Pages are **immutable** — edits always produce a new URL.

---

## Execution flow (high level)

1. Decide **mode**
2. Decide **starting point** (template scaffold or freehand)
3. Decide **format** (Markdown / HTML / JSX)
4. Generate or transform content
5. Validate
6. Publish (unless local-only)

---

## Starting point decision

### 1) User explicitly asks for a scaffold
- Read `templates/INDEX.md`
- Show relevant templates (filter by format if known)
- Let user choose
- Load selected template

### 2) User wants a scaffold from a screenshot / description
- Follow `templates/create-template.md`
- Create a new template file under:
  - `templates/markdowns/` for markdown
  - `templates/htmls/` for html
  - `templates/jsx/` for jsx
- Update `templates/INDEX.md`
- Then continue like a normal template flow

### 3) User wants to enhance existing markdown
- Analyze content
- Identify visualization opportunities:
  - trends → line
  - categories → bar
  - proportions → pie
  - relationships → scatter
- Add multiple charts where justified
- Keep original structure intact
- Publish as a new page

### 4) User describes content (no scaffold mentioned)
- Match content type using routing table
- Load corresponding scaffold template
- Generate content from it

### 5) Nothing matches
- Generate freehand:
  - title
  - structured body
  - optional footer

---

## Format decision

| Format | Use when | `contentType` |
|---|---|---|
| **Markdown** | Reports, docs, dashboards, resumes, charts | `"markdown"` (or omit) |
| **HTML** | Layout-heavy pages, visual polish, static UI | `"html"` |
| **JSX** | Interactivity, filters, state, dynamic charts | `"jsx"` |

### Critical rule
If using HTML or JSX, always explicitly set `contentType`.  
Otherwise the page renders incorrectly.

---

## Content-type routing

Use this when generating structured Markdown or HTML content.

| Content type | Triggers | Template |
|---|---|---|
| Resume / CV | resume, CV, profile | `resume-cv.md` |
| Report | report, analysis, findings | `report.md` |
| Company profile | company, about, services | `company-profile.md` |
| Dashboard | KPIs, metrics, scorecard | `dashboard-metrics.md` |
| Documentation | docs, guide, manual | `documentation-guide.md` |
| Proposal | proposal, pitch, quote | `proposal-pitch.md` |
| Newsletter | newsletter, digest, changelog | `newsletter-update.md` |
| Portfolio | portfolio, projects | `portfolio-showcase.md` |
| Event | event, invitation, RSVP | `event-invitation.md` |
| Generic | everything else | freehand |

### Golden rule
Never invent content to fill sections.  
Omit anything without real data.

---

## Template scaffold workflow

When a template is selected:

1. Read template file from `templates/`
2. Show the scaffold skeleton to the user in a code block
3. Ask what to change:
   - content
   - sections
   - colors
4. Replace placeholders with user data and remove irrelevant sections
5. Validate
6. Publish

If the user already provided full content, skip template browsing and go
straight to generation.

---

## Markdown enhancement (charts)

When enhancing markdown:

- Add charts using `markdown-ui-widget`
- Use multiple charts when data supports it
- Ensure:
  - numeric values are plain numbers (no `$`, `%`, `K`, etc.)
  - units go in labels, not values

Template guide: `templates/charts.md`

---

## Validation checklist

Before publishing:

- Content under **100 KB**
- Correct `contentType`
- Charts valid (if markdown)
- HTML sanitized (no scripts)
- JSX:
  - only allowed imports (`react`, `react-dom`)
  - no external packages
- No placeholder text left

Template guide: `templates/validation.md`

---

## Publishing

### Preferred (script)

```bash
python scripts/publish.py --file <path> --content-type <markdown|html|jsx> --title "<title>"
```

### Direct API contract (source-of-truth behavior)

Use `POST https://saved.md/api/pages` with JSON.

Required/expected payload fields:

- `markdown` (string): page source body for markdown, html, or jsx pages
- `contentType` (string): `"markdown"`, `"html"`, or `"jsx"`

Example payload:

```json
{
  "markdown": "# My Page\n\nPublished from skill",
  "contentType": "markdown"
}
```

For markdown pages, `contentType` may be omitted, but setting it explicitly is
recommended for consistency.

### Remixing an existing page (immutable URLs)

When users request edits to an existing saved.md URL:

1. Parse page id from URL
2. `GET /api/pages/{id}` and read `markdown` + `contentType`
3. Apply requested edits to the returned `markdown`
4. `POST /api/pages` using the edited `markdown` and the same `contentType`
5. Return the **new** URL (old URL remains unchanged)

Never imply in-place updates are possible.