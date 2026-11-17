---
name: resume-creator
description: Create, make, write, or improve a resume; output valid Reactive Resume JSON or a standalone, deployable single-file HTML resume. Use when a user asks to create a resume, generate a CV, make a resume website, or improve resume content.
version: 1.0.1
author: 0xcjl
license: MIT
metadata:
  hermes:
    tags: [resume, html, reactive-resume, static-site, bilingual, accessibility, print]
    related_skills: [agent-skill-publisher]
---

# Resume Creator

Build professional resumes through conversational AI for [Reactive Resume](https://rxresu.me), a free and open-source resume builder, or as a standalone HTML resume site.

## Core Principles

1. **Never hallucinate** - Only include information explicitly provided by the user
2. **Ask questions** - When information is missing or unclear, ask before assuming
3. **Be concise** - Use clear, direct language; avoid filler words
4. **Validate output** - Ensure all generated JSON conforms to the schema

## First-Turn Selection Gate

For a new resume, do not generate an artifact before collecting the choices
that are still missing. Ask in this order and do not repeat a choice the user
has already supplied:

1. **Deliverable:** single-file HTML, Reactive Resume JSON, or both.
2. **Language:** Chinese, English, or bilingual.
3. **Presentation:** read [references/template-selection.md](references/template-selection.md) and present both visual paths in the conversation language: all 15 Reactive Resume visual adaptations with their adaptation characteristics and suitable directions, followed by all three native HTML styles with their visual characteristics and suitable scenarios. Recommend five Reactive Resume adaptations tailored to the supplied resume facts and target reader; when those facts are unavailable, recommend the neutral fallback five specified in the reference. The recommendation is not a default.

For JSON, the user chooses one of the 15 Reactive Resume templates. For
single-file HTML, the user chooses either a named **Reactive Resume visual
adaptation** or a native HTML style. A visual adaptation is a newly authored,
self-contained HTML rendition guided by the selected template; it is not an
export from the Reactive Resume app or a claim of pixel-exact parity.

Never silently apply a visual default. An agent may recommend five options, but
must wait for the user's selection unless the user explicitly delegates the
choice. Once all choices are known, briefly restate the chosen deliverable,
language, and presentation before generating.

## Output Modes

Select the output from the user's requested destination; do not silently replace one mode with the other.

- **Reactive Resume JSON (default):** Use when the user asks for Reactive Resume, importable JSON, or does not request a file or website. Follow the schema workflow below and read [references/schema.md](references/schema.md).
- **Single-file HTML:** Use when the user explicitly asks for HTML, a website resume, a file that opens locally, a static site, print-ready output, or a PDF-friendly web resume. Produce one complete `.html` file that can be opened directly with `file://`; do not require a build step, server, JavaScript framework, remote stylesheet, image CDN, font download, credential, or external service.
- **Both:** When the user explicitly asks for both, produce each artifact from the same verified facts. JSON stays schema-valid; HTML is an independent presentation layer. Do not attempt to make HTML conform to the Reactive Resume JSON schema.

For HTML mode, first gather the same factual content needed for a resume. Write only facts the user has provided or explicitly approved; preserve uncertainty as a question or omit the claim. Do not invent employers, dates, degrees, credentials, metrics, links, contact details, or project outcomes. A polished visual treatment must not imply experience that the source material does not support.

### Single-file HTML Requirements

- Include `<!doctype html>`, a declared document language, UTF-8 viewport metadata, a descriptive `<title>`, and all CSS inside one `<style>` block. Keep scripts out unless they are necessary for an explicitly requested, local-only interaction; the resume must remain readable without JavaScript.
- Use semantic structure appropriate to a resume: `<header>`, `<main>`, named `<section>` elements with headings, lists for achievements, and native `<a>` links for supplied email, phone, and URLs. Escape user-provided text before inserting it into HTML.
- Make the layout responsive using fluid sizing and a narrow-screen layout; avoid horizontal scrolling and color-only distinctions. Use a readable system-font stack and sufficient contrast so the file stays dependable when opened offline.
- Add `@media print` rules for clean A4/Letter-friendly printing: remove screen-only decoration, retain link destinations where useful, use sensible margins, and avoid splitting a role or major heading from its content where CSS support permits. Do not claim that the output is a generated PDF unless one has actually been generated and checked.
- Provide accessible navigation and reading order: one visible `h1`, sequential headings, meaningful link text, visible keyboard focus, and no essential information conveyed only by color, hover, image, or icon. Treat a supplied headshot as optional and include meaningful `alt` text only when the user supplied a factual description; otherwise omit it or use empty alt text for decoration.
- Keep external deployment optional and non-mutating. State that the same file can be uploaded to any static host or served by an existing static-site workflow, but do not deploy, publish, or create an account unless the user explicitly authorizes it.

Before delivering an HTML file, verify that it is a single self-contained file, parses as HTML, contains the expected semantic landmarks, and can be opened locally in a browser or an equivalent local renderer. For the final visual and alignment review, read [references/html-quality-check.md](references/html-quality-check.md). Report any unverified visual or print/PDF aspect clearly.

When the user explicitly authorizes static deployment, use the same source file for the deployed artifact and read the deployment review in [references/html-quality-check.md](references/html-quality-check.md). Verify the public URL separately from local rendering: DNS/TLS when a custom domain is involved, HTTP success, content identity or an equivalent source-to-public check, and a clean-browser visual pass. Confirm whether personal contact details are intended to be public before publishing; omit them from the public variant when the user requests it. Do not attribute browser-extension DOM injection to the deployed file without comparing against an extension-free renderer.

### Language and HTML Style

Keep the resume language aligned with the user's target reader. Support Chinese, English, and bilingual output; ask which one to use when the supplied facts do not make it clear. For bilingual output, preserve proper names, URLs, dates, credentials, and numbers exactly; translate only claims that the user supplied or approved.

Match the interaction language to the user's latest substantive resume message:
reply in Chinese to Chinese interaction and in English to English interaction.
This applies to the visual-path explanation, all option descriptions,
recommendations, questions, progress updates, and delivery note. Preserve
template names, product names, code, URLs, and user-provided proper names.
For a genuinely mixed-language request, follow the language the user uses for
the request itself, unless they explicitly ask for another response language.

For HTML output, read [references/template-selection.md](references/template-selection.md) before the presentation question. Show the full requested comparison, then wait for one named Reactive Resume visual adaptation or one native HTML style. Read [references/html-styles.md](references/html-styles.md) when the user selects a native style. If the user explicitly delegates the choice, recommend and state the selected option before generating.

## Application Tracking (explicit request only)

When the user explicitly asks to track or manage job applications, read [references/application-tracking.md](references/application-tracking.md). Do not load or mention application-tracking operations for ordinary resume creation.

## Workflow

### Client Compatibility

This shared skill is available to Codex and Hermes. Use Reactive Resume MCP
application tools only when the current client explicitly exposes them. If they
are unavailable, do not invent tool calls or claim that an application was
created or updated; gather the required facts and generate valid Reactive
Resume JSON instead.

### Step 1: Gather Basic Information

Ask for essential details first, unless the user has already provided them:

- Full name
- Professional headline/title
- Email address
- Phone number
- Location (city, state/country)
- Website (optional)

### Step 2: Collect Section Content

For each section the user wants to include, gather specific details. Never invent dates, company names, or achievements.

**Experience**: company, position, location, period (e.g., "Jan 2020 - Present"), description of responsibilities/achievements

**Education**: school, degree, area of study, grade (optional), location, period

**Skills**: name, proficiency level (Beginner/Intermediate/Advanced/Expert), keywords

**Projects**: name, period, website (optional), description

**Other sections**: languages, certifications, awards, publications, volunteer work, interests, references

### Step 3: Configure JSON Layout and Design (JSON only)

Skip this step for HTML-only output. For JSON output, ask about:

- Template preference (read [references/template-selection.md](references/template-selection.md) and present the 15 choices)
- Page format: A4 or Letter
- Which sections to include and their order

### Step 3A: Configure HTML Presentation (HTML only)

Read [references/template-selection.md](references/template-selection.md), then the selected HTML style guidance if applicable. Create one accessible, responsive, print-ready file from the verified resume facts. Do not copy an external template or make the HTML depend on external assets.

### Step 4: Generate Valid JSON

Output must conform to the Reactive Resume schema. See [references/schema.md](references/schema.md) for the complete schema structure.

Key requirements:

- All item `id` fields must be valid UUIDs
- Description fields accept HTML-formatted strings
- Website fields require both `url` and `label` properties
- Colors use `rgba(r, g, b, a)` format
- Fonts must be available on Google Fonts

## Resume Writing Tips

Share these tips when helping users craft their resume content:

### Content Guidelines

- **Lead with impact**: Start bullet points with action verbs (Led, Developed, Increased, Managed)
- **Quantify achievements**: Use numbers when possible ("Increased sales by 25%", "Managed team of 8")
- **Tailor to the role**: Emphasize relevant experience for the target position
- **Be specific**: Replace vague terms with concrete examples
- **Keep it concise**: 1-2 pages maximum for most professionals

### Section Order Recommendations

For most professionals:

1. Summary (if experienced)
2. Experience
3. Education
4. Skills
5. Projects (if relevant)
6. Certifications/Awards

For students/recent graduates:

1. Education
2. Projects
3. Skills
4. Experience (if any)
5. Activities/Volunteer

### Common Mistakes to Avoid

- Including personal pronouns ("I", "my")
- Using passive voice
- Listing job duties instead of achievements
- Including irrelevant personal information
- Inconsistent date formatting

## Output Format

For JSON output, produce a complete object that conforms to the Reactive Resume schema. The user can then import it directly into Reactive Resume at https://rxresu.me. For HTML output, deliver the requested `.html` file and briefly state the chosen language and style.

Example minimal structure:

```json
{
  "picture": { "hidden": true, "url": "", "size": 80, "rotation": 0, "aspectRatio": 1, "borderRadius": 0, "borderColor": "rgba(0, 0, 0, 0.5)", "borderWidth": 0, "shadowColor": "rgba(0, 0, 0, 0.5)", "shadowWidth": 0 },
  "basics": { "name": "", "headline": "", "email": "", "phone": "", "location": "", "website": { "url": "", "label": "" }, "customFields": [] },
  "summary": { "title": "Summary", "columns": 1, "hidden": false, "content": "" },
  "sections": { ... },
  "customSections": [],
  "metadata": { "template": "onyx", "layout": { ... }, ... }
}
```

For the complete schema, see [references/schema.md](references/schema.md).

## Asking Good Questions

When information is missing, ask specific questions:

- "What was your job title at [Company]?"
- "What dates did you work there? (e.g., Jan 2020 - Dec 2022)"
- "What were your main responsibilities or achievements in this role?"
- "Do you have a specific target role or industry in mind?"

Avoid compound questions. Ask one thing at a time for clarity.
