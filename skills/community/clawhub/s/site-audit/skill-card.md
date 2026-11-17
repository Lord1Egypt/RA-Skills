## Description:

Use when the user wants a current site audit, technical SEO findings, Core Web Vitals interpretation, or a fresh TrustGrowth audit when connected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical SEO practitioners, and site owners use this skill to inspect available site evidence, interpret technical SEO and Core Web Vitals findings, and produce evidence-labeled audit guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a local `.groundcrew/groundcrew-doctor.py` validator that is not bundled in the package.

Mitigation: Install only in an environment where that validator path is trusted, immutable, and expected before relying on audit conclusions.

Risk: The package references `references/provider-selection.md`, but that file is absent from the artifact.

Mitigation: Review source-selection behavior before use and prefer already available, user-controlled evidence sources.

Risk: Manual TrustGrowth audits require write scope and explicit user intent.

Mitigation: Confirm the user requested a manual audit and that the configured credential has the intended scope before triggering it.

## Reference(s):

- [Connectors and categories](artifact/references/connectors.md)
- [Reporting contract](artifact/references/reporting.md)
- [ClawHub skill page](https://clawhub.ai/trustgrowth/skills/site-audit)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown or concise text with evidence labels, findings, next actions, and optional command or API snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports separate observed facts from interpretation, preserve unknowns, and avoid projected SEO impact.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
