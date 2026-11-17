## Description:

Create wireframes and user flows. Use when sketching page layouts in ASCII/SVG, mapping flows, or exporting to HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use this skill to generate quick page wireframes, component sketches, user-flow diagrams, SVG annotations, and standalone HTML exports during UI planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, overwrite, or modify local output files, including annotated SVGs.

Mitigation: Use explicit --output paths and keep backups of source SVGs before running annotate or export commands.

Risk: User-provided labels, titles, notes, or SVG content may be embedded into SVG or HTML artifacts that are later opened in a browser or published.

Mitigation: Avoid untrusted input for labels, titles, notes, and SVG files when generated output will be opened in a browser or hosted on a trusted site.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated artifacts are ASCII text, SVG files, or standalone HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be written to user-specified local paths.]

## Skill Version(s):

3.4.1 (source: ClawHub release metadata; artifact frontmatter lists 3.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
