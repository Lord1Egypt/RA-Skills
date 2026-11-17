## Description:

Generate clean table images from data for messaging platforms, with dark and light themes, custom styling, emoji support, RTL support, and auto-sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to convert structured JSON rows into clean PNG table images for Discord, Telegram, WhatsApp, and similar channels where ASCII tables render poorly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emoji artwork is downloaded and cached from a live CDN without a server-resolved provenance guarantee.

Mitigation: Pin or vendor emoji assets, validate downloaded SVGs, disclose cache behavior, and apply network limits before broad deployment.

Risk: Image generation depends on Sharp, which the security evidence flags for review.

Mitigation: Pin Sharp to a reviewed non-vulnerable version and keep dependency scanning in the release gate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dannyshmueli/skills/table-image-generator)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [PNG image files with concise Markdown and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports JSON input through command arguments, stdin, or data files; optional title, column, header, alignment, width, font, dark mode, RTL, wrapping, and compact layout settings.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
