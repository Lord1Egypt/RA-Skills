## Description:

Creates and manages price alerts that notify users when token prices move above or below target values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liji3597](https://clawhub.ai/user/liji3597)

### License/Terms of Use:


## Use Case:

External users use this skill to create, review, delete, and manually check Solana token price alerts, including above-threshold, below-threshold, stop-loss, and take-profit alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Important alert behavior depends on shared modules outside the skill artifact.

Mitigation: Install only in a controlled OpenClaw deployment where the shared modules are trusted, versioned, and permissioned.

Risk: Global alert checking can process alerts across users.

Mitigation: Restrict manual or scheduled price checks to an authorized scheduler or system account.

Risk: The skill handles user identifiers and persistent alert records.

Mitigation: Apply the deployment's normal access controls, retention policy, and audit review for user alert data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liji3597/skills/solana-alerts)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and JSON status messages from Node.js command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and SOLANA_NETWORK; uses shared deployment modules for alert storage, formatting, scheduling, and notification behavior.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
