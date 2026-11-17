## Description:

WeChat Mini Program automation testing toolkit. Supports launching DevTools, page navigation, element interaction, screenshots, console log reading, and more. Use when the user needs to automate mini program testing, control WeChat DevTools, read console logs, or perform UI screenshot comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eumenides-k](https://clawhub.ai/user/eumenides-k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to automate WeChat Mini Program testing through WeChat DevTools, including navigation, element interaction, screenshots, console log review, performance monitoring, and UI regression checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local automation code has unsafe execution and data-handling issues.

Mitigation: Install and run the skill only in a controlled development environment with test data, and review the automation code before installation.

Risk: A WebSocket endpoint can connect the automation runner to WeChat DevTools.

Mitigation: Restrict the endpoint to localhost and avoid untrusted endpoint values.

Risk: Screenshots, exported reports, WXML/page data, form inputs, and system information may contain sensitive information.

Mitigation: Treat generated artifacts and extracted runtime data as sensitive before storing or sharing them.

Risk: The skill depends on the external miniprogram-automator npm package.

Mitigation: Pin the dependency locally before use in a controlled testing environment.

## Reference(s):

- [WeChat Mini Program Automation Testing API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, markdown, json]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated test artifacts may include screenshots, JSON reports, and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local test scripts, screenshots, console log exports, and UI regression reports in the user's workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
