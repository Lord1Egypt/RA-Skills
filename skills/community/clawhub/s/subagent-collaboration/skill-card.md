## Description:

Subagent Collaboration helps OpenClaw users analyze available subagents, choose collaboration patterns, generate multi-agent workflow designs, and run safety checks for subagent configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanlinsec-sys](https://clawhub.ai/user/nanlinsec-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and generate OpenClaw multi-subagent workflows for analysis, software delivery, consultation, relay, and workflow orchestration tasks. It also provides configuration analysis, model and concurrency recommendations, and safety-check reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated executable JavaScript may be affected by untrusted task text.

Mitigation: Avoid untrusted task descriptions and review generated .js files before running them.

Risk: The skill can write generated files to broad or hard-coded local paths.

Mitigation: Pass an explicit output directory and verify generated output paths before execution.

Risk: Security evidence marks the release suspicious because local file generation and generated code execution require operator review.

Mitigation: Use the security-check report as a pre-execution review step and accept the skill only in environments where local file generation is permitted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nanlinsec-sys/skills/subagent-collaboration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON workflow files, JavaScript code snippets, shell commands, and security-check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and node; generated workflow and JavaScript files should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
