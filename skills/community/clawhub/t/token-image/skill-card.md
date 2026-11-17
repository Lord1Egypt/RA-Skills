## Description:

Generate themed social and marketing image React components using design tokens, producing TSX files that render to PNG.

This skill is ready for commercial/non-commercial use.

## Publisher:

[czl9707](https://clawhub.ai/user/czl9707)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to generate coordinated social cards, banners, Open Graph images, and related marketing visuals from selected design-token presets. The workflow collects theme, image, format, layout, and branding inputs, then guides agents to create shared TSX/CSS files and per-image React components for PNG rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill bootstraps a local .token-image workspace and writes generated files under .token-image/src/.

Mitigation: Run it in a project sandbox or review the target workspace before generation so unrelated project files and secrets are not exposed to generated tooling.

Risk: The init flow installs npm dependencies and Playwright Chromium, including unpinned registry tooling noted by the security summary.

Mitigation: Review package installation steps first and prefer pinned dependencies or a reviewed lockfile before running setup in sensitive environments.

Risk: The workflow launches a local editor after generating image components.

Mitigation: Use it only in an environment where opening a local development service is acceptable, and close the editor when inspection is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/czl9707/skills/token-image)
- [Viewport reference](artifact/references/viewports.md)
- [Component reference](artifact/references/components.md)
- [Default stylesheet](artifact/references/default-styles.css)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated TSX/CSS project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates shared viewport and stylesheet files plus per-image React components intended to render to PNG.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
