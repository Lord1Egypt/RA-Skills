## Description:

Teaching App Builder turns teaching text, concepts, lecture notes, or course material into a self-contained interactive HTML teaching app with visuals, interaction patterns, and optional CDN-hosted libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwugit](https://clawhub.ai/user/junwugit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and instructional designers use this skill to convert source teaching material into a browser-openable HTML app with diagrams, charts, formulas, stepwise explanations, quizzes, and focused interactions. It is suited for external or internal teaching demos when the user supplies the factual instructional content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML files may contact public CDNs when opened.

Mitigation: Install and use the skill only when public CDN loading is acceptable; prefer local or SRI-protected dependencies for sensitive deployments.

Risk: Untrusted teaching material inserted into generated pages can create Markdown or DOM sanitization risk.

Mitigation: Ask the agent to sanitize Markdown and review generated HTML before opening or distributing pages built from untrusted material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junwugit/skills/teaching-app-builder)
- [CDN catalog](artifact/references/cdn-catalog.md)
- [Professional color schemes](artifact/references/color-schemes.md)
- [Teaching interaction components](artifact/references/components.md)
- [Library snippets](artifact/references/libraries.md)
- [Single-file skeleton and quality checklist](artifact/references/skeleton.md)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Configuration instructions, Guidance]

**Output Format:** [Single-file HTML plus concise Markdown delivery notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML may reference public CDNs when opened in a browser.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
