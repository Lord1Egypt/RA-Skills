# Resume Creator

> **English documentation for the ClawHub package**

Create fact-grounded Reactive Resume JSON or a polished, offline-ready single-file HTML resume.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Reactive Resume](https://img.shields.io/badge/Reactive%20Resume-compatible-1558d6.svg)](https://rxresu.me/)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)

---

## What It Does

**Resume Creator** turns verified resume facts into either a schema-valid
[Reactive Resume](https://rxresu.me/) JSON file, a self-contained HTML resume
that opens directly from disk, or both. It never invents experience, dates,
metrics, education, links, or credentials.

```text
"Create a bilingual HTML resume from this Markdown file."
→ asks for output, language, and visual path
→ produces one responsive, printable .html file with inline CSS
```

## Why Use It

| | Without this skill | With Resume Creator |
|---|---|---|
| Facts | Polished wording can drift from the source | Only supplied or approved facts are used |
| Deliverable | A page may require a build or external assets | One offline-ready HTML file or importable JSON |
| Presentation | A visual style can be silently chosen | Explicit choice from 15 adaptations or 3 native styles |
| Publishing | Local preview is mistaken for a public deployment | Privacy, hash, DNS/TLS, and clean-render checks are separate |

## Use Cases

| Scenario | Fit | Why |
|---|---:|---|
| Create or improve a professional resume | ✅ | Collects facts, content, output, language, and visual choices |
| Reactive Resume import | ✅ | Produces JSON following the maintained schema reference |
| Portable resume website or print-friendly HTML | ✅ | Generates semantic, responsive, inline-CSS HTML |
| Static deployment after explicit approval | ✅ | Uses the same HTML source and validates public delivery |
| Full job-application pipeline | ⚠️ | Use the optional application-tracking mode only when explicitly requested |
| General portfolio, landing page, or product site | ❌ | Use a dedicated frontend or portfolio workflow instead |
| Fabricating achievements or tailoring unsupported claims | ❌ | Provide verified facts first |

## Trigger Keywords

**English:** `create a resume`, `make a resume`, `build my CV`, `write my CV`,
`improve my resume`, `resume website`, `HTML resume`, `single-file resume`,
`online resume`, `static resume site`, `bilingual resume`, `Chinese resume`,
`English resume`, `Reactive Resume JSON`, `resume JSON`, `printable resume`,
`resume PDF layout`, `deploy my resume`, `resume template`, `resume redesign`.

## Quick Start

### Install

```bash
# ClawHub
clawhub install 0xcjl/resume-creator

# Or clone and expose the folder through your agent's skill directory
git clone https://github.com/0xcjl/resume-creator.git
```

### Use

Provide a resume, Markdown notes, or verified career facts and say, for
example: “Create a bilingual HTML resume.” The skill answers in the language used in
the request: Chinese requests receive Chinese interaction; English requests
receive English interaction.

## Choice-First Workflow

Before generating a new resume, the skill collects only missing choices:

1. Deliverable: Reactive Resume JSON, standalone HTML, or both.
2. Language: Chinese, English, or bilingual.
3. Presentation: one of 15 Reactive Resume visual adaptations, or one of
   three native HTML styles.

It describes every option and recommends five relevant visual adaptations,
but does not silently select one. The 15 adaptations are authored HTML
interpretations, not claimed pixel-perfect exports from the Reactive Resume
application.

## HTML Output and Deployment

HTML output is one complete `.html` file: semantic landmarks, inline CSS,
system fonts, responsive layout, visible focus states, and paper-friendly
`@media print` styling. It has
no build step, remote stylesheet, image CDN, or required credential.

Deployment is optional and requires explicit authorization. When approved,
the deployment review checks:

- whether the user intends phone, email, address, or other contact details to
  be public;
- public HTTPS content against the final local source (hash or equivalent);
- exact custom-domain DNS and certificate readiness when applicable;
- desktop, narrow, and print layout in a clean browser/profile.

Browser extensions can inject or rewrite page text after a site loads. The
skill compares an extension-free rendering before attributing such a defect to
the HTML or host.

## Quality and Safety

- Facts stay grounded in user-provided or explicitly approved source material.
- HTML validation checks semantic structure, single-file constraints, language
  anchors, repeated experience-item alignment, and final-item wrapper errors.
- Long prose is aligned deliberately; headings, dates, bullets, metadata, and
  skill chips are not justified as prose.
- Deployment acceptance is distinct from local preview acceptance.

Read the complete reusable instructions in [SKILL.md](./SKILL.md). Detailed
HTML and deployment checks live in
[references/html-quality-check.md](./references/html-quality-check.md).

## Architecture

```text
resume-creator/
├── SKILL.md                         # Agent instructions and JSON workflow
├── references/
│   ├── schema.md                    # Reactive Resume schema reference
│   ├── template-selection.md        # 15 adaptations and 3 native styles
│   ├── html-styles.md               # Native HTML style guidance
│   ├── html-quality-check.md        # Render and deployment acceptance
│   └── application-tracking.md      # Explicit-only optional mode
├── README.md
├── README.zh-CN.md
└── LICENSE
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| A public page differs from the local file | CDN/cache or a different artifact was deployed | Compare fetched public content with the source hash |
| Text duplicates, indents, or becomes narrow in one browser | A browser extension has rewritten the DOM | Check an extension-free profile; pause the extension for the site |
| A role's bullets appear beside its date | A wrapper or grid boundary is malformed | Run the structural and visual item-header checks |
| JSON import fails | A required schema field or UUID is invalid | Revalidate against `references/schema.md` |

## Credits

- Built as an agent-skill workflow for
  [Reactive Resume](https://github.com/AmruthPillai/Reactive-Resume), whose
  JSON workflow and template vocabulary inspired this skill.
- Reactive Resume is licensed under MIT; this skill is an independent,
  compatible instruction package and is not an official Reactive Resume
  product.

## License

[MIT](./LICENSE) © 2026 Jialin Cao (0xcjl)
