## Description:

Pause your agent for human approval before high-risk actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrchop](https://clawhub.ai/user/mrchop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to pause automated workflows before sensitive actions and wait for a human approver to approve or reject by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval requests send the approver email, action title, optional context, and VetoAPI key to vetoapi.com.

Mitigation: Confirm that this data sharing is acceptable for the workflow, and avoid putting secrets, regulated data, or unnecessary business details in approval context.

Risk: The approval wait can be indefinite because the skill polls until a decision is returned.

Mitigation: Add a timeout, maximum wait period, and failure handling before using the skill in automated production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrchop/skills/veto-approval)
- [VetoAPI API Reference](https://vetoapi.com/docs)
- [Get VetoAPI Key](https://vetoapi.com/get-key)
- [VetoAPI](https://vetoapi.com)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a boolean approval result to the calling agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
