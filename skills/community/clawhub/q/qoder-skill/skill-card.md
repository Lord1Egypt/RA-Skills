## Description:

Qoder Skill integrates Alibaba Cloud Qoder for AI-assisted code generation, refactoring, documentation generation, SPEC-driven development, testing, and codebase analysis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frisky1985](https://clawhub.ai/user/frisky1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to invoke Qoder for code generation, refactoring, documentation, tests, SPEC-driven development, and codebase analysis in a local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Qoder CLI can access prompts, source files, directories, and environment variables from the agent session.

Mitigation: Use the skill only in a controlled workspace after reviewing intended file access and trusting both the local qoder binary and Alibaba Cloud/Qoder service.

Risk: API keys and service configuration may be exposed if stored loosely in the workspace or shell environment.

Mitigation: Store Qoder credentials with restrictive permissions or in a secret manager, and avoid committing configuration files that contain secrets.

Risk: Examples include email analysis and reporting, which may process sensitive communications.

Mitigation: Do not use the email-analysis or reporting examples on sensitive communications unless data handling, access control, and review requirements are satisfied.

Risk: Generated or refactored code may be incorrect, insecure, or broader than intended.

Mitigation: Review generated changes before merging, and run normal tests, code review, and security checks for affected code.

## Reference(s):

- [Qoder official documentation](https://help.aliyun.com/product/qoder)
- [Qoder configuration reference](references/qoder_config.md)
- [Qoder usage examples](references/examples.md)
- [ClawHub Qoder Skill page](https://clawhub.ai/frisky1985/skills/qoder-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, generated code or files, configuration snippets, and structured command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a local Qoder CLI and external Alibaba Cloud/Qoder service using workspace files, prompts, directories, and environment variables available to the session.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
