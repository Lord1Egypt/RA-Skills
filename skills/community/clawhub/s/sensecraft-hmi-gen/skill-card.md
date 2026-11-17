## Description:

Generate beautiful web content for SenseCraft HMI e-ink displays with AI-powered layout selection and e-ink optimization for screens from 800x480 to 1600x1200.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killingjacky](https://clawhub.ai/user/killingjacky)

### License/Terms of Use:

MIT

## Use Case:

Developers and SenseCraft HMI users use this skill to generate e-ink-optimized HTML pages, gather display configuration, preview content locally, and prepare content for the SenseCraft HMI HTML widget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts local Node/Express services and persists configuration and token files.

Mitigation: Review generated files before use, treat .wizard-config.json and token URLs as sensitive, and stop the PM2-managed service when finished.

Risk: Forwarding the localhost server to the public internet can expose generated content with weak token-only access control.

Mitigation: Use HTTPS, short-lived tokens, stronger authentication, and access restrictions before exposing the service outside localhost.

## Reference(s):

- [E-Ink Design Patterns](references/design-patterns.md)
- [E-Ink Layout Templates](references/layouts.md)
- [SenseCraft HMI Screen Specifications](references/screen-specs.md)
- [SenseCraft HMI service](https://sensecraft.seeed.cc/hmi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML/CSS/JavaScript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project files, display configuration, token files, image assets, and browser-previewable e-ink web content.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
