## Description:

Create, make, write, or improve a resume; output valid Reactive Resume JSON or a standalone, deployable single-file HTML resume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, and developers use this skill to turn verified resume facts into an importable Reactive Resume JSON file, an offline-ready single-file HTML resume, or both. It is suited for resume creation, resume improvement, bilingual resume preparation, print-friendly HTML resumes, and explicitly authorized static deployment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume content may expose personal contact details or career history if the user chooses to publish generated HTML.

Mitigation: Confirm which contact details may be public before deployment, and inspect the public output separately from the local file.

Risk: A polished resume could misrepresent the candidate if unsupported achievements, dates, credentials, or metrics are added.

Mitigation: Use only user-provided or explicitly approved facts, ask when information is missing, and omit unsupported claims.

Risk: Generated HTML may have layout, accessibility, or print issues that are not caught by structural parsing alone.

Mitigation: Run local visual checks at desktop, narrow, and print views, and report any unverified visual or print behavior.

Risk: Public deployment can differ from the reviewed local HTML because of cache, host transformation, DNS, TLS, or browser-extension effects.

Mitigation: Verify the public URL over HTTPS, compare source-to-public content identity when possible, check custom-domain readiness, and review in a clean browser profile.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xcjl/skills/resume-creator)
- [Reactive Resume](https://rxresu.me)
- [Reactive Resume Schema](https://rxresu.me/schema.json)
- [Reactive Resume Schema Reference](references/schema.md)
- [Presentation Selection](references/template-selection.md)
- [HTML Resume Styles](references/html-styles.md)
- [HTML Resume Quality Check](references/html-quality-check.md)
- [Application Tracking](references/application-tracking.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown conversation with generated Reactive Resume JSON or a standalone single-file HTML resume when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are grounded in user-provided or explicitly approved facts. HTML output is self-contained, responsive, accessible, and print-oriented; JSON output follows the Reactive Resume schema.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
