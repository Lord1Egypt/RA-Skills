## Description:

Use when needing to interact with Jenkins CI/CD via REST API - triggering builds, listing projects, or checking build results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lentiancn](https://clawhub.ai/user/lentiancn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to manage Jenkins project configuration, trigger builds, and check build results through guided REST API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send Jenkins credentials to project-configured URLs without validating or clearly confirming the destination first.

Mitigation: Use only trusted PROJECTS.md entries, HTTPS-only Jenkins URLs, a host allowlist or explicit host confirmation, and least-privileged Jenkins API tokens.

Risk: Broad auto-invocation for generic words such as build can trigger Jenkins workflows in the wrong project context.

Mitigation: Require explicit project and destination confirmation before authenticated Jenkins requests or build triggers.

Risk: PROJECTS.md changes can alter where authenticated Jenkins requests are sent.

Mitigation: Treat PROJECTS.md edits as security-sensitive configuration changes and review them before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lentiancn/skills/skill-jenkins)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Jenkins credentials in JENKINS_USER and JENKINS_API_TOKEN, with Jenkins URLs configured per project in PROJECTS.md.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
