## Description:

One-click initialization of an AI-driven unit testing environment for frontend projects, with support for React, Vue, pure TypeScript, and Next.js.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hibehero](https://clawhub.ai/user/hibehero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to initialize and maintain Vitest-based unit testing in frontend projects. It detects the project framework, prepares testing configuration, adds reusable Claude Code test-generation prompts, and can wire project-scoped pre-commit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify a project by adding test dependencies, Vitest setup files, Claude Code command prompts, and a Husky pre-commit hook.

Mitigation: Review the generated files and hook changes before committing or enabling them in repositories that require team approval.

Risk: AI-assisted test generation and repair may produce tests that are incorrect or that hide source-code defects.

Mitigation: Inspect generated tests, review any source-code diagnostics, and rerun the test suite and coverage checks before relying on the results.

## Reference(s):

- [Unit Test Automation ClawHub Page](https://clawhub.ai/hibehero/skills/setup-unit-test)
- [AI Unit Test Generation Rules](artifact/references/gen-unit-test-prompt.md)
- [Test Failure Repair Rules](artifact/references/fix-test-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON detection output, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install development dependencies and write Vitest setup files, Claude Code command prompts, and a Husky pre-commit hook inside the target project.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
