## Description:

Helps developers create and integrate WorkoPilot AI capabilities into business systems, including AI services, digital employees, iframe skill cards, attachment classification, API examples, integration plans, and troubleshooting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workopilot](https://clawhub.ai/user/workopilot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to plan, configure, test, and troubleshoot WorkoPilot AI services, digital employees, iframe integrations, document extraction, and related API workflows for business applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through credential and configuration handling for WorkoPilot integrations.

Mitigation: Use a dedicated .env.workopilot file or a secret manager, avoid command-line API keys, and keep API keys out of frontend code and source control.

Risk: Authenticated requests may be sent to an unintended WorkoPilot host if configuration is wrong.

Mitigation: Verify the resolved WorkoPilot base URL before making authenticated API requests, especially when switching between production and test endpoints.

Risk: Generated setup steps may modify project configuration or create WorkoPilot resources beyond the user's intended scope.

Mitigation: Require explicit confirmation before changing unrelated project configuration files or creating, updating, or reusing WorkoPilot resources.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/workopilot/workopilot.skills/tree/main/skills/workopilot-service-builder)
- [ClawHub skill page](https://clawhub.ai/workopilot/skills/workopilot-service-builder)
- [WorkoPilot API endpoint](https://agent.workopilot.com/net-api)
- [WorkoPilot test API endpoint](https://agenttest.workopilot.com/net-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, JSON examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoints, environment variable names, integration identifiers, validation steps, and troubleshooting notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
