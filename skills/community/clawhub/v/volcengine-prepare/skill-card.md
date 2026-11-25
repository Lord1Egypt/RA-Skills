## Description:

Analyzes a local project or GitHub repository and recommends ranked Volcengine deployment options before the user chooses an execution path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assess whether a project has a deployable service surface, compare suitable ECS, VKE, and veFaaS paths, and choose CLI or IaC resource management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review coverage is incomplete: one script was only partially analyzed, and permission errors may affect service-availability checks.

Mitigation: Review the partially analyzed script before use and independently verify service availability when permission errors occur.

## Reference(s):

- [Deployment mode heuristics](references/deploy-mode-heuristics.md)
- [Volcengine Prepare on ClawHub](https://clawhub.ai/volc-sdk-team/skills/volcengine-prepare)
- [Publisher profile: volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

## Skill Output:

**Output Type(s):** [Analysis, Deployment guidance, Markdown, Configuration guidance]

**Output Format:** [Concise Markdown analysis with ranked deployment options and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a minimal JSON choice record when a deployment decision needs to persist across steps.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
