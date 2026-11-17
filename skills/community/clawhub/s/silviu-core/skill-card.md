## Description:

Implements Silviu-specific guardrails and runbooks to enforce validation, prevent common errors, and manage browser and GitHub interactions in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unknoownd](https://clawhub.ai/user/unknoownd)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to keep OpenClaw workflows disciplined when validating tasks, attaching a browser tab, and checking GitHub repository availability before audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repo audit preflight commands contact GitHub and may reveal the target repository URL or metadata to GitHub.

Mitigation: Run the preflight only for repositories the operator intends to check, and treat the repository URL as information shared with GitHub.

Risk: Browser attach steps require an active Chrome tab with the OpenClaw Browser Relay intentionally enabled.

Mitigation: Enable the relay only on the intended active tab and verify attached tabs before browser automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unknoownd/skills/silviu-core)
- [Publisher profile](https://clawhub.ai/user/unknoownd)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operational runbooks and guardrails for validation, browser attachment, and repository audit preflight checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
