## Description:

Provides Docker-based browser automation with Camoufox, OS-level input, and persistent fingerprints for authorized QA, compatibility testing, and defensive security research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use the skill to test anti-bot behavior, browser compatibility, and detection systems on sites they own or are authorized to assess.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The mutable `latest` container image can change between installations.

Mitigation: Review image updates and pin a verified version or digest for repeatable deployments.

Risk: Without API authentication, anyone who can reach the browser service can control it and access its sessions.

Mitigation: Set `AUTH_TOKEN` and bind published ports to loopback or place the service behind an authenticating proxy.

Risk: Browser dialogs auto-accept by default and may confirm destructive actions.

Mitigation: Call `handle_dialog` with `accept: false` before each stateful step that could raise a dialog, and use only dedicated test accounts.

Risk: Persistent profiles and optional CAPTCHA extensions can expose session data across pages.

Mitigation: Use isolated test profiles, protect `/userdata`, and remove profile data when testing ends.

## Reference(s):

- [Setup and configuration](references/setup.md)
- [HTTP API reference](https://psyb0t.github.io/docker-stealthy-auto-browse/api/)
- [Humanized input reference](https://psyb0t.github.io/docker-auto-linux-desk/humanized-input/)
- [Script mode control flow](https://psyb0t.github.io/docker-stealthy-auto-browse/script-mode/#control-flow)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Screenshots, Guidance]

**Output Format:** [JSON API requests and responses, extracted page text or HTML, screenshots, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser output depends on the authorized target and requested action.]

## Skill Version(s):

3.9.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
