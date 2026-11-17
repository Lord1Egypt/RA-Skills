## Description:

Spin up a remote browser session via the TinyFish Browser API and get a CDP URL for driving it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bunsdev](https://clawhub.ai/user/bunsdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create hosted Chromium sessions for browser automation with Playwright, Puppeteer, or other DevTools Protocol clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs and browser activity are sent to TinyFish as a third-party hosted browser provider.

Mitigation: Use the skill only when TinyFish is approved for the data and sites being automated.

Risk: The TinyFish API key may be exposed if it is broadly scoped or visible in process arguments.

Mitigation: Scope and rotate TINYFISH_API_KEY, restrict environment access, and harden the helper before handling sensitive workflows.

## Reference(s):

- [TinyFish Browser API documentation](https://docs.tinyfish.ai/browser-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash command examples and JSON response shape]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TINYFISH_API_KEY; TinyFish returns session_id, cdp_url, and an authenticated base_url.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
