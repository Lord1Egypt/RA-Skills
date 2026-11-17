## Description:

Generate and preview CSS shadow effects using CLI tools for box-shadow, text-shadow, drop-shadow, layered shadows, presets, animations, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use Shadow to generate reusable CSS shadow values, compose saved shadow presets, preview effects, and export CSS, JSON, or SCSS for design systems and UI implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved shadow names and CSS values are stored locally in ~/.shadow/data.jsonl.

Mitigation: Avoid saving names or CSS/color values from untrusted sources and review saved records before reuse.

Risk: Generated HTML previews may contain saved shadow values that are not escaped or validated.

Mitigation: Review generated preview files before opening them in a browser, especially when inputs came from another user or system.

## Reference(s):

- [Shadow on ClawHub](https://clawhub.ai/bytesagain-lab/skills/shadow)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [CLI text output with CSS, JSON, SCSS, Markdown command examples, and optional HTML preview files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist saved shadow records to ~/.shadow/data.jsonl and write preview or export files when requested.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
