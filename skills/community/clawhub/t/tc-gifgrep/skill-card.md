## Description:

Search, preview, download, and process GIFs from Tenor and Giphy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search GIF providers, return GIF URLs, download selected GIFs, and generate static frames or frame sheets for downstream media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the GifGrep CLI from an upstream package may introduce supply-chain risk, especially when using a moving latest version.

Mitigation: Review the upstream package source before installation and pin a specific trusted version where feasible.

Risk: GIF downloads and generated images can create or replace files at user-provided output paths.

Mitigation: Use non-sensitive output directories and review output paths before running download, frame extraction, or frame sheet operations.

Risk: Giphy and Tenor API keys may be sent to third-party GIF provider services.

Mitigation: Provide API keys only when their use with those services is acceptable, and avoid using credentials with broader privileges than needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/tc-gifgrep)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce GIF URLs, downloaded GIF files, static image frames, or frame sheet image files depending on the invoked GifGrep operation.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
