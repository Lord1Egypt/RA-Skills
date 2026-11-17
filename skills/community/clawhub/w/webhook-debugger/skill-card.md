## Description:

Test, debug, and inspect webhooks locally. Receive webhooks, inspect payloads, debug integrations, and replay requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxuyaun](https://clawhub.ai/user/chenxuyaun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a local webhook listener, inspect incoming payloads, verify signatures, and replay or forward requests while debugging API and third-party integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Captured webhook requests may contain secrets, payment data, or other sensitive payload contents.

Mitigation: Use test webhook data where possible, avoid capturing production secrets, and clear local history when debugging is complete.

Risk: Replay or forwarding behavior can send captured request contents to an unintended destination.

Mitigation: Double-check every replay or forward target URL before sending captured requests.

Risk: Local request history can retain sensitive webhook data after testing.

Mitigation: Treat stored history as sensitive and clear it when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenxuyaun/skills/webhook-debugger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers local request capture, inspection, replay, forwarding, and history management.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
