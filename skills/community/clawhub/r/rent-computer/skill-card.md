## Description:

Helps users request a computer rental when their computer lacks sufficient performance or they want to rent a high-performance computer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyyinfo](https://clawhub.ai/user/cyyinfo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review rentable computer or GPU server options and submit a rental request with their address, contact method, and requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can route vague performance complaints into a rental process.

Mitigation: Use this skill only when the user explicitly asks to rent a computer, GPU server, or similar resource.

Risk: The workflow collects and submits address and contact details without a clear final consent step.

Mitigation: Before submission, show the destination service, address, contact method, and message, then ask the user to confirm.

Risk: Users may include unrelated sensitive information in the rental message.

Mitigation: Tell users their details will be sent to zhiweisoft.com and ask them to omit unrelated sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyyinfo/skills/rent-computer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text conversation with structured rental request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May collect address, contact method, and rental requirements before submitting a request.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
