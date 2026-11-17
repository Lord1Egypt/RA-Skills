## Description:

Legacy verification-guided task discipline that helps structure task claims so they can be checked against evidence, receipts, or review criteria, without emitting receipts, verifying signatures, performing cryptographic checks, proving task completion, or approving execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nutstrut](https://clawhub.ai/user/nutstrut)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, operators, and workflow developers use this skill as a verification gate before important actions such as payments, publishing, messaging, automation steps, or decisions. It asks the agent to compare output against a task specification and return PASS, FAIL, or INDETERMINATE before proceeding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A PASS verdict could be mistaken for authorization to complete an irreversible action.

Mitigation: Keep a separate human approval step for payments, public posting, account changes, and other irreversible actions.

Risk: The skill could be treated as cryptographic proof, receipt verification, or proof of task completion.

Mitigation: Use it as a local workflow guardrail only; use a dedicated verification service for receipts, signatures, or settlement finality.

Risk: Sensitive data could be shared with an optional external verification layer.

Mitigation: Use only the minimum structured information needed for verification and do not send secrets or sensitive content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nutstrut/skills/verified-task)
- [OpenClaw Integration Notes](artifact/references/openclaw-integration.md)
- [Decision Template](artifact/assets/DECISION-TEMPLATE.md)
- [Use Case Examples](artifact/assets/USE-CASE-EXAMPLES.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON verdict object and Markdown decision records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a PASS, FAIL, or INDETERMINATE verdict with a reason and confidence; operator override remains explicit.]

## Skill Version(s):

1.0.8 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
