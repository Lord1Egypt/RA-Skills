## Description:

Validate PDFs against PDF/UA-1 using ua1.dev or api.ua1.dev from AI coding agents (OpenClaw, Claude Code, Codex, OpenCode). Use when an agent needs deterministic accessibility checks, compact machine-readable verdicts, CI gating, or structured remediation loops for PDF files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hajekt2](https://clawhub.ai/user/hajekt2)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run deterministic PDF/UA-1 validation from agent workflows, CI gates, or remediation loops. It helps capture compact validation verdicts, group failed findings by rule, and rerun checks after fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected local PDFs to the default UA1 validation service or to an endpoint configured with UA1_API_BASE.

Mitigation: Use it only with PDFs approved for that service or configured endpoint, and avoid confidential, regulated, or credential-bearing files unless the endpoint and environment settings have been reviewed.

## Reference(s):

- [UA1 API health endpoint](https://api.ua1.dev/api/health)
- [UA1 API validation endpoint](https://api.ua1.dev/api/validate)
- [UA1 compact validation endpoint](https://api.ua1.dev/api/validate?format=compact)
- [ClawHub skill page](https://clawhub.ai/hajekt2/skills/ua1-validator-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/hajekt2)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON validation responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pass, fail, or transport-error exit codes for CI gating.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
