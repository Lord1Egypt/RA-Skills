## Description:

Build automation workflows and internal tools with Windmill's code-first platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill as concise guidance for building Windmill scripts, flows, schedules, secrets, self-hosted deployments, and webhook-triggered internal tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Windmill workflows created from this guidance may expose webhook-triggered automation without authentication.

Mitigation: Validate tokens in script logic or place webhook endpoints behind an authenticated reverse proxy.

Risk: Sensitive values may be exposed if users store secrets as plaintext Windmill variables.

Mitigation: Use Windmill secrets for sensitive data and avoid placing credentials in visible variables.

Risk: Scheduled or suspended flows may run at unexpected times, overlap, or wait indefinitely.

Mitigation: Set explicit timezones, mutex locks, and suspend-step timeouts when building production workflows.

Risk: Generated scripts and flows may fail if type signatures, return values, dependencies, or branch result references are incorrect.

Mitigation: Test scripts individually, verify flow branches, and review dependencies before deploying workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with concise operational notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code or external tool calls are included in the skill package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
