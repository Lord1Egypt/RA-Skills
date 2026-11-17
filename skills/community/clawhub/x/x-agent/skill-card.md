## Description:

Plan and run X (Twitter) operations in three modes: monitor-only intelligence, draft-and-approve posting, and limited automation with strict guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inceptivco](https://clawhub.ai/user/inceptivco)

### License/Terms of Use:


## Use Case:

External users and operators use this skill to plan X account workflows, monitor topics and accounts, draft posts or replies for approval, and run tightly limited automation after guardrails are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting or reply automation may exceed the intended scope if limits are not defined before access is granted.

Mitigation: Start in monitor-only or draft-and-approve mode, then enable limited automation only for pre-approved playbooks with max posts per day, max replies per hour, quiet hours, and a named kill switch owner.

Risk: X credentials could be exposed if they are pasted into chat or stored in shared prompts.

Mitigation: Keep credentials out of chat and configure API credentials only in the local environment before granting posting access.

Risk: Generated posts may contain unverifiable claims or restricted legal, medical, financial, or political content.

Mitigation: Require draft review with risk flags and confidence levels, block restricted categories unless explicitly allowed, and keep approval gates before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inceptivco/skills/x-agent)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces monitor briefs, draft packages, and automation reports with risk flags, approval status, limits, skipped actions, and policy blocks.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
