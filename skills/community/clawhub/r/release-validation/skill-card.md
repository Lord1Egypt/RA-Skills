## Description:

Test the latest OpenClaw main commit through an isolated OCM copy or an explicitly approved in-place gateway update, then guide structured release feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw](https://clawhub.ai/user/openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and release testers use this skill to validate OpenClaw release candidates against a selected gateway, capture manual surface feedback, and prepare sanitized campaign reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can ask the agent to run a mutable remote installer through Bash when OCM is missing.

Mitigation: Require explicit human approval before installation; prefer a pinned or independently verified OCM install before using the skill.

Risk: In-place validation can modify a real OpenClaw gateway, including state, plugins, and runtime channel.

Mitigation: Use the isolated OCM copy path when possible; require explicit approval, verified backup or snapshot, dry-run review, and readiness checks before in-place mutation.

Risk: Release feedback may contain local paths, gateway details, identifiers, raw logs, prompts, responses, tool payloads, or credentials.

Mitigation: Use the skill's sanitization rules and review gates before posting; keep tooling packets private unless the user separately chooses to report them.

## Reference(s):

- [OpenClaw Release Validation on ClawHub](https://clawhub.ai/openclaw/skills/release-validation)
- [OpenClaw maturity scorecard](https://docs.openclaw.ai/maturity/scorecard.md)
- [Structured release report contract](references/structured-report.md)
- [Tooling-feedback packet procedure](references/tooling-feedback.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown worksheets and reports, JSON campaign artifacts, shell commands, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes private redacted tooling-feedback packets only when setup, build, backup, OCM, or cleanup tooling fails.]

## Skill Version(s):

0.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
