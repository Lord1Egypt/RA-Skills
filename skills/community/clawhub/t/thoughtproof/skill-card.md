## Description:

ThoughtProof verifies AI reasoning, detects blind spots, and builds consensus across multiple model families.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thoughtproof](https://clawhub.ai/user/thoughtproof)

### License/Terms of Use:

MIT; Business Source License for the consensus protocol

## Use Case:

Developers, engineers, and decision makers use ThoughtProof to get second opinions on AI outputs, compare independent model proposals, surface blind spots, and preserve a local audit trail for decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned global third-party CLI that may change behavior or receive unsafe updates.

Mitigation: Pin and review the pot-cli version where possible, scan it before installation, and do not run it with elevated privileges.

Risk: Verification prompts and chained prior context can be sent to multiple model providers.

Mitigation: Redact confidential legal, medical, financial, business, and personal information before verification or context chaining.

Risk: Consensus output can still be incorrect or misleading, especially for high-stakes decisions.

Mitigation: Treat the output as decision support, require human review, and validate important conclusions against independent evidence.

## Reference(s):

- [Epistemic Block Format](references/block-format.md)
- [Consensus Protocol](references/consensus-protocol.md)
- [ThoughtProof website](https://thoughtproof.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown-style CLI output and locally stored JSON epistemic blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification blocks can include proposals, critique, synthesis, confidence scores, dissent, action items, and Model Diversity Index metrics.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
