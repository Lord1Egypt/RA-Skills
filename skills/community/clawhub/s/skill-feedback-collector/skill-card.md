## Description:

Human-in-the-loop MCP feedback collector that pauses agent work for browser-based feedback and can auto-dequeue queued tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2019-02-18](https://clawhub.ai/user/2019-02-18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to pause automated work for human confirmation, collect browser-based feedback, and continue through queued tasks when a workflow needs interactive review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default browser control panel can expose feedback history and controls to clients that can reach the service.

Mitigation: Run it only on localhost or a trusted, firewalled network, and set a strong FEEDBACK_TOKEN for shared or public deployments.

Risk: Feedback and queued tasks may contain sensitive information and are persisted locally.

Mitigation: Avoid placing secrets in feedback, and regularly review or clear feedback-history.json.

Risk: Queued browser or API tasks can steer subsequent agent work.

Mitigation: Apply the agent's normal safety, review, and confirmation rules to queued tasks before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2019-02-18/skills/skill-feedback-collector)
- [Publisher profile](https://clawhub.ai/user/2019-02-18)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Plain text MCP tool responses with setup guidance in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return human feedback text or an auto-dequeued task; local conversation history is retained up to 500 entries.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
