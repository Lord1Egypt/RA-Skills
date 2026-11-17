## Description:

Detects feature drift in tabular ML models using Superwise Compare Distribution policies, manages Superwise dataset and drift policy setup, ingests inference records, and sends Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mark-stadtmueller](https://clawhub.ai/user/mark-stadtmueller)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to add scheduled drift checks for tabular models, compare inference distributions against a training baseline in Superwise, and receive operational alerts when drift is detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The production scheduler exposes an unauthenticated /run-check endpoint that can trigger repeated Superwise uploads, policy actions, and Telegram alerts.

Mitigation: Add authentication to /run-check, prefer POST, rate limit requests, and enforce a single-run lock before deploying the scheduler publicly.

Risk: The skill sends model inference data to Superwise and depends on a configured inference endpoint.

Mitigation: Use only trusted Superwise accounts and trusted inference endpoints, and confirm the data is approved for third-party processing before running the skill.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Pin production dependency versions before deploying the scheduled drift detection service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mark-stadtmueller/skills/superwise-drift-detection-skill)
- [Superwise API and guides](https://docs.superwise.ai/mcp)
- [Superwise Python SDK reference](https://mcp.sdk.docs.superwise.ai/mcp)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, Python setup scripts, and environment configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through credential setup, dataset creation, policy creation, drift checks, scheduling, and alert configuration.]

## Skill Version(s):

1.0.5 (source: server release metadata and skill.py metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
