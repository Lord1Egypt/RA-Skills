## Description:

End-to-end runbook for deploying, operating, troubleshooting, and monitoring RAGFlow (runtime ops only).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yitingou](https://clawhub.ai/user/yitingou)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations engineers use this skill to deploy, operate, troubleshoot, monitor, and run safe system-level checks for RAGFlow runtime environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can deploy mutable upstream Docker content, which may change between reviews or differ from a production baseline.

Mitigation: Use a pinned RAGFlow release or commit and inspect Compose files before starting containers.

Risk: Bearer-token checks over weakly constrained HTTP can expose credentials or permit unintended API access.

Mitigation: Prefer HTTPS or loopback-only HTTP, restrict network exposure, and use a low-privilege monitoring API key.

Risk: Scheduled checks or restore steps can embed secrets in local scheduler files or affect persistent data.

Mitigation: Avoid secrets in cron or launchd files and require explicit confirmation before restore or scheduled-task setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yitingou/skills/ragflow-runbook)
- [RAGFlow docs](https://ragflow.io/docs/)
- [RAGFlow upstream repository](https://github.com/infiniflow/ragflow)
- [RAGFlow GitHub issues](https://github.com/infiniflow/ragflow/issues)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown runbook guidance with shell commands, Python helper usage, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime operations only; outputs avoid application-layer content workflows.]

## Skill Version(s):

0.1.4 (source: frontmatter, CHANGELOG, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
