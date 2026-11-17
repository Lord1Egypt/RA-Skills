## Description:

Build an urgent return action sheet for items with deadlines, packing needs, proof, route order, and a final checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Busy shoppers, households, and assistants use this skill to triage expiring product returns, gather proof, prepare packages or labels, and create a grounded route or batch plan before return windows close.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share shopping and return details such as order numbers, labels, receipts, and item locations.

Mitigation: Provide only the details needed for planning and redact unnecessary personal data before sharing receipts, labels, or paperwork.

Risk: Store policies, deadlines, fees, eligibility, and return methods can vary or change.

Mitigation: Independently verify each policy and deadline with the store or seller before acting on the plan.

Risk: Route or batch suggestions may be unreliable if locations, hours, appointments, or constraints are missing.

Mitigation: Use only user-provided locations and constraints; when geography is unclear, produce a logical batch order instead of a fastest-route claim.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/harrylabsj/skills/return-window-rescue-planner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown action sheet with triage lists, an inventory table or bullets, route or batch order, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only output; no code execution, network access, credentials, account access, files, or websites are required.]

## Skill Version(s):

1.0.1 (source: skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
