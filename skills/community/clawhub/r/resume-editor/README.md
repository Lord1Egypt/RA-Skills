# Resume Editor

AI-powered resume builder that runs locally. Import from PDF, edit interactively, export to styled HTML and PDF — in 6 languages, 4 themes.

**Works with:** [OpenClaw](https://github.com/openclaw/openclaw) · Claude Code · OpenAI Codex

## Features

- **PDF Import** — Extract structured data from existing resumes
- **AI Editing** — Add/update sections through natural conversation
- **4 Themes** — Modern, Classic, Minimal, Creative
- **Custom Themes** — Derive and reuse your own style from any built-in theme
- **6 Languages** — English, 中文, 日本語, Français, Deutsch, Español
- **Dual Export** — Styled HTML + print-ready PDF (A4)
- **Editable Review Loop** — Browser-based preview and edit before final export
- **Local-first** — Everything runs locally, no data leaves your machine

## Prerequisites

- **Python 3.7+** is required for resume generation scripts
- **Optional**: `pip install pymupdf` for PDF import
- **Optional**: `pip install playwright && playwright install chromium` (recommended) OR `pip install pdfkit && brew install wkhtmltopdf` for PDF export

## Installation

### OpenClaw

**Option 1: Install from ClawHub (recommended)**

```bash
openclaw skills install resume-editor
```

The published ClawHub page for this skill is:
`https://clawhub.ai/chijiang/resume-editor`

**Option 2: Install from GitHub**

```bash
openclaw skills install git:chijiang/resume-editor
```

This matches OpenClaw's documented `git:` source install format.

**Option 3: Manual workspace install**

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/chijiang/resume-editor.git ~/.openclaw/workspace/skills/resume-builder
```

OpenClaw's documented workspace skill path is `~/.openclaw/workspace/skills/<skill>/SKILL.md`.

### Claude Code

**Option 1: Global skill install**

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/chijiang/resume-editor.git ~/.claude/skills/resume-builder
```

Restart your Claude Code session to activate it.

**Option 2: Install via plugin marketplace**

In a Claude Code session, run:

```
/plugin marketplace add chijiang/resume-editor
/plugin install resume-builder@resume-editor
/reload-plugins
```

This repo includes a `.claude-plugin/marketplace.json`, so the marketplace install path can reference the `resume-builder` plugin from the `resume-editor` marketplace.

### OpenAI Codex

Codex discovers skills from `.agents/skills` in the current repo, or from `~/.agents/skills` for user-wide install.

**Option 1: Project-scoped install**

```bash
mkdir -p .agents/skills
git clone https://github.com/chijiang/resume-editor.git .agents/skills/resume-builder
```

**Option 2: User-scoped install**

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/chijiang/resume-editor.git ~/.agents/skills/resume-builder
```

No `AGENTS.md` wiring is required for Codex skill discovery. You can still use `AGENTS.md` for repo-specific working rules, but the skill itself should live under a discovered `.agents/skills` path.

## Usage

After installing, just talk to your AI agent naturally:

- "Create a resume for me"
- "Import my resume from `resume.pdf`"
- "Add a project section: built a React dashboard"
- "Export my resume as PDF with the modern theme"
- "Translate my resume to Chinese"

The skill auto-detects when you're working on resumes and guides the process.

## Quick Start (CLI)

If you prefer to run scripts directly without an AI agent:

```bash
# Generate HTML from example data
python3 scripts/export_resume.py --format html --theme modern --lang en references/example-resume.json output.html

# Convert to PDF
python3 scripts/export_resume.py --format pdf --theme modern --lang en references/example-resume.json output.pdf

# Generate editable review HTML first
python3 scripts/export_resume.py --format html --theme modern --lang en --editable references/example-resume.json editable-output.html

# Create a reusable custom theme from an existing base
python3 scripts/create_theme.py editorial --base modern

# Export with your custom theme later
python3 scripts/export_resume.py --format html --theme editorial --lang en references/example-resume.json editorial-output.html

# Import from existing PDF
python3 scripts/extract_from_pdf.py existing-resume.pdf extracted.json

# Validate a resume JSON against the canonical schema
python3 scripts/validate_resume.py resume.json
```


## Languages

| Code | Language |
|------|----------|
| `en` | English |
| `zh` | 中文 |
| `ja` | 日本語 |
| `fr` | Français |
| `de` | Deutsch |
| `es` | Español |

## Resume Data Schema

```json
{
  "personal": {
    "name": "Your Name",
    "email": "you@example.com",
    "phone": "+86 138-0000-0000",
    "location": "City, Country",
    "linkedin": "https://linkedin.com/in/yourprofile",
    "github": "https://github.com/yourusername",
    "photo": "photo.jpg"
  },
  "summary": "A brief professional summary...",
  "education": [
    {
      "institution": "University Name",
      "degree": "Bachelor of Science in Computer Science",
      "period": "2016-2020",
      "location": "City",
      "gpa": "3.8/4.0",
      "honors": ["Dean's List", "Scholarship"]
    }
  ],
  "experience": [
    {
      "company": "Company Name",
      "position": "Job Title",
      "period": "2020-Present",
      "location": "City",
      "description": "High-level role description — scope, leadership, business impact.",
      "responsibilities": ["Responsibility 1", "Responsibility 2"],
      "achievements": ["Achievement with measurable result"]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "role": "Lead Developer",
      "period": "2023",
      "technologies": ["Python", "React", "AWS"],
      "description": "What the project does and your contribution.",
      "achievements": ["Key result with metrics"]
    }
  ],
  "skills": {
    "programming": ["Python", "JavaScript", "Go"],
    "frameworks": ["React", "Django"],
    "tools": ["Git", "Docker", "Kubernetes"],
    "languages": ["Chinese (Native)", "English (Fluent)"]
  }
}
```

> Only `personal.name` is required. All other fields are optional. The canonical machine-readable schema is in [`references/resume-schema.json`](references/resume-schema.json).

## Example

A complete example is in [`references/example-resume.json`](references/example-resume.json). Try it:

```bash
python3 scripts/export_resume.py \
  --format html --theme modern --lang en \
  references/example-resume.json \
  example-output.html
```

Open `example-output.html` in a browser to preview.

## Recommended Journey

For meaningful edits or imported resumes, use this flow:

1. Import or create `resume.json`
2. Generate an editable HTML preview
3. Review and refine content visually
4. Copy the updated JSON back into your working file
5. Export a final non-editable HTML or PDF

If the default themes are close but not quite right:

1. Pick the nearest built-in theme
2. Scaffold a reusable custom theme with `scripts/create_theme.py`
3. Adjust `user-themes/<name>/style.css`
4. Reuse that theme name in future exports

## Project Structure

```
resume-editor/
├── SKILL.md                  # Skill definition for AI agents
├── plugin.json               # Plugin metadata
├── README.md                 # This file
├── references/
│   ├── example-resume.json   # Example resume (fictional data)
│   └── resume-schema.json    # Canonical resume schema
├── scripts/
│   ├── create_theme.py       # Scaffold a reusable custom theme
│   ├── export_resume.py      # Unified JSON → HTML/PDF export
│   ├── extract_from_pdf.py   # PDF → JSON
│   ├── generate_html.py      # JSON → HTML (multi-theme, multi-language)
│   ├── generate_pdf.py       # HTML → PDF
│   ├── resume_utils.py       # Shared schema/localization helpers
│   └── validate_resume.py    # Validate a resume JSON against the schema
├── assets/
│   ├── css/                  # Theme stylesheets
│   │   ├── modern.css
│   │   ├── classic.css
│   │   ├── minimal.css
│   │   └── creative.css
│   └── templates/            # HTML wrapper template
│       └── base.html
├── previews/                 # Pre-rendered theme samples (regenerable from references/example-resume.json)
│   ├── modern.html
│   ├── classic.html
│   ├── minimal.html
│   └── creative.html
└── commands/
    └── resume-export.md      # Slash command definition
```

## Best Practices

- **Work Experience** → High-level: role scope, team size, business impact, leadership
- **Projects** → Technical depth: tools, architecture, quantified achievements
- **Quantify** — "Improved efficiency by 30%" > "Improved efficiency"
- **Action verbs** — Led, Architected, Built, Designed, Optimized
- **Proofread** — Typos kill first impressions
- **Photo** — Optional via `personal.photo` (path, URL, or data URI). Hidden by default in all built-in themes; enable it in a custom theme's CSS. Only include a photo when the target market expects one — many regions (US/UK/Canada/Australia/much of EU) penalize or reject photo resumes.

## License

MIT

---

<p align="center">
  <sub>Built for <a href="https://github.com/openclaw/openclaw">OpenClaw</a> · Compatible with Claude Code & Codex</sub>
</p>
