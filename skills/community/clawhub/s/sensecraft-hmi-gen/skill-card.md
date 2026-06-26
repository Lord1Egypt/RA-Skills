## Description: <br>
Generate artistic, minimalist web content optimized for SenseCraft HMI e-ink displays with AI-assisted layout selection and screen-aware color and resolution guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KillingJacky](https://clawhub.ai/user/KillingJacky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, designers, and SenseCraft HMI users use this skill to generate e-ink-optimized HTML content, collect screen and layout preferences, preview the result locally, and prepare it for display through the SenseCraft HMI HTML widget. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated content is served through a local web server and may be exposed if forwarded to the public internet. <br>
Mitigation: Use access-controlled tunnels or reverse proxies, keep the tokenized URL private, and stop the PM2 service when the display no longer needs access. <br>
Risk: Tokenized preview URLs, local images, or generated page content may reveal private information if shared or published. <br>
Mitigation: Avoid sensitive content in generated pages, keep local image paths and tokenized URLs private, and review content before exposing it through a public tunnel. <br>
Risk: The skill requires Node/npm setup and PM2-managed service operation. <br>
Mitigation: Install and run it only in environments where local Node services are acceptable, and review service logs and lifecycle commands before use. <br>


## Reference(s): <br>
- [SenseCraft HMI Web Content Generator on ClawHub](https://clawhub.ai/KillingJacky/sensecraft-hmi-gen) <br>
- [SenseCraft HMI service](https://sensecraft.seeed.cc/hmi) <br>
- [E-Ink Design Patterns](references/design-patterns.md) <br>
- [E-Ink Layout Templates](references/layouts.md) <br>
- [SenseCraft HMI Screen Specifications](references/screen-specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated HTML/CSS/JavaScript, local configuration JSON, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated pages are intended to match selected e-ink display dimensions and color capabilities.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
