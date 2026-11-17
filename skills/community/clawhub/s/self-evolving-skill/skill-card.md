## Description:

Meta-cognitive self-learning system - Automated skill evolution based on predictive coding and value-driven mechanisms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whtoo](https://clawhub.ai/user/whtoo)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to create, execute, analyze, list, save, and load adaptive OpenClaw skills through CLI, TypeScript, and MCP-style tool interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked the release suspicious because local storage and runtime behavior are inconsistent and tool inputs may be logged.

Mitigation: Review the configured storage directory before use, avoid passing secrets or personal data in execution context, and prefer a release with clear retention, deletion, and log redaction controls.

Risk: The skill stores learning data locally and may receive arbitrary task context.

Mitigation: Run it in a scoped workspace, limit context to non-sensitive task data, and review stored data before sharing or redeploying the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whtoo/skills/self-evolving-skill)
- [Publisher Profile](https://clawhub.ai/user/whtoo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON tool responses, TypeScript API calls, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist skill and execution data to local filesystem storage.]

## Skill Version(s):

1.0.2 (source: package.json, openclaw.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
