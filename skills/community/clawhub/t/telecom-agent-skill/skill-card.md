## Description:

Turn your AI Agent into a Telecom Operator. Bulk calling, ChatOps, and Field Monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kflohr](https://clawhub.ai/user/kflohr)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent manage telecom campaigns, request approvals, monitor call progress, and retrieve call transcripts through a telecom operator console.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger bulk calling and public telephone network actions.

Mitigation: Use a pinned and reviewed release, require explicit human approval for campaigns and calls, and configure spending, rate, and destination controls before use.

Risk: The skill can record calls and expose transcripts.

Mitigation: Confirm recording consent, transcript retention, and access-control policies before using it with real callers or customer data.

Risk: The skill requires telecom provider onboarding and credentials.

Mitigation: Limit Twilio credential scope and rotate or revoke credentials if the skill behavior or release provenance cannot be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kflohr/skills/telecom-agent-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and JSON status examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve Twilio onboarding, campaign approvals, call recording, transcript retrieval, and remote monitoring workflows.]

## Skill Version(s):

0.1.5 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
