## Description:

Use this skill when the user uploads a `.sb3` or `.sprite3` file, or when the conversation is about Scratch and clearer block-style visualization would help.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-bra0](https://clawhub.ai/user/z-bra0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and Scratch users use this skill to inspect uploaded Scratch projects, reason about Scratch code, and show block-style visualizations instead of raw Scratch JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Oversized or malicious Scratch archives could consume local disk, memory, or CPU during extraction.

Mitigation: Review before installation, run in a constrained environment, and add archive and JSON size limits before processing untrusted uploads.

## Reference(s):

- [Uploaded Scratch Files](references/UPLOADS.md)
- [Block Catalog Spec](data/BLOCK_CATALOG_SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with fenced ASCII Scratch block renderings and concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses internal scratch-json for reasoning; user-facing Scratch code is rendered through scripts/render_ascii.py.]

## Skill Version(s):

0.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
