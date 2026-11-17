## Description:

Analyzes self-hosted SonarQube projects, retrieves filtered issues, checks Quality Gate status, and suggests remediation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipeoff](https://clawhub.ai/user/felipeoff)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to inspect SonarQube findings for projects or pull requests, summarize issue severity, and receive suggested next steps before merging or releasing code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to a SonarQube instance and authentication token.

Mitigation: Use a dedicated least-privileged token, store it in protected environment or secret storage, and avoid committing it in openclaw.json.

Risk: Using HTTP or an untrusted network path can expose SonarQube traffic or credentials.

Mitigation: Use HTTPS for any non-local SonarQube server and restrict network access to trusted environments.

Risk: Suggested fixes may not be appropriate for every codebase or rule context.

Mitigation: Review remediation suggestions manually and run lint, typecheck, and tests before accepting changes.

Risk: Unpinned npx or global installs can pull a different package version later.

Mitigation: Pin the npm package version in CI and automation workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felipeoff/skills/sonarqube-analyzer)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown, and CLI text summaries with remediation guidance and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SonarQube server URL, authentication token, and project key; pull request, severity, limit, action, and output format are optional.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
