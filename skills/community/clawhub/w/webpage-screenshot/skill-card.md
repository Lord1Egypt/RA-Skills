## Description:

Opens a specified webpage and captures it as a PNG image file when a user needs a URL screenshot or page snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[malenconiaprincep](https://clawhub.ai/user/malenconiaprincep)

### License/Terms of Use:


## Use Case:

Developers, operators, and other agent users use this skill to capture full-page visual records of webpages as PNG files, or to inspect webpage state through a browser snapshot when a saved image is not required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full-page screenshots can capture secrets, private account data, or internal content.

Mitigation: Review target pages and authenticated sessions before saving or sharing screenshots.

Risk: Browser automation setup from unpinned or untrusted project dependencies can introduce supply-chain risk.

Mitigation: Run Playwright from a pinned project dependency or trusted lockfile and install Chromium in a trusted environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/malenconiaprincep/skills/webpage-screenshot)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and procedural steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a PNG screenshot file at a user-specified path; default output is screenshot.png.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
