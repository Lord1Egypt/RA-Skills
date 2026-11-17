## Description:

Render Regulex-style railroad diagrams for a JavaScript regular expression and export the exact same SVG/PNG as the Regulex-Plus web UI Export Image feature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipedream941](https://clawhub.ai/user/pipedream941)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical writers use this skill to turn JavaScript regular expressions into Regulex-style railroad diagrams for documentation, sharing, debugging, or embedding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a headless local browser with sandboxing disabled.

Mitigation: Review before installing, prefer trusted regex inputs, and run in a locked-down container or low-privilege account when possible.

Risk: The skill depends on browser automation tooling and a local Chrome or Edge installation.

Mitigation: Keep Chrome or Edge and npm dependencies updated before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pipedream941/skills/regex-visualizer)
- [README](README.md)
- [Renderer script](scripts/render.mjs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; the renderer writes SVG and PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports JavaScript regex input and i/m/g flags; requires Node.js, puppeteer-core, and a local Chrome or Edge browser.]

## Skill Version(s):

1.0.0 (source: release metadata, manifest.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
