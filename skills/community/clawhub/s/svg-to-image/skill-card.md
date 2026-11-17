## Description:

Convert SVG to PNG or JPG for quick sharing (e.g. Telegram) or print.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrost](https://clawhub.ai/user/qrost)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to rasterize SVG assets into PNG or JPG files for sharing in chat, use in documents, or print, with optional width, height, and DPI controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converting untrusted SVG files may allow the renderer to access local or network resources.

Mitigation: Run conversions for untrusted SVGs in a sandbox with limited filesystem and network access.

Risk: Unpinned image-rendering dependencies can change behavior across installs.

Mitigation: Pin dependency versions before broad or repeated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qrost/skills/svg-to-image)
- [Publisher GitHub profile](https://github.com/QROST)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG or JPG image files with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional output width, height, and DPI controls.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
