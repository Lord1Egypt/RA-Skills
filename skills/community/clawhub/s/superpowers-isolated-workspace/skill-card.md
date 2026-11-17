## Description:

Use when starting feature work that needs isolation from the current workspace; it creates isolated git branches with clean setup and safety verification for OpenClaw environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill at the start of feature work to create a separate feature branch, select or prepare a workspace path, install project dependencies, and verify a clean baseline before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run package-manager and build commands in the current checkout, which may execute project-controlled code.

Mitigation: Use it only in repositories you trust and review dependency or build setup before allowing those commands to run.

Risk: The skill can create branches and alter or commit .gitignore, changing repository state.

Mitigation: Confirm the intended branch and ignore-file changes before proceeding, then inspect git status afterward.

Risk: The skill describes isolation while relying on git branches and workspace selection, which may not provide a fully separate working tree.

Mitigation: Treat it as branch and workspace preparation rather than strong filesystem isolation; use a real separate workspace when that isolation is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/superpowers-isolated-workspace)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with bash command blocks and status-report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository state changes such as branch creation, .gitignore updates, dependency setup, and baseline test execution.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
