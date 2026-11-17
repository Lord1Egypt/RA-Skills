## Description:

Extract visual identity into reusable Design DNA JSON, then apply it to generate faithful UI from references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leostehlik](https://clawhub.ai/user/leostehlik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to analyze supplied screenshots, images, or URLs and capture their visual identity in reusable Design DNA JSON, then generate UI that follows those references. It is intended for explicit reference matching and design-system work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found the scan was partial: a referenced path was missing, and scanner behavior for the CLI-installed skill could not be established.

Mitigation: Review the installed skill and its behavior before relying on its results.

Risk: Design data extracted from references may contain information that should not be shared publicly.

Mitigation: Treat extracted design data as potentially nonpublic until its sharing scope is confirmed.

Risk: Analyzing a supplied URL contacts its host, and generated UI may use external assets or dependencies.

Mitigation: Use intended references and review the reported external URLs; pin or vendor JavaScript dependencies as described in the generation guide.

## Reference(s):

- [Design DNA Schema](references/schema.md)
- [Generation Guide](references/generation-guide.md)
- [ClawHub release page](https://clawhub.ai/leostehlik/skills/visual-dna)
- [Design DNA inspiration](https://github.com/zanwei/design-dna)
- [no-slop-ui companion guidance](https://github.com/LeoStehlik/no-slop-ui)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Code, Files, Guidance]

**Output Format:** [Design DNA JSON and generated UI code, typically self-contained HTML with inline CSS and JavaScript.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the supplied references and any external dependency URLs used.]

## Skill Version(s):

0.2.3 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
