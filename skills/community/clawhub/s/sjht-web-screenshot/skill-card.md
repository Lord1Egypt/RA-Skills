## Description:

Capture screenshots of web pages running on local or remote servers using Puppeteer in headless Chromium, including login-required single-page applications when configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aowind](https://clawhub.ai/user/aowind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to capture repeatable screenshots of public or authenticated web application pages for UI review, documentation, and release evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill weakens browser isolation while capturing pages in headless Chromium.

Mitigation: Run it only against trusted sites in a contained environment.

Risk: The JSON configuration can drive login flows and broad page navigation.

Mitigation: Restrict who can edit capture configs and avoid committing real credentials.

Risk: The storeLogin option can mutate application state directly.

Mitigation: Treat storeLogin as a privileged app-state mutation feature and review its config before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aowind/skills/sjht-web-screenshot)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON configuration examples; generated artifacts are PNG screenshots and result.json metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
