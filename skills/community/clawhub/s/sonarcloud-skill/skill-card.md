## Description:

Use when a user asks to inspect, triage, close, resolve, false-positive, wontfix, review, measure, or configure SonarCloud or SonarQube project findings and settings across repositories; securely reads the token from environment variables and can auto-read project settings from sonar-project.properties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nick2bad4u](https://clawhub.ai/user/nick2bad4u)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and manage SonarCloud or SonarQube issues, hotspots, measures, quality gates, quality profiles, project settings, and project tags across repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sonar tokens can grant access to project findings, settings, and management actions.

Mitigation: Use environment variables or a secret manager for tokens, and avoid pasting tokens into command arguments, logs, or chat output.

Risk: Project mutation actions can change issue dispositions, hotspot reviews, quality gates, quality profiles, settings, or tags.

Mitigation: Run read-only commands first, use dry-run mode when available, and require explicit approval before applying project changes.

Risk: The raw API fallback can perform actions beyond wrapped commands if used carelessly.

Mitigation: Limit raw API calls to the intended SonarCloud or SonarQube origin and use relative endpoint paths.

Risk: The inspected package references a helper script that was not present in the artifact.

Mitigation: Confirm the helper script is available in the installed skill package before relying on command examples.

## Reference(s):

- [SonarCloud Management Skill on ClawHub](https://clawhub.ai/nick2bad4u/skills/sonarcloud-skill)
- [Server-resolved source repository](https://github.com/Nick2bad4u/SonarCloud-Skill)
- [SonarCloud API origin](https://api.sonarcloud.io)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Sonar API responses and project settings; token values should not be displayed.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
