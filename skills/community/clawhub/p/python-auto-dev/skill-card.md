## Description:

Automates Python code generation, test creation, test execution, debugging guidance, and optimization reporting for a configured Windows conda environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptjason](https://clawhub.ai/user/aptjason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold Python code, generate tests, run pytest, inspect failures, and produce optimization reports within a configured local conda workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated source, tests, and profiling runs may execute unintended code in the configured workspace.

Mitigation: Run the skill only in a disposable or tightly scoped workspace with non-sensitive environment variables, and review generated source before test or profile execution.

Risk: Unsafe command and source generation paths can make untrusted specs, filenames, paths, or code risky to process.

Mitigation: Avoid untrusted inputs until command invocation and generated-source handling are fixed; validate paths and commands before execution.

Risk: Unpinned dependencies and local conda assumptions can produce inconsistent or unexpected behavior.

Mitigation: Pin dependencies and confirm the expected Windows conda path, environment, and project directory before use.

## Reference(s):

- [Script Usage Guide](references/script-usage.md)
- [ClawHub Skill Page](https://clawhub.ai/aptjason/skills/python-auto-dev)
- [Publisher Profile](https://clawhub.ai/user/aptjason)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with generated Python files, JSON reports, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated code, tests, reports, profile data, and debugging guidance to configured local paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
