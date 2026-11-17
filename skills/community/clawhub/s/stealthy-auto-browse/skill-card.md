## Description:

Headless-detection-resistant browser automation in Docker for authorized QA, compatibility testing, and defensive security research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security testers use this skill to exercise anti-bot behavior, browser compatibility, and authorized security tests on sites they own or have written permission to assess.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags the mutable `latest` container image as a medium-confidence supply-chain risk; some reference checks were incomplete.

Mitigation: Review the setup guidance and use only a container image version whose identity has been verified. Be cautious with credentials, browser sessions, and writable host folders.

Risk: Without `AUTH_TOKEN`, anyone who can reach the browser API can control the browser and its session.

Mitigation: Bind the API to localhost or an authenticating proxy, set `AUTH_TOKEN` for non-localhost deployments, and keep the noVNC viewer private.

Risk: Browser actions can capture page content and may automatically accept dialogs that trigger state changes.

Mitigation: Use only authorized targets, limit capture to test needs, and disable dialog auto-accept before actions on stateful sites.

## Reference(s):

- [Setup guide](references/setup.md)
- [Project homepage](https://github.com/psyb0t/docker-stealthy-auto-browse)
- [Humanized input API reference](https://github.com/psyb0t/docker-stealthy-auto-browse/blob/main/docs/api.md#humanized-input)
- [Script mode control flow](https://github.com/psyb0t/docker-stealthy-auto-browse/blob/main/docs/script-mode.md#control-flow)
- [ClawHub release page](https://clawhub.ai/psyb0t/skills/stealthy-auto-browse)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Screenshots, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON browser responses, extracted page text or DOM data, screenshots, files, and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected browser action and the authorized test target.]

## Skill Version(s):

3.6.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
