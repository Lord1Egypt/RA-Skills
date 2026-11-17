## Description:

Outputs a corresponding Chinese poem based on the user's selected option: input A returns Yong Liu, input B returns Chun Xiao, and results are written to /workspace/assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luokeer52](https://clawhub.ai/user/luokeer52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to route a simple A/B selection to a poem result and save the result under /workspace/assets. Review is recommended because the packaged behavior also operates as an authenticated remote-service client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill presents as a simple poem selector but operates as an authenticated remote-service client with credential use, network forwarding, payment-history access, and persistent session state.

Mitigation: Review before installation; restrict endpoints, credentials, and session persistence, and require an explicit privacy notice before use.

Risk: The security guidance warns against installing this as a simple poem utility without review.

Mitigation: Rewrite the poem selection locally or republish the skill with an accurate remote-client purpose, safer credential handling, pinned dependencies, and opt-in session persistence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luokeer52/skills/test-txt)
- [Publisher profile](https://clawhub.ai/user/luokeer52)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Plain text or JSON responses surfaced from the remote service, with setup instructions in Markdown and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save results to /workspace/assets and may return purchase-history URLs or full JSON envelopes when content is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
